#!/usr/bin/env python3
"""MOT-VID-012 schedule builder: cue phrases -> timecodes off the paced VO; writes schedule.json,
the numbered asset folder, the Cutroom spec, and the brief's Visual Schedule block."""
import json,re,os,shutil,sys
ROOT="/Users/brooksorradre2/Documents/marketing brain"
D=f"{ROOT}/brands/motilli/creative/MOT-VID-012"
W=json.load(open(f"{D}/vo/words_final.json"))
words=W["words"]; DUR=W["duration"]
norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower().replace("-"," ")).split()
nw=[norm(w["w"]) for w in words]; flat=[]; 
for i,ws in enumerate(nw):
    for t in ws: flat.append((t,i))
def find(phrase, after=0.0):
    p=norm(phrase); n=len(p)
    for k in range(len(flat)-n+1):
        if [t for t,_ in flat[k:k+n]]==p and words[flat[k][1]]["s"]>=after-0.05:
            return words[flat[k][1]]["s"]
    raise SystemExit(f"CUE NOT FOUND: {phrase!r}")
def tc(t): return f"{int(t//60)}:{t%60:04.1f}"
def tcs(t): return f"{int(t//60)}:{int(t%60):02d}"
LIB=json.load(open(f"{D}/library-frames/index.json"))
NURSE=f"{D}/avatar/nurse_cand_1.png"
LABEL=f"{ROOT}/brands/motilli/celery juice gummies/brand/website-assets/label 1.png"
G=lambda n: f"{D}/keyframes/g{n}.png"
# type, cue, intent, source(kind,key), pip?, extra note
B=[
("CARD","If you're taking Mounjaro","The four real pens, first frame. TOP BANNER (editor GFX) reads 'The organ your GLP-1 stack is missing' and holds 0:00 to about 0:07, red box top-center like the reference.",("gen",101),False,"Alt Use: Broll folder, the Ozempic box and pen clip."),
("UGC","haven't gone in days","Her, in the hallway, hand on her stomach. Real footage.",("lib","broll_07_constipation_hallway"),False,""),
("CARD","still stir Miralax","MiraLAX going into the coffee, real jar in frame. Lands on 'Miralax'.",("gen",102),False,"Alt Use: Broll folder, MiraLAX jar and glass clip."),
("UGC","fiber gummies","Real Metamucil Fiber Gummies in hand. Real footage.",("lib","broll_34_metamucil_gummies"),False,"Trim to the bottle-in-hand moment only."),
("CARD","magnesium, and a probiotic","The nightstand: magnesium, Align, water glass.",("gen",103),False,""),
("CARD","look at that lineup","THE CABINET. Repeat image 1 of 3 (again at 'look at the cabinet again' and '3 more bottles'). Hold through 'for a second'.",("gen",104),False,""),
("CARD","The scale can be moving","Feet on the scale. The progress is real.",("gen",105),False,"Alt Use: Broll folder, before-and-after clip."),
("UGC","midsection is distended","Bloated stomach, side-on. Real footage.",("lib","broll_10_bloated_bra"),False,"Alt: Broll folder '7am vs' clip."),
("CARD","same question starts every morning","Edge of the bathtub, hand on stomach, looking at the floor. Hold through 'did any of it work?'",("gen",106),False,""),
("FACE","I want to show you","BARE. The promise lands on her face. Hold through 'through your digestion'.",("face",None),False,""),
("SCIENCE","while you kept adding bottles","Tease: the lit tract, full frame, two seconds.",("lib","sci_35_xray_tract"),False,""),
("PIP","the organ where part","The stacked MiraLAX jars as a small inset over her chest. The stack is the problem.",("lib","broll_04_miralax_stack"),True,""),
("SCIENCE","the slowdown begins","The tract with the stomach lit red at the top. Two seconds, then back to her.",("lib","sci_08_tract_stomach_blocked"),False,""),
("FACE","I'm a nurse with 25 years","BARE. Credential on her face, nothing over it. Hold through 'size of the stack'. No badge, no name, no employer anywhere in the ad.",("face",None),False,""),
("UGC","Your GLP-1 is doing something real","The injection. Real footage.",("lib","broll_08_glp1_injection"),False,""),
("CARD","reduce hunger","Pushing the plate away, content. Positive beat, she is winning here.",("gen",108),False,""),
("SCIENCE","slow gastric emptying","Use: Science Animations folder, 04 stomach stalled.",("lib","sci_04_stomach_stalled"),False,""),
("CARD","keep the progress","The waistband gap. Hold through 'value from it'.",("gen",109),False,"Alt Use: Broll folder, before-and-after clip."),
("FACE","The trouble starts","BARE. Hold through 'one switch'.",("face",None),False,""),
("SCIENCE","slow the rate at which food","Use: Science Animations folder, veo 001 slowed emptying.",("lib","sci_04_stomach_stalled"),False,"Second half of the same stalled-stomach clip, or veo_001_gi_tract_slowed_emptying."),
("SCIENCE","reduce movement through","Use: Science Animations folder, STOMACH AND COLON REACTION.",("lib","sci_28_stomach_colon"),False,""),
("SCIENCE","stool can stay downstream","Use: Science Animations folder, Stool sitting.",("lib","sci_33_stool_sitting"),False,""),
("SCIENCE","become harder","Use: Science Animations folder, 07 drying hardening. Hold through 'removing water'.",("lib","sci_07_drying"),False,""),
("SCIENCE","removing water","Use: Science Animations folder, 09 colon only. The colon doing its job, alone.",("lib","sci_09_colon_only"),False,""),
("CARD","fullness, bloat","Leaning back from dinner, hands on the stomach, button undone. Hold through 'by dinner'.",("gen",110),False,"Alt Use: Science Animations folder, veo_010_science distended belly."),
("CARD","Now look at the cabinet again","THE CABINET, repeat 2 of 3. Same picture, now it is the evidence.",("gen",104),False,""),
("PIP","Miralax helps hold water","Inset: the real MiraLAX jar. One product per inset, cut on each product name.",("gen",201),True,""),
("PIP","Fiber can change","Inset: Metamucil Fiber Gummies.",("gen",202),True,""),
("PIP","Probiotics focus","Inset: Align box.",("gen",203),True,""),
("PIP","Magnesium can affect","Inset: Nature Made magnesium citrate.",("gen",204),True,""),
("PIP","hydration still matters","Inset: the water glass filling.",("gen",205),True,""),
("FACE","Each one has a reason","BARE. Fairness beat, she is not mocking the cabinet.",("face",None),False,""),
("SCIENCE","supporting delayed movement","Use: Science Animations folder, STOMACH CONTRACTION. Hold through 'higher in digestion'.",("lib","sci_29_stomach_contraction"),False,""),
("FACE","The organ your routine","BARE. The reveal line starts on her face...",("face",None),False,""),
("SCIENCE","is your stomach","...and cuts to the HERO on 'stomach': Science Animations folder, UPSTREAM (warning on the stomach, red X on the colon, green arrow). Hold 3 seconds. This is the most important cut in the ad.",("lib","sci_34_upstream_hero"),False,""),
("FACE","That qualification matters","BARE. Hold through 'other causes'.",("face",None),False,""),
("SCIENCE","may work in more than one part","Use: Science Animations folder, 16 tract healthy (neutral whole tract).",("lib","sci_16_tract_healthy"),False,""),
("SCIENCE","the slowdown can begin upstream","Use: Science Animations folder, 08 tract stomach blocked (callback).",("lib","sci_08_tract_stomach_blocked"),False,""),
("PIP","aimed at water","Inset: THE MAP card (four labels on the colon, stomach 'not covered'). Hold through 'farther down'.",("gen",301),True,""),
("FACE","Your effort made sense","BARE. Absolution. Hold through 'proper place'.",("face",None),False,""),
("PIP","The incomplete map","Inset: THE MAP card again, one beat. Callback, allowed repeat.",("gen",301),True,""),
("SCIENCE","support digestive rhythm upstream","Use: Science Animations folder, 03 peristalsis normal (the fix, moving).",("lib","sci_03_peristalsis"),False,""),
("SCIENCE","avoid treating more bulk","Use: Science Animations folder, 10 fiber volume buildup.",("lib","sci_10_fiber_buildup"),False,""),
("CARD","work alongside the shot","The Ozempic pen in her hand, full frame. Hold through 'against it'.",("gen",107),False,""),
("FACE","That last part matters","BARE.",("face",None),False,""),
("CARD","cancel the weight-loss effect","Worried on the scale. The fear, shown.",("gen",212),False,""),
("PIP","Your medication's effects","Inset: the two-column 'Not the same switch' card. Hold through 'trying to manage'.",("gen",302),True,""),
("SCIENCE","unwanted digestive slowdown","Use: Science Animations folder, 04 stomach stalled (callback). Hold through 'trying to manage'.",("lib","sci_04_stomach_stalled"),False,""),
("FACE","Digestive support is not","BARE. The boundary is spoken to camera, nothing over it. Hold through 'your medication'.",("face",None),False,""),
("CARD","Keep your prescriber involved","The exam room. Hold through 'involved'.",("gen",112),False,""),
("FACE","review the ingredients against","BARE.",("face",None),False,""),
("SCIENCE","the first job is stomach motility","Use: Science Animations folder, veo 011 restored motility.",("lib","sci_49_restored_motility"),False,""),
("CARD","Celery juice extract","Fresh celery, full frame, lands on 'Celery'.",("gen",207),False,""),
("PIP","containing apigenin","Inset: APIGENIN spec card. Hold through 'support that movement'.",("gen",304),True,""),
("SCIENCE","support that movement","Use: Science Animations folder, 03 peristalsis normal (callback, the fix).",("lib","sci_03_peristalsis"),False,""),
("UGC","sulfur-related odor","Hand to mouth after the burp, embarrassed. Hold through 'burps'.",("gen",111),False,"Alt Use: Science Animations folder, 06 sulfide gas rising."),
("CARD","Chlorophyll or chlorophyllin","The green vial, full frame, lands on 'Chlorophyll'.",("gen",208),False,""),
("PIP","takes that job","Inset: CHLOROPHYLLIN spec card.",("gen",305),True,""),
("SCIENCE","addressing the sulfur compounds","Use: Science Animations folder, 13 chlorophyll neutralize. Hold through 'with them'.",("lib","sci_13_chlorophyll"),False,""),
("CARD","a large fiber load","The Metamucil tub and the gloopy glass. Unappetizing on purpose.",("gen",209),False,""),
("CARD","A low dose","The heaping scoop next to the tiny pinch. The scale contrast is the point.",("gen",206),False,""),
("SCIENCE","supports the gut farther down","Use: Science Animations folder, 14 soluble fiber flow.",("lib","sci_14_soluble_fiber"),False,""),
("PIP","without turning bulk","Inset: SOLUBLE PREBIOTIC FIBER spec card.",("gen",306),True,""),
("PIP","digestion does not happen in one place","Inset: the THREE-JOB map (upstream, along the way, downstream). Hold through 'support downstream'.",("gen",303),True,""),
("SCIENCE","The formula accounts for","Use: Science Animations folder, 16 tract healthy restored, full frame. Hold through 'support downstream'.",("lib","sci_16_tract_healthy"),False,""),
("CARD","Putting those 3 jobs","THE CABINET, repeat 3 of 3, last time. Hold through 'defeat the point'.",("gen",104),False,""),
("PRODUCT","Motilli combines them","CUT IN ON 'MOTILLI'. First time the brand exists. Use: Product Focused folder, bottle with celery on the windowsill.",("lib","prod_45_bottle_celery_window"),False,"Only if missing, Make: the i2i bottle-on-counter card (attached on the board)."),
("PRODUCT","forest-green heart gummy","Use: Product Focused folder, gummy held in fingers.",("lib","prod_38_gummy_fingers"),False,"Only if missing: the i2i gummy-in-palm card."),
("PRODUCT","The daily serving is 2 gummies","Use: Product Focused folder, pouring into the palm. Exactly TWO gummies must be visible on '2'.",("lib","prod_43_pour_palm"),False,"Only if missing: the i2i two-gummies-and-bottle card."),
("PRODUCT","the routine is simple","Use: Product Focused folder, taking the gummy with the coffee mug. Hold through 'across the cabinet'.",("lib","prod_44_take_gummy_coffee"),False,""),
("CARD","an ordinary morning","Coffee at the window, unhurried.",("gen",210),False,""),
("CARD","your first thought","Waking up, phone still face down.",("gen",401),False,""),
("CARD","waistband negotiation","Buttoning the jeans, easy. Lands on 'waistband'.",("gen",211),False,""),
("PRODUCT","the cabinet is no longer","The cabinet cleared, one Motilli bottle in it. Payoff of the 3 cabinet shots. Hold through 'running the routine'.",("gen",310),False,""),
("FACE","That is the direction","BARE. Hold through 'timeline'.",("face",None),False,""),
("PIP","a crowded stack","Inset: THE MAP card, third and last use. Hold through 'part of the problem'.",("gen",301),True,""),
("SCIENCE","covers the upstream slowdown","Use: Science Animations folder, UPSTREAM hero, second and last use. Hold through 'number of bottles'.",("lib","sci_34_upstream_hero"),False,""),
("PRODUCT","Learn more about Motilli","Her, holding the bottle beside her face, label to camera. Hold through 'link below'.",("gen",311),False,"Alt Use: Product Focused folder, the nurse-in-scrubs bottle clip."),
("PRODUCT","review the ingredients with","The real Supplement Facts label, full frame. Hold through 'prescriber'.",("file",LABEL),False,""),
("PRODUCT","90-day money-back guarantee","Bottle on the windowsill again with the 90-DAY MONEY-BACK GUARANTEE badge stickered top-left (badge supplied). Hold to the end.",("lib","prod_45_bottle_celery_window"),False,"Badge: keyframes g312."),
]
sched=[]; last=0.0
for typ,cue,intent,src,pip,note in B:
    t=find(cue,last); 
    if t<last-0.01: raise SystemExit(f"ORDER: {cue} at {t} before {last}")
    last=t
    if src[0]=="gen": frame=G(src[1]); use=None; make="yes"
    elif src[0]=="lib": frame=LIB[src[1]]["frame"]; use=LIB[src[1]]["file"]; make=None
    elif src[0]=="face": frame=NURSE; use=None; make=None
    else: frame=src[1]; use="brand website assets, label 1"; make=None
    sched.append(dict(t=t,tc=tc(t),type=typ,cue=cue,intent=intent,frame=frame,use=use,pip=pip,note=note,src=src))
for i,b in enumerate(sched): b["end"]=sched[i+1]["t"] if i+1<len(sched) else DUR; b["hold"]=round(b["end"]-b["t"],1)
json.dump(sched,open(f"{D}/build/schedule.json","w"),indent=1)
long=[(b["tc"],b["cue"],b["hold"]) for b in sched if b["hold"]>4.0]
print("beats",len(sched),"dur",round(DUR,1),"events/4s min",int(DUR/4)+1); print("holds>4s:",long)
# numbered asset folder
A=f"{D}/assets"; shutil.rmtree(A,ignore_errors=True); os.makedirs(A)
seen={}
for b in sched:
    if b["type"]=="FACE": continue
    slug=re.sub(r"[^a-z0-9]+","-",b["cue"].lower()).strip("-")[:28]
    ext=os.path.splitext(b["frame"])[1] or ".jpg"
    name=f"{int(b['t']*10):04d}_{b['type'].lower()}_{slug}{ext}"
    shutil.copy(b["frame"],f"{A}/{name}"); b["asset"]=name
shutil.copy(G(312),f"{A}/badge_90day_guarantee.png"); shutil.copy(NURSE,f"{A}/avatar_base_frame_nurse.png")
print("assets",len(os.listdir(A)))
json.dump(sched,open(f"{D}/build/schedule.json","w"),indent=1)
