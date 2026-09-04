import importlib

import pytest

from user_scanner.core.result import Result


def test_pdf_media_rejects_private_ip_before_network(monkeypatch):
    import user_scanner.core.pdf_generator as pdf_gen

    calls = []
    monkeypatch.setattr(pdf_gen, "PIL_AVAILABLE", True)
    monkeypatch.setattr(
        pdf_gen.httpx,
        "get",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    if hasattr(pdf_gen.httpx, "stream"):
        monkeypatch.setattr(
            pdf_gen.httpx,
            "stream",
            lambda *args, **kwargs: calls.append((args, kwargs)),
        )

    assert pdf_gen.fetch_and_resize_image("https://127.0.0.1/avatar.png") is None
    assert calls == []


def test_pdf_media_rejects_hostname_resolving_private_before_network(monkeypatch):
    import user_scanner.core.pdf_generator as pdf_gen

    calls = []
    monkeypatch.setattr(pdf_gen, "PIL_AVAILABLE", True)
    monkeypatch.setattr(
        pdf_gen.socket,
        "getaddrinfo",
        lambda *args, **kwargs: [(2, 1, 6, "", ("127.0.0.1", 443))],
        raising=False,
    )
    monkeypatch.setattr(
        pdf_gen.httpx,
        "get",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    if hasattr(pdf_gen.httpx, "stream"):
        monkeypatch.setattr(
            pdf_gen.httpx,
            "stream",
            lambda *args, **kwargs: calls.append((args, kwargs)),
        )

    assert pdf_gen.fetch_and_resize_image("https://media.example.test/avatar.png") is None
    assert calls == []


def test_pdf_media_rejects_declared_oversize_before_body_read(monkeypatch):
    import user_scanner.core.pdf_generator as pdf_gen

    class LegacyResponse:
        status_code = 200
        headers = {"content-type": "image/png", "content-length": str(9 * 1024 * 1024)}
        content_accessed = False

        @property
        def content(self):
            self.content_accessed = True
            return b"not-an-image"

    class StreamResponse:
        status_code = 200
        headers = {"content-type": "image/png", "content-length": str(9 * 1024 * 1024)}
        iterated = False

        def iter_bytes(self):
            self.iterated = True
            yield b"x"

    class StreamContext:
        def __init__(self, response):
            self.response = response

        def __enter__(self):
            return self.response

        def __exit__(self, exc_type, exc, tb):
            return False

    legacy = LegacyResponse()
    streamed = StreamResponse()
    monkeypatch.setattr(pdf_gen, "PIL_AVAILABLE", True)
    monkeypatch.setattr(pdf_gen.httpx, "get", lambda *args, **kwargs: legacy)
    monkeypatch.setattr(pdf_gen.httpx, "stream", lambda *args, **kwargs: StreamContext(streamed))
    monkeypatch.setattr(pdf_gen.socket, "getaddrinfo", lambda *args, **kwargs: [(2, 1, 6, "", ("203.0.113.10", 443))], raising=False)

    assert pdf_gen.fetch_and_resize_image("https://media.example.test/avatar.png") is None
    assert legacy.content_accessed is False
    assert streamed.iterated is False


@pytest.mark.anyio
@pytest.mark.parametrize(
    "field,value",
    [
        ("concurrency", 0),
        ("concurrency", 101),
        ("timeout", 0),
        ("timeout", 121),
        ("cross_depth", 0),
        ("cross_depth", 6),
        ("cross_sweep", -1),
        ("cross_sweep", 21),
    ],
)
async def test_mcp_rejects_out_of_range_scan_controls(monkeypatch, field, value):
    import user_scanner.mcp.handlers as handlers

    monkeypatch.setattr(handlers, "_run_scan", lambda *args, **kwargs: [Result.available()])
    monkeypatch.setattr(handlers, "run_cross_scan", lambda *args, **kwargs: [])
    arguments = {"username": "testuser", field: value}
    if field.startswith("cross_"):
        arguments["cross_scan"] = True

    with pytest.raises(ValueError, match=field):
        await handlers.execute_scan(arguments, is_email=False)


def test_email_orchestrator_import_does_not_patch_httpx_initializers():
    import httpx
    import user_scanner.core.email_orchestrator as email_orchestrator

    original_client = getattr(email_orchestrator, "_original_client_init", httpx.Client.__init__)
    original_async = getattr(email_orchestrator, "_original_async_client_init", httpx.AsyncClient.__init__)
    httpx.Client.__init__ = original_client
    httpx.AsyncClient.__init__ = original_async
    before_client = httpx.Client.__init__
    before_async = httpx.AsyncClient.__init__

    try:
        importlib.reload(email_orchestrator)
        assert httpx.Client.__init__ is before_client
        assert httpx.AsyncClient.__init__ is before_async
    finally:
        httpx.Client.__init__ = original_client
        httpx.AsyncClient.__init__ = original_async


def test_updater_uses_atomic_upgrade_and_reports_success(monkeypatch):
    import user_scanner.utils.update as update_mod

    calls = []
    monkeypatch.setattr(update_mod.subprocess, "check_call", lambda args: calls.append(args))

    assert update_mod.update_self() is True
    assert calls == [[
        update_mod.sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "user-scanner",
    ]]


def test_updater_reports_failure_without_false_success(monkeypatch, capsys):
    import user_scanner.utils.updater_logic as updater_logic

    monkeypatch.setattr(updater_logic, "load_config", lambda: {"auto_update_status": True})
    monkeypatch.setattr(updater_logic, "get_pypi_version", lambda _url: "9.9.9")
    monkeypatch.setattr(updater_logic, "load_local_version", lambda: ("1.0.0", "local"))
    monkeypatch.setattr(updater_logic, "update_self", lambda: False)
    monkeypatch.setattr("builtins.input", lambda _prompt: "y")

    updater_logic.check_for_updates()
    output = capsys.readouterr().out
    assert "Update successful" not in output
    assert "Update failed" in output


def test_http_client_cache_is_bounded_and_closes_evictions(monkeypatch):
    import user_scanner.core.orchestrator as orchestrator

    class DummyClient:
        def __init__(self, *args, **kwargs):
            self.closed = False

        def close(self):
            self.closed = True

    old_clients = dict(orchestrator._clients)
    orchestrator._clients.clear()
    monkeypatch.setattr(orchestrator.httpx, "Client", DummyClient)

    try:
        created = [orchestrator.get_client(False, f"http://proxy-{i}.example:8080") for i in range(33)]
        assert len(orchestrator._clients) <= 32
        assert any(client.closed for client in created)
    finally:
        orchestrator._clients.clear()
        orchestrator._clients.update(old_clients)
