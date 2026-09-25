# Results — Data Engineering Fundamentals

## 1. Secure landing zones (Linux, ubuntu:22.04)
- `/data/landing` 750, `raw/` 750, `staging/` 750, `processed/` 700, `umask 027`

## 2. Log analysis (`scripts/log_analysis.sh`)
- `logs/app.log`: 500 lines, ERROR 81, WARN 84
- Top IP `192.168.1.12` (31), top code `200` (207), top endpoint `/health` (117)
- Report: `logs/analysis_errors.txt` (81 lines, gitignored artifact)

## 3. REST API (`scripts/fetch_api.py`)
- `jsonplaceholder.typicode.com/users` (10) + `/posts` (100)
- Output: `data/landing/raw/users_*.json/.csv`, `posts_*.json`

## 4. Docker
- Image `de-fundamentals:1.0` built and run (ingest reproduced in container)
- `docker-compose.yml` service `db` (postgres:16) healthy via `pg_isready`

## 5. Git
- `main`: baseline `0adc514`, feature `d0027eb`, merge `519ed3a`
- This PR: adds results report + staging promotion proof
