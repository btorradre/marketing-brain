# Research basis and boundaries

Latest expansion: the [September 7 Nuora study](nuora-study/NUORA-ANALYSIS.md) adds 158 previously absent exact texts. The combined corpus contains 392 transcripts and 79 case entries covering 77 distinct texts. The counts below describe the original September 6 study unless stated otherwise. Nuora’s wider fetch covered 170 completed grouped texts; all openings and 30 full transcripts were qualitatively reviewed.

## Provenance

Study date: September 6, 2026. Source: the user’s TrendTrack workspace, starting with Nivara Official and covering all 29 tracked entries. The retrieval produced 248 grouped transcript rows, representing 233 distinct full texts within brands. The curated library contains 49 cases. Seventeen videos were downloaded and inspected at five sampled frames each, alongside thumbnail review.

These counts include short promotions, music, animation, and other formats as well as VSLs. The study was not an exhaustive review of every ad. Sampled frames identify visible presentation; they do not establish speaker identity, synthesized voice, AI production origin, or every moment of a video. Transcripts can contain recognition and punctuation errors. Do not derive universal sentence-length or connective-frequency targets from their punctuation.

The original workspace artifacts are under `_engine/research/trendtrack-ai-ugc-vsls-2026-09-06/`: `AI-UGC-VSL-BREAKDOWN.md`, `evidence-gallery.html`, `evidence-index.json`, and `coverage.json`. The packaged copy of the report is `AI-UGC-VSL-BREAKDOWN.md` beside this file, with `evidence-index.json` and `coverage.json`. Read `case-index.md` for case analysis and full transcript links; `corpus-manifest.json` accounts for the 233 grouped transcripts and one supplemental current-video transcript. No API connection is required.

## Evidence-to-instruction map

The observations below describe advertising rhetoric. The corresponding writing rules are editorial deductions, not results from controlled conversion experiments. None of the ads establishes product efficacy for a new brief.

| Source case | Observed pattern | Transferable writing decision |
|---|---|---|
| [N1: Nivara Official](https://medias.trendtrack.io/facebook/video/3c3c896737b5d685679c120591222b331087138f58067ff7da3188aa71b3737c.mp4) | Feature jobs and buying criteria precede the recommendation. Explanatory sentences alternate with brief verdicts. | Teach the relevant job before asking the listener to value an ingredient; keep the explanation and the brand distinct. |
| [L1: Lanural](https://medias.trendtrack.io/facebook/video/6ad933ea2e8ba3700a0bb235798ee914de6d9d1d352daf293022c00895aefe5b.mp4) | A claimed obstacle is followed by a proposed ingredient role and a manufacturing distinction. | Include a specification only when its supported role changes product selection; avoid decorative science. |
| [L2: Lanural](https://medias.trendtrack.io/facebook/video/08857a6140dc6cbe3bc76a67b04418178d1779cab7c325cc65fab237bad07e2a.mp4) | The customer story begins with a specific unresolved sensation and closes on the corresponding daily relief. | Use recognizable experience and return to the opening activity; keep the explanation within the narrator’s knowledge. |
| [G1: GLP-1 SOS Supplements](https://medias.trendtrack.io/facebook/video/cd3a136d451aea5720807cc27e979bd071ccc3fa8e466442b159ce340c3a862a.mp4) | Failed purchases and unwanted trade-offs create the question the mechanism answers. | Explain the particular gap in past attempts instead of merely declaring alternatives ineffective. |
| [Z1: blog.zafiraorganics.com](https://medias.trendtrack.io/facebook/video/252f5ee4de546a6d55af86ab5ec0861fad85c76d8678c37a3af3b79dd3bc0df0.mp4) | A long explanatory script uses linked questions and a recurring physical analogy. | Length must earn attention through new necessary understanding; maintain one literal mapping for the analogy. |
| [C1: CAVAÉ](https://medias.trendtrack.io/facebook/video/ac7d777bed86c7d00e42e5f1f5b438b81f9789e31c2b6babce115a4da025d0e9.mp4) | The ad makes delivery route the reason the product differs. | The product rationale may be delivery or construction; it does not have to be a new ingredient. Advertising coherence is not clinical validation. |
| [R2: Resilia](https://medias.trendtrack.io/facebook/video/5160c28a5c21807b9db173a0c0c86cb11d8ecae2c678f7b698278a1b85f7786e.mp4) | The brand appears near the beginning of the transcript. | A product-first structure is valid when the question concerns the product; late introduction is not universal. |
| [E1: Elvera](https://medias.trendtrack.io/facebook/video/7386699790306cb8d2e48c0b9e67b4888f4583c8eb18703ea3cadf83c8d35ec2.mp4) | A specific daily scene leads to an early product reveal and subsequent explanation. | Product entry can precede detailed education if the script establishes relevance and continues the argument. |
| [U3: Nuora](https://medias.trendtrack.io/facebook/video/7f26217be952be3cbf9d556bfda44518cb8a88683fdcaabf3e7b31309c3a992f.mp4) | Interview questions follow the explanation into audience objections and product selection. | Use dialogue to ask the next unresolved question, not to distribute a monologue between speakers. |
| [B1: go.blymeskinsystems.com](https://medias.trendtrack.io/facebook/video/3cdf52ac842ce2b54cf727836eaa5e68dd5b9397b9603c634d3b0b4e8ea656ee.mp4) | The creative sells an information-seeking next click rather than completing a named-product pitch. | Match explanation and CTA to the destination; do not force a purchase close onto an article bridge. |

## What was observed versus what this skill adds

**Observed across selected examples:** explanations of prior failure, plain-language analogies, ingredient or feature roles, criteria-to-product bridges, everyday outcome scenes, different narrator modes, and both early and late brand entry. Related scripts and repeated texts were observed; the brands’ internal testing procedures were not.

**Editorial tools added by this skill:** the four explanation questions, stopping rule, main-proposition sentence check, before-and-after exercises, and semantic review rubric. These make the patterns usable for drafting. They are not measured formulas for conversion or mandatory features of every successful VSL. The workshop examples are original fictional exercises, not transcript quotations. The added hook/psychology mappings and case annotations are also editorial interpretations, not measured psychological or conversion effects.

A sentence may appropriately be longer to preserve cause and immediate consequence. Another may need to be shorter to land the implication. The study supports coherent thought progression; it does not justify a fixed percentage of connective-led sentences, a compulsory 23-beat script, a universal brand-reveal timestamp, or a forced biology lesson for every product.

## Performance and factual limits

Grouped reuse and longest observed run are deployment proxies. They do not establish spend, revenue, ROAS, profit, or that the script caused scaling. Ten individual-ad scans added status context: several representative ads were inactive; two long-running active examples were flagged as plateaued; another lacked sufficient performance history. Stronger longevity for one ad must not be assigned to another ad from the same brand.

First spoken-brand position was measured as a fraction of transcript words where available. It is not a video timestamp and does not locate the first visible product appearance. N1 was about 84% through its words, E1 about 23%, and R2 about 2%; this contrast motivates flexible ordering, not any of those percentages as a target.

Medical explanations, testimonials, exact outcomes, studies, credentials, and scarcity statements were not independently substantiated. Nivara and CAVAÉ offer different commercially coherent explanations for similar frustrations; this is a reason to separate rhetoric from evidence. A new product script needs its own factual basis. Borrow structure, not an unsupported premise or a competitor’s personal story.
