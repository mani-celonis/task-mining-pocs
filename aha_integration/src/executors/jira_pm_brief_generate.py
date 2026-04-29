#!/usr/bin/env python3
"""
Build a detailed PM brief (Markdown) from JSON emitted by jira_board_overview.py --json.
Themes enumerate every issue with summary, status, sprint, optional description snippet (ADF flattened).

Usage:
  python src/executors/jira_board_overview.py --json --extra-fields > snap.json
  python src/executors/jira_pm_brief_generate.py --input snap.json --output path/to/brief.md

  Default output directory: $KNOWLEDGE_ROOT/AhaAgent/jira-briefs/ when KNOWLEDGE_ROOT is set, else data/jira-briefs/.

  # Or stdin:
  python src/executors/jira_board_overview.py --json --extra-fields | \\
    python src/executors/jira_pm_brief_generate.py --input - --slug tm-detailed
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_project_root, "src"))
os.chdir(_project_root)

from api.jira_adf import adf_to_plain_text, truncate_text
from pm_data_paths import jira_briefs_dir

_STOP = frozenset(
    """
    and for the with from this that have were been into than then them they
    when what which while will with without your also only over such some
    more most much must make like just each other into about after again
    """.split()
)


def fields(i: Dict[str, Any]) -> Dict[str, Any]:
    return i.get("fields") or {}


def issue_key(i: Dict[str, Any]) -> str:
    return i.get("key") or "?"


def summary(i: Dict[str, Any]) -> str:
    return (fields(i).get("summary") or "").strip() or "(no summary)"


def status_name(i: Dict[str, Any]) -> str:
    return (fields(i).get("status") or {}).get("name") or "?"


def priority_name(i: Dict[str, Any]) -> str:
    return (fields(i).get("priority") or {}).get("name") or "?"


def assignee_display(i: Dict[str, Any], redact: bool) -> str:
    if redact:
        return "—"
    a = fields(i).get("assignee")
    if not a:
        return "Unassigned"
    return (a.get("displayName") or a.get("accountId") or "?").strip()


def sprint_display(i: Dict[str, Any]) -> str:
    sp = fields(i).get("sprint")
    if not sp:
        return "—"
    names: List[str] = []
    if isinstance(sp, list):
        for s in sp:
            if isinstance(s, dict) and s.get("name"):
                names.append(str(s["name"]))
    elif isinstance(sp, dict) and sp.get("name"):
        names.append(str(sp["name"]))
    return ", ".join(names) if names else "—"


def description_snippet(i: Dict[str, Any], max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    raw = fields(i).get("description")
    plain = adf_to_plain_text(raw)
    return truncate_text(plain, max_chars)


def issuetype(i: Dict[str, Any]) -> str:
    return (fields(i).get("issuetype") or {}).get("name") or "?"


def primary_component(i: Dict[str, Any]) -> str:
    comps = fields(i).get("components") or []
    if isinstance(comps, list) and comps:
        c0 = comps[0]
        if isinstance(c0, dict) and c0.get("name"):
            return str(c0["name"])
    return "(no component)"


def epic_key_for(
    issue: Dict[str, Any], epic_link_field_id: Optional[str]
) -> Optional[str]:
    if epic_link_field_id:
        raw = fields(issue).get(epic_link_field_id)
        if isinstance(raw, dict) and raw.get("key"):
            return str(raw["key"])
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    p = fields(issue).get("parent")
    if isinstance(p, dict) and p.get("key"):
        pit = (p.get("fields") or {}).get("issuetype") or {}
        if (pit.get("name") or "").lower() == "epic":
            return str(p["key"])
    return None


def epic_title_for(issue: Dict[str, Any], ek: str) -> str:
    p = fields(issue).get("parent")
    if isinstance(p, dict) and p.get("key") == ek:
        t = (p.get("fields") or {}).get("summary")
        if isinstance(t, str) and t.strip():
            return t.strip()
    return ek


def tokenize_summaries(texts: List[str]) -> List[str]:
    out: List[str] = []
    for t in texts:
        for w in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", t.lower()):
            if w not in _STOP:
                out.append(w)
    return out


def workstream_hints(summaries: List[str], limit: int = 8) -> List[str]:
    """Bracket or prefix patterns from titles, e.g. [Migration-v1]."""
    hints: List[str] = []
    seen = set()
    for s in summaries:
        m = re.match(r"^\s*(\[[^\]]+\])\s*", s)
        if m:
            h = m.group(1)
            if h not in seen:
                seen.add(h)
                hints.append(h)
        if len(hints) >= limit:
            break
    return hints


def theme_narrative_paragraph(summaries: List[str]) -> str:
    if not summaries:
        return "_No summaries in this theme._"
    tokens = tokenize_summaries(summaries)
    top = Counter(tokens).most_common(8)
    topic_bits = ", ".join(f"**{w}** ({c})" for w, c in top[:6]) if top else ""
    hints = workstream_hints(summaries)
    hint_line = ""
    if hints:
        hint_line = " Title tags / prefixes seen: " + ", ".join(f"`{h}`" for h in hints) + "."
    if topic_bits:
        return (
            f"Recurring words in issue titles: {topic_bits}.{hint_line} "
            f"*(Deterministic extract — interpret with engineering context.)*"
        )
    return f"Issue titles span varied work.{hint_line} *(Add PM narrative after review.)*"


def load_json(path: str) -> Dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def group_by_component(
    issues: List[Dict[str, Any]], epic_field: Optional[str]
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, str]]:
    """theme_name -> issues; epic key -> epic title."""
    by_comp: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    epic_titles: Dict[str, str] = {}
    for issue in issues:
        if issuetype(issue).lower() == "epic":
            continue
        by_comp[primary_component(issue)].append(issue)
        ek = epic_key_for(issue, epic_field)
        if ek and ek not in epic_titles:
            epic_titles[ek] = epic_title_for(issue, ek)
    return dict(by_comp), epic_titles


def group_by_epic(
    issues: List[Dict[str, Any]], epic_field: Optional[str]
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, str]]:
    """epic key -> issues (epic as theme)."""
    by_ep: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    titles: Dict[str, str] = {}
    for issue in issues:
        if issuetype(issue).lower() == "epic":
            continue
        ek = epic_key_for(issue, epic_field) or "_no_epic_"
        by_ep[ek].append(issue)
        if ek != "_no_epic_" and ek not in titles:
            titles[ek] = epic_title_for(issue, ek)
    return dict(by_ep), titles


def render_issue_table_row(
    host: str,
    issue: Dict[str, Any],
    max_desc: int,
    redact: bool,
) -> str:
    desc = description_snippet(issue, max_desc)
    desc_cell = desc.replace("|", "\\|") if desc else "—"
    summ = summary(issue).replace("|", "\\|")
    return (
        f"| [{issue_key(issue)}]({host.rstrip('/')}/browse/{issue_key(issue)}) | {summ} | "
        f"{status_name(issue)} | {priority_name(issue)} | {sprint_display(issue)} | "
        f"{assignee_display(issue, redact)} | {desc_cell} |"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate detailed Jira PM brief from overview JSON")
    parser.add_argument("--input", "-i", required=True, help="Path to JSON or - for stdin")
    parser.add_argument(
        "--output",
        "-o",
        default="",
        help="Output .md path (default: under AhaAgent/jira-briefs/ in vault or data/jira-briefs/ in repo)",
    )
    parser.add_argument("--slug", default="tm-jql-brief-detailed", help="Filename slug if --output omitted")
    parser.add_argument(
        "--group-by",
        choices=("component", "epic"),
        default="component",
        help="Primary theme grouping",
    )
    parser.add_argument("--max-desc-chars", type=int, default=400, help="ADF description snippet length (0=omit)")
    parser.add_argument("--redact-assignees", action="store_true", help="Hide assignee names")
    parser.add_argument(
        "--large-theme-threshold",
        type=int,
        default=40,
        help="Add epic TOC when a theme has at least this many issues",
    )
    parser.add_argument(
        "--max-issues-per-theme",
        type=int,
        default=0,
        help="If >0, move overflow issues to Appendix per theme",
    )
    args = parser.parse_args()

    data = load_json(args.input)
    issues: List[Dict[str, Any]] = data.get("issues") or []
    host = (data.get("jira_host") or "https://celonis.atlassian.net").rstrip("/")
    epic_field = data.get("epic_link_field_id")
    jql = data.get("jql", "")
    source = data.get("source", "?")
    extra = data.get("extra_fields", False)

    if args.group_by == "component":
        grouped, epic_titles = group_by_component(issues, epic_field)
        theme_names = sorted(grouped.keys(), key=lambda x: (-len(grouped[x]), x))
    else:
        grouped, epic_titles = group_by_epic(issues, epic_field)
        theme_names = sorted(
            grouped.keys(),
            key=lambda k: (-len(grouped[k]), k if k != "_no_epic_" else "zzz"),
        )

    out_path = args.output.strip()
    if not out_path:
        jbd = jira_briefs_dir()
        jbd.mkdir(parents=True, exist_ok=True)
        out_path = str(jbd / f"{date.today().isoformat()}_{args.slug}.md")

    lines: List[str] = []
    lines.append("# Jira PM brief (detailed themes)")
    lines.append("")
    lines.append("## Context")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|-------|-------|")
    lines.append(f"| Date | {date.today().isoformat()} |")
    lines.append(f"| Source | `{source}` |")
    lines.append(f"| Issues in JSON | {len(issues)} |")
    lines.append(f"| Group by | {args.group_by} |")
    lines.append(f"| extra_fields in snapshot | {extra} |")
    lines.append("| PM product focus | *(edit after generation)* |")
    lines.append("")
    if jql:
        lines.append("<details><summary>JQL</summary>\n\n```")
        lines.append(jql)
        lines.append("```\n</details>\n")
    if not extra and args.max_desc_chars > 0:
        lines.append(
            "> **Note:** Snapshot lacks `description`/`sprint` fields. Re-run "
            "`jira_board_overview.py --json --extra-fields` for snippets and sprint column.\n"
        )

    lines.append("## Executive summary")
    lines.append("")
    lines.append(
        f"- **{len(issues)}** issues in export; themes below **list every non-Epic issue** once under `{args.group_by}` grouping."
    )
    lines.append(
        f"- **Detailed mode:** per-theme narrative from title tokens; epic subsections; full table per epic."
    )
    lines.append("")

    lines.append("## Themes (categorized work — detailed)")
    lines.append("")

    appendix: List[str] = []
    covered_keys = set()

    for theme in theme_names:
        bucket = grouped[theme]
        if args.group_by == "epic" and theme == "_no_epic_":
            display_theme = "(no epic link)"
        else:
            display_theme = theme

        lines.append(f"### Theme: {display_theme}")
        lines.append("")
        lines.append(f"- **Issues in theme:** {len(bucket)}")
        lines.append(f"- **Narrative:** {theme_narrative_paragraph([summary(x) for x in bucket])}")
        lines.append("")

        if len(bucket) >= args.large_theme_threshold:
            epic_counts: Counter = Counter()
            for x in bucket:
                ek = epic_key_for(x, epic_field) or "_no_epic_"
                epic_counts[ek] += 1
            lines.append("**Epic quick list (count):**")
            for ek, cnt in epic_counts.most_common():
                label = epic_titles.get(ek, ek) if ek != "_no_epic_" else "(no epic)"
                lines.append(f"- `{ek}` — {label[:80]}{'…' if len(label) > 80 else ''} — **{cnt}**")
            lines.append("")

        by_epic: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for x in bucket:
            ek = epic_key_for(x, epic_field) or "_no_epic_"
            by_epic[ek].append(x)

        epic_order = sorted(by_epic.keys(), key=lambda k: (k == "_no_epic_", k))

        for ek in epic_order:
            epic_issues = sorted(by_epic[ek], key=issue_key)
            if args.max_issues_per_theme > 0 and len(epic_issues) > args.max_issues_per_theme:
                main_slice = epic_issues[: args.max_issues_per_theme]
                overflow = epic_issues[args.max_issues_per_theme :]
            else:
                main_slice = epic_issues
                overflow = []

            if ek == "_no_epic_":
                lines.append("#### Issues without epic link")
            else:
                et = epic_titles.get(ek, ek)
                lines.append(f"#### Epic `{ek}` — {et}")
            lines.append("")
            lines.append(
                "| Key | Summary | Status | Priority | Sprint | Assignee | Description (snippet) |"
            )
            lines.append("|-----|---------|--------|----------|--------|----------|-------------------------|")
            for x in main_slice:
                lines.append(render_issue_table_row(host, x, args.max_desc_chars, args.redact_assignees))
                covered_keys.add(issue_key(x))
            lines.append("")

            if overflow:
                appendix.append(
                    f"### Appendix overflow: {display_theme} / `{ek}` ({len(overflow)} issues)\n"
                )
                appendix.append(
                    "| Key | Summary | Status | Priority | Sprint | Assignee | Description (snippet) |\n"
                )
                appendix.append(
                    "|-----|---------|--------|----------|--------|----------|-------------------------|\n"
                )
                for x in overflow:
                    appendix.append(
                        render_issue_table_row(
                            host, x, args.max_desc_chars, args.redact_assignees
                        )
                    )
                    covered_keys.add(issue_key(x))
                appendix.append("\n")

    missing = [issue_key(x) for x in issues if issuetype(x).lower() != "epic" and issue_key(x) not in covered_keys]
    if missing:
        lines.append("## Coverage check")
        lines.append("")
        lines.append(f"**Missing from themes (unexpected):** {', '.join(missing[:50])}")
        lines.append("")

    if appendix:
        lines.append("## Appendix (theme overflow)")
        lines.append("")
        lines.extend(appendix)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(out_path, file=sys.stderr)


if __name__ == "__main__":
    main()
