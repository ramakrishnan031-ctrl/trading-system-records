---
name: handoff-28jul-resume
description: "FINAL HAND-OFF 28-Jul-2026 evening. ⛔ WEDNESDAY 29-JUL IS THE T2 ARM AND A CHANGE FREEZE — a real position is held overnight. Tuesday evening is CLOSED: CHECK 1/2/3 all passed, the 18:45 EOD baseline ran on old code and PASSED, and `52ead46..ce08668` (24 commits) was pushed at 18:46:19 and verified three ways. main is 1 ahead — `53a2443`, docs-only, deliberately unpushed until Thursday. Tree clean. EXACT NEXT ACTION: tomorrow, P0 date check then the T2 arm — nothing else."
metadata:
  node_type: memory
  type: project
  originSessionId: 58e849b5-81c5-4b96-89bc-182326b7fbbc
  modified: 2026-07-28T15:04:42.218Z
---

# ⛔⛔ WEDNESDAY 29-JUL IS THE T2 ARM AND A CHANGE FREEZE. A REAL POSITION IS HELD OVERNIGHT.

**NOTHING is built, pushed, merged, flipped or tuned on 29-Jul** — not docs, not tests, not "just a
small fix". Wednesday's ONLY content:
1. **P0 — THE DATE:** `date "+%A %d-%b-%Y"` must print **Wednesday 29-Jul-2026**. *The T2 script will
   run perfectly on the wrong day.*
2. **The T2 arm itself, per `docs/T2_RUNBOOK_29-JUL.txt`** (step-zero hash `0a3c505c…` — all four
   copies already agree, bit-rot trap gone; band reads −10%/+10% as VALUES).
3. **Observation.** Nothing else.

⭐ **The next code slot is THURSDAY 30-JUL evening.** ⛔ Do not start a build task tomorrow.

### ✅ TWO PRECONDITIONS FOR THE ARM, VERIFIED TONIGHT — do not re-derive them in the morning
- **`schema_version` = 45.** ⛔ If it reads 44 tomorrow, the migration did not hold ⇒ **ABORT.**
- **The overnight kill switch will CLEAR ITSELF.** State going into the night is `SOFT_KILL`,
  reason `circuit_breaker_force_close_15:15`, triggered `2026-07-28T15:15:01` by `order_monitor`.
  ✅ That reason **is** in `SCHEDULED_KILL_REASONS` (`capital/kill_switch.py:114-117`, alongside
  `EOD_SQUAREOFF`), so `auto_clear_scheduled_kill()` clears it at the 08:15 boot — exactly as it did
  this morning from the identical reason. ⛔ **No `deploy/resume.sh` is needed.** Only a SAME-DAY
  *emergency* kill would require one. [[killswitch-autoclear-prior-day]]

⚠️ **Expect an `WARNING` "Orphan GTT" next morning** — T2's GTT is seen by the never-run FIX-183
prepass. It is EXPECTED, not a finding. ⛔ `--arm-overnight` exit 1 still means stock is held overnight.

---

## ✅ TUESDAY 28-JUL IS CLOSED. Everything on the card ran.

### WHAT CHANGED
- **PUSHED 18:46:19 IST — `52ead46..ce08668`, 24 commits.** Authorised by Rama's 15:45 override
  (*"Any pending commit, push, pull — do it now. PC == VM 100%"*), which had already been written
  into the deploy calendar's Tue row with its justification.
- ⚠️ **`main` is 1 AHEAD, not 0.** Writing this deploy into `docs/SYSTEM_MAP.md` + `PATHS.md` produced
  one further commit, **`53a2443`** (docs only: 2 files, 3 insertions). ⛔ **Deliberately NOT pushed —
  it goes Thursday.** Committed rather than left dirty because the no-deploy rule governs **PUSHING,
  not committing**, and two power-downs already cost sessions today. **Tree clean, stash empty.**
- **The stray-`.pyc` detector is 🏷️ DEPLOYED** (`8331fb0`) — an 11th, monitoring-only EOD check.
  ⛔ **NOT "VERIFIED LIVE".** Its first production run is **WED 29-JUL 18:45**.
- Also discharged: the fix061 test repair, `1b03a64` recovery docs, and **`45e0133`+`d2426d2`**,
  which the ledger had recorded as *"COMMITTED, UNPUSHED BY DESIGN → Thursday"* — they went tonight.
- ⛔ **ZERO production/config/trading-path files.** Non-doc set across all 24 commits is exactly three:
  `scripts/system_manager.py` + two test files ⇒ **Wednesday's 08:15 boot carries zero live boot
  variables even after the push.** (`main.py` never imports `system_manager`; it is an 18:45 EOD cron.)

### ⭐⭐ THE ORDER WAS REVERSED ON THE NIGHT — AND THE REASON IS THE PART WORTH KEEPING
A power-down moved the clock from ~17:45 to 18:40, so **the 18:45 EOD job was allowed to run FIRST,
on the OLD code, as a deliberate baseline.** The deciding reason was **diagnostic, not timing**:
27-Jul's EOD report never appeared, so *"is the EOD job broken at all?"* was genuinely open. Pushing
first would have left **two candidate causes and one observation**. [[feedback-baseline-before-change-28jul]]

### WHAT WAS VERIFIED, AND HOW
- **CHECK 1 — PASSED 17:11.** `active` · `NRestarts=0` · `ActiveEnterTimestamp=08:15:15` unchanged.
- **CHECK 2 — PASSED 17:11.** `pb01_capture SUCCESS 17:00:04` **and** 12 rows dated 28-Jul (the row
  COUNT is the proof; the heartbeat logs `queued=`, not captured).
- **CHECK 3 — PASSED 18:41.** `inactive (dead)` · `Result=success` · `ExecMainStatus=0` · exit
  **17:35:04** · `NRestarts=0`.
  - **Error census 9 — ALL NINE CLASSIFIED, not counted.** 1 CRITICAL 08:15:16 startup kill-switch
    notice · 4 ERROR = 2 `slippage_exceeded` × 2 loggers (INFOBEAN 0.44>0.42, HEXT 2.40>1.47 — the
    guard *refusing an entry*) · 3 CRITICAL 15:15:01 routine circuit-breaker SOFT_KILL triple ·
    1 ERROR 17:35:03 `kiteconnect.ticker "Connection closed: None - None"`, 1s before the exit,
    paired with the `live_feed` disconnect WARNING = websocket teardown at shutdown.
  - ⚠️ **The card's rule "any new CRITICAL at all is NOT clean" would have raised a FALSE ALARM.**
    Its "5-and-explained" baseline was measured at **10:20**, before the 15:15 kill and the 17:35
    shutdown ⇒ **a full-day census can never be 5.** The card has been corrected in place.
  - ⭐ **Classified by a falsifiable test:** `circuit_breaker_force_close_15:15` appears **4× on every
    one of 22/23/24/27/28-Jul** — a daily designed property. Full-day census comparables:
    **6 / 11 / 12 / 13 / today 9** — lower than each of the three most recent trading days.
    Exact and widened regex both returned 9 ⇒ nothing hid behind a whitespace variant.
  - **Capital: ZERO orphaned reservations**, reconciled independently — **25 RESERVE = 21 RELEASE +
    4 COMMIT**. The card's own 14:12 SWIGGY false-positive `3cdce65f04bc44b4` is now terminated.
    `RESET_PNL` present (1) ⇒ the routine 15:15 kill did **not** forfeit it, matching 24-Jul.
  - **Orders: 7 FAILED ↔ 7 `entry_cancelled_zero_fill`**, each ~60-70s later, 1:1 in time order; the
    2 REJECTED are exactly the 2 slippage rejections (no order placed ⇒ correctly no zero-fill line).
    ⚠️ *Width: matched by count and time-order, NOT by symbol — that log line has no symbol field.*
  - **Book FLAT:** 4 positions taken → 4 COMMIT → 4 RELEASE_USED → zero open.
- **18:45 EOD BASELINE — PASSED, and it CLOSED A SUSPECT.** `reports/system_manager/2026-07-28.txt`
  **PRESENT** (4,242 B), heartbeat `system_manager_eod SUCCESS 18:45:05`, 10 full sections,
  `check_failed`=0 ⇒ **the EOD job works; 27-Jul's absence is explained by the schema-refusal night
  ALONE.** ✅ Control held: **zero `STRAY` lines** — the detector wasn't deployed yet, so its absence
  was the control. Job confirmed **finished** before the push replaced its own source.
- **PUSH VERIFIED THREE WAYS, each falsifiable:**
  - (a) PC `ce08668` == VM bare `ce08668`.
  - (b) **md5 `35012cbb…` (re-measured live 18:43) → `a57af797b2624399b54b80b444c245da`** — the value
    pre-registered in the card; `stray_pyc_check` occurrences **0 → 2**. It could have been red.
  - (c) **Reflog pair, both `2026-07-28 18:46:19 +0530`: `push` AND `checkout`** (the checkout line is
    the event that writes the tree). Prior `52ead46 @ 09:15:25` pair intact ⇒ `gc.reflogExpire=never`
    (set ~15:3x, before the push) is holding.
- ⚠️ **`post-receive` said "crontab AUTO-INSTALLED from canonical" — verified a NO-OP** (110 lines;
  EOD entry byte-identical pre/post; zero `deploy/` files in the diff). Checked, not assumed.
- ⚠️ **A probe of mine erred, and the correction is worth keeping:**
  `git -C ~/systems/trading-system rev-parse` fails *"not a git repository"* **BY DESIGN** — the
  deployed tree is a **checkout target** of the bare repo and has no `.git`. That is exactly why the
  card specifies **md5, "not a date"** as the tree-level check. ⛔ Not a deploy failure.

### ⭐ WEDNESDAY GO/NO-GO — DECIDED, per runbook case (b)
> *Does any unexplained noise touch the ORDER or CAPITAL path?* → **NO ⇒ ✅ PROCEED.**
Capital reconciles with zero orphans; every FAILED trade has its designed cancel; both REJECTED are
the slippage guard working; the 4 non-baseline census lines are a proven-daily designed kill and a
shutdown-time socket close. Schema reads **45**, not 44. ⛔ If `schema_meta` reads 44 tomorrow, ABORT.

### REMAINING OPEN ITEMS
- ⚠️ **OPEN OBSERVATION, NOT CLOSED: PB-01 25 → 12.** Touches neither the order nor the capital path
  ⇒ it does not gate Wednesday. ⛔ But *"does not gate" is not "explained"* — account for it tomorrow.
- 🏷️ **The detector is DEPLOYED, not VERIFIED LIVE.** Wed 18:45 is its first production run; ⭐ one run
  will then be an **OCCASION, not a property**. Do not write it up as reliability.
- ⏳ **THU 30-JUL owes:** `fix-tests-27jul` · `fix-boot-27jul` · `214a878` · `249317d`;
  `fix-symdir-27jul` → 31-Jul. ⛔ **§7.1 pre-push gate (#16a inert on the VM) must be RE-RUN on the
  night** — the 28-Jul run printed `PROCEED`, but that does not carry forward.
  ✅ Reflog protection DONE — not owed again.
- **K1** emergency kill + same-day restart ⇒ exit 4 (docs fixed, **behaviour half OPEN**, gate after
  4-Aug) · **K2** the 06-Jul ₹10,000 drift events · **K3** drift <₹250 invisible (noise tier=DEBUG) ·
  **T2** `tests/crash_test/`(8) + `tests/core/`(1) never run in the gate · **T3** `test_fix181`
  LIMIT-vs-MARKET on the HARD_KILL flatten · **T4** `backfill_closure_source_w8.py:92`.
  All registered in `docs/decisions/ACTIONS_not_decisions.md`.
- ✅ Checked and **not** a finding: `watchman.md`/`flow_trace.md` MISSING appears in the 22-, 23- and
  24-Jul EOD reports too — pre-existing and routine.

### NEW PRODUCTION RISKS INTRODUCED TONIGHT
**None.** No production code, config, or trading-path file changed. The single runtime addition is an
EOD-cron check that cannot affect trading and cannot stop a boot. It is contained:
`system_manager.py:1093-1102` wraps every check in try/except — a raiser logs `check_failed`, becomes
a WARNING section, and the report still builds. It can **never** trip a soft-kill.
⭐ **NOT a change-freeze breach:** the freeze forbids changes *on Wednesday*; this landed Tuesday.
Say that explicitly or someone will read the Wednesday run as a violation.

---

---

## 🌙 LATE-EVENING BATCH (19:50→~22:00) — TWO MORE THINGS LANDED

### ⚠️⚠️ A. RAMA IS UNAVAILABLE 11:00–17:00 IST — WED · THU · FRI · SAT
**RECORDED on all four deploy-calendar rows** so it is not re-discovered on Friday.
- **THE ARM (Wed) COLLIDES ⇒ 🔴 AN OPEN DECISION, OWED BEFORE 10:30.** The runbook wants
  **13:00** (acceptable 12:30–14:00, ABORT outside **10:30–14:30**, P6 needs ~30 min) — the aim and
  the whole acceptable band sit inside the unavailable window. **Only legal slot: 10:30–11:00**,
  with NO slack for §3's by-hand broker check. ⚠️ COST: void risk **≥9% vs ~2.8%** (the 13:00
  anchor is half the reduction; ~9.0% is measured at an **11:30** anchor and 10:30 is earlier, so
  **no honest number exists for 10:30** — do not invent one). Options: arm 10:30 · carve ~40 min
  out of the window · slip (⛔ not free — never a Friday arm, 3-Aug is owned by the rule going
  live ⇒ Tue 4-Aug, colliding with the flag flip). ⛔ **His call. If undecided by 10:30, DO NOT ARM.**
- ✅ **THE CLOSE (Thu) DOES NOT COLLIDE** — §7 gives it no clock time, only "market hours only"
  ⇒ **09:15–11:00 works**, and early is better (a SELL rejection = DDPI unauthorised, restarts the pair).
- ⭐ **UNATTENDED-WINDOW RISK, ANSWERED FROM SOURCE:** protection is the **broker-side GTT alone**,
  independent of our service/VM/laptop ⇒ being unattended **changes nothing** (max loss ~₹10).
  `eod_squareoff.py:1064-1072` filters `("MIS","CO")` ⇒ the 15:15/EOD machinery **cannot touch**
  the CNC share (which is what keeps the test valid). ⛔ **`liveness_probe.py` is DETECTION, NOT
  PROTECTION** — it only alerts; no restart, no corrective action anywhere in it.

### ✅ B. THE SEVEN REGISTER FILES ARE CONSOLIDATED INTO ONE — AND IT IS IN THE REPO
**`docs/MASTER_PENDING_28-Jul-2026.txt`** (`d5b9d8c`) + a md5-identical read-copy in Downloads.
⭐ **RAMA: IT IS SELF-CONTAINED AND THE SEVEN ORIGINALS ARE SAFE TO DELETE** (they were NOT
deleted — that is his to do). Reconciliation **M=118 exact · K≈91 · J=211 derived** of ~420
appearances. ⛔ J is a residual, not a measurement.
⭐⭐ **THE JOB WAS NOT BOOKKEEPING — IT FOUND A LIVE PRODUCTION GAP:**
**`liveness_probe.py:108 _LIVENESS_END = 16:00` vs `service_window_end: "17:35"` ⇒ 95 MINUTES
UNWATCHED EVERY TRADING DAY.** A 16:20 death looks exactly like "no breakouts" the next morning.
The manual ~17:10 alive check **is** the compensating control. It existed ONLY in the file that
was about to be deleted. [[feedback-operator-planning-docs-external]]
⚠️ **AND A CORRECTION WHERE TWO SOURCES DISAGREED AND BOTH WERE WRONG — `trades.sector`:**
MEASURED NULL on 361 rows (→16-Jul), **`'UNKNOWN'` on 81 (20-Jul→28-Jul)**, a real value on
**exactly ONE trade ever**. So the 16-Jul "NULL at INSERT" is obsolete AND `PATHS.md`'s "B1
CLOSED" is wrong — the write path shipped, the **resolution** did not. ⛔ **The error direction
INVERTED** (NULL = silently permissive; one `UNKNOWN` bucket = sums the whole book). **Read
`sector_exposure()`'s 'UNKNOWN' handling BEFORE D1/sizing moves.**
⚠️ Also corrected: `one_trade_per_symbol_direction_per_day` + mis_filter SHADOW read as *shipped*
in the old register but are **on `fix-symdir-27jul`, ABSENT from main** ⇒ live **Mon 3-Aug**, not
Friday (the old register contradicted itself; §9 and the calendar are right).

---

## ⏰ THE EXACT NEXT ACTION
**Tomorrow (Wed 29-Jul): run the P0 date check, then arm T2 per `docs/T2_RUNBOOK_29-JUL.txt`, then
observe. Nothing else — no builds, no pushes, no tuning.** Tonight's card
(`Downloads/TUESDAY_EVENING_CHECKS_28-JUL.txt`) is **spent and amended to match what happened**; it
needs nothing further.

[[feedback-baseline-before-change-28jul]] [[deploy-record-exists-28jul]] [[slice25-execution-plan-27jul]]
[[feedback-status-label-rule-27jul]] [[feedback-no-fixed-test-baseline]] [[feedback-absence-needs-wide-check]]
