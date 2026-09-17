# FILE 17 — §1–§3 RECORDED · NEUTRALITY PROOF CORRECTED BY MEASUREMENT

**27-Aug-2026 (Thu), ~11:5x IST · market OPEN.** 🔬 MEASURED · 📄 EVIDENCE ·
💭 INFERENCE · 👤 RAMA'S · 🏷️ VACUOUS.

⛔ **NOTHING BUILT.** Build gated to **17:45**. ⛔ No push, ⛔ no code, ⛔ no test.
🔬 `origin/main` = **`bc9a9f5`** (measured). ⭐ This is the LAST scoping record —
the next output is implemented code and test results.

---

## 1 — ✅ TAKEN · `leverage_map.DELIVERY` IS PINNED TO EXACTLY `1.0`

⭐ **Exact-match validation. Anything ≠ `1.0` ⇒ CRITICAL, exit 5.** ⛔ Not a WARN,
⛔ not a range check.
⭐ **Reason:** CNC delivery is cash-and-carry. **1× is the PRODUCT, ⛔ not a
tunable parameter** — there is no delivery leverage to configure.

⭐ **This SHARPENS 👤 Rama's future-proofing rather than violating it**, by
separating two genuinely different events:
- **A LIMIT NUMBER CHANGED** (`INTRADAY 5.0 → 6.0`) ⇒ ✅ config-only. Exactly what
  he asked for.
- **A NEW PRODUCT WAS ADOPTED** (MTF — interest charges, pledge mechanics,
  different margin rules) ⇒ 🔴 **not a number change**, and it *should* require
  deliberate work.

⛔ **No `product_mode` flag tonight.** If MTF ever arrives, *that* unit introduces
the mode and relaxes the pin. ↩️ **Reversible:** change the pin to a bound.

🔬 **Scope note, measured (§3):** the pin governs the sizing path of **79 real CNC
trades** in the current population — ⛔ it is not a theoretical constraint.

---

## 2 — ✅ TAKEN · `ABSOLUTE_MAX_LEVERAGE = 20.0`, TWO BLOCKS, TONIGHT

```yaml
leverage_map:            # OPERATIONAL — routine values
  INTRADAY: 5.0
  COVER_ORDER: 6.0
  DELIVERY: 1.0          # 🔴 PINNED — §1
  BRACKET_ORDER: 5.0

leverage_safety:         # GOVERNANCE — deliberate, reviewed, rarely touched
  min_allowed: 1.0
  max_allowed: 10.0      # INTERNAL SAFETY CEILING
```

⭐ **`ABSOLUTE_MAX_LEVERAGE = 20.0` — a code-side constant.** ⭐ Its rationale
claims **no regulatory number**; it is arithmetic about **typos**:

| typo | result | caught by 20.0? |
|---|---|---|
| dropped decimal on `5.0` | `50` | ✅ |
| dropped decimal on `6.0` | `60` | ✅ |
| doubled digit | `55` | ✅ |
| deliberate values | `12` · `15` · `18` | ⭐ permitted — ⛔ nobody types these by accident |

⇒ ⭐ **20.0 catches every plausible ACCIDENT while permitting a DELIBERATE
governance change up to 20× with ⛔ no code work.**
⚠️ ⛔ **NOT a SEBI limit. ⛔ NOT a broker limit. ⛔ NOT externally mandated.** An
internal absolute — ⛔ and it must never be described otherwise.
↩️ **Reversible:** one constant.

🔴 **`leverage_safety` IS SELF-VALIDATING** — otherwise the governance block
becomes an unvalidated source of capital authority. **All fail closed:**
`min_allowed` missing · `max_allowed` missing · `min_allowed < 1.0` ·
`max_allowed < min_allowed` · `max_allowed > ABSOLUTE_MAX_LEVERAGE` ·
NaN / ±Infinity · non-numeric. ⛔ **No silent default anywhere in this block.**

⭐ **RECORDED:** `min_allowed` / `max_allowed` are ⛔ **NOT routine trading knobs.**
They are governance values, changed deliberately and reviewed.

⇒ ⭐ **The contract now holds in full:** a fat-finger touches ONE block and is
caught · a legitimate change up to 20× touches TWO blocks (two deliberate edits,
⛔ still no code) · beyond 20× needs code, ⭐ correct for an event that exceptional.

---

## 3 — 🔴 THE NEUTRALITY PROOF · ⭐ THE PROPOSED REPLAY IS NOT POSSIBLE — A BETTER ONE IS

### 3.1 · ⛔ THE `qty_by_capital` REPLAY FAILS ITS OWN PRECONDITION

FILE 17 §3 required checking first, and ⛔ not faking a replay. 🔬 **Checked:**

| input needed to recompute `qty_by_capital` | present? |
|---|---|
| `entry_target_price` | ✅ **709 / 709** |
| `margin_reserved` | ✅ **709 / 709** |
| `qty_by_capital` (the output) | ✅ 709 / 709 |
| 🔴 **available capital at sizing time** | 🔴 **NOT PERSISTED — no such column exists** |

🔬 A full column scan of `trades` for `avail|capital|base|bucket` returns only
`qty_by_capital` itself.

⇒ 🔴 **`qty_by_capital = available_capital / (price / leverage)` CANNOT be
recomputed** — the numerator is not stored.
⇒ ⚠️ **AND BACKING IT OUT WOULD BE CIRCULAR:** deriving
`implied_capital = qty_by_capital × price / L_old` and then re-deriving with
`L_new` only re-proves `L_new == L_old` — 🏷️ **a green test that cannot go red.**
⛔ **I am not doing that, and I am not calling it a replay.**

### 3.2 · ✅ A NON-CIRCULAR PROOF EXISTS — AND ITS BASELINE IS ALREADY CAPTURED

⭐ `margin_reserved` is persisted **independently at reserve time**, so
`implied_leverage = qty_planned × entry_target_price / margin_reserved`
is derived from **three stored columns that do not include `qty_by_capital`.**
⇒ ⭐ **Non-circular, and it CAN go red.**

🔬 **BASELINE MEASURED 27-Aug ~11:5x, on the live DB:**

| product (via `orders` LEFT JOIN `leg='ENTRY'`) | rows | min implied | max implied | verdict |
|---|---|---|---|---|
| **MIS** | **495** | **5.0000** | **5.0000** | ✅ **EXACTLY 5.0, zero variance** |
| **CNC** | **79** | **1.0000** | **1.0000** | ✅ **EXACTLY 1.0, zero variance** |
| `(NULL — no ENTRY row)` | **135** | 1.0 | 5.0 | ⚠️ a mix; product unresolvable |

⇒ 🔬 **PROVEN: the deployed `leverage_map` values are EXACTLY what was applied
across 574 production trades with a resolvable product.** ⛔ Not approximately —
`min == max` to four decimals on both.

⇒ ⭐ **THIS IS THE NIGHT'S PRE-FIX EVIDENCE (nine-part contract, item 4), and the
acceptance test is EQUALITY:** after U3, recompute the same expression; **any row
whose implied leverage moves off 5.0 (MIS) or 1.0 (CNC) is an immediate,
unambiguous RED.**

⭐ **It also corroborates L-2 behaviourally:** every MIS trade received **exactly**
`5.0` — ⛔ never a broker-varying figure. 📄 That is what FIX-072 being unwired
looks like from the data side, ⭐ an independent confirmation of the static proof.
⚠️ ⛔ It still does **not** show 5.0 is Zerodha's *actually applicable* margin
(A-6) — ⭐ only that the configured number is the one the system used.

### 3.3 · ⚠️ TWO HONEST LIMITS ON THIS PROOF

1. 🔴 **135 rows (19%) carry NO resolvable product** — the standing schema hazard
   firing exactly as recorded (*"there is no `trades.product`; a missing ENTRY row
   gives `product NULL` = invisible to any product filter"*). ⛔ Those rows cannot
   be attributed per-intent and are **excluded**, ⛔ not silently folded in.
2. ⚠️ 🔬 **`COVER_ORDER` and `BRACKET_ORDER` are NOT EXERCISED — zero production
   rows.** ⇒ Their configured `6.0` / `5.0` are validated but **never applied**.
   🏷️ **NOT EXERCISED** — ⛔ do not report them as proven.

⚠️ ⭐ **METHOD NOTE FOR TONIGHT:** the population is **still growing** — it read
708 at ~10:30 and **709** at ~11:5x. ⇒ 🔴 **Re-capture the baseline AFTER market
close**, immediately before the change, so pre- and post- are the same population.
⛔ Do not reuse today's 11:5x numbers as the post-close baseline.

---

## 4 — B-1 … B-8 ACCEPTED, BINDING (⛔ not re-debated)

| # | accepted |
|---|---|
| **B-1** | **U3-c IS ATOMIC** — remove the default **+** update all dependent real-`FundManager` tests **+** add red-capable missing-map protection **+** run the suite, **ALL IN ONE COMMIT.** ⚠️ **If the count grows substantially beyond 8, STOP AND REASSESS** whether U3 still fits beside the F6 extraction — ⭐ scope discipline outranks finishing every test edit |
| **B-2** | **`POSITIONAL` STAYS INVALID.** Authoritative set = `INTRADAY · COVER_ORDER · BRACKET_ORDER · DELIVERY`. ⛔ Do NOT broaden it to make two old tests green — correct them to the intent they meant |
| **B-3** | **MUTATION-STYLE ACCEPTANCE.** A test must go RED if: the hardcoded map resurrects · unknown-intent→1.0 resurrects · an invalid leverage boots · DELIVERY validation is removed · upper-bound protection weakens. ⛔ Asserting today's valid config is green is **INSUFFICIENT**. ⭐ No framework needed — the requirement is RED-capability |
| **B-4** | **PARITY = ONE VALIDATOR**, not "both files hold the same numbers": same config → same validated representation → same intent resolution → same capital calculation, Live and Paper. ⛔ Never duplicate two validators to claim parity |
| **B-5** | Direction ranking stands. **TOO HIGH = the blowup direction** ⇒ CRITICAL/exit-5 on all four = primary protection. TOO LOW also fails closed (silent non-trading is still wrong). UNKNOWN INTENT fails closed. **FINITE rejected explicitly** — NaN, +Inf, −Inf; ⛔ a range check alone lets them through |
| **B-6** | Error shape: *"Invalid `leverage_map.INTRADAY`: expected a finite value within the approved range."* — naming map, intent AND reason |
| **B-7** | **A-4 STANDS.** FIX-072 may never be wired without declaring its authority model. ⛔ Constructor wiring must never silently change capital authority |
| **B-8** | Evidence labels unchanged, incl. 🏷️ **VACUOUS** for the 0/0 live-margin result. ⛔ Do not cite the zero |

---

## 5 — STATUS · ⛔ NOTHING IS BUILT

**PROVEN (new today):** the configured leverage is EXACTLY what production applied
— MIS `5.0` × 495 rows, CNC `1.0` × 79 rows, zero variance · `main.py:2715` is the
only production `FundManager` construction and it supplies the map ·
`"POSITIONAL"` is not a valid intent yet appears in two test maps.

**NOT PROVEN:** that `5.0` is Zerodha's actually applicable margin (A-6) · that
U3's implementation is correct — ⛔ **not built** · that its red-capable tests
exist — ⛔ **not written** · that `20.0` or `10.0` are externally mandated — ⛔ they
are internal · that ≥8 test files is the true edit count — 💭 predicted only.

**NOT EXERCISED:** `COVER_ORDER` / `BRACKET_ORDER` leverage — zero production rows.

**VACUOUS:** the 0/0 live-margin log entries.

**⛔ NOT DONE:** UNIT 1 · UNIT 2 · UNIT 3 · any push · any test.
🔴 ⛔ **U3 must not be marked DONE or HELD until the red-capable tests actually
prove the contract.** ⛔ HELD ≠ DONE. ⛔ Code existing ≠ contract proven.

⭐ **LANDING RECORD when it ships — exact wording:**
> *"DELIVERY leverage was ALREADY implemented; U3 added ⛔ no second calculation.
> U3 hardened the existing configuration authority by removing latent duplicate
> and silent-fallback sources, pinning DELIVERY to 1.0, and enforcing complete,
> finite, bounded validation across all four intents under a self-validating
> governance block."*
