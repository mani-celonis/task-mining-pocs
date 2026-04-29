"""
Fetch Feature Suggestions assigned to the current PM and cross-reference
them against the PM's product backlog.

Config-driven: reads .aha-config.yml for user_email, product_key,
products, and suggestion_portal. Reads .env for AHA_API_KEY only.

Outputs structured JSON to stdout for the agent to process.
"""

import json
import os
import sys
import time
from collections import Counter

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from dotenv import load_dotenv

from src.api.client import AhaApiClient
from src.lib.aha_helpers import (
    THROTTLE_BATCH,
    THROTTLE_SLEEP,
    build_idf,
    fetch_backlog,
    keyword_match,
    paginate,
    strip_html,
)

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
CONFIG_PATH = os.path.join(REPO_ROOT, ".aha-config.yml")
AHA_BASE_URL = "https://celonis.aha.io"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(
            "ERROR: .aha-config.yml not found. "
            "Run the onboarding skill or setup wizard first.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    missing = []
    if not config.get("user_email"):
        missing.append("user_email")
    if not config.get("product_key"):
        missing.append("product_key")
    if not config.get("suggestion_portal") or not config["suggestion_portal"].get(
        "product_key"
    ):
        missing.append("suggestion_portal.product_key")

    if missing:
        print(
            f"ERROR: .aha-config.yml is missing required fields: {', '.join(missing)}. "
            "See .aha-config.example.yml for the expected format.",
            file=sys.stderr,
        )
        sys.exit(1)

    return config


def fetch_suggestions(client, portal_key, review_status):
    """Paginate through all ideas in the suggestion portal with the given status."""
    ideas = []
    for idea in paginate(
        client,
        f"/products/{portal_key}/ideas",
        "ideas",
        extra_params={"workflow_status": review_status},
    ):
        ideas.append(
            {
                "ref": idea.get("reference_num", ""),
                "name": idea.get("name", ""),
                "id": idea.get("id"),
            }
        )
    return ideas


def fetch_idea_detail(client, ref):
    """Fetch full detail for a single idea."""
    resp = client.get(f"/ideas/{ref}")
    return resp.get("idea", resp)


def fetch_record_links(client, idea_id):
    """Fetch record links for an idea (requires numeric ID)."""
    try:
        resp = client.get(f"/ideas/{idea_id}/record_links")
        return resp.get("record_links", [])
    except Exception:
        return []


def main():
    config = load_config()
    load_dotenv(os.path.join(REPO_ROOT, ".env"))

    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("ERROR: AHA_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)

    client = AhaApiClient(api_key)

    user_email = config["user_email"].lower()
    product_key = config["product_key"]
    portal = config["suggestion_portal"]
    portal_key = portal["product_key"]
    review_status = portal.get("review_status", "In Review")
    category_names = {
        p.get("category", "").lower() for p in config.get("products", []) if p.get("category")
    }

    # Step 1: list suggestions
    print(
        f"Fetching suggestions from {portal_key} with status '{review_status}'...",
        file=sys.stderr,
    )
    all_suggestions = fetch_suggestions(client, portal_key, review_status)
    print(f"  Found {len(all_suggestions)} suggestions total.", file=sys.stderr)

    if not all_suggestions:
        print(
            json.dumps(
                {
                    "suggestions": [],
                    "backlog_item_count": 0,
                    "note": (
                        f"No suggestions found with status '{review_status}' in product {portal_key}. "
                        "Verify that review_status in .aha-config.yml matches your Aha! workflow."
                    ),
                }
            )
        )
        return

    # Step 2: fetch detail per suggestion, filter by assignee
    print("Fetching details and filtering by assignee...", file=sys.stderr)
    mine = []
    request_count = 0
    for s in all_suggestions:
        if request_count > 0 and request_count % THROTTLE_BATCH == 0:
            time.sleep(THROTTLE_SLEEP)
        try:
            detail = fetch_idea_detail(client, s["ref"])
        except Exception as e:
            print(f"  Warning: failed to fetch {s['ref']}: {e}", file=sys.stderr)
            request_count += 1
            continue
        request_count += 1

        assigned = detail.get("assigned_to_user") or {}
        assigned_email = (assigned.get("email") or "").lower()
        if assigned_email != user_email:
            continue

        description_raw = detail.get("description", "")
        description_plain = strip_html(description_raw)

        categories = detail.get("categories", []) or []
        cat_names = [c.get("name", "") for c in categories if isinstance(c, dict)]

        votes = detail.get("votes", 0)
        created_by = (
            detail.get("created_by_portal_user")
            or detail.get("created_by_idea_user")
            or detail.get("created_by_user")
            or {}
        )

        mine.append(
            {
                "ref": s["ref"],
                "id": detail.get("id"),
                "name": detail.get("name", s["name"]),
                "description": description_plain,
                "url": f"{AHA_BASE_URL}/ideas/ideas/{s['ref']}",
                "status": (
                    detail.get("workflow_status", {}).get("name", "Unknown")
                    if isinstance(detail.get("workflow_status"), dict)
                    else str(detail.get("workflow_status", "Unknown"))
                ),
                "created_by": created_by.get("name", "Unknown"),
                "votes": votes,
                "categories": cat_names,
            }
        )

    print(f"  {len(mine)} suggestions assigned to {user_email}.", file=sys.stderr)

    # Step 3: fetch record_links per suggestion
    print("Fetching record links...", file=sys.stderr)
    for i, s in enumerate(mine):
        if i > 0 and i % THROTTLE_BATCH == 0:
            time.sleep(THROTTLE_SLEEP)
        links = fetch_record_links(client, s["id"])
        s["linked_records"] = []
        for link in links:
            record = link.get("record", {})
            s["linked_records"].append(
                {
                    "ref": record.get("reference_num", ""),
                    "name": record.get("name", ""),
                    "type": record.get("type", ""),
                    "link_type": link.get("link_type_name", ""),
                }
            )

    # Step 4: fetch PM's backlog (epics + features + ideas)
    print(f"Fetching backlog for product {product_key}...", file=sys.stderr)
    backlog = fetch_backlog(client, product_key)
    type_counts = Counter(item["type"] for item in backlog)
    print(
        f"  {len(backlog)} backlog items loaded "
        f"(epics={type_counts.get('epic', 0)}, "
        f"features={type_counts.get('feature', 0)}, "
        f"ideas={type_counts.get('idea', 0)}).",
        file=sys.stderr,
    )

    # Step 5: keyword match (IDF-weighted) and category overlap
    print("Matching suggestions against backlog...", file=sys.stderr)
    idf = build_idf(backlog)
    for s in mine:
        search_text = f"{s['name']} {s['description']}"
        s["backlog_matches"] = keyword_match(search_text, backlog, idf)
        s["category_overlap"] = [
            c for c in s["categories"] if c.lower() in category_names
        ]
        word_count = len(s["description"].split())
        s["has_enough_context"] = word_count >= 50

    output = {
        "user_email": user_email,
        "product_key": product_key,
        "suggestion_portal": portal_key,
        "review_status": review_status,
        "suggestions": mine,
        "backlog_item_count": len(backlog),
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
