#!/usr/bin/env python3
"""Normalize official press logos for inlining: ink monochrome, viewBox-safe,
strip width/height, namespace ids, single-line. Outputs <name>.norm.svg."""
import re
INK = "#1a1411"
FILES = {
    "usatoday": "usatoday.svg",
    "foxwordmark": "foxwordmark.svg",
    "cosmopolitan": "cosmopolitan.svg",
    "forbes": "forbes.svg",
    "womenshealth": "womenshealth.svg",
}
for key, fn in FILES.items():
    s = open(fn).read()
    s = s[s.find("<svg"):]                      # drop xml decl / comments
    tag = re.search(r"<svg[^>]*>", s, re.S).group(0)
    nt = tag
    if "viewBox" not in nt:                      # synthesize viewBox from width/height
        w = re.search(r'\bwidth="([\d.]+)', nt); h = re.search(r'\bheight="([\d.]+)', nt)
        if w and h:
            nt = nt[:-1] + f' viewBox="0 0 {w.group(1)} {h.group(1)}">'
    nt = re.sub(r'\s(width|height)="[^"]*"', "", nt)   # let CSS size it
    s = s.replace(tag, nt, 1)
    # ink-out every hex fill/stroke; leave 'none'
    s = re.sub(r'(fill|stroke)="#[0-9A-Fa-f]{3,8}"', lambda m: f'{m.group(1)}="{INK}"', s)
    s = re.sub(r'(fill|stroke):\s*#[0-9A-Fa-f]{3,8}', lambda m: f'{m.group(1)}:{INK}', s)
    # namespace ids so multiple inlined logos don't collide
    for _id in set(re.findall(r'id="([^"]+)"', s)):
        ns = f"{key}-{_id}"
        s = re.sub(r'id="' + re.escape(_id) + r'"', f'id="{ns}"', s)
        for pat in (f'url(#{_id})', f'href="#{_id}"', f'xlink:href="#{_id}"'):
            s = s.replace(pat, pat.replace(f'#{_id}', f'#{ns}'))
    s = re.sub(r"<svg(\s)", r'<svg class="plogo"\1', s, count=1)
    s = re.sub(r">\s+<", "><", s).strip()       # collapse whitespace
    open(f"{key}.norm.svg", "w").write(s)
    print(f"{key:14s} {len(s):5d} bytes")
