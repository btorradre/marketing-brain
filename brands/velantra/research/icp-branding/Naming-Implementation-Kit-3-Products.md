# Velantra Naming Implementation Kit — Straw Tote · Boat Tote · Weekender · Meridian

**Date:** 2026-07-22 (Meridian added same day) · **Status:** READY TO EXECUTE on Brooks's go — nothing pushed yet
**Companions:** `Velantra-Naming-System-The-Women.md` (full system) · `Vestirsi-Brand-Study.md` (model)

---

## 0. The architecture in one line

Four bags = four facets of ONE Velantra Woman (the Vestirsi synthesis): **her workweek, her every day, her weekends away, her summer.** The name is the only place this shows up on a PDP — **no on-page vignette, no biography.** Like Vestirsi names "the Eden" but never writes Eden a summer or a schedule, the bag is never personified (brand law). The one-woman idea lives lightly on the About page; cross-sells complete the set.

## 1. The renames

| Live product (handle — unchanged) | New Shopify title |
| :--- | :--- |
| `copy-of-velantra-straw-tote` | **The Sofia — Woven Straw Tote** |
| `velantra-boat-tote-2` | **The Camille — Boat Tote** |
| `velantra-weekender` | **The Eleanor — Weekender** |
| `velantra-meridian-tote` | **The Margot — Structured Work Tote** |

**Margot positioning (per Brooks):** the chic/professional bag. Not a utility laptop hauler — boardroom polish. Margot R. is the existing "former designer loyalist" testimonial archetype ("I've carried the designer names, and this is the one strangers actually stop to ask about"), so the chic-professional slot was written for her. Camille vs. Margot split (Vestirsi's Rita/Vera split): Camille = off-duty everyday errands; Margot = on-duty professional polish. No overlap.

**"Meridian" retirement:** descriptor becomes the category term "Structured Work Tote" ("work tote" = the search term; "Meridian" is a proprietary word with zero SEO value). Live Meridian-pack ads keep running unchanged — the bag pictured is identical and congruence rides on the product, not the word. Keep "Meridian" in the PDP SEO meta for a transition month if any scaled ad names it on-screen.

- **Titles only. Handles, URLs, variant IDs untouched** → no 301s, no Meta catalog/pixel reset, Google/Meta feeds pick up new titles as a routine update.
- Descriptor stays in the title → category SEO ("straw tote", "boat tote", "weekender bag") and Google Ads keyword/landing congruence preserved; Straw Tote delay-notice audience still recognizes their bag.
- Colorways read naturally: "The Camille in Navy," "The Sofia in Sky Blue."
- Future line extensions franchise the name (Vestirsi "Bella Family" law): "The Sofia Mini," never a new name.
- Camille note: overlaps with UGC avatar roster name. Fine to keep (avatars are internal casting labels). Approved alternate if Brooks prefers: **The Frances**.
- Accessories (Bag Scarf, charms, keychain, organizer) stay descriptive — finishing touches, not characters.

## 2. PDP copy blocks (paste-ready)

Structure per PDP: **H1 = title · existing craft/function copy below, unchanged.** No epithet, no vignette. The name is the only brand layer the page adds — everything else describes the bag and speaks to the buyer, Vestirsi-style. No "the summer one"–style epithet subtitle: it states the obvious (a woven straw tote is self-evidently the summer bag), cheapens the name, and lowers perceived value. The bag is never given a life, a summer, or a schedule; personifying it is a brand law violation (and it reads forced — telling, not showing).

Cross-sell ordering (internal logic only): **Margot (workweek) → Eleanor (weekend away) → Sofia (summer) → Camille (every day) → Margot.**

### The Margot — Structured Work Tote
> **The Margot**

### The Eleanor — Weekender
> **The Eleanor**

### The Sofia — Woven Straw Tote
> **The Sofia**

### The Camille — Boat Tote
> **The Camille**

**Cross-sell footer:** plain product suggestion only — "You may also like the Camille," "Pair with the Eleanor." No narrative footer (kill "Sofia's summer ends. The errands don't."); the bags have no lives to narrate.

## 3. About-page story block (Jessica's voice — the anchor)

> **SUPERSEDED 2026-07-22:** the block below is now the closing beat of the full founder story in `Jessica-Founder-Story.md` — use that document's §3 as the About-page copy.

> **Why our bags have names**
>
> I don't design for a market. I design for one woman at a time. She has a life, a schedule, somewhere to be — and by the time a bag is finished, I know her name.
>
> Margot. Camille. Eleanor. Sofia.
>
> You'll recognize them. You might be one of them.
>
> You're probably all four.
>
> — Jessica

That last line IS the multi-bag mechanic (Vestirsi's one-woman-many-moments engine) in one sentence.

**Guardrails honored:** persona-anchored, zero origin claims (no place names, no "atelier" additions); women are openly muses, never claimed real customers; no competitor references.

## 4. Collection page

All-bags collection cards show the name only — no epithet subtitle:
`The Margot` / `The Camille` / `The Eleanor` / `The Sofia`

## 5. Omnisend rollout series ("Meet the Women")

Fluid-width HTML convention per `reference_omnisend_velantra_campaigns`. Weekly cadence:

1. **"Our bags have names now"** — the founder letter (About block), all four names introduced, no hard sell. Pure brand equity send.
2. **"Meet the Sofia"** — name only, summer styling on the bag itself + PDP (lead with the hero, in season now). Show the bag in summer, don't narrate Sofia's summer.
3. **"Meet the Margot"** — name only, desk-to-dinner styling + PDP.
4. **"Meet the Camille"** — name only, everyday utility + colorway spread + PDP.
5. **"Meet the Eleanor"** — name only, what-fits / packing demo + PDP.

Timing caution: Straw Tote delay-notice campaign is in flight — Email 1 must not read as a shipping update; keep it clearly brand-story. Suppress the open-delay-ticket segment from Email 2 if needed.

## 6. Ads posture (nothing breaks)

- **TOF unchanged:** hooks stay category/avatar language ("this straw tote…", boatkin hooks). Names are a brand layer, not a hook.
- **PDP congruence:** ad says "straw tote" → PDP title still contains "Woven Straw Tote." ✓
- **MOF/BOF + retargeting:** names become the payoff ("Everyone's asking about the Sofia").
- Google Ads search campaigns unaffected (descriptors keep keyword relevance).

## 7. Execution checklist (on go)

1. Shopify Admin API (client creds in `.env`): update 4 product titles; update SEO title/meta description keeping category terms first ("Woven Straw Tote | The Sofia | Velantra"; Meridian keeps "Meridian" in SEO meta for one transition month).
2. Prepend vignette block to each PDP description (body_html top), leave craft copy intact.
3. Add "Why our bags have names" section to About page.
4. Collection card subtitles (theme/metafield depending on Shrine setup).
5. Build 5-email Omnisend series (drafts for approval before send).
6. Internal: skill registry keys UNCHANGED (`strato`, `boat-tote`, `weekender`, meridian); update display-name lines in velantra product skills + memory.
7. Future products enter via "Meet ___" launches (Portia, Rosalie, Lola per full-system doc).
