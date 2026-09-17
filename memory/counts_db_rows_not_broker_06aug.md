---
name: counts-db-rows-not-broker-06aug
description: "One defect with three faces — the system counts its own DB records where it means to count the broker's reality (held, the slot cap, the shutdown guard)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2a4a3971-dd6a-4008-aba8-92b69d464d12
  modified: 2026-08-06T13:10:15.994Z
---

# COUNTING ITS OWN RECORDS WHERE IT MEANS THE BROKER'S REALITY — **ONE finding, THREE faces**

⛔ **File these together. They are not three findings.** Measured 06-Aug-2026, all three on the
same day, all three on the same phantom trade (`trd_e66ee17b…`, ATULAUTO).

| # | site | what it counts | what it means to count | measured 06-Aug |
|---|---|---|---|---|
| 1 | `orders/cnc_gtt_monitor.py:464` `_gather` | `held += abs(int(qty))` over CNC `positions()` | shares actually held | broker said **`0 holdings`** (24 consecutive reads); predicate said **`held=1`** ⇒ 3 live SELL GTTs placed on a flat holding |
| 2 | `capital/risk_engine.py:469` slot cap | `trades.status IN (OPEN,PARTIAL,PENDING_FILL)`, **no date bound, no broker check** | live delivery positions | phantom permanently occupies **1 of 3** slots (33 % of delivery concurrency) |
| 3 | `main.py` EOD self-exit guard | open **DB rows** | open **broker positions** | `17:35:00.002` — *"past 17:35 IST but **2** active position(s) remain — staying up to manage them; will exit once flat"* — **only ONE is real** |

## ⭐⭐ WHY FILING THEM TOGETHER MATTERS
**Fixing `held` alone leaves faces 2 and 3 intact**, and each independently keeps a phantom alive:
the slot cap keeps consuming concurrency, and the shutdown guard keeps the service up.

## 🔴 FACE 3 IS THE ONE WITH THE COMPOUNDING COST
**"Will exit once flat" can NEVER again be satisfied while a phantom `OPEN` row exists with no path
to close.** ⇒ ⛔ **not "one night's boot skipped" — NO census ever, NO 08:15 boot ever, NO kill
auto-clear ever, and a process crossing midnight repeatedly** with date-keyed logic
(`SUBSTR(created_at,1,10)`, daily counters, `_TODAY` captures) rolling over inside a live process
that has never done it once.
⇒ **A manual nightly stop becomes a STANDING OPERATIONAL BURDEN until F6 lands.** ⛔ Named so it
does not become permanent by going unnamed.
**(P) 18:37** — the deferred "manage them" loop polls `get_positions`+`get_margins`+`get_quote(2)`
**every 15 s**, indefinitely, after close.

## THE DISCRIMINATOR, FOR ANY NEW SITE
> **Does this count answer a question about OUR RECORDS, or about THE BROKER?** If the second, a
> `trades`/`gtt_state` query cannot answer it — ⛔ and `trades` has **no `product` column** either
> *(see [[schema-product-is-on-orders-05aug]])*, so a product-aware version needs a join it does not do.

Related: [[f6-delivery-exit-abs-defect-06aug]] · [[t2-shared-cash-seam-29jul]] ·
[[feedback-never-classify-by-free-text]] *(same shape: branching on the wrong source of truth)*.
