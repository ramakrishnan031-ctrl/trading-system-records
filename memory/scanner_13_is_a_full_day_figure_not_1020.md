---
name: scanner_13_is_a_full_day_figure_not_1020
description: The 13-scanner expectation is a full-day figure, not a 10:20 one — only 9 had posted by 10:20 on 04-Sep, so a 10:20 shortfall is normal, not a fault.
metadata:
  type: reference
---

📊⏰ **"13 DISTINCT SCANNERS BY 10:20" IS THE WRONG DEADLINE — 13 IS A FULL-DAY FIGURE.**

🔬 MEASURED 07-Sep-2026 against `webhook_audit` (`data_store/trading_system.db`), date `2026-09-04`, the last trading day:

| by 10:20 | first post |
|---|---|
| ✅ 9 scanners had posted | earliest `09:18:17` (positional_momentum_long) |
| ⛔ gap_go_short | `10:33:15` |
| ⛔ first_pullback_short | `10:36:14` |
| ⛔ gap_fade_short | `10:39:16` |
| ⛔ gap_fade_long | `12:06:17` |

⇒ ⭐ **The 13th scanner did not arrive until 12:06.** A 10:20 reading of **9–12 is the NORMAL shape**, ⛔ not a shortfall.

🔬 Day total on 04-Sep = **14** = the 13 + `pb01_breakout_retest` at `17:00:07` (EOD, 1 row).
⛔ `range_breakout_long` / `range_breakout_short` did NOT post — consistent with 0 rows in 223,484; permanently "configuration-verified only" → [[webhook_audit_is_the_instrument_06sep]]

⛔ **Nothing posts before ~09:18** — the market opens 09:15. A 0-row `webhook_audit` at 08:5x is ⭐ CORRECT, ⛔ not a receiver fault. ⚠️ Always prove such a zero non-vacuous by re-running the same query against the prior trading day → [[a_floor_is_not_a_non_vacuity_check]]

**Why:** the 07-Sep Monday card set the checkpoint at 10:20, which the last trading day would have FAILED. Reading it literally manufactures a false alarm on a clean morning.
**How to apply:** ⭐ take the scanner count at **~12:30 or later**, ⛔ never at 10:20. At 10:20 read only the **401 count** — that one IS meaningful from the first post onward.
