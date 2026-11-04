#!/usr/bin/env python3
"""
validate_skill.py — check the skill is installable and internally consistent.

Checks:
  * SKILL.md starts with frontmatter on line 1, has name + description
  * name: lowercase letters, digits, hyphens; matches the directory name
  * description <= 1024 chars (portable limit; Claude Code truncates at 1536)
  * only frontmatter keys accepted on every surface (portable set)
  * SKILL.md under 500 lines (progressive-disclosure guidance)
  * every relative file path mentioned in any .md (references/…, workflows/…,
    checklists/…, templates/…, evaluation/…, scripts/…) exists
  * no empty files; every script compiles
"""
import py_compile
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "anti-slop"
PORTABLE = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
PATH_RX = re.compile(r"`?((?:references|workflows|checklists|templates|evaluation|scripts)/[\w./-]+\.(?:md|py|yml|json))`?")
errors = []


def err(msg):
    errors.append(msg)


skill_md = SKILL / "SKILL.md"
text = skill_md.read_text(encoding="utf-8")
lines = text.splitlines()
if lines[0] != "---":
    err("SKILL.md: frontmatter must start on line 1")
end = lines.index("---", 1)
front = {}
for ln in lines[1:end]:
    m = re.match(r"^([a-zA-Z][\w-]*):\s*(.*)$", ln)
    if m:
        front[m.group(1)] = m.group(2)
for key in ("name", "description"):
    if not front.get(key):
        err(f"SKILL.md: missing {key}")
name = front.get("name", "")
if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
    err(f"SKILL.md: invalid name {name!r}")
if name != SKILL.name:
    err(f"SKILL.md: name {name!r} != directory {SKILL.name!r}")
if len(front.get("description", "")) > 1024:
    err(f"SKILL.md: description is {len(front['description'])} chars (> 1024)")
extra = set(front) - PORTABLE
if extra:
    err(f"SKILL.md: non-portable frontmatter keys {sorted(extra)}")
if len(lines) >= 500:
    err(f"SKILL.md: {len(lines)} lines (keep under 500)")

for md in SKILL.rglob("*.md"):
    for ref in PATH_RX.findall(md.read_text(encoding="utf-8")):
        ref = ref.rstrip(".")
        if "<" in ref or "*" in ref:
            continue
        candidates = [SKILL / ref, md.parent / ref, md.parent / Path(ref).name]
        if not any(c.exists() for c in candidates):
            err(f"{md.relative_to(SKILL)}: broken reference {ref}")

for f in SKILL.rglob("*"):
    if f.is_file() and f.stat().st_size == 0:
        err(f"empty file: {f.relative_to(SKILL)}")
for py in (SKILL / "scripts").glob("*.py"):
    try:
        py_compile.compile(str(py), doraise=True)
    except py_compile.PyCompileError as e:
        err(f"{py.name}: {e}")

files = [f for f in SKILL.rglob("*") if f.is_file()]
if errors:
    print("\n".join(f"✗ {e}" for e in errors))
    sys.exit(1)
print(f"✓ skill valid — {len(files)} files, SKILL.md {len(lines)} lines, description {len(front['description'])} chars")
