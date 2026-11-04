"""
Regression tests for slop_scan.py.

Every rule must have a POSITIVE case (must fire) and, where false positives are
plausible, a NEGATIVE case (must not fire). A new rule without a positive case
fails `test_every_rule_has_a_positive_case`.

Run: python3 -m pytest tests/   or   python3 tests/test_rules.py
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN = ROOT / "skills" / "anti-slop" / "scripts" / "slop_scan.py"
spec = importlib.util.spec_from_file_location("slop_scan", SCAN)
slop = importlib.util.module_from_spec(spec)
sys.modules["slop_scan"] = slop
spec.loader.exec_module(slop)

# rule id -> (filename, content). Content repeats where a threshold requires it.
POSITIVE = {
    "AI-HEX": ("a.css", ".x{color:#6366f1}"),
    "GRADIENT-PURPLE": ("a.tsx", '<div className="bg-gradient-to-r from-purple-600 to-blue-500" />'),
    "GRADIENT-TEXT": ("a.tsx", '<h1 className="bg-clip-text text-transparent" />'),
    "DEFAULT-ACCENT": ("a.tsx", '<a className="bg-indigo-600"/><b className="text-blue-600"/><i className="border-violet-500"/>'),
    "GLASS": ("a.css", ".a{backdrop-filter: blur(8px)} .b{backdrop-filter: blur(4px)}"),
    "BLOB": ("a.tsx", '<div className="absolute -top-10 h-72 w-72 rounded-full bg-cyan-400 blur-3xl" />'),
    "FLOATING": ("a.css", "@keyframes float { 50% { transform: translateY(10px) } }"),
    "GLOW": ("a.tsx", '<button className="shadow-purple-500/50" />'),
    "FONT-DEFAULT": ("a.tsx", 'import { Inter } from "next/font/google";'),
    "RADIUS-SPAM": ("a.tsx", '<i className="rounded-2xl"/>' * 12),
    "SHADOW-SPAM": ("a.tsx", '<i className="shadow-lg"/>' * 10),
    "HERO-3-CARDS": ("a.tsx", '<div className="grid md:grid-cols-3" />'),
    "EMOJI-ICON": ("a.tsx", '<div>"🚀"</div><div>"🔒"</div>'),
    "SPARKLE": ("a.tsx", 'import { Sparkles } from "lucide-react"; <Sparkles />'),
    "COPY-HYPE": ("a.tsx", "<h1>Elevate your workflow</h1><p>A seamless experience</p>"),
    "STOCK-IMAGERY": ("a.tsx", '<img alt="" src="https://images.unsplash.com/photo-1" />'),
    "LOREM": ("a.html", "<p>Lorem ipsum dolor sit amet</p>"),
    "UNVERIFIED-PROOF": ("a.tsx", "<p>Trusted by 10,000+ teams</p><p>99.9% uptime</p>"),
    "SHADCN-UNTOUCHED": ("components.json", '{"tailwind": {"baseColor": "slate"}}'),
    "BOUNCE": ("a.tsx", '<i className="animate-bounce" />'),
    "FL-PURPLE": ("main.dart", "color: Colors.deepPurple,"),
    "FL-SEED-DEFAULT": ("main.dart", "ColorScheme.fromSeed(seedColor: Colors.blue)"),
    "FL-HARDCODED-COLOR": ("home.dart", "Colors.red " * 15),
    "FL-GRADIENT": ("main.dart", "LinearGradient(colors: [Colors.purple, Colors.blue])"),
    "SW-PURPLE": ("V.swift", "Text(\"a\").foregroundColor(.purple)"),
    "KT-TEMPLATE-THEME": ("Color.kt", "val Purple80 = Color(0xFFD0BCFF)"),
    "DEAD-LINK": ("a.tsx", '<a href="#">Pricing</a>'),
    "NOOP-HANDLER": ("a.tsx", "<button onClick={() => {}}>Buy</button>"),
    "FORM-NO-HANDLER": ("a.html", '<form class="x"><input></form>'),
    "CONSOLE-ONLY": ("a.tsx", "<button onClick={() => console.log('clicked')}>Go</button>"),
    "DIV-BUTTON": ("a.tsx", "<div className=\"card\" onClick={open}>x</div>"),
    "IMG-NO-ALT": ("a.html", '<img src="a.png">'),
    "FOCUS-REMOVED": ("a.css", "a { outline: none; }"),
    "HTML-NO-LANG": ("a.html", "<html><body></body></html>"),
    "TINY-TEXT": ("a.css", ".a{font-size: 10px} .b{font-size: 11px}"),
    "ZOOM-BLOCKED": ("a.html", '<meta name="viewport" content="width=device-width, user-scalable=no">'),
    "ICON-BUTTON-NO-LABEL": ("a.tsx", "<button><svg /></button>"),
    "FONT-IMPORT-BLOCKING": ("a.css", "@import url('https://fonts.googleapis.com/css2?family=Fraunces');"),
    "IMG-NO-DIMENSIONS": ("a.html", '<img alt="" src="1.png"><img alt="" src="2.png"><img alt="" src="3.png">'),
    "TRANSITION-ALL": ("a.tsx", '<i className="transition-all"/>' * 5),
    "FIXED-WIDTH": ("a.css", ".a{width: 1200px} .b{width: 900px}"),
}

NEGATIVE = {
    "AI-HEX": ("a.css", ".x{color:#2C3E8F}"),
    "GRADIENT-PURPLE": ("a.css", ".x{background: linear-gradient(#F4F1E8, #EAE5D6)}"),
    "DEFAULT-ACCENT": ("a.tsx", '<a className="bg-accent text-accent-ink"/>'),
    "FONT-DEFAULT": ("a.css", "body { font-family: 'IBM Plex Sans', sans-serif; }"),
    "HERO-3-CARDS": ("a.css", ".g{grid-template-columns: 7fr 5fr}"),
    "DEAD-LINK": ("a.html", '<a href="#main">Skip</a> <a href="/pricing">Pricing</a>'),
    "FORM-NO-HANDLER": ("a.tsx", "<form onSubmit={save}><input /></form>"),
    "DIV-BUTTON": ("a.tsx", "<button onClick={open}>x</button>"),
    "IMG-NO-ALT": ("a.html", '<img src="a.png" alt="">'),
    "FOCUS-REMOVED": ("a.tsx", '<a className="outline-none focus-visible:ring-2" />'),
    "HTML-NO-LANG": ("a.html", '<html lang="fr"></html>'),
    "ZOOM-BLOCKED": ("a.html", '<meta name="viewport" content="width=device-width, initial-scale=1">'),
    "ICON-BUTTON-NO-LABEL": ("a.tsx", '<button aria-label="Close"><svg /></button>'),
    "COPY-HYPE": ("a.tsx", "<h1>Know who owes you, to the franc.</h1>"),
    "UNVERIFIED-PROOF": ("a.tsx", "<p>Opening to shops in Djibouti.</p>"),
    "FL-HARDCODED-COLOR": ("app_theme.dart", "Colors.red " * 30),  # theme files are exempt
}


def rules_fired(filename: str, content: str) -> set:
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / filename).write_text(content, encoding="utf-8")
        return {f["rule"] for f in slop.scan(Path(d))["findings"]}


def test_every_rule_has_a_positive_case():
    missing = {r.id for r in slop.RULES} - set(POSITIVE)
    assert not missing, f"rules without a positive test case: {sorted(missing)}"


def test_positive_cases_fire():
    failures = [rid for rid, (fn, c) in POSITIVE.items() if rid not in rules_fired(fn, c)]
    assert not failures, f"rules that did not fire on their positive case: {failures}"


def test_negative_cases_do_not_fire():
    failures = [rid for rid, (fn, c) in NEGATIVE.items() if rid in rules_fired(fn, c)]
    assert not failures, f"false positives: {failures}"


def test_seed_is_slop_and_example_is_clean():
    seed = slop.scan(ROOT / "bench" / "seeds" / "generic-landing")
    after = slop.scan(ROOT / "examples" / "harbor-ledger" / "after")
    assert seed["score"] < 20, seed["score"]
    assert after["score"] >= 95, (after["score"], [f["rule"] for f in after["findings"]])
    assert after["categories"]["function"] == 100


def test_cli_json_and_fail_under():
    seed = ROOT / "bench" / "seeds" / "generic-landing"
    out = subprocess.run([sys.executable, str(SCAN), str(seed), "--json"], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout)["tool"] == "anti-slop"
    gate = subprocess.run([sys.executable, str(SCAN), str(seed), "--fail-under", "50"], capture_output=True, text=True)
    assert gate.returncode == 1


def test_skips_dependency_dirs():
    with tempfile.TemporaryDirectory() as d:
        nm = Path(d) / "node_modules" / "lib"
        nm.mkdir(parents=True)
        (nm / "x.css").write_text(".x{color:#6366f1}", encoding="utf-8")
        assert slop.scan(Path(d))["score"] == 100


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} passed")
