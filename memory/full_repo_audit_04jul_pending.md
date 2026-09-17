---
name: full-repo-audit-04jul-complete
description: "04-Jul full-repo deep audit COMPLETE — 11-agent fan-out (run sequentially after an API-limit burn) delivered docs/audit/full_system_audit_04july2026.md; 13 HIGH / 47 MEDIUM, 0 CRITICAL"
metadata: 
  node_type: memory
  type: project
  originSessionId: f39c9932-1562-4657-8d80-d3327d287983
---

# Full-repo deep audit (04-Jul-2026) — COMPLETE

**Deliverable (in repo):** `docs/audit/full_system_audit_04july2026.md` — consolidated, de-duplicated, severity-ranked, every finding cites file:line.

**Process note:** first attempt launched all 11 agents in PARALLEL → API session-limit burn twice, zero reports. Re-run SEQUENTIALLY (one agent → collect report → next), resuming each interrupted agent via SendMessage(agentId) so its read context was preserved. Per-agent raw reports saved in the session scratchpad `audit_01..11_*.md`. Rule now permanent: [[feedback-sequential-agents-only]].

**Result:** **0 CRITICAL · 13 HIGH · 47 MEDIUM · ~55 LOW.** No money is being lost right now under normal operation.

**★ Dominant theme — dead safety nets** (protections that look active, pass their tests, do nothing):
- H-1 FIX-190 Bug E cancel-resting-exits — dead column `orders.broker_order_id` (real PK `order_id`); OperationalError swallowed → emergency flatten leaves live SL/TGT → naked reverse. `order_placer.py:3613`
- H-6 same dead column in BreakevenManager `breakeven_manager.py:385` (also entirely unwired)
- H-8 ShadowTracker TGT recalc dead — wrong column `strategy_name` vs `strategy` `shadow_tracker.py:317`
- H-11 `_invalidate_token()` wrong path (CWD vs data_store/session/) → FIX-062 auth-restart-loop guard inert `main.py:127`
- H-9 FIX-049 candle late-tick discard dead + off-by-one landmine `candle_store.py:174/286`
- SlBreachMonitor (FIX-134-39) + BreakevenManager (FIX-132-8) never wired into main.py
- Root cause: schema/path/wiring drift masked by tests that mock the broken thing. Systemic fix = schema-backed integration tests for raw-SQL money paths + a "wired-in" assertion per safety layer.

**Other HIGH clusters:**
- Emergency-exit chain: H-1 + H-2 (EXITING → close_trade "double close" early-return, capital locked ~30min, loss invisible to both daily-loss gates) + H-3 (retry places fresh SL+TGT on closed/protected trade) + M-O1 (`_flatten_broker_position` double-prefixes NSE:NSE → always raw MARKET, FIX-181 cap dead). `order_placer.py` + `order_reconciler.py:1743`
- HARD_KILL: H-4 retry loop re-fires stale qty → double-sell after ambiguous first exit; H-5 sweep hardcodes intent=INTRADAY → sweeping CNC opens naked MIS short. `kill_switch.py:1218/1166`
- H-6 CNC GTT exit-day broken end-to-end (held-qty double-counts same-day CNC sell → false F6 → row retired → never finalized, capital never released). `cnc_gtt_monitor.py`
- H-7 per-strategy position cap TOCTOU-racy (outside portfolio_lock, no in-flight comp) → Chartink burst blows cap 2→5; triplicated. `signal_processor.py:843`
- H-12 paper get_positions strips qty sign → FIX-190 reverse-flatten DOUBLES a short in paper (parity + can't validate flatten). `zerodha_adapter.py:1077`
- H-13 TokenMonitor expiry latch never resets → one blip permanently disarms token-expiry alerting. `token_monitor.py:130`
- H-10 place() result=None deref after 16388 on final attempt → leaked reservation, stuck PENDING. `order_placer.py:1335`

**Verified CLEAN:** layering (core/sr_detector/ops); ops_dashboard web security (login_required + before_request guard, mode=ro DB, path-traversal defenses, XSS-safe, loopback bind); Control Tower read-only; git hygiene (credentials.xlsx gone, no tracked secrets, crontab==registry); v28 ATTACH discipline; webhook auth timing-safe; single Decimal charges authority.

**Remediation order (in report §Recommended):** 1) emergency-exit chain 2) HARD_KILL 3) CNC GTT exit-day 4) dead safety nets + systemic test 5) per-strategy cap + paper parity 6) reporting integrity + capital MEDIUMs 7) LOW hygiene.

**Likely next ask from Rama:** a fix-plan / batched remediation. Related: [[audit_remediation_status_02jul]] · [[audit_lowsev_verify_03jul]] · [[t2_halt_investigation_reconciler_tag_bug_01jul]] (the original broker_order_id/tag class).
