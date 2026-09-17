---
name: slice1-rr-fix-deployed-22jun
description: "Slice 1 DEPLOYED 22-Jun — fill-time TGT now honours each strategy's R:R (all 4 recalc sites) + SL/TGT after-check; schema v35"
metadata: 
  node_type: memory
  type: project
  originSessionId: 352c7b01-735b-48d3-8902-0d349b1dfe25
---

Slice 1 deployed to `main` 22-Jun-2026 (commit a730c63, Option 2). Activates on
the VM's next restart (Tuesday 23-Jun 08:30) — code is on disk; the running
service still has old code until then; live DB migrates v34→v35 on that restart.

**The bug (root cause):** the fill-time TGT recalc used order_placer's hardcoded
`self._rr_ratio` (default 2.0, never overridden in main.py) instead of the
originating strategy's `tgt_risk_reward`. Deferred exits are the ONLY TGT that
reaches the broker (placement defers), so the broker TGT was ALWAYS 2.0-based —
gap_fade (1.5) / gap_go (2.5) traded at the wrong R:R; FIX-013's "preserve R:R"
was unmet.

**Fix (Part A):** strategy R:R frozen at placement → `trades.tgt_risk_reward_applied`
(schema v35) + carried on the ENTRY `_FillEntry`; read at fill via
`_resolve_fill_rr()` at **all 4** recalc sites — the 3 audited PLUS the TGT-retry
path (order_placer line ~2462) the audit missed (same 2.0 bug). NULL/recovered
(pre-v35) trades → fall back to `self._rr_ratio` (2.0) **+ WARNING**.

**After-check (Part B):** `_verify_exits_placed()` reads the persisted SL/TGT
order rows (ground truth; parity-safe — paper+live persist the same rows), checks
price + qty vs intended. Missing/wrong SL = **CRITICAL**, TGT-only = **WARN**,
**alert-only** (no auto-cancel this slice). Verdict in `trades.exits_verified` /
`exits_verify_detail` — READ-BACK, unlike the write-only v34 sizing cols. CO SL is
broker-managed (bracket) → TGT-only check.

**Schema v35:** trades += tgt_risk_reward_applied / exits_verified /
exits_verify_detail; rebuild-trades migration (v34 pattern); DB-copy gated on the
real live DB (34→35, 77 trades preserved, integrity ok, idempotent). 16 new tests;
full suite = pre-existing baseline (zero new). Parity verified.

**Sequencing (Option 2):** YAMLs kept at CURRENT values (gap_fade 1.5 / gap_go 2.5
/ rest 2.0) for one day so Tuesday's live trades prove the broker honours EACH
strategy's distinct R:R. **Part C (all 15 YAMLs → 1.5) lands Wednesday 24-Jun**
AFTER the proof — NOT today.

**Why:** [[live_trading_readiness]] correctness — broker must trade each strategy's
configured R:R. **How to apply:** Tuesday, paste a real trade row showing
`tgt_risk_reward_applied` + `tgt_initial == broker resting TGT` + an
`exits_verified=1` line = the fix proof. Then Wednesday set all YAMLs to 1.5.

**RESUME SCHEDULE (Rama, 22-Jun):** continue THIS R:R/Slice-1 subject **Tuesday
23-Jun after 15:30 IST** (post market-close) — that's when Tuesday's live trades
exist to provide the proof above. Don't push it earlier in the day.

Related: [[db_schema_v28_split]], [[deploy_requires_restart]], [[tgt_retry_mechanism]],
[[fix_190_incident]] (Bug C SL-only path), [[feedback_paper_live_parity]].
NOT in this slice: Slice 2 (per-strategy intent/master trade_type), Slice 3
(pre-flight strategy table), exit auto-cancel/re-place, full position-size intent recon.
