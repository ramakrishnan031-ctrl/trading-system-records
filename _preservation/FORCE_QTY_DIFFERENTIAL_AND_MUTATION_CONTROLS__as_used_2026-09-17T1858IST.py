"""force_qty build controls (17-Sep-2026). ASCII stdout.
PART 1 -- DIFFERENTIAL: the new sizer with force_qty=None vs the e7bf477 sizer (git blob), over a grid.
          Every SizingResult field (incl. breakdown and reason) and every logger call must be identical.
PART 2 -- MUTATION CONTROLS: the new test file, run against deliberately broken copies of the new sizer.
          Each mutation MUST make at least one test fail, else the tests do not testify about it."""
import importlib.util
import itertools
import subprocess
import sys
import types
from pathlib import Path

WT = Path("D:/Projects/wt-sr-shadow-15sep")
sys.path.insert(0, str(WT))
HERE = Path(__file__).resolve().parent

import capital  # noqa: E402  (package)
from capital.fund_manager import CapitalSnapshot  # noqa: E402
from core.time_authority import now_ist  # noqa: E402


def p(*a):
    print(" ".join(str(x) for x in a).encode("ascii", "backslashreplace").decode("ascii"))


def load_module(name, source):
    mod = types.ModuleType(name)
    mod.__file__ = str(HERE / (name + ".py"))
    sys.modules[name] = mod  # dataclasses resolves annotations via sys.modules[cls.__module__]
    exec(compile(source, mod.__file__, "exec"), mod.__dict__)
    return mod


old_src = subprocess.run(["git", "-C", str(WT), "show", "e7bf477:capital/position_sizer.py"],
                         capture_output=True, check=True).stdout.decode("utf-8")
new_src = (WT / "capital" / "position_sizer.py").read_text(encoding="utf-8")
assert old_src != new_src
OLD = load_module("ps_old_e7bf477", old_src)
NEW = load_module("ps_new_forceqty", new_src)


class FM:
    def __init__(self, total, intra, pos):
        self.s = CapitalSnapshot(total=total, intraday_avail=intra, intraday_reserved=0.0, intraday_used=0.0,
                                 positional_avail=pos, positional_reserved=0.0, positional_used=0.0,
                                 daily_realized_pnl=0.0, ts=now_ist().replace(tzinfo=None).isoformat())

    def get_snapshot(self):
        return self.s


class Log:
    def __init__(self):
        self.calls = []

    def __getattr__(self, level):
        if level in ("debug", "info", "warning", "error", "critical"):
            return lambda msg, extra=None: self.calls.append((level, msg, dict(extra or {})))
        raise AttributeError(level)


LEV = {"INTRADAY": 5.0, "COVER_ORDER": 6.0, "DELIVERY": 1.0, "BRACKET_ORDER": 5.0}
caps = [(9_992.80, 6_994.96, 2_997.84), (100_000.0, 70_000.0, 30_000.0), (500.0, 350.0, 150.0)]
prices = [(100.0, 98.0), (1200.0, 1188.0), (6000.0, 5940.0), (100.0, 99.99), (50.0, 49.96), (250.0, 260.0), (3.0, 2.9)]
intents = ["INTRADAY", "DELIVERY", "COVER_ORDER"]
tiers = ["HIGH", "MEDIUM", "LOW"]
lots = [1, 2, 25]
perfs = [1.0, 0.0, 2.0, 0.5]
offsets = [0.0, 0.002]
modes = [dict(enabled=True, flat_value_rs=None), dict(enabled=False, flat_value_rs=1500.0)]
vcaps = [0.40, 0.50]
n = mism = 0
for (tot, ia, pa), (e, s), it, tr, lot, pw, off, md, vc in itertools.product(caps, prices, intents, tiers, lots, perfs, offsets, modes, vcaps):
    side = "BUY" if s < e else "SELL"
    res = []
    for M, extra in ((OLD, {}), (NEW, {"force_qty": None})):
        lg = Log()
        sz = M.PositionSizer(fund_manager=FM(tot, ia, pa), leverage_map=LEV, risk_per_trade_pct=0.01,
                             max_concentration_pct=0.10, max_position_value_pct=vc, logger=lg,
                             delivery_risk_per_trade_pct=0.01, delivery_max_concentration_pct=0.10,
                             delivery_max_position_value_pct=vc, **md, **extra)
        try:
            r = sz.calculate("SYM", side, e, s, it, score_tier=tr, lot_size=lot, entry_offset_pct=off, perf_weight=pw)
            out = ("OK", r.success, r.qty, r.margin_required, r.risk_amount, r.bucket, r.constraint, r.reason, r.breakdown)
        except Exception as exc:  # a raise must be identical too
            out = ("RAISE", type(exc).__name__, str(exc))
        res.append((out, lg.calls))
    n += 1
    if res[0] != res[1]:
        mism += 1
        if mism <= 3:
            p("MISMATCH", (tot, e, s, it, tr, lot, pw, off, md, vc), res[0][0][:7], res[1][0][:7])
outcomes = None
p("PART 1 differential: cases", n, "| mismatches", mism)

# control for PART 1: the same comparison must SEE a difference when one exists
lg1, lg2 = Log(), Log()
a = OLD.PositionSizer(fund_manager=FM(9_992.80, 6_994.96, 2_997.84), leverage_map=LEV, risk_per_trade_pct=0.01,
                      max_concentration_pct=0.10, max_position_value_pct=0.5, logger=lg1)
b = NEW.PositionSizer(fund_manager=FM(9_992.80, 6_994.96, 2_997.84), leverage_map=LEV, risk_per_trade_pct=0.01,
                      max_concentration_pct=0.10, max_position_value_pct=0.5, logger=lg2, force_qty=1)
ra = a.calculate("SYM", "BUY", 1200.0, 1188.0, "INTRADAY")
rb = b.calculate("SYM", "BUY", 1200.0, 1188.0, "INTRADAY")
p("PART 1 control (force_qty=1 vs old): differs ->", (ra, lg1.calls) != (rb, lg2.calls), "| old", ra.constraint, ra.qty, "| new", rb.constraint, rb.qty)

# ---- PART 2
TEST = WT / "tests" / "unit" / "test_force_qty_override_17sep.py"
MUTS = {
    "M1 forced qty + 1": ("            tiered_qty = self._force_qty\n", "            tiered_qty = self._force_qty + 1\n"),
    "M2 value cap skipped under override": ("        if position_value > max_position_value:\n",
                                            "        if self._force_qty is None and position_value > max_position_value:\n"),
    "M3 constructor ignores force_qty": ("        self._force_qty = force_qty\n", "        self._force_qty = None\n"),
    "M4 warning renamed": ('                "position_sizer.force_qty_override",\n', '                "position_sizer.renamed",\n'),
    "M5 lot rounding bypassed": ("        final_qty = (tiered_qty // lot_size) * lot_size\n", "        final_qty = tiered_qty\n"),
    "M6 constructor accepts 0": ("isinstance(force_qty, bool) or not isinstance(force_qty, int) or force_qty < 1",
                                 "isinstance(force_qty, bool) or not isinstance(force_qty, int) or force_qty < 0"),
}
for name, (a_, b_) in MUTS.items():
    cnt = new_src.count(a_)
    if cnt != 1:
        p(name, "SKIPPED: anchor count", cnt)
        continue
    msrc = new_src.replace(a_, b_, 1)
    mod = load_module("capital.position_sizer", msrc)
    sys.modules["capital.position_sizer"] = mod
    capital.position_sizer = mod
    spec = importlib.util.spec_from_file_location("t_fq_" + name[:2], TEST)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    fails, total = [], 0
    import inspect
    import pytest  # noqa: F401
    for fname, fn in sorted(vars(tm).items()):
        if not (fname.startswith("test_") and callable(fn)):
            continue
        params = getattr(fn, "pytestmark", [])
        argsets = [()]
        for m in params:
            if m.name == "parametrize":
                argsets = [(v,) for v in m.args[1]]
        for args in argsets:
            total += 1
            try:
                fn(*args)
            except BaseException:  # noqa: BLE001
                fails.append(fname)
    p(f"PART 2 {name}: tests run {total}, FAILED {len(fails)} ->", "CAUGHT" if fails else "NOT CAUGHT", sorted(set(fails))[:4])
