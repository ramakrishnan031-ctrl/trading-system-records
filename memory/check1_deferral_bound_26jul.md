---
name: check1-deferral-bound-26jul
description: "CHECK1's mid-fill deferral (§D) — the bound is check1_mid_fill_defer_sec, WALL-CLOCK SECONDS, default 0.0 = OFF = pre-§D path proven structurally; raising it above 0 goes live in LIVE ONLY because paper can never produce the mid-fill refusal."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8999ae0b-3d00-4770-8853-d467ee57f31a
  modified: 2026-07-26T11:19:39.104Z
---

**§D built 26-Jul-2026 (`81f9372`, branch `hold-check1-w8-26jul`, UNPUSHED). CHECK1 can defer
finalizing when one of OUR OWN legs is filling, so our fill callback — not the reconciler's
backstop — releases the capital.**

⛔ **THE KNOB: `order_reconciler.check1_mid_fill_defer_sec`, DEFAULT `0.0` = OFF.**
**SECONDS, NOT CYCLES** — a cycle count is a proxy for elapsed time whose meaning changes
silently the day `poll_interval_sec` is retuned.

⭐ **0.0 IS A TRUE NO-OP, PROVEN STRUCTURALLY, NOT BY SIMILARITY.** At 0.0 the gate is not
entered: the bookkeeping is never read or written and the clock is never consulted. The test
replaces `_check1_deferred_since` with a tripwire raising on ANY access and `_monotonic` with a
callable that raises. Planting `> 0.0` → `>= 0.0` gives **2 RED for two independent reasons** —
the tripwire, AND the capital assertion (0 releases instead of 1).

⚠️⚠️ **BEFORE RAISING IT ABOVE 0, KNOW THESE TWO THINGS — both measured, not assumed:**
1. **PAPER CAN NEVER EXERCISE IT.** `zerodha_adapter.cancel_order`'s paper branch (`:909-918`)
   returns `success=True, reason=""` unconditionally ⇒ `_cancel_reason_being_processed` cannot
   fire ⇒ **the deferral is structurally unreachable in paper.** Turning it on ships an
   unrehearsed path straight into LIVE. (Same shape as the live-only rung 1.)
2. **IT IS NARROW.** ONLY the broker's own `"being processed"` refusal defers. The common
   shape — a leg already `COMPLETE` locally, **35 of 41 measured** — still finalizes in CHECK1
   at every bound, by design (ladder rows 1-2). So the knob buys less than it appears to.

⭐ **THE GATE RUNS BEFORE THE CLAIM, and that is the whole mechanism.** The instant
`mark_trade_manually_closed` fires, `order_placer._handle_exit_fill` hits its double-close guard
at `:2374` and CHECK1 owns the close regardless. ⇒ at bound > 0 the **orphan-leg cancel is
HOISTED ABOVE THE CLAIM** (the broker's refusal IS the signal). Safe both ways; if the position
turns out not to be gone, G5b re-places a recovery SL next cycle — strictly less harm than the
pre-§D path, which closes the trade and releases its capital on the same premise.

⏳ **EXPIRY: a mid-fill claim is a claim about NOW.** Bound elapsed with nothing terminal ⇒ the
claim is STALE, rung 4 falls **SILENT** (including for the contradiction check — a stale claim
must not manufacture a disagreement with a live source), and the verdict falls to
`EXTERNAL_UNATTRIBUTED` at CRITICAL. **Rungs 1-3 untouched** — expiry retires a stale claim, it
never destroys good evidence; forcing CRITICAL on a leg that DID reach COMPLETE would be a false
alarm manufactured by a timer. Logged `CHECK1 DEFERRAL EXPIRED UNRESOLVED` at WARNING **whatever
verdict follows** — an expired deferral is the case where the design was wrong.

🔁 **RESTART-SAFETY, ANSWERED AND PINNED (the question §D raised and §C did not):** the clock is
in memory, the trade is not. Die mid-deferral and the trade is still `OPEN` in the DB with its
capital reserved ⇒ boot rehydrates it and the next reconcile cycle re-enters CHECK1 with an empty
map, starting a **NEW bounded window, never an unbounded one**. Losing the clock costs at most
one more window of seconds; **it can never strand capital.** Persisting it would buy nothing and
cost a migration on the capital-bearing table.

Related: [[rms-manual-close-is-mislabel-26jul]] · [[unpushed-pending-deploy-ledger]] ·
[[feedback-no-fixed-test-baseline]]
