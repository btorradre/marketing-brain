#!/usr/bin/env python3
"""
recolor_theme.py — apply a brand palette to the Elixir theme NATIVELY (no CSS overlay).

Writes the palette into config/settings_data.json (5 color schemes + global tokens + cart
drawer + body background + announcement banner) and sections/header-group.json, then sweeps
every sections/*.liquid + snippets/*.liquid for leftover Elixir-demo blue/navy hexes.

Usage: python recolor_theme.py palette.json [--theme <id>]
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
import shopify_api as S

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('palette'); ap.add_argument('--theme')
    a = ap.parse_args()
    P = json.load(open(a.palette)); theme = a.theme or S.active_theme()
    BRAND, DEEP, DARKB = P['BRAND'], P['BRAND_DEEP'], P['BRAND_DARK']
    DARK, MAROON, GOLD, GOLDL = P['DARK'], P['MAROON'], P['GOLD'], P['GOLD_LT']
    CREAM, PAPER, OFF, INK, MUTED, LIGHT, LINE, GREEN = (P['CREAM'], P['PAPER'], P['OFF'],
        P['INK'], P['MUTED'], P['LIGHT'], P['LINE'], P['GREEN'])

    # ---- settings_data.json ----
    sd = json.loads(S.get_asset(theme, 'config/settings_data.json')); c = sd['current']
    g = {
      'global_section_text_color': LIGHT, 'global_section_accent_1_color': GOLD,
      'global_section_accent_2_color': GOLDL, 'global_section_button_color': BRAND,
      'global_section_button_text_color': '#ffffff',
      'global_header_color': '#ffffff', 'header_border_color': LINE,
      'global_footer_color': DARK, 'global_dropdown_color': OFF,
      'global_button_background_color': BRAND, 'global_button_text_color_primary': '#ffffff',
      'global_button_border_color': BRAND, 'global_button_hover_bg_color': GOLD,
      'global_button_hover_text_color': DARK,
      'button_gradient_start': BRAND, 'button_gradient_end': DEEP,
      'button_gradient_hover_start': GOLD, 'button_gradient_hover_end': P['GOLD_DK'],
      # body background (kills the demo navy gradient)
      'global_section_use_gradient_background': False,
      'global_section_background_color': '#ffffff',
      'global_section_gradient_background':
          'linear-gradient(180deg, rgba(255,255,255,1), rgba(255,255,255,1) 100%)',
      'global_section_gradient_color_1': BRAND, 'global_section_gradient_color_2': GOLD,
      # menu drawer
      'global_drawer_color': '#ffffff', 'global_drawer_text_color': '#121212',
      # cart drawer tokens
      'cart_drawer_primary_text_color': INK, 'cart_drawer_header_bg': CREAM,
      'cart_drawer_footer_bg': OFF, 'cart_drawer_accent_color': GOLD,
      'cart_drawer_checkout_button_bg': BRAND, 'cart_drawer_item_saving_text': BRAND,
      'cart_drawer_free_product_label_bg': GREEN, 'cart_drawer_discount_bg_color': PAPER,
      'cart_drawer_discount_text_color': BRAND, 'cart_drawer_fs_icon_active_color': BRAND,
      'cart_drawer_shipping_protection_text': INK,
      'use_theme_colors_cart_drawer': False,
      # social proof / announcement
      'social_proof_bg_color': DARK, 'social_proof_text_color': LIGHT, 'social_proof_icon_color': GOLD,
      'discount_banner_text_color': PAPER, 'discount_banner_gradient_start_color': BRAND,
      'discount_banner_gradient_end_color': DARKB,
    }
    for k, v in g.items():
        if k in c: c[k] = v
    # clear social links (remove social icons) — comment out the next line to keep them
    for k in list(c):
        if k.startswith('social_') and k.endswith('_link'): c[k] = ''
    # color schemes
    schemes = {
      'scheme-1': dict(background=PAPER, text=INK, button=BRAND, button_label='#ffffff', secondary_button_label=BRAND, accent_1=GOLD, shadow=MAROON),
      'scheme-2': dict(background=CREAM, text=INK, button=BRAND, button_label=PAPER, secondary_button_label=INK, accent_1=GOLD, shadow=MAROON),
      'scheme-3': dict(background=MAROON, text=LIGHT, button=GOLD, button_label=DARK, secondary_button_label=LIGHT, accent_1=GOLD, shadow=DARK),
      'scheme-4': dict(background=DARK, text=LIGHT, button=GOLD, button_label=DARK, secondary_button_label=LIGHT, accent_1=GOLD, shadow=DARK),
      'scheme-5': dict(background=BRAND, text=PAPER, button=GOLD, button_label=BRAND, secondary_button_label=PAPER, accent_1=GOLDL, shadow=MAROON),
    }
    for name, vals in schemes.items():
        if name in c.get('color_schemes', {}):
            c['color_schemes'][name]['settings'].update(vals)
    S.put_asset(theme, 'config/settings_data.json', json.dumps(sd, ensure_ascii=False))
    print('recolored settings_data.json')

    # ---- header-group.json (announcement bar + header) ----
    hg = json.loads(S.get_asset(theme, 'sections/header-group.json'))
    for sid, sec in hg['sections'].items():
        st = sec.get('settings', {})
        if sec.get('type') == 'custom-announcement-bar':
            st['background_color'] = BRAND; st['text_color'] = PAPER
            for i in range(1, 6):
                st[f'slide_{i}_bg_color'] = BRAND; st[f'slide_{i}_text_color'] = PAPER
        if sec.get('type') == 'header':
            st['menu_underline_color'] = GOLD; st['top_border_color'] = DARKB
    S.put_asset(theme, 'sections/header-group.json', json.dumps(hg, ensure_ascii=False))
    print('recolored header-group.json')

    # ---- sweep leftover demo blue/navy across sections + snippets ----
    cmap = {'#141720': DARK, '#242833': DARK, '#181b1d': DARK, '#1e242e': MAROON,
            '#0f203e': MAROON, '#358bff': GOLD, '#368afe': GOLD, '#85b8ff': GOLDL,
            '#6489bd': P['GOLD_DK'], '#0374a5': BRAND, '#334fb4': BRAND, '#2563eb': BRAND,
            '#133d51': MUTED, '#092d3e': INK}
    assets = S._admin('GET', f'themes/{theme}/assets.json')['assets']
    keys = [x['key'] for x in assets if x['key'].startswith(('sections/', 'snippets/')) and x['key'].endswith('.liquid')]
    n = 0
    for k in keys:
        v = S.get_asset(theme, k)
        if not v: continue
        nv = v
        for a_, b_ in cmap.items():
            nv = nv.replace(a_, b_).replace(a_.upper(), b_)
        if nv != v:
            S.put_asset(theme, k, nv); n += 1
    print('swept', n, 'files for demo blue/navy')

if __name__ == '__main__':
    main()
