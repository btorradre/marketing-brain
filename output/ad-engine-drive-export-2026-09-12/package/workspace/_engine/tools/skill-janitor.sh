#!/usr/bin/env bash
# skill-janitor — keeps skill definitions clean so updates don't leave stale files behind.
#
# SCOPE: operates ONLY on skill directories:
#   - <vault>/.claude/skills/*
#   - ~/.claude/skills/*
# It NEVER touches the copy/advertorial/listicle version libraries under _engine/ or brands/
# (those "v2/v3" files are real deliverables, not stale skills).
#
# ACTIONS (everything recoverable — routes to macOS Trash, never rm):
#   1. Remove build/editor junk inside skill dirs: *.bak, *~, .DS_Store
#   2. Remove superseded SKILL variants kept next to the canonical SKILL.md
#      (e.g. SKILL-v7.md, SKILL-UPDATED-v6.md, SKILL-old.md, SKILL.md.bak, "SKILL copy.md")
#   3. Report project<->user duplicates and their drift (does not auto-resolve content drift)
#
# USAGE:
#   skill-janitor.sh                # full sweep across all skill dirs + report
#   skill-janitor.sh <path>         # scoped: clean only the skill dir containing <path>
#                                   #   (used by the PostToolUse hook after a skill edit)

set -uo pipefail

VAULT="/Users/brooksorradre2/Documents/marketing brain"
PROJ_SKILLS="$VAULT/.claude/skills"
USER_SKILLS="$HOME/.claude/skills"
LOG="$VAULT/_engine/tools/skill-janitor.log"
TS="$(date '+%Y-%m-%d %H:%M:%S')"

trash_bin() { command -v trash >/dev/null 2>&1 && trash "$1" || rm -rf "$1"; }
note() { echo "$1"; echo "[$TS] $1" >> "$LOG"; }

# Remove stale files inside a single skill directory.
clean_skill_dir() {
  local dir="$1"
  [ -d "$dir" ] || return 0
  # follow symlinks to the real dir so we clean the canonical copy
  dir="$(cd "$dir" 2>/dev/null && pwd -P)" || return 0
  local removed=0

  # 1. junk
  while IFS= read -r -d '' f; do
    trash_bin "$f"; note "junk removed: ${f/#$HOME/~}"; removed=$((removed+1))
  done < <(find "$dir" -maxdepth 2 \( -name '*.bak' -o -name '*~' -o -name '.DS_Store' \) -print0 2>/dev/null)

  # 2. superseded SKILL variants (anything matching SKILL*.md / *SKILL*.md that is NOT the canonical SKILL.md)
  while IFS= read -r -d '' f; do
    base="$(basename "$f")"
    [ "$base" = "SKILL.md" ] && continue
    trash_bin "$f"; note "superseded skill file removed: ${f/#$HOME/~}"; removed=$((removed+1))
  done < <(find "$dir" -maxdepth 1 -type f \( -iname 'SKILL*.md' -o -iname '*-SKILL*.md' -o -iname 'SKILL copy*.md' \) -print0 2>/dev/null)

  [ "$removed" -gt 0 ] && note "  -> cleaned $removed file(s) in ${dir/#$HOME/~}"
  return 0
}

# Report project<->user duplicate skills and drift.
report_dupes() {
  [ -d "$PROJ_SKILLS" ] || return 0
  for p in "$PROJ_SKILLS"/*; do
    [ -e "$p" ] || continue
    name="$(basename "$p")"
    u="$USER_SKILLS/$name"
    [ -e "$u" ] || continue
    if [ -L "$p" ]; then continue; fi   # already a symlink -> single source of truth, fine
    if [ -f "$p/SKILL.md" ] && [ -f "$u/SKILL.md" ]; then
      if diff -q "$p/SKILL.md" "$u/SKILL.md" >/dev/null 2>&1; then
        note "DUP (identical): $name exists in project AND user — consider symlinking project -> user"
      else
        note "DRIFT: $name SKILL.md differs between project and user — manual review (symlink to retire the shadow)"
      fi
    fi
  done
}

echo "=== skill-janitor $TS ==="
if [ "${1:-}" != "" ]; then
  # scoped mode: find the skill dir that contains the given path
  path="$1"
  case "$path" in
    *"/.claude/skills/"*)
      sub="${path#*/.claude/skills/}"; skill="${sub%%/*}"
      for root in "$PROJ_SKILLS" "$USER_SKILLS"; do clean_skill_dir "$root/$skill"; done
      ;;
    *) : ;;  # edit was not under a skills dir — nothing to do
  esac
else
  # full sweep
  for root in "$PROJ_SKILLS" "$USER_SKILLS"; do
    [ -d "$root" ] || continue
    for d in "$root"/*; do [ -d "$d" ] && clean_skill_dir "$d"; done
  done
  report_dupes
  note "full sweep complete."
fi
