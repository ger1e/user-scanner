import ipaddress
import socket
from typing import Callable, Iterable
from urllib.parse import urljoin, urlsplit

import httpx


MAX_MEDIA_BYTES = 8 * 1024 * 1024
MAX_MEDIA_REDIRECTS = 3
_REDIRECT_STATUSES = {301, 302, 303, 307, 308}
_MEDIA_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    )
}


def _is_public_ip(value: str) -> bool:
    try:
        return ipaddress.ip_address(value).is_global
    except ValueError:
        return False


def _resolved_addresses(info: Iterable[tuple]) -> set[str]:
    addresses: set[str] = set()
    for row in info:
        try:
            sockaddr = row[4]
            addresses.add(str(sockaddr[0]))
        except (IndexError, TypeError):
            continue
    return addresses


def is_safe_media_url(
    url: str,
    *,
    resolver: Callable[..., Iterable[tuple]] = socket.getaddrinfo,
) -> bool:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except (TypeError, ValueError):
        return False

    if parsed.scheme.lower() != "https" or not parsed.hostname:
        return False
    if parsed.username or parsed.password:
        return False
    if port not in (None, 443):
        return False

    hostname = parsed.hostname.rstrip(".")
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        literal = None

    if literal is not None:
        return literal.is_global

    try:
        info = resolver(hostname, 443, type=socket.SOCK_STREAM)
    except (OSError, socket.gaierror):
        return False

    addresses = _resolved_addresses(info)
    return bool(addresses) and all(_is_public_ip(address) for address in addresses)


def _header(headers, name: str) -> str:
    if headers is None:
        return ""
    value = headers.get(name)
    if value is None:
        value = headers.get(name.lower())
    return "" if value is None else str(value)


def fetch_media_bytes(
    url: str,
    *,
    timeout: float = 5.0,
    max_bytes: int = MAX_MEDIA_BYTES,
    max_redirects: int = MAX_MEDIA_REDIRECTS,
    resolver: Callable[..., Iterable[tuple]] = socket.getaddrinfo,
    httpx_module=httpx,
) -> tuple[bytes, str, str] | None:
    current = url

    for _ in range(max_redirects + 1):
        if not is_safe_media_url(current, resolver=resolver):
            return None

        try:
            with httpx_module.stream(
                "GET",
                current,
                headers=_MEDIA_HEADERS,
                timeout=timeout,
                follow_redirects=False,
                trust_env=False,
            ) as response:
                if response.status_code in _REDIRECT_STATUSES:
                    location = _header(response.headers, "location")
                    if not location:
                        return None
                    current = urljoin(current, location)
                    continue

                if response.status_code != 200:
                    return None

                content_type = _header(response.headers, "content-type").split(";", 1)[0].strip().lower()
                if not content_type.startswith("image/"):
                    return None

                declared_text = _header(response.headers, "content-length")
                if declared_text:
                    try:
                        if int(declared_text) > max_bytes:
                            return None
                    except ValueError:
                        return None

                chunks: list[bytes] = []
                total = 0
                for chunk in response.iter_bytes():
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > max_bytes:
                        return None
                    chunks.append(bytes(chunk))

                return b"".join(chunks), content_type, current
        except (httpx.HTTPError, OSError, ValueError):
            return None

    return None
