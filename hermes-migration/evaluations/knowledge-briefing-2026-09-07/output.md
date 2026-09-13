Loaded and used the installed knowledge base. I verified the inventory, exercised find_swipes.py, and read 22 distinct full transcripts plus their case analyses. The remaining corpus stays available for task-specific retrieval.

1. Verified inventory

Recounted from corpus-manifest.json, transcripts.jsonl, cases.json, patterns.json, and the original Nuora research data:

- 392 exact within-brand transcript texts in the combined library.
- 171 Nuora texts within that library.
- 23 reusable pattern families.
- 79 case entries covering 77 distinct transcripts. U1/NU001 and U2/NU002 are duplicate case coverage, not additional texts.
- September 7 Nuora fetch: 170 exact texts, representing 168 normalized word sequences and 47,101 words.
- That fetch overlaps 12 previously held texts and adds 158. One earlier, separately retrieved interview—U3—is absent from the grouped fetch. Thus: 13 previously held Nuora texts plus 158 additions gives 171.

Review coverage is different from inventory:
- The Nuora study records all 170 openings reviewed, but only 30 full qualitative reviews; 140 remain opening-only reviews.
- Its 24 execution families classify that Nuora fetch. They are not the same taxonomy as the specialist’s 23 transferable patterns.
- The original cross-brand study selected 49 cases; the expansion added 30 case entries.
- Nine Nuora entries are nondeveloped audio, fragments, or music—not developed VSL examples.

All 392 packaged transcript files matched their indexed text and SHA-256 hashes. Case-analysis files were present. Manifest-listed original source hashes also matched. Shared and original Nuora analysis, index, coverage, family assignments, and variant comparisons were identical.

None of this establishes conversion performance. Reuse and longevity show deployment, not profitable scale or causation.

2. Full sources actually read

For compact, exact citations below:

S = /opt/vault/agents/hermes/shared-skills/ai-ugc-vsl-swipe-copywriting/references
N = /opt/vault/marketing-brain/_engine/research/nuora-trendtrack-2026-09-07

Cross-brand full transcripts read, all under S/transcripts/:

| Case | Source filename |
|---|---|
| N1 | T-f63943a7-8f4c227c71bb.txt |
| N5 | T-f63943a7-6fac9c2312d2.txt |
| L2 | T-fcc41353-47c031132b12.txt |
| G2 | T-9e7b452e-69ab344fe3ee.txt |
| Z2 | T-eadeca8f-eb68b5d5c02f.txt |
| U3 | T-8bff2239-7662abfd77d1.txt |
| A2 | T-f1578708-32664b8dc867.txt |
| R2 | T-122358d6-8371488673bf.txt |
| F4 | T-e5e46883-28d0167aab19.txt |
| F1 | T-3d94c275-67a2257931c7.txt |
| B1 | T-1b605f19-f0f71ac58fc9.txt |

Original Nuora full transcripts read:
N/transcripts/NU001.txt, NU002.txt, NU012.txt, NU046.txt, NU048.txt, NU069.txt, NU117.txt, NU121.txt, NU129.txt, NU136.txt, and NU141.txt.

Each case’s analysis was also read at S/cases/<case-ID>.md. These are 22 distinct texts totaling 7,221 words—not a claim to have qualitatively reviewed all 392.

3. Most useful frameworks

“Strongest” here means most useful structurally for the appropriate buying question—not proven highest-converting.

A. Recognition → explanation → buying criteria
Fits: problem-aware viewers whose recurring experience remains unexplained.
Question: “Why does this keep happening, and what should a credible solution do?”
Sequence: precise situation → acknowledge effort → supported explanation of the gap → required actions → feature jobs → product match → relevant proof → next action.
Nuora often adds a second question: not just “why this ingredient?” but “why this specification or combination?”
Sources: N1 and NU136; S/cases/N1.md and N/transcripts/NU136.txt.
Boundary: transfer the dependency, not their diagnoses, biological barriers, or attacks on medical advice.

B. Failed attempts → preserve the gain
Fits: skeptical buyers who want a problem resolved without sacrificing something valuable.
Question: “Can I keep what is working without accepting this trade-off?”
Sequence: valued gain → unwanted cost → relevant unsuccessful attempts → supported distinction → product fit → evidence for both sides → return to the valued activity.
Sources: G2, Z2, F1; their full paths are listed above.
The same structure spans medication-related advertising and capacity-versus-appearance bag advertising. Medical compatibility cannot be inferred from that structural similarity.

C. Buying guide / inspection
Fits: solution-aware shoppers comparing options.
Question: “What should I check before buying?”
Sequence: inspection task → meaningful criterion → why it matters → product meets criterion → evidence → purchase action.
Sources: N5; N/transcripts/NU048.txt.
Teach a useful test, not an arbitrary specification chosen merely because our product has it. “Only brand” and superiority claims require independent support.

D. Customer discovery
Fits: viewers wondering whether another purchase could genuinely differ from previous attempts.
Question: “Why would this attempt be different?”
Sequence: specific difficulty → relevant attempts → documented discovery → understandable explanation → selection reason → supported experience → resolution of the opening situation.
Sources: L2 and Z2; S/cases/L2.md and S/cases/Z2.md.
L2’s useful move is closing on the exact sensation introduced—not generic wellness. Without a real customer account, use a transparent demonstrator or hypothetical scenario, not invented testimony.

E. Objection dialogue / characters explaining jobs
Fits: several connected questions, especially suitability and comparison.
Question: “But why does that apply to my situation?”
Sequence: question → answer → natural follow-up → criterion → product role → remaining objection → routine/action.
Sources: U3; N/transcripts/NU129.txt and NU001.txt.
NU001 assigns a job to each ingredient-character; NU129 lets alternatives voice objections. This may aid comprehension, but dialogue and animation do not relax claim standards.

F. Founder decision story
Fits: a seller-trust gap.
Question: “Why did you build this particular product?”
Sequence: real motive → unmet requirement → actual design decisions → evidence → product → practical invitation.
Source: A2; S/cases/A2.md.
The transferable element is the connection between motive and design choices. Founder sincerity is not efficacy proof.

G. Product-aware demonstration / review
Fits: viewers already interested in the product or category.
Question: “Does its function or quality justify choosing it?”
Sequence: product or observable challenge → inspection/demo → relevant explanation → supported conclusion → action.
Sources: F4, F1, R2.
F4 asks the viewer to compare bags; R2 names the product immediately. A late reveal is optional. A reverse-warning hook needs a truthful qualification, not a fabricated complaint.

H. Price concession → specification
Fits: price-aware buyers.
Question: “Why does it cost this much?”
Sequence: concede actual price → explain real design trade-offs → connect features to meaningful jobs → evidence → accurate terms → action.
Source: N/transcripts/NU121.txt.
The hypothesis is that candor plus a concrete value explanation reduces distrust. An admission does not validate the remaining claims.

I. Two separate trust arguments
Category skepticism: acknowledge the specific ad-fatigue concern → explain a relevant distinction → substantiate it → recommendation.
Source: N/transcripts/NU069.txt.

Seller authenticity: acknowledge a genuine channel question → demonstrate verifiable identifiers → identify the authorized destination → purchase action.
Source: N/transcripts/NU012.txt.

Do not collapse these into one “skeptic hook.” Doubting efficacy is not evidence of buying a counterfeit, and an official seller does not prove efficacy.

J. Offer-first / reason-why offer
Fits: warm buyers whose obstacle is current terms or timing.
Question: “What changed, and why act now?”
Sequence: verified event or qualification → actual offer → brief relevance/proof → terms → action.
Sources: N/transcripts/NU002.txt and NU117.txt.
The apology-to-discount reveal and warehouse-event story are observed devices. Neither authorizes invented discounts, stock, incidents, or deadlines. A visible link is not inventory evidence.

K. Staged progress / restored participation
Fits: questions about actual use and what improvement would mean.
Sequence: documented expectations → supported milestones and uncertainty → ordinary valued activity → next step.
Sources: Z2; N/transcripts/NU141.txt and NU046.txt.
Use timelines only when substantiated. Never reinterpret worsening symptoms as proof that a supplement works. A concession about exaggeration does not make an exaggerated benefit acceptable.

L. Article bridge
Fits: an information-seeking destination rather than immediate purchase.
Question: “Is this explanation worth reading?”
Sequence: recognition → useful partial answer → exact information promised by the article → why it matters → article CTA.
Source: B1; S/cases/B1.md.
Transfer the destination-specific structure, not its purported encounter, age comparisons, or transformation.

4. Hooks, psychology, proof, and transitions

The practical hook shortlist:

- Recognition: name the unresolved moment.
- Failed attempts: explain the shared gap rather than declaring everything ineffective.
- Preserve the gain: identify what the buyer refuses to sacrifice.
- Inspection: give an observable buying test.
- Honest contradiction: open a specific question and resolve it promptly.
- Price or skepticism concession: answer the actual objection.
- Real offer event: communicate genuine changed terms.

Psychological hypotheses—not measured effects—include recognition, relief from self-blame, loss avoidance, selection agency, curiosity, perceived candor, and imagining future use. Choose one primary appeal; do not stack every trigger into the opening.

Keep four commercial questions separate:
“Why this solution?” → “Why this formulation?” → “Why this seller?” → “Why now?”

For each feature, write:
buyer requirement → feature → supported action → relevant consequence.

Proof must match the uncertainty:
- A genuine demonstration can support the function shown.
- A testimonial establishes what that person reported, not a universal result.
- Ingredient research does not automatically substantiate the finished formulation.
- A mechanism explanation or analogy is not proof.
- A guarantee addresses purchase risk, not clinical efficacy.

CTA transitions should finish the argument: criteria → inspect the product; demonstrated function → see specifications; authenticity checks → authorized seller; real offer → current terms; information gap → the matching article.

At sentence level: preserve cause and consequence, define terms through their jobs, use at most one helpful analogy, and cut repeated explanation before cutting necessary reasoning.

5. Future workflow and limitations

For substantial drafts, the workflow is:

1. Retrieve current product, brand, offer, claim, and customer evidence.
2. Establish audience awareness, skepticism, narrator legitimacy, destination, and available proof.
3. Use find_swipes.py to select relevant cases by buying question.
4. Read the closest full transcripts and analyses.
5. Write original copy using the argument structure—not competitor claims, people, or experiences.
6. Verify claim support, hook/body continuity, feature relevance, CTA destination, and spoken clarity.

I followed the index into brand and strategy files. A useful caution: Wend’s local brief contains proposed pricing, an unresolved guarantee, and explicit unverified-literature warnings. Those are not automatically publishable current facts.

No core specialist research files were missing. Ancillary routing has limitations: brands/README.md references a renavita directory absent from this mirror; Motilli does not have the advertised root 00-brief.md; the strategy README’s extra skills/ path segment is stale, and its referenced swipe-adaptation.md is absent at that location. Actual paths must be resolved rather than assumed. The mirror also excludes media binaries; I did not visually review videos or establish speaker identity or AI origin.

Memory save succeeded. Location: the existing persistent memory store, target=memory. The tool did not expose a physical filesystem filename. I added one compact reference linking the index and shared specialist, with current-brand-truth and full-source retrieval requirements; no existing memory was removed or replaced.

This is retrieval-based knowledge use—not model fine-tuning or permanent retention of the whole corpus. No source files or settings were modified, and nothing was published or sent externally.
