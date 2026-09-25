"""Tests for scripts/promote_to_staging.py."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import promote_to_staging


class PromoteTest(unittest.TestCase):
    def test_promotes_latest_csv(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw"
            staging = Path(tmp) / "staging"
            raw.mkdir()
            (raw / "users_20240101T000000Z.csv").write_text(
                "id,name,email,city\n1,Ada,ada@example.com,London\n")
            (raw / "users_20240202T000000Z.csv").write_text(
                "id,name,email,city\n2,Alan,alan@example.com,Manchester\n")
            dst = promote_to_staging.main(
                raw_pattern=str(raw / "users_*.csv"), staging_dir=str(staging))
            self.assertEqual(dst.name, "users_20240202T000000Z.csv")
            self.assertTrue(dst.exists())
            self.assertIn("Manchester", dst.read_text())

    def test_no_raw_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                promote_to_staging.main(
                    raw_pattern=str(Path(tmp) / "nothing_*.csv"),
                    staging_dir=str(Path(tmp) / "staging"))


if __name__ == "__main__":
    unittest.main()
