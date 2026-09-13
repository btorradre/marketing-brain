#!/usr/bin/env python3
"""Build the three VitaWild-style Lunessa listicles from one template.
Outputs: public/11-reasons/, public/11-reasons-genetic/, public/11-reasons-menopause/
Shared reason images live in public/11r-assets/ (r1..r11).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """    :root {
      --accent: #580e05;
      --accent-hover: #441008;
      --accent-light: #fdf0ef;
      --text-dark: #1a1a1a;
      --text-body: #444444;
      --text-meta: #666666;
      --text-light: #888888;
      --bg-white: #ffffff;
      --bg-subtle: #faf8f8;
      --border: #e5e7eb;
      --star: #f59e0b;
      --guarantee-bg: #fef9e7;
      --guarantee-border: #f5d565;
      --good: #157347;
      --bad: #b02a37;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: var(--text-body); background: var(--bg-white); line-height: 1.65; -webkit-font-smoothing: antialiased; }
    .page { max-width: 720px; margin: 0 auto; padding: 0 20px; }
    .author-avatar { width: 34px; height: 34px; border-radius: 50%; object-fit: cover; }
    .hero-image { width: 100%; border-radius: 12px; margin: 24px 0 10px; display: block; }
    .sticky-cta { position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000; background: #fff; border-top: 1px solid var(--border); box-shadow: 0 -4px 16px rgba(0,0,0,0.08); padding: 10px 16px calc(10px + env(safe-area-inset-bottom)); text-align: center; transform: translateY(110%); transition: transform 0.3s ease; }
    .sticky-cta.visible { transform: translateY(0); }
    .sticky-cta-btn { display: block; max-width: 480px; margin: 0 auto; background: var(--accent); color: #fff; font-size: 16px; font-weight: 700; padding: 13px 24px; border-radius: 8px; text-decoration: none; }
    .sticky-cta-btn:hover { background: var(--accent-hover); }
    .sticky-cta-sub { display: block; font-size: 12px; color: var(--text-light); margin-top: 5px; }
    body.cta-visible .footer { padding-bottom: 110px; }
    .eyebrow { display: inline-block; margin-top: 36px; padding: 5px 14px; background: var(--accent-light); color: var(--accent); font-size: 13px; font-weight: 700; border-radius: 20px; letter-spacing: 0.5px; text-transform: uppercase; }
    .headline { font-size: 30px; font-weight: 800; color: var(--text-dark); line-height: 1.2; margin-top: 20px; margin-bottom: 12px; }
    @media (max-width: 600px) { .headline { font-size: 25px; } }
    .byline { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: 13px; color: var(--text-light); padding-bottom: 20px; border-bottom: 1px solid var(--border); margin-bottom: 8px; }
    .byline .stars { color: var(--star); letter-spacing: 1px; }
    .byline b { color: var(--text-meta); font-weight: 600; }
    .hook-quote { font-size: 19px; font-weight: 700; color: var(--text-dark); margin: 24px 0 8px; text-align: center; }
    .tldr { background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 12px; padding: 16px 22px; margin: 20px 0 8px; font-size: 16.5px; font-weight: 600; color: var(--text-dark); text-align: center; }
    .reason { padding: 30px 0 6px; }
    .reason-chip { display: inline-block; background: var(--accent-light); color: var(--accent); font-size: 14px; font-weight: 800; border-radius: 20px; padding: 6px 16px; margin: 14px 0 12px; letter-spacing: 0.3px; }
    .reason-title { font-size: 22px; font-weight: 800; color: var(--text-dark); line-height: 1.3; margin-bottom: 12px; }
    @media (max-width: 600px) { .reason-title { font-size: 19px; } }
    .reason p { font-size: 17px; color: var(--text-body); margin-bottom: 14px; line-height: 1.7; }
    .reason strong { color: var(--text-dark); }
    .reason-image { width: 100%; border-radius: 12px; display: block; }
    .arrow-cta { display: block; font-size: 16.5px; font-weight: 700; color: var(--accent); text-decoration: none; margin: 6px 0 10px; }
    .arrow-cta:hover { text-decoration: underline; }
    .section-image { width: 100%; border-radius: 12px; margin: 20px 0 8px; display: block; }
    .compare-wrap { overflow-x: auto; margin: 26px 0; }
    .compare-table { width: 100%; border-collapse: collapse; font-size: 14px; min-width: 520px; border: 1px solid var(--border); }
    .compare-table caption { caption-side: top; text-align: center; font-size: 18px; font-weight: 800; color: var(--text-dark); padding-bottom: 12px; }
    .compare-table th, .compare-table td { padding: 11px 12px; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
    .compare-table thead th { background: var(--accent); color: #fff; font-size: 13.5px; }
    .compare-table thead th:first-child { width: 30%; }
    .compare-table tbody th { font-weight: 600; color: var(--text-dark); background: var(--bg-subtle); font-size: 13.5px; }
    .compare-table .yes { color: var(--good); font-weight: 700; }
    .compare-table .no { color: var(--bad); font-weight: 600; }
    .compare-note { font-size: 12.5px; color: var(--text-light); margin-top: 8px; line-height: 1.5; }
    .testimonial { background: var(--bg-subtle); border-radius: 12px; padding: 24px 28px; margin: 32px 0; }
    .testimonial-stars { color: var(--star); font-size: 18px; margin-bottom: 10px; letter-spacing: 2px; }
    .testimonial-text { font-size: 16px; font-style: italic; color: #555; line-height: 1.65; margin-bottom: 12px; }
    .testimonial-author { font-size: 14px; font-weight: 600; color: var(--text-dark); }
    .verified-badge { display: inline-block; background: var(--accent-light); color: var(--accent); font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-left: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
    .cta-wrap { text-align: center; margin: 32px 0; }
    .cta-btn { display: inline-block; background: var(--accent); color: #fff; font-size: 17px; font-weight: 700; padding: 16px 40px; border-radius: 8px; text-decoration: none; transition: background 0.2s, transform 0.15s; width: 100%; max-width: 480px; text-align: center; }
    .cta-btn:hover { background: var(--accent-hover); transform: translateY(-1px); }
    .cta-sub { display: block; text-align: center; font-size: 13px; color: var(--text-light); margin-top: 8px; }
    .close-section { padding: 40px 0 20px; border-top: 1px solid var(--border); text-align: center; }
    .close-section p { font-size: 18px; color: var(--text-body); margin-bottom: 18px; line-height: 1.65; max-width: 600px; margin-left: auto; margin-right: auto; }
    .sellout { background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 12px; padding: 24px 28px; margin: 36px 0; }
    .sellout h3 { font-size: 19px; color: var(--text-dark); margin-bottom: 10px; }
    .sellout p { font-size: 15.5px; color: var(--text-body); line-height: 1.65; }
    .trust-badges { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin: 28px 0; }
    .trust-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 8px; padding: 10px 16px; font-size: 13px; font-weight: 600; color: var(--text-meta); }
    .guarantee-banner { background: var(--guarantee-bg); border: 1px solid var(--guarantee-border); border-radius: 12px; padding: 24px 28px; margin: 32px 0; text-align: center; }
    .guarantee-banner .guarantee-title { font-size: 18px; font-weight: 700; color: var(--text-dark); margin-bottom: 8px; }
    .guarantee-banner p { font-size: 15px; color: var(--text-body); line-height: 1.6; }
    .faq-section { padding: 40px 0; border-top: 1px solid var(--border); }
    .faq-heading { font-size: 24px; font-weight: 700; color: var(--text-dark); text-align: center; margin-bottom: 28px; }
    .faq-item { border-bottom: 1px solid var(--border); }
    .faq-question { width: 100%; background: none; border: none; padding: 18px 0; font-size: 16px; font-weight: 600; color: var(--text-dark); text-align: left; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-family: inherit; line-height: 1.4; }
    .faq-question:hover { color: var(--accent); }
    .faq-icon { font-size: 22px; font-weight: 300; color: var(--text-light); transition: transform 0.25s; flex-shrink: 0; margin-left: 16px; }
    .faq-item.open .faq-icon { transform: rotate(45deg); }
    .faq-answer { max-height: 0; overflow: hidden; transition: max-height 0.3s ease, padding 0.3s ease; }
    .faq-item.open .faq-answer { max-height: 400px; padding-bottom: 18px; }
    .faq-answer p { font-size: 15px; color: var(--text-body); line-height: 1.65; }
    .footer { padding: 32px 0; border-top: 1px solid var(--border); text-align: center; }
    .footer p { font-size: 12px; color: var(--text-light); line-height: 1.7; max-width: 600px; margin: 0 auto; }
    .footer a { color: var(--text-light); text-decoration: underline; }"""

PDP = "https://getlunessa.co/products/lunessa-red-yeast-rice-coq10-gummies-2"

MASTER_TABLE = f"""    <div class="compare-wrap">
      <table class="compare-table">
        <caption>How Lunessa Compares</caption>
        <thead>
          <tr><th></th><th>Lunessa</th><th>Other Red Yeast Rice</th><th>CoQ10-Only Bottles</th></tr>
        </thead>
        <tbody>
          <tr><th>Red yeast rice dose</th><td class="yes">✓ 2,400mg — full research dose</td><td class="no">✗ ~600mg, a quarter of the dose</td><td class="no">✗ None</td></tr>
          <tr><th>CoQ10 dose</th><td class="yes">✓ 200mg pharmaceutical-grade</td><td class="no">✗ None — depletion ignored</td><td class="no">✗ Usually 50–100mg, underdosed</td></tr>
          <tr><th>Monacolin K content</th><td class="yes">✓ Standardized &amp; disclosed</td><td class="no">✗ Undisclosed, varies by batch</td><td class="no">—</td></tr>
          <tr><th>Citrinin testing</th><td class="yes">✓ Every batch, certified free</td><td class="no">✗ Rarely tested</td><td class="no">—</td></tr>
          <tr><th>Cholesterol pathways covered</th><td class="yes">✓ All three — production, clearance, oxidation</td><td class="no">✗ One</td><td class="no">✗ One, partially</td></tr>
          <tr><th>Format</th><td class="yes">✓ 2 sugar-free raspberry gummies</td><td class="no">✗ Horse-pill capsules, 4–8/day</td><td class="no">✗ Softgels</td></tr>
        </tbody>
      </table>
      <p class="compare-note">Category comparison based on typical label values of leading retail red yeast rice and CoQ10 supplements as of July 2026.</p>
    </div>"""


def reason(num, img, alt, chip, title, body_html, cta_text, rid=""):
    idattr = f' id="{rid}"' if rid else ""
    return f"""    <!-- REASON {num} -->
    <div class="reason"{idattr}>
      <img src="../11r-assets/{img}" alt="{alt}" class="reason-image">
      <span class="reason-chip">{chip}</span>
      <h2 class="reason-title">{num}. {title}</h2>
{body_html}
      <a class="arrow-cta" href="{PDP}">👉 {cta_text}</a>
    </div>"""


def build(variant):
    v = variant
    reasons = []
    reasons.append(reason(1, "r1-liver.jpg", "The liver — where most blood cholesterol is made", "🎯 Works at the Source",
        "It works where cholesterol is actually made — your liver", v["r1_body"], "Work on the Source, Not the Sliver"))
    reasons.append(reason(2, "r2-artery.jpg", "Artery cross-section in three stages: healthy, early plaque, narrowed", "🧬 All Three Pathways",
        "It covers all three cholesterol pathways — not just one", v["r2_body"], "Cover All Three Pathways"))
    reasons.append(reason(3, "r3-doses.jpg", "Lunessa bottle beside a balance scale with gummies", "💪 Full Clinical Doses",
        "The actual research doses — in two gummies, not horse pills",
        """      <p>The clinical research on red yeast rice used 2,400mg per serving. The typical store bottle gives you 600mg — a quarter of the dose. CoQ10 research points to 200mg; most bottles contain 50–100mg. If you've "tried red yeast rice and it didn't work," the dose is almost always why.</p>
      <p>Lunessa delivers <strong>2,400mg + 200mg per serving — the research numbers, exactly</strong> — in two sugar-free raspberry gummies instead of a handful of horse pills.</p>""",
        "Get the Full Clinical Dose"))
    reasons.append(reason(4, "r4-tested.jpg", "Lunessa bottle on a laboratory bench beside a microscope", "🛡️ Certified Clean",
        "Every batch is tested for the toxin cheap brands hide",
        """      <p>Poorly fermented red yeast rice can carry citrinin — a kidney-stressing contaminant the FDA has warned about. Most brands never test for it, and most won't even disclose their monacolin K content because it varies batch to batch.</p>
      <p>Lunessa is <strong>third-party tested and certified citrinin-free — every batch</strong> — with standardized potency, made in a GMP-certified, FDA-registered facility.</p>""",
        "See the Tested-Clean Difference", rid="sticky-trigger"))
    reasons.append(reason(5, "r5-energy.jpg", "Energetic woman hiking a coastal trail at sunrise", "⚡ Energy You Can Feel",
        "It protects your energy — and you feel it within weeks",
        """      <p>The same liver enzyme that makes cholesterol also makes CoQ10 — the molecule your muscles and brain run on. That's why cholesterol-lowering so often comes packaged with aching legs and afternoon fog. Lunessa's 200mg puts back what the process takes out.</p>
      <p>And you notice it: the most common early report is steadier energy and a clearer head within the first 2–4 weeks — a signal you can feel while you wait for the one you can measure.</p>""",
        "Protect Your Energy"))
    reasons.append(reason(6, "r8-labslip.jpg", "Lab report on a desk with reading glasses", "📊 Lab-Slip Results",
        "The results show up where it counts — your bloodwork",
        """      <p>This isn't about feeling vaguely "healthier." Women with stubborn numbers report drops that years of discipline never produced: 268 to 176 in five months. 263 to 189 in eight weeks. 234 to 158 in three months. Meaningful changes typically show at the 8–10 week mark — which is why Lunessa recommends bloodwork around week eight. Your labs decide, not us.</p>""",
        "Let Your Next Lab Slip Decide"))
    reasons.append(reason(7, "r11-guarantee.jpg", "Lunessa bottle on a pedestal in soft studio light", "🛡️ Risk Free",
        "Backed by a full 90-day money-back guarantee",
        """      <p>Ninety days is enough time to make the one change Lunessa asks for — two gummies a day — get bloodwork at week eight, and set it next to your baseline. If your numbers don't improve, every penny back. No forms, no fight, no questions.</p>
      <p>A company that lets your lab slip be the referee isn't guessing.</p>""",
        "Try It Risk-Free Today"))

    # testimonial between reasons 6 and 7
    reasons.insert(6, f"""    <div class="testimonial">
      <div class="testimonial-stars">★★★★★</div>
      <p class="testimonial-text">{v["testimonial_text"]}</p>
      <p class="testimonial-author">— {v["testimonial_author"]} <span class="verified-badge">Verified</span></p>
    </div>""")

    reasons_html = "\n\n".join(reasons)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{v["title"]}</title>
  <style>
{CSS}
  </style>
</head>
<body>

  <div class="page">

    <div class="eyebrow">{v["eyebrow"]}</div>

    <h1 class="headline">{v["headline"]}</h1>

    <div class="byline">
      <img src="../genetic/images/author.jpg" alt="Susan Hartley" class="author-avatar">
      <span>By <b>Susan Hartley</b></span>·<span>Last Updated July 2026</span>·<span class="stars">★★★★★</span><b>4.8/5</b>
    </div>

    <p class="hook-quote">"Read this BEFORE your next lipid panel."</p>

{MASTER_TABLE}

    <div class="tldr">{v["tldr"]}</div>

{reasons_html}

    <div class="guarantee-banner">
      <p class="guarantee-title">🛡️ 90-Day Money-Back Guarantee</p>
      <p>Try Lunessa risk-free. If your numbers don't improve within 90 days, you'll receive a full refund. No questions asked.</p>
    </div>

    <!-- CLOSE -->
    <div class="close-section">
      <p><strong>Reaching #7 means one thing: you're serious about your next lab report.</strong></p>
      <p>You now know more about how cholesterol actually works than most people ever will — the three pathways, the real doses, the contamination problem, the CoQ10 drain. The only question left is whether your next blood draw looks like your last one.</p>

      <img src="../genetic/images/product-hero.jpg" alt="Lunessa Red Yeast Rice + CoQ10 gummy supplement" class="section-image" style="max-width: 480px; margin-left: auto; margin-right: auto;">

      <div class="cta-wrap" style="margin-top: 28px;">
        <a href="{PDP}" class="cta-btn">Claim Buy 2, Get 1 Free →</a>
        <span class="cta-sub">Free Shipping · 90-Day Guarantee · No Subscription Required · While Supplies Last</span>
      </div>

      <div class="trust-badges">
        <div class="trust-badge">✓ Third-Party Tested</div>
        <div class="trust-badge">✓ Citrinin-Free Certified</div>
        <div class="trust-badge">✓ GMP Certified</div>
        <div class="trust-badge">✓ FDA-Registered Facility</div>
        <div class="trust-badge">✓ 90-Day Money-Back</div>
      </div>
    </div>

    <!-- SELLOUT -->
    <div class="sellout">
      <h3>Sell-out risk: high</h3>
      <p>Lunessa is made in small, third-party-tested batches at full clinical doses — no fillers, no shortcuts — and when a batch sells out, restocks can take weeks. As of this week, Lunessa is in stock with the Buy 2, Get 1 Free offer, while supplies last.</p>
    </div>

    <!-- FAQ -->
    <div class="faq-section">
      <h2 class="faq-heading">Frequently Asked Questions</h2>

      <div class="faq-item">
        <button class="faq-question">When will I see results?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>Most women notice energy changes within 2–4 weeks. Meaningful lab changes typically show at the 8–10 week mark. We recommend bloodwork around week eight to compare against your baseline.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">{v["faq_q"]}<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>{v["faq_a"]}</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">I've tried red yeast rice before and it didn't work.<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>Check the label of what you took. Most bottles contain 600mg per serving — a quarter of the 2,400mg used in the clinical research. Lunessa delivers the full research doses: 2,400mg red yeast rice plus 200mg CoQ10 per serving. Dose is usually the difference.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">Why not just buy red yeast rice and CoQ10 separately?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>You could — if you can find a red yeast rice with disclosed, standardized monacolin K, certified citrinin-free, at 2,400mg, plus a separate pharmaceutical-grade 200mg CoQ10. That's two hard-to-find bottles, a bigger monthly bill, and six capsules a day. Lunessa is both, at full doses, in two gummies.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">Can I take Lunessa alongside my statin?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>Many women use Lunessa while working with their doctor on the right long-term plan. Because red yeast rice works on the same pathway as statins, always talk to your physician before combining or changing anything.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">Will it cause the muscle pain and fog I've heard about with statins?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>Those effects are largely tied to CoQ10 depletion — the same pathway that makes cholesterol also makes CoQ10. Lunessa includes 200mg of CoQ10 per serving specifically to replace what cholesterol management depletes.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">Is it safe long-term? What about contamination?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>Every batch is third-party tested and certified citrinin-free (a toxin found in poorly fermented red yeast rice). Sugar-free, vegan, made in a GMP-certified, FDA-registered facility, with a published certificate of analysis.</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-question">What if it doesn't work for me?<span class="faq-icon">+</span></button>
        <div class="faq-answer"><p>90-day money-back guarantee. If your numbers don't improve, full refund. No questions.</p></div>
      </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
      <p>This article is paid editorial content. Testimonials reflect individual experiences and are not guaranteed outcomes; results may vary. Comparison tables reflect typical label values across the retail category and are not statements about any specific brand. These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease. Consult your physician before starting any supplement, especially if you are currently taking medication. Do not discontinue prescribed medications without speaking with your physician.</p>
      <p style="margin-top: 12px;">
        &copy; 2026 Lunessa. All rights reserved. &nbsp;·&nbsp;
        <a href="#">Privacy Policy</a> &nbsp;·&nbsp;
        <a href="#">Terms of Service</a> &nbsp;·&nbsp;
        <a href="#">Contact Us</a>
      </p>
    </div>

  </div>

  <!-- Sticky CTA -->
  <div class="sticky-cta" id="stickyCta">
    <a href="{PDP}" class="sticky-cta-btn">Try Lunessa Risk-Free →</a>
    <span class="sticky-cta-sub">90-Day Money-Back Guarantee · Free Shipping</span>
  </div>

  <script>
    document.querySelectorAll('.faq-question').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        var item = this.parentElement;
        var wasOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(function(el) {{ el.classList.remove('open'); }});
        if (!wasOpen) {{ item.classList.add('open'); }}
      }});
    }});

    (function() {{
      var trigger = document.getElementById('sticky-trigger');
      var bar = document.getElementById('stickyCta');
      if (!trigger || !bar) return;
      function onScroll() {{
        var passed = trigger.getBoundingClientRect().top < window.innerHeight;
        bar.classList.toggle('visible', passed);
        document.body.classList.toggle('cta-visible', passed);
      }}
      window.addEventListener('scroll', onScroll, {{ passive: true }});
      onScroll();
    }})();

    (function() {{
      var params = new URLSearchParams(window.location.search);
      var hasParams = false;
      params.forEach(function() {{ hasParams = true; }});
      if (!hasParams) return;
      document.querySelectorAll('a[href*="getlunessa.co"]').forEach(function(a) {{
        try {{
          var url = new URL(a.href);
          params.forEach(function(v, k) {{ url.searchParams.set(k, v); }});
          a.href = url.toString();
        }} catch (e) {{}}
      }});
    }})();
  </script>

</body>
</html>
"""


VARIANTS = {
    "7-reasons-genetic": {
        "title": "7 Reasons Why These Gummies Are the #1 Natural Choice for Genetic High Cholesterol in 2026",
        "eyebrow": "2026 Buyer's Guide · Genetic Cholesterol",
        "headline": "7 Reasons Why These Gummies Are the #1 Natural Choice for Genetic High Cholesterol in 2026",
        "tldr": "TLDR: Lunessa's Red Yeast Rice + CoQ10 gummies have 7 advantages no other cholesterol supplement matches — especially for stubborn, inherited numbers 👇",
        "r1_body": """      <p>If high cholesterol runs in your family, your liver doesn't just make cholesterol — it over-makes it, by genetic design, around the clock. And since <strong>75–80% of the cholesterol in your blood comes from your liver</strong>, not your plate, years of oatmeal and discipline never stood a chance. Lunessa's red yeast rice works on the same liver enzyme prescription drugs target — the source, not the sliver.</p>""",
        "r2_body": """      <p>Genetic high cholesterol is three problems at once: your liver over-produces (production), your LDL receptors under-clear (clearance), and the LDL left circulating oxidizes into the form that actually builds plaque (oxidation).</p>
      <p>Statins and standalone red yeast rice address production only. Lunessa's full-spectrum red yeast rice supports production <em>and</em> clearance, while 200mg of CoQ10 defends against oxidation. <strong>Three pathways. One serving.</strong></p>""",
        "r10_body": """      <p>You've already proven discipline was never the problem — the clean eating, the running, the labels read like contracts. Lunessa asks for exactly one change: two gummies a day. It fits into the life you already have.</p>""",
        "testimonial_text": "\"Eleven years of oatmeal, fish oil, and running 15 miles a week. LDL never budged from 263. Eight weeks on Lunessa: 189. My husband eats Domino's. His is 172. I cried when I saw my number.\"",
        "testimonial_author": "Rachel T., 49",
        "faq_q": "My cholesterol is genetic. Can anything natural actually help?",
        "faq_a": "Genetic high cholesterol means your liver overproduces LDL and clears it slowly — which is why diet alone rarely moves the number. Red yeast rice works on the same liver pathway that prescription treatments target while supporting the receptors that clear LDL from your blood — and CoQ10 addresses the third pathway, oxidation. It's one of the few natural approaches built for all three pathways instead of one.",
    },
    "7-reasons-menopause": {
        "title": "7 Reasons Why These Gummies Are the #1 Natural Cholesterol Choice for Women Over 50 in 2026",
        "eyebrow": "2026 Buyer's Guide · Cholesterol After 50",
        "headline": "7 Reasons Why These Gummies Are the #1 Natural Cholesterol Choice for Women Over 50 in 2026",
        "tldr": "TLDR: Lunessa's Red Yeast Rice + CoQ10 gummies have 7 advantages no other cholesterol supplement matches — especially for women whose numbers jumped after menopause 👇",
        "r1_body": """      <p>If your number was fine for thirty years and jumped after menopause, the cause was never your plate. <strong>75–80% of the cholesterol in your blood is made by your own liver</strong> — and estrogen used to keep that production quietly in check. When it left, the output climbed, no matter what you ate. Lunessa's red yeast rice works on the same liver enzyme prescription drugs target — the thing that actually changed.</p>""",
        "r2_body": """      <p>Menopause breaks three things at once: your liver makes more cholesterol (production), your body pulls less of it back out (clearance), and what lingers in your blood oxidizes into the form that actually builds plaque (oxidation). All three were estrogen's quiet jobs.</p>
      <p>Statins and standalone red yeast rice address production only. Lunessa's full-spectrum red yeast rice supports production <em>and</em> clearance, while 200mg of CoQ10 defends against oxidation. <strong>Three pathways. One serving.</strong></p>""",
        "r10_body": """      <p>You've already punished your kitchen for a number your kitchen didn't cause. Lunessa asks for exactly one change: two gummies a day. It fits into the life you already have — including the birthday cake you've been skipping for no reason.</p>""",
        "testimonial_text": "\"My numbers were fine my entire life. Two years after menopause, my LDL was up 44 points and my doctor said the word 'statin.' Three months on Lunessa and my recheck came back 47 points lower. She looked at the chart twice and said 'whatever you're doing, keep doing it.'\"",
        "testimonial_author": "Linda S., 61",
        "faq_q": "My cholesterol was fine until menopause. Will this help me?",
        "faq_a": "That's exactly who Lunessa was formulated for. When estrogen declines, your liver makes more cholesterol, your body clears less of it, and what lingers in your blood oxidizes unprotected. Lunessa was built around that exact set of changes — the system that actually flipped at menopause.",
    },
}

for slug, v in VARIANTS.items():
    outdir = os.path.join(HERE, "public", slug)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w") as f:
        f.write(build(v))
    print("built", slug)
