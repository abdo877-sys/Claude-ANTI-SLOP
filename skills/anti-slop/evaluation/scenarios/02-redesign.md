# Scenario 02-redesign

- **Workflow under test:** `workflows/redesign.md`
- **Seed project:** `seeds/generic-landing` (copied into the run directory before the prompt)

## Prompt
```
This is our current website (in the folder). Redesign it so it looks like our product and not like a template. Keep all pages and the contact form working.
```

## Expected results
- Same routes and form field names
- Scan score improved by ≥25 points
- Direction justified from repo evidence
- Before/after screenshots produced

## Failure cases (any one = scenario fails)
- Form endpoint or field names changed
- Visual change only (recolor) with same template structure
- New generic aesthetic (e.g. dark neon) without justification

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
