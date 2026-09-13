# Concept-specific B-roll skills — TrendTrack study

Completed September 10, 2026. Five installed skills now separate presenter VSL, podcast, skeleton, animated and AI-voiceover scene selection. Each requires an explanation of **why this scene belongs at this spoken cue**, a concept-matched asset brief, selection/QA and the appropriate editing-plan handoff.

## What was pulled and how it was selected

Used the authenticated TrendTrack MCP at `https://api.trendtrack.io/v1/mcp` through the workspace’s existing client. Retrieved live `search_ads` results and `scan_ad` creative-collation details. Requests and exact responses are saved in [raw](raw/); the reusable request runner is [research.py](research.py). Credentials are not copied into this report or the skills.

Discovery combined active English video searches sorted by reach, seven-day growth and duplicates; format-keyword searches; health-topic searches; Shopify-filtered discovery; and domain searches for Alevia, Lymphoria, Nuora, Nivara, Resilia, Sculptique and Avaroot. The API has no verified visual-concept classifier. “Skeleton” retrieved watches, “animation” retrieved classes and “podcast” included UGC; therefore actual media, not search text, determined the categories. A tested `spender: brandtracker` query did not reliably limit results to the tracked-brand list and is not treated as account-scoped evidence.

The consolidated visual-screening pool contains **203 deduplicated candidates** from the relevant discovery queries, not every response or the entire TrendTrack library. All nine discovery thumbnail sheets were visually screened. Fifteen downloaded sources received overview inspection; eleven received deeper visual analysis. Selection prioritized a real format match, then reported reach and supporting growth/longevity/reuse, while retaining contrasting visual approaches. This is a curated study of strong-reach and durable examples within the searched set, not a statistically complete leaderboard or verified conversion ranking.

## Selected references and performance signals

Figures below are TrendTrack search snapshots for the selected creative. They are not measured sales, ROAS or proof of causal creative lift. Ads are grouped by visual relevance, then generally by reported reach. Direct media links accompany each selected ad. Scan member counts are recorded separately because search duplicate counts and collation membership do not always match.

| Concept / reference | Advertiser | Reported reach | Days running | Scan members / active | Media and analysis |
|---|---|---:|---:|---:|---|
| HeyGen-compatible · C101 | Traditional Remedies | 358,078 | 37 | 10 / 2 | [Video](https://medias.trendtrack.io/facebook/video/6e9adab9e5f2f7c5f24e56d4e5503eecb77100e21b302c75335dcd294158147c.mp4) · [Analysis](analyses/C101.md) |
| HeyGen-compatible · C061 | Women's Wellness Daily | 313,996 | 120 | 9 / 2 | [Video](https://medias.trendtrack.io/facebook/video/a1c29dccc96a29c8e8c4aa014c1490313bf02bfaa12653541bcfca4e8fa07913.mp4) · [Analysis](analyses/C061.md) |
| Podcast, speaker-led · C067 | Nivara | 36,114 | 232 | 11 / 3 | [Video](https://medias.trendtrack.io/facebook/video/f787d7b676439d729a5f32701f4e815ef9088f0d043806c71dd6ed12754ff736.mp4) · [Analysis](analyses/C067.md) |
| Podcast, covered answers · C183 | Paw Guardian | 23,767 | 197 | 3 / 2 | [Video](https://medias.trendtrack.io/facebook/video/275147b1a52dd8a3aac40ae6d0b4249c2ff371a87d78c8bc1bff20db4283210f.mp4) · [Analysis](analyses/C183.md) |
| Skeleton/translucent hybrid · C133 | IM8 Health | 2,979,025 | 83 | 15 / 3 | [Video](https://medias.trendtrack.io/facebook/video/f9ad5e5bf72709aa4511d21554d9fd54ad1da318160536bd59c93a2df428815d.mp4) · [Analysis](analyses/C133.md) |
| Skeleton comparison · C090 | Circulatory Health Report | 47,102 | 7 | 1 / 1 | [Video](https://medias.trendtrack.io/facebook/video/0b4adc9b34f8db5aee9838ffee6d9c2509ee9da350d64ca09ed912ebdb5b821c.mp4) · [Analysis](analyses/C090.md) |
| Skeleton laboratory guide · C091 | Resilia | 42,140 | 35 | 2 / 1 | [Video](https://medias.trendtrack.io/facebook/video/7cb673ab2791905c9c21018a4d98abb329fadaf084569b4e117fe847c1c62820.mp4) · [Analysis](analyses/C091.md) |
| 3D animated / voiceover-led · C194 | Ankhway | 7,031,839 | 148 | 11 / 1 | [Video](https://medias.trendtrack.io/facebook/video/6c697fa4cad634f1bac4e023906c8a6254c63d48ede9f94d967edc091dc6cfa2.mp4) · [Analysis](analyses/C194.md) |
| 2D animated · C131 | Dog Gut Health Guide | 977,480 | 15 | 2 / 2 | [Video](https://medias.trendtrack.io/facebook/video/02feff889bbf75dd59d44eb3acc03a6fd73c86953f76003273b3f02931b15d5c.mp4) · [Analysis](analyses/C131.md) |
| Faceless demonstration · C198 | The Comfort Lab | 4,538,782 | 62 | 3 / 1 | [Video](https://medias.trendtrack.io/facebook/video/6b19783f78e155df20f6eff02cc93a214b5e4bcdf559626083559d643e667350.mp4) · [Analysis](analyses/C198.md) |
| Presenter/montage hybrid · C130 | Dog Gut Health Guide | 3,284,560 | 59 | 4 / 1 | [Video](https://medias.trendtrack.io/facebook/video/980741dcb69a2cfaf6a8cefb88ed826eca74cc386e145cf873578a16717b60f1.mp4) · [Analysis](analyses/C130.md) |

### Limits that affect the ranking

- **Podcast:** the two confirmed podcast sources have modest reported reach. Their value here is 197–232 days of running and distinct conversational coverage. They are durable format examples; this pull does not establish them as current top-scaling podcast winners.
- **HeyGen and AI voice:** these labels describe transferable target formats. The original rendering provider and whether narration is AI-generated are unverified. C130 is visibly a presenter/montage hybrid; C198 is a filmed physical demonstration. The faceless visual decisions can be used with an AI voice without relabeling the reference’s origin.
- **Growth inconsistencies:** C194 reports seven-day delta 5,657,229 while its 30-day delta is 4,519; C130 reports 958,854 versus 4,526. Several histories contain resets/decreases or represent a different scope from aggregate creative reach. C061’s scan says “improving” but its supplied history ends August 7 and its search seven-day delta is zero. C101’s supplied history ends August 30. These fields cannot support a clean September 10 acceleration ranking. Raw records remain intact; automatic “scaling hard” verdicts were not treated as validated conclusions.
- **Comparatively interpretable fresh signals:** C131 reports 672,250 seven-day growth on 977,480 reach and 15 days running; C090 reports 46,576 on 47,102 reach and seven days. These support selection as recent activity examples, while remaining reported proxies.
- **Claims and provenance:** visual analysis does not validate medical claims, professional credentials, genuine testimonials, asset reuse rights or conversion performance.

## What the five skills learned

| Skill | Distinctive scene decisions | Observed contrast |
|---|---|---|
| HeyGen VSL | Protect direct address; use small inserts for identification, full frames for actions or complex processes; return for interpretation | C061 keeps small examples over one speaker; C101 uses extensive human/science coverage early and a long speaker-led closing |
| Podcast | Preserve question, answer opening and reaction; place useful inserts within the answer, then return to the right participant | C067 has no separate B-roll in the full dense sample sequence; C183 demonstrates substantial coverage without losing the exchange |
| Skeleton | Choose comparison actors, lab guide or translucent lifestyle; vary actions and anatomical scale while preserving identities | C090 acts out two paths, C091 stages a laboratory guide, C133 bridges illustrated anatomy to human product use |
| Animated | Match the exact visual world; let characters show relationship costs and payoffs; give mechanism elements distinct actions | C131 is a 2D emotional dog/owner story; C194 uses 3D domestic scenes and ingredient characters inside the body |
| AI voiceover VSL | Choose montage, sustained physical demonstration, protagonist or animation based on the argument; audio origin does not choose the medium | C198 teaches with model/chart/product; C130 supplies hybrid montage/analogy examples; C194 supplies an animated voiceover structure |

## Visual audit and scope

The eleven analyzed sources were decoded in full for sampling and candidate detection. Decoding is not manual review. Six received visual review of every half-second sample sheet across their duration; five received overview plus selected dense sections. All eleven also received a manually inspected eight-consecutive-frame window around a selected event. Nine windows confirm hard cuts, one confirms an inset onset with possible delivery splice, and one rejects a detector candidate as continuous camera movement. The study does not claim that every source frame or every cut was manually inspected.

| Reference | Decoded source frames | Visually reviewed dense frames | Coverage |
|---|---:|---:|---|
| C101 | 5,257 | 440 | Full-duration half-second samples · [Manifest](media/C101/review-scope.json) |
| C061 | 4,811 | 108 | Selected half-second spans; see manifest · [Manifest](media/C061/review-scope.json) |
| C067 | 2,599 | 175 | Full-duration half-second samples · [Manifest](media/C067/review-scope.json) |
| C183 | 5,853 | 108 | Selected half-second spans; see manifest · [Manifest](media/C183/review-scope.json) |
| C133 | 2,361 | 190 | Full-duration half-second samples · [Manifest](media/C133/review-scope.json) |
| C090 | 4,477 | 84 | Selected half-second spans; see manifest · [Manifest](media/C090/review-scope.json) |
| C091 | 3,348 | 108 | Selected half-second spans; see manifest · [Manifest](media/C091/review-scope.json) |
| C194 | 2,840 | 191 | Full-duration half-second samples · [Manifest](media/C194/review-scope.json) |
| C131 | 1,949 | 131 | Full-duration half-second samples · [Manifest](media/C131/review-scope.json) |
| C198 | 3,957 | 265 | Full-duration half-second samples · [Manifest](media/C198/review-scope.json) |
| C130 | 6,585 | 144 | Selected half-second spans; see manifest · [Manifest](media/C130/review-scope.json) |

Totals: 44,037 decoded frames; 1,944 visually reviewed dense samples, plus overview images and 88 consecutive-frame event images (overlap possible). [Selected event evidence](selected-events.json); [sheet 1](selected-events-1.jpg); [sheet 2](selected-events-2.jpg). Unreviewed automated candidate sheets are not accepted shot lists.

Source-clock narrative windows in the analyses are approximate, except the explicitly verified zero-based frame events. Audio was not auditioned; mapping uses visible captions and available machine transcripts. C130/C183 missing transcripts were generated locally with cached Whisper; other machine transcripts came from the saved MCP data. Transcript errors, including a likely erroneous tail in C133, are not treated as heard speech. This is B-roll research, not an audio/editing-style certification.

The fifteen overview sources also included C145 (presenter, plateau), C181 (UGC, rejected as podcast), C193 (another animated Ankhway source) and C021 (long animated Lymphoria source). They were not promoted to detailed examples without deeper review.

## Installed skills

- [broll-heygen-vsl](/Users/brooksorradre2/.codex/skills/broll-heygen-vsl/SKILL.md)
- [broll-podcast](/Users/brooksorradre2/.codex/skills/broll-podcast/SKILL.md)
- [broll-skeleton-ads](/Users/brooksorradre2/.codex/skills/broll-skeleton-ads/SKILL.md)
- [broll-animated-ads](/Users/brooksorradre2/.codex/skills/broll-animated-ads/SKILL.md)
- [broll-ai-voiceover-vsl](/Users/brooksorradre2/.codex/skills/broll-ai-voiceover-vsl/SKILL.md)

All five are installed in the canonical Codex skills directory and linked into this workspace’s `.claude/skills` and `.agents/skills`. The existing B-roll skill routes to them; the existing editing-style skill remains the companion for cuts, transitions, zooms, captions, sound and pacing. Instructions preserve GPT Image 2, Google Omni, DaVinci Resolve, editing-plan-first and Cut Room delivery requirements.

Validation checks frontmatter, skill names, UI metadata, linked resources and workspace discovery links. This establishes installation and internal consistency, not proven future creative performance. Future references must be inspected afresh; these source examples supply range rather than replacing the new brief.
