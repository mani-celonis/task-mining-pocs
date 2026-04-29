#!/usr/bin/env python3
"""
Pull Jira issues via JQL search (preferred for PM scope) or Agile board, group by epic,
print Markdown + optional JSON.

Requires in .env:
  JIRA_HOST, JIRA_EMAIL, JIRA_API_TOKEN

  One of:
  - JIRA_JQL              recommended: TM + sprint/backlog slice (see .env.example)
  - JIRA_JQL_PATH         path to .jql file under repo (e.g. data/jira-jql/ml-infra.jql)
  - JIRA_BOARD_ID         fallback: full board issue list

  JIRA_JQL overrides JIRA_JQL_PATH when both are set.

Usage:
  python src/executors/jira_board_overview.py
  python src/executors/jira_board_overview.py --json
  python src/executors/jira_board_overview.py --jql 'project = TM AND ...'
  python src/executors/jira_board_overview.py --json --extra-fields   # + description, sprint (for PM brief)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_project_root, "src"))
os.chdir(_project_root)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    env_path = os.path.join(_project_root, ".env")
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from api.jira_client import JiraApiClient, normalize_jira_host


def find_epic_link_field_id(fields: List[Dict[str, Any]]) -> Optional[str]:
    for f in fields:
        if (f.get("name") or "").strip().lower() == "epic link":
            return f.get("id")
    return None


def issue_type_name(issue: Dict[str, Any]) -> str:
    it = issue.get("fields", {}).get("issuetype") or {}
    return (it.get("name") or "?").strip()


def issue_key(issue: Dict[str, Any]) -> str:
    return issue.get("key") or "?"


def issue_summary(issue: Dict[str, Any]) -> str:
    return (issue.get("fields", {}).get("summary") or "").strip() or "(no summary)"


def status_name(issue: Dict[str, Any]) -> str:
    st = issue.get("fields", {}).get("status") or {}
    return (st.get("name") or "?").strip()


def assignee_display(issue: Dict[str, Any]) -> str:
    a = issue.get("fields", {}).get("assignee")
    if not a:
        return "Unassigned"
    return (a.get("displayName") or a.get("emailAddress") or a.get("accountId") or "?").strip()


def epic_key_from_fields(
    issue: Dict[str, Any], epic_link_field_id: Optional[str]
) -> Optional[str]:
    if epic_link_field_id:
        raw = (issue.get("fields") or {}).get(epic_link_field_id)
        if isinstance(raw, dict) and raw.get("key"):
            return str(raw["key"])
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    p = (issue.get("fields") or {}).get("parent")
    if isinstance(p, dict) and p.get("key"):
        pit = (p.get("fields") or {}).get("issuetype") or {}
        if (pit.get("name") or "").lower() == "epic":
            return str(p["key"])
    return None


def browse_url(host: str, key: str) -> str:
    base = normalize_jira_host(host).rstrip("/")
    return f"{base}/browse/{key}"


def read_jql_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        parts = []
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            parts.append(s)
        return " ".join(parts).strip()


def resolve_jql(cli_jql: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Returns (jql, path_used_or_none). CLI wins over JIRA_JQL env over JIRA_JQL_PATH file.
    """
    if cli_jql and cli_jql.strip():
        return cli_jql.strip(), None
    env_jql = (os.getenv("JIRA_JQL") or "").strip()
    if env_jql:
        return env_jql, None
    path_raw = (os.getenv("JIRA_JQL_PATH") or "").strip()
    if path_raw:
        p = path_raw if os.path.isabs(path_raw) else os.path.join(_project_root, path_raw)
        if os.path.isfile(p):
            q = read_jql_file(p)
            if q:
                return q, p
    return None, None


def fetch_board_issues(
    client: JiraApiClient, board_id: str, field_ids: List[str]
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    start = 0
    max_results = 100
    fields_param = ",".join(field_ids)
    while True:
        data = client.get(
            f"/rest/agile/1.0/board/{board_id}/issue",
            params={
                "startAt": start,
                "maxResults": max_results,
                "fields": fields_param,
            },
        )
        issues = data.get("issues") or []
        out.extend(issues)
        total = int(data.get("total", len(out)))
        start += len(issues)
        if start >= total or not issues:
            break
    return out


def build_epic_groups(
    issues: List[Dict[str, Any]],
    epic_link_field_id: Optional[str],
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Dict[str, Any]], List[Dict[str, Any]]]:
    epic_issues: Dict[str, Dict[str, Any]] = {}
    children_by_epic: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    no_epic: List[Dict[str, Any]] = []

    for issue in issues:
        k = issue_key(issue)
        itn = issue_type_name(issue)
        if itn.lower() == "epic":
            epic_issues[k] = issue
            continue

        ek = epic_key_from_fields(issue, epic_link_field_id)
        if ek:
            children_by_epic[ek].append(issue)
            continue

        no_epic.append(issue)

    return dict(children_by_epic), epic_issues, no_epic


def render_markdown(
    host: str,
    scope_title: str,
    epic_issues: Dict[str, Dict[str, Any]],
    children_by_epic: Dict[str, List[Dict[str, Any]]],
    no_epic: List[Dict[str, Any]],
    issue_count: int,
) -> str:
    lines: List[str] = []
    lines.append(f"# Jira overview ({scope_title})")
    lines.append("")
    lines.append(f"- **Issues in scope:** {issue_count}")
    lines.append(f"- Epics in result set: {len(epic_issues)}")
    lines.append(f"- Issues with epic link / parent epic: {sum(len(v) for v in children_by_epic.values())}")
    lines.append(f"- Issues without epic grouping: {len(no_epic)}")
    lines.append("")

    all_epic_keys = sorted(set(epic_issues.keys()) | set(children_by_epic.keys()))
    for ek in all_epic_keys:
        epic = epic_issues.get(ek)
        title = issue_summary(epic) if epic else "(epic not in result — linked issues only)"
        lines.append(f"## Epic {ek}: {title}")
        lines.append("")
        if epic:
            lines.append(
                f"- Status: {status_name(epic)} | {browse_url(host, ek)}"
            )
            lines.append("")
        for ch in sorted(children_by_epic.get(ek, []), key=issue_key):
            lines.append(
                f"- **{issue_key(ch)}** — {issue_summary(ch)}  "
                f"({status_name(ch)}; {assignee_display(ch)})  "
                f"[link]({browse_url(host, issue_key(ch))})"
            )
        if not children_by_epic.get(ek):
            lines.append("_No child issues in scope with Epic Link to this epic._")
        lines.append("")

    if no_epic:
        lines.append("## Not linked to an epic (in this result set)")
        lines.append("")
        for issue in sorted(no_epic, key=issue_key):
            lines.append(
                f"- **{issue_key(issue)}** — {issue_summary(issue)}  "
                f"({status_name(issue)}; {assignee_display(issue)})  "
                f"[link]({browse_url(host, issue_key(issue))})"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Jira overview via JQL or board (read-only)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON to stdout",
    )
    parser.add_argument(
        "--also-markdown",
        action="store_true",
        help="After JSON, print Markdown (use with --json)",
    )
    parser.add_argument(
        "--jql",
        type=str,
        default=None,
        help="Override JIRA_JQL / JIRA_JQL_PATH for this run",
    )
    parser.add_argument(
        "--extra-fields",
        action="store_true",
        help="Request description (ADF) and sprint — larger payloads; use with jira_pm_brief_generate.py",
    )
    args = parser.parse_args()

    host = (os.getenv("JIRA_HOST") or "").strip()
    email = (os.getenv("JIRA_EMAIL") or "").strip()
    token = (os.getenv("JIRA_API_TOKEN") or "").strip()
    board_id = (os.getenv("JIRA_BOARD_ID") or "").strip()

    base_missing = [
        n
        for n, v in (
            ("JIRA_HOST", host),
            ("JIRA_EMAIL", email),
            ("JIRA_API_TOKEN", token),
        )
        if not v
    ]
    if base_missing:
        print("Set in .env: " + ", ".join(base_missing), file=sys.stderr)
        sys.exit(1)

    jql, jql_path_used = resolve_jql(args.jql)
    source: str
    scope_title: str
    board_id_out: Optional[str] = None
    jql_out: Optional[str] = None

    client = JiraApiClient(host, email, token)
    try:
        all_fields = client.get_fields()
    except Exception as e:
        print(f"Failed to load Jira fields (check host, email, token): {e}", file=sys.stderr)
        sys.exit(1)

    epic_link_id = find_epic_link_field_id(all_fields)
    base_field_ids = [
        "summary",
        "status",
        "issuetype",
        "priority",
        "assignee",
        "labels",
        "components",
        "parent",
        "created",
        "updated",
    ]
    field_ids = base_field_ids + ([epic_link_id] if epic_link_id else [])
    extra_fields = args.extra_fields or (os.getenv("JIRA_EXTRA_FIELDS") or "").strip().lower() in (
        "1",
        "true",
        "yes",
    )
    if extra_fields:
        for fid in ("description", "sprint"):
            if fid not in field_ids:
                field_ids.append(fid)

    try:
        if jql:
            issues = client.search_issues(jql, field_ids)
            source = "jql"
            jql_out = jql
            scope_title = "JQL search"
            if len(jql) <= 100:
                scope_title = f"JQL: {jql}"
            else:
                scope_title = f"JQL ({len(issues)} issues)"
        elif board_id:
            issues = fetch_board_issues(client, board_id, field_ids)
            source = "board"
            board_id_out = board_id
            scope_title = f"board {board_id}"
        else:
            print(
                "Set one of: JIRA_JQL, JIRA_JQL_PATH (file), or JIRA_BOARD_ID — "
                "or pass --jql '...'. See .env.example.",
                file=sys.stderr,
            )
            sys.exit(1)
    except Exception as e:
        print(f"Failed to fetch issues: {e}", file=sys.stderr)
        sys.exit(1)

    children_by_epic, epic_issues, no_epic = build_epic_groups(issues, epic_link_id)

    payload: Dict[str, Any] = {
        "source": source,
        "jira_host": normalize_jira_host(host),
        "extra_fields": extra_fields,
        "epic_link_field_id": epic_link_id,
        "totals": {
            "issues": len(issues),
            "epic_issues": len(epic_issues),
            "with_epic_link": sum(len(v) for v in children_by_epic.values()),
            "without_epic_link": len(no_epic),
        },
        "epic_keys": sorted(set(epic_issues.keys()) | set(children_by_epic.keys())),
        "issues": issues,
    }
    if board_id_out is not None:
        payload["board_id"] = board_id_out
    if jql_out is not None:
        payload["jql"] = jql_out
    if jql_path_used:
        payload["jql_path"] = jql_path_used

    md = render_markdown(
        host, scope_title, epic_issues, children_by_epic, no_epic, len(issues)
    )

    if args.json:
        print(json.dumps(payload, indent=2))
    if not args.json or args.also_markdown:
        if args.json and args.also_markdown:
            print()
        print(md, end="" if md.endswith("\n") else "\n")


if __name__ == "__main__":
    main()
