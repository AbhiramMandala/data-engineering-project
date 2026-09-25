"""Task 3: Collect data from REST APIs into the landing zone."""
import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path("data/landing/raw")
RAW.mkdir(parents=True, exist_ok=True)

def fetch_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": "de-fundamentals/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    # Public test API - no key needed. Swap for your own source later.
    users = fetch_json("https://jsonplaceholder.typicode.com/users")
    posts = fetch_json("https://jsonplaceholder.typicode.com/posts")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    users_path = RAW / f"users_{ts}.json"
    posts_path = RAW / f"posts_{ts}.json"
    users_path.write_text(json.dumps(users, indent=2))
    posts_path.write_text(json.dumps(posts, indent=2))

    # Flattened CSV sample for staging demo
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
