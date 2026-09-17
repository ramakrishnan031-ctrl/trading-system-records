---
name: t2-btst-close-defer-30jul
description: "30-Jul-2026: the T2 close was stood down and moved to Fri 31-Jul. A T1/BTST sell debits demat at SETTLEMENT, not at the order, so a Thursday EXIT=0 would have proved the order path and NOT DDPI. Rama's stated mechanism was wrong; his conclusion was right. The 5 GTTs re-verified ACTIVE 30-Jul 10:45."
metadata: 
  node_type: memory
  type: project
  originSessionId: 91948a89-4eda-4cd0-ac78-c3b773765042
  modified: 2026-07-30T05:20:12.303Z
---

# T2 CLOSE MOVED THU 30-JUL -> FRI 31-JUL. Rama's call, 30-Jul ~10:50.

Thursday 09:25 Holdings showed all five **Qty 0 / T1: 3** — bought Wed, not yet in
demat. Card reissued: `Downloads/FRI_31-JUL_T2_CLOSE_COMMANDS.txt` (Thursday's is
SUPERSEDED). [[t2-arm-result-29jul]] [[t2-shared-cash-seam-29jul]]

## ⛔⛔ A BTST/T1 CLOSE CANNOT TEST DDPI — NEVER RECORD ONE AS A PASS
**SOURCED from Zerodha's own BTST-settlement docs, not from our code** (there is no
TPIN/eDIS handling anywhere in the codebase — that is why this is broker-side):
shares are **credited** to demat T+1, **earmarked**, then **debited T+2**, and
*"since shares are credited and debited from your demat account, DP charges apply
like normal delivery transactions."*
⇒ **The demat debit DOES happen** — so the asking card's premise *"the shares never
leave the demat account because they were never in it"* is **FALSE**.
⭐ **But the authorisation event is TIME-SHIFTED, not absent.** At order time free
demat qty is 0 ⇒ nothing for the placement-time gate to check [INFERENCE — no
Zerodha doc states the T1 case either way; search width: support ×8, Z-Connect ×3,
Kite forum]. ⇒ **EXIT=0 on a BTST sell proves the order path only, and a DDPI
failure would surface at Friday's EPI as SHORT DELIVERY/auction — not as EXIT=1.**
A worse failure mode than the clean rejection the card was built around.

## ⛔ "NO TPIN POPUP" WAS NEVER THE TEST — an API order cannot show a popup
The popup is a Kite web/app artifact. `--close-overnight` goes through kiteconnect,
which returns an **error string**. The script's real criterion is
`st == "COMPLETE"` (`scripts/t2_cnc_gtt_realtest.py:451`). The §E box was removed.

## ⚠️ THE SCRIPT BLAMES DDPI FOR EVERY EXIT=1 — it cannot tell the difference
`:456` logs *"DDPI/TPIN may be unauthorised"* for **any** non-COMPLETE status.
Three causes are indistinguishable from the exit code: a genuine CDSL rejection ·
a LIMIT still **OPEN** inside `_poll_terminal`'s **~22 s** budget (`polls=12,
gap=2.0`, `:279`) · an LTP-fetch abort (`:266`, no MARKET fallback). ⛔ **Read the
Kite order status, never the exit code alone.** [[feedback-verify-rc-not-output]]

## ✅ NO QUANTITY GATE EXISTS ON THE CLOSE PATH — the sell would have worked
`run_close_overnight` (`:437-458`) never reads holdings; it takes `--qty` from the
CLI. The adapter's only gate is `delivery_enabled` (`broker/zerodha_adapter.py:558`),
True on T2's own instance. Zerodha permits T1 CNC sells (BTST) and all five were
T2T/GSM/ASM-clear. ⇒ **A2's feared free-qty-0 rejection does not exist.**

## ✅ RE-VERIFIED 30-Jul 10:45 (broker API, read-only `get_gtts()`)
All five **ACTIVE · two-leg · qty 3 · SELL · CNC**, correct symbol, **all 20 price
levels match the card exactly. Zero extra GTTs, zero drift from the arm.** Holdings
qty=0/t1=3/realised=0 on all five ⇒ nothing sold. Cost of shares **Rs 643.98**
[MEASURED, API] vs Rs 649.35 on screen (charges). Unrealised P&L **Rs 0.00** — flat.

## ⚠️ THE FRIDAY-ONLY COST, and it is the only real one
**An EXIT=1 on FRIDAY holds real stock across the WEEKEND — 3 unsupervised days**
(a GTT cannot fire while the market is closed). Thursday it cost one night. ⇒ the
card tells Rama to report an EXIT=1 **that morning**, not in the evening.
⭐ Friday's 08:15 boot carries Thursday night's code slot (incl. fix-symdir) but
**the close does not depend on the service** — own adapter, own DB, GTTs at Zerodha.
DP charges ~Rs 75-80 apply either day — waiting costs nothing there.
