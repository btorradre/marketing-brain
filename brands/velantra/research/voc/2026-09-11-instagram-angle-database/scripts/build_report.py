import json,csv,re,math,collections,html,unicodedata,hashlib
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Spacer,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from angle_content import ANGLES
ROOT=Path(__file__).resolve().parents[1];DB=ROOT/'database';OUT=ROOT/'report';OUT.mkdir(exist_ok=True)
def rows(name):return [json.loads(x) for x in (DB/(name+'.jsonl')).read_text().splitlines()]
POSTS=rows('posts');COMMENTS=rows('comments');SEEDS=rows('seed_register');PS={p['post_id']:p for p in POSTS};CS={c['comment_id']:c for c in COMMENTS};ST=json.loads((DB/'summary.json').read_text())
RUNS=[json.loads(f.read_text())|{'wave':f.name[:-9]} for f in sorted((ROOT/'raw').glob('*-run.json'))]
COST=sum(x.get('usageTotalUsd',0) for x in RUNS)
pdfmetrics.registerFont(TTFont('ArialU','/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialB','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
styles={
 'title':ParagraphStyle('title',fontName='ArialB',fontSize=21,leading=25,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='ArialB',fontSize=11.5,leading=15,spaceBefore=8,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='ArialU',fontSize=10.5,leading=14.3,spaceAfter=9),
 'quote':ParagraphStyle('quote',fontName='ArialU',fontSize=10.5,leading=14,spaceAfter=4,leftIndent=10),
 'small':ParagraphStyle('small',fontName='ArialU',fontSize=8.5,leading=11.5,spaceAfter=6),
 'cell':ParagraphStyle('cell',fontName='ArialU',fontSize=8,leading=10.5),
}
PAGES=[];USED=set();QUOTE_LOG=[];SOURCE_INDEX={p['post_id']:f'P{i+1:04}' for i,p in enumerate(sorted(POSTS,key=lambda p:p['post_id']))}
def clean(s):return str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
def esc(s):return html.escape(str(s)).replace('\n','<br/>')
def mdclean(s):
 s=re.sub(r'<a href="([^"]+)">(.*?)</a>',r'[\2](\1)',s)
 return re.sub('<[^>]+>','',html.unescape(s))
def para(text,style='body'):return ('p',text,style)
def heading(s):return para(s,'h')
def page(title,blocks):PAGES.append({'title':title,'blocks':blocks})
def qblock(cid):
 c=CS[cid]
 if cid in USED:return [para(f'Related evidence already quoted in this report: <a href="{esc(c["source_url"])}">{esc(cid)}</a>.','small')]
 USED.add(cid);t=c['text'];tokens=list(re.finditer(r'\S+',t));end=tokens[min(24,len(tokens))-1].end() if tokens else 0
 # Select a contiguous verbatim span supported by the PDF font.
 sub=t[:end];glyphs=pdfmetrics.getFont('ArialU').face.charToGlyph
 parts=[];start=0
 for i,ch in enumerate(sub):
  if (ord(ch) not in glyphs and ch not in '\n\t') or ord(ch) in [0xfe0e,0xfe0f,0x200d] or unicodedata.category(ch)=='Cf':
   parts.append(sub[start:i]);start=i+1
 parts.append(sub[start:]);sub=max(parts,key=lambda x:len(x.split())).strip()
 exact=sub in t;omission=''
 QUOTE_LOG.append({'comment_id':cid,'post_id':c['post_id'],'excerpt':sub,'exact_contiguous':exact,'source_url':c['source_url'],'words':len(sub.split())})
 p=PS.get(c['post_id'],{});label=SOURCE_INDEX.get(c['post_id'],c['post_id']);clip=' [excerpt]' if sub!=t else ''
 return [para('“'+esc(sub)+'”'+clip+omission,'quote'),para(f'<a href="{esc(c["source_url"])}">{label} / {esc(cid)} / @{esc(c["author"] or "unknown")}</a> · {esc(c["published_at"][:10] or "date unavailable")} · {c["likes"]} likes at collection.','small')]
def prose(s):return para(esc(clean(s)))
def tblock(headers,data,widths=None):return ('table',headers,data,widths)
def eligible(c):
 t=c['text']
 return (c['post_id'] not in {'ig:DJ_994UpN_7'} and c['signal_class']=='substantive_candidate' and c['evidence_role']!='creator_reply' and c['category']=='handbag_context' and '@' not in t and len(t.split())>=5 and sum(ch.isascii() for ch in t)/max(len(t),1)>.78 and not re.search(r'\b(hair|hairdresser|shoes|jacket|sunglasses|watch|collab|follow me|my page|dm me)\b',t,re.I))
GOOD=[c for c in COMMENTS if eligible(c)]
def score(c):return math.log1p(max(0,int(c['likes'])))*2+min(len(c['text'].split()),35)/20
BYPOST=collections.defaultdict(list)
for c in GOOD:BYPOST[c['post_id']].append(c)
# 1
page('Velantra voice of the customer',[
 prose('[INFERRED] The strongest working frame is the desire to express personal taste and look well dressed while feeling in control of what the bag costs. This is an interpretation of the sampled conversations, not a proven motive for every Velantra buyer.'),
 prose(f'The refresh contains {len(POSTS):,} unique social posts and {len(COMMENTS):,} deduplicated comments. Instagram supplies {ST["comments_by_platform"]["instagram"]:,} comments; TikTok supplies {ST["comments_by_platform"]["tiktok"]:,}. The research begins with 167 supplied references and adds 480 new posts discovered through topic searches and seed creators. There are 214 available automatic Instagram transcripts.'),
 heading('The strategic distinction'),prose('Affordable luxury is the broad value position. The angles underneath it represent different reasons to care: discovering a less-obvious brand, elevating an outfit, rejecting a price premium, building a restrained wardrobe, dressing for a trip, or choosing a useful work bag. These should be tested as distinct motives rather than synonyms for one message.'),
 heading('What to prioritize'),prose('Start with outfit elevation, discovery, selective designer spending and personal taste beyond the logo. Use specific material and construction evidence to support those desires. Keep founder origin, gifting and male-approval messaging available as hypotheses with thinner direct evidence.'),
 heading('What the sample does not establish'),prose('These are public category conversations, not a verified Velantra customer panel. Sales, gender, country, income and purchase status are not confirmed by a handle or a comment. Engagement is a snapshot and cannot rank conversion performance. The report retains disagreement because it helps distinguish a useful audience segment from an overgeneralized claim.'),
 prose('Collection date: September 11, 2026. Available post dates span August 27, 2022 to September 11, 2026. Historical posts remain dated; this is not a trend forecast based only on recent content. Prior Velantra research remains preserved as a separate cohort.')])
# 2
page('Reading map and decision use',[
 tblock(['Pages','Contents'],[['1-8','Synthesis, method, language, contradictions and database use'],['9-40','Sixteen angle dossiers, each with interpretation and a separate evidence screen'],['41-90','Fifty selected source dossiers with short audience excerpts and traceable identifiers'],['91-95','Product applications and testing distinctions across the Velantra catalog'],['96-99','Complete supplied-link register and retrieval status'],['100','Collection manifest, source inventory and provenance']], [55,465]),
 heading('Choose an angle by the job it does'),prose('A creative brief should state a motive, the relevant audience context, the selected product and the evidence that makes the promise believable. The angle dossiers provide that starting point. Their product mappings are research recommendations, not validated statements about a product’s capacity, material grade or manufacturing origin.'),
 heading('Read both pages of each angle'),prose('The first page is an analyst-written interpretation with curated anchors. The second page is an evidence screen drawn from explicit comment-language matches. Those screens are labeled as candidate retrieval: a keyword can appear in disagreement, sarcasm or an unrelated detail. Use the original source and surrounding record before promoting a candidate into a claim.'),
 heading('Use the source dossiers for context'),prose('A post can attract agreement, objections and requests for links simultaneously. Each source dossier shows the collected and screened counts, creator context, a short caption excerpt and selected comments. Read these together rather than treating a single high-liked reply as a referendum on the whole audience.'),
 heading('Use the database for breadth'),prose('The full caption, available automatic transcript and exact comment text are retained in CSV, JSONL and SQLite. The PDF is the readable research layer. Source URLs, identifiers and raw export locations make it possible to inspect a quote, reclassify it or add future waves without losing its origin.')])
# 3
page('Sampling, quality and limits',[
 prose('The starting sample is a deliberately chosen creative-reference set. Expansion follows those creators and adjacent search terms. This is useful for discovering language and candidate angles, but it is not probability sampling. A result’s presence depends on what the platform and scraper returned, which sources had comments available and which posts were selected for deeper collection.'),
 tblock(['Record class','Count'],[[k.replace('_',' '),str(v)] for k,v in ST['signal_classes'].items()],[380,140]),
 prose(f'The lexical screen identifies {ST["audience_substantive_bag_candidates"]:,} audience-comment candidates on posts screened as handbag context. That is a review queue, not {ST["audience_substantive_bag_candidates"]:,} verified buying insights. Short replies may still be meaningful; longer replies can still be spam. Possible commercial endorsements are separately marked.'),
 prose('Seed Instagram collection requested up to 100 comments per post. New-post batches requested 80 or 100. TikTok requests used 80, 100 or 200. Embedded comments in metadata add another collection route; deduplication removes repeated comment IDs. Source membership is retained when a record appears in multiple waves.'),
 prose('Instagram and TikTok expose different slices and sorting behavior. The requested limit is not a guarantee that all comments were returned. Counts shown beside a post are reported platform totals, whereas collected counts describe the local sample. They should not be confused.'),
 prose('The purchase-status field records only whether the text contains a first-person ownership/purchase phrase. It does not verify a transaction or identify a Velantra customer. Cross-platform users are not assumed to be different people. The apparent cross-post of the bag-judgment concept is explicitly treated as related content.')])
# 4
page('Positioning, motives and execution formats',[
 prose('A broad position answers why the brand deserves consideration. An angle supplies a particular reason to enter that decision. An execution format determines how the idea is communicated. Mixing these levels makes a library look diverse while repeatedly asking the viewer to believe the same thing.'),
 tblock(['Level','Meaning','Example in this research'],[['Position','Overall value proposition','Affordable luxury, with timeless styling as brand context'],['Motive','Desired personal outcome','Look intentional while exercising taste and spending judgment'],['Angle','Reason to reconsider a choice','Discover a new bag brand; stop paying a prestige premium'],['Context','Where the desire becomes salient','European trip, commute, summer wardrobe'],['Proof','Why this product satisfies it','Verified design/material detail; actual fit; reliable seller evidence'],['Format','Presentation vehicle','Founder story, listicle, comparison, podcast or unboxing'],['Trigger','Reason to act now','Accurate availability, a relevant new color or an actual offer']],[62,192,266]),
 heading('Preserve the requested range'),prose('The research includes the requested seasonal, designer-comparison and conspiracy-related themes even where older internal copy rules discouraged those executions. Studying a theme does not establish its factual premise. No new ad, image, video, storyboard or edit is produced by this report.'),
 heading('Aspiration remains the lead'),prose('Product applications emphasize the desired look, silhouette, materials and wardrobe effect. Capacity and convenience are supporting reasons. The confidence branch should not be reduced to fear of judgment; the value branch should not presume that the buyer feels embarrassed about her finances.'),
 heading('One variable at a time'),prose('For a useful angle test, hold the selected model, offer and destination steady where possible. Changing the bag, styling, promise and price simultaneously may produce a winner, but it will not reveal which motive drove the difference.')])
#5
page('Customer language and the phrases behind it',[
 prose('Use short, traceable phrases to understand the thought pattern. Do not present these as Velantra testimonials. The wording below is drawn from category conversations and includes individual opinion, not independently verified product judgments.'),
 *qblock('igc:17902347504498071'),*qblock('igc:18086502293161610'),*qblock('igc:18120831529793735'),*qblock('igc:17983545684107015'),*qblock('igc:17879919228486307'),
 heading('Interpret the phrase before borrowing it'),prose('“Designer bag ick” describes aversion to an existing buying pattern. “Midluxury” is category shorthand for a middle position. “Timeless” invokes longevity of taste, but it does not prove physical durability. A personal-item-size request is a specific fit objection. Each belongs in a different part of the message.'),
 prose('Phrases such as quiet luxury, old money and expensive-looking recur in creator language as well as comments. Keep speaker roles separate. A creator saying that a look is desirable is a proposition; an audience member describing why she wants it is stronger evidence of the motive.')])
#6
page('Contradictions that should shape the messaging',[
 heading('Selling designer bags can fund another designer bag'),prose('On the “sold my designer handbags” seed, one viewer says she may sell some pieces to save for a Kelly. Designer fatigue can mean editing a collection rather than leaving the category. A blanket anti-designer interpretation would miss her desired outcome.'),*qblock('igc:18018691025696915'),
 heading('European style can invite resistance to rigid rules'),prose('A viewer on the Europe fall-packing seed resists the idea that visitors must become Parisian or Milanese. This matters for positioning the trip as enjoyable styling guidance rather than a social examination.'),*qblock('igc:17896322463662005'),
 heading('Founder interest can become an immediate fit question'),prose('The founder reference attracts intended-purchase language and a request for exact length. A story can bring attention while the product still has to pass practical evaluation.'),*qblock('igc:18094937147375384'),*qblock('igc:18004564757771553'),
 prose('The working implication is segmentation. Keep customers who love designer ownership, visible branding or backpacks visible in the database. They are not statistical noise. They help identify where a proposed message needs a narrower claim or a different product application.')])
#7
page('A research-led testing order',[
 tblock(['Priority','Test family','Learning objective'],[['First','Outfit elevation','Does a concrete styling effect create product interest?'],['First','New-brand discovery','Does unfamiliarity feel exciting once trust questions are answered?'],['First','Selective designer spending','Which value explanation respects the buyer’s taste?'],['First','Logo independence','Is the desired identity distinction, restraint or simply a liked shape?'],['Supporting','Quality and material proof','Which specifics resolve the actual hesitation?'],['Contextual','Work, travel and seasonal texture','Which model fits a distinct wardrobe job?'],['Exploratory','Founder and gifting','Does the proposed motive appear in owned customer responses?'],['Exploratory','Judgment and conspiracy','Does the premise hold, and does attention translate into a useful result?']],[62,170,288]),
 prose('This order is an analyst recommendation based on the available language and its fit with the requested brand direction. It is not a ranking of measured advertising performance. The corpus contains no campaign spend, attributed purchases, conversion rates or randomized test outcomes.'),
 heading('Record the outcome at the right level'),prose('Capture the selected product, message, proof, offer, audience and destination for each test. Read hook rate as an attention measure. Read click behavior as interest, and purchases and margin as business outcomes. Retain comments as qualitative context rather than treating them as the conversion denominator.'),
 heading('Use objections to design proof'),prose('Low-price skepticism asks for material evidence. Unknown-brand skepticism asks for credibility. Laptop questions ask for fit. Travel objections ask for a realistic carrying role. These are different uncertainties and should not all receive the same generic “premium quality” answer.'),
 prose('Before any later ad production, create or update the required editing plan and follow the workspace’s media and Cut Room instructions. This database supplies research for that phase; it does not substitute for an editing plan.')])
#8
page('Working with the searchable database',[
 tblock(['File','Use'],[['database/velantra-voc.sqlite','Searchable relational database: posts, comments and seed register'],['database/comments.csv / .jsonl','Exact text, IDs, source URLs, speaker role, flags and theme matches'],['database/posts.csv / .jsonl','Creator captions, automatic transcripts, dates, engagement and collection counts'],['database/discovered_posts.csv','All 480 posts beyond the supplied-link sample'],['database/seed_register.csv','Original notes, canonical URLs, duplicates and retrieval status'],['raw/*-items.json','Unmodified source exports; row locators in normalized records'],['raw/*-run.json and *-input.json','Run IDs, request settings, completion and actual charges'],['taxonomy.json','Exact regular expressions used for candidate retrieval']],[220,300]),
 heading('Useful search patterns'),prose('Filter comments by signal_class = substantive_candidate, category = handbag_context and evidence_role = audience_comment_purchase_unverified. Then search the text for a specific concern such as laptop, leather, too heavy or never heard. Join on post_id to read the creator’s caption and available transcript before interpreting the comment.'),
 prose('theme_tags match the comment itself. context_tags match the parent post’s caption/transcript. A context tag is not a statement that the commenter endorsed the theme. Seed notes preserve the original intended angle and are never used as proof of what the source actually said.'),
 prose('The same_text_count field exposes repeated phrasing across records. It is a screening aid, not a bot verdict. Likewise, possible-commercial-promotion flags do not prove a paid relationship. The raw text remains available for correction.'),
 prose('The database keeps historical research outside the new collection totals. Existing August 2 and August 31 men’s reports and raw CSVs remain at their original paths. Add future collection waves with persistent platform IDs, preserve provenance, and rerun the same classification transparently.')])
#9-40
for a in ANGLES:
 b=[prose(a['motive']),para(esc(a['priority']+' | '+a['instinct']),'small'),prose(a['finding']),heading('Potential Velantra application'),prose(a['application']),prose('Product candidates: '+a['products']),heading('Counterevidence and claim boundary'),prose(a['counter'])]
 for cid in a['evidence'][:2]:
  if cid in CS:b+=qblock(cid)
 b+=[heading('Test and missing evidence'),prose(a['test']),prose(a['gap'])]
 page(a['title'],b)
 cand=[c for c in GOOD if a['key'] in c['theme_tags'] and c['comment_id'] not in USED];cand.sort(key=score,reverse=True);take=[];counts=collections.Counter()
 # Curated third anchor first; then source-diverse lexical retrieval.
 for cid in a['evidence'][2:]:
  if cid in CS and cid not in USED:take.append(CS[cid]);counts[CS[cid]['post_id']]+=1
 for c in cand:
  if counts[c['post_id']]>=2 or c['comment_id'] in {x['comment_id'] for x in take}:continue
  take.append(c);counts[c['post_id']]+=1
  if len(take)>=9:break
 direct=[c for c in COMMENTS if a['key'] in c['theme_tags'] and c['signal_class']=='substantive_candidate' and c['category']=='handbag_context' and c['evidence_role']!='creator_reply']
 b=[prose(f'{len(direct):,} screened audience-comment candidates directly match this theme’s retrieval terms, across {len({c["post_id"] for c in direct})} posts. These are lexical matches, not validated motive frequencies. The excerpt screen below includes support, disagreement and questions.'),para('Open the linked source and read its post record before using a line. Speaker purchase status is unverified. Likes are collection-time snapshots.','small')]
 for c in take:b+=qblock(c['comment_id'])
 if len(take)<5:b+=[heading('Sparse direct evidence'),prose('The small number of relevant direct-language examples is itself a coverage gap. Creator narratives and category-adjacent comments remain available in the database, but do not fill it. The preceding interpretation is therefore a hypothesis to investigate with owned customer responses.')]
 page(a['title']+' | evidence screen',b)
#41-90 source selection
mandatory=['ig:DadwnM1hmXa','ig:DYPRepaNGq3','ig:DYSXIp6MRCO','ig:DcWLvteqezx','ig:DaAQeKXMGaz','ig:DbEHV44MYoJ','ig:DZf-NuYgpG-','ig:C7AKRw8Sy6U','ig:DbIhkWAMEWB','ig:DO8lWKXClxX','ig:DYU6BvfAVmQ','ig:DPG9kZ5kZWk','ig:DcgfD_ejl4-','ig:Dcgl2JFNPPf','ig:DbopI80TuC2','ig:Cl2HtNBtl03','ig:DSUPUC0iF5r','ig:DZ5YybMyYZp','tt:7668001244018986273','tt:7218302653489483051','tt:7681030709988969741','tt:7666956616465435918','tt:7627179930677333270','tt:7527006509264276766','tt:7652379521559137566']
selected=[];creatorcount=collections.Counter()
for pk in mandatory:
 if pk in PS and len(BYPOST[pk])>=3:selected.append(pk);creatorcount[PS[pk]['creator']]+=1
for p in sorted(POSTS,key=lambda p:len(BYPOST[p['post_id']]),reverse=True):
 pk=p['post_id']
 if pk in selected or len(BYPOST[pk])<4 or p['category']!='handbag_context':continue
 if creatorcount[p['creator']]>=3:continue
 if p['platform']=='tiktok' and sum(PS[k]['platform']=='tiktok' for k in selected)>=12:continue
 selected.append(pk);creatorcount[p['creator']]+=1
 if len(selected)==50:break
assert len(selected)==50,len(selected)
(ROOT/'selected-source-dossiers.json').write_text(json.dumps(selected,indent=2))
for n,pk in enumerate(selected,1):
 p=PS[pk];cs=[c for c in COMMENTS if c['post_id']==pk];sid=SOURCE_INDEX[pk]
 b=[para(f'<a href="{esc(p["url"])}">{sid} · {esc(pk)} · @{esc(p["creator"])}</a>','h'),para(f'{p["platform"].title()} · Published {p["published_at"][:10] or "unknown"} · {"Supplied reference "+p["seed_id"] if p["seed_id"] else "Discovered source"}','small'),
 prose(f'{p["comments_reported"]:,} comments reported by the platform; {len(cs):,} unique comments collected; {p["substantive_candidates"]:,} substantive audience candidates before manual interpretation. {p["likes"]:,} post likes and {p["views"]:,} reported plays/views at collection. Counts are exposure and retrieval context, not performance proof.'),
 heading('Creator context'),]
 cap=p['caption'];cap_tokens=list(re.finditer(r'\S+',cap));cap=cap[:cap_tokens[min(24,len(cap_tokens))-1].end()] if cap_tokens else '[No caption available]';cap=''.join(ch for ch in cap if (ord(ch) in pdfmetrics.getFont('ArialU').face.charToGlyph or ch in '\n\t') and unicodedata.category(ch)!='Cf' and ord(ch) not in [0xfe0e,0xfe0f])
 b+=[para(esc(cap)+' [creator-caption excerpt; display omits unsupported emoji]','quote'),para('Transcript: '+('automatic, unverified; full text in post record' if p['transcript'] else 'not available')+'. Source selection: relevant conversation with sufficient substantive candidates; independent creator variety.','small'),
 para('Post-context retrieval tags: '+esc(', '.join(p['theme_tags']) or 'none')+'. These describe matching language, not verified claims.','small'),heading('Audience excerpts')]
 candidates=sorted(BYPOST[pk],key=score,reverse=True);take=[c for c in candidates if c['comment_id'] not in USED][:9]
 for c in take:b+=qblock(c['comment_id'])
 if len(take)<4:
  b+=[prose('Additional comments from this source appear in the relevant angle pages. Repeated quotes are intentionally not used to inflate the evidence. The complete local record includes the full collected conversation slice and exact source locators.')]
 b+=[para('Read-through: these excerpts are a selected source notebook, not an assertion that every reply expresses a buying motive. The source can contain promotional, humorous, contradictory and unrelated reactions. Full source: '+esc(p['raw_refs'][0])+'.','small')]
 page(f'Source dossier {n:02} | {p["creator"]}',b)
#91-95 product applications
PRODUCT_PAGES=[
 ('Structured bags and a considered wardrobe',[
 ('Vivienne and Delphine','Discovery, old-money styling, European everyday style and outfit elevation are plausible research entries. Distinguish the selected model through its actual silhouette and details. A controlled styling comparison should reveal what the bag contributes to the look; the product name alone does not answer that question.'),
 ('Ingrid','Explore the relationship between a structured tote and feeling composed. Work polish and long-lived taste can be different entrances to the same product. Check the dedicated product records before making any capacity, aging or material claim.'),
 ('Portico and Rosalie','Use their own design identities rather than treating them as interchangeable alternatives to a famous bag. Individuality and the pleasure of choosing a less-obvious shape may be more appropriate hypotheses than generic old-money wording.')],
 'The new-brand evidence includes a concern that lesser-known designs may look too much like copies. The test should therefore make the positive reason for choosing a particular Velantra design visible. Heritage and quality equivalence are not established by resemblance.',
 'Compare outfit effect, discovery and price justification in separate message cells. Hold the model, color, styling quality and offer steady. Collect open-ended reasons for choosing that model over the other Velantra shapes.'),
 ('Totes, work polish and everyday style',[
 ('Meridian','The current registry uses Meridian; older research may call this family Margot. Use the registry mapping when joining old and new research. Work-bag positioning is a research hypothesis that still needs verified fit and material facts for the selected product.'),
 ('Camille','Differentiate an everyday carryall styling role from a weekend-transit role. The desired look may be casual and intentional rather than formal. Capacity should support that look, not replace the emotional reason to carry the bag.'),
 ('Ingrid as a comparison candidate','A second tote can help investigate which silhouette customers prefer, but changing product and message simultaneously prevents a clean angle comparison. Test the message on one model first, then assess product preference separately.')],
 'Laptop questions recur in the source material. A response needs device dimensions and an actual fit check, not a generic laptop-friendly label. The new research also preserves objections about weight and one-shoulder carrying.',
 'Ask what is carried on a normal day, which part of the outfit the buyer wants to improve, and what would make the bag uncomfortable. Record the practical requirement and the desired identity as separate fields.'),
 ('Texture-led seasonal desire',[
 ('Sofia','The Sofia Woven Tote belongs in a distinct summer-texture conversation. Use source reactions to learn which visual details feel desirable, expensive-looking or too delicate. Do not transfer complaints about a different woven product into assertions about Sofia.'),
 ('Colette','The Colette Wool Tote gives the research a different material and seasonal context. Investigate how the chosen texture complements coats, knitwear and the intended wardrobe. The material named by the product does not by itself prove durability or care requirements.'),
 ('Juliette','The Juliette Suede Tote deserves its own tactile and styling questions. A softer visual treatment, if supported by the actual selected product, can appeal for different reasons from a structured top handle. Verify current product details before production.')],
 'The summer-reference sample contains substantial link-request traffic. It supplies creative breadth but does not prove that a named bag was the season’s sales leader. Seasonal appeal should be analyzed independently from material-value objections.',
 'Compare a seasonal wrapper against an evergreen texture-and-outfit message. Preserve the chosen bag and presentation quality. Ask shoppers to name the detail that makes the piece feel right for the season rather than prompting them with the intended adjective.'),
 ('Eleanor, the trip and the large-bag identity',[
 ('Eleanor Weekender','Separate aspirational departure, a coordinated travel look and the desire to carry a larger bag. Each can start a different conversation. The desired travel image is the lead; capacity, closure, dimensions and carrying method need direct proof.'),
 ('European fall trip','The occasion is more specific than general European styling. Record destination, length of trip, transport and daily activities before deciding which bag role is being sold. A stylish airport arrival and all-day sightseeing can require different choices.'),
 ('Men’s travel context','The prior men’s research remains useful historical material. Its counts are not mixed into this refresh. Do not infer that a gender or identity concern has disappeared market-wide because it appeared infrequently in a particular comment scrape.')],
 'The strongest opposing travel comments favor backpacks for comfort and convenience. That does not defeat a weekender proposition; it establishes the need to define when the bag is meant to be carried. Do not promise to replace every other travel bag.',
 'Test style-led travel against preparation-led travel on the same product and load. Ask which part of the journey the buyer imagines using it for. Validate physical scale and actual packing before claiming either carry-on or personal-item compatibility.'),
 ('Accessories, gifting and the collection destination',[
 ('Bag Scarf, Cherry Charm and Horse Charm','These can be investigated as styling additions and expressions of personal taste. The evidence here is principally about bags, so accessory-specific motives remain hypotheses. Do not assume that a bag buyer wants a charm or scarf without testing.'),
 ('Boat Tote Keychain and Bag Organizer','Treat these as different propositions. A keychain can participate in gifting or collection identity; an organizer may answer a practical need. Product compatibility and fit require current evidence. Function should not silently become the lead for the whole fashion brand.'),
 ('Collection versus product destination','Discovery can reasonably lead to a range of shapes, while a precise fit or material promise may need a specific product page. Compare those routes deliberately. A collection page should help a shopper recognize the model and style direction that brought her there.')],
 'Gifting evidence is thin and category-adjacent examples include fragrance and jewelry. Those references can inspire research questions, but cannot supply handbag-recipient satisfaction or Velantra social proof.',
 'Ask whether the purchase is for the buyer or someone else, how the recipient’s taste was inferred, and which detail made the choice feel personal. Test accessory interest as a separate decision rather than interpreting a bundle purchase as proof of a styling motive.')]
for title,sections,boundary,test in PRODUCT_PAGES:
 b=[prose('Product mappings are analyst recommendations for research and testing. Product names come from the September 4 catalog registry. Current prices, inventory, specifications and performance are not verified by this report.')]
 for name,s in sections:b+=[heading(name),prose(s)]
 b+=[heading('Evidence boundary'),prose(boundary),heading('Next useful test'),prose(test),para('Internal sources: brands/velantra/product-skills/registry.json; brands/velantra/ops/claude-project-instructions.md. Older brand architecture is retained for context; current product records and explicit updated instructions take precedence.','small')]
 page(title,b)
#96-99
for n in range(4):
 subset=SEEDS[n*42:(n+1)*42]
 data=[]
 for s in subset:
  tail=s['url'].rstrip('/').split('/')[-1];label=SOURCE_INDEX.get(s.get('post_id'),'--');data.append([s['seed_id'],f'<a href="{esc(s["url"])}">{esc(tail)}</a>',esc(s['actual_creator'] or s['platform']),str(s['comments_collected']), 'Yes' if s['status']=='retrieved' else 'No'])
 page(f'Supplied-source register | {n+1} of 4',[
 prose('Every unique supplied URL is retained, including references outside handbags. “Retrieved” means a usable post record was returned. The original annotations and repeated-link counts are preserved in database/seed_register.csv; they are not factual summaries of the source.'),
 tblock(['Seed','Source link / shortcode','Creator or platform','Cmts','Retrieved'],data,[38,132,260,36,54]),
 para('Unavailable Instagram posts: S029 (DbAfK_wgaqj) and S050 (DbJW8B9AHqf), returned not found. S076 TrendTrack and S154 X were not retrieved through the available public web fetch. Their original reference intentions remain unverified.','small')])
#100
page('Sources, collection record and reproducibility',[
 prose(f'All 13 Apify runs completed successfully. Reported actor charges total ${COST:.4f}. These are the run-level usageTotalUsd values; they are not a separately reconciled account invoice. Raw exports, input requests, build schemas and completion records are retained locally.'),
 tblock(['Wave','Run ID','USD'],[[r['wave'],r['id'],f'{r.get("usageTotalUsd",0):.4f}'] for r in RUNS],[236,215,69]),
 heading('Full source inventory'),prose('database/posts.csv is the complete source catalog: original URL, creator, publication date, platform, caption, available transcript and raw export references. database/comments.csv adds exact comment text, source link and identifier. Each PDF excerpt links to its comment or parent post and carries a comment ID. TikTok comment links use the post URL plus that ID; individual-comment resolution is not claimed.'),
 heading('Research methods and internal context'),para('<a href="https://apify.com/apify/instagram-scraper">Apify Instagram Scraper</a>; <a href="https://apify.com/apify/instagram-comment-scraper">Instagram Comments Scraper</a>; <a href="https://apify.com/apify/instagram-reel-scraper">Instagram Reel Scraper</a>; <a href="https://apify.com/apify/instagram-search-scraper">Instagram Search Scraper</a>; <a href="https://apify.com/clockworks/tiktok-scraper">Clockworks TikTok Scraper</a>; <a href="https://apify.com/clockworks/tiktok-comments-scraper">TikTok Comments Scraper</a>. Live input schemas and run settings are saved in raw/.','small'),
 prose('Brand context: Velantra ops/claude-project-instructions.md; product-skills/registry.json; research/positioning/2026-07-28-brand-architecture.md; research/voc/2026-08-02-mens-travel-bag-voc.md and 2026-08-31-mens-voc-v2.md. These are internal records, not independent verification of product claims. Prior raw comment exports remain in the same research/voc folder.'),
 prose('Report limitations: automatic transcripts were not manually audio-verified; visual frames were not audited; sentiment and theme matches are not market prevalence; public claims and individual allegations are not independently established. The report is intended to guide grounded research and messaging tests.')])
assert len(PAGES)==100,len(PAGES)
# Render with measured page layouts and a readable minimum scale.
pdf=canvas.Canvas(str(OUT/'Velantra-Voice-of-Customer-100-Pages.pdf'),pagesize=(612,792));pdf.setTitle('Velantra voice of the customer')
qa=[];md=[]
for i,p in enumerate(PAGES,1):
 blocks=[('p',esc(p['title']),'title')]+p['blocks'];flows=[]
 md+=['# '+p['title'],'']
 for b in blocks:
  if b[0]=='p':
   flows.append(Paragraph(b[1],styles[b[2]]))
   if b[2]!='title':md+=[mdclean(b[1]),'']
  else:
   _,headers,data,widths=b
   cells=[[Paragraph('<b>'+esc(h)+'</b>',styles['cell']) for h in headers]]+[[Paragraph(str(c),styles['cell']) for c in r] for r in data]
   tb=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),('LINEBELOW',(0,0),(-1,0),.5,colors.grey),('BOTTOMPADDING',(0,0),(-1,-1),1.5 if headers[0]=='Seed' else 5),('TOPPADDING',(0,0),(-1,-1),1.5 if headers[0]=='Seed' else 5)]));flows.append(tb);flows.append(Spacer(1,8))
   md+=[' | '.join(headers),' | '.join(['---']*len(headers))]+[' | '.join(mdclean(str(c)) for c in r) for r in data]+['']
 def total(width):
  return sum(f.wrap(width,2000)[1]+getattr(f,'getSpaceBefore',lambda:0)()+getattr(f,'getSpaceAfter',lambda:0)() for f in flows)
 h=total(520);scale=min(1,698/h)
 # When content is taller, reduce uniformly but flag anything below .84 for revision.
 qa.append({'page':i,'title':p['title'],'height':round(h,1),'scale':round(scale,3)})
 pdf.bookmarkPage('page'+str(i));pdf.addOutlineEntry(p['title'],'page'+str(i),level=0)
 pdf.saveState();pdf.translate(46,756);pdf.scale(scale,scale);y=0
 for f in flows:
  w,hh=f.wrap(520,2000);y-=getattr(f,'getSpaceBefore',lambda:0)();y-=hh;f.drawOn(pdf,0,y);y-=getattr(f,'getSpaceAfter',lambda:0)()
 pdf.restoreState();pdf.setFont('ArialU',8);pdf.setFillColor(colors.grey);pdf.drawRightString(566,24,str(i));pdf.setFillColor(colors.black);pdf.showPage()
pdf.save()
(OUT/'Velantra-Voice-of-Customer.md').write_text('\n'.join(md))
(OUT/'layout-qa.json').write_text(json.dumps(qa,indent=2));(OUT/'quote-audit.json').write_text(json.dumps(QUOTE_LOG,ensure_ascii=False,indent=2))
(ROOT/'angle-dossiers.json').write_text(json.dumps(ANGLES,ensure_ascii=False,indent=2))
# Human-readable source IDs used by the report.
with (DB/'report-source-index.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['report_source_id','post_id','creator','published_at','url']);w.writerows([SOURCE_INDEX[p['post_id']],p['post_id'],p['creator'],p['published_at'],p['url']] for p in POSTS)
print(json.dumps({'pages':len(PAGES),'quotes':len(QUOTE_LOG),'min_scale':min(x['scale'] for x in qa),'crowded_pages':[x for x in qa if x['scale']<.84],'cost':COST},indent=2))
