"""
Reusable helpers for Aha! REST workflows.

Promoted from `src/executors/suggestion_review.py` so any executor or
scratchpad can import them instead of re-implementing pagination,
text matching, or backlog fetches.

All functions take an `AhaApiClient` (from `src.api.client`) so callers
control auth and rate-limit behavior.
"""

import math
import re
import time
from collections import Counter
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Throttling defaults (tuned for Aha!'s 300/min, 20/sec limits)
# ---------------------------------------------------------------------------

THROTTLE_BATCH = 15
THROTTLE_SLEEP = 1.1
PAGINATE_PAGE_SLEEP = 0.1


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------

def strip_html(text) -> str:
    """Strip tags and collapse whitespace. Accepts str, dict (with `body`), or None."""
    if not text:
        return ""
    if isinstance(text, dict):
        text = text.get("body", "")
    cleaned = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", cleaned).strip()


# Extremely common English / product-generic words that carry no signal
# for matching suggestions to backlog items. IDF still handles most of the
# work; this is a belt-and-braces filter so rare-but-useless tokens like
# "celonis" (appears in only a few titles but is meaningless for matching)
# don't pollute the `matching_words` display.
_STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "out", "off", "via",
    "this", "that", "these", "those", "have", "has", "had", "will",
    "can", "could", "should", "would", "may", "might", "must",
    "any", "all", "some", "each", "every", "other", "another", "more",
    "most", "less", "least", "also", "but", "not", "nor", "than",
    "then", "when", "where", "which", "who", "whom", "whose", "what",
    "why", "how", "within", "without", "onto", "upon", "between",
    "across", "through", "over", "under", "above", "below",
    "are", "was", "were", "been", "being", "does", "did", "doing",
    "celonis", "aha",
}


def tokenize(text: str) -> set:
    """Lowercase 3+ char word tokens, stopwords removed."""
    tokens = set(re.findall(r"[a-z]{3,}", text.lower()))
    return tokens - _STOPWORDS


# ---------------------------------------------------------------------------
# API record normalization
# ---------------------------------------------------------------------------

def normalize_status(record: dict) -> Tuple[str, bool]:
    """Return (status_name, complete?) tuple from an Aha! record."""
    ws = record.get("workflow_status")
    if isinstance(ws, dict):
        return ws.get("name", "Unknown"), bool(ws.get("complete"))
    if ws:
        return str(ws), False
    return "Unknown", False


def normalize_description(record: dict) -> str:
    """Plain-text description from a record's `description` field."""
    desc = record.get("description")
    if isinstance(desc, dict):
        return strip_html(desc.get("body", ""))
    return strip_html(desc or "")


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def paginate(
    client,
    path: str,
    collection_key: str,
    extra_params: Optional[Dict[str, str]] = None,
    per_page: int = 200,
    page_sleep: float = PAGINATE_PAGE_SLEEP,
) -> Iterator[dict]:
    """Yield every record from a paginated Aha! list endpoint.

    `collection_key` is the JSON key holding the array (e.g. "epics",
    "features", "ideas"). Sleeps `page_sleep` seconds between pages.
    """
    page = 1
    while True:
        params = {"per_page": str(per_page), "page": str(page)}
        if extra_params:
            params.update(extra_params)
        resp = client.get(path, params=params)
        batch = resp.get(collection_key, [])
        if not batch:
            return
        for record in batch:
            yield record
        total_pages = resp.get("pagination", {}).get("total_pages", 1)
        if page >= total_pages:
            return
        page += 1
        if page_sleep:
            time.sleep(page_sleep)


# ---------------------------------------------------------------------------
# Backlog fetch (epics + features + ideas) for cross-referencing
# ---------------------------------------------------------------------------

def fetch_backlog(client, product_key: str) -> List[dict]:
    """Fetch epics + features + ideas for the product, tagged with `type`.

    Idea descriptions come from the list endpoint and are used for
    matching. Epic/feature descriptions require per-item detail calls
    and are left blank here for cost reasons.
    """
    items: List[dict] = []

    for epic in paginate(client, f"/products/{product_key}/epics", "epics"):
        status, complete = normalize_status(epic)
        items.append(
            {
                "ref": epic.get("reference_num", ""),
                "name": epic.get("name", ""),
                "description": "",
                "type": "epic",
                "status": status,
                "complete": complete,
            }
        )

    for feature in paginate(client, f"/products/{product_key}/features", "features"):
        status, complete = normalize_status(feature)
        items.append(
            {
                "ref": feature.get("reference_num", ""),
                "name": feature.get("name", ""),
                "description": "",
                "type": "feature",
                "status": status,
                "complete": complete,
            }
        )

    for idea in paginate(client, f"/products/{product_key}/ideas", "ideas"):
        status, complete = normalize_status(idea)
        items.append(
            {
                "ref": idea.get("reference_num", ""),
                "name": idea.get("name", ""),
                "description": normalize_description(idea),
                "type": "idea",
                "status": status,
                "complete": complete,
            }
        )

    return items


def fetch_all_ideas(client, product_key: str) -> List[dict]:
    """List-endpoint fetch for every Idea in a product. Fast (no detail calls).

    Each result keeps the raw API shape; pull `reference_num`, `name`,
    `description`, `workflow_status`, etc. as needed.
    """
    return list(paginate(client, f"/products/{product_key}/ideas", "ideas"))


def fetch_ideas_with_categories(
    client,
    refs: Iterable[str],
    throttle_batch: int = THROTTLE_BATCH,
    throttle_sleep: float = THROTTLE_SLEEP,
) -> List[dict]:
    """Second-pass detail fetch for Ideas (categories, custom fields, etc.).

    Categories are only returned by `GET /ideas/{ref}`, not by the list
    endpoint. Use this after `fetch_all_ideas` + a name filter to enrich
    a small set of refs.

    Returns one dict per ref; refs that 404 or error out are skipped.
    Throttles automatically: sleeps `throttle_sleep` after every
    `throttle_batch` requests.
    """
    results: List[dict] = []
    for i, ref in enumerate(refs):
        if i > 0 and i % throttle_batch == 0:
            time.sleep(throttle_sleep)
        try:
            resp = client.get(f"/ideas/{ref}")
        except Exception:
            continue
        idea = resp.get("idea", resp)
        results.append(idea)
    return results


# ---------------------------------------------------------------------------
# IDF-weighted keyword matching
# ---------------------------------------------------------------------------

def build_idf(items: List[dict]) -> Dict[str, float]:
    """Compute inverse-document-frequency weights over a corpus of items.

    Common tokens like 'orchestration' or 'engine' (present in a large
    share of items) end up near zero; distinctive tokens like 'upload'
    or 'iframe' get high weight. Items must have `name` and may have
    `description`.
    """
    n = max(len(items), 1)
    df: Counter = Counter()
    for item in items:
        tokens = tokenize(f"{item.get('name', '')} {item.get('description', '')}")
        for t in tokens:
            df[t] += 1
    return {t: math.log((n + 1) / (dfreq + 1)) + 1.0 for t, dfreq in df.items()}


def keyword_match(
    text: str,
    items: List[dict],
    idf: Dict[str, float],
    min_score: float = 1.5,
    top_k: int = 10,
) -> List[dict]:
    """Rank items by IDF-weighted token overlap with `text`.

    Each result preserves the item's metadata plus `matching_words` and
    `match_score`. Results are sorted highest-score first and capped at
    `top_k`.
    """
    sug_tokens = tokenize(text)
    if not sug_tokens:
        return []

    scored: List[dict] = []
    for item in items:
        item_tokens = tokenize(f"{item.get('name', '')} {item.get('description', '')}")
        overlap = sug_tokens & item_tokens
        if not overlap:
            continue
        score = sum(idf.get(t, 1.0) for t in overlap)
        if score < min_score:
            continue
        ranked_words = sorted(overlap, key=lambda t: -idf.get(t, 1.0))[:8]
        scored.append(
            {
                "ref": item.get("ref", ""),
                "name": item.get("name", ""),
                "type": item.get("type", ""),
                "status": item.get("status", ""),
                "complete": item.get("complete", False),
                "matching_words": ranked_words,
                "match_score": round(score, 2),
            }
        )
    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_k]
