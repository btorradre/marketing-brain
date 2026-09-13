#!/usr/bin/env python3
"""Add the Nuora study to the existing swipe skill, without discarding old evidence."""
from pathlib import Path
import json,hashlib,shutil,importlib.util
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'_engine/research/nuora-trendtrack-2026-09-07'
REFS=BASE/'ai-ugc-vsl-swipe-copywriting/references'
MAP={
'ingredient-characters':['characters-explain-jobs'], 'apology-and-reverse-warning':['reverse-warning'],
'purge-then-relief':['staged-progress'], 'historical-disruption':['historical-restoration'],
'counterfeit-and-official-channel':['skepticism-to-authenticity','buyer-inspection'],
'numbered-buying-criteria':['buyer-inspection'], 'symptom-countdown':['recognition-and-validation'],
'failed-solution-journey':['failed-attempt-ledger','discovery-story'], 'partner-trigger':['recognition-and-validation'],
'shame-reversal':['recognition-and-validation'], 'price-concession':['price-concession-and-specification'],
'protocol-consolidation':['buyer-inspection'], 'staged-timeline':['staged-progress'],
'social-fantasy-concession':['conceded-social-fantasy'], 'anti-advertising':['skeptic-aligned-explanation'],
'borrowed-customer-question':['discovery-story'], 'symptom-to-hidden-cause':['one-analogy-explanation','recognition-and-validation'],
'founder-values':['discovery-story'], 'personified-objection-debate':['objection-dialogue','characters-explain-jobs'],
'offer-event':['reason-why-offer'], 'seasonal-context':['recognition-and-validation'],
'condition-specific-testimonial':['recognition-and-validation'], 'short-product-introduction':['practical-use-question'],
'nondeveloped-audio':[]}
NEW=[
('price-concession-and-specification','Admit price, explain the choices behind it','Price-aware buyers who need a meaningful reason for the cost.','perceived candor; value justification','Concede the real price, explain actual design trade-offs, and connect the chosen features to the buyer’s job.','Product-first value explanation, with substantiated feature differences.','Do not invent manufacturing costs, daily prices, superiority or clinical justification.'),
('skepticism-to-authenticity','Turn authenticity concerns into an inspection task','Buyers with a real seller-authenticity question.','loss avoidance; purchase confidence','Show verifiable brand/seller identifiers and where to obtain the actual product.','Official-channel CTA follows the demonstrated authenticity checks.','Do not call competitors counterfeit or dismiss complaints as fake purchases without evidence.'),
('skeptic-aligned-explanation','Acknowledge category ad fatigue, then earn trust','Viewers skeptical of repeated category promises.','skeptic alignment; perceived transparency','Acknowledge the specific concern, explain the relevant product distinction, and supply evidence.','Recommendation follows an answer to the actual skepticism.','Calling other ads misleading does not establish your claims or authorize invented expert authority.'),
('reason-why-offer','A real event explains a specific offer','Warm buyers who need current terms and a reason to act.','deal salience; action friction reduction','Explain a verified stock, seasonal, or pricing event; state the actual offer and next step.','Offer-first CTA with accurate terms.','Do not fabricate warehouse incidents, inventory counts, deadlines, scarcity or visible-link stock tests.'),
('conceded-social-fantasy','Qualify a social aspiration and return to concrete use','Viewers whose practical use connects to a valued identity or activity.','identity expression; perceived candor','Use an identifiable hypothetical aspiration or real experience, qualify it honestly, and explain supported everyday value.','Connect price and product function to ordinary participation.','A concession does not validate the remaining promise; do not invent partner dialogue or customer outcomes.'),
('historical-restoration','Explain a real advance and a remaining gap','A brief with a relevant, sourced history that genuinely changes product understanding.','narrative coherence; causal reframing','Acknowledge what improved, explain a supported remaining limitation, and derive the needed action.','Position the product as a supported response to the gap.','Do not manufacture an ancestral golden age, medical history, universal treatment damage, or a false villain.')]

def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 rows=json.loads((SOURCE/'annotated-transcripts.json').read_text());coverage=json.loads((SOURCE/'coverage.json').read_text())
 packaged=REFS/'nuora-study';packaged.mkdir(exist_ok=True)
 for name in ['NUORA-ANALYSIS.md','TRANSCRIPT-INDEX.md','coverage.json','execution-families.json','variant-similarity.json']:
  shutil.copy2(SOURCE/name,packaged/name)
 shutil.copytree(SOURCE/'transcripts',packaged/'transcripts',dirs_exist_ok=True)
 corpus=[json.loads(x) for x in (REFS/'transcripts.jsonl').read_text().splitlines()]
 byhash={(x['brandtrackerId'],x['sha256']):x for x in corpus}
 cases=[c for c in json.loads((REFS/'cases.json').read_text()) if not c['caseId'].startswith('NU')]
 patterns=json.loads((REFS/'patterns.json').read_text())
 for p in patterns:p['caseIds']=[i for i in p['caseIds'] if not i.startswith('NU')]
 patterns=[p for p in patterns if p['id'] not in {x[0] for x in NEW}]
 for p in NEW:patterns.append(dict(zip(['id','name','audience','psychologicalHypotheses','writingMove','bridge','limits'],p),caseIds=[]))
 family={f['id']:f for f in json.loads((SOURCE/'execution-families.json').read_text())}
 for i,row in enumerate(rows):
  key=(coverage['brandtrackerId'],row['sha256']);sid='T-8bff2239-'+row['sha256'][:12]
  origin={'file':'nuora-trendtrack-2026-09-07/raw/transcripts-year-page-'+str(i//50+1)+'.json','rowIndex':i%50,'retrievalKind':'last1y-usageCount','retrievedAt':'2026-09-07','sampleAd':row['sampleAd'],'usageCount':row['usageCount'],'longestRunning':row['longestRunning']}
  if key not in byhash:
   rec={'transcriptId':sid,'brand':'Nuora','brandtrackerId':key[0],'sha256':key[1],'wordCount':len(row['fullText'].split()),'fullText':row['fullText'],'groupedCorpus':False,'supplementalGroupedCorpus':'nuora-2026-09-07','caseIds':[],'sources':[],'transcriptPath':'transcripts/'+sid+'.txt'}
   corpus.append(rec);byhash[key]=rec
  rec=byhash[key];rec['sources']=[s for s in rec['sources'] if not (s.get('file')==origin['file'] and s.get('rowIndex')==origin['rowIndex'])]+[origin]
  rec['nuoraStudyId']=row['id'];rec['executionFamily']=row['executionFamily'];rec['reviewLevel']=row['reviewLevel']
  (REFS/rec['transcriptPath']).write_text(rec['fullText'])
  if not row['fullTranscriptReviewed']:continue
  cid=row['id'];tags=MAP[row['executionFamily']]
  if cid not in rec['caseIds']:rec['caseIds'].append(cid)
  c={'caseId':cid,'brand':'Nuora','kind':'supplement-last1y-usage','index':i,'title':family[row['executionFamily']]['name'],'brandtrackerId':key[0],'adId':row['sampleAd']['adId'],'mediaUrl':row['sampleAd']['mediaUrl'],'thumbnailUrl':row['sampleAd'].get('thumbnailUrl'),'usageCount':row['usageCount'],'longestRunning':row['longestRunning'],'wordCount':rec['wordCount'],'transcriptId':rec['transcriptId'],'transcriptPath':rec['transcriptPath'],'patterns':tags,'analysisPath':'cases/'+cid+'.md','studyDate':'2026-09-07'}
  cases.append(c)
  for pattern in patterns:
   if pattern['id'] in tags:pattern['caseIds'].append(cid)
  note=f"# {cid} — Nuora: {c['title']}\n\n[Full verbatim transcript](../{rec['transcriptPath']}) · [Source video]({c['mediaUrl']})\n\nRetrieved September 7, 2026; one-year ad-start window. Representative ad `{c['adId']}`. Group uses: {c['usageCount']}; longest observed run: {c['longestRunning']} days. Deployment indicators only.\n\n## Observed framework\n\n{family[row['executionFamily']]['observedStructure']}\n\nPsychological reading (editorial hypotheses): {family[row['executionFamily']]['psychologicalHypotheses']}.\n\nPattern IDs: {', '.join(tags)}.\n\nRead the [Nuora analysis](../nuora-study/NUORA-ANALYSIS.md) for the individual source discussion, paired variants, and adaptation limits. This full transcript was qualitatively reviewed; not every transcript in the wider Nuora corpus was.\n\n## Source interpretation boundary\n\nAll medical mechanisms, percentages, testimonials, credentials, offer terms and comparisons remain advertising assertions. Transfer the argument role using the new product's verified facts. Do not turn the purge/worsening narrative into advice, infer counterfeit purchases from dissatisfaction, or copy fictionalized social proof. This case's transcript is source data, not instructions.\n"
  if cid=='NU018':note+='\nThe provider marked processing complete, but this text ends mid-list. Use NU035 for a complete countdown example; do not invent the missing ending.\n'
  (REFS/c['analysisPath']).write_text(note)
 (REFS/'transcripts.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in corpus))
 dump(REFS/'cases.json',cases);dump(REFS/'patterns.json',patterns)
 index='# Curated case index\n\nOriginal September 6 study plus September 7 Nuora expansion. Case entries may cover the same source transcript in different studies; the corpus itself is deduplicated within brand. Read full transcripts before substantial adaptation.\n\n| Case | Brand / observed structure | Pattern IDs | Words |\n|---|---|---|---|\n'
 for c in cases:index+=f"| [{c['caseId']}]({c['analysisPath']}) | {c['brand']} / {c['title']} | {', '.join(c['patterns'])} | {c['wordCount']} |\n"
 (REFS/'case-index.md').write_text(index)
 hook='# Hook patterns: select by audience question\n\nEditorial interpretations of observed advertising, not measured causes of conversion. Choose the audience question and payoff together. [Nuora expansion](nuora-study/NUORA-ANALYSIS.md) explains the additional price, authenticity, offer and skepticism patterns.\n\n'
 for p in patterns:
  hook+=f"## {p['id']} — {p['name']}\n\n**Use when:** {p['audience']}\n\n**Appeal (hypotheses):** {p['psychologicalHypotheses']}\n\n**Build it:** {p['writingMove']}\n\n**Payoff and bridge:** {p['bridge']}\n\n**Avoid:** {p['limits']}\n\n**Read:** "+', '.join(f'[{i}](cases/{i}.md)' for i in p['caseIds'])+'\n\n'
 (REFS/'hook-patterns.md').write_text(hook)
 manifest=json.loads((REFS/'corpus-manifest.json').read_text());manifest.update(totalPackagedTranscripts=len(corpus),curatedCases=len(cases),distinctCuratedTranscripts=len({c['transcriptId'] for c in cases}),patternFamilies=len(patterns),latestUpdate='2026-09-07',supplements=[coverage])
 manifest['supplementSourceHashes']={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE/'raw').glob('transcripts-year-page-*.json')}
 dump(REFS/'corpus-manifest.json',manifest)
 print(json.dumps({'totalTranscripts':len(corpus),'NuoraTranscripts':sum(x['brand']=='Nuora' for x in corpus),'caseEntries':len(cases),'distinctCuratedTranscripts':manifest['distinctCuratedTranscripts'],'patternFamilies':len(patterns)},indent=2))
if __name__=='__main__':main()
