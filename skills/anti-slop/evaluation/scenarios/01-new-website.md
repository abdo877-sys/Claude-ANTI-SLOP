# Scenario 01-new-website

- **Workflow under test:** `workflows/new-website.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build a marketing website for Harbor Ledger, a bookkeeping app for small shops in Djibouti. Shop owners use it to track credit they give to regular customers and to send payment reminders by WhatsApp. It is available in French and Arabic. Pages: home, pricing (free and 600 DJF/month), contact.
```

## Expected results
- Brief exists with evidence-based direction (not 'clean modern SaaS')
- Core object (customer credit / receipt) visible in the hero
- FR and AR supported; RTL layout correct in Arabic
- Pricing reflects exactly two plans; no invented third plan
- Contact form submits with validation and success state
- No invented testimonials, user counts or partner logos

## Failure cases (any one = scenario fails)
- Indigo/violet accent or gradient hero
- Three feature cards with icons
- 'Trusted by 10,000+ businesses' or similar invented proof
- Arabic page left-to-right or with Latin-only font
- Dead nav links

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
