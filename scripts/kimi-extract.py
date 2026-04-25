#!/usr/bin/env python3
"""
Kimi Skills Extractor
Extracts downloaded Kimi skill zips into the repo, deduplicating by keeping only
the most recent file when Chrome created numbered duplicates like "skill (1).zip".

USAGE:
  python scripts/kimi-extract.py
  python scripts/kimi-extract.py --downloads-dir ~/Downloads --hours-back 6

After extraction, run: git add skills && git commit -m "Update Kimi skills $(date +%Y-%m-%d)"
"""
import argparse
import os
import re
import sys
import zipfile
from datetime import datetime, timedelta
from pathlib import Path


def strip_suffix(stem: str) -> str:
    return re.sub(r" \(\d+\)$", "", stem)


def _find_downloads_dir() -> Path:
    # On Windows, the Downloads folder may not be under the home drive (e.g. redirected to F:\).
    # Query the real path via the Windows Shell COM API when available.
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            )
            val, _ = winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")
            winreg.CloseKey(key)
            p = Path(val)
            if p.is_dir():
                return p
        except Exception:
            pass
    return Path.home() / "Downloads"


def main():
    parser = argparse.ArgumentParser(description="Extract Kimi skill zips into the repo.")
    parser.add_argument("--downloads-dir", default=None,
                        help="Path to Downloads folder (default: ~/Downloads)")
    parser.add_argument("--hours-back", type=int, default=4,
                        help="Only consider zips newer than this many hours (default: 4)")
    parser.add_argument("--skills-dir", default=None,
                        help="Path to skills/ directory (default: <repo-root>/skills)")
    args = parser.parse_args()

    if args.downloads_dir:
        downloads_dir = Path(args.downloads_dir)
    else:
        downloads_dir = _find_downloads_dir()
    repo_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    skills_dir = Path(args.skills_dir) if args.skills_dir else repo_root / "skills"

    if not downloads_dir.is_dir():
        print(f"Error: downloads dir not found: {downloads_dir}", file=sys.stderr)
        sys.exit(1)
    if not skills_dir.is_dir():
        print(f"Error: skills dir not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    cutoff = datetime.now() - timedelta(hours=args.hours_back)
    all_zips = [
        p for p in downloads_dir.glob("*.zip")
        if datetime.fromtimestamp(p.stat().st_mtime) > cutoff
    ]
    print(f"Found {len(all_zips)} zip(s) newer than {args.hours_back} hours in {downloads_dir}")

    # Deduplicate: strip " (N)" suffix, keep the most recently modified file per base name
    groups: dict[str, list[Path]] = {}
    for z in all_zips:
        base = strip_suffix(z.stem)
        groups.setdefault(base, []).append(z)

    unique = {base: max(paths, key=lambda p: p.stat().st_mtime) for base, paths in groups.items()}
    print(f"Unique skills to extract: {len(unique)}")

    extracted = 0
    failed = 0

    for name, zip_path in sorted(unique.items()):
        dest = skills_dir / name
        if dest.exists():
            import shutil
            shutil.rmtree(dest)
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(dest)
            print(f"  Extracted: {name}")
            extracted += 1
        except Exception as e:
            print(f"  Failed to extract {zip_path.name}: {e}", file=sys.stderr)
            failed += 1

    print()
    print(f"Done. Extracted: {extracted}  Failed: {failed}")
    print(f"Total skill dirs now: {sum(1 for p in skills_dir.iterdir() if p.is_dir())}")


if __name__ == "__main__":
    main()
