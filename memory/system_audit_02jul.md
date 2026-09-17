---
name: system_audit_02jul
description: Full security & integrity audit 02-Jul (investigate-only) — 1 CRITICAL + 4 HIGH; full report in docs/audit/
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e62fe89-aead-435f-8580-0a242667edcc
---

Full-repo security & integrity audit, 02-Jul-2026, INVESTIGATION-ONLY (no code changed). 5 parallel category agents (deepest A–C), every Critical/High + material Mediums lead-verified against source. Full report: `docs/audit/system_security_audit_02jul2026.md`.

**CRITICAL (1):**
- **C-1** — Live secrets committed in git-tracked `.env.example` (+ history): api_key/api_secret/**TOTP 2FA seed** for LFL836 (primary) AND DR6114 (enabled), real TELEGRAM_BOT_TOKEN, WEBHOOK_SECRET. `FILL_WHEN_READY` on disabled accts proves the rest are real. → rotate ALL creds + purge history NOW. BOTH.

**HIGH (4):**
- **A-1** — Timed-out entry that DID reach broker → `_check_unknown_in_flight` (order_reconciler.py:3113-3186) matches only persisted `broker_order_id` (never persisted on timeout) → marks FAILED + releases capital w/o confirming broker absence → later fills as unprotected NAKED position (orphan-adoption disowns as "human"). Root enabler: broker `tag` written but never read for correlation. EOD-sweep bounds to intraday. LIVE.
- **A-2** — `BrokerTimeoutError` retried (signal_processor.py:1009 bundles it w/ rate-limit) → 2nd `kite.place_order` = double entry. Contradicts FIX-068. Today masked only by entry-throttle (min_gap 20s/cooldown 300s), NOT idempotency. LIVE.
- **B-1** — Daily-loss unrealized-MTM term is DEAD (update/remove_unrealized_mtm called only by tests; grep-decisive) → both loss controls realized-only → concurrent open drawdown can overshoot 3%. NOT W10. risk_engine.py:500 + fund_manager.py:1265-1296. BOTH.
- **C-2** — Webhook `0.0.0.0` + `require_hmac:false` (config comment says bind "relies on require_hmac=true" — violated); sole live auth = committed `?token=` over plaintext; paper can be unauthenticated. BOTH.

**MEDIUM:** C-3 (healthcheck 0.0.0.0:8080 no-auth leaks P&L/capital/kill-state/account_id) · D-1 (`close_trade` non-atomic TOCTOU close guard → double non-idempotent `release_used`; fix = conditional UPDATE+rowcount) · E-1 (crash between broker-accept & local-persist → naked; same root as A-1) · A-3 (kill-switch TOCTOU in place() between check@932 & submit@1203).

**LOW-MED:** F-1 (min_free_disk_gb 2GB silently ignored — main.py:1728 reads it off `system` not `system.logging` → hardcoded 1GB) · C-4 (token file no chmod 0600) · E-2 (SOFT/HARD-kill auto-clear has NO reason-allowlist → operator's manual overnight HARD_KILL lifted at 08:15 boot; by-design but real) · E-4 (order_monitor/reconciler/eod/live_feed no /health liveness) · B-2 (sector-exposure not reservation-aware; unreachable at current leverage) · C-5 (secret prefixes in logs).

**Positive:** E-3 session-expiry FAILS SAFE (halts); kill-switch same-day always persists; no SQL/shell injection; dedup robust (3-layer); no config safety-bypass switch.

**Already-tracked (mapped):** W10 (double-cost, re-confirmed, ≠B-1) · W11 · W2 · W3 (A-1 tag-gap partially overlaps but distinct) · the 2 operator resilience items confirmed.

**Convergence:** A & E independently found the SAME root (recovery keys on a broker_order_id/order-row absent for timeout+crash; tag never correlated; orphan-adoption disowns as human) — highest-value code fix after C-1.

**Recommended act-order (NOT done — investigate phase):** C-1 rotate → C-2 lock webhook → A-1/E-1 shared tag-correlation fix → A-2 stop retrying timeout → B-1 wire MTM → D-1 conditional close → rest. Each fix = PERMANENT + paper/live parity + fail-on-old tests.

**Why:** first full adversarial audit since the 14-15-Jun pass; surfaced a genuine CRITICAL (public creds) + a non-functioning advertised safety control (B-1) + a naked-position/double-entry class on the live order path (A-1/A-2) not previously understood.
