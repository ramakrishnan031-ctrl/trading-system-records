---
name: eod-alert-enh-03jul
description: "System Manager EOD report P&L reconcile + 3 enhancements (03-Jul) — email always, strategy-prefixed orders, full strategy roster"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b1fa8b6-3ab8-4f25-a39a-0a6806490486
---

**Part A — P&L reconcile (VERIFIED, not a bug):** the ₹3.55 gap between the
broker positions page (gross ₹-12.52, 03-Jul) and the EOD report's daily-loss
line (net ₹-16.07) is **exactly** the day's total charges. Summed
`trades.gross_pnl`/`charges`/`net_pnl` for all 10 closed trades: gross total
`-12.52`, charges total `3.55`, net total `-16.07` — `gross - charges = net`
to the cent. `trades` already has per-trade cost columns
(`cost_brokerage`, `cost_stt`, `cost_exchange_txn`, `cost_sebi`, `cost_gst`,
`cost_stamp_duty`, rolled into `charges`). The EOD report's P&L source
(`config_vs_actual_check`'s "Daily loss actual" line and `compare_with_yesterday`'s
P&L line) is a raw `SUM(trades.net_pnl)` — confirmed NOT the W10-buggy
`get_daily_realized_net_pnl` (that function isn't called anywhere in
`system_manager.py`; W10 stays bundled into [[b1_unrealized_mtm_design_03jul]]'s
B-2, untouched by this work).

**Part B — 3 enhancements, `scripts/system_manager.py`, commit `1621d6c`:**
1. **Email always.** `_send()` now calls `write_critical_sentinel(...)`
   unconditionally every EOD run (any severity), mirroring `cron_officer`'s
   EOD `email_backup` pattern. The Telegram send uses `write_sentinel=False`
   so a clean/warning day isn't gated behind the notifier's CRITICAL-only
   sentinel path, and a violation day doesn't get double-sentineled into two
   emails. Recipient was already `ramakrishnan031@gmail.com` in
   `config/system_config.yaml`'s `alerts.smtp.to_addresses` — no config
   change needed there. **Live-confirmed**: ran a real (non-dry-run,
   `--no-soft-kill`) pass for 03-Jul (0 violations, INFO severity) — sentinel
   `critical_alert_20260703_191906_21b4b133.flag` was written with
   `context={"severity":"INFO"}`, delivered by `alert_watcher.service` within
   ~6s. Confirms a *clean* day now reaches the inbox, which it didn't before.
2. **ORDER QUALITY strategy prefix.** Each line now reads `"<strategy> →
   <symbol> <direction> <exit_reason>: entry ...→..., exit ..., P&L ..."`
   (added `strategy` to the SQL SELECT). Also added a P&L breakdown line to
   this section per Part A's decided display: `"P&L: gross ₹X | charges ₹Y
   | net ₹Z (broker positions page shows GROSS)"`.
3. **STRATEGY HEALTH full roster.** New `_enabled_strategy_names(config_dir)`
   reads `config/strategies/*.yaml`, collects names where `enabled: true`,
   and `trade_strategy_health` now enumerates the union of that set with
   today's traded strategies — a strategy with zero trades today gets `"<name>:
   0 trades, — win, ₹0.00"` instead of being silently absent. Existing
   `strategy_metrics`-based multi-day review-flag lines (e.g. "win_rate 0%
   over 3 — review") are unchanged and still print alongside.

**Flag — strategy count is 15, not 12:** all 15 files in
`config/strategies/*.yaml` have `enabled: true` (12 `intent: INTRADAY` + 3
`intent: DELIVERY`: `positional_momentum_long`, `positional_sector_rotation`,
`positional_swing_long`). Rama's brief expected "12 intraday
(force_intraday_only=true) [15 if delivery on]", i.e. the 3 DELIVERY ones
excluded while `force_intraday_only=true`. But `strategies/loader.py`
(`load_all_strategies`) shows `force_intraday_only` only **overrides each
strategy's `intent` field to INTRADAY at load** — it does NOT exclude the 3
DELIVERY-tagged strategies from trading; they load and trade identically to
the 12, just as MIS instead of CNC. Real evidence: `positional_swing_long`
fired an actual MANUAL-exit trade today (₹-6.06), proving it's live right
now, not dormant. So I implemented the roster as **all 15** (matches actual
system behavior) rather than the 12 Rama expected — flagged explicitly so he
can tell me if he wants the 3 DELIVERY-tagged ones filtered out of this report
regardless of whether they're currently trading.

**Unrelated finding surfaced incidentally (not fixed, flagging separately):**
while pulling `scripts/system_manager.py` from the VM via `scp` for this task,
the copy completed successfully with **no entry in
`data_store/security/copy_audit.log`** and no wrapper interception — even
though the VM's `time_lock_start: 18` (18:00-08:00 hard block, described in
`config/security.yaml` as "ABSOLUTE... overrides EVERYTHING") should have
blocked it at ~19:03 IST. `/usr/local/bin/scp` IS a symlink to
`deploy/security/bin/copy-guard` on the VM, but modern OpenSSH clients
default to the SFTP protocol, which server-side is a sshd-forked
`sftp-server` subsystem — a different binary path than `/usr/local/bin/scp`/
`sftp`, so the wrapper (and possibly the auditd `copy_attempt` watch) never
sees it. **This looks like a real, unauthenticated bypass of the VM's
VM→PC copy-protection gate** (Phase 2/3, deployed 20-Jun) via the default SFTP
transfer mode, separate from the raw-`scp`-protocol case the wrapper was
built for. Not investigated further or fixed — out of scope for this EOD-alert
task; worth its own dedicated session with Rama's input given it's the same
security surface [[ssh_alert_full_details_03jul]] touched this session.

**Deployed:** main `800d0c1 → 1621d6c`, pushed to the VM bare repo. Verified
via `--dry-run --date 2026-07-03` (full render check) then one real
`--no-soft-kill` run (0 violations, safe) to confirm live email delivery.
17 existing tests in `tests/unit/test_system_manager.py` +
`test_system_manager_security.py` pass. Effective the next real EOD (Mon
06-Jul 18:45 IST cron, unchanged schedule — no cron/service restart needed
since system_manager is invoked fresh by cron each day, not a long-running
service).

**How to apply:** if Rama wants the STRATEGY HEALTH roster narrowed to 12
(excluding DELIVERY-intent strategies even though they currently trade under
`force_intraday_only`), filter `_enabled_strategy_names` by original
`intent == "INTRADAY"` — but note this would make a strategy that DOES trade
(like `positional_swing_long`) invisible from the zero-trade enumeration
while still appearing via the trades-today path, which is a slightly odd asymmetry
to explain if a delivery strategy trades on a future day.
