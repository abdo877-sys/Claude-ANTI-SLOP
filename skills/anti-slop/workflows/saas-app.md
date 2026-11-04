# Workflow — SaaS application UI

The app is used daily. Identity lives in precision, density and details — not
in decoration. Marketing pages are a separate job (use new-website or redesign).

## 1. Evidence
- Core objects (projects, invoices, tickets…), the 3 most frequent tasks,
  user expertise, data density, team vs solo, locales.
- Existing design system or component library.

## 2. Direction
Usually High-end SaaS, Technical, Swiss or Minimalist — but derive it. The
signature move should live in the core object (how a ticket, an invoice, a
deploy is represented), not in chrome.

## 3. System
- Density modes if users differ (comfortable/compact).
- Type: reading face optimised for UI at 13–16px; tabular figures; a mono for IDs/code.
- Color: neutral chrome, one accent, semantic states, status colors that pass contrast and are also labelled.
- Components from an accessible primitive library (or the existing one), themed with tokens.

## 4. App shell
- Navigation reflects the object model (not "Dashboard, Analytics, Settings" by default).
- Command palette (⌘K) if the app has >10 destinations or power users.
- Breadcrumbs for deep hierarchies; page titles match nav labels.

## 5. Screens
For each core object: list → detail → create/edit, each with empty, loading,
error, permission-denied and success states. Tables per `components.md`.
Keyboard shortcuts for frequent actions, discoverable (tooltip/help).
Optimistic updates where safe; undo instead of confirm dialogs where possible.

## 6. Real functionality
Wire to the real API or a clearly local mock layer the user agreed to. Never
render invented metrics on a dashboard as if real. Placeholder data must be
visibly sample data ("Sample project") and removable.

## Quality checks
- [ ] Every primary task completable by keyboard only
- [ ] All CRUD states exist and were exercised in the browser
- [ ] No hard-coded colors/sizes in components (scan clean)
- [ ] Tables usable at 390px
- [ ] Performance: route-level splitting; heavy widgets lazy
