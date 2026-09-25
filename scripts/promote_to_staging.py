"""Promote latest raw users CSV to staging with basic validation."""
import glob
import shutil
from pathlib import Path

raw_files = sorted(glob.glob("data/landing/raw/users_*.csv"))
if not raw_files:
    raise SystemExit("No raw CSV found. Run scripts/fetch_api.py first.")
src = Path(raw_files[-1])
dst_dir = Path("data/landing/staging")
dst_dir.mkdir(parents=True, exist_ok=True)
dst = dst_dir / src.name
shutil.copy(src, dst)
print(f"Promoted {src} -> {dst} ({sum(1 for _ in open(dst))-1} data rows)")
