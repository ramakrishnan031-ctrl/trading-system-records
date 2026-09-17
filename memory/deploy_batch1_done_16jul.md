---
name: deploy-batch1-done-16jul
description: "16/17-Jul-2026 ~23:55 IST — BATCH-1 DEPLOYED. PC main == VM bare == eb9cffa, 100% SYNCED, zero unpushed. Carries the E4 capital finding + P3-s14 to the LOOP queue."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**✅🗂️🚀 BATCH-1 IS DEPLOYED — 16-Jul-2026 23:54–23:55 IST, off-market.**
**🔝 PC `main` == VM bare == `eb9cffa` — 100% SYNCED, ZERO unpushed (not even docs).** Tag
`deploy-17jul-batch1` → `eb9cffa` **IS the deployed HEAD**, so the code-identity delta is not merely
markdown-only — it is **EMPTY**. Schema **v44 unchanged, no migration**; integrity/FK clean; services healthy;
no code changed during the deploy. Backup `data_store/backups/pre_deploy_batch1.db` (357MB, integrity ok, 361
trades). Report `docs/audit/deploy_done_batch1_16jul2026.md`; batch detail `batch1_done_16jul2026.md`.

**All 15 items verified IN THE CHECKED-OUT TREE** (not just the bare repo): b64-XLSX gone + ignore gap closed ·
no token in the cron log · DEPLOYMENT.md path corrected · SYSTEM_MAP INDEX · PATHS header · README +
ops/__init__ · sqlite3 hoisted · candle date via today_ist · entry_start_time explained (**value UNCHANGED**) ·
M-K5 redaction · GUI session key · win% one-denominator · holiday guard · portable test · cron_alerts
tri-state. Modules compile; `config_loader.load_all()` OK.

**⏰ NOTHING OWED — but know WHEN each item bites (deploy ≠ restart):**
- **GUI session key (F2): at the GUI's NEXT RESTART.** `gui-dashboard` is `active/running` on the OLD code
  right now ⇒ **its next restart is the LAST one that will log Rama out.** `data_store/session/gui_secret_key`
  does not exist yet — correct, the fix is lazy (writes on first use).
- **Cron items** (win%/holiday guard/token/candles/alert escalation): each job's **next scheduled run**.
- **M-K5**: at the next `main.py` boot (the snapshot is written at startup).
- **trading-system**: halted on the planned SOFT_KILL (dated 16-Jul ⇒ a PRIOR-DAY kill at the 17-Jul 08:15
  boot ⇒ `clear_stale_state` auto-clears it — [[killswitch-autoclear-prior-day]]). **No restart, no action.**
- **Boot-readiness verified:** deployed `EXPECTED_SCHEMA_VERSION=44` == live v44 ⇒ the 08:15 boot **skips
  migration**; no migration sentinel fired.

**🔴🔝 CARRIED TO THE LOOP QUEUE (the reason this batch mattered):**
1. **E4 CAPITAL FINDING — the daily-loss limit is fed GROSS P&L.** CHECK1/RMS/manual closes pass `costs=0.0`
   into `release_used` where `pnl = gross_pnl - costs` ⇒ **`pnl_delta` (the loss-limit's input) AND available
   capital are credited with gross, not net.** The note called it "slightly optimistic"; the book is **gross
   −0.007R vs net −0.100R** ⇒ costs ARE the loss, so the control is fed the WRONG number, not a slightly-off
   one. Fix = LOOP (capital path). Mechanism recorded in [[capital-operational-note]].
2. **P3-s14 ESCALATED** — the webhook "300s dark window" is NOT missing logging: `_process_signal` has no
   generic handler around the INSERT, so the **dedup claim is never rolled back** ⇒ retries DUPLICATE-bounced.
   The fix is that rollback = **control flow deciding whether a signal enters at all**.
3. **6 DEFERRED:** A5 (gitignored Word binaries — Rama authors) · A6 (**underspecified — one table row, no
   content**) · pytest skew (a DECISION: root `>=9.0.3` vs GUI `==8.3.4`) · C4 (F2 tail, ~20 per-job criterion
   decisions, several read capital state) · C5 (B-1 metrics design) · **D2 IMPOSSIBLE as specified —
   `tests/crash_test/ct_utils.py:63` hardcodes `DB_PATH = data_store/trading_system.db`, opened WRITABLE, a
   module constant ⇒ "scratch only, never live" needs a harness change.**

**✅ GROUP-E OUTCOMES:** **M-SC2 CLOSED — RUNTIME-PROVEN** (screened CSV **1 row/40B on 13-15-Jul → 25
rows/2,033B on 16-Jul**, the first EOD after M-SC2b deployed; one of the register's four HONEST-CLOSURE gaps
now shut) · **BK-8 core CLEAN** (no hardcoded config defaults in capital/orders/signals/screening/core — the
pydantic loader really IS the single source, previously UNVERIFIED; residual = 5 scripts defaulting
`TRADING_MODE` to `"live"`) · **F4 auto-clear benign** (clean daily `KILL_AUTO_CLEARED` cadence) · **E3/P3-r8
blocked on Rama** (the contract note lives outside the repo).

**⏰ STILL OWED (from earlier today):** F1 gate-8 **observe soak** (first data Fri 17-Jul) → Rama-gated enforce
flip · **alert-watcher 24h soak** re-sample · **⚠️ the FIRST LIVE HARD_KILL is M-C8's real test** (the drill
was mock-broker only) — [[deploy-mc-cluster-done-16jul]].

**Rollback (schema-free):** L1 revert any one of the 15 (each independent) · L2 reset `main` to the pre-batch
base `362e166` (= the deployed M-C cluster `06a61cb` + the classification docs commit) · DB
`pre_deploy_batch1.db`.

See [[batch1-done-16jul]] [[batch-classification-16jul]] [[deploy-mc-cluster-done-16jul]]
[[unpushed-pending-deploy-ledger]]
</content>

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 408 B (budget 300 B). The index now carries a hook and this link.

- ✅🗂️ **[BATCH-1 DEPLOYED (16-Jul)](deploy_batch1_done_16jul.md)** — 15 items live. **🔴 To the LOOP: E4 — CHECK1/RMS `costs=0.0` ⇒ the DAILY-LOSS LIMIT is fed GROSS not net** (gross −0.007R vs net −0.100R ⇒ costs ARE the loss) · **P3-s14** (webhook dedup rollback). 🏆 M-SC2 CLOSED runtime-proven. Per-item detail + the 6 findings: [[batch1-done-16jul]]. [[deploy-batch1-done-16jul]]
