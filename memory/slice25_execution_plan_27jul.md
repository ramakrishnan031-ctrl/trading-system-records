---
name: slice25-execution-plan-27jul
description: "Slice 2.5 day-by-day execution plan — the T2 overnight leg is NOT isolated from the live service, --arm-overnight exit 1 still holds stock, and the 2FA seed move blocks Mon 3-Aug."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T17:21:04.152Z
---

Plan: `docs/audit/slice25_execution_plan_27jul2026.md` · **operator card:
`docs/T2_RUNBOOK_29-JUL.txt`** (⛔ both uncommitted 27-Jul so the Monday card's 24-commit assertion
stays true; commit after the push). ⭐ **The runbook's two calming facts, both source-derived: max
overnight loss = ONE SHARE (~Rs 10), and a GTT CANNOT FIRE while the market is closed — so there is
NO overnight execution risk; the gap risk lands at the Thu 09:15 open.** Decisions: #16a **BLOCK**,
S4 **DEGRADE** [[failfast-vs-degrade-discriminator-27jul]]; 2FA seed move **deferred off 31-Jul**.
⛔ **A PLAN — nothing enabled, no flag flipped, no script run.** [[handoff-26jul-alert-stream]]

## ⛔ The four things that will be misread if not written down

1. ⭐⭐ **T2's overnight GTT IS VISIBLE TO THE LIVE SERVICE. Its DB is isolated; the BROKER ACCOUNT
   IS NOT.** `CncGttMonitor` is built **unconditionally** (`main.py:2686`, NOT gated on
   `delivery_enabled`), wired at `:2713`, and `adopt_orphan_gtts()` runs as a prepass on **every**
   reconcile cycle (`order_reconciler.py:668`). GTT ops are ungated by design
   (`zerodha_adapter.py:683,734,766` — "protection must survive disablement").
   ⇒ **the morning after arming: ONE `WARNING` "Orphan GTT — no open delivery trade (IDEA)",
   deduped once per gtt_id per process. EXPECTED, NOT a finding** — its ABSENCE is the interesting
   result. ⭐ Safe: adoption only INSERTs or WARNs, never deletes; `_orphan_sweep_and_cap` never
   touches a GTT with no `gtt_state` row (FIX-182). ⭐ **Free bonus: this is the first ever real
   execution of piece #8 (FIX-183 adoption), two stages early.**
2. ⛔⛔ **`--arm-overnight` EXIT 1 STILL MEANS YOU ARE HOLDING STOCK OVERNIGHT.**
   `run_single_session` sets `intentional_hold = True` **before** evaluating the result
   (`if arm_overnight: intentional_hold = True; … return 0 if ok else 1`), so the `finally` skips
   BOTH ensure-flat and GTT deletion. **Confirm the broker position and the GTT by hand, whatever
   the exit code says.**
3. ✅✅ **SUPERSEDED 27-Jul 22:4x — THE BIT-ROT TRAP IS REMOVED, NOT DOCUMENTED.** `fix-t2-repair-07jul`
   is MERGED and PUSHED (`e6ec75b`), the band is widened, and **ALL THREE copies are now sha256
   `0a3c505c…`** — repo, VM `scripts/`, VM `~/t2_proof_run/` — **verified by computing on the VM,
   not by assuming the sync worked.** The runbook's step-zero assertion was re-checked against the
   file it points at: MATCH. ⇒ **running the wrong PATH can no longer run the wrong CODE.**
   ⚠️ **Keep checking the sha256 anyway** — it is what proves the above is still true, and
   **`--help` is still not a check** (every version has `--arm-overnight`).
   ⛔ Old hashes, for RECOGNITION only: `a5779420…` = repaired but un-widened (band still −3/+5) ·
   `23aca731…` = the bit-rotted copy. Seeing either means a stale copy.
   ⭐⭐ **AND THE CARD NOW GUARDS THE DATE (`0a6a95f`): "DO NOT RUN THIS ON TUESDAY 28-JUL."**
   Rama opens the T2 card on TUESDAY while checking the migration — reading it then is fine,
   running it is not. **P0 = `date "+%A %d-%b-%Y"` must print Wednesday 29-Jul-2026.** ⭐ It is P0,
   not P6, because it is **the only precondition that can be wrong while every other check passes
   cleanly — the script runs perfectly on the wrong day.** The calendar is the constraint; nothing
   in the code knows what date the plan says. ⛔ Arming on Tuesday would put a real CNC position
   into v45's single-variable boot and confound it.
4. ⭐ **T2 needs NO push, NO flag, NO deploy** — `_build_live_adapter` passes
   `delivery_enabled=True` on its own adapter instance (`:144`, "the gated exception").

## ⚠️⚠️ MEASURED 27-Jul — T2's GTT band makes the arm ROUGHLY A COIN FLIP

735 real symbol-days of 1-min candles (`analytics.db candles`, 19-Jun→24-Jul-2026, 482 symbols,
`is_synthetic=0`). **P(touch −3% or +5% before close), 11:30 anchor: 33.9% overall, 52.2% for
shares <Rs150.** A same-day trigger **VOIDS the arm** (day trade ⇒ no demat debit ⇒ nothing proved)
and costs a market day. ⛔ **This is NOT an edge case — it is the modal risk.**

⚠️ **SAMPLE LIMIT, stated: IDEA is NOT in the candle set at all** (0 candles, 0 `daily_symbol_stats`
rows; cheapest measured symbol = Rs 13.90). At ~Rs 10 it sits **below the sample floor**, so 52.2%
is a proxy and probably optimistic. [[feedback-verify-rc-not-output]]

**Levers, measured (11:30 anchor, <150 bucket):** band −3/+5 → −10/+10 = 52.2% → **9.0%** ·
→ −15/+15 = **1.5%** · anchor 11:30 → 13:30 = 52.2% → 23.9% (2.2×) · instrument <150 → >1000 =
52.2% → 13.9% (3.8×). ⭐ **BAND WIDTH DOMINATES and costs zero exposure.**

✅ **APPLIED 27-Jul `e6ec75b`: keep IDEA · band −10/+10 · arm ~13:00** ⇒ ~2.8%, expected arm-days
2.09 → 1.03. **−10/+10 not −20:** our `_validate_trigger_distance` has only a MIN (0.25%), **no
max** — but a **broker-side cap is UNVERIFIED from source** (kiteconnect does NO client-side
validation of `place_gtt`), so take the smallest band that solves it. ⛔ **A rejected GTT burns the
day exactly as a trigger does — do NOT "improve" this to ±20.**
⚠️⚠️ **THE OFFSETS WERE THREE SITES, NOT THE "2-line change" this file used to claim** — the real
placement, the **dry-run plan**, AND the seeded throwaway `trades` row. Fixing only the first would
have left a `--dry-run` rehearsal printing a band the real run does not use. Now **ONE constant pair
`_OCO_SL_MULT`/`_OCO_TGT_MULT`** with the reasoning attached, so it cannot drift again.
⭐ **The SL LIMIT sits `gtt_sl_limit_offset_pct` (3%) BELOW the trigger** ⇒ at LTP 10.00: trigger
9.0, limit 8.7 = **−13.0% of arm price** (was −6.0%). **The widen made the gap floor DEEPER, not
shallower** — recomputed from source, not adjusted by hand.
⭐ **Widening breaks no assertion** — `broker_ok`/`store_ok` check two-leg/OCO, SELL+CNC+qty, and the
durable row; **neither looks at trigger LEVELS. The structure is the proof; the levels are
incidental.**

⭐ **A gap-open does NOT invalidate the test.** An unsold share Thursday is still in Holdings ⇒ the
close step still exercises the demat debit. **Only a WEDNESDAY sale voids it.**

## Calendar (no weekday NSE holiday until 14-Sep-2026)

`27-Jul observe+push → 28-Jul v45 boot (single variable) → 29-Jul T2 arm → 30-Jul T2 close = DDPI
PROVEN → 4-Aug flag flip + carry pilot → earliest completion Thu 6-Aug, ZERO redos.`
- ⛔ **Friday is never an arm day** (a Fri→Mon carry holds real stock 3 unsupervised days for no
  extra evidence).
- ⛔ **Mon 3-Aug is BLOCKED** — the 2FA seed move is Fri 31-Jul/Sat 1-Aug and the re-enrol is
  **one-way, no rollback**, so 3-Aug is the first boot on a new enrolment. ⭐ This morning is the
  precedent: a rotated credential's broker acceptance stays UNPROVEN until a live boot answers.
  **A one-way credential change earns its own single-variable day.** [[feedback-no-fixed-test-baseline]]

## ⭐ Restart or resume — only desk work resumes

**Stage 2 DDPI rejection ⇒ RESTART stage 1 (2 days + broker turnaround).** A same-day square proves
nothing about demat. **Any carry-pilot failure ⇒ RESTART the pilot (2+ days)** — the evidence is an
*unbroken* carry across a real boot. ⇒ **four days is the ZERO-REDO FLOOR, not the plan.** One redo
in stage 3 ⇒ mid-August.

## ⭐⭐ The first irreversible step = all FOUR flags true together (Tue 4-Aug)

`delivery_enabled=true` + `force_intraday_only=false` + `trade_type=DELIVERY|BOTH` +
**`conditional_allocation_enabled=true`** ← the forgotten one; without it **70 % of capital strands
in the idle intraday bucket** (~₹6,913 of ₹9,875.60). The first three are **AND**-ed at
`zerodha_adapter.py:558` ⇒ any one false keeps the lock fully closed, so the flips can be staged.
⭐ **Rollback:** `delivery_enabled=false` refuses NEW CNC orders while GTT ops stay ungated ⇒
disarming never strands protection. ⛔ **What cannot be undone: a CNC already settled into demat —
it must be SOLD, and selling needs DDPI.** That is why stage 2 gates stage 3.

## 🟡 vs 🟢 — a green paper carry is WRONG evidence, not weak

`_paper_holdings` has one writer (`seed_paper_holding`, a test helper) ⇒ paper can inject a carry's
END STATE but never the TRANSITION. **A paper Mon→Tue prints a clean `GTT_EXIT` while protection was
torn down.** [[paper-cannot-exercise-class-26jul]]

## §B — one not-started piece left, and it is two items

**#15 paper CNC fidelity is DONE (`f7eedd3`).** Remaining: **#16a config foot-gun** (~2–3 h, precedent
`config_auditor.py:196` + `raise_if_blocked()`; blocks the FLAG FLIP, not stage 1) and **#16b
GTT-linkage-loss** (4–6 h, LOW confidence, a design question). ⭐ **Re-scope #16b AFTER v45 lands** —
it is the same false premise as CHECK1 ("no position ⇒ closed externally") and the `closure_source`
vocabulary in tonight's 24 commits changes the available answer. ⇒ **neither blocks stages 1–2: the
T2 pair can start 29-Jul with no code written.**
