# FROZEN PREDICTION — EOD LIFECYCLE PIPELINE-AWARE CHECK

**Frozen 25-Aug-2026, IST, BEFORE any code was written.** ⛔ This file is not edited after the build.
**Base:** deployed HEAD `195436bb6323c981d68f313ad7c39858cc0a4653`.
**Unit:** the EOD lifecycle check only (A + C + D, one code path).

---

## THE CHANGE I PREDICT I WILL MAKE

**1 · `core/state_store.py`** — ADD one new read beside `count_active_positions()`, which is
**left byte-identical**:
`get_active_positions_with_identity()` → one atomic query returning, per active trade
(`OPEN`/`PARTIAL`/`PENDING_FILL`): `trade_id · symbol · status · strategy · entry_product`,
via `orders LEFT JOIN … AND leg='ENTRY'`.
🔬 Join-fanout checked in advance: **595/595 trades have exactly one ENTRY order row** ⇒ the LEFT
JOIN cannot duplicate a trade. If that ever stops holding, the count inflates — a stay-up bias.

**2 · `main.py`** — ADD a pure resolver + change **one expression** inside `_eod_self_exit_due`:

```
OLD:  active = int(store.count_active_positions())
NEW:  active = <count of active positions that REQUIRE THIS SERVICE>
```

**Resolution order (Rama's correction — identity is normally KNOWABLE):**
`trades.strategy` → strategy YAML `intent:` — **PRIMARY**
`orders.product` (ENTRY) → `PRODUCT_TO_INTENT` — **SECOND, INDEPENDENT**

**Classification:**
| both known & DISAGREE | → **CONFLICT** → requires service **+ report** |
| strategy known | → resolved = strategy intent |
| only product known | → resolved = product intent |
| neither known | → **UNRESOLVED** → requires service **+ report** |
| resolved = DELIVERY | → does **NOT** require the service (broker holds the OCO) |
| resolved = INTRADAY | → **requires** the service (abnormal survival past square-off) |

⛔ **No literal `"15:30"`.** The square-off deadline is read from the **configured**
`trading_hours.eod_squareoff_time`.

---

## FALSIFIERS — ⭐ each must be able to go RED

| # | prediction | falsified if |
|---|---|---|
| **F-1** | **T-1 FAILS on the pre-fix tree.** Delivery-only carry (BALUFORGE 1 @ 610.45 + KAMATHOTEL 2 @ 220.56 = ₹1,051.57) ⇒ new code EXITS; old code STAYS UP | T-1 passes against `195436b` ⇒ the test proves nothing |
| **F-2** | **T-6: all three other consumers unchanged.** `count_active_positions()` is **byte-identical** at `195436b` vs the unit, proven by `git diff` on the function, and `risk_engine.py` / `main.py:3207` / `portfolio_allocator.py` are untouched | any diff hunk touches that function or those call sites |
| **F-3** | **T-3 asserts BOTH** stay-up **and** a report. A silent stay-up is half a failure | the test asserts only the boolean |
| **F-4** | **T-5 no regression** — empty book still EXITS, identical to old code | empty-book behaviour differs |
| **F-5** | **The 4 existing test files that call `_eod_self_exit_due`** (`test_main`, `test_mc8_async_hardkill`, `test_service_window_config`, `test_alert_delivery_phase1`) **still pass unchanged** — the signature stays backward-compatible | any of them needs editing to pass |
| **F-6** | **The flatten gate is untouched.** `_ACTIVE_FLATTEN_IN_PROGRESS` semantics and ordering are byte-identical; the flatten check still runs BEFORE any position query | the flatten branch moves or changes |
| **F-7** | **The gate is a clean differential** — the new-failure set vs base is EMPTY | any test fails on the unit that passed on base |

## WHAT I EXPECT TO BE HARD / MIGHT GO WRONG

- 💭 The 4 existing test files mock the store. If they pass a `Mock`, the new read returns a `Mock`
  and iteration raises. **Prediction: I handle this by falling back to `count_active_positions()`
  on any failure of the new path, logging at ERROR.** The fallback direction is *conservative* — it
  counts MORE positions, so it biases toward staying up.
  ⚠️ **If instead I find myself EDITING those 4 test files to make them pass, F-5 is falsified and I
  must say so.**
- 💭 `_eod_self_exit_due` returns a 2-tuple consumed by the thread body. Conflicts need a report
  channel without breaking arity ⇒ **prediction: an optional `on_unresolved` callback, defaulted to
  None**, latched once by the caller (same shape as the existing `warned_not_flat` latch).
- 💭 Risk: the resolver needs strategy intents, which live in `strategies/loader.py`
  (`StrategyConfig.intent`), not `config_loader`. ⇒ prediction: pass a resolver function from the
  main() call site, not a new import inside the gate.

## ⛔ WHAT I PREDICT WILL **NOT** CHANGE

`count_active_positions()` · `capital/risk_engine.py` · `allocation/portfolio_allocator.py` ·
`main.py:3207` · the kill switch · `_ACTIVE_FLATTEN_IN_PROGRESS` · EXITING-blindness (inherited, not
fixed) · any capital/config/sizing/risk surface · `tier_multipliers` · cron · systemd units.

## ⛔ NOT DONE IN THIS UNIT
No push. No deploy. No service action. No cron. No paper drill (paper nets by SYMBOL, live Kite per
(SYMBOL, PRODUCT) ⇒ a paper green on a product-semantics change is vacuous).
