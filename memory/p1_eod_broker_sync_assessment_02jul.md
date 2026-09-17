---
name: p1_eod_broker_sync_assessment_02jul
description: P1 EOD broker-sync/observer READ-ONLY assessment (02-Jul) — eod_verify false-VERIFYs (local-only + dead column bug); no scheduled EOD P&L/capital broker reconcile; build sequence set. No code
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

P1 EOD broker-sync / observer — read-only architecture + gap assessment (02-Jul, no code). Full doc: `docs/design/p1_eod_broker_sync_assessment_02jul2026.md` (SYSTEM_MAP + PATHS point to it). Done via 4 parallel source reads, crux claims re-verified.

**STEP 0 exists-vs-missing:** NO artifact literally named "EOD-broker-sync"/"EOD-observer" was ever closed (28-Jun = MFE/MAE excursion only). Capability is spread: `reconcile_positions.py`@15:45 (standalone cron, broker↔local POSITIONS, but detect+alert-only, paper fabricates OK, gates nothing) · `order_reconciler` 15s CHECK1-9 (in-process, broker-authoritative, auto-fixes; PROCESS-DEPENDENT) · `eod_squareoff`@15:17 (in-process flatten; PROCESS-DEPENDENT) · Control Tower@17:05 (read-only FRESHNESS observer, NO broker session) · CHECK9/f6de000 (in-session SL-race+oversell). A-1/E-1 in-session naked = already FIXED `9becf8c`.

**Confirmed gaps (STEP 2):**
- **eod_verify FALSE-VERIFY (severe):** `scripts/eod_verify.py:44-81` makes ZERO broker calls — VERIFIED whenever local DB shows 0 OPEN/PARTIAL trades + 0 PENDING orders. A broker naked position the DB doesn't know → "EOD VERIFIED: all clear". ISSUES_FOUND sent via `send_info` (low sev).
- **NEW: eod_verify P&L arm is DEAD (column bug):** queries `system_net_pnl - broker_net_pnl` (`:61`) but real cols = `system_pnl`/`broker_pnl` (`schema.sql:783-785`) → OperationalError swallowed by bare except → variance stuck 0.0. AND its source `pnl_reconciliation` is never populated (`reconcile_pnl.py` NOT scheduled — not in crontab/registry; also reads generic `ZERODHA_API_KEY`/`ACCESS_TOKEN` never set → would ERROR).
- **No EOD P&L OR capital broker reconcile.** Capital is LOCAL-authoritative: `sync_from_broker` only at startup + 09:15 one-shot, never periodic/EOD. `system_manager`@18:45 capital = local DB "no broker".
- **Capital drift = detect-only, never kills:** escalation gated by `source_module`; `order_reconciler`-sourced (G3, CHECK5) is non-escalating (INFO-log). Only fund_manager-INTERNAL inconsistency (invariant/commit/bucket/CHECK7) kills — i.e. local-vs-itself, never local-vs-broker.
- **Process-down-at-EOD (highest risk):** service down at 15:17 → square-off never fires → naked overnight; reconcile_positions@15:45 CRITICAL-alerts (detect only) while eod_verify@15:55 emits contradictory VERIFIED.
- Others: orphan-ORDERS at broker not covered by cron (CHECK6 in-session only); reconcile_positions no paper parity; reconciler/eod-scheduler no `/health` liveness (audit E-4).

**Truth-source:** positions/orders = broker (continuous, not a discrete EOD event); realized P&L = broker-priced but locally-ledgered; capital = LOCAL (broker only sampled for alerting after 09:15).

**Build sequence:** P1 = standalone, process-independent, broker-authoritative EOD reconcile (positions+orders+P&L+capital; REAL verification replacing eod_verify false-VERIFY; broker-unreachable⇒UNVERIFIED never false-pass; subsumes orphaned reconcile_pnl + fixes column/creds bugs; consumes reconcile_positions so VERIFIED can't contradict it; +capital-vs-margins; paper parity via adapter; fold in manual-close + exit-reason label refinement `order_placer.py:2092`). P2 = divergence observer/alerting + `/health` liveness (E-4) + feed Control Tower. P3 = in-session edges (make G3 drift escalate; guarded EOD orphan auto-flatten). Related: [[ref_security_audit_02jul]], [[control_tower_phase1a_29jun]], [[get_daily_realized_pnl_double_cost_01jul]], [[a1_e1_orphan_fix_impl_02jul]], [[check9_race_aware_fix_01jul]].
