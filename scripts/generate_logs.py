"""Generate realistic sample app.log for Task 2 log analysis."""
import random
from datetime import datetime, timedelta

random.seed(42)
levels = ["INFO", "INFO", "INFO", "INFO", "WARN", "ERROR"]
endpoints = ["/api/users", "/api/orders", "/api/products", "/api/login", "/health"]
status_ok = [200, 200, 200, 201, 301]
status_err = [404, 500, 502, 403, 429]
ips = [f"192.168.1.{i}" for i in range(2, 25)]

start = datetime(2026, 9, 20, 9, 0, 0)
lines = []
for i in range(500):
    ts = (start + timedelta(seconds=i * random.randint(20, 90))).strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(levels)
    ip = random.choice(ips)
    ep = random.choice(endpoints)
    if level == "INFO":
        status = random.choice(status_ok)
        msg = f'GET {ep} {status} {random.randint(12, 420)}ms'
    elif level == "WARN":
        status = random.choice([301, 429])
        msg = f'GET {ep} {status} slow-response {random.randint(800, 2500)}ms'
    else:
        status = random.choice(status_err)
        msg = f'GET {ep} {status} FAILED user_id={random.randint(1000, 1099)}'
    lines.append(f"{ts} [{level}] {ip} - {msg}")

with open("logs/app.log", "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"Wrote {len(lines)} lines to logs/app.log")
