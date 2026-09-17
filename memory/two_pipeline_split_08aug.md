---
name: two-pipeline-split-08aug
description: "Delivery and intraday became two independent books on 08-Aug-2026 — separate limits AND separate counters, one resolver, measured exposure change. BUILT on a branch, not deployed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 35a1c3dd-75a3-42ce-bdc5-d5e981dad58a
  modified: 2026-08-08T09:12:17.150Z
---

# 🧭 TWO-PIPELINE SPLIT — `<BUILT 08-Aug · feat/delivery-config-split>` ⛔ NOT DEPLOYED

> **RAMA, 08-Aug-2026:** *"One system, one command centre — from signal receipt to order
> management to EOD report. But TWO PIPELINES, delivery and intraday, each trading on
> their OWN config settings. NEVER shared values. No combined metric, limitation factor,
> or setting."*

⛔ **NOT riding with F6.** Record: `docs/audit/delivery_config_split_08aug2026.md`.

## 🔑 THE TEST TO APPLY TO ANY GATE YOU TOUCH

**"Can a delivery trade change what intraday is allowed to do, or the reverse?"**
⛔ If yes, that gate is not split. ⭐⭐ **SEPARATING THE LIMITS IS THE EASY HALF — A
SHARED COUNTER WITH TWO LIMITS READING IT IS STILL A SHARED LIMIT.**

**FOUR couplings existed; only ONE was written down:** open-position count · daily trade
count · consecutive-loss streak (**one shared streak halted both books**) ·
🔑 **in-flight reservations — the one a limits-only build would have kept, because it
lives IN MEMORY, not in a table anyone can query.**

⭐ `risk_engine`'s `A5` note called the first *"INTENTIONAL asymmetric coupling … academic,
because capital binds long before these counts."* **Removed, not softened** — academic or
not, it is a delivery carry deciding whether an intraday entry may happen.

## 📐 ONE RESOLVER — `capital/pipeline_policy.py`

`resolve_pipeline_policy(product)` returns every effective limit **+ its source**.
⛔ **Branch on the RESOLVED BROKER PRODUCT, never on `trade_type`** — `trade_type` says
which products may trade TODAY, ⛔ not which policy an order uses.
⛔ **No `if DELIVERY:` in any gate** — a per-gate branch is a per-gate chance to forget one.
⭐ `policy_source=` is on **every** decision log + `main.py` prints both books at boot ⇒
proof the split is **LIVE**, not merely CONFIGURED.

## 💰 THE NUMBERS — MEASURED (ratios are capital-invariant)

- **INTRADAY daily loss REBASED onto the 70% bucket ⇒ TIGHTER by 30%**: 3%×total →
  3%×70% = **2.10% of total** (₹3,000→₹2,100 at ₹1L). ⭐ A consequence of "no shared
  purse", ⛔ **not a separate tightening decision.**
- **DELIVERY daily loss: NEW, its own purse** — 3% of the 30% bucket = 0.90% of total.
- 🔴 **DELIVERY POSITION SIZE ×1.50–1.53 (MEDIUM) / ×1.7–1.8 (HIGH) — A REAL EXPOSURE
  INCREASE, ⛔ not a bug fix.** ⭐⭐ **The rise is almost ENTIRELY THE TIER, not the
  percentages**: rebasing onto the 30% bucket makes the risk term SMALLER in rupees
  (0.6% of total vs 1%) and cuts the max-position-value ceiling 400k→120k.
- **CAPS: 5+3 = 8 concurrent · 10+5 = 15/day — both CORRECT.**

## 🎯 THE TIER MECHANISM — why 60/60/63 looks odd

**(P) scorer's MEASURED ceiling is 65; intraday HIGH is 80 ⇒ HIGH UNREACHABLE ⇒ every
delivery position has been sized LOW ×0.50 since delivery went live** — that is the
8→4 halving on 07-Aug. Delivery 60/60/63 puts both tiers inside the achievable band.
⛔ **THE ENTRY GATE IS NOT LOOSENED — delivery's pass mark is the same 60.**
⭐ Delivery LOW is unreachable **by construction** (medium == min_pass) ⇒ delivery's
ordering is `high > medium >= min_pass`, deliberately looser than intraday's strict chain.

## ⛔ NULL FAILS CLOSED — the scaffold's promise is REVERSED

The V3 03.06 comment said *null ⇒ use the global*. **Correct for an inert scaffold,
unsafe now.** With delivery ACTIVE a null delivery value is a **STARTUP VALIDATION
ERROR** — a fall-back would size a delivery trade off the intraday book's policy with
nothing downstream able to tell. ⭐ Conditional on ACTIVE so an intraday-only deployment
still boots.

## 🔴 STOP-AND-REPORT FIRED (§3.7) — THE CAPS WERE **NOT** RENAMED

`max_open_positions` / `max_daily_trades` are now **INTRADAY-ONLY in behaviour**, but the
KEYS are unchanged: **9 readers still present them as global.** ⚠️ **The live-facing one:
`ops_dashboard/.../capacity.py` labels them `global/concurrent` and compares against a
count of ALL positions ⇒ it will read "7/5 open" and look breached when nothing is,
on the first day a delivery position is carried.** Also `config_auditor.py:442`'s
cumulative-risk audit silently became intraday-only. 🔴 **OWED RAMA: rename + fix 9 sites,
or keep the names and fix the labels.**

## ⚠️ STILL CROSS-PIPELINE — named, ⛔ not resolved

🔴 **`one_trade_per_symbol_direction_per_day: true` is THE ONE genuinely cross-pipeline
GATE left standing** — a delivery entry blocks an intraday entry on the same
symbol+direction, and vice versa. ⛔ **That is OPEN-1, unruled.**
Also: `max_sector_exposure_pct` (one cap, both books, on total) · the unrealized-MTM term
in DAILY_LOSS is **not** pipeline-scoped ⇒ ⛔ **resolve before ever flipping
`daily_loss_include_unrealized` ON** · every count reads **DB ROWS, not broker reality**.

## 🔴 THE GATE FOUND THREE DEFECTS IN THIS BUILD — TWO OF THEM MINE

**Run 1: `RC=1`, 21F/5603P. SET-compare vs the §8.12 nine: 0 baseline-only, 12 NEW.**
⛔ **None labelled "known PC-env" — that is a label, not a diagnosis.**
- **10× encoding** — 🔴 **MINE.** `scripts/forward_shadow_record.py:47` reads
  `config/scoring_weights.yaml` with a bare `Path.read_text()`, **no `encoding=`**; my
  glyphs contain `0x90`/`0x9B`, which **cp1252 cannot decode**. ⚠️ **My first reading was
  WRONG** — the file already held **51** non-ASCII bytes cp1252 decodes fine, so it is
  **the specific bytes**, not non-ASCII as such. ⇒ **KEEP `scoring_weights.yaml` ASCII.**
  🔴 **The unencoded read is the REAL defect, RECORDED NOT FIXED — it sits on the 18:15
  forward-shadow path whose output CANNOT BE REGENERATED.**
- **1× `snapshot` 9 fields** — 🔴 **MINE.** I added 4 keys; **RE11 is LOCKED**. ⭐
  **Reverted: widening a locked contract to make a new feature convenient should cost
  its OWN decision, not ride inside another.** §3.5 is satisfied by the log.
- **1× streak "one data source"** — the assertion was a **TEXT PROXY**
  (`count("recent_trade_pnls")==1`). ⭐ **PROPERTY VERIFIED BEFORE THE NUMBER WAS
  TOUCHED:** one def + one call of `_count_trailing_losses`, one selection point — both
  still true. Rewritten to those invariants.

**Run 2: `RC=1`, 9F/5616P/4S in 896 s — the set IS the baseline nine, LINE FOR LINE.**
⭐ **Pass count reconciles with no remainder: `5582 + 34 = 5616`** — the check a
failure-set compare CANNOT make (it says nothing about a test that stopped being
COLLECTED). 🏷️ **REGRESSION ACCEPTED — zero NEW; 9 known baseline; RC=1 by convention.**

## 🧪 TESTS — 34, RED-first BY EXPERIMENT

Reverting only the **behavioural** half while keeping config+resolver ⇒ **13 failed /
20 passed.** ⭐ The 20 green are exactly the resolver/config tests — the experiment
isolates what the CODE change buys from what the CONFIG change buys. ⛔ Deleting the new
module gives only an ImportError, which proves nothing about the assertions.
⚠️ **PAPER CANNOT exercise a CNC round trip, T+1 settlement, or a carry becoming a
holding.** Test 15 seeds a carried row in SQL ⇒ proves the **COUNT**, ⛔ not settlement.

## ⚠️ THE ONE JUDGEMENT CALL — intraday sizing did NOT rebase

§3.4 (*"every intraday percentage against the intraday bucket"*) and test 12 (*"MIS sizing
byte-identical"*) **cannot both hold**. Resolved: delivery sizing → its bucket · intraday
sizing → **TOTAL, unchanged** · intraday **daily-loss** → rebased (§3.4's only NAMED
consequence). Recorded at `PipelinePolicy.sizing_base` with the one-line reversal.
🔴 **Rama's to overrule — rebasing intraday sizing too would cut every MIS position ~30%.**

Related: [[f6-deploy-authorised-08aug]] · [[rulings-1-2-taken-07aug]] ·
[[capital-vocabulary]] · [[paper-cannot-exercise-class-26jul]]
