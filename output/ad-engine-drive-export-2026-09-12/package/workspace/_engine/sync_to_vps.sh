#!/bin/bash
# Push the local marketing brain (plus Claude memory) to the VPS mirror.
# Usage: ./_engine/sync_to_vps.sh          (light: files <= 10MB, fast)
#        ./_engine/sync_to_vps.sh --full   (everything, incl. video/media)
#
# NO --delete on purpose: the VPS agents write into this folder (concepts,
# pages, reports). A blind delete-push would wipe their work. If you truly
# need a hard mirror, run with --delete-risky.
set -euo pipefail

VPS="root@187.124.249.12"
DEST="/opt/vault/marketing-brain/"
SRC="$(cd "$(dirname "$0")/.." && pwd)/"
MEM="$HOME/.claude/projects/-Users-brooksorradre2-Documents-marketing-brain/memory/"

ARGS=(-az --exclude '.DS_Store' --exclude 'node_modules' --exclude '.git')
case "${1:-}" in
  --full) ;;
  --delete-risky) ARGS+=(--delete) ;;
  *) ARGS+=(--max-size=10M) ;;
esac

echo "Syncing marketing brain -> $VPS:$DEST"
rsync "${ARGS[@]}" "$SRC" "$VPS:$DEST"

echo "Syncing Claude memory -> ${DEST}_memory/"
rsync -az --exclude '.DS_Store' "$MEM" "$VPS:${DEST}_memory/"

echo "✅ sync complete $(date '+%Y-%m-%d %H:%M')"
