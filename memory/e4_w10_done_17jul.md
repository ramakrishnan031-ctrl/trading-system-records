---
name: e4-w10-done-17jul
description: "E4+W10 FIXED 17-Jul as ONE contract migration (pnl_delta=NET) on branch e4-w10-pnl-contract — LOCAL/UNPUSHED. DEPLOY AWAITS RAMA'S EXPLICIT RISK-POSTURE SIGN-OFF (the loss limit now trips LATER)."
metadata: 
  node_type: memory
  type: project
  originSessionId: b1aa742a-e0f9-46e6-9de8-800ed4bc60dd
---

**FIXED, LOCAL, UNPUSHED.** Branch `e4-w10-pnl-contract` @ **`ad34ee4`** (2 commits: `1f4509e` the
contract migration + `ad34ee4` a self-review fix; off `4c148fb`), schema v44 unchanged, **branch
never pushed** (`git ls-remote` empty). Report: `docs/audit/e4_w10_done_17jul2026.md`. Supersedes
the investigation [[e4-investigation-17jul]] (which stays valid as the *why*).

**FULL REGRESSION: `10 failed / 4835 passed / 4 skipped`, rc=1, 12m57s — 0 ATTRIBUTABLE, PROVEN.**
The 10 are the known **time-gated PC-env** set (10 in-window; the 11th = FIX-189 clock-guard, only
after 16:00 IST — this ran ~11:00). **2 of the failing suites (`test_fix181`, `test_main`) touch
files this change edits**, so it was NOT taken on trust: re-ran those 4 suites on the TRUE
pre-change tree ⇒ `comm -23` = **0 new**, `diff` = **IDENTICAL**.

**⚠️ PROCESS TRAP HIT (worth remembering): `git checkout HEAD -- <files>` during the attribution
step SILENTLY WIPED uncommitted edits** to `order_reconciler.py` (the fail-open fix). Caught only
because `git status` didn't list a file it should have. **Commit BEFORE any checkout-based
attribution**, and re-verify the file afterwards.

## ⛔ THE GATE — deploy needs Rama's EXPLICIT sign-off
**The daily-loss limit now fires on the TRUE net ⇒ on typical days it trips LATER than today's
double-counted figure.** Correct, but a **live risk-posture change**. Deploy = Rama **flattens
manually first** (no flatten mechanism was built), then push + tag. Rollback = revert the one
commit (schema-free).

## THE CONTRACT (now stated in code)
**`fm_ledger.pnl_delta` is NET; `costs` is observability-only and is NEVER re-subtracted.**
Reader `state_store.get_daily_realized_net_pnl` → `SUM(pnl_delta)`. The 3 backstop paths
(reconciler CHECK1 + CHECK4-partial, cnc_gtt_monitor) now take the **shared mode-agnostic
CostCalculator** (`main.py:1786`, pre-mode-branch ⇒ parity free) via new helper
**`broker/cost_calculator.round_trip_costs_or_zero`** — **fail-OPEN**: a cost-calc failure
degrades to 0.0 **loudly**, never blocks a capital release (blocking would strand margin in
`used` all session). `release_used` now persists `trade_id` (was 155/155 NULL).

## ⭐ 3 THINGS THE INSTRUCTION GOT WRONG — verified, then NOT implemented
Mirror of [[feedback-verify-the-finding-premise]]:
1. **`reset_daily_pnl` needed NO change** — it reads the reader and writes `−old_pnl`, so it is in
   lockstep **by construction** under either contract. Editing it would have BROKEN it.
2. **Rehydrate/restart already followed NET** — `release_used` credits `pnl` and stores that same
   number; rehydrate replays `pnl_delta` directly. Restart==continuous already. The **M-C1 seed**
   (`main.py:2170`) subtracts Σ over the EXACT rows Phase 2 re-adds ⇒ **contract-invariant**.
   Both pinned by test, not changed.
3. **No `ProductResolver` needed** — `product` is already in scope at both reconciler call sites
   (`:1082`/`:1873` derive `intent` FROM it). GTT path is CNC by construction.

## ⭐ THE CONSUMER THE INVESTIGATION MISSED (real blast-radius extension)
**CHECK1 + GTT also write `trades.net_pnl` FROM `release_result.pnl_delta`**, via
`record_manual_close_financials` / `record_gtt_close_financials` which **hardcoded
`gross_pnl=net_pnl, charges=0.0`**. Honest only while costs were 0 — with real costs those rows
would silently claim "gross==net, charges==0". **Both writers gained `gross_pnl` and moved in the
same commit.** Preserves `PATHS.md:447`'s `Σ pnl_delta == Σ trades.net_pnl` (both sides move
together).

## PROOF
**RED-on-old: 14 failed / 5 passed, rc=1** on the TRUE pre-change tree (`git checkout 4c148fb --`
+ grep-confirm, **never stash**) vs **19 passed** fixed. Cleanest: reader returns **−140.0** for a
NET row of −100/costs 40, and `CapitalSnapshot.daily_realized_pnl=−140.0` ⇒ **both control halves
proven fed the double-subtract**. The 5 passing on old are contract-agnostic guards + new-helper
policy tests (correctly not RED-on-old). Tests: `tests/unit/test_e4_w10_pnl_contract.py` (19).
**Only ONE pre-existing test failed**: `test_migrations.py:234` 450.0→500.0 — a deliberate
contract inversion (cf. M-C6/FIX-133). `test_fund_manager.py:2318` +
`test_mo2_check4_partial_capital.py` did **NOT** fail (zero-cost fixtures ⇒ contract-agnostic).

## LIVE-LEDGER FACT (verified `mode=ro`) — live DB is `data_store/trading_system.db`
Only **RELEASE_USED** (155 rows, Σpnl −96.45, Σcosts **60.24**) and **RESET_PNL** (22, +147.98)
carry `pnl_delta`; the other 1983 rows are 0.0 ⇒ the reader needs **no entry_type filter**.
(`data/trading_system.db` is a **stale May-18 artifact** — no fm_ledger. Don't confuse them.)

## HISTORICAL GAP — NOT backfillable, and bounded
The 36 `costs=0` rows were written gross; their real costs were never computed ⇒ any backfill
would be fabrication. **Bounded**: the control is per-day and `RESET_PNL` zeroes it nightly ⇒ only
today's rows matter, and from the first boot on the new code every row is NET. Reporting-history
artifact, not a live-control one. **Edge**: deploying AFTER today's EOD reset makes the new reader
read that day as `Σcosts` (small positive ⇒ no breach ⇒ harmless).

Links: [[e4-investigation-17jul]] [[capital-operational-note]] [[dual-daily-loss-mechanism]]
[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]] [[feedback-paper-live-parity]]
