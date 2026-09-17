---
name: kite_ip_allowlist_dependency
description: Zerodha Kite dev-console has a static-IP allowlist for order placement — MUST update on any VM IP change
metadata: 
  node_type: memory
  type: project
  originSessionId: 926bcdec-f5d1-4d8b-ab01-42b2d61dba29
---

The Zerodha Kite developer app enforces a **static-IP allowlist for order
placement** (NOT for read APIs). On any VM public-IP change this MUST be updated
at https://developers.kite.trade/apps → app → static/allowed IPs, or live trading
silently breaks.

**18-Jun-2026 incident (root cause of the whole day's cascade):** VM IP migrated
161.118.188.171 → 161.118.187.249, but the Kite console still allowlisted the old
IP. Symptom: `get_margins`/`get_positions` (reads) worked, but every `place_order`
returned **HTTP 403 PermissionException "IP (...) is not allowed to place orders
for this app."** Chain: signals approved → place_order 403 → 3 consecutive API
failures → kill_switch **auto-trip SOFT_KILL** (api_failure_threshold=3). On the
next restart, persisted SOFT_KILL → `main.py` HALT → `exit(4)` → systemd + the
**watchman watchdog** crash-looped it (~17 restarts). This was also the cause of
the morning 08:10 "spurious auth burst" trip.

**Resolution:** Rama added 161.118.187.249 to the Kite allowlist. Then: stop
service → set kill_switch_state row to INACTIVE (operator resume) → restart.
Verified: health ok, kill_switch_active=false, new public IP :5000/health=200,
30 order placements with ZERO 403s post-restart, real fills (REDINGTON etc.).

**Operational lessons:**
- Add "update Kite dev-console allowed IP" to the VM-IP-migration checklist
  ([[project_vm_architecture_locked]]).
- A persisted SOFT_KILL turns into a fatal HALT crash-loop on restart (KS3). To
  recover: clear kill_switch_state to INACTIVE first, THEN restart. Do NOT just
  `systemctl restart` a HALTed service — the watchman will crash-loop it.
- read-API success does NOT prove the broker path is healthy; order placement has
  a separate IP gate. See [[deploy_requires_restart]], [[dual_daily_loss_mechanism]].

**Follow-up — DONE.** The 18-Jun crash-loop was the PRE-FIX-185 behaviour.
- **FIX-185** (since): `KillSwitch.record_api_failure(exc)` returns early for a
  `BrokerAuthError` → a 403 NO LONGER counts toward the auto-trip → **no SOFT_KILL,
  no HALT, no crash-loop.** With reads un-gated, `order_monitor`/`order_reconciler`
  never escalate and the token is never invalidated. So a pure IP-403 now just
  fails each entry (`signal_processor` SP12 `_PipelineReject`) and **self-recovers
  on the NEXT signal once the IP is allowlisted — no restart, no manual resume.**
- **20-Jun headless alert (commit 7126034):** new `broker/auth_recovery.py`
  (`classify_broker_auth_error` IP-vs-token-vs-unknown · `get_public_ip` ·
  `build_ip403_alert_body`); `record_api_failure` now fires **ONE CRITICAL
  alert/hour** on an IP-allowlist 403 with the **VM's current public IP + exact
  Kite steps**, via the injected notifier → sentinel → **email** (the live channel
  while Telegram is banned to 22-Jun). Throttled 1/hr, outside the lock,
  best-effort; FIX-185 preserved. **Why/How:** when live entries stop, check email
  — it names the exact IP to paste into Kite; do that and trading resumes on its
  own. Verified live: `get_public_ip()` → `161.118.187.249`. The token-watcher
  restart-retry idea was investigated and **dropped as moot** (no halt occurs to
  retry). Updating the Kite console on a VM-IP change is still Rama's external step.
- **DEFERRED (Rama's diary batch, his call):** add a **startup pre-flight
  IP-allowlist check** — the IP is constant for the day, so one cheap probe at boot
  (e.g. a harmless/cancellable order-API touch, or a dedicated check) would catch a
  stale allowlist BEFORE any signal trades, firing the same `build_ip403_alert_body`
  alert proactively instead of on the first live entry. Entry-path alert is the
  reactive net; this is the proactive net. Reuse `broker/auth_recovery.py`.
  Related: [[softkill_investigation_20jun]], [[fix_188_headless_autostart]],
  [[smtp_alert_watcher_config]].
