---
name: paper-gtt-can-fire-26jul
description: "A paper GTT can now FIRE (zerodha_adapter, paper-only) — it unblocks the INTRADAY CNC lifecycle in paper (healthy / GTT_EXIT / F6 all reachable) but NOT the overnight carry, which stays irreducible."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1c52b905-f204-4abe-966d-ae9b3bbd045e
  modified: 2026-07-26T14:51:00.677Z
---

**Built 26-Jul-2026 on `hold-check1-w8-26jul`, UNPUSHED. `broker/zerodha_adapter.py` —
PRODUCTION CODE, paper-only branch.** Report: `docs/audit/paper_gtt_trigger_26jul2026.md`.

⭐ **WHY: Slice 2.5's gate is "paper-proven", and EVERY CNC exit runs through a GTT.** Nothing
ever wrote a paper GTT status but `"active"` ⇒ `CncGttMonitor`'s primary path (triggered+flat
→ `GTT_EXIT`) and F6 were unreachable by a paper session. **The gate could not cover the exit
path it exists to gate.**

**WHAT:** `_gtt_triggered_leg(trigger_values, ltp)` — a **pure** predicate (0=SL, 1=TGT, None)
— plus `_paper_settle_gtt_triggers()`, called at the top of `get_gtt()`/`get_gtts()`. **No new
machinery:** reuses `_fetch_ltp()` (built for paper LTP-gated fills). ⭐ Reachable in a REAL
paper session — `main.py:2012` injects a Kite-backed `quote_provider`.
Rules: bounds **INCLUSIVE** (Zerodha fires when LTP *reaches* the trigger) · **SL checked
FIRST** (a poll can see a price outside BOTH bounds; the protective leg must win) · malformed
condition never fires · LTP fetched **outside** the lock · **status flip only, places nothing**.

⛔ **NOT MODELLED, each pinned by a test:** (1) **overnight/while-down triggering — the whole
point of a GTT**; (2) tick-level path (we poll ⇒ paper UNDER-triggers — safe direction, but it
cannot prove a GTT *would* fire); (3) **trigger ≠ fill** — reading a triggered paper GTT as
"position closed" is the passes-wrongly failure this guards.

✅ **WHAT IT UNBLOCKS (intraday, within one session): healthy · triggered→`GTT_EXIT` · F6 ·
orphan-active-flat — ALL now reachable.**
⛔ **WHAT IT DOES NOT: the overnight carry.** Paper position state is in-memory and dies with
the nightly restart; `_paper_holdings` has no production writer. **Mon→Tue live pair stays
IRREDUCIBLE.** [[paper-cannot-exercise-class-26jul]]

⚠️ **I GOT B4 WRONG FIRST AND CHECKED IT.** I read `held` as holdings-only ⇒ concluded every
paper CNC GTT is torn down on cycle 1. **`_gather` (`cnc_gtt_monitor.py:353-367`) sums holdings
AND CNC *positions*** — and paper positions are a real simulation carrying the order's true
product **since `f7eedd3`**. ⭐ **`f7eedd3` + this change are complementary: without the product
fix a paper CNC position reports `MIS` and `_gather` skips it.**

🧪 **EVIDENCE:** 17 new tests · blast radius **133/133**. ⭐ **RED-first measured TWICE — the
first attempt was weak:** removing the whole change gives a *collection error* (symbol absent),
which proves nothing about behaviour. Neutering only the settle pass gives **5 of 17 failing on
BEHAVIOUR** — exactly the five asserting triggering happens; the 12 green ones are the pure
predicate, the invariants and the two LIMIT tests, which **must** be green both ways.

⭐⭐ **B6 — THE PROOF IT IS REAL:** the established way to reach `triggered` was
`env.adapter._paper_gtts[gid]["status"] = "triggered"`. A new test produces the identical
observable by **moving the price and reading the public path**. **A test that no longer has to
cheat is the difference between a simulation and a stub.**

⚠️ **3 EXISTING FIXTURES HAD TO CHANGE AND THE REASON IS THE POINT:** they seeded ACTIVE GTTs
at `[100,110]`/`[1,2]` while the fixture quotes **337.0 for every symbol** — an untriggered GTT
3× below the traded price, a state production cannot produce, which survived only because a
paper GTT could never fire. Re-pointed to `[320,360]`. **Check the fixture against production
shape.** [[capital-readers-fixed-25jul]]

Related: [[paper-cannot-exercise-class-26jul]] · [[unpushed-pending-deploy-ledger]]
