"""Vercel serverless entry point — exports the Flask WSGI app."""

import os
import sys

# Add project root to path so meta_ads and backend packages are importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the Flask app — Vercel's Python runtime looks for `app`
from backend.app import app
