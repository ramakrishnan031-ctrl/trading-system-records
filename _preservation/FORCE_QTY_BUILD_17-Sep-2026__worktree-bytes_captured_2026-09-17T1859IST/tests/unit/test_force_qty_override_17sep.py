"""
tests/unit/test_force_qty_override_17sep.py

position_sizing.force_qty (17-Sep-2026, TESTING VM ONLY) — Rama: "All stocks can be
traded without concentration limits, But only with 1 Qty; [Not more than 1qty]".

An OVERRIDE, not a clamp: with force_qty set, PositionSizer uses exactly that quantity
in place of the risk / capital / concentration rungs and the tier × perf multiplier.
The SL-distance guard before them and the tail after them still run (lot rounding,
output qty guard, position-value cap, minimum). Default None = today's sizing.

Pinned here:
  * config: absent -> None; 1 and 5 load; 0, -1, true, 1.5, "1" are refused;
  * a stock the 10% concentration rung zeroes is sized to exactly 1;
  * 1 can never become more: lot 2 -> BELOW_MIN, never rounded up;
  * the tail still rejects: position-value cap, SL-distance guard;
  * a zero multiplier does not skip an override;
  * one WARNING per sizing call, naming the key and the value;
  * margin_required / risk_amount are built from the forced quantity;
  * the constructor refuses a bad value;
  * main.py passes ps_cfg.force_qty into the one production PositionSizer(...).
"""
from __future__ import annotations

import ast
import copy
import sys
from pathlib import Path

import pytest
import yaml

_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))

from capital.fund_manager import CapitalSnapshot            # noqa: E402
from capital.position_sizer import PositionSizer            # noqa: E402
from core.config_loader import PositionSizingConfig         # noqa: E402
from core.time_authority import now_ist                     # noqa: E402

_LEV = {"INTRADAY": 5.0, "COVER_ORDER": 6.0, "DELIVERY": 1.0, "BRACKET_ORDER": 5.0}
_TIERS = {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.5}

# The testing VM's capital at the 17-Sep boot (Rs 9,992.80 total).
_TOTAL, _INTRA, _POS = 9_992.80, 6_994.96, 2_997.84


class _FM:
    def __init__(self, total=_TOTAL, intraday=_INTRA, positional=_POS):
        self._snap = CapitalSnapshot(
            total=total, intraday_avail=intraday, intraday_reserved=0.0,
            intraday_used=0.0, positional_avail=positional, positional_reserved=0.0,
            positional_used=0.0, daily_realized_pnl=0.0,
            ts=now_ist().replace(tzinfo=None).isoformat())

    def get_snapshot(self):
        return self._snap


class _Log:
    def __init__(self):
        self.calls = []

    def _rec(self, level, msg, extra=None):
        self.calls.append((level, msg, dict(extra or {})))

    def debug(self, msg, extra=None):
        self._rec("DEBUG", msg, extra)

    def info(self, msg, extra=None):
        self._rec("INFO", msg, extra)

    def warning(self, msg, extra=None):
        self._rec("WARNING", msg, extra)

    def error(self, msg, extra=None):
        self._rec("ERROR", msg, extra)

    def critical(self, msg, extra=None):
        self._rec("CRITICAL", msg, extra)


def _sizer(force_qty=None, log=None, max_position_value_pct=0.50, **kw):
    return PositionSizer(
        fund_manager=kw.pop("fm", _FM()), leverage_map=_LEV,
        risk_per_trade_pct=0.01, max_concentration_pct=0.10,
        max_position_value_pct=max_position_value_pct,
        tier_multipliers=_TIERS, logger=log,
        delivery_risk_per_trade_pct=0.01, delivery_max_concentration_pct=0.10,
        delivery_max_position_value_pct=max_position_value_pct,
        force_qty=force_qty, **kw)


# ── config ────────────────────────────────────────────────────────────────────

def _repo_position_sizing() -> dict:
    raw = yaml.safe_load((_REPO / "config" / "system_config.yaml").read_text(encoding="utf-8"))
    ps = copy.deepcopy(raw["position_sizing"])
    assert "force_qty" not in ps, "the repo config must keep force_qty ABSENT (testing VM only)"
    return ps


def test_config_absent_force_qty_is_none() -> None:
    assert PositionSizingConfig(**_repo_position_sizing()).force_qty is None


@pytest.mark.parametrize("value", [1, 5])
def test_config_accepts_positive_integers(value) -> None:
    ps = _repo_position_sizing()
    ps["force_qty"] = value
    assert PositionSizingConfig(**ps).force_qty == value


@pytest.mark.parametrize("value", [0, -1, True, False, 1.5, 1.0, "1"])
def test_config_refuses_anything_else(value) -> None:
    ps = _repo_position_sizing()
    ps["force_qty"] = value
    with pytest.raises(Exception) as exc:
        PositionSizingConfig(**ps)
    assert "force_qty" in str(exc.value)


def test_config_explicit_null_is_off() -> None:
    ps = _repo_position_sizing()
    ps["force_qty"] = None
    assert PositionSizingConfig(**ps).force_qty is None


# ── sizer ─────────────────────────────────────────────────────────────────────

def test_a_stock_the_concentration_rung_zeroes_is_sized_to_one() -> None:
    """Rs 1,200 share at Rs 9,992.80: floor(999.28 / 1200) = 0 -> today: rejected."""
    off = _sizer().calculate("SYM", "BUY", 1200.0, 1188.0, "INTRADAY", score_tier="HIGH")
    assert not off.success and off.qty == 0 and off.constraint == "CONCENTRATION", off
    on = _sizer(force_qty=1).calculate("SYM", "BUY", 1200.0, 1188.0, "INTRADAY", score_tier="HIGH")
    assert on.success and on.qty == 1 and on.constraint == "FORCE_QTY", on
    assert on.breakdown["qty_by_concentration"] == 0 and on.breakdown["force_qty"] == 1
    assert on.breakdown["tier_multiplier_mode"] == "FORCE_QTY"
    assert on.margin_required == pytest.approx(1200.0 / 5.0)
    assert on.risk_amount == pytest.approx(12.0)


def test_a_normally_sized_stock_is_also_forced_to_one() -> None:
    off = _sizer().calculate("SYM", "BUY", 100.0, 98.0, "INTRADAY", score_tier="HIGH")
    assert off.success and off.qty > 1, off
    on = _sizer(force_qty=1).calculate("SYM", "BUY", 100.0, 98.0, "INTRADAY", score_tier="HIGH")
    assert on.success and on.qty == 1 and on.constraint == "FORCE_QTY", on


def test_one_can_never_become_more_lot_two_is_below_min() -> None:
    r = _sizer(force_qty=1).calculate("SYM", "BUY", 100.0, 98.0, "INTRADAY", lot_size=2)
    assert not r.success and r.qty == 0 and r.constraint == "BELOW_MIN", r


@pytest.mark.parametrize("lot", [1, 2, 3, 5, 25, 75])
def test_forced_one_is_one_or_rejected_for_every_lot(lot) -> None:
    r = _sizer(force_qty=1).calculate("SYM", "SELL", 100.0, 102.0, "INTRADAY", lot_size=lot)
    assert r.qty in (0, 1) and (r.qty == 1) == (lot == 1), (lot, r)


def test_the_lot_rounding_still_applies_to_a_forced_quantity() -> None:
    """The tail runs for an override too: force 3 at lot 2 rounds DOWN to 2 (skew 33% < 50%).

    With force_qty=1 a bypassed rounding is invisible (BELOW_MIN still rejects lot >= 2),
    so this is the case that can tell whether rounding ran at all.
    """
    r = _sizer(force_qty=3, lot_skew_rejection_threshold=0.5).calculate(
        "SYM", "BUY", 100.0, 98.0, "INTRADAY", lot_size=2)
    assert r.success and r.qty == 2 and r.constraint == "FORCE_QTY", r


def test_the_position_value_cap_still_rejects() -> None:
    """0.50 x 9,992.80 = 4,996.40 -> a Rs 6,000 share is rejected even at 1."""
    log = _Log()
    r = _sizer(force_qty=1, log=log).calculate("SYM", "BUY", 6000.0, 5940.0, "INTRADAY")
    assert not r.success and r.constraint == "POSITION_VALUE_CAP", r
    assert any(c[0] == "CRITICAL" and c[1] == "position_sizer.position_value_cap_exceeded" for c in log.calls)


def test_the_sl_distance_guard_still_rejects() -> None:
    r = _sizer(force_qty=1).calculate("SYM", "BUY", 100.0, 99.99, "INTRADAY")
    assert not r.success and r.constraint == "INVALID_SL_DISTANCE", r


def test_a_zero_multiplier_does_not_skip_the_override() -> None:
    off = _sizer().calculate("SYM", "BUY", 100.0, 98.0, "INTRADAY", perf_weight=0.0)
    assert not off.success and off.constraint == "ZERO_MULTIPLIER", off
    on = _sizer(force_qty=1).calculate("SYM", "BUY", 100.0, 98.0, "INTRADAY", perf_weight=0.0)
    assert on.success and on.qty == 1, on


def test_delivery_bucket_is_forced_and_capped_on_its_own_pct() -> None:
    r = _sizer(force_qty=1).calculate("SYM", "BUY", 2000.0, 1900.0, "DELIVERY")
    assert r.success and r.qty == 1 and r.bucket == "positional", r
    assert r.margin_required == pytest.approx(2000.0)


def test_one_warning_per_call_naming_key_and_value() -> None:
    log = _Log()
    s = _sizer(force_qty=1, log=log)
    s.calculate("AAA", "BUY", 100.0, 98.0, "INTRADAY")
    s.calculate("BBB", "SELL", 200.0, 204.0, "INTRADAY")
    w = [c for c in log.calls if c[1] == "position_sizer.force_qty_override"]
    assert [c[0] for c in w] == ["WARNING", "WARNING"], log.calls
    assert [c[2]["symbol"] for c in w] == ["AAA", "BBB"]
    assert all(c[2]["config_key"] == "position_sizing.force_qty" and c[2]["force_qty"] == 1 for c in w)


def test_off_emits_no_override_warning() -> None:
    log = _Log()
    _sizer(log=log).calculate("AAA", "BUY", 100.0, 98.0, "INTRADAY")
    assert not any(c[1] == "position_sizer.force_qty_override" for c in log.calls)


@pytest.mark.parametrize("bad", [0, -1, True, 1.5, "1"])
def test_constructor_refuses_a_bad_value(bad) -> None:
    with pytest.raises(ValueError) as exc:
        _sizer(force_qty=bad)
    assert "force_qty" in str(exc.value)


def test_constructor_default_is_off() -> None:
    import inspect
    p = inspect.signature(PositionSizer.__init__).parameters["force_qty"]
    assert p.default is None


# ── wiring ────────────────────────────────────────────────────────────────────

def test_main_passes_force_qty_from_config_into_the_production_sizer() -> None:
    """The value must ARRIVE: a config key the constructor never receives proves nothing."""
    tree = ast.parse((_REPO / "main.py").read_text(encoding="utf-8"))
    sites = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "PositionSizer"]
    assert len(sites) == 1, f"expected ONE production PositionSizer(...) in main.py, found {len(sites)}"
    kw = {k.arg: k.value for k in sites[0].keywords}
    assert "force_qty" in kw, "main.py does not pass force_qty"
    v = kw["force_qty"]
    assert (isinstance(v, ast.Attribute) and v.attr == "force_qty"
            and isinstance(v.value, ast.Name) and v.value.id == "ps_cfg"), ast.dump(v)
    # control: the same walk sees a keyword that is certainly there
    assert "max_position_value_pct" in kw
