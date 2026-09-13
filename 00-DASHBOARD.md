# 🧠 Marketing OS — Command Center

The operating system for pumping out ads at scale. Three layers: the **Engine** (reusable brain), the **Brands** (identical workspaces), and the **Archive** (cold storage, ignored by Obsidian).

*Last reorganized: 2026-06-22 — see [[MIGRATION-LOG]] for every move.*

---

## 🏭 The Factory Loop — how to make an ad

```
1. Pick a brand        → brands/<brand>/00-brief.md   (the source of truth)
2. Pull intelligence   → brand swipe/ + _engine/swipe-library/ + _engine/frameworks/
3. Generate            → run a skill (see Pipelines below); it reads brand by convention
4. Output lands in     → brands/<brand>/creative/  or  pages/
5. Pick the winner     → archive the rest to /_archive/
```

The whole point of the layout: **every brand has the same shape**, so a skill runs on any brand by name — no path guessing.

---

## 📁 Structure

```
marketing brain/
├── 00-DASHBOARD.md      ← you are here
├── MIGRATION-LOG.md     ← reversible record of the 2026-06-22 reorg
│
├── _engine/             ← THE BRAIN (reusable across all brands)
│   ├── frameworks/      ← DR fundamentals, psychology layer, banned-patterns, funnel, google-ads
│   ├── copywriting/     ← advertorial · listicle · hooks · long-form systems + references
│   ├── agents/          ← market-analyst · creative-strategist · copy-chief · hook-writer · …
│   ├── swipe-library/   ← cross-brand: statics · native-images · video-ads · 1000s of refs
│   ├── research/        ← competitive analysis + gethookd research (docs)
│   ├── sops/            ← operating SOPs, support, anti-chargeback, PMF
│   ├── tools/           ← python utilities + n8n export
│   ├── business/        ← P&L / financials
│   └── conversation-log/← auto-logged sessions
│
├── brands/              ← one identical workspace per brand (see _TEMPLATE/README.md)
│   ├── _TEMPLATE/       ← copy this to launch a new brand
│   ├── motilli/  lunessa/  velantra/  solorna/  renavita/  Orelli/  luma tea/  kalo rips/
│   │
│   └── each = brand/ · research/ · swipe/ · copy/ · creative/ · pages/ · funnel/ · ops/
│
├── swipe-intake/        ← n8n → vault ad ingestion queue
└── _archive/            ← cold storage (29GB stale media), EXCLUDED from Obsidian index
```

> **Apps** (specialist, replication-brief-machine, marketing-brain-cloud) now live **outside** the vault at `~/Documents/marketing-apps/` — they're software, not knowledge.

---

## 🎯 Brands

| Brand | Category | Status |
|---|---|---|
| **motilli** | Celery juice fiber gummies (GLP-1) | most built-out — the model brand |
| **lunessa** | Red Yeast Rice + CoQ10 (women 50+) | active |
| **velantra** | Leather goods (totes/bags) | active |
| **renavita** | Supplement | active |
| **solorna** | Fashion | testing |
| **Orelli** | Quiz-funnel brand | testing |
| **luma tea** | Beverage | early |
| **kalo rips** | Footwear swipe | stub |

Open any brand's `00-brief.md` first.

---

## 🛠️ Pipelines (skills)

Production skills live in `.claude/skills/`. Common ones:

- **Replicate an ad** → `higgsfield-replicator` (canonical) · `ad-replicator` · `video-scene-replicator`
- **AI UGC** → `aiugc-infinite` (two-cut) · `aiugc-longform` (VSL) · `aiugc-orchestrator`
- **Animated / claymation** → `animated-video` · `claymation`
- **Copy** → `long-form-copy` · `shopify-listicle-builder` · `rapid-vsl`
- **Pages** → `elixir-pdp-builder` · `landing-page-builder` · `sales-page-builder`
- **Audit** → `cro-agent` · `motilli-funnel-agent` · `broll-auditor`
- **Voice** → `elevenlabs-agent` (single source of truth for cloned voices → `voice-registry.json`)

---

## 🔑 Key references

- **Copy laws / banned AI patterns** → [[_engine/frameworks/# BANNED PATTERNS_ THE AI COPY BLACKLIST]]
- **Fundamentals index** → [[_engine/frameworks/_MOC-fundamentals]]
- **Agents** → `_engine/agents/`
- **API keys** → `.env` (root)
- **Cold archive** → `_archive/` (safe to move to external drive or prune)

## Shared ad memory

[[_engine/ad-system/data/memory/INDEX|Ad system memory — brands, creatives, decisions and agent notes]] · [Open Ad Studio](http://127.0.0.1:8791)

Use the linked creative record and agent notes when resuming ad work. Current workspace instructions govern over historical pipeline guidance above.
