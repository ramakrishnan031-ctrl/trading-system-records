---
name: q9-batch5-post-restart-18jul
description: "18-Jul Q9 batch 5 DONE — post-restart capital restoration wired-proven. The day's realized P&L SURVIVES by construction (never in memory) and kill state survives via KillSwitch.__init__ -> _load_state_from_store (KS3, NOT clear_stale_state). ⚠️ Monday's boot exercises only the TRIVIAL case; the LIVE seed has NO integration coverage. Q9 IS COMPLETE."
metadata: 
  node_type: memory
  type: project
  originSessionId: 53e59a7c-edb5-400e-9b3e-6d5981ddd5a2
  modified: 2026-07-18T15:18:40.625Z
---

**♻️✅ Q9 BATCH 5 — POST-RESTART CAPITAL RESTORATION IS WIRED. 18-Jul-2026.**
Report `docs/audit/q9_batch5_post_restart_capital_18jul2026.md`. **Tag `deploy-18jul-q9-batch5`→`a9758b3`; PC == VM == `230dd32`.** **TEST-ONLY — zero production
files.** **⇒ Q9 IS COMPLETE** except the coverage-matrix metadata back-fill.

## THE FOUR FAILURE MODES — ALL CLEAN, no STOP-AND-REPORT
* **(a) THE DAY'S REALIZED P&L SURVIVES — BY CONSTRUCTION.** `FIX-051` removed the in-memory
  `_daily_pnl`; `get_daily_realized_net_pnl` **recomputes from `fm_ledger` on every read**, and
  **BOTH** daily-loss halves read it that way (`fund_manager.py:1279` gate, `:1507` snapshot).
  **There is nothing to lose.** Runtime: `-1104.80` → `-1104.80` identical. Also proven the limit
  still **ENFORCES** on the restored value (`REJECTED_DAILY_LOSS` *specifically*, + the negative
  half). ⇒ **a restart does NOT hand the system a fresh loss budget.**
* **(b) KILL STATE SURVIVES — but NOT via `clear_stale_state`.** ⚠️ That function returns early on
  `_state == INACTIVE`, which is exactly what a fresh process has. **The restorer is
  `KillSwitch.__init__` → `_load_state_from_store()` (`kill_switch.py:250`, KS3 "Audit Issue #18
  fix")**. Same-day kills persist; prior-day auto-clear (Rama's 20-Jun headless decision). BOTH
  halves asserted + the restored kill still BLOCKS a placement (empty broker call record).
  **📌 I nearly filed a false LIVE finding here — checking line 250 inverted the premise.**
* **(c) Reservations/used:** OPEN/PARTIAL replayed; **a `PENDING_FILL` reservation is DELIBERATELY
  NOT restored** (`get_all_open_trades()` = OPEN/PARTIAL only). Correct + safer: the DB cannot know
  if the broker filled it, so capital is **RETURNED to available** and `main.py:3207`'s synchronous
  `reconcile_once()` adopts-or-fails against **BROKER TRUTH**. Measured: reserved 2520→0,
  avail +2520, **used 4000 unchanged, total unchanged**.
* **(d) IDEMPOTENT at the level that exists:** two full BOOT CYCLES ⇒ identical state (systemd
  case). **Within ONE instance it is NOT** — `initialize()` has an H-4 double-call guard,
  `rehydrate` has none (used 4000→8000). **UNREACHABLE** (one call site `main.py:2286`, no retry
  loop, a restart is a new process). Pinned by a test asserting the single call site.

## THE RESTORE MAP (boot order)
`clear_stale_state` (`main.py:1768`) → seed (**PAPER** `paper_capital` `:2243` / **LIVE**
`broker.get_margins().net − today_realized_pnl_carryover()` `:2255`, M-C1) → `initialize()` `:2259`
→ **`rehydrate_from_open_trades()` `:2286`** (Phase 1 open-trade replay `:1685` · Phase 2 today's
`RELEASE_USED` P&L carryover `:1703` · Phase 3 invariant ONCE `:1718` → `CapitalStateInconsistent`
⇒ **exit 3, fail-closed**) → paper adapter re-sync (FIX-156) → **`reconcile_once()` `:3207`**.
**⚠️ Phase 2 applies `SUM(pnl_delta)` to `_total`; the READER returns `SUM(pnl_delta) − SUM(costs)`
— they differ by exactly the E4/W10 double-subtraction (observed −1052.40 vs −1104.80). DO NOT
CONFLATE.**

## ⚠️⚠️ TWO THINGS FOR RAMA
* **MONDAY 20-Jul 08:15 EXERCISES ONLY THE TRIVIAL CASE.** Flat book + fresh day ⇒ **Phase 1 = 0
  replays, Phase 2 = 0 P&L rows ⇒ rehydrate is a NO-OP.** It proves the boot doesn't crash on the
  restore path, nothing more. **STILL UNPROVEN IN PRODUCTION after Monday:** Phase 1 replay of a
  real open position · Phase 2 P&L carryover · the M-C1 live-seed cancellation · same-day-kill
  survival. All need a **MID-DAY restart with live state**.
* **PRODUCTION RUNS `--mode live`, BUT THE WIRED FIXTURE IS PAPER** ⇒ **the LIVE seed
  (`broker.net − carryover`) has NO integration coverage**, only unit
  (`tests/unit/test_mc1_live_seed_rehydrate.py`). Removing the M-C1 subtraction would silently
  **inflate live reservable capital** on a warm restart and no wired test would notice ⇒ **now
  PINNED STRUCTURALLY** (fails if the subtraction goes, or if Phase 2 and the carryover stop
  sharing `_today_release_used_pnl_rows`). Verified to bite.

## ⭐ BITE PROOF — and a VACUOUS HARNESS OF MY OWN, caught for the 2nd batch running
5 value-shaped plants. **A2 is the meaningful one:** carry **90%** of the P&L ⇒ internally
consistent, global identity intact ⇒ **`CapitalInvariantViolation` = 0 AND `CapitalStateInconsistent`
= 0** yet the test fails naming it: `TOTAL not restored: 490952.73 -> 491857.46`. **That is the
E4/W10 class.**
**⚠️⚠️ PLANT C EXPOSED MY OWN VACUOUS TEST:** the first `_restart()` rebuilt the FundManager but
**REUSED the fixture's KillSwitch**. `is_active()` reads only in-memory `_state`, so every kill
assertion checked a flag the test never restored — **it would have passed with the KS3 load
deleted**. Fixed by rebuilding the KillSwitch inside `_restart()`; Plant C now fails 3 tests.
**📌 Batch 4 = 2 gaps found by planting; batch 5 = 1 more. Planting is NOT a formality.**

## PARITY — one path, two seeds (NOT the P1 /health shape)
`rehydrate` has **no** `paper_mode`/`is_paper`/`live_mode` branch; both modes call the same
`initialize()` + `rehydrate_from_open_trades()`. **Only the SEED differs.** The live-only carryover
subtraction exists so live's seed cancels Phase 2's re-addition **by construction** (they share ONE
row-selection helper `_today_release_used_pnl_rows` `:1757`); the docstring names **paper as "the
parity reference"**. Pinned structurally.

## C-2 — BATCH 3's E4/W10 EVIDENCE RE-VERIFIED IN A **SEEDED** WORKTREE: UNCHANGED ✅
`reader(-1052.4000) − truth(-1052.4000) = **0.0000**`, costs 52.40; **2 failed / 4 passed** on
`ad34ee4` (control on main: **5 passed, 1 xfailed — XFAIL not XPASS**). Identical to the original
bare-worktree run. **Why the defective env didn't matter:** the missing `config/instruments.csv`
only breaks `main.py`'s InstrumentCache, which **boot-path UNIT tests** build — the E4/W10 evidence
runs on the `wired_system` fixture over a `tmp_path` DB and never touches it. Read-only; nothing
merged; worktree removed. **⇒ the evidence under Rama's pending decision STANDS.**
**C-1 done:** the stale **7.34×** in batch 4 §10 → **9.54×** (authoritative registry).

## Related
[[q9-batch4-sizing-reachability-18jul]] · [[q9-batch3-capital-invariant-18jul]] ·
[[q9-batch2-killswitch-toctou-18jul]] · [[q9-batch1-daily-loss-wired-18jul]] ·
[[killswitch-autoclear-prior-day]] · [[e4-w10-done-17jul]] · [[capital-operational-note]] ·
[[feedback-verify-the-finding-premise]].
