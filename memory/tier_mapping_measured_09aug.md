---
name: tier-mapping-measured-09aug
description: "Rama's 50-54/55-59/60+ tier mapping MEASURED against frozen build 65b7196 — intraday doubles, delivery barely moves, and the mapping is only expressible if min_pass_score drops to 50."
metadata: 
  node_type: memory
  type: project
  originSessionId: 47b06b64-d65c-4b31-9c0d-e9517c6a78bf
  modified: 2026-08-09T14:34:12.161Z
---

# 📐 TIER MAPPING — MEASURED, ⛔ NOTHING BUILT

## §2.1 ✅ THE FROZEN BUILD'S ACTUAL VALUES — read from the REF, ⛔ not the dirty worktree
**(P) `git show 65b7196:` and `git show main:`.** ⭐ **The card's recollection was RIGHT for the frozen build and I confirm it; ⛔ but `main` is a THIRD state it did not name.**

| | `tier_multipliers` (intraday) | `delivery_tier_multipliers` | thresholds |
|---|---|---|---|
| **frozen `65b7196`** | HIGH 1.0 · MED **0.70** · LOW **0.50** | HIGH 1.0 · MED **0.85** · LOW **0.70** | intraday 60/65/80 · delivery 60/60/63 |
| **deployed `main`** | HIGH 1.0 · MED 0.70 · LOW 0.50 | 🔴 **KEY ABSENT** ⇒ delivery falls on the intraday family ⇒ **LOW 0.50** | intraday 60/65/80 only — ⛔ **no delivery thresholds exist** |

## 🔴 THE CORRECTION THAT MATTERS — DELIVERY IS NOT AT `0.70`, AND CANNOT BE
**Ceiling 65, `min_pass` 60 ⇒ every passing score is in [60,65].** With delivery thresholds **60/63**: **[60,63) → MEDIUM 0.85 · [63,65] → HIGH 1.00.** ⛔⛔ **DELIVERY `LOW` (0.70) IS UNREACHABLE BY CONSTRUCTION** — `config_loader.py` validates delivery as `high > medium >= min_pass` *(looser than intraday's strict chain, deliberately)*, and its comment forbids "fixing" it. ⇒ **the card's `₹350 → ₹500` prices a multiplier the shipping build cannot produce.**

## 📏 §1 — WHERE IT ACTUALLY BITES (⚠️ all at `perf_weight = 1.0`, ₹10,000 reference)
**`qty = floor(allocation ÷ entry_price)`** *(the long risk form is algebraically this; `position_sizer.py` says so)*. **Intraday alloc `35,000/6 = ₹5,833.33` · Delivery alloc `3,000/6 = ₹500.00`.**

| | before | after (60+→100%) | factor |
|---|---|---|---|
| **INTRADAY 60-64** | 0.50 → ₹2,917 | 1.00 → ₹5,833 | 🔴 **×2.00** |
| **INTRADAY exactly 65** | 0.70 → ₹4,083 | ₹5,833 | ×1.43 |
| **DELIVERY 60-62 vs FROZEN** | 0.85 → ₹425 | ₹500 | **×1.18** |
| **DELIVERY 63-65 vs FROZEN** | 1.00 → ₹500 | ₹500 | ⭐ **NO CHANGE** |
| **DELIVERY vs DEPLOYED `main`** | 0.50 → ₹250 | ₹500 | ×2.00 |

🔴 **§1.1's PREMISE IS REFUTED: THE CAPS NEVER BIND, AT ANY PRICE.** Max order at mult 1.0 = **₹5,833** vs concentration **₹7,000** and position-value **₹8,750**; delivery **₹500** vs **₹600**/**₹750**. ⇒ ⛔ **there is NO price above which "the multiplier starts deciding" — it decides EVERYWHERE, so the intraday doubling applies across the WHOLE price range, not just dear shares.** ⭐ Corroborated by the config's own comments *("20% sits just ABOVE the 1/6 = 16.7% allocation … only catches an anomaly"; "₹8,750 vs a ₹5,833 order")*.
⭐ **AND THE "WIDER TRADEABLE BAND" IS NOT DELIVERY-ONLY:** intraday reject-to-zero moves **₹2,917 → ₹5,833** — far larger in rupees than delivery's ₹425 → ₹500.
⚠️ **THE DOUBLING IS AN UPPER BOUND, ⛔ NOT UNIFORM:** `effective_mult = min(1.0, tier × perf_weight)`, `perf_weight ∈ [0.5, 2.0]`, `dynamic_by_winrate: true` ⇒ ×2.00 holds for any symbol at `perf_weight ≤ 1.0` and decays to **×1.00 at perf_weight = 2.0**, where a top strategy ALREADY reaches full allocation. **The realised distribution is VM-side.**

## 🔑 §2.2 + THE STRUCTURAL FINDING — WHY THE MAPPING NEEDS `min_pass = 50`
**Assignment and multiplier live in TWO files, as suspected: thresholds in `config/scoring_weights.yaml`, multipliers in `system_config.position_sizing`; `capital/pipeline_policy.py` joins them per pipeline** *(delivery `:383-384/:329`, intraday `:418-419/:392`)*.
⭐⭐ **Rama's table maps ONTO this machinery EXACTLY — but only at `min_pass_score = 50`:** `medium=55 · high=60 · LOW 0.75 · MEDIUM 0.85 · HIGH 1.00`, and the validator `high > medium > min_pass` reads `60 > 55 > 50` ✅.
🔴 **At today's `min_pass = 60` it is NOT expressible by thresholds:** `high > medium > 60` forces `high ≥ 62`, so **some of [60,65] is ALWAYS below HIGH.** ⇒ **"60+ → 100%" is reachable ONLY by setting the MULTIPLIERS to 1.0** — config-only *(no logic rewrite)*, ⛔ **but it makes tiering a NO-OP in both pipelines.**
⇒ 🔑 **WHAT WAS APPROVED IS NOT "three tiers arriving": it is TIERING SWITCHED OFF at today's pass mark, with a three-band table pre-loaded for the day `min_pass` drops to 50.** ⚠️ Bands `50-54`/`55-59` are **FUTURE-PROOFING**, ⛔ not working tiers — the "configured, started, inert" class.

## ⛔ §2.3 / §2.4 — `NOT MEASURED`, AND THE REASON IS THE PC
**(P) the local snapshot `data_store/trading_system.db` holds `trades=0`, `orders=0`, `signals=0`** — all three checked, and no scored-signal corpus exists elsewhere on the PC *(no forward-shadow or screened-stocks artifact; only docs)*. ⇒ ⛔ **the corpus count of delivery signals priced between the two thresholds, and any "on real entries" before/after, are VM-SIDE ONLY.** ⭐ **`NOT MEASURED` with its reason IS a score; ⛔ an example dressed as a corpus is not.** 📌 Corroborates `N9-26`.

⛔ **NOTHING BUILT, no config value changed, `min_pass_score` untouched, the frozen build unamended. §3 is Rama's — both options were put with numbers, ⛔ neither chosen.**

See also [[two-pipeline-split-08aug]] · [[capital-vocabulary]] · [[screener-score-ceiling-65]] · [[tick4-blocked-on-sizing-deploy-09aug]]

## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 620 B (budget 450 B). The index now carries a hook and this link.

- 📐🔴🔝 **[TIER MAPPING — ⛔ *"DELIVERY IS UNCHANGED"* IS TRUE **ONLY ON `65b7196`'s TREE**, AND THIS LINE HAD DROPPED THE BASE (re-measured 20-Aug)](tier_mapping_measured_09aug.md)** — ⭐ that file's own table already says it: on **DEPLOYED `main` the `delivery_tier_multipliers` KEY IS ABSENT ⇒ delivery falls on the INTRADAY family**, so a tier change moves **BOTH** books (`×2.00`, its own row). ⛔ `3cf3729`'s *"INERT BY CONSTRUCTION"* tag describes ITS tree. ✅ On `65b7196`: intraday-only, thresholds `60/60/63`, LOW unreachable. ⛔ Caps never bind. → [[no-two-pipeline-split-deployed-20aug]]

## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 359 B (budget 300 B). The index now carries a hook and this link.

- ⚠️🔢 **A ROUTING SLIP CAUGHT: `0.70/0.70/0.70` is NOT the deployed triple.** Deployed = **`1.0/0.70/0.50`**, measured 3 ways (VM config file · the running process's boot emission · `config_snapshots` id 37). ⛔ A FLAT triple = spread **1.00× = TIERING OFF ENTIRELY** — a different policy, ⛔ not a rounding slip. [[tier_mapping_measured_09aug]]
