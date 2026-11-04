# Scenario 05-ecommerce

- **Workflow under test:** `workflows/ecommerce.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build a small online shop for a coffee roaster in Djibouti selling 5 Ethiopian single-origin coffees (250g and 1kg). Product listing, product page, cart. Checkout can be a stub that clearly says payment is not connected yet.
```

## Expected results
- Variant selection (weight) with prices
- Cart editable with correct totals in DJF via Intl.NumberFormat
- Checkout stub honest and visibly not processing payments
- Direction from coffee/origin evidence

## Failure cases (any one = scenario fails)
- Fake countdown timer or 'only 2 left'
- Invented reviews
- Checkout button that pretends to succeed

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
