#!/usr/bin/env python3
"""
oj_harvest.py: pull every applicant on an OnlineJobs.ph job post.

The v2 inbox is a SPA over a REST API, so this reads the API directly instead of
clicking rows. Clicking does not survive the list: it re-renders and collapses
back to 20 rows after every open, which silently truncates a harvest.

Auth is a per-session bearer token that the app holds in the browser. It is read
live out of the open session on every run and is never written to disk. Do not
hardcode it, do not put it in .env, do not print it.

Endpoints (discovered live 2026-08-03):
  GET /api/v1/message/jobs/{job_hash}?page=N&per_page=20   thread list
  GET /api/v1/message/thread/{thread_hash}?page=1&per_page=20   message bodies
  GET /api/v1/contacts/pinned                              already-pinned workers

usage:
  python3 oj_harvest.py --job-hash oeE7N4Wb --run <run_dir> [--headless]
"""
import argparse, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE = Path.home() / ".claude" / "playwright-profiles" / "hiring"
API = "https://api.onlinejobs.ph/api/v1"
APP = "https://v2.onlinejobs.ph"


def grab_token(page):
    """Pull the bearer out of the live session. Checks storage, then falls back
    to sniffing an outgoing API request."""
    tok = page.evaluate("""() => {
      const hunt = (store) => {
        for (let i = 0; i < store.length; i++) {
          const k = store.key(i);
          let v = store.getItem(k);
          if (!v) continue;
          if (/^\\d+\\|[A-Za-z0-9]{20,}$/.test(v)) return v;
          try {
            const o = JSON.parse(v);
            for (const key of ['token','access_token','authToken','bearer']) {
              if (typeof o?.[key] === 'string' && /^\\d+\\|/.test(o[key])) return o[key];
            }
          } catch (e) {}
        }
        return null;
      };
      return hunt(localStorage) || hunt(sessionStorage);
    }""")
    if tok:
        return tok
    holder = {}
    page.on("request", lambda r: holder.setdefault(
        "t", (r.headers or {}).get("authorization", "").replace("Bearer ", ""))
        if "api.onlinejobs.ph" in r.url and (r.headers or {}).get("authorization") else None)
    page.goto(f"{APP}/message/jobs/{holder.get('job','')}", wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    return holder.get("t")


def api_get(page, token, path):
    """Fetch from inside the page origin so CORS and cookies behave."""
    return page.evaluate(
        """async ([url, tok]) => {
             const r = await fetch(url, {headers: {Authorization: 'Bearer ' + tok,
                                                   Accept: 'application/json'}});
             if (!r.ok) return {__error: r.status};
             return await r.json();
           }""", [f"{API}{path}", token])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job-hash", required=True, help="e.g. oeE7N4Wb")
    ap.add_argument("--run", required=True)
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    run_dir = Path(args.run).expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            str(PROFILE), headless=args.headless,
            viewport={"width": 1440, "height": 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_timeout(60000)
        page.goto(f"{APP}/message/jobs/{args.job_hash}", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        if "/login" in page.url or page.query_selector("input[type=password]"):
            sys.exit("not logged in. Sign in in the open window, then re-run.")

        token = grab_token(page)
        if not token:
            sys.exit("could not read the session token. Reload the inbox and retry.")
        print("session token acquired (not stored)", flush=True)

        # Already-pinned workers, so the run never re-pins one and never
        # archives someone Brooks pinned by hand.
        # This endpoint keys on jobseeker_id / user_hash, NOT id. Using id
        # silently yields {None} and reports one pin no matter how many exist.
        pinned = api_get(page, token, "/contacts/pinned")
        pinned_ids, pinned_hashes = set(), set()
        if isinstance(pinned, list):
            for p in pinned:
                if not isinstance(p, dict):
                    continue
                if p.get("jobseeker_id"):
                    pinned_ids.add(p["jobseeker_id"])
                if p.get("user_hash"):
                    pinned_hashes.add(p["user_hash"])
        print(f"already pinned: {len(pinned_ids)}", flush=True)

        threads, pg = [], 1
        while True:
            r = api_get(page, token,
                        f"/message/jobs/{args.job_hash}?page={pg}&per_page=20")
            if not isinstance(r, dict) or "data" not in r:
                break
            threads.extend(r["data"])
            meta = r.get("meta", {})
            if pg >= meta.get("last_page", pg):
                break
            pg += 1
        print(f"threads: {len(threads)}", flush=True)

        applicants = []
        for i, t in enumerate(threads, 1):
            th, pr = t.get("thread", {}), t.get("partner", {})
            hash_id = th.get("hash_id")
            body = api_get(page, token,
                           f"/message/thread/{hash_id}?page=1&per_page=20")
            msgs = body.get("data", []) if isinstance(body, dict) else []
            # applicant's own messages only; ours would pollute the filter-word gate
            mine = [m for m in msgs if m.get("sender_id") == pr.get("id")
                    or (m.get("sender") or {}).get("id") == pr.get("id")]
            texts = [re.sub(r"<[^>]+>", " ", str(m.get("message") or m.get("body") or ""))
                     for m in (mine or msgs)]
            full = "\n\n".join(t for t in texts if t.strip())
            links = re.findall(r"https?://[^\s<>\"')\]]+", full)

            applicants.append({
                "id": hash_id,
                "name": pr.get("name"),
                "email": pr.get("email"),
                "worker_hash": pr.get("hash_id"),
                "partner_id": pr.get("id"),
                "subject": th.get("subject"),
                "apply_points": th.get("apply_points"),
                "convo_count": th.get("convo_count"),
                "is_archived": th.get("is_archived"),
                "already_pinned": (pr.get("id") in pinned_ids
                                   or pr.get("hash_id") in pinned_hashes),
                "applied_at": t.get("latest_message_date"),
                "conversation_url": f"{APP}/message/conversation/{hash_id}",
                "raw_text": f"{th.get('subject') or ''}\n\n{full}",
                "links": links,
            })
            if i % 10 == 0 or i == len(threads):
                print(f"  {i}/{len(threads)} bodies", flush=True)

        (run_dir / "applicants.json").write_text(json.dumps(applicants, indent=2))
        ctx.close()

    got = sum(1 for a in applicants if len(a["raw_text"]) > 120)
    print(f"\nwrote {run_dir/'applicants.json'}")
    print(f"{len(applicants)} applicants, {got} with a real cover letter, "
          f"{sum(1 for a in applicants if a['already_pinned'])} already pinned, "
          f"{sum(1 for a in applicants if a['is_archived'])} already archived")


if __name__ == "__main__":
    main()
