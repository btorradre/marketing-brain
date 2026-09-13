#!/usr/bin/env python3
"""Reproducible corpus indexing and explicit editorial family annotation."""
import json,re,hashlib,difflib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FAMILIES=[
('ingredient-characters','Ingredient characters assemble the formula',[1,3,4,5,23,24],'One ingredient, one symptom, one job; the brand combines the jobs.','concreteness; comprehension; completeness'),
('apology-and-reverse-warning','Apparent apology or warning reveals an offer',[2,14,22,51,60,61,72,73,74,75,76,77,78,79,118,119,150],'Open a reputational concern, affirm product claims, then resolve the concern as a better deal.','curiosity; expectation violation; value anchoring'),
('purge-then-relief','Initial worsening is reframed as progress',[7,8,16,17,31,32,153],'Present an unwanted early experience as evidence of action before promising relief.','expectation management; objection preemption; commitment reinforcement'),
('historical-disruption','Historical progress creates an alleged downstream problem',[9,10,11],'Acknowledge the benefit of an old intervention, then argue it left a gap that the product restores.','narrative coherence; causal reframing; restoration'),
('counterfeit-and-official-channel','Skepticism becomes a counterfeit/official-channel argument',[12,13,20,38,42,52,93,128,143,165],'Move from disappointment or copies to authenticity checks and the official purchase destination.','loss avoidance; skepticism redirection; purchase confidence'),
('numbered-buying-criteria','Countdown of formulation criteria',[48,49,50],'Source, potency and pairing become a numbered comparison checklist.','selection agency; specificity; reduced uncertainty'),
('symptom-countdown','Recognizable signs in a list or countdown',[18,35,36,89,97,103],'Give recognizable entry points and explain each through the preferred account.','recognition; completion expectancy; self-relevance'),
('failed-solution-journey','A sequence of attempted remedies earns a new choice',[21,71,155],'Chronological failed attempts create the question answered by a claimed expert discovery.','effort validation; narrative identification; reason to reconsider'),
('partner-trigger','A relationship-related cause opens the explanation',[26,30,40],'A provocative interpersonal explanation transitions into a practical biological story.','curiosity; reduced self-blame; relationship relevance'),
('shame-reversal','Reject hygiene blame and explain recurrence',[27,28,29,156],'Name a shaming explanation, reject it, validate effort, then propose a new causal account.','validation; relief from self-blame; earned authority'),
('price-concession','Admit price, then explain design trade-offs',[34,121,127,151,152,161],'Agree the product costs money; explain the cheaper choices the brand says it declined and why.','two-sided argument; perceived transparency; value justification'),
('protocol-consolidation','Separate symptom remedies become one routine',[43,55,91,98,99,101],'Map symptoms to ingredient jobs, expose cost or complexity, and consolidate into one product.','convenience; reduced choice burden; value anchoring'),
('staged-timeline','A timeline turns mechanism into expected experience',[37,44,45,56,58,59,65,66,67,68,82,83,84,85,86,87,105,106,107,108,109,110,141,166],'Alternate unseen mechanism and imagined milestones before an everyday outcome.','future-use imagination; expectancy; narrative progression'),
('social-fantasy-concession','Desired social reaction followed by a modest concession',[46,47,64,104,111,112],'Stage a desired reaction, concede exaggeration, then translate value into everyday freedom.','social recognition; identity expression; two-sided argument'),
('anti-advertising','Attack misleading category advertising, then differentiate',[69],'Voice the viewer’s ad fatigue and substitute a specific product-selection argument.','skeptic alignment; perceived candor; trust'),
('borrowed-customer-question','A Reddit-style account supplies the teaching question',[88,102,164,168],'Retell a specific unresolved case, interpret failed attempts, and recommend a formulation.','identification; borrowed social evidence; explanatory authority'),
('symptom-to-hidden-cause','Symptoms lead through a claimed obstacle to product criteria',[25,57,90,94,95,96,100,120,136,137,138,139,140,142,170],'Use recognition, recurrence and a physical analogy to establish a claimed obstacle and solution jobs.','recognition; causal comprehension; uncertainty reduction'),
('founder-values','Why we built it and which compromises we rejected',[122,123,124,125,126,163],'Link seller values to specific formulation decisions and dissatisfaction with alternatives.','seller trust; motive transparency; value justification'),
('personified-objection-debate','Products or foods voice the buyer’s objections',[129,130,131,132,133,148],'Let an alternative object, then answer with a audience-specific rationale and product roles.','vicarious learning; objection resolution; preserving desired activities'),
('offer-event','Deadline or warehouse event gives a reason to buy',[6,117,134,135,162],'Lead with a purported deadline or inventory event, then state discount and action.','urgency; deal salience; reason-why pricing'),
('seasonal-context','A season supplies the problem and desired activity',[144,145],'Connect familiar seasonal conditions to a proposed routine and an offer.','situational salience; future-use imagination'),
('condition-specific-testimonial','Condition-specific customer claim or treatment comparison',[54,92,149,167,169],'Call out a condition, claim practitioner/customer support, then give a routine and outcome.','identification; borrowed authority; social confirmation'),
('short-product-introduction','Short direct product or category explanation',[15,33,39,41,62,63,146,147,154,157,158,159,160],'Quick recognition or a stitched opening leads into product use or category relevance.','immediacy; simplicity; familiarity'),
('nondeveloped-audio','Music, fragments, or short nondeveloped dialogue',[19,53,70,80,81,113,114,115,116],'Excluded from developed VSL framework conclusions.','not assigned')]
DEEP=[1,2,3,7,9,12,18,21,26,34,27,35,38,43,46,48,69,88,91,95,117,121,123,129,132,134,136,141,144,149]

def main():
 rows=json.loads((ROOT/'transcripts.json').read_text());mapping={n:f for f in FAMILIES for n in f[2]}
 assert len(mapping)==170 and len([n for f in FAMILIES for n in f[2]])==170
 assert len(set(x['sha256'] for x in rows))==170
 records=[]
 for i,x in enumerate(rows,1):
  f=mapping[i]; records.append({**x,'executionFamily':f[0],'psychologicalHypotheses':f[4].split('; '),'fullTranscriptReviewed':i in DEEP,'reviewLevel':'full transcript qualitative review' if i in DEEP else 'opening reviewed; family assigned from visible wording; no individual full-text qualitative review','transcriptPath':'transcripts/'+x['id']+'.txt'})
 (ROOT/'annotated-transcripts.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 families=[{'id':f[0],'name':f[1],'transcriptIds':[f'NU{n:03}' for n in f[2]],'count':len(f[2]),'observedStructure':f[3],'psychologicalHypotheses':f[4]} for f in FAMILIES]
 (ROOT/'execution-families.json').write_text(json.dumps(families,indent=2)+'\n')
 normalize=lambda t:re.findall(r'\w+',t.lower())
 similarities=[]
 for a,b in [(9,10),(9,11),(44,45),(105,106),(108,109),(117,162),(34,121),(48,49)]:
  left,right=rows[a-1],rows[b-1];ratio=difflib.SequenceMatcher(None,normalize(left['fullText']),normalize(right['fullText']),autojunk=False).ratio()
  similarities.append({'left':left['id'],'right':right['id'],'normalizedWordSequenceSimilarity':round(ratio,4)})
 normalized_count=len({tuple(normalize(x['fullText'])) for x in rows})
 manifest={'studyDate':'2026-09-07','brand':'Nuora','brandtrackerId':'8bff2239-0790-4f87-a97e-15434c0fc9b6','trackerUrl':'https://app.trendtrack.io/en/workspace/w-brookss-workspace-OrIOUrb/brandtracker/8bff2239-0790-4f87-a97e-15434c0fc9b6','window':'last1y: relative ad start-date window, not transcript processing date','endpoint':'get_brandtracker_transcripts','pagesRetrieved':4,'endpointReportedGroups':170,'retrievedRows':170,'exactDistinctTranscripts':170,'normalizedDistinctTranscripts':normalized_count,'totalTranscriptWords':sum(len(x['fullText'].split()) for x in rows),'fullTranscriptQualitativeReviews':len(DEEP),'fullReviewedIds':[f'NU{x:03}' for x in DEEP],'openingReviews':170,'executionFamilies':24,'newExactTextsVersusLocalNuora':158,'overlapWithLocalNuora':12,'priorNuoraTextAbsentFromNewGroupedFetch':1,'transcriptCreditsUsed':255,'clinicalClaimsVerified':False,'visualFormatRechecked':False,'sourceNote':'Full texts preserved including ASR errors, fragments and incidental music. Counts describe retrieval and qualitative coverage, not ads proven to convert. Group uses and longestRunning are not attributed performance.'}
 (ROOT/'coverage.json').write_text(json.dumps(manifest,indent=2)+'\n');(ROOT/'variant-similarity.json').write_text(json.dumps(similarities,indent=2)+'\n')
 lines=['# Nuora transcript index','', '170 completed grouped transcripts retrieved in the one-year ad-start window. Full verbatim source texts linked below. Psychological labels are editorial hypotheses. Thirty full transcripts were reviewed; all 170 openings were reviewed.','', '| ID | Execution family | Uses | Longest run, days | Words | Review | Source |','|---|---|---:|---:|---:|---|---|']
 for x in records:lines.append(f"| [{x['id']}]({x['transcriptPath']}) | {x['executionFamily']} | {x['usageCount']} | {x['longestRunning']} | {len(x['fullText'].split())} | {'Full text' if x['fullTranscriptReviewed'] else 'Opening'} | [Media]({x['sampleAd'].get('mediaUrl') or x['sampleAd'].get('thumbnailUrl')}) |")
 (ROOT/'TRANSCRIPT-INDEX.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(manifest,indent=2));print('SIMILARITY',json.dumps(similarities));print('FAMILY COUNTS',[(f[0],len(f[2])) for f in FAMILIES])
if __name__=='__main__':main()
