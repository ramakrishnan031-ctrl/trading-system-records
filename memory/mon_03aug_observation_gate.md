---
name: mon-03aug-observation-gate
description: "MON 3-AUG is the observation day for the newly-live symbol+direction rule, and the TUE 4-AUG flag flip is hard-gated on it — including how to read a zero result."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7fe300ed-c132-40c8-900a-e2fba3315944
  modified: 2026-08-04T04:56:07.817Z
---

> ## ✅⭐⭐ **04-AUG 10:07 — THE GATE IS CLOSED BY EVIDENCE. RULE `<VERIFIED LIVE>`.**
> Monday produced **ZERO rows** (= NO EVIDENCE, carried forward). **Tuesday EXERCISED it:**
> `SCI REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` @ `2026-08-04T10:07:00+05:30` —
> *"SCI LONG already traded today (1 executed trade(s))"*.
> ⭐⭐ **CORRECT ON ALL THREE AXES, not just "it fired":** (1) **SAME direction** — LONG blocked
> LONG, ⛔ NOT the opposite-direction/reversal case the gate called WORSE-than-unexplained;
> (2) **counted the OPEN fill** (10:06:15, qty 1) — in `_EXECUTED_TRADE_STATUSES`;
> (3) ⭐ **correctly IGNORED the earlier FAILED attempt** (10:01:14, qty 0) — `FAILED` is NOT an
> executed status, so the count was **1, not 2**. A naive `status='CLOSED'` query would have
> reported this working rejection as UNEXPLAINED and postponed the flip for no reason.
> ⇒ **No postponement. WED 5-AUG FLIP stands on this half.** ⛔ Still gated on its OTHER parts.

**MON 3-AUG-2026 IS AN OBSERVATION DAY. ⛔ BUILD NOTHING; MEASURE.** The
symbol+direction rule went live at Monday's 08:15 boot — deployed Fri 31-Jul
21:44:48 as `96a5e66..297b587`, verified 3 ways + `load_all()` = CONFIG_LOAD_OK.
It is **ONE live boot variable**: the rule can only ADD a rejection
(`signals.status = REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT`), never place a trade.

✅⛔ **"3-AUG IS A HOLIDAY" WAS RAISED 31-Jul AND IS FALSE — DO NOT RE-LITIGATE.**
⭐ **NOW CLOSED AGAINST THE PRIMARY SOURCE, not just the file: NSE circular
NSE/CMTR/71775 (12-Dec-2025), `~/Downloads/NSE_HOLIDAY.pdf`. 3-Aug-2026 is a MONDAY and is on
NEITHER list (15 trading holidays + 4 weekend); the only August entry in the circular is
15-Aug, a SATURDAY. Independence Day is the 15th, not the 3rd.**
`config/nse_holidays_2026.yaml` (the file `config_loader.py:2166` resolves by year, and the
sole source — every consumer routes through `utils/holiday_guard.py`) has **NO August entry
at all**; the list jumps 2026-06-26 → 2026-09-14. The system's own `is_trading_day()` returns
**True for 2026-08-03 (Mon)** and `next_trading_day(31-Jul)` = **2026-08-03**. ⇒ No collision;
the observe-Mon → flip-Tue sequence stands UNCHANGED. ⭐ And the gate is self-protecting
anyway: a closed market yields zero rows + zero signal traffic, which the card already reads
as NO EVIDENCE, never a pass — so a wrong holiday file could not have let the flip through.
✅ **THE FILE RECONCILES TO THE CIRCULAR EXACTLY — 15/15 + 4/4 ⇒ no data defect, nothing to
edit.** ⛔ **ROOT CAUSE WAS A MISREAD: a COMMENT (`# 15-Aug-2026 (Sat)…`) read as DATA** —
registered F6, and the rule is [[feedback-verify-scheduling-facts-31jul]].
✅ **NOTHING WAS EVER REVERTED because nothing landed** — clean tree, no commit after
`2b2ea77`, card body still `'2026-08-03'` ×3, Downloads calendar md5-identical to tracked.

▶️ **CARD (the query + the full decision table): `Downloads/MON_03-AUG_OBSERVATION_CARD.txt`**,
mirrored in the tracked calendar `docs/DEPLOY_CALENDAR_28-JUL_TO_04-AUG.txt` §7.2.

⛔⛔ **THE TUE 4-AUG FLAG FLIP IS HARD-GATED ON MONDAY.** Any UNEXPLAINED row —
both direction counts 0, or ONLY the opposite direction — **POSTPONES THE FLIP**.
It is the query's answer, not a judgement made on the day. Opposite-direction-only
is WORSE than unexplained: the rule blocked a REVERSAL, which its own docstring
says would be wrong ⇒ **the rule also comes back OFF**.

⭐⭐ **ZERO ROWS IS NOT A PASS** — it means the rule was never EXERCISED. Read it as
NO EVIDENCE, never as good evidence, and say so out loud. It does NOT postpone the
flip (that is a DELIVERY change), but it carries forward as an OPEN observation.
⚠️ And prove the day had signal traffic **before** believing the zero — a zero must
not be a silent plumbing failure.

⛔ **COUNT TRADES THE WAY THE RULE COUNTS THEM:** `_EXECUTED_TRADE_STATUSES`
(PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL) on
`SUBSTR(created_at,1,10)`. A query written on `status='CLOSED'` would report
correctly-working rejections as UNEXPLAINED and postpone 4-Aug for no reason.

⚠️ **EXPECT A NEW `REJECTED_NOT_MIS_TRADABLE (shadow)` WARNING from Monday.** That is
the `mis_filter` SHADOW log — **nothing was dropped**. Verified on the deployed tree:
`secondary_screener.py:144` rejects only when shadow is false; the newly-reachable
`_is_mis_blocked_decision` does two in-memory reads + one log; `mis_blocklist._persist_locked`
(the only writer) is reachable ONLY from `record_block`. ⛔ Do not misread it as enforcing.

⚠️ **STILL OWED BEFORE THE CARRY PILOT:** the buy-day product filter (+ CRITICAL-on-NULL),
with Q9's BL9 trace attached — schedule it between Monday and the flip. [[q4-hard-kill-delivery-30jul]]
⛔⛔ **AND THAT GAP IS ONE EVENING — Monday is BUILD-NOTHING and the filter is CAREFUL-LOOP
(it decides a PRODUCT on a live order) ⇒ its honest window was the WEEKEND (Sat 1 / Sun 2-Aug).
DO NOT RUSH IT MONDAY NIGHT; something slips instead.** ⭐ **OPEN — RAMA'S CALL, DECIDE BEFORE
MONDAY:** as recorded the flip's gate is **TWO**-part and the filter gates the **CARRY PILOT**
half (flip could still go); 31-Jul's instruction described it as **THREE**-part (a filter slip
postpones ALL of 4-Aug). Same deadline either way — they differ only if the filter SLIPS.

Related: [[feedback-status-label-rule-27jul]] · [[unpushed-pending-deploy-ledger]] ·
[[feedback-no-fixed-test-baseline]]
