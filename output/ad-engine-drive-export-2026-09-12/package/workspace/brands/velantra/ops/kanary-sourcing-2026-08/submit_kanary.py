import sys, time
sys.path.insert(0,'/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/9cf22fc3-1d55-489d-a4b5-3701c8b88be7/scratchpad')
from kanary_data import SHARED, SKUS
from playwright.sync_api import sync_playwright

URL = "https://form.jotform.com/252946341687468"
OUT = "/private/tmp/claude-503/-Users-brooksorradre2-Documents-marketing-brain/9cf22fc3-1d55-489d-a4b5-3701c8b88be7/scratchpad"
ONLY = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
DRY  = "--dry" in sys.argv

PAGE1 = ["q62_businessName","q2_q2_textbox0","q61_email","q23_productName","q63_productLink","q65_orderQuantity"]

def sf(page, name, value, required=True):
    loc = page.locator(f'[name="{name}"]')
    if loc.count() == 0:
        print(f"   !! MISSING {name}"); return
    el = loc.first
    try:
        el.fill(value, timeout=6000)
        return
    except Exception:
        pass
    try:
        if el.evaluate("e => e.tagName.toLowerCase()") == "select":
            el.select_option(value, timeout=6000); return
    except Exception:
        pass
    # JS fallback for fields JotForm keeps visually hidden
    page.evaluate("""([n,v]) => { const e = document.querySelector(`[name="${n}"]`); if(!e) return;
        e.value = v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }""", [name, value])
    print(f"   (js-set {name})")

def run(page, idx, sku):
    print(f"\n=== [{idx+1}/6] {sku['q23_productName']}")
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(3500)
    page.evaluate("""() => { for (const sel of ['#branding-footer','.jotform-footer','[class*=\"branding\"]','#stripe-branding','.formFooter']) document.querySelectorAll(sel).forEach(e=>e.remove()); }""")

    merged = dict(SHARED); merged.update(sku)

    # ---- PAGE 1 ----
    for n in PAGE1: sf(page, n, merged[n])
    page.screenshot(path=f"{OUT}/p1_{idx+1}.png", full_page=True)
    page.evaluate("()=>document.querySelector('.form-pagebreak-next').click()")
    page.wait_for_timeout(2500)

    # ---- PAGE 2 ----
    sf(page, "q94_productDetails", merged["q94_productDetails"])
    sf(page, "q95_whatImprovements", merged["q95_whatImprovements"])

    page.evaluate("""()=>{const e=document.querySelector('input[name=\"q97_areYou\"][value=\"Yes\"]'); e.click();}""")
    page.wait_for_timeout(2000)

    for n in ["q98_nameOf","q99_currentPurchase","q100_currentManufacturing","q101_productDefect",
              "q67_targetPrice","q106_targetMarkets106","q103_certificationRequirements","q107_areYou107"]:
        sf(page, n, merged[n])

    page.evaluate("""()=>{const e=document.querySelector('input[name=\"q104_howAre[]\"][value=\"Fulfilling from China\"]'); e.click();}""")

    m, d, y = SHARED["date"]
    page.locator("#lite_mode_105").fill(f"{m}-{d}-{y}")
    page.locator("#lite_mode_105").press("Tab")
    page.wait_for_timeout(1200)

    # ---- verify before submitting ----
    chk = page.evaluate("""()=>({
      date: [document.getElementById('month_105').value, document.getElementById('day_105').value, document.getElementById('year_105').value].join('-'),
      lite: document.getElementById('lite_mode_105').value,
      selling: (document.querySelector('input[name="q97_areYou"]:checked')||{}).value || null,
      fulfil: [...document.querySelectorAll('input[name="q104_howAre[]"]:checked')].map(e=>e.value),
      empty: [...document.querySelectorAll('.form-textbox, textarea')].filter(e=>e.name && e.name.startsWith('q') && !e.value && e.offsetParent).map(e=>e.name)
    })""")
    print("   verify:", chk)

    page.screenshot(path=f"{OUT}/p2_{idx+1}.png", full_page=True)
    if DRY:
        print("   DRY RUN - not submitting"); return "dry"

    page.evaluate("()=>document.querySelector('.form-submit-button').click()")
    page.wait_for_timeout(10000)
    body = page.inner_text("body").replace("\n"," ")
    ok = "error on this page" not in body.lower()
    page.screenshot(path=f"{OUT}/result_{idx+1}.png", full_page=True)
    print(f"   url={page.url}")
    print(f"   body={body[:200]}")
    print("   ->", "SUBMITTED" if ok else "FAILED")
    return "ok" if ok else "fail"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_context(viewport={"width":1400,"height":1100},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36").new_page()
    results=[]
    for i, sku in enumerate(SKUS):
        if ONLY is not None and i != ONLY: continue
        try: results.append((sku['q23_productName'], run(page, i, sku)))
        except Exception as e:
            print("   EXCEPTION:", repr(e)[:250]); results.append((sku['q23_productName'],"exception"))
        time.sleep(2)
    b.close()
print("\n==== SUMMARY ====")
for n,r in results: print(f"  {r:10} {n}")
