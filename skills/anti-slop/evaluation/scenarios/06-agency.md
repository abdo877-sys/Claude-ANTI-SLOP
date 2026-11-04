# Scenario 06-agency

- **Workflow under test:** `workflows/agency.md`
- **Seed project:** `none` (empty directory)

## Prompt
```
Build a website for Rift Studio, a 4-person brand and motion studio in Addis Ababa whose clients are cultural institutions and music festivals. Include work index, one case study page, studio page and inquiry form.
```

## Expected results
- Bold idea traceable to the studio's evidence
- Works without JS effects and with reduced motion
- Inquiry form with budget/timeline fields that submits

## Failure cases (any one = scenario fails)
- Custom cursor/WebGL that breaks mobile or keyboard
- Claims of awards
- Generic 'We craft digital experiences' copy

## Automated thresholds (with skill)
- `slop_scan`: overall ≥ 90 (new) or ≥ +25 vs seed; zero critical; function = 100
- `page_check`: no overflow at 390/820/1440; no console errors; no low-contrast text

## Human scoring
Blind-score both outputs with `../rubric.md`. The harness (`bench/run_benchmark.py`) prepares a blind kit and `scores.csv`.
