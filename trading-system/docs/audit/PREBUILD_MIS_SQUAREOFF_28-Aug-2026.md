# PRE-BUILD RECORD — MIS AUTO-SQUARE-OFF UNIT (FILE 22 §2)

🚦 **PRE-BUILD REVIEW GATE: VERIFY → REPORT → STOP → WAIT.** This unit submits
**exit orders on the capital/order path**, so the standing gate applies. ⛔ Nothing
is built until 👤 Rama rules on §3 below.

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.

---

## §1 — B-1's TRACE · ✅ COMPLETE

**The question FILE 22 asks: is `circuit_breaker_force_close_15:15` the MIS
square-off, or a different control that merely coincides in time?**

> ### 🔬 **ANSWER: A DIFFERENT CONTROL. IT CLOSES NOTHING.**

`main.py:693-698`, quoted:

```python
"circuit_breaker.force_close_triggered: soft_kill, EOD squareoff handles positions"
kill_switch.soft_kill(reason="circuit_breaker_force_close_15:15",
                      triggered_by="order_monitor")
```

⭐ `main.py:704` even carries `⛔ Do NOT restore "will close all positions"`.
⇒ **Per B-1: LEAVE IT.** ⛔ It is not the square-off and must not be moved.

### 🔴 AND THE SQUARE-OFF DOES EXIST — so B-1's "do not duplicate" binds

🔬 `orders/eod_squareoff.py` — a **polling thread** (5 s interval) firing at
`trading_hours.eod_squareoff_time` = **`"15:17"`** (`config/system_config.yaml:49`).

🔬 **What that one trigger actually does, measured from the 27-Aug run:**

| # | step | is it square-off? |
|---|---|---|
| 1 | `soft_kill` (skipped if already active) | kill control |
| 2 | **Pass 1: cancel all pending orders** | ✅ square-off |
| 3 | sleep 2 s | — |
| 4 | **Pass 2: exit all open positions** (MIS/CO, broker-filtered) | ✅ square-off |
| 5 | EOD summary | reporting |
| 6 | **WAL checkpoint** (FIX-047) | 🔴 **day-boundary bookkeeping** |
| 7 | **`fund_manager.reset_daily_pnl`** | 🔴 **day-boundary ACCOUNTING** |

> 🔴 **`eod_squareoff` IS A COMPOUND END-OF-DAY ROUTINE, ⛔ NOT A SQUARE-OFF TIMER.**
> ⇒ **Neither branch of B-1 applies cleanly**, and the difference is not cosmetic.

---

## §2 — 🔴 WHY "JUST MOVE 15:17 → 15:07" IS UNSAFE

🔬 `capital/fund_manager.py:1687-1701` — `reset_daily_pnl` writes a **`RESET_PNL`
ledger entry with `pnl_delta = -old_pnl`** so the day's `SUM(pnl_delta)` becomes 0.
⭐ It is a **day-boundary accounting act**, ⛔ not a display reset.

⇒ Moving the single `eod_squareoff_time` to `15:07` moves that reset **10 minutes
earlier**, and:

> 🔴 **ANY REALISED P&L LANDING BETWEEN 15:07 AND 15:17 WOULD BE BOOKED *AFTER* THE
> DAY'S RESET.** ⚠️ And such fills are **expected, not hypothetical**: a **non-CAS**
> MIS position is auto-squared by the broker at **15:25** — 📄 eighteen minutes after
> the proposed reset.

🏷️ **This is a silent money-path defect**, exactly the class the standing hazards
name. ⛔ It would not raise an error; the day's P&L would simply be wrong.

⇒ ⛔ **DO NOT MOVE `eod_squareoff_time`.**

---

## §3 — 🔴 THE ONE DECISION FOR 👤 RAMA · ⛔ NOTHING BUILT UNTIL HE RULES

⭐ **PROPOSED (mine): ADD a dedicated two-pass MIS square-off at the derived
`15:07` / `15:10`, and LEAVE `eod_squareoff_time: 15:17` exactly as it is.**

⭐ **It does NOT violate B-1's "do not build a second square-off subsystem", because
it builds NO second selector.** It is a **scheduler + named wrapper** that invokes the
**existing, already-verified** exit path:

| B-1 concern | how this respects it |
|---|---|
| no duplicate selector | reuses `EMERGENCY_FLATTEN_PRODUCTS` + the existing broker-position filter |
| no duplicate exit construction | reuses the existing direction-aware exit-order path |
| no second subsystem | new code = **timing + states + telemetry only** |

⇒ At 15:17 the existing routine still runs and now finds **0 MIS positions** — ⭐ the
correct empty-book behaviour, and a **free backstop**. Bookkeeping stays at 15:17.

🔴 **THE ALTERNATIVE, IF 👤 RAMA PREFERS THE LITERAL FILE 22 READING** — move
`eod_squareoff_time` to 15:07 — ⛔ **requires first splitting the P&L reset and WAL
checkpoint out to their own later trigger.** ⭐ That is a **larger** change on the
capital ledger, ⛔ not a smaller one.

---

## §4 — SCOPE · ⭐ MOST OF FILE 22 §2 IS ALREADY SHIPPED AND CORRECT

🔬 Measured 28-Aug at `52ccb4f` (full evidence: `FILE21_MIS_AUTOSQUAREOFF_28-Aug-2026.md`).

| FILE 22 item | status | evidence |
|---|---|---|
| **B-2** MIS-only, authoritative product | ✅ **ALREADY CORRECT** | `eod_squareoff.py:1086` filters on the **broker position's** `p.product` against `EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS","CO"})` (`core/constants.py:42`). ⛔ Never strategy intent, ⛔ never GTT presence, ⛔ never `trades.product` (HAZ-4). |
| **B-3** `qty != 0`, shorts BUY to close | ✅ **ALREADY CORRECT** | `:1086` `int(p.qty) != 0` · `:1169` `exit_side = "SELL" if direction == "LONG" else "BUY"`. Behaviourally corroborated: SHANTIGOLD (SHORT) closed by the system's own BUY SL 27-Aug 10:30:59. |
| **B-6** separate from GTT_EXIT | ✅ already separate modules | `orders/cnc_gtt_monitor.py` vs `orders/eod_squareoff.py` |
| **B-7** system action, never waits | ✅ already a polling thread | `:312` |
| entry cutoff separate | ✅ | `entry_end: "15:00"` (`:47`) |
| **B-1** trace | ✅ **DONE** (§1) | |
| **B-4** two passes from fresh broker state | ⚠️ **PARTIAL** — Pass 1/Pass 2 exist but are **2 s apart**, ⛔ not 15:07/15:10, and Pass 2's `remaining` semantics need verifying against B-4 | |
| **B-5** explicit states + real timestamps | 🔴 **TO BUILD** | |
| **B-10** fail-closed config validation | 🔴 **TO BUILD** | |
| **B-9** red-capable matrix | 🔴 **TO BUILD** | |
| **B-8** Live+Paper parity | 🔴 **TO VERIFY** | |
| **D-1** the cutoff config | 🔴 **TO BUILD** | |

> ⭐ **THE ACTUAL BUILD IS: config + timing + states + telemetry + tests.**
> ⛔ **NOT a new selector, ⛔ not short handling, ⛔ not a product boundary** — those
> three are already shipped and were verified today.

---

## §5 — 👤 RAMA'S CUTOFF DECISION, RECORDED · ⭐ ACCEPTED

👤 FILE 22 §1: *"taking the EARLIEST as THE cutoff is conservative for every stock —
⛔ no per-stock classification is needed anywhere in the code"* ⇒ a **single global**
`mis_squareoff_cutoff = 15:12`.

⭐ **This overrides my FILE 21 per-segment proposal, and it is 👤 his call. It is
adopted, ⛔ not re-argued.**

⚠️ **The one consequence, stated once and then dropped:** a non-CAS position is now
squared at **15:07** instead of its own broker cutoff of **15:25** ⇒ ⭐ ~18 minutes of
intraday holding time surrendered on every **non-F&O** stock. 🔬 Of the five MIS
symbols traded 27-Aug, **four were non-F&O** (`is_fno=false`). 👤 Rama has weighed
simplicity against that and chosen simplicity. ⭐ Recorded so a future reader knows
it was a **decision**, ⛔ not an oversight.

```yaml
trading_hours:
  mis_squareoff_cutoff:        "15:12"   # Zerodha CAS (earliest equity). BROKER-ADJUSTABLE.
  mis_squareoff_first_offset:  "5m"      # ⇒ CHECK 1 = 15:07
  mis_squareoff_second_offset: "2m"      # ⇒ CHECK 2 = 15:10
```

📄 Recorded alongside, per FILE 22 §1: Zerodha states the timings *"may be adjusted
based on market volatility"* ⇒ ⛔ never a code constant; and that it is *"under no
obligation"* to square off ⇒ ⛔ **broker square-off is NOT a safety net.**

---

## §6 — 🔒 FROZEN PREDICTION (B-11) · ⭐ WRITTEN BEFORE ANY GATE RUNS

⭐ Scored **after** the tests, ⛔ not adjusted to fit them.

1. **With no MIS position open, nothing changes.** Both passes log FLAT and submit
   **zero** orders. 🔬 Today's book is CNC-only ⇒ the live proof case.
2. **CNC is never selected.** OAL and RAMRAT — CNC/DELIVERY with ACTIVE GTT legs —
   must appear as `CNC_excluded`, ⛔ never as candidates.
3. **Only an open MIS position at 15:07 produces a new order.**
4. **The full-gate differential shows ZERO new failures**, and the test-count delta
   equals exactly the number of new cases added.
5. **The product-boundary mutation (MIS → CNC) turns the suite RED.** ⭐ If it does
   not, the suite is vacuous and the unit does not ship.
6. **The SHORT case (`qty = −1` → BUY) passes WITHOUT touching production code** —
   because `qty != 0` and the direction-aware exit side are already shipped. ⭐ If a
   production change turns out to be needed there, my §4 reading was **wrong** and
   that must be recorded as a miss.
7. **`reset_daily_pnl` still fires at 15:17**, ⛔ not 15:07. Any change to that
   timestamp means §2's hazard was not respected.

---

## §7 — WHAT IS NOT MEASURED

1. ⛔ **B-4's `remaining` semantics in the CURRENT Pass 2 have not been read
   end-to-end.** ⭐ Required before building.
2. ⛔ **Live/Paper parity of the exit path has not been verified today** (B-8).
3. ⛔ **The unit is NOT built, NOT tested, NOT pushed.** ⛔ No auto-square-off code
   has been modified.
4. 🏷️ **The 15:07/15:10 passes have never run** — no production evidence exists and
   none can before Monday.

⛔ push ≠ boot · ⛔ executed ≠ exercised · ⛔ green ≠ red-capable ·
⛔ order accepted ≠ position closed · ⛔ a broker query failure ≠ a flat book.

## END OF PRE-BUILD RECORD
