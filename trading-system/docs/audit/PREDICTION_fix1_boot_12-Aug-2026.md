# 🔮 FROZEN PREDICTION — THE 12-Aug-2026 08:15 BOOT, AFTER FIX 1 `2e1f109`

> ## ⛔⛔ **FROZEN AT 11-Aug-2026 16:05 IST, BEFORE ANY PUSH. ⛔ NO EDIT ABOVE THE ADDENDA LINE, FOR ANY REASON — ⭐ ESPECIALLY IF IT IS WRONG. A wrong call is the RESULT, ⛔ not a problem.**

**Written before Gate D. ⛔ If the install does not happen tonight, this prediction is `NOT TESTED` and is re-used unchanged on whatever night Fix 1 actually installs — ⛔ it is NOT rewritten for a new date.**

🧪 **PARITY — the change is in `capital/fund_manager.py`, which BOTH books share.** ⛔ No paper rehearsal is claimed: `trades` holds **573 rows, all `mode=LIVE`, zero paper rows** (measured 11-Aug 15:50), so no paper analogue exists to run. [[paper-cannot-exercise-class-26jul]]

---

## ① 🔑 THE BRANCH — **NO-CARRY. THIS IS THE WHOLE POINT OF THE PREDICTION.**

**(P) MEASURED 11-Aug 15:25:52 IST, after market close:** `trades` rows with status in
`OPEN`/`EXITING`/`PARTIAL`/`PENDING_FILL`, **across ALL dates = ZERO. THE BOOK IS FLAT.**
**(P) Both delivery entries today FAILED at `qty_filled = 0`** — FUSION `positional_swing_long`
10:02:16 and ROLEXRINGS `positional_sector_rotation` 10:11:15, the 60 s LIMIT self-cancels.
**(P) Today's only fills were 3 MIS rows / 4 shares, all closed intraday.**

> ## ⛔⛔ **THEREFORE, STATED PLAINLY AND IN ADVANCE:**
> ## **"Fix 1's changed carried-position rehydration path will NOT execute at the 12-Aug 08:15 boot. That boot is therefore NOT evidence that the changed carry path works."**

⭐ **This is a CORRECT and VALUABLE prediction, ⛔ not a failed deployment.** What tomorrow CAN
establish is that Fix 1 is **INERT-SAFE on a flat book** — that it changes nothing when there is
no carry. ⛔ **It cannot establish that the carry arithmetic is right.** That requires a boot with
a real carried CNC position, and **the next such boot is unscheduled.**

🔑 **THE TRAP THIS PREDICTION EXISTS TO PREVENT: a clean boot tomorrow morning will be tempting to
read as *"Fix 1 works."* ⛔ IT IS NOT THAT. It is *"Fix 1 did not break the ordinary path."***

---

## ② THE CAPITAL ARITHMETIC — EVERY OPERAND SHOWN

**(P) MEASURED CLOSING STATE, 11-Aug 16:01:26 IST:**

| term | value | source |
|---|---|---|
| today's `fm_ledger` INIT | **`₹10,645.60`** | `08:16:05.618629` |
| today's realised P&L | **`−₹25.45`** | 3 closed trades, `net_pnl` sum |
| intraday bucket, last write | **`₹7,426.47`** | `RELEASE_USED 11:11:44.864` |
| positional bucket, last write | **`₹3,193.68`** | `RELEASE 10:13:22.528` |
| `RESET_PNL` | `0.0` | `15:17:02.939` |
| carried positions | **ZERO** | measured 15:25:52 |

**THE PREDICTION, derived — ⛔ not recalled:**

```
tomorrow INIT  ≈ 10,645.60 − 25.45  =  ₹10,620.15        ← CENTRAL ESTIMATE
replay (carry) =  ₹0.00                                   ← THE LOAD-BEARING TERM
positional_avail = 0.30 × INIT − 0.00  ≈  ₹3,186.05
intraday_avail   = 0.70 × INIT         ≈  ₹7,434.11
INV6 margin      = positional_avail − replay ≈ +₹3,186.05
```

> ## 🔑 **THE CALL: `replay = ₹0.00` EXACTLY, and `positional_avail` = `0.30 × INIT` with NOTHING SUBTRACTED.**
> Contrast today, where the replay was **`446.106 + 460.91632 = ₹907.0223`** and `positional_avail`
> came out `3,193.68 − 907.02 = ₹2,286.66`. **Tomorrow that subtraction term must be ABSENT.**

⚠️ **BRACKET ON `INIT`, stated rather than hidden — ⛔ I am NOT claiming ₹10,620.15 to the paisa.**
**`₹10,590 – ₹10,680`.** The uncertainty is broker settlement, ⛔ not arithmetic: DIFFNKG (sold
07-Aug) and MANINFRA (sold 10-Aug) sale proceeds credit on their own T+1 schedules, and today's
MIS losses debit on theirs. ⭐ **If INIT lands outside that bracket, the BRACKET is wrong — ⛔ that
does NOT falsify the `replay = 0` call, which is the real prediction. Score them separately.**

---

## ③ FALSIFIERS — ⛔ SCORE BY SIGNATURE, ⛔ NEVER BY NARRATIVE

| # | call | CONFIRMED by | REFUTED by |
|---|---|---|---|
| **F1** | the boot survives | service `active`/`running`; no `HARD_KILL` written 12-Aug | any `HARD_KILL` with `capital_invariant_violated` dated 12-Aug |
| **F2** | **`replay = ₹0.00`** | `fm_ledger` 12-Aug has **NO `RELEASE_USED` rows at boot**, and `fund_manager.initialize` shows `positional_avail = 0.30 × total` **exactly** | any boot-time `RELEASE_USED`, or `positional_avail < 0.30 × total` |
| **F3** | **the changed carry path does NOT execute** | zero carried-position rehydration entries in the 12-Aug log | any carry-rehydrate log line naming a symbol |
| **F4** | prior-day `SOFT_KILL` auto-clears | *"Kill switch auto-cleared: prior … reason=circuit_breaker_force_close_15:15 … new day 2026-08-12 starts clean"* | kill still active after 08:15:5x |
| **F5** | INIT in bracket | `08:16:0x` INIT within **`₹10,590 – ₹10,680`** | outside it — ⭐ **scores F5 ONLY, ⛔ not F2** |
| **F6** | `cnc_gtt_monitor` finds nothing to do | no `gtt_exit`, no `_recreate`, no `_queue_preopen` for any symbol | any GTT action at the 12-Aug boot |

**(P) KILL STATE AT FREEZE: `SOFT_KILL`, reason `circuit_breaker_force_close_15:15`, triggered
`2026-08-11T15:15:01.737731`, by `order_monitor`.** ⭐ This is the ROUTINE 15:15 kill — the FIRST
literal in `SCHEDULED_KILL_REASONS` (`capital/kill_switch.py:121-124`) — and `clear_stale_state`
auto-clears it at the next 08:15 boot. ⛔ **EXPECTED. ⛔ NOT an incident. ⛔ Do NOT run
`deploy/resume.sh` for it** — and ⭐ **expect tonight's 18:45 EOD SUMMARY to contradict its own
READINESS block about exactly this, which is register row `N11-01` scoring itself.**

---

## ④ 🚦 OUTCOMES DECLARED AVAILABLE UP FRONT

- **`NOT TESTED`** — ⭐ **the single most likely non-result**, and it applies if the install does
  not happen tonight (any Gate A–C red, or authorisation withheld). ⛔ Then NOTHING here is scored
  and this file is re-used unchanged.
- **`CANNOT DETERMINE`** — if the 12-Aug boot is disturbed by anything not in this file.
- ⛔ **A HARD_KILL for an unrelated reason makes every row `NOT TESTED`, ⛔ never "wrong"** —
  exactly as 10-Aug scored.

## ⑤ ⛔ WHAT THIS PREDICTION DOES **NOT** CLAIM

⛔ It does **not** claim Fix 1 is correct. ⛔ It does **not** claim the carry double-count is
resolved. ⛔ It does **not** licence `VERIFIED LIVE` — ⭐ that label needs a boot with a **real
carried CNC position**, and no such boot is scheduled. **Tomorrow's best possible outcome is
`DEPLOYED` + `inert-safe on a flat book`, and that is the ceiling.**

---
<!-- ═══════════════ ADDENDA BELOW THIS LINE ONLY ═══════════════ -->

## ADDENDUM 1 — **F7: THE POSITIVE SIGNATURE.** Added 11-Aug-2026 **19:06 IST (measured)**, ⛔ BEFORE the push (D1), ⛔ before any result exists.

📜 **AUTHORISED BY RAMA, 11-Aug-2026 evening, VERBATIM:** *"Add the addendum BEFORE D1, not after. All six
falsifiers are absence-signatures, so 'deployed and inert' and 'never deployed' currently score identically —
the broker_cash/carry log keys are the only presence signature in the change, and without them tomorrow is
unscoreable. D2's md5 proves the file reached the VM; the log keys prove the running process loaded it. Both
go in the record."*

### 🔑 THE DEFECT IN F1–F6, STATED PLAINLY

**Every one of F1–F6 is an ABSENCE signature** — no HARD_KILL, no `RELEASE_USED`, no carry-rehydrate line, no
GTT action, kill auto-cleared, INIT in bracket. ⛔ **A boot on a build where Fix 1 was NEVER DEPLOYED would
satisfy all six identically.** On a flat book the fix is arithmetically inert (`carry = 0` ⇒ `_bucket_base`
returns `total × pct`, the previous expression unchanged), so **F1–F6 cannot distinguish `DEPLOYED + inert`
from `NOT DEPLOYED AT ALL`.** Without a presence test, 12-Aug is **unscoreable** on the only question the
install asks.

### F7 — THE CALL

> ## **`fund_manager.sync_from_broker` will log the keys `broker_cash` AND `carry` on 12-Aug.**

**(P) CODE-MEASURED at `2e1f109`, 11-Aug 18:0x IST** — `capital/fund_manager.py`, the `sync_from_broker`
log call. At `645728d` it is `extra={"old_total", "new_total"}`; at `2e1f109` it is
`extra={"old_total", "new_total", "broker_cash", "carry"}`. ⭐ **The call site is UNCONDITIONAL — it does not
sit behind any carry test**, so it fires on a flat book exactly as on a carried one. ⛔ This is the ONLY
new observable in the change that does not require a carried position.

| | CONFIRMED by | REFUTED by |
|---|---|---|
| **F7** | a 12-Aug `fund_manager.sync_from_broker` line carrying **both** `broker_cash` and `carry` | the same line carrying only `old_total`/`new_total` ⇒ **the running process is NOT the new code** |

⚠️ **`NOT TESTED` if `sync_from_broker` never fires on 12-Aug** (e.g. the boot dies first, or the 09:15 FM9
sync does not run). ⛔ Absence of the LINE is `NOT TESTED`; presence of the line WITHOUT the keys is `REFUTED`.
⭐ **Score those two apart.**

### 🧾 THE TWO PROOFS ARE DIFFERENT CLAIMS — ⛔ NEVER COLLAPSE THEM

| proof | what it establishes | what it CANNOT establish |
|---|---|---|
| **D2 md5 (tonight)** | the FILE reached the VM's disk, byte-identical | ⛔ that any process ever loaded it |
| **F7 log keys (12-Aug)** | the RUNNING PROCESS loaded the new code | ⛔ that the carry arithmetic is correct |

⛔ **NEITHER licenses `VERIFIED LIVE`.** F7 confirming raises 12-Aug's ceiling from *"nothing broke"* to
**`DEPLOYED` + `inert-safe on a flat book`, PROVEN LIVE-LOADED** — ⭐ and that remains the ceiling, because the
carry path still does not execute on a flat book (F3). **`VERIFIED LIVE` still requires a boot with a real
carried CNC position, and no such boot is scheduled.**

⛔ **NOTHING ABOVE THE ADDENDA LINE HAS BEEN EDITED.** F1–F6 and the ₹10,590–₹10,680 bracket stand exactly as
frozen at 16:04:42.

---

## ADDENDUM 2 — **THE SCORE.** Written 12-Aug-2026 after the boot. ⛔ NOTHING ABOVE THE ADDENDA LINE TOUCHED.

**(P) ALL FIGURES MEASURED 12-Aug-2026 IST, source named per row. Base for every ₹ figure = today's `fm_ledger` INIT `₹10,620.60`.**

### 🚦 RESULT — ⛔ SCORED SEPARATELY, ⛔ NOT COLLAPSED

| # | call | verdict | the SIGNATURE that decided it |
|---|---|---|---|
| **F1** | boot survives | ✅ **CONFIRMED** | `ActiveEnterTimestamp Wed 2026-08-12 08:15:19 IST`, `MainPID 3437568`, `NRestarts=0`, `active`/`running`. `HARD_KILL` count **0** — width: whole `logs/system_2026-08-12.log`, case-insensitive |
| **F2** | **`replay = ₹0.00`** | ✅ **CONFIRMED** | `fund_manager.initialize` @ `08:15:27.721`: `total 10620.60` · `positional_avail 3186.18` · `intraday_avail 7434.42`. **`0.30 × 10,620.60 = 3,186.18` and `0.70 × 10,620.60 = 7,434.42` — EXACT, to the paisa, nothing subtracted.** `RELEASE_USED` rows dated 12-Aug = **0**. ⭐ Contrast 11-Aug: `3,193.68 − 907.02 = 2,286.66` |
| **F3** | carry path does NOT execute | ✅ **CONFIRMED** | `rehydrate_carry` count **0**, whole log. ⭐ **AND NOT VACUOUSLY:** `fund_manager.rehydrated` + `fund_manager.rehydrate_complete` BOTH fired ⇒ the rehydrate path RAN; only the `if self._positional_carry:` branch (`fund_manager.py:1838`) did not. ⭐ Corroborated from the other side by F7's `"carry":0.0` |
| **F4** | prior-day `SOFT_KILL` auto-clears | ✅ **CONFIRMED** | verbatim @ `08:15:19.840`: *"Kill switch auto-cleared: prior SOFT_KILL from 2026-08-11 (reason=circuit_breaker_force_close_15:15 by=order_monitor) -- new day 2026-08-12 starts clean (HEADLESS); audited to system_events"*. `kill_switch_state` now `INACTIVE` by `main.auto_clear_stale` @ `08:15:19.836875` |
| **F5** | INIT in bracket | ✅ **CONFIRMED** | INIT **`₹10,620.60`** @ `2026-08-12T08:15:27.718977+05:30` — inside `₹10,590 – ₹10,680`. ⭐ `+₹0.45` from the `₹10,620.15` central estimate. ⛔ The bracket was scored, ⛔ not the paisa |
| **F6** | `cnc_gtt_monitor` idle | ✅ **CONFIRMED** | `gtt_exit` / `_recreate` / `queued_preopen` all **0**, whole log; `gtt_state` ACTIVE = **0**. ⭐ **AND IT WAS REACHED, ⛔ not skipped: `cnc_gtt.hydrated` is present in the boot sequence** — the distinction that mattered on 10-Aug, when the HARD_KILL preceded the monitor by ~60 s |
| **F7** | **the RUNNING PROCESS loaded Fix 1** | ✅ **CONFIRMED** | `09:15:00.052` — `{"msg":"fund_manager.sync_from_broker","broker_cash":10620.6,"carry":0.0,"new_total":10620.6,"old_total":10620.6}`. **BOTH new keys present.** At `645728d` this line carries only `old_total`/`new_total` |

### 🔑 F7 — THE WINDOW, AND A FACT THE PREDICTION DID NOT KNOW

**(P) WINDOW = THE 09:15 FM9 SYNC. ⛔ NOT THE BOOT — and the boot was never a candidate.**
**(P) `sync_from_broker` has EXACTLY ONE invocation in the whole deployed tree: `main.py:1012`, inside
`market_open_margin_sync` (FIX-164).** Width: `grep -rn "\.sync_from_broker(" --include=*.py .`, whole tree,
tests excluded, **untruncated** *(a first pass through `head` returned exactly 10 lines and was DISCARDED as
truncated, ⛔ not read as evidence)*. ⇒ ⭐ **the 08:15 absence was STRUCTURAL, ⛔ not a pending result.**
📌 **This SHARPENS ADDENDUM 1's *"fires ~09:15"* into a measured single-window fact**, and it means the
frozen instruction *"check BOTH windows before declaring NOT TESTED"* could only ever have resolved at 09:15.
✅ Not gated on the balance moving: the call is unconditional once the wait elapses (`main.py:1005-1012`), and
the log call at `fund_manager.py:1469-1472` is reached by straight-line code with no early return.
✅ **Silence ≠ crash was tested for, not assumed:** the capture also grepped `market_open_margin_sync`, which
returned the SUCCESS line (`delta 0.0`, `old 10620.6`, `new 10620.6`), ⛔ not `failed` and ⛔ not `skipping`.

### 🧾 THE LADDER — WHERE TODAY LEFT IT

| rung | claim | state after 12-Aug |
|---|---|---|
| ① | the FILE is on the VM | ✅ **DONE** — `capital/fund_manager.py` `md5 9ff45f6664fdfef330a0bf1dd66f2a53`, re-verified pre-boot 07:5x, byte-identical to Fix 1 |
| ② | the RUNNING PROCESS loaded it | ✅ **PROVEN TODAY — F7, `09:15:00.052`** |
| ③ | the carry ARITHMETIC is correct | ⛔ **NOT ESTABLISHED. Needs a boot with a real carried CNC position; none is scheduled.** |

> ## 🏷️ **STATUS = `DEPLOYED` + `INERT-SAFE ON A FLAT BOOK, PROVEN LIVE-LOADED`.**
> ## ⛔⛔ **NOT `VERIFIED LIVE`. ⛔ NOT "Fix 1 works." ⛔ NOT on any argument available today.**

🔑 **THE CEILING HELD, AND THE TRAP WAS REAL.** F1–F6 are all ABSENCE signatures, and the deployed code makes
`new_total = broker_balance + carry_total` with `carry_total = 0.0` on a flat book ⇒ **arithmetically the
pre-Fix-1 expression, unchanged.** F7's own payload proves it: `"carry":0.0`, `old_total == new_total ==
broker_cash == 10620.6`. ⇒ ⛔ **F1–F6 would look EXACTLY like this on a build where Fix 1 had never been
deployed.** ⭐ **F7 is the ONLY row that discriminated, exactly as ADDENDUM 1 said it would — and the
addendum was written 29 seconds before the push, before any result existed.**

⚠️ **WHAT TODAY DID NOT TEST, ⛔ and must not be demoted because the boot was clean:** the carry arithmetic ·
`_bucket_base` under a non-zero carry · the double-count that Fix 1 exists to prevent · the intraday-bucket
sweep (LATENT) · anything requiring a carried CNC position.

### 📎 FREE MEASUREMENT — FILED, ⛔ NOT CHASED

**(P) The boot emitted TWO CONTRADICTORY `startup_scenario` lines 15 ms apart:**
`08:15:19.841` `startup_scenario=COLD: new day (prev=2026-08-11, today=2026-08-12)` and
`08:15:19.856` `startup_scenario=CRASH: same day, no SHUTDOWN event found`.
⭐ A RECURRENCE of the filed 06-Aug mislabel — now with **both labels in one boot, after a DELIBERATE stop**.
⛔ Not chased. ⛔ Whether `CRASH` alters boot recovery remains UNVERIFIED, exactly as filed.

**⛔ NOTHING ABOVE THE ADDENDA LINE HAS BEEN EDITED — appended only; frozen region lines 1-103 re-verified
`md5 bb72f04abc763f1c4e9377fe97ad9576` after this write.**

---

## ADDENDUM 3 — **RAMA'S CORRECTION TO THE *"ALL ABSENCE SIGNATURES"* SHORTHAND.** Added 12-Aug-2026 after the score. ⛔ NOTHING ABOVE THE ADDENDA LINE TOUCHED. ⛔ ADDENDUM 1 AND 2 LEFT INTACT — this SUPERSEDES their wording, it does ⛔ NOT delete it.

📜 **RAMA, 12-Aug-2026, VERBATIM:** *"My 'every one of F1–F6 is an absence signature' was too broad and you should not carry it forward — F1 is survival, F4 is a presence event, F5 is a numeric range. The precise version: F1–F6 individually cannot prove the changed carry arithmetic executed, because on a flat book their values are identical to the pre-Fix-1 path; F7 is the deliberate presence signature."*

### ⛔ THE SHORTHAND WAS WRONG, AND IT WAS WRONG IN **BOTH** DIRECTIONS OF USE

**(P) IT IS FALSE AS A DESCRIPTION OF THE ROWS** — three of the six are ⛔ not absences at all:

| # | what it actually is | measured today |
|---|---|---|
| **F1** | **SURVIVAL** — a compound: a PRESENCE (`active`/`running`, `MainPID 3437568`) *and* an absence (`HARD_KILL` count 0) | `08:15:19` |
| **F4** | **A PRESENCE EVENT** — a log line that must EXIST and match text | *"Kill switch auto-cleared… starts clean (HEADLESS)"* @ `08:15:19.840` |
| **F5** | **A NUMERIC RANGE** — a value inside a bracket, ⛔ not the absence of anything | INIT `₹10,620.60` ∈ `₹10,590–₹10,680` |
| F2 · F3 · F6 | genuinely absence-shaped | `RELEASE_USED` 0 · `rehydrate_carry` 0 · `gtt_exit`/`_recreate`/`queued_preopen` 0 |

### ✅ THE PRECISE FORMULATION — ⭐ USE THIS ONE, ⛔ RETIRE THE SHORTHAND

> ## **`F1`–`F6` INDIVIDUALLY CANNOT PROVE THE CHANGED CARRY ARITHMETIC EXECUTED — because ON A FLAT BOOK THEIR VALUES ARE IDENTICAL TO THE PRE-FIX-1 PATH. `F7` IS THE DELIBERATE PRESENCE SIGNATURE.**

🔑 **WHY THE CORRECTION MATTERS AND IS NOT PEDANTRY:** the shorthand located the defect in the **SHAPE** of the rows (*"they are absences"*), which is false and would wrongly imply that ADDING a presence-shaped row fixes it — ⛔ **`F4` and `F5` ARE presence/value-shaped and they still cannot discriminate.** The real property is **INVARIANCE UNDER THE CHANGE ON A FLAT BOOK**: `carry_total = 0.0` ⇒ `new_total = broker_balance + 0.0` and `_bucket_base` returns `total × pct` ⇒ **every one of the six takes the SAME value on Fix-1 code and on pre-Fix-1 code.** ⭐ **What made `F7` work was ⛔ not that it is a presence — it is that it observes a term (`carry`) that EXISTS ONLY IN THE NEW CODE.**

**(P) CONFIRMED BY `F7`'s OWN PAYLOAD, `09:15:00.052`:** `broker_cash:10620.6` · `carry:0.0` · `old_total:10620.6` · `new_total:10620.6` — ⭐ **the VALUES are pre-Fix-1-identical; only the KEYS are new.** ⇒ **the discriminator was the key set, ⛔ never the value.**

⚠️ **CARRIED-FORWARD WORDING CORRECTED IN THE LIVING RECORDS TOO** (deploy ledger top block, `SYSTEM_MAP` banner) — ⛔ the shorthand is not left standing where it is read first. ⛔ **`ADDENDUM 1`'s and `ADDENDUM 2`'s text is UNCHANGED and UNDELETED; this addendum governs.**

### 📎 SECOND CORRECTION, SAME DAY — **§6's MERGE TEST WAS RUN AGAINST THE WRONG COMMIT**

⛔ **The claim was *"Fix 2 does not conflict with `2e1f109`"* but the test run was `git merge-tree --write-tree cb6769d 4bd8a42`.** **(P) THEY ARE DIFFERENT COMMITS: `cb6769d6140db253cf31be4c7b8197a0b5517b5e` has PARENT `2e1f109d1d520728d3517569c38e1063bf3b925e`** ⇒ cb6769d is the CHILD; `2e1f109` IS an ancestor of it. ✅ **RE-RUN AGAINST THE NAMED COMMIT: `git merge-tree --write-tree 2e1f109 4bd8a42` → exit `0`, tree `e2a0531e618ecff9698808cd539f08dffe2bbf90`, `CONFLICT` count **0**, no output past line 1.** ⭐ **A DIFFERENT TREE OID from the cb6769d run (`460a7684…`) — as expected, since cb6769d also carries Screen-04 ⇒ ⛔ the two runs are NOT interchangeable, which is exactly why the substitution was a defect.** 🔑 **RULE: THE COMMIT IN THE COMMAND MUST BE THE COMMIT IN THE CLAIM — a superset ref may be a STRONGER test, but it is ⛔ NOT THE STATED ONE.**
