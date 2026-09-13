"""Pronunciation lexicon.

Loads a JSON map of tricky words / brand terms -> phonetic respelling or an
SSML phoneme spec, and applies it to a line BEFORE synthesis so the fix is
deterministic and identical across every segment and every creator variation.

Lexicon JSON formats (any mix):
  {
    "Boatkin":  "Boat-kin",                         # simple respelling
    "seagrass": "SEE-grass",
    "Velantra": {"alphabet": "ipa", "ph": "vəˈlæntrə"},   # SSML phoneme tag
    "Motilli":  {"alphabet": "cmu-arpabet", "ph": "M OW T IY L IY"}
  }

Respellings are plain text substitutions. Phoneme specs are wrapped in
<phoneme> SSML tags (honored by ElevenLabs SSML-capable models).
Matching is whole-word and case-insensitive; the original casing of the match
is irrelevant because we replace with the lexicon's canonical form.
"""
import json
import re


def load_lexicon(path):
    if not path:
        return {}
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit("[ugc-forge] Lexicon must be a JSON object {word: replacement}.")
    return data


def _replacement(value, original_word):
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and value.get("ph"):
        alphabet = value.get("alphabet", "ipa")
        return f'<phoneme alphabet="{alphabet}" ph="{value["ph"]}">{original_word}</phoneme>'
    raise SystemExit(f"[ugc-forge] Bad lexicon entry for {original_word!r}.")


def apply_lexicon(text: str, lexicon: dict) -> str:
    if not lexicon:
        return text
    # Replace longest keys first so multi-word brand terms win over substrings.
    for word in sorted(lexicon, key=len, reverse=True):
        pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
        text = pattern.sub(lambda m, w=word: _replacement(lexicon[w], m.group(0)), text)
    return text


def uses_ssml(lexicon: dict) -> bool:
    return any(isinstance(v, dict) and v.get("ph") for v in lexicon.values())
