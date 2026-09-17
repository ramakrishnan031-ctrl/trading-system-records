---
name: fix2-scored-14aug
description: "Fix 2 (1c8c710) scored on its first live boot 14-Aug-2026 — DEPLOYED + proven live-loaded, NOT VERIFIED LIVE; and the mis-specified-probe class that nearly reported a correct deploy as dead."
metadata: 
  node_type: memory
  type: project
  originSessionId: c1209cf3-aa8d-4745-9d6c-9e7a09062975
  modified: 2026-08-14T03:56:48.777Z
---

# Fix 2's first live boot — SCORED 14-Aug-2026

**Label reached: `DEPLOYED` + *proven live-loaded*. ⛔ NOT `VERIFIED LIVE`.** The ceiling was stated
in advance on 13-Aug and was **not** exceeded.

**Ladder:** ① file on disk ✅ (md5 13-Aug, re-verified today) · ② the running process loaded it ✅
(**today**) · ③ the predicates are CORRECT ⛔ **NOT REACHED** — neither failure arm fired
(cash `₹5,589` ≫ floor `₹2,000`; book FLAT ⇒ no carry).

## Boot — measured, not observed
Pre-boot control at `08:10:32`: `inactive`/`dead`, `ExecMainStartTimestamp` still **Thu 13-Aug
08:15:16**. Post-boot: **Fri 2026-08-14 08:15:12 IST**, `active`/`running`, `MainPID 3612311`,
`NRestarts=0`. ⭐ Without the pre-read, `active` is a check that could not have gone red.
`HARD_KILL` today = **0**. Prior-day `SOFT_KILL` **auto-cleared** `08:15:13.714` →
`INACTIVE`/`auto_clear_stale` — the headless guarantee fired.
P1's one named risk closed **live**: `"Config loaded from config (8 files)"` ⇒ `config/preflight.yaml`
(a 9th file in `config/`) not picked up ⇒ `extra="forbid"` never engaged.

## Scores
P1 ✅ · P2 ✅ (falsifier mis-specified, below) · P3 PASS+wording ✅ / **bracket REFUTED** ·
P4 ✅ · P5 ✅ · P6 ✅ so far (**entries NOT YET DETERMINABLE**, `entry_start=10:00`) ·
P7 first half ✅ / **second half NOT YET DETERMINABLE** (16:22 officer run) · P8 ✅.

**The two presence signatures, both first-ever occurrences in a 4,500-line log:**
- `preflight.log:4432` — `kite_funds_available ✅ PASS 38ms funds available: ₹5,589 (floor ₹2,000)`.
  The **eleven** prior runs (lines 3156→4316, 04-Aug→13-Aug) all read `funds available: ₹X` with
  **no `(floor …)` suffix**.
- `preflight.log:4489` — `capital_deployment ✅ PASS 1ms capital deployed 0.0% of opening cash
  (margin_used ₹0 / opening cash ₹5,589; pending ₹0)`. `grep -c "of opening cash"` = **1**.

## 🔴 THE FINDING — P2's falsifier is MIS-SPECIFIED and fired on a correct deploy
The frozen falsifier: *"`grep -c min_broker_cash_rs logs/preflight.log` still 0 after phase A."*
After phase A it **is** still `0` — yet the code is demonstrably live (the two signatures above).
**Cause:** `preflight.log` renders a **human tree** (`├─ name ✅ PASS Nms message`) and never carries
structured field names. C2 shows `min_broker_cash_rs` appears **6×** in `broker.py`; it just does not
reach *that* log. ⇒ ⛔ **Following the falsifier literally would have reported *"the running process
is NOT the new code"* about a process that is** — i.e. a rollback of a correct deploy.
P2's two innocent causes were ruled out **in advance**: header `LIVE/LFL836` (not paper) +
`kite_token_fresh_today ✅ PASS token minted today (2026-08-14)` (token mtime `08:15:01.694`).

## The ₹5,000 credit, and the drift CRITICAL it produced
`net=5588.6` held `08:15:26` → `09:16:10.750`, then stepped to `net=10588.6` at `09:16:25.847`.
A single **+₹5,000.00** credit just after the 09:15 open. Yesterday's close `₹10,578.60` ⇒ today
settles `₹10,588.60` = **+₹10.00**. ⇒ P3's bracket `₹9,500`–`₹11,500` was wrong **in the 08:30
window** and right 46 minutes later — **REFUTED on the number as measured**, ⛔ not softened.
`09:16:25.848 order_reconciler` `G3 CAPITAL_DRIFT: expected=5588.60 actual=10588.60 delta=5000.00
tolerance=558.86`; CRITICAL telegram `09:16:26.497`; `drift_handler` `"non-escalating source"`,
`tier=HARD` ⇒ alerted, **could not escalate**.
⛔ **Not Fix 2 — attributed by width:** the class fired 05-Aug 17× · 06-Aug 12× · 07-Aug 6× ·
11-Aug 2× · 12-Aug 2× · 14-Aug 1×; zero on 03/04/10/13 ⇒ predates the deploy on five days, and
`order_reconciler` is not among Fix 2's six files.
⚠️ **But the recorded decomposition does NOT apply today** — [[capital_drift_is_operand_mismatch_05aug]]
says delta = *deployed capital + unsettled realised P&L*; today deployed `₹0`, trades `0` ⇒ that
yields `₹0`, not `₹5,000`. **Today's cause is a broker-side credit: a different mechanism wearing the
same alert.**

## ⭐ The new predicate is REACHABLE — proven from the historical record
`preflight.log:4025`, `PRE-FLIGHT — Phase B — 10-Aug-2026`:
`capital_deployment ✅ PASS 1ms capital deployed 432.3% (margin_used ₹907 / total ₹210; pending ₹0)`
⇒ a real production state where `used > opening` which the **old code passed silently**. Under Fix 2
it WARNs. ⭐ Answers *"could this check ever go red?"* with a measured **YES**.
⛔ Does **not** make it `VERIFIED LIVE`: not deployed on 10-Aug, and this is a retrospective log read,
not an execution. Rung ③ still needs a live firing. See [[delivery_book_ceiling_10aug]].

## ⚠️ LATENT — the opening-cash operand seam
Phase B read `opening cash ₹5,589` at 09:14 while live cash became `₹10,588.60` at 09:16:25 — a
₹5,000 divergence **within two minutes of the check**. If `margin_used` ever exceeds the *opening*
snapshot while actual cash is higher, the new WARN can fire on a healthy book. **LATENT** (needs
`used > ₹5,588.60`; today `used = ₹0`), ⛔ not LIVE ⇒ document, do not chase.
📌 The same operand choice that makes the predicate reachable on a low-cash morning makes it
false-positive-capable on a mid-morning credit.

## Not done
⛔ No deploy · no push · no service start/stop/restart · no kill clear · no `resume.sh` · no config
edit · no code · **no broker call of my own** (every cash figure read from the system's own logs) ·
no second unit · no M-C2 · no filesystem cleanup · nothing removed under `D:\Projects\` ·
worktrees **9** / heads **78** / tags **32** unchanged · ⛔ nothing edited above the addenda line.

Record: `docs/audit/PREDICTION_fix2_boot_14-Aug-2026.md` ADDENDUM 1 (frozen region md5
`2a193eb8…` re-verified intact after the append) · register rows `N14-01`…`N14-06`.
See [[probe_method_must_be_verified_14aug]].

## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 531 B (budget 450 B). The index now carries a hook and this link.

- ⏳🔮🔝 **[FIX 2 SCORED 14-Aug — TWO HALVES STILL OPEN, ⛔ recorded as `NOT YET DETERMINABLE`, ⛔ never as a pass](fix2_scored_14aug.md)** — ① **P6's ENTRIES half**: `entry_start=10:00`, 0 trades at 09:20 ⇒ the window had not opened at report time. ② **P7's SECOND half**: registry re-divergence at the **16:22** officer run; at 09:18 registry mtime was still `13-Aug 18:56:31` (= the push) and tracked-file drift was EMPTY. 📌 **Both are FREE measurements at the next EOD pass — ⛔ neither needs a change.**
