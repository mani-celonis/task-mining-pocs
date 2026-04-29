"""
Cross-reference meeting discussion topics with Aha! Ideas.

Reference implementation. The AI assistant writes a version of this script
into src/executors/scratchpad.py at runtime, customized with keywords
extracted from the meeting being processed.

Uses helpers from src.lib.aha_helpers so the script stays short — pagination,
detail fetches with throttling, and category lookups all live in the shared
library. For ad-hoc one-shot reads, prefer `python -m src.cli get ...`.

CONFIGURE: Set PRODUCT_KEY and RELEVANT_CATEGORIES to match your Aha!
workspace before running manually. When the AI runs this via the scratchpad
pattern, it fills these values automatically from cursor-rule-aha-agent.mdc.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from dotenv import load_dotenv

from src.api.client import AhaApiClient
from src.lib.aha_helpers import fetch_all_ideas, fetch_ideas_with_categories

load_dotenv()
client = AhaApiClient(os.getenv("AHA_API_KEY"))

# ---------------------------------------------------------------------------
# CONFIGURE: Replace these with your own values
# ---------------------------------------------------------------------------

PRODUCT_KEY = "<YOUR_PRODUCT_KEY>"  # e.g. "OPER", "AIMODULES"

RELEVANT_CATEGORIES = {
    # Lowercase Aha! Idea category names for your product.
    # Used to filter Ideas to only those in your domain.
    # e.g. {"forms", "triggers", "tasks", "notifications"}
}

MEETING_KEYWORDS = [
    # Keywords extracted from the meeting's discussion points and action items.
    # The AI populates these at runtime; for manual runs, add your own.
    # Use lowercase partial stems for broader matching (e.g. "migrat" matches
    # "migration", "migrating", "migrate").
]

# ---------------------------------------------------------------------------
# 1. List all Ideas (fast, list-endpoint only — no detail calls)
# ---------------------------------------------------------------------------

print(f"Fetching ideas for product {PRODUCT_KEY}...")
ideas = fetch_all_ideas(client, PRODUCT_KEY)
print(f"Total ideas: {len(ideas)}")

# ---------------------------------------------------------------------------
# 2. First-pass keyword match on Idea names
# ---------------------------------------------------------------------------

name_matched = []
for idea in ideas:
    name = idea.get("name", "")
    name_lower = name.lower()
    hits = [kw for kw in MEETING_KEYWORDS if kw in name_lower]
    if hits:
        name_matched.append((idea.get("reference_num"), name, hits))

print(f"\nName-matched ideas: {len(name_matched)}")
print("Fetching details for category filtering...\n")

# ---------------------------------------------------------------------------
# 3. Second-pass detail fetch for categories (auto-throttled)
# ---------------------------------------------------------------------------

hits_by_ref = {ref: hits for ref, _, hits in name_matched}
name_by_ref = {ref: name for ref, name, _ in name_matched}
details = fetch_ideas_with_categories(client, [ref for ref, _, _ in name_matched])

results = []
for idea in details:
    ref = idea.get("reference_num")
    cats = [
        c.get("name", "")
        for c in (idea.get("categories", []) or [])
        if isinstance(c, dict)
    ]
    cats_lower = {c.lower() for c in cats}
    status = idea.get("workflow_status", {}).get("name", "?")
    hits = hits_by_ref.get(ref, [])

    in_relevant_category = bool(cats_lower & RELEVANT_CATEGORIES)
    if in_relevant_category or len(hits) >= 2:
        results.append(
            {
                "ref": ref,
                "name": name_by_ref.get(ref, idea.get("name", "")),
                "status": status,
                "categories": cats,
                "keywords": hits,
            }
        )

results.sort(key=lambda x: len(x["keywords"]), reverse=True)

# ---------------------------------------------------------------------------
# 4. Output
# ---------------------------------------------------------------------------

print(f"Matched ideas: {len(results)}\n")
for r in results[:15]:
    cat_str = ", ".join(r["categories"]) if r["categories"] else "—"
    kw_str = ", ".join(r["keywords"][:3])
    print(f"  {r['ref']:<20} [{r['status']:<20}] {r['name'][:65]}")
    print(f"  {'':20} cats: {cat_str} | matched: {kw_str}")
