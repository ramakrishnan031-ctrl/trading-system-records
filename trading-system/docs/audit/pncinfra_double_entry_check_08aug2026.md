# PNCINFRA 06-Aug — THE DOUBLE-ENTRY CHECK. **VERDICT: NO DEFECT. NO GATE HOLE.**

**Measured 08-Aug-2026, read-only** (`sqlite3 -readonly` against the live VM DB +
`logs/system_2026-08-06.log`). ⛔ No code, no writes, service untouched.

> ## 🔴 **THE CARD'S PREMISE DID NOT SURVIVE CHECKING: NEITHER ORDER EVER FILLED.**
> The alert reads *"ORDER PLACED … ₹240.94"*. **(P)** `order_placer.place_start` for that
> trade logs `"entry_price": 240.9407` — ⭐ **that is the PLACEMENT price, and the alert
> fires at placement, not at fill.** **(P)** every ENTRY order is `CANCELLED` with
> `qty_filled = 0`. **There was no position, so there was nothing for a duplicate-entry
> gate to prevent.** 🏷️ *An audit finding is a HYPOTHESIS — verify its premise.*

---

## 1.1 · THE LIFECYCLE — **(P)** · **X3+** (DB trades + DB orders + app log)

**THREE** PNCINFRA SHORT attempts on 06-Aug, ⛔ not two:

| # | trade | strategy | created | status | entry_time | net_pnl |
|---|---|---|---|---|---|---|
| 1 | `trd_6e108607…` | `first_pullback_short` | **13:18:15.979** | **`FAILED`** | *(none)* | *(null)* |
| 2 | `trd_1a67e00e…` | `vwap_rejection_short` | **13:42:24.774** | **`FAILED`** | *(none)* | *(null)* |
| 3 | `trd_e66c8a9a…` | `vwap_rejection_short` | **14:18:24.713** | **`FAILED`** | *(none)* | *(null)* |

**Their ENTRY orders — all MIS, all `CANCELLED`, all `qty_filled = 0`:**
`13:18:25.687` · `13:42:24.843` · `14:18:26.424`.
⭐ The order-placement timestamps match the alert timestamps to the millisecond
(`13:42:24.845` / `14:18:26.426`), which is what identifies those alerts as PLACEMENT
alerts. **Cause of death: the orders never filled and were cancelled** — `order_monitor`
tracked each one and `order_monitor.fill_timeout_sec: 60` cancels an unfilled entry.

**⇒ Was trade 1 terminal before `14:18:24`? YES — `FAILED`, and its order was cancelled
~60 s after 13:42.**

## 1.2 · WAS GATE 1 EVALUATED? — **YES, AND IT FIRED 19 TIMES THAT DAY** · **(P)** · **X2**

⭐ **Proven POSITIVELY rather than by absence:** `SYMBOL_DIRECTION` appears **19 times**
in `logs/system_2026-08-06.log`, e.g.

```
10:05:22.001  Signal sig_bb3d9cf4… (ASTERDM) rejected at SYMBOL_DIRECTION_DAILY_LIMIT:
              ASTERDM LONG already traded today (1 executed trade(s))
```

⇒ **the gate is live, reachable and rejecting on the very day in question.**

**Why it did not fire for PNCINFRA:** it reads
`count_executed_trades_today_for_symbol_direction`, which reuses
`_EXECUTED_TRADE_STATUSES` (`PENDING_FILL·OPEN·PARTIAL·EXITING·CLOSED·CLOSED_MANUAL`).
**`FAILED` is not in that set, so the count was 0 and the gate correctly permitted.**

> ### ⛔ **THAT EXCLUSION IS NOT A HOLE — IT IS FIX-181, AND REMOVING IT WOULD BE THE DEFECT.**
> `state_store.py:678-682` states the reason in its own words: *"a burst of broker
> rejections … silently exhausts `max_daily_trades` and halts trading."* ⭐ **Counting a
> never-filled order as "traded today" would let three unfilled attempts lock a symbol
> out for the day — and on 06-Aug that is exactly what would have happened.**

## 1.3 · WAS GATE 3 EVALUATED? — **YES** · **(P)** · **X2**

All three approvals log `checks_run=10 approved=True failed_check=none` — the full RE5
sequence including check 10 `DUPLICATE_SYMBOL`. `has_active_position` matches
`OPEN/PARTIAL/PENDING_FILL`; by 14:18 no PNCINFRA trade held any of those. **Gate 3
correctly permitted.**

## 1.4 · 🔑 THE CORPUS SCAN — **THE SHAPE IS ABSENT. COUNT = 0.** · **(P)** · **X2**

**Search width:** every `trades` row created on/after `2026-08-03`, grouped by
(date, symbol, direction), restricted to the **same executed-status set gate 1 itself
uses**. Population searched: **24 executed trades** across the window.

| scan | result |
|---|---|
| **on/after 03-Aug (gate LIVE)** | 🟢 **0 groups** |
| ⭐ **CONTROL — before 03-Aug (gate NOT live)** | 🔴 **4 groups** |

⭐⭐ **The control is what makes the zero mean something: the identical query finds the
shape 4 times before the gate went live and 0 times after.** ⛔ A zero with no control
would have been a check that could not have gone red.

⚠️ **The unfiltered scan (any status, incl. FAILED/REJECTED) returns 16 groups** — e.g.
`ENGINERSIN ×6`, `SILVERBEES ×5` and `×4`, `PNCINFRA ×3`. **Those are repeated
ATTEMPTS, not repeated trades**, and reading that list as duplicate entries is precisely
the error this card nearly made. 🏷️ Filed separately below.

> ### ⇒ **THE OPEN-1 EVIDENCE DOES *NOT* NEED RE-LABELLING.**
> The card's conditional was *"if it is greater than zero…"*. **It is zero.** The 65
> gate-1 rejections describe a gate that is holding.

## 1.5 · P&L — **(P)**

**Zero realised, on all three.** `net_pnl` is NULL, no `exit_price`, no `entry_time` —
nothing opened. ⭐ **The cost of the episode is not a loss; it is three unfilled attempts
and their latency.**

---

## 🎯 THE PRE-REGISTERED EXPECTATION, SCORED

| claim | verdict |
|---|---|
| *"trade 1 was terminal before 14:18"* | ✅ **RIGHT** — `FAILED`, cancelled ~60 s after 13:42 |
| *"gate 1's status set is where the hole is"* | ❌ **WRONG** — the set is correct and the exclusion is FIX-181, deliberate and load-bearing |
| *the fallback: "gate 1 simply did not run"* | ❌ **ALSO NOT THE CASE** — it ran and rejected 19 signals that day |

⭐ **The expectation was half right for the right reason and half wrong for an
instructive one:** it assumed the terminal status must be one the gate *ought* to have
counted. The terminal status was `FAILED`, which the gate is *designed* not to count.

## ⚠️ PARITY — **stated precisely, because the honest answer is "no instrument"**

⛔ **The paper path shows nothing that day, and NOT because it agreed.** **(P)** the VM
DB holds **561 trades, ALL `mode=LIVE`, zero paper rows** — paper runs on the PC, whose
local DB is empty. ⇒ **there is no paper observation of 06-Aug to compare.** ⭐ An absent
instrument is not a passing control.

---

## 🏷️ FILED — found while measuring, ⛔ NOT chased

1. ⚠️ **49 `FAILED` + 10 `REJECTED` vs 24 executed since 03-Aug** — **two-thirds of trade
   rows never opened exposure.** The 16-group unfiltered scan is the same phenomenon.
   ⛔ Not investigated here; it is a fill-rate question, not a gate question, and it
   deserves its own measurement rather than a paragraph in someone else's card.
2. ⭐ **The "ORDER PLACED … ₹price" alert cannot be told apart from a fill by reading it.**
   That is what turned three unfilled attempts into a reported double-entry incident.
   ⛔ Not a wording fix to make here — but it is the mechanism, and it will recur.
