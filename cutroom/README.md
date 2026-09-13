# Cutroom

Internal Milanote-style whiteboard for visual creative briefs. Projects → boards → assets, cloud-backed by Supabase Storage.

- **Start:** `python3 server.py` → http://localhost:8765
- **Boards** are JSON files in `boards/`, images in `assets/` — everything is file-based.
- **Use in browser:** drag cards, double-click to edit, drop images anywhere, scroll to pan, pinch/ctrl-scroll to zoom, ⌫ deletes selected. Saves are automatic.
- **AI briefs:** Claude builds storyboard boards via the `cutroom` skill (`board_builder.py` does the layout from a content spec).
- **Share:** `python3 export_board.py <slug>` → one self-contained HTML in `exports/` (send via Slack/email).
- **Projects:** sidebar on the home page; boards carry a `project` slug in their JSON.
- **Cloud:** every save syncs to the private Supabase bucket `cutroom` (`supabase_store.py push|pull|status` for manual control).
- **Database:** SQL migrations live in `supabase/migrations/` and are applied to the Supabase project by GitHub Actions on every push to `main`. See `supabase/README.md` for the three repo secrets it needs.
- **Config:** copy `.env.example` to `.env`. Generated content (`assets/`, `boards/`, `exports/`) is gitignored — the Supabase bucket is its source of truth.
