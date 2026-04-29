"""
Read-only CLI for ad-hoc Aha! lookups.

Run from the repo root:

    python -m src.cli get /features/OPER-E-1234
    python -m src.cli get /products/OPER/ideas --param per_page=5
    python -m src.cli paginate /products/OPER/epics --collection epics

Errors go to stderr with non-zero exit. JSON goes to stdout, so the output
composes with `jq`, `>`, `| less`, etc.

Read-only by design: no `post`/`put`/`delete` subcommands. Writes still go
through `src/executors/scratchpad.py` so the project's approval guardrails
(see AGENTS.md "Ask First" tier) keep applying.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

from src.api.client import AhaApiClient
from src.lib.aha_helpers import paginate

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _parse_params(pairs):
    """Convert ['k=v', 'a=b'] into {'k': 'v', 'a': 'b'}."""
    result = {}
    for raw in pairs or []:
        if "=" not in raw:
            print(
                f"ERROR: --param expects key=value, got {raw!r}",
                file=sys.stderr,
            )
            sys.exit(2)
        key, _, value = raw.partition("=")
        result[key.strip()] = value
    return result


def _build_client():
    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    api_key = os.getenv("AHA_API_KEY")
    if not api_key:
        print("ERROR: AHA_API_KEY not set in .env", file=sys.stderr)
        sys.exit(1)
    return AhaApiClient(api_key)


def cmd_get(args):
    client = _build_client()
    params = _parse_params(args.param)
    try:
        resp = client.get(args.path, params=params or None)
    except Exception as e:
        print(f"ERROR: GET {args.path} failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.raw:
        print(json.dumps(resp))
    else:
        print(json.dumps(resp, indent=2))


def cmd_paginate(args):
    client = _build_client()
    extra = _parse_params(args.param)

    items = []
    for i, record in enumerate(
        paginate(client, args.path, args.collection, extra_params=extra or None)
    ):
        items.append(record)
        if args.max_pages is not None:
            # paginate() uses per_page=200 by default; cap items accordingly.
            if len(items) >= args.max_pages * 200:
                break

    if args.raw:
        print(json.dumps(items))
    else:
        print(json.dumps(items, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description="Read-only CLI for ad-hoc Aha! lookups.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_get = sub.add_parser("get", help="Single GET request, prints JSON to stdout.")
    p_get.add_argument("path", help="API path, e.g. /features/OPER-E-1234")
    p_get.add_argument(
        "--param",
        action="append",
        metavar="KEY=VALUE",
        help="Query parameter (repeatable). Example: --param per_page=5",
    )
    p_get.add_argument(
        "--raw",
        action="store_true",
        help="Print compact JSON (no indentation).",
    )
    p_get.set_defaults(func=cmd_get)

    p_page = sub.add_parser(
        "paginate",
        help="Auto-page a list endpoint and emit one JSON array.",
    )
    p_page.add_argument("path", help="List endpoint, e.g. /products/OPER/epics")
    p_page.add_argument(
        "--collection",
        required=True,
        help="JSON key holding the array, e.g. epics, features, ideas.",
    )
    p_page.add_argument(
        "--param",
        action="append",
        metavar="KEY=VALUE",
        help="Query parameter (repeatable).",
    )
    p_page.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional cap on pages fetched (each page is up to 200 items).",
    )
    p_page.add_argument(
        "--raw",
        action="store_true",
        help="Print compact JSON (no indentation).",
    )
    p_page.set_defaults(func=cmd_paginate)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
