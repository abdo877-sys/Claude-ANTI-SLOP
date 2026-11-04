#!/usr/bin/env python3
"""
slop_scan.py — static detector for generic AI-generated frontend.

Finds the code-level tells of "AI slop" UI (default palettes, gradients,
glassmorphism, blobs, emoji icons, template layouts, hype copy) plus the
engineering failures that usually travel with them (dead links, no-op
buttons, click-handlers on divs, missing alt text, removed focus rings,
render-blocking fonts, unsized images).

Platforms: web (HTML/CSS/Tailwind/React/Vue/Svelte/Astro), Flutter,
SwiftUI, Jetpack Compose, React Native.

Usage:
    python3 slop_scan.py <root>                       # human report
    python3 slop_scan.py <root> --json > before.json  # machine report
    python3 slop_scan.py <root> --compare before.json # before -> after
    python3 slop_scan.py <root> --md report.md        # markdown report
    python3 slop_scan.py <root> --fail-under 75       # CI gate
    python3 slop_scan.py --list-rules                 # rule catalogue

Static analysis cannot see a rendered page. A high score means "no known
tells in the code", not "well designed". Always pair it with the visual
review in checklists/quality-gate.md.

Standard library only. Python 3.8+.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

VERSION = "1.0.0"

SKIP_DIRS = {
    "node_modules", ".git", "build", "dist", ".next", ".nuxt", ".svelte-kit",
    ".dart_tool", "Pods", "DerivedData", ".gradle", "out", "coverage", ".venv",
    "venv", "__pycache__", ".turbo", ".expo", "vendor", ".anti-slop", ".vercel",
    "generated", ".idea", "storybook-static",
}
WEB = {".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".ts", ".js", ".mjs",
       ".html", ".htm", ".vue", ".svelte", ".astro", ".mdx"}
MARKUP = {".tsx", ".jsx", ".html", ".htm", ".vue", ".svelte", ".astro", ".mdx"}
STYLE = {".css", ".scss", ".sass", ".less"}
DART, SWIFT, KOTLIN = {".dart"}, {".swift"}, {".kt", ".kts"}
CODE = WEB | DART | SWIFT | KOTLIN

WEIGHT = {"critical": 12.0, "major": 6.0, "minor": 2.0}
CATEGORIES = ("identity", "function", "accessibility", "performance")

AI_HEX = ("6366f1|4f46e5|4338ca|818cf8|8b5cf6|7c3aed|6d28d9|a855f7|9333ea|c084fc|"
          "3b82f6|2563eb|1d4ed8|60a5fa|ec4899|db2777|6200ee|3700b3|bb86fc|673ab7|"
          "6650a4|d0bcff|625b71|7d5260|efb8c8|ccc2dc")


def rx(p, flags=re.IGNORECASE):
    return re.compile(p, flags)


@dataclass
class Rule:
    id: str
    category: str
    severity: str
    title: str
    pattern: re.Pattern
    exts: set
    fix: str
    threshold: int = 1
    skip_theme_files: bool = False


RULES = [
    # ======================= IDENTITY (aesthetic tells) =======================
    Rule("AI-HEX", "identity", "critical", "Default AI palette color literal (indigo/violet/purple/stock blue)",
         rx(r"(?:#|0x(?:ff)?)(" + AI_HEX + r")\b"), CODE,
         "Replace with a token derived in the creative brief. Literals belong only in the token file."),
    Rule("GRADIENT-PURPLE", "identity", "critical", "Purple/indigo/violet <-> blue/pink gradient",
         rx(r"from-(?:purple|indigo|violet|fuchsia)-\d{2,3}[^\"'`]{0,80}?to-(?:blue|pink|purple|indigo|cyan|violet|fuchsia)-\d{2,3}"
            r"|from-(?:blue|pink|cyan)-\d{2,3}[^\"'`]{0,80}?to-(?:purple|indigo|violet|fuchsia)-\d{2,3}"
            r"|(?:linear|radial|conic)-gradient\([^)]*(?:#(?:" + AI_HEX + r")|purple|indigo|violet)[^)]*\)"),
         WEB, "Remove. If depth is needed use the direction's depth model (tone steps, rules, texture, single-hue ramp)."),
    Rule("GRADIENT-TEXT", "identity", "major", "Gradient-filled headline text",
         rx(r"bg-clip-text[^\"'`]{0,60}text-transparent|text-transparent[^\"'`]{0,60}bg-clip-text|-webkit-background-clip:\s*text"),
         WEB, "Solid ink headlines; emphasis comes from size, weight, face and placement."),
    Rule("DEFAULT-ACCENT", "identity", "major", "Untouched framework accent (indigo/violet/blue-500..700 utilities)",
         rx(r"\b(?:bg|text|border|ring|fill|stroke|from|to|via)-(?:indigo|violet|purple|blue)-(?:500|600|700)\b"),
         WEB, "Map to a semantic token (bg-accent, text-accent) defined from the brief.", threshold=3),
    Rule("GLASS", "identity", "major", "Reflexive glassmorphism",
         rx(r"backdrop-blur(?:-\w+)?[^\"'`]{0,80}bg-(?:white|black)/(?:5|10|15|20|30)|bg-(?:white|black)/(?:5|10|15|20|30)[^\"'`]{0,80}backdrop-blur|backdrop-filter:\s*blur"),
         WEB, "Solid surface token. Keep blur only where content genuinely scrolls beneath fixed chrome.", threshold=2),
    Rule("BLOB", "identity", "major", "Decorative blurred blobs / orbs",
         rx(r"(?:absolute|fixed)[^\"'`]{0,120}rounded-full[^\"'`]{0,120}blur-(?:2xl|3xl|\[\d{2,}px\])"
            r"|rounded-full[^\"'`]{0,120}blur-(?:2xl|3xl|\[\d{2,}px\])[^\"'`]{0,120}(?:absolute|fixed)"
            r"|filter:\s*blur\(\s*(?:[4-9]\d|\d{3,})px\s*\)"),
         WEB, "Delete. Background interest must carry meaning (product content, typography, a texture from the direction)."),
    Rule("FLOATING", "identity", "minor", "Random floating / drifting decorative elements",
         rx(r"animate-(?:float|blob|drift|wiggle)\b|@keyframes\s+(?:float|blob|drift)"), WEB,
         "Remove ambient motion that encodes nothing. Motion must explain state or hierarchy."),
    Rule("GLOW", "identity", "minor", "Colored glow shadows",
         rx(r"shadow-(?:purple|indigo|violet|blue|pink|fuchsia|cyan)-\d{3}(?:/\d+)?|shadow-\[0_0_\d+px"), WEB,
         "Remove; emphasis through contrast and position."),
    Rule("FONT-DEFAULT", "identity", "major", "Default AI typeface as the voice (Inter/Poppins/Roboto/Montserrat/Open Sans)",
         rx(r"font-family:\s*['\"]?(?:Inter|Poppins|Roboto|Montserrat|Open Sans)\b"
            r"|import\s*\{[^}]*\b(?:Inter|Poppins|Montserrat|Roboto)\b[^}]*\}\s*from\s*['\"]next/font"
            r"|fonts\.googleapis\.com/css2?\?family=(?:Inter|Poppins|Montserrat|Roboto)\b"
            r"|fontFamily:\s*\{[^}]*['\"](?:Inter|Poppins)['\"]"),
         WEB, "Choose a pairing from references/typography.md that follows from the creative direction."),
    Rule("RADIUS-SPAM", "identity", "minor", "Same large radius on everything",
         rx(r"\brounded-(?:xl|2xl|3xl)\b|border-radius:\s*(?:1[6-9]|2\d|3\d)px"), WEB,
         "One radius philosophy, assigned by role (container/control/chip).", threshold=12),
    Rule("SHADOW-SPAM", "identity", "minor", "Soft blurred shadow on everything",
         rx(r"\bshadow-(?:md|lg|xl|2xl)\b|box-shadow:\s*0\s+\d+px\s+\d+px\s+rgba\(\s*0,\s*0,\s*0"), WEB,
         "One depth model. Real elevation only for things that float (menus, dialogs, toasts).", threshold=10),
    Rule("HERO-3-CARDS", "identity", "major", "Three-column feature grid (the template section)",
         rx(r"(?:sm|md|lg):grid-cols-3\b|grid-template-columns:\s*repeat\(\s*3\s*,\s*(?:1fr|minmax\([^)]*\))\s*\)"), MARKUP | STYLE,
         "Use a layout move from references/layout.md. Keep 3 columns only if the content is truly 3 parallel items (justify it).",
         threshold=1),
    Rule("EMOJI-ICON", "identity", "major", "Emoji used as interface icons",
         rx(r"[\"'>{]\s*(?:🚀|✨|⚡|🔥|💡|🎯|🔒|📈|💎|🌟|⭐|🛡️|🤖|🧠|💪|🎨|📊|🔧|⚙️|💬|📱|🌍|✅)"), CODE,
         "One icon family matched to the type weight, or no icon.", threshold=2),
    Rule("SPARKLE", "identity", "minor", "Sparkle / magic-wand 'AI' motif as decoration",
         rx(r"\b(?:Sparkles?|WandSparkles|Wand2|auto_awesome)\b|✨"), CODE,
         "Only if the feature is literally generative and the brand owns the motif.", threshold=2),
    Rule("COPY-HYPE", "identity", "minor", "Interchangeable hype copy",
         rx(r"\b(?:elevate your|unleash|supercharge|seamless(?:ly)?|revolutioni[sz]e|empower(?:ing)? (?:you|your)|"
            r"transform (?:your|the way)|next[- ]level|game[- ]chang(?:er|ing)|cutting[- ]edge|"
            r"all[- ]in[- ]one (?:platform|solution)|unlock (?:your|the) (?:full )?potential|"
            r"harness the power|in today'?s fast[- ]paced)\b"), CODE,
         "Concrete claim: who gets what result. Numbers and nouns over adjectives.", threshold=2),
    Rule("STOCK-IMAGERY", "identity", "major", "Stock / placeholder imagery services",
         rx(r"images\.unsplash\.com|source\.unsplash|pravatar\.cc|i\.pravatar|picsum\.photos|placehold\.(?:co|it)|"
            r"via\.placeholder|randomuser\.me|ui-avatars\.com|dummyimage\.com|undraw\.co"), CODE,
         "Real product imagery, real content, or typographic composition. Ask the user for assets."),
    Rule("LOREM", "identity", "major", "Lorem ipsum / placeholder copy shipped in UI",
         rx(r"\blorem ipsum\b|\bdolor sit amet\b"), CODE, "Write real copy from the brief or mark it clearly as TODO for the user."),
    Rule("UNVERIFIED-PROOF", "identity", "minor", "Social proof numbers that look invented",
         rx(r"trusted by (?:over )?\d[\d,.]*\+?|\b\d{1,3}(?:[,.]\d{3})*\+?\s*(?:k\+?\s*)?(?:happy |active |satisfied )?(?:users|customers|teams|developers|companies)\b|99\.9+%\s*uptime"),
         MARKUP, "Use only figures the user supplied. Otherwise remove the claim.", threshold=2),
    Rule("SHADCN-UNTOUCHED", "identity", "major", "shadcn/ui theme left on its defaults",
         rx(r"\"baseColor\"\s*:\s*\"(?:slate|zinc|neutral|gray|stone)\"|--primary:\s*222\.2\s+47\.4%\s+11\.2%|--primary:\s*240\s+5\.9%\s+10%"
            r"|--primary:\s*oklch\(0\.205 0 0\)"),
         WEB | {".json"}, "Rewrite the CSS variables from the brief's tokens."),
    Rule("BOUNCE", "identity", "minor", "Attention-seeking default animation",
         rx(r"\banimate-(?:bounce|pulse|ping)\b|cubic-bezier\(\s*0?\.\d+\s*,\s*-?\d*\.?\d+\s*,\s*0?\.\d+\s*,\s*1\.[2-9]"), WEB,
         "Motion tokens from the brief; pulse only for genuinely live status."),

    # Flutter / SwiftUI / Compose identity
    Rule("FL-PURPLE", "identity", "critical", "Flutter template purple",
         rx(r"Colors\.(?:deepPurple|purple|indigo)(?:Accent)?\b"), DART, "Explicit ColorScheme + ThemeExtension from the brief."),
    Rule("FL-SEED-DEFAULT", "identity", "major", "ColorScheme.fromSeed with a stock seed and nothing else",
         rx(r"ColorScheme\.fromSeed\(\s*seedColor:\s*Colors\.\w+\s*\)"), DART, "Define the scheme from the brief's palette."),
    Rule("FL-HARDCODED-COLOR", "identity", "major", "Hard-coded colors outside theme files",
         rx(r"\bColors\.(?!transparent\b)\w+|\bColor\(0x[0-9a-f]{8}\)"), DART,
         "Theme.of(context).colorScheme / ThemeExtension.", threshold=15, skip_theme_files=True),
    Rule("FL-GRADIENT", "identity", "major", "Purple/blue LinearGradient (Flutter)",
         rx(r"LinearGradient\([^;]{0,200}?Colors\.(?:deepPurple|purple|indigo|blue|pink)"), DART, "Remove or single-hue ramp."),
    Rule("SW-PURPLE", "identity", "critical", "SwiftUI purple/indigo accent",
         rx(r"\.(?:tint|accentColor|foregroundColor|foregroundStyle)\(\s*\.(?:purple|indigo)\s*\)|Color\.(?:purple|indigo)\b"), SWIFT,
         "Brand colors from the asset catalog."),
    Rule("KT-TEMPLATE-THEME", "identity", "critical", "Android Studio template theme (Purple80/Pink40...)",
         rx(r"\b(?:Purple80|PurpleGrey80|Pink80|Purple40|PurpleGrey40|Pink40)\b"), KOTLIN, "Replace Color.kt/Theme.kt with the brief's palette."),

    # ======================= FUNCTION (fake / dead UI) =======================
    Rule("DEAD-LINK", "function", "major", "Links that go nowhere (href=\"#\", empty, javascript:void)",
         rx(r"href=\{?[\"']\s*#?\s*[\"']\}?|href=\{?[\"']javascript:void\(0\);?[\"']\}?"), MARKUP,
         "Link to a real route/anchor, or render a <button> with a real handler, or remove it."),
    Rule("NOOP-HANDLER", "function", "major", "Event handlers that do nothing",
         rx(r"on(?:Click|Submit|Change|Press|Tap)=\{\s*\(\s*\w*\s*\)\s*=>\s*(?:\{\s*\}|null|undefined|void 0)\s*\}"
            r"|onPressed:\s*\(\)\s*\{\s*\}|onTap:\s*\(\)\s*\{\s*\}|@click=\"\s*\"|\bonclick=\"\s*\"|action:\s*\{\s*\}"), CODE,
         "Implement the behavior, disable the control with an explanation, or remove it."),
    Rule("FORM-NO-HANDLER", "function", "major", "Form with no submit handling",
         rx(r"<form(?![^>]*(?:action=|onSubmit=|@submit|on:submit|method=|\{\.\.\.))[^>]*>"), MARKUP,
         "Wire submit (server action, handler, or action URL) with validation, loading, success and error states."),
    Rule("CONSOLE-ONLY", "function", "minor", "Handler whose only effect is console.log / alert",
         rx(r"=>\s*(?:console\.log|alert)\([^)]*\)\s*\}?"), WEB, "Real behavior or remove the control.", threshold=1),

    # ======================= ACCESSIBILITY =======================
    Rule("DIV-BUTTON", "accessibility", "major", "Click handler on a non-interactive element",
         rx(r"<(?:div|span|li|img|section|article)\b(?![^>]*\brole=)[^>]*\bon(?:Click|click)\b"), MARKUP,
         "Use <button> or <a>. If impossible: role, tabIndex=0 and key handlers."),
    Rule("IMG-NO-ALT", "accessibility", "major", "Image without alt attribute",
         rx(r"<img\b(?![^>]*\balt=)[^>]*>"), MARKUP, "alt=\"\" for decoration, meaningful alt for content."),
    Rule("FOCUS-REMOVED", "accessibility", "major", "Focus outline removed without a visible replacement",
         rx(r"\boutline-none\b(?![^\"'`]*focus-visible)|outline:\s*(?:none|0)\s*;?(?![^}]*:focus-visible)"), WEB,
         "Keep a visible :focus-visible ring styled from the tokens.", threshold=1),
    Rule("HTML-NO-LANG", "accessibility", "minor", "<html> without lang",
         rx(r"<html(?![^>]*\blang=)[^>]*>"), MARKUP, "Set lang (and dir for RTL)."),
    Rule("TINY-TEXT", "accessibility", "minor", "Text below 12px",
         rx(r"text-\[(?:[0-9]|1[01])px\]|font-size:\s*(?:[0-9]|1[01])px"), WEB, "12px minimum; 16px for body.", threshold=2),
    Rule("ZOOM-BLOCKED", "accessibility", "major", "Pinch-zoom disabled",
         rx(r"user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0)?\b"), MARKUP, "Remove the restriction."),
    Rule("ICON-BUTTON-NO-LABEL", "accessibility", "minor", "Icon-only button without accessible name",
         rx(r"<button\b(?![^>]*\baria-label)[^>]*>\s*<(?:svg|[A-Z]\w*Icon|[A-Z]\w*\s*/>)"), MARKUP,
         "Add aria-label or visually hidden text.", threshold=1),

    # ======================= PERFORMANCE =======================
    Rule("FONT-IMPORT-BLOCKING", "performance", "minor", "Render-blocking @import of web fonts",
         rx(r"@import\s+url\(\s*['\"]?https://fonts\.googleapis"), STYLE,
         "Self-host or use the framework font loader (next/font, @fontsource) with font-display: swap."),
    Rule("IMG-NO-DIMENSIONS", "performance", "minor", "<img> without width/height (layout shift)",
         rx(r"<img\b(?![^>]*\b(?:width|height)=)[^>]*>"), MARKUP,
         "Set intrinsic width/height or aspect-ratio; use the framework image component.", threshold=3),
    Rule("TRANSITION-ALL", "performance", "minor", "transition: all (animates layout properties)",
         rx(r"\btransition-all\b|transition:\s*all\b"), WEB, "Transition only transform/opacity/color.", threshold=5),
    Rule("FIXED-WIDTH", "performance", "minor", "Large fixed pixel widths (breaks small screens)",
         rx(r"\bw-\[(?:[5-9]\d\d|\d{4,})px\]|(?<![-\w])width:\s*(?:[5-9]\d\d|\d{4,})px"), WEB,
         "Fluid widths (max-width, minmax, clamp, %).", threshold=2),
]

THEME_HINT = re.compile(r"(theme|color|colour|palette|tokens?|design[_-]?system|brand)", re.I)


def iter_files(root: Path):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            p = Path(dirpath) / fn
            if p.suffix not in CODE and fn != "components.json":
                continue
            if fn.endswith((".min.js", ".min.css", ".g.dart", ".freezed.dart", ".d.ts", ".map")):
                continue
            try:
                if p.stat().st_size > 1_500_000:
                    continue
            except OSError:
                continue
            yield p


def scan(root: Path) -> dict:
    stats = {"files": 0, "web": 0, "flutter": 0, "swift": 0, "kotlin": 0}
    raw: dict = {}
    for path in iter_files(root):
        ext = path.suffix
        stats["files"] += 1
        if ext in WEB: stats["web"] += 1
        elif ext in DART: stats["flutter"] += 1
        elif ext in SWIFT: stats["swift"] += 1
        elif ext in KOTLIN: stats["kotlin"] += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        is_theme = bool(THEME_HINT.search(path.name))
        rel = str(path.relative_to(root))
        for rule in RULES:
            if not (ext in rule.exts or (path.name == "components.json" and ".json" in rule.exts)):
                continue
            if rule.skip_theme_files and is_theme:
                continue
            for m in rule.pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                entry = raw.setdefault(rule.id, {"count": 0, "locations": []})
                entry["count"] += 1
                if len(entry["locations"]) < 10:
                    entry["locations"].append(f"{rel}:{line}  {m.group(0).strip()[:80]}")

    by_id = {r.id: r for r in RULES}
    findings, cat_pen = [], {c: 0.0 for c in CATEGORIES}
    for rid, e in raw.items():
        r = by_id[rid]
        if e["count"] < r.threshold:
            continue
        over = e["count"] / max(r.threshold, 1)
        factor = min(2.0, 1.0 + math.log2(over) * 0.35) if over > 1 else 1.0
        pen = WEIGHT[r.severity] * factor
        cat_pen[r.category] += pen
        findings.append({"rule": rid, "category": r.category, "severity": r.severity, "title": r.title,
                         "count": e["count"], "penalty": round(pen, 1), "fix": r.fix, "locations": e["locations"]})
    order = {"critical": 0, "major": 1, "minor": 2}
    findings.sort(key=lambda f: (CATEGORIES.index(f["category"]), order[f["severity"]], -f["penalty"]))

    categories = {c: max(0, round(100 - p)) for c, p in cat_pen.items()}
    total = max(0, round(100 - sum(cat_pen.values())))
    return {"tool": "anti-slop", "version": VERSION, "root": str(root), "score": total,
            "grade": grade(total), "categories": categories,
            "design_file": (root / "DESIGN.md").exists(), "stats": stats, "findings": findings}


def grade(s: int) -> str:
    if s >= 90: return "Intentional — no known tells"
    if s >= 75: return "Mostly intentional — a few defaults remain"
    if s >= 55: return "Templated — reads as a starter kit"
    if s >= 35: return "Generic — looks AI-generated"
    return "Slop — indistinguishable from every other AI site"


def bar(s: int, w: int = 28) -> str:
    n = round(s / 100 * w)
    return "█" * n + "░" * (w - n)


def text_report(r: dict, before: dict | None) -> str:
    out = []
    s = r["stats"]
    out.append(f"\nANTI-SLOP scan v{r['version']} — {r['root']}")
    out.append(f"files: {s['files']} (web {s['web']}, flutter {s['flutter']}, swift {s['swift']}, kotlin {s['kotlin']})\n")
    out.append(f"  SCORE {r['score']:>3}/100  {bar(r['score'])}  {r['grade']}")
    for c in CATEGORIES:
        b = f"   (was {before['categories'].get(c, '?')})" if before else ""
        out.append(f"    {c:<14}{r['categories'][c]:>3}{b}")
    if before:
        d = r["score"] - before["score"]
        out.append(f"\n  before {before['score']} -> after {r['score']}  ({'+' if d >= 0 else ''}{d})")
        b_ids = {f["rule"] for f in before["findings"]}
        a_ids = {f["rule"] for f in r["findings"]}
        if b_ids - a_ids: out.append(f"  fixed: {', '.join(sorted(b_ids - a_ids))}")
        if a_ids - b_ids: out.append(f"  new:   {', '.join(sorted(a_ids - b_ids))}")
    out.append(f"  DESIGN.md present: {'yes' if r['design_file'] else 'no'}\n")
    if not r["findings"]:
        out.append("No known code-level tells. Static analysis can't see the rendered page —")
        out.append("run the visual review in checklists/quality-gate.md before calling it done.\n")
    cur = None
    for f in r["findings"]:
        if f["category"] != cur:
            cur = f["category"]
            out.append(f"── {cur.upper()} " + "─" * (40 - len(cur)))
        out.append(f"[{f['severity'][:4].upper()}] {f['rule']:<22} ×{f['count']:<3} −{f['penalty']:<5} {f['title']}")
        for loc in f["locations"][:3]:
            out.append(f"        {loc}")
        if f["count"] > 3:
            out.append(f"        … {f['count'] - 3} more")
        out.append(f"        fix: {f['fix']}")
    return "\n".join(out) + "\n"


def md_report(r: dict, before: dict | None) -> str:
    lines = [f"# ANTI-SLOP scan — score {r['score']}/100", "", f"_{r['grade']}_", "",
             "| Category | Score |" + (" Before |" if before else ""), "|---|---|" + ("---|" if before else "")]
    for c in CATEGORIES:
        lines.append(f"| {c} | {r['categories'][c]} |" + (f" {before['categories'].get(c, '')} |" if before else ""))
    lines += ["", "| Severity | Rule | Count | Where (first) | Fix |", "|---|---|---|---|---|"]
    for f in r["findings"]:
        where = f["locations"][0].split("  ")[0] if f["locations"] else ""
        lines.append(f"| {f['severity']} | `{f['rule']}` | {f['count']} | `{where}` | {f['fix']} |")
    lines += ["", "Static analysis only. See `checklists/quality-gate.md` for the rendered-page review."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Detect generic AI-generated frontend patterns.")
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", metavar="FILE")
    ap.add_argument("--compare", metavar="BEFORE_JSON")
    ap.add_argument("--fail-under", type=int)
    ap.add_argument("--list-rules", action="store_true")
    a = ap.parse_args()

    if a.list_rules:
        for r in RULES:
            print(f"{r.id:<22} {r.category:<14} {r.severity:<9} {r.title}")
        print(f"\n{len(RULES)} rules")
        return
    root = Path(a.root).resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    res = scan(root)
    before = json.loads(Path(a.compare).read_text(encoding="utf-8")) if a.compare else None
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(text_report(res, before))
    if a.md:
        Path(a.md).write_text(md_report(res, before), encoding="utf-8")
    if a.fail_under is not None and res["score"] < a.fail_under:
        print(f"score {res['score']} < required {a.fail_under}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
