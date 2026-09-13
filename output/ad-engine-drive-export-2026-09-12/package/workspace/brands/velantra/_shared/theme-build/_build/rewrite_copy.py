#!/usr/bin/env python3
"""Rewrite icon_bar, benefits, and editorial tile copy on each product template.
Reads each template from Shopify, surgically patches the copy blocks, writes back.
Preserves feature_carousel image refs and everything else."""
import json, urllib.request, urllib.parse, urllib.error

SHOP = "uzdgxy-sb.myshopify.com"
THEME_ID = 139283431489
TOKEN = "[REDACTED_SECRET]"

# ──────────────────────────────────────────────────────────────────────────────
# NEW COPY — sharper, more tactile, more declarative
# ──────────────────────────────────────────────────────────────────────────────

COPY = {
    # ─── CORE BAGS ────────────────────────────────────────────────────────────
    "boat-tote-2": {
        "icon_bar": [
            ("DESIGN", "Soft-Sided, Hard-Worn",
             "Open top, deep cavity, leather where the canvas wears. Holds a beach day, a workday, a weekend."),
            ("CRAFT", "Canvas + Italian Leather",
             "18oz natural cotton from a New England mill. Handles vegetable-tanned in Tuscany. Patinas with every trip."),
            ("LONGEVITY", "Designed to Be Repaired",
             "Hand-bound seams. Replaceable handles. Traceable leather. We&rsquo;ll fix it free for two years."),
        ],
        "benefits": [
            ("INSIDE", "One zip pocket, one slip", "Sized for a phone on one side, a passport on the other."),
            ("AT THE BASE", "Saddle-leather binding", "Double-stitched corners. Holds shape under a full grocery run."),
            ("LAPTOP READY", "13-inch sleeve at the back", "Padded by the canvas body. Nothing bounces."),
            ("THE INSERT", "Drop-in Bag Organizer", "Six-pocket felt insert. Lifts out, moves between bags.", "bag-organizer"),
        ],
        "editorial": [
            ("THE LEATHER", "Tanned in Tuscany, finished by us", "left",
             "Our handles come from a tannery that has used the same well-water and oak bark since 1923. We finish each one by hand — burnishing the edge, beeswax-sealing the grain. By month six, it knows you."),
            ("THE PROMISE", "Two years covered. Lifetime in our shop.", "right",
             "Two-year warranty on materials and stitching. After that, we repair anything for the cost of materials. Send it back. Get it back better than you sent it."),
        ],
    },
    "meridian-tote": {
        "icon_bar": [
            ("DESIGN", "Built Around a 15-Inch Laptop",
             "Every line traces back to the silhouette inside. Suede sleeve. Rigid back panel. Magnetic top."),
            ("CRAFT", "Drum-Dyed Full-Grain",
             "Color that lives in the leather, not on top of it. Edges painted in eight coats, hand-sanded between each."),
            ("LONGEVITY", "Florentine Brass Hardware",
             "Solid brass feet, recessed pulls, antiqued by hand. Won&rsquo;t tarnish. Won&rsquo;t snag."),
        ],
        "benefits": [
            ("INSIDE", "Suede-lined throughout", "Tonal microsuede &mdash; kinder to a laptop, holds the structure crisp."),
            ("FOR THE DAY", "Three pockets, sized for a life", "One zip for the wallet, two open for the phone and passport. Magnetic top stays shut."),
            ("AT THE BASE", "Four solid brass feet", "Keep the bag off the ground, off the train floor, off the bar."),
            ("LAPTOP READY", "15-inch sleeve, padded", "Drops in flat against the rigid back panel. No friction."),
        ],
        "editorial": [
            ("THE BUILD", "Engineered around the screen", "left",
             "Most work totes are bags first, then made to fit a laptop. The Meridian was drawn the other way &mdash; start with the 15-inch silhouette, work outward, never crowd the device."),
            ("THE HARDWARE", "Brass that ages on the job", "right",
             "Sourced from a Florentine foundry that&rsquo;s poured for the European houses for forty years. Starts polished. Ends with the warm patina of a decade of meetings."),
        ],
    },
    "weekender": {
        "icon_bar": [
            ("DESIGN", "48 Hours, Carry-On Sized",
             "Two outfits, two pairs of shoes, a toiletry kit &mdash; and still fits under the seat in front of you."),
            ("CRAFT", "Waxed Canvas + Saddle Leather",
             "British-milled cotton, hot-waxed and hand-finished. Saddle leather at every wear point. Built for the road."),
            ("LONGEVITY", "Re-Waxable, Repairable",
             "Re-wax it. Re-stitch it. The bag that gets better in the weather."),
        ],
        "benefits": [
            ("THE TOP", "Full-length brass zip", "Two-way pull, smoke-glass coating. Opens flat for tray-style packing."),
            ("ON THE SHOULDER", "Detachable padded strap", "Clips on for the walk. Clips off in the overhead."),
            ("THE BACK", "Trolley sleeve", "Threads over any roller-suitcase handle. Hands free through the terminal."),
            ("INSIDE", "One zip pouch, one shoe bag", "A small interior zip for the toothbrush. A canvas shoe bag tucked in the base."),
        ],
        "editorial": [
            ("THE CANVAS", "Waxed in Lancashire", "left",
             "Our canvas comes from a mill that has been waxing cotton for over a century. Water-resistant from day one. Softens, burnishes, and stops shedding where it bends."),
            ("ON THE ROAD", "Sized by the airlines, not by us", "right",
             "We benchmarked every major carrier&rsquo;s carry-on dimensions, then designed to the strictest of them. Clears the gate at Frontier and Cathay both."),
        ],
    },
    "portico-bucket-bag": {
        "icon_bar": [
            ("DESIGN", "Soft, Sculptural, Cinched",
             "A pebbled leather body that slouches in your hand and holds its line when set down. A drawstring you can work one-handed."),
            ("CRAFT", "Drum-Tumbled, Not Pressed",
             "Most pebbled leather is embossed. Ours is tumbled for hours until the grain emerges from the hide itself. No two bags pebble the same."),
            ("LONGEVITY", "Lined in Microsuede",
             "A lining that won&rsquo;t shed, won&rsquo;t snag, won&rsquo;t bleed. Pulled out, brushed off, back to new."),
        ],
        "benefits": [
            ("AT THE TOP", "One-handed drawstring", "Suede pull, brass-tipped, threaded through hand-set eyelets. Cinches with a tug."),
            ("THE POUCH", "Detachable zip clutch", "Clips inside on a leather lanyard. Pull it out, use it as a clutch on its own."),
            ("ON THE SHOULDER", "Adjustable strap", "Crossbody one notch, shoulder the next. Brass-set rivets &mdash; never glue."),
        ],
        "editorial": [
            ("THE LEATHER", "Pebble grain, drawn out by hand", "left",
             "Hours of drum-tumbling, no machine emboss. The grain belongs to the hide, not to a press. Each bag arrives slightly different from its neighbor."),
        ],
    },
    "evening-bag": {
        "icon_bar": [
            ("DESIGN", "Petite, Two-Way Carry",
             "Small enough for the hand. Slip the chain inside for a top-handle silhouette. Drop it out for the crossbody."),
            ("CRAFT", "Italian Smooth Calf",
             "The same leather used by the Rue Cambon houses. Soft enough to take a finish, structured enough to hold one."),
            ("LONGEVITY", "Hand-Painted Edges",
             "Eight coats of edge paint, hand-sanded between each. The kind of detail you only notice when it&rsquo;s missing."),
        ],
        "benefits": [
            ("INSIDE", "Phone, card, key", "Three slots in microsuede &mdash; a phone on one side, a card case and key on the other."),
            ("THE STRAP", "Convertible chain", "Slim gold-tone chain that drops out or tucks inside. Top-handle for dinner. Crossbody for after."),
            ("THE CLOSURE", "Magnetic plus hidden snap", "Holds without a click. Opens without a fumble."),
        ],
        "editorial": [
            ("THE FINISH", "Edged by hand, eight coats deep", "left",
             "Every edge sanded, painted, dried, and sanded again. Eight coats. You won&rsquo;t see the work &mdash; you&rsquo;ll notice when another bag doesn&rsquo;t have it."),
        ],
    },
    "blackwood-carry": {
        "icon_bar": [
            ("DESIGN", "Architectural, All-Black",
             "Matte body, gunmetal hardware, sharp corners that wear soft. A silhouette for the late train and the long flight."),
            ("CRAFT", "Double-Dyed, UV-Sealed",
             "Most black leather oxidizes to brown. Ours is dyed twice and sealed with a UV-stable topcoat. Stays black for years."),
            ("LONGEVITY", "Brushed Gunmetal Hardware",
             "Hardware that won&rsquo;t tarnish, won&rsquo;t scratch the body. A finish that disappears in your hand."),
        ],
        "benefits": [
            ("INSIDE", "Padded 16-inch sleeve", "Lined in dark microsuede, against the rigid back panel. Fits a 16-inch MacBook Pro with the cable tucked."),
            ("ORGANIZED", "Five interior pockets", "One zip, two slip, one phone slot, one pen loop. Everything where you reach for it."),
            ("THE FEET", "Gunmetal, set in leather", "Four matte feet at the base. Keep the bag off the floor, off the bar, off the floor of the cab."),
        ],
        "editorial": [
            ("THE FINISH", "Black, kept black", "left",
             "Most black leather browns within a year. Ours is double-dyed in the drum, then sealed with a UV-stable topcoat. Five years in, it still photographs the same."),
        ],
    },
    # ─── ACCESSORIES (icon_bar only) ──────────────────────────────────────────
    "bag-scarf": {
        "icon_bar": [
            ("DESIGN", "Three Ways to Tie",
             "Handle wrap. Neck knot. Belt loop. A 90cm silk twilly with hand-rolled edges."),
            ("CRAFT", "Como-Milled Silk",
             "Woven and printed at the same Como mill that supplies the houses. Hand-rolled at the edge &mdash; never machine-hemmed."),
            ("LONGEVITY", "Limited Runs",
             "Each colorway runs once, then retires. Never re-stocked."),
        ],
    },
    "boat-tote-keychain": {
        "icon_bar": [
            ("DESIGN", "A Pocket-Sized Boat Tote",
             "Three inches of canvas and leather. Same fabric as the bag. Same edge finish."),
            ("CRAFT", "Made From Offcuts",
             "Built from canvas and leather scraps left behind from boat tote production. Nothing wasted."),
            ("LONGEVITY", "Solid Brass Clip",
             "Spring-loaded swivel clasp. The same hardware as the big bag."),
        ],
    },
    "bag-organizer": {
        "icon_bar": [
            ("DESIGN", "Six Pockets, Free-Standing",
             "A felt insert that holds a laptop, a water bottle, a phone, keys, and the small things that get lost."),
            ("CRAFT", "Pressed Wool Felt",
             "Holds its shape inside any bag. Moves between bags without sagging."),
            ("LONGEVITY", "70% Recycled Wool",
             "Compostable at the end of its life. Built to last long enough that it won&rsquo;t be."),
        ],
    },
    "cherry-charm": {
        "icon_bar": [
            ("DESIGN", "A Small Statement",
             "A glossy leather cherry on a brass swivel. The smallest way to make a bag your own."),
            ("CRAFT", "Patent-Finish Leather",
             "Hand-finished gloss. Won&rsquo;t crack, won&rsquo;t chip, even after a year clinking around in a tote."),
            ("LONGEVITY", "Hand-Shaped, Each One",
             "Every charm cut, shaped, and finished from a single piece of leather. No two are identical."),
        ],
    },
    "horse-charm": {
        "icon_bar": [
            ("DESIGN", "Saddle-Inspired",
             "Modeled on the hand-stitched bridles of the family workshops that taught us how to work leather."),
            ("CRAFT", "Saddle-Stitched by Hand",
             "Two-needle stitching &mdash; the same method as a horse bridle. Won&rsquo;t unzip if a single stitch fails."),
            ("LONGEVITY", "Solid Brass Hardware",
             "Hand-set spring clip. Won&rsquo;t loosen. Won&rsquo;t tarnish."),
        ],
    },
}

# ──────────────────────────────────────────────────────────────────────────────

def get_template(suffix):
    url = f"https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json?asset%5Bkey%5D=templates/product.{suffix}.json"
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(json.loads(r.read())["asset"]["value"])

def put_template(suffix, data):
    url = f"https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json"
    body = json.dumps({"asset": {"key": f"templates/product.{suffix}.json",
                                  "value": json.dumps(data, indent=2)}}).encode()
    req = urllib.request.Request(url, data=body, method="PUT",
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return f"FAIL {e.code}: {e.read()[:200].decode()}"

def patch(suffix, copy):
    print(f"\n== product.{suffix}.json")
    tpl = get_template(suffix)
    sections = tpl["sections"]

    # Patch icon_bar
    if "icon_bar" in sections and "icon_bar" in copy:
        ib = sections["icon_bar"]
        pillars = copy["icon_bar"]
        # Existing block ids in block_order
        order = ib["block_order"]
        for i, (eyebrow, headline, body) in enumerate(pillars[:len(order)]):
            bid = order[i]
            ib["blocks"][bid]["settings"]["eyebrow"] = eyebrow
            ib["blocks"][bid]["settings"]["headline"] = headline
            ib["blocks"][bid]["settings"]["body"] = f"<p>{body}</p>"
        print(f"  ✓ icon_bar — {len(pillars)} pillars")

    # Patch benefits (some products don't have this section)
    if "benefits" in sections and "benefits" in copy:
        bb = sections["benefits"]
        benefits = copy["benefits"]
        order = bb["block_order"]
        # Add more blocks if our copy has more than existing
        while len(order) < len(benefits):
            new_id = f"benefit_{len(order)}"
            bb["blocks"][new_id] = {"type": "benefit", "settings": {}}
            order.append(new_id)
        for i, entry in enumerate(benefits):
            bid = order[i]
            s = bb["blocks"][bid]["settings"]
            s["eyebrow_small"] = entry[0]
            s["headline"] = entry[1]
            s["body"] = f"<p>{entry[2]}</p>"
            if len(entry) > 3:  # has linked product
                s["linked_product"] = entry[3]
                s["link_label"] = "Shop"
            else:
                # strip any prior link
                s.pop("linked_product", None)
                s.pop("link_label", None)
        # Trim extra blocks
        for bid in list(order[len(benefits):]):
            bb["blocks"].pop(bid, None)
            order.remove(bid)
        print(f"  ✓ benefits — {len(benefits)} blocks")

    # Patch editorial
    if "editorial" in sections and "editorial" in copy:
        et = sections["editorial"]
        tiles = copy["editorial"]
        order = et["block_order"]
        # Add more if needed
        while len(order) < len(tiles):
            new_id = f"tile_{len(order)}"
            et["blocks"][new_id] = {"type": "tile", "settings": {}}
            order.append(new_id)
        for i, (eyebrow, headline, position, body) in enumerate(tiles):
            bid = order[i]
            s = et["blocks"][bid]["settings"]
            s["eyebrow"] = eyebrow
            s["headline"] = headline
            s["image_position"] = position
            s["body"] = f"<p>{body}</p>"
        for bid in list(order[len(tiles):]):
            et["blocks"].pop(bid, None)
            order.remove(bid)
        print(f"  ✓ editorial — {len(tiles)} tiles")

    status = put_template(suffix, tpl)
    print(f"  → PUT: {status}")

def main():
    for suffix, copy in COPY.items():
        patch(suffix, copy)
    print("\nAll done.")

if __name__ == "__main__":
    main()
