#!/usr/bin/env python3
"""Convert index.html into a PageFly-ready Custom HTML/Liquid block.

- Rewrites local images/<name> refs to their Shopify CDN URLs (.cdn_cache.json).
- Extracts the <style> CSS and scopes EVERY selector under `.adv-root` so the
  page's generic rules (body, p, h1, a, *, etc.) cannot leak into the Shopify
  theme or PageFly's own chrome.
- Wraps the <body> inner HTML in <div class="adv-root">.
- Emits the paste block (pagefly-block.html) and a full-document preview
  (pagefly-preview.html) for local verification.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
HTML = (ROOT / "index.html").read_text()
CACHE = json.loads((ROOT / ".cdn_cache.json").read_text())

PREFIX = ".adv-root"

# 1) image refs -> CDN
for name, meta in CACHE.items():
    HTML = HTML.replace(f"images/{name}", meta["url"])
leftover = re.findall(r'(?:src|poster)="images/[^"]+"', HTML)
assert not leftover, f"unrewritten local refs: {leftover}"

# 2) pull out <style> ... </style> and <body> ... </body>
style_css = re.search(r"<style>(.*?)</style>", HTML, re.S).group(1)
body_inner = re.search(r"<body>(.*?)</body>", HTML, re.S).group(1)

# 3) scope the CSS
def split_rules(css):
    rules, i, n = [], 0, len(css)
    while i < n:
        prelude = ""
        while i < n and css[i] != "{":
            prelude += css[i]; i += 1
        if i >= n:
            break
        i += 1  # consume {
        depth, block = 1, ""
        while i < n and depth > 0:
            c = css[i]
            if c == "{": depth += 1
            elif c == "}": depth -= 1
            if depth > 0: block += c
            i += 1
        rules.append((prelude.strip(), block))
    return rules

def scope_selector_list(sel):
    out, seen = [], set()
    for p in (s.strip() for s in sel.split(",")):
        if not p:
            continue
        if p == ":root":
            scoped = ":root"
        elif p == "*":
            scoped = f"{PREFIX} *"
        elif p in ("html", "body"):
            scoped = PREFIX
        else:
            scoped = f"{PREFIX} {p}"
        if scoped not in seen:
            seen.add(scoped); out.append(scoped)
    return ", ".join(out)

def scope_css(css):
    parts = []
    for prelude, block in split_rules(css):
        if prelude.startswith("@media"):
            parts.append(f"{prelude} {{{scope_css(block)}}}")
        elif prelude.startswith("@"):  # keyframes/font-face — leave as-is
            parts.append(f"{prelude} {{{block}}}")
        else:
            parts.append(f"{scope_selector_list(prelude)} {{{block}}}")
    return "\n".join(parts)

scoped = scope_css(style_css)

# Hardening preamble: re-assert base typography at higher specificity than bare
# theme element rules (p{}, h1{}, a{} …) so the theme can't bleed INTO the block.
# color:inherit is limited to text holders that don't carry class-based colors,
# so design colors (statbox, dq, tcard …) are preserved.
HARDEN = (
    "/* PageFly hardening - keep theme base typography from bleeding in */\n"
    ".adv-root, .adv-root *{box-sizing:border-box;}\n"
    ".adv-root p,.adv-root h1,.adv-root h2,.adv-root h3,.adv-root h4,.adv-root a,"
    ".adv-root span,.adv-root div,.adv-root li,.adv-root td,.adv-root th,"
    ".adv-root b,.adv-root strong,.adv-root em,.adv-root button{"
    "font-family:inherit;letter-spacing:normal;}\n"
    ".adv-root h1,.adv-root h2,.adv-root h3,.adv-root h4{color:inherit;}\n"
    ".adv-root p,.adv-root li,.adv-root td,.adv-root th{color:inherit;line-height:inherit;}\n"
)
scoped = HARDEN + scoped

block = f"<style>\n{scoped}\n</style>\n<div class=\"adv-root\">{body_inner}</div>"
# ASCII-safe: convert every non-ASCII char (—, ·, ®, ★, ✓, emoji…) to a numeric
# HTML entity so PageFly can't double-encode it into mojibake. CSS is pure ASCII,
# so this only touches the visible text/attributes.
block = block.encode("ascii", "xmlcharrefreplace").decode("ascii")
(ROOT / "pagefly-block.html").write_text(block)

preview = (
    "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
    "<title>PageFly block preview</title>"
    # simulate a theme paragraph rule to prove scoping doesn't leak:
    # realistic hostile theme base typography (no !important):
    "<style>body{font-family:Georgia;margin:0;color:#0a0a0a;line-height:2} "
    "p{font-family:Georgia;color:#b30000;font-size:13px} h2{font-family:Georgia;color:#b30000} "
    ".theme-chrome{padding:20px;background:#222;color:#fff}</style></head><body>"
    "<div class=\"theme-chrome\"><p>THEME HEADER paragraph — should stay Georgia (proves no leak out)</p></div>"
    f"{block}"
    "<div class=\"theme-chrome\"><p>THEME FOOTER paragraph — should stay red &amp; Georgia</p></div>"
    "</body></html>"
)
(ROOT / "pagefly-preview.html").write_text(preview)

print("block bytes:", len(block))
print("scoped rules sample:", scoped[:200].replace("\n", " "))
print("wrote pagefly-block.html, pagefly-preview.html")
