#!/usr/bin/env python3
"""Guard the review copy in compose.py before compositing.

Ports the four laws from the Weekender verified-buyer run
(`products/weekender/concepts/7:24:26 - verified buyer mof .../check_quotes.py`)
plus this product's own claim bans. Run it after ANY copy edit.

    python3 check_copy.py        (exit 1 on any failure)

1. A headline set in quotation marks is a PULL QUOTE and must be a verbatim
   whole sentence of the body. A clause with its comma swapped for a period is
   a doctored quote and a plain substring test waves it through. V5's headline
   is deliberately left unquoted, as a bare brand claim, exactly as R5 sets it.
2. Curly quotation marks only, never straight ASCII. Both review references wrap
   the body in them.
3. No doubled spaces, no em or en dashes, every line non-empty.
4. No banned claim: origin, BNPL, capacity, or "structured" / "stands on its own"
   (PRODUCT-TRUTH.md §11 clears none of them).

Not enforced here because it cannot bite on this set: one face per named
reviewer. V5 is a still life and V6 is a torso crop, so neither shows a face.
"""
import importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cmp", os.path.join(ROOT, "compose.py"))
cmp_ = importlib.util.module_from_spec(spec)
sys.argv = ["check_copy"]
spec.loader.exec_module(cmp_)

BANNED = re.compile(
    r"Ital(y|ian)|handwoven|hand-woven|Afterpay|Klarna|Affirm|"
    r"structured|stands on its own|holds its shape|"
    r"laptop|fits a \w+|litre|liter|coastal",
    re.I)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


fails = []
for slug, raw in cmp_.COPY.items():
    for mode in ("brand", "review"):
        if isinstance(raw, dict) and mode in raw:
            block = raw[mode]
        elif mode == "brand" and not (isinstance(raw, dict) and "review" in raw):
            block = raw
        else:
            continue

        if isinstance(block, dict):
            head = block.get("headline", "")
            body_lines = block.get("body", [])
            who = block.get("who", "")
            # Collect EVERY string in the block, so the tagline / sub / kicker
            # slots on V1-V4 are scanned too and not just the review triplet.
            lines = []
            for v in block.values():
                lines.extend(v if isinstance(v, list) else [v])
        else:
            head, who = "", block[-1]
            body_lines = list(block[:-1])
            lines = list(block)

        for t in lines:
            if not isinstance(t, str):
                continue
            if not t.strip():
                fails.append(f"{slug}/{mode}: empty line")
            if "'" in t:
                fails.append(f"{slug}/{mode}: straight apostrophe in {t!r}")
            if '"' in t:
                fails.append(f"{slug}/{mode}: straight double quote in {t!r}")
            if "  " in t:
                fails.append(f"{slug}/{mode}: doubled space in {t!r}")
            if "—" in t or "–" in t:
                fails.append(f"{slug}/{mode}: em or en dash in {t!r}")
            hit = BANNED.search(t)
            if hit:
                fails.append(f"{slug}/{mode}: banned claim {hit.group(0)!r} in {t!r}")

        # law 1: a QUOTED headline must be a whole sentence of the body
        if head.startswith("“") or head.startswith('"'):
            want = head.strip("“”\"").rstrip(".!?").lower()
            got = [s.rstrip(".!?").lower() for s in sentences(" ".join(body_lines))]
            if want not in got:
                fails.append(f"{slug}/{mode}: quoted headline is not a whole sentence "
                             f"of the body: {head!r}")

        # law 2: a review body carries curly quotation marks around it
        if mode == "review" and body_lines:
            if not (body_lines[0].lstrip().startswith("“")
                    and body_lines[-1].rstrip().endswith("”")):
                fails.append(f"{slug}/{mode}: review body is not wrapped in curly "
                             f"quotation marks")
            if "Verified Buyer" not in who:
                fails.append(f"{slug}/{mode}: review attribution missing Verified Buyer")

if fails:
    print("COPY GUARD FAILED:")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print(f"COPY GUARD: clean  (MODE={cmp_.MODE}, BIRKIN={cmp_.BIRKIN})")
