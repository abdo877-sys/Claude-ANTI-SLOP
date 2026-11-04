# Functionality checklist — click everything

Test in a running browser where possible. Mark each: ✅ works · ⚠️ known gap (explain) · ⛔ broken.

## Navigation and links
- [ ] Every nav item goes to the right place; current page marked (`aria-current`)
- [ ] Logo links home
- [ ] No `href="#"`, empty href or `javascript:` links remain
- [ ] External links open correctly; `rel="noopener"` where `target="_blank"`
- [ ] Anchors scroll to the right section and focus moves there
- [ ] 404 route exists and offers a way forward

## Buttons and controls
- [ ] Every button does what its label says (no no-op handlers, no console-only handlers)
- [ ] Disabled controls explain why
- [ ] Loading states prevent double submit

## Forms
- [ ] Submit empty → clear errors, focus on first invalid field
- [ ] Submit invalid → specific messages, input preserved
- [ ] Fix a field, then click submit directly — the click lands (no layout shift from errors disappearing on blur)
- [ ] Submit valid → success state with next step; data actually sent (or mocked with user consent, documented)
- [ ] Autocomplete attributes correct; mobile keyboards correct (`inputmode`)

## Search, filters, sort
- [ ] Results change correctly; "no results" state exists
- [ ] State reflected in URL when shareable; back button restores it
- [ ] Clearing filters works

## Disclosure widgets
- [ ] Dropdowns, menus, accordions, tabs open/close by mouse, touch and keyboard (Enter/Space/Esc/arrows)
- [ ] Modals: focus in, focus trapped, Esc closes, focus returns, background inert
- [ ] Mobile menu: opens, closes, closes on route change, works when resized

## Data states
- [ ] Loading, empty, error (with retry) and success exist for every async block
- [ ] No invented data presented as real; sample data labelled

## Responsive
- [ ] 320 / 390 / 768 / 1024 / 1440: nothing overflows, nothing overlaps, primary action reachable
