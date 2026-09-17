"""Build the testing-VM system_config.yaml for force_qty (4 changes, closed change set) from the preserved VM bytes
(md5 4eab1ae5...), then validate. Never touches the VM or the worktree. ASCII stdout.
Checks: (1) new loader + NEW yaml loads with the 4 values; (2) new loader + OLD yaml loads, force_qty None (the
intermediate state code-before-config); (3) OLD loader + NEW yaml FAILS (=> config goes LAST, rolls back FIRST);
(4) NEW yaml with force_qty 0 FAILS naming force_qty; (5) auditor, all groups, old vs new yaml: finding diff;
(6) the new yaml differs from the old in exactly the intended lines."""
import difflib
import hashlib
import shutil
import subprocess
import sys
import types
from pathlib import Path

WT = Path("D:/Projects/wt-sr-shadow-15sep")
sys.path.insert(0, str(WT))
HERE = Path(__file__).resolve().parent
OUT = HERE / "cfgcheck"
SRC = Path("D:/Projects/_preservation/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml")


def p(*a):
    print(" ".join(str(x) for x in a).encode("ascii", "backslashreplace").decode("ascii"))


raw = SRC.read_bytes()
assert hashlib.md5(raw).hexdigest() == "4eab1ae5a9716059431b55a210e917c9"
assert raw.count(b"\r") == 0 and raw.endswith(b"\n")
L = raw.decode("utf-8").split("\n")


def one(pred, what):
    hits = [i for i, l in enumerate(L) if pred(l)]
    assert len(hits) == 1, (what, hits)
    return hits[0]


i_es = one(lambda l: l.startswith('  entry_start: "10:00"        # [LAUNCH-PHASE]'), "entry_start")
i_msq = one(lambda l: l.startswith("  max_single_order_qty: 10000 # FIX-041"), "max_single_order_qty")
i_mpv = one(lambda l: l.startswith("  max_position_value_pct: 0.40   # hard cap"), "max_position_value_pct")
i_dmpv = one(lambda l: l.startswith("  delivery_max_position_value_pct: 0.40   # = global"), "delivery_max_position_value_pct")
assert i_es < i_msq < i_mpv < i_dmpv
assert sum("force_qty" in l for l in L) == 0

N = list(L)
# apply bottom-up so earlier indices stay valid
N[i_dmpv] = N[i_dmpv].replace("delivery_max_position_value_pct: 0.40", "delivery_max_position_value_pct: 0.50", 1)
N.insert(i_dmpv, "  # TESTING VM ONLY (17-Sep-2026, Rama): 0.40 -> 0.50 with force_qty. Production and the repo keep 0.40.")
N[i_mpv] = N[i_mpv].replace("max_position_value_pct: 0.40", "max_position_value_pct: 0.50", 1)
N.insert(i_mpv, "  # TESTING VM ONLY (17-Sep-2026, Rama): 0.40 -> 0.50 with force_qty. Production and the repo keep 0.40.")
N[i_msq + 1:i_msq + 1] = [
    "  # force_qty -- TESTING VM ONLY (17-Sep-2026, Rama: \"only with 1 Qty; [Not more than 1qty]\").",
    "  # OVERRIDE, not a clamp: every sized signal gets exactly this qty; the risk / capital /",
    "  # concentration rungs and the tier x perf multiplier are BYPASSED (the SL-distance guard,",
    "  # lot rounding, output qty guard, position-value cap and minimum still run).",
    "  # Production and the repo: key ABSENT (= null = OFF).",
    "  force_qty: 1",
]
N[i_es] = N[i_es].replace('entry_start: "10:00"', 'entry_start: "09:30"', 1)
N.insert(i_es, '  # TESTING VM ONLY (17-Sep-2026, Rama): "10:00" -> "09:30". Production and the repo keep "10:00".')
new_text = "\n".join(N)
new_bytes = new_text.encode("utf-8")

OUT.mkdir(exist_ok=False)
(OUT / "system_config.NEW.yaml").write_bytes(new_bytes)
p("NEW yaml", len(new_bytes), "B md5", hashlib.md5(new_bytes).hexdigest(), "| lines", new_text.count("\n"), "| CR", new_bytes.count(b"\r"))

# (6) exact diff
d = [x for x in difflib.unified_diff(L, N, lineterm="", n=0) if not x.startswith(("---", "+++"))]
p("DIFF old->new (", len([x for x in d if x[:1] in "+-"]), "changed lines):")
for x in d:
    p("  ", x[:170])

# config dirs
for tag, yb in (("new", new_bytes), ("old", raw)):
    dst = OUT / f"cfg_{tag}"
    shutil.copytree(WT / "config", dst)
    (dst / "system_config.yaml").write_bytes(yb)

from core import config_loader as NEWL  # noqa: E402  (the worktree = the build)
from core.config_auditor import audit_app_config  # noqa: E402

c_new = NEWL.load_all(OUT / "cfg_new")
ps, th = c_new.system.position_sizing, c_new.system.trading_hours
p("(1) new loader + NEW yaml: OK | force_qty", ps.force_qty, "| entry_start", th.entry_start, "| max_position_value_pct",
  ps.max_position_value_pct, "| delivery_max_position_value_pct", ps.delivery_max_position_value_pct,
  "| max_concentration_pct", ps.max_concentration_pct, "| delivery_max_concentration_pct", ps.delivery_max_concentration_pct,
  "| risk.max_open_positions", c_new.system.risk.max_open_positions)
c_old = NEWL.load_all(OUT / "cfg_old")
p("(2) new loader + OLD yaml: OK | force_qty", c_old.system.position_sizing.force_qty, "| entry_start", c_old.system.trading_hours.entry_start)

old_src = subprocess.run(["git", "-C", str(WT), "show", "e7bf477:core/config_loader.py"], capture_output=True, check=True).stdout.decode("utf-8")
m = types.ModuleType("config_loader_e7bf477")
m.__file__ = str(HERE / "config_loader_e7bf477.py")
sys.modules[m.__name__] = m
exec(compile(old_src, m.__file__, "exec"), m.__dict__)
try:
    m.load_all(OUT / "cfg_new")
    p("(3) OLD loader + NEW yaml: LOADED  <-- UNEXPECTED")
except Exception as exc:  # noqa: BLE001
    s = str(exc)
    p("(3) OLD loader + NEW yaml: FAILED as expected |", type(exc).__name__, "| mentions force_qty:", "force_qty" in s, "|", s[:160].replace("\n", " "))
ctl = m.load_all(OUT / "cfg_old")
p("(3-control) OLD loader + OLD yaml: OK | entry_start", ctl.system.trading_hours.entry_start)

bad = OUT / "cfg_bad"
shutil.copytree(OUT / "cfg_new", bad)
bt = new_text.replace("\n  force_qty: 1\n", "\n  force_qty: 0\n", 1)
assert bt != new_text
(bad / "system_config.yaml").write_bytes(bt.encode("utf-8"))
try:
    NEWL.load_all(bad)
    p("(4) force_qty 0: LOADED  <-- UNEXPECTED")
except Exception as exc:  # noqa: BLE001
    s = str(exc)
    p("(4) force_qty 0: FAILED as expected | mentions force_qty:", "force_qty" in s, "|", s[:140].replace("\n", " "))


def findings(cfg, d):
    rep = audit_app_config(cfg, config_dir=d)
    return [(f.group if hasattr(f, "group") else "", getattr(f, "code", ""), str(getattr(f, "severity", "")),
             str(getattr(f, "message", ""))) for f in rep.findings]


fo, fn = findings(c_old, OUT / "cfg_old"), findings(c_new, OUT / "cfg_new")
p("(5) auditor ALL groups: old", len(fo), "findings | new", len(fn))
p("    codes old:", sorted({(x[1], x[2]) for x in fo}))
p("    codes new:", sorted({(x[1], x[2]) for x in fn}))
so, sn = set(fo), set(fn)
for x in sorted(so - sn):
    p("    ONLY OLD:", x[1], x[2], "|", x[3][:200])
for x in sorted(sn - so):
    p("    ONLY NEW:", x[1], x[2], "|", x[3][:200])
p("    C2 / C2d present in NEW:", [x[1] for x in fn if x[1].startswith("C2")])
