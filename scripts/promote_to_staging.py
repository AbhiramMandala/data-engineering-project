"""Promote latest raw users CSV to staging with basic validation."""
import glob
import shutil
from pathlib import Path


def main(raw_pattern="data/landing/raw/users_*.csv",
         staging_dir="data/landing/staging"):
    raw_files = sorted(glob.glob(raw_pattern))
    if not raw_files:
        raise SystemExit("No raw CSV found. Run scripts/fetch_api.py first.")
    src = Path(raw_files[-1])
    dst_dir = Path(staging_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    shutil.copy(src, dst)
    rows = sum(1 for _ in open(dst)) - 1
    print(f"Promoted {src} -> {dst} ({rows} data rows)")
    return dst


if __name__ == "__main__":
    main()
