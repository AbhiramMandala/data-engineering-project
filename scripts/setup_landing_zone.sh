#!/bin/bash
# Task 1: Create secure data landing zones with Linux permissions.
# Usage: bash scripts/setup_landing_zone.sh [base_dir]
#   base_dir defaults to data/landing
# Run on Linux, WSL2/Ubuntu, Git Bash, or inside a Linux container:
#   docker run --rm -v "$PWD:/app" -w /app ubuntu:22.04 bash scripts/setup_landing_zone.sh
set -euo pipefail

BASE="${1:-data/landing}"

mkdir -p "$BASE/raw" "$BASE/staging" "$BASE/processed"

# raw: immutable ingress, owner + group read/execute (750)
chmod 750 "$BASE/raw"
# staging: team working area (750; add setgid/chgrp for a shared group as needed)
chmod 750 "$BASE/staging"
# processed: restricted, owner-only (700)
chmod 700 "$BASE/processed"
chmod 750 "$BASE"

echo "Landing zones under $BASE:"
ls -l "$BASE"
echo "--- numeric perms (expect 750 750 750 700) ---"
stat -c '%a %n' "$BASE" "$BASE/raw" "$BASE/staging" "$BASE/processed"
echo "Recommended umask for data engineers: 027 (currently $(umask))"
