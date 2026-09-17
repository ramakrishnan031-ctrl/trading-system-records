---
name: v3_step4b_hardgate_scorer_impl_11jul
description: V3 Step 4b — 03.03 Hard-Gate + 03.04 scorer re-scale IMPLEMENTED behind default-OFF v3_hardgate_mode; off=byte-identical; offline parity tool built; STOPPED AT OFF; BUILT-but-UNPUSHED
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Step 4b (11-Jul-2026): 03.03 Hard-Gate extraction + 03.04 scorer re-scale IMPLEMENTED behind a default-OFF flag. STOPPED AT OFF (nothing flipped to shadow/enforce). BUILT-but-UNPUSHED.** Implements the approved plan [[v3_step4_hardgate_scorer_plan_11jul]] with the ratified A1-A9 answers. First change to the LIVE scoring path — delivered byte-identical at OFF.

**Files:** NEW `screening/hard_gate.py`, `scripts/v3_hardgate_parity_recompute.py`, `tests/unit/test_hard_gate.py` (18), `tests/unit/test_v3_hardgate_parity.py` (6). MODIFIED `screening/secondary_screener.py` (v3 branches), `screening/step_executor.py` (+exclude_steps), `core/config_loader.py` (ScoringConfig v3 fields), `core/config_auditor.py` (B5 invariant), `config/scoring_weights.yaml` (v3 block), `main.py` (HardGate + screener wiring).

**Design (single-seam ADAPT, no fork):**
- **Flag `scoring.v3_hardgate_mode: off|shadow|enforce` (default "off" — quoted, YAML reads bare `off` as False!).** OFF = the existing 10-step scorer + 60/80/65 thresholds run UNCHANGED (byte-identical live path). The v3 code only executes in shadow/enforce branches gated by the mode.
- **`screening/hard_gate.py::HardGate.evaluate`** — pre-scoring binary battery: at-circuit + circuit-proximity + freshness(60s, A4); **liquidity NO-OP (A8, spread_check stays scored)**. The pre-fill `_circuit_proximity_reason` was RELOCATED here as a shared pure fn; `secondary_screener._circuit_proximity_reason` now DELEGATES to it (OFF byte-identical, single source — no duplication). V3-playbook gates (confirmation/pullback/R:R/extreme) NOT built yet (later). Missing-data: proximity fail-open, missing triggered_at admits.
- **Re-scale is THRESHOLD-ONLY (A5):** 8 weights kept at Σ80 (scoring_weights.yaml 10 weights UNCHANGED; step_executor gets `exclude_steps={circuit_check,signal_age}` in v3). NEW score = `rescaled_total = Σ(raw·w kept present)/Σ(w kept present)×100` (shared helper in hard_gate.py, mirrors the proportional scorer; quality_scorer code UNCHANGED). v3 thresholds are SEPARATE keys `v3_min_pass_score 50 / v3_medium 56 / v3_high 75` — the OLD 60/80/65 keys stay, so reports/GUI/tests reading them are UNAFFECTED (A6). `rescaled_total`/`tier_for`/`rescale_min_score` shared by the live v3 path AND the recompute tool.
- **Modes:** OFF byte-identical; SHADOW runs the OLD path for the live decision + logs OLD-vs-NEW (`_log_v3_shadow_compare`, pure side-effect); ENFORCE (`_screen_v3_enforce`) runs the gate FIRST → 8-step → v3 thresholds → NO signal_age defense (gate owns freshness). Same ScreeningResult shape/status vocabulary.
- **A7 min_score:** INVENTORY = all 15 `config/strategies/*.yaml` are `min_score: 0` → re-scale (`new=1.25·old−25`) is INERT today; implemented for future non-zero overrides.
- **A9:** threshold ordering high>medium>min_pass enforced BOTH in `config_loader.ScoringConfig` model_validator (fail-fast at load) AND `config_auditor` B5 (advisory BLOCK), for OLD + v3 sets.

**Parity proof (G2, `scripts/v3_hardgate_parity_recompute.py`):** deterministic OFFLINE recompute from persisted `screener_results.step_results_json` — reconstructs OLD (cross-check vs stored), the gate outcome, and NEW; classifies UNCHANGED/FLIP_PASS/FLIP_FAIL/TIER_SHIFT/NOW_GATED; confirms flips ⊆ explained residual (signal_age==0.5 OR circuit_check==0); DATA-FITs thresholds around 50/56/75 to minimize flips. **Synthetic self-demo: zero-unexplained, fit picked min_pass=53.** ⚠️ **BINDING real-data run PENDING on a VM backup** (local DB has 0 screener_results rows) — that flip-set report + final data-fit thresholds are the artifact for Web Claude+ChatGPT+Rama sign-off BEFORE any shadow/enforce flip.

**Acceptance gates:** **G1 (off byte-identity)** — existing screener/scorer/step_executor/nocil/config tests pass UNCHANGED + explicit `test_off_mode_byte_identical_to_no_v3`. **G3 (regression)** — full suite **4459 pass / 41 fail** (the 41 = PRE-EXISTING PC-env baseline [[pc_test_env_hygiene]]; +24 new tests); **test_main clean-vs-dirty stash-diff IDENTICAL (26==26) → zero new failures**. paper==live (pure gate/helpers, no mode branch). 222 changed-area tests pass.

**STOPPED AT OFF — no live behaviour changed; nothing flipped.** BUILT-but-UNPUSHED (with Steps 1-3). Docs: SYSTEM_MAP.md, PATHS.md, ledger. **NEXT (Rama/off-market, AFTER the VM parity artifact is signed off): push → flip to shadow (soak) → flip to enforce.** Then the later V3 playbook gates (confirmation/pullback/R:R/extreme) + 03.05-03.09.
