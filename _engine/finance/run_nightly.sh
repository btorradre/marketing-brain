#!/bin/zsh
# Nightly wrapper invoked by the LaunchAgent at 00:00 local time.
# launchd hands processes a bare PATH, so node/vercel/python are resolved here.

export PATH="/Users/brooksorradre2/.npm-global/bin:/opt/homebrew/bin:/usr/local/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/bin:/bin:/usr/sbin:/sbin"

HERE="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HERE/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/$(date +%Y-%m-%d).log"

{
  echo "===== run started $(date '+%Y-%m-%d %H:%M:%S %Z') ====="
  cd "$HERE" || exit 1
  python3 run_nightly.py --days 60
  echo "===== run finished rc=$? $(date '+%Y-%m-%d %H:%M:%S %Z') ====="
  echo
} >> "$LOG" 2>&1

# Keep 30 days of logs.
find "$LOG_DIR" -name '*.log' -type f -mtime +30 -delete 2>/dev/null

# Keep 90 days of snapshot archives.
find "$HERE/data/archive" -name '*.json' -type f -mtime +90 -delete 2>/dev/null
