---
name: a_terminal_mark_can_delete_its_own_retry_04sep
description: "Marking a row terminal from an UNVERIFIED broker response, when the retry sweep excludes terminal rows, makes a false success latch permanently - the error deletes the evidence of itself; plus what a manual Kite close actually leaves behind"
metadata: 
  node_type: memory
  type: project
  originSessionId: 161ed55b-a158-4c12-a83a-53edac5888db
  modified: 2026-09-04T06:25:50.622Z
---

🔴 **AN ERROR THAT REMOVES ITS OWN CORRECTION PATH.**

## The shape

🔬 `order_reconciler._cancel_orphaned_orders_for_trade` (FIX-148) checks the
broker **response** -- `result.success` -- ⛔ but never the **effect**: it never
polls `get_order_history`. ⭐ Exactly one rung below F2's `_verify_cancelled`.

⭐ On `success` it calls `_mark_order_cancelled_local`, ⭐ which sets the row
**CANCELLED** -- ⭐ and 🔬 the sweep's own query is
`... AND status NOT IN ('CANCELLED','COMPLETE','REJECTED','FAILED')`.

⇒ 🔴 ⭐ **A false success LATCHES PERMANENTLY.** ⭐ It is never retried, ⭐ because the
retry set is defined by exactly the field the error just wrote. ⭐ Local reads
CANCELLED while the order stays live at the broker. 🔬 Only the *ambiguous* branch
survives across cycles.

⇒ ⭐ 📄 Name this separately from *"accepted ≠ effective"*, ⭐ because it is nastier:
⭐ **a wrong belief that deletes the evidence of itself.** ⭐ The system cannot
self-heal -- ⛔ not because nothing checks, ⭐ but because the check's INPUT SET was
filtered by the error.

## 🔴 RULE (standing)

⛔ **NEVER mark local state terminal from an UNVERIFIED broker response when the
retry set is defined by that same terminal state.** ⇒ ⭐ Either verify before
marking, ⭐ or keep a separate `pending_verification` flag the sweep does ⛔ **not**
filter out.

⏸ ⭐ **F3 work:** ⭐ grep for this shape everywhere -- ⭐ a row marked terminal from an
unverified response **and** a sweep that excludes terminal rows. ⭐ 📄 It is the
second half of the same contract gap as the **0-of-20** `place_order` finding:
⭐ one is *"we never check the write"*, ⭐ the other is *"and our unchecked belief
hides itself."* → [[restore_submitted_is_not_restore_live_04sep]]

## ⚖️ CALIBRATION -- structural, ⛔ NOT observed

🔬 **No false `cancel_order` success has ever been measured here.** ⭐ The 3-of-3
CANCEL_FAILED was the **opposite** error: ⭐ those cancels **did** take effect
(terminal at +1.115 s) ⭐ and the verifier was too impatient. ⇒ ⭐ Record it, ⛔ do not
act on it in a live session.

⭐ 📄 Correct wording: ⭐ *"15-30 s is an expected detection/cleanup path, ⛔ not a
guaranteed broker-side cancellation bound."*

## ⚠️ The `mid_fill` branch defers to a component that barely runs

⭐ *"Order ... being processed"* → ⭐ the code leaves the row for `order_monitor`.
⚠️ ⭐ 📄 But `order_monitor` produced **one log line on a full trading day.**
🔬 **Measured instance:** ⭐ ANANTRAJ 15:12:25 `cancel_order` → *"Order cannot be
cancelled as it is being processed. Try later."* ⇒ ⭐ that row went terminal at
**15:17:04** -- ⭐ five minutes later, ⭐ via the **EOD stale-order sweep**, ⛔ not via
`order_monitor`.

## 🔬 A MANUAL (Kite-side) CLOSE -- what it actually leaves

⭐ **CLOSE FIRST, then cancel, then VERIFY.** ⭐ Proven at source, ⛔ not reasoned:
🔬 **FIX-186 (FIX 3)** in the G5b path -- *"skip recovery SL when the broker
positively reports no live position for this symbol (manual close likely in
progress)"*.
  · ⭐ **Close-first** ⇒ ⭐ flat at broker ⇒ ⭐ G5b **skips**. ⭐ Safe.
  · ⛔ **Cancel-first** ⇒ ⭐ an OPEN trade with a live position and no active SL =
    🔬 G5b's exact **RC7** trigger, ⭐ and its other guards would ⛔ not stop it (⭐ the
    local SL row reads CANCELLED, ⭐ the settling window is long past,
    ⭐ `_already_has_live_sl` finds nothing) ⇒ 🔴 ⭐ **G5b arms a stop the human never
    placed**, ⭐ which he then orphans.
⚠️ ⭐ Residual: ⭐ the guard is `if broker_positions is not None` ⇒ ⭐ an unavailable
snapshot lets G5b proceed fail-safe ⭐ and it could arm on a flat position.

⭐ 🔬 There is ⛔ **NO system-side manual exit.** `_CONTROL_ACTIONS` is an explicit
allowlist (⭐ *"⛔ never a path passthrough"*): `entries.pause`, `entries.resume`,
`trading.stop`, `strategy.toggle`, `limits.update`. ⛔ No close-position action.
⭐ `trading.stop` is the kill switch -- ⛔ far too big, ⭐ and it leaves kill state
standing. ⇒ ⭐ **Kite by hand is the only route**, ⭐ and every manual intervention
therefore creates orphans.

⭐ 🔬 `_cancel_oco_siblings` has exactly ONE caller (`order_placer.py:2434`), ⭐ keyed
on `event.broker_order_id` from a **managed bracket-leg fill** ⇒ ⭐ a Kite-side close
is ⛔ not that fill, ⭐ so the OCO sweep does not retire the siblings.
⇒ ⭐ **A natural TGT/SL fill IS that managed fill** ⇒ ⭐ it goes flat CLEAN.
⭐ **So waiting is not merely cheaper -- it is safer than a hand close.**

## 🔴 WHY "VERIFY ZERO RESTING" IS THE LOAD-BEARING STEP

⭐ Three independent mechanisms, ⭐ three ways to be wrong, ⭐ **one check that catches
all three**:
  ⭐ **a.** ⭐ a false cancel-success **latches** and is never retried;
  ⭐ **b.** ⭐ *"being processed"* defers to a component that does not appear to run;
  ⭐ **c.** ⭐ G5b's skip guard is snapshot-conditional and fails **open**.
⇒ 🔴 ⭐ **FLAT = 0 open + 0 partial + no residual + NO RESTING SL/TGT/GTT.**
⛔ A position count is ⛔ not a flat book. ⭐ And a watcher result cannot authorise an
action -- ⭐ take a fresh read immediately before, ⭐ and refuse on any change.

⭐ See also [[push_to_main_force_reverts_and_replaces_crontab_04sep]] ·
[[config_edit_without_restart_is_a_split_state_04sep]]
