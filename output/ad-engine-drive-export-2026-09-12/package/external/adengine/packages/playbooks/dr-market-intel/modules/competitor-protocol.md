# Competitor protocol — find the gap, never the copy

The gap between what the market wants and what category advertising currently offers is where the best-performing creative lives. This protocol locates that gap precisely enough to brief from.

## Operating rules

1. **Study the angle, not the execution.** Format, editing, and production quality are irrelevant here. The core message is the only thing that matters. A beautifully shot ad running one week is worth less than an ugly one running six months.
2. **Running time is the signal.** An ad live 90+ days is a proven winner and gets treated as evidence. Record the first-seen date on every ad, and note when the library only shows a range.
3. **Category patterns reveal category gaps.** When every competitor says the same thing, the first brand to say something different owns that position by default.
4. **Never recommend copying.** The output is differentiation, not replication. See Law 6.
5. **Map to awareness levels.** Most category advertising clusters at one or two levels, and that clustering shows exactly where the opening is.

## Pulling real ads

TrendTrack is connected, so work from live data rather than from category memory:

| Need | Tool |
|---|---|
| Find advertisers in a category | `mcp__claude_ai_TrendTrack__search_advertisers` |
| Pull their running ads | `mcp__claude_ai_TrendTrack__search_ads` |
| Ads currently scaling | `mcp__claude_ai_TrendTrack__get_brandtracker_scaling_ads` |
| Video ad transcripts | `mcp__claude_ai_TrendTrack__get_brandtracker_transcripts` |
| One-shot competitor brief | `mcp__claude_ai_TrendTrack__brief_competitor` |
| What changed on a tracked brand | `mcp__claude_ai_TrendTrack__analyze_brand_changes` |
| Their email program | `mcp__claude_ai_TrendTrack__search_emails`, `analyze_shop_emails` |

Check `mcp__claude_ai_TrendTrack__check_credits` before a large sweep. For a video ad worth a real teardown, run the `ad-watcher` skill on it rather than working from the transcript alone.

Record every ad's identifier and first-seen date. An analysis that cannot be re-verified in the library is not intelligence.

## Output sections

### SECTION 1 — CATEGORY ANGLE MAP

For each competitor ad:

- Competitor name and ad identifier
- **Core angle**: the single idea the ad is built around, one sentence
- **Awareness level**
- **Hook type**: problem naming / failed solution / transformation / social proof / direct offer
- **Creative maturity**: fresh angle, or repeated for years?
- **Running time** and first-seen date

### SECTION 2 — CATEGORY PATTERNS

- What angle does every competitor share?
- What awareness level is the entire category clustering at?
- What messaging has gone invisible through repetition? (Cross-check `_engine/frameworks/fundamentals/angle-saturation-map.md`.)
- What customer desire is the category consistently failing to address? Answer this against the VoC index, not against intuition. A gap the customers do not care about is not a gap.

### SECTION 3 — GAP ANALYSIS

3 to 5 clear gaps nobody is running. For each:

- What the gap is
- Why it exists (usually: the category cannot make the claim, or has not noticed the desire, or finds the angle unglamorous)
- The brief direction it points to
- One example hook that would own it

Each gap must survive the swap test before it is listed. A gap only we can fill is a position. A gap anyone could fill is a trend.

### SECTION 4 — DIFFERENTIATION STRATEGY

The single most defensible creative position for this brand:

- The position in one sentence
- The awareness level to target first
- The hook that signals the position immediately
- Why it is hard for competitors to replicate quickly

"Hard to replicate" means grounded in something structural: our actual physical product facts, our price-to-quality reality, our founder, our manufacturing truth. A position built only on a phrase gets copied in three weeks.

## The Law 6 gate, restated

Everything in this document is input. None of it is copy.

For Velantra, the output of this protocol may never become an ad that mentions, implies, or price-compares against another brand. Translate every gap into a positive claim built from our own physical facts before it reaches `dr-angle-bank`, and set `brand_law_check: flagged:competitor-comparison` on any record that cannot survive that translation.

The one carve-out is a format that IS a comparison (a ranked roundup, "I tested five bags"). Inside it: Hermes and "Birkin" stay out entirely, every competitor is treated as genuinely excellent and given a trade-off rather than a defect, and no competitor price is quoted unless it was verified on that brand's own site.
