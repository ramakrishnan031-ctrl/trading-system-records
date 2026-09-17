---
name: p1_eod_broker_reconcile_build_design_02jul
description: "P1 build design (02-Jul, no code) — standalone broker-authoritative EOD reconcile scripts/eod_broker_reconcile.py @15:58 replacing eod_verify false-VERIFY; VERIFIED/ISSUES/UNVERIFIED; shadow-first"
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

P1 broker-authoritative EOD reconcile — BUILD DESIGN done 02-Jul (design-to-build spec, NO code). Full doc: `docs/design/p1_eod_broker_reconcile_build_design_02jul2026.md` (SYSTEM_MAP + PATHS point to it). Builds on [[p1_eod_broker_sync_assessment_02jul]].

**Architecture:** NEW standalone `scripts/eod_broker_reconcile.py` (not an in-place eod_verify rewrite) so it can SHADOW alongside eod_verify then become authoritative. Runs @**15:58** (after reconcile_positions @15:45 + settle) with its OWN creds via `reconcile_positions._resolve_credentials` (AccountRegistry + token file) → **runs even if trading-system.service was DOWN at 15:17** (the highest-risk gap — square-off never fired). Queries broker `get_positions`/`get_all_orders`/`get_margins`/day-P&L, compares to local, emits **VERIFIED** (broker-confirmed clean) / **ISSUES** (divergence) / **UNVERIFIED** (broker unreachable — NEVER false-pass). Replaces eod_verify's local-only false-VERIFY.

**Subsumes reconcile_pnl:** real creds (not the never-set generic `ZERODHA_API_KEY`) + queries the CORRECT `system_pnl`/`broker_pnl`/`variance` cols (schema already right `schema.sql:783-785`; the bug was eod_verify's query using non-existent `system_net_pnl`/`broker_net_pnl` → swallowed → variance 0.0). **Consumes reconcile_positions:** reads `position_reconciliation`; any ORPHAN/MISSING/QTY_MISMATCH → P1 can't be VERIFIED (kills the VERIFIED-vs-15:45-CRITICAL contradiction); also does its own get_positions for robustness.

**Hooks:** cron_registry `eod_broker_reconcile` @15:58 critical+monitored; READ trades/orders/fm_ledger/position_reconciliation; WRITE pnl_reconciliation (correct cols) + NEW `eod_broker_reconciliation` verdict table (date PK, per-dim statuses, overall_status VERIFIED|ISSUES|UNVERIFIED, mode, notes, verified_at — PURE-ADD migration). Surfacing: EOD Telegram + Control Tower finding/freshness source + cron_officer --eod-summary.

**4 detections (compare+emit):** (1) orphan positions broker vs local (ORPHAN/MISSING/QTY_MISMATCH — catches process-down naked at EOD); (2) capital drift `get_margins().net` vs `fm._total`; (3) ledger drift (3-balance invariant + `Σ RELEASE_USED.pnl_delta` vs broker day-P&L; cross-checks [[get_daily_realized_pnl_double_cost_01jul]]); (4) manual broker actions + the exit-reason **TGT_HIT vs MANUAL_CLOSE label refinement** (deferred `order_placer.py:2092`) across alert+stored+stats.

**Boundary:** DETECT + VERIFY + ALERT ONLY. NO auto-fix (flatten/capital-correct/relabel) = **P3**.

**Parity:** ONE path — adapter `get_positions` etc.; in PAPER the "broker" is the sim (`_paper_positions`) → **self-consistency check, labeled `mode=PAPER`**, not independent authority; no if-paper branch (strictly better than reconcile_positions' fabricated paper OK).

**Rollout SHADOW-first:** `eod_reconcile.authoritative=false` default → P1 @15:58 writes its verdict + logs/alerts at INFO WITHOUT replacing eod_verify @15:55 or gating → observe a few EODs (catch eod_verify-VERIFIED-but-P1-ISSUES = false-VERIFY in the wild; confirm UNVERIFIED on unreachable) → flip authoritative=true → CUTOVER retires eod_verify + reconcile_pnl (registry swap, like daily_review→daily_trade_review Phase C). Reversible via flag + git.

**Deploy/rollback:** off-market; new job + cron entry + pure-add table migration + shadow flag; rollback = flip authoritative false / revert. Isolated from B-1 (`risk_engine`/`fund_manager`/`order_reconciler` MTM) + A-2/C-1; own branch off main. P1 reuses reconciler broker-access/compare PATTERNS but is a SEPARATE standalone job (does NOT modify the 15s in-session reconciler). Related: [[audit_remediation_status_02jul]], [[b1_daily_loss_unrealized_mtm_impl_02jul]], [[control_tower_phase1a_29jun]], [[phase_c_cutover_01jul]].
