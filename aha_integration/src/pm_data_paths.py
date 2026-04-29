"""
Resolve PM working directories: Obsidian vault (KNOWLEDGE_ROOT/AhaAgent/...) vs repo data/ fallback.

When KNOWLEDGE_ROOT is set in .env, most working files go under <KNOWLEDGE_ROOT>/AhaAgent/<sub>/
(glossary, intake, jira-briefs, etc.). Dated Aha feature-suggestion API exports use
<KNOWLEDGE_ROOT>/incoming/feature-suggestions/ (see incoming_feature_suggestions_dir).
Optional planning markdown may live under <KNOWLEDGE_ROOT>/portfolio/products/planning/
(see default_planning_docs_dir).

When KNOWLEDGE_ROOT is unset, use <repo>/data/<sub>/ for local-only / CI use.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(_REPO_ROOT / ".env")
    except ImportError:
        pass


def knowledge_root() -> Optional[Path]:
    """Path to the vault (or knowledge folder) root, or None if not configured / invalid."""
    _load_dotenv()
    kr = (os.getenv("KNOWLEDGE_ROOT") or "").strip()
    if not kr:
        return None
    p = Path(kr).expanduser().resolve()
    return p if p.is_dir() else None


def use_vault_for_pm_data() -> bool:
    return knowledge_root() is not None


def aha_agent_subdir(*parts: str) -> Path:
    """Under KNOWLEDGE_ROOT: AhaAgent/<parts>. Falls back to repo data/<first part>/... if no vault."""
    kr = knowledge_root()
    if kr is not None:
        p = kr / "AhaAgent"
        for x in parts:
            p = p / x
        return p
    p = _REPO_ROOT / "data"
    for x in parts:
        p = p / x
    return p


def jira_briefs_dir() -> Path:
    return aha_agent_subdir("jira-briefs")


def intake_dir() -> Path:
    return aha_agent_subdir("intake")


def feature_suggestions_dir() -> Path:
    """AhaAgent/feature-suggestions (or data/feature-suggestions). Not the default root for aha_feature_suggestions exports; use incoming_feature_suggestions_dir."""
    return aha_agent_subdir("feature-suggestions")


def incoming_feature_suggestions_dir() -> Path:
    """Default root for dated aha_feature_suggestions output: incoming/ when a vault is set, else repo data/."""
    kr = knowledge_root()
    if kr is not None:
        return kr / "incoming" / "feature-suggestions"
    return _REPO_ROOT / "data" / "feature-suggestions"


def default_planning_docs_dir() -> Path:
    """Primary convention: ``KNOWLEDGE_ROOT/portfolio/products/planning``.

    Use when the vault root is the parent of a ``portfolio`` folder (see planning_docs_dir_candidates
    for an alternate when ``KNOWLEDGE_ROOT`` is already the inner ``portfolio`` directory).
    The directory may not exist; callers should check is_dir() before listing.
    When KNOWLEDGE_ROOT is unset, resolves to ``data/portfolio/products/planning`` under the repo.
    """
    kr = knowledge_root()
    if kr is not None:
        return kr / "portfolio" / "products" / "planning"
    return _REPO_ROOT / "data" / "portfolio" / "products" / "planning"


def planning_docs_dir_candidates() -> list[Path]:
    """Return typical planning-folder paths under the knowledge root (0–2 may exist).

    Order: (1) ``<KR>/portfolio/products/planning`` when KR is the vault parent;
    (2) ``<KR>/products/planning`` when KR is already the inner ``portfolio`` (or same layout
    without the extra ``portfolio`` segment). Skills should use the first path where is_dir().
    """
    kr = knowledge_root()
    if kr is not None:
        return [kr / "portfolio" / "products" / "planning", kr / "products" / "planning"]
    b = _REPO_ROOT / "data"
    return [b / "portfolio" / "products" / "planning", b / "products" / "planning"]
