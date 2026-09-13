#!/usr/bin/env python3
"""
Generate N two-cut AIUGC scripts via Anthropic Opus.

Output schema (JSON array):
[
  {
    "id": "ad_001",
    "hook_type_hint": "subtle|stunt",
    "setting_hint": "kitchen|bathroom|bedroom|gym|...",
    "cut1_vo": "<= ~22 words, ~8s of speech, ends mid-thought to set up cut",
    "cut2_visual_prompt": "Visual prompt for Seedance i2v action scene with product",
    "rationale": "one-line strategic why"
  }
]
"""
import argparse, json, os, sys, pathlib, glob

VAULT = pathlib.Path("/Users/brooksorradre2/Documents/marketing brain")

def load_env():
    env = VAULT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if v and not os.environ.get(k):
                os.environ[k] = v

def load_brand_context(brand_key, registry):
    bd = registry["brand_defaults"].get(brand_key, {})
    vault_path = bd.get("vault_path")
    chunks = []
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
        "rotation_pool": bd.get("rotation_pool") or [],
    }

SYSTEM = """You are a direct-response AIUGC scriptwriter producing prompts for a two-model pipeline:
- CUT 1: Higgsfield Marketing Studio Video (mode=ugc) — talking head with native VO
- CUT 2: Seedance 2.0 image-to-video, seeded from Cut 1's last frame — same creator using/holding/wearing the product

You produce JSON only. No markdown, no preamble.

CUT 1 RULES (talking-head VO):
1. cut1_vo MUST be <=22 words. Count them.
2. Voice = the avatar from VoC docs. Specific, conversational, no AI-copy tells.
3. Cut 1 ENDS MID-THOUGHT or with a setup line creating pull-through to Cut 2 ("...and watch what happened next" / "...this is what I do every morning" / "...let me show you").
4. NEVER use banned AI-copy phrases: "game-changer", "revolutionary", "you won't believe", "literally life-changing", "in a world where", "imagine if", "introducing".

CUT 2 RULES (Seedance 2.0 i2v prompt — seeded from Cut 1's last frame):
The creator is ALREADY in the seed frame. Do NOT re-describe her appearance, clothing, hair, or setting. Describe ONLY motion + product action + identity lock.

Required structure (60-120 words, in this order):
  a. UGC ANCHOR (always lead): "UGC creator, iPhone handheld, harsh window light, slightly imperfect framing,"
  b. CREATOR ACTION ON PRODUCT — ONE concrete physical verb chain. Use literal verbs: unscrews, lifts, tilts, pours, scoops, taps, twists, sips, drinks, sets down, snaps, dabs, rubs, spreads, wears, slips on, glances, nods, half-smiles. NEVER use abstract verbs (uses, interacts with, enjoys, experiences, showcases).
  c. CAMERA — exactly one: "locked-off camera, minimal handheld jitter" OR "slow handheld, no zoom, no pan". No orbits, no rotates, no dollies (these scramble product labels).
  d. SFX (no music, no narration): name the action sound. "Soft cap-pop and liquid sip SFX, no music, no narration." Cut 2 is silent of dialogue so Cut 1's VO dominates.
  e. IDENTITY + PRODUCT LOCK (verbatim): "Maintain exact appearance from reference image, no face morphing, no warping hands, no logo morphing, keep label perfectly readable, no garbled text. 5s, 720p, 9:16."

CUT 2 NEGATIVE RULES:
- DO NOT redescribe the creator's appearance, hair, outfit, or face — the seed frame defines them.
- DO NOT add "cinematic", "dramatic", "epic", "slow motion" — these break UGC believability.
- DO NOT request rotational camera moves on the product — labels scramble.
- DO NOT ask for new objects to appear — seed frame defines props.

GENERAL RULES:
- Each ad = different angle/desire. No repetition of the same hook idea twice.
- setting_hint must come from: kitchen, bathroom, bedroom, gym, office, in_car, street, nature.
- hook_type_hint is "subtle" for trust niches (health, premium) and "stunt" for snacks/tech/comedy/viral. Default subtle.

Output schema (strict JSON array, exactly N items):
[{"id":"ad_001","hook_type_hint":"subtle","setting_hint":"kitchen","cut1_vo":"...","cut2_visual_prompt":"...","rationale":"..."}]
"""

def generate(brand, count, concept, registry_path, out_path):
    load_env()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not in env", file=sys.stderr)
        sys.exit(2)

    registry = json.loads(pathlib.Path(registry_path).read_text())
    bctx = load_brand_context(brand, registry)

    user_msg = f"""Brand: {brand}
Product context: {bctx['product_context']}

Concept seed (optional): {concept or '(none — invent N angles from the vault docs)'}

Brand vault docs (research, VoC, copywriting briefs):
---
{bctx['context_md'] or '(no vault docs found — work from product context only)'}
---

Generate exactly {count} two-cut UGC ad scripts. Return strict JSON array, ids "ad_001"..."ad_{count:03d}"."""

    try:
        from anthropic import Anthropic
    except ImportError:
        print("Installing anthropic SDK...", file=sys.stderr)
        os.system(f"{sys.executable} -m pip install -q anthropic")
        from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        scripts = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"ERROR: model returned non-JSON. Raw:\n{text[:2000]}", file=sys.stderr)
        sys.exit(3)

    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_path).write_text(json.dumps(scripts, indent=2))
    print(f"Wrote {len(scripts)} scripts to {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--brand", required=True)
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--concept", default="")
    p.add_argument("--registry", default=str(pathlib.Path(__file__).parent.parent / "registry.json"))
    p.add_argument("--output", required=True)
    a = p.parse_args()
    generate(a.brand, a.count, a.concept, a.registry, a.output)
