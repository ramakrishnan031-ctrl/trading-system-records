---
name: capital-operational-note
description: Daily loss limit reads fm_ledger.pnl_delta not trades.net_pnl; RMS closes pass costs=0.0
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7cbac53e-3446-42e1-8243-b814aa9e0215
---

Daily loss limit (Rs 300) reads `fm_ledger.pnl_delta` — **NOT** `trades.net_pnl`.

- `get_daily_realized_net_pnl()` (state_store.py) sums `fm_ledger.pnl_delta − costs`; the breach check in `FundManager.release_used()` uses this.
- RMS / externally-closed trades (CHECK1, order_reconciler.py) call `release_used(costs=0.0)` → fm_ledger PnL excludes exit brokerage/STT, so the loss-limit view is slightly optimistic for those trades.
- Reports use `trades.net_pnl` (written by `close_trade`).
- Both ledgers agree in the normal exit path (same gross − charges).

**✅ RE-VERIFIED AT HEAD 16-Jul-2026 (batch-1 E4 / P3-s13) — still true, and the mechanism is:**
`order_reconciler.py:1109` passes `costs=0.0` into `release_used`, where
`pnl = gross_pnl − costs` ⇒ **`pnl` IS GROSS**; then `projected_after = avail_before + margin + pnl`
and `pnl_delta = pnl`. So on every CHECK1/RMS/manual close **BOTH** the daily-loss limit's input
**and available capital** are credited with **gross, not net**.

**⚠️ "slightly optimistic" UNDERSTATES it.** This book's own numbers are **gross ≈ −0.007R vs net
−0.100R** — costs ARE substantially the loss. A control fed gross on these closes is not fed a
slightly-off number; it is fed the wrong one. The register records this as "by-design"
([[pending-register-16jul]] P3-s13) — the mechanism above is what that claim has to justify.
**NOT fixed: any change here is a capital path ⇒ LOOP** (design → ChatGPT → implement), never a
batch item. [[batch1-done-16jul]]

**How to apply:** If the EOD daily-summary PnL differs from what tripped (or didn't trip) the loss limit, reconcile `fm_ledger` vs `trades` — they diverge on RMS/manual closes. When judging whether the loss limit "should" have tripped on a day with RMS/manual closes, remember its input was gross for those trades. Related: [[live-trading-readiness]], [[feedback-paper-live-parity]].
