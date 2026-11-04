# Scenario 08-improve-ui

- **Workflow under test:** `workflows/improve-ui.md`
- **Seed project:** `seeds/generic-landing` (copied into the run directory before the prompt)

## Prompt
```
Improve the UI of this page — fix whatever is weakest, but don't redesign it.
```

## Expected results
- Broken/accessibility issues fixed first
- Tokens consolidate duplicate values
- Layout structure largely preserved
- Report lists every behavior change

## Failure cases (any one = scenario fails)
- Full redesign despite instructions
- New dependencies added for styling

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
