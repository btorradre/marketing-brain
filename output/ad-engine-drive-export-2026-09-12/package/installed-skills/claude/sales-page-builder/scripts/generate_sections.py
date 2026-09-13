#!/usr/bin/env python3
"""
Split the single-file sales page into TWO Shopify theme sections at the buy-box
slot, inlining the Shopify Files CDN urls. The native buy box goes BETWEEN them.

The page HTML must keep these exact comment markers (the example does):
    <!-- ============ HERO ============ -->            (start of the page body)
    <!-- ============ BUY BOX ============ -->         (offer slot — REMOVED; native box takes its place)
    <!-- ============ BEFORE & AFTER ============ -->  (start of the bottom half)
    <!-- ============ FOOTER ============ -->          (we stop before the fake footer; theme footer stays)

Prereq: /tmp/sp_cdn.json (from upload_files.py).
Output: BASE/shopify/sp-<SLUG>-top.liquid  and  sp-<SLUG>-bottom.liquid
"""
import json, re

# ===================== EDIT PER BRAND =====================
BASE   = "/abs/path/to/brands/<brand>"
SOURCE = f"{BASE}/sales-page.html"       # your assembled single-file page
SLUG   = "thyroid"                        # short slug -> section/template/page names
# =========================================================

html = open(SOURCE).read()
cdn  = json.load(open("/tmp/sp_cdn.json"))

style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
# keep the theme header + footer (real cart): drop the chrome-hide rule if present
style = re.sub(r"\s*[^\n]*shopify-section-group-(header|footer)-group[^\n]*display:none[^\n]*\n", "\n", style)

def between(a, b):
    return html[html.index(a):html.index(b)]

TOP    = between("<!-- ============ HERO ============ -->",
                 "<!-- ============ BUY BOX ============ -->")
BOTTOM = between("<!-- ============ BEFORE & AFTER ============ -->",
                 "<!-- ============ FOOTER ============ -->")

def swap(s):
    for name, url in cdn.items():
        s = s.replace(f"generated-images/{name}", url)
    assert "generated-images/" not in s, "unmapped image — add it to upload_files.py IMAGES"
    return s
TOP, BOTTOM = swap(TOP), swap(BOTTOM)

DISCLAIMER = """
<section class="section" style="padding:30px 0;background:var(--cream-3);border-top:1px solid var(--line);">
  <div class="wrap center"><p class="disclaimer" style="max-width:680px;margin:0 auto;">
  These statements have not been evaluated by the Food and Drug Administration. This product is not intended to
  diagnose, treat, cure, or prevent any disease. Content on this page is not medical advice and should not replace
  consultation with a qualified healthcare provider.</p></div></section>
"""

top = (f'<style>{style}</style>\n<div id="rv-adv">\n{TOP}\n'
       '<a id="buy" aria-hidden="true" style="display:block;position:relative;top:-30px;visibility:hidden;"></a>\n</div>\n'
       '{% schema %}\n{"name":"Sales Page Top","tag":"section","class":"sp-section","settings":[]}\n{% endschema %}\n')
bottom = (f'<div id="rv-adv">\n{BOTTOM}\n{DISCLAIMER}\n</div>\n'
          '{% schema %}\n{"name":"Sales Page Bottom","tag":"section","class":"sp-section","settings":[]}\n{% endschema %}\n')

open(f"{BASE}/shopify/sp-{SLUG}-top.liquid", "w").write(top)
open(f"{BASE}/shopify/sp-{SLUG}-bottom.liquid", "w").write(bottom)
print(f"wrote sp-{SLUG}-top.liquid ({len(top)}b) + sp-{SLUG}-bottom.liquid ({len(bottom)}b); images mapped: {len(cdn)}")
