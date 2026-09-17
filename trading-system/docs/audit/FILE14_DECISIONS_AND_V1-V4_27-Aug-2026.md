# FILE 14 — DECISIONS RECORDED · CORRECTIONS APPLIED · V-1…V-4 MEASURED

**27-Aug-2026 (Thu), ~10:3x–11:0x IST · market OPEN.**
🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S.

⛔ **§4 IS NOT IN THIS DOCUMENT.** FILE 14 gates the build at **17:45**; it is
~11:00 and the market is open. ⛔ No push, ⛔ no build, ⛔ no branch working-tree
operation, ⛔ no revert-trigger change, ⛔ no sector build, ⛔ no NI-16 build.
⭐ Everything below is **records + four read-only measurements**.

🔬 `origin/main` resolved BY MEASUREMENT at session time = **`bc9a9f5`**.
🔬 Merge-base re-verified = **`645728d`**. ⚠️ ROOT sits on
`feat/delivery-config-split`; every branch figure is read from git objects.

---

## 1 — DECISIONS RECORDED (D-1 … D-9)

⭐ Each carries rationale + a one-line reversal. ⛔ None waits.

| # | decision | rationale (measured) | ↩️ reversal |
|---|---|---|---|
| **D-1** | **Rollback TREE `75e637c` → `bc9a9f5`** | E-3: `STARTUP 3797 COLD` `08:15:27.356` > `ExecMainStart 08:15:15`; L-1 satisfied (`3794` was 26-Aug); 0 ERROR; kill auto-cleared; `NRestarts=0`; holdings clean | set TREE back to `75e637c` |
| **D-2** | **MIS planning basis = 3.5× total** | 👤 Rama's own stated model: ₹10,000 → MIS 70% = ₹7,000 × 5 = ₹35,000. `0.70 × 5.0 = 3.5` **is** that model | revert basis to total capital |
| **D-3** | **F2 splits: F2-CORE ships, F2-SIZING deferred** | conc. cap `0.10×TOTAL ≈ ₹1,054` → `0.20×BASIS ≈ ₹7,381` = **~7×**; concentration is the **unique** binding rung (V-4) ⇒ a 7× cap **is** a 7× size, at 38–39% WR vs ~43.5% breakeven | F2-SIZING is QUEUED, ⛔ not discarded |
| **D-4** | **Method = OPTION B, scoped to F2-CORE** | reimplement vs current main; `pipeline_policy.py` (420 lines, 0 collisions) transplants; ⚠️ FINDING 1 repaired first | switch to Option A per component |
| **D-5** | **K-1 = NOT a defect; conservative and correct** | ₹6.07/six rows 26-Aug = 0.057% of ₹10,567.60; ⭐ **V-4 now closes it completely** | switch to gross-P&L release |
| **D-6** | **F9 score-sector: leave as-is, PARKED — NON-CORE** | `_step_6` returns `0.5` for every symbol ⇒ a CONSTANT ⇒ ⛔ cannot change RANKING; scorer inverts above ~35 | wire or retire later, deliberately |
| **D-7** | **Revert trigger: wording UNCHANGED, stays DISARMED** | quantity **B**, rule **E**, `carry>0` met on **0 of 9,289** samples | reword only after a real T+1 carry |
| **D-8** | **NI-16 BLOCKED → QUEUED, ⛔ not built** | branch resolves it via `min(1.0, …)` inside the allocation; main is LIVE-but-LATENT (`perf_weight ≡ 1.0`) | rides with F2-SIZING |
| **D-9** | **Two operative audit files ship** | `RUNBOOK_n907_install_20-Aug-2026.md` (12 cmd-lines) + `OPS2_HANDOVER_RAMA_23-Aug-2026.md` (13); both absent from the VM | keep them PC-side |

🔴 **D-1 EXECUTED AS A RECORD ONLY** (zero runtime): the ledger's TREE line now
reads `bc9a9f5`, with old TREE · new TREE · reason · evidence · timestamp.
⛔ **The TREE is NOT advanced again to tonight's SHA** — ⭐ a push is not a boot;
tomorrow's 08:15 is.

---

## 2 — RECORD CORRECTIONS APPLIED (R-1 … R-10)

| # | correction | applied where |
|---|---|---|
| R-1 | **RECOVERED ≠ RE-EXECUTED.** The 08:00 session was preserved on disk; only the section depending on the **future** 09:15 window was missing, and it was recovered from the still-running VM | §7 of `SECTION_E_AND_F2_INVENTORY` already states this verbatim |
| R-2 | **E-4 UNPROVEN** — the bare phrase `strategy resolver` also returns 0, so absence cannot distinguish *did not fire* from *never appears* | already recorded; unchanged |
| R-3 | **E-6 UNPROVEN, and today was NON-DISCRIMINATING** — at 12.98 s even 15 s reads GREEN | already recorded; unchanged |
| R-4 | **E-5 PASS on BOTH legs, flat-book only.** `carry = 0` is ⛔ not carry correctness | §7 states it |
| R-5 | **F2 figures corrected: 48 ahead / 81 behind · 102 files / +12,168 / −1,107** | MEMORY.md + HAZARDS already carry this |
| R-6 | **OPTION C REFUTED BY MEASUREMENT** | §4 of the inventory |
| R-7 | **CONFIG_UNACCESSED = 388 — RECORDED, ⛔ NOT CHASED** | BOARD; ⛔ no attempt to "use" 388 keys |
| R-8 | **RESET_PNL 15:17:02 vs close 15:19:53 = a BOUNDED QUESTION, ⛔ not a fault** | BOARD; ⛔ ordering unchanged |
| R-9 | **`git status` is BRANCH-RELATIVE** — `alerts/delivery.py` is a stale-branch artifact, ⛔ not a gap | RULES already carries it |
| R-10 | **A green check is evidence only if it could have been red** — FINDING 1 stands | RULES; gates D-4 |

---

## 3 — 🔴 V-1 … V-4 · MEASURED

### V-1 · IS F6-leg ALREADY FIXED BY `c39e799`? → 🟢 **PREDICTION HELD**

🔬 `c39e799` (08-Aug) — *"fix(delivery): F6 — exit identity, not exit quantity"*,
**8 files, +1,864/−21**; `orders/cnc_gtt_monitor.py` **+326**.

**The exact line, before → after:**
```python
-                held[sym] = held.get(sym, 0) + abs(int(qty))
+                held[sym] = held.get(sym, 0) + max(0, int(qty))
```

📄 And the commit explains the mechanism in its own words, verbatim:
> *"The old `abs(int(qty))` double-counted the sale on a T+1 exit (holdings 0 +
> abs(-1) = 1), which forced `held != 0` — and `held == 0` is the SOLE door to
> `_finalize_gtt_exit`, so one line … ⛔ **Deleting abs() does not fix it either:
> the signed sum gives -1**"*

🔴 ⭐ **THAT LAST CLAUSE IS THE MOST VALUABLE THING V-1 FOUND.** The obvious repair
— *delete the `abs()`* — is **WRONG**: the signed sum yields `−1`, which also fails
`held == 0`. Only `max(0, int(qty))` is correct. ⇒ ⚠️ **A fresh build tonight would
very plausibly have shipped the naive fix.**

✅ **And it is MORE than the predicted one-line fix.** `c39e799` also replaces the
**predicate** as its title claims — the ladder moves from
`GTT triggered + holding STILL > 0` to **`exit OBSERVED + holding STILL > 0`** —
and adds `_release_stranded_delivery_trades` (Invariant A) plus
`_exit_observed_repeatedly` / `_exit_observed_no_recreate` guards.

⇒ 🎯 **METHOD FOR UNIT 1 = EXTRACT, ⛔ not build.** 🔬 Main has moved only
**+3/−1** in `cnc_gtt_monitor.py` since the merge-base, and `orders/` collides on
**F6 alone** (no PIPE/RENAME/GOV/SIZING touch) ⇒ the extraction is clean.
⛔ **Nothing extracted — V-1 answers, it does not act.**

---

### V-2 · DOES DROPPING F2-SIZING COLLAPSE THE COLLISION SURFACE? → 🟡 **HELD IN SUBSTANCE · ⛔ FAILED AS WORDED**

🔬 **Collisions re-measured at `645728d`:** **34 total** = 19 code/config + 13
`tests/` + 2 `docs/` + `PATHS.md`. ⚠️ *(The inventory's "31 code/config + 3 docs"
counted `tests/` as code. Same 34; different partition. ⛔ No figure is wrong.)*

**🔬 ATTRIBUTION — every code/config collision to its owning commit:**

| file | F6 | PIPE `12348ec` | RENAME `aa364e2` | GOV `247b983` | SIZING `65b7196` |
|---|:--:|:--:|:--:|:--:|:--:|
| `capital/fund_manager.py` | ✔ | ✔ | | ✔ | |
| `capital/position_sizer.py` | | ✔ | | | ✔ |
| `capital/risk_engine.py` | | ✔ | ✔ | | |
| `config/system_config.yaml` | | ✔ | ✔ | | ✔ |
| `core/config_auditor.py` | | | ✔ | | |
| `core/config_loader.py` | | ✔ | ✔ | | ✔ |
| `core/schema.sql` | | | ✔ | | ✔ |
| `core/state_store.py` | ✔ | ✔ | ✔ | | ✔ |
| `main.py` | | ✔ | ✔ | ✔ | |
| `signals/signal_processor.py` | | ✔ | ✔ | | |
| `orders/cnc_gtt_monitor.py` | ✔ | | | | |
| `orders/order_reconciler.py` | ✔ | | | | |
| `ops_dashboard/` × 6 | | | ✔ | | |
| `PATHS.md` | | | | | ✔ |

**🔬 THE TWO COUNTS ASKED FOR:**

> **F2-CORE surface = 7 files** — `fund_manager.py` · `risk_engine.py` ·
> `system_config.yaml` · `config_loader.py` · `state_store.py` · `main.py` ·
> `signal_processor.py` **+ the new `pipeline_policy.py` (0 collisions).**
>
> **F2-SIZING-only = `position_sizer.py`'s rewrite · `schema.sql` · `PATHS.md`.**
> **RENAME-only = 7 files** — `config_auditor.py` + 6 × `ops_dashboard/`.
> **F6-only (UNIT 1, ⛔ not F2) = `cnc_gtt_monitor.py` · `order_reconciler.py`.**

⇒ **19 code/config collisions → 7 for F2-CORE.**

**🔴 THE PREDICTION, SCORED HONESTLY.** It said *"`position_sizer.py` falls
entirely on the SIZING side … the NI-series revert risk goes to zero."*

- ⛔ **FAILED as worded — `position_sizer.py` is touched by PIPE too.** 🔬 PIPE
  **121 lines** vs SIZING **520 lines**.
- ✅ **HELD in substance, and by a stronger route than predicted.** 🔬 PIPE's 121
  lines are purely additive (`policy_provider=None` param + `_policy_for()`), and
  its own comment states: *"Without a provider this reproduces the pre-08-Aug
  scalars exactly … which keeps every existing sizer test — and MIS sizing —
  byte-identical."* 🔬 **AND deployed main ALREADY carries the per-book scalars**
  — `position_sizer.py:207-209` `_delivery_risk_per_trade_pct`,
  `_delivery_max_concentration_pct`, `_delivery_max_position_value_pct`, validated
  at `:376-380` (F1's work).
  ⇒ ⭐ **F2-CORE can ship with `position_sizer.py` UNTOUCHED.** The PIPE change is
  an architectural refactor, ⛔ not a CORE requirement.
- ⛔ **"Risk goes to zero" is FALSE and stays recorded as false.** 🔬 The 7 CORE
  files still carry **19 main commits, +957/−100**:

| CORE file | main commits | main +/− |
|---|:--:|---|
| `main.py` | 5 | +393/−29 |
| `core/state_store.py` | 4 | +102/−7 |
| `capital/risk_engine.py` | 3 | +116/−16 |
| `core/config_loader.py` | 3 | +102/−20 |
| `config/system_config.yaml` | 2 | +40/−9 |
| `capital/fund_manager.py` | 1 | +156/−12 |
| `signals/signal_processor.py` | 1 | +48/−7 |

🔬 **But what the split DOES remove is large and exact:** `position_sizer.py`
(**5** commits, +187/−42 — NI-5/NI-17/NI-18/NI-1), `config_auditor.py` (**4**,
+134/−15 — NI-5/NI-11/NI-12/NI-2), `db_reader.py` (**11**, +1,338/−14),
`schema.sql` (1). ⇒ **≥21 main commits and ≥+1,662 lines of main's repairs leave
the merge surface.** ⭐ The two worst NI-carrying files both drop out.

**🔬 CAN F2-CORE SHIP WITHOUT THE BREAKING `intraday_max_*` RENAME? → ✅ YES.**
🔬 **PIPE references `intraday_max_open_positions` / `intraday_max_daily_trades` in
ZERO production files.** 🔬 GOV's single reference is a **test fixture** —
`test_pipeline_loss_governor.py`, a `RiskEngine(...)` kwarg. 🔬 The rename is
introduced **solely** by `aa364e2`, a standalone `refactor(config)!` spanning 16+
files including 6 × `ops_dashboard/`.
⇒ ⭐ **The rename is separable.** 🔴 **D1 (NO PARTIAL DEPLOY) still binds the
rename itself if and when it ships** — ⛔ it does **not** bind F2-CORE to it.
⚠️ 💭 Per-book limits without the rename means adding `delivery_max_*` alongside the
existing `max_*` keys; that is a **design choice for tonight**, ⛔ not a measurement.

---

### V-3 · DOES F2-CORE NEED SCHEMA v46? → ✅ **NO. CONFIRMED.**

🔬 **RENAME's entire touch on `core/schema.sql` is ONE COMMENT LINE:**
```
+--                Q1 (intraday_max_open_positions; renamed 08-Aug-2026), all daily counters
```
🔬 **SIZING owns the whole substantive change: `+28/−5`** — the 8 sizing-audit
columns (`qty_by_allocation`, `qty_by_segment_capital`, `qty_by_broker_margin`,
`qty_by_max_position_value`, `qty_by_max_qty`, `planning_basis_rs`,
`capital_per_trade_allocation`, `risk_budget_per_trade`).
🔬 PIPE and GOV touch `schema.sql` **not at all**.

⇒ ✅ **F2-CORE requires NO schema change. The live DB stays v45.**
⚠️ Standing: if v46 is ever pushed it lands only at the next **OFF-MARKET** boot —
⛔ an evening schema push buys a night of CRITICALs.

---

### V-4 · DID K-1's DEDUCTION EVER CHANGE A SIZE? → 🟢 **PREDICTION HELD. D-5 CLOSES COMPLETELY.**

🔬 Measured across the **whole** trade population, live DB:

| measure | value |
|---|---|
| trades with a recorded `binding_constraint` | **708** |
| `binding_constraint = concentration` | **708 — 100%** |
| `binding_constraint = capital` | 🔴 **0** |
| `binding_constraint = risk` / `flat` | **0** / **0** |
| rows where `qty_by_capital <= qty_by_concentration` (i.e. capital *would* bind) | 🔴 **0** |
| **min** ratio `qty_by_capital / qty_by_concentration` | **1.75×** |
| **mean** ratio | **37.0×** |
| ranges | `qty_by_capital` 2…689 · `qty_by_concentration` 1…19 |

⇒ 🔴 **The capital rung has NEVER bound, and at its very tightest still permitted
1.75× the concentration rung.** ⇒ K-1's ₹6.07/day (0.057% of capital) cannot have
changed a single position size — it would need to close a **75% gap at minimum**
and a **37× gap on average**.
⇒ ✅ **D-5 CLOSES COMPLETELY. K-1 is NOT a defect and is now fully measured.**

🔬 The 63 rows with `binding_constraint IS NULL` are `FAILED` 29 · `CLOSED` 16 ·
`CANCELLED` 9 · `CLOSED_MANUAL` 9 — ⭐ trades with no sizing decision recorded,
⛔ not a hidden capital-bound population.

⚠️ ⭐ **AND V-4 IS ALSO THE EVIDENCE UNDER D-3.** The same measurement that closes
K-1 proves concentration is the **unique** binding rung ⇒ **the branch's
`0.10×TOTAL → 0.20×BASIS` rewrite is a ~7× change to the ONLY rung that actually
sets size.** ⭐ D-3's split is therefore measured, ⛔ not cautious.

---

## 4 — §4 IS NOT STARTED · ⏸ **GATED TO 17:45**

⛔ Nothing in §4 was begun: no UNIT 1 extraction, no UNIT 2 removal, no push, no
records beyond D-1's TREE line. ⭐ The market is open; FILE 14 forbids it.

**What §3 has already decided FOR tonight:**
- ✅ **UNIT 1 method = EXTRACT** `c39e799`'s `cnc_gtt_monitor.py` change (V-1 HELD).
  ⚠️ Its **T+1 arm stays NOT EXERCISED** until a real carry. ⛔ Do not claim it.
- ✅ **F2-CORE scope = 7 collision files + `pipeline_policy.py`**, ⛔ no schema
  change, ⛔ no `intraday_max_*` rename, ⛔ `position_sizer.py` untouched.
- ⏸ **UNIT 2 (F11 dead-config)** — ⛔ not started; each key still owes a
  no-live-reader proof.

---

## 5 — WHAT I DID ⛔ NOT MEASURE
1. **No branch code was executed.** Every §3 figure is a git/DB/static read.
   ⛔ F2's correctness remains **UNKNOWN**; ⛔ no branch test was run.
2. **Whether F2-CORE's 7 collision files merge cleanly** — I counted commits and
   line deltas; ⛔ I did **not** attempt a merge or resolve one conflict.
3. **UNIT 2's F11 keys** — ⛔ no live-reader proof attempted for
   `order_protocol`, `dynamic_by_winrate`, `sl_atr_multiplier`,
   `delivery_max_position_value`.
4. **The per-book-limits-without-rename design** — 💭 stated as an option; ⛔ not
   designed, ⛔ not costed.
5. **`c39e799`'s other 7 files** (`fund_manager.py` +44, `state_store.py` +118,
   `order_reconciler.py` +9) — V-1 read the `cnc_gtt_monitor.py` change
   end-to-end; ⛔ the rest were not traced, and they are part of any extraction.
6. **FINDING 1's repair** — ⛔ not written. D-4 requires it *before* the branch
   suite becomes an acceptance gate.
