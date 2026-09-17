---
name: v3_step4_hardgate_scorer_plan_11jul
description: "V3 Step 4 PLAN-ONLY — coupled 03.03 Hard-Gate extraction + 03.04 scorer re-scale design doc; no code, default-OFF flag + offline parity proof; awaiting ChatGPT review"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Step 4 (11-Jul-2026): PLAN/DESIGN ONLY for the COUPLED 03.03 Hard-Gate extraction + 03.04 scorer re-scale. NO code written, NO config changed, NO live behaviour altered, ledger untouched.** Doc: **`docs/v3/V3_STEP4_HARDGATE_SCORER_PLAN.md`** (sections P1-P8, self-contained for Web Claude + ChatGPT). Follows [[v3_step3_market_regime_11jul]]. First change to the LIVE scoring path → planned, not built.

**Verified current state:** circuit_check (step 9) + signal_age (step 10) are BOTH scored (weight 10 each, `scoring_weights.yaml`) AND already act as gates (at-circuit penalized / pre-fill proximity hard-reject `_circuit_proximity_reason`; signal_age==0 → hard reject `secondary_screener.py:275`; intake expiry 600s upstream). Scorer is PROPORTIONAL `total=Σachieved/Σweights_present×100`, min_pass 60, tiers 80/65. **Single live seam = `secondary_screener.screen()`** (only caller `signal_processor.py:778`; built once `main.py:2447-2455`). **KEY ENABLER: `screener_results.step_results_json` persists every per-step raw score** → the old-vs-new parity proof is a deterministic OFFLINE recompute over historical rows (no live run).

**Core design decisions in the plan:**
- **P1 extract, don't duplicate:** new `screening/hard_gate.py::HardGate` runs at the exact spot the pre-fill circuit reject already occupies inside `screen()`, BEFORE the scorer; circuit/age logic RELOCATED (step_executor drops steps 9&10 → 8 steps Σ80; scoring_weights drops the 2 keys). One path, no fork.
- **P2/P3 re-scale is THRESHOLD-ONLY (critical):** re-weighting the 8 steps to Σ100 is SCALE-INVARIANT under proportional scoring (no-op). Keep 8 weights at Σ80; recalibrate thresholds. For a gate-survivor (circuit=10 constant; age_c∈{5,10}): OLD=a8+10+age_c, NEW=1.25·a8. Map: `new=1.25·old−12.5−1.25·age_c`. Analytic thresholds (age≤30s reference): **min_pass 60→50, medium 65→56, high 80→75.**
- **EXACT parity IMPOSSIBLE** (age folded into the OLD pass decision; a single new threshold can't reproduce it). Residual = the age 30-60s band (marginally more permissive — intended, since freshness is now a binary gate). at-circuit-but-passed signals now gate-rejected (≈0, intended). MUST data-fit thresholds on the historical corpus.
- **P4 parity proof:** offline recompute from `step_results_json` classifying every historical signal UNCHANGED/FLIP-PASS/FLIP-FAIL/TIER-SHIFT/NOW-GATED; accept iff flips ⊆ explained residual. Build-gate test on a real backup + live shadow-compare.
- **P5 Hard-Gate module:** houses the full V3 battery with per-rule SCOPE (LIVE: circuit+proximity+freshness+liquidity; PLAYBOOK-shadow: confirmation/pullback/R:R/strong-HTF/extreme) + missing-data rule (must-have fail-CLOSED; must-not-have fail-OPEN). R:R uses ANCHOR-only levels until swings validated. Only LIVE rules gate the live flow.
- **P6 safety spine:** `scoring.v3_hardgate_mode: off|shadow|enforce` (default OFF → byte-identical live path). shadow = compute both, act on OLD, log the pair. enforce = act on NEW. Feasible at the single `screen()` seam.
- **P7 regression map:** consumers of `screener_results.score`/thresholds = reports (daily_trade_review/daily_report read from config snapshot → auto-follow, but the `min_pass_score=60` build-gate test needs update), GUI (strategy_tower/db_reader/strategy_score — display only), config_auditor (only B4 tier_multipliers rule → unaffected; propose new high>medium>min invariant). Flag-OFF byte-identity test + stash-diff full-suite.

**P8 OPEN QUESTIONS for ChatGPT:** (1) final threshold values — fresh-reference (recommended) vs conservative; (2) accept the age-band residual as intended; (3) freshness gate cutoff — 60s vs the ambiguous 90s/600s (needs ONE authoritative number, Phase-0 flag); (4) re-scale the per-strategy `min_score` overrides too? (inventory `config/strategies/*.yaml` non-zero min_score). **NEXT = ChatGPT/Web Claude review → Step-4b implements the approved values behind the default-OFF flag.**
