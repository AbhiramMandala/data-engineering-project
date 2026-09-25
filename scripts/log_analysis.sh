#!/bin/bash
# Task 2: Read the diary file (log) with simple Linux commands.
# Beginner dictionary:
#   grep = find lines with a word | sort = put in order
#   uniq -c = count repeats | awk = pick columns | head = show first few
#   wc -l = count lines
# Run in Git Bash / WSL / Linux / Docker Linux box
# Usage: bash scripts/log_analysis.sh [logs/app.log]
set -e
LOG=${1:-logs/app.log}

echo "=== 1. How many lines? How many errors / warnings? ==="
wc -l "$LOG"
echo -n "ERROR count: "; grep -c "ERROR" "$LOG" || true
echo -n "WARN count: "; grep -c "WARN" "$LOG" || true

echo ""
echo "=== 2. Which 5 computers asked the most? ==="
grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' "$LOG" | sort | uniq -c | sort -nr | head -5

echo ""
echo "=== 3. Which answer codes appeared, and how often? (200 = OK) ==="
grep -oE ' [0-9]{3} ' "$LOG" | tr -d ' ' | sort | uniq -c | sort -nr

echo ""
echo "=== 4. Which 5 pages were visited the most? ==="
grep -oE '/api/[a-z]+|/health' "$LOG" | sort | uniq -c | sort -nr | head -5

echo ""
echo "=== 5. Show 10 error lines (date + who failed) ==="
awk '/ERROR/ {print $1, $2, $NF}' "$LOG" | head -10

echo ""
echo "=== 6. How many diary lines per hour? ==="
awk '{print substr($1,1,10)" "substr($2,1,2)":00"}' "$LOG" | sort | uniq -c | head -10

echo ""
echo "=== 7. Save only the error lines into a small report file ==="
grep "ERROR" "$LOG" > logs/analysis_errors.txt
echo "Wrote logs/analysis_errors.txt ($(wc -l < logs/analysis_errors.txt) lines)"
