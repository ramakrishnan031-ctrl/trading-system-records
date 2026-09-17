---
name: telegram-alert-enhancements-29jun
description: "Telegram alert redesign DEPLOYED to main 61246d9 (29-Jun post-close): Direction line on signal+order alerts + EOD summary redesign (🟢/🔴 long/short split, per-trade detail). Rebased onto Control Tower; ff-merged+pushed+restart exit0; cosmetic alert-text only, NO schema"
metadata:
  node_type: memory
  type: project
  originSessionId: 4b77fdb8-7ea5-4ee9-bbe8-ab048798239f
---

**Telegram alert enhancements — DEPLOYED to main `61246d9` (29-Jun ~19:25 IST, post-close).** Cosmetic alert-text only, no trading-logic/DB-schema change. Shared notifier body ⇒ paper+live parity (mode only sets the `[{mode}]` title prefix). main is again the single source of truth — NO dangling approved-but-unmerged branch (the local branch was deleted post-merge; it was never on origin).

**What shipped (3 code files + SYSTEM_MAP header):**
- CHANGE 1 — Direction (LONG/SHORT) is the FIRST body line on INTRADAY SIGNAL (`signals/signal_processor.py::_emit_signal_alert`, above `Strategy:`) + ORDER PLACED (`orders/order_placer.py::_format_order_placed_body`, NEW pure staticmethod extracted from `place()`, above `Fill:`). Both normalise SELL→SHORT / BUY→LONG defensively.
- CHANGE 2 — EOD DAILY SUMMARY redesign (`orders/eod_squareoff.py::_format_summary_body`, NEW pure staticmethod from `_send_daily_summary`; empty-trades branch unchanged): Best/Worst carry `DIRECTION | exit_reason`; **🟢 Long / 🔴 Short split** (n, W/L, P&L from real directions, totals overall W/L); per-strategy 🟢/🔴 (long first) + per-trade detail `• STOCK - DIR - ₹entry - ₹exit (TAG) - ±₹pnl`. Helpers `_disp_dir`/`_exit_tag`(SL/TGT/EOD/MAN/TO/CB)/`_summary_entry_px`. P&L/win-rate/AvgR/capital/SmartTGT formats UNCHANGED.

**The REBASE (key event):** branch was cut off OLD main `033ae58`; tonight's earlier Control Tower deploy advanced main to `4cbeb2a`, so it was NOT a clean ff. Rebased `da78db4`→`61246d9` onto current main: **only the 2 doc headers (`SYSTEM_MAP.md`, `PATHS.md`) conflicted** (both edited by Control Tower + this branch); resolved preserving BOTH (Telegram note prepended ahead of the Control Tower entry; kept DB **v40**, dropped the branch's stale v39). The 3 code files applied CLEAN (main never touched them). PATHS.md ended with zero net diff vs main.

**4 conditions (ChatGPT's):** (1) ff → NO (main moved) → clean rebase; (2) no schema migration ✓; (3) no cron_registry/crontab change ✓; (4) no config outside Telegram scope ✓ (diff = SYSTEM_MAP doc + 3 code files + test).

**Verification (post-deploy, all green):** restart **exited 0** on the FIX-189 market-window guard @19:26 IST (new code boots, no import/syntax break; activates next session Tue 08:15); **Config Auditor 0 BLOCK** (1 pre-existing unrelated WARN: entry_end 15:15 vs eod 15:17); `sr_detector.enabled` still **true**; `reports/daily_report.py` heartbeat intact (import L1871 + call L1872); Control Tower 17:05 runner registered; **live crontab == canonical, zero drift**; render of the approved samples on the DEPLOYED tree matches Rama's approval (Long −₹9.08 / Short +₹8.75, 4L/1S). Pre-deploy: live DB backed up `data_store/backups/pre_telegram_deploy_20260629_192423.db` (integrity ok, v40). Tests post-rebase: 146 passed / 0 regressions (11 alert + eod_squareoff + signal_processor).

**OBSOLETE warning corrected:** the prior note feared the auto-install post-receive hook would DROP the 4 `tools/claude` claude-heartbeat lines (05:30/10:31/15:32/20:33). It did NOT — those 4 lines are now PART of the canonical `deploy/cron/trading-system.cron` (43 cmd-lines incl. heartbeats), so the auto-install installs them correctly. No manual preservation needed anymore.

**NOT in scope (separate tickets, untouched):** entry_end review, T1 disk-metric repair, T2 retention job, T3 weekly advisory scanners. Related: [[feedback_paper_live_parity]] · [[feedback_system_map_first]] · [[control_tower_phase1a_29jun]].
