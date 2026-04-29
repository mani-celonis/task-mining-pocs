#!/usr/bin/env python3
"""
Verify agentic harness integrity for AhaAgent.
Checks: required paths, rule frontmatter, executor + CLI + helpers syntax.
No API key or network required. Run from repo root.
"""

import os
import re
import sys
import py_compile
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

REQUIRED_PATHS = [
    "src/",
    "src/api/",
    "src/cli.py",
    "src/lib/",
    "src/lib/aha_helpers.py",
    "src/executors/",
    "docs/",
    "docs/aha_api_notes.md",
    "docs/celonis_aha_rules.md",
    "docs/knowledge_layout.md",
    "docs/knowledge_multiroot.md",
    "docs/templates/jira_pm_brief.md",
    "src/pm_data_paths.py",
    ".cursor/rules/",
    ".cursor/skills/",
]

REQUIRED_RULES = [
    ".cursor/rules/aha-agent.mdc",
    ".cursor/rules/product-tagging.mdc",
]

REQUIRED_SKILLS = [
    ".cursor/skills/onboarding/SKILL.md",
    ".cursor/skills/external-knowledge/SKILL.md",
    ".cursor/skills/meeting-notes/SKILL.md",
    ".cursor/skills/aha-bulk-update/SKILL.md",
    ".cursor/skills/jira-board-overview/SKILL.md",
    ".cursor/skills/jira-pm-brief/SKILL.md",
    ".cursor/skills/aha-feature-suggestions/SKILL.md",
]

FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n",
    re.DOTALL,
)


def check_paths() -> list[str]:
    """Verify required paths exist. Returns list of errors."""
    errors = []
    for p in REQUIRED_PATHS:
        path = REPO_ROOT / p
        if not path.exists():
            errors.append(f"Missing path: {p}")
    return errors


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Extract YAML frontmatter from content. Returns (parsed dict or None, rest)."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, content
    # Minimal YAML parse - just check for key fields
    block = match.group(1)
    result = {}
    for line in block.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip().lower()] = val.strip().strip('"\'')
    return result, content[match.end() :]


def check_rules() -> list[str]:
    """Verify rule files exist and have valid frontmatter. Returns list of errors."""
    errors = []
    for p in REQUIRED_RULES:
        path = REPO_ROOT / p
        if not path.exists():
            errors.append(f"Missing rule: {p}")
            continue
        content = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        if fm is None:
            errors.append(f"Rule {p} has no YAML frontmatter (--- ... ---)")
        elif "description" not in fm:
            errors.append(f"Rule {p} frontmatter missing 'description'")
    return errors


def check_skills() -> list[str]:
    """Verify skill files exist and have valid frontmatter. Returns list of errors."""
    errors = []
    for p in REQUIRED_SKILLS:
        path = REPO_ROOT / p
        if not path.exists():
            errors.append(f"Missing skill: {p}")
            continue
        content = path.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        if fm is None:
            errors.append(f"Skill {p} has no YAML frontmatter (--- ... ---)")
        elif "description" not in fm or "name" not in fm:
            errors.append(f"Skill {p} frontmatter missing 'name' or 'description'")
    return errors


def check_executor_syntax() -> list[str]:
    """Verify scratchpad, CLI, and shared helpers all compile."""
    errors = []
    targets = [
        REPO_ROOT / "src" / "executors" / "scratchpad.py",
        REPO_ROOT / "src" / "cli.py",
        REPO_ROOT / "src" / "lib" / "aha_helpers.py",
    ]
    for target in targets:
        rel = target.relative_to(REPO_ROOT)
        if not target.exists():
            errors.append(f"Missing {rel}")
            continue
        try:
            py_compile.compile(str(target), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"{rel} has syntax errors: {e}")
    return errors


def main() -> int:
    all_errors = []
    all_errors.extend(check_paths())
    all_errors.extend(check_rules())
    all_errors.extend(check_skills())
    all_errors.extend(check_executor_syntax())

    if all_errors:
        print("verify_harness: FAILED", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("verify_harness: OK (paths, rules, skills, executor + CLI + helpers syntax)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
