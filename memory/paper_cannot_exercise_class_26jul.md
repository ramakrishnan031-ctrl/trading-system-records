---
name: paper-cannot-exercise-class-26jul
description: "The named pattern 'PAPER CANNOT EXERCISE IT' — a paper branch returning a CONSTANT cannot produce a VARIABLE input, so every behaviour keyed to that variation is untested however many paper sessions run; 3 instances found independently 26-Jul-2026 plus a full sweep of the adapter."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1c52b905-f204-4abe-966d-ae9b3bbd045e
  modified: 2026-07-26T17:46:54.924Z
---

⛔ **BEFORE CALLING ANYTHING "PAPER-PROVEN", ASK WHAT INPUT TRIGGERS IT AND WHETHER THE PAPER
ADAPTER CAN PRODUCE THAT INPUT.** A paper branch that returns a **constant** cannot produce a
**variable** input ⇒ every behaviour keyed to that variation is untested no matter how many
paper sessions run.

**Why:** "paper-proven" is the literal gate on Slice 2.5 going live with real capital. Three
instances were found **independently, in one weekend**, on three unrelated investigations —
that makes it a class, not a coincidence:

| instance | consequence |
|---|---|
| `product="MIS"` hardcoded in the paper book (fixed `f7eedd3`) | paper could not exercise the CNC EOD exemption — *the stated gate for delivery going live* |
| `get_trades()` returns `[]` | paper cannot reach CHECK1 rungs 1-2 ⇒ the contradiction rule, a **safety** property, can never fire there |
| `cancel_order` returns success unconditionally | paper cannot exercise §D's mid-fill deferral **at all** |

**How to apply:**
- ⭐ **CHEAP DIAGNOSTIC: a test that reaches PAST the public API to set up state is naming a
  gap.** Found gap #1 below exactly that way — `env.adapter._paper_gtts[gid]["status"] =
  "triggered"` exists because the adapter cannot produce that transition.
- ⚠️ **"N unit tests on the real paper adapter" ≠ "a paper session can demonstrate it."** Two
  different claims. Only say the one you measured.
- Where paper structurally cannot rehearse a path, **label it a live-only path** — do not let
  it inherit paper's green.

📊 **SWEEP, 26-Jul (`docs/audit/paper_fidelity_gaps_26jul2026.md`):** 22 `zerodha_adapter`
methods have a paper branch; 3 are paper-only seams/setters ⇒ **19 answer a broker question,
of which 9 return a constant outcome and 5 more carry a field that never varies — 14 of 19**
(the remaining 5 are genuine simulations; 9+5+5=19, every method in exactly one bucket).
⛔ **NOTHING FIXED — several are legitimate; which is which is a design conversation.**

🔴 **THE THREE THAT GATE SLICE 2.5 — classified WEAKER (proves less) vs WRONG (green that
means the opposite). ⭐ Only WRONG is urgent:**
1. ✅ **FIXED 26-Jul** — `_paper_gtts` status was only ever written `"active"` ⇒ **a GTT could
   NEVER FIRE in paper**, so `CncGttMonitor`'s PRIMARY path (triggered+flat → `GTT_EXIT`) and
   F6 were unreachable while 25 tests *looked* like coverage. **Was WRONG-class.** See
   [[paper-gtt-can-fire-26jul]].
2. 🔴 **WRONG — and now the ONLY one. SCOPED + SPECIFIED 26-Jul →
   `docs/audit/paper_overnight_carry_26jul2026.md`.** All three paper stores are in-memory
   (`zerodha_adapter.py:424/429/432`) and die with the restart while `gtt_state` (a real table)
   survives ⇒ Tuesday `_gather` sees empty/empty/empty against a live row ⇒ **rung 4's SECOND
   sub-branch, `cnc_gtt_monitor.py:412`** (*"GTT gone + flat — the GTT did its job"*) — ⚠️ **not
   the delete-the-orphan branch: `present_active` is False because the paper GTT died too.**
   `_finalize_gtt_exit` then books a P&L at **Tuesday's live LTP** (paper `get_trades()==[]` ⇒
   `_resolve_exit_price` falls through), releases capital, publishes `PositionClosed` and CLEANs
   the row. **Every artefact is indistinguishable from a real carried exit.**
   ⚖️ **LATENT, and it arms itself at the worst moment:** `reconcile()` has no `delivery_enabled`
   gate but the row set is empty today ⇒ **reachable the instant delivery is flipped in paper,
   which is the instant the paper run becomes the gate.**
   📊 **THE FRACTION:** of 14 lifecycle stages, 9 paper-provable, 2 only via a seam / degraded,
   **3 not at all** (T+1 transition · the Tuesday re-verify · DDPI) — and those 3 are consecutive
   and ARE delivery.
   ⭐ **PASS for the live pair = the first Tuesday reconcile emits `healthy:<symbol>` and
   finalises NOTHING.** That label is the one observation paper structurally cannot produce.
   ⛔ **Do NOT "fix" by persisting positions (invents a settlement model) or by calling
   `seed_paper_holding()` from production (a test seam on the live path). The honest
   position is that the Mon→Tue live pair is IRREDUCIBLE — keep saying so.**
   ✅💡 **THE RUN NOW SAYS IT (`ea65581`) — `CncGttMonitor._announce_paper_carry_blind_spot`.**
   CRITICAL, keyed off `gtt_state.created_at < today`, firing **BEFORE** the misleading
   `GTT_EXIT` (pinned on the ORDER of the two alerts — a reader meeting a tidy exit ten seconds
   later will not connect them). ⛔ **It ANNOUNCES, it does not DIVERGE:** the fabricated exit
   still happens, because making paper behave differently from live here is its own parity lie.
   **PAPER-ONLY BY A MODE CHECK**, not a config flag — proven silent in LIVE against an
   *identical* backdated row (same store, same adapter, only `mode` differs). Detection **fails
   CLOSED** (a blank `created_at` is never "carried"); once per calendar date, so a
   `needs_review` latch cannot re-announce every 15-min cycle. **Silent today: delivery is off
   ⇒ the loop has no rows.** ⭐ The gap itself is UNCHANGED — the live pair is still irreducible.
3. **WEAKER** — `cancel_order` constant success ⇒ [[check1-deferral-bound-26jul]] Limit 1.
   Absent coverage, no false green; the knob ships OFF.
   Also WEAKER: `get_trades()==[]` ⇒ CHECK1 rungs 1-2 + the contradiction rule unreachable.
   ⚠️ That rule is a SAFETY property — never offer "paper saw no contradiction" as evidence.

⚠️ **AND THE LARGEST, not a method:** `_synth_fill` writes only
`{"status":"COMPLETE","filled_qty":qty}` ⇒ **paper can never produce a REJECTED order and
never a PARTIAL fill.** Every paper order fills, completely, always.

⭐⭐ **A SECOND AXIS, ADDED 02-Aug (#2c Step-1) — NOT a missing METHOD but a wrong KEYING, and it is the one that makes a paper run LIE: PAPER NETS BY *SYMBOL*, LIVE KITE NETS PER *(SYMBOL, PRODUCT)*.** `_paper_positions` is a symbol-keyed dict (and `get_positions` iterates it), so in paper a sell of ANY product offsets a position of ANY other product. In LIVE it does not: selling MIS against a CO/CNC position does **not** close it — it opens a fresh NAKED position while the original survives.

⛔ **STANDING VALIDATION RULE (general, not #2c-specific): a PAPER DRILL OF ANY PRODUCT-SEMANTICS CHANGE IS VACUOUSLY GREEN.** Anything whose correctness depends on product IDENTITY — emergency flattens, EOD/kill squareoff, orphan recovery, the carry pilot — must be validated against LIVE semantics or BY CONSTRUCTION (code + broker docs + a cited prior measurement), **never by a paper run**. ⚠️ Corollary: paper also cannot produce two rows for one symbol with different products, so the Kite per-(symbol,product) ROW HAZARD ([[q4-hard-kill-delivery-30jul]] ledger #2/#2b) is live-only too.

📌 Where this bit: #2c was carded to "map the intent" at the reconciler flatten; a paper drill would have shown it working. Step-1 stopped it instead — `intent` IS the live Kite `product` field, and **Audit 3.1 says a CO position cannot be squared by a reverse order at all** (broker rejects; correct path = `cancel_order(entry_broker_id, variety="co")`, which `eod_squareoff` already does). Redesign = **#2c-R**, not started.

💡 **Cheapest remedy if one is ever wanted: not a richer simulation — a REFUSAL SEAM** (make
one call fail on demand). One seam serves `cancel_order`, `modify_order`, `place_order` and the
GTT trio, and changes no default behaviour.

Related: [[check1-deferral-bound-26jul]] · [[feedback-paper-live-parity]] ·
[[feedback-verify-rc-not-output]] · [[clock-dependency-class-26jul]]
