#!/bin/bash
# Task 2: Log analysis with Linux commands
# Run in Git Bash / WSL / Linux / Docker Linux container
# Usage: bash scripts/log_analysis.sh [logs/app.log]
set -e
LOG=${1:-logs/app.log}

echo "=== 1. Total lines, errors, warnings ==="
wc -l "$LOG"
echo -n "ERROR count: "; grep -c "ERROR" "$LOG" || true
echo -n "WARN count: "; grep -c "WARN" "$LOG" || true

echo ""
echo "=== 2. Top 5 IPs by request count ==="
grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' "$LOG" | sort | uniq -c | sort -nr | head -5

echo ""
echo "=== 3. HTTP status code distribution ==="
grep -oE ' [0-9]{3} ' "$LOG" | tr -d ' ' | sort | uniq -c | sort -nr

echo ""
echo "=== 4. Top 5 requested endpoints ==="
grep -oE '/api/[a-z]+|/health' "$LOG" | sort | uniq -c | sort -nr | head -5

echo ""
echo "=== 5. ERROR lines with user_id (awk filter) ==="
awk '/ERROR/ {print $1, $2, $NF}' "$LOG" | head -10

echo ""
echo "=== 6. Hourly error trend ==="
awk '{print substr($1,1,10)" "substr($2,1,2)":00"}' "$LOG" | sort | uniq -c | head -10

echo ""
echo "=== 7. Save ERROR lines to report ==="
grep "ERROR" "$LOG" > logs/analysis_errors.txt
echo "Wrote logs/analysis_errors.txt ($(wc -l < logs/analysis_errors.txt) lines)"
