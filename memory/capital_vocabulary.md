---
name: capital-vocabulary
description: "PERMANENT doc rule (19-Jul, from Rama): live ACTUAL CAPITAL Rs 9,875.60, 70/30 intraday(MIS)/delivery(CNC); broker 5x MIS / 1x CNC; the SYSTEM IS UNAWARE of leverage and sizes against UNLEVERED capital. Four quantities diverge — always label which: ACTUAL CAPITAL / BUYING POWER / RISK CAPITAL / POSITION EXPOSURE."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-08-08T11:13:28.764Z
---

> ## 🔧 CORRECTED 08-Aug-2026 — **"THE SYSTEM IS UNAWARE OF LEVERAGE" IS TOO STRONG.**
>
> **(S) `position_sizer.py:475`: `margin_per_share = entry_price / leverage`, feeding
> `qty_by_capital`.** ⇒ **`leverage_map` IS read and IS applied — to exactly ONE of the
> three candidate quantities.** `qty_by_risk` and `qty_by_concentration` are unlevered.
>
> ⭐ **The old wording is right about the OUTCOME and wrong about the MECHANISM**, and the
> difference matters: *"unaware"* implies wiring the 5× in would be an ADDITION, when it
> is already wired and simply never binds *(492/492 samples bound on concentration, 0
> ties)*. ⛔ **A build that "adds leverage to sizing" on the strength of that sentence
> would put a SECOND levered term on a path that already has one.**
>
> ✅ **USE:** *"the system READS leverage but sizes against UNLEVERED capital IN
> PRACTICE — `leverage_map` applies ONLY to `qty_by_capital`, which is not the binding
> constraint."* 🔴 **And Rama's model (`qty = capital-per-scrip ÷ SL points`) differs
> from the code by ~140× at ₹10k unless its numerator is a RISK BUDGET — that numerator
> is the one thing that must be named before any sizing build.**
> → `docs/audit/sizing_model_questions_08aug2026.md`

> ## ⚠️ RE-MEASURED 27-Jul-2026 — **Rs 9,875.60 IS NOT A CONSTANT. IT IS A DAILY MEASUREMENT.**
>
> It is the broker's opening balance, written as the day's `INIT` row in `fm_ledger`, and it moves
> with every day's P&L:
>
> | 19-Jul | 21-Jul | 22-Jul | 23-Jul | 24-Jul | 27-Jul | **28-Jul** |
> |---|---|---|---|---|---|---|
> | 9,875.60 | 9,858.73 | 9,838.00 | 9,852.30 | 9,865.30 | 9,871.80 | **9,872.30** |
>
> ⭐ **28-Jul measured live at the boot: `fund_manager.rehydrate_complete → total: 9872.3`.** That
> log line is the cheapest daily read of ACTUAL CAPITAL — no DB query needed.
>
> ⭐ **THE FIX IS NOT TO RE-PIN IT TO 9,871.80** — that just restarts the same decay. It is
> [[feedback-no-fixed-test-baseline]]'s class: **a number pinned where a property is meant.**
> **THE PROPERTY: actual capital is the latest `INIT` row of `fm_ledger`, re-read, not remembered.**
> `SELECT amount FROM fm_ledger WHERE entry_type='INIT' ORDER BY date DESC LIMIT 1`
>
> ✅ **The derived threshold is unaffected**: 3 % × 9,871.80 = **Rs 296.15**, so "≈ Rs 296" still
> holds to the rupee — the 8-day drift is ~Rs 4. ⚠️ But that is luck, not design: a deposit or a bad
> week moves the base, and every document quoting Rs 9,875.60 would still say Rs 296.
> ⭐ Treat the ~Rs 9.8k figure as an **order of magnitude**, never as a value to compute against.
> **RULE: read a threshold's BASE from the ledger before computing against it**, exactly as
> [[dual-daily-loss-mechanism]] already says to read the threshold itself from code.

> ## ⚠️ RE-SWEPT 28-Jul — THE 27-Jul SWEEP BELOW WAS RIGHT ON **CODE**, INCOMPLETE ON **DOCS**
>
> It checked the two operator artefacts and the **dated** audit reports and concluded "nothing
> load-bearing." ⭐ **The class it missed is the one a date does not freeze: UNDATED, PRESENT-TENSE
> authorities.** Five, all quoting the 19-Jul ₹9,875.60:
>
> | where | why it is the load-bearing shape |
> |---|---|
> | **`docs/SYSTEM_MAP.md:76`** | states "ACTUAL CAPITAL Rs 9,875.60" as a **PERMANENT doc rule** — the line every other doc cites. The 27-Jul box credited SYSTEM_MAP for stating the *limit* as a %, and missed that it pins the *base* as a constant |
> | **`docs/audit/MONDAY_POST_SESSION_CHECKLIST.md:29`** | "≈ Rs 296 (3 % × Rs 9,875.60)" in a checklist **re-read every Monday** — not a dated report |
> | **`docs/audit/slice25_execution_plan_27jul2026.md:241,244`** | ":244 *reviewed against* ₹9,875.60" is a **review basis**. Written 27-Jul quoting the 19-Jul figure |
> | `docs/decisions/02_d1_concentration_sizing.md:8` | "~Rs 990 = 10 % of ~Rs 9,875" — **D1 is an OPEN decision**; its numbers are what Rama decides on |
> | `Downloads/MASTER_PENDING_REVISED_27-Jul*` (both) | tagged **`[MEASURED]`**, which makes a stale figure read as authoritative |
>
> ✅ **No conclusion moves today** — 3 % × 9,872.30 = **₹296.17** vs ₹296.27. Defects in FORM, not
> outcome. ⚠️ The exposure is structural: a deposit or a bad week breaks all five at once and
> nothing says so.
>
> ## ⛔ A HYPOTHESIS I CHASED AND **REFUTED** — do not re-raise it
>
> `human_order_margin_tolerance: 5000.0` is an absolute at **50.6 % of capital** — worse than any
> drift_handler rung. It widens the band at `order_reconciler.py:3397`, and the `return None` at
> `:3399` sits ABOVE the `CapitalDriftDetected` publish, so it looks like it swallows the whole
> ₹250/1,000/2,500 kill ladder. **IT DOES NOT.** `_ESCALATING_SOURCES` (`capital/drift_handler.py:65-69`)
> = `{fund_manager, fund_manager_self_check, fund_manager_bucket_overflow}` — **`order_reconciler`
> is NOT in it**, so that publisher was never a kill path. The ladder stays reachable via
> `sync_from_broker`, which publishes on any change **> ₹1.0**, un-gated. ⇒ ₹5,000 costs **alert
> sensitivity on one non-escalating source**, not kill coverage. The config comment is accurate.
>
> ## ✅ SWEEP DONE 27-Jul — the CODE half, re-verified independently 28-Jul
>
> Asked of every hit: *decorative, or does something DEPEND on it?* (A stale figure in prose is
> untidy; in a **threshold or precondition** it is a defect.)
>
> | where | verdict |
> |---|---|
> | **CODE** | ✅ **capital is READ, never assumed** — `fund_manager._total` initialises to `0.0` and is only ever set from `broker_balance` (`:440`, `:1393`). **No hardcoded capital, no fallback default.** Not the `product="MIS"` / `_CONFIG_FILES` shape. |
> | **operator artefacts** (`T2_RUNBOOK_29-JUL`, `TUESDAY_28-JUL_CARD`) | ✅ **quote no capital figure at all** — the best possible result for the documents read under pressure |
> | `SYSTEM_MAP.md` | ✅ states the limit as a **percentage** (`daily_loss_limit_pct = 0.03`) and records that the absolute was DELETED 24-Jun. One rounded "−Rs 300" in a headroom calc; conclusion robust (18.8 % vs 19.07 % at the real Rs 296.15). |
> | dated audit reports | ✅ correctly FROZEN — "opening was 9857.30 on 21-Jul" is a fact about 21-Jul, not a claim about today |
> | `candle_retention_…_19jul` B4 | ✅ self-labelling — "computed against the **current** unlevered regime (≈ Rs 9,875)" and says to re-run if leverage is modelled |
>
> ⚠️ **ADJACENT, RECORDED NOT A DEFECT:** `drift_handler` escalates on **absolute** rupees —
> `log_only 250 / soft_kill 1,000 / hard_kill 2,500`. Correctly absolute (a book-vs-broker
> **discrepancy** is not a risk fraction), **but calibrated against a ~Rs 10k account**: at
> hard_kill that is 25 % of capital today. ⭐ **If capital ever changes materially, these three
> change meaning silently** — they are the one place a capital move would be felt without anything
> saying so.

**PERMANENT DOCUMENTATION RULE (Rama, 19-Jul-2026; ChatGPT concurs).** Live **ACTUAL CAPITAL =
Rs 9,875.60 _as measured 19-Jul-2026_** (see the box above — it is a daily figure), split
**Intraday (MIS) 70% / Delivery (CNC) 30%**. The broker applies **5× buying power to MIS, 1× to CNC**. **⭐ THE SYSTEM DOES NOT KNOW ABOUT THE 5× — it sizes against UNLEVERED capital**,
so a Rs 10,000 MIS position the broker margins at Rs 2,000 is treated as Rs 10,000.

Four quantities were interchangeable at 1× and now diverge — **every rupee figure in any document must
say which one it means:**
- **ACTUAL CAPITAL** — Rs 9,875.60. The daily-loss threshold's base (3% ≈ **Rs 296**; the ledger INIT
  rows showed Rs 9,995–10,040, matching Rama's independent Rs 9,875.60). [[dual-daily-loss-mechanism]]
  [[e4-w10-outcome-impact-19jul]]
- **BUYING POWER** — capital × leverage (5× MIS, 1× CNC).
- **RISK CAPITAL** — what is at risk on a position (entry → stop).
- **POSITION EXPOSURE** — the notional value of the position.

**⚠️ Documentation rule ONLY — do NOT design, model or build anything about leverage/margin/Slice 2.5**
until Rama scopes it. Recorded because a Rs 10,000 MIS position now has four different "sizes."

Related: [[e4-w10-outcome-impact-19jul]] [[capital-chain-binding-constraint-analysis-13jul]]
[[dual-daily-loss-mechanism]] [[capital-operational-note]]
