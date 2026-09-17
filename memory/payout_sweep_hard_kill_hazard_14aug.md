---
name: payout-sweep-hard-kill-hazard-14aug
description: A payout/settlement sweep landing mid-session can hard-kill BOTH books today
metadata:
  type: project
---


## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1219 B (budget 450 B). The index now carries a hook and this link.

- 💀🔴🔝 **A ⛔ **LIVE** HAZARD FOUND 14-Aug — A PAYOUT / SETTLEMENT SWEEP LANDING WHILE POSITIONS ARE OUTSTANDING CAN HARD-KILL **BOTH** BOOKS **TODAY**, ⛔ with or without the capital-recomputation feature. `<MEASURED · NOT FIXED>`** 🔑 `capital/fund_manager.py:2391` `_check_invariant`'s per-bucket non-negativity guard (H-1 + M-C3) raises on `avail`/`used`/`reserved` `< -tol`, and `_handle_invariant_violation` escalates it to `hard_kill` ⇒ **one bucket negative kills BOTH.** 📉 Already witnessed: the deployed code quotes it at `:385-390` — *"`0.30 * 209.80 - 907.02 = -844.08` and INV6 hard-killed BOTH books"* (SEBI swept ~₹8,774 on 09-Aug; 10-Aug boot died on it). ⚠️ **Fix 1 repaired ONLY the BOOT-time version** (`_intraday_carry`/`_positional_carry`) ⇒ 🔴 **the MID-SESSION version is UNREPAIRED.** ✅ The event IS observable — the live margins response carries `utilised.payout`; the adapter discards it at `broker/zerodha_adapter.py:1451`. 🔴 **HOT CANDIDATE — ⛔ NOT ADDED: the one-line/day `MEMORY.md` budget was spent on the Fix 2 score. ⭐ Rama's call whether it earns a second line.** 📋 Register `N14-09`. ⛔ Separate defect, ⛔ NOT the recomputation unit.
