---
name: mid_fill_rung_manufactures_own_sl_10sep
description: "The false OWN_SL closures come from CHECK1 precedence rung 4 (EV_MID_FILL) -- a 'cancel refused: being processed' claim taken as fill evidence and never revisited; its designed expiry guard is configured OFF in production"
metadata:
  type: project
---

🔴 **A FALSE `OWN_SL` IS MANUFACTURED BY PRECEDENCE RUNG 4, ⛔ NOT BY A BROKEN
CLASSIFIER.** 🔬 MEASURED 10-Sep-2026 against production at `3b15bbf` (deployed
tree md5-identical to the worktree for all five files read).

## ⭐ THE MECHANISM, END TO END
1. CHECK1 tries to cancel the orphan SL. The broker refuses: *"Order cannot be
   cancelled as it is being processed. Try later."*
2. That refusal sets `mid_fill=True` on that leg
   (`order_reconciler.py:1318` `_mid = {b for b, _l in orphan.mid_fill}`).
3. `closure_classifier.classify()` builds `named_by_midfill` (`:125-127`). No
   other source speaks, so no contradiction fires, and the ladder falls to
   **rung 4 `EV_MID_FILL`** (`:157-159`) → `OWN_SL` at severity **INFO**.
4. `order_reconciler.py:1340` writes it via `set_trade_closure_axes`, whose SQL is
   `SET closure_source = COALESCE(closure_source, ?)` (`state_store.py:1788`) —
   ⛔ **write-once. Nothing ever revisits it.**
5. The leg then does **not** fill. It goes CANCELLED ten minutes later. ⛔ The
   attribution stands forever.

## 🔬 THE THREE CASES, AND THE CONTROL
| Date | Symbol | rung | closure_source | Truth |
|---|---|---|---|---|
| 03-Sep | ANANTRAJ | `mid_fill` | **OWN_SL** | ⛔ FALSE — SL CANCELLED 15:17:04, never filled |
| 07-Sep | V2RETAIL | `none` | **EXTERNAL_UNATTRIBUTED** | ✅ CORRECT |
| 09-Sep | ORCHPHARMA | `mid_fill` | **OWN_SL** | ⛔ FALSE — SL CANCELLED 15:17:02, never filled |

⭐⭐ **V2RETAIL IS THE CONTROL AND IT EXONERATES THE CLASSIFIER.** Same mid-fill
refusal at 15:17:20 — but its EOD leg had genuinely gone COMPLETE at 15:17:07, so
`named_by_local={EOD}` and `named_by_midfill={SL}` **disagreed**, the contradiction
rule fired (`:131-140`), and the verdict was `EXTERNAL_UNATTRIBUTED rung=none` at
CRITICAL. ⇒ ⭐ **The ladder, the contradiction rule and the first principle all work.
Rung 4 alone is the defect** — and only when it is the *sole* speaker.

## 🔴 THE GUARD EXISTS AND IS SWITCHED OFF
`check1_mid_fill_defer_sec: **0.0**` — measured in **production's own
`config/system_config.yaml:463`**, not just the repo's. `_check1_deferral_gate`
returns `0.0` for any non-positive value (`:1113-1116`), so `deferral_expired` is
**permanently False** and rung 4 **can never go stale**. ⭐ §D built the expiry that
would have caught exactly this and shipped it disabled.

## ⛔ WHAT THIS IS NOT
⛔ It is **not** `order_manager.close_trade`'s `_EXIT_REASON_TO_CLOSURE_SOURCE` map
(`order_manager.py:106-108`). That path writes `status='CLOSED'` with a validated
`exit_reason`; all three incident rows are `CLOSED_MANUAL` / `exit_reason='MANUAL'`,
which that map cannot produce. ⛔ Nor the W8 backfill — it requires
`o.status='COMPLETE'`.

⭐ **ChatGPT's frozen rule maps onto the EXISTING vocabulary with no new enum:**
`EXTERNAL_UNATTRIBUTED` already means *"nothing of ours accounts for it"* and
`core/closure_source.py` explicitly forbids minting `BROKER_RMS`/`OPERATOR_MANUAL`.
⇒ ⭐ the fix is to stop rung 4 claiming a fill, ⛔ not to add a value.

See [[a_terminal_mark_can_delete_its_own_retry_04sep]] ·
[[orders_qty_filled_is_never_populated_10sep]] ·
[[no_order_path_can_send_market_09sep]].
