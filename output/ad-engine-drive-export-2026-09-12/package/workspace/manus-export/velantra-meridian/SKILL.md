---
name: velantra-meridian
description: Product scale for the Velantra Meridian, a structured leather handbag. Documents the product's visual identity, hardware, and colorway reference coverage so image/video generation stays accurate to the real product. Use whenever generating creative — static ad replication, video scene replication, or b-roll sourcing — for the Velantra Meridian specifically.
---

# Velantra Meridian — Product Scale

Use this whenever generating creative (static ad replication, video scene replication, or b-roll sourcing) for the Velantra Meridian specifically. It documents the product's visual identity and available colorways so that image/video generation stays accurate to the real product, and it explains how the product's reference images are organized so downstream generation work can pull the right seed images.

## Product identity

- **Product:** Velantra Meridian
- **Category:** Structured leather handbag
- **Brand:** Velantra

### Visual description

- **Silhouette:** Birkin-inspired structured handbag, wider than tall, clean geometric lines.
- **Body:** Full premium pebbled leather construction (single color throughout).
- **Hardware:** Silver/palladium turn-lock clasp, silver buckle accents, silver feet.
- **Handles:** Two rigid top handles in matching leather.
- **Closure:** Front flap with centered turn-lock mechanism.
- **Strap:** Front belt strap connecting handles through the flap.
- **Construction:** Single-material leather. The entire bag is one color — no canvas, no two-tone. This is a LEATHER bag, which is the key visual distinction from the brand's canvas-based products (like the Boat Tote or Weekender).

### Available colorways

| Colorway | Reference coverage | Notes |
|----------|--------|-------|
| Black | 9 reference images | Classic black leather, silver hardware |
| Brown | 7 reference images | Warm tan/camel leather |
| Coffee Brown | 7 reference images | Darker espresso-toned brown |
| Gray | 6 reference images | Cool medium gray leather |
| White | 5 reference images | Clean white/cream leather |
| Green | 1 reference image | Deep emerald green |
| Burgundy | 1 reference image | Rich wine/burgundy |
| Light Blue | 2 reference images | Soft powder blue |
| Ultra Light Blue | 1 reference image | Very pale icy blue |

40 total reference images across these 9 colorways, with multiple angles per color for the better-covered colorways (black, brown, coffee brown, gray, white).

## How to use this

1. When generating any Meridian creative, use the visual description above as the ground truth for the product's construction (single-material pebbled leather, silver hardware, turn-lock flap closure, rigid top handles).
2. Pick reference images matching the colorway called for in the brief. If a specific colorway is forced, pull 2–3 reference angles for that colorway specifically as the image-to-image seed set.
3. If no colorway is specified, a representative curated subset covering all colorways can be used so the generation model has broad visual grounding.
4. This is a leather bag — never let a generation model introduce canvas panels, two-tone coloring, or mixed materials. The entire bag is one leather color throughout.

## Rules & standards

- The product is a single-material leather bag — reject any generated frame that introduces canvas, two-tone paneling, or a second material.
- Hardware is always silver/palladium — reject any generated frame showing gold or brass hardware.
- The closure is a front flap with a centered turn-lock and a front belt strap connecting the handles through the flap — reject any frame inventing a different closure mechanism (zip, magnetic snap, etc.).
