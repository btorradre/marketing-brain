#!/usr/bin/env python3
"""
Generate N long-form (90-180s) VSL scripts via Anthropic Opus, in the
HurAgain "single-shot continuous talking head" pattern.

Output: JSON array. Each ad is {id, hook_overlay_text, hook_overlay_style,
vsl_script, estimated_duration_seconds, narrative_arc_check}.
"""
import argparse, json, os, sys, pathlib, glob, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import _env
_env.load_env()

VAULT = _env.VAULT
WORDS_PER_SECOND = 4.2  # conversational rant cadence

def load_brand_context(brand_key, registry):
    bd = registry["brand_defaults"].get(brand_key, {})
    chunks = []
    vault_path = bd.get("vault_path")
    if vault_path:
        base = VAULT / vault_path
        if base.exists():
            md_files = sorted(glob.glob(str(base / "**/*.md"), recursive=True))[:30]
            for f in md_files:
                try:
                    txt = pathlib.Path(f).read_text(errors="ignore")
                    if 200 < len(txt) < 30000:
                        chunks.append(f"### {pathlib.Path(f).relative_to(VAULT)}\n{txt[:8000]}")
                except Exception:
                    pass
    ctx = "\n\n".join(chunks)[:30000]
    return {
        "context_md": ctx,
        "product_context": bd.get("product_context") or "",
        "narrative_voice": bd.get("narrative_voice") or "",
    }

SYSTEM = """You are a direct-response VSL scriptwriter producing long-form continuous-shot UGC scripts in the HurAgain / Joint Pain Experts pattern.

You produce JSON only. No markdown, no preamble.

FORMAT YOU ARE WRITING FOR:
- Single creator, single setting, single continuous shot (one phone-selfie take, no cuts).
- 90-180s total (target user-specified). Conversational rant cadence (~4.2 words/sec).
- Hook overlay text burned in for first ~8s.
- No B-roll, no SFX cues, no scene markers, no music notes — just continuous spoken script.

NARRATIVE ARC (enforce in this order with target word counts for ~120s ad):
  Beat 1 (Hook, 3-5s, 15-25 words): A single curiosity-promise line. Examples that work: "I'm gonna tell you the one thing that helped my [pain]..." / "What if I told you [one plant / one supplement] fixed my [pain] in [N] weeks." End the hook by setting up a lived-in story (not a list).
  Beat 2 (Agitation, 15-30s, 70-130 words): Concrete sensory pain. Specific moments: 3am wake-ups, "have to think about every chair before you sit," can't sleep on the side, etc. Rotate the avatar's actual lived details from the brand vault — never invent generic pain.
  Beat 3 (Authority subversion, 12-20s, 50-80 words): "Doctors said wear and tear / wear it out / just getting older / handed me anti-inflammatories like that was an answer." Position the gatekeeper as having missed the obvious.
  Beat 4 (Mechanism, 20-35s, 90-150 words): Plain-English science of WHY this works. ALWAYS include: (a) the named mechanism (e.g. estrogen → tendon lubrication; or the brand's specific mechanism from the vault), (b) why nothing else worked (e.g. "didn't touch the actual problem"), (c) a memorable metaphor (HurAgain used "WD-40 on my hips" / "rusted hinge to well-oiled machine" — write a different metaphor each time, don't reuse).
  Beat 5 (Solution, 12-20s, 50-90 words): Name the product. Quote what makes THIS one different (potency, source, formulation, dosage from the vault). Soft, not salesy.
  Beat 6 (Personal proof, 8-15s, 35-65 words): One specific outcome moment. "Within X weeks, I noticed Y." Tie back to the agitation beat — the specific 3am wake-up is now gone, etc.
  Beat 7 (CTA + guarantee, 5-10s, 20-40 words): "Link below" / "I'll drop the link" / "60-day guarantee" / "don't wait as long as I did." Soft pull.

HARD RULES:
1. No scene markers. No "[cut to]". No "[B-roll]". No stage directions. ONLY the spoken words, exactly as the creator would say them, contractions and all.
2. The script must be ONE continuous monologue. Use natural commas, periods, question marks, em-dashes.
3. NO AI-copy banned phrases: "game-changer", "revolutionary", "you won't believe", "literally life-changing", "in a world where", "imagine if", "introducing", "are you tired of".
4. NO clichés like "I tried everything!" without follow-through specifics.
5. The hook_overlay_text is the BURNED text on screen, NOT the spoken hook. It's a 4-10 word teaser. Examples that work: "After trying 14 supplements for my hip pain", "My hip pain journey (tried everything)", "What finally worked for my joint pain". Match the overlay to the avatar's voice — older woman uses "supplement" not "supplements"; corporate tone never works.
6. estimated_duration_seconds must be (word_count / 4.2) rounded to int.
7. Each ad in a batch gets a different angle/desire — no repetition of the same hook idea.

OUTPUT SCHEMA (strict JSON array of N items):
[
  {
    "id": "vsl_001",
    "hook_overlay_text": "...",
    "hook_overlay_style": "red_badge",
    "vsl_script": "<continuous spoken monologue, no markup, ends with CTA>",
    "estimated_duration_seconds": 118,
    "narrative_arc_check": {
      "hook_words_1_to_22": "<verbatim first ~22 words of vsl_script>",
      "agitation_section_first_sentence": "...",
      "mechanism_section_first_sentence": "...",
      "solution_section_first_sentence": "...",
      "cta_section": "<verbatim final ~30 words of vsl_script>"
    }
  }
]
"""

def generate(brand, count, duration, concept, registry_path, out_path):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr); sys.exit(2)

    registry = json.loads(pathlib.Path(registry_path).read_text())
    bctx = load_brand_context(brand, registry)
    if not bctx["product_context"] and not bctx["context_md"]:
        print(f"WARNING: no vault docs found for brand '{brand}' — script will rely on concept seed only", file=sys.stderr)

    target_words = int(duration * WORDS_PER_SECOND)

    user_msg = f"""Brand: {brand}
Product context: {bctx['product_context']}
Narrative voice for this brand: {bctx['narrative_voice']}

Target duration per ad: {duration}s (≈ {target_words} spoken words at conversational pace)
Concept seed (optional): {concept or '(none — invent N angles from the vault docs)'}

Brand vault docs (research, VoC, copywriting briefs):
---
{bctx['context_md'] or '(no vault docs found — work from product context only)'}
---

Generate exactly {count} long-form continuous-shot VSL scripts following the 7-beat arc. Each ad gets a different angle/desire. Return strict JSON array, ids "vsl_001"..."vsl_{count:03d}"."""

    try:
        from anthropic import Anthropic
    except ImportError:
        os.system(f"{sys.executable} -m pip install -q anthropic")
        from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        scripts = json.loads(text)
    except json.JSONDecodeError:
        print(f"ERROR: model returned non-JSON. Raw:\n{text[:2500]}", file=sys.stderr); sys.exit(3)

    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_path).write_text(json.dumps(scripts, indent=2))
    print(f"Wrote {len(scripts)} VSL scripts to {out_path}", file=sys.stderr)
    for s in scripts:
        wc = len(s["vsl_script"].split())
        actual = wc / WORDS_PER_SECOND
        print(f"  {s['id']}: {wc} words, ~{actual:.0f}s spoken (claimed {s.get('estimated_duration_seconds')})", file=sys.stderr)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--brand", required=True)
    p.add_argument("--count", type=int, default=3)
    p.add_argument("--duration", type=int, default=120)
    p.add_argument("--concept", default="")
    p.add_argument("--registry", default=str(pathlib.Path(__file__).parent.parent / "registry.json"))
    p.add_argument("--output", required=True)
    a = p.parse_args()
    generate(a.brand, a.count, a.duration, a.concept, a.registry, a.output)
