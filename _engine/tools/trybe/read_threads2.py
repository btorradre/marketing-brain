"""Full extraction: enumerate ALL sidebar conversations, open each, dump complete pane text."""
import json
from playwright.sync_api import sync_playwright

OUT = "/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/55693610-c9a6-4e75-8f07-4a68ef0650d2/scratchpad"

with sync_playwright() as p:
    b = p.chromium.connect_over_cdp("http://localhost:9333")
    pg = [x for x in b.contexts[0].pages if not x.url.startswith("devtools")][-1]
    pg.goto("https://jointrybe.com/brand/chat", wait_until="domcontentloaded")
    pg.wait_for_timeout(3500)

    # scroll sidebar list fully to load every conversation
    for _ in range(6):
        pg.evaluate("""
          () => {
            for (const el of document.querySelectorAll('div')) {
              if (el.scrollHeight > el.clientHeight + 50 && el.getBoundingClientRect().x < 700 && el.querySelector('img')) {
                el.scrollTop = el.scrollHeight;
              }
            }
          }
        """)
        pg.wait_for_timeout(700)

    names = pg.evaluate("""
      () => {
        const out = [];
        for (const el of document.querySelectorAll('div,span,p,h3,h4,strong')) {
          const t = (el.innerText||'').trim();
          const m = t.match(/^(.{2,40}) \\(DM\\)$/);
          if (m && el.getBoundingClientRect().x < 700 && !el.querySelector('div')) out.push(m[1]);
        }
        return [...new Set(out)];
      }
    """)
    print("CONVERSATIONS:", json.dumps(names))

    threads = {}
    for name in names:
        try:
            pg.get_by_text(f"{name} (DM)", exact=False).first.click()
            pg.wait_for_timeout(2200)
            for _ in range(6):
                pg.evaluate("""
                  () => {
                    let best=null;
                    for (const el of document.querySelectorAll('div')) {
                      if (el.scrollHeight > el.clientHeight + 50) {
                        const r = el.getBoundingClientRect();
                        if (r.x > 500 && (!best || r.width > best.getBoundingClientRect().width)) best = el;
                      }
                    }
                    if (best) best.scrollTop = 0;
                  }
                """)
                pg.wait_for_timeout(600)
            body = pg.evaluate("document.body.innerText")
            # thread pane = text after the last '\nBack\n' marker
            idx = body.rfind("\nBack\n")
            threads[name] = body[idx:] if idx != -1 else body
            print(f"OK {name}: {len(threads[name])} chars")
        except Exception as e:
            print(f"FAIL {name}: {e}")

    json.dump(threads, open(f"{OUT}/threads_full.json", "w"), indent=1)
    print("saved threads_full.json")
