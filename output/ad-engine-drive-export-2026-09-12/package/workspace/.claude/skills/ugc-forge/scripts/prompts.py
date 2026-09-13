"""Prompt assembly: the fixed STYLE ANCHOR appended to every segment prompt.

Redundancy is the safeguard against drift — even though frame-chaining already
carries identity/wardrobe/lighting forward, we re-state the anchor on every call.
"""

DEFAULT_STYLE = {
    "creator": "the same young woman from the reference image, same face and hair",
    "wardrobe": "same outfit as the reference",
    "setting": "same room/background as the reference",
    "lighting": "same soft natural daylight as the reference",
    "feel": "shot on an iPhone front camera, vertical, candid UGC, slight handheld motion, natural skin texture",
}


def load_style(settings: dict) -> dict:
    style = dict(DEFAULT_STYLE)
    for k in style:
        if settings.get(f"style_{k}"):
            style[k] = settings[f"style_{k}"]
    if settings.get("style"):  # full override block from a settings JSON
        style.update(settings["style"])
    return style


def style_anchor_block(style: dict) -> str:
    return (
        f"STYLE ANCHOR (keep identical every shot): {style['creator']}; "
        f"wardrobe: {style['wardrobe']}; setting: {style['setting']}; "
        f"lighting: {style['lighting']}; {style['feel']}. "
        "Do not change the person, wardrobe, lighting, or setting. No on-screen text."
    )


def build_prompt(visual_direction: str, style: dict, *, talking_head: bool) -> str:
    speak = (
        "The creator is speaking to camera (mouth moving naturally — speech audio "
        "is added separately, do not rely on rendered words). "
        if talking_head else
        "B-roll: no speaker on screen, the product/scene in motion. "
    )
    return f"{visual_direction.strip()}. {speak}{style_anchor_block(style)}"
