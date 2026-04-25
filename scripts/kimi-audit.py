#!/usr/bin/env python3
"""
Kimi Skills Audit
Compares locally extracted skills against a reference list from the Kimi UI.
Prints missing skills and the window._kimiTargets snippet for kimi-download.js.

USAGE:
  python scripts/kimi-audit.py --kimi-names "skill-a,skill-b,..."
  python scripts/kimi-audit.py  # shows local count only
"""
import argparse
import json
import os
import sys

KIMI_CLI_SKILLS = {
    "codex-worker", "feature-smoke-test", "gen-changelog", "gen-docs",
    "gen-rust", "pull-request", "release", "translate-docs", "worktree-status",
}

def main():
    parser = argparse.ArgumentParser(description="Audit local Kimi skills vs the official list.")
    parser.add_argument("--kimi-names", default="",
                        help="Comma-separated skill names from kimi-list.js output")
    parser.add_argument("--skills-dir", default=None,
                        help="Path to skills/ directory (default: <repo-root>/skills)")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = args.skills_dir or os.path.join(repo_root, "skills")

    if not os.path.isdir(skills_dir):
        print(f"Error: skills dir not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    local = {
        d for d in os.listdir(skills_dir)
        if os.path.isdir(os.path.join(skills_dir, d)) and d not in KIMI_CLI_SKILLS
    }

    if not args.kimi_names.strip():
        print("No --kimi-names provided. Showing local skill count only.")
        print(f"Local skills: {len(local)}")
        print()
        print("To get the full Kimi list, run kimi-list.js in the browser console and")
        print("pass the output here with: python scripts/kimi-audit.py --kimi-names \"...\"")
        return

    kimi = {s.strip() for s in args.kimi_names.split(",") if s.strip()}

    missing = sorted(kimi - local)
    extra = sorted(local - kimi)

    print(f"Kimi official : {len(kimi)}")
    print(f"Local         : {len(local)}")
    print()

    if not missing:
        print("All Kimi skills are present locally.")
    else:
        print(f"Missing locally ({len(missing)}):")
        for name in missing:
            print(f"  - {name}")
        print()
        print("Set these as targets in the browser before running kimi-download.js:")
        print(f"window._kimiTargets = {json.dumps(missing)}")

    if extra:
        print()
        print("Local only (not in Kimi list — may have been removed from the platform):")
        for name in extra:
            print(f"  + {name}")

if __name__ == "__main__":
    main()
