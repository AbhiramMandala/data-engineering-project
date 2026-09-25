# Data Engineering Fundamentals (Beginner Friendly)

A small hands-on project that teaches the basics of data engineering:
1. **Landing zones** — folders where new data arrives, with locks (permissions) on them
2. **Log analysis** — reading computer diary files with simple Linux commands
3. **API ingestion** — downloading data from a website that shares test data
4. **Docker** — running your code inside a sealed box that works on any machine
5. **Git + Pull Requests** — saving versions of your code and asking to merge changes

## Words you will see (simple meanings)

| Word | Simple meaning |
|---|---|
| Landing zone | A folder where fresh data lands first (`raw/`), then moves to `staging/` and `processed/` |
| Permission (750 / 700) | A lock on a folder. 750 = owner + team can open, others cannot. 700 = only owner |
| Log file | A diary file where a program writes what happened |
| API | A website address that gives you data instead of a web page |
| Container | A sealed box with everything your code needs, so it runs the same everywhere |
| Branch | A copy of your code where you can try changes safely |
| Pull Request (PR) | Asking "please check my changes and add them to the main code" |

## Project map

```
.
├── data/landing/{raw,staging,processed}/  # landing zones (only tiny .gitkeep placeholder files are saved in git)
├── docs/pipeline.png                       # picture of the whole project
├── logs/app.log                            # sample diary file (made by a script)
├── scripts/
│   ├── setup_landing_zone.sh               # Task 1: make folders + put locks on them
│   ├── generate_logs.py                    # make a sample diary file
│   ├── log_analysis.sh                     # Task 2: read the diary with Linux commands
│   ├── fetch_api.py                        # Task 3: download test data into raw/
│   ├── promote_to_staging.py               # move the newest raw file into staging/
│   └── make_diagram.py                     # re-draw docs/pipeline.png (needs pillow)
├── tests/                                  # small automatic checks for the scripts
├── .github/workflows/ci.yml                # robot that runs the checks on every push
├── Dockerfile                              # Task 4: recipe for the sealed box (copies scripts/ + logs/)
├── docker-compose.yml                      # Task 4: runs the box + a Postgres database
├── requirements.txt
├── RESULTS.md
└── .gitignore                              # tells git which files to skip (downloaded data, reports)
```

## What you need first

| Tool | How to check | Why |
|---|---|---|
| Git | `git --version` | save code versions |
| Python 3.12+ | `python --version` | run the scripts |
| Docker Desktop | `docker --version` | run sealed boxes |
| A Linux shell | `bash --version` | Git Bash, WSL2/Ubuntu, or a Linux box in Docker |

> Windows cannot do Linux folder locks by itself. So run Task 1 inside
> WSL2/Ubuntu or a Linux box (example below) — then the locks are real.

## Start here (copy-paste)

```bash
git clone https://github.com/AbhiramMandala/data-engineering-project.git
cd data-engineering-project
pip install -r requirements.txt
```

## Task 1 — Make landing zones (folders + locks)

A landing zone is just 3 folders: `raw/` (new data lands here),
`staging/` (cleaning area), `processed/` (finished data).

```bash
bash scripts/setup_landing_zone.sh
```

What it does, in plain words: creates the 3 folders, then puts locks on
them — team can open `raw/` and `staging/` (750), only you can open
`processed/` (700). It prints the locks so you can see them.

To prove the locks on Windows, run the same script inside a Linux box:

```bash
docker run --rm -v "$PWD:/app" -w /app ubuntu:22.04 bash scripts/setup_landing_zone.sh
```

## Task 2 — Read a diary (log) file

First make a sample diary file (500 lines, some normal lines, some warnings, some errors):

```bash
python scripts/generate_logs.py
bash scripts/log_analysis.sh logs/app.log
```

What you will see: total lines (500), error count (81), warning count (84),
which computer asked the most, which pages were visited most, and a new
report file `logs/analysis_errors.txt` with only the error lines.

Linux commands used, in plain words:
`grep` = find lines with a word • `sort` = put in order •
`uniq -c` = count repeats • `awk` = pick columns • `head` = show first few.

## Task 3 — Download data from a test website (API)

```bash
python scripts/fetch_api.py            # downloads 10 users + 100 posts into data/landing/raw/
python scripts/promote_to_staging.py   # copies the newest file into data/landing/staging/
```

The website is a free practice site, no password needed. Files are named
with the date and time, e.g. `users_20260925T073805Z.json`.

## Task 4 — Run it inside Docker (sealed box)

```bash
docker build -t de-fundamentals:1.0 .
docker compose up -d db               # starts a practice database on your machine
docker exec defaultproject-db-1 pg_isready -U postgres   # should say "accepting connections"
docker compose run --rm ingest        # runs the same download script, inside the box
docker compose down                   # stop everything
```

Simple idea: the box already has Python and the scripts inside
(`COPY scripts/ + logs/` in the `Dockerfile`). When it runs, the script
creates the data folders itself and saves files to your computer through
the shared folder (`./data/landing/raw`).

## Task 5 — Save versions with Git, propose changes with a Pull Request

```bash
git checkout -b feature/my-change     # make a safe copy to work in
# ... change something, then check your work:
python -m unittest discover -s tests
git add . && git commit -m "feat: describe your change"
git push -u origin feature/my-change
gh pr create --base main --head feature/my-change   # ask for a review
```

Simple idea: `main` is the good copy. You never edit it directly —
you work on a branch copy, then a Pull Request asks someone to check
and merge it in.

## How to check everything still works

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
bash scripts/setup_landing_zone.sh
bash scripts/log_analysis.sh logs/app.log
```

## How to clean up

```bash
docker compose down -v
rm -f data/landing/raw/users_* data/landing/raw/posts_* data/landing/staging/users_*
```

(These files are re-made every time you run Task 3, so deleting them is safe.)

## Windows CMD vs Git Bash (which command where)

| I want to... | Windows CMD | Git Bash / Linux |
|---|---|---|
| Open the project | `cd /d "C:\Users\AbhiramMandala\Documents\Default Project"` | `cd` to where you cloned it |
| Make landing zones | use Git Bash or the Linux-box command | `bash scripts/setup_landing_zone.sh` |
| Run the download in Docker | `docker run --rm -v "%cd%\data\landing\raw:/app/data/landing/raw" de-fundamentals:1.0` | `docker run --rm -v "$PWD/data/landing/raw:/app/data/landing/raw" de-fundamentals:1.0` |
| Run the checks | `python -m unittest discover -s tests` | same |
