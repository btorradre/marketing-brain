#!/usr/bin/env python3
"""
v4 product-truth blocks for the Sofia Woven Tote.

REFERENCE LAW (Brooks, 8/05): `_REF-product.jpg` is THE product reference and is wired into
EVERY generation as the bag authority. Its belt geometry (horizontal band + one diagonal) is
canonical for all colourways.

Derived by studying _REF-product.jpg at full resolution:
- deep leather band across the top; the handles pass through narrow SLOTS cut into it
- band's lower edge: step down at far left into a squared tab, up, a wide flat-bottomed centre
  panel between the two handle slots, up, step down at far right into a squared tab; square
  corners, all one sheet
- belts: ONE strap runs nearly horizontal across the bag below the flap; a SECOND strap crosses
  it diagonally from upper right to lower left ending in a rounded tip; a short pointed tab
  hangs from the flap centre behind them
- body: soft slouchy hand woven straw, side walls flaring into soft woven WINGS at the top
  corners, rounded base, no hard corners
- weave: chunky twisted cord rows; wide braided lacing with visible X pattern up each side edge
- stitching: pale tonal stitching on the leather edges (subtle, thread close to leather colour)
"""

SOFT = (
    "BODY SHAPE, CRITICAL: the woven body is SOFT and unstructured, never a rigid box. Hand woven "
    "straw that slouches and gives under its own weight: the side walls flare gently outward and "
    "upward, ending in soft woven wings at the top outer corners exactly as in the product "
    "reference. The base is a soft rounded rectangle, no hard corners, no creased edges, no moulded "
    "panels. The bag reads as pliable basketry, not structured moulded leather goods. Keep the "
    "gentle irregularity and slight asymmetry of a handmade woven bag."
)

WEAVE = (
    "WEAVE: coarse and chunky, thick twisted straw cord in clearly visible horizontal rows, "
    "slightly irregular and handmade, never a fine uniform machine grid. A wide braided lacing "
    "with a visible criss-cross X pattern runs vertically up each side edge of the bag, exactly "
    "as in the product reference."
)

FLAP = (
    "FLAP, CRITICAL, copy it EXACTLY from the product reference: one deep leather band lies flat "
    "across the entire top of the bag. The two rolled handles pass through two narrow slots cut "
    "into this band. The band's lower edge is cut, all in the same single sheet, into: a squared "
    "tab stepping down at the far left, a wide flat-bottomed centre panel between the two handle "
    "slots, and a squared tab stepping down at the far right, with square crisp corners "
    "throughout. These are silhouettes cut into ONE sheet, never separate applied patches and "
    "never rounded pillows. The flap lies completely flat against the woven front. No extra "
    "leather pieces, strips, loops or fragments exist anywhere on the bag beyond the flap, the "
    "two handles, the two belt straps and the small centre tab."
)

BELTS = (
    "BELT STRAPS, CRITICAL, copy the arrangement EXACTLY from the product reference: one narrow "
    "leather strap runs nearly horizontally across the front of the bag just below the flap, its "
    "left end angling slightly downward. A second narrow strap crosses over it diagonally, running "
    "from the upper right down toward the lower left, ending in a rounded tip. A short pointed "
    "leather tab hangs down from the centre of the flap behind the straps. This is NOT a symmetric "
    "X and NOT a V. Keep the straps narrow, flat and lying against the weave."
)

TONAL = (
    "STITCHING: stitch lines on the leather are subtle and tonal, the thread close to the leather "
    "colour, so they read quietly. No bright white contrast stitching."
)

NOMETAL = "No metal hardware anywhere, no buckles, no logos, no lettering."

REAL = (
    "A real photograph on a medium format camera with a 100mm lens, never a 3D render or CGI: real "
    "straw fibre with individual strands and slight irregularity, real leather grain with soft "
    "natural sheen and micro creasing, natural depth of field falloff, subtle photographic grain. "
    "No plastic smoothness, no glossy render highlights, no synthetic perfection."
)

STAGE = (
    "Setting: one continuous soft warm pale oat-greige seamless studio sweep, hex #E7E3DB, filling "
    "the whole frame. No horizon line, no visible wall-to-floor edge, no corner. Soft even diffused "
    "studio light from the front left. Exactly ONE soft contact shadow directly beneath the bag. No "
    "person, no hand, no props, no pedestal, no table, no surface line. Square 1:1 frame, bag "
    "centred, occupying about 72 percent of the frame height."
)

SHAPE = " ".join([SOFT, WEAVE, FLAP, BELTS, TONAL, NOMETAL])
