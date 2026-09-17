---
name: gui_readiness_g3_0_03jul
description: "P1 GUI readiness verdict: READY + DISPLAY-ONLY CONFIRMED (240 tests, POST=/login+logout only) + G3.0 control-plane facts (kill-switch in-memory sole authority; no hot reload; Q7 options table) — both docs committed e7a6a37 on gui-deploy-03jul"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54ecd864-01af-4fbe-b453-740efca8a1e9
---

**03-Jul market-hours read-only audit, committed `e7a6a37` on `gui-deploy-03jul` (docs-only).**

**PART 1 — READINESS VERDICT: "GUI READY + DISPLAY-ONLY CONFIRMED — safe to bundle tonight"**
(`ops_dashboard/docs/G2_READINESS_VERDICT.md`). Evidence: fresh **240 passed in 48.71s** (both
fixtures) · route audit 29 routes, **POST = /login + /logout ONLY**, all /api/* GET
(/api/reports/download GET + hard-403 while download=false, analytics.py:168) · backend greps:
0 SQL mutations, subprocess = only host_reader fixed-argv `systemctl is-active`, 0 kiteconnect/
broker imports · controls = **NO backend module exists** (static controls.html via generic GET
/<page>, 0 fetch/POST/form) · locks: reports_download_enabled=false (yaml:33 + INSTALL.md:39),
session_cookie_secure=true (INSTALL.md:38) · diff gate **4 buckets, 76→78 files** (the 2 docs;
E1 final gate tonight must expect **78/4**) · **P1.4 = NO-OP: credentials.xlsx .gitignore rule
ALREADY in the batch (`aa02f9f`, C-1 ancestor)** — no new commit made (a GUI-branch commit
would have added a 5th bucket and failed the gate; separate branch unnecessary). Full
ordering-(a) merge chain **re-proven CLEAN vs e7a6a37** (678c592→f5fd4d9→4817032→GUI).

**PART 2 — G3.0 CONTROL-PLANE FACTS** (`ops_dashboard/docs/G3_0_CONTROL_PLANE_INVESTIGATION.md`,
cited file:line, for Web-Claude G3 design):
- **Q1: NO — external DB writes never take effect live.** is_active = in-memory
  (kill_switch.py:394-406); DB row read ONCE at construction (:745-748); process overwrites the
  row on every in-process persist (KS9). Call sites: main:2726 (startup gate),
  order_placer:932, tgt_retry_manager:271.
- **Q2:** clear-while-running ⇒ divergence (DB INACTIVE, memory killed) — `resume.sh`
  stop→clear→start IS load-bearing (port-5001 instance-lock, 18-Jun collision; script aborts
  start on failed clear; --force for HARD_KILL).
- **Q3:** hot reload DOES NOT EXIST (config_loader.py:38, loader.py:27 explicit). Operator
  pause DOES NOT EXIST; **automatic** per-strategy pause EXISTS: governor `_paused_today`
  in-memory set (strategy_governor.py:42, resets restart/new-day), enforced at
  signal_processor:729/1470 (STRATEGY_CIRCUIT_BREAKER).
- **Q4:** :5000 = GET /health + POST /webhook/<scanner> (authed ingest); :8080 = GET /health,
  /metrics, /metrics/prometheus — no mutating admin route anywhere; BOTH Flask apps in-process
  → loopback admin endpoint = the only mechanism that could touch live memory (capability
  fact).
- **Q5:** SIGINT+SIGTERM → _shutdown_event (main:1051-60); unit KillSignal=SIGINT,
  TimeoutStopSec=30, Restart=on-failure, **RestartPreventExitStatus=3 4** (exit4 = kill-halt,
  no hammer-restart); shutdown flattens NOTHING (broker-resident protection + next-boot
  reconcile).
- **Q6:** ubuntu = `(ALL) NOPASSWD: ALL` (live sudo -l) → GUI restart needs NO sudoers change;
  auditd watches /etc/sudoers{,.d} + unit files + config/ + .env (record-only).
- **Q7 table** in the doc: per control (Halt/Clear/Restart/Pause/Resume) × mechanism
  (systemctl / resume.sh / in-process endpoint [new-small] / DB-write [ineffective live] /
  YAML+restart / governor-set [new-small] / file-flag [doesn't exist]) with latency, restart?,
  race, parity (all yes), footprint.

SYSTEM_MAP (G2c section, new paragraph) + PATHS (GUI blurb) pointer edits committed in the same
e7a6a37. Tonight's GO sequence unchanged — still holding for Rama's GO after 17:05.
