"""
Flatten Jira Cloud issue description from Atlassian Document Format (ADF) to plain text.
"""

from __future__ import annotations

import re
from typing import Any, List, Optional


def _collect_text_nodes(node: Any, out: List[str]) -> None:
    if node is None:
        return
    if isinstance(node, str):
        s = node.strip()
        if s:
            out.append(s)
        return
    if not isinstance(node, dict):
        return
    if node.get("type") == "text":
        t = node.get("text")
        if isinstance(t, str) and t:
            out.append(t)
        return
    for key in ("content",):
        child = node.get(key)
        if isinstance(child, list):
            for c in child:
                _collect_text_nodes(c, out)
        elif child is not None:
            _collect_text_nodes(child, out)


def adf_to_plain_text(adf: Any) -> str:
    """Convert ADF JSON (or None) to a single plain-text string."""
    if adf is None:
        return ""
    if isinstance(adf, str):
        return adf.strip()
    if not isinstance(adf, dict):
        return ""
    parts: List[str] = []
    _collect_text_nodes(adf, parts)
    raw = " ".join(parts)
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw


def truncate_text(text: str, max_chars: int) -> str:
    if max_chars <= 0 or not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"
