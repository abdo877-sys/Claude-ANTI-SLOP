# Workflow — frontend quality audit (no changes)

Deliver a report the user can act on. Do not modify project files (write
only inside `.anti-slop/`).

## 1. Scope
Routes/screens to audit, target devices, and whether the site can be run locally or via URL.

## 2. Collect evidence
```bash
mkdir -p .anti-slop
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py . --json > .anti-slop/scan.json
python3 ${CLAUDE_SKILL_DIR}/scripts/slop_scan.py . --md .anti-slop/scan.md
python3 ${CLAUDE_SKILL_DIR}/scripts/page_check.py <url> --json --out .anti-slop/screens > .anti-slop/page.json
```
Repeat page_check for each key route. Then walk `checklists/functionality.md`,
`accessibility.md` and `performance.md` manually where tools allow.

## 3. Score
Score every dimension of `evaluation/rubric.md` (0–4) with **one line of
evidence per score** (file:line, screenshot name, or measured value).
Unverifiable dimensions are marked "not assessed", not guessed.

## 4. Report
Use `templates/quality-report.md`:
- Summary: overall score, the 3 most important problems, the 3 quickest wins.
- Findings grouped by category, each with severity, evidence, impact, fix.
- What was verified and how; what wasn't and why.
- Recommended workflow for the fix (improve-ui, fix-ai-generated, redesign).

Write it to `.anti-slop/report.md` and summarise it in chat.

## Quality checks
- [ ] Every claim has evidence; no invented metrics
- [ ] Severity reflects user impact, not personal taste
- [ ] No project files changed
