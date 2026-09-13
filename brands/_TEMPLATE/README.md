# Brand Workspace Template

**Copy this entire `_TEMPLATE/` folder and rename it to launch a new brand.** Every brand in this vault has the identical shape below so that skills and agents can find anything by convention — no guessing where a brand keeps its product images or copy.

```
<brand>/
├── 00-brief.md     ← START HERE. Avatar, positioning, VoC, product context, offer. The source of truth.
├── brand/          ← Identity assets: logo, hero/product-reference images, brand guide, legal
├── research/       ← Market & avatar research dossiers, ICP, VoC raw data
├── swipe/          ← Brand-specific saved references + winning ads + ad breakdowns
├── copy/           ← advertorials · listicles · long-form · hooks · scripts · concepts (+ briefs/, strategy/)
├── creative/       ← statics · video · b-roll · native · generated · product-images · ugc
├── pages/          ← PDPs · landing pages · advertorial pages · theme/shopify · previews
├── funnel/         ← CRO audits · funnel analysis
└── ops/            ← deploy scripts, data exports, customer-support SOPs, misc operational files
```

## Conventions skills rely on

- **Hero / product-reference image** lives in `brand/` (e.g. `brand/website-assets/` or `brand/product-references/`). Register its path in the skill registries when launching the brand.
- **Strategic docs** (`Master_Copywriting_Brief`, `Avatar_VoC`, `Product_Context`) live in `copy/briefs/` or `copy/strategy/`.
- **Generated factory output** (renders, test runs) is disposable — once a winner is chosen, archive the rest to `/_archive/` rather than letting it accumulate here.

## Launching a new brand
1. `cp -R brands/_TEMPLATE brands/<newbrand>`
2. Fill in `00-brief.md`.
3. Drop the hero image into `brand/`.
4. Add the brand to the skill registries (`.claude/skills/aiugc-infinite/registry.json`, `higgsfield-replicator/products.json`, etc.) with its `vault_path` and `hero_image`.
