# Migration Log — Marketing OS Reorg

Date: 2026-06-22
Principle: separate Engine / Brands / Factory-Output. No deletions of data — apps moved out whole, dead media cold-archived. Every move below is reversible (reverse src<->dst).

## Moves


### Apps moved out of vault -> ~/Documents/marketing-apps/
- `specialist/` -> `~/Documents/marketing-apps/specialist/`
- `replication-brief-machine/` -> `~/Documents/marketing-apps/replication-brief-machine/`
- `marketing-brain-cloud/` -> `~/Documents/marketing-apps/marketing-brain-cloud/`
- `specialist-codex-prompt.md` -> `~/Documents/marketing-apps/`

### Dead media cold-archived -> _archive/ (nothing deleted)
- `brands/lunessa/videos` -> `_archive/lunessa/videos`
- `brands/lunessa/video editors` -> `_archive/lunessa/video-editors`
- `b-roll` -> `_archive/global/b-roll`
- `higgsfield-runs` -> `_archive/global/higgsfield-runs`
- `gethookd-cache` -> `_archive/global/gethookd-cache`
- `research/gethookd-research/videos` -> `_archive/global/gethookd-research-videos`
- `archive` -> `_archive/legacy-archive`

### Knowledge consolidated -> _engine/
- `copywriting` -> `_engine/copywriting`
- `agents` -> `_engine/agents`
- `SOPs` -> `_engine/sops`
- `research` -> `_engine/research`
- `fundamentals` -> `_engine/frameworks/fundamentals`
- `funnel analysis` -> `_engine/frameworks/funnel-analysis`
- `google-ads-knowledge` -> `_engine/frameworks/google-ads`
- `# BANNED PATTERNS_ THE AI COPY BLACKLIST.md` -> `_engine/frameworks/`
- `_MOC-fundamentals.md` -> `_engine/frameworks/`
- `skills/CUSTOMER-PSYCHOLOGY-LAYER-PATCHES.md` -> `_engine/frameworks/`
- `video ads` -> `_engine/swipe-library/video-ads`
- `native images` -> `_engine/swipe-library/native-images`
- `statics` -> `_engine/swipe-library/statics`
- `skills/funnel-advisory` -> `_engine/standalone-skills/funnel-advisory`
- `skills/hook-congruence` -> `_engine/standalone-skills/hook-congruence`
- `tools` -> `_engine/tools`
- `n8n_export_all.sh` -> `_engine/tools/`
- `Q1_2026_PL_Analysis.xlsx` -> `_engine/business/`
- `Shopify_PL_Jan2026-YTD.xlsx` -> `_engine/business/`
- `conversation-log` -> `_engine/conversation-log`
- `skills/video-gen.zip` -> `_archive/global/`
- `skills/watch.zip` -> `_archive/global/`

### Brand reshape: motilli
- `brands/motilli/product-images` -> `brands/motilli/creative/`
- `brands/motilli/natives` -> `brands/motilli/creative/`
- `brands/motilli/concepts` -> `brands/motilli/creative/`
- `brands/motilli/Motilli Content Library` -> `brands/motilli/creative/`
- `brands/motilli/workflows` -> `brands/motilli/creative/`
- `brands/motilli/landing-pages` -> `brands/motilli/pages/`
- `brands/motilli/cro` -> `brands/motilli/funnel/`
- `brands/motilli/audits` -> `brands/motilli/funnel/`
- `brands/motilli/ad-watcher` -> `brands/motilli/swipe/`
- `brands/motilli/Motilli Winning Ads.rtf` -> `brands/motilli/swipe/`
- `brands/motilli/brand-guide.md` -> `brands/motilli/brand/`
- `brands/motilli/operations` -> `brands/motilli/ops/`
- `brands/motilli/migration` -> `brands/motilli/ops/`

### Brand reshape: lunessa
- `brands/lunessa/website assets` -> `brands/lunessa/brand/`
- `brands/lunessa/L.png` -> `brands/lunessa/brand/`
- `brands/lunessa/lunessa profile pic.jpg` -> `brands/lunessa/brand/`
- `brands/lunessa/headlines.png` -> `brands/lunessa/brand/`
- `brands/lunessa/Lunessa.docx` -> `brands/lunessa/brand/`
- `brands/lunessa/legal` -> `brands/lunessa/brand/`
- `brands/lunessa/fh research docs` -> `brands/lunessa/research/`
- `brands/lunessa/hyperthyroidism market research` -> `brands/lunessa/research/`
- `brands/lunessa/hypothyroidism assets` -> `brands/lunessa/research/`
- `brands/lunessa/menopause research 2.0` -> `brands/lunessa/research/`
- `brands/lunessa/post menopause research docs` -> `brands/lunessa/research/`
- `brands/lunessa/listicle` -> `brands/lunessa/copy/`
- `brands/lunessa/advertorial prompt` -> `brands/lunessa/copy/`
- `brands/lunessa/Long Form Copy Breakdown.pdf` -> `brands/lunessa/copy/`
- `brands/lunessa/instagram creative concepts` -> `brands/lunessa/copy/`
- `brands/lunessa/new concepts` -> `brands/lunessa/copy/`
- `brands/lunessa/Evolve Winning Ads Doucment + Templates _ Body Copies.pdf` -> `brands/lunessa/swipe/`
- `brands/lunessa/video ad swipes` -> `brands/lunessa/swipe/`
- `brands/lunessa/image ads` -> `brands/lunessa/creative/`
- `brands/lunessa/broll-scenes` -> `brands/lunessa/creative/`
- `brands/lunessa/statics` -> `brands/lunessa/creative/`
- `brands/lunessa/new product images` -> `brands/lunessa/creative/`
- `brands/lunessa/product images` -> `brands/lunessa/creative/`
- `brands/lunessa/alibaba product images` -> `brands/lunessa/creative/`
- `brands/lunessa/website ugc` -> `brands/lunessa/creative/`
- `brands/lunessa/sarah mitchell` -> `brands/lunessa/creative/`
- `brands/lunessa/landing pages` -> `brands/lunessa/pages/`
- `brands/lunessa/orders_export_1.csv` -> `brands/lunessa/ops/`

### Brand reshape: velantra
- `brands/velantra/icp:branding` -> `brands/velantra/research/icp-branding`
- `brands/velantra/product-images` -> `brands/velantra/creative/`
- `brands/velantra/statics` -> `brands/velantra/creative/`
- `brands/velantra/ugc creators` -> `brands/velantra/creative/`
- `brands/velantra/workflows` -> `brands/velantra/creative/`
- `brands/velantra/product pages` -> `brands/velantra/pages/`

### Brand reshape: solorna
- `brands/solorna/solorna_brand_document.txt` -> `brands/solorna/brand/`
- `brands/solorna/product images ` -> `brands/solorna/creative/`
- `brands/solorna/ugc` -> `brands/solorna/creative/`
- `brands/solorna/prompts_beige.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_black.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_brown.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_coffee.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_khaki.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_skyblue.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_beige.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_black.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_brown.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_coffee.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_khaki.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/prompts_skyblue.txt` -> `brands/solorna/creative/prompts/`
- `brands/solorna/solorna_img2img_prompts.json` -> `brands/solorna/creative/prompts/`
- `brands/solorna/solorna_product_image_prompts.json` -> `brands/solorna/creative/prompts/`

### Brand reshape: renavita
- `brands/renavita/renavita logo.png` -> `brands/renavita/brand/`
- `brands/renavita/renavita social proof  2.png` -> `brands/renavita/brand/`
- `brands/renavita/renavita social proof .png` -> `brands/renavita/brand/`
- `brands/renavita/press-logos` -> `brands/renavita/brand/`
- `brands/renavita/research dossier` -> `brands/renavita/research/`
- `brands/renavita/ad-copy-aligned` -> `brands/renavita/copy/`
- `brands/renavita/listicle-bp` -> `brands/renavita/copy/`
- `brands/renavita/listicle-ceylon` -> `brands/renavita/copy/`
- `brands/renavita/listicle-chol` -> `brands/renavita/copy/`
- `brands/renavita/listicle-metformin` -> `brands/renavita/copy/`
- `brands/renavita/natives` -> `brands/renavita/copy/`
- `brands/renavita/product images` -> `brands/renavita/creative/`
- `brands/renavita/generated-images` -> `brands/renavita/creative/`
- `brands/renavita/menopause-pdp` -> `brands/renavita/pages/`
- `brands/renavita/product-page` -> `brands/renavita/pages/`
- `brands/renavita/shopify` -> `brands/renavita/pages/`
- `brands/renavita/theme-sections` -> `brands/renavita/pages/`
- `brands/renavita/checkout-extension` -> `brands/renavita/pages/`
- `brands/renavita/alevia-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/compare-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/core-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/footer-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/index.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/renavita-lp.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/results-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/timeline-preview.html` -> `brands/renavita/pages/previews/`
- `brands/renavita/deploy_menopause.py` -> `brands/renavita/ops/scripts/`
- `brands/renavita/deploy_page.py` -> `brands/renavita/ops/scripts/`
- `brands/renavita/deploy_theme.py` -> `brands/renavita/ops/scripts/`
- `brands/renavita/generate_sections.py` -> `brands/renavita/ops/scripts/`
- `brands/renavita/upload_files.py` -> `brands/renavita/ops/scripts/`

### Brand reshape: Orelli
- `brands/Orelli/node_modules` -> `_archive/global/Orelli-node_modules/`
- `brands/Orelli/hero_response.json` -> `_archive/global/Orelli-api-debris/`
- `brands/Orelli/hero_ref_response.json` -> `_archive/global/Orelli-api-debris/`
- `brands/Orelli/imagen_response.json` -> `_archive/global/Orelli-api-debris/`
- `brands/Orelli/hero_request.json` -> `_archive/global/Orelli-api-debris/`
- `brands/Orelli/assets` -> `brands/Orelli/brand/`
- `brands/Orelli/statics` -> `brands/Orelli/brand/`
- `brands/Orelli/public` -> `brands/Orelli/brand/`
- `brands/Orelli/research docs` -> `brands/Orelli/research/`
- `brands/Orelli/survey data` -> `brands/Orelli/research/`
- `brands/Orelli/Orelli Quiz Funnel — Younger Avatar (Women 20-30).md` -> `brands/Orelli/copy/`
- `brands/Orelli/coravita-landing-section.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/coravita-landing-v2.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/coravita-v2-landing.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/coravita-v3-landing.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/motilli-glp1-diarrhea-landing.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/motilli-glp1-pdp.liquid` -> `brands/Orelli/pages/`
- `brands/Orelli/florava-landing.html` -> `brands/Orelli/pages/`
- `brands/Orelli/quiz-funnel.html` -> `brands/Orelli/pages/`
- `brands/Orelli/florava-deploy` -> `brands/Orelli/pages/`
- `brands/Orelli/gen_hero.sh` -> `brands/Orelli/ops/`
- `brands/Orelli/gen_image.sh` -> `brands/Orelli/ops/`
- `brands/Orelli/serve-lp.js` -> `brands/Orelli/ops/`
- `brands/Orelli/server.js` -> `brands/Orelli/ops/`
- `brands/Orelli/test_higgsfield.mjs` -> `brands/Orelli/ops/`
- `brands/Orelli/package-lock.json` -> `brands/Orelli/ops/`
- `brands/Orelli/package.json` -> `brands/Orelli/ops/`
- `brands/Orelli/quiz-leads.json` -> `brands/Orelli/ops/`
- `brands/Orelli/section-content.json` -> `brands/Orelli/ops/`
- `brands/Orelli/vercel.json` -> `brands/Orelli/ops/`
- `brands/Orelli/api` -> `brands/Orelli/ops/`
- `brands/Orelli/web-traffic-estimator` -> `brands/Orelli/ops/`
- `brands/Orelli/hero_lifestyle.png` -> `brands/Orelli/ops/`
- `brands/Orelli/hero_lifestyle_ref.png` -> `brands/Orelli/ops/`

### Brand reshape: kalo rips + luma tea
- `brands/kalo rips/sandal rip` -> `brands/kalo rips/swipe/`
- `brands/luma tea/logos` -> `brands/luma tea/brand/`
- `brands/luma tea/product images` -> `brands/luma tea/creative/`
- `brands/luma tea/theme` -> `brands/luma tea/pages/`

### Product references distributed to brands + skill refs fixed
- `_engine/swipe-library/statics/product references/lunessa` -> `brands/lunessa/brand/product-references/`
- `_engine/swipe-library/statics/product references/motilli` -> `brands/motilli/brand/product-references/`
- `_engine/swipe-library/statics/product references/velantra` -> `brands/velantra/brand/product-references/`

### Fixed stale BRAND_CONFIG paths in replicator Python (were already broken pre-migration)
- patched stale paths in `.claude/skills/broll-sourcer/broll_sourcer.py`
- patched stale paths in `.claude/skills/video-scene-replicator/pipeline.py`
- patched stale paths in `.claude/skills/fashion-replicator/fashion_replicator.py`

---

## Summary

- **Before:** 51GB, every brand a different shape, 3 apps + node_modules inside the vault, stale HOME.md.
- **After:** ~19.7GB live vault (29GB cold-archived, nothing deleted).
- Apps moved to `~/Documents/marketing-apps/`.
- Knowledge consolidated under `_engine/`.
- All 8 brands reshaped to the `_TEMPLATE` standard (brand·research·swipe·copy·creative·pages·funnel·ops).
- Skill path references updated + verified to resolve on disk.
- `_archive/` excluded from Obsidian index (`.obsidian/app.json` userIgnoreFilters).

### How to reverse any move
Each line above is `mv SRC -> DST`. To undo, run `mv DST/<item> SRC`. Apps: `mv ~/Documents/marketing-apps/<app> ./`.

### Next (optional)
- Move `_archive/` (29GB) to an external drive once confident nothing is needed.
- Fill in `00-brief.md` for brands that lack one.
- `git init` a knowledge-only repo (media gitignored) for version safety.

### Deletions to macOS Trash (2026-06-22, recoverable until Trash emptied)
- TRASHED `_archive/lunessa/videos` ( 25G)
- TRASHED `_archive/lunessa/video-editors` (1.1G)
- TRASHED `_archive/global/b-roll` (1.3G)
- TRASHED `brands/motilli/creative/workflows/glp1-vsl-01/broll` (577M)
- TRASHED `brands/motilli/creative/MOT-GLP1-VSL-01/b-roll` ( 46M)

### Skill consolidation: single source of truth (2026-06-22)
- skill `broll-sourcer`: removed stale project copy, symlinked project -> `~/.claude/skills/broll-sourcer`
- skill `video-scene-replicator`: removed stale project copy, symlinked project -> `~/.claude/skills/video-scene-replicator`
- skill `video-editor-brief`: removed stale project copy, symlinked project -> `~/.claude/skills/video-editor-brief`

### Skill lifecycle automation (2026-06-22)
- Retired the manual cp -f user->project sync hack (removed 2 obsolete permission rules).
- 3 duplicated skills (broll-sourcer, video-scene-replicator, video-editor-brief): project shadows replaced with symlinks -> ~/.claude/skills (single source of truth, USER canonical). Re-applied brand-path fixes to canonical copies.
- Added `_engine/tools/skill-janitor.sh`: cleans stale skill files (.bak, *~, .DS_Store, superseded SKILL*.md variants) inside skill dirs ONLY; routes to Trash; logs to skill-janitor.log. NEVER touches the copy/advertorial version libraries.
- Wired PostToolUse(Edit|Write) hook in .claude/settings.local.json -> runs the janitor scoped to the edited skill dir. Pipe-tested + live-fire proven (auto-removed a planted stale file).

### Velantra reorg: product-first (2026-06-22)
- `velantra/brand/product-references/boat tote` -> `velantra/products/boat-tote/product-references/`
- `velantra/creative/product-images/boat tote` -> `velantra/products/boat-tote/product-images/`
- `velantra/creative/statics/boat tote` -> `velantra/products/boat-tote/statics/`
- `velantra/creative/boat tote/ripped ugc` -> `velantra/products/boat-tote/ugc/`
- `velantra/brand/product-references/weekender` -> `velantra/products/weekender/product-references/`
- `velantra/creative/product-images/weekender` -> `velantra/products/weekender/product-images/`
- `velantra/creative/weekender/weekender aivo 1` -> `velantra/products/weekender/video/`
- `velantra/brand/product-references/meridian` -> `velantra/products/meridian/product-references/`
- `velantra/creative/product-images/meridian` -> `velantra/products/meridian/product-images/`
- `velantra/creative/product-images/straw birkin` -> `velantra/products/straw-birkin/product-images/`
- `velantra/creative/statics/straw birkin` -> `velantra/products/straw-birkin/statics/`
- `velantra/creative/straw birkin ` -> `velantra/products/straw-birkin/ugc/`
- `velantra/creative/straw birkin ripped` -> `velantra/products/straw-birkin/ugc-ripped/`
- `velantra/brand/product-references/jelly tote` -> `velantra/products/jelly-tote/product-references/`
- `velantra/creative/jelly firkin ripped` -> `velantra/products/jelly-tote/ugc-ripped/`
- `velantra/brand/product-references/inspired birkin` -> `velantra/products/inspired-birkin/product-references/`
- `velantra/creative/ugc creators/Caroline Nutt` -> `velantra/_shared/ugc-creators/`
- `velantra/creative/workflows/video ad references` -> `velantra/_shared/references/`
- `velantra/brand/product-references/_build` -> `velantra/_shared/theme-build/`
- `velantra/brand/product-references/pov-test-001` -> `velantra/_shared/experiments/`
- `velantra/brand/product-references/omnisend` -> `velantra/_shared/omnisend/`
- `velantra/brand/product-references/velantra-popup.liquid` -> `velantra/_shared/site-assets/`
- `velantra/brand/product-references/straw-tote-delay-email.html` -> `velantra/_shared/site-assets/`
- `velantra/brand/product-references/alia-popups-build-spec.md` -> `velantra/_shared/site-assets/`

### Long-form copy: monolith -> modular system (2026-06-22)
- copied 164KB monolith -> `_engine/copywriting/long form copy/reference/long-form-copy-MASTER-reference.md` (deep reference)
