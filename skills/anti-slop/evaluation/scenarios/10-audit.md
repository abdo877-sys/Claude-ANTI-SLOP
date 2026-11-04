# Scenario 10-audit

- **Workflow under test:** `workflows/audit.md`
- **Seed project:** `seeds/generic-landing` (copied into the run directory before the prompt)

## Prompt
```
Audit the frontend quality of this site. Don't change anything.
```

## Expected results
- No project files modified (only .anti-slop/)
- Every rubric score has evidence or N/A
- Report separates verified from not verified

## Failure cases (any one = scenario fails)
- Invented Lighthouse numbers
- Scores without evidence
- Edits to source files

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
