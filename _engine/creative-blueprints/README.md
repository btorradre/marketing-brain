# Creative blueprints and editing profiles

Canonical engine library: **13 concept families, 15 variants, 30 blueprint/profile documents and 14 callable skills**. Each variant covers scripting structure, visual-to-line relationships, cuts, transitions, B-roll placement and style, movement, captions, sound, pacing and endings. The definitions include 96 beat slots and 48 style specifications across the variants.

Start with the [creative diversity router](skills/creative-diversity-router/SKILL.md) or the [comparison catalog](skills/creative-diversity-router/references/blueprint-catalog.md). Use the [manifest](manifest.json) for stable IDs and relative file paths. This whole folder can be copied into another harness without the surrounding vault.

## Call from a harness

Python 3.9+; standard library only. From the repository root:

```sh
python3 _engine/creative-blueprints/blueprints.py list --json
python3 _engine/creative-blueprints/blueprints.py show greenscreen-comparison-guide --format json
python3 _engine/creative-blueprints/blueprints.py context greenscreen-comparison-guide
python3 _engine/creative-blueprints/blueprints.py validate
```

`show --format json` returns named beat/style fields, editorial rules and bundle-relative paths. `--format blueprint` or `--format profile` returns the corresponding Markdown. `context` prints the selected skill, blueprint, editing profile, source audit, contracts and shared SOPs as one reading packet; source image links still resolve from the named original files. Choose a profile with the router before loading a packet. Commands work from any current directory when called by their actual script path.

Give an agent this instruction:

> Read `_engine/creative-blueprints/README.md` and its router. Select the concept by communication job and visual treatment. Load the chosen profile with `blueprints.py context PROFILE_ID`, inspect its linked evidence, and map the approved target script to its blueprint and editing rules. Save a concrete editing plan before production. Keep observed evidence and proposed direction separate.

If the harness discovers skills through a directory, register all 14 with:

```sh
python3 _engine/creative-blueprints/blueprints.py install --skills-dir /path/to/harness/skills
```

Registration creates links, preserves existing entries, and safely skips links already resolving to this library. It refuses name conflicts before creating links; choose a separate directory or intentionally reconcile existing skills. Keep the bundle in place after registration. A running host may need its skill catalog refreshed. In the original vault, existing `.claude/skills` and Codex discovery names already resolve to this engine copy.

For a small Git checkout containing only this package:

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone --filter=blob:none --sparse https://github.com/btorradre/marketing-brain.git marketing-brain
cd marketing-brain
git sparse-checkout set _engine/creative-blueprints
python3 _engine/creative-blueprints/blueprints.py validate
```

The retained study JPEGs are ordinary Git files scoped by this folder's `.gitattributes`; this package needs no LFS fetch. No external Python dependencies, credentials or media services are required to read or validate it.

## Available variants

| Stable profile ID | Blueprint | Editing profile | Source |
|---|---|---|---|
| `street-personal-profile` | [Personal wardrobe interview](skills/concept-street-style-interview/references/street-personal-profile-blueprint.md) | [Profile](skills/concept-street-style-interview/references/street-personal-profile-editing-profile.md) | [R01](research/R01/analysis.md) |
| `street-event-roundup` | [Event outfit roundup](skills/concept-street-style-interview/references/street-event-roundup-blueprint.md) | [Profile](skills/concept-street-style-interview/references/street-event-roundup-editing-profile.md) | [R11](research/R11/analysis.md) |
| `cultural-conversation` | [Brand cultural conversation](skills/concept-brand-cultural-interview/references/cultural-conversation-blueprint.md) | [Profile](skills/concept-brand-cultural-interview/references/cultural-conversation-editing-profile.md) | [R07](research/R07/analysis.md) |
| `greenscreen-comparison-guide` | [Greenscreen comparison and service guide](skills/concept-ai-greenscreen-guide/references/greenscreen-comparison-guide-blueprint.md) | [Profile](skills/concept-ai-greenscreen-guide/references/greenscreen-comparison-guide-editing-profile.md) | [R05](research/R05/analysis.md) |
| `podcast-reverse-listicle` | [Podcast-style reverse-selling listicle](skills/concept-podcast-split-screen/references/podcast-reverse-listicle-blueprint.md) | [Profile](skills/concept-podcast-split-screen/references/podcast-reverse-listicle-editing-profile.md) | [R02](research/R02/analysis.md) |
| `craft-to-carry-film` | [Craft-to-carry brand film](skills/concept-branded-craft-film/references/craft-to-carry-film-blueprint.md) | [Profile](skills/concept-branded-craft-film/references/craft-to-carry-film-editing-profile.md) | [R03](research/R03/analysis.md) |
| `animated-discovery-musical` | [Animated discovery narrative with refrain](skills/concept-animated-discovery-musical/references/animated-discovery-musical-blueprint.md) | [Profile](skills/concept-animated-discovery-musical/references/animated-discovery-musical-editing-profile.md) | [R04](research/R04/analysis.md) |
| `animated-silent-microstory` | [Silent animated desire and reveal](skills/concept-animated-silent-story/references/animated-silent-microstory-blueprint.md) | [Profile](skills/concept-animated-silent-story/references/animated-silent-microstory-editing-profile.md) | [R06](research/R06/analysis.md) |
| `countdown-product-catalogue` | [Countdown product catalogue](skills/concept-countdown-catalogue/references/countdown-product-catalogue-blueprint.md) | [Profile](skills/concept-countdown-catalogue/references/countdown-product-catalogue-editing-profile.md) | [R08](research/R08/analysis.md) |
| `voiceover-creator-endorsement` | [Creator-style product voiceover](skills/concept-product-voiceover/references/voiceover-creator-endorsement-blueprint.md) | [Profile](skills/concept-product-voiceover/references/voiceover-creator-endorsement-editing-profile.md) | [R09](research/R09/analysis.md) |
| `voiceover-concise-value` | [Concise product-and-value voiceover](skills/concept-product-voiceover/references/voiceover-concise-value-blueprint.md) | [Profile](skills/concept-product-voiceover/references/voiceover-concise-value-editing-profile.md) | [R14](research/R14/analysis.md) |
| `urban-collection-film` | [Urban fashion collection film](skills/concept-urban-fashion-film/references/urban-collection-film-blueprint.md) | [Profile](skills/concept-urban-fashion-film/references/urban-collection-film-editing-profile.md) | [R10](research/R10/analysis.md) |
| `fashion-world-montage` | [Fashion worldbuilding still montage](skills/concept-fashion-mood-montage/references/fashion-world-montage-blueprint.md) | [Profile](skills/concept-fashion-mood-montage/references/fashion-world-montage-editing-profile.md) | [R12](research/R12/analysis.md) |
| `kinetic-product-detail-sequence` | [Kinetic product-detail still sequence](skills/concept-kinetic-product-details/references/kinetic-product-detail-sequence-blueprint.md) | [Profile](skills/concept-kinetic-product-details/references/kinetic-product-detail-sequence-editing-profile.md) | [R13](research/R13/analysis.md) |
| `ai-ugc-greenscreen-story` | [AI UGC greenscreen product story](skills/concept-ai-ugc-greenscreen/references/ai-ugc-greenscreen-story-blueprint.md) | [Profile](skills/concept-ai-ugc-greenscreen/references/ai-ugc-greenscreen-story-editing-profile.md) | [W01](research/W01/analysis.md) |

## Evidence and production scope

The added [AI UGC greenscreen family](skills/concept-ai-ugc-greenscreen/SKILL.md) captures the Nuamore-style corner guide, Eleanor travel and Vivienne quiet-luxury work, including exact voice, reveal and pacing corrections. Its workspace evidence is separately labeled W01. Load it with `python3 _engine/creative-blueprints/blueprints.py context ai-ugc-greenscreen-story`.

The [14-reference study index](research/INDEX.md) links each source, analysis and retained evidence. All 21,504 decoded frames were inspected at thumbnail scale, with selected enlarged checks. Audio observations are model-assisted, not directly auditioned; exact sound/word alignment and R04's spoken/sung boundaries remain unresolved. Source tools, AI origin, rights and performance are generally unknown. Proposed dwell ranges are adaptable editorial direction, not recovered project settings or validated optimums.

For production, read the [production contract](skills/creative-diversity-router/references/production-contract.md) and [application contract](skills/creative-diversity-router/references/profile-contract.md). Use the [editing-plan template](skills/creative-diversity-router/assets/concept-editing-plan-template.md). Current user instructions and approved copy take precedence. The library preserves GPT Image 2 / Google Omni / DaVinci Resolve / Cut Room requirements; it does not install those integrations, brand/product evidence, the broader host skill collection or a live ad-system database. An actual storyboard or production delivery requires those dependencies, not merely this library.

## Maintain

Edit `skills/creative-diversity-router/references/profiles.json`, then run:

```sh
python3 _engine/creative-blueprints/skills/creative-diversity-router/scripts/render_profiles.py
python3 _engine/creative-blueprints/blueprints.py validate
```

The renderer maintains all 30 paired documents. Update the manifest if IDs, titles, families or source paths change. Validation checks relative links, recorded source coverage and generated-document consistency; it does not rewatch videos, certify audio or measure creative performance. Preserve analysis provenance and limitations when adapting this package.
