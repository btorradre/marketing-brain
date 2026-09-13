#!/bin/zsh
# Weekly wrapper invoked by the LaunchAgent (Mon 08:47 local).
# launchd hands processes a bare PATH, so python is resolved here.

export PATH="/Users/brooksorradre2/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/bin:/bin:/usr/sbin:/sbin"

HERE="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HERE/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y-%m-%d).log"

export SSL_CERT_FILE="$(python3 -m certifi 2>/dev/null)"

{
  echo "===== restock watch started $(date '+%Y-%m-%d %H:%M:%S %Z') ====="
  cd "$HERE" || exit 1
  python3 restock_check.py
  echo "===== finished rc=$? $(date '+%Y-%m-%d %H:%M:%S %Z') ====="
  echo
} >> "$LOG" 2>&1

# Keep 90 days of logs and reports.
find "$LOG_DIR" -name '*.log' -type f -mtime +90 -delete 2>/dev/null
find "$HERE/reports" -name '2*.md' -type f -mtime +90 -delete 2>/dev/null
