---
name: min_score_floor_60_26jun
description: "min_score 0→60 set explicitly in all 15 strategy YAMLs (26-Jun); BUT the effective score floor was ALREADY 60 via the min_pass_score fallback — so this is an explicitness no-op, and the 60 floor is very aggressive (~2% of signals pass)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b445dff-c546-4ec1-b292-3ec665699a63
---

**min_score 0 → 60 in all 15 `config/strategies/*.yaml` (26-Jun-2026).** Score scale is
**0–100** (`screening/quality_scorer.py:3,95-96`); stored in `screener_results.score`.

**★ KEY FINDING — the backlog audit's "signals NOT filtered by score" was WRONG.** The
effective floor was **ALREADY 60**: `screening/secondary_screener.py:215-221` computes
`effective_min = strategy.min_score if strategy.min_score > 0 else min_pass_score`, and
`config/scoring_weights.yaml:22` `min_pass_score: 60`. So with min_score=0 the floor FELL
BACK to min_pass_score=60. Setting min_score=60 ⇒ effective_min=60 either way ⇒ **this change
is a behavioural NO-OP at the current min_pass_score=60.** Its only value is explicitness +
**decoupling** the per-strategy floor from min_pass_score (pins it at 60 even if min_pass_score
later moves). Trade-off: future lowering now means editing 15 YAMLs, not just min_pass_score.

**★ LIVE SCORE DISTRIBUTION (VM `screener_results`, 49,178 scored signals 12–25 Jun, read-only):**
min=0, **max=65**, median=57, avg=52.3. **Only ~2.4% (1,158) score ≥60**; 73% cluster at 50–59
(just below the floor). `eligible_score` (threshold actually applied) = **60 for 83%** (40,821
rows) — current state; was a temporary **55** on 16–18 Jun (7,044 rows, a TEMP deviation, since
reverted; 17-Jun passed 3,000 vs ~100–200/day at 60). On 60-floor days the pass rate is ~1.5–2%
(e.g. 19-Jun 37 passed/4,485; 25-Jun 98/5,418). **So the 60 floor — already live — rejects ~98%
of scored signals.** The scale tops out at 65, so 60 is near the ceiling = a HIGH bar.

**★ FLAGGED to Rama:** (1) the floor is already 60, so Monday is UNCHANGED by this edit; (2) the
60 floor is very tight (~2% pass) — if Rama wants MORE signals through, the lever is to LOWER the
floor (e.g. min_pass_score 55 → ~10× more passed on 16–18 Jun), not this edit; (3) the audit
mis-stated the floor as absent — corrected here.

No schema/code; config-only; parity (the strategy YAMLs are the SINGLE shared paper+live config —
no per-mode fork). Takes effect at the next boot (Mon 29-Jun 08:15; today is the Muharram holiday).
Branch `score-floor-60-and-ddpi-26jun`. See [[ddpi_enabled_26jun]], [[slice2_strategy_control_24jun]].
