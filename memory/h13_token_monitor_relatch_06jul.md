---
name: h13_token_monitor_relatch_06jul
description: "Wave-3 H-13 DONE (06-Jul, commit e965589 unpushed) — TokenMonitor expiry latch now RESETS on a valid check + classifies transient-vs-expiry; restores the token-expiry safety net that was permanently disarmed after one blip/expiry."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-3 H-13 FIXED** (commit `e965589`, main, UNPUSHED — Rama pushes off-market). One fix = one commit (`broker/token_monitor.py` + `tests/unit/test_h13_token_monitor_relatch.py` ONLY; H-11/H-8/H-9 untouched). Ref finding H-13 in `docs/audit/full_system_audit_04july2026.md`.

**Root cause:** `TokenMonitor.check_now()` (`token_monitor.py:130-141`) treated ANY exception from `profile_fn()` (= raw `broker_adapter._kite.profile`, wired at `main.py:2453`) as a token expiry → CRITICAL "TOKEN EXPIRED" + SOFT_KILL via `_handle_expiry`, which SET `self._expiry_fired=True` and **nothing ever cleared it**. Two failure modes: (1) a transient network blip (`NetworkException`/5xx/timeout) fired a FALSE expiry + soft_kill and LATCHED; (2) once latched, a later GENUINE expiry no-op'd (`_handle_expiry:152-153` early-returns when `_expiry_fired` True) → no alert, no soft_kill → system kept attempting entries on a dead token until a restart. Dead safety net (reported healthy, did nothing).

**Expiry-vs-transient signal (Step 1.2):** classify on BOTH exception TYPE (`type(exc).__name__ == "TokenException"`, kiteconnect, matched by name — no hard import) AND message via `broker/auth_recovery.py::classify_broker_auth_error` (returns `TOKEN_EXPIRED` / `IP_NOT_ALLOWLISTED` / `AUTH_UNKNOWN`; token markers incl. `access_token`/`invalid token`/`session expired`/fallback `"token" in text`). `NetworkException`/`DataException`/timeout → `AUTH_UNKNOWN` → transient. `IP_NOT_ALLOWLISTED` = token VALID (profile is a read, not IP-gated) → do not fire.

**Fix (at the source, `token_monitor.py`):** (a) on a SUCCESSFUL check → `self._expiry_fired = False` (re-arm; latch is now once-per-EPISODE not once-per-process; logs `token_recovered` if it was set). (b) new `_is_token_expiry(exc)` gate — fire `_handle_expiry` ONLY when it returns True; a transient logs a WARNING (`transient_check_error`) and does NOT latch / soft_kill / alert. Once-per-episode suppression preserved (repeats within one dead-token episode still no-op). Added top-level `from broker.auth_recovery import classify_broker_auth_error` (stdlib-only, same package, no circular import).

**Consumer/state scan (Step 1.3):** `_expiry_fired` is referenced ONLY inside `token_monitor.py` (`:76/152/154`) — no external consumer. Resetting on success cannot cause duplicate alerts (reset happens only when the token is CONFIRMED valid; while it stays dead, `profile_fn` keeps raising → never resets → still one alert per episode) and masks no genuine expiry (a real expiry never succeeds a check).

**Parity:** single monitor, paper-mode `check_now()` is a no-op (`:127-128`), one live instance at `main.py:2453` — no paper-specific duplicate. One fix, both modes.

**Tests** (`test_h13_token_monitor_relatch.py`; REAL `check_now`/`_is_token_expiry`/`_handle_expiry`/latch + `classify_broker_auth_error` run; only the `profile_fn` API boundary simulated via a sequenced fake raising REAL kiteconnect exceptions; notifier=MagicMock, on_expiry=spy): classifier unit · T1 real expiry alerts once (episode suppression intact) · **T2 re-arm after recovery → 2nd expiry alerts (RED before fix: latch never reset → 1)** · **T3 transient blip does NOT latch, later real expiry still alerts (RED before fix: blip latched → real expiry no-op'd → 0)**. RED proven by `git checkout` to HEAD (transient fired false expiry CRITICAL; T2+T3 fail), then restored. **109 green** across H-13 + `test_fix128_token_monitor` + `test_auth_recovery` + `test_fix062_token_invalidation` + `test_kill_switch` + `test_preflight_state_security` + `test_exceptions`; 0 regressions.

**Residual risk:** restores a token-expiry SAFETY NET that had been dead (unnoticed expiry → auth failures / halted entries). Narrow residual: a SUSTAINED non-token auth failure that classifies `AUTH_UNKNOWN` stays silent (no CRITICAL/soft_kill) — a distinct "degraded/transient-error" alert does NOT exist in TokenMonitor and is a FUTURE item (not added — keeps scope minimal, avoids re-introducing false positives).

Related: [[h12_paper_positions_signed_06jul]] · auth_recovery from [[s1a_webhook_allowlist_rotation_05jul]] era · [[fix_187_headless_totp]] (token refresh). **Wave-3 status: H-12✓ · H-13✓ · H-11/H-8/H-9 PENDING.** STOP after H-13 (did not start H-11); await review.
