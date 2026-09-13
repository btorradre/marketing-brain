# SOPs — Standard Operating Procedures
**The single source of truth for how we operate.** Every SOP in the portfolio lives here. From now on, any new SOP goes in this folder — nowhere else.

_Last updated: 2026-09-08_

---

## 📋 Index

| SOP | Scope | What it governs |
|---|---|---|
| **[Ad-Editing-Plan-First-SOP.md](Ad-Editing-Plan-First-SOP.md)** | All brands, all ad work | Mandatory editing plan before asset/voice generation or editing; reference cut analysis, line-to-visual schedule, audio/captions, revisions and QA. Created proactively without a separate user prompt. |
| **[Video-Brief-Format-SOP.md](Video-Brief-Format-SOP.md)** | All brands — LAW as of 2026-08-21 | The canonical brief format for every new video concept. Section order, the building-block prompt system, the visual schedule, the QC checklist. Exemplar + blank template in `brief-templates/`. |
| **[Seedance-Prompt-System.md](Seedance-Prompt-System.md)** | All brands, all video skills | How we prompt Seedance 2.5. The 12-module stack, the 8 content profiles, cut grammar, timing and word-density law, engine binding, QA and the retry ladder. Replaces the three legacy prompt formats. |
| **[Segment-Brief-SOP.md](Segment-Brief-SOP.md)** | All brands | Production brief format for segmented video runs. Its duration caps are superseded by the Seedance Prompt System. |
| **[Anti-Chargeback-SOP.md](Anti-Chargeback-SOP.md)** | All brands | Preventing, intercepting, and fighting chargebacks. CS scripts, evidence kits, reason-code playbook, SLAs. |
| **DR-Operating-System-SOP.docx** | All brands | The direct-response operating system / master workflow. |
| **DR-SOP-Obsidian.md** | All brands | DR workflow inside the Obsidian vault. |
| **Product-Market-Fit-SOP.md** | All brands | Validating product–market fit before scaling. |
| **Lunessa_Customer_Support_SOP.docx** | Lunessa | Brand-specific customer support procedures. |
| **Motilli_Customer_Support_SOP.docx** | Motilli | Brand-specific customer support procedures. |

---

## 🧭 Conventions (how we run this folder)

1. **One home.** Every SOP lives in `marketing brain/SOPs/`. No SOPs scattered in `brands/`, `fundamentals/`, etc.
2. **Naming:** `Topic-SOP.md` for portfolio-wide; `Brand_Topic_SOP.ext` for brand-specific.
3. **Header on every SOP:** Owner · Applies to (brands) · Last updated.
4. **Portfolio-first:** write SOPs to apply to ALL brands by default; use `[Brand]` / `[DESCRIPTOR]` placeholders. Only make a brand-specific SOP when the brand genuinely diverges.
5. **When you add an SOP, add a row to the index above.**

---

## 🔜 SOP backlog (gaps worth filling)

- **Refund & Returns SOP** — unify the refund authority referenced in the Anti-Chargeback SOP across all brands.
- **Subscription Lifecycle SOP** — sign-up clarity, pre-billing reminders, dunning, cancellation (the biggest chargeback lever).
- **Fulfillment / 3PL SOP** — tracking upload standard, lost-package handling, SLA.
- **Customer Support Master SOP** — channels, tone, response-time SLAs, escalation (consolidate the per-brand CS docs into one standard + brand annexes).
- **Payments / Payout Health SOP** — daily disputes-queue check, payout-failure monitoring, reserve tracking (ties to the Shopify Holds tab).

---

## 📎 Note — duplicate left in place
A copy of `Lunessa_Customer_Support_SOP.docx` also exists at `marketing-brain-cloud/vault/lunessa/research/`. That path is a **cloud-synced vault**, so I left it untouched to avoid breaking sync. The canonical copy is the one here in `SOPs/`. Say the word if you want the cloud copy removed or re-pointed.
