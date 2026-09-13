#!/usr/bin/env python3
"""Rebuild the Motilli GLP-1 advertorial as a NATIVE PageFly page, using the
Alex Robinson "Health Insider" .pagefly export as the structural template.

Strategy: reuse the template's masthead Section verbatim, then build the article
Section by CLONING the template's Heading2 / Paragraph3 / Image3 / Button2 nodes
(preserving each node's classGlobalStyling AND its per-id entry in the top-level
styles[] array). Content is swapped to Motilli's editorial copy. Output is zipped
back into a .pagefly importable file.
"""
import json, copy, uuid, zipfile, re
from pathlib import Path

REF = Path("/Users/brooksorradre2/Documents/marketing brain/copywriting/advertorial/alex robinson skill references/export-pages-2025-11-24-21-12-47 (4).pagefly")
OUT_DIR = Path("/Users/brooksorradre2/Documents/marketing brain/brands/motilli/landing-pages/motilli-glp1-stuck-advertorial/pagefly-native")
OUT_DIR.mkdir(exist_ok=True)
PRODUCT_URL = "https://getmotilli.com/products/motilli-3-bottle-90day-reset"

CDN = {
    "receipt":  "https://cdn.shopify.com/s/files/1/0975/3201/9055/files/problem_receipt.png?v=1780351970",
    "gut":      "https://cdn.shopify.com/s/files/1/0975/3201/9055/files/gut_hero.png?v=1780351972",
    "jar":      "https://cdn.shopify.com/s/files/1/0975/3201/9055/files/motilli_jar.png?v=1780349344",
    "family":   "https://cdn.shopify.com/s/files/1/0975/3201/9055/files/relief_family.png?v=1780349349",
    "split":    "https://cdn.shopify.com/s/files/1/0975/3201/9055/files/mechanism_split.png?v=1780349341",
}
DIM = {"receipt": (2048,2048), "gut": (2048,1360), "jar": (1024,1024), "family": (2688,1520), "split": (1920,1080)}

# ---- load template json out of the .pagefly zip ----
with zipfile.ZipFile(REF) as z:
    name = [n for n in z.namelist() if n.endswith(".json")][0]
    tpl = json.loads(z.read(name))

items_by_id = {it["id"]: it for it in tpl["items"]}
styles_by_id = {st["id"]: st for st in tpl["styles"]}

def child_types(node):
    return [items_by_id[c]["type"] for c in node.get("children", []) if c in items_by_id]

# ---- locate source nodes ----
body = next(it for it in tpl["items"] if it["type"] == "Body")
layout = next(items_by_id[c] for c in body["children"] if items_by_id[c]["type"] == "Layout")
sections = [items_by_id[c] for c in layout["children"] if items_by_id[c]["type"] == "Section"]
mast_section = sections[0]
art_section_src = sections[1] if len(sections) > 1 else sections[0]

# masthead heading (white-span heading inside masthead section)
def descendants(nid):
    out = [nid]
    for c in items_by_id[nid].get("children", []):
        if c in items_by_id:
            out += descendants(c)
    return out
mast_ids = descendants(mast_section["id"])
mast_heading = next(items_by_id[i] for i in mast_ids if items_by_id[i]["type"] == "Heading2")

H_SRC = next(it for it in tpl["items"] if it["type"] == "Heading2" and "Icon" in child_types(it) and it["id"] != mast_heading["id"])
P_SRC = next(it for it in tpl["items"] if it["type"] == "Paragraph3")
IMG_SRC = next(it for it in tpl["items"] if it["type"] == "Image3")
BTN_SRC = next(it for it in tpl["items"] if it["type"] == "Button2")
ROW_SRC = next(it for it in tpl["items"] if it["type"] == "Row")
COL_SRC = next(it for it in tpl["items"] if it["type"] == "Column")

# ---- new graph accumulators ----
new_items = {}
new_styles = []

def nid():
    return str(uuid.uuid4())

def add_style(old_id, new):
    if old_id in styles_by_id:
        st = copy.deepcopy(styles_by_id[old_id]); st["id"] = new; new_styles.append(st)

def clone_rec(src_id):
    src = items_by_id[src_id]
    n = nid(); node = copy.deepcopy(src); node["id"] = n
    node["children"] = [clone_rec(c) for c in src.get("children", []) if c in items_by_id]
    new_items[n] = node; add_style(src_id, n)
    return n

def clone_flat(src_id):
    src = items_by_id[src_id]
    n = nid(); node = copy.deepcopy(src); node["id"] = n; node["children"] = []
    new_items[n] = node; add_style(src_id, n)
    return n

def H(text):
    n = clone_rec(H_SRC["id"]); new_items[n]["data"]["value"] = text; return n

def P(html):
    n = clone_flat(P_SRC["id"]); new_items[n]["data"]["value"] = html; return n

def IMG(key, alt):
    n = clone_flat(IMG_SRC["id"]); w, h = DIM[key]
    new_items[n]["data"].update(src=CDN[key], alt=alt, width=w, height=h,
                                naturalWidth=w, naturalHeight=h)
    return n

def BTN(text):
    n = clone_rec(BTN_SRC["id"])
    new_items[n]["data"]["value"] = text
    new_items[n]["data"]["href"] = PRODUCT_URL
    return n

# ---- copy masthead subtree verbatim (ids + styles) and set its text ----
for i in mast_ids:
    new_items[i] = copy.deepcopy(items_by_id[i])
    if i in styles_by_id:
        new_styles.append(copy.deepcopy(styles_by_id[i]))
new_items[mast_heading["id"]]["data"]["value"] = '<span style="color: rgb(255, 255, 255);">GLP-1 Wellness Insider</span>'

# ---- Motilli editorial content, in order ----
SEP = " &nbsp;·&nbsp; "
content = []
content.append(H("Stuck on Your GLP-1? Bloated, Burping, and Going Days Without?"))
content.append(P("<strong>Linda K.</strong> — On Mounjaro&reg; for 11 months · Lost 34 lbs" + SEP +
                 "GLP-1 Wellness Insider · Updated April 2026 · &#10003; Verified GLP-1 User"))
content.append(P('No more "cement stomach." No more sulfur burps that clear a room. No more sitting there '
                 'waiting for something — anything — to happen. These celery juice gummies are helping '
                 '<strong>10,000+ women</strong> on GLP-1 medications get their normal mornings back — '
                 "here's exactly how it works.*"))
content.append(P("&#8594; If you've been on Ozempic&reg;, Wegovy&reg;, Mounjaro&reg;, Zepbound&reg;, or "
                 "Rybelsus&reg; and your stomach feels like wet cement after every meal, you're bloated, "
                 "and you haven't gone in days…<br><br>"
                 "&#8594; If you've already tried the obvious things — Miralax, fiber, stool softeners — "
                 "and they either did nothing or made the bloating worse…<br><br>"
                 "&#8594; If you've started to wonder whether you'll have to quit the medication just to "
                 "feel normal again…"))
content.append(P("I was you. I tried fiber. I tried laxatives. I tried stool softeners. Nothing worked. "
                 "Some of them actually made the bloating worse. I was ready to quit Mounjaro&reg; and "
                 "throw away thirty-four pounds of progress."))
content.append(P("Then a friend showed me something that changed everything. It was designed specifically "
                 "for people on GLP-1 medications — not a normal gut. A slow GLP-1 gut. Let me show you why "
                 "it works when everything else doesn't.*"))
content.append(P("<strong>50% of people quit their GLP-1 medication</strong> because of side effects like "
                 "these. Motilli is built to help you stay in the other half — without giving up the weight "
                 "loss.* <em>(Source: published GLP-1 discontinuation data, 2025)</em>"))

content.append(H("The $150 Problem Nobody Adds Up"))
content.append(P("Before I found what actually helped, I spent months buying things that were never going to "
                 "work. Here's my actual receipt:"))
content.append(IMG("receipt", "My receipt: fiber gummies $12, Miralax $25, stool softener $18, mag citrate $9, prescription $90 — $154 wasted, versus Motilli at $29.99/mo."))
content.append(P("I was already paying over $900 a month for my Mounjaro. Thirty dollars to actually feel "
                 "comfortable living in the body it was giving me — that math took me way too long to find.*"))

content.append(H("Here's What Your Doctor Never Explained"))
content.append(IMG("gut", "Your stomach basically stops moving — your GLP-1 slows your stomach by 50% or more, so food sits, ferments, and hardens."))
content.append(P("Here's what nobody tells you when you start these medications: GLP-1s don't just quiet your "
                 "appetite. They slow your stomach — the very top of your digestive system — by 50% or more. "
                 "That's how they work. But it also means food stops moving when it should, sits where it "
                 "shouldn't, and the problems start at the top, not in the colon.*"))
content.append(P("I spent three weeks pouring things into my colon. Laxatives, fiber, stool softeners. None "
                 "of it touched what was happening."))
content.append(P("<strong>Stimulant laxatives</strong> (Dulcolax, Senna, Ex-Lax) force your colon to "
                 "contract. But the medication is already suppressing those contractions — so you're fighting "
                 "your own prescription. The result is cramping, urgency, or nothing at all. And the colon was "
                 "never the problem."))
content.append(P("<strong>Fiber supplements</strong> (Metamucil, Benefiber) add bulk to push things along. "
                 "But bulk needs movement to work — and my stomach had barely any. Adding bulk to a jammed "
                 "system just made the bloating worse. Every woman I've talked to in the GLP-1 groups says the "
                 "same thing about fiber."))
content.append(P("<strong>Miralax</strong> pulls water into the colon. But nothing was stuck in my colon — it "
                 "was stuck in a stomach that wouldn't empty. Aimed at the wrong organ entirely, did nothing "
                 "for the sulfur burps, and I kept needing more for less.*"))
content.append(P("<strong>And the sulfur burps?</strong> Nothing in the laxative aisle even tries. That "
                 "rotten-egg smell is hydrogen sulfide gas — food fermenting in a stomach that stopped moving. "
                 "No laxative touches the gas, because no laxative works on the stomach.*"))
content.append(P("The fix isn't more force on the wrong end. It's doing three specific things at the same "
                 "time, on the organ that's actually slowed.*"))
content.append(IMG("split", "Every laxative aims at the colon. Motilli works at the stomach with three actions — motility, sulfur, soften."))

content.append(H("One More Thing — And This Was My Biggest Question"))
content.append(P("Before I go further: when I first read that something could restore my stomach's movement, "
                 "my first thought was that it would cancel my weight loss."))
content.append(P("It won't. And I want to explain why, because it almost stopped me from trying this."))
content.append(P("Your medication does two separate things to your stomach. One part controls how fast food "
                 "empties out — that's the slowdown that makes you feel full faster. That's the appetite "
                 "suppression. That's the weight loss. Your medication does that on purpose, and you want to "
                 "keep it."))
content.append(P("The other part is the natural muscle movement that should still be carrying food through "
                 "the stomach — that movement also stalls on the medication, and that's where the backup "
                 "comes from. That's what Motilli restores."))
content.append(P("Two different jobs. Two different parts of the stomach. Motilli only touches the second "
                 "one. My appetite suppression never changed. I'm still losing weight. I just stopped paying "
                 "the tax for it every single day.*"))

content.append(H("The Three-Part Formula That Works On The Stomach"))
content.append(IMG("jar", "Motilli celery juice fiber gummies — the three-part daily formula for a slowed GLP-1 stomach."))
content.append(P("When I went looking for something that did all three — at the doses that actually matter — I "
                 "couldn't find it on the supplement shelf. What's out there is mostly a general gut gummy with "
                 "a new label. The one formula built specifically for a slowed GLP-1 stomach is "
                 "<strong>Motilli</strong>. Here's what each part does, and why all three have to work "
                 "together:*"))
content.append(P("<strong>Part 1 — Motility.</strong> Apigenin, from cold-pressed celery juice concentrate. It "
                 "supports the stomach's natural muscle movement — the exact signal the medication quieted. It "
                 "doesn't override the medication. It restores the carrying movement without touching the "
                 "fullness control.*"))
content.append(P("<strong>Part 2 — Gas Neutralization.</strong> Sodium copper chlorophyllin. It binds directly "
                 "to hydrogen sulfide — the specific molecule behind the rotten-egg burps — and disarms it "
                 "before it rises. It doesn't mask the smell. It neutralizes what makes it.*"))
content.append(P("<strong>Part 3 — Downstream Flow.</strong> Low-bulk soluble prebiotic fiber. The opposite of "
                 "the bulking fiber that made me feel worse. It softens and draws in moisture without adding "
                 "bulk to a system that's already jammed — so things clear once the stomach starts moving "
                 "again.*"))
content.append(P("<strong>Why all three, and not just one?</strong> Restore movement but leave the sulfur gas, "
                 "and the gas keeps distending the stomach and slowing it back down. Neutralize the gas but "
                 "never restore movement, and food keeps sitting and making more. Soften downstream but leave "
                 "the stomach stalled, and nothing new arrives to move. Each one alone is a door with two "
                 "locks still shut. That's why the single-ingredient products I tried first did a little, then "
                 "stopped.*"))

content.append(H("What's Inside Motilli — And Why Each One Matters"))
content.append(P("&#127793; <strong>Celery Juice Concentrate</strong> (standardized for Apigenin) — supports "
                 "the stomach's natural muscle movement your medication quieted, so food moves through instead "
                 "of sitting and fermenting.*<br><br>"
                 "&#128994; <strong>Sodium Copper Chlorophyllin</strong> — binds hydrogen sulfide, the gas "
                 "behind egg burps, and neutralizes it at the source instead of covering the smell.*<br><br>"
                 "&#128167; <strong>Low-Bulk Soluble Fiber</strong> (prebiotic, gel-forming) — softens and "
                 "lubricates without adding bulk to a backed-up system. The opposite of the fiber that makes "
                 "bloating worse.*<br><br>"
                 "&#9889; <strong>Folate (5-MTHF) + B6</strong> (methylated, bioavailable) — when you eat less, "
                 "you absorb less. These are in the active forms your body can actually use.*<br><br>"
                 "&#128737;&#65039; <strong>Vitamins A, C &amp; K</strong> — the nutrients that quietly run low "
                 "on a reduced-calorie GLP-1 diet, built into the same two gummies.*<br><br>"
                 "&#127811; <strong>No Stimulants. No Bulk.</strong> Nothing that forces a contraction the "
                 "medication is suppressing. Works with the slowed system, not against it — so no cramping.*"))
content.append(P("<strong>Motilli — Celery Juice Fiber Gummies</strong><br>&#9733;&#9733;&#9733;&#9733;&#9733; "
                 "4.7 out of 5 · 2,107 reviews" + SEP + "$29.99/mo" + SEP +
                 "&#9733; Buy 2, Get 1 FREE — limited time" + SEP + "&#128155; 90-Day Money-Back Guarantee"))
content.append(BTN("Start Feeling Normal Again &#8594;"))

content.append(H("What Happened to Me — Week by Week"))
content.append(P("I was skeptical. I'd already tried everything. But the mechanism made sense in a way that "
                 "nothing else had. So I ordered a jar. Two gummies after dinner. And here's what happened:*"))
content.append(P("<strong>Day 1.</strong> Two gummies after dinner. No cramping. No urgency. Just went to bed "
                 "normally.*"))
content.append(P("<strong>Days 3–5.</strong> The burps went first. I ate the onion rings at dinner on day four "
                 "because my husband ordered them and I thought, fine, I'll deal with it later. I didn't have "
                 "to.*"))
content.append(P("<strong>Week 1–2.</strong> The cement started lifting. I went on my own — no Miralax, no "
                 "pushing, just normal. I actually sat there for a second not believing it was happening.*"))
content.append(P("<strong>Week 3–4.</strong> I stopped planning my day around the bathroom. My daughter's "
                 "birthday dinner, I stayed for the whole thing. Didn't think about it once until the drive "
                 "home, when I realized I hadn't thought about it.*"))
content.append(P("<strong>Month 2+.</strong> Normal most mornings. Still on my Mounjaro. Still losing weight. "
                 "My sister started asking what changed because she said I just looked different — more "
                 "relaxed, she said. She's on Ozempic. I sent her a jar.*"))
content.append(IMG("family", "A woman in her late 50s, relaxed and laughing at an outdoor family table."))
content.append(P("<em>The marker isn't a lab number. It's the afternoon you stay for the whole thing.</em>"))

content.append(H("Why I Started Writing About This At All"))
content.append(P("I've been in the GLP-1 support groups for almost a year. I watch the same conversation "
                 "happen every single week — someone posts that they're ready to quit their medication because "
                 "the constipation is unbearable, everyone recommends Miralax and fiber, it doesn't work, they "
                 "ask what else there is. Nobody mentions that the whole category of solutions is aimed at the "
                 "wrong organ."))
content.append(P("I'm not a doctor. I'm a retired high school principal from Ohio who spent three nights "
                 "reading PubMed at midnight because I wasn't willing to give up thirty-four pounds. When I "
                 "found the stomach-versus-colon explanation, everything I'd tried made sense for the first "
                 "time — it wasn't that I'd been unlucky, it was that every product I'd tried was built for a "
                 "different body."))
content.append(P("If I'd understood this in month one, I would have saved four months and about $150. That's "
                 "why I write about it now.*"))
content.append(BTN("Get Gentle Relief Now &#8594;"))

content.append(H("What Women Are Telling Me"))
content.append(P('<strong>Carol R., 59 · On Wegovy&reg; for 7 months</strong> &#9733;&#9733;&#9733;&#9733;&#9733;'
                 '<br>"I\'d tried everything — Miralax every single day, mag citrate, three kinds of fiber. I '
                 'was so sure this was just another gummy I almost didn\'t order. Week one my husband noticed '
                 'the burps were gone before I did. By week five I\'d stopped the Miralax completely, which I '
                 'hadn\'t managed in a year. Still on my Wegovy, still losing. I just don\'t dread eating '
                 'anymore."'))
content.append(P('<strong>Janet M., 63 · On Mounjaro&reg; for 10 months</strong> &#9733;&#9733;&#9733;&#9733;&#9733;'
                 '<br>"The part that got me was being able to delete the note on my phone where I tracked the '
                 'last time I\'d gone — that\'s how bad Mounjaro made it. I\'m on my second jar and I deleted it '
                 'last week. The buy-two-get-one meant I could send the spare to my sister, who\'s on Ozempic '
                 'and right where I was a year ago."'))
content.append(P('<strong>Sue D., 61 · On Ozempic&reg; for 13 months</strong> &#9733;&#9733;&#9733;&#9733;&#9733;'
                 '<br>"I\'m a retired nurse, so I\'ve seen every supplement scam there is. What sold me was that '
                 'it didn\'t pretend to be a cure-all — it does three specific things and that\'s it. Sulfur '
                 'burps gone in about a week. By two months I sat through my granddaughter\'s whole recital — '
                 'the year before I\'d left halfway through. Worth every penny."'))
content.append(P('<strong>Donna K., 56 · On Zepbound&reg; for 5 months</strong> &#9733;&#9733;&#9733;&#9733;&#9733;'
                 '<br>"Eight days without going. Fiber made it worse, Miralax barely touched it. The '
                 'stomach-not-colon thing finally made sense. No cramps, no emergency — it just gently started '
                 'working by the end of the first week. I\'m staying on my medication now. I wasn\'t going to '
                 'before."'))

content.append(H("Don't Quit Your Medication Over This."))
content.append(P("Your medication is doing its job. Your stomach just needs the right support to catch up.* "
                 "People who quit early lose far less of the weight than those who stay. You shouldn't have to "
                 "choose between losing the weight and feeling human — and with Motilli, you don't.*"))
content.append(BTN("Start Feeling Normal Again &#8594;"))
content.append(P("&#128155; <strong>90-Day Money-Back Guarantee.</strong> Try Motilli for a full 90 days. The "
                 "longer your stomach has been slowed, the longer it takes to restore its natural muscle "
                 "movement — so use every day of it. If your digestion hasn't come back, you get every cent "
                 "back. No questions.*  ·  Made in USA"))

# ---- build article Section -> Row -> Column(content) ----
art_col = clone_flat(COL_SRC["id"]); new_items[art_col]["children"] = content
art_row = clone_flat(ROW_SRC["id"]); new_items[art_row]["children"] = [art_col]
art_sec = clone_flat(art_section_src["id"]); new_items[art_sec]["children"] = [art_row]

# ---- Body + Layout (verbatim ids) wrapping masthead + article ----
new_items[body["id"]] = copy.deepcopy(body)
if body["id"] in styles_by_id: new_styles.append(copy.deepcopy(styles_by_id[body["id"]]))
new_items[layout["id"]] = copy.deepcopy(layout)
if layout["id"] in styles_by_id: new_styles.append(copy.deepcopy(styles_by_id[layout["id"]]))
new_items[body["id"]]["children"] = [layout["id"]]
new_items[layout["id"]]["children"] = [mast_section["id"], art_sec]

# ---- assemble + prune to reachable ----
reachable = set(descendants_new := [])
def walk_new(i):
    if i in reachable: return
    reachable.add(i)
    for c in new_items[i].get("children", []):
        if c in new_items: walk_new(c)
walk_new(body["id"])

out = copy.deepcopy(tpl)
out["items"] = [new_items[i] for i in new_items if i in reachable]
out["styles"] = [st for st in new_styles if st["id"] in reachable]
# de-dup styles by id (masthead copy + clones)
seen = set(); ded = []
for st in out["styles"]:
    if st["id"] not in seen: seen.add(st["id"]); ded.append(st)
out["styles"] = ded

# ASCII-safe every rendered text field: PageFly renders Heading/Paragraph/Button
# `value` and Image `alt` as HTML, so converting non-ASCII (—, ·, –, ®, ★, ✓, emoji)
# to numeric HTML entities makes them bulletproof against PageFly's charset handling
# (which was double-encoding the raw UTF-8 into â€" / Â· gibberish).
def _esc(s):
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")
for _it in out["items"]:
    _d = _it.get("data")
    if isinstance(_d, dict):
        for _k in ("value", "alt"):
            if isinstance(_d.get(_k), str):
                _d[_k] = _esc(_d[_k])

json_name = "1 - Motilli GLP-1 Stuck.json"
json_path = OUT_DIR / json_name
json_path.write_text(json.dumps(out, ensure_ascii=False))
pagefly_path = OUT_DIR / "motilli-glp1-stuck.pagefly"
with zipfile.ZipFile(pagefly_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(json_path, arcname=json_name)

# sanity
types = {}
for it in out["items"]: types[it["type"]] = types.get(it["type"], 0) + 1
# orphan check: every child id exists
allids = {it["id"] for it in out["items"]}
missing = [c for it in out["items"] for c in it.get("children", []) if c not in allids]
print("items:", len(out["items"]), "| styles:", len(out["styles"]))
print("type counts:", types)
print("missing child refs:", missing[:5], "(", len(missing), ")")
print("roots:", [it["type"] for it in out["items"] if it["id"] not in {c for x in out["items"] for c in x.get('children',[])}])
print("wrote:", pagefly_path)
