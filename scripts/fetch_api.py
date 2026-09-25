"""Task 3: download practice data from a free test website into raw/.

Beginner note: an 'API' here is just a web address that sends back data
(lists of users and posts) instead of a web page. No password needed.
Files are saved with the date/time in the name, e.g. users_20260925T073805Z.json.
"""
import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# raw/ = the folder where brand-new data lands first. Make it if missing.
RAW = Path("data/landing/raw")
RAW.mkdir(parents=True, exist_ok=True)

def fetch_json(url: str, timeout: int = 30):
    # Ask the website for data and turn its answer into a Python list/dict.
    req = urllib.request.Request(url, headers={"User-Agent": "de-fundamentals/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    # Free practice site - no key needed. Swap these links for your own data later.
    users = fetch_json("https://jsonplaceholder.typicode.com/users")
    posts = fetch_json("https://jsonplaceholder.typicode.com/posts")

    # Stamp = current date/time, so every download gets its own file names.
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    users_path = RAW / f"users_{ts}.json"
    posts_path = RAW / f"posts_{ts}.json"
    users_path.write_text(json.dumps(users, indent=2))
    posts_path.write_text(json.dumps(posts, indent=2))

    # A simple table version (CSV) of the users, for the staging demo.
    csv_path = RAW / f"users_{ts}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "email", "city"])
        w.writeheader()
        for u in users:
            w.writerow({"id": u["id"], "name": u["name"], "email": u["email"],
                        "city": u["address"]["city"]})

    print(f"Saved {len(users)} users -> {users_path}")
    print(f"Saved {len(posts)} posts -> {posts_path}")
    print(f"Saved CSV -> {csv_path}")

if __name__ == "__main__":
    main()
