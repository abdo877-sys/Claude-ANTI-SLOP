# Scenario 07-dashboard

- **Workflow under test:** `workflows/dashboard.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build a dashboard for a solar mini-grid operator monitoring 12 village sites: energy produced today, battery levels, sites with faults. Use a mock data module.
```

## Expected results
- Blocks map to written user questions
- Faults surfaced first; comparison context on metrics
- Per-block loading/error/empty states
- Sample data labelled

## Failure cases (any one = scenario fails)
- Equal KPI cards with no comparison
- Charts without units/time range
- Color-only fault status

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
