---
name: senco-double-entry-27jul
description: "The 27-Jul SENCO re-entry is a POLICY GAP, not a defect — every gate worked. The real finding is underneath: first entries lose money (n=181, mean -0.40, win 40.3%), corroborating the 24-Jul entries conclusion from an independent direction."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-28T04:50:18.705Z
---

**First live-trading finding since the board was cleared.** Full analysis:
`docs/audit/senco_double_entry_27jul2026.md` (⛔ untracked 27-Jul; commit after the push).

## ⛔ IT IS A POLICY GAP, NOT A DEFECT — so it cannot be "fixed now"

`trd_c9675b4fae4a` entry **10:02:17 @ 418.75** → **TGT_HIT 10:13:31 @ 425.05, +5.84**.
`trd_910664791d6e` entry **10:14:51 @ 425.25** (⭐ **0.20 ABOVE the first exit**) → **SL_HIT
10:25:53 @ 420.85, −4.86**. Exit→re-entry gap **80 s**. Pair nets **+0.98** — the re-entry gave back
**83 %** of the first trade's profit. ⚠️ Trade 2's **SL (421.02) sat ABOVE trade 1's ENTRY (418.75)**.

⭐⭐ **THE SHAPE, and it is not "a second signal arrived":** `open_low_breakout_long` fired SENCO
**every ~5–6 minutes all morning**. `10:08` scored an identical **60** and PASSED the screener — it
was blocked **only** by `REJECTED_STRATEGY_POSITION_LIMIT`. ⇒ **a continuous signal stream held back
by the open-position guard, which releases the instant the position closes; the very next hit went
straight in.**

## The four hypotheses, answered from data

- **Same alert twice? NO** — different `triggered_at` (10:02:00 / 10:14:00), different fingerprints.
  **Dedup was NOT too narrow.**
- **Different strategies? NO** — the same strategy both times.
- **Stale state? NO, REFUTED** — exit 10:13:31, second signal 10:14:11 (40 s later), and the guards
  provably fired while open (`STRATEGY_POSITION_LIMIT` 10:08, `DUPLICATE_SYMBOL` 10:03 + 10:09).
- **Satisfied every rule? YES** — score **60 against `min_pass_score: 60`, a pass by ONE point**,
  tier LOW. From 10:19 the same scanner scored **59** and everything was rejected.

## ✅ B — FIX-181 WORKS, and it is an ALLOW-LIST (which is why one rule covers both)

`state_store.py:678-705` `_EXECUTED_TRADE_STATUSES = (PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED,
CLOSED_MANUAL)`. ⭐ **REJECTED, CANCELLED and FAILED are all excluded by naming what COUNTS rather
than what doesn't — a deny-list fix would have covered one and missed the other.**
**MEASURED today: 7 trade rows → `count_trades_today()` = 4** (4 CLOSED counted; 2 FAILED + 1
REJECTED excluded). **4 of `max_daily_trades: 10`** — no capacity lost.
⚠️ **PREMISE CORRECTION: there were ZERO broker-REJECTED orders today** (COMPLETE 8 · CANCELLED 4 ·
REJECTED 0). The 4 CANCELLED are **OCO siblings, one per closed trade — normal LIMIT_TRIPLE**, not
failures. The "rejections" in the screenshots are the **SIGNAL** stream (1,273 signals;
`REJECTED_SCORE_59` ×526). **Signal rejections ≠ broker order rejections.**

## ⚠️ C — THE COOLDOWN IS NOT EVIDENCE-BACKED. n = 2.

Whole book: **FIRST entries n=181, total −71.91, mean −0.397, win 40.3 %** · **RE-ENTRIES n=2, total
−6.53, win 0 %**. Gaps: **<5 min n=1** (SENCO −4.86) · **5–30 n=0** · **30+ n=1** (RALLIS 21-Jul,
43.5 min, −1.67).
**A 30-min rule: blocks 1 trade · avoids +4.86 · forgoes 0.00 wins.**
⛔ **"Wins forgone = 0" is NOT evidence the rule is free — it is evidence there is NO DATA.**
Re-entries are **1.1 %** of the book; the whole stake is ~₹5 over five weeks. ⭐ **And the one a
30-min rule would MISS (RALLIS, 43.5 min) also lost.** ⇒ **insufficient evidence, not "no".**

## 🆕 28-JUL — **A THIRD INSTANCE, NEXT DAY, ALMOST THE SAME CLOCK. n=2 → n=3.**

Seen live at ~10:20 while taking an early read for the T2 go/no-go — **not** looked for.
**AURIONPRO SHORT** `trd_d49eff32` entry 10:00:21 @ 754.00 → **TGT_HIT 10:09:47 @ 742.70, +10.51
net** ⇒ `trd_2da809d3` **re-enters SHORT 10:11:12 @ 739.95**. **Exit→re-entry gap 85 s** (SENCO's
was **80 s**). Same symbol **and** same direction, so it is the shape
`one_trade_per_symbol_direction_per_day` targets — **not** a reversal.

⭐ **THIS IS THE MOST USEFUL THING ABOUT IT: the rule going live Mon 3-Aug WILL BIND.** The calendar
gives 3-Aug as a full observation day for that rule; today proves there will be something to
observe. It is no longer a rule that might never fire.
⚠️ **AND THE HONEST HALF: today's first leg WON (+10.51) and the re-entry's outcome is UNKNOWN**
(still OPEN when measured). ⇒ this instance **adds to the SHAPE evidence, NOT to the "re-entries
lose" evidence** — §C's "n=2, insufficient" verdict stands unchanged until it closes. ⛔ Do not
count it as a third loss; that is the arithmetic error this file already warns about.
⚠️ **Frequency worth WATCHING, not concluding:** RALLIS 21-Jul · SENCO 27-Jul · AURIONPRO 28-Jul =
3 in ~5.5 weeks, but **2 on consecutive trading days.** Could be regime, could be noticing.
⭐ Both gates behaved: the 300 s per-symbol throttle had expired (652 s since first entry) and the
open-position guard released on the close — **the same mechanism as SENCO, confirmed twice.**

## ⭐⭐ THE FINDING THAT MATTERS MORE — and it corroborates 24-Jul independently

**The re-entry question is worth ₹4.86 over five weeks. The FIRST-entry population is −₹71.91 over
the same trades.** Optimising a 1.1 % tail while 98.9 % bleeds.
⭐ **Win rate 40.3 % — computed differently, over a different slice, and it lands on the 24-Jul
number** (38–39 % win vs **43.5 % breakeven**, RR median 0.33). **The standing "⛔ DO NOT loosen the
V3 gate / `rr_floor`" conclusion is REINFORCED, not challenged.** [[entries-buy-extension-24jul]]
⚠️ **Both SENCO entries scored EXACTLY the `min_pass_score` of 60.** Marginal-score admission is a
bigger lever than re-entry.
