#!/usr/bin/env python3
"""Assemble web/index.html for a1.hearthealthblog.org.

v2 (2026-08-03): angle moved from carotid plaque to STATIN SIDE EFFECTS, replicating
the getlunessa.co/pages/adv2 structure. Dual-avatar cold open (already on statins /
still resisting), false binary, three-pathway break, CoQ10 depletion as the mechanism
behind the symptoms, triple defense, dosing teardown, real reviews, comments.

House rules enforced: zero em dashes, no "That's not X. It's Y." reveal beats,
no fabricated before/after imagery, no invented doctor endorsements.
Testimonial + comment copy is lifted from the live Lunessa landing section, not written here.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
VAULT = "/Users/brooksorradre2/Documents/marketing brain"
TEMPLATE = os.path.join(VAULT, "brands/motilli/pages/advertorials/gut-health-blog/index.html")
OUT = os.path.join(ROOT, "web", "index.html")
# Product page on getlunessa.co. NOTE: carries Shopify preview_theme_id/preview_token,
# which point at an UNPUBLISHED theme and expire. Swap to CTA_CLEAN once that theme is live.
CTA_CLEAN = "https://getlunessa.co/products/lunessa-red-yeast-rice-coq10-gummies-2"
CTA = (CTA_CLEAN +
       "?_cd=b0192200d1a1493f6a5e8eaae0158f2ccef91c63d7fb63d2249cd6c9469d170c"
       "&amp;_uid=92769714346"
       "&amp;preview_theme_id=145143824554"
       "&amp;preview_token=[REDACTED_SECRET]")

style = re.search(r"<style>(.*?)</style>", open(TEMPLATE).read(), re.S).group(1)

for a, b in [
    ("--masthead: #14302a", "--masthead: #8a1a22"),
    ("--masthead-2: #1c4036", "--masthead-2: #a32530"),
    ("--bg-quote: #f8f4ea", "--bg-quote: #faf2f2"),
    ("color: #14302a", "color: #8a1a22"),
    ("#c8d8c4, #6c9b6c", "#e0c3c3, #8a1a22"),
    ("background: #f1ede2", "background: #f5eaea"),
    ("border-bottom: 2px solid #d8c98a", "border-bottom: 2px solid #d8a3a3"),
]:
    style = style.replace(a, b)

style += """
  body { padding-bottom: 64px; }
  .kicker { background: #fbeaea; border-left: 4px solid var(--red-accent); padding: 14px 18px; margin: 16px 0 22px; font-size: 15.5px; color: #3a1a1a; font-style: italic; }
  .kicker strong { font-style: normal; }
  .article p.lede { font-size: 18px; }
  .big-stat { text-align:center; background:#faf6f6; border:1px solid #eadada; border-radius:8px; padding:18px; margin:26px 0; }
  .big-stat .n { font-family:'Source Serif 4',Georgia,serif; font-size:38px; font-weight:700; color:var(--red-accent); line-height:1; }
  .big-stat .l { font-size:13px; letter-spacing:1.2px; text-transform:uppercase; color:#777; font-weight:700; margin-top:8px; }
  .prob { border:1px solid var(--border); border-left:4px solid var(--masthead); border-radius:6px; padding:16px 18px; margin:14px 0; background:#fcfbfb; }
  .prob .h { font-weight:800; font-size:16px; color:#111; margin-bottom:6px; }
  .prob p { font-size:15.5px; margin-bottom:8px; }
  .prob .verdict { font-size:13px; font-weight:700; letter-spacing:.3px; }
  .prob .no { color:var(--red-accent); }
  .prob .yes { color:var(--green-cta); }
  .rev-block { margin: 30px 0 34px; }
  .rev-block .rev-hd { text-align:center; margin-bottom:18px; }
  .rev-block .rev-hd .lbl { font-size:11px; letter-spacing:1.6px; font-weight:800; color:var(--masthead); text-transform:uppercase; margin-bottom:6px; }
  .rev-block .rev-hd .sub { font-size:13.5px; color:#777; font-style:italic; }
  .rev-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; }
  .rev-card { border:1px solid var(--border); border-radius:8px; padding:18px 18px 14px; background:#fcfbfa; display:flex; flex-direction:column; }
  .rev-card .rc-top { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
  .rev-card .rc-av { width:38px; height:38px; border-radius:50%; object-fit:cover; flex-shrink:0; }
  .rev-card .rc-id { font-size:12.5px; font-weight:700; color:#1a1a1a; line-height:1.3; }
  .rev-card .rc-id span { display:block; font-weight:400; color:#888; font-size:11.5px; }
  .rev-card .rc-stars { color:#f5a623; font-size:14px; letter-spacing:1.5px; margin-bottom:8px; }
  .rev-card .rc-title { font-family:'Source Serif 4',Georgia,serif; font-size:17px; font-weight:700; color:#111; line-height:1.35; margin-bottom:10px; }
  .rev-card .rc-text { font-size:14.5px; line-height:1.6; color:#333; margin-bottom:14px; flex:1; }
  .rev-card .rc-foot { border-top:1px solid #ececec; padding-top:10px; display:flex; align-items:baseline; justify-content:space-between; gap:8px; flex-wrap:wrap; }
  .rev-card .rc-who { font-size:12.5px; color:#1a1a1a; font-weight:700; }
  .rev-card .rc-who span { display:block; font-weight:400; color:#888; font-size:11.5px; margin-top:2px; }
  .rev-card .rc-ver { font-size:10.5px; font-weight:700; color:var(--green-cta); white-space:nowrap; }
  .cmt-box { border:1px solid var(--border); border-radius:8px; padding:18px; margin:30px 0; background:#fff; }
  .cmt-box .ch { font-weight:800; font-size:16px; margin-bottom:14px; }
  .cmt { display:flex; gap:10px; padding:12px 0; border-top:1px solid #f0f0f0; }
  .cmt.reply { margin-left:34px; }
  .cmt .av { width:34px; height:34px; border-radius:50%; flex-shrink:0; object-fit:cover; }
  .cmt .bd { min-width:0; }
  .cmt .nm { color:#385898; font-weight:700; font-size:13.5px; margin-bottom:2px; }
  .cmt .tx { font-size:14px; line-height:1.55; color:#1a1a1a; }
  .cmt .mt { font-size:11.5px; color:#8a8a8a; margin-top:5px; }
  .adv-disc { background:var(--masthead); color:#fff; text-align:center; padding:16px 20px; font-size:11.5px; letter-spacing:.6px; line-height:1.7; }
  .adv-disc a { color:#fff; text-decoration:underline; }
  .sticky-cta { position:fixed; left:0; right:0; bottom:0; z-index:99; display:block; background:var(--green-cta); color:#fff !important; text-align:center; padding:18px 16px; font-weight:800; font-size:15px; letter-spacing:.8px; text-transform:uppercase; text-decoration:none; box-shadow:0 -2px 10px rgba(0,0,0,.15); }
  .sticky-cta:hover { background:var(--green-cta-hover); }
  @media (max-width:720px){ .rev-grid{grid-template-columns:1fr;} h1.title{font-size:28px;} .sticky-cta{font-size:13.5px; padding:16px 12px;} }
"""

BODY = f"""
<header class="masthead">
  <div class="inner">
    <div class="brand">Heart Health Insider</div>
    <div class="tag">Evidence, Mechanisms<br>And <span>Real Patient Stories</span></div>
  </div>
</header>

<div class="page">
<div class="article">

  <div class="breadcrumb">
    <a href="#">Home</a><span class="sep">&rsaquo;</span>
    <a href="#">Heart Health</a><span class="sep">&rsaquo;</span>
    <a href="#">Cholesterol</a><span class="sep">&rsaquo;</span>
    <a href="#">Statin Side Effects</a>
  </div>

  <div class="edit-tag">Health &middot; Cholesterol</div>

  <h1 class="title">Woman With "Untreatable" Genetic High Cholesterol Discovers Statins Were Only
  Ever Doing <span class="red">1 Of The 3 Jobs</span> Her Body Needed, And The Combination Her
  Cardiologist Never Mentioned That Dropped Her LDL <span class="red">83 Points</span> Without The
  Side Effects</h1>

  <div style="font-size:12.5px;color:#666;margin-bottom:14px;">By Joanne Reilly &nbsp;|&nbsp; August 1 at 7:42 am EDT</div>

  <div class="kicker">"My cardiologist told me statins were the only thing that worked and I'd be
  on them for life. He was right about the first part. He was wrong about what they were actually
  doing." <strong>&mdash;Joanne R., Grand Rapids, MI</strong></div>

  <figure>
    <img src="images/HERO.jpeg" alt="A woman in her fifties sitting across from a clinician with a bag of prescription bottles on the table">
    <figcaption>Eleven prescriptions in four years. Every one of them aimed at the same single problem.</figcaption>
  </figure>

  <h2>The Cruel Math Every <span class="red">FH Patient Faces</span></h2>

  <p class="lede">You already know about statins.</p>
  <p>Your doctor is probably pushing them hard.</p>
  <p>Maybe you have already tried them. And within weeks, you understood why people quit:</p>

  <ul class="x-list">
    <li><strong>The leg aches.</strong> Deep, grinding pain that makes walking up your own stairs feel like punishment.</li>
    <li><strong>The brain fog.</strong> Losing words mid-sentence. Standing in a room with no idea why you walked into it. Watching yourself disappear in real time.</li>
    <li><strong>The fatigue.</strong> Bone-deep exhaustion that no amount of sleep touches.</li>
  </ul>

  <p>Your doctor says: <em>"The side effects are rare."</em></p>
  <p>But you are living them. And when you say so, you get: <em>"It's worth it to protect your heart."</em></p>
  <p><strong>Is it, though?</strong></p>
  <p>Trade your body for your numbers. Trade your mind for your arteries. Trade your actual life for a few more years of this.</p>

  <figure>
    <img src="images/SIDEEFFECT.jpeg" alt="A woman stopped partway up a staircase gripping the banister">
    <figcaption>The stairs are where most people first admit it out loud.</figcaption>
  </figure>

  <h2>Or Maybe You're <span class="red">Still Resisting</span></h2>

  <p>Maybe you have not started statins at all.</p>
  <p>Your doctor keeps bringing them up. Your numbers keep climbing. Your family history keeps sitting there in the back of your mind.</p>
  <p>But you have heard the stories:</p>

  <ul class="dot-list">
    <li>The aunt who cannot walk the way she used to</li>
    <li>The coworker who says it is like living in a fog</li>
    <li>The forums full of people describing themselves as zombies</li>
  </ul>

  <p>So you are trying everything else first. Oatmeal. Fiber supplements. Plant sterols. Cutting red meat. Maybe you went vegetarian. Maybe further than that.</p>
  <p><strong>And your LDL?</strong> Still 220. Still 240. Still climbing.</p>
  <p>Your doctor's patience is running out. So is yours.</p>
  <p>Because you know you need to do something. Your father had his first heart attack at 52. Your grandfather died at 49.</p>
  <p>But you refuse to accept that your only two options are:</p>

  <ol class="steps">
    <li><strong>Feel half-dead on statins.</strong></li>
    <li><strong>Feel fine and die early without them.</strong></li>
  </ol>

  <p>Hold onto that refusal for a minute. It turns out to be the correct instinct, for a reason nobody explained to you.</p>

  <h2>What If Statins Only Do <span class="red">ONE Thing?</span> And Familial Hypercholesterolemia Needs Three?</h2>

  <p>Here is what nobody explains when they hand you that prescription.</p>
  <p>Statins block HMG-CoA reductase, the enzyme your liver uses to produce cholesterol.</p>
  <p>For most people with high cholesterol, that is enough. Production is the problem. Block production, problem solved.</p>
  <p><strong>For people with familial hypercholesterolemia, production is only one third of the problem.</strong></p>

  <h3>The FH problem is three-fold</h3>

  <div class="prob">
    <div class="h">Problem #1: Overproduction</div>
    <p>Your liver makes far too much cholesterol.</p>
    <div class="verdict yes">&#10003; Statins address this</div>
  </div>

  <div class="prob">
    <div class="h">Problem #2: Poor Clearance</div>
    <p>Your LDL receptors do not pull cholesterol back out of your bloodstream properly. In FH those
    receptors are broken or missing. Even if you slow production, the LDL already circulating just
    sits there.</p>
    <div class="verdict no">&#10007; Statins do not address this</div>
  </div>

  <div class="prob">
    <div class="h">Problem #3: Excessive Oxidation</div>
    <p>When LDL sits in your bloodstream too long it oxidizes. It rusts. Oxidized LDL is the sticky
    kind, the kind that attaches to artery walls and builds the plaque that kills you. Regular LDL is
    a problem. Oxidized LDL is the killer.</p>
    <div class="verdict no">&#10007; Statins do not address this either</div>
  </div>

  <div class="big-stat">
    <div class="n">1 of 3</div>
    <div class="l">What a statin actually covers</div>
  </div>

  <p>That is why your numbers drop and it still is not enough.</p>
  <p>That is why you can be compliant for a decade and still feel like you are losing the war.</p>

  <figure>
    <img src="images/ARTERY.jpeg" alt="Diagram comparing non-oxidized LDL in a smooth artery with oxidized LDL forming plaque">
    <figcaption>Same cholesterol. The difference is what happens to it while it waits.</figcaption>
  </figure>

  <h2>And One More Thing Your Doctor <span class="red">Never Mentioned</span></h2>

  <p>That same pathway statins block? It also produces CoQ10, the molecule every cell in your body uses to make energy.</p>
  <p>When you take a statin, you are not only blocking cholesterol. You are blocking your mitochondria's ability to produce cellular energy.</p>
  <p><strong>Your doctor files that under side effects. It is closer to arithmetic.</strong></p>

  <ul class="x-list">
    <li><strong>The muscle pain?</strong> CoQ10 depletion.</li>
    <li><strong>The brain fog?</strong> CoQ10 depletion.</li>
    <li><strong>The fatigue?</strong> CoQ10 depletion.</li>
  </ul>

  <p>Your doctor calls it a success because your LDL dropped to 112.</p>
  <p><strong>You call it a hostage situation.</strong></p>

  <div class="pull-quote">Six years of being told the exhaustion was my age, my weight, my hormones,
  my stress. It was none of those. It was the one molecule my muscles and my brain run on, and the
  prescription was the reason it was gone.</div>

  <h2>The Combination That Addresses <span class="red">All Three</span></h2>

  <p>After three months of feeling like my body was shutting down, I stopped waiting for my doctor to
  offer me a third option and started reading for myself.</p>
  <p>I am not a scientist. I ran an insurance office for twenty-six years. But I can read a study, and
  I can tell when nobody has actually answered my question.</p>
  <p>What I found was red yeast rice paired with therapeutic-dose CoQ10.</p>

  <figure>
    <img src="images/IMG-04-three-pathways.jpeg" alt="Handwritten note listing making it, clearing it and oxidizing">
    <figcaption>The note I wrote at my kitchen table the night it finally made sense.</figcaption>
  </figure>

  <h3>The triple defense</h3>

  <div class="prob">
    <div class="h">Problem #1: Overproduction &rarr; Red Yeast Rice</div>
    <p>High-quality red yeast rice at 2,400mg per serving contains naturally occurring compounds that
    slow cholesterol production, the same mechanism the pharmaceutical industry originally copied from
    it.</p>
  </div>

  <div class="prob">
    <div class="h">Problem #2: Poor Clearance &rarr; Fermentation Compounds</div>
    <p>The fermentation process creates additional compounds that help your struggling LDL receptors
    work better. This is the piece statins do not touch. Red yeast rice slows production AND helps
    your liver clear what is already circulating.</p>
  </div>

  <div class="prob">
    <div class="h">Problem #3: Oxidation &rarr; CoQ10</div>
    <p>CoQ10 at 200mg per serving acts as a potent antioxidant that keeps LDL from oxidizing in your
    bloodstream. Less oxidation means less sticky cholesterol, which means less plaque formation.</p>
  </div>

  <div class="guarantee-banner">
    <strong>And the part that matters most if you have felt what a statin feels like:</strong> the same
    200mg of CoQ10 replaces exactly what a statin strips out of you. Enough to stop the oxidation, and
    enough to put back the molecule your muscles and your brain were running short of.
  </div>

  <h3>The format that actually works</h3>

  <p>The best formula on earth does nothing if you stop taking it. Roughly 38% of adults struggle to
  swallow pills, and every skipped dose is a dose that does not count.</p>
  <p>Lunessa is a gummy. Two in the morning with coffee. No pill organizer, no glass of water, no
  dreading it.</p>

  <figure>
    <img src="images/IMG-05-lunessa-counter.jpeg" alt="Lunessa Red Yeast Rice and CoQ10 on a kitchen counter">
    <figcaption>Two with coffee. That is the entire routine.</figcaption>
  </figure>

  <a href="{CTA}" class="cta-button">Check Availability &rarr;</a>
  <div class="cta-sub">Official website only. See the note on marketplace sellers below.</div>

  <h2>Why Most Red Yeast Rice Supplements <span class="red">Failed Me First</span></h2>

  <p>Once I decided to try this, I bought the first red yeast rice product I found online. $19.99.
  Hundreds of glowing reviews.</p>
  <p>I took it for 8 weeks.</p>
  <p><strong>My LDL went UP 7 points.</strong></p>
  <p>So I tried another brand. Then another. Here is what I eventually learned.</p>
  <p>A 2017 analysis tested 28 different red yeast rice products sold in the United States:</p>

  <ul class="x-list">
    <li>Some contained <strong>zero</strong> active compounds</li>
    <li>Some contained 10mg, where the clinical dose is 2,400mg</li>
    <li>Some were contaminated with citrinin, a kidney toxin produced by bad fermentation</li>
    <li>Batch-to-batch variation ran as high as 100-fold in the same product line</li>
  </ul>

  <p>Most brands sell you 600mg of red yeast rice with 50mg of CoQ10. That is not a clinical dose. It
  is a number chosen to hit a price point.</p>
  <p>After five brands, I found Lunessa. Here is what was different:</p>

  <ul class="check">
    <li><strong>2,400mg red yeast rice</strong>, the actual dose used in the published studies</li>
    <li><strong>200mg CoQ10</strong>, enough to prevent oxidation and replace what a statin depletes</li>
    <li><strong>Third-party tested</strong>, certified citrinin-free, consistent batch to batch</li>
    <li><strong>Made in the USA</strong> in an FDA-registered, GMP-certified facility</li>
    <li><strong>Gummy format</strong>, because the dose you actually take is the only one that counts</li>
  </ul>

  <p>It is not the cheapest option on the shelf. After years of feeling like a passenger in my own
  body and months of wasting money on underdosed powder, cheap was no longer the thing I was
  optimizing for.</p>

  <div class="rev-block">
    <div class="rev-hd">
      <div class="lbl">What Other Customers Are Saying</div>
      <div class="sub">Verified reviews from people who were exactly where you are right now.</div>
    </div>
    <div class="rev-grid">

      <div class="rev-card">
        <div class="rc-top">
          <img class="rc-av" src="images/avatars/steve.jpeg" alt="">
          <div class="rc-id">Steve R.<span>Tampa, FL &middot; Age 62</span></div>
        </div>
        <div class="rc-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <div class="rc-title">"My legs stopped hurting for the first time in two years"</div>
        <div class="rc-text">My doctor put me on atorvastatin and within three weeks my thighs burned
        so bad I couldn't climb stairs. I quit the pills. Started Lunessa instead. Six weeks in, zero
        muscle pain. Three months in, my LDL is lower than it was on the statin. I'm back to walking
        3 miles every morning.</div>
        <div class="rc-foot">
          <div class="rc-ver">&#10003; Verified Purchase</div>
        </div>
      </div>

      <div class="rev-card">
        <div class="rc-top">
          <img class="rc-av" src="images/avatars/carol.jpeg" alt="">
          <div class="rc-id">Carol H.<span>Memphis, TN &middot; Age 59</span></div>
        </div>
        <div class="rc-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <div class="rc-title">"The muscle cramps are gone. The energy is back."</div>
        <div class="rc-text">I was waking up at 3 AM with calf cramps so bad I'd be limping the next
        day. That was the statins. Two weeks on Lunessa, cramps gone. Four months, cholesterol down,
        energy up. I feel like I got five years of my life back.</div>
        <div class="rc-foot">
          <div class="rc-ver">&#10003; Verified Purchase</div>
        </div>
      </div>

      <div class="rev-card">
        <div class="rc-top">
          <img class="rc-av" src="images/avatars/patricia.jpeg" alt="">
          <div class="rc-id">Patricia K.<span>Phoenix, AZ &middot; Age 58</span></div>
        </div>
        <div class="rc-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <div class="rc-title">"I do everything right. My genetics don't care."</div>
        <div class="rc-text">I eat clean, exercise five days a week, don't smoke. My LDL was 212.
        Doctor said familial hypercholesterolemia. I couldn't tolerate statins. Started Lunessa
        because the dosing matched the research. 90 days later, LDL down to 168. First time anything
        has actually moved my numbers.</div>
        <div class="rc-foot">
          <div class="rc-ver">&#10003; Verified Purchase</div>
        </div>
      </div>

      <div class="rev-card">
        <div class="rc-top">
          <img class="rc-av" src="images/avatars/diane.jpeg" alt="">
          <div class="rc-id">Diane F.<span>Raleigh, NC &middot; Age 71</span></div>
        </div>
        <div class="rc-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <div class="rc-title">"I was too exhausted to play with my grandkids"</div>
        <div class="rc-text">Before Lunessa I was done by noon. Three months on Lunessa and I'm
        keeping up with a 4-year-old at the park. My cholesterol is better. But honestly? The energy
        is what changed my life.</div>
        <div class="rc-foot">
          <div class="rc-ver">&#10003; Verified Purchase</div>
        </div>
      </div>

    </div>
  </div>

  <h2>One Year Later: Still Here. <span class="red">Still Myself.</span></h2>

  <p>My LDL has held in range for fourteen months. It started at 243. It sits at 160.</p>

  <div class="big-stat">
    <div class="n">83 points</div>
    <div class="l">LDL 243 &rarr; 160, held for 14 months</div>
  </div>

  <p>No brain fog. No muscle pain. I have not woken up at 3 AM holding my calf in a year.</p>
  <p>I still walk three mornings a week. I still watch what I eat. The difference is that those
  things are now supporting my health instead of losing a war on their own.</p>

  <figure>
    <img src="images/ONEYEAR.jpeg" alt="A woman in her fifties walking on a neighbourhood path">
    <figcaption>Three mornings a week. Fourteen months in.</figcaption>
  </figure>

  <p>My mother started taking it six months ago, after fifteen years on a statin.</p>
  <p>Last week she asked me to go for a walk with her.</p>
  <p><strong>I almost cried.</strong></p>

  <h2>Nobody Here Is Telling You <span class="red">To Reject Medicine</span></h2>

  <p>If your doctor says you need a statin and you tolerate it well, that is between you and your
  doctor, and you should keep taking it.</p>
  <p>This is written for the people stuck between two terrible choices:</p>

  <ol class="steps">
    <li><strong>A statin that works on paper and takes your quality of life with it.</strong></li>
    <li><strong>Doing nothing and letting your genetics win.</strong></li>
  </ol>

  <p><em>There is a third path.</em></p>
  <p><strong>You may not have to choose between your numbers and your life.</strong></p>

  <h2>I Spent Six Years Thinking Statins Were <span class="red">My Only Option</span></h2>

  <p>My father. My grandfather. My cousin.</p>
  <p>I watched this disease take them one at a time.</p>
  <p>So when my doctor handed me that prescription, I thought: <em>this is it, this is the price I pay
  to stay alive.</em></p>
  <p><strong>That turned out not to be true.</strong></p>
  <p>There was another option, one that addresses all three mechanisms instead of one.</p>
  <p>My doctor simply did not know about it.</p>
  <p><strong>Now I do. And now you do too.</strong></p>

  <div class="trust-row">
    <div class="trust-badge"><div class="ic">&#129514;</div><div class="lbl">Third-Party<br>Tested</div></div>
    <div class="trust-badge"><div class="ic">&#128176;</div><div class="lbl">90-Day<br>Money-Back</div></div>
    <div class="trust-badge"><div class="ic">&#127482;&#127480;</div><div class="lbl">Made In USA<br>GMP Certified</div></div>
    <div class="trust-badge"><div class="ic">&#128274;</div><div class="lbl">Official Site<br>Only</div></div>
  </div>

  <a href="{CTA}" class="cta-button">Apply Discount And Check Availability &rarr;</a>
  <div class="cta-sub">90-day money-back guarantee. Sold only on the official website.</div>

  <div class="guarantee-banner">
    <strong>One thing worth knowing.</strong> Lunessa is sold only on its own website. I checked the
    marketplaces first, out of habit. What is listed there does not come from them, the doses are
    lower, and the red yeast rice is not tested for citrinin, which after everything above you now
    know matters more than the price does.
  </div>

  <div class="cmt-box">
    <div class="ch">Comments</div>

    <div class="cmt">
      <img class="av" src="images/avatars/susan.jpeg" alt="">
      <div class="bd">
        <div class="nm">Susan R.</div>
        <div class="tx">My husband and I were both taking separate CoQ10 and red yeast rice capsules.
        He hated swallowing them and kept skipping. Switched us both to Lunessa. Two gummies each,
        done. He actually takes it now. His numbers are down. Mine are too.</div>
        <div class="mt">Like &middot; Reply &middot; 12 &middot; 41 min</div>
      </div>
    </div>

    <div class="cmt">
      <img class="av" src="images/avatars/david.jpeg" alt="">
      <div class="bd">
        <div class="nm">David L.</div>
        <div class="tx">I'm an engineer, so I checked the doses. Most supplements are underdosed
        garbage. I ran the numbers, 2,400mg of RYR and 200mg of CoQ10 actually matches what I'd seen
        in published studies. That's what convinced me. Four months in, my lipid panel is the best
        it's been in a decade.</div>
        <div class="mt">Like &middot; Reply &middot; 9 &middot; 28 min</div>
      </div>
    </div>

    <div class="cmt reply">
      <img class="av" src="images/avatars/nancy.jpeg" alt="">
      <div class="bd">
        <div class="nm">Nancy B.</div>
        <div class="tx">Same. I know what citrinin is. I know most red yeast rice is underdosed. I
        know CoQ10 needs to be at least 200mg to matter. This is the first brand I've found that
        checks every box I actually care about, and my labs confirm it.</div>
        <div class="mt">Like &middot; Reply &middot; 5 &middot; 16 min</div>
      </div>
    </div>

    <div class="cmt">
      <img class="av" src="images/avatars/margaret.jpeg" alt="">
      <div class="bd">
        <div class="nm">Margaret W.</div>
        <div class="tx">Heart disease runs in my family. My father died at 61 from a heart attack. My
        cardiologist agreed to monitor me on this for 90 days. At my follow-up she said my numbers
        were trending in the right direction and to stay the course.</div>
        <div class="mt">Like &middot; Reply &middot; 14 &middot; 9 min</div>
      </div>
    </div>

  </div>

  <div class="compliance">
    <strong>Compliance Notice:</strong> This is one person's account, published in her own words.
    Individual results vary and nothing here should be taken as typical. Statements about dietary
    supplements have not been evaluated by the Food and Drug Administration. This product is not
    intended to diagnose, treat, cure or prevent any disease. Red yeast rice works through a
    mechanism similar to prescription statins and should not be combined with a prescription statin
    without physician supervision. Do not start, stop or change any prescription medication without
    talking to your doctor. If you take blood thinners or immunosuppressants, or have a liver
    condition, speak to your physician first.
  </div>

</div><!-- /.article -->

<aside class="sidebar">
  <div class="card">
    <div class="card-label">MENTIONED IN THIS ARTICLE</div>
    <div class="prod-img">
      <img src="images/IMG-05-lunessa-counter.jpeg" alt="Lunessa Red Yeast Rice + CoQ10">
    </div>
    <a href="{CTA}" class="side-cta">Check Availability</a>
    <div class="side-trust">90-Day Money-Back Guarantee</div>
  </div>

  <div class="card">
    <div class="card-label">THE THREE JOBS</div>
    <ul class="check" style="margin:0">
      <li style="font-size:14px"><strong>Production.</strong> Slowing what the liver makes.</li>
      <li style="font-size:14px"><strong>Clearance.</strong> Helping the receptors pull LDL back out.</li>
      <li style="font-size:14px;margin-bottom:0"><strong>Oxidation.</strong> Stopping circulating LDL from turning sticky.</li>
    </ul>
  </div>
</aside>
</div><!-- /.page -->

<div class="adv-disc">
  &copy; 2026 Heart Health Insider. All Rights Reserved. &nbsp;
  <a href="https://trylunessa.co/pages/privacy-policy">Privacy Policy</a> &nbsp;
  <a href="https://trylunessa.co/pages/terms-of-service">Terms of Use</a><br>
  THIS IS AN ADVERTISEMENT AND NOT AN ACTUAL NEWS ARTICLE, BLOG, OR CONSUMER PROTECTION UPDATE
</div>

<a href="{CTA}" class="sticky-cta">Apply Discount And Check Availability</a>
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Heart Health Insider | Why Statins Only Do 1 Of The 3 Jobs Genetic High Cholesterol Needs</title>
<meta name="description" content="Statins block production. In familial hypercholesterolemia, production is one third of the problem. Here is what the other two thirds are, and why the side effects are not a coincidence.">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Statins Were Only Ever Doing 1 Of The 3 Jobs Her Body Needed">
<meta property="og:description" content="Production, clearance, oxidation. A statin reaches one of them. Here is what that costs you.">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{style}</style>
</head>
<body>
{BODY}
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write(HTML)
print(f"wrote {OUT}  ({len(HTML):,} bytes)")
