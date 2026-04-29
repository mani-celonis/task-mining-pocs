#!/usr/bin/env python3
"""
List Celonis Epics (Aha! Features) assigned to a user that have no Jira epic linked.
Usage: python check_missing_jira.py [assignee_name_or_email]
"""

import os
import sys

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_project_root, "src"))
os.chdir(_project_root)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = os.path.join(_project_root, ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from api.client import AhaApiClient


def matches_assignee(assigned_to_user, search: str) -> bool:
    """Check if assigned_to_user matches the search string (name or email)."""
    if not assigned_to_user:
        return False
    search_lower = search.lower()
    if isinstance(assigned_to_user, str):
        return search_lower in assigned_to_user.lower()
    name = (assigned_to_user.get("name") or "").lower()
    email = (assigned_to_user.get("email") or "").lower()
    return search_lower in name or search_lower in email


def has_jira_epic(integration_fields: list) -> bool:
    """Check if integration_fields contains a Jira epic link."""
    if not integration_fields:
        return False
    for field in integration_fields:
        if isinstance(field, dict) and field.get("service_name") == "jira":
            return True
    return False


def main():
    assignee_search = sys.argv[1] if len(sys.argv) > 1 else "Frederik Chettouh"

    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("Missing AHA_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    client = AhaApiClient(api_key)
    fields = "name,reference_num,assigned_to_user,integration_fields,url"

    all_assigned = []
    page = 1
    total_pages = 1

    print(f"Fetching features assigned to '{assignee_search}'...")
    while page <= total_pages:
        res = client.get(
            "/features",
            params={"fields": fields, "page": str(page), "per_page": "100"},
        )
        features = res.get("features", [])
        pagination = res.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)

        for f in features:
            if matches_assignee(f.get("assigned_to_user"), assignee_search):
                all_assigned.append(f)

        page += 1

    no_jira = [f for f in all_assigned if not has_jira_epic(f.get("integration_fields") or [])]

    print(f"\n=== Epics assigned to {assignee_search} with NO Jira epic linked ===\n")
    print(f"Total assigned: {len(all_assigned)}")
    print(f"Missing Jira link: {len(no_jira)}\n")

    if not no_jira:
        print("None found. All assigned epics have a Jira epic linked.")
        return

    for f in no_jira:
        ref = f.get("reference_num", "?")
        name = f.get("name", "")
        url = f.get("url", f"https://celonis.aha.io/features/{ref}")
        print(f"  {ref}  {name[:70]}{'...' if len(name) > 70 else ''}")
        print(f"    {url}")
        print()


if __name__ == "__main__":
    main()
