#!/usr/bin/env python3
"""Transform the 'Health Insider Kids' PageFly template into the Motilli GLP-1
confession advertorial: keep the element scaffold + styles, swap in confession
copy and Motilli CDN images, re-zip as a .pagefly import file."""
import json, uuid, zipfile, copy
from pathlib import Path

SRC = Path('extracted/1 - Health Insider Kids.json')
OUT_JSON_NAME = '1 - GLP-1 Insider Confession.json'
OUT_PAGEFLY = Path('../motilli-glp1-confession.pagefly')

PRODUCT_URL = 'https://getmotilli.com/products/motilli-3-bottle-90day-reset'
HERO = 'https://cdn.shopify.com/s/files/1/0975/3201/9055/files/gut_hero_b65bda29-393f-44a6-8738-b8b384bb7238.jpg?v=1780359901'
JAR  = 'https://cdn.shopify.com/s/files/1/0975/3201/9055/files/motilli_jar_586cd2e4-9d01-4550-8409-139aab432f6d.png?v=1780359000'

d = json.load(open(SRC))
items = d['items']
styles = d['styles']
by = {i['id']: i for i in items}
style_by = {s['id']: s for s in styles}

new_items = []   # cloned items to append
new_styles = []  # cloned styles to append

def clone_tree(root_id):
    """Deep-clone an element subtree with fresh ids; clone matching style entries."""
    old = by[root_id]
    new = copy.deepcopy(old)
    nid = str(uuid.uuid4())
    new['id'] = nid
    # clone children recursively
    new['children'] = [clone_tree(c) for c in old.get('children', [])]
    new_items.append(new)
    # clone style entry if present
    if root_id in style_by:
        st = copy.deepcopy(style_by[root_id])
        st['id'] = nid
        new_styles.append(st)
    by[nid] = new
    return nid

# ---- prototypes ----
HEAD_PROTO = 'd000674d-7668-485a-a744-c09f7f7c98c5'   # section Heading2 (+Icon)
PARA_PROTO = '59b6b531-585b-4bef-973e-e0e1efcb2e73'   # body Paragraph3 (+Dropcap)
IMG_PROTO  = 'ee1e3d73-3736-47b2-8ad2-f1c8867952b7'   # hero Image3

def H(text):
    nid = clone_tree(HEAD_PROTO)
    by[nid]['data']['value'] = text
    return nid

def P(html):
    nid = clone_tree(PARA_PROTO)
    by[nid]['data']['value'] = html
    return nid

def IMG(src, alt, w, h):
    nid = clone_tree(IMG_PROTO)
    dat = by[nid]['data']
    dat['src'] = src; dat['alt'] = alt
    dat['naturalWidth'] = w; dat['naturalHeight'] = h
    dat['width'] = w; dat['height'] = h
    return nid

# ---- reused (edit in place) ----
by['bde5bfc3-47cf-4dba-8166-1f20b5269180']['data']['value'] = '<span style="color: rgb(255, 255, 255);">The GLP-1 Insider</span>'  # masthead
TITLE = "How A Gastroenterologist's Confession About My Wegovy® Side Effects Exposed Why Most GLP-1 Users Stay Bloated, Backed Up, And Burping Sulfur"
by['7faab936-2204-474b-a74b-3e9bd0291f34']['data']['value'] = TITLE
by['77d966e5-4012-4a9b-888f-ff4ee0dc61a7']['data']['value'] = TITLE
by['b2e66e48-0c29-41d4-9530-5a4d7bfeb321']['data']['value'] = 'November 14th, 2025 at 8:42 am EDT'  # dateline
by['1a1c19a9-6430-4c54-b11c-08c9146e30e3']['data']['value'] = (
    "I'd lost 34 pounds on Wegovy®. I also hadn't gone in over a week, and the burps were humiliating. "
    "Then my gastroenterologist told me I'd been treating the wrong organ the whole time — and everything "
    "in my cabinet was aimed at the wrong one. <strong>— Janet R.</strong>")  # lede / quote

# hero image
hd = by['ee1e3d73-3736-47b2-8ad2-f1c8867952b7']['data']
hd['src'] = HERO; hd['alt'] = 'Tired woman in her early 50s at her kitchen table, hand on her stomach'
hd['naturalWidth'] = 1400; hd['naturalHeight'] = 791; hd['width'] = 1400; hd['height'] = 791

# main CTA button
mb = by['124dc607-fe03-43d9-80e2-2950fe360c4c']['data']
mb['value'] = 'CLAIM BUY 2, GET 1 FREE — FREE SHIPPING'
mb['href'] = PRODUCT_URL
# sidebar CTA button
sb = by['c54afa12-6b16-4191-bed1-324ea07ec41e']['data']
sb['value'] = 'CHECK AVAILABILITY'
sb['href'] = PRODUCT_URL

# sidebar block
sd1 = by['8c348467-fd86-46e2-8a1f-1d987d322b94']['data']  # product image
sd1['src'] = JAR; sd1['alt'] = 'Motilli jar with green gummies'
sd1['naturalWidth'] = 1024; sd1['naturalHeight'] = 1024; sd1['width'] = 1024; sd1['height'] = 1024
by['cdf00e13-cd0f-49c4-9377-4d22c237499c']['data']['value'] = 'Keep Your Medication. Keep Your Mornings — With Motilli'  # sidebar heading
sd2 = by['f6ed571a-0af4-4dfc-85d7-01b59e1c32c6']['data']  # second sidebar image
sd2['src'] = JAR; sd2['alt'] = 'Motilli gummies'
sd2['naturalWidth'] = 1024; sd2['naturalHeight'] = 1024; sd2['width'] = 1024; sd2['height'] = 1024
by['057547e3-1a71-4863-a68d-21124e5b3a75']['data']['value'] = (
    'The gastroenterologist-recommended formula made for GLP-1 side effects. '
    'Motility, gas, and downstream flow — all three, in one gummy. About a dollar a day.')  # sidebar desc

# footer
by['f5390d99-bbae-40f2-b981-d75cfa04eb73']['data']['value'] = '© 2025 The GLP-1 Insider. All Rights Reserved. Privacy Policy Terms of Use'
by['6fc8d185-5856-4acc-85c8-d28f658817c2']['data']['value'] = (
    'THIS IS AN ADVERTISEMENT AND NOT AN ACTUAL NEWS ARTICLE, BLOG, OR CONSUMER PROTECTION UPDATE. '
    'Ozempic®, Wegovy®, Mounjaro®, and Zepbound® are registered trademarks of their respective owners, '
    'none of which are affiliated with or endorse Motilli. These statements have not been evaluated by the FDA. '
    'This product is not intended to diagnose, treat, cure, or prevent any disease. Individual results vary.')

# ---- body content ----
body = [
 ('p','<strong>"You\'re not backed up where you think you\'re backed up."</strong>'),
 ('p',"I'd come in because I hadn't gone in nine days, my stomach felt like it was full of wet cement, and I couldn't stop burping something that smelled like rotten eggs."),
 ('p','"But I\'ve tried everything," I said. "Miralax, magnesium, fiber, probiotics. Three months. Nothing moved."'),
 ('p','Dr. Marsh barely looked at the list. "Everything you\'ve been taking was built for a problem you don\'t have."'),
 ('p',"She's a gastroenterologist. For two years she'd seen almost nothing but GLP-1 patients — and she said it was happening to nearly all of them. The weight came off, and the digestion quietly ground to a halt."),
 ('p','"The problem isn\'t where you think it is," she said. "And once you see where it actually is, your whole cabinet makes sense. None of it could have worked."'),
 ('p','That was the part no nine-minute appointment had ever told me — and it\'s the part that saved me from another $400 in pills, and from the one "fix" my doctor floated that would have cost me every pound I\'d lost.'),
 ('h','The Thing My Doctor Never Said In Nine Minutes'),
 ('p',"Here's what Dr. Marsh confirmed, in plain language, the way no one had bothered to."),
 ('p',"The medication doesn't slow the colon. It slows the <strong>stomach</strong>. Food sits there for hours — sometimes days. It ferments, and that's the sulfur. It dries out and hardens, and that's the cement feeling. By the time anything reaches the colon, it's already hard, and there's barely anything there."),
 ('p','The colon was never blocked. It was nearly empty.'),
 ('p','"And everything you\'ve been taking," she said, "is aimed at the colon. The problem was never there. It\'s at the stomach."'),
 ('p',"I'd had it backwards for three months. So had every doctor I'd raised it to."),
 ('h',"Why Your Regular Doctor Won't Get You Here"),
 ('p','I asked her why nobody else had said any of this.'),
 ('p','Time, mostly. A primary-care visit isn\'t built to work out which organ a side effect actually starts in, so "common" constipation gets the common answer — more water, more fiber, give it time. And the right answer is newer than the problem. The prescriptions exploded faster than the playbook updated.'),
 ('p',"So millions of women got handed colon advice for a stomach problem, and were told they just weren't doing it hard enough."),
 ('p',"That's the part that made me angry. I hadn't been failing. Every tool I reached for was pointed at the wrong organ."),
 ('p',"<strong>Miralax</strong> pulls water into the colon to soften what's sitting there — but nothing was sitting there."),
 ('p',"<strong>Fiber gummies</strong> add bulk in the colon to push things along — but when food can't leave the stomach, more bulk only makes the jam worse."),
 ('p','<strong>Dulcolax</strong> forces the colon to squeeze — and you can squeeze an empty pipe all day and nothing comes out.'),
 ('p','<strong>Smooth Move</strong> stimulates the lower intestine — but the holdup is at the stomach, not the bottom.'),
 ('p','"These aren\'t bad products," she said. "They\'re just aimed at the colon. Your problem moved up to the stomach the day you started the shot."'),
 ('h','The Three Things That Actually Work On The Stomach'),
 ('p','So the real question was simple: what works on the stomach?'),
 ('p',"She'd spent months in the research. Three things kept surfacing, and the solution needed all three."),
 ('p','The first was <strong>apigenin</strong>, a compound concentrated in celery. It supports the vagus nerve — the one that tells the stomach when to contract and push food through. GLP-1 medications mute that signal. Apigenin helps the stomach start contracting again.'),
 ('p',"And no, it doesn't undo the weight loss. The appetite control happens in your brain. The stomach slowing is separate and local. Apigenin only moves the stomach from frozen back to slow — it doesn't touch why you're eating less. You keep every bit of the appetite control."),
 ('p',"That handled motility. But weeks of slow digestion meant the sulfur gas was already there, and getting things moving doesn't neutralize gas that's already formed. So the second was <strong>chlorophyllin</strong>. It binds to hydrogen sulfide and disarms it before it rises. It doesn't mask the smell — it neutralizes the molecule that makes it."),
 ('p',"And everything downstream was still backed up from weeks of stalled digestion. The third was a specific <strong>low-bulk soluble fiber</strong> — not the bulk fiber every doctor pushes, which is the last thing a jammed system needs. This kind draws moisture in and softens what's stuck without adding volume, so things can clear once the stomach is working again."),
 ('p','Motility. Gas neutralization. Downstream flow. All three, together.'),
 ('p','"That\'s why your cabinet never had a chance," she said. "Every product did one piece. Most did the wrong piece."'),
 ('h','So I Tried Juicing The Celery Myself'),
 ('p',"My first thought walking out of there was that I'd skip the supplement aisle entirely. Apigenin comes from celery. Celery's three dollars a bunch. I'd just juice it myself."),
 ('p','So I bought a juicer and started.'),
 ('p',"It took over my kitchen. Bunches of celery every few days, the counter wet with it, pulp everywhere, twenty minutes of prep before my biggest meal — every single day, or it didn't count. And once I was buying the volume you'd need to get anywhere near what the research used, the grocery bill climbed faster than the pills ever had."),
 ('p',"I lasted about two weeks before I admitted I'd never keep it up."),
 ('p',"And juicing only ever got me one of the three pieces anyway. Celery juice gets you somewhere near the apigenin, and nothing else. It does nothing for the sulfur gas already built up — that needs the chlorophyll. It leaves the backup downstream right where it was, because softening that takes the soluble fiber, not more liquid. And a glass I made at home came with no label — no way to know whether I was getting the dose the research used or a fraction of it."),
 ('p',"I needed all three, at the right amounts, in something I'd actually take every day. Juicing was none of that."),
 ('p','That\'s when Dr. Marsh named the one company that had built exactly that: <strong>Motilli</strong>. A gummy made specifically for people on GLP-1 medications — not a general digestive supplement with a new label.'),
 ('img_jar',),
 ('p',"I'll be honest — a gummy felt too easy. Three weeks earlier I'd left my daughter's birthday dinner before the cake because I couldn't sit through it. Green candy was supposed to fix that?"),
 ('p',"But I checked it against everything she'd told me. <strong>Celery juice concentrate standardized for apigenin. Chlorophyll. Low-bulk soluble prebiotic fiber.</strong> Motility, gas, downstream flow — all three, at concentrations that matched the research she'd been reading."),
 ('p','Two gummies a day, thirty minutes before my biggest meal.'),
 ('h','What Happened When I Finally Treated The Right Organ'),
 ('p',"Day three: nothing. But this wasn't a laxative yanking my colon. It was getting my stomach moving on its own, and that takes a few days."),
 ('p','Day five: the cement eased. Maybe placebo, I told myself.'),
 ('p','Day ten: I went. On my own. No Miralax, no enema, no emergency. I sat there almost not believing it.'),
 ('h','The 90-Day Turnaround'),
 ('p',"By week three the sulfur burps were nearly gone. I had coffee with a friend and didn't think about my breath once — I can't tell you how long it had been since that was true."),
 ('p',"Around a month in, I deleted the tracker note off my phone — the one where I'd logged the last time I'd gone, until it read like a calendar of bad days."),
 ('p',"By day ninety my mornings ran on a schedule I didn't have to think about. Still on Wegovy®. Still down the weight. The backup, the bloating, the gas — gone."),
 ('p','I stayed for the whole birthday dinner the next time. Cake included.'),
 ('p',"When I told other women on the shot, most were skeptical. A gummy? I thought the same — right up until I understood why the ones they'd tried had failed them."),
 ('h','Motilli vs. Miralax &amp; Laxatives'),
 ('p','<strong>✓ Works on the stomach — where the backup actually starts</strong><br><strong>✓ Restores motility (apigenin), without overriding your medication</strong><br><strong>✓ Neutralizes the sulfur gas (chlorophyll) — doesn\'t mask it</strong><br><strong>✓ Softens the downstream backup without adding bulk</strong><br><strong>✓ Built for a GLP-1 gut — works with the shot, not against it</strong><br><br>Miralax &amp; laxatives do none of the above — every one of them is aimed at the colon.'),
 ('p',"It's sold directly — not on Amazon, not in stores — so the formula doesn't get swapped out or cut."),
 ('p','"I don\'t recommend much off the shelf," she told me. "I recommend this because it\'s the first one that put all three together, in the right forms, at the doses the research actually calls for."'),
 ('h','What The Backup Was Really Costing Me'),
 ('p','One night I added up what I\'d spent fixing the wrong organ — Miralax, magnesium, three fiber products, probiotics, a prescription, and co-pays for visits that ended in "drink more water." North of $400. For nothing.'),
 ('p','Motilli runs about $29.99 a bottle. Roughly a dollar a day.'),
 ('p','But the money was never the real cost.'),
 ('p','The real cost was the dinner I walked out of. The trips I talked myself out of. The conversations I cut short because of my breath. The weeks I spent wondering if I\'d have to lower my dose and hand back the weight just to feel human.'),
 ('p','That was the choice I thought I was stuck with. I never had to make it.'),
 ('h',"You Shouldn't Have To Choose"),
 ('p','You don\'t have to choose between the weight loss and your digestion. Right now Motilli has an offer for anyone ready to give it a real run, not just a few days:'),
 ('p','<strong>Buy 2, Get 1 Free</strong> — three bottles, three months, about how long it takes for regular mornings to become your normal.'),
 ('p',"Shipping's free. And it's backed by a <strong>90-Day Money-Back Guarantee</strong> — if your mornings don't change, send back what's left and you're not out a dollar."),
 ('p',"With 4.9 out of 5 from thousands of GLP-1 users, most people never reach for a laxative again. They're too busy getting their mornings back — without giving up a single pound the shot is giving them."),
 ('p',"One thing Dr. Marsh wanted me to pass on: the guarantee only comes with ordering directly from Motilli. Order through a reseller and you lose it — and you can't be sure how long it's been sitting on a shelf."),
 ('h','Two Mornings'),
 ('p',"You've got two versions of tomorrow morning in front of you."),
 ('p',"In one, you keep treating the colon — another box of Miralax, another fiber tub, another day planned around a bathroom — hoping the side effect sorts itself out. It won't. It's mechanics, not mystery, and nothing aimed at the colon reaches a problem that started in the stomach."),
 ('p','In the other, you treat the organ that actually slowed, keep every pound the shot is giving you, and stop bracing each morning for a backup that\'s finally gone.'),
 ('p','The choice seems obvious.'),
 ('p',"One thing worth knowing: Motilli's made in small batches and sold directly, so it sells out for stretches at a time. When a run is gone, it's gone until the next one."),
 ('p',"Don't wait for another wasted month."),
]

body_ids = []
for entry in body:
    if entry[0] == 'h':
        body_ids.append(H(entry[1]))
    elif entry[0] == 'p':
        body_ids.append(P(entry[1]))
    elif entry[0] == 'img_jar':
        body_ids.append(IMG(JAR, 'Motilli jar — clear glass jar with bright green label and green gummies', 1024, 1024))

# closing + reinforce paragraphs (after the CTA button)
closing_id = P('Your stomach will thank you. And your mornings might finally be yours again.')
reinforce_id = P('Click the link above to see if Motilli is still offering Buy 2, Get 1 Free and free shipping.')

# ---- rebuild article column children ----
ART = '0bdac53b-2066-442e-8277-53845d6f2035'
by[ART]['children'] = (
    ['7faab936-2204-474b-a74b-3e9bd0291f34',   # title
     '77d966e5-4012-4a9b-888f-ff4ee0dc61a7',   # title (variant)
     'b2e66e48-0c29-41d4-9530-5a4d7bfeb321',   # dateline
     '1a1c19a9-6430-4c54-b11c-08c9146e30e3',   # lede / quote
     'ee1e3d73-3736-47b2-8ad2-f1c8867952b7']   # hero
    + body_ids
    + ['124dc607-fe03-43d9-80e2-2950fe360c4c',  # CTA button
       closing_id, reinforce_id]
)

# ---- append clones ----
items.extend(new_items)
styles.extend(new_styles)

# ---- prune unreachable items/styles ----
reachable = set()
def mark(i):
    if i in reachable or i not in by: return
    reachable.add(i)
    for c in by[i].get('children', []): mark(c)
for r in [x['id'] for x in items if x['type'] == 'Body']:
    mark(r)
d['items'] = [i for i in items if i['id'] in reachable]
d['styles'] = [s for s in styles if s['id'] in reachable]

print('items kept:', len(d['items']), '| styles kept:', len(d['styles']), '| body blocks:', len(body_ids))

# ---- write json + zip ----
out_json = Path(OUT_JSON_NAME)
out_json.write_text(json.dumps(d, ensure_ascii=False))
with zipfile.ZipFile(OUT_PAGEFLY, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(out_json, OUT_JSON_NAME)
print('wrote', OUT_PAGEFLY.resolve())
