#!/usr/bin/env python3
"""Guard the review copy in overlay.py before compositing.

A pull quote sits in quotation marks, so it has to be a real sentence of the review
it sits on — not a clause with the comma swapped for a period. This catches the
doctored-quote case that a plain substring test waves through, plus straight ASCII
quote marks and doubled spaces.

Usage:  python3 check_quotes.py      (exit 1 on any failure)
"""
import importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("ov", os.path.join(ROOT, "overlay.py"))
ov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ov)

FAILS = []


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


for name, q in ov.QUOTES.items():
    body = " ".join(q["body"])
    head = q["headline"]

    # 1. headline must equal one whole sentence of the body, case-insensitively
    want = head.rstrip(".!?").lower()
    got = [s.rstrip(".!?").lower() for s in sentences(body)]
    if want not in got:
        near = next((s for s in got if want in s), None)
        FAILS.append(f"{name}: headline is not a complete sentence of the body.\n"
                     f"    headline: {head}\n"
                     f"    {'clause inside: ' + near if near else 'no match at all in body'}")

    # 2. no straight ASCII quote marks anywhere
    for label, text in (("headline", head), ("body", body), ("who", q["who"])):
        for ch, nm in (("'", "straight apostrophe"), ('"', "straight double quote")):
            if ch in text:
                FAILS.append(f"{name}: {nm} in {label}")

    # 3. no doubled spaces, and every body line non-empty
    if "  " in body:
        FAILS.append(f"{name}: doubled space in body")
    if any(not ln.strip() for ln in q["body"]):
        FAILS.append(f"{name}: empty body line")

for name in ov.QUOTES:
    print(f"{'FAIL' if any(f.startswith(name + ':') for f in FAILS) else 'ok  '} {name}")

if FAILS:
    print("\n" + "\n".join(FAILS))
    sys.exit(1)
print(f"\nall {len(ov.QUOTES)} quotes clean")
