# Benchmark: default Claude Code vs Claude Code + ANTI-SLOP

**Status: harness ready, no comparative results published yet.** Nothing in
this repository claims a measured win over default behavior. The only
before/after so far is `examples/harbor-ledger/`, a single worked run of the
workflow on a hand-written seed — useful as a demonstration, not as evidence.

## Method
1. Ten scenarios (`skills/anti-slop/evaluation/scenarios/`), one per workflow,
   each with a fixed prompt, optional seed project, expected results and failure cases.
2. Both arms run the **same prompt** headlessly with the same model. The skill is
   installed only in the treatment arm (project-level `.claude/skills/`).
3. Automated: `slop_scan.py` (and `page_check.py` with `--page-check`).
4. Human: outputs are copied to `blind/<scenario>/A|B` in random order and
   scored with `evaluation/rubric.md` by someone who hasn't seen `key.json`.
5. A scenario counts as a win only if the treatment scores higher on the rubric
   and triggers none of the scenario's failure cases.

```bash
npm i -g @anthropic-ai/claude-code      # if needed; you need your own access
pip install playwright && python3 -m playwright install chromium   # for --page-check
python3 bench/run_benchmark.py --page-check
```
Run each scenario at least 3 times per arm before drawing conclusions; model
output varies between runs.

## Publishing results
Commit `bench/runs/<run-id>/results.csv`, `blind/scores.csv`, `key.json` and the
model/version used. Report losses and ties as prominently as wins.

## Seeds
- `seeds/generic-landing/` — a hand-written page reproducing common generic
  patterns (indigo gradients, Inter, glass nav, blobs, emoji cards, invented
  proof, dead links, removed focus). Used by scenarios 02, 08, 09, 10 and by the regression tests.
