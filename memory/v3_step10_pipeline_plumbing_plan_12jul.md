---
name: v3_step10_pipeline_plumbing_plan_12jul
description: "V3 Step 10 — pipeline-plumbing PLAN ONLY (how the V3 chain threads through _process_one in shadow); nothing built, ledger unchanged. TASK-0 headline = plumbing built/OFF, decision content missing."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3a8e48f-3a62-4b08-be45-1271e86b1c37
---

**V3 SHARED-ENGINE — STEP 10 · PIPELINE PLUMBING — PLAN ONLY (12-Jul-2026, off-market).** Design doc `docs/v3/V3_STEP10_PIPELINE_PLUMBING_PLAN.md` (TASK-0 inventory + P1-P10, self-contained for Web Claude + ChatGPT + Rama). **NO code / config / VM change; deploy ledger UNCHANGED (nothing built).** Baseline `main`@`c1ad82e` (VM shadow×2, else OFF). Runs in parallel with the scorer + allocator shadow soaks.

**TASK-0 HEADLINE (the whole point):** Steps 1-9 built every V3 module as an **independent, local shadow** — each observes/logs its OWN decision and gates nothing. What is genuinely MISSING is NOT more modules; it is the **chain**:
- **Decision content (the real V3 IP, unbuilt):** no **playbook registry / PB-01 definition** (no `v3_playbook` field on `StrategyConfig` — verified absent); the **playbook-scope hard gates** (confirmation / valid-pullback / S&R-R:R / strong-HTF / extreme) are **NAMED in `hard_gate.py:6-8` docstring but have ZERO code** (stubs); the **3-layer score (Playbook 40 / Context 40 / Execution 20)** is **NOT built** — only the **8-step "Execution seed" re-scale** exists (`hard_gate.py:171` `rescaled_total`; `quality_scorer.py` UNCHANGED).
- **Consumption wiring (produce→nobody-drinks):** **regime** runs once/cycle and exposes `runner.latest` but **nothing consumes it** ("gates NOTHING", `regime/runner.py:6-7`); **S&R** is observer-only (`confidence_class=ANCHOR_ONLY`, observed at `signal_processor.py:517`) — **nothing consumes levels for a decision**.
- **Allocator scope empty:** shadow observes the **existing FCFS flow**, NOT a V3 set — `enforce_scope: v3_only` + `v3_scope_fn=lambda s: getattr(s,"v3_playbook",False)` (`main.py:2732`) → always False → "none exist yet".
- **PB-01 front-end MISSING:** no stateful **overnight watchlist** / next-morning 5-min entry (`EntryGate` is same-day, cleared at EOD by FIX-046).
- **Built + ready:** the **seam** (`_process_one` sizing→allocator-hook boundary, `signal_processor.py:924-965`), the **candidate primitive** (`_build_candidate`→`ScoredCandidate`+`AdmitPayload`), sizing (`sl_price` param seam open), entry/trade-mgmt/exit (03.07-09 complete). **One-liner for Rama:** pipes built + OFF; water (playbook/gates/3-layer-score) not; regime/S&R drip to the floor.

**SEAM DECISION (P2):** a V3 branch **INSIDE `_process_one`, flag-selected** — realized as (i) additive **enrichment** of the candidate already flowing through the live path (attach regime + S&R + gate + 3-layer-score fields) and (ii) a **flag-gated STOP-and-emit** for `v3_playbook` candidates (write a would-be-trade JSONL instead of `_admit_and_place`). Reuses screen/derive/size verbatim. Rejected: (b) separate stream consumer (re-implements the pipeline — R2 forbidden), (c) replay harness (can't produce a live would-be to compare). PB-01's overnight watchlist is a new signal **SOURCE** (emits into the same `_process_one`, like `webhook_receiver`), NOT a new pipeline.

**NEW flags planned (all default-OFF, byte-identical):** `StrategyConfig.v3_playbook: bool=False`; master `v3_chain_mode: off|shadow` (binary — no enforce yet); `watchlist.enabled: false`. **Would-be output** = `data_store/v3/would_be_trades.jsonl` (NO schema change, mirrors allocator `regret.jsonl`), compared via a NEW `v3_shadow_soak_report --v3` mode. **PB-01 promotion evidence is its OWN would-be track record** (via existing `shadow_tracker`), NOT OLD-vs-NEW (no live twin) — honesty flagged.

**PB-01 rides INTRADAY (delivery stays OFF):** entry = next-morning 5-min retest, same-day exit under `force_intraday_only`; the overnight part is analysis WATCHLIST (no CNC/GTT/capital carry). Delivery double-locks + Option-A 12/3 split untouched. True overnight position-carry = Slice 2.5 (out of scope).

**SEQUENCING (P8):** 1 playbook substrate → 2 consumption wiring → 3 3-layer score → 4 playbook gates → 5 would-be record+emission → 6 overnight watchlist+next-morning entry → 7 allocator scope → 8 soak. Steps 2-5 provable on EXISTING live signals first (webhook exercises the enrichment); watchlist (6) added after the plumbing is proven, then PB-01 rides it.

**OPEN QUESTIONS to relay (P10):** Q1 PB-01 gate rules+thresholds; Q2 3-layer sub-weights + seed→20 rescale; Q3 strong-HTF source (S&R TF_ROLE swings? regime?); Q4 regime as multiplier vs gate-input; Q5 watchlist retest level+window; Q6 flag granularity (per-playbook once >1).

Builds on [[v3_phase0_investigation_11jul]] (source-verified `8116b74` gap analysis) + the Steps 1-9 chain [[v3_shadow_deploy_soak_12jul]] / [[v3_step9_exit_engine_12jul]]. **NEXT = Web Claude + ChatGPT + Rama review → separate build instruction authorizes Step-10 build (per P8 sequencing).** Related deferred front-end context: [[delivery_slice25_status_30jun]] (Slice 2.5 = the OTHER delivery track, not PB-01), [[sr_v1_calibration_deferred_30jun]] (S&R calibration gates the S&R-R:R gate).
