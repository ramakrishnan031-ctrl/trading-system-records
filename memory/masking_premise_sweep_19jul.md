---
name: masking-premise-sweep-19jul
description: "19-Jul READ-ONLY+docs: swept the REFUTED 'a size multiplier is masked by the concentration cap' premise from the record (corrected 5 docs with dated legible notes) and checked whether the refutation moves any reachability verdict. VERDICT: it moves NONE. The 4 sizing-guard UNREACHABLE verdicts rest on their own algebra/config/pinning, not masking; batch-4 reasoned the post-cap mechanism CORRECTLY — decision file 06 misattributed the masking claim to it. #06's gate corrected to merit(D2/D3)+leverage, NOT the cap. Memory-palace snapshot taken → compaction precondition MET."
metadata:
  node_type: memory
  type: project
  originSessionId: 35afb62d-26b3-4c8b-a62f-fa6b431ad21b
  modified: 2026-07-20T14:23:53.037Z
---

**MASKING-PREMISE SWEEP + REACHABILITY RE-CHECK (19-Jul-2026, READ-ONLY + docs).**
Report `docs/audit/masking_premise_sweep_19jul2026.md`. Follows the PerformanceAllocator measurement
[[candle-retention-perfallocator-feasibility-19jul]] which refuted "a size multiplier is masked by the
concentration cap that binds 100% of trades" (perf_weight is a **post-cap multiplier**, changes final qty on
**233/298 = 78%** over [0.5,2.0], 151/298 over [0.8,1.25]).

## ⭐ A — THE PREMISE WAS A HALF-CORRECTED RECORD; SWEPT (5 docs, dated + legible)
Corrected each occurrence with a dated note that leaves the superseded claim struck-through-but-readable (per
the record-correction discipline), NOT a silent rewrite:
- `docs/decisions/00_INDEX.md:27` — the **coupling section** ("#06↔D1: a size multiplier is masked …").
- `docs/decisions/06_performance_allocator.md` — 3 **body** bullets (What-is-known / What-is-unknown /
  What-changes-if-wrong); the top UPDATE block already refuted, the body still asserted.
- `docs/audit/decision_readiness_triage_19jul2026.md:26` — the **coupling paragraph** (`#06↔D1` → `#06↔merit(D2/D3)+leverage`).
- `docs/audit/decision_packages_19jul2026.md:63` — the **table cell** ("likely masked by the concentration cap").
- `docs/audit/e4_w10_outcome_impact_19jul2026.md:95` — the COMPUTABLE-NOW row → **COMPUTED: YES, 233/298.**
CLEAN (no correction): `sizing_interaction_impact_report_13jul2026.md:43` + `capital_sizing_audit_18jun` state only
the TRUE part ("concentration binds 100%" / "the Rs-cap never binds; concentration binds lower first") — never the
masking inference. `SYSTEM_MAP.md:1165` = false positive (unrelated try/except). Memory palace = CLEAN (no topic
file asserted it). PATHS.md = clean.

## ⭐ B — DOES THE REFUTATION MOVE ANY REACHABILITY VERDICT? **NO — it moves NONE.**
Reviewed the Q9 coverage matrix's 4 sizing rows (`q9_coverage_matrix_final_18jul2026.md`); each UNREACHABLE
verdict rests on its **own algebra/config/pinning**, not on masking:
- **Row 10 — max_position_value 40% cap = UNREACHABLE.** Position value = concentration arm (10%) × tier (0.5)
  ≈ 5% today; even at perf=2.0 the 2× ceiling caps it at ~2×10% = **20% < 40%**. Robust to perf_weight; batch-4
  memory §42-43 already reasoned the perf=2.0→20% case. **No move.**
- **Row 13 — M-C6 ZERO_MULTIPLIER SKIP = UNREACHABLE.** Reason = the **pinning** (`perf_weight ≡ 1.0`) + tier
  floor; even if wired, the clamp [0.5,2.0] keeps effective_mult ≥ 0.25 > 0. Matrix correctly cites the pinning,
  **not** the cap. **No move.** (§B2 target — confirmed no leak.)
- **Row 17 — concentration + >cap = REACHABLE (298/298).** The refutation *confirms* it. **No move.**
- **Row 18 group — risk/capital/lot-skew/BELOW_MIN/FLAT/explosion/2× ceiling = UNREACHABLE.** risk/capital arms
  never win the `min()` (own comparison, `qty_by_risk ≤ qty_by_concentration` in 0 rows); lot_size=1 ⇒ skew/lot
  dead; FLAT needs OFF-mode (enabled=true); the **2× ceiling is latent by the same pinning** (perf≡1.0 ⇒
  tiered ≤ raw). None invoke masking. **No move.**
**⭐ Batch-4 got it RIGHT** — it reasoned the post-cap mechanism correctly (`perf_weight=2.0 → 2× the
concentration arm; G14 40% cannot catch a 20% position`). **The masking claim was a later editorial gloss in
decision file 06 that MISATTRIBUTED itself to batch-4.** The lesson: a real refutation corrects a stated
*coupling* without touching the *verdicts* — do not let it over-propagate. (The separate, VALID population-bias
qualification — the upstream cap enriches the sizer population 1.45× in >Rs990 names — STANDS; it is about
population, not masking.)

## ⭐ #06's GATE, CORRECTED (carry everywhere)
#06 is **NOT** gated on the concentration cap. It is gated on the multiplier's **MERIT (D2/D3 — is there a
signal worth scaling by? the win-rate signal has no proven ranking power: M-S4 ρ+0.003, D3 OOS non-replication)**
+ the **sizing/leverage** picture (where it genuinely touches D1). Shelf-life caveat travels with it: 233/298 is
computed against **today's UNLEVERED sizing**; 5× MIS would change the regime (raw_qty grows ⇒ binds on *more*).
Do NOT wire it / do NOT recommend wiring — #06 is Rama's; its merit is untouched by this batch.

## ⭐ C — MEMORY-PALACE SNAPSHOT TAKEN → COMPACTION PRECONDITION MET
The owed MEMORY.md compaction was blocked because the palace is not git-tracked and no backup existed (an
interrupted trim was undiffable). A timestamped snapshot is now taken on the PC (path recorded in the MEMORY.md
header note + the report). **Compaction still NOT performed — it waits for after Monday**, done unhurried and
diffed against a fresh snapshot then. The precondition (a diffable baseline exists) is now MET.

## Queue after Monday (unchanged) + Monday reminders
⚠️ **20-Jul: `check_scanner:703` CLOSED — REFUSED WITH EVIDENCE** (external Chartink, not local `/health`;
a 401 there is an anomaly). Real sibling = `scripts/preflight/checks/signals.py:28`. [[preflight-401-third-sibling-20jul]]
Boot-path pair (careful loop): live-seed extraction from `main()` + `check_scanner:703` (add `==401`, do NOT
escalate) · live-path quote observability · 403 signal-count (~338k) · deferred `event_type` / `Rejected
(Sizing/Capital)` label / `build_taxonomy_map()` · wave-7 backlog · degenerate Rs 0.29 SL · **MEMORY.md
compaction (snapshot now taken).** ⚠️ MONDAY 20-Jul: 08:15 TOTP · 08:15-09:00 boot · **pre-10:00 403s NORMAL** ·
10:00 entries · 15:15 cutoff · 15:17 squareoff · 15:50 eod_cleanup (0 rows) · 16:22 registry · **18:15 fwd shadow
OOS day 4 — check real `sim_R`, not nulls.**

Related: [[candle-retention-perfallocator-feasibility-19jul]] [[q9-batch4-sizing-reachability-18jul]]
[[consecutive-losses-gate-wired-19jul]] [[feedback-verify-the-finding-premise]] [[feedback-live-vs-latent-findings]]
[[throttle-selection-record-correction-19jul]] [[decision-packages-19jul]]
