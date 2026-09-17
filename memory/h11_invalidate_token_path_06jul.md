---
name: h11_invalidate_token_path_06jul
description: "Wave-3 H-11 DONE (06-Jul, commit f7282f0 unpushed) — main._invalidate_token now targets the REAL token path data_store/session/zerodha_token.json (was CWD), re-arming the FIX-062 auth-restart-loop guard."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-3 H-11 FIXED** (commit `f7282f0`, main, UNPUSHED — Rama pushes off-market). One fix = one commit (`main.py` + new `tests/unit/test_h11_invalidate_token_path.py` + `tests/unit/test_fix062_token_invalidation.py` path-corrected; H-8/H-9 untouched). Ref finding H-11 in `docs/audit/full_system_audit_04july2026.md`.

**Root cause:** `main._invalidate_token()` used `Path("zerodha_token.json")` (process CWD), but the broker token lives/reads at **`data_store/session/zerodha_token.json`** everywhere: live-startup loader `scripts/zerodha_login.py::is_token_valid`/`load_token` (called `main.py:1800/1806`), `_load` (`:314/:399/:1637`), `scripts/auto_refresh_token.py:61 _DEFAULT_TOKEN_PATH`, deploy/token_watcher scripts, PATHS.md:26. On the VM CWD=project root so `Path("zerodha_token.json")` = a NON-existent file → on a BrokerAuthError `_invalidate_token` logged "not found, skipping" and left the dead token → FIX-062 restart-loop guard **inert** (service could loop on a revoked token).

**Guard flow (now armed) — caller trace:** critical failure whose reason contains `"BrokerAuthError"` → `_make_critical_failure_cb._on_critical_failure` (`main.py:570`) → `_mark_auth_failed()` sets `_broker_auth_failed=True` → `_shutdown` (`:1107-1108`) calls `_invalidate_token()` → real token renamed to `.invalid` → next non-interactive live boot: `is_token_valid(account, data_store/session/zerodha_token.json)` (`:1800`) → False → CRITICAL "Token missing or expired" → **`return 6`** (fail-fast, no reuse of the dead token). (Ultimate loop-stop past that is systemd StartLimit/RestartPreventExitStatus = unit config, not this code.)

**Fix:** added module consts `_TOKEN_PATH = Path("data_store/session/zerodha_token.json")` + `_TOKEN_INVALID_PATH = _TOKEN_PATH.with_suffix(".invalid")` and pointed `_invalidate_token` at them (same atomic `os.rename`, correct target; warning now prints the real path). Loader/writers UNCHANGED. No shared const existed before (all sites inline the literal) — the new const unifies only `_invalidate_token`; the loader sites still inline `Path("data_store/session/zerodha_token.json")` = residual duplication (PATHS.md is the authoritative record; broad consolidation is out of H-11 scope).

**Consumer/state scan:** token writer (interactive login / `auto_refresh_token`) + loader (`zerodha_login`) already use this exact path; invalidation only renames on an auth-fail shutdown → no clash. `_broker_auth_failed` has no consumer beyond `_shutdown`.

**Parity:** token invalidation is mode-agnostic (one Kite token; paper has no real token and never gets a real BrokerAuthError → flag never set) — single path, no paper duplicate.

**Tests** (`test_h11_invalidate_token_path.py`; REAL `main._invalidate_token`/`_shutdown` + REAL loader `zerodha_login.is_token_valid`/`load_token` against a genuine token file at the loader's real relative path via temp chdir; only `_shutdown`'s component collaborators are MagicMocked): **T1** invalidate renames the real token → loader can no longer load it (RED before: real token survived, `is_token_valid` True) · **T2** auth-fail `_shutdown` flow → `is_token_valid` False so next boot fails fast (RED before) · **T3** valid token round-trips when flag not set (no clash). The pre-existing FIX-062 suite encoded the WRONG CWD path in its fixtures (the audit's "test mocks the broken thing" pattern) → 3 fixtures corrected to the real path. RED proven by `git checkout` to HEAD (invalidate logged "not found, skipping"; real token survived). **58 green** (H-11 + FIX-062 + H-13 + FIX-128 + auth_recovery + clock_skew + preflight_security); 0 regressions.

**Residual risk:** restores the FIX-062 auth-restart-loop guard that had been DEAD (a revoked-but-present token could loop the service). Residual token-path duplication (loader sites still inline the literal; not consolidated — out of scope). PATHS.md already records the authoritative path.

Related: [[fix_187_headless_totp]] · [[token_workflow_confirmed_21jun]] · [[h13_token_monitor_relatch_06jul]] · [[h12_paper_positions_signed_06jul]]. **Wave-3 status: H-12✓ · H-13✓ · H-11✓ · H-8/H-9 PENDING.** STOP after H-11 (did not start H-8); await review.
