# BUILD RECORD — MIS AUTO-SQUAREOFF ORCHESTRATOR · 28-Aug-2026

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.

> ## 🏷️ **STATUS: BUILT · GATED · COMMITTED LOCALLY · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED · 🏷️ NOT EXERCISED IN PRODUCTION.**
> ⛔ A production-safe claim is **NOT** made. ⭐ The 15:07/15:10 passes have never
> run and cannot before **Mon 31-Aug 08:15**.

Commits (worktree `mis-work`, branch `fix/mis-autosquareoff-28aug`, base `52ccb4f`):
**`6f00b4d`** the orchestrator · **`effff24`** G (adapter parity) + D (C-3 16/18).
🔬 ROOT untouched at `feat/delivery-config-split @ 6d24a83`.

---

## 1 — THE GATE

| | |
|---|---|
| command | `python -m pytest tests/unit tests/integration` — ⭐ the frozen form, ⛔ not `run_tests.py` |
| SHA | `effff24b8d3c5cec025d4ded60d030a5dca2e239` |
| window | `15:36:17 → 15:53:59`, `1018.73 s` |
| **RESULT** | 🔬 **`10 failed · 5,956 passed · 4 skipped`**, raw `PYTEST_RC=1` |
| failure set | ⭐ **ID-IDENTICAL** to the standing recorded ten (`ledger:1556`) |
| **NEW-FAILURE SET** | ✅ **EMPTY** |

🧮 **The delta decomposes exactly, ⛔ nothing unexplained:**

```
C-4 serial baseline @ 52ccb4f ......................... 5,896 passed
+ tests/unit/test_mis_autosquareoff.py ................ +59   (35 + 24 wrapped)
+ tests/unit/test_unit3a_leverage_validation.py ....... + 1   (C-3 accounting)
                                                        ─────
                                                        5,956  ✅ measured
```

⛔ **No general EOD behaviour changed.** 🔬 `orders/eod_squareoff.py` is
**byte-unmodified**; `test_eod_squareoff_general_settings_are_untouched` pins
`eod_squareoff_time 15:17`, `exit_protocol LIMIT_THEN_MARKET`, `limit_grace_sec
120`, `entry_end 15:00`.

---

## 2 — 🔬 MUTATION EVIDENCE · **TWELVE** IN THE HARNESS + **THREE** ONE-OFFS

⭐ Each names an observed **unsafe event** (FILE 27 A-8), ⛔ not "goes RED".

> 🔴 **CORRECTED 28-Aug.** ⛔ This header read *"14 MUTATIONS, ALL RED"* and was
> wrong **in both directions**: the reproducible harness holds **TWELVE**, and the
> table below it lists **FIFTEEN** — twelve plus three one-offs run separately
> (the last three rows). ⛔ *Fourteen* was neither number.
>
> 🔬 **Re-run 28-Aug from a `git`-verified-clean tree at `22a143f`:**
> `MUTATIONS RUN: 12 · RED: 12 · ALL MUTATIONS RED: True`, tree clean after.
> ⚠️ An earlier re-run reported one row **ANCHOR-MISSING** — ⛔ *not* RED — and a
> later one ran against a **contaminated file**. Both are recorded, with cause, in
> [`MUTATION_AND_FAILURE_EVIDENCE_28-Aug-2026.md`](MUTATION_AND_FAILURE_EVIDENCE_28-Aug-2026.md) §3.

| mutation | unsafe event it would allow |
|---|---|
| `MIS_PRODUCT → "CNC"` | a CNC position is squared off |
| `MIS_PRODUCT → "CO"` | a CO position is squared off |
| predicate widened to `{MIS, CNC}` | CNC enters the MIS path |
| `_product_of` defaults to `"MIS"` | a missing product becomes eligible |
| `qty != 0` → `qty > 0` | a SHORT is never closed |
| drop cancel-before-exit | an exit is submitted with a live SL ⇒ position reversed |
| remove `max(0, …)` floor | a negative sleep |
| remove the R-2 cap | PASS 1's promotion crosses CHECK_2 |
| PASS 2 uses `LIMIT` | PASS 2 blocks past the cutoff |
| shared fired flag | PASS 2 never fires at all |
| drop the margin ≥ poll floor | an incoherent config is accepted |
| query failure → `[]` | a broker outage reads as flat |
| *(the twelve above are the harness; the three below were run as one-offs)* | |
| Pass-1 loses its product filter | the 15:17 sweep could reach CNC |
| new unit inherits CO | CO eligibility leaks in |
| **+ G:** revert paper default to `"MIS"` | paper more permissive than live |

---

## 3 — 🔒 PREDICTIONS 1–29 · SCORED AGAINST RAW OUTPUT

| # | verdict | evidence |
|---|---|---|
| 1, 2, 3 | ✅ GREEN | flat / CNC-only book ⇒ zero orders |
| **4** | ✅ **GREEN** | 🔬 0 new failures; delta decomposes exactly |
| 5, 8, 10, 13, 14 | ✅ GREEN | mutations RED |
| 6 | ✅ GREEN | 🔬 `eod_squareoff.py` byte-unmodified |
| 7 | ✅ GREEN | `reset_daily_pnl` still fires at 15:17 |
| **9, 16** | ✅ **GREEN ×3** | structural SQL · 2 mutations RED · 🔬 **live behaviour (§4)** |
| 11, 15 | ✅ GREEN | `entry_end ≥ CHECK_1` fails closed |
| 12 | ✅ GREEN | missing product excluded both modes; mutation RED |
| **17, 20** | ⚠️ **GREEN under the MEASURED-BOUND ESTIMATE ONLY** | ≈2.035 s vs 120 s. ⛔ **NOT** "guaranteed worst case" — 🏷️ `cancel_order` n=4, `place_order` n=10 are THIN, and ⛔ broker latency can exceed any historical maximum |
| **18** | 🔴 **REFUTED** | a decrement path exists (`order_reconciler.py:2408`). ⭐ Recorded as a miss; ⭐ the *method* failed, not just the answer |
| **19** | ✅ **GREEN** | G built; reverting the paper default turns `test_19` RED |
| 21 | ✅ GREEN | grace capped to 64 s at +90 s; promotion ≤ CHECK_2 |
| 22, 27 | ✅ GREEN | mutations RED |
| **28** | ✅ **GREEN — ⛔ RE-EARNED, not as first scored** | 🔴 First scored GREEN on *"mutations RED"* when that mutation had returned **ANCHOR-MISSING** — ⛔ it never ran, so it proved nothing and the GREEN was **unearned**. 🔬 Cause was **tooling**: COMMIT 1 moved the guard to `core/mis_squareoff_timing.py:129` and the harness still patched `orders/`. The validation is where it was designed to be and still fails closed (`margin_sec=4, poll_interval_sec=5` ⇒ `MisSquareoffConfigError`). ⭐ Anchor repointed, re-run **RED** from a clean tree ⇒ GREEN now stands on a mutation that actually executed |
| 23 | ✅ GREEN | `limit_grace_sec=9999` ⇒ PASS 2 completes < 5 s |
| **24** | ⚠️ **PREMISE DOES NOT OBTAIN** | 🔬 the delay placement is **per-SYMBOL** (`eod_squareoff.py:1378` `if i < len(rows)-1`), so the pessimistic per-call case is not the code's behaviour. Its ~8.245 s bound is arithmetic, ⛔ not a measured run |
| 25 | ✅ GREEN | serial poller max-in-flight == 1, **plus a non-vacuity control** proving the detector can observe 2 |
| 26 | ✅ GREEN | PASS 1 fails every attempt ⇒ PASS 2 still runs; `PASS_1_ABANDONED_FOR_PASS_2` |
| 29 | ✅ GREEN (2 of 3 clauses) | grace 0, no sleep, `PASS_1_DEGRADED_TO_MARKET` recorded. ⚠️ *"PASS 2 still evaluated on time"* is covered by separate tests, ⛔ **not asserted in the same scenario** |

⭐ **24 GREEN · 2 conditional · 1 REFUTED · 1 premise-void.** ⛔ No prediction was
edited after seeing a result.

---

## 4 — ⭐ TWO DEFECTS THE PROCESS CAUGHT, ⛔ NOT ME

**(a) My own unit latched a failed PASS 1 as *done*.** A PASS 1 whose broker query
raised was marked `_fired[PASS_1] = True`, breaking both the bounded-retry count
and the B-2 starvation guard. ⭐ **Same class as reading a query failure as flat** —
*"we never found out"* silently becoming *"we finished"*. Fixed with
`_INCONCLUSIVE_STATES`; `test_26` and `test_pass_1_retries_are_bounded` are the
falsifiers.

**(b) My main.py wiring caused 23 NEW `test_main` failures.** The fixture builds a
MagicMock config, so `MisSquareoffTiming.build()` raised during the boot sequence.
🔬 First gate: `33 failed / 5,928 passed` vs the baseline 10.

> ⭐ **The fix was completing the test's config mock — the exact `service_window_end`
> precedent — ⛔ NOT relaxing the validation.** ⚠️ Relaxing it was the tempting wrong
> fix and would have destroyed the fail-closed property #28 exists to protect.
> ⭐ And the failure was **fail-closed working correctly**: an unparseable cutoff
> stopped the boot rather than defaulting. ⭐ Found here, ⛔ not at 08:15 on Monday.

---

## 5 — ⛔ ITEM C · **BLOCKED · STOPPED AND REPORTED, ⛔ NOT IMPROVISED**

🔬 `test_12_mis_sizing_is_byte_identical` exists **only** at
`6d24a83:tests/unit/test_two_pipeline_split.py`, on `feat/delivery-config-split`.
⛔ It is **not** at `52ccb4f`.

⇒ Repairing it requires editing the **F2 working tree**, which the standing hazard
forbids outright; ⛔ and porting it into this worktree would be importing F2 scope,
also forbidden (FILE 25 C). ⇒ 🏷️ **It belongs to the F2 track (Sat/Sun), ⛔ not
tonight.** ⛔ Nothing was improvised.

---

## 6 — WHAT IS **NOT** CLAIMED

⛔ PASS 2 is production-proven · ⛔ the 15:07/15:10 paths have been exercised ·
⛔ special sessions are handled · ⛔ broker latency is bounded · ⛔ 2.035 s is a
guaranteed worst case · ⛔ single-thread execution is guaranteed in the NEW code
*because* the OLD scheduler is single-threaded (⭐ it is **tested**, #25, not
inherited) · ⛔ predictions are green beyond the evidence above.

🏷️ **Known limitation, recorded in the config's own provenance block:** the cutoff
is **absolute IST, not session-relative**. `special_sessions` (FIX-094) moves
`eod_squareoff_time` per date but ⛔ does not move this, and ⚠️ **the ordering
invariant will not detect the divergence** because `15:12 < 19:12` is numerically
valid. ⛔ Not built tonight. 🏷️ `special_sessions` ships fully commented out ⇒ **NOT
EXERCISED**.

🏷️ **Also standing, ⛔ untouched:** S-1's eventual-consistency observation on the OLD
path · the post-reset P&L window measured live today · P-1's log-legibility defect.

⛔ push ≠ boot · ⛔ executed ≠ exercised · ⛔ exercised ≠ load-bearing ·
⛔ green ≠ red-capable · ⛔ started on time ≠ completed before cutoff ·
⛔ order accepted ≠ position closed · ⛔ broker query failure ≠ flat ·
⭐ **SIMPLE BY DECISION, ⛔ NOT SIMPLE BY ACCIDENT.**

## END
