#!/usr/bin/env python3
"""Pre-render the dashboard as a self-contained static HTML file.

Runs the full pipeline, embeds all JSON data directly into the HTML,
and writes a standalone index.html that can be hosted on GitHub Pages
or any static file server.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.server import run_pipeline, _load_samples
from pathlib import Path

TEMPLATE = Path(__file__).parent / "web" / "templates" / "dashboard.html"
OUTPUT_DIR = Path(__file__).parent / "docs"


def build():
    print("Running pipeline...")
    data = run_pipeline()
    samples = _load_samples()

    print("Reading template...")
    html = TEMPLATE.read_text()

    html = html.replace("{{ data_json | safe }}", json.dumps(data))
    html = html.replace("{{ samples_json | safe }}", json.dumps(samples))

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / "index.html"
    out_path.write_text(html)
    print(f"Static dashboard written to {out_path}")
    print(f"  Size: {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
