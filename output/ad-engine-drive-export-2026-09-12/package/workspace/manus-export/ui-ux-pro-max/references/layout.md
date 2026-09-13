# Layout & Responsive (Priority 5 — HIGH)

## Core rules

- `width=device-width, initial-scale=1` in the viewport meta tag — never disable zoom.
- Design mobile-first, then scale up to tablet and desktop.
- Use a systematic, consistent set of breakpoints (e.g. 375 / 768 / 1024 / 1440).
- Minimum 16px body text on mobile (smaller triggers unwanted auto-zoom on iOS Safari).
- Line length: roughly 35-60 characters on mobile, 60-75 on desktop.
- No horizontal scroll on mobile — content must fit the viewport width.
- Use an incremental spacing system (4pt/8dp) rather than arbitrary spacing values.
- Keep component spacing comfortable for touch — not so cramped it causes mis-taps.
- Use a consistent max-width container on desktop.
- Define an explicit, layered z-index scale (e.g. 0/10/20/40/100/1000) rather than ad hoc values.
- A fixed navbar or bottom bar must reserve safe padding so it never covers underlying content.
- Avoid nested scroll regions that fight with the main page scroll.
- Prefer a dynamic viewport height unit over a flat 100vh on mobile (address-bar resize issues).
- Keep the layout readable and operable in landscape orientation, not just portrait.
- Show core content first on mobile; fold or hide secondary content behind disclosure.
- Establish visual hierarchy through size, spacing, and contrast — never color alone.

## Layout & spacing (app) — Do / Don't

| Rule | Do | Don't |
|---|---|---|
| Safe-area compliance | Respect top/bottom safe areas for fixed headers, tab bars, CTA bars | Fixed UI placed under the notch, status bar, or gesture area |
| System bar clearance | Spacing for status/nav bars and the gesture home indicator | Tappable content colliding with OS chrome |
| Consistent content width | Predictable content width per device class | Mixing arbitrary widths between screens |
| 8dp spacing rhythm | Consistent 4/8dp spacing system for padding/gaps/section spacing | Random spacing increments with no rhythm |
| Readable text measure | Long-form text stays readable on large devices | Edge-to-edge paragraphs on tablets |
| Section spacing hierarchy | Clear vertical rhythm tiers (e.g. 16/24/32/48) by hierarchy | Similar UI levels with inconsistent spacing |
| Adaptive gutters by breakpoint | Larger horizontal insets on wider widths and in landscape | Same narrow gutter on every device size/orientation |
| Scroll and fixed-element coexistence | Bottom/top content insets so lists aren't hidden behind fixed bars | Scroll content obscured by sticky headers/footers |

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Responsive + Layout categories (15 rows) and `app-interface.csv` Safe Areas category (1 row).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 15 | Layout | Z-Index Management | Web | Stacking context conflicts cause hidden elements | `Define z-index scale system (10 20 30 50)` | `Use arbitrary large z-index values` | `z-10 z-20 z-50` | `z-[9999]` | High |
| 16 | Layout | Overflow Hidden | Web | Hidden overflow can clip important content | `Test all content fits within containers` | `Blindly apply overflow-hidden` | `overflow-auto with scroll` | `overflow-hidden truncating content` | Medium |
| 17 | Layout | Fixed Positioning | Web | Fixed elements can overlap or be inaccessible | `Account for safe areas and other fixed elements` | `Stack multiple fixed elements carelessly` | `Fixed nav + fixed bottom with gap` | `Multiple overlapping fixed elements` | Medium |
| 18 | Layout | Stacking Context | Web | New stacking contexts reset z-index | `Understand what creates new stacking context` | `Expect z-index to work across contexts` | `Parent with z-index isolates children` | `z-index: 9999 not working` | Medium |
| 19 | Layout | Content Jumping | Web | Layout shift when content loads is jarring | `Reserve space for async content` | `Let images/content push layout around` | `aspect-ratio or fixed height` | `No dimensions on images` | High |
| 20 | Layout | Viewport Units | Web | 100vh can be problematic on mobile browsers | `Use dvh or account for mobile browser chrome` | `Use 100vh for full-screen mobile layouts` | `min-h-dvh or min-h-screen` | `h-screen on mobile` | Medium |
| 21 | Layout | Container Width | Web | Content too wide is hard to read | `Limit max-width for text content (65-75ch)` | `Let text span full viewport width` | `max-w-prose or max-w-3xl` | `Full width paragraphs` | Medium |
| 64 | Responsive | Mobile First | Web | Design for mobile then enhance for larger | `Start with mobile styles then add breakpoints` | `Desktop-first causing mobile issues` | `Default mobile + md: lg: xl:` | `Desktop default + max-width queries` | Medium |
| 65 | Responsive | Breakpoint Testing | Web | Test at all common screen sizes | `Test at 320 375 414 768 1024 1440` | `Only test on your device` | `Multiple device testing` | `Single device development` | Medium |
| 66 | Responsive | Touch Friendly | Web | Mobile layouts need touch-sized targets | `Increase touch targets on mobile` | `Same tiny buttons on mobile` | `Larger buttons on mobile` | `Desktop-sized targets on mobile` | High |
| 67 | Responsive | Readable Font Size | All | Text must be readable on all devices | `Minimum 16px body text on mobile` | `Tiny text on mobile` | `text-base or larger` | `text-xs for body text` | High |
| 68 | Responsive | Viewport Meta | Web | Set viewport for mobile devices | `Use width=device-width initial-scale=1` | `Missing or incorrect viewport` | `<meta name='viewport'...>` | `No viewport meta tag` | High |
| 69 | Responsive | Horizontal Scroll | Web | Avoid horizontal scrolling | `Ensure content fits viewport width` | `Content wider than viewport` | `max-w-full overflow-x-hidden` | `Horizontal scrollbar on mobile` | High |
| 70 | Responsive | Image Scaling | Web | Images should scale with container | `Use max-width: 100% on images` | `Fixed width images overflow` | `max-w-full h-auto` | `width='800' fixed` | Medium |
| 71 | Responsive | Table Handling | Web | Tables can overflow on mobile | `Use horizontal scroll or card layout` | `Wide tables breaking layout` | `overflow-x-auto wrapper` | `Table overflows viewport` | Medium |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 28 | Safe Areas | Safe Area Insets | safe area insets notch gesture | iOS/Android/React Native | Content must not overlap notches/gesture bars | `Wrap screens in SafeAreaView or apply insets` | `Place tappable content under system bars` | `<SafeAreaView style={{ flex: 1 }}><Screen /></SafeAreaView>` | `<View style={{ flex: 1 }}><Screen /></View>` | High |
