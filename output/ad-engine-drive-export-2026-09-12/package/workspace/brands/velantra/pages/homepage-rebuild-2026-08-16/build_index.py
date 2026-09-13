import json

CDN = "https://cdn.shopify.com/s/files/1/0627/4092/2433/files"

HERO = """<div class="v2-hero">
  <div class="v2-hero-text">
    <div class="v2-hero-inner">
      <p class="v2-eyebrow">Velantra</p>
      <h1 class="v2-hero-title">Luxury, without the logo.</h1>
      <p class="v2-hero-sub">Structured bags in leather, canvas, and solid brass, covered for two full years. The price reflects the build, never a label.</p>
      <div class="v2-hero-ctas">
        <a class="v2-btn v2-btn-solid" href="/collections/handbags">Shop Now</a>
      </div>
    </div>
  </div>
  <div class="v2-hero-img">
    <img src="{CDN}/weekender-blk-07-hardware.png?v=1786307208&width=1400" alt="The Eleanor Weekender in black leather with solid brass hardware">
  </div>
</div>

<style>
  .v2-hero { display: grid; grid-template-columns: 1fr 1fr; width: 100%; background: #F6F3EE; }
  .v2-hero-text { display: flex; align-items: center; justify-content: center; padding: 72px 48px; }
  .v2-hero-inner { max-width: 470px; }
  .v2-eyebrow { font-size: 0.78rem; letter-spacing: 0.26em; text-transform: uppercase; opacity: 0.6; margin-bottom: 20px; }
  .v2-hero-title { font-size: clamp(38px, 4.6vw, 62px); font-weight: 600; line-height: 1.04; margin-bottom: 20px; color: #1a1a1a; }
  .v2-hero-sub { font-size: clamp(15px, 1.4vw, 18px); line-height: 1.6; color: #1a1a1a; opacity: 0.82; margin-bottom: 30px; }
  .v2-hero-ctas { display: flex; gap: 14px; flex-wrap: wrap; }
  .v2-btn { display: inline-block; padding: 15px 30px; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; text-decoration: none; border-radius: 2px; }
  a.v2-btn-solid { background: #1a1a1a !important; color: #ffffff !important; border: 1px solid #1a1a1a !important; text-decoration: none !important; }
  a.v2-btn-solid:visited { color: #ffffff !important; }
  a.v2-btn-solid:hover { background: #333333 !important; color: #ffffff !important; }
  a.v2-btn-ghost { border: 1px solid #1a1a1a !important; color: #1a1a1a !important; background: transparent !important; text-decoration: none !important; }
  a.v2-btn-ghost:visited { color: #1a1a1a !important; }
  a.v2-btn-ghost:hover { background: #1a1a1a !important; color: #ffffff !important; }
  .v2-hero-img { min-height: 0; }
  .v2-hero-img img { width: 100%; height: 100%; min-height: 520px; object-fit: cover; display: block; }
  @media (max-width: 780px) {
    .v2-hero { grid-template-columns: 1fr; }
    .v2-hero-img { order: -1; }
    .v2-hero-img img { min-height: 0; height: 64vw; }
    .v2-hero-text { padding: 40px 24px 48px; }
    .v2-hero-inner { text-align: center; }
    .v2-hero-ctas { justify-content: center; }
  }
</style>
""".replace("{CDN}", CDN)

SILHOUETTES = """<div class="v2-sil">
  <div class="v2-sil-head">
    <p class="v2-eyebrow">The Collection</p>
    <h2 class="v2-h2">Find your silhouette</h2>
    <p class="v2-sub">Each bag is built for a different day of your week.</p>
  </div>
  <div class="v2-sil-grid">
    {%- assign m = all_products['velantra-margot-tote'] -%}
    <a class="v2-sil-card" href="{{ m.url }}">
      <div class="v2-sil-img">{{ m.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', alt: m.title }}</div>
      <p class="v2-sil-role">The Work Tote</p>
      <h3 class="v2-sil-name">{{ m.title }}</h3>
      <p class="v2-sil-price">{{ m.price | money }}</p>
      <p class="v2-sil-line">Carries the laptop and keeps its posture.</p>
    </a>
    {%- assign e = all_products['velantra-weekender'] -%}
    <a class="v2-sil-card" href="{{ e.url }}">
      <div class="v2-sil-img">{{ e.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', alt: e.title }}</div>
      <p class="v2-sil-role">The Weekender</p>
      <h3 class="v2-sil-name">{{ e.title }}</h3>
      <p class="v2-sil-price">{{ e.price | money }}</p>
      <p class="v2-sil-line">Three days away in one unchecked bag.</p>
    </a>
    {%- assign d = all_products['velantra-delphine'] -%}
    <a class="v2-sil-card" href="{{ d.url }}">
      <div class="v2-sil-img">{{ d.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', alt: d.title }}</div>
      <p class="v2-sil-role">The Top Handle</p>
      <h3 class="v2-sil-name">{{ d.title }}</h3>
      <p class="v2-sil-price">{{ d.price | money }}</p>
      <p class="v2-sil-line">For dinners and everywhere polished.</p>
    </a>
    {%- assign c = all_products['the-colette-wool-tote'] -%}
    <a class="v2-sil-card" href="{{ c.url }}">
      <div class="v2-sil-img">{{ c.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', alt: c.title }}</div>
      <p class="v2-sil-role">The Carryall</p>
      <h3 class="v2-sil-name">{{ c.title }}</h3>
      <p class="v2-sil-price">{{ c.price | money }}</p>
      <p class="v2-sil-line">Brushed wool for the cold months.</p>
    </a>
  </div>
  <div class="v2-sil-all"><a href="/collections/handbags">Shop all handbags &rarr;</a></div>
</div>

<style>
  .v2-sil { max-width: 1240px; margin: 0 auto; padding: 64px 20px 56px; }
  .v2-sil-head { text-align: center; max-width: 560px; margin: 0 auto 42px; }
  .v2-h2 { font-size: clamp(26px, 3vw, 38px); font-weight: 600; margin: 10px 0 12px; }
  .v2-sub { font-size: 1rem; line-height: 1.6; opacity: 0.8; }
  .v2-sil-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
  .v2-sil-card { display: block; text-decoration: none; color: inherit; }
  .v2-sil-img img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; display: block; }
  .v2-sil-role { font-size: 0.75rem; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.6; margin: 16px 0 4px; }
  .v2-sil-name { font-size: 1.1rem; font-weight: 600; margin: 0 0 2px; }
  .v2-sil-price { font-size: 0.98rem; margin: 0 0 8px; opacity: 0.85; }
  .v2-sil-line { font-size: 0.93rem; line-height: 1.5; opacity: 0.75; }
  .v2-sil-all { text-align: center; margin-top: 40px; }
  .v2-sil-all a { font-size: 0.95rem; font-weight: 600; color: inherit; text-decoration: underline; text-underline-offset: 4px; }
  @media (max-width: 900px) { .v2-sil-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 520px) { .v2-sil-grid { grid-template-columns: 1fr; gap: 32px; } }
</style>
"""

VALUE = """<div class="v2-value">
  <div class="v2-value-head">
    <p class="v2-eyebrow">Where the money goes</p>
    <h2 class="v2-h2">What you are paying for</h2>
    <p class="v2-sub">What we skip is the logo, and the markup that comes with it.</p>
  </div>
  <div class="v2-value-grid">
    <div class="v2-value-col">
      <img src="{CDN}/weekender-blk-01-front.png?v=1786307190&width=800" alt="Black leather bag with structured body" loading="lazy">
      <h3 class="v2-value-title">Leather with structure</h3>
      <p class="v2-value-text">Bodies that stand on their own and materials that earn character with age.</p>
    </div>
    <div class="v2-value-col">
      <img src="{CDN}/weekender-dc-07-hardware.png?v=1786228302&width=800" alt="Solid brass turn-lock hardware" loading="lazy">
      <h3 class="v2-value-title">Solid brass hardware</h3>
      <p class="v2-value-text">Turn-locks, fittings, and feet in real brass, with weight you can feel.</p>
    </div>
    <div class="v2-value-col">
      <img src="{CDN}/weekender-blk-interior-tripleflap.png?v=1786927857&width=800" alt="Finished interior of a Velantra bag" loading="lazy">
      <h3 class="v2-value-title">Finished inside and out</h3>
      <p class="v2-value-text">Reinforced stitching and interiors built as carefully as the exterior.</p>
    </div>
  </div>
</div>

<style>
  .v2-value { background: #F6F3EE; padding: 64px 20px; }
  .v2-value-head { text-align: center; max-width: 560px; margin: 0 auto 42px; }
  .v2-value-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 1240px; margin: 0 auto; }
  .v2-value-col { text-align: center; }
  .v2-value-col img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; margin-bottom: 18px; }
  .v2-value-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
  .v2-value-text { font-size: 0.95rem; line-height: 1.6; opacity: 0.8; max-width: 320px; margin: 0 auto; }
  @media (max-width: 780px) { .v2-value-grid { grid-template-columns: 1fr; gap: 36px; } }
</style>
""".replace("{CDN}", CDN)

WARRANTY = """<div class="v2-warranty">
  <p class="v2-warranty-eyebrow">The Two-Year Promise</p>
  <h2 class="v2-warranty-title">Guaranteed for two years.<br>Built for decades.</h2>
  <p class="v2-warranty-text">Every Velantra bag comes with two full years of coverage and free replacement. We can promise that because of how they are built.</p>
</div>

<style>
  .v2-warranty { background: #191919; color: #F6F3EE; text-align: center; padding: 76px 24px; }
  .v2-warranty-eyebrow { font-size: 0.78rem; letter-spacing: 0.26em; text-transform: uppercase; opacity: 0.65; margin-bottom: 18px; }
  .v2-warranty-title { font-size: clamp(28px, 3.6vw, 46px); font-weight: 600; line-height: 1.15; margin-bottom: 18px; color: #F6F3EE; }
  .v2-warranty-text { font-size: 1rem; line-height: 1.65; opacity: 0.85; max-width: 520px; margin: 0 auto; }
</style>
"""

PHILOSOPHY = """<div class="v2-philo">
  <p class="v2-eyebrow">Our Philosophy</p>
  <h2 class="v2-h2">Built to last decades, not seasons.</h2>
  <p class="v2-philo-text">Velantra is for the woman who knows what a bag should actually cost. We put the money into leather, brass, and stitching, and we leave the logo off. What is left is a bag that strangers ask about for years.</p>
  <a class="v2-btn v2-btn-ghost" href="/collections/handbags">Explore the Collection</a>
</div>

<style>
  .v2-philo { max-width: 640px; margin: 0 auto; text-align: center; padding: 36px 24px 52px; }
  .v2-philo .v2-h2 { margin: 12px 0 16px; }
  .v2-philo-text { font-size: 1.02rem; line-height: 1.7; opacity: 0.85; margin-bottom: 30px; }
</style>
"""

def adv(code, full_width=True):
    return {
        "type": "advanced-content",
        "blocks": {"liq": {"type": "liquid", "settings": {"code": code, "width": "100%", "alignment": "center"}}},
        "block_order": ["liq"],
        "settings": {"full_width": full_width, "space_around": False},
    }

# press_cbs carried over verbatim from the live template
press = json.load(open("index_current.json"))["sections"]["press_cbs"]

template = {
    "sections": {
        "hero": adv(HERO),
        "press_cbs": press,
        "silhouettes": adv(SILHOUETTES),
        "warranty": adv(WARRANTY),
        "bags_accessories": {
            "type": "promo-grid",
            "blocks": {
                "advanced_gnzTTq": {
                    "type": "advanced",
                    "settings": {
                        "subheading": "",
                        "heading": "The Bags",
                        "heading_size": "h2",
                        "textarea": "Structured silhouettes in leather and canvas.",
                        "cta_text1": "SHOP NOW",
                        "cta_link1": "shopify://collections/handbags",
                        "cta_text2": "",
                        "cta_link2": "",
                        "image": "shopify://shop_images/margot-black-hero.jpg",
                        "video_url": "",
                        "width": "50",
                        "height": 500,
                        "text_align": "vertical-center horizontal-center",
                        "color_accent": "rgba(0,0,0,0)",
                        "boxed": False,
                        "framed": False,
                    },
                },
                "advanced_hCD3yy": {
                    "type": "advanced",
                    "settings": {
                        "subheading": "",
                        "heading": "The Finishing Touches",
                        "heading_size": "h2",
                        "textarea": "Scarves, charms, and organizers to make it yours.",
                        "cta_text1": "Shop Now",
                        "cta_link1": "shopify://collections/accessories",
                        "cta_text2": "",
                        "cta_link2": "",
                        "image": "shopify://shop_images/delphine-dark-chocolate-04-hardware_871401db-bdc0-49ff-b532-6fbe415cff5d.png",
                        "video_url": "",
                        "width": "50",
                        "height": 500,
                        "text_align": "vertical-center horizontal-center",
                        "color_accent": "rgba(0,0,0,0)",
                        "boxed": False,
                        "framed": False,
                    },
                },
            },
            "block_order": ["advanced_gnzTTq", "advanced_hCD3yy"],
            "settings": {"full_width": False, "gutter_size": 20, "space_above": True, "space_below": False},
        },
        "philosophy": adv(PHILOSOPHY, full_width=False),
        "newsletter": {
            "type": "newsletter",
            "blocks": {
                "title": {"type": "title", "settings": {"title": "Join the list", "heading_size": "h2"}},
                "text": {"type": "text", "settings": {"text": "<p>Be first to new silhouettes, colorways, and restocks.</p>"}},
                "form": {"type": "form"},
            },
            "block_order": ["title", "text", "form"],
            "settings": {"align_text": "center"},
        },
    },
    "order": [
        "hero",
        "press_cbs",
        "silhouettes",
        "warranty",
        "bags_accessories",
        "philosophy",
        "newsletter",
    ],
}

out = json.dumps(template, indent=2)
open("index_new.json", "w").write(out)
# request body for the Assets API
body = {"asset": {"key": "templates/index.json", "value": out}}
open("index_put_body.json", "w").write(json.dumps(body))
print("built", len(out), "bytes")
