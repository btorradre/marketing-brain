#!/usr/bin/env bash
# Launch the ugc-forge UI (stdlib only — no pip install needed).
# Usage: ./ui/run.sh   then open http://127.0.0.1:8765
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$DIR/ui/server.py"
