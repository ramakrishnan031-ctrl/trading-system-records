---
name: m3-attach-the-sha-correction
description: M3: attach the SHA or the line describes code that is not running (sizing divisor)
metadata:
  type: project
---


## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 467 B (budget 450 B). The index now carries a hook and this link.

- 📐⚠️🔝 **M3 CORRECTION — ⛔ ATTACH THE SHA OR THE LINE DESCRIBES CODE THAT IS NOT RUNNING: the sizing divisor `max_daily_trades` (`position_sizer.py:433`) belongs to the UNPUSHED allocation model `65b7196`.** ⛔ **The DEPLOYED `645728d` has NO divisor — `qty_by_capital = floor(avail_bucket ÷ margin_per_share)` over the WHOLE bucket** (`:419`, `avail` = `snap.intraday_avail`/`snap.positional_avail` at `:294`). [[stated-vs-configured-limits-09aug]]
