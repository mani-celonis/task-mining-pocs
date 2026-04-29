#!/usr/bin/env python3
"""
Report whether required env vars are set (never print values).
Run from the AhaAgent repository root (directory containing src/ and scripts/).

Exit code: 0 if reports complete; 1 if Python dependencies are missing.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _nonempty(name: str) -> bool:
    v = os.getenv(name)
    return bool(v and str(v).strip())


def main() -> int:
    os.chdir(REPO_ROOT)

    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv: MISSING (run: pip install -r requirements.txt)", file=sys.stderr)
        return 1

    load_dotenv(REPO_ROOT / ".env")

    try:
        import requests  # noqa: F401
    except ImportError:
        print("import requests: MISSING (run: pip install -r requirements.txt)", file=sys.stderr)
        return 1

    print("import requests: OK")

    print(f"AHA_API_KEY: {'set' if _nonempty('AHA_API_KEY') else 'missing'}")

    jira_vars = (
        "JIRA_HOST",
        "JIRA_EMAIL",
        "JIRA_API_TOKEN",
        "JIRA_BOARD_ID",
    )
    for name in jira_vars:
        print(f"{name}: {'set' if _nonempty(name) else 'missing'}")

    # Optional: external PM knowledge (Obsidian vault or folder). Never print the path value.
    kr = os.getenv("KNOWLEDGE_ROOT", "").strip()
    if not kr:
        print("KNOWLEDGE_ROOT: missing (optional; see .cursor/skills/external-knowledge)")
    else:
        p = Path(kr).expanduser()
        if p.is_dir():
            aa = p / "AhaAgent"
            if aa.is_dir():
                print("KNOWLEDGE_ROOT: set, directory exists, AhaAgent/ present")
            else:
                print("KNOWLEDGE_ROOT: set, directory exists, AhaAgent/ missing (see docs/knowledge_layout.md)")
        else:
            print("KNOWLEDGE_ROOT: set but not a directory (check path)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
