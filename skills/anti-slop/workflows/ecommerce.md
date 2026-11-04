# Workflow — e-commerce interface

Goal: confidence and speed from discovery to paid. Identity comes from the
product and its photography; the UI must get out of the way at checkout.

## 1. Evidence
Catalog size, price range, product type (fashion, food, electronics, crafts),
how buyers choose (look, specs, reviews, price), markets, currencies, payment methods,
shipping regions, return policy. Real product photos (ask).

## 2. Direction
Let the product decide: fashion/luxury → Art-direction-driven or Luxury;
crafts/food → Organic or Editorial; tech → Technical/Swiss; kids → Playful.
Keep checkout neutral and calm regardless of direction.

## 3. Key screens
- **Listing:** filters that match how buyers choose; result count; sort;
  filter state in the URL; real empty state; pagination or "load more" with stable focus.
- **Product page:** large gallery (zoom, swipe, keyboard), price incl. taxes/
  shipping clarity, variant selection with stock per variant, delivery estimate,
  returns, real reviews only, sticky add-to-cart on mobile.
- **Cart:** editable quantities, remove with undo, totals with breakdown,
  no surprise fees later.
- **Checkout:** guest checkout, minimal fields, correct `autocomplete`, address
  lookup if available, clear errors, payment via the provider's hosted/elements
  UI, order confirmation with what happens next.

## 4. Trust without fakery
No fake countdown timers, no fake "12 people are viewing", no invented reviews or
stock scarcity. Show real policies, real contact, secure payment marks only for providers actually used.

## 5. Performance
Product images are the LCP — optimise aggressively, responsive sizes, priority on the first image.
Defer reviews/recommendations widgets.

## Quality checks
- [ ] Complete purchase path tested in the provider's test mode (or clearly mocked with user consent)
- [ ] Filters, sort, variants, cart edits all functional and reflected in URL/state
- [ ] Prices/currency formatted per locale (`Intl.NumberFormat`)
- [ ] Checkout keyboard-completable; errors announced
- [ ] No dark patterns (see §4)
