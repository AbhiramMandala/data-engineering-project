"""Tests for scripts/fetch_api.py (no network: urlopen is mocked)."""
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import fetch_api

USERS = [
    {"id": 1, "name": " Ada Lovelace ".strip(), "email": "ada@example.com",
     "address": {"city": "London"}},
    {"id": 2, "name": "Alan Turing", "email": "alan@example.com",
     "address": {"city": "Manchester"}},
]
POSTS = [{"id": 1, "userId": 1, "title": "hello", "body": "world"}]


class FakeResp:
    def __init__(self, payload):
        self._buf = io.BytesIO(json.dumps(payload).encode())

    def read(self):
        return self._buf.read()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def fake_urlopen(req, timeout=30):
    url = req.full_url if hasattr(req, "full_url") else req
    if url.endswith("/users"):
        return FakeResp(USERS)
    return FakeResp(POSTS)


class FetchApiTest(unittest.TestCase):
    def test_main_writes_json_and_csv(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "raw"
            with patch.object(fetch_api, "RAW", raw), \
                 patch("urllib.request.urlopen", side_effect=fake_urlopen):
                fetch_api.main()
            users_files = sorted(raw.glob("users_*.json"))
            posts_files = sorted(raw.glob("posts_*.json"))
            csv_files = sorted(raw.glob("users_*.csv"))
            self.assertEqual(len(users_files), 1)
            self.assertEqual(len(posts_files), 1)
            self.assertEqual(len(csv_files), 1)
            self.assertEqual(len(json.loads(users_files[0].read_text())), 2)
            rows = csv_files[0].read_text().splitlines()
            self.assertEqual(rows[0], "id,name,email,city")
            self.assertEqual(len(rows), 3)  # header + 2 users
            self.assertIn("London", rows[1])


if __name__ == "__main__":
    unittest.main()
