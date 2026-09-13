"""Publish manually authored cohorts; validate quotations; serialize manual dispositions.
No text classifier, embedding model or keyword assignment is used here.
"""
import csv, json, re
from pathlib import Path
from collections import defaultdict, Counter
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[2]
records=json.loads((HERE/'quote-review-records.json').read_text())
byid={q['review_id']:q for q in records}
anchors=[]
source=(HERE/'cohorts.template.md').read_text()
# Correct the repeated Q282 excerpt so the combined selected wording stays short.
source=source.replace('That burgundy is gorgeous btw but I already have a Tod’s in Burgundy.', 'but I already have a Tod’s in Burgundy.')
def quote(m):
    q=byid[m[1]]; s=m[2]
    assert s in q['full_text'], (m[1], 'not an exact substring', s, q['full_text'])
    assert len(s.split())<=25,(m[1],len(s.split()))
    before=source[:m.start()]
    match=list(re.finditer(r'<a id="c(\d+)"',before))
    cohort='C'+match[-1][1]
    anchors.append(dict(review_id=q['review_id'],cohort=cohort,excerpt=s,comment_id=q['comment_id'],post_id=q['post_id'],source_url=q['source_url'],exact_contiguous=True,words=len(s.split())))
    pages=', '.join(map(str,q['report_pages']))
    return f'> {s}\n\n[Source {q["review_id"]}](<{q["source_url"]}>) · `{q["comment_id"]}` · under @{q["creator"]} · report p. {pages}. Exact excerpt.'
rendered=re.sub(r'\{\{(Q\d{3})::(.*?)\}\}',quote,source,flags=re.S)
(RESEARCH/'cohorts.md').write_text(rendered)
(HERE/'cohort-anchor-audit.json').write_text(json.dumps(anchors,ensure_ascii=False,indent=2)+'\n')
assignments=defaultdict(list)
def group(spec,role,cohorts,note):
    for token in spec.replace(' ',',').split(','):
        if not token: continue
        if '-' in token:
            a,b=map(int,token.split('-')); nums=range(a,b+1)
        else: nums=[int(token)]
        for n in nums:
            assert 1<=n<=603
            assignments[f'Q{n:03}'].append(dict(role=role,cohorts=cohorts.split() if cohorts else [],note=note))
# Every group below is an explicit editorial decision after full-comment reading.
# A support entry is evidence of a motive, not verification of a person's membership.
group('1-2,173','support','C03','Designer-spending discussion: dissatisfaction or satisfaction with midrange alternatives; these are same-thread signals, not independent studies.')
group('3,169,204,228','support','C07','Timeless preference, deliberate purchase delay, continued use or refusal to replace a loved bag merely for a trend.')
group('4','context','','Commenter generalizes about European behavior; do not infer population-level habits or actual purchase motive.')
group('5,9,64,130-132,140,217,221-225','decision_condition','C10 C11','Specific fit, device, carrying or luggage question; useful product requirement, not proof of current Velantra capacity.')
group('6','support_and_boundary','C07 C17','Selling some designer pieces to save for a Kelly; selective collecting rather than designer abandonment.')
group('7,34,36,50,62,66,78-80,112-115,117,133,205-206','support','C13','Defends personal choice or particular styles; do not count as endorsement of universal logo, city or approval rules.')
group('8','purchase_intent','','Payday purchase intent for hoodie and duffel, not evidence that a founder story caused the decision.')
group('10,15,43,45,70,111,273,275,316,324','support','C04','Preference for less-obvious bags, discovery, creative design or an uncommon choice; strength varies from a specific reason to positive discovery response.')
group('11,33,83,91,143,159-161,163,166','decision_condition','','Quality, authenticity, transaction or seller uncertainty. Retain context; these do not establish industry-wide deception or verified faults.')
group('12,95,229','boundary','C02 C04','Rejects close copying or objects to derivative design; an unfamiliar designer alternative is not automatically acceptable.')
group('13','context','','Sarcastic or skeptical response in a resale/scam discussion; not a positive new-brand discovery statement.')
group('14,16-20','transaction_only','','Brand/link/purchase-location request without enough stated motive to assign a persona.')
group('21','exclude','','Founder revenue speculation, not buyer motivation or verified financial evidence.')
group('22-23','exclude','','Seller self-promotion or another designer discussing their own business; do not infer buyer founder loyalty.')
group('24-25,31,177,208,279,311,314,415,452,461,561','support','C02','Explicit budget pressure, price/access question or response to inaccessible luxury; not evidence of income or willingness to switch to Velantra.')
group('26,282','support','C08 C17','Milestone purchase memory; Q282 also evaluates a new color relative to an existing collection. Designer context is preserved.')
group('27,67-69,76,391,394','support','C05','Prioritizes personal style or the combination of bag and outfit; some entries are requests or critiques rather than completed purchases.')
group('28,32,44,73,108,116','unverified_claim','','Value, manufacture, status or price-hype assertion; no basis to treat it as a verified category fact or distinct conspiracy cohort.')
group('29,100-101,106,121,127,219,236,254,276,294,317,460,585','support_or_requirement','C09','Material, construction, surface-care or durability evaluation. Alleged quality failures are unverified and concern the referenced category product.')
group('30,128','price_context','','Price assertion/correction without a personal motive; historical source figure not a verified current price.')
group('35,110,266-267,269,534-536,540','support','C01','Restrained branding or admiration for composed elegance; style-interview praise is broader than a handbag purchase and does not prove wealth.')
group('37-40,55,197','boundary','C03 C07','Defends established designer style, quality or longevity. Reported experience is not proof for Velantra and does not support designer exit.')
group('41,122,256','context','C07','Trend-cycle or hype observation; weaker than an explicit personal decision to buy or abstain.')
group('42','limited_style_signal','C01','Calls Léo et Violette classic; a style preference without an explicit purchase reason.')
group('46-47,52,54,61,338-342','boundary','C01 C18','Disputed geographic/style rule or counterexample; not reliable population evidence. Named style figures here do not demonstrate imitation intent.')
group('48,59,85,105,107,135-136,138,141,146','boundary','C10 C11','Comfort, weight, carrying or value objection, often favoring backpacks; does not establish a tote solution or universal travel preference.')
group('49','weak','','Negative preference with little explanation; no reliable motive inferred.')
group('51','context','','Design comparison without a clear statement of purchase desire.')
group('53','transaction_only','','Shipping geography is a logistics question, not European-style aspiration.')
group('56-57,123,180-187,318,383','limited_context','C18','Destination, timing or seasonal purchase context. Some may be shopping at the destination; narrower pre-trip handbag motive remains unproven.')
group('58,104,380,411','support','C12','Travel purchase, memory, place-of-making preference or attraction to the shopping experience; transfer to an online Velantra purchase is uncertain.')
group('60','context','','Speculates about other people carrying real versus fake bags; not a self-reported travel motive.')
group('63,145,179,370,381-382,385,387','destination_shopping','C12','Destination prices or purchase logistics; adjacent to a travel-memory cohort but not proof of sentimental motive or pre-departure purchase.')
group('65','style_rule_context','','Declares that vanity cases belong inside luggage, a prescriptive style opinion without a personal purchase motive.')
group('71,74,167,264,352-354,356,359-360,416,431,454','style_filter','C05 C06','Specific shape, color, logo, practicality or taste evaluation; useful style boundary, not a demographic or evidence of creator agreement.')
group('72,390,406','limited_association','C19','Named character/celebrity style association without explicit imitation purchase. Both Blair comments share a parent post.')
group('75,84,86,96,129,153-156,194,199,201,207,211,215,230,235','exclude','','Unrelated product/person discussion, creator-line repetition, adjacent category or named-person mention that does not establish a handbag buyer motive.')
group('77','weak','','Generic content praise, possibly commercial context; no specific handbag buying motive established.')
group('81-82,478,480-481','recipient_context','C14','Gift/partner appreciation in audience language; not direct evidence of the giver decision or male approval as a motive. Some are Malay and not quoted in the cohort cards.')
group('87,97','value_context','','Price or selection criticism; limited basis for a distinct personal buyer history.')
group('88,137,323,325,397-398,401,405','support','C10','Work, study or training requirements linked to style or an attractive carrying option. Product capability must be checked separately.')
group('89,253,257','skepticism_condition','','Scarcity or marketing skepticism. Allegations remain unverified and do not establish industry corruption.')
group('90,99,120,171,175,371-374,376-377,423','resale_value_context','C02','Seeking designer value, resale or transaction information; some want the original label. Replica/factory allegations are not facts or proof of switching intent.')
group('92,343-351','transaction_response','','Reseller complaint, skepticism or dispute advice. Trust context, not a new persona or verified allegation.')
group('93,293,310,321','context','','Celebrity, designer or authenticity discussion without clear desire to imitate a person. Q293 is explicitly a vendor claim.')
group('94,289,291-292,296-297','replica_context','','Authenticity/replica evaluation or price assertion; do not convert into verified quality equivalence or a Velantra buyer identity.')
group('98,109,192,487-488,490-491,494','qualified_value_context','C03','Contains spending/value criticism but also replicas, manufacture assertions or broader values. Preserve the full context and treat allegations as unverified.')
group('102','weak','','Product joke rather than verified material behavior or a clear buying motive.')
group('103','context','','Authenticity stitching debate, not measured durability evidence.')
group('118,124','decision_condition','','Hardware care or carrying orientation for security; do not mistake practical reasons for anti-logo identity.')
group('119,126,165,232,242,244-246,248,250-251,363-368,399,409,440,447,514-516,520-522,559-560,565-566,598','support_or_style_signal','C06','Specific visual attraction to color, finish, shape, texture or personalization; generic/promotion-like examples are weaker than self-reported choice. Q165 has possible promotional language.')
group('125,150-152,288,400,462','gift_evidence','C14','Gift intent, recipient reaction or giver report. Preserve negative outcomes and functional limitations; not all are gift-giver statements.')
group('134,322','support','C10','Self-reported work/laptop use of a named category bag; not verified product performance for Velantra.')
group('139,142,149,233-234,378,508,544,546-548','support','C15','Interest in men’s bags, styling, first purchase or acceptance. Identity and job details apply only where explicitly stated.')
group('144','exclude','','Repeats creator snack wording; not an independently expressed bag capacity requirement.')
group('147','weak','','Generic travel/adventure reaction without a clear bag-specific motivation.')
group('148,274,290','qualified_support','C02','Lower-price or similar-look preference; replica/alternative context and quality tradeoffs must remain visible.')
group('157-158,209,247,252,255,259-261,312,463,468,493,495,524-525,527,586-587,590,596,600-601','decision_condition','','Stock, delivery, policy, checkout, website or shipping issue; no persona assigned merely from the complaint/request.')
group('162,168,174,227,281,287,384,436,471','support','C17','Collection ownership, pleasure, an additional purchase or distinct occasion/style roles. Buying for use and buying for financial investment are different.')
group('164','support','C01 C02','Self-reported quiet-luxury-thread purchase at a sale price; supports attainable satisfaction without verifying general price levels.')
group('170','decision_condition','C07','Wishlist/decision tool context, weaker than an explicit intentional-purchase motive.')
group('172,188-189,202,249,268,271,277-278,280,283,285-286,303,307-309,313,315,319,330,386,403,435,439,443-446,448-450,453,457-459,469-470,475,489,492,496,504,517,519,526,528,530,533,538,553-554,556,562,568,571-575,578,580-581','limited_or_transaction_signal','','Product admiration, recommendation, ownership, wish or transaction interest without enough independent motive to create another cohort; consult full context before use. Some could support an existing card secondarily.')
group('178,210,212-213,216,218,220,223,226,231,239-243','limited_or_requirement','','Specific product/fit interest or preference, insufficient as a distinct persona anchor; no new cohort inferred.')
group('190-191,193,195-196','adjacent_values_context','','Lifestyle/wealth/consumption discussion rather than direct handbag purchase evidence. Do not infer a career, wealth level or motive for the full audience.')
group('198','values_condition','','Explicit smaller-label, quality and fair-wage preference; different from vegan materials or founder fandom. Velantra practices unverified here.')
group('200,203','weak','','Aesthetic dislike without enough explanation to assign a distinct motive.')
group('214,320,442,595','support','C16','Explicit animal-material avoidance or preference for vegan alternatives; product eligibility requires full composition, not appearance.')
group('237','qualified_requirement','','Wants to see lining but also aspires to start a leather company; not clean consumer-only evidence.')
group('238,414,421,584','exclude','','Seller or brand promotion; not independent consumer evidence.')
group('258','unverified_claim','C09','Strong claim about another product\'s leather/workmanship without independent verification; material concern is relevant, allegation is not established.')
group('262-263,265,270,302,335,355,357-358,432','support','C13','Defends a personally liked bag or freedom of choice against fashion rules; do not treat as agreement with the source creator.')
group('272','decision_condition','C09 C10','Closure usability question based on hearsay; answer with direct product evidence.')
group('284','decision_condition','','Size identification request, not a persona by itself.')
group('295','qualified_style_signal','C02','Affection for a street-market bag in a fake-bag discussion; limited evidence for an attainable-look motive.')
group('298-301,304-306,424-429','judgment_reaction','','Humor, ratings, disagreement or repeated creator wording. Some approval exists, but buying to gain male approval is not demonstrated.')
group('326-327,329,332-333,549,599,603','boundary','C10 C11','Backpack preference, load, size or carrying-comfort objection. Do not assume every appearance-focused buyer accepts the tradeoff.')
group('328','support','C11','Explicit wish to look cute at the airport while acknowledging that backpacks have a role.')
group('331','requirement','C11','Self-reported large-tote preference/use; practical signal rather than a full persona.')
group('334','context','','Sarcastic sunglasses response to a logo rule, not a bag-purchase motive.')
group('336','qualified_context','C03','Suggests a non-logo alternative but adds an unverified quality allegation.')
group('337','boundary','C01 C18','Explains bag orientation by theft concern rather than a style rule; no product theft-prevention evidence.')
group('361-362','weak','C05 C06','Praises video aesthetics or outfit confidence; weaker than a direct handbag motive and possible engagement-style wording.')
group('369,375,434,438,464-467','transaction_only','','Product link, size, identity, shipping or purchase question; does not establish a new persona.')
group('379','wish_context','C17','Product already on a wishlist; possible collection interest without a distinct reason.')
group('388-389,392-393,395-396','context','','Style interview reactions, identity questions or social commentary; do not infer audience demographics or bag-buying motives.')
group('402','limited_social_reward','C05 C06','Reports another person admiring the bag; category social-response evidence, not a promised Velantra outcome.')
group('404','exclude','','Explicit PR-list request; possible creator/commercial motive rather than independent purchase evidence.')
group('407-408,410,412-413','destination_context','C12','Price or shop context in Florence; not sufficient alone for a memory-driven buyer persona.')
group('417','limited_requirement','C10','Exaggerated humorous self-description about carrying many things; real packing capacity cannot be inferred.')
group('418','design_suggestion','','Asks a designer to reinterpret shopping bags; suggestion rather than an established cohort.')
group('419-420,422','exclude','','Video count, appearance or sarcastic content reaction unrelated to a clear handbag choice.')
group('430','boundary','C01 C04','Describes quiet-luxury distinctiveness as performative; low-logo styling does not guarantee positive reception.')
group('433,437','seller_history','','Recalls the creator selling unique bags; not clean consumer evidence for a new buyer persona.')
group('441,474','exclude','','Creator appearance or video-production praise, not a bag motivation.')
group('451','boundary','','Challenges a handmade-versus-luxury premise; no manufacturing claims are verified by this comment.')
group('455-456','qualified_value_context','C03','Designer-overrated opinion or agreement under a small-maker post; no personal designer-exit history established.')
group('472','proof_request','C11','Asks to see normal-speed packing, a useful evidence request rather than a persona.')
group('473','boundary','C02 C03','Defends expensive luggage and rejects compromise; cannot assume all viewers want a lower price.')
group('476-477','decision_condition','C11','Weight-limit experience and modular packing/value critique; not current policy advice or evidence of Velantra capability.')
group('479,482-483,485-486','context','','Brand list, well wishes, brand confusion or buying-location question; no clear new persona motive.')
group('484','adjacent_influence','C19','Malay clothing-purchase influence comment; adjacent creator influence, not handbag imitation evidence.')
group('497-503','context','','Hypothetical bag-versus-partner choices, insults and resale jokes; no verified gifting, investment or male-approval cohort.')
group('505','unverified_claim','','Generalizes about expensive luggage owners flying private/first; do not infer income or travel behavior.')
group('506-507,510-513','adjacent_or_generic','','Candles, shoes, clothing or general content reaction; not handbag-specific persona evidence.')
group('509','security_concern','C11','Belief that conspicuous expensive luggage attracts theft; no factual theft reduction claim is supported.')
group('518','humor','','Joke about a thrift filming scenario; not purchase evidence.')
group('523','language_preference','','Objects to personifying bags; useful voice preference, not a buyer cohort.')
group('529,531','trust_condition','','Questions repetitive praise and actual ownership; do not treat all positive comments as verified reviews.')
group('532','exclude','','Unrelated religious passage; no handbag persona inferred.')
group('537,539','context','','Accent/name observation; no handbag buying motivation or verified class identity.')
group('541-543,545,582','boundary','C15','Gendered resistance to men carrying the shown bag. Preserve as objection, not a demographic or sexuality inference.')
group('550-552,555,557-558','limited_context','C05 C10','Content praise or visual capacity reaction; no tested capacity and no full purchase motive. Product/creator engagement may influence wording.')
group('563-564','weak','','Style dislike or repeated rating/repurchase wording; do not assume a verified owner experience.')
group('567,569-570,576-577,579,583','adjacent_or_transaction','','Other-item request, brand reply, travel greeting, expense joke or briefcase location question; insufficient distinct persona evidence.')
group('588-589,591-594','adjacent_or_incomplete','','Clothing/fragrance stock questions, an incomplete sentence or lookbook request; not a handbag cohort.')
group('597,602','decision_condition','C10 C11','Crossbody attachment or lunch-box fit request; verify exact SKU rather than extrapolating from appearance.')
group('176','qualified_support','C03 C07','Expresses designer ick but asks which bags the creator kept; permits collection editing rather than assuming complete designer exit.')
# Selected anchors receive a separate explicit anchor role, not automatic text tagging.
for a in anchors:
    assignments[a['review_id']].append(dict(role='selected_anchor',cohorts=[a['cohort']],note='Exact excerpt selected in the manually authored cohort card; read its accompanying interpretation and boundary.'))
missing=[q['review_id'] for q in records if q['review_id'] not in assignments]
assert not missing,missing
out=[]
for q in records:
    ds=assignments[q['review_id']]
    out.append(dict(review_id=q['review_id'],comment_id=q['comment_id'],post_id=q['post_id'],report_pages=q['report_pages'],source_url=q['source_url'],reviewed_full_comment=True,cohorts=sorted(set(c for d in ds for c in d['cohorts'])),dispositions=ds,selected_anchor=any(d['role']=='selected_anchor' for d in ds)))
(HERE/'quote-cohort-ledger.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
with (HERE/'quote-cohort-ledger.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['review_id','comment_id','post_id','report_pages','source_url','reviewed_full_comment','cohorts','roles','review_note','selected_anchor'])
    w.writeheader()
    for q in out:
        w.writerow({**{k:q[k] for k in ['review_id','comment_id','post_id','source_url','reviewed_full_comment','selected_anchor']},'report_pages':';'.join(map(str,q['report_pages'])),'cohorts':';'.join(q['cohorts']),'roles':';'.join(dict.fromkeys(d['role'] for d in q['dispositions'])),'review_note':' / '.join(d['note'] for d in q['dispositions'] if d['role']!='selected_anchor')})
lines=['# Review ledger: all 603 report quotes','','Reviewed September 11, 2026. Every row corresponds to a unique report comment whose full stored text was read. Cohort links indicate where a statement is useful, including as counterevidence; they do not assign a verified person to a segment. All dispositions are manually specified. No clustering or keyword-based assignment was used.','','[Cohort guide](../../../cohorts.md) · [Detailed notes](manual-review-notes.md) · [CSV](quote-cohort-ledger.csv) · [Full source text](quote-review-records.json)','','`Support` and `selected_anchor` are distinct from conditions, boundaries, context and exclusions. A comment can have more than one role. Selected anchors in the guide include contextual qualifications.','','| Quote / original source | Report page | Cohorts | Review disposition and reason |','|---|---|---|---|']
for q in out:
    ds=[d for d in q['dispositions'] if d['role']!='selected_anchor']
    roles='; '.join(dict.fromkeys(d['role'] for d in ds))
    notes=' / '.join(dict.fromkeys(d['note'] for d in ds))
    cs=', '.join(f'[{c}](../../../cohorts.md#{c.lower()})' for c in q['cohorts']) or 'No cohort assigned'
    marker=' **Card anchor.**' if q['selected_anchor'] else ''
    lines.append(f'| [{q["review_id"]}](<{q["source_url"]}>) `{q["comment_id"]}` | {", ".join(map(str,q["report_pages"]))} | {cs} | **{roles}**. {notes.replace("|","/")}{marker} |')
(HERE/'quote-cohort-ledger.md').write_text('\n'.join(lines)+'\n')
summary={'report_pages_reviewed':100,'unique_full_comments_reviewed':len(out),'cohort_cards':19,'exploratory_cards':['C18','C19'],'anchor_occurrences':len(anchors),'unique_anchor_comments':len(set(a['comment_id'] for a in anchors)),'all_excerpts_exact_contiguous':all(a['exact_contiguous'] for a in anchors),'max_excerpt_words':max(a['words'] for a in anchors),'all_report_comments_have_manual_dispositions':not missing,'assignment_method':'explicit manually authored record groups and card selections; script only serializes and checks','main_markdown_words':len(rendered.split()),'source_scope_note':'603 unique report comments; not manual review of all 16,437 collected comments'}
(HERE/'cohort-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
