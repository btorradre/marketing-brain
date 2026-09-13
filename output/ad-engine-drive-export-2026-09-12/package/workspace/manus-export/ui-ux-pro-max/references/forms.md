# Forms & Feedback (Priority 8 — MEDIUM)

## Core rules

- A visible label per input — never rely on a placeholder as the only label.
- Show validation errors directly below the related field.
- Show a loading state, then a success/error state, on submit.
- Mark required fields clearly (e.g. an asterisk).
- Show a helpful message and an available action for any empty state.
- Auto-dismiss toast notifications after 3-5 seconds.
- Confirm before any destructive action.
- Provide persistent helper text below complex inputs, not just a placeholder.
- Disabled elements should use reduced opacity (~0.38-0.5) plus a cursor change plus the semantic disabled attribute — all three, not just a visual cue.
- Reveal complex options progressively; don't overwhelm the user with every option up front.
- Validate on blur, not on every keystroke — show an error only after the user has finished with that field.
- Use semantic input types (email, tel, number) so mobile devices show the correct keyboard.
- Provide a show/hide toggle on password fields.
- Use autocomplete/content-type attributes so the OS/browser can autofill correctly.
- Allow undo for destructive or bulk actions (e.g. an "Undo delete" toast).
- Confirm completed actions with brief visual feedback (a checkmark, a toast, a color flash).
- Error messages must include a clear recovery path (retry, edit, a help link) — not just a statement that something went wrong.
- Multi-step flows should show a step indicator or progress bar, and allow navigating back.
- Long forms should auto-save drafts to prevent data loss on an accidental dismissal.
- Confirm before dismissing a sheet/modal that has unsaved changes.
- Error messages must state both the cause and how to fix it — never just "Invalid input."
- Group related fields logically (a fieldset/legend, or clear visual grouping).
- A read-only state should look and behave distinctly from a disabled state.
- After a failed submit, auto-focus the first invalid field.
- For multiple simultaneous errors, show a summary at the top with anchor links to each field.
- Mobile input height should be at least 44px to meet touch-target requirements.
- Destructive actions should use a semantic danger color (red) and be visually separated from primary actions.
- Toasts must never steal keyboard focus; use a polite live-region announcement for screen readers.
- Form errors should use a live region or alert role so screen readers announce them.
- Error and success state colors must meet 4.5:1 contrast.
- A request timeout must show clear feedback with a retry option.

## Full rule database (verbatim from source)

Source: `ux-guidelines.csv` Forms + Feedback + Data Entry categories (17 rows) and `app-interface.csv` Forms + Feedback categories (7 rows).

| No | Category | Issue | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|
| 54 | Forms | Input Labels | All | Every input needs a visible label | `Always show label above or beside input` | `Placeholder as only label` | `<label>Email</label><input>` | `placeholder='Email' only` | High |
| 55 | Forms | Error Placement | All | Errors should appear near the problem | `Show error below related input` | `Single error message at top of form` | `Error under each field` | `All errors at form top` | Medium |
| 56 | Forms | Inline Validation | All | Validate as user types or on blur | `Validate on blur for most fields` | `Validate only on submit` | `onBlur validation` | `Submit-only validation` | Medium |
| 57 | Forms | Input Types | All | Use appropriate input types | `Use email tel number url etc` | `Text input for everything` | `type='email'` | `type='text' for email` | Medium |
| 58 | Forms | Autofill Support | Web | Help browsers autofill correctly | `Use autocomplete attribute properly` | `Block or ignore autofill` | `autocomplete='email'` | `autocomplete='off' everywhere` | Medium |
| 59 | Forms | Required Indicators | All | Mark required fields clearly | `Use asterisk or (required) text` | `No indication of required fields` | `* required indicator` | `Guess which are required` | Medium |
| 60 | Forms | Password Visibility | All | Let users see password while typing | `Toggle to show/hide password` | `No visibility toggle` | `Show/hide password button` | `Password always hidden` | Medium |
| 61 | Forms | Submit Feedback | All | Confirm form submission status | `Show loading then success/error state` | `No feedback after submit` | `Loading -> Success message` | `Button click with no response` | High |
| 62 | Forms | Input Affordance | All | Inputs should look interactive | `Use distinct input styling` | `Inputs that look like plain text` | `Border/background on inputs` | `Borderless inputs` | Medium |
| 63 | Forms | Mobile Keyboards | Mobile | Show appropriate keyboard for input type | `Use inputmode attribute` | `Default keyboard for all inputs` | `inputmode='numeric'` | `Text keyboard for numbers` | Medium |
| 78 | Feedback | Loading Indicators | All | Show system status during waits | `Show spinner/skeleton for operations > 300ms` | `No feedback during loading` | `Skeleton or spinner` | `Frozen UI` | High |
| 79 | Feedback | Empty States | All | Guide users when no content exists | `Show helpful message and action` | `Blank empty screens` | `No items yet. Create one!` | `Empty white space` | Medium |
| 80 | Feedback | Error Recovery | All | Help users recover from errors | `Provide clear next steps` | `Error without recovery path` | `Try again button + help link` | `Error message only` | Medium |
| 81 | Feedback | Progress Indicators | All | Show progress for multi-step processes | `Step indicators or progress bar` | `No indication of progress` | `Step 2 of 4 indicator` | `No step information` | Medium |
| 82 | Feedback | Toast Notifications | All | Transient messages for non-critical info | `Auto-dismiss after 3-5 seconds` | `Toasts that never disappear` | `Auto-dismiss toast` | `Persistent toast` | Medium |
| 83 | Feedback | Confirmation Messages | All | Confirm successful actions | `Brief success message` | `Silent success` | `Saved successfully toast` | `No confirmation` | Medium |
| 91 | Data Entry | Bulk Actions | Web | Editing one by one is tedious | `Allow multi-select and bulk edit` | `Single row actions only` | `Checkbox column + Action bar` | `Repeated actions per row` | Low |

### App-interface rows (iOS/Android/React Native specific)

| No | Category | Issue | Keywords | Platform | Description | Do | Don't | Code Example Good | Code Example Bad | Severity |
|---|---|---|---|---|---|---|---|---|---|---|
| 13 | Feedback | Loading Indicators | activity indicator skeleton | iOS/Android/React Native | Show visible feedback during network operations | `Use ActivityIndicator or skeleton for >300ms operations` | `Leave button and screen frozen` | `{loading ? <ActivityIndicator /> : <Button title="Save" />}` | `"<Button title=""Save"" onPress={submit} /> // no loading"` | High |
| 14 | Feedback | Success Feedback | toast checkmark banner | iOS/Android/React Native | Confirm successful actions with brief feedback | `Show toast/checkmark or banner` | `Complete actions silently with no confirmation` | `showToast('Saved successfully')` | `// silently update state only` | Medium |
| 15 | Feedback | Error Feedback | inline error banner | iOS/Android/React Native | Show clear error messages near the problem | `input-level error + summary banner` | `Only change border color with no explanation` | `<TextInput ... /><Text style={{color:'red'}}>{error}</Text>` | `<TextInput style={{borderColor:'red'}} />` | High |
| 16 | Forms | Inline Validation | onBlur validation | iOS/Android/React Native | Validate inputs on blur or submit with clear messaging | `Validate onBlur and onSubmit` | `Validate on every keystroke causing jank` | `onBlur={() => validateEmail(value)}` | `onChangeText={v => validateEmail(v)} // every char` | Medium |
| 17 | Forms | Keyboard Type | keyboardType returnKeyType | iOS/Android/React Native | Use appropriate keyboardType and returnKeyType | `Match email/tel/number/search types` | `Use default keyboard for all inputs` | `<TextInput keyboardType="email-address" />` | `<TextInput keyboardType="default" />` | Medium |
| 18 | Forms | Auto Focus & Next | autoFocus blurOnSubmit onSubmitEditing | iOS/Android/React Native | Guide users through form fields with Next/Done flows | `Use onSubmitEditing to focus next input` | `Force users to tap each field manually` | `onSubmitEditing={() => nextRef.current?.focus()}` | `// no onSubmitEditing, manual tap only` | Low |
| 19 | Forms | Password Visibility | secureTextEntry toggle | iOS/Android/React Native | Allow toggling password visibility securely | `Provide Show/Hide icon toggling secureTextEntry` | `Force users to type blind with no option` | `<TextInput secureTextEntry={secure} /><Icon onPress={toggle} />` | `<TextInput secureTextEntry /> // no toggle` | Medium |
