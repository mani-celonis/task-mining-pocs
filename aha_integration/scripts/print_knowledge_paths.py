#!/usr/bin/env python3
"""
Print resolved PM knowledge paths from pm_data_paths (KNOWLEDGE_ROOT / data/ fallback).
Never prints API keys or tokens. Run from repo root:
  python scripts/print_knowledge_paths.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)
sys.path.insert(0, str(REPO_ROOT / "src"))

_DATE_DIR = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main() -> int:
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv: MISSING (run: pip install -r requirements.txt)", file=sys.stderr)
        return 1

    load_dotenv(REPO_ROOT / ".env")

    try:
        from pm_data_paths import (
            default_planning_docs_dir,
            feature_suggestions_dir,
            incoming_feature_suggestions_dir,
            intake_dir,
            jira_briefs_dir,
            knowledge_root,
            planning_docs_dir_candidates,
        )
    except ImportError as e:
        print(f"Cannot import pm_data_paths: {e}", file=sys.stderr)
        return 1

    kr = knowledge_root()
    if kr is None:
        print("KNOWLEDGE_ROOT: not set or not a valid directory (using repo data/ fallbacks below)")
    else:
        print(f"KNOWLEDGE_ROOT: {kr}")

    print(f"jira_briefs: {jira_briefs_dir()}")
    print(f"intake: {intake_dir()}")
    print(f"feature_suggestions (legacy AhaAgent subtree, not default export root): {feature_suggestions_dir()}")
    inc = incoming_feature_suggestions_dir()
    print(f"incoming_feature_suggestions (default aha_feature_suggestions exports): {inc}")

    cands = planning_docs_dir_candidates()
    found = [p for p in cands if p.is_dir()]
    if found:
        for p in found:
            print(f"planning_docs: {p}")
    else:
        print(
            "planning_docs: (no default folder yet; try, under KNOWLEDGE_ROOT, "
            f"portfolio/products/planning or products/planning — e.g. {default_planning_docs_dir()})"
        )

    if not inc.is_dir():
        print("latest_feature_suggestion_snapshot: (incoming directory does not exist yet)")
        return 0

    dated = [
        p
        for p in inc.iterdir()
        if p.is_dir() and _DATE_DIR.match(p.name)
    ]
    if not dated:
        print("latest_feature_suggestion_snapshot: no YYYY-MM-DD subfolders under incoming (no exports yet)")
        return 0

    latest = sorted(dated, key=lambda p: p.name)[-1]
    print(f"latest_feature_suggestion_date_dir: {latest}")
    mds = sorted(latest.glob("feature-suggestions-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if mds:
        print(f"latest_feature_suggestion_markdown: {mds[0].name}")
    else:
        print("latest_feature_suggestion_markdown: (no feature-suggestions-*.md in latest date folder)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
