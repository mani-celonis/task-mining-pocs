#!/usr/bin/env python3
"""
Compare the vault at KNOWLEDGE_ROOT to the layout expected for AhaAgent PM workflows.

Reads KNOWLEDGE_ROOT from .env (or optional CLI path). Does not print the path value;
only status lines (ok / missing).

Run from the AhaAgent repository root.
Exit code: 0 if all required items exist, 1 if any required item is missing or KNOWLEDGE_ROOT unset.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Paths relative to KNOWLEDGE_ROOT (required for meeting-notes + tagging workflows).
REQUIRED: tuple[tuple[str, str], ...] = (
    ("file", "AhaAgent/product-glossary.md"),
    ("dir", "AhaAgent/Products"),
    ("dir", "AhaAgent/Meetings"),
    ("dir", "AhaAgent/Meetings/Transcripts"),
    ("dir", "AhaAgent/jira-briefs"),
    ("dir", "AhaAgent/intake"),
    ("dir", "incoming/feature-suggestions"),
    ("file", "Tasks/README.md"),
    ("file", "GOALS.md"),
)


def main() -> int:
    os.chdir(REPO_ROOT)

    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv: MISSING (run: pip install -r requirements.txt)", file=sys.stderr)
        return 1

    load_dotenv(REPO_ROOT / ".env")

    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).expanduser().resolve()
    else:
        kr = (os.getenv("KNOWLEDGE_ROOT") or "").strip()
        if not kr:
            print("KNOWLEDGE_ROOT: not set; pass a path: python scripts/knowledge_gap_check.py /path/to/vault")
            return 1
        root = Path(kr).expanduser().resolve()

    if not root.is_dir():
        print("KNOWLEDGE_ROOT: not a directory (check .env or CLI argument)")
        return 1

    all_ok = True
    for kind, rel in REQUIRED:
        p = root / rel
        if kind == "file":
            ok = p.is_file()
        else:
            ok = p.is_dir()
        status = "ok" if ok else "MISSING"
        if not ok:
            all_ok = False
        # Print relative requirement only, not the resolved root
        print(f"{rel}: {status}")

    if all_ok:
        print("knowledge_gap_check: all required paths present")
    else:
        print("knowledge_gap_check: see MISSING above; see docs/knowledge_layout.md")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
