import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeSafetyContractTests(unittest.TestCase):
    def test_authorised_use_boundary_precedes_capability_marketing(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        lowered = readme.casefold()
        key_features = lowered.index("key features")
        preface = lowered[:key_features]

        self.assertIn("authorized defensive", preface)
        self.assertIn("investigative indicator", preface)
        self.assertIn("explicit permission", preface)
        self.assertLess(preface.index("authorized defensive"), preface.index("455+"))

        # Avoid marketing language that overstates attribution or encourages misuse.
        self.assertNotIn("analyze target behavior", lowered)
        self.assertNotIn("verify account registrations in seconds", lowered)
        self.assertNotIn("go beyond account enumeration", lowered)


if __name__ == "__main__":
    unittest.main()
