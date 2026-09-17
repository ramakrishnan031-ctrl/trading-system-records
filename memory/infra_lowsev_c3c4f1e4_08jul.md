---
name: infra_lowsev_c3c4f1e4_08jul
description: "Low-sev infra/security hardening batch C-3/C-4/F-1/E-4 BUILT + committed — branch infra-lowsev-c3c4f1e4-08jul @dd4f3f4 (LOCAL/UNPUSHED, off main 271d24f); zero trading-path; A-3 excluded"
metadata: 
  node_type: memory
  type: project
  originSessionId: a1ce6ed3-8992-41fa-9570-f5c148c8d6b8
---

**Low-sev INFRA/security batch (audit 02-Jul `system_security_audit_02jul2026.md`) BUILT + committed — branch `infra-lowsev-c3c4f1e4-08jul` @ `dd4f3f4` (08-Jul, LOCAL/UNPUSHED, off main `271d24f`, main untouched).** Zero trading-path behaviour change; proper source fixes. **Push OFF-MARKET only** (built mid-market, safe = local branch). **A-3 (last-mile kill re-check) EXCLUDED** — kill-path, separate careful item.

- **C-3 (MED)** `scripts/healthcheck_server.py`: default bind `0.0.0.0:8080`→**`127.0.0.1`** (was leaking live P&L/capital/kill-switch posture unauth via /metrics+/health). + payload scrub: `/health` no longer returns `account_id` (→`account_present` bool), raw exception strings genericised (token/kill_switch/db → `*_check_failed`; real error still logged server-side). main.py passes no host → default applies.
- **C-4 (LOW-MED)** `scripts/zerodha_login.py::save_token`: token file (holds `access_token`+`api_key`) was written at umask default (0644 world-readable). Now `os.open(...,0o600)` (no world-readable window) + `chmod 0600` (tightens a pre-existing file) + session dir `chmod 0700`. **OFF-MARKET VM OP owed:** one-time `chmod 600` of the CURRENT live `data_store/session/zerodha_token.json` (the next 08:15 refresh rewrites it 0600 anyway — so low urgency).
- **F-1 (LOW-MED)** `main.py`: `getattr(app_config.system,"min_free_disk_gb",1.0)` ALWAYS fell back to 1.0 (field is on nested `LoggingConfig`, SystemConfig is `extra="forbid"`) → configured 2 GB floor silently ignored. Now reads **`app_config.system.logging.min_free_disk_gb`**. **PATHS.md: no change** (code config-read path, not a documented filesystem path).
- **E-4 (LOW-MED)** daemon liveness on `/health`: added read-only `is_alive()` to `OrderMonitor`/`OrderReconciler`/`EodSquareoff` (thread checks) + a `daemon_liveness_provider` wired into `/health` (mirrors `tgt_retry` pattern). The 3 poll threads GATE health (dead→503); `live_feed` connection reported but **NON-gating** (feed disconnect auto-heals via reconnect → must not false-alarm uptime monitors).

**Tests:** `test_healthcheck_server.py` (+C-3 bind/scrub + E-4 liveness matrix: dead-reconciler-503, live-feed-non-gating-200, provider-raises-503, backward-compat), `test_zerodha_login.py` (+C-4 0600/0700 POSIX-gated + cross-platform chmod-call spy + pre-existing-file tighten), `test_f1_disk_config_floor.py` (NEW; F-1 path resolves + old top-level attr absent — put in its OWN file so staging didn't re-scan `test_config_loader.py`, whose pre-existing `password_env` test lines trip the commit secret-scanner as a false positive). **241 passed, 2 skipped (POSIX perms on Windows), 0 regressions** (incl. order_monitor/reconciler/eod_squareoff suites 199 green). Pre-commit secret-scanner passed.

SYSTEM_MAP.md batch-done note PENDING the next off-market doc-sync on main (deferred to keep main untouched; batched with [[wave5_runtime_validated_08jul]] + [[p1_reintegrated_271d24f_08jul]]). Cleared to build by TRACK-1 [[wave5_runtime_validated_08jul]]. [[build_plans_commitA_B_d1_07jul]] · [[full_repo_audit_04jul_pending]]
