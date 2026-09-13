# TTS input text. "Velantra" is respelled Vell-Ahn-Trah (plain spelling = "Volantra" 6/6).
BODY = ("This is the Colette from Vell-Ahn-Trah. "
        "It's brushed wool with leather wrapped handles and a belted front, "
        "it's cut to stand upright on its own, and there's no logo anywhere. "
        "I filled it all the way up, set it down, and it stayed standing. "
        "My laptop, a water bottle and a sweater all go in. "
        "It comes in caramel and espresso. "
        "They're running a pre-order right now, thirty dollars off before it ships in October. "
        "I left the link below.")

HOOKS = {
    "A": "If you're looking for the perfect fall bag, I found it.",
    "B": "Fall's almost here and I found the bag for the whole season.",
    "C": "I thought a wool bag this soft would collapse. It doesn't.",
}

def full(hook_key):
    return HOOKS[hook_key] + " " + BODY
