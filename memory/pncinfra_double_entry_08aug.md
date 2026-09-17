---
name: pncinfra-double-entry-08aug
description: "The 06-Aug PNCINFRA \"two identical entries\" alert was NOT a gate hole — neither order ever filled. Gate 1 and gate 3 both ran correctly; the corpus scan with a control confirms the gate is holding."
metadata: 
  node_type: memory
  type: project
  originSessionId: 35a1c3dd-75a3-42ce-bdc5-d5e981dad58a
  modified: 2026-08-08T09:50:54.838Z
---

# 🟢 PNCINFRA 06-Aug — **NO DEFECT, NO GATE HOLE.** Measured 08-Aug, read-only.

Record: `docs/audit/pncinfra_double_entry_check_08aug2026.md`.

## ⛔ THE PREMISE FAILED — **NEITHER ORDER EVER FILLED**

**(P)** THREE PNCINFRA SHORT attempts on 06-Aug (⛔ not two — 13:18 · 13:42 · 14:18),
**ALL `FAILED`**, every ENTRY order `CANCELLED` with **`qty_filled = 0`**, no
`entry_time`, no `net_pnl`. **There was no position, so there was nothing for a
duplicate-entry gate to prevent.**

🔑 **THE MECHANISM THAT MADE IT LOOK LIKE A DOUBLE ENTRY, and it will recur: the alert
reads *"ORDER PLACED … ₹240.94"* and `order_placer.place_start` logs
`"entry_price": 240.9407` — ⭐ THAT IS THE PLACEMENT PRICE. The alert fires at
PLACEMENT, not at fill, and cannot be told apart from a fill by reading it.** Order
timestamps match the alert timestamps to the millisecond. Cause of death:
`order_monitor.fill_timeout_sec: 60` cancels an unfilled entry.

## ✅ BOTH GATES RAN, AND BOTH WERE RIGHT

- **Gate 1 fired 19× on 06-Aug** *(e.g. `10:05:22 ASTERDM LONG already traded today`)* ⇒
  ⭐ **proven live POSITIVELY, not by absence.** It did not fire for PNCINFRA because
  `count_executed_trades_today_for_symbol_direction` reuses `_EXECUTED_TRADE_STATUSES`
  and **`FAILED` is not in it ⇒ the count was 0.**
- ⛔⛔ **THAT EXCLUSION IS NOT A HOLE — IT IS FIX-181 AND REMOVING IT WOULD BE THE
  DEFECT.** `state_store.py:678-682`: *"a burst of broker rejections … silently exhausts
  `max_daily_trades` and halts trading."* ⭐ **Counting a never-filled order as "traded
  today" would have locked PNCINFRA out for the day after three unfilled attempts.**
- **Gate 3 ran too:** all three approvals log `checks_run=10` (the full RE5 sequence incl.
  `DUPLICATE_SYMBOL`); nothing was OPEN/PARTIAL/PENDING_FILL by 14:18.

## ✅ THE CORPUS SCAN — **0, WITH A CONTROL THAT COULD HAVE MADE IT RED**

Width: every `trades` row on/after 03-Aug, grouped (date, symbol, direction), restricted
to gate 1's own executed set. Population **24 executed trades**.
**On/after 03-Aug (gate LIVE) = 0 · ⭐ CONTROL before 03-Aug (gate NOT live) = 4.**
⇒ 🟢 **THE OPEN-1 EVIDENCE STANDS — the 65 gate-1 rejections describe a gate that is
holding. ⛔ No re-labelling owed.**
⚠️ **The UNFILTERED scan returns 16 groups** (`ENGINERSIN ×6`, `SILVERBEES ×5/×4`) —
⛔ **those are repeated ATTEMPTS, not repeated trades, and reading that list as duplicate
entries is exactly the error this check nearly made.**

## ⚠️ PARITY — "no instrument", ⛔ not "agreed"

**(P)** the VM DB holds **561 trades, ALL `mode=LIVE`, ZERO paper rows** — paper runs on
the PC, whose local DB is empty. ⇒ **there is no paper observation of 06-Aug to
compare.** ⭐ **An absent instrument is not a passing control.**

## 🏷️ FILED, ⛔ NOT CHASED

⚠️ **49 `FAILED` + 10 `REJECTED` vs 24 EXECUTED since 03-Aug — two-thirds of trade rows
never opened exposure.** A fill-rate question, ⛔ not a gate question; it deserves its own
measurement rather than a paragraph in someone else's card.

Related: [[senco-double-entry-27jul]] · [[feedback-verify-the-finding-premise]] ·
[[feedback-absence-needs-wide-check]] · [[two-pipeline-split-08aug]]
