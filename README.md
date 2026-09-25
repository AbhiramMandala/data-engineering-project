# Data Engineering Fundamentals — Linux + Git

End-to-end mini project covering:
1. Secure data landing zones (Linux permissions)
2. Log analysis (`grep`, `awk`, `sort`, `uniq`)
3. REST API ingestion (Python + `urllib`, no API key)
4. Docker containers (ingest image + Postgres)
5. Git branching + Pull Requests

## Project structure

```
.
├── data/landing/{raw,staging,processed}/  # Task 1 + 3 (only .gitkeep committed; ingested files are gitignored)
├── docs/pipeline.png                       # architecture flowchart
├── logs/app.log                            # Task 2 sample logs (generated)
├── scripts/
│   ├── setup_landing_zone.sh               # Task 1: mkdir + chmod 750/700
│   ├── generate_logs.py                    # create sample logs/app.log
│   ├── log_analysis.sh                     # Task 2: Linux log analysis
│   ├── fetch_api.py                        # Task 3: REST ingestion -> raw/
│   ├── promote_to_staging.py               # raw/ -> staging/ promotion
│   └── make_diagram.py                     # regenerate docs/pipeline.png (needs pillow)
├── tests/
│   ├── test_fetch_api.py                   # mocked, no network
│   └── test_promote_to_staging.py
├── .github/workflows/ci.yml                # compile + tests + logs + docker build
├── Dockerfile                              # Task 4 (copies scripts/ + logs/; fetch_api.py creates data dirs at runtime)
├── docker-compose.yml                      # Task 4 (ingest + postgres:16)
├── requirements.txt
├── RESULTS.md
└── .gitignore
```

## Prerequisites

| Tool | Check | Notes |
|---|---|---|
| Git | `git --version` | 2.40+ |
| Python 3.12+ | `python --version` | stdlib only for ingestion; `pillow` only for the diagram |
| Docker Desktop | `docker --version` | with Linux containers |
| Linux shell | `bash --version` | Git Bash, WSL2/Ubuntu, or `ubuntu:22.04` container |

> Windows NTFS does not enforce Linux permission bits. Run Task 1 in
> WSL2/Ubuntu or a Linux container so `chmod`/`stat` behave for real.

## Setup

```bash
git clone https://github.com/AbhiramMandala/data-engineering-project.git
cd data-engineering-project
pip install -r requirements.txt
```

## Task 1 — Secure data landing zones

```bash
bash scripts/setup_landing_zone.sh
# raw/ 750 (immutable ingress) • staging/ 750 (team) • processed/ 700 (owner-only), umask 027
```

Linux-container equivalent (proves real permission bits):

```bash
docker run --rm -v "$PWD:/app" -w /app ubuntu:22.04 bash scripts/setup_landing_zone.sh
```

## Task 2 — Analyze logs with Linux commands

```bash
python scripts/generate_logs.py        # 500-line sample -> logs/app.log
bash scripts/log_analysis.sh logs/app.log
# 500 lines • 81 ERROR • 84 WARN • top IP/code/endpoint • writes logs/analysis_errors.txt (gitignored)
```

## Task 3 — Collect data from REST APIs

```bash
python scripts/fetch_api.py            # 10 users + 100 posts -> data/landing/raw/users_*.json/.csv
python scripts/promote_to_staging.py   # latest raw CSV -> data/landing/staging/
```

## Task 4 — Docker containers

```bash
docker build -t de-fundamentals:1.0 .
docker compose up -d db               # postgres:16 on :5432
docker exec defaultproject-db-1 pg_isready -U postgres
docker compose run --rm ingest        # same fetch_api.py, reproducibly, writes to mounted raw/
docker compose down
```

Note: the image `COPY`s `scripts/` + `logs/`; the landing directories are
created at runtime by `fetch_api.py` (`Path.mkdir(parents=True, exist_ok=True)`)
and persisted via the `./data/landing/raw` bind mount.

## Task 5 — Git branching + pull requests

```bash
git checkout -b feature/<name>
# ... edit, then:
python -m unittest discover -s tests
git add . && git commit -m "feat: ..."
git push -u origin feature/<name>
gh pr create --base main --head feature/<name>
```

## Verification

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
bash scripts/setup_landing_zone.sh
bash scripts/log_analysis.sh logs/app.log
```

## Cleanup

```bash
docker compose down -v
rm -f data/landing/raw/users_* data/landing/raw/posts_* data/landing/staging/users_*
```

## Shell cheat-sheet (Windows CMD vs Git Bash/Linux)

| Action | CMD | Git Bash / Linux |
|---|---|---|
| Enter project | `cd /d "C:\Users\AbhiramMandala\Documents\Default Project"` | `cd ~/Documents/"Default Project"` |
| Landing zones | (use Git Bash or container) | `bash scripts/setup_landing_zone.sh` |
| Container ingest (CMD) | `docker run --rm -v "%cd%\data\landing\raw:/app/data/landing/raw" de-fundamentals:1.0` | `docker run --rm -v "$PWD/data/landing/raw:/app/data/landing/raw" de-fundamentals:1.0` |
| Tests | `python -m unittest discover -s tests` | same |
