"""WSGI entry point for production deployment (Render, Railway, etc.)."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.server import app, run_pipeline

run_pipeline()

if __name__ == "__main__":
    app.run()
