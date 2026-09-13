# Navigation Patterns (Priority 9 — HIGH)

## Core rules

- Bottom navigation: maximum 5 items, each with both a label and an icon.
- Use a drawer/sidebar for secondary navigation, not for primary actions.
- Back navigation must be predictable and consistent, and preserve scroll position/state.
- Every key screen should be reachable via a deep link/URL, for sharing and for notifications.
- On iOS, use a bottom tab bar for top-level navigation; on Android, a top app bar with a navigation icon.
- Navigation items need both an icon and a text label — icon-only navigation hurts discoverability.
- The current location must be visually highlighted (color, weight, an indicator) within the navigation.
- Keep primary navigation (tabs/bottom bar) clearly separated from secondary navigation (drawer/settings).
- Modals and sheets must offer a clear close/dismiss affordance; support swipe-down-to-dismiss on mobile.
- Search should be easily reachable (a top bar or a tab) and offer recent/suggested queries.
- On web, use breadcrumbs for hierarchies three or more levels deep.
- Navigating back must restore the previous scroll position, filter state, and any in-progress input.
- Support system gesture navigation (iOS swipe-back, Android predictive back) without conflicting with it.
- Use badges on nav items sparingly, to indicate unread/pending state, and clear them once visited.
- When actions exceed available space, use an overflow/"more" menu rather than cramming everything in.
- Bottom navigation is for top-level screens only — never nest sub-navigation inside it.
- On large screens (≥1024px) prefer a sidebar; on small screens use bottom/top nav.
- Never silently reset the navigation stack or unexpectedly jump the user back to home.
- Keep navigation placement consistent across every page — don't vary it by page type.
- Don't mix tab navigation, a sidebar, and bottom navigation at the same hierarchy level.
- Never use a modal for a primary navigation flow — it breaks the user's sense of place.
- After a page transition, move keyboard/screen-reader focus to the main content region.
- Keep core navigation reachable from deep pages — don't hide it entirely inside a sub-flow.
- Keep dangerous actions (delete account, log out) visually and spatially separated from normal nav items.
- If a nav destination is temporarily unavailable, explain why rather than silently hiding it.

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Navigation + Search categories (8 rows) and `app-interface.csv` Navigation category (3 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Navigation | Smooth Scroll | Web | Anchor links should scroll smoothly to target section | `Use scroll-behavior: smooth on html element` | `Jump directly without transition` | `html { scroll-behavior: smooth; }` | `<a href='#section'> without CSS` | High |
| 2 | Navigation | Sticky Navigation | Web | Fixed nav should not obscure content | `Add padding-top to body equal to nav height` | `Let nav overlap first section content` | `pt-20 (if nav is h-20)` | `No padding compensation` | Medium |
| 3 | Navigation | Active State | All | Current page/section should be visually indicated | `Highlight active nav item with color/underline` | `No visual feedback on current location` | `text-primary border-b-2` | `All links same style` | Medium |
| 4 | Navigation | Back Button | Mobile | Users expect back to work predictably | `Preserve navigation history properly` | `Break browser/app back button behavior` | `history.pushState()` | `location.replace()` | High |
| 5 | Navigation | Deep Linking | All | URLs should reflect current state for sharing | `Update URL on state/view changes` | `Static URLs for dynamic content` | `Use query params or hash` | `Single URL for all states` | Medium |
| 6 | Navigation | Breadcrumbs | Web | Show user location in site hierarchy | `Use for sites with 3+ levels of depth` | `Use for flat single-level sites` | `Home > Category > Product` | `Only on deep nested pages` | Low |
| 89 | Search | Autocomplete | Web | Help users find results faster | `Show predictions as user types` | `Require full type and enter` | `Debounced fetch + dropdown` | `No suggestions` | Medium |
| 90 | Search | No Results | Web | Dead ends frustrate users | `Show 'No results' with suggestions` | `Blank screen or '0 results'` | `Try searching for X instead` | `No results found.` | Medium |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 9 | Navigation | Back Behavior | back handler navigation stack | iOS/Android/React Native | Back navigation should be predictable and preserve state | `Use navigation.goBack and keep screen state` | `Reset stack or exit app unexpectedly` | `onPress={() => navigation.goBack()}` | `BackHandler.exitApp() on first press` | Critical |
| 10 | Navigation | Bottom Tabs | tab bar max items | iOS/Android/React Native | Bottom tab bar should have at most 5 primary items | `Use 3–5 tabs and move extras to More/Settings` | `Overloaded tab bar with many icons` | `Home/Explore/Profile/Settings` | `Home/Explore/Shop/Cart/Profile/Settings/More` | Medium |
| 11 | Navigation | Modal Escape | modal dismiss close affordance | iOS/Android/React Native | Modals/sheets must have clear close actions | `Provide close button and swipe-down where platform expects` | `Trapping users in modal with no obvious exit` | `<Modal><Button title="Close" onPress={onClose} /></Modal>` | `<Modal><View>{children}</View></Modal>` | High |
