#!/bin/bash
# Task 1: Make the 3 landing-zone folders and put locks (permissions) on them.
# Beginner note: raw/ = new data lands here. staging/ = cleaning table.
#   processed/ = finished data. Locks: 750 = owner+team can open, 700 = owner only.
# Run on Linux, WSL2/Ubuntu, Git Bash, or inside a Linux box (see README).
# Usage: bash scripts/setup_landing_zone.sh [folder]
set -euo pipefail

# Which folder to build under (default: data/landing).
BASE="${1:-data/landing}"

mkdir -p "$BASE/raw" "$BASE/staging" "$BASE/processed"

# raw: new data comes in, team may read (750)
chmod 750 "$BASE/raw"
# staging: team cleaning area (750)
chmod 750 "$BASE/staging"
# processed: finished data, owner only (700)
chmod 700 "$BASE/processed"
chmod 750 "$BASE"

echo "Landing zones under $BASE:"
ls -l "$BASE"
echo "--- locks as numbers (expect 750 750 750 700) ---"
stat -c '%a %n' "$BASE" "$BASE/raw" "$BASE/staging" "$BASE/processed"
echo "Tip for data engineers: set umask 027 so new files are born locked (now: $(umask))"
