#!/usr/bin/env python3
"""
run_benchmark.py — compare default Claude Code with Claude Code + ANTI-SLOP.

For each scenario in skills/anti-slop/evaluation/scenarios/:
  1. creates two run directories: baseline/ and anti-slop/ (seed copied in if any)
  2. installs the skill ONLY in anti-slop/.claude/skills/anti-slop (project level)
  3. runs the same prompt headlessly in both (default: `claude -p`)
  4. runs slop_scan.py on both outputs (and page_check.py if --page-check and an index.html exists)
  5. writes results.csv and a blind-scoring kit (outputs renamed A/B, key in key.json)

Human rubric scores (evaluation/rubric.md) must be filled in blind afterwards:
    bench/runs/<run-id>/blind/<scenario>/{A,B}  +  scores.csv

This script never fabricates results: if a command fails, the row says so.

Usage:
    python3 bench/run_benchmark.py                       # all scenarios
    python3 bench/run_benchmark.py --only 09-fix-ai-generated --page-check
    python3 bench/run_benchmark.py --claude-cmd "claude -p --permission-mode acceptEdits"
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "anti-slop"
SCEN = SKILL / "evaluation" / "scenarios"
SCAN = SKILL / "scripts" / "slop_scan.py"
PAGE = SKILL / "scripts" / "page_check.py"


def parse(md: Path) -> dict:
    text = md.read_text(encoding="utf-8")
    prompt = re.search(r"## Prompt\s+```\s*\n(.*?)\n```", text, re.S).group(1).strip()
    seed = re.search(r"\*\*Seed project:\*\*\s*`([^`]+)`", text).group(1)
    return {"id": md.stem, "prompt": prompt, "seed": None if seed == "none" else REPO / "bench" / seed}


def scan(path: Path) -> dict:
    out = subprocess.run([sys.executable, str(SCAN), str(path), "--json"], capture_output=True, text=True)
    return json.loads(out.stdout) if out.returncode == 0 else {"score": None, "categories": {}}


def page(path: Path) -> int | None:
    html = next((p for p in [path / "index.html", path / "dist" / "index.html", path / "public" / "index.html"] if p.exists()), None)
    if not html:
        return None
    out = subprocess.run([sys.executable, str(PAGE), str(html), "--json", "--out", str(path / ".anti-slop-bench")],
                         capture_output=True, text=True)
    try:
        return len(json.loads(out.stdout)["summary"]["issues"])
    except Exception:  # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", help="scenario id (repeatable)")
    ap.add_argument("--claude-cmd", default="claude -p", help="headless command; the prompt is appended")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--page-check", action="store_true")
    ap.add_argument("--allow-global-skill", action="store_true",
                    help="run even if ~/.claude/skills/anti-slop exists (it would contaminate the baseline)")
    a = ap.parse_args()

    if (Path.home() / ".claude" / "skills" / "anti-slop").exists() and not a.allow_global_skill:
        sys.exit("A global ~/.claude/skills/anti-slop exists and would leak into the baseline. Move it away first.")
    if not shutil.which(shlex.split(a.claude_cmd)[0]):
        sys.exit(f"command not found: {a.claude_cmd}")

    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    root = REPO / "bench" / "runs" / run_id
    rows, key = [], {}
    for md in sorted(SCEN.glob("*.md")):
        sc = parse(md)
        if a.only and sc["id"] not in a.only:
            continue
        for arm in ("baseline", "anti-slop"):
            d = root / sc["id"] / arm
            d.mkdir(parents=True)
            if sc["seed"]:
                shutil.copytree(sc["seed"], d, dirs_exist_ok=True)
            if arm == "anti-slop":
                shutil.copytree(SKILL, d / ".claude" / "skills" / "anti-slop")
            print(f"[{sc['id']}] {arm} …", flush=True)
            try:
                res = subprocess.run(shlex.split(a.claude_cmd) + [sc["prompt"]], cwd=d, capture_output=True,
                                     text=True, timeout=a.timeout)
                (d / ".bench-transcript.txt").write_text(res.stdout + "\n--- stderr ---\n" + res.stderr, encoding="utf-8")
                status = "ok" if res.returncode == 0 else f"exit {res.returncode}"
            except subprocess.TimeoutExpired:
                status = "timeout"
            if arm == "anti-slop":
                shutil.rmtree(d / ".claude" / "skills" / "anti-slop", ignore_errors=True)  # don't let the skill files be scanned
            s = scan(d)
            rows.append({"scenario": sc["id"], "arm": arm, "status": status, "scan": s["score"],
                         **{f"scan_{k}": v for k, v in s.get("categories", {}).items()},
                         "page_issues": page(d) if a.page_check else ""})
        # blind kit
        blind = root / "blind" / sc["id"]
        arms = ["baseline", "anti-slop"]
        random.shuffle(arms)
        for label, arm in zip("AB", arms):
            shutil.copytree(root / sc["id"] / arm, blind / label, ignore=shutil.ignore_patterns(".bench-transcript.txt", ".claude"))
        key[sc["id"]] = dict(zip("AB", arms))

    root.mkdir(parents=True, exist_ok=True)
    with open(root / "results.csv", "w", newline="", encoding="utf-8") as f:
        fields = sorted({k for r in rows for k in r}, key=lambda k: (k != "scenario", k != "arm", k))
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (root / "key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    (root / "blind" / "scores.csv").write_text(
        "scenario,output,originality,coherence,typography,layout,spacing,color,responsive,accessibility,interaction,performance,code,notes\n",
        encoding="utf-8")
    print(f"\nresults: {root/'results.csv'}\nblind kit: {root/'blind'} (score with evaluation/rubric.md, open key.json only after)")


if __name__ == "__main__":
    main()
