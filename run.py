#!/usr/bin/env python3
"""
Work IQ × Celonis Task Mining — Proof of Concept

Demonstrates how Microsoft Work IQ agent signals can be ingested alongside
Celonis Task Mining desktop/browser captures, clustered into semantic tasks
via AI, and visualized as a unified Process Intelligence Graph.

Usage:
    pip install -r requirements.txt
    python run.py

Then open http://localhost:5050 in your browser.
"""

import sys
import os
import webbrowser
from threading import Timer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.server import app, run_pipeline


def open_browser():
    webbrowser.open("http://localhost:5055")


def main():
    print("=" * 64)
    print("  Work IQ × Celonis Task Mining — POC")
    print("  Contoso Financial Services — Loan Origination")
    print("=" * 64)
    print()

    run_pipeline()

    print("Dashboard ready at: http://localhost:5055")
    print("API endpoints:")
    print("  GET /api/raw       — Raw events from both sources")
    print("  GET /api/unified   — Normalized unified events")
    print("  GET /api/pig       — Process Intelligence Graph")
    print("  GET /api/pipeline  — Full pipeline output")
    print()
    print("Press Ctrl+C to stop.\n")

    Timer(1.5, open_browser).start()
    app.run(host="0.0.0.0", port=5055, debug=False)


if __name__ == "__main__":
    main()
