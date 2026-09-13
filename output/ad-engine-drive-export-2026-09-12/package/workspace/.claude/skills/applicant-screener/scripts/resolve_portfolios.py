#!/usr/bin/env python3
"""
resolve_portfolios.py: open the links yt-dlp cannot and pull playable media out.

Almost every real portfolio arrives as a Google Drive folder or a Canva site, so
skipping these means scoring nobody on their actual work. This opens each one in
the logged-in browser, finds video files or embeds, and writes the discovered
URLs back onto the applicant so harvest_media.py can fetch them.

usage:
  python3 resolve_portfolios.py --run <run_dir> [--headless] [--limit N]
"""
import argparse, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE = Path.home() / ".claude" / "playwright-profiles" / "hiring"
VIDEO_EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv")


def drive_folder(page, url):
    """Enumerate a Drive folder. Tiles carry the file id in data-id."""
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(4500)
    for _ in range(6):  # lazy grid
        page.keyboard.press("End")
        page.wait_for_timeout(900)
    return page.evaluate("""() => {
      const out = [];
      document.querySelectorAll('[data-id]').forEach(el => {
        const id = el.getAttribute('data-id');
        const name = (el.getAttribute('aria-label') || el.innerText || '').trim().slice(0,120);
        if (id && /^[A-Za-z0-9_-]{20,}$/.test(id)) out.push({id, name});
      });
      const seen = new Set();
      return out.filter(o => !seen.has(o.id) && seen.add(o.id));
    }""")


def page_media(page, url):
    """Canva sites, personal domains: <video> tags, embeds, and media links."""
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    for _ in range(4):
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(1200)
    return page.evaluate("""() => {
      const abs = (u) => { try { return new URL(u, location.href).href } catch(e){ return null } };
      const vids = Array.from(document.querySelectorAll('video'))
        .flatMap(v => [v.currentSrc, v.src, ...Array.from(v.querySelectorAll('source')).map(s=>s.src)])
        .filter(Boolean).map(abs);
      const frames = Array.from(document.querySelectorAll('iframe'))
        .map(f => f.src).filter(Boolean).map(abs)
        .filter(u => /youtube|youtu\\.be|vimeo|drive\\.google|loom|wistia|streamable|dailymotion/.test(u));
      const links = Array.from(document.querySelectorAll('a[href]'))
        .map(a => a.href)
        .filter(u => /youtube|youtu\\.be|vimeo|drive\\.google|loom|wistia|streamable|\\.mp4|\\.mov|\\.webm/i.test(u));
      const uniq = [...new Set([...vids, ...frames, ...links])].filter(Boolean);
      return uniq.slice(0, 40);
    }""")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    run_dir = Path(args.run).expanduser().resolve()
    idx_path = run_dir / "media" / "index.json"
    app_path = run_dir / "applicants.json"
    if not idx_path.exists():
        sys.exit("run harvest_media.py first so needs_browser exists")

    index = json.loads(idx_path.read_text())
    applicants = json.loads(app_path.read_text())
    by_id = {str(a.get("id")): a for a in applicants}

    todo = [e for e in index if e.get("needs_browser")]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(todo)} applicants with browser-only links", flush=True)

    found_total = 0
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            str(PROFILE), headless=args.headless,
            viewport={"width": 1440, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(60000)

        for e in todo:
            discovered = []
            for url in e["needs_browser"]:
                try:
                    if "drive.google.com/drive/folders" in url:
                        files = drive_folder(page, url)
                        vids = [f for f in files
                                if f["name"].lower().endswith(VIDEO_EXT)
                                or not re.search(r"\.(jpg|jpeg|png|pdf|docx?|gif|webp)$",
                                                 f["name"], re.I)]
                        discovered += [f"https://drive.google.com/file/d/{f['id']}/view"
                                       for f in vids[:8]]
                    else:
                        discovered += page_media(page, url)
                except Exception as ex:
                    print(f"    {url[:60]} -> {type(ex).__name__}", file=sys.stderr)
            discovered = [u for u in dict.fromkeys(discovered) if u]
            e["resolved"] = discovered
            found_total += len(discovered)
            a = by_id.get(str(e.get("id")))
            if a is not None:
                a["links"] = list(dict.fromkeys((a.get("links") or []) + discovered))
            print(f"  {e.get('name','?')[:32]:<34} +{len(discovered)}", flush=True)
        ctx.close()

    idx_path.write_text(json.dumps(index, indent=2))
    app_path.write_text(json.dumps(applicants, indent=2))
    print(f"\nresolved {found_total} media URLs into applicants.json")
    print("now re-run harvest_media.py to download them")


if __name__ == "__main__":
    main()
