# FILE 16 — UNIT 3 FINAL SCOPE · ACCEPTED · PREDICTION FROZEN

**27-Aug-2026 (Thu), ~11:4x IST · market OPEN.** 🔬 MEASURED · 📄 EVIDENCE ·
💭 INFERENCE · 👤 RAMA'S · 🏷️ VACUOUS.

⛔ **NOTHING BUILT.** §2–§4 gated to **17:45**. ⛔ No push, ⛔ no code change,
⛔ no test written, ⛔ no branch operation. ⭐ This document is **records + three
read-only measurements that close gaps I myself flagged as NOT PROVEN.**
🔬 `origin/main` = **`bc9a9f5`** (measured). ⚠️ ROOT is on the F2 branch; every
quote is `git show origin/main:…`.

---

## 1 — A-1 … A-7 · ACCEPTED, BINDING

| # | accepted |
|---|---|
| **A-1** | `leverage_map.DELIVERY: 1.0` EXISTS and is ACTIVE via the one intent-generic multiply (`fund_manager.py:267-268`). ⇒ **U3-a NO-OP · U3-b NO-OP.** ⛔ Do NOT add a delivery multiply — a second multiply site is a second source of truth |
| **A-2** | **ONE leverage source, ONE calculation** (`capital = notional / leverage`). ⭐ Intent selects the **VALUE**; ⛔ intent must never select a different **ALGORITHM** |
| **A-3** | **(A) calculation parameterisation** = ✅ already config-driven · **(B) runtime authority/safety** = 🔴 NOT solved. ⛔ Never claim a leverage change is safe because the number lives in YAML — ⚠️ syntactically valid ≠ economically safe |
| **A-4** | 🔴 **FIX-072 is a STANDING ARCHITECTURAL CONSTRAINT.** If ever wired it must declare its authority model explicitly — `CONFIG_ONLY` · `BROKER_ONLY` · `BROKER_WITH_CONFIG_CEILING` · `BROKER_WITH_CONFIG_FLOOR`. ⛔ Wiring alone must never decide it |
| **A-5** | The 0/0 live-margin log result is 🏷️ **VACUOUS** — the positive control failed. ⛔ Do not cite the zero. ⭐ The static wiring proof stands alone |
| **A-6** | **CONFIGURED leverage ≠ ACTUAL APPLICABLE leverage.** The system never asks the broker. ⛔ `5.0` is not evidence Zerodha grants 5× on anything |
| **A-7** | 5× = broker/MIS leverage · 70% = MIS allocation · 3.5× = the planning multiple `0.70 × 5.0` produces. ⛔ NEVER "3.5× leverage". ⭐ 5× = `5.0`, ⛔ not `0.05` |

---

## 2 — THE CEILING CONFLICT · ⭐ RESOLVED, WITH ONE ITEM 👤 OPEN

⭐ **The tension is real:** a ceiling hardcoded at `10.0` means a legitimate future
12× needs a **CODE** change — 🔴 exactly the headache 👤 Rama asked to remove. But an
unbounded YAML ceiling is no guard at all, since a fat-finger could widen it.

⭐ **ADOPTED SHAPE — two blocks, two different kinds of edit:**

```yaml
leverage_map:            # OPERATIONAL — routine values
  INTRADAY: 5.0
  COVER_ORDER: 6.0
  DELIVERY: 1.0
  BRACKET_ORDER: 5.0

leverage_safety:         # GOVERNANCE — deliberate, reviewed, rarely touched
  min_allowed: 1.0
  max_allowed: 10.0      # INTERNAL SAFETY CEILING
```

⇒ ⭐ A **fat-finger touches ONE block and is CAUGHT**. ⭐ A legitimate regulatory
change touches **TWO** blocks — two deliberate edits, ⛔ never an accident, ⛔ and
still **no code change**. ⇒ 👤 Rama's contract survives.

### 🔴 THE ONE ITEM 👤 RAMA MUST SET — AND THE DEFAULT I APPLIED

`leverage_safety.max_allowed` must itself sit inside a **hard code bound**,
⭐ otherwise the guard guards nothing (anyone could raise the ceiling to 500).
👤 **That absolute number is Rama's to set once, with its reason recorded.**
⛔ I did not invent it.

⇒ 🏷️ **FILE 16's OWN FALLBACK APPLIED:** he has not set it, so per §2's
instruction — *"If he does not set it, use the G2 threshold `10.0` for BOTH and
record that the two-block structure is deferred"* —

> ✅ **TONIGHT: a SINGLE bound `1.0 ≤ leverage ≤ 10.0`, hardcoded.**
> ⏸️ **The `leverage_safety` two-block structure is DEFERRED, ⛔ not rejected.**
> 👤 **OPEN FOR RAMA: the absolute code bound** that `max_allowed` may never
> exceed. ⭐ Until he sets it, the ceiling stays code-side and a future 12× *would*
> need a code change — ⚠️ **recorded plainly as the known cost of deferring.**

⚠️ ⭐ **`10.0` IS AN INTERNAL SAFETY CEILING.** ⛔ NOT a broker limit. ⛔ NOT a SEBI
limit. ⭐ It is defensible only because `config_auditor.py:697` **already uses it**
(`if value > 10`) ⇒ ⛔ no new number is introduced, and it clears the highest
configured value (`COVER_ORDER: 6.0`) with margin.
⛔ **Never describe it as externally mandated.**

---

## 3 — THE ASYMMETRY · ⭐ THE CURRENT GUARD COVERS THE WRONG HALF

| dir | failure | effect | 🔬 CURRENT COVERAGE | rank |
|---|---|---|---|---|
| **2** | **TOO HIGH** — `50` for `5.0` (dropped decimal) | `margin = notional/50` ⇒ **10× intended quantity** | 🔴 **WARN only, and only INTRADAY + COVER_ORDER** | 🔴 **THE CAPITAL-BLOWUP DIRECTION — highest** |
| **1** | **TOO LOW** — `0.05` for `5.0` | `margin = notional/0.05` ⇒ every MIS size **1/100th of intent** | 🔴 **NONE** — G2 tests `> 10` only ⇒ ⛔ not even a WARN | money-safe but **SILENT**: the system quietly stops trading meaningfully |
| **3** | **UNKNOWN INTENT** — `.get(intent, 1.0)` | falls back to `1.0` = the MINIMUM of every configured value ⇒ **always over-reserves, under-sizes** | none | ⭐ errs CONSERVATIVE ⇒ **LATENT UNDER-SIZING**, ⛔ not a blowup. ⭐ Still must fail closed — *silently wrong is wrong* |
| **4** | **DELIVERY unvalidated** | CNC is cash-and-carry ⇒ ⭐ **there is no such thing as delivery leverage** | 🔴 **ZERO — G2 checks neither DELIVERY nor BRACKET_ORDER** | special handling below |

🔴 **⇒ THE ACTUAL CAPITAL-PROTECTION CHANGE IN THIS UNIT is raising Direction 2
from WARN to CRITICAL/exit-5 across ALL FOUR intents.** The lower bound protects
against silent non-trading — ⛔ a different problem, ⛔ not a lesser one.

⭐ **DIRECTION 4 — SPECIAL HANDLING, as instructed:** bound `DELIVERY` like the
others, **AND** emit a **WARN — ⛔ not CRITICAL — if `DELIVERY != 1.0`**, naming
**MTF** explicitly. ⭐ That flags an unusual-but-possibly-intended value without
blocking a future deliberate MTF decision, ⭐ which is a different product and a
different decision.

---

## 4 — 🔬 THREE NEW MEASUREMENTS (read-only) — U3-c's PREREQUISITE

### 4.1 · ✅ U3-c STEPS 1–2 ARE NOW **PROVEN** (was NOT PROVEN in FILE 15 §7)

🔬 **Every `FundManager(` occurrence in the deployed tree, classified:**
- `capital/fund_manager.py:283` — 🔬 **a DOCSTRING** (`Usage::` block opens at
  `:282`). ⛔ Not code.
- **`main.py:2715` — the ONLY production construction site**, and it supplies
  `leverage_map=leverage_map` at `:2725`. ✅
- Everything else (≈100 sites) is under `tests/`, and most use `_MockFundManager`,
  ⛔ not the real class.

⇒ ✅ **PROVEN: the only legitimate production path supplies the validated map.**
⇒ ⭐ U3-c step 2 is satisfied; the hardcoded default at `:312-318` is **LATENT**,
confirming (⛔ not assuming) FILE 15's finding.

### 4.2 · 🔴 U3-c IS **NOT** A SIX-LINE DELETION — IT BREAKS TESTS

🔬 At least **six test files construct the REAL `FundManager` with NO
`leverage_map` argument**, i.e. they depend on the `:312-318` hardcoded default:
`tests/crash_test/test_double_release.py` · `tests/crash_test/test_fund_manager_edges.py`
· `tests/unit/test_gate8_sector_toctou.py` · `tests/unit/test_h7_strategy_cap_toctou.py`
· `tests/unit/test_phase19_batch2.py` (**5 sites**) · `tests/unit/test_order_reconciler.py:2106`.
⇒ ⚠️ **Removing the default makes a missing map fail — which is the POINT (U3-c
step 4) — but every one of these must be updated in the same commit.**
⭐ Budget for it; ⛔ do not discover it at 22:00.

### 4.3 · 🔴 U3-e (STRICT INTENT LOOKUP) BREAKS TWO MORE — AND EXPOSES A REAL BUG

🔬 `_ALL_INTENTS` = `{INTRADAY, COVER_ORDER, BRACKET_ORDER, DELIVERY}`
(`fund_manager.py:100-102`). 🔬 **`"POSITIONAL"` is NOT a valid intent** — yet two
tests build a `leverage_map` with it:
- `tests/unit/test_fix133_dynamic_sizing.py:36` — `{"INTRADAY": 5.0, "POSITIONAL": 1.0}`
- `tests/unit/test_mc6_zero_multiplier_skip.py:46` — `{"INTRADAY": 5.0, "POSITIONAL": 1.0}`

⇒ ⭐ Today these are harmless *because* `PositionSizer` (`:183`) does **not**
validate and `.get(intent, 1.0)` silently absorbs the bad key.
⇒ 🔴 **That is precisely Direction 3 in the wild — an invalid intent name sitting
in the test suite, invisible, for however long.** ⭐ Under U3-e's strict lookup they
fail, ⭐ which is the correct outcome and is itself evidence the guard works.
🏷️ **Recorded as a FINDING, ⛔ not fixed tonight beyond what U3-e forces.**

---

## 5 — 🔴 THE FROZEN PREDICTION — ⭐ WRITTEN NOW, BEFORE ANY CODE EXISTS

> 🧊 **FROZEN 27-Aug-2026 ~11:4x IST, before UNIT 3 is implemented, before any
> test is written.** ⭐ Scored ONLY after the tests run.
>
> **With the current map (`5.0 / 6.0 / 1.0 / 5.0`), ALL SEVEN hold:**
> 1 same config values · 2 same intent → same value · 3 same qty/price inputs ·
> 4 **same calculated capital/margin** · 5 same downstream sizing ·
> 6 same persisted audit values · 7 same Live/Paper result.
>
> ⇒ ⭐ **ONLY an invalid configuration produces a new outcome: BOOT FAILURE.**
>
> **HELD** iff every valid current calculation is identical **AND** every invalid
> leverage fails closed.
> **FAILED** if any valid calculation changes, **or** any invalid leverage boots,
> **or** any unknown intent silently becomes 1×.

⚠️ 💭 **AND A SECOND, HONEST PREDICTION about the work itself** (⭐ frozen too, so
it can be scored): *the test suite will require edits in **at least 8 files**
(§4.2's six + §4.3's two). ⭐ If it turns out to be fewer, my measurement was
wrong; if far more, the unit may not fit the evening beside UNIT 1.*

---

## 6 — UNIT 3 FINAL SCOPE (⭐ for 17:45, ⛔ not started)

- **U3-c** remove the latent duplicate — in the required order: find all sites
  (✅ done, §4.1) → confirm every legitimate path supplies the map (✅ done) →
  remove the numeric dict → make a missing map fail **clearly** → a RED-CAPABLE
  test that a missing map ⛔ cannot resurrect hardcoded leverage.
- **U3-d** fail-closed validation: present · numeric · **FINITE (⚠️ NaN and
  Infinity rejected explicitly — a range check alone lets them through)** ·
  `≥ 1.0` · `≤ 10.0`. Violation ⇒ **CRITICAL naming the map AND the intent, then
  exit 5.** ⛔ Never coerce, ⛔ never default.
  Error shape: *"Invalid `leverage_map.INTRADAY`: expected a finite value within
  the approved range."*
- **U3-e** ONE validated object passed downstream; **STRICT** intent lookup
  thereafter. ⛔ Do NOT duplicate independent validation in `FundManager` and
  `PositionSizer`.
- **U3-f** parity — Live and Paper resolve the same validated map.
- **U3-g** ⛔ touch nothing else: not `0.70`/`0.30`, not `5.0`, not any cap, not a
  sizing formula, not `position_sizer`'s arithmetic, not broker-margin behaviour,
  not the schema.
- **18-test matrix** (4 valid · 12 fail-closed · 1 parity · 1 neutrality) — ⭐ each
  must be able to go **RED** if its protection is removed. ⛔ One broad green test
  is not acceptable.
  ⭐ **Partial credit already exists:** `tests/unit/test_fund_manager.py:597`
  (`leverage_map={"INTRADAY": 5.0}  # missing 3 intents`) is already a red-capable
  missing-intent test. ⭐ Extend, ⛔ do not duplicate it.

---

## 7 — EVIDENCE LIMITS (updated)

**PROVEN:** `DELIVERY 1.0` in deployed config · DELIVERY uses the generic
calculation · configured leverage is wired into production · `broker_adapter` is
NOT wired into the production `PositionSizer` · the latent `FundManager` hardcoded
map exists · leverage bounds are absent · G2 is incomplete (2 of 4 intents, upper
only, WARN) · values are `5.0 / 6.0 / 1.0 / 5.0` · ⭐ **NEW: `main.py:2715` is the
only production `FundManager` construction and it supplies the map** · ⭐ **NEW:
`"POSITIONAL"` is not a valid intent yet appears in two test leverage maps.**

**NOT PROVEN:** that `5.0` equals the broker's actual applicable margin for any
symbol or day · that U3's implementation is correct — ⛔ **it has not been built** ·
that U3's red-capable tests exist — ⛔ **not written** · that `10.0` is externally
mandated — ⛔ **it is not; it is internal** · that 8 files is the true test-edit
count — 💭 predicted, ⛔ not verified.

**VACUOUS:** the 0 live-margin log entries — the positive control was absent.

**⛔ NOT DONE:** UNIT 1 · UNIT 2 · UNIT 3 · any push · any test.
🔴 ⛔ **U3 is NOT "DONE" and must not be recorded as such** — ⭐ it is SCOPED,
MEASURED and FROZEN. ⛔ HELD ≠ DONE.

⭐ **RECORD U3 THIS WAY when it lands, ⛔ never as "added GTT leverage":**
> *"DELIVERY leverage was ALREADY implemented; U3 added ⛔ no second calculation.
> U3 hardened the existing configuration authority by removing latent duplicate
> and silent-fallback sources and enforcing complete, finite, bounded validation
> across all four intents."*
