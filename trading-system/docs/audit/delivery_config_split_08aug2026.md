# TWO-PIPELINE SPLIT — BUILD RECORD, 08-Aug-2026

**Status:** `<BUILT>` — ⛔ NOT DEPLOYED, NOT PUSHED, NOT VERIFIED LIVE.
**Branch:** `feat/delivery-config-split` · ⛔ deliberately NOT riding with F6.

> **"One system, one command centre — from signal receipt to order management to EOD
> report. But TWO PIPELINES, delivery and intraday, each trading on their OWN config
> settings. NEVER shared values. No combined metric, limitation factor, or setting."**
> — Rama, 08-Aug-2026

⛔ **This is a RECORD, not a design document.** What was built · the numbers · the tests.

---

## 1 · THE TEST APPLIED TO EVERY GATE

**Can a delivery trade change what intraday is allowed to do, or the reverse?**
Up to 07-Aug the answer was **yes in four places**, and only one of them was written down.

| coupling | before 08-Aug | now |
|---|---|---|
| open-position count | the intraday branch counted **ALL** positions incl. delivery — a delivery carry consumed an intraday slot | intraday counts non-delivery only |
| daily trade count | same | same |
| consecutive-loss streak | **one shared streak** — 4 intraday losses halted delivery too | one streak per pipeline (delivery 3, intraday 4) |
| in-flight reservations | `count_live_reservations()` was **unscoped** — an in-flight delivery entry filled an intraday slot | `count_live_reservations_for_bucket()` |

🔑 **The fourth is the one that would have survived a limits-only build**: it lives in
memory, not in a table anyone can query. ⛔ **Separating the LIMITS was the easy half.
A shared counter with two limits reading it is still a shared limit.**

🏷️ The `A5` note in `risk_engine` called the first coupling an *"INTENTIONAL asymmetric
coupling … academic, because capital binds long before these counts."* It is **removed**,
not softened: academic or not, it is a delivery trade changing what intraday may do.

---

## 2 · THE NUMBERS — MEASURED, on the real config

⚠️ **No rupee capital value exists in config** (the ACTUAL is a daily `fm_ledger` INIT
figure), so two reference totals are shown. The **ratios are capital-invariant**.

### A · INTRADAY DAILY-LOSS LIMIT — rebased onto the intraday bucket ⇒ **TIGHTER**

| total | BEFORE (3% × total) | AFTER (3% × 70% bucket) | change |
|---|---|---|---|
| ₹1,00,000 | **₹3,000.00** (3.00% of total) | **₹2,100.00** (2.10% of total) | **−₹900 (−30%)** |
| ₹10,00,000 | **₹30,000.00** | **₹21,000.00** | **−₹9,000 (−30%)** |

⭐ A consequence of "no shared purse", ⛔ **not a separate tightening decision.**

### B · DELIVERY DAILY-LOSS LIMIT — new, its own purse

BEFORE: **no separate limit existed** — delivery losses counted against the one shared
figure. AFTER: **3% × the 30% bucket** = ₹900 / ₹9,000 at the two references (0.90% of
total). ⛔ **REALISED only.**

### C · DELIVERY POSITION SIZE — ⚠️ **A REAL EXPOSURE INCREASE**

Representative delivery setup: entry ₹500, SL ₹475 (5% stop), leverage 1.0 (unleveraged).

| total | BEFORE qty / value | AFTER qty / value | change |
|---|---|---|---|
| ₹1,00,000 | **10** / ₹5,000 | **15** / ₹7,500 | **1.50×** |
| ₹10,00,000 | **100** / ₹50,000 | **153** / ₹76,500 | **1.53×** |

**Both sides are CONCENTRATION-bound.** BEFORE = base TOTAL, risk 1%, conc 10%, tier
**LOW ×0.50**. AFTER = base DELIVERY BUCKET, risk 2%, conc 30%, tier **MEDIUM ×0.85**.
⭐ **On a HIGH-tier delivery signal (score ≥ 63) the AFTER qty is 17 / 180 — ×1.7–1.8.**

⭐⭐ **The offsetting halves are worth seeing separately, because "we doubled the risk
percentage" would be the wrong summary:** rebasing onto the 30% bucket makes the risk
term *smaller* in rupees (2% × 30% = 0.6% of total, vs 1% before) and cuts the
`max_position_value` ceiling from ₹400,000 to ₹120,000. **The increase comes almost
entirely from the TIER**, not from the percentages.

### The tier mechanism — why the numbers look odd

| | min / medium / high | effect |
|---|---|---|
| scorer **measured ceiling** | **65** | 4 of 10 steps hardcoded `None` |
| INTRADAY | 60 / 65 / 80 | **HIGH unreachable**; 60-64 = LOW **×0.50** |
| DELIVERY | **60 / 60 / 63** | 60-62 = MEDIUM ×0.85 · 63-65 = HIGH ×1.0 |

⛔ **THE ENTRY GATE IS NOT LOOSENED — delivery's pass mark is the same 60.** Only the
size of a position that already passed changes. Delivery **LOW is unreachable by
construction** (medium == min_pass): a delivery signal below the pass mark is *rejected*,
not sized small. That is why the delivery ordering is `high > medium >= min_pass`.

🔴 **This is what halved a live position 8 → 4 on 07-Aug**, and it had been doing so
since delivery went live.

### Caps

`intraday 5 open / 10 per day` · `delivery 3 open / 5 per day`
⇒ **8 concurrent positions and 15 entries per day are now CORRECT.**

---

## 3 · TESTS — 33, RED-first

`tests/unit/test_two_pipeline_split.py` — **33 passed**.

**RED proof by experiment, ⛔ not by assertion.** Reverting only the BEHAVIOURAL half
(engine · state_store · sizer · fund_manager · market_windows · scorer · screener ·
processor · receiver · main) while keeping the DECLARATIVE half (config · loader ·
resolver): **13 failed / 20 passed.** ⭐ The 20 that stay green are precisely the
resolver/config tests, which is the correct result — it isolates what the *code* change
buys from what the *config* change buys. A bare `git rm` of the new module gives only an
ImportError, which proves the tests import it and nothing about their assertions.

Two tests carry an explicit **control** so they cannot be vacuous: test 05 runs the same
state through a single-book engine and asserts it *rejects*; test 07 asserts the same
4-loss state *does* stop an intraday entry.

⚠️ **PARITY, stated per test rather than once:** the resolver, SQL predicate, sizer and
admission tests are pure and paper exercises them identically. ⛔ **Paper CANNOT exercise
a real CNC round trip, T+1 settlement, or a carried position becoming a holding.** Test
15 seeds a carried row in SQL — that proves the **COUNT**, ⛔ nothing about settlement.

---

## 3a · 🔴 THE REGRESSION GATE FOUND THREE REAL DEFECTS IN THIS BUILD

**First full run: `PYTEST_RC=1` · 21 failed / 5,603 passed / 4 skipped in 883.96 s.**
⚠️ **The wrapper exited 0 because its last command was a `tail` — `D5.1` again.** The RC
was captured to a variable and read back separately; ⛔ **the wrapper's exit code is not
the gate's verdict.**

**SET-compared against the recorded §8.12 baseline nine — ⛔ not count-matched:**
**baseline-only = 0 · NEW = 12.** ⛔ **None of the twelve was labelled "known PC-env"** —
that is a label, not a diagnosis. Diagnosed:

| # | new failures | diagnosis | fix |
|---|---|---|---|
| **10** | `test_hard_gate` ×6 · `test_forward_shadow_empty_day` ×4 | 🔴 **CAUSED BY THIS BUILD.** `scripts/forward_shadow_record.py:47` reads `config/scoring_weights.yaml` with a bare `Path.read_text()` — **no `encoding=`**. My comment added glyphs containing bytes `0x90`/`0x9B`, which **cp1252 cannot decode**. ⚠️ My first reading — *"non-ASCII broke it"* — was **wrong**: the file already carried **51** non-ASCII bytes that cp1252 happens to decode. It is the specific bytes | config comment rewritten **ASCII-only**; `codecs.decode(raw, "cp1252")` now succeeds |
| **1** | `test_the_streak_has_exactly_one_data_source` | The assertion was `src.count("recent_trade_pnls") == 1` — a **TEXT PROXY** for "one source". The split gives one source **per pipeline**, so the literal count is 3 | ⭐ **PROPERTY VERIFIED BEFORE THE NUMBER WAS TOUCHED:** `_count_trailing_losses` is still **one definition + one call**, and there is still exactly **one selection point**. Assertion rewritten to those two invariants, with the reason recorded in the test |
| **1** | `test_snapshot_has_all_nine_fields` | 🔴 **CAUSED BY THIS BUILD.** I added 4 keys to `ApprovalResult.snapshot`. **RE11 is a LOCKED design decision** pinned by that test | **REVERTED.** §3.5 wants the source on every *decision*; the INFO log already carries it. ⭐ Widening a locked contract to make a new feature more convenient should cost its own decision, not ride inside another |

### ✅ RE-RUN AFTER THE FIXES

**`PYTEST_RC=1` · 9 failed / 5,616 passed / 4 skipped in 896.00 s.**
**SET-compare: the failing set is the §8.12 baseline nine, LINE FOR LINE — zero new,
zero missing.**
⭐ **And the PASS COUNT reconciles with no remainder: `5,582 + 34 = 5,616`** (34 = this
build's new test file) — the check a failure-set compare **cannot** make, because it says
nothing about a test that stopped being COLLECTED.

🏷️ **REGRESSION ACCEPTED — zero NEW failures; 9 known baseline failures; RC=1 by baseline
convention.** ⛔ Not "gate green": *accepted* is a judgement with its basis attached.

> ### ⚠️ **THE `forward_shadow_record.py:47` UNENCODED READ IS A REAL LATENT DEFECT, RECORDED NOT FIXED.**
> It is on the **18:15 forward-shadow path, whose output cannot be regenerated**, and a
> single out-of-codepage character in a config comment is enough to crash it on any host
> whose default codec is not UTF-8. ⛔ **Not fixed inside this card** — that path is not
> this build's to touch. **The config file is kept ASCII-only instead**, with the reason
> written at the top of it so the next editor does not re-trip it.

---

## 4 · 🔴 STOP-AND-REPORT (§3.7) — THE CAPS WERE **NOT** RENAMED

§3.7 says rename or re-scope, **and STOP if another caller depends on the portfolio-wide
meaning.** ⛔ **The condition fires.** The engine's *behaviour* is now intraday-only (that
is §0 and test 5, non-optional); the **keys are unchanged** and these readers still
present them as global:

| reader | what it does with them | impact |
|---|---|---|
| `core/config_auditor.py:442` | `max_cum = risk_per_trade_pct × max_open_positions` | 🔴 **cumulative-risk audit is now intraday-only but does not say so**; delivery's 2%×3 is not audited at all |
| `ops_dashboard/.../capacity.py:135-138` | labels them **`global/day`** and **`global/concurrent`**, comparing to `open_positions_count()` (**all** positions) | 🔴 **will read "7/5 open" and look breached when nothing is** |
| `ops_dashboard/.../strategy_tower.py:122` | `global_max_open` | misleading label |
| `ops_dashboard/.../risk_capital.py:61` · `trading.py:95` · `operations.py:58` | surfaces the raw values | misleading label |
| `allocation/portfolio_allocator.py:41` | free-slot arithmetic | default-OFF; would over-count free slots if enabled |
| `scripts/preflight/checks/config_integrity.py:116` · `scripts/system_manager.py:141` · `reports/daily_trade_review.py:1234` | reads / displays | display only |

⇒ 🔴 **OWED RAMA:** rename to `intraday_max_open_positions` / `intraday_max_daily_trades`
and fix these nine sites, **or** leave the names and fix the *labels*. ⛔ Not decided here.
⚠️ **The dashboard one is the live-facing one** — it will look wrong on the first day a
delivery position is carried.

---

## 5 · REMAINING CROSS-PIPELINE COUPLINGS — named, ⛔ not resolved

1. 🔴 **`one_trade_per_symbol_direction_per_day: true`** — **the one genuinely
   cross-pipeline GATE left standing.** A delivery entry on a symbol blocks an intraday
   entry on the same symbol+direction that day, and vice versa. ⛔ **That is OPEN-1,
   unruled — flagged here, deliberately NOT resolved.**
2. ⚠️ **`max_sector_exposure_pct: 0.40`** — one sector cap across both books, resolved
   against **total** capital. Not in scope; naming it so it is not mistaken for split.
3. ⚠️ **The unrealized-MTM term in DAILY_LOSS is not pipeline-scoped** (a per-trade
   in-memory map with no product key). Delivery is REALISED-only so it never consumes it;
   for intraday it is unchanged. ⛔ **If `daily_loss_include_unrealized` is ever flipped
   ON, a delivery position's mark would move the INTRADAY gate. Resolve before flipping.**
4. ⚠️ **The webhook edge cannot resolve a product** (it has the scanner, not the strategy
   objects), so it now uses the **WIDEST** age limit across pipelines and
   `signal_processor` makes the authoritative per-pipeline call after its strategy
   lookup — still before any sizing or order. ⛔ Restoring the intraday value at the edge
   would silently re-create a shared limit.
5. ⚠️ **Every count here counts DB ROWS, not broker reality.** A phantom `OPEN` row (the
   F6 defect class) occupies a delivery slot that does not exist at the broker. Pre-existing
   and unchanged by this build.

---

## 6 · §4 — DETERMINED WHILE BUILDING

**4.1 — the "10-minute entry timeout" is `signal_queue.expiry_sec: 600`.** **(S)** its own
comment: *"WR6: 10 min — Chartink triggered_at is scan time, not delivery time"*, and it
is what `webhook_receiver` and `signal_processor` both read for signal AGE.
⛔ `order_monitor.fill_timeout_sec: 60` is a different mechanism — it cancels an *unfilled
order*, not a stale signal.

**4.2 — `is_entry_allowed_for_strategy()` did NOT need a product argument.** A new sibling
`is_entry_allowed_for_pipeline(now, policy)` was added instead, and the chain is
**pipeline floor → per-strategy window**, exactly as the global floor already worked. ⭐ A
product argument on the strategy check would have conflated two different scopes in one
function.

---

## 7 · ⚠️ ONE JUDGEMENT CALL — INTRADAY SIZING DID **NOT** REBASE

§3.4 says *"every intraday percentage against the intraday bucket"*; §5 test 12 says
*"MIS sizing byte-identical to today"*. **Both cannot hold** — intraday sizing resolves
against TOTAL capital today.

**Resolved:** delivery sizing → the delivery bucket (new behaviour, breaks nothing);
**intraday sizing → TOTAL capital, unchanged**; the intraday **daily-loss** limit **does**
rebase (§3.4's only NAMED consequence, and the one it asked to have measured).
Recorded in `PipelinePolicy.sizing_base` with the one-line change needed to reverse it.
🔴 **Rama's to overrule** — rebasing intraday sizing too would cut every MIS position ~30%.

---

## 7a · 🔴 THREE THINGS WAIT ON RAMA — **RECORDED, ⛔ NOT RESOLVED**

### 7a.1 · C5 — **CLASSIFIED, ⛔ NOT TUNED**

**5 intraday slots × 1 % = 5.0 % of total theoretical aggregate open risk, against a
2.10 % daily realised stop.** ⭐ **The warning is TRUE, and the split made it VISIBLE
rather than creating it** — before the rebase the check compared a fraction of TOTAL
against a fraction of the BUCKET and was quiet for the wrong reason.

> ## 🔑 **IT IS A CLASSIFICATION QUESTION, NOT A NUMBER QUESTION.**
>
> | if the intended design is… | then… |
> |---|---|
> | **a SIMULTANEOUS-EXPOSURE ceiling and a DAILY REALISED stop are DELIBERATELY DIFFERENT CONTROLS** | ⭐ **the warning is a risk-SHAPE notice and NOTHING needs changing.** Five positions can be open at once; the daily stop ends the day before they all resolve badly. The two answer different questions |
> | **the invariant is that theoretical aggregate open risk may NEVER exceed the daily stop** | 🔴 **that is a RISK-POLICY decision**, and one of `5`, `1 %` or `2.10 %` has to move |

⛔ **Not silently changed. None of the three numbers is touched.**

### 7a.2 · THE SIZING NUMERATOR — **asked in HIS terms, ⛔ not ours**

`qty = capital-per-scrip ÷ SL points` differs from the running code by **~140× at ₹10k**
depending on what the numerator is. ⛔ *"Risk budget vs deployable capital"* is **our
vocabulary**, and asking it that way asks him to learn our words to answer his own
question.

> ### ⭐ **THE QUESTION TO PUT: *"What fraction of your money are you willing to lose on ONE trade if its stop is hit?"***
> **His answer IS the numerator.** *(Today's code says 1 % of total — ₹100 on ₹10k.)*
> ⛔ Nothing is built until he answers.

### 7a.3 · THE `margins()` READING — ⛔ **a measurement, not a decision**

Added to `MONDAY_10-Aug-2026_PREDICTION.md` **§3.6b** as an operational step, **after
E1–E7 are scored**. ⛔ **If no natural delivery entry occurs, it does not happen** —
`NOT MEASURED` is a valid outcome and a trade must not be manufactured for it.

---

## 8 · WHAT IS DELIBERATELY SHARED

One broker session · one signal queue (capacity / backpressure / warning) · one clock ·
one kill switch · one alert channel · one database · one EOD report · `min_qty_threshold`
· `min_tick_size` · `gtt_sl_limit_offset_pct` (3%, a delivery-leg mechanic, asserted
unchanged by test 11). **One command centre, two books.**
