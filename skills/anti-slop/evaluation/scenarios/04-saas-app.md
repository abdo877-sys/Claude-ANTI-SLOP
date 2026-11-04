# Scenario 04-saas-app

- **Workflow under test:** `workflows/saas-app.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build the main app screens for a ticket triage tool used by a 5-person IT support team: ticket list with filters, ticket detail, and create ticket. Use local mock data in a separate module.
```

## Expected results
- Mock data isolated and labelled as sample
- List/detail/create with loading, empty, error states
- Filters reflected in URL
- Keyboard shortcuts for frequent actions
- Table usable on mobile

## Failure cases (any one = scenario fails)
- KPI card grid with invented metrics as home
- Filters that do nothing
- Clickable div rows without keyboard support

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
