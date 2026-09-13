# 2026-05-09 — Branded Statics Scrape (Saturday Discovery)

**Run type:** Saturday discovery day — hunting net-new health/supplement brands running polished branded statics
**Operator:** market-analyst (scheduled task)
**Chrome status:** Stable. One initial connection blip recovered with fresh tab. No crashes.

---

## Brands Scanned

| Brand | Domain | Verdict | New folder? |
|---|---|---|---|
| Bloom & Bond | bloomandbonds.com | **Does not qualify** — native/UGC only | Yes (logged for native_ads track) |
| Nuvara / Sophie's Natural Health Guide | nuvarawellness.com, sophiesnaturalhealthguide.com | **Qualifies** — clinical illustration + before/after | Yes |
| Provitalean | rejuveen.com | **Marginal** — 2 of 8 ads qualify (X-ray + before/after) | Yes |

---

## Images Downloaded

**None this session.** Image URL extraction was blocked — Meta's CDN gates direct image src access in the Ad Library viewer (URLs returned scrubbed / cookie-data placeholders rather than fetchable URLs). Browser tool screenshot save_to_disk also did not surface files into the mounted workspace from this Cowork environment.

**Mitigation:** Library IDs are recorded in each brand's catalog.md so the assets can be re-pulled by direct ad-detail URL when image fetch is unblocked, OR a manual operator pass can resolve them in a follow-up session.

This is a known browser-environment limitation in the current scheduled-task setup — flagging for engineering follow-up.

---

## Design Trends Spotted

### 1. The "Anti-GLP-1 Damage" Wave Is Saturating
Three of three discovery brands (Bloom & Bond, Nuvara, Provitalean) are running **GLP-1-side-effect** angles — hair loss, post-stop rebound, "the REAL shock 6 months after stopping." This is no longer an emerging angle; it's a category. The differentiator is now the *visual archetype* used to sell the angle, not the angle itself.

### 2. Clinical Illustration Is Re-Emerging
Both Nuvara (split-panel follicle cross-section) and Provitalean (X-ray torso) are leading with **rendered medical-illustration imagery** rather than photography. This is a notable swing — most of the supplement vertical has been UGC-dominant for 18+ months. Looks like operators are testing pattern-interrupts against feed fatigue.

### 3. Native-Voiced Persona Pages Are the New Storefront
Nuvara runs ads under "Sophie's Natural Health Guide" (a persona/influencer-style page name) instead of "Nuvara" directly. Provitalean runs under "Sarah Collins" and "Menopause And Me." The branded supplement page is becoming the *destination*, not the *publisher*. Page-name-as-character is a deliberate trust play — it lets the ad read as authority-friend POV, not branded promo.

### 4. Bloom & Bond Confirms The Native-Image Saturation
~330 active ads, all native/UGC. They've doubled down on the native track and are clearly winning on volume. Worth a separate native-track catalog entry — they're a textbook study in native-image volume play.

---

## Template Recommendations

### Top Recommendation: Lunessa "Receptor Cross-Section" Static
Steal Nuvara's split-panel follicle illustration archetype and adapt for Lunessa. Render a cross-section of an estrogen receptor or hot-flash neural pathway — left panel "what menopause does," right panel "what Lunessa does." This is archetype #7 (Medical/Clinical Proof) and it's an open lane in the menopause vertical (most competitors are running lifestyle photos or before/afters).

### Secondary: Motilli "X-Ray Pattern Interrupt"
Provitalean's color X-ray torso with red-highlight overlay is a strong feed-stopper. Motilli could run a stomach/gut variant with the same pseudo-clinical register. Strong odds of high CTR off pure pattern-interrupt against UGC feed.

### Skip: Bloom & Bond template lift
Native-only. Nothing to template here for the statics archive — but the hook line "GLP-1 gave you your body back. Then it took your hair." is worth recording in the hook swipe file, separately.

---

## Catalog Entries Created

- `/statics/branded_statics/nuvara/catalog.md`
- `/statics/branded_statics/provitalean/catalog.md`
- `/statics/branded_statics/bloom_and_bond/catalog.md` (with non-qualifying verdict)

---

## Chrome Issues

- One initial browser-connection blip on first navigate (recovered with fresh tab).
- One "tab no longer exists" event during the first navigation attempt.
- One 180s timeout during a click attempt that opened the ad-detail modal — recovered, no crash.
- Image fetch via JS DOM evaluation returned scrubbed URLs (FB-side cookie/auth gating).

---

## Next Run Recommendations

1. **Tomorrow (Sun):** Re-scrape Tier 1 — Neurosmile, GLP-1 SOS, Auri Labs — these have weekly velocity worth tracking.
2. **Next discovery day:** Search keywords *"Tirzepatide alternative"*, *"natural Ozempic"*, *"Wegovy companion"* — same vein, fresh brands likely.
3. **Image fetch follow-up:** Investigate using the direct Ad Library Library ID URL pattern (https://www.facebook.com/ads/library/?id={LIBRARY_ID}) which sometimes exposes a different DOM that allows image fetch. Worth a 10-min experiment in the next run.
