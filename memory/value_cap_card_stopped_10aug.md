---
name: value-cap-card-stopped-10aug
description: "CLOSED 10-Aug (Rama: change nothing). The VALUE CAPS card was stopped at its own §4 gate before any edit: §1.1's delivery cap verified (₹750, change nothing — CONFIRMED), but intraday ALREADY has a ₹8,750 cap, a ₹6,000 ceiling can never bind by construction (qty×price ≤ ₹5,833 always), and an absolute ₹ key is a guarded deleted key the config auditor tells you to remove."
metadata: 
  node_type: memory
  type: project
  originSessionId: 55f762b9-1f1c-4ab4-b80b-c1b50da706f7
  modified: 2026-08-10T11:14:24.273Z
---

**`<MEASURED ONLY · ⛔ NOTHING EDITED · ⛔ NOTHING COMMITTED>`** — the card's own §4 says
*"Report §1.1's measured delivery cap and §3's failure count FIRST. ⛔ If either differs from what is
stated here, STOP before editing."* ⭐ **Delivery matched; two other premises did not.**
🧪 **PARITY: pure sizing — paper exercises it identically. ⛔ Nothing was built, so nothing is claimed.**

---

## ① ✅ §1.1 VERIFIED — THE DELIVERY DECISION IS RIGHT

**(P) `system_config.yaml:258` `delivery_max_position_value_pct: 0.25` · `:255` the DELIVERY PLANNING
BASIS is `₹3,000` (bucket × 1.0, unleveraged, at ₹10k).** ⇒ **cap = `0.25 × 3,000 = ₹750`** ✅
**exactly as the card states**, against a delivery allocation of `3,000 ÷ 6 = ₹500`.
⇒ ⭐ **`₹750` already sits ABOVE the allocation and already does the backstop job ⇒ *"change nothing"*
is CONFIRMED BY MEASUREMENT.** ⛔ **And the requested `₹1,500` would have DOUBLED it — a LOOSENING.**

---

## ② 🔴 BUT INTRADAY ALREADY HAS THE SAME THING — the card's own test, applied to its own case

**(P) `:228` `max_position_value_pct: 0.25` · `:187` the INTRADAY PLANNING BASIS is
`₹35,000 = ₹7,000 × leverage 5`.** ⇒ **cap = `0.25 × 35,000 = ₹8,750`**, against an allocation of
`35,000 ÷ 6 = ₹5,833`.

> ## ⭐⭐ **`₹8,750 > ₹5,833` — SO THE CARD'S DELIVERY ARGUMENT (*"already above the allocation ⇒ change nothing"*) GIVES THE SAME ANSWER FOR INTRADAY.** ⛔ **The premise *"nothing to rewrite, one config line"* mis-states the starting point: a cap EXISTS and it already backstops.**

⭐ `₹6,000` would be a **TIGHTER** anomaly backstop (`1.03×` the allocation vs `1.50×`) — ⛔ **a
legitimate choice, but a TIGHTENING of a working control, ⛔ not the addition of a missing one.**

---

## ③ 🔑🔑 AND `₹6,000` COULD NEVER BIND — **BY CONSTRUCTION, ⛔ not by sampling**

**(P) `capital/position_sizer.py:586-589`:**
```
stop_pct         = sl_rupees / entry_price
risk_budget      = allocation * stop_pct
qty_by_allocation = floor(risk_budget / sl_rupees)
```
⭐ **Substitute and the stop CANCELS: `allocation × (sl/price) ÷ sl = allocation ÷ price`** ⇒
**`qty = floor(allocation ÷ price)`** — which is the build's own title, *"the stop moves the money,
not the size"*, and the suite pins it (`tight.qty == wide.qty == 58`).
**And `effective_mult` is clamped `≤ 1.0`** *(test: `⛔ NOT 116`; its docstring — "6 × allocation = the
basis exactly and any excess would breach it")*.

> ## ⇒ **`qty × price ≤ allocation = ₹5,833.33` AT ANY PRICE, ANY STOP, ANY TIER. A `₹6,000` CEILING CAN NEVER FIRE.**
> ⛔ **It is an INERT ceiling, ⛔ not a backstop.** ⭐ **This also ANSWERS §3's gate without editing
> anything: ZERO new failures — because the cap can never bind at all.**
*(Cross-check at the suite's own price of `₹100`: `58 × 100 = ₹5,800` · `40 × 100 = ₹4,000` · the
delivery case `5 × 100 = ₹500` — all below `₹6,000`.)*

---

## ④ 🚫 THE KEY ITSELF IS **GUARDED** — an absolute ₹ cap was DELETED and is policed

**(P) `core/config_auditor.py:347-352`** raises **`B2_max_position_value_rs_resurrected`** (WARN):
*"position_sizing.max_position_value_rs reappeared — BUILD 1 replaced it with the capital-relative
`max_position_value_pct`. **Remove the Rs key.**"* ⚠️ **And preflight `B_single_source` asserts *"no
resurrected deleted keys (daily_loss_limit / max_position_value_rs / live_test_* / …)"*.**

⇒ ⛔ **Adding it under that name TRIPS A NAMED GUARD; adding it under a DIFFERENT name EVADES a guard
built for exactly this.** ⭐ The card's §2.2 anticipated the tension *("twice retired absolute limits
for rotting")* — ⛔ **but not that an AUTOMATED CHECK already enforces it.**

---

## ⑤ 📌 ALSO VERIFIED, AND IT MAKES §2.1 A NO-OP

⛔ **There is nothing to drop: `max_qty` is NOT shipped.** Both occurrences in `system_config.yaml`
(`:230`, `:261`) are **COMMENTED**, and every line the working tree adds over `65b7196` is a comment.
⭐ **The `3` was always a PROPOSAL.** ⚠️ `position_sizer.py:602-604` shows the code *supports* a
`max_qty` policy lever that TRIMS, distinct from `max_single_order_qty` which REJECTS —
**the mechanism exists, unset.** [[stated-vs-configured-limits-09aug]]

---

## ⑥ 🟢 **ANSWERED AND CLOSED, 10-Aug — RAMA: CHANGE NOTHING.**

> ## ⭐⭐ **A POSITION-VALUE CAP ON THIS SYSTEM HAS EXACTLY TWO STATES, AND *"BACKSTOP"* IS NOT ONE OF THEM:** **ABOVE the allocation ⇒ INERT** *(`₹8,750` today and the proposed `₹6,000` are EQUALLY incapable)* · **BELOW it ⇒ IT BECOMES THE SIZER**, binds on every trade, and costs the twelve-test rewrite.
> 🔑 **THE ALLOCATION *IS* THE POSITION-VALUE CAP — `₹5,833` intraday, `₹500` delivery, BY CONSTRUCTION** ⇒ ⛔ **there is nothing for a second ceiling to protect.**

✅ **DECISION: intraday `0.25` STAYS · delivery `0.25` STAYS · `max_qty` STAYS ABSENT.**
⛔ **THE SIZING-CAP THREAD IS CLOSED — no further rounds.** ⛔ **And the percentage-precision question
is DECLINED: `0.17142857` vs `0.18` only matters if the cap is changing, and it is not.**

### 🏷️ THREE WRONG NUMBERS, ONE ROOT CAUSE — ⭐ recorded because the cause is reusable
**`₹2,000`** *(would have bound every trade)* → **`₹1,500`** for delivery *(would have DOUBLED a
`₹750` cap the intent was to TIGHTEN)* → **`₹6,000`** *(inert, guarded, duplicating a working
`₹8,750`)*.
> ## ⛔ **ALL THREE CAME FROM PROPOSING A CEILING WITHOUT FIRST MEASURING WHAT ALREADY CAPS THE THING.** ⭐ **The allocation was the cap the whole time — in the sizer that had already been read.**

### ⭐⭐ AND THE GUARD DESERVES THE CREDIT
**`config_auditor.py:347-352` `B2_max_position_value_rs_resurrected`, with preflight's
`B_single_source` behind it: a control built for EXACTLY this case fired on EXACTLY this case.**
> 🔑 **THE SHARPER HALF: adding the key under a DIFFERENT NAME would have EVADED a guard built for
> it.** ⛔ **A rename is not a workaround — it is the failure mode the guard exists to catch.**

---

## ⑦ 📌 IF SMALLER TEST-PHASE POSITIONS ARE EVER WANTED — ⛔ RECORD, ⛔ DO NOT BUILD

> ## ⭐ **THERE IS NO FREE LEVER.** The suite pins `₹5,833 → 58 shares`, so **ANY mechanism that reduces position size breaks the SAME TWELVE TESTS** — a value cap, a smaller basis, or a larger divisor. **The cost is identical whichever is pulled.**
> ⇒ 📌 **`SMALLER TEST-PHASE POSITIONS = one config line + the twelve-edit test split. No cheaper path
> exists.`** ⛔ **So it is a decision about whether the smaller size is worth a session, ⛔ NOT a
> question about which knob.**

⭐ **Nothing is unprotected while that waits: positions are ALREADY bounded at `₹5,833` / `₹500`.**

---

## ⑧ ⚠️ TWO QUALIFIERS ON §⑥, ACCEPTED — ⭐ AND THE LESSON THAT ACTUALLY GENERALISES

**⑧.1 — IT IS A FACT ABOUT *THIS* SIZER, ⛔ NOT A UNIVERSAL LAW.** `qty × price ≤ allocation` holds
**while `qty = floor(allocation ÷ price)` holds.** ⛔ **A deliberate redesign of the sizing formula
RE-OPENS the question**, and a future reader must check the formula still reduces that way before
re-applying the conclusion. [[stated-vs-configured-limits-09aug]]

**⑧.2 — ⛔ THE GUARD DID NOT BLOCK THE EDIT; *MEASUREMENT* DID.** `B2_max_position_value_rs_resurrected`
is a **WARN raised when the key is ALREADY PRESENT** — it would have caught the key **after** it was
written, at the next audit or preflight run. ⭐ **It is a NET, ⛔ not a GATE.** The thing that actually
stopped the edit was measuring what already capped the position. ⭐ **The *"a rename would have evaded
it"* point stands unchanged.**

> ## ⭐⭐ **THE PERMANENT LESSON IS THE REVIEW *ORDER*, ⛔ NOT THE THREE NUMBERS:**
> ## **① MEASURE THE EXISTING CONTROL → ② ESTABLISH WHAT IT ACTUALLY BINDS ON → ③ ONLY THEN PROPOSE A NEW ONE.**
> ⛔ **All three wrong figures came from skipping ① and ②.**

🔒 **LOCKED, ⛔ DO NOT REOPEN:** intraday `0.25` · delivery `0.25` · `max_qty` absent · tiers,
thresholds, bases, counts, loss limits and both concentration caps unchanged · **⛔ no twelve-test
split · ⛔ no percentage-precision investigation.**
