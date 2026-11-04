# Workflow — redesign an existing website

A redesign changes direction and structure but keeps the product, its
content, its routes and its working behavior.

## 1. Inventory before opinion
- List routes, components, forms, integrations (analytics, CMS, auth, payments).
- Baseline: `slop_scan.py . --json > .anti-slop/before.json` and
  `page_check.py` on the key routes; keep the screenshots as "before".
- Note what works today and must not break (forms, SEO URLs, tracking events).

## 2. Diagnose
Write in the brief: what the current site says about the product vs. what it
should say. Name the 3 biggest problems (e.g. "nothing on screen is specific to
the product", "four competing CTAs", "mobile nav hides booking").

## 3. Direction
Full `references/creative-direction.md` process. Keep brand equity that has
value (logo, a known color) and make it specific rather than discarding it.

## 4. Tokens first, then structure
1. Introduce the token layer alongside existing styles.
2. Migrate shared components (buttons, nav, footer, forms) to tokens.
3. Recompose pages one at a time, starting with the highest-traffic route.
   Keep URLs and anchor IDs stable; keep analytics hooks and form field names.
4. Remove the old styles only when no route uses them.

## 5. Protect what worked
- Same routes, redirects for anything renamed.
- Same `name` attributes on form fields and the same submit endpoints.
- Same meta titles unless intentionally improved.

## Quality checks
- [ ] Before/after: scan score up, page_check issues down, screenshots side by side
- [ ] No route, form or integration broken (functionality checklist)
- [ ] No regressions in contrast/keyboard vs. before
- [ ] DESIGN.md written; old one-off styles removed
- [ ] Report: what changed, what was intentionally kept, what remains
