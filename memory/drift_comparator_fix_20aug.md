---
name: drift-comparator-fix-20aug
description: "The G3 capital-drift comparator FIX (7fc5d5a, BUILT-UNPUSHED 20-Aug) — the corrected expression, why carry cancels, the named residuals, the D1 paper ruling, the one falsifier that can still kill it, and the RC-1..RC-8 record-correction pass (gate wording, bounded paper negative, skip-guard non-vacuity)."
metadata: 
  node_type: memory
  type: project
  originSessionId: c1c3a97c-8f7a-417a-8528-0564e8fed40c
  modified: 2026-08-25T04:06:17.151Z
---

# G3 DRIFT COMPARATOR — THE FIX. `7fc5d5a` · **DEPLOYED 20-Aug 19:34:17 · ⛔ NOT VERIFIED LIVE**

✅ **PUSHED `08b462b` → `7fc5d5a` on Rama's own words: *“Capital drift - Please try to deploy
now”* / *“Please proceed”*.** ⛔ **No override was used or logged — the base had not moved, so
no refit was owed.** Verified FILE/CONFIG level only: `origin/main` two ways · PC==VM md5 on all
three (non-vacuous — all three differed before) · deployed-tree drift EMPTY via the corrected
`GIT_INDEX_FILE` recipe · **the hook restarted NOTHING** (alert-watcher / gui-dashboard /
token-watcher PIDs unchanged, `NRestarts=0`) · crontab md5 + 46 job lines unchanged despite the
*“AUTO-INSTALLED”* message.
🛑 **The service was NOT started. FIRST EXECUTION IS THE 08:15 BOOT.** The falsifiers below
become scorable only in tomorrow's live session.
🔴 **THE BASE MOVED ⇒ n907 / tiers / controlplane all need a REFIT **and** a FULL RE-GATE;
n907's green gates from tonight are STALE.** See [[unpushed-pending-deploy-ledger]].

⭐ **The DIAGNOSIS is not new — it is [[capital-drift-is-operand-mismatch-05aug]],
measured 05-Aug and independently re-measured 20-Aug (4 alarms, residual 0.00
each).** ⛔ Do not re-derive it. **What is new is that a fix is authorised and
built**, which retires that file's *"⛔ NO FIX AUTHORISED"* line.

## THE CHANGE — `orders/order_reconciler.py` + one pure adapter property

```
OLD  expected = snapshot.total                      # REAL CAPITAL
NEW  held     = intraday_reserved + intraday_used
              + positional_reserved + positional_used
     expected = snapshot.total − held − snapshot.daily_realized_pnl   # CHECK 1
     held_today      = held − (intraday_carry + positional_carry)
     margin_residual = held_today − margins.used                      # CHECK 2
```

⭐⭐ **NO NEW STATE WAS NEEDED — every operand was ALREADY on `CapitalSnapshot`
and already exported to the reconciler.** `daily_realized_pnl` is the day-scoped
SQL accumulator (`state_store.py:2555`, indexed generated `date` column).

⭐ **CHECK 2 IS SEPARATE ON PURPOSE** — its residual must stay visible, never be
absorbed into CHECK 1. It is logged every cycle and rides in CHECK 1's alert
`context`. ⛔ **It gets NO alert of its own**, and the reason is a measurement
gap: broker `used` for a **settled CNC holding is UNMEASURED** (it plausibly
leaves `utilised.debits` while `held` keeps it), so alerting would false-fire on
the first carry day.

## ⭐ WHY CARRY CANCELS (and is deliberately ABSENT from CHECK 1)

carry `C`, broker net `N`, new margin `M` ⇒ `total = N+C`, `held = C+M`
⇒ `expected = (N+C) − (C+M) = N−M`. **Exact.** ⚠️ **CHECK 2 still needs `−carry`.**

## ⛔ RESIDUALS — PRESENT BY DESIGN. ⛔ NOT DEFECTS. ⛔ Do not "fix" them.
1. Flat `leverage_map.INTRADAY: 5.0` vs the broker's **per-instrument, MTM** MIS
   margin (~₹0.32/leg). ⚠️ **INFERRED — `order_margins()` was NEVER called.**
2. The **5% RESERVE buffer** inflates `held` between placement and fill
   (₹21.64 at 11:07:14; gone at COMMIT 19 s later). **Transient.**
3. **Mid-session restart** — `_intraday_carry` is deliberately `0.0`
   (`fund_manager.py:1832`, *"NOT MEASURED"*). **Pre-existing; SURFACED, ⛔ not created.**

## ⛔ TOLERANCE WAS NOT TOUCHED — and that is the point
All four alarms fall below the **₹50 base**, so they clear **without** the 10%
band. ⚠️ `FIX-190`'s band exists *solely* to absorb deployed capital; this
removes its REASON. ⛔ **Retiring the band is a SEPARATE decision** — it needs
multi-day observation **including a carry day**, and tightening a live alarm in
the same change that alters its comparator would confound both.

## 🔴 D1 — RULE #8 DELIBERATELY DEVIATED FROM, ON THE RECORD
**LIVE-only.** The reconciler asks the **adapter** a capability question
(`produces_broker_equivalent_margins`) instead of branching on a mode label —
**preserving `RC15`** (*"No paper-mode special-casing in reconciler; paper
behaviour is owned by the adapter"*). Skip is logged at **WARNING**, ≥1×/session,
reusing the existing 30-min throttle (**no new state**). ⛔ An adapter **lacking**
the property **RUNS** the check — fail-safe.
⛔ **Option 1a (paper net = capital − held) was REJECTED as TAUTOLOGICAL** — it
compares X against X and would manufacture a false GREEN on the very check being
fixed. **Option 1b** (adapter simulates its own margin) is the correct long-term
fix, **OWED, ⛔ NOT BUILT** — it reaches the BOOT path.
📌 **Rama, 20-Aug: *"ignore paper trade, no longer going back to paper trade anymore."***
⭐ Search width for the cost of the skip — **re-measured 20-Aug (supersedes the earlier
76 / 1,041 figures):** **137 `.log` files — ZERO `[PAPER]` alert titles of ANY kind vs
**1,048** `[LIVE]`**, and `mode=live` **134** / `mode=paper` **0**. ⇒ *“PAPER capital-drift alert occurrences before this fix: ZERO in the available/bounded corpus; the check was NEVER EXERCISED in PAPER.”*

## ⭐ TESTS — NON-VACUITY PROVEN, ⛔ not assumed
The 51 `MagicMock` snapshot doubles were replaced by **one real `CapitalSnapshot`
factory**: a MagicMock answers unset fields with MagicMocks, so
`delta <= tolerance` **silently stopped being a comparison** and the check quietly
stopped firing **while the tests still looked green** — the recorded
fixture-hazard class, found live in this file.
⭐ **PLANT PROOF — COMPARATOR: with the OLD comparator restored, 7 of 8 new tests go RED**;
CASE 1 (flat book) correctly stays green because old and new agree when
`held = 0`. The planted run reproduced `delta=1155.50` — the fixture data is
faithful to the real 10:10:22 alarm.

## 🔴 THE ONE FALSIFIER THAT CAN STILL KILL THIS
The identity was derived from **ONE day with carry = 0**. ⛔ **The first CARRY
DAY is its real test.**

### ⚠️ CORRECTED WORDING — 👤 Rama, 25-Aug 09:45. ⛔ THE OLD ₹-ONLY FORM IS WITHDRAWN.
▎ **`carry > 0` IS AN EXPLICIT PRECONDITION OF THE REVERT CONDITION.**
▎ IF `carry > 0` **AND** the CHECK 1 residual ≈ the carried CNC amount
▎    ⇒ 🔴 carry-algebra defect condition is relevant ⇒ **REVERT** (👤 on Rama's word).
▎ IF `carry = 0` and the residual merely RESEMBLES a position value
▎    ⇒ ⛔ **NOT a carry failure.** It is **same-day broker-`used` settlement lag.**
▎    ⛔ Do NOT revert · ⛔ do NOT tune · ⛔ do NOT report it as the trigger firing.

🔬 **WHY THIS EXISTS — measured 25-Aug.** The 24-Aug series contains
`residual = 441.12` on **55 samples** and `residual = 610.37` on **46 samples**,
both with **`carry = 0.00`**. ⇒ ⛔ **The ₹-amount-only trigger, applied as written,
would have declared a FALSE REVERT of a WORKING unit on 101 samples.**
⭐ **A rupee amount alone is NEVER sufficient.** ⛔ A wording fix, ⛔ not a code fix.
📄 `docs/audit/CARRY_DAY_25-Aug-2026.md`.
Frozen prediction: `docs/audit/PREDICTION_driftcomparator_20-Aug-2026.md`
(md5 `b6afe93b7629f0ce5bba0b33bb09d41a`, whole file, 123 lines, frozen **before** the gate).

⭐ **Kill ladder unaffected — measured:** G3's `source_module="order_reconciler"`
is **not** in `drift_handler._ESCALATING_SOURCES`, so DH1 logs INFO and never
escalates. See [[capital-drift-is-operand-mismatch-05aug]] · [[unpushed-pending-deploy-ledger]]
· [[paper-cannot-exercise-class-26jul]] · [[feedback-verify-rc-not-output]]

## 🧿 RECORD-CORRECTION PASS — 20-Aug ~14:0x (`RC-1`…`RC-8`). ⛔ NO CODE CHANGED.
Authorised by ChatGPT red-team 20-Aug 13:39. Every figure below was **re-run in that
session**, ⛔ not recalled. **Implementation ACCEPTED and left untouched.**

### 🏷️ `RC-3` — THE GATE WORDING. ⛔ *"GATE — PASS"* IS FORBIDDEN BY THIS PROJECT'S OWN RULE
`N12-16` `<RULE · BINDING>` already permits a non-zero rc — *"⛔ A non-zero `rc` alone
does NOT fail the gate; ⛔ an UNATTRIBUTED failure does"* — **and mandates the wording**
*"full clean-worktree regression completed; rc=1; all failures independently attributed;
no `<unit>`-specific failure found."* ⛔ **NEVER *"the full gate passed"***. Written a
second time at `docs/audit/f6_build_08aug2026.md:307-313`. ⇒ the sentence that survives:
> *"full clean-worktree regression completed; rc=1; all failures independently
> attributed; no capital-drift-comparator-specific failure found."*

**⛔ THE DIFFERENTIAL PASSED; THE FULL SUITE IS NOT GREEN.** `RAW_PYTEST_RC=1` re-read
from `gate-drift.rc` — a FILE, ⛔ never a pipe (`D5.1`).

### 📏 `RC-8` — SIX NUMBERS, EACH WITH ITS COMMAND. ⛔ NEVER COLLAPSE THEM
| scope | command | result |
|---|---|---|
| targeted / new | `pytest tests/unit/test_order_reconciler.py -k "<the 11>"` | **11 passed, 86 deselected, rc 0** |
| unit subset (ONE file) | `pytest tests/unit/test_order_reconciler.py -q` | cand **97 passed rc 0** · base **86 passed rc 0** |
| full suite | `pytest tests/unit tests/integration` | cand **7F / 5,657P / 4S rc 1** · base **7F / 5,646P / 4S rc 1** |
| differential | `comm` both ways | **0 NEW · 0 disappeared · 7 common · +11 passed** |

⭐ **The arithmetic closes both ways: 86 deselected + 11 selected = 97, and 5,646 + 11 = 5,657.**
⭐ All 11 proven ABSENT at base (`git grep "def <name>" 08b462b` = 0 each).
⛔ ***"97 passed" NEVER means the project passes*** — it is ONE FILE.

### ✅ `RC-1` + `RC-7` — THE SKIP IS TESTED BOTH WAYS, AND THE TESTS ARE NON-VACUOUS
**3 passed, 94 deselected, rc 0.** `test_g3_skip_taken_when_adapter_margins_not_broker_equivalent`
(asserts 0 actions, 0 events, `notifier.send` not called, and — at `logging.WARNING` — that
the log carries `"CAPITAL-DRIFT + MARGIN RECONCILIATION SKIPPED"` **and** `"PAPER"`) ·
`test_g3_skip_not_taken_in_live` (same numbers, 1 action + 1 event) ·
`test_g3_missing_capability_attribute_runs_the_check` (`MagicMock(spec=[...])`, attribute
truly absent ⇒ the check **RUNS**).

⭐⭐ **THE GAP THAT WAS FOUND AND CLOSED: the commit's plant restored the OLD COMPARATOR,
which is orthogonal to the skip guard — so the skip tests' falsifiability had NEVER been
established.** Two-way byte-plant, restored and md5-verified
(`3b9f36c6e3ed42cfe513c1d64cb3da94`, 222,651 B, `git status` empty):
* **skip DISABLED** (`if False and …`) ⇒ `skip_taken` **RED**, other two green.
* **skip FORCED** (`if True or …`) ⇒ `skip_not_taken_in_live` **and** `missing_capability` **RED**, `skip_taken` green.

⇒ **each test fails under exactly the mutation it guards and no other.**
⭐ **"Skip is visible" is STRUCTURAL, ⛔ not asserted:** `_last_capital_drift_alert_poll`
initialises to `None` (`:407`) and the throttle returns `True` when `last is None` ⇒ the
WARNING **cannot** be throttled away on its first call. Guard at `:3652` sits **BEFORE**
`get_margins()` at `:3667`.

### 📊 `RC-2` — THE PAPER NEGATIVE, NOW **BOUNDED** (supersedes the earlier 76 / 1,041)
**PAPER capital-drift alert occurrences before this fix: ZERO.** Re-grepped read-only on the
VM at `/home/ubuntu/systems/trading-system`: `Capital Drift` = **79**, `[LIVE]` **79**,
`[PAPER]` **0**.
⭐ **WIDTH BESIDE THE ZERO: 137 `.log` files; 24 `system_*.log` spanning 2026-07-20 → 2026-08-20.**
⭐ **CONTROL:** `[LIVE]` = **1,048** in the same corpus ⇒ the tag is findable.
⭐⭐ **DECISIVE:** `mode=live` **134** · `mode=paper` **0** · `paper_mode=False` on **all 24 days**.
⚠️ **The 310 `paper` hits are a FALSE FRIEND: 262 are the tickers `SESHAPAPER` / `JKPAPER`.**
🚫 **No wider corpus exists** — `telegram_alerts` holds **0 rows** and has **zero production
writers** (recorded 05-Jul, `docs/audit/audit_05jul2026.md:310`).
⇒ ⭐ **THE SURVIVING STATEMENT:** *“PAPER capital-drift alert occurrences before this fix: ZERO in the available/bounded corpus; the check was NEVER EXERCISED in PAPER.”*
⚠️ **AND THE BOUNDARY TRAVELS WITH IT, or the claim is not a measurement: ZERO alerts means **no historical paper exercise was OBSERVED** — ⛔ it is **NOT** proof that the paper implementation was ever CAPABLE of exercising the broker-equivalent condition. 📏 **BOUNDS: 137 `.log` files · 24 `system_*.log` · 2026-07-20 → 2026-08-20; and `telegram_alerts` (0 rows, ⛔ no production writer) means the LOG CORPUS **IS** THE WHOLE AVAILABLE HISTORY.**

### 🔬 `RC-4` — CHECK 2 IS INSTRUMENTATION. ⛔ NOT A VALIDATED CHECK
Re-measured **with controls**: base `08b462b` first-party `MarginInfo.used` consumers = **0**,
while the *identical* grep returns **7** at `7fc5d5a` ⇒ the zero is real. VM logs: `utilised`
**0** · `debits` **0** · `broker_used` **0**, against a control of `net=` **50,823**.
⚠️ **`M3`:** the parse is `:1474` **at `7fc5d5a`** but `:1454` at base — ⛔ never cite it SHA-less.
🔴 **OWED, WITH ITS TRIGGER:** on the FIRST live cycle after deploy **while an MIS position is
open**, read `G3 MARGIN_RECON` from `logs/system_<date>.log` and reconcile `broker_used`
against the Funds-page *"Used margin"*. **Only then** may a CHECK 2 threshold be decided.
⛔ The ₹0.32 attribution stays **INFERRED** — `order_margins()` was never called.

### 🔴🧊 `RC-5` — THE CARRY-DAY FALSIFIER, FROZEN
comparator identity = **MEASURED / SUPPORTED for a NON-CARRY book**; carry-day correctness =
⛔ **NOT YET PROVEN**. Verbatim: *"if a carried CNC position produces a CHECK 1 residual
approximately equal to that position's value, the carry algebra is WRONG and this unit must
be REVERTED, not tuned."*
⛔ **PROHIBITED ON THAT DAY:** ⛔ tuning the tolerance to hide it · ⛔ adding an unexplained
carry term · ⛔ changing `_total` · ⛔ changing RESERVE/COMMIT · ⛔ changing segment buckets.
⇒ **STOP and re-open the mathematical design.**

### ✅ `RC-6` — DIFF SCOPE, 8/8 VERIFIED
**3 files only** (`order_reconciler.py`, `zerodha_adapter.py`, `test_order_reconciler.py`);
parent of `7fc5d5a` **IS** `08b462b`; adapter change is **ONE pure `@property`**
(`produces_broker_equivalent_margins` → `return not self._paper`) with **no `self.*`
assignment**; `get_margins()` body **byte-identical**; `fund_manager.py` /
`utils/startup_checks.py` / `position_sizer.py` / `drift_handler.py` /
`system_config.yaml` all `git diff --quiet` CLEAN ⇒ ⛔ no boot-path change; the only two
`paper` matches in the whole diff are a **docstring** and a **log string** ⇒ ⛔ no mode-label
branch; **F6 `c39e799` absent by CONTENT** (`_resolve_release_reservation_id`,
`get_reservation_id_for_trade`, `test_f6_delivery_exit_predicate` → **0 hits** in both trees,
with a positive control proving the search finds them in `c39e799` itself).

⚠️ **NEW ISSUE FOUND EN ROUTE — see [[unpushed-pending-deploy-ledger]] and `N20-19`:** the gate's
*"failure MESSAGES are identical too"* claim is **VACUOUS** — `gate-*.failmsgs` is
byte-for-byte `gate-*.failids` plus the 7-char `FAILED ` prefix, and **zero** short-summary
lines carry a ` - <reason>` suffix ⇒ that comparison **could not have gone red** (`V5`).
⭐ The id-level `comm` differential is REAL and unaffected; only the second check stacked on
top of it is withdrawn. ⛔ **NOT fixed — `run_gate.sh` is gate machinery and n907 owns tonight.**
⛔⛔ **WITHDRAWING THE CLAIM IS *NOT* A REPAIR — `run_gate.sh` IS UNCHANGED AND REMAINS DEFECTIVE.** 🏷️ **`DISCOVERED · RECORDED · ⛔ NOT FIXED`** — ⛔ not *“handled”*, ⛔ not *“closed”*. 🔴 **TRIGGER: the next gate-machinery window — ⛔ never a deploy evening, ⛔ never the session that USES the gate. Until then ⛔ no reader may cite `failmsgs` as independent evidence.**
⚠️ **TWO PRE-EXISTING RECORD-HYGIENE DEFECTS, ⛔ NOT CAUSED BY THIS SESSION, ⛔ NOT FIXED (`N20-20`):** ① register row **`N20-14`** has a broken markdown column count (5 structural pipes vs 3) — proven pre-existing: present at `b019540`, and this pass's `git diff` never touches its line. ② the index's own gate `LC_ALL=C awk 'length>(index($0,“🔝”)?450:300)' MEMORY*.md` returns **80 lines** (ARCHIVE 57 · BOARD 22 · REFERENCE 1) — **`MEMORY.md` itself passes with 0**, and all three offending files were last written BEFORE this session. ⚠️ **Fix ② by RELOCATING content to topic files, ⛔ NEVER by raising the cap.**
