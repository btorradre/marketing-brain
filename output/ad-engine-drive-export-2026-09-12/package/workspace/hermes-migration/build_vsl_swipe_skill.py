#!/usr/bin/env python3
"""Rebuild a portable, traceable corpus from the existing September 6 retrieval."""
import hashlib, json
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'_engine/research/trendtrack-ai-ugc-vsls-2026-09-06'
DEST=BASE/'ai-ugc-vsl-swipe-copywriting/references'
# IDs, selection criteria and interpretation are editorial annotation, not measured effects.
PATTERNS=[
('recognition-and-validation','Specific experience contradicts reassurance','N1 N3 N4 L2 E1 P1','Problem-aware people who feel their repeated experience has not been explained.','recognition; validation; relief from self-blame','Open with an observable recurring situation; acknowledge the unresolved question; give a supported explanation.','The promised explanation must account for the opening experience before the product appears.','Do not assert doctors are wrong, dismiss diagnoses, or borrow lab thresholds from the ad.'),
('failed-attempt-ledger','Attempt, cost or effort, disappointing consequence','G1 G2 L2 A1 NH1','Skeptical buyers who have already tried relevant alternatives.','effort validation; anticipated regret; reason to reconsider','Select a few real attempts; show the specific gap they share; define what a new option needs to do.','Move from the shared limitation into selection criteria, then product fit.','Do not invent expenditure, personal failure, or claim every alternative is ineffective.'),
('preserve-the-gain','Keep a valued gain while resolving its trade-off','G2 G3 Z2 F1','People reluctant to sacrifice something they value to solve another problem.','loss aversion hypothesis; conflict resolution; regained agency','Name the gain and unresolved cost; explain the supported way the proposed solution addresses the conflict.','Show evidence for both sides of the desired combination.','Do not imply a supplement preserves treatment benefits or eliminates side effects without evidence.'),
('buyer-inspection','Inspect this before choosing','N5 A1 SA1','Solution-aware shoppers comparing formulations or features.','agency; competence; reduced uncertainty','Turn the choice into an observable check; explain why the criterion matters; show the product meets it.','Checklist match: the brand answers the inspection task.','Specifications, exclusivity and comparative superiority require product-specific support.'),
('practical-use-question','How to use an already interesting category','R1 NH1','Ingredient- or solution-aware viewers with a real use question.','practical utility; relevance; earned authority','Answer the use question within approved directions, then explain the meaningful product distinction.','Recommendation follows the useful answer and supported criteria.','Do not reuse medical dosing or fabricate a clinician narrator.'),
('reverse-warning','An apparent complaint becomes an honest qualification','R2 U2','Product-aware viewers who have a reason to care about a review or real offer.','expectation violation; curiosity','Name the product and a truthful surprising qualification; resolve the apparent warning promptly.','Early reveal; explain the qualification and practical value.','No fabricated complaint, miraculous outcome, or invented apology/discount.'),
('discovery-story','An unusual discovery becomes relevant to daily life','R3 L3 A2 AR2','Problem-aware viewers who need a credible reason to consider a different approach.','curiosity; narrative identification; earned trust','Start with a sourced discovery or founder decision; expand to a recognizable problem; explain the selection.','The product is the next supported event in the story.','Shock without relevance fails; invented first-person histories are not usable testimonials.'),
('success-with-hidden-cost','An outward success conflicts with felt experience','Z2 C2 AR1 B2','An audience whose desired identity or activity is threatened despite apparent progress.','identity continuity; recognition; emotional contrast','Show the contradiction through an actual situation; identify what the person wants restored.','Use the product rationale to connect to a supported activity, not an abstract transformation.','Do not invent trauma, lab results, relationship dialogue, or promised recovery.'),
('one-analogy-explanation','One physical analogy makes the missing link understandable','Z1 N2 L1 C1 E2','Viewers who need an unfamiliar functional distinction explained.','comprehension; uncertainty reduction','State the literal supported process, map one familiar analogy to it, and reuse that mapping only while useful.','Derive a feature requirement from the explanation.','An analogy cannot establish clinical efficacy; do not mix metaphors or invent a hidden cause.'),
('staged-progress','Small developments lead back to ordinary participation','Z2 R4 G3','Buyers whose skepticism concerns what actual use or progress would look like.','credible expectations; future-use imagination; identity restoration','Use documented milestones and remaining uncertainty; finish with a concrete activity.','Product use and relevant evidence lead into the outcome sequence.','Do not invent days-to-results or imply an individual timeline is typical.'),
('objection-dialogue','Each answer earns the next buyer question','U3 S1 H1 P2','Audiences with several connected objections or a context-specific suitability question.','vicarious learning; objection resolution; reduced embarrassment','Ask the question raised by the previous answer; keep speaker knowledge and commercial roles distinct.','Questions advance from explanation to selection and practical use.','Source medical advice is unverified; do not create fake experts, witnesses, or endorsements.'),
('article-curiosity','An information promise earns the next click','Z3 B1','Briefs whose conversion event is an article visit rather than immediate purchase.','curiosity; low-commitment next action','Give recognition and a useful partial answer; state exactly what the article will explain.','The bridge is to information and must match the actual destination.','Do not promise an imminent in-video answer and withhold it, or assume clicks prove purchases.'),
('participatory-proof','Ask the viewer to inspect or compare','F4 F2','Product-aware buyers evaluating quality, appearance or value.','participation; uncertainty reduction; concrete proof','Pose a visible comparison; show relevant details; explain the supported conclusion.','Early product demonstration supplies its own relevance.','Actual visuals and provenance must support the comparison; do not fake aged products or price anchors.'),
('one-purchase-many-uses','A narrow purchase occasion expands into daily usefulness','F1 F3 F6 F8','Buyers who understand the product but question versatility or ongoing value.','future-use imagination; reduced choice burden; value','Start with a concrete occasion; show supported additional use cases and the features that enable them.','Product-first or discovery bridge, with feature-to-use explanation.','Do not invent capacity, material, airline compatibility, or customer experience.'),
('meaning-and-real-offer','A specific object or actual availability supplies a reason now','F5 F7 U2','Warm audiences evaluating personal meaning, price or a genuine offer.','identity expression; value anchoring; action friction reduction','Tie meaning to a specific design or use; state only the actual current offer and terms.','Product/offer-first; evidence and terms resolve the remaining buying obstacle.','Celebrity association, awards, restocks, scarcity and discounts in swipes are unverified historical claims.'),
('ordered-risk-explanation','An ordered sequence makes a developing problem legible','S2','A brief that needs an accurate ordered explanation and has evidence for its stages.','attention through sequence; perceived relevance of consequences','Use only verified stages or steps and explain the consequence of each without implying inevitable deterioration.','Any solution recommendation needs independent support for its role; the source ad does not provide it.','The source kidney-disease fear ladder is unverified and must not supply medical facts or treatment advice.'),
('characters-explain-jobs','Personified parts make feature roles memorable','U1 H1 H2 Z4 AU1','Requests for explanatory dialogue or adjacent animated formats.','concreteness; memory aid; question sequencing','Give each character one supported job and connect the jobs to the buyer question.','A combined product must actually supply the stated jobs.','An animated claim is still a claim; do not force this adjacent format into spoken UGC.')]

CASE_SEQUENCE = {
'N1': ('Symptoms despite reassuring lab interpretation → repeated invalidation → claimed limits of an earlier iron form → absorption/storage/support jobs → complete-formula criteria → Ferravital → next action.', 'The buyer is taught what complete means before the bottle recommendation. The ad’s thresholds and ingredient efficacy claims remain unverified.'),
'N2': ('Heavy-period context → refill versus ongoing loss → claimed ingredient jobs → product fit.', 'The audience situation changes around related buying criteria. Use the recurring-loss metaphor only if the new product evidence supports its literal premise.'),
'N3': ('Postpartum symptoms and dismissal → advocate narrator → explanation and formulation criteria → product → caring for oneself and a child.', 'The emotional close enlarges the consequence of relief. A nurse role and patient history require actual support.'),
'N5': ('Turn the bottle over → reject a label feature → explain the claimed limitation → identify formulation requirements → recommend the match.', 'The opening turns passive listening into an inspection task for solution-aware shoppers.'),
'L1': ('Failed remedies → claimed protective layer and impaired movement → ingredient role → fermentation requirement → recommendation → routine and expectations.', 'There are two purchasing arguments: why this ingredient, then why this particular preparation. The second needs evidence of a meaningful distinction.'),
'L2': ('Still feeling full after going → unsuccessful attempts → household analogy for a claimed obstacle → ingredient and product → feeling light after going.', 'The close resolves the precise opening sensation instead of ending on generic wellness. ASR product spelling is preserved in the source.'),
'G1': ('Attempt, price, disappointing result repeated → frustration and expense → situation-specific explanation → two ingredient jobs → usable relief → action.', 'A failure ledger gives the new explanation a concrete problem to solve. Brand visibility was observed in video even though the transcript does not clearly name it.'),
'G2': ('Repeated digestive frustration → temptation to abandon valued progress → situation-specific product → explanation → preserving the gain → next action.', 'The key emotional purchase is avoiding the trade-off. The new product requires its own evidence for that combined promise.'),
'R1': ('Practical usage question → claimed speaker authority → ingredient explanation → formulation distinctions → recommendation.', 'The opening assumes ingredient interest. Answering the use question is part of the attention bargain, not a pretext for an unrelated pitch.'),
'R2': ('Immediate brand warning → warning reverses into praise → claimed experience → product value.', 'Brand entry is near the beginning. Curiosity concerns the qualification, not the identity of a hidden product.'),
'R3': ('Unusual household incident → wider familiar symptoms → discovery and explanation → product selection → household relevance.', 'The shock earns its place only when the story becomes relevant to ordinary life. Do not reuse the incident as a fabricated customer experience.'),
'Z1': ('Failed familiar advice → claimed signal-versus-response distinction → stable analogy used to explain prior failures → ingredient role → concentration/formulation criteria → product.', 'A long script advances through multiple real questions. Coherent rhetoric does not verify the ad’s neuroscience or dosing claims.'),
'Z2': ('Weight-loss success with lost joy → relationships and dismissal → search for explanation → refusal to surrender progress → protocol → initial skepticism → small changes → ordinary family participation.', 'The branded product appears well before the end, leaving room for uncertainty and a gradual story. The milestones and dialogue are ad claims, not reusable testimony.'),
'C1': ('Disappointing iron results → claimed limited absorption route → door analogy → different delivery format → product.', 'A delivery feature supplies the differentiation. This explanation differs from Nivara’s swallowed-formula argument; neither is independently verified here.'),
'C2': ('Lost running ability → apparently measurable problem → alternate explanation → product format → return to valued performance.', 'The outcome matters because it restores an activity. Competitor lab and pace numbers cannot be transferred.'),
'A1': ('Four rejected remedies → each rejection introduces a requirement → combination satisfies the checklist → practical routine and reassurance.', 'Product entry follows completed criteria, around the middle rather than a fixed late position. The limited observed run does not make this a proven winner.'),
'A2': ('Sister’s repeated private problem → reason for founding → research and formulation decisions → product and seller trust.', 'The founder’s commercial motive is part of the story; caring about a problem does not prove the solution works.'),
'E1': ('Specific morning bathroom scene → familiar disappointment → early product reveal → ingredient jobs → return to daily participation.', 'The script names the product around 23 percent through transcript words and continues explaining afterward.'),
'U3': ('Recurring concern → failed attempts → claimed obstacle → why this audience differs → ingredient jobs → objection about a previous product → recommendation and routine.', 'Follow-up questions perform actual reasoning. The supplied medical assertions and diabetes-specific recommendations are unverified.'),
'F1': ('Travel need → capacity versus polished appearance → product → packing and feature details → ongoing use and value.', 'A demonstrable trade-off supports a product rationale without a hidden medical mechanism. ASR errors prevent treating every transcribed construction phrase as reliable.'),
'F4': ('Ask which bag is older → inspect visible aging → explain materials through use → long-term value.', 'The viewer participates in the quality argument. A comparable new ad needs authentic provenance for the actual old and new products.'),
'F6': ('Bought for vacation → useful beyond the trip → capacity and design details → everyday value.', 'The argument expands a narrow purchase occasion. Verify every feature and use claim for the new product.'),
'S2': ('An asserted sequence of disease stages escalates perceived danger and introduces a claimed drainage explanation.', 'This is a historical example of fear-based sequencing, not a medical teaching source. Do not transfer its disease staging or treatment implications.'),
}

def write_json(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def main():
 raw=SOURCE/'raw'; brands=json.loads((raw/'brands.json').read_text()); cases=json.loads((raw/'cases-internal.json').read_text())
 records={}; raw_count=0; source_hashes={}
 def record(brand,text,origin,sample,usage=None,days=None,grouped=True):
  digest=hashlib.sha256(text.encode()).hexdigest(); key=(brand['id'],digest)
  if key not in records:
   sid='T-'+brand['id'][:8]+'-'+digest[:12]
   records[key]={'transcriptId':sid,'brand':brand['name'],'brandtrackerId':brand['id'],'sha256':digest,'wordCount':len(text.split()),'fullText':text,'groupedCorpus':grouped,'caseIds':[],'sources':[],'transcriptPath':'transcripts/'+sid+'.txt'}
  records[key]['sources'].append({'file':origin[0],'rowIndex':origin[1],'retrievalKind':origin[2],'sampleAd':sample,'usageCount':usage,'longestRunning':days})
  return records[key]
 for b in brands:
  for kind in ['usage','longest']:
   p=raw/('nivara-transcripts-usage.json' if b['name']=='Nivara Official' and kind=='usage' else b['id']+'-'+kind+'.json')
   if not p.exists():continue
   source_hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
   for i,a in enumerate(json.loads(p.read_text())['result']['structuredContent'].get('data',[])):
    raw_count+=1;record(b,a['fullText'],(p.name,i,kind),a['sampleAd'],a.get('usageCount'),a.get('longestRunning'))
 grouped=len(records)
 for c in cases:
  b=next(b for b in brands if b['id']==c['brandtrackerId']); key=(b['id'],hashlib.sha256(c['fullText'].encode()).hexdigest())
  if key not in records:
   fn=b['id']+'-'+c['kind']+'.json'; source_hashes[fn]=hashlib.sha256((raw/fn).read_bytes()).hexdigest()
   row=record(b,c['fullText'],(fn,c['index'],c['kind']),{'adId':c['adId'],'mediaUrl':c['mediaUrl'],'thumbnailUrl':c['thumbnailUrl']},c.get('usageCount'),c.get('longestRunning'),False)
  else:row=records[key]
  row['caseIds'].append(c['caseId']);c['transcriptId']=row['transcriptId'];c['transcriptPath']=row['transcriptPath']
  c['patterns']=[p[0] for p in PATTERNS if c['caseId'] in p[2].split()]
  c['analysisPath']='cases/'+c['caseId']+'.md'
 for row in records.values():(DEST/row['transcriptPath']).write_text(row['fullText'])
 with (DEST/'transcripts.jsonl').open('w') as f:
  for row in records.values():f.write(json.dumps(row,ensure_ascii=False)+'\n')
 annotated=[]
 for c in cases:
  ps=[p for p in PATTERNS if p[0] in c['patterns']]
  text=f"# {c['caseId']} — {c['brand']}: {c['title']}\n\nSource: September 6, 2026 TrendTrack retrieval. Advertising assertions are not verified product evidence.\n\n[Full verbatim transcript](../{c['transcriptPath']}) · [Source media]({c['mediaUrl']})\n\n"
  text+=f"- Source row: `{c['brandtrackerId']}`, `{c['kind']}`, index {c['index']}; representative ad `{c['adId']}`.\n- Transcript words: {c['wordCount']}; grouped uses: {c.get('usageCount')}; longest observed run: {c.get('longestRunning')} days. Deployment indicators, not conversion results.\n"
  if c.get('individualStatus'):text+=f"- Representative status at original scan: {c['individualStatus']}; verdict: {c.get('individualScanVerdict','not recorded')}. Historical status only.\n"
  if 'firstNamedProductWordFraction' in c:text+=f"- Approximate first named product position: {c['firstNamedProductWordFraction']:.1%} of transcript words, not video time.\n"
  if c['caseId'] in CASE_SEQUENCE:
   sequence, distinction = CASE_SEQUENCE[c['caseId']]
   text += '\n## Observed argument in this case\n\n' + sequence + '\n\n' + distinction + '\n'
  text+='\n## Opening from retrieved transcript\n\n> '+' '.join(c['fullText'].split()[:45])+' …\n\nThe excerpt preserves the source wording; its factual claims and speaker role are unverified. Read the full transcript for the payoff and product bridge.\n\n## Editorial interpretation\n\n'
  if not ps:text+='Use the original study for this case; no detailed pattern annotation has been assigned.\n'
  for p in ps:
   text+=f"### {p[0]}\n\nAudience fit: {p[3]}\n\nPsychological reading (hypothesis): {p[4]}.\n\nTransferable writing move: {p[5]}\n\nProduct/CTA bridge: {p[6]}\n\nAdaptation limit: {p[7]}\n\n"
  text+='## Adaptation exercise\n\nIdentify the current belief, the question opened, the explanation actually supplied, the selection criterion, and the closing activity in this transcript. Keep that dependency only where it fits the new brief. Replace all claims, personal scenes, proof and offer terms with the new product’s supported material. Cite this case ID in strategy notes when requested.\n'
  (DEST/c['analysisPath']).write_text(text)
  annotated.append({k:v for k,v in c.items() if k!='fullText'})
 write_json(DEST/'cases.json',annotated)
 patterns=[dict(zip(['id','name','caseIds','audience','psychologicalHypotheses','writingMove','bridge','limits'],[p[0],p[1],p[2].split(),*p[3:]])) for p in PATTERNS]
 write_json(DEST/'patterns.json',patterns)
 md='# Hook patterns: select by audience question\n\nThese are editorial interpretations of observed ads, not measured causes of performance. Combine sparingly. Source case links lead to full transcripts and provenance.\n\n'
 for p in PATTERNS:
  md+=f"## {p[0]} — {p[1]}\n\n**Use when:** {p[3]}\n\n**Appeal:** {p[4]} (hypotheses).\n\n**Build it:** {p[5]}\n\n**Payoff and bridge:** {p[6]}\n\n**Avoid:** {p[7]}\n\n**Read:** "+', '.join(f'[{cid}](cases/{cid}.md)' for cid in p[2].split())+'\n\n'
 (DEST/'hook-patterns.md').write_text(md)
 index='# Curated case index\n\n49 selected cases. All have full source transcripts. Tags are qualitative editorial annotations. For noncurated texts use `find_swipes.py --all`; do not imply every corpus entry was deeply analyzed.\n\n| Case | Brand / observed structure | Pattern IDs | Words |\n|---|---|---|---|\n'
 for c in cases:index+=f"| [{c['caseId']}]({c['analysisPath']}) | {c['brand']} / {c['title']} | {', '.join(c['patterns'])} | {c['wordCount']} |\n"
 (DEST/'case-index.md').write_text(index)
 manifest={'studyDate':'2026-09-06','packagedDate':'2026-09-07','sourceWorkspacePath':str(SOURCE.relative_to(BASE.parent)),'trackedEntries':len(brands),'groupedRows':raw_count,'distinctWithinBrandGroupedTranscripts':grouped,'supplementalDistinctCaseTranscripts':len(records)-grouped,'totalPackagedTranscripts':len(records),'curatedCases':len(cases),'patternFamilies':len(PATTERNS),'deduplication':'exact UTF-8 fullText SHA-256 within brandtrackerId; no ASR normalization','transcriptPreservation':'individual .txt equals fullText exactly; transcripts.jsonl also retains fullText','sources':source_hashes,'limits':'Historical deployment proxies, not causal conversion or medical evidence. Wider corpus includes adjacent formats. Current-video supplemental case is outside the grouped transcript count.'}
 write_json(DEST/'corpus-manifest.json',manifest)
 print(json.dumps({k:v for k,v in manifest.items() if k not in ['sources','limits']},indent=2))
if __name__=='__main__':
 main()
 supplement=BASE/'augment_vsl_with_nuora.py'
 if supplement.exists() and (BASE.parent/'_engine/research/nuora-trendtrack-2026-09-07/annotated-transcripts.json').exists():
  import subprocess,sys
  subprocess.run([sys.executable,str(supplement)],check=True)

