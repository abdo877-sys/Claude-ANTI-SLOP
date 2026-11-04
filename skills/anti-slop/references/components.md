# Component standards

Every component: semantic element, token-only styling, all states designed
(default, hover, focus-visible, active, disabled, loading, error), keyboard
operable, and it actually does something.

## Buttons
- `<button type="button|submit">` for actions; `<a href>` for navigation. Never swap them.
- Hierarchy: one primary per view; secondary as outline or tonal; tertiary as text.
- Loading: keep width stable, show progress, set `aria-busy="true"`, disable double submit.
- Disabled: explain why nearby (tooltip or helper text), don't just grey out.
- Min target 44×44px (padding counts).

## Navigation
- `<header>` + `<nav aria-label="Main">`; current page has `aria-current="page"`.
- Mobile: if more than ~5 items, use a disclosure button with `aria-expanded`
  and `aria-controls`; trap focus only for modal menus; Esc closes; focus returns to the toggle.
- Keep the one primary action visible on mobile — don't hide it in the menu.
- Skip link as the first focusable element: `<a href="#main" class="skip">Skip to content</a>`.

## Headers / heroes
- One `<h1>` per page. The hero states what this is for whom, with proof
  (real product, real number, real work). See `layout.md` § moves.

## Footers
- Only links that exist. Contact that works. Legal links if needed. No 5 columns of filler.

## Forms
- Visible `<label for>` on every field (placeholders are not labels).
- Correct `type`, `autocomplete`, `inputmode`; `required` + `aria-describedby` for hints and errors.
- Validate on blur and submit, not on every keystroke. Error text says how to fix it.
- Clear an error while the user types the fix — **never hide it on blur**: the
  collapsing message shifts the layout and the click meant for the submit button
  lands on empty space. (Found by actually clicking, in this skill's own test.)
- On error, move focus to the first invalid field or an error summary.
- Submitting: loading state; success: a real confirmation (what happens next).
- Never lose user input on error or navigation.

## Modals / dialogs
- Native `<dialog>` with `showModal()` where possible (focus trap + Esc built in),
  or a library primitive (Radix, React Aria, Headless UI).
- Labelled by its heading (`aria-labelledby`), focus moves in on open and back on close,
  background inert, scroll locked. Don't use modals for content that deserves a page.

## Menus, dropdowns, tabs, comboboxes
- Follow the WAI-ARIA Authoring Practices patterns, or use an accessible
  primitive library already in the project. Arrow keys within, Tab out, Esc closes.
- Tabs: `role="tablist"`, `tab`, `tabpanel`, roving tabindex; the URL reflects the tab if it's shareable.

## Cards — only when genuinely appropriate
A card is an object you can pick up: it has its own identity and one main
action (a product, a project, a person). If items are compared, use rows.
If content is grouped, use a section with a heading. Never nest cards.
Whole-card links: one real `<a>` stretched with a pseudo-element, not an onClick div.

## Tables
- Real `<table>` with `<caption>`, `<th scope>`. Right-align numbers with tabular figures.
- Sortable columns expose `aria-sort`. Sticky header for long tables.
- On mobile: prioritise columns, allow horizontal scroll inside a labelled
  region (`role="region" aria-label tabindex="0"`), or reflow to definition lists.

## Data visualization
- Choose the chart by the question: change over time → line; comparison → bar;
  part-to-whole with ≤5 parts → stacked bar (not pie); distribution → histogram/dot.
- Label directly instead of legends where possible; start bar axes at zero.
- Provide the data as a table or summary text for screen readers.
- Never show invented data as if it were real. Empty data gets an empty state.

## Empty states
Signature move as art (if any) + one sentence in the product's voice + the
single action that fills the state. "No invoices yet — your first one takes a minute. [New invoice]"

## Loading states
- <300ms: show nothing. 300ms–2s: skeleton shaped like the real content.
  >2s: progress with what's happening. Long jobs: let users leave and notify.
- Skeletons in `--surface`, no rainbow shimmer.

## Error states
What happened (plain words), what the user can do, and their input preserved.
Network errors offer retry. 404 pages offer search or the main routes. Never show stack traces.
