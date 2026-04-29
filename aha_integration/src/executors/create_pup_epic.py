#!/usr/bin/env python3
"""
Create a launch-type Public Preview (PuP) Celonis Epic linked to a parent Celonis Feature.
Usage: python create_pup_epic.py <parent_epic_ref> [--release-month YYYY-MM]
Example: python create_pup_epic.py DEVEX-E-42 --release-month 2026-07
"""

import argparse
import os
import re
import sys
from typing import Optional

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


def find_july_release(client: AhaApiClient, product_id: str, year: int = 2026) -> Optional[dict]:
    """Find a release in July of the given year for the product."""
    page = 1
    total_pages = 1
    july_pattern = re.compile(r"2026[-.]?07|july\s*2026", re.I)

    while page <= total_pages:
        res = client.get(
            f"/products/{product_id}/releases",
            params={"page": str(page), "per_page": "100"},
        )
        releases = res.get("releases", [])
        pagination = res.get("pagination", {})
        total_pages = pagination.get("total_pages", 1)

        for r in releases:
            ref = r.get("reference_num", "")
            name = r.get("name", "")
            start = r.get("start_date") or ""
            end = r.get("end_date") or ""
            # Match July 2026 by name or date
            if july_pattern.search(name) or july_pattern.search(ref):
                return r
            if start and start.startswith(f"{year}-07"):
                return r
            if end and end.startswith(f"{year}-07"):
                return r

        page += 1

    return None


def main():
    parser = argparse.ArgumentParser(description="Create PuP epic linked to parent Celonis Feature")
    parser.add_argument("parent_ref", help="Parent epic reference_num (e.g. DEVEX-E-42)")
    parser.add_argument("--release-month", default="2026-07", help="Release month YYYY-MM (default: 2026-07)")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without creating")
    args = parser.parse_args()

    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("Missing AHA_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    client = AhaApiClient(api_key)
    parent_ref = args.parent_ref.strip().upper()

    # 1. Fetch parent epic (Celonis Feature)
    print(f"Fetching parent epic {parent_ref}...")
    try:
        epic_res = client.get(f"/epics/{parent_ref}")
        parent_epic = epic_res.get("epic", epic_res)
    except Exception as e:
        print(f"Failed to fetch epic {parent_ref}: {e}", file=sys.stderr)
        sys.exit(1)

    parent_name = parent_epic.get("name", "Unknown")
    parent_release = parent_epic.get("release") or {}
    if isinstance(parent_release, dict):
        product = parent_release.get("product") or {}
    else:
        product = {}
    product_id = product.get("id") or product.get("reference_num") or ""

    # Get product from epic's product if available
    if not product_id and parent_epic.get("product"):
        product_id = parent_epic["product"].get("id") or parent_epic["product"].get("reference_num")

    # Fallback: derive from reference_num (e.g. DEVEX-E-42 -> DEVEX)
    if not product_id:
        product_id = parent_ref.split("-")[0] if "-" in parent_ref else "DEVEX"

    # 2. Find July 2026 release
    year = int(args.release_month.split("-")[0])
    print(f"Searching for {args.release_month} release in product {product_id}...")
    release = find_july_release(client, product_id, year)

    if not release:
        print(f"No July {year} release found for product {product_id}.", file=sys.stderr)
        print("Please create a July 2026 release in Aha! first, or specify --release-month.", file=sys.stderr)
        sys.exit(1)

    release_ref = release.get("reference_num")
    release_id = release.get("id") or release_ref
    print(f"Using release: {release_ref}")

    # 3. Build feature payload (Celonis Epic = Aha! Feature)
    feature_name = f"[PuP] {parent_name}"
    description = f"<p>Public Preview phase for {parent_name}. Parent: {parent_ref}</p>"

    payload = {
        "feature": {
            "name": feature_name,
            "description": description,
            "release": release_ref,
            "epic": parent_ref,
            "custom_fields": {
                "launch_type": "PuP",
            },
        }
    }

    if args.dry_run:
        print("\n[DRY RUN] Would POST to /releases/{}/features:".format(release_id))
        import json
        print(json.dumps(payload, indent=2))
        return

    # 4. Create the feature
    print(f"\nCreating PuP epic: {feature_name}")
    try:
        result = client.post(f"/releases/{release_id}/features", payload)
        created = result.get("feature", result)
        ref = created.get("reference_num", "?")
        print(f"Created: {ref} - {created.get('name', '')}")
        print(f"URL: https://celonis.aha.io/features/{ref}")
    except Exception as e:
        print(f"Failed to create feature: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            try:
                print(f"Response body: {e.response.text}", file=sys.stderr)
            except Exception:
                pass
        sys.exit(1)


if __name__ == "__main__":
    main()
