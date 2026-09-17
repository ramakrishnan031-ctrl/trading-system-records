---
name: audit_lowsev_verify_03jul
description: "7 lower-severity audit findings verified vs current main (03-Jul) — 5 fix, 1 accept-per-locked-decision (E-2), 1 accept-with-note (B-2 partially fixed); batch order for ONE off-market deploy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54ecd864-01af-4fbe-b453-740efca8a1e9
---

**Lower-severity audit closeout verification (03-Jul, read-only, vs main==9becf8c + live VM checks).**
Verdicts (evidence file:line in the session report):

- **C-3 FIX (still live):** healthcheck :8080 binds 0.0.0.0 (default `healthcheck_server.py:243-44`;
  `main.py:2834-36` passes only port; **live `ss` confirmed 0.0.0.0:8080 + :5000**). /health leaks
  `account_id`+`expires_at` (`:38-40`) + raw `str(exc)` (`:79,96`); /metrics leaks pnl/capital/kill
  (`:110-126`). **ALL consumers are VM-localhost** (preflight `engine.py:27-28`, GUI metrics_client
  per D8/Q2) → bind 127.0.0.1 breaks NOTHING; + scrub payload (drop account_id, generic db_error).
- **C-4 FIX (still live, WORSE than audit):** `zerodha_login.py:159-60` save_token no chmod —
  **live perms 0664 (world-readable, group-writable)**, record holds access_token+api_key. Fix:
  chmod 0600 after write + session dir 0700 (token-watcher/monitor read as same user = unaffected).
- **F-1 FIX (still live):** `main.py:1739` `getattr(app_config.system,'min_free_disk_gb',1.0)` but
  field lives on **LoggingConfig** (`config_loader.py:702-05`; yaml `:267` = 2.0) → always 1.0. Fix:
  read `…system.logging.min_free_disk_gb` DIRECTLY (no getattr default — fail-fast per foundation
  rules); passes to `startup_checks.py:1589`.
- **E-4 FIX (still live):** `/health` checks = db/token/kill_switch/tgt_retry ONLY
  (`healthcheck_server.py:83-96`) — no order_monitor / order_reconciler / eod_scheduler /
  live_feed liveness (order_monitor self-stops after 3 fails, invisible). Fix: mirror the
  tgt_retry provider pattern ×4. **Synergy: B-1's MTM freshness rides the reconciler — E-4 makes a
  dead reconciler visible on /health + preflight Phase-B.**
- **A-3 FIX (still live):** last-mile kill check `order_placer.py:932` is NOT last-mile — network
  I/O between it and submit `:1203` (`_fetch_ltp` +57/+151, `_check_liquidity` +245); header OP-LM1
  claim aspirational. Fix: re-check `is_active("entry")` (in-memory) immediately before
  `engine.execute()` → FAILED+release (same as :932 path). Bounded today (leak is SL/TGT-protected).
- **E-2 ACCEPT (locked decision — task file conflicts with it):** `clear_stale_state`
  (`kill_switch.py:199-248`) clears EVERY prior-day kill **by explicit documented decision — the
  20-Jun-2026 "HEADLESS GUARANTEE" (docstring L200-212)**: new day always starts clean; safety net
  = KILL_AUTO_CLEARED audit + EOD-report analysis (Task B). Same-day kills persist (L220-21);
  `auto_clear_scheduled_kill` (L250-88) already refuses HARD_KILL/emergency/open-positions.
  Operator tooling: `scripts/clear_kill_switch.py` = resume only (no first-class overnight-kill
  CLI). **Recommendation: keep locked decision; add ops-doc line "to hold a morning boot: disable
  token-watcher/service, NOT a kill" + OPTIONAL narrow carve-out (prior-day HARD_KILL AND
  triggered_by operator/manual survives) ONLY if Rama revises the 20-Jun decision.**
- **B-2 ACCEPT-WITH-NOTE (audit partially stale):** `state_store.sector_exposure:709-23` ALREADY
  counts in-flight `PENDING_FILL` rows ("RE6 audit fix") — residual = reserve→persist window (rows
  not yet written; fm reservations carry no sector) + `PENDING` status omitted. Unreachable in
  practice: concentration-capped per-position margin ≈2% × max_open 5 = ~10% « 40% cap (boundary
  only reachable at max_position_value_pct=0.40 sizing ×5 same-sector — not realistic at ₹10k).
  Note in docs; future hardening = sector on reservations + add PENDING.

**BATCH ORDER (one off-market deploy, after the current batch+GUI soak; commits separable):**
Commit A (pure infra, zero trading-path): C-4 + F-1 + C-3 + E-4 · Commit B (trading-path, tiny):
A-3 · Commit C (ONLY if Rama revises 20-Jun): E-2 carve-out · B-2: docs note only. Each with
fail-on-old tests; all parity-clean (infra or mode-agnostic). No interaction with deployed
A-1/E-1/A-2 or queued B-1 (except the E-4×B-1 synergy). Rides the same wave as B-1b/W10/D-1.
**SYSTEM_MAP pointer DEFERRED** — tree=gui-deploy-03jul frozen for tonight's push (same flag as
[[b1_unrealized_mtm_design_03jul]] / [[d1_close_trade_race_design_03jul]]).
