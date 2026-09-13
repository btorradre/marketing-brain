#!/usr/bin/env python3
"""Generate per-product PDP JSON templates for the Cuyana-style Velantra rebuild.

Output: templates/product.{handle}.json — one file per in-scope product.
These reference the custom pdp-* sections + snippets we already uploaded.
"""
import json, os
from pathlib import Path

BUILD = Path(__file__).parent
PRODUCTS = json.loads((BUILD / "_products.json").read_text())["products"]

# ──────────────────────────────────────────────────────────────────────────────
# Product-specific content
# ──────────────────────────────────────────────────────────────────────────────

CORE = {
    "velantra-boat-tote-2": {
        "category": "everyday-tote",
        "short_name": "Boat Tote",
        "blurb": "An open-top everyday carry in canvas and full-grain leather. Designed to soften with use — built to last decades.",
        "monogram": False,
        "customize": True,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Relaxed & Versatile", "body": "An open silhouette that holds everything from a laptop to a beach towel without losing its shape."},
            {"eyebrow": "QUALITY", "headline": "Made to Soften", "body": "Heavyweight cotton canvas paired with full-grain leather handles that patina beautifully."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Built to Outlast", "body": "Tanned at LWG-certified tanneries. Designed for repair, not replacement."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Two internal pockets", "body": "One zippered, one open — for keys, sunglasses, and the things that get lost."},
            {"eyebrow": "BUILT IN", "headline": "Reinforced base", "body": "Double-stitched and saddle-leather bound. Holds shape when fully loaded."},
            {"eyebrow": "READY FOR", "headline": "13-inch laptop", "body": "Slips in flat against the back panel, padded by the canvas body."},
            {"eyebrow": "PAIRS WITH", "headline": "Bag Organizer", "body": "Drop-in insert that turns the open top into a structured commute bag.", "linked": "bag-organizer"},
        ],
        "editorial_tiles": [
            {"eyebrow": "ITALIAN LEATHER", "headline": "Tanned the slow way", "body": "Our leather handles come from a 4th-generation Tuscan tannery that still vegetable-tans every hide by hand. The result: a finish that softens, deepens, and tells the story of where you've taken it.", "position": "left"},
            {"eyebrow": "MADE TO OUTLAST", "headline": "Two-year warranty. Lifetime repair.", "body": "If anything fails in normal use, we'll repair it. If we can't repair it, we'll replace it. Tell us where to send it.", "position": "right"},
        ],
        "feature_captions": [
            "Full-grain leather handles, raw-cut edges hand-burnished",
            "Heavyweight cotton canvas, 18oz — built to hold its shape",
            "Top-load opening — wide enough for a laptop bag or a beach towel",
            "Made by hand at our New York atelier",
        ],
    },
    "velantra-meridian-tote": {
        "category": "structured-tote",
        "short_name": "Meridian",
        "blurb": "A structured leather tote built for the boardroom and the airport. Suede-lined, zip-top, and quietly architectural.",
        "monogram": False,
        "customize": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Architectural & Quiet", "body": "Clean lines, sharp edges, and the proportions of a classic — engineered to look intentional from any angle."},
            {"eyebrow": "QUALITY", "headline": "Full-Grain Leather", "body": "Drum-dyed for color that lives in the leather, not on top of it."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Tanned Responsibly", "body": "LWG Gold-rated tannery. Edge-painted with water-based finishes."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Suede lining", "body": "Soft microsuede protects the contents and keeps the structure crisp."},
            {"eyebrow": "ORGANIZED", "headline": "Three internal pockets", "body": "One zippered, two open — sized for a phone, a passport, a notebook."},
            {"eyebrow": "READY FOR", "headline": "15-inch laptop", "body": "Padded back panel takes a full-size MacBook Pro without bulk."},
            {"eyebrow": "DETAIL", "headline": "Hand-set hardware", "body": "Antique brass feet, magnetic closure, and a recessed zipper pull."},
        ],
        "editorial_tiles": [
            {"eyebrow": "THE ARCHITECTURE", "headline": "Built around the laptop", "body": "Most work totes are bags first, then we make them fit a laptop. The Meridian was designed the other way around — every line traces back to the 15-inch silhouette inside.", "position": "left"},
            {"eyebrow": "THE HARDWARE", "headline": "Brass that ages with you", "body": "Solid brass feet and closures from a Florentine foundry. They start polished and end up with the kind of warm patina only a decade of use can produce.", "position": "right"},
        ],
        "feature_captions": [
            "Full-grain Italian leather, drum-dyed",
            "Suede-lined interior in tonal microsuede",
            "Solid brass feet — keep the bag standing, off the ground",
            "Recessed zip pull and magnetic top closure",
        ],
    },
    "velantra-weekender": {
        "category": "weekender",
        "short_name": "Weekender",
        "blurb": "A 48-hour bag in waxed canvas and saddle leather. Carry-on sized. Built to age in transit.",
        "monogram": False,
        "customize": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Carry-On Sized", "body": "Sized to slide into any overhead bin while still holding two days of clothes."},
            {"eyebrow": "QUALITY", "headline": "Saddle Leather Trim", "body": "Thick, vegetable-tanned leather at every wear point — handles, base corners, strap mounts."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Repairable Construction", "body": "Hand-stitched. Rebuilt at the seam, not thrown away."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Full-length zip top", "body": "Opens flat to a wide compartment — pack it like a duffel, lift it out like a tray."},
            {"eyebrow": "BUILT IN", "headline": "Detachable strap", "body": "Padded shoulder strap clips off when you don't need it."},
            {"eyebrow": "READY FOR", "headline": "Two-day trip", "body": "Sized to fit two pairs of shoes, four outfits, and a toiletry kit."},
            {"eyebrow": "DETAIL", "headline": "Trolley sleeve", "body": "Slides over a roller suitcase handle for hands-free transit."},
        ],
        "editorial_tiles": [
            {"eyebrow": "WAXED CANVAS", "headline": "Gets better with the weather", "body": "British-milled waxed cotton — water-resistant from day one, with a finish that softens and burnishes wherever the bag flexes and rubs.", "position": "left"},
            {"eyebrow": "ON THE ROAD", "headline": "Sized for the bin", "body": "We benchmarked every major airline's carry-on dimensions, then built the Weekender to fit the strictest of them.", "position": "right"},
        ],
        "feature_captions": [
            "British waxed canvas — water-resistant, made to patina",
            "Saddle leather handles and base corners",
            "Detachable padded shoulder strap",
            "Trolley sleeve for hands-free airport transit",
        ],
    },
    "velantra-portico-bucket-bag": {
        "category": "structured",
        "short_name": "Portico",
        "blurb": "A drawstring bucket bag in soft pebbled leather. Roomy enough for everyday, refined enough for evening.",
        "monogram": False,
        "customize": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Soft & Sculptural", "body": "A drawstring silhouette that slouches naturally and holds its proportion when set down."},
            {"eyebrow": "QUALITY", "headline": "Pebbled Full-Grain", "body": "Drum-tumbled for the soft, lived-in pebble that defines our signature leather."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Tanned Responsibly", "body": "LWG-certified tanneries. Edge finishing free of chrome and solvents."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Suede drawstring closure", "body": "Microfiber drawstring tightens with one hand and stays closed in transit."},
            {"eyebrow": "ORGANIZED", "headline": "Detachable pouch", "body": "Internal zip pouch clips out — use it as a clutch on its own."},
            {"eyebrow": "READY FOR", "headline": "Day or evening", "body": "Adjustable shoulder strap takes it from crossbody to shoulder to clutch."},
        ],
        "editorial_tiles": [
            {"eyebrow": "THE LEATHER", "headline": "Pebbled, not pressed", "body": "Most pebbled leather is embossed by machine. Ours is drum-tumbled for hours until the grain emerges from the leather itself — softer, deeper, never uniform.", "position": "left"},
        ],
        "feature_captions": [
            "Pebbled full-grain leather, drum-tumbled",
            "Suede drawstring with brass-tipped pull",
            "Detachable internal zip pouch",
            "Adjustable strap — crossbody to shoulder",
        ],
    },
    "velantra-evening-bag": {
        "category": "micro",
        "short_name": "Evening Bag",
        "blurb": "A petite top-handle bag in calf leather. Sized for the essentials. Built for the long evening.",
        "monogram": False,
        "customize": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Petite & Practical", "body": "Small enough to carry by hand, generous enough for a phone, a card case, and a lipstick."},
            {"eyebrow": "QUALITY", "headline": "Calf Leather", "body": "Italian smooth calf — the same leather used by the houses on Rue Cambon."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Made to Last", "body": "Hand-stitched. Re-finishable. Designed for decades, not seasons."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Card and phone slot", "body": "Two interior compartments — one for a phone, one for a card case and key."},
            {"eyebrow": "READY FOR", "headline": "Convertible strap", "body": "Slip the chain inside to carry by top-handle, or wear it crossbody."},
            {"eyebrow": "DETAIL", "headline": "Hand-finished edges", "body": "Every edge painted, dried, and sanded eight times before final finish."},
        ],
        "editorial_tiles": [
            {"eyebrow": "THE FINISH", "headline": "Edged by hand", "body": "Eight coats of edge paint, hand-sanded between each. The kind of detail you only notice when it's missing — and we obsess over it.", "position": "left"},
        ],
        "feature_captions": [
            "Italian smooth calf leather",
            "Convertible top-handle and chain strap",
            "Hand-painted edges, eight coats",
            "Magnetic top closure with hidden snap",
        ],
    },
    "velantra-blackwood-carry": {
        "category": "structured",
        "short_name": "Blackwood",
        "blurb": "A structured leather carry in matte black. Hardware in gunmetal. Designed for the late commute and the long flight.",
        "monogram": False,
        "customize": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Quiet & Architectural", "body": "Black-on-black with gunmetal hardware. A silhouette that disappears into the city and stands out everywhere else."},
            {"eyebrow": "QUALITY", "headline": "Matte Full-Grain", "body": "A matte-finish leather that resists fingerprints and softens at the corners with use."},
            {"eyebrow": "SUSTAINABILITY", "headline": "LWG-Certified Tannery", "body": "Made at one of fewer than 50 LWG Gold tanneries in the world."},
        ],
        "benefits": [
            {"eyebrow": "INSIDE", "headline": "Padded laptop sleeve", "body": "16-inch laptop fits flat against the back panel, padded in soft microsuede."},
            {"eyebrow": "ORGANIZED", "headline": "Five internal compartments", "body": "Phone slot, pen loops, two open pockets, one zippered."},
            {"eyebrow": "DETAIL", "headline": "Gunmetal hardware", "body": "All-metal hardware in matte gunmetal — won't tarnish, won't scratch the body."},
        ],
        "editorial_tiles": [
            {"eyebrow": "THE FINISH", "headline": "Black, deeper", "body": "Most black leather oxidizes brown over time. Ours is double-dyed and finished with a UV-stable topcoat — engineered to stay black for years.", "position": "left"},
        ],
        "feature_captions": [
            "Matte black full-grain leather",
            "Gunmetal hardware, scratch-resistant",
            "Padded sleeve fits a 16-inch laptop",
            "Five organizational pockets inside",
        ],
    },
}

ACCESSORIES = {
    "bag-scarf": {
        "category": "accessory",
        "short_name": "Bag Scarf",
        "blurb": "A silk twilly scarf for tying to handles. Hand-rolled edges. Made in a Como mill.",
        "monogram": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Two Ways to Wear", "body": "Tie to a bag handle, knot around the neck, or thread through a belt loop."},
            {"eyebrow": "QUALITY", "headline": "Italian Silk Twill", "body": "Woven in Como, hand-rolled at the edges."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Made in Small Runs", "body": "Limited seasonal prints. Never restocked."},
        ],
    },
    "boat-tote-keychain": {
        "category": "accessory",
        "short_name": "Keychain",
        "blurb": "A miniature boat-tote keychain in matching leather. Clips to your zipper pull, your belt loop, or your real bag.",
        "monogram": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Mini Boat Tote", "body": "A 3-inch leather replica of our signature boat tote — same canvas, same trim."},
            {"eyebrow": "QUALITY", "headline": "Solid Brass Clip", "body": "Spring-loaded swivel clasp. Built to last, like the bag it's modeled on."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Made from Offcuts", "body": "Constructed from canvas and leather scraps left over from boat tote production."},
        ],
    },
    "bag-organizer": {
        "category": "accessory",
        "short_name": "Bag Organizer",
        "blurb": "A felt insert that turns any open-top tote into a structured commute bag. Drop in, pull out, move between bags.",
        "monogram": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Six Compartments", "body": "Pockets for a laptop, a water bottle, a phone, keys, and the small things that get lost."},
            {"eyebrow": "QUALITY", "headline": "Pressed Wool Felt", "body": "Holds its shape inside or out — moves between bags without sagging."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Recycled Wool Blend", "body": "70% recycled wool. Compostable at end of life."},
        ],
    },
    "velantra-cherry-charm": {
        "category": "accessory",
        "short_name": "Cherry Charm",
        "blurb": "A leather cherry charm in glossy red. Clips to any zipper pull, handle, or strap.",
        "monogram": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "A Small Statement", "body": "A glossy leather cherry on a brass swivel — the smallest way to make a bag your own."},
            {"eyebrow": "QUALITY", "headline": "Patent Leather Finish", "body": "Glossy finish that won't crack, even after a year of clinking around in a tote."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Made by Hand", "body": "Each charm hand-shaped from a single piece of leather."},
        ],
    },
    "velantra-horse-charm": {
        "category": "accessory",
        "short_name": "Horse Charm",
        "blurb": "A leather horse-head charm. Brass-mounted. A small tribute to equestrian craft.",
        "monogram": False,
        "icon_bar": [
            {"eyebrow": "DESIGN", "headline": "Saddle-Inspired", "body": "Modeled on the hand-stitched bridles of the family workshops that taught us how to work leather."},
            {"eyebrow": "QUALITY", "headline": "Solid Brass Hardware", "body": "Hand-set spring clip — won't loosen, won't tarnish."},
            {"eyebrow": "SUSTAINABILITY", "headline": "Saddle Stitched", "body": "Two-needle hand stitching, the same method used on a horse bridle."},
        ],
    },
}

ALL = {**CORE, **ACCESSORIES}
PRODUCT_BY_HANDLE = {p["handle"]: p for p in PRODUCTS}

# ──────────────────────────────────────────────────────────────────────────────
# Shared content
# ──────────────────────────────────────────────────────────────────────────────

DIMENSIONS_CARE_TEMPLATE = """<p><strong>Dimensions</strong><br>
Please see product details below.</p>
<p><strong>Material</strong><br>
Full-grain leather, canvas, and hand-set hardware.</p>
<p><strong>Care</strong><br>
Wipe clean with a soft, dry cloth. Condition leather every 6&ndash;12 months with a neutral leather cream. Avoid prolonged exposure to direct sunlight, water, and heat.</p>"""

SHIPPING_RETURNS = """<p><strong>Shipping</strong><br>
Free standard shipping on orders over $100. Orders ship within 1&ndash;2 business days from our New York atelier.</p>
<p><strong>Returns</strong><br>
30-day returns on unused items in original condition. Personalized items are final sale.</p>
<p><strong>Repairs</strong><br>
Every Velantra bag is covered by our Two-Year Warranty. We&rsquo;ll repair or replace anything that fails in normal use.</p>"""

# ──────────────────────────────────────────────────────────────────────────────
# Template builder
# ──────────────────────────────────────────────────────────────────────────────

def build_main_blocks(handle, spec, p):
    """Return (blocks_dict, block_order_list) for the main-product section."""
    blocks = {}
    order = []

    # 1. Short blurb (text block w/ rich content)
    if spec.get("blurb"):
        blocks["blurb"] = {
            "type": "text",
            "settings": {"text": f"<p>{spec['blurb']}</p>"}
        }
        order.append("blurb")

    # 2. Variant picker (native, color swatches if Color option present)
    has_color = any(o["name"].lower() == "color" for o in p.get("options", []))
    blocks["variants"] = {
        "type": "variant_picker",
        "settings": {
            "picker_type": "button",
            "product_dynamic_variants_enable": True,
            "color_swatches": has_color,
            "variant_labels": True
        }
    }
    order.append("variants")

    # 3. Price (above ATC, per Cuyana reference)
    blocks["price"] = {"type": "price", "settings": {}}
    order.append("price")

    # 4. Buy buttons (Shop Pay installments auto-rendered below when dynamic checkout enabled)
    blocks["buy"] = {
        "type": "buy_buttons",
        "settings": {
            "show_dynamic_checkout": True,
            "surface_pickup_enable": True
        }
    }
    order.append("buy")

    # 5. Send a hint (subtle row with top divider)
    blocks["hint"] = {
        "type": "custom",
        "settings": {"code": "{% render 'pdp-send-hint' %}"}
    }
    order.append("hint")

    # 6. Add Accessories (expandable accordion, open by default — pulls from accessories collection)
    blocks["inline_acc"] = {
        "type": "custom",
        "settings": {"code": "{% render 'pdp-inline-accessories' %}"}
    }
    order.append("inline_acc")

    # 10. Dimensions & Care accordion (native tab block)
    # 7. Check In-Store Availability (accordion, custom)
    blocks["in_store"] = {
        "type": "custom",
        "settings": {"code": "{% render 'pdp-in-store' %}"}
    }
    order.append("in_store")

    # 8. Dimensions & Care accordion (native tab block)
    blocks["tab_dim"] = {
        "type": "tab",
        "settings": {
            "title": "Dimensions & Care",
            "content": DIMENSIONS_CARE_TEMPLATE
        }
    }
    order.append("tab_dim")

    # 9. Shipping & Returns accordion (native tab block)
    blocks["tab_ship"] = {
        "type": "tab",
        "settings": {
            "title": "Shipping & Returns",
            "content": SHIPPING_RETURNS
        }
    }
    order.append("tab_ship")

    # 10. Two Year Warranty accordion (native tab block)
    blocks["tab_warranty"] = {
        "type": "tab",
        "settings": {
            "title": "Two Year Warranty",
            "content": "<p>Every Velantra bag is covered for two years against defects in materials and construction. If anything goes wrong in normal use, we&rsquo;ll repair or replace it.</p><p>After two years, we continue to offer repair service for the cost of materials. Designed to last decades, not seasons.</p>"
        }
    }
    order.append("tab_warranty")

    return blocks, order


def build_template(handle, spec):
    p = PRODUCT_BY_HANDLE.get(handle)
    if not p:
        print(f"  SKIP {handle} — not in product list")
        return None
    images = p.get("images", [])
    img_srcs = [i.get("src", "") for i in images]

    # Build main section
    main_blocks, main_order = build_main_blocks(handle, spec, p)

    sections = {}
    order = []

    # 1. Breadcrumb
    sections["breadcrumb"] = {"type": "pdp-breadcrumb", "settings": {}}
    order.append("breadcrumb")

    # 2. Main (gallery + buy column)
    sections["main"] = {
        "type": "main-product",
        "settings": {
            "image_position": "left",
            "image_size": "large",
            "product_zoom_enable": True,
            "thumbnail_position": "below",
            "thumbnail_height": "fixed",
            "mobile_layout": "full",
            "enable_video_looping": True,
            "product_video_style": "muted"
        },
        "blocks": main_blocks,
        "block_order": main_order
    }
    order.append("main")

    # 3. Customize companion grid (only for products that need it)
    if spec.get("customize"):
        # Build with 3 default companion products
        companions = ["bag-organizer", "boat-tote-keychain", "bag-scarf"]
        cblocks = {}
        corder = []
        for i, h in enumerate(companions):
            cp = PRODUCT_BY_HANDLE.get(h)
            if cp:
                bid = f"item_{i}"
                cblocks[bid] = {
                    "type": "companion",
                    "settings": {
                        "product": h,
                        "tagline": "Slip inside" if i == 0 else ""
                    }
                }
                corder.append(bid)
        if cblocks:
            sections["customize"] = {
                "type": "pdp-customize-grid",
                "settings": {
                    "eyebrow": "MAKE IT YOURS",
                    "heading": f"Customize Your {spec['short_name']}",
                    "intro": "<p>Add an organizer, charm, or scarf to complete your bag — all designed to match.</p>",
                    "bg_color": "#faf8f4"
                },
                "blocks": cblocks,
                "block_order": corder
            }
            order.append("customize")

    # 4. Warranty
    sections["warranty"] = {
        "type": "pdp-warranty",
        "settings": {
            "eyebrow": "OUR PROMISE",
            "heading": "Two-Year Warranty",
            "body": "<p>Every Velantra bag is built to last. If anything fails in normal use, we&rsquo;ll repair or replace it.</p>",
            "link_url": "/pages/warranty",
            "link_label": "Read the warranty",
            "bg_color": "#1a1a1a",
            "text_color": "#ffffff"
        }
    }
    order.append("warranty")

    # 5. Icon bar (Design / Quality / Sustainability)
    ib_blocks = {}
    ib_order = []
    for i, pillar in enumerate(spec.get("icon_bar", [])):
        bid = f"pillar_{i}"
        ib_blocks[bid] = {
            "type": "pillar",
            "settings": {
                "eyebrow": pillar["eyebrow"],
                "headline": pillar["headline"],
                "body": f"<p>{pillar['body']}</p>"
            }
        }
        ib_order.append(bid)
    if ib_blocks:
        sections["icon_bar"] = {
            "type": "pdp-icon-bar",
            "settings": {"bg_color": "#faf8f4", "text_color": "#1a1a1a"},
            "blocks": ib_blocks,
            "block_order": ib_order
        }
        order.append("icon_bar")

    # 6. Benefit blocks (for products that have them)
    bb_blocks = {}
    bb_order = []
    for i, b in enumerate(spec.get("benefits", [])):
        bid = f"benefit_{i}"
        s = {
            "eyebrow_small": b.get("eyebrow", ""),
            "headline": b["headline"],
            "body": f"<p>{b['body']}</p>",
        }
        if b.get("linked"):
            s["linked_product"] = b["linked"]
            s["link_label"] = "Shop"
        bb_blocks[bid] = {"type": "benefit", "settings": s}
        bb_order.append(bid)
    if bb_blocks:
        sections["benefits"] = {
            "type": "pdp-benefit-blocks",
            "settings": {
                "eyebrow": "BUILT-IN BENEFITS",
                "heading": "Made with intention",
                "layout": "stack",
                "bg_color": "#ffffff"
            },
            "blocks": bb_blocks,
            "block_order": bb_order
        }
        order.append("benefits")

    # 7. Feature carousel — pull images 1-4 from product
    fc_blocks = {}
    fc_order = []
    captions = spec.get("feature_captions", [])
    for i in range(min(4, len(img_srcs))):
        bid = f"slide_{i}"
        cap = captions[i] if i < len(captions) else ""
        # NOTE: image set via shopify_image when we have file references;
        # for now leave image blank — populates from product gallery via fallback,
        # OR is filled when Higgsfield-generated assets are uploaded.
        fc_blocks[bid] = {
            "type": "slide",
            "settings": {"caption": cap}
        }
        fc_order.append(bid)
    # Ensure at least 4 slides
    while len(fc_order) < 4:
        bid = f"slide_{len(fc_order)}"
        fc_blocks[bid] = {"type": "slide", "settings": {"caption": captions[len(fc_order)] if len(fc_order) < len(captions) else ""}}
        fc_order.append(bid)
    sections["feature_carousel"] = {
        "type": "pdp-feature-carousel",
        "settings": {
            "eyebrow": "IN DETAIL",
            "heading": f"Every detail, considered",
            "bg_color": "#ffffff"
        },
        "blocks": fc_blocks,
        "block_order": fc_order
    }
    order.append("feature_carousel")

    # 8. Editorial tiles
    et_blocks = {}
    et_order = []
    for i, t in enumerate(spec.get("editorial_tiles", [])):
        bid = f"tile_{i}"
        et_blocks[bid] = {
            "type": "tile",
            "settings": {
                "image_position": t.get("position", "left"),
                "eyebrow": t["eyebrow"],
                "headline": t["headline"],
                "body": f"<p>{t['body']}</p>"
            }
        }
        et_order.append(bid)
    if et_blocks:
        sections["editorial"] = {
            "type": "pdp-editorial-tile",
            "settings": {"bg_color": "#ffffff"},
            "blocks": et_blocks,
            "block_order": et_order
        }
        order.append("editorial")

    # 9. Style With (manual product picker — populate with 4 other in-scope products)
    style_picks = [h for h in CORE.keys() if h != handle][:4]
    if handle in ACCESSORIES:
        # For accessories, pair with bags
        style_picks = list(CORE.keys())[:4]
    sw_blocks = {}
    sw_order = []
    for i, h in enumerate(style_picks):
        if PRODUCT_BY_HANDLE.get(h):
            bid = f"card_{i}"
            sw_blocks[bid] = {"type": "card", "settings": {"product": h}}
            sw_order.append(bid)
    if sw_blocks:
        sections["style_with"] = {
            "type": "pdp-style-with",
            "settings": {
                "heading": "Pair With" if handle in ACCESSORIES else "Style With",
                "bg_color": "#faf8f4"
            },
            "blocks": sw_blocks,
            "block_order": sw_order
        }
        order.append("style_with")

    # 10. Recently viewed (native Impulse section)
    sections["recently_viewed"] = {
        "type": "recently-viewed",
        "settings": {}
    }
    order.append("recently_viewed")

    return {"sections": sections, "order": order}


def main():
    out_dir = BUILD / "templates"
    out_dir.mkdir(exist_ok=True)
    built = 0
    for handle, spec in ALL.items():
        tpl = build_template(handle, spec)
        if tpl is None: continue
        # File name: product.{handle stripped of velantra prefix maybe}
        # Shopify caps template "suffix" length — use a short suffix
        suffix = handle.replace("velantra-", "").replace("-", "-")
        fname = f"product.{suffix}.json"
        (out_dir / fname).write_text(json.dumps(tpl, indent=2))
        print(f"  ✓ {fname}")
        built += 1
    print(f"\nBuilt {built} templates → {out_dir}")

if __name__ == "__main__":
    main()
