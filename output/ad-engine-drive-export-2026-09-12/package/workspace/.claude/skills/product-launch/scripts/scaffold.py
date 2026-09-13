#!/usr/bin/env python3
"""Create the product's home in the vault and its product-scale skill stub.

Two artifacts outlive the launch and are the reason later ad work stays on-model:

  brands/<brand>/products/<slug>/     the folder every downstream skill reads
  ~/.claude/skills/<brand>-<slug>/    the product-scale skill: the locked identity
                                      block that every generation prompt pastes

The identity block is written with TODO markers, not guesses. A product-scale skill
that invents hardware, lining or dimensions is worse than no skill at all, because
every ad afterwards inherits the invention. Fill it from the source pack and from
Brooks, then delete the markers.

Usage:
  python3 scaffold.py --spec spec.json
  python3 scaffold.py --spec spec.json --no-skill
"""
import argparse, json, re
from pathlib import Path

VAULT = Path("/Users/brooksorradre2/Documents/marketing brain")
SKILLS = Path.home() / ".claude" / "skills"

SUBDIRS = ["source", "product-references", "product-images", "pdp",
           "statics", "video", "broll", "concepts", "ugc"]

TRUTH = """# {title} — Product Truth

> Single source of truth for this product. Every ad, static, PDP claim and generation
> prompt reads from here. **Nothing in this file may be a guess.** If a fact is not
> confirmed by the source listing, a real photo, or Brooks, it stays marked TODO.

- **Handle:** `{handle}`  ·  **Slug:** `{slug}`  ·  **Template suffix:** `{suffix}`
- **Price:** ${price}
- **Source reference:** {source_url}
- **Launched:** TODO
- **Status:** draft

## Colorways
{colorways}

## Dimensions
TODO — measure or confirm with Brooks. Never carry a competitor's numbers over as ours.

## Materials
TODO — body / trim / hardware / lining, each named.

## Opening mechanism
TODO — describe how it actually opens, in the words a prompt can use. This is the single
most-failed detail in generation (see the Weekender flap and Straw Tote flap laws).

## Carry truth
TODO — hand, forearm, shoulder, crossbody. Handle drop decides this, not preference.
If the handles cannot reach a shoulder, say so: engines invent a strap to bridge an
impossible pose.

## Scale anchor
TODO — dimensions alone do not hold scale in a prompt. Write the relational line
("as wide as her shoulders", "reaches from her hip toward her knee").

## Claims cleared for customer-facing copy
TODO — only what the live PDP and the supplier confirm.

## Banned
- No origin claims (designed in the U.S., handcrafted by skilled artisans overseas).
- No invented certifications, tanneries, studies, percentages or review counts.
- No competitor photography, ever, including as an i2i seed for a published asset.
"""

SKILL_STUB = """---
name: {brand}-{slug}
description: Product scale and locked product truth for the {title_bare}. Use for ANY content generation involving this product, video ads, statics, UGC, PDP imagery, b-roll, concepts. Contains the verbatim identity block that must be pasted into every generation prompt. Trigger whenever the {short} is generated, rendered, prompted or replicated.
disable-model-invocation: false
---

# {title} — Product Scale & Locked Product Truth

Configuration layer for ALL {short} content generation. Every downstream pipeline pulls
its product truth from HERE. The blocks below are verbatim: paste them, do not paraphrase.

Full truth file: `brands/{brand}/products/{slug}/PRODUCT-TRUTH.md`

## Product Identity

- **Product:** {title}
- **Handle:** `{handle}`  ·  **Price:** ${price}
- **Colorways:** {colorway_list}
- **Dimensions:** TODO
- **Hardware:** TODO
- **Carry truth:** TODO
- **Positioning:** TODO

## References

| Path | Use as |
|---|---|
| `brands/{brand}/products/{slug}/product-references/` | canonical i2i seeds |
| `brands/{brand}/products/{slug}/product-images/colors/` | per-colorway angle set (live gallery) |
| `brands/{brand}/products/{slug}/source/` | competitor reference, READ ONLY, never published |

## VERBATIM IDENTITY BLOCK (paste into every prompt)

> TODO — one long sentence naming silhouette, proportion, body material, trim material,
> handles, hardware colour and placement, closure, interior lining, and "no logos anywhere
> on the bag". Write it only after looking at real photos.

## VERBATIM PHOTOREAL BLOCK (paste into every prompt)

> The attached reference supplies GEOMETRY AND MATERIALS ONLY. Do not inherit its lighting,
> its background, its clean edges or its polished product-photo look. Shot on a phone in
> available light: visible sensor noise, imperfect focus, slight handheld tilt, real
> shadows, creased and lightly scuffed leather, visible fibres in the weave, dust and
> fingerprints. NOT a 3D render, NOT CGI, NOT a product visualisation, no Blender, Octane,
> Unreal or Keyshot look, no ray tracing, no catalogue retouching.

## Frame QA (mandatory)

Every generated frame is checked against real photos, not against this text, for:
silhouette, closure mechanism, hardware count and placement, interior lining, logo-free
surfaces, and the 3D-render tell. A frame that nails the product but reads as CGI is a
reject. Generate three variants per scene and pick.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--no-skill", action="store_true")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text())
    brand = spec.get("brand", "velantra")
    suffix = spec.get("template_suffix") or spec["handle"].replace(f"{brand}-", "")
    slug = spec.get("slug", suffix)
    root = VAULT / "brands" / brand / "products" / slug

    for d in SUBDIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    for c in spec["colorways"]:
        (root / "product-images" / "colors" / c["name"]).mkdir(parents=True, exist_ok=True)
    print(f"   folders -> {root}")

    truth = root / "PRODUCT-TRUTH.md"
    if truth.exists():
        print(f"   PRODUCT-TRUTH.md already exists, left alone")
    else:
        truth.write_text(TRUTH.format(
            title=spec["title"], handle=spec["handle"], slug=slug, suffix=suffix,
            price=spec.get("price", "TODO"),
            source_url=spec.get("source_url", "TODO"),
            colorways="\n".join(f"- {c['name']}" + (f" ({c['hex']})" if c.get("hex") else "")
                                for c in spec["colorways"])))
        print(f"   wrote {truth.name}")

    if args.no_skill:
        return
    short = spec.get("short_name", spec["title"])
    title_bare = re.sub(r"^the\s+", "", spec["title"], flags=re.I)
    sk = SKILLS / f"{brand}-{slug}"
    if (sk / "SKILL.md").exists():
        print(f"   skill {sk.name} already exists, left alone")
        return
    sk.mkdir(parents=True, exist_ok=True)
    (sk / "SKILL.md").write_text(SKILL_STUB.format(
        brand=brand, slug=slug, title=spec["title"], short=short,
        title_bare=title_bare,
        handle=spec["handle"], price=spec.get("price", "TODO"),
        colorway_list=", ".join(c["name"] for c in spec["colorways"])))
    print(f"   product-scale skill -> {sk}/SKILL.md  (fill the TODOs before any ad work)")


if __name__ == "__main__":
    main()
