#!/usr/bin/env python3
"""
Lints a Seedance prompt against _engine/sops/Seedance-Prompt-System.md.

Catches the mechanical failures the spec exists to prevent: runtime that doesn't
match in all three places, an undeclared or miscounted cut budget, overfull
dialogue that will compress and desync, missing guard modules, and overrides
with no answering continuity line.

Usage:
    python3 seedance_prompt_lint.py <prompt.txt> [--duration 25] [--profile P2]
    python3 seedance_prompt_lint.py <manifest.json>   # lints every segment prompt

Exit 0 = clean, 1 = errors. Warnings never fail the run.
"""

import json
import re
import sys
from pathlib import Path

BAND_A = ["FORMAT", "CAST", "WARDROBE", "SET", "PRODUCT", "LOOK", "VOICE", "SOUND"]
GUARDS = ["CONTINUITY", "TEXT", "NEGATIVES"]
MODULE_ORDER = BAND_A + GUARDS

CUT_VALUES = {"open", "jump cut", "hard cut", "match cut", "continuous"}
CUT_SYNTAX_HINT = "use 'SHOT 1.' / 'HARD CUT TO SHOT n.' / 'JUMP CUT TO SHOT n.' / 'MATCH CUT TO SHOT n.' / 'CONTINUOUS INTO SHOT n.'"
BANNED_TRANSITIONS = ["whip pan", "zoom transition", "crossfade", "dissolve", "speed ramp"]
ABSTRACT_VERBS = ["uses", "showcases", "interacts with", "experiences", "enjoys", "demonstrates"]

WPS_TARGET = 2.8
WPS_CEILING = 3.2
ENGINE_MAX_SECONDS = 30
ENGINE_MIN_SECONDS = 4
CREDIT_PREAUTH_PER_SEC = 63

# ByteDance says 1000 English words; Replicate passes along a BytePlus 600-word
# recommendation and enforces 4000 chars. Design to the tightest credible number.
PROMPT_WORD_TARGET = 600
PROMPT_WORD_CEILING = 1000
PROMPT_CHAR_CEILING = 4000

# Practitioners report shots degrading well before ByteDance's own 9-shot example.
SHOT_CEILING = 6

# Words that bias the model toward stock "AI video" aesthetics or destabilise motion.
# "fast" is repeatedly called the single most dangerous word in a Seedance prompt.
SLOP_WORDS = [
    "cinematic", "epic", "stunning", "dynamic", "8k", "4k", "masterpiece",
    "award-winning", "unreal engine", "hyperrealistic", "breathtaking", "majestic",
]
UNSTABLE_WORDS = ["fast", "rapidly", "quickly", "frantic"]

# Naming an absent OBJECT summons it, so these modules must describe positively.
# LOOK/VOICE/SOUND are excluded on purpose: they negate aesthetics and audio, which
# is both intended and the one place ByteDance says negation reliably works.
CONTENT_MODULES = ["CAST", "WARDROBE", "SET", "PRODUCT"]

# Prompt text, not a parameter, decides generation vs editing vs extension.
ROUTE_KEYWORDS = {
    "adds": "puts on / picks up",
    "add": "put on / pick up",
    "remove": "takes off / sets down",
    "removes": "takes off / sets down",
    "delete": "takes off / sets down",
    "replace": "swaps to",
    "replaces": "swaps to",
    "extend": "continues",
    "continue": "keeps going",
}

# profile -> (min_runtime, max_runtime, min_cuts, max_cuts, modules that may be absent)
PROFILES = {
    "P1": (15, 30, 4, 6, {"PRODUCT"}),
    "P2": (20, 30, 5, 7, set()),
    "P3": (15, 25, 5, 8, {"VOICE"}),
    "P4": (8, 20, 1, 3, {"VOICE", "PRODUCT"}),
    "P5": (15, 30, 5, 8, {"CAST", "WARDROBE", "VOICE"}),
    "P6": (20, 30, 6, 8, set()),
    "P7": (20, 30, 4, 9, set()),
    "P8": (20, 30, 4, 6, set()),
}

BEAT_RE = re.compile(
    r"\[(\d{1,2}):(\d{2})\s*[–\-—]\s*(\d{1,2}):(\d{2})\][ \t]*([^\n]*)", re.I
)


def classify_cut(header):
    """'SHOT 2. HARD CUT.' -> 'hard cut'; 'SHOT 1. OPEN.' -> 'open'."""
    h = re.sub(r"\bshot\s*\d+\s*\.?", "", header.strip(), flags=re.I)
    h = re.sub(r"\b(to|into)\b", "", h, flags=re.I)
    h = h.strip().strip(".").strip().lower()
    return h or "open"
DIALOGUE_RE = re.compile(r"^\s*DIALOGUE:\s*(.+)$", re.I | re.M)
FORMAT_SECONDS_RE = re.compile(r"(\d{1,2})[\s-]*second", re.I)
FORMAT_CUTS_RE = re.compile(r"exactly\s+(\d+)\s+(?:\w+\s+)?cuts?", re.I)
OVERRIDE_RE = re.compile(r"OVERRIDE\s*[—\-–]\s*([A-Z]+)", re.I)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def ok(self):
        return not self.errors


def _secs(m, s):
    return int(m) * 60 + int(s)


def parse_beats(text):
    """Returns [(start_s, end_s, cut_value, body_text)] in document order."""
    beats = []
    matches = list(BEAT_RE.finditer(text))
    for i, m in enumerate(matches):
        start = _secs(m.group(1), m.group(2))
        end = _secs(m.group(3), m.group(4))
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        beats.append((start, end, classify_cut(m.group(5)), text[m.end():body_end]))
    return beats


def check_modules(text, rep, profile):
    optional = PROFILES.get(profile, (0, 0, 0, 0, set()))[4] if profile else set()

    present = {}
    for mod in MODULE_ORDER:
        m = re.search(rf"^\s*{mod}\b", text, re.M)
        if m:
            present[mod] = m.start()
        elif mod in optional:
            pass
        else:
            rep.err(f"missing module: {mod}")

    # order check across whatever is present
    seen = [(pos, mod) for mod, pos in present.items()]
    seen.sort()
    actual = [mod for _, mod in seen]
    expected = [m for m in MODULE_ORDER if m in present]
    if actual != expected:
        rep.err(f"modules out of spec order.\n    expected: {' -> '.join(expected)}\n    found:    {' -> '.join(actual)}")

    # guards must come after the timeline
    beats = parse_beats(text)
    if beats:
        last_beat_pos = text.rfind("DIALOGUE:")
        for g in GUARDS:
            if g in present and present[g] < last_beat_pos:
                rep.err(f"{g} appears before the end of the timeline; guards close the prompt")
    return present


def check_runtime(text, beats, rep, api_duration, profile):
    fmt = re.search(r"^\s*FORMAT.*$", text, re.M)
    declared = None
    if fmt:
        m = FORMAT_SECONDS_RE.search(fmt.group(0))
        if m:
            declared = int(m.group(1))
    if declared is None:
        rep.err("FORMAT does not state a runtime in seconds")

    beat_total = beats[-1][1] if beats else 0

    if not beats:
        rep.err("no beats found; expected blocks like '[00:00-00:03] CUT: open'")
        return

    if beats[0][0] != 0:
        rep.err(f"timeline starts at {beats[0][0]}s, must start at 00:00")

    for i in range(1, len(beats)):
        if beats[i][0] != beats[i - 1][1]:
            rep.err(
                f"beat gap/overlap: beat {i} ends at {beats[i-1][1]}s but beat {i+1} starts at {beats[i][0]}s"
            )

    # the three-way match
    vals = {"FORMAT": declared, "beat sum": beat_total}
    if api_duration is not None:
        vals["duration param"] = api_duration
    distinct = {v for v in vals.values() if v is not None}
    if len(distinct) > 1:
        rep.err(
            "runtime mismatch (the model will compress and desync): "
            + ", ".join(f"{k}={v}s" for k, v in vals.items() if v is not None)
        )

    if beat_total > ENGINE_MAX_SECONDS:
        rep.err(f"runtime {beat_total}s exceeds the {ENGINE_MAX_SECONDS}s single-pass cap; split per the retry ladder")
    if beat_total < ENGINE_MIN_SECONDS:
        rep.err(f"runtime {beat_total}s is under the {ENGINE_MIN_SECONDS}s engine minimum")

    if profile in PROFILES:
        lo, hi, _, _, _ = PROFILES[profile]
        if not (lo <= beat_total <= hi):
            rep.warn(f"profile {profile} expects {lo}-{hi}s, this is {beat_total}s")


def check_cuts(text, beats, rep, profile):
    fmt = re.search(r"^\s*FORMAT.*$", text, re.M | re.S)
    block = text[: text.find("CAST")] if "CAST" in text else text
    m = FORMAT_CUTS_RE.search(block)
    if not m:
        rep.err("FORMAT does not declare a cut count ('contains exactly N cuts'); "
                "without it the model either ignores the timeline or cuts every 2s")
        declared = None
    else:
        declared = int(m.group(1))

    actual = [b[2] for b in beats]
    for i, cut in enumerate(actual):
        if cut not in CUT_VALUES:
            rep.err(f"beat {i+1}: unknown cut header '{cut}'; {CUT_SYNTAX_HINT}")
    if actual and actual[0] != "open":
        rep.err(f"beat 1 must be 'SHOT 1.', found '{actual[0]}'")
    if "open" in actual[1:]:
        rep.err("a bare 'SHOT n.' header appears after beat 1; every later beat must name its cut")

    real_cuts = sum(1 for c in actual[1:] if c in {"jump cut", "hard cut", "match cut"})
    if declared is not None and declared != real_cuts:
        rep.err(f"FORMAT declares {declared} cuts, the timeline contains {real_cuts}")

    runtime = beats[-1][1] if beats else 0
    if runtime and real_cuts:
        per_cut = runtime / real_cuts
        if per_cut > 5.0:
            rep.warn(f"one cut per {per_cut:.1f}s; under 1-per-5s reads like a webinar")
        if per_cut < 3.5:
            rep.warn(f"one cut per {per_cut:.1f}s; over 1-per-3.5s and the model loses the thread")

    if profile in PROFILES:
        _, _, lo, hi, _ = PROFILES[profile]
        if not (lo <= real_cuts <= hi):
            rep.warn(f"profile {profile} expects {lo}-{hi} cuts, this has {real_cuts}")

    # scan the timeline only, and never flag a transition that is being negated
    for i, (_, _, _, body) in enumerate(beats):
        low = body.lower()
        for banned in BANNED_TRANSITIONS:
            for m in re.finditer(re.escape(banned), low):
                if re.search(r"\bno\s+$", low[: m.start()]):
                    continue
                rep.err(f"beat {i+1}: banned transition '{banned}'; reads agency-produced")


def check_beats(beats, rep):
    for i, (start, end, cut, body) in enumerate(beats):
        n = i + 1
        dur = end - start
        if dur <= 0:
            rep.err(f"beat {n}: non-positive duration")
            continue

        for field in ("FRAME:", "ACTION:", "DIALOGUE:"):
            if field not in body.upper():
                rep.err(f"beat {n}: missing {field.rstrip(':')} field")

        d = DIALOGUE_RE.search(body)
        if d:
            line = d.group(1).strip()
            silent = line.lower().startswith("(none")
            if not silent:
                words = len(re.findall(r"[\w']+", line.strip('"')))
                wps = words / dur
                if wps > WPS_CEILING:
                    rep.err(
                        f"beat {n}: {words} words in {dur}s = {wps:.1f} w/s, over the {WPS_CEILING} ceiling. "
                        f"Cut to <={int(dur * WPS_TARGET)} words. Overfull beats compress and desync."
                    )
                elif wps > WPS_TARGET:
                    rep.warn(f"beat {n}: {wps:.1f} w/s, above the {WPS_TARGET} target; underfill is safer")
                if dur > 7:
                    rep.warn(f"beat {n}: {dur}s talking beat; over 7s the viewer wants a cut")
                if dur < 3:
                    rep.warn(f"beat {n}: {dur}s talking beat; under 3s the line clips")

        low = body.lower()
        for verb in ABSTRACT_VERBS:
            if re.search(rf"\b{verb}\b", low):
                rep.warn(f"beat {n}: abstract verb '{verb}' gets fudged; use a concrete physical verb")

        if re.search(r"\b(our|we're|we are|us)\b", low) and "DIALOGUE" in body.upper():
            d2 = DIALOGUE_RE.search(body)
            if d2 and re.search(r"\b(our|we're|we are)\b", d2.group(1).lower()):
                rep.err(f"beat {n}: creator speaks as the brand ('our'/'we're'); "
                        f"first person plural reads as paid. Use 'they're'.")


def check_overrides(text, rep):
    overrides = {m.group(1).upper() for m in OVERRIDE_RE.finditer(text)}
    if not overrides:
        return
    cont = re.search(r"^\s*CONTINUITY:(.*?)(?=^\s*TEXT:|^\s*NEGATIVES:|\Z)", text, re.M | re.S)
    cont_text = cont.group(1).lower() if cont else ""
    if not cont_text:
        rep.err("PHASE OVERRIDE present but no CONTINUITY block; overrides leak")
        return
    for mod in overrides:
        if "unless" not in cont_text and "except" not in cont_text:
            rep.warn(f"OVERRIDE on {mod}: CONTINUITY should carve it out explicitly "
                     f"('...in every beat except where a PHASE OVERRIDE states otherwise')")
            break
    if len(cont_text.split()) < 25:
        rep.warn("CONTINUITY is thin for a prompt with overrides; name what must NOT drag along")


def check_length(text, rep):
    """ByteDance's failure mode past the limit is silent dilution, not an error."""
    words = len(re.findall(r"[\w'@:]+", text))
    chars = len(text)
    if words > PROMPT_WORD_CEILING:
        rep.err(f"prompt is {words} words, over the {PROMPT_WORD_CEILING}-word ceiling; "
                f"the model starts silently dropping elements, it does not error")
    elif words > PROMPT_WORD_TARGET:
        rep.warn(f"prompt is {words} words, above the {PROMPT_WORD_TARGET}-word target")
    if chars > PROMPT_CHAR_CEILING:
        rep.err(f"prompt is {chars} chars, over the {PROMPT_CHAR_CEILING}-char cap some hosts enforce")


def check_route_hazard(text, rep):
    """2.5 picks generation vs editing vs extension from PROMPT TEXT, not a param.

    An innocent 'she adds a scarf' can reroute the whole job into edit mode,
    which force-locks duration to -1 and throws the timeline away.
    """
    for m in re.finditer(r"^\s*ACTION:\s*(.+)$", text, re.I | re.M):
        line = m.group(1).lower()
        for kw, safer in ROUTE_KEYWORDS.items():
            if re.search(rf"\b{kw}\b", line):
                rep.warn(f"ACTION uses '{kw}', which can reroute the task into "
                         f"edit/extend mode; prefer '{safer}'")


def check_slop(text, rep):
    low = text.lower()
    for w in SLOP_WORDS:
        for m in re.finditer(rf"\b{re.escape(w)}\b", low):
            if re.search(r"\bno\s+\w*\s*$", low[: m.start()]):
                continue  # "no cinematic look" is negating slop, which is correct
            rep.warn(f"slop word '{w}' biases toward stock AI-video aesthetics; cut it")
            break
    for w in UNSTABLE_WORDS:
        for m in re.finditer(rf"\b{w}\b", low):
            rep.warn(f"'{w}' destabilises motion; make exactly one element fast "
                     f"and explicitly stabilise the rest")
            break


def check_inline_negation(text, rep):
    """Naming an absent object summons it. 'no hard hat' produces hard hats."""
    # Bound every block by the NEXT module of any kind, or the check bleeds into
    # LOOK/SOUND and flags their legitimate negations.
    marks = []
    for mod in MODULE_ORDER:
        m = re.search(rf"^\s*{mod}\b", text, re.M)
        if m:
            marks.append((m.start(), mod))
    tl = text.find("TIMELINE")
    if tl > 0:
        marks.append((tl, "TIMELINE"))
    marks.sort()
    for i, (start, mod) in enumerate(marks):
        if mod not in CONTENT_MODULES:
            continue
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        block = text[start:end]
        for m in re.finditer(r"\bno\s+([a-z][a-z\- ]{2,25}?)(?=[,.;\n])", block, re.I):
            obj = m.group(1).strip()
            if obj.lower() in {"drift", "morphing", "color shift", "colour shift"}:
                continue
            rep.warn(f"{mod} negates content ('no {obj}'), which tends to summon it. "
                     f"Describe the space positively instead, or move it to NEGATIVES.")


def check_text_guard(text, rep):
    m = re.search(r"^\s*TEXT:(.*)$", text, re.M)
    if m and not re.search(r"\bno on-screen text\b|\bno text\b", m.group(1), re.I):
        rep.warn("TEXT is enabled; Seedance garbles brand names, burn hooks and captions in post instead")


def lint(text, api_duration=None, profile=None, label=""):
    rep = Report()
    check_modules(text, rep, profile)
    beats = parse_beats(text)
    check_runtime(text, beats, rep, api_duration, profile)
    check_cuts(text, beats, rep, profile)
    check_beats(beats, rep)
    check_overrides(text, rep)
    check_text_guard(text, rep)
    check_length(text, rep)
    check_route_hazard(text, rep)
    check_slop(text, rep)
    check_inline_negation(text, rep)
    if len(beats) > SHOT_CEILING:
        rep.warn(f"{len(beats)} shots; practitioners report dropped shots past ~{SHOT_CEILING}. "
                 f"Check the output for a silently skipped beat.")

    runtime = beats[-1][1] if beats else (api_duration or 0)
    head = f"{label} " if label else ""
    print(f"\n{head}{runtime}s, {max(0, len(beats)-1)} cuts, profile {profile or 'unset'}")
    for e in rep.errors:
        print(f"  ERROR   {e}")
    for w in rep.warnings:
        print(f"  warn    {w}")
    if rep.ok() and not rep.warnings:
        print("  clean")
    if runtime:
        print(f"  credits: needs ~{int(CREDIT_PREAUTH_PER_SEC * runtime)} clear for pre-auth")
    return rep.ok()


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2

    path = Path(args[0])
    duration = None
    profile = None
    for i, a in enumerate(args):
        if a == "--duration" and i + 1 < len(args):
            duration = int(args[i + 1])
        if a == "--profile" and i + 1 < len(args):
            profile = args[i + 1].upper()

    if not path.exists():
        print(f"not found: {path}")
        return 2

    if path.suffix == ".json":
        data = json.loads(path.read_text(), strict=False)
        segs = data.get("segments", [])
        if not segs:
            print("manifest has no segments[]")
            return 2
        allok = True
        for s in segs:
            ok = lint(
                s.get("prompt", ""),
                s.get("duration", duration),
                s.get("profile", profile),
                label=f"segment {s.get('index', '?')}:",
            )
            allok = allok and ok
        return 0 if allok else 1

    return 0 if lint(path.read_text(), duration, profile, label=path.name + ":") else 1


if __name__ == "__main__":
    sys.exit(main())
