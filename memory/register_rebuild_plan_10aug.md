---
name: register-rebuild-plan-10aug
description: "The MASTER_REGISTER rebuild — PHASE 1 COMPLETE 11-Aug (commit 1bde728 on main, 333 rows/291 merged, statuses UNVERIFIED). Findings 1-7, the four-source verification, and what is still owed."
metadata: 
  node_type: memory
  type: project
  originSessionId: a9e5145e-3355-41d5-843b-a151f730acea
  modified: 2026-08-10T18:51:55.975Z
---

# 🔨 THE REGISTER REBUILD — SOURCES VERIFIED 10-Aug-2026. ⛔ PHASE 1 NOT STARTED.

## ✅ §1 · THE SUBSET CLAIM — RE-VERIFIED MYSELF, ⛔ not taken on report. IT HOLDS.
**(P) sorted line-set comparison, CRLF-normalised, all three pairs:**

| pair | unique to `Downloads/` | unique to `docs/` | verdict |
|---|---|---|---|
| 28-Jul | **0** | **15** *(⚠️ the card said 6 — a LARGER superset, same conclusion)* | `docs/` strict superset |
| 30-Jul | **1** | 56 | ⭐ that line is a **SHORTER PREFIX-VARIANT**: `docs:67` is the SAME row extended with `⚠️ OPEN (§7.9(f))…`, `Downloads:53` just ends early ⇒ **nothing unique** |
| 04-Jul audit | **0** | **0** | **content-identical** |

> ## ⇒ ✅ **USE THE `docs/` COPIES ONLY.** ⭐ **AND AN IMPROVEMENT ON THE CARD: the 04-Jul audit is content-identical to `docs/audit/full_system_audit_04july2026.md`, so ALL FOUR SOURCES LIVE IN `docs/` — `Downloads/` is set aside ENTIRELY.**

**THE FOUR SOURCES:** ① `docs/MASTER_PENDING_28-Jul-2026.txt` ② `docs/MASTER_PENDING_30-Jul-2026.md` ③ `docs/MASTER_PENDING_01-Aug-2026.md` ④ `docs/audit/full_system_audit_04july2026.md`

## 🔴 §2 · THE ROOT CAUSE — VERIFIED, and it is STRUCTURAL
**(P) the precedence sentence exists in BOTH superseded files:** `28-Jul:7` *"WHERE THE TWO DISAGREE, \*\*\* THIS FILE WINS \*\*\* and the 01-Aug register is…"* · `30-Jul:8` *"Where the two disagree, THIS FILE WINS…"*.
⇒ ⭐⭐ **THE WORKING REGISTER IS AN INDEX THAT IS SUBORDINATE TO TWO FILES IT SUPERSEDED.** To answer *"what is open"* you must read three files and know which wins. ⛔ **No amount of appending fixes that — it is why the register is not trusted.**
⛔ **THE NEW REGISTER MUST REVERSE IT EXPLICITLY: `MASTER_REGISTER.md` WINS over all four.** ⭐ The *"THIS FILE WINS"* sentence created the chain and ⛔ must not survive into the new one.

## 🧮 §3 · THE `G5/G6/G16` DISCREPANCY — CARRY IT, ⛔ DO NOT SILENTLY FIX IT
**(P) the 30-Jul file RECORDS IT AGAINST ITSELF at `:11`:** *"§3.7's sweep closes **G5 · G6 · G16** with evidence, but §6's `K` list does not deduct them — so the carried figure **M=131 still contains those 3**."*
⭐ **Its OWN sweep reconciliation is internally consistent** *(`N=38 = C4 + M1 + P20 + D10 + ✅2 + 🟪1`, where `C` IS `G5·G6·G16·R0`)* — **the break is between that sweep and the carried `M=131` inherited from the 28-Jul edition** (whose own reconciliation is `N=420 = M118 + K91 + J211`).
⇒ 🔑 **SHOW BOTH: `M=131` as carried, and `M=128` after deducting the three. ⛔ Print the working; do not present the corrected number alone.**

## 📏 §4 · SCALE — MEASURED, and it decides the batching
| source | bytes | lines | sections | distinct IDs | table rows |
|---|---|---|---|---|---|
| 28-Jul | 55,730 | 743 | – | 67 | 0 |
| 30-Jul | 50,818 | 723 | 32 | 65 | 110 |
| **01-Aug (working)** | **405,802** | **2,667** | **113** | **129** | **334** |
| 04-Jul audit | 38,805 | 274 | 26 | 16 | – |

⇒ **~551 KB, 4,407 lines, 113 sections in the working register alone, and its rows run to ~8,000 CHARACTERS each.** ⛔ **PHASE 1 IS NOT ONE SESSION.** ⭐ Plan: **batch by SOURCE then by SECTION**, report after each batch, and carry a running dedup key.

## 🔨 §4b · PHASE 1 — BATCH 1 DONE 10-Aug. ⛔ THE REGISTER IS PARTIAL AND SAYS SO.
**✅ `docs/MASTER_REGISTER.md` CREATED (258 lines, UNDATED).** ⚠️ **UNTRACKED — where it gets COMMITTED is a decision: ⛔ do NOT let it land silently on `feat/delivery-config-split`, a docs-only branch that is NOT in the install order** *(that is the naming trap one more time)*.
- ✅ **MERGED: source ① `MASTER_PENDING_28-Jul-2026.txt` IN FULL + the 31 current 10-Aug items.**
- ⛔ **NOT STARTED: ② 30-Jul · ③ 01-Aug · ④ 04-Jul audit.** The file's own header states this in a table — ⭐ **a partial register that does not announce itself as partial is the whole problem returning under a new filename.**
- 🔑 **THE PRECEDENCE IS REVERSED IN THE FILE: `THIS FILE WINS`, forwards.** ⛔ And it states that until batches 2-4 land, the four sources remain authoritative for anything NOT listed.
- 📏 **ARITHMETIC: 63 top-level (28-Jul) + 15 `X` + 55 sub-items = 133 · +31 current = **164**.** ⚠️ **`0` duplicates merged, and that is NOT a clean-reconciliation signal — dedup happens ACROSS editions and only one is merged. The dedup work BEGINS in batch 2.**
- ⛔ **Status is ONLY `CLOSED-WITH-EVIDENCE` or `UNVERIFIED`; nothing was checked against code.** ⛔ **No `HISTORICAL` header added to any source** — that waits for Phase 2. ✅ **All four sources UNTOUCHED** *(⚠️ `01-Aug` shows ` M` in git — that predates this session, `167+/7−`, ⛔ not the rebuild)*.

## 🟢 §4d · COMMITTED ON `main`, AND BATCH 2 IS IN
✅ **`b9bf6fa` (batch 1) + `6e274ca` (batch 2) on `main` — ⭐ the RIGHT branch: `main` is install ④, the base six branches fork from, and DOCS-ONLY so it cannot touch F6's payload.** **(P) `git diff --name-only f963438..HEAD -- '*.py' '*.yaml' '*.sql' '*.sh'` is EMPTY; F6's code SHA stays `9fdfe41`.** ⛔ **Quote `9fdfe41` for BEHAVIOUR and the tip for PUSHING** — the same split used for Fix 2. 🗑️ The stray untracked copy in the `feat/delivery-config-split` worktree was md5-verified against the committed blob, then removed.
- 📏 **BATCH 2 (`30-Jul`, read at `main` HEAD `f963438`, clean): 30 new rows · 118 duplicate appearances merged · running total 164 → **194**.** ⭐ **The dedup count moved `0 → 118`, the expected consequence of 30-Jul being a DELTA on 28-Jul, ⛔ not a success measure.**
- ⛔ **BATCHES 3 (`01-Aug`, the big one) and 4 (`04-Jul audit`) NOT STARTED.**

## 🔴 §4i · CORRECTED 11-Aug — THE AT-RISK PASS IS **27 ROWS, NOT ELEVEN**
**(P) `HEAD` = `N9-01`…`N9-11` and **ZERO** `N10-`; the WORKING TREE = `N9-01`…`N9-27` **AND** `N10-01`…`N10-11`.** ⇒ the uncommitted pass is the SOLE source of **`N9-12`…`N9-27` (16) + `N10-*` (11) = 27 rows.** ✅ The 10-Aug read-only copy captured the WHOLE FILE, so the preservation stands — ⛔ **but `A10-32` is blocked against 27 rows, not 11.**

## 🔎 §4j · PRESENCE CHECK, 11-Aug — SIX CONVERSATION-BORNE THREADS. ⭐ NONE IS `NOWHERE`.
**Answered `IN §H` / `EXPECTED IN BATCH 3` / `NOWHERE` with evidence; ⛔ NO rows added** *(batch 3 carries them with their original IDs; pre-adding would create the duplicate this rebuild removes)*.
- 🔴 **THREE OF THE SIX LIVE ONLY IN THE UNCOMMITTED PASS, ⛔ NOT IN `HEAD`:** the **`sync_from_broker` SECOND FIRING SITE** *(rebases `_total`, ⛔ not the reservations ⇒ can kill a RUNNING session at 09:15 — ⛔ NOT `A10-30`, which is the boot path)* · **the cron chain running while the service was DEAD** · **the whole ALERT-REMEDIATION thread (`N9-14`, 14 swallowed paths, 5 limiters)**.
- ✅ In `HEAD`: **`N9-07`** · the **two remaining `abs()`** sites · **`instruments.csv` gitignored**.
- ⭐⭐ **THE CHECK PAID FOR ITSELF A SECOND WAY: it did not find a LOST item — it found that THREE KNOWN items were sitting in the AT-RISK file.**
✅ **Also fixed (`b7a6cd1`): `A10-31` reordered back into sequence** *(an ID out of order reads as missing rows)* **and `A10-10` now NAMES all ten unpushed refs** — ⛔ **the count has been wrong three times (8·9·10), and a count without names cannot be checked by anyone.**

## 🔒 §4h · THE ELEVEN ROWS ARE PRESERVED — 10-Aug, ⛔ BY FILE COPY, ⛔ NO GIT OPERATION
✅ **`sha256 4e132b3a3085be3f20f069e65829d87bf3b5bda74b1dfa6a9f185d42be6646f6` · `405,802` bytes · source and copy VERIFIED IDENTICAL · read-only (`444`) · all 11 `N10-*` present in the copy.**
📁 `…\scratchpad\PRESERVED_10Aug2026\MASTER_PENDING_01-Aug-2026.WORKING-TREE.md` + `MANIFEST.txt`.
⛔ **NOT committed, NOT stashed, branch UNTOUCHED** — ⭐ the copy removes the DESTRUCTION risk **without changing what `HEAD` means for a source mid-rebuild.**
⚠️ **INSURANCE, ⛔ NOT THE MERGE: it does NOT unblock `A10-32`.** That unblocks only once `N10-01`…`N10-11` are **merged into the register by batch 3**.
⚠️ **CAVEAT STATED: the path is under `AppData\Local\Temp`, subject to OS/tool cleanup ⇒ adequate SAME-WEEK insurance, ⛔ NOT a durable archive.** ⭐ Durable preservation means committing the pass on its own branch — ⛔ deliberately not taken.

## 💥 §4g · FINDING 6 — SOURCE ③ HAS **TWO REVISIONS**, AND ONE OF THEM IS UNCOMMITTED AND UNIQUE
🔴🔴 **`docs/MASTER_PENDING_01-Aug-2026.md` in the ROOT worktree carries an UNCOMMITTED 167-line *"10-AUG-2026 REGISTER PASS"*. (P) ITS ROWS `N10-01`…`N10-11` EXIST NOWHERE ELSE — `HEAD` has **ZERO** `N10-` references and holds only `N9-01`…`N9-11`.**
⇒ ⛔⛔ **A BRANCH SWITCH OR `checkout -f` WOULD DESTROY ELEVEN REGISTER ROWS** and an N-arithmetic (`260 → 271`, and `271 → 277` if the six candidates are admitted) present in no other file.
⇒ 🔑 **BATCH 3 MUST READ `HEAD` *AND* THE UNCOMMITTED PASS, and say which line came from which.** ⭐ Batch 1 already captured the pass's **SUBSTANCE** as `A10-01`…`A10-31`; ⛔ what it does NOT carry is its **ROW IDENTITY** (`N10-*`) and its arithmetic.
⚠️ **THIS GATES `A10-32` (*"return the root worktree to `main`"*) — ⛔ that must NOT happen until the pass is preserved.** ⭐ The root being parked on `feat/delivery-config-split` has now produced **FOUR** problems: the sizing tests reading a different config · the CRLF conversions · *"the tree is dirty"* at every gate · and the register landing where Rama does not look.
✅ **LOCATION RECORDED (`c05efe8`): the register is on `main`; read it at `D:\Projects\trading-system-main\docs\MASTER_REGISTER.md` until the root returns to `main`.** ⛔ **NEVER a second copy — two copies of a register IS the defect.**

## 🔴 §4e · FINDING 4 — AN ID COLLISION ACROSS SOURCES. ⭐ THE SHARPEST RESULT OF BATCH 2.
⛔⛔ **`Q4` AND `Q6` MEAN TWO DIFFERENT THINGS: 28-Jul `§3`'s are DEPLOY-QUEUE BRANCHES (`249317d`, `fix-symdir-27jul`); 30-Jul `§3.3`'s are QUESTIONS in `q4_hard_kill_delivery_decision_30jul2026.md`.** ⭐⭐ **This is the dedup hazard IN REVERSE — *"deduplicate by identity, never by wording"* ALSO MEANS ⛔ NEVER MERGE ON AN ID ALONE.** ✅ Re-IDed **`QD-*`** with the originals preserved in the statement text.

## 🔴 §4f · FINDING 5 — MY 30 ROWS ≠ THE SOURCE'S "24 ARISING", ⛔ AND IT WAS NOT FORCED
**2 of the source's 24 are STATUS UPDATES here, ⛔ not rows** *(they are new FACTS about existing items)*; and **my granularity is FINER in `§4.3`/`§3.3` — ⭐ because a BUNDLE IS EXACTLY WHAT HIDES AN ITEM.** ⛔ **Neither number was adjusted to agree; both are stated.**

## 🔴 §4c · FINDING 1 — THE 28-Jul FILE'S OWN *"EXACT"* `M=118` OMITS ITS ENTIRE §6
**(P) its enumeration is `§2 (13) + §3 (6) + §4 (25) + §5 (11) + §7 (7) + §8 (1)` = 63 top-level + 55 sub-items = 118 — and `§6 X1-X15` appears in NEITHER `M` NOR `K`,** although the file's own banner lists `X1-X15` among its contents. ⇒ **TRUE CARRY = 133.** ⭐ The file called `M=118` *"EXACT"*; it is exact only for what it enumerated. ⛔ Recorded, ⛔ not corrected in the source.
⚠️ **AND A THIRD FIGURE IS NOW VISIBLE: 30-Jul carries `M=131`, which reconciles to NEITHER `118` NOR `133`.** ⛔ Left visible; ⛔ not reconciled in Phase 1.

## ⏰ §5 · WHY PHASE 1 DID NOT START ON 10-Aug — ⛔ SUPERSEDED, RAMA OVERRULED
⛔ **The card's own §6 + DATE-OF-WORK header bar it before the 11-Aug 08:15 prediction scoring**, and ⭐ **the campaign's own record says large careful work begun at the end of a long session is *"exactly the rushed work every rule this week exists to prevent"*.** ⇒ **Phase 1 opens in the 11-Aug DAYTIME gap** *(after scoring, before Fix 1's evening install)*. ⛔ **Never on an install evening.**

## ⛔ §6 · BINDING ON PHASE 1
⛔ **CREATE ONE NEW FILE `docs/MASTER_REGISTER.md` — UNDATED by design. ⛔ Do NOT edit the four sources; ⛔ delete nothing.**
⛔ **STATUS IN PHASE 1 IS ONLY `CLOSED-WITH-EVIDENCE` or `UNVERIFIED`** — ⭐ **a status inherited from a file is NOT a measurement**, and inheriting them is how the old register became untrustworthy. ⛔ **Including items the sources call done.**
⛔ **Dedup BY IDENTITY, never by similar wording; two rows = one row listing BOTH IDs; unsure ⇒ keep both, mark `POSSIBLE DUPLICATE`.**
⚠️ **A total that reconciles CLEANLY is this campaign's strongest false-confidence signal — show the working, and if it does NOT reconcile, LEAVE THAT VISIBLE.** [[feedback-verify-rc-not-output]]
🔑 **Phase 2 (verify) is SEPARATE SESSIONS, in batches: `COMPLETE`/`PARTIAL`/`OPEN` + `CANNOT DETERMINE`; code beats source and the disagreement is a FINDING; and every row separates `BUILT` from `DEPLOYED` — ⭐ TEN refs are unpushed right now.** [[install-collision-map-10aug]] [[feedback-status-label-rule-27jul]]

---

## 🏁 §7 · PHASE 1 COMPLETE — 11-Aug-2026, commit `1bde728` on `main`
✅ **ALL FOUR SOURCES MERGED.** Batch 3 read **BOTH revisions** of source ③ (`HEAD` + the preserved copy). Batch 4 = **0 new rows / 41 merged** — ⭐ correct, ⛔ not a miss: `G20` holds them **by pointer** by explicit design, and re-enumerating would FORK the register.
📏 **GRAND TOTAL 333 rows · 291 merged.** ⛔ **IT DOES NOT FULLY RECONCILE AND `§L` SAYS WHERE:** `§B`'s 95 live in `integrity_audit_2026.md` (⛔ outside the four sources) and are merged as a BAND · the 27 pass rows are merged as FAMILIES with their unique members named, ⛔ not as 27 written rows · `§C.10` says 8 operator items where this holds 9 · **five `M` figures (118·128·131·132·133) describe overlapping populations and ⛔ NONE IS CHOSEN.**
## 🔴 **FINDING 7 — THE FIFTEEN `X` ITEMS FELL OUT OF THE CHAIN AND NEVER RE-ENTERED.** Source ③'s `A=132` inherits S2's `131` ← S1's `118`, **and `118` omits `X1`…`X15`.** (P) source ③ carries **NO** `X` family — `X7` = **ZERO** hits. ⭐⭐ **They survive ONLY because batch 1 RE-DERIVED the count instead of reading the total.**
✅ **The `THIS FILE WINS` backward-pointer is DELETED; all four sources carry a `HISTORICAL — SUPERSEDED` header, PREPENDED ONLY — (P) 4/7/4/4 insertions, ZERO deletions.** ⛔ **The preserved copy was NOT edited — its `sha256` IS the record** *(re-verified `4e132b3a…` after the batch)*.
🔓 **`A10-32` REDUCED, ⛔ NOT DISCHARGED** — content represented + full text preserved ⇒ a switch no longer destroys unrecoverable information, ⛔ but the 27 are not individually written. **Rama's call; worktree NOT switched.**
🔴🔴 **`§M` RECORDS WHAT IS STILL OWED: the 08:15 BOOT IS *NOT OBSERVED* AND BOTH FROZEN PREDICTIONS ARE *NOT SCORED* — `CANNOT DETERMINE` from the PC (it needs the VM, and VM commands are prohibited).** ⛔ **NOT "passed". They outrank everything and the observation CANNOT BE RE-RUN.**
