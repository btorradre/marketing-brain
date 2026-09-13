# SOP: Video Creative Analysis (Gemini)

## Purpose
Analyze competitor or reference video ads to extract creative mechanics, persuasion architecture, and adaptation blueprints. Uses Gemini's native video understanding — no frame extraction needed.

## Tool Location
`/agents/creative-strategist/tools/analyze_video.py`

## Prerequisites
- `GEMINI_API_KEY` set in environment or `/Documents/marketing brain/.env`
- `pip install google-genai` (google-genai package)
- Video file accessible locally (download from Meta Ad Library, TikTok, etc.)

## Analysis Modes

### 1. Full Breakdown (`--mode full`)
Complete scene-by-scene analysis. Use when you need to understand every detail of a creative for replication or deep study.

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode full
```

### 2. Quick Summary (`--mode quick`)
High-level concept, hook, core mechanic, and steal-worthy elements. Use for rapid competitive scanning when reviewing multiple ads.

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode quick
```

### 3. Adaptation Mode (`--mode adaptation --brand "Motilli"`)
Full breakdown PLUS a complete brand-specific adaptation plan with villain mapping, ingredient heroes, rewritten scene breakdown, hook variations, and production recommendations.

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode adaptation --brand "Motilli"
```

### 4. Hook Analysis (`--mode hooks`)
Deep dive on the first 5 seconds only. Extracts the hook formula and generates 5 templated variations.

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode hooks
```

### 5. Ingredient Spotlight (`--mode ingredients`)
Focus on how the ad introduces and highlights each ingredient/feature. Provides a reusable template.

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode ingredients
```

## Saving Output

```bash
python3 tools/analyze_video.py --video "/path/to/video.mp4" --mode full \
    --output "/agents/creative-strategist/briefs/2026-03-24_Resilia_AnimatedVillain_analysis.md"
```

## Integration with Creative Sprint Workflow

### When to use video analysis:
1. **Before a creative sprint** — Analyze 2-3 top-performing competitor ads to identify steal-worthy mechanics
2. **During brief creation** — Reference a specific ad's structure as a template for your brief
3. **For adaptation projects** — When a client says "make me something like THIS" — run adaptation mode to get a complete blueprint

### Workflow:
1. Download the video (Meta Ad Library, TikTok, screen record, etc.)
2. Run `analyze_video.py` in the appropriate mode
3. Save the output to `/briefs/` or `/working-drafts/`
4. Use the analysis to inform your creative brief
5. Cross-reference with anti-mimicry audit — adapt the MECHANICS, not the surface

## Brand Registry
The tool has built-in context for: **Motilli**, **Lunessa**, **Velantra**

To add a new brand, update the `BRAND_REGISTRY` dict in `analyze_video.py` with:
- product, mechanism, key_ingredients, avatar, positioning, core_promise, research_docs
