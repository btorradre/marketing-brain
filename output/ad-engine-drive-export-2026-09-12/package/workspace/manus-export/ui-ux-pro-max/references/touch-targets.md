# Touch & Interaction (Priority 2 — CRITICAL)

Touch targets and interaction feedback are the second most critical category — right after accessibility, before performance. Undersized or unresponsive touch controls are one of the fastest ways an interface reads as unpolished.

## Core rules

- Minimum touch target: 44×44pt (Apple) / 48×48dp (Material) — extend the hit area beyond the visual bounds if the icon itself is smaller.
- Minimum 8px/8dp gap between adjacent touch targets.
- Use click/tap for primary interactions; never rely on hover alone (hover doesn't exist on touch devices).
- Disable a button during an async operation and show a spinner or progress indicator.
- Clear error messages placed near the problem, not just at the top of the page.
- Add a pointer cursor to clickable elements on web.
- Avoid horizontal swipe gestures on main content; prefer vertical scroll.
- Use `touch-action: manipulation` on web to reduce the ~300ms tap delay.
- Use platform-standard gestures consistently; don't redefine swipe-back, pinch-zoom, etc.
- Don't block OS-level system gestures (Control Center, edge-swipe-back, etc.).
- Provide visual feedback on press (ripple or highlight).
- Use haptic feedback for confirmations and important actions — but don't overuse it.
- Never rely on gesture-only interactions for critical actions; always provide a visible control as well.
- Keep primary touch targets away from the notch, dynamic island, gesture bar, and screen edges.
- Avoid requiring pixel-perfect taps on small icons or thin edges.
- Swipe actions must show a clear affordance or hint (a chevron, a label, a one-time tutorial).
- Use a movement threshold before starting a drag, to avoid accidental drags from an imprecise tap.

## Interaction (app) — Do / Don't

| Rule | Do | Don't |
|---|---|---|
| Tap feedback | Clear pressed feedback (ripple/opacity/elevation) within 80-150ms | No visual response on tap |
| Animation timing | Micro-interactions around 150-300ms with platform-native easing | Instant transitions or slow (>500ms) animations |
| Accessibility focus | Screen-reader focus order matches visual order; descriptive labels | Unlabeled controls, confusing focus traversal |
| Disabled state clarity | Semantic disabled state, reduced emphasis, no tap action | Controls that look tappable but do nothing |
| Touch target minimum | ≥44×44pt (iOS) / ≥48×48dp (Android); expand hit area for small icons | Tiny tap targets or icon-only hit areas without padding |
| Gesture conflict prevention | One primary gesture per region; avoid nested tap/drag conflicts | Overlapping gestures causing accidental actions |
| Semantic native controls | Native interactive primitives with proper accessibility roles | Generic containers used as primary controls with no semantics |

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Touch + Interaction categories (14 rows) and `app-interface.csv` Touch category (3 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 22 | Touch | Touch Target Size | Mobile | Small buttons are hard to tap accurately | `Minimum 44x44px touch targets` | `Tiny clickable areas` | `min-h-[44px] min-w-[44px]` | `w-6 h-6 buttons` | High |
| 23 | Touch | Touch Spacing | Mobile | Adjacent touch targets need adequate spacing | `Minimum 8px gap between touch targets` | `Tightly packed clickable elements` | `gap-2 between buttons` | `gap-0 or gap-1` | Medium |
| 24 | Touch | Gesture Conflicts | Mobile | Custom gestures can conflict with system | `Avoid horizontal swipe on main content` | `Override system gestures` | `Vertical scroll primary` | `Horizontal swipe carousel only` | Medium |
| 25 | Touch | Tap Delay | Mobile | 300ms tap delay feels laggy | `Use touch-action CSS or fastclick` | `Default mobile tap handling` | `touch-action: manipulation` | `No touch optimization` | Medium |
| 26 | Touch | Pull to Refresh | Mobile | Accidental refresh is frustrating | `Disable where not needed` | `Enable by default everywhere` | `overscroll-behavior: contain` | `Default overscroll` | Low |
| 27 | Touch | Haptic Feedback | Mobile | Tactile feedback improves interaction feel | `Use for confirmations and important actions` | `Overuse vibration feedback` | `navigator.vibrate(10)` | `Vibrate on every tap` | Low |
| 28 | Interaction | Focus States | All | Keyboard users need visible focus indicators | `Use visible focus rings on interactive elements` | `Remove focus outline without replacement` | `focus:ring-2 focus:ring-blue-500` | `outline-none without alternative` | High |
| 29 | Interaction | Hover States | Web | Visual feedback on interactive elements | `Change cursor and add subtle visual change` | `No hover feedback on clickable elements` | `hover:bg-gray-100 cursor-pointer` | `No hover style` | Medium |
| 30 | Interaction | Active States | All | Show immediate feedback on press/click | `Add pressed/active state visual change` | `No feedback during interaction` | `active:scale-95` | `No active state` | Medium |
| 31 | Interaction | Disabled States | All | Clearly indicate non-interactive elements | `Reduce opacity and change cursor` | `Confuse disabled with normal state` | `opacity-50 cursor-not-allowed` | `Same style as enabled` | Medium |
| 32 | Interaction | Loading Buttons | All | Prevent double submission during async actions | `Disable button and show loading state` | `Allow multiple clicks during processing` | `disabled={loading} spinner` | `Button clickable while loading` | High |
| 33 | Interaction | Error Feedback | All | Users need to know when something fails | `Show clear error messages near problem` | `Silent failures with no feedback` | `Red border + error message` | `No indication of error` | High |
| 34 | Interaction | Success Feedback | All | Confirm successful actions to users | `Show success message or visual change` | `No confirmation of completed action` | `Toast notification or checkmark` | `Action completes silently` | Medium |
| 35 | Interaction | Confirmation Dialogs | All | Prevent accidental destructive actions | `Confirm before delete/irreversible actions` | `Delete without confirmation` | `Are you sure modal` | `Direct delete on click` | High |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | Touch | Touch Target Size | touch 44x44 hitSlop | iOS/Android/React Native | Primary touch targets must be at least 44x44pt | `Increase hitSlop or padding to meet minimum` | `Small icons with tiny touch area` | `<Pressable hitSlop={10}><Icon /></Pressable>` | `<Pressable><Icon style={{ width: 16, height: 16 }} /></Pressable>` | Critical |
| 7 | Touch | Touch Spacing | touch spacing gap 8px | iOS/Android/React Native | Adjacent touch targets need enough spacing | `Keep at least 8dp spacing between touchables` | `Cluster many buttons with no gap` | `<View style={{ gap: 8 }}><Button ... /><Button ... /></View>` | `<View><Button ... /><Button ... /></View>` | Medium |
| 8 | Touch | Gesture Conflicts | scroll swipe back gesture | iOS/Android/React Native | Custom gestures must not break system scroll/back | `Reserve horizontal swipes for carousels` | `Full-screen custom swipe conflicting with back` | `HorizontalPager inside vertical ScrollView` | `PanResponder on full screen blocking back` | High |
