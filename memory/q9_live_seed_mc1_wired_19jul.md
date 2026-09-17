---
name: q9-live-seed-mc1-wired-19jul
description: "Q9 closes — the LIVE capital seed (M-C1) cancellation is wired and bite-proven; 21/22 layers wired, 15 reachable; plus the fifth permanent rule (a regression run must not cross midnight) and a baseline that moved 12 to 16."
metadata: 
  node_type: memory
  type: project
  originSessionId: 106a4d20-abb3-49c1-bdf3-ab5c0f4839d0
  modified: 2026-07-21T08:28:46.999Z
---

**DEPLOYED 19-Jul-2026 ~00:5x IST (off-market, system DOWN).** PC == origin == VM bare ==
`1fc95c1`; tag `deploy-19jul-q9-live-seed` → `abf276a`; delta tag..HEAD = markdown only.
Schema v44 unchanged. **TEST-ONLY** — the commit touches ONE file under `tests/integration/`,
nothing outside `tests/`, so there is **zero production impact before Monday's boot**.
Rollback = `git revert abf276a`, nothing to unwind.

## What the gap was

Every wired test in Q9 batches 1–5 ran the `paper_mode=True` fixture while production runs
`--mode live`. The parity claim for the whole programme was **structural, not tested**, and it
stopped exactly where the two modes genuinely diverge — the seed.

- PAPER `main.py:2243` — static `paper_capital`, correctly excludes today's P&L.
- LIVE `main.py:2255` — `broker.get_margins().net − fund_manager.today_realized_pnl_carryover()`.

The broker's `net` **already includes** today's realized P&L; rehydrate Phase 2
(`fund_manager.py:1703-1711`) then **re-adds** it. Without the subtraction, today's P&L is counted
twice and **live reservable capital silently inflates on a warm restart** — the system would trade
on capital it does not have. Both sides sum `pnl_delta` from the **shared**
`_today_release_used_pnl_rows` (`:1757`), so they cancel to `broker.net` by construction.

**Measured:** `_total` lands on `broker.net` within 5.8e-11. Remove the subtraction and it lands
**18,094.54 high — exactly the carryover**, counted twice.

## The three things worth remembering

**1. The cancellation is CONTRACT-INDEPENDENT ⇒ it survives E4/W10.** `net − Σ + Σ = net` holds
whatever `pnl_delta` means, because both sides sum the same field from the same rows. The
daily-loss **reader** — the quantity E4/W10 changes — is ~~not involved at all~~ **[⚠️ CORRECTED 20-Jul: FALSE — the reader IS called on the seed/rehydrate path (`fund_manager.py:1760`); it is absent only from the cancellation ALGEBRA, which cancels because both sides sum the SAME rows. See [[mc1-live-seed-rederivation-20jul]] / `mc1_live_seed_rederivation_20jul2026.md`.]** in the cancellation (reader −18,189.08 vs
carryover −18,094.54; the −94.54 difference is exactly `SUM(costs)`). So E4/W10 can land without
disturbing live seeding. See [[e4-w10-done-17jul]].

**2. No test can reach a real broker, and no live-mode fixture was built.** The live seed needs
exactly one number, so a 12-line local `_StubBroker` supplies it — parameterising `wired_system`
into live mode would have put adapter construction and credential loading one refactor away from a
test. `TestNoBrokerReachable` pins the whole tree: constructing `KiteConnect` or reading
`ZERODHA_*` fails; `from kiteconnect import exceptions` (which the adapter tests need) does not.
The first version of that guard was **over-broad** and flagged 7 legitimate exception imports.

**3. HONEST SCOPE — the seed expression is replicated, not executed.** The two lines at
`main.py:2255-2258` are **inline in `main()` with no function boundary**, so no test can invoke
them without running `main()` — which in live mode is precisely what must never happen. The
expression stays under batch 5's structural regex pin. What the tests drive is real and call-count
proven: `today_realized_pnl_carryover` · `_today_release_used_pnl_rows` (**called exactly 2×, one
per side**) · `initialize` · `rehydrate_from_open_trades`. No claim is made that the real live-seed
path executes end-to-end, because it does not.

## Q9 final tally

**21 of 22 layers WIRED · 15 REACHABLE** under current production config.
🔴 **The one NOT closed: layer 14, the consecutive-losses gate (RE10) — still UNIT-ONLY.** Its gate
ORDER is proven (RE5 checks `CONSECUTIVE_LOSSES` before `DAILY_LOSS`), but its enforcing branch has
no wired positive. It needs ≥4 consecutive losing closes, which collides with the daily-loss limit
and deserves its own design — deliberately not smuggled into this batch.

**⚠️ Monday 20-Jul 08:15 exercises only the TRIVIAL case:** a cold boot on a flat book ⇒ Phase 1
replays 0 trades, Phase 2 carries 0 rows, carryover = 0, the subtraction is a no-op, rehydrate is a
NO-OP. **The cancellation this batch proves will not have run in production.** Still unproven in
production, all needing a mid-day restart with live state: Phase 1 replay of a real open position ·
Phase 2 P&L carryover · **the M-C1 cancellation with a non-zero carryover** · same-day-kill
survival. And the first live HARD_KILL is still M-C8's real test. See
[[q9-batch5-post-restart-18jul]] and [[q9-money-path-coverage-18jul]].

## 📌 THE FIFTH PERMANENT RULE — a regression run must not cross midnight

"Base and mine in the SAME TIME WINDOW" is **necessary but not sufficient**. The first base/mine
pair here was **discarded**: MINE ran 23:30–23:56, BASE 23:57–00:13, and the comparison returned
**both `comm` directions non-empty** — impossible for a test-only file addition (a new test file
cannot make `test_risk_engine::test_consecutive_losses_at_limit` *pass*).

Cause, verified in source rather than assumed: `_TODAY = now_ist().date().isoformat()` is captured
at module **import (collection)** time (`tests/unit/test_risk_engine.py:49`,
`tests/unit/test_phase3_delivery_caps_conditional_capital.py:35`) while the engine computes the
date at **execution** time. A run that collects on one date and executes on the next reads its own
seeded trades as *yesterday's*.

**At ~15 min/run, any regression started after ~23:15 IST is unsafe.** Same family as the
git-ignored-`instruments.csv` masking rule: an environmental asymmetry that corrupts attribution
**silently** instead of announcing itself. Joins the other four rules in
`docs/SYSTEM_MAP.md`. Redone in one window (Sun 00:15–00:44): **BASE 5017 vs MINE 5030, `comm` both
directions EMPTY, zero attributable, xfailed=1/XPASS=0.**

## ⚠️ The regression baseline moved 12 → 16 — and one half is NOT PC-only

All four are present in **BASE**, so attribution was unaffected, but the next batch inherits them.

- **`test_fix129_ntp_check` ×2 — 🔴 FAILS ON THE VM TOO, not a PC-env item.** Pure float64
  precision: `drift_sec` lands exactly one half-ULP below the bound (`assert 0.9999997615814209 >=
  1.0`, `2.999999761581421 >= 3.0`). At epoch ≈1.78e9 the ULP is ≈4.8e-7, so whether `local + 1.0`
  rounds up or down is decided by the clock's low bits — **a coin flip per run** (the discarded
  pair caught one of the pair in base and the *other* in mine). The fetcher is a **stub**: no
  network, no real NTP. **Fix is `pytest.approx` — RAMA'S CALL, deliberately not done in a
  test-only M-C1 batch.**
- **`test_instance_lock` ×2 — PC-only** (all pass on the VM): stale
  `%TEMP%\trading-system.lock` naming **PID 8708, which is not running**; port 5001 free.

## ⚡ The power outage, and why it mattered

The build session was ended by a power cut (Ctrl+C, then unclean shutdown) **after** `abf276a` was
committed but **before** the regression ran. Two casualties, both repaired before any measurement:

1. `tests/integration/test_q9_live_seed_mc1_wired.py` was **deleted from the working tree** while
   the git object survived. Restored with `git checkout --`; verified **byte-identical** to the
   commit.
2. The venv **lost `pyotp` and `waitress`**, both pinned in `requirements.txt`. Not cosmetic:
   `tests/unit/test_gui_secret_key.py` imports `ops_dashboard.backend.app` → `pyotp`, so
   collection **aborted for the entire suite**. Reinstalling at pinned versions returned base
   collection to exactly **5017** — proof the repair restored the declared state rather than
   changing it.

**The restored file was re-proven to BITE before it was trusted** — planting `carryover → 0.0`
failed 7 tests with the anti-vacuity gate firing first (`assert 0.0 != 0.0`), message matching the
report verbatim. This is [[verify-check-the-rc-not-the-output]] applied to a recovered artefact:
a file restored from git is not *known good* until it has been seen to fail.

## Bite proof (from the build session, re-verified after restore)

The meaningful plant makes the two sides compute rows **independently** — the §A2 silent-drift
mode. Every value stays plausible and internally consistent, so **`CapitalInvariantViolation` and
`CapitalStateInconsistent` both fired 0 times** (production's own runtime guards see nothing), yet
the cross-check reports *"LIVE SEED DID NOT CANCEL: `_total`=470691.7238 but
broker.net=471234.5600"*. That is the E4/W10 bug class, in the live seed.
See [[feedback-live-vs-latent-findings]].
