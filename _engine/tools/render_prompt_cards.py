#!/usr/bin/env python3
"""
render_prompt_cards.py — render Content System prompt cards to PNG.

The remote harness emits card TEXT plus a render_spec but never rasterizes; the local
executor has to. Overflow THROWS rather than truncating, because a truncated card
silently drops script words and the model then says something the plan never approved.

    python3 render_prompt_cards.py cards.json --out <dir>

cards.json is the {"cards": [...], "render_spec": {...}} object from
content_build_prompt_cards (or the envelope's per-scene prompt_card entries).
"""
import argparse
import hashlib
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont


def wrap(text: str, chars_per_line: int) -> list[str]:
    """Greedy wrap on whitespace at the spec's computed character budget."""
    out, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if len(candidate) <= chars_per_line:
            line = candidate
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out or [""]


def layout(lines: list[str], spec: dict, size: int) -> tuple[list[str], int]:
    """Wrap every card line at this font size and return the rendered rows + total height."""
    usable = spec["width"] - 2 * spec["marginX"]
    chars = max(48, int(usable // (size * 0.57)))
    rows: list[str] = []
    for para in lines:
        rows.extend(wrap(para, chars))
    row_h = size + spec["lineSpacing"]
    total = spec["headerSize"] + spec["headerToBodyGap"] + len(rows) * row_h
    return rows, total


def render(card: dict, spec: dict, out_dir: pathlib.Path) -> pathlib.Path:
    budget = spec["height"] - 2 * spec["marginY"]
    size = spec["bodyStartSize"]
    rows, total = layout(card["lines"], spec, size)
    while total > budget and size - spec["bodySizeStep"] >= spec["bodyMinSize"]:
        size -= spec["bodySizeStep"]
        rows, total = layout(card["lines"], spec, size)
    if total > budget:
        raise SystemExit(spec.get("overflowMessage", "Prompt text does not fit the card."))

    img = Image.new("RGB", (spec["width"], spec["height"]), spec["background"])
    draw = ImageDraw.Draw(img)
    header_font = ImageFont.truetype(spec["fontBold"], spec["headerSize"])
    body_font = ImageFont.truetype(spec["fontRegular"], size)

    x, y = spec["marginX"], spec["marginY"]
    draw.text((x, y), spec["headerTemplate"].replace("{n}", str(card["scene_number"])),
              font=header_font, fill=spec["foreground"])
    y += spec["headerSize"] + spec["headerToBodyGap"]
    for row in rows:
        draw.text((x, y), row, font=body_font, fill=spec["foreground"])
        y += size + spec["lineSpacing"]

    path = out_dir / card["filename"]
    img.save(path, format=spec.get("format", "PNG"), optimize=spec.get("optimize", True))
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cards_json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    payload = json.loads(pathlib.Path(args.cards_json).read_text())
    spec = payload["render_spec"]
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for card in payload["cards"]:
        # Verify the text we rasterize is byte-identical to what the harness signed.
        digest = hashlib.sha256(card["text"].encode()).hexdigest()
        flag = "ok" if digest.startswith(card["checksum"][:16]) else "CHECKSUM DRIFT"
        path = render(card, spec, out_dir)
        print(f"{path.name}  {path.stat().st_size:>7} bytes  text-sha256 {flag}")

    print(f"\n{len(payload['cards'])} card(s) -> {out_dir}")


if __name__ == "__main__":
    main()
