#!/usr/bin/env python3
"""
Test script: fetches features from Aha! API and prints those assigned to Frederik Chettouh.
"""

import os
import sys

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_project_root, "src"))
os.chdir(_project_root)

from dotenv import load_dotenv

load_dotenv()

from api.client import AhaApiClient

ASSIGNEE_MATCH = "Frederik Chettouh"


def matches_assignee(assigned_to_user) -> bool:
    if not assigned_to_user:
        return False
    if isinstance(assigned_to_user, str):
        return ASSIGNEE_MATCH.lower() in assigned_to_user.lower()
    name = (assigned_to_user.get("name") or "").lower()
    email = (assigned_to_user.get("email") or "").lower()
    return (
        ASSIGNEE_MATCH.lower() in name
        or ASSIGNEE_MATCH.lower() in email
    )


def main():
    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("Missing AHA_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    client = AhaApiClient(api_key)
    all_features = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        res = client.get(
            "/features",
            params={
                "fields": "name,reference_num,assigned_to_user",
                "page": str(page),
                "per_page": "100",
            },
        )
        features = res.get("features", [])
        all_features.extend(features)
        pagination = res.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)
        page += 1

    assigned = [f for f in all_features if matches_assignee(f.get("assigned_to_user"))]

    print("\n--- Features assigned to Frederik Chettouh ---\n")
    if not assigned:
        print("(none found)\n")
        return
    for f in assigned:
        print(f"  {f.get('reference_num', '?')}  {f.get('name', '')}")
    print(f"\nTotal: {len(assigned)} feature(s)\n")


if __name__ == "__main__":
    main()
