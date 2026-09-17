---
name: gui_g2a_dashboard_03jul
description: "Ops Dashboard G2a — isolated Flask GUI skeleton + Dashboard (M1) built on branch gui-g2a-03jul (PC-only, not merged)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 157eab85-5916-43a3-9c57-323a11cc5b69
---

Ops Dashboard **Phase G2a COMPLETE** (03-Jul-2026): isolated read-only Flask GUI skeleton + Dashboard (M1). Branch **`gui-g2a-03jul`** (off the fix-p1 checkout; **NOT merged to main**; PC-only, NO VM deploy). Follows [[gui_g0_backend_investigation_02jul]]. Folder renamed to **`ops_dashboard/`** (not gui_project) per G1.

**HARD ISOLATION (test-gated I7, all green):** zero production imports (AST gate over `ops_dashboard/backend/**`), SQLite opened **read-only** (`file:<abs>?mode=ro` + ATTACH analytics ro + `busy_timeout=30000`; a write raises `sqlite3.OperationalError` — proven), **no kiteconnect** in its own git-ignored `.venv` (`pip show kiteconnect` fails), binds **127.0.0.1:8500 loopback only** (0.0.0.0 refused at startup + proven not bound). No prod startup/systemd/cron/hook touched.

**Stack:** Flask 3.1.3 + Waitress 3.0.2 + pyotp + PyYAML + pytest (own `backend/requirements.txt`). `db_reader.py` = the ONLY SQLite touchpoint. Readers: db_reader / metrics_client (`:8080/health` GET, unreachable⇒trader_alive=False never raises) / config_reader (config_snapshots.config_json snapshot-first, YAML fallback) / host_reader (`systemctl is-active`→"unavailable" on Windows). Services: freshness (IST fixed +5:30 market clock, drives 5s/60s poll + GRAY-vs-RED), pipeline_state (pure `derive_color`), capacity, summary_bar, strategy_panel.

**Auth** (`backend/auth.py`): single-user pbkdf2_sha256(salted)+TOTP(pyotp)+5-fail/15-min lockout; CLI `python -m backend.auth --setup --username --password`. Cookie HttpOnly+SameSite=Strict; **Secure config-gated** (`server.session_cookie_secure` default false so loopback-HTTP dev login works; →true under TLS in G2c). login_required on ALL routes incl static (before_request guard; only /login GET/POST exempt; login.html fully self-contained inline CSS).

**M1 Dashboard:** 13-stage pipeline big-cards (GRAY/BLUE/YELLOW/ORANGE/GREEN/RED/PURPLE; blink active) + halt rail; Daily Capacity Monitor (8 primary quotas Limit·Used·Remaining: daily-trades 10, open-pos 5, daily-loss 3%×capital, intraday-capital 70%×capital, consec-losses 5, signal-queue 300, delivery×2 INERT); Strategy panel (per-strategy signals/trades/W-L/net/rank); service-health strip; last-10 events; trader-down banner. 4 JSON APIs `/api/{dashboard,pipeline,capacity,strategy_panel}` all login_required. Frontend = base.html (Alpine over JSON, poll from freshness.poll_ms) + dashboard.html + login.html + vendored htmx 1.9.12 + alpine 3.14.1 + dark style.css.

**STEP-0 capacity inventory** → `ops_dashboard/docs/G2a_capacity_inventory.md`: 30 configured-limit keys mapped to live-counter source (table.col+WHERE) + remaining formula + v1 Y/N. 8 documented ambiguity decisions (D1 daily-trades counts cancelled=YES; D2 daily-loss uses fm_ledger RELEASE_USED not get_daily_realized_net_pnl [W10]; D3 capital used=margin_used +pending; D4 opening-capital fallback→AWAITING; D5 consec-loss streak def; D6 delivery INERT; D7 in-memory counters deferred; D8 queue via /health). Key schema facts reused: signals.status reject families = `REJECTED_{check}` (risk: OPEN_POSITIONS/DAILY_TRADES/DAILY_LOSS/CONSECUTIVE_LOSSES/SECTOR_EXPOSURE/...; capital: CAPITAL/RESERVE_FAILED/SIZING_VALID); no positions/holdings table; opening capital = Σ INIT balance_after (total, not per-bucket).

**VERIFIED (evidence captured):** 102 tests pass on BOTH v41+v42 synthetic fixtures (conftest builds faithful DDL + seeds); V4 funnel exact (Received 100 / Validated 85 / Duplicate 10 / Rejected 5 / Orders-Created 70 / Orders-Filled 60 + all 13 stages); real Waitress server `/`→302→`/login`, `/login`→200, `/api/*` no-auth→401, 0.0.0.0:8500 not bound (loopback confirmed). `mode` is a data attribute (session/snapshot), never a code branch (parity).

**Deviations flagged:** (1) SESSION_COOKIE_SECURE default false on loopback-HTTP dev (else login can't work without TLS) → true in G2c. (2) UI rendered via Alpine-over-JSON (not htmx fragments) because APIs are JSON-contract-first; htmx vendored+available, poll cadence still driven by freshness flag. (3) tiny `util`-style IST clock lives in freshness.py (the market-clock module) — no separate util file added.

**NEXT = Web Claude reviews G0 report + capacity inventory → issues G2b (M2–M20).** Doc updates (SYSTEM_MAP GUI section G2a state, PATHS ops_dashboard paths, mempalace g2a_dashboard node) committed on `gui-g2a-03jul` (also carries the previously-uncommitted G0 docs, which cleans fix-p1's tree for [[offmarket_deploy_runbook_final_03jul]]). Pending G2c decisions Q1 Tailscale-vs-443 / Q2 :8080 exposure / Q3 reports-download NOT pre-built.
