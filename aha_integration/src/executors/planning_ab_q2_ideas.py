#!/usr/bin/env python3
"""
Q2 Annotation Builder: fetch AIMODULES Ideas, dedupe against planning candidates, optionally POST.
See plan: Q2 Annotation Builder Ideas (product Ideas, not SUGGESTION workspace).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from difflib import SequenceMatcher
from html import escape
from typing import Any

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_project_root, "src"))
os.chdir(_project_root)

from dotenv import load_dotenv
from api.client import AhaApiClient

# --- Q2 2026 candidates (P0 "Q1 leftovers" excluded per plan) ---

CANDIDATES: list[dict[str, str]] = [
    {
        "name": "Harden PIG writebacks for enterprise scale (GA target)",
        "summary": "Harden writeback infrastructure for enterprise data volumes and unblock GA for GDC and FTG.",
    },
    {
        "name": "GA: Generic Duplicate Checker (GDC) on PIG writebacks",
        "summary": "After writebacks are hardened, migrate GDC onto PIG writebacks and ship GA.",
    },
    {
        "name": "Annotation Builder: failure notifications for automations",
        "summary": "Notify on automated execution failures, unsubscription from recurrent failures, schema/data or GenAI limit issues.",
    },
    {
        "name": "Fixed Annotation Builder version for automated executions",
        "summary": "Let automations run a pinned AB configuration version as Studio/CMP config evolves.",
    },
    {
        "name": "Configurable embedding model for Free Text Grouping (FTG)",
        "summary": "Support model choice for FTG embedding/clustering to cover Omnia/BYOM and customer restrictions (e.g. AWS only).",
    },
    {
        "name": "FTG: persist embeddings for scalability (e.g. Celostar)",
        "summary": "Remove regenerate-on-every-run bottleneck; investigate persisting embeddings for GA-scale FTG.",
    },
    {
        "name": "GDC as a service in ETL (PySpark) — trust annotations in pipeline",
        "summary": "Package GDC for data engineers in PySpark ETL to dedupe and flag before data reaches end-user views.",
    },
    {
        "name": "Chain non-LLM annotations via AF modules or OE",
        "summary": "Integrate all annotations via AF modules or OE for chaining, depending on pipeline builder delivery.",
    },
    {
        "name": "From prompt assistant to full assistant in Annotation Builder",
        "summary": "From one prompt, select data, write instructions, and create output schema to cut time to first annotation.",
    },
]

SIMILARITY_SKIP_THRESHOLD = 0.62
SIMILARITY_DETAIL_THRESHOLD = 0.48
DETAIL_FETCH_BUDGET = 20
DETAIL_EVERY = 15
DETAIL_SLEEP = 1.1
TARGET_CATEGORY = "Annotation Builder"


def read_product_key(config_path: str) -> str:
    with open(config_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("product_key:"):
                return line.split(":", 1)[1].strip().strip("'\"")
    raise ValueError("product_key not found in .aha-config.yml")


def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def fetch_all_ideas(client: AhaApiClient, product_key: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    page = 1
    while True:
        resp = client.get(
            f"/products/{product_key}/ideas",
            params={"per_page": "200", "page": str(page)},
        )
        for idea in resp.get("ideas", []):
            r = idea.get("reference_num") or ""
            n = idea.get("name") or ""
            if r:
                refs.append((r, n))
        total_pages = int(resp.get("pagination", {}).get("total_pages") or 1)
        if page >= total_pages:
            break
        page += 1
    return refs


def best_match(
    title: str, existing: list[tuple[str, str]]
) -> tuple[str | None, str | None, float]:
    nt = normalize(title)
    best_ref, best_name, best_ratio = None, None, 0.0
    for ref, name in existing:
        nn = normalize(name)
        r = SequenceMatcher(a=nt, b=nn).ratio()
        if r > best_ratio:
            best_ratio, best_ref, best_name = r, ref, name
        if nt in nn or nn in nt:
            r2 = max(r, 0.75)
            if r2 > best_ratio:
                best_ratio, best_ref, best_name = r2, ref, name
    return best_ref, best_name, best_ratio


def html_description(name: str, summary: str) -> str:
    return f"<p><strong>{escape(name)}</strong></p><p>{escape(summary)}</p>"


def fetch_idea_detail(client: AhaApiClient, ref: str) -> dict[str, Any]:
    return client.get(f"/ideas/{ref}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create",
        action="store_true",
        help="POST new Ideas for rows that are not likely duplicates (after dry-run review).",
    )
    parser.add_argument(
        "--include-review",
        action="store_true",
        help="Also POST rows in the 'Review' band (0.5–0.62 similarity) when you confirm they are not duplicates.",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("Missing AHA_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    config_path = os.path.join(_project_root, ".aha-config.yml")
    product_key = read_product_key(config_path)
    client = AhaApiClient(api_key)

    print(f"Fetching all Ideas for product {product_key}…")
    existing = fetch_all_ideas(client, product_key)
    print(f"Found {len(existing)} existing Ideas.\n")

    details_fetched = 0
    rows: list[dict[str, Any]] = []

    for c in CANDIDATES:
        name = c["name"]
        best_ref, best_name, ratio = best_match(name, existing)
        action = "Create"
        note = ""
        if ratio >= SIMILARITY_SKIP_THRESHOLD:
            action = "Skip (likely duplicate)"
            note = f"Similarity {ratio:.2f}"
        elif ratio >= 0.5:
            action = "Review"
            note = f"Similarity {ratio:.2f}"

        cat_note = ""
        if (
            best_ref
            and ratio >= SIMILARITY_DETAIL_THRESHOLD
            and details_fetched < DETAIL_FETCH_BUDGET
        ):
            if details_fetched > 0 and details_fetched % DETAIL_EVERY == 0:
                time.sleep(DETAIL_SLEEP)
            detail = fetch_idea_detail(client, best_ref)
            details_fetched += 1
            idea = detail.get("idea") or detail
            cats = idea.get("categories") or []
            cat_titles = [
                (x or {}).get("name") for x in cats if isinstance(x, dict)
            ]
            if (
                cat_titles
                and TARGET_CATEGORY
                and TARGET_CATEGORY not in str(cat_titles)
            ):
                note += f" | existing categories: {cat_titles}"

        rows.append(
            {
                "proposed": name,
                "snippet": c["summary"][:120] + ("…" if len(c["summary"]) > 120 else ""),
                "match_ref": best_ref,
                "match_name": best_name,
                "ratio": ratio,
                "action": action,
                "note": note,
            }
        )

    print("Dedupe (best name match per candidate):\n")
    for r in rows:
        m = f"{r['match_ref']}: {r['match_name'][:70]}…" if r["match_name"] and len(r["match_name"]) > 70 else f"{r['match_ref']}: {r['match_name']}"
        if not r["match_name"]:
            m = "—"
        print(
            f"- {r['proposed']}\n  Match: {m} (ratio {r['ratio']:.2f}) → {r['action']}\n  {r['note']}\n"
        )

    to_create = [r for r in rows if r["action"] == "Create"]
    to_review = [r for r in rows if r["action"] == "Review"]

    if to_review and not args.create:
        print(
            f"\n{len(to_review)} row(s) are 'Review' (similarity 0.5–0.62). "
            "Use --create --include-review if they are not duplicates of the matched Idea.\n"
        )

    if not args.create:
        print("Dry run only. Use --create to POST Ideas for rows marked Create.")
        return

    if args.include_review:
        to_create = [r for r in rows if r["action"] in ("Create", "Review")]

    if not to_create:
        print("No rows to POST (use --include-review for 'Review' rows).")
        return

    print(
        f"\nPOSTing {len(to_create)} Idea(s) to /products/{product_key}/ideas …\n"
    )
    for r in to_create:
        cand = next(x for x in CANDIDATES if x["name"] == r["proposed"])
        body = {
            "idea": {
                "name": r["proposed"][:200],
                "description": html_description(
                    r["proposed"][:200], cand["summary"][:2000]
                ),
            }
        }
        try:
            out = client.post(f"/products/{product_key}/ideas", data=body)
            idea = out.get("idea") or out
            ref = idea.get("reference_num", "?")
            print(f"OK  {ref} — {r['proposed']}")
            if idea.get("url"):
                print(f"    {idea.get('url')}")
        except Exception as e:  # noqa: BLE001
            print(f"ERR {r['proposed']}: {e}", file=sys.stderr)
            # continue with other rows; user can retry


if __name__ == "__main__":
    main()
