import json
import tempfile
import unittest
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised by the Python 3.10 CI job
    import tomli as tomllib

from scripts.audit_embedded_client_material import (
    MANIFEST_SCHEMA,
    audit_embedded_client_material,
    scan_embedded_client_material,
)


ROOT = Path(__file__).resolve().parents[1]


class RepositoryGovernanceTests(unittest.TestCase):
    def test_development_toolchain_is_exactly_pinned_and_ci_uses_it(self):
        config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        dev = set(config["project"]["optional-dependencies"]["dev"])
        for requirement in (
            "ruff==0.15.22",
            "mypy==2.3.1",
            "tomli==2.4.1; python_version < '3.11'",
            "types-colorama==0.4.15.20260508",
        ):
            self.assertIn(requirement, dev)

        for name in ("lint-pr.yml", "lint-push.yml", "tests-pr.yml", "tests-push.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn('pip install ".[dev,mcp]"', workflow)
            self.assertNotIn("pip install ruff", workflow)

    def test_embedded_client_material_requires_value_free_manifest_review(self):
        literal = "fixture-client-material-123456789"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "user_scanner" / "fixture.py"
            source.parent.mkdir()
            source.write_text(f'API_KEY = "{literal}"\n', encoding="utf-8")
            manifest_path = root / "security" / "embedded-client-material.json"
            manifest_path.parent.mkdir()
            manifest_path.write_text(
                json.dumps({"schema": MANIFEST_SCHEMA, "entries": []}),
                encoding="utf-8",
            )

            failures = audit_embedded_client_material(root, manifest_path)
            self.assertEqual(len(failures), 1)
            self.assertIn("unreviewed", failures[0])
            self.assertNotIn(literal, failures[0])

            finding = scan_embedded_client_material(root)[0]
            manifest_path.write_text(
                json.dumps(
                    {
                        "schema": MANIFEST_SCHEMA,
                        "entries": [
                            {
                                "path": finding["path"],
                                "kind": finding["kind"],
                                "sha256": finding["sha256"],
                                "provenance": "inherited-upstream",
                                "review_state": "unverified-client-material",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(audit_embedded_client_material(root, manifest_path), [])


if __name__ == "__main__":
    unittest.main()
