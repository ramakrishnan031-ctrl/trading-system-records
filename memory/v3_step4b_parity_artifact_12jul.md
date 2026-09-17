---
name: v3_step4b_parity_artifact_12jul
description: "V3 Step 4b BINDING parity artifact — offline recompute over 114,807 real screener_results rows; PARITY_OK, all 114 flips explained; two real tool bugs fixed. Awaiting ChatGPT sign-off before shadow flip"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Step 4b — BINDING PARITY ARTIFACT produced 12-Jul-2026 (I located the data + ran it; Rama reviews outputs only, per the bridge rule).** Follows [[v3_step4b_hardgate_scorer_impl_11jul]]. Read-only, no live change, flag stays OFF, nothing pushed.

**Discrepancy explained (why ChatGPT couldn't find/run it):** the parity script IS present — `D:\Projects\trading-system\scripts\v3_hardgate_parity_recompute.py` — but Step-4b is **built-but-unpushed**, so it's ONLY in the PC dev work-tree, NOT on the VM/bare repo where it was looked for. And the local dev DB `data_store/trading_system.db` has **0 screener_results rows** (empty dev DB, not the data source). NOT missing — unpushed + wrong-place + empty-dev-DB. Both resolved by me (no Rama action).

**Data source:** VM SSH (passwordless `trading-vm`, off-market weekend = quiescent). Live has 114,807 screener_results rows (12-Jun→10-Jul). I built a **slim read-only extract** (only id/signal_id/score/tier/status/step_results/eligible_score) from the backup `data_store/backups/trading_system-2026-07-11.db` → `/tmp/sr_slim.db` (33 MB) → SCP'd to the PC scratchpad → ran the tool against the copy → removed the VM temp. Never touched the live/production DB.

**TWO REAL TOOL BUGS found + root-fixed (the recompute was wrong before this):**
1. **Column name:** the tool read `step_results_json` but the actual `screener_results` COLUMN is `step_results` (the persist PARAM was `step_results_json`; the column is `step_results`). Also `screener_results` has NO `direction` column → dropped the circuit-proximity re-derivation from the gate reconstruction (proximity is enforced PRE-scoring, so any row WITH step_results already passed it → zero flips; the only NOW_GATED source is at-circuit `circuit_check==0`).
2. **Baseline threshold:** the tool used the stored `status` as "OLD" — but `min_pass_score` was **55 from 06→10-Jul** (dropped 06-Jul `8a3e0b7`, restored to 60 on 10-Jul `61ae9cc`), so ~23k rows scored 55-59 are stored PASSED yet would REJECT at today's 60. Fixed: **RECOMPUTE OLD at the CURRENT config (60/80/65)** + model the signal_age defense-in-depth, comparing OFF-today vs enforce-today. This cut false FLIP_FAILs from 23,299 → 10.

**THE ARTIFACT (thresholds 8-step scale: min_pass 50 / medium 56 / high 75 — the plan's fresh-reference):**
- corpus = 114,807 rows (VM backup 2026-07-11, 12-Jun→10-Jul).
- **UNCHANGED 114,693 (99.90%)** · **FLIP_PASS 104** · **FLIP_FAIL 10** · TIER_SHIFT 0 · NOW_GATED 0.
- **PARITY_OK = True — ZERO UNEXPLAINED.** All 114 flips explained:
  - **104 FLIP_PASS = age-band (signal_age==0.5):** 30-60s signals that OLD score-rejected only due to the −5 age penalty; freshness is now a binary GATE so they pass on merit (A2-accepted intended improvement).
  - **10 FLIP_FAIL = rounding-boundary:** `old_total==60` exactly (a8≈39.55; 59.5→60 rounds up to pass) while the ÷80 re-scale rounds to 49 (just under 50). Inherent ÷100-vs-÷80 integer-rounding sliver (0.009%); all fresh (age=1.0) non-circuit. A precise, defensible THIRD residual category.
- **Harness cross-check PASSED:** recomputed OLD full-total == stored `score` on ALL scored rows (0 mismatches) — validates the recompute mirrors the engine's proportional formula.

**Interpretation:** the OFF→enforce transition preserves the pass/tier decision on 99.90% of a month of real signals; the 0.10% that move are ALL the intended age-band admissions + a negligible rounding edge — nothing unexplained, nothing lost that shouldn't be. Confirms A1 (50/56/75 fresh-reference works) + A2 (residual accepted).

**Tool now correct + tested** (`tests/unit/test_v3_hardgate_parity.py`: +recompute-at-current-config + rounding_boundary tests; 8 pass). **STILL default-OFF; nothing flipped; nothing pushed.** Artifacts (flip-set report + counts + console + slim DB) in the session scratchpad. **NEXT: hand this artifact to Web Claude + ChatGPT for sign-off → THEN (Rama/off-market) push → flip `v3_hardgate_mode` off→shadow (soak) → enforce.** Related [[risk_config_tighten_10jul]] (the 55→60 history that confounded the raw stored status).

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 331 B (budget 300 B). The index now carries a hook and this link.

- 🧭✅⚖️ **[Step 4b BINDING PARITY 114,807 rows PARITY_OK](v3_step4b_parity_artifact_12jul.md)** — @50/56/75 UNCHANGED 99.90% / FLIP_PASS 104 age-band / FLIP_FAIL 10 rounding / 0 UNEXPLAINED. [[v3_step4b_hardgate_scorer_impl_11jul]] (impl, default-OFF `v3_hardgate_mode`) · [[v3_step4_hardgate_scorer_plan_11jul]] (plan).
