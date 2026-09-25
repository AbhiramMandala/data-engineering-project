# What I built (simple summary)

## 1. Landing zones — folders with locks (Linux)
- Made `raw/`, `staging/`, `processed/` folders
- Locks: `raw/` 750, `staging/` 750, `processed/` 700 (only I can open it)

## 2. Log reading — diary file + Linux commands
- Made a 500-line practice diary (`logs/app.log`): 81 errors, 84 warnings
- Found: busiest computer, most-visited pages, most common answer codes
- Saved only the error lines into `logs/analysis_errors.txt`

## 3. Downloading data — free test website (API)
- Downloaded 10 users + 100 posts into `data/landing/raw/`
- Copied the newest file into `data/landing/staging/`

## 4. Docker — sealed box
- Built picture `de-fundamentals:1.0`; the download script runs the same inside the box
- Practice database (postgres:16) starts fine and answers "accepting connections"

## 5. Git — versions + asking to merge (Pull Request)
- Main copy + safe work copies (branches), merged back with Pull Request #1
- Everything under my name, working tree clean
