---
name: t2-arm-result-29jul
description: "T2 ARMED 29-Jul-2026: 5 CNC positions held overnight with 5 OCO GTTs. THE FIVE SYMBOL-GTT_ID PAIRS (unreconstructable). Broker vs system gtt_state agree EXACTLY on all five. DDPI now VERIFIED broker-side, not assumed. Kite's web UI never shows a GTT ID - pull from the API."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5ad0f836-2535-4418-b411-366cf7f765be
  modified: 2026-07-30T14:38:02.433Z
---

# T2 ARM RESULT — 29-Jul-2026 (Wed). 5 positions held overnight.

**Arm 11:37–11:43 IST. All 5 commands EXIT=0. Manual-buy fallback never used.**
Close card: `Downloads/THU_30-JUL_T2_CLOSE_COMMANDS.txt`. [[t2-multi-stock-28jul]]

## 🔑🔑 THE FIVE PAIRS — **cannot be reconstructed; the script prints nothing**
MEASURED from `kite.get_gtts()` 29-Jul. All five: **ACTIVE · two-leg · qty 3 · CNC**.

| SYMBOL | GTT_ID | SL trig/limit | TGT trig/limit | store dir `t2_proof_20260729_` |
|---|---|---|---|---|
| IOB       | **329514838** | 30.5 / 29.55 | 37.2 / 37.00 | 113746 |
| TRIDENT   | **329515817** | 22.4 / 21.70 | 27.4 / 27.25 | 114157 |
| SOUTHBANK | **329515899** | 41.8 / 40.50 | 51.1 / 50.80 | 114223 |
| MSUMI     | **329515981** | 36.9 / 35.75 | 45.1 / 44.85 | 114244 |
| SJVN      | **329516027** | 61.6 / 59.75 | 75.2 / 74.80 | 114258 |

ID order == arm order == store-dir time order. Total invested **₹649.35** (MEASURED,
Rama's broker screen) vs ~₹645 ESTIMATED. ASM/GSM/T2T: **all five clear** ⇒ full basket.

## ⛔ CORRECTION — **KITE'S WEB UI NEVER DISPLAYS A GTT ID**
The 28-Jul note said "take the GTT_ID from Kite". **MEASURED WRONG 29-Jul: the Kite web
UI does not show GTT id numbers at all.** Expected behaviour, not a fault.
⇒ **The ONLY source is the API lister** (arm card §D, `k.get_gtts()`), which Rama cannot
run himself. ⚠️ His by-hand check (ACTIVE · OCO · qty 3 · CNC) is still the valid
broker-side proof — it just cannot yield the id. **Whoever runs the API is the only one
who can produce the pairs, and Thursday's close takes the id as an argument.**

## ✅⭐ THE CROSS-CHECK THIS TEST EXISTS FOR — **ARM SIDE PASSES, ZERO DIVERGENCE**
Two independent records: the broker's, and the system's own `gtt_state` in each isolated
`data_store/t2_proof_20260729_*/t2_proof.db`. **They agree on all five, on every field**
— gtt_id · symbol · qty 3 · all four price levels · status ACTIVE · `needs_review=0`.
⭐ **This is the arm-side half of "does the system's picture match the broker's". The
SELL side is still open — Thursday's close tests it.**

## ✅ DDPI — **relabel ASSUMPTION → VERIFIED (broker-side, not source)**
Zerodha Console → Account → Demat: **DDPI request Completed 2026-06-26 14:11:36.**
⛔ Still NOT verifiable from source — there is **no TPIN/eDIS/DDPI handling anywhere in
the codebase** (VERIFIED by grep). The code issues a plain CNC LIMIT SELL and only
*observes* the outcome: COMPLETE ⇒ pass; anything else ⇒ CRITICAL, **GTT KEPT**, exit 1.
⚠️ Corollary: if DDPI were off, a **firing GTT would also fail to execute** — the
overnight protection rests on the same setting the test tests.

## ✅ Two things worth recording as they happened
- **The script placed every BUY itself** (`:358-368`) — marketable LIMIT, not raw MARKET
  (Zerodha's API refuses raw MARKET; LTP-fetch failure ABORTS, never falls back).
- **Kill switch still INACTIVE at 11:31**, two hours into session ⇒ the prior-day
  auto-clear guarantee held end to end. [[killswitch-autoclear-prior-day]]

## Thursday 30-Jul — the close
`--symbol X --qty 3 --close-overnight <GTT_ID>` × 5, window 09:15–11:00.
**EXIT=0** ⇒ sold, no TPIN, GTT deleted ⇒ DDPI proven for that stock.
**EXIT=1** ⇒ sell rejected, GTT **KEPT deliberately** — stop and report.
⚠️ **ONE "Orphan GTT" WARNING per stock at 08:15–08:25 is CORRECT, not a fault** — five
warnings expected. [[slice25-execution-plan-27jul]]
⚠️ Per-scrip DP charge ~₹15–16 per SELL ⇒ **N=5 ≈ ₹75–80**, against ₹649 invested.

## Note, do not act (freeze)
Today's five `t2_proof_20260729_*` dirs join 5 from 28-Jul and 7 from 10-Jul.
⛔ Harmless; cleanup waits for the freeze to lift.

## ⚠️🕳️ PRECISION ADDED 30-Jul 20:0x — WHERE `gtt_state` ACTUALLY LIVES (a Friday-morning trap)
**The LIVE `data_store/trading_system.db` has `gtt_state` = ZERO ROWS. MEASURED 30-Jul, and it is
CORRECT — not a loss of protection.** The arm ran through `t2_cnc_gtt_realtest.py`, which writes its
`gtt_state` only into a **per-run throwaway store**: `_throwaway_store_path()` =
`data_store/t2_proof_<ts>/t2_proof.db`, deliberately in its OWN subdir so the ATTACHed
`analytics.db` sibling is isolated too, and `_assert_isolated()` *refuses to run* against the live DB.
⇒ **So "broker == system `gtt_state` on all 5" above means the THROWAWAY store's rows, NOT the live
DB's.** ⛔ **Do NOT query live `gtt_state` to confirm the five GTTs — it will show 0 and read as
"protection gone".** The ONLY authority is the broker API (`k.get_gtts()`); the card's five GTT_IDs were
re-measured from it 30-Jul 10:45. Consistent with [[t2-shared-cash-seam-29jul]]: the DB is isolated,
the account is not. ⭐ And nothing on the 30-Jul deploy night touched them — the close rehearsal
returned at the confirm guard *before* any adapter or broker client was built.
