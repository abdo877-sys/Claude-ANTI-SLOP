# Contributing to ANTI-SLOP

Thanks for helping make AI-built interfaces better. Principles for contributions
mirror the skill's: evidence over opinion, nothing fake, small reviewable changes.

## Quick start
```bash
python3 tools/validate_skill.py      # structure, frontmatter, links
python3 tests/test_rules.py          # scanner regression tests (or: python3 -m pytest tests/)
```
Both run in CI on every PR.

## Add a tell (scanner rule)
1. Add a `Rule(...)` to `RULES` in `skills/anti-slop/scripts/slop_scan.py` — pick a category
   (identity, function, accessibility, performance) and severity (critical = recognisable from across the room,
   major = clearly templated or broken, minor = generic only in bulk). Use `threshold` for "only in bulk".
2. Add a **positive** case to `POSITIVE` in `tests/test_rules.py` (the test fails without it).
3. If false positives are plausible, add a **negative** case to `NEGATIVE`.
4. Explain the rule in `skills/anti-slop/references/ai-tells.md`.

## Report a false positive
Open a "False positive" issue with the smallest snippet that triggers it and why it's legitimate.
Best: a PR adding it to `NEGATIVE` together with the regex fix.

## Improve the method
Workflows, references and checklists are instructions an agent follows. Changes should be:
- **Concrete** — a step the agent can execute or a check it can verify.
- **Short** — the skill body stays in context; every line costs tokens.
- **Linked** — new files must be referenced from `SKILL.md` or a workflow (the validator checks paths exist).

## Benchmark results
Run `bench/run_benchmark.py` (see `bench/README.md`), score blind, and open a PR with
`results.csv`, `blind/scores.csv`, `key.json`, and the model/version used. Losses and ties are as welcome as wins.

## Examples
Real before/after runs are welcome **with permission** for any third-party site. Include the brief,
DESIGN.md, scan reports, screenshots and an honest REPORT.md (verified / not verified).

## Don'ts
- No copied designs, assets or code from other sites or skills.
- No claims of results that weren't measured.
- No new runtime dependencies for the scanner (standard library only).

By contributing you agree your work is released under the MIT license and to follow the
[Code of Conduct](CODE_OF_CONDUCT.md).
