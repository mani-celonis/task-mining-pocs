#!/usr/bin/env python3
"""
Pull Aha feature suggestions assigned to a user and save a dated local snapshot.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))
os.chdir(_PROJECT_ROOT)

from dotenv import load_dotenv

from api.client import AhaApiClient
from pm_data_paths import incoming_feature_suggestions_dir

DEFAULT_ASSIGNEE = "Frederik Chettouh"
DEFAULT_WORKSPACE_KEY = "SUGGESTION"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull Aha feature suggestions assigned to a user and save a local snapshot."
    )
    parser.add_argument("--assignee", default=None, help="Assignee name or email fragment")
    parser.add_argument("--output-dir", default=None, help="Directory for saved snapshots")
    parser.add_argument(
        "--workspace-key",
        default=None,
        help="Aha Feature Suggestions workspace key used by /products/{key}/ideas",
    )
    parser.add_argument("--status", default=None, help="Only include items with this status name")
    parser.add_argument("--limit", type=int, default=None, help="Limit saved results after filtering")
    return parser.parse_args()


def load_feature_request_config(config_path: str) -> Dict[str, str]:
    if not os.path.exists(config_path):
        return {}

    config: Dict[str, str] = {}
    in_feature_requests = False

    with open(config_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                continue

            if not line.startswith(" ") and stripped.endswith(":"):
                in_feature_requests = stripped[:-1] == "feature_requests"
                continue

            if not in_feature_requests or not line.startswith("  "):
                continue

            key, sep, value = stripped.partition(":")
            if not sep:
                continue

            value = value.strip().strip("'\"")
            config[key.strip()] = value

    return config


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "report"


def html_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        if "body" in value:
            return html_to_text(value.get("body"))
        return html_to_text(json.dumps(value))
    if not isinstance(value, str):
        return str(value)

    text = unescape(value)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    return text.strip()


def snippet(text: str, max_chars: int = 400) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 3].rstrip() + "..."


def matches_assignee(assigned_to_user: Any, assignee_query: str) -> bool:
    if not assigned_to_user:
        return False

    needle = assignee_query.lower()
    if isinstance(assigned_to_user, str):
        return needle in assigned_to_user.lower()

    name = str(assigned_to_user.get("name") or "").lower()
    email = str(assigned_to_user.get("email") or "").lower()
    return needle in name or needle in email


def status_name(item: Dict[str, Any]) -> str:
    status = item.get("workflow_status") or item.get("status") or {}
    if isinstance(status, dict):
        return status.get("name") or "Unknown"
    if isinstance(status, str) and status:
        return status
    return "Unknown"


def person_name(value: Any, default: str = "Unknown") -> str:
    if isinstance(value, dict):
        return value.get("name") or value.get("email") or default
    if isinstance(value, str) and value:
        return value
    return default


def item_url(ref: str, item: Dict[str, Any]) -> str:
    return item.get("url") or f"https://celonis.aha.io/ideas/{ref}"


def iter_idea_refs(client: AhaApiClient, workspace_key: str) -> Iterable[Dict[str, Any]]:
    page = 1
    total_pages = 1

    while page <= total_pages:
        resp = client.get(
            f"/products/{workspace_key}/ideas",
            params={
                "page": str(page),
                "per_page": "200",
                "fields": "reference_num,name,assigned_to_user,workflow_status",
            },
        )
        ideas = resp.get("ideas", [])
        for idea in ideas:
            yield idea

        pagination = resp.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)
        page += 1


def fetch_detail(client: AhaApiClient, ref: str) -> Dict[str, Any]:
    resp = client.get(f"/ideas/{ref}")
    return resp.get("idea", resp)


def normalize_item(detail: Dict[str, Any]) -> Dict[str, Any]:
    ref = detail.get("reference_num") or "?"
    description_raw = detail.get("description") or ""
    description_text = html_to_text(description_raw)
    created_by = (
        detail.get("created_by_user")
        or detail.get("created_by")
        or detail.get("created_by_idea_user")
        or detail.get("created_by_portal_user")
    )
    return {
        "reference_num": ref,
        "name": detail.get("name") or "",
        "url": item_url(ref, detail),
        "status": status_name(detail),
        "assigned_to": person_name(detail.get("assigned_to_user")),
        "created_by": person_name(created_by),
        "created_at": detail.get("created_at") or "",
        "updated_at": detail.get("updated_at") or "",
        "description_raw": description_raw,
        "description_text": description_text,
    }


def sort_key(item: Dict[str, Any]) -> str:
    return item.get("updated_at") or item.get("created_at") or ""


def render_markdown(
    items: List[Dict[str, Any]],
    pulled_at: str,
    assignee: str,
    workspace_key: str,
    status_filter: Optional[str],
) -> str:
    counts = Counter(item["status"] for item in items)
    lines = [
        "# Feature Suggestions Snapshot",
        "",
        f"- Pulled at: {pulled_at}",
        f"- Assignee: {assignee}",
        f"- Workspace key: {workspace_key}",
        f"- Total: {len(items)}",
    ]

    if status_filter:
        lines.append(f"- Status filter: {status_filter}")

    lines.extend(["", "## Count By Status", ""])

    if counts:
        for name, count in sorted(counts.items()):
            lines.append(f"- {name}: {count}")
    else:
        lines.append("- No matching feature suggestions")

    lines.extend(["", "## Newest Updated", ""])
    newest = sorted(items, key=sort_key, reverse=True)[:10]
    if newest:
        for item in newest:
            updated_at = item["updated_at"] or item["created_at"] or "Unknown"
            lines.append(
                f"- [{item['reference_num']}]({item['url']}) — {item['name']} ({item['status']}, {updated_at})"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Suggestions", ""])
    if not items:
        lines.append("No matching feature suggestions.")
        return "\n".join(lines) + "\n"

    for item in items:
        lines.extend(
            [
                f"### {item['reference_num']} — {item['name']}",
                "",
                f"- Status: {item['status']}",
                f"- Assigned to: {item['assigned_to']}",
                f"- Created by: {item['created_by']}",
                f"- Created at: {item['created_at'] or 'Unknown'}",
                f"- Updated at: {item['updated_at'] or 'Unknown'}",
                f"- Link: {item['url']}",
                "",
                snippet(item["description_text"]) or "No description available.",
                "",
            ]
        )

    return "\n".join(lines)


def write_outputs(output_root: str, assignee: str, payload: Dict[str, Any]) -> Dict[str, str]:
    date_part = payload["pulled_at"][:10]
    out_dir = Path(output_root) / date_part
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = slugify(assignee)
    markdown_path = out_dir / f"feature-suggestions-{slug}.md"
    json_path = out_dir / f"feature-suggestions-{slug}.json"

    markdown_body = render_markdown(
        payload["items"],
        payload["pulled_at"],
        payload["assignee"],
        payload["workspace_key"],
        payload.get("status_filter"),
    )

    markdown_path.write_text(markdown_body, encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return {"markdown": str(markdown_path), "json": str(json_path)}


def build_payload(
    items: List[Dict[str, Any]],
    assignee: str,
    workspace_key: str,
    status_filter: Optional[str],
) -> Dict[str, Any]:
    return {
        "pulled_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "assignee": assignee,
        "workspace_key": workspace_key,
        "status_filter": status_filter,
        "total": len(items),
        "items": items,
    }


def main() -> int:
    args = parse_args()
    load_dotenv()
    config = load_feature_request_config(os.path.join(_PROJECT_ROOT, ".aha-config.yml"))

    assignee = args.assignee or config.get("assignee") or DEFAULT_ASSIGNEE
    output_dir = args.output_dir or config.get("output_dir") or str(incoming_feature_suggestions_dir())
    workspace_key = args.workspace_key or config.get("workspace_key") or DEFAULT_WORKSPACE_KEY
    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("Missing AHA_API_KEY in .env", file=sys.stderr)
        return 1

    client = AhaApiClient(api_key)

    matching_refs: List[str] = []
    for idea in iter_idea_refs(client, workspace_key):
        if matches_assignee(idea.get("assigned_to_user"), assignee):
            ref = idea.get("reference_num") or ""
            if ref:
                matching_refs.append(ref)

    items: List[Dict[str, Any]] = []
    for ref in matching_refs:
        if not ref:
            continue

        detail = fetch_detail(client, ref)
        normalized = normalize_item(detail)
        if args.status and normalized["status"].lower() != args.status.lower():
            continue
        items.append(normalized)

    items.sort(key=sort_key, reverse=True)
    if args.limit is not None:
        items = items[: args.limit]

    payload = build_payload(items, assignee, workspace_key, args.status)
    output_paths = write_outputs(output_dir, assignee, payload)

    print(f"Saved {payload['total']} feature suggestion(s) for {assignee}.")
    print(f"Markdown: {output_paths['markdown']}")
    print(f"JSON: {output_paths['json']}")
    if items:
        print("Top refs:")
        for item in items[:10]:
            print(f"  {item['reference_num']}  {item['status']}  {item['name']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
