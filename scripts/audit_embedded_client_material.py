#!/usr/bin/env python3
"""Fail closed on unreviewed credential-shaped literals without printing values."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path


MANIFEST_SCHEMA = "user-scanner/embedded-client-material/v1"
GOOGLE_API_KEY = re.compile(r"AIza[0-9A-Za-z_-]{35}")
SENSITIVE_NAMES = {
    "accesstoken",
    "apikey",
    "apitoken",
    "authorization",
    "authtoken",
    "clientid",
    "clientsecret",
    "xapikey",
    "xshopifystorefrontaccesstoken",
}
ENTRY_KEYS = {"path", "kind", "sha256", "provenance", "review_state"}


def _normalized_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _identity(path: str, kind: str, value: str) -> tuple[str, str, str]:
    return path, kind, hashlib.sha256(value.encode("utf-8")).hexdigest()


def scan_embedded_client_material(root: Path) -> list[dict[str, str | int]]:
    source_root = root / "user_scanner"
    findings: dict[tuple[str, str, str], dict[str, str | int]] = {}

    for path in sorted(source_root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)

        for node in ast.walk(tree):
            literal = _literal_string(node)
            if literal is not None:
                for match in GOOGLE_API_KEY.finditer(literal):
                    key = _identity(relative, "google-api-key", match.group(0))
                    findings.setdefault(
                        key,
                        {"path": key[0], "kind": key[1], "sha256": key[2], "line": node.lineno},
                    )

            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                value_node = node.value
                value = _literal_string(value_node)
                if value is None or len(value) < 16 or GOOGLE_API_KEY.search(value):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [target.id for target in targets if isinstance(target, ast.Name)]
                if any(_normalized_name(name) in SENSITIVE_NAMES for name in names):
                    key = _identity(relative, "named-credential-literal", value)
                    findings.setdefault(
                        key,
                        {"path": key[0], "kind": key[1], "sha256": key[2], "line": value_node.lineno},
                    )

            if isinstance(node, ast.Dict):
                for key_node, value_node in zip(node.keys, node.values):
                    field = _literal_string(key_node)
                    value = _literal_string(value_node)
                    if (
                        field is None
                        or value is None
                        or len(value) < 16
                        or GOOGLE_API_KEY.search(value)
                        or _normalized_name(field) not in SENSITIVE_NAMES
                    ):
                        continue
                    key = _identity(relative, "credential-header-or-field", value)
                    findings.setdefault(
                        key,
                        {"path": key[0], "kind": key[1], "sha256": key[2], "line": value_node.lineno},
                    )

    return sorted(findings.values(), key=lambda item: (str(item["path"]), str(item["kind"]), str(item["sha256"])))


def audit_embedded_client_material(root: Path, manifest_path: Path) -> list[str]:
    failures: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"embedded client material manifest is unreadable: {exc}"]

    if not isinstance(manifest, dict) or manifest.get("schema") != MANIFEST_SCHEMA:
        return ["embedded client material manifest has an unsupported schema"]
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return ["embedded client material manifest entries must be a list"]

    reviewed: set[tuple[str, str, str]] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            failures.append(f"manifest entry {index} has an invalid closed shape")
            continue
        if entry.get("provenance") != "inherited-upstream":
            failures.append(f"manifest entry {index} has invalid provenance")
        if entry.get("review_state") != "unverified-client-material":
            failures.append(f"manifest entry {index} has invalid review state")
        digest = entry.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            failures.append(f"manifest entry {index} has an invalid SHA-256 fingerprint")
            continue
        identity = (entry.get("path"), entry.get("kind"), digest)
        if not all(isinstance(value, str) for value in identity):
            failures.append(f"manifest entry {index} has invalid identity fields")
        elif identity in reviewed:
            failures.append(f"manifest entry {index} duplicates a reviewed fingerprint")
        else:
            reviewed.add(identity)

    detected = scan_embedded_client_material(root)
    detected_identities = {
        (str(item["path"]), str(item["kind"]), str(item["sha256"])) for item in detected
    }
    for item in detected:
        identity = (str(item["path"]), str(item["kind"]), str(item["sha256"]))
        if identity not in reviewed:
            failures.append(
                f"unreviewed embedded client material: {item['path']}:{item['line']} "
                f"{item['kind']} sha256={item['sha256']}"
            )
    for path, kind, digest in sorted(reviewed - detected_identities):
        failures.append(f"stale embedded client material review: {path} {kind} sha256={digest}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("security/embedded-client-material.json"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    failures = audit_embedded_client_material(root, manifest)
    if failures:
        print("embedded client material audit: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"embedded client material audit: PASS ({len(scan_embedded_client_material(root))} reviewed fingerprints)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
