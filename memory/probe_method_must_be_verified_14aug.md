---
name: probe-method-must-be-verified-14aug
description: "A RED check is evidence only once its method is verified — three mis-specified probes in one morning, each of which nearly manufactured a false alarm."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c1209cf3-aa8d-4745-9d6c-9e7a09062975
  modified: 2026-08-14T03:57:11.706Z
---

# ⛔ A RED CHECK IS EVIDENCE ONLY ONCE ITS METHOD IS VERIFIED

The corpus already holds *"a green check is evidence only if it could have been red"*
([[feedback_verify_rc_not_output]]). **This is its mirror, and it was missing.** A mis-specified
probe manufactures a **false alarm in whichever direction it points** — on 14-Aug-2026 it pointed
**both** ways within one hour.

## Three instances, one morning

**① P2's frozen falsifier grepped a structured field name against a rendered log.**
*"`grep -c min_broker_cash_rs logs/preflight.log` still 0 after phase A"* ⇒ REFUTED. After phase A it
**was** still `0` — but the deploy was correct and provably live. `preflight.log` renders a human
tree (`├─ name ✅ PASS Nms message`) and **never** carries structured field names; the field exists
6× in `broker.py` and simply does not reach that log. Following it literally meant reporting
*"the running process is NOT the new code"* — and the card's own instruction on REFUTED was
**"⛔ Report immediately"**, i.e. a rollback path for a healthy deploy.

**② My own md5 re-verification of a frozen prediction came back MISMATCHED.**
The file was untouched (`mtime 2026-08-13 18:56:12.791`, 10,260 B, 154 lines, **0 CR**). My **region
selector** was wrong: the frozen region is `head -153` (through the `## ADDENDA` heading itself), not
`awk '/^## ADDENDA/{exit}'`. Correct method reproduces `2a193eb8…` exactly.

**③ I read the wrong file and concluded a register was three days stale.**
`docs/MASTER_PENDING_01-Aug-2026.md` has zero `N12`/`N13` rows, mtime `11-Aug 11:34` — so I drafted
*"the register is stale"*. ⛔ **False: that file is the SOURCE.** The REGISTER is
`D:/Projects/trading-system-main/docs/MASTER_REGISTER.md`, on the **`main` worktree**, and it is
current (`N13` = 16 rows, mtime `13-Aug 20:01`). The source file itself says so at its line 178:
*"content flows source → register"*.

## Why

A check that cannot find the thing reports its absence as a **finding**, and an absence-shaped
finding reads as urgent. Two of the three above were **already drafted as findings** before the
method was questioned. The green-check rule protects against complacency; **nothing protected against
alarm** until this line existed.

## How to apply

Before reporting **any** red/absent/mismatched result:

1. **Ask "could this probe have found the thing?"** — name the artefact the probe reads and confirm
   the thing would actually appear *there*, in *that* form. Structured field ≠ rendered log line.
2. **Reproduce a KNOWN-GOOD case with the same probe.** If the method cannot go green on something
   that is definitely true, it has not been shown to work. (Same shape as the deletion-safety query
   that returned *"safe"* for all ten branches — [[unpushed-pending-deploy-ledger]].)
3. **Confirm you are reading the right file** before concluding a file is wrong — source vs register,
   working tree vs deployed tree, worktree vs worktree. [[install_collision_map_10aug]] is the same
   trap on branch names: **check content, never the name** — and here, never the *path* either.
4. Only then report. A red result that survives all three is a finding; one that does not is a
   method bug, and it belongs in the record as such.

📌 **PATH NAME ≠ OBJECT TYPE, and PROBE ≠ EVIDENCE.** Classify before concluding, in both directions.
See [[fix2_scored_14aug]] for the morning this came from.

## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 601 B (budget 450 B). The index now carries a hook and this link.

- 🔍🔴🔝 **[⛔ A **RED** CHECK IS EVIDENCE ONLY ONCE ITS METHOD IS VERIFIED — NEW RULE, 14-Aug](probe_method_must_be_verified_14aug.md)** — ⭐ the mirror of *"a green check is evidence only if it could have been red"*, and it was MISSING. **THREE mis-specified probes fired in one morning**, two of them already drafted as findings: P2's frozen falsifier (would have declared a CORRECT deploy dead) · an md5 REGION SELECTOR · reading `MASTER_PENDING` (the SOURCE) and concluding the REGISTER was stale. ⛔ **Ask *"could this probe have found the thing?"* BEFORE reporting any absence.**
