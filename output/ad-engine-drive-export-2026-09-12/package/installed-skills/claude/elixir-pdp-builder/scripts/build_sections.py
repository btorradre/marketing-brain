#!/usr/bin/env python3
"""
build_sections.py — render the fixed custom-section set with a brand's palette + images,
push them to the Elixir theme, and wire them into templates/product.json (below the buy box).

Before running this, Claude should have:
  1. produced palette.json   (scripts/extract_palette.py)
  2. rewritten the example copy inside each templates/*.liquid for THIS brand
     (from the research docs — pains, mechanism, FAQ objections, reviews)
  3. produced images.json mapping __IMG_*__ tokens -> uploaded asset/CDN URLs

Usage: python build_sections.py palette.json [images.json] [--theme <id>] [--order rv-feeling-worse,...]
"""
import sys, os, json, argparse, glob, subprocess
sys.path.insert(0, os.path.dirname(__file__))
import shopify_api as S

TPL_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
DEFAULT_ORDER = ['rv-feeling-worse', 'rv-core', 'rv-stages', 'rv-compare',
                 'rv-timeline', 'rv-results', 'rv-reviews', 'rv-faq']

def render(text, palette, images):
    for role, val in palette.items():
        text = text.replace('__%s__' % role, val)
    for tok, url in (images or {}).items():
        text = text.replace(tok, url)
    return text

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('palette'); ap.add_argument('images', nargs='?')
    ap.add_argument('--theme'); ap.add_argument('--order')
    a = ap.parse_args()
    palette = json.load(open(a.palette))
    images = json.load(open(a.images)) if a.images else {}
    theme = a.theme or S.active_theme()
    order = (a.order.split(',') if a.order else DEFAULT_ORDER)

    # 1) render + push each section file that exists as a template
    pushed = []
    for name in order:
        fp = os.path.join(TPL_DIR, name + '.liquid')
        if not os.path.exists(fp):
            print('skip (no template):', name); continue
        body = render(open(fp).read(), palette, images)
        S.put_asset(theme, 'sections/%s.liquid' % name, body)
        pushed.append(name); print('pushed', name)

    # 2) wire into product template order (after the buy box; never reorder buy-box blocks)
    t = json.loads(S.get_asset(theme, 'templates/product.json'))
    keep_top = [s for s in t['order'] if s in t['sections'] and
                t['sections'][s]['type'] in ('shop-product-details', 'sticky-add-to-cart')]
    for name in pushed:
        sid = name.replace('-', '_')
        t['sections'][sid] = {'type': name, 'settings': {}}
    t['order'] = keep_top + [n.replace('-', '_') for n in pushed]
    S.put_asset(theme, 'templates/product.json', json.dumps(t, ensure_ascii=False))
    print('order:', t['order'])

if __name__ == '__main__':
    main()
