---
name: consecutive-losses-gate-wired-19jul
description: "Q9 completes at 22/22 — layer 14 (consecutive-losses RE10) wired; there is no counter, so a win resets it and a restart is not a bypass; reachable but never yet fired; plus the NTP assertion that was an 18% coin flip."
metadata: 
  node_type: memory
  type: project
  originSessionId: 106a4d20-abb3-49c1-bdf3-ab5c0f4839d0
  modified: 2026-07-19T06:30:08.375Z
---

**DEPLOYED 19-Jul-2026 ~02:3x IST (off-market, system DOWN).** PC == origin == VM bare ==
`7319d06`; tag `deploy-19jul-consecutive-losses` → `d271525`; delta tag..HEAD = markdown only.
Schema v44 unchanged. **TEST-ONLY** — `git diff --name-only 1fc95c1..d271525` = 3 files, **all
under `tests/`**. Rollback = revert, nothing to unwind.

## ⭐ THERE IS NO COUNTER — the finding that shaped everything

The streak is **RECOMPUTED on every `approve()`** from `recent_trade_pnls(max_consec+1, today)`
(`state_store.py:851`) and `_count_trailing_losses` (`risk_engine.py:250-251, 674`). It is never
incremented and never held in memory — `core/schema.sql:459-460` confirms the stored
`consecutive_losses` column "was never written". Three consequences, each **proven, not described**:

**1. WHAT RESETS IT — and this is operator-relevant, not bookkeeping.**
   (a) **Any non-loss close.** Only the *trailing* run is counted, and RE10 defines a loss as
   `net_pnl < -1e-6`, so a **breakeven breaks the streak too**.
   (b) **A new day** — FIX-183 scopes the query to `SUBSTR(exit_time,1,10)`. Its comment records
   the outage that forced it: a cross-day streak was a **DEADLOCK**, because breaking it needs a
   winning trade and the block makes one impossible.
   ⇒ **The halt is NOT for the rest of the day. ONE winning close lifts it immediately.** That is
   the good version of the two systems Rama could have owned.

**2. IT SURVIVES A RESTART BY CONSTRUCTION** — nothing in memory to lose. Same shape as batch 5's
   daily P&L (FIX-051). **A restart is NOT a bypass.** [[q9-batch5-post-restart-18jul]]

**3. It is read at ENTRY but only changes at EXIT**, so in-flight positions are never
   retro-blocked. Not a defect — and it is why production shows streaks *longer* than the threshold.

## ⭐ REACHABILITY — a category of its own

Not UNREACHABLE like batch 4's guards (dead by algebra), and not routinely binding either.
Measured against production, not argued:

- **The precondition has been met on 3 of 21 trading days** — streaks of **5, 5, 6**
  (2026-06-24, 07-07, 07-08).
- **Yet `REJECTED_CONSECUTIVE_LOSSES` = 0 across ALL 32,928 signals.**

Both halves were checked before concluding, because a streak of 6 against a threshold of 4 looks
like a bypass:

1. **No bypass.** On 2026-07-08 the streak reached 4 at exit **10:22:23**, but **all six trades had
   been ENTERED by 10:14:19** — every one before the threshold existed.
2. **Why it never fired.** All **63** signals arriving after 10:22:23 were
   `SKIPPED_QUOTE_UNAVAILABLE` — they died upstream of the risk engine, so it was never consulted.

> **⚠️ CORRECTED 19-Jul (census claim 1):** point 2's reason is **survivorship bias** — 07-08 is the pre-09-Jul pruned era (`REJECTED_*` deleted, `SKIPPED_*` kept), so acceptance actually *accelerated* after 10:22 (peak 1,462/hr; 63 = 1.21%, 6th-lowest of 21 days). **The verdict + point 1 STAND** (entry-vs-exit recomputation, verified separately; the census *strengthens* "reachable" — the gate is consulted ~975×/day). [[signal-mortality-census-19jul]]

⇒ **LIVE, correctly configured, precondition demonstrably met, never yet the binding rejection.**

## ⚠️ The brief's collision premise was INVERTED

RE5 order is `... 5 DAILY_TRADES · 6 CONSECUTIVE_LOSSES · 7 DAILY_LOSS`, so the daily-loss **GATE**
is checked **AFTER** this one and **cannot mask it at all**. The real hazard is the **post-close
breach** — a *different* mechanism with its own key (`FundManager(daily_loss_limit_pct=0.02)` =
₹10,000, vs the gate's 5% = ₹25,000) — arming a **SOFT KILL** that then fires `KILL_SWITCH` at
check 1 and produces a rejection that looks like success. See [[dual-daily-loss-mechanism]].

The shared `_drive_close` defaults to **−9,000/close**; four would blow through both limits. This
batch drives **−1,000/close** and **asserts** the sizing stays inside both rather than trusting the
arithmetic. `_assert_no_earlier_gate_can_mask()` re-checks all five earlier gates at every probe.

## 🔧 The measuring instrument was bent by 18% (fixed FIRST, deliberately)

`test_fix129_ntp_check`'s `drift_sec >= 1.0` / `>= 3.0` were **not flakes but wrong assertions**.
`check_ntp_sync` (`utils/startup_checks.py:534-548`) computes `drift = offset − elapsed`, which is
**always ≤ the injected offset**, so `>= offset` can only pass when the error terms vanish.

| Assertion | Failures / 100,000 |
|---|---|
| old `>= 1.0` | **17,940 (17.94%)** |
| old `>= 3.0` | **18,324 (18.32%)** |
| fixed `approx(abs=0.05)` | **0** (+ 40 consecutive pytest runs clean) |

**⭐ This retro-explains the M-C1 batch's discarded regression pair** — at ~18% each, base catching
one and mine the other is the expected outcome, not a coincidence.
[[feedback-regression-must-not-cross-midnight]]

**📌 THE RULE: an exact comparison on a small delta derived from a LARGE EPOCH is float64-unsafe.**
At epoch ~1.784e9 one ULP is 2⁻²² = 2.384e-07. **But the ULP only explains the unsafety — it must
NOT size the tolerance.** Measured: elapsed between the two clock reads is max 9.1e-06, ~38× the
ULP, and the **Windows scheduler quantum (~15.6 ms)** dwarfs both. Hence **50 ms**, still **20×
below** the 1.0 s margin to the nearest decision boundary, with two permanent guards proving it
cannot blur a decision. **🔴 It failed on the VM too** — a genuine cross-platform defect.
**THE REGRESSION BASELINE IS NOW 14, down from 16.**

## ⭐ A third harness hole — caught ONLY by the full-suite regression

The first MINE run carried **one attributable failure** that **passed in isolation, passed under
`-k`, and passed across all 103 `tests/integration` tests**. Cause: the fixture default
`paper_auto_fill_delay_sec=0.05` makes the paper adapter fill a placed order 50 ms later
**asynchronously**, racing the explicit fills these tests publish to control each close's **sign**.
Under full-suite load the adapter won and the P&L flipped. Every other Q9 batch already sets
`60.0`; this module had omitted it.

> **📌 This is exactly why "STOP on any NEW failure" is the rule.** Re-running until it looked green
> would have "worked" — it passes in isolation every time. The failure was real and the cause was in
> my harness.

Two more, same batch: my own parity guard matched `"live"` inside **`"deLIVEry"`** and failed on
correct code; and `_probe_signal_status` could settle on **`"PASSED"`**, which is the *screening*
verdict (`secondary_screener.py:353,512`) landing **before** the risk engine rules — making any
positive assertion on a specific rejection a race. Callers asserting a risk verdict now pass
`ignore={"PASSED"}`.

**⇒ Planting/regression has now found holes in the TESTS rather than in production in 6 instances
across 5 batches.** [[verify-check-the-rc-not-the-output]]

## Bite proof

Neutering the comparison (`consec >= max_consec + 100`) → **3 failures** naming the gate and the
count. Breaking the counter (`_count_trailing_losses` → 0) → **9 failures**, with the anti-vacuity
assertion catching it first (*"streak is 0, not 4 — a rejection here would be for some other
reason"*). **`CapitalInvariantViolation` = 0 and `CapitalStateInconsistent` = 0** in both.

## ✅ Pre-Monday VM check (read-only) — nothing blocks the 08:15 boot

All **94** modules `main.py` imports resolve on the deployed tree (0 failures).
`reports/signal_status.py` + `daily_report.py` are **NOT on the boot path** (cron-only 16:05) and
import cleanly anyway. Crontab correct; `15 8 * * 1-5 auto_refresh_token` present; nothing untoward
before 08:15. `trading-system.service` **enabled/loaded**, last `ExecMainStatus=0`; token file
**absent** as designed; disk 25%. One stale `/tmp/trading-system.lock` was **my own artefact** from
running the instance-lock tests on the VM (PID 1491115 dead, no flock holder, port 5001 free ⇒
could not have blocked a boot) — removed.

Regression: BASE 5030 (16F) vs MINE 5045 (14F), `comm` mine-only EMPTY, base-only = exactly the 2
NTP tests, `xfailed=1/XPASS=0`. **22 tests pass ON THE VM**; live DB mtime unchanged either side.
Report `docs/audit/consecutive_losses_gate_wired_19jul2026.md`. [[q9-live-seed-mc1-wired-19jul]]
