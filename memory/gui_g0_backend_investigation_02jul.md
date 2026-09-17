---
name: gui_g0_backend_investigation_02jul
description: "Frontend GUI Phase G0 backend investigation — report location + 5 design-critical findings (investigation-only, no code)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 157eab85-5916-43a3-9c57-323a11cc5b69
---

Frontend GUI (Rama's pending decision #8) is moving. **Phase G0 = backend investigation ONLY** (zero code changes) COMPLETE 02-Jul-2026. Report: `docs/gui_project/G0_BACKEND_INVESTIGATION_REPORT.md` (8 sections, every claim cited `file:line`). Method: 5 parallel read-only agents + direct verification of the two CRITICAL sections (control §3, security §6). Also recorded in `mempalace.yaml` (gui_project node), `docs/SYSTEM_MAP.md` (new "GUI Project" section stub after the header), `PATHS.md` (top pointer).

**Locked v1 decisions (Rama, 02-Jul):** same Oracle VM · browser-from-anywhere HTTPS-only single-user auth-required · runs while PC off · desktop-first + mobile-responsive · control depth = view + safe controls (pause/resume · enable/disable · kill pending orders · manual square-off · emergency halt · restart) · ~20 view modules.

**5 design-critical findings (FACTS for Web Claude G1, not design):**
1. **TWO existing Flask+Waitress HTTP servers**, both daemon-threads INSIDE `main.py` (up only while trader runs): webhook `:5000` (HMAC/`?token=` auth, `require_hmac:false`) + healthcheck/metrics `:8080` **UNAUTHENTICATED** (`scripts/healthcheck_server.py` — `/health` `/metrics` `/metrics/prometheus`, exposes P&L/capital/kill-switch/open-positions). Both bind `0.0.0.0`, plain HTTP. **NO reverse proxy / NO TLS** (only a DEPLOYMENT.md §8 recommendation). ufw opens 5000. No fastapi/uvicorn/websockets/node in-repo; Python 3.12.3, flask 3.1.3 + waitress 3.0.2 pinned.
2. **Control plane barely exists.** Only operator surfaces today = `scripts/clear_kill_switch.py` (clear halt) + `systemctl restart` (SSH). **NO programmatic entry point** for: pause strategy, live enable/disable (config loaded ONCE, no hot reload → restart required), cancel pending orders, single-position square-off, trigger-halt-on-demand (all halt triggers are automatic; forcing one = raw DB write). **No inbound Telegram** (outbound-only). Every existing control path is **paper==live parity** (pure resolver / adapter-abstracted).
3. **No cross-process push transport** — `core/events.py` EventBus + CandleStore callbacks are in-process only. GUI must POLL: SQLite (WAL + `busy_timeout=30000` ⇒ a read-only reader is safe concurrent with the writer during market hours) or the in-process `/metrics`. **Live LTP is NOT persisted** (only in trader memory / broker) → GUI needs its own broker session for live prices (pattern: `scripts/eod_broker_reconcile.py`).
4. **DB = 43 main + 3 analytics = 46 tables** (schema v42 in the `fix-p1` checkout; **live VM = v41** @ 9becf8c — `eod_broker_reconciliation` not yet on VM). **NO `positions` table** (status-filtered `trades`) / **NO `holdings` table** (CNC via `gtt_state`). Data exists for nearly every view module; the gaps are control APIs + live LTP + VM CPU/RAM (psutil ABSENT → `system_metrics` cpu/mem = -1.0; only disk real).
5. **18:00–08:00 time-lock = `copy_gate.py` guard over scp/sftp/rsync ONLY** — NOT a network/SSH/browser lock; would NOT block nighttime browser access. Copy-protection = exfil control on scp/sftp/rsync (HTTP file-serving bypasses it). `security_monitor`'s **9 checks never inspect listening ports** (check 7 counts only `:22` sessions); a GUI writing under `config/` or `.env` trips auditd (11 watches) / check-6, writes to `data_store`/`logs`/`reports` do not. fail2ban = sshd jail only (no HTTP jail). All alert-only, never block.

**Logs** (Logs Viewer): 3 JSON-lines files (`system_/trades_/reconciler_*.log`) + plain `debug_*`/`cron-*`; plain `FileHandler` (not Rotating); 30-day cron cleanup. **Reports:** `reports/output/daily_trade_review_report_<date>.xlsx` @16:07, **NO retention** (grows unbounded). **Cron** = 45 registry jobs; **6 systemd units**. **Health reuse:** healthcheck_server + preflight `vm_health.py` + `capture_metrics_baseline.py` + Control Tower freshness + security_monitor.

**[REQUIRES LIVE VM]** (not run from PC): `systemctl is-active`, `ss -tlnp`, live fail2ban/auditctl rules, RAM/CPU/disk headroom (documented floor 2 vCPU / 2 GB / 20 GB). **NEXT = G1** (Web Claude designs GUI architecture from the report).

NOTE: report + 3 doc updates are UNCOMMITTED working-tree changes on branch `fix-p1-eod-broker-reconcile-02jul` (relevant to [[offmarket_deploy_runbook_final_03jul]]'s clean-tree merge — Rama may want them on a separate docs branch or stashed before the C-1→B-1→P1 merge).
