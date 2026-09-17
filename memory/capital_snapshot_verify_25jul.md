---
name: capital-snapshot-verify-25jul
description: §B capital_snapshot plan VERIFIED read-only 25-Jul. WARN does NOT fire on a normal boot (preflight 09:14 >> INIT 08:15). Preflight is ALERT-ONLY. 🔴 INIT is NOT unique per day and db_reader.opening_capital ALREADY doubles (10/30 dates).
metadata: 
  node_type: memory
  type: project
  originSessionId: 94025df9-7b5d-4673-aa44-14ccbe9d87b3
  modified: 2026-07-25T03:29:44.761Z
---

**capital_snapshot reader-redirect (§B) — PLAN VERIFIED, NOTHING BUILT (25-Jul, read-only; DB `mode=ro&immutable=1`, zero-trace confirmed).**

**C2 ⭐ THE ONE THAT DECIDED THE BUILD — the planned WARN does NOT fire on a normal boot.** `preflight_phase_b` = `14 9 * * 1-5` (**09:14**, `market_day_only:true`); the INIT row is written at **08:15:2x–08:15:36** (MEASURED, last 5 trading days). ~59 min of margin. On the restart path too: `main.py:2375 fund_manager.initialize()` precedes `main.py:3481 run_on_demand_if_missed()`. The only case that WOULD warn — no INIT row by 09:14 — means the app never booted, which is a TRUE alarm (the S4 shape). **The B1 trap does not apply.**

**C3 — preflight is ALERT-ONLY; a CRITICAL cannot block the boot.** `preflight/__init__.py:11` ("pre-flight is the eyes, Rama is the gate") · `orchestrator.py:234-236` returns 0 even with CRITICAL findings · `cron_registry.yaml:207` `critical:false`. Structurally it could not block anyway — separate cron process an hour after boot. **No back door:** `FundManagerBalanceCheck` never sets `auto_fixable` (defaults False ⇒ `fix()` never called), and the sentinel's only two consumers (`cron_officer.py:480`, `cron_report_render.py:67`) are reporting. ⇒ **the `<=0/NaN → CRITICAL` branch adds NO new way to lose a trading day.**

**C4 🔴 INIT is NOT unique per day — and the exposure is ALREADY LIVE.** H-4's guard is the in-memory per-process `self._initialized`; `state_store.py:2527` says it outright — *"one INIT row per process start"*. A mid-day restart writes a 2nd INIT row for the same date. MEASURED: **10 of 30 INIT dates have >1 row.** **2026-07-21 (the forced 11:57 restart): n=2, SUM=19,716.03 vs a true opening of ~Rs 9,857.30 — a clean 2×.**
⇒ **`db_reader.opening_capital:317` ALREADY uses `SUM(...)`**, so the dashboard read double on 21-Jul and every percentage against it was half. **Pre-existing defect in shipped code — reported, NOT fixed (one fix per commit).**
⇒ **The correct accessor exists and is restart-safe: `state_store.get_opening_capital()` (`:2539-2546`) takes `ORDER BY ts ASC LIMIT 1` — the FIRST INIT row — and returns `None` when absent, which is exactly the WARN signal.** **§B must use it, NOT SUM.**

**C5 ⚠️ the anti-dup premise is partly FALSE — `fm_ledger` does NOT hold those three values.** Its columns are `ledger_id, ts, entry_type, amount, bucket, balance_before, balance_after, signal_id, reservation_id, reason, session_id, direction, trade_id, margin_delta, pnl_delta, costs` — **deltas, not levels**. `margin_used`/`realized_pnl_today`/`cash_floor` are **`capital_snapshot`** columns. Correct statement: every value is DERIVABLE, but **`margin_used` comes from `trades` (`SUM(margin_reserved)` over OPEN/PARTIAL/PENDING_FILL), not `fm_ledger`**. Existing accessors to reuse: `get_opening_capital()` + `get_daily_realized_net_pnl()`.

**⚠️ FLAGGED — `cash_floor` ≠ total capital.** `db_reader:329` computes `total = cash_floor + margin_used + margin_reserved`, so `cash_floor` is the free-cash residual. `FundManagerBalanceCheck` asserts `cash_floor > 0` (`engine.py:105-106`); redirecting it to opening capital silently changes the check's MEANING from "is there free cash?" to "did the day seed a positive opening?" and it stops detecting a fully-deployed book. Belongs in the §B commit message and at the site — same class as the plan's own B4 note.

**C1 — the 3 read sites are complete** (grepped): `preflight/checks/engine.py:94` · `healthcheck_server.py:187` · `db_reader.py:325`+`:337`. Two near-misses dismissed: `eod_broker_reconcile.py:441 _local_capital_snapshot` reads **fm_ledger** (a name, not a read site); `backup_restore_drill.py:48` is a table-name list.

⛔ **Nothing built. B4/B5/B6 still owed by the build.** Report `docs/audit/capital_snapshot_verify_2026-07-25.md`. [[fixation-batch-24jul-handoff]]
