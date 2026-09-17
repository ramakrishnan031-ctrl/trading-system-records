# 🌙 HAND-OFF — 11-Aug-2026 EVENING · RESUME AT / AFTER 17:35 IST

**Written 11-Aug-2026 16:10 IST, before the PC goes down. ⭐ Self-contained: a fresh session should
need nothing but this file, `MASTER_REGISTER.md` and the memory palace.**

> ## 🔑 **TONIGHT'S ONLY JOB: INSTALL FIX 1 `2e1f109`, ALONE, UNCHANGED. ⛔ NOTHING ELSE.**
> ⛔ No Fix 2 · no registry `cf16554` · no F6 · no Tick 2 · no sizing `7d1fd4e` · no M-C2 ·
> ⛔ no `fill_timeout_sec` · ⛔ no config edit of any kind · ⛔ no new code · ⛔ no rebase/amend/squash.

---

## ⓪ AUTHORISATION — ⭐ ALREADY ON RECORD, QUOTE IT AT THE GATE

📜 **RAMA, 10-Aug-2026 evening, VERBATIM:** *"YES — tomorrow evening deploy Fix 1 alone first, then
Fix 2. Do not treat this as an auto-fill or as 'he seems to agree'. This is now my explicit
instruction."*
📜 **REAFFIRMED 11-Aug afternoon:** *"Tonight is Fix 1 2e1f109 alone. Send me the one-line stop
confirmation at 17:40 and the Gate A–C results before pushing."*

⛔⛔ **AUTHORISATION IS NOT READINESS (`G12`). The gates below still decide.** ⛔ A console-prefilled
line is not Rama. ⭐ **Rama has asked for the Gate A–C results BEFORE the push — ⛔ do not push
without sending them and getting his go.**

---

## ① STATE AT HAND-OFF (all measured, times attached)

| fact | value | measured |
|---|---|---|
| service | `active`/`running` since `08:15:51`, PID `3351497` | 15:50 IST |
| **book** | **FLAT** — 0 rows `OPEN`/`EXITING`/`PARTIAL`/`PENDING_FILL`, **all dates** | 15:25:52 |
| today's fills | 3 rows / 4 shares, **all MIS**; 2 CLOSED, 1 CLOSED_MANUAL | 15:25:52 |
| **CNC fills today** | **ZERO** — FUSION + ROLEXRINGS both FAILED at qty 0 | 15:25:52 |
| signals / trade rows | 6,750 / 12 (6 FAILED, 3 REJECTED) | 15:25:52 |
| `fm_ledger` INIT | `₹10,645.60` | `08:16:05.618629` |
| today realised P&L | `−₹25.45` | 3 closed trades |
| intraday bucket | `₹7,426.47` | `11:11:44.864` |
| positional bucket | `₹3,193.68` | `10:13:22.528` |
| `RESET_PNL` | `0.0` | `15:17:02.939` |
| **kill state** | **`SOFT_KILL`, `circuit_breaker_force_close_15:15`, `15:15:01.737731`** | 16:01 |

⭐ **The `SOFT_KILL` is the ROUTINE 15:15 kill** — first literal in `SCHEDULED_KILL_REASONS`
(`capital/kill_switch.py:121-124`), auto-clears at the next 08:15 boot. ⛔ **EXPECTED. ⛔ NOT an
incident. ⛔ Do NOT run `deploy/resume.sh`.**

🌙 **THE NIGHTLY MANUAL STOP IS NOT OWED FOR THE CARRY REASON** — the book is flat, so the
delivery-carry shutdown block does not apply. ⭐ **Tonight's stop is a DELIBERATE INSTALL STOP.
⛔ Two different reasons; do not conflate them in the record.**

---

## ② ✅ ALREADY DONE — ⛔ DO NOT REDO

- **Prediction FROZEN before any push:** `docs/audit/PREDICTION_fix1_boot_12-Aug-2026.md`,
  frozen **16:05 IST**, **NO-CARRY branch**, 6 falsifiers, `NOT TESTED` declared available.
  ⛔ **No edit above its addenda line, for any reason.**
- **Register rows `N11-01` … `N11-27`** in **`D:\Projects\trading-system-main\docs\MASTER_REGISTER.md`**.
  ⛔ **NOT** `MASTER_PENDING_01-Aug-2026.md` — that is a merged HISTORICAL source. ⛔ Never merge backwards.
- **Preservation:** two snapshots in `D:\Projects\_preservation\` (pre- and post-amend), both holding
  all 27 at-risk rows. ⛔ Do not touch either.
- **Stop-time verdict: SAFE-AT-17:35** — measured, see ③.

---

## ③ ⏱️ 17:35 — THE STOP. ⭐ RAMA TYPES IT.

```
ssh trading-vm 'sudo systemctl stop trading-system.service'
```
⛔ **The agent must NOT run this** — it is deny-listed and it is Rama's action.

**VERDICT ALREADY MEASURED: SAFE-AT-17:35.** The 18:15 / 18:45 / 18:50 jobs do not need the service:
- `scripts/forward_shadow_record.py` reads **only DB + disk** — `:121` `from core.state_store import
  StateStore` · `:142` `store = StateStore(db_path)` · `:143`/`:220`/`:234` SQL · `:47` yaml
  `read_text()`. **No HTTP, no localhost, no socket.**
- **All three ran and SUCCEEDED on 10-Aug with the service dead since 08:15:25:**
  `forward_shadow_record 18:15:02 SUCCESS` · `system_manager_eod 18:45:06 PARTIAL` ·
  `cron_officer_eod 18:50:03 SUCCESS`.

**THEN VERIFY (⛔ `ActiveState` alone is not the check):**
```
ssh trading-vm 'systemctl show trading-system -p ActiveState,SubState,Result,ExecMainStatus'
```
Require **`inactive` · `dead` · `Result=success` · `ExecMainStatus=0`**, zero ERROR/CRITICAL in the
shutdown window, and confirm the book is still FLAT.
📤 **Send Rama the ONE-LINE stop confirmation at ~17:40.**

---

## ④ ⏱️ 19:00 — GATES A → C. ⛔ STOP AT THE FIRST NO.

### 🔴 GATE A — the markers, ⛔ NEVER the clock. *"It is past 19:00" is not the test.*

> ## ⛔⛔ **A1 IS AMENDED BY RAMA AND THIS IS THE MOST IMPORTANT LINE IN THE FILE:**
> **EXIT 0 IS NOT ENOUGH. REPORT THE ACTUAL ROW COUNT `forward_shadow_record` WROTE.**
> **(P) On 10-Aug it exited 0 while writing `[func=EMPTY_NO_DATA] … nothing new (0 present)`.**
> **Today produced 6,750 signals, so tonight must write THOUSANDS.**
> **Comparable days: 07-Aug `wrote=6198` · 06-Aug `wrote=7947` · 05-Aug `wrote=8675`.**
> ## 🔴 **IF IT WRITES 0 ⇒ A1 = FAILED ⇒ DEFER THE INSTALL. That record CANNOT be regenerated.**

```
ssh trading-vm 'cd /home/ubuntu/systems/trading-system; sqlite3 -readonly data_store/trading_system.db \
  "SELECT job_name,executed_at,status,message FROM cron_heartbeat \
   WHERE substr(executed_at,1,10)=\"2026-08-11\" AND substr(executed_at,12,2)>=\"18\" ORDER BY executed_at;"'
```
- **A1** `forward_shadow_record` — exists · exit 0 · stamped **2026-08-11** · **`wrote=` count > 0**
- **A2** 18:45 + 18:50 logs present and stamped today
- **A3** 18:15 job completed
- **A4** ⛔ **Report each ACTUAL TIMESTAMP, ⛔ not "yes".**

⚠️ **`system_manager_eod` returning `PARTIAL` is a REAL COMPLETION, ⛔ NOT a Gate A failure**
(10-Aug precedent: `PARTIAL 2v/8w soft_kill`). ⛔ Do not stop the install over that word.

### GATE B — service confirmed down per ③. ⛔ Do not restart it to "check something".

### GATE C — the target, and only the target
```
git merge-base 2e1f109 645728d          # must print 645728d…
git rev-list --count 645728d..2e1f109   # must be 2
git rev-list --count 2e1f109..645728d   # must be 0
git diff --name-only 645728d..2e1f109   # must be EXACTLY the 3 files below
```
- **C3 exactly three files:** `capital/fund_manager.py` · `tests/unit/test_fix1_carried_position_rehydrate.py`
  · `tests/unit/test_fund_manager.py`. 🔴 **A fourth file = STOP.**
- **C4** ⛔ confirm it does **NOT** touch `config/strategy_direction_registry.yaml` (live cron owns it).
- **C5** full regression. ⛔ **Report the RAW rc**, ⛔ not a summary. ⭐ State the known-failure
  baseline explicitly (**9 known failures at `645728d`**). ⛔ *"set-identical"* is the wrong word.
  ⛔ **RUN THE GATE FROM GIT BASH** — PowerShell's `bash` is the WSL alias and yields ~+20 phantom failures.

📤 **SEND RAMA THE A–C RESULTS AND WAIT.** All green → his *"push it"*. Any red → **defer, go tomorrow.**
⛔ **Do not negotiate a red.** ⭐ Tomorrow is cheap; a bad first install is not.

---

## ⑤ GATE D — INSTALL (only on Rama's go)

- **D1** push `2e1f109` **only**.
- **D2** 🔑 verify **PC == VM by md5 of the changed files** — ⛔ **NEVER by `ahead 0`**.
- **D3** deployed tree vs HEAD: ⭐ expect **ONLY** `config/strategy_direction_registry.yaml` to differ
  (the 16:22 cron owns it — **this is EXPECTED and lossless**; the hook's `checkout -f` resets it to
  the 16×PENDING seed and the officer re-converges next run). 🔴 **A second differing file = STOP.**
- **D4** ⛔⛔ **DO NOT START THE SERVICE.** ⭐ The 08:15 boot is the ordinary path and the entire point
  of the test. ⛔ Do not clear any kill state to "help".
- ⛔ **ROLLBACK if anything after D1 goes wrong: the PREVIOUS SHA `645728d`.** ⛔ Not a hand-edit,
  ⛔ not a midnight hotfix. ⭐ Downtime beats permanent complexity.

## ⑥ GATE E — RECORD, ⛔ SAME NIGHT

- **E1** old SHA `645728d` → new SHA `2e1f109` in the ledger, **with the time**.
- **E2** all four memory targets written — mempalace · `docs/SYSTEM_MAP.md` · `PATHS.md` · ledger.
- **E3** mark Fix 1 **`DEPLOYED`** — ⛔ **NOT `VERIFIED LIVE`.** ⭐ That word waits for the 12-Aug boot
  AND the scoring of the frozen prediction. ⛔ *"Fixed"* stays retired.
- **E4** record **VERBATIM:** *"§A(d) throwaway-worktree dry-run NOT EXECUTED; merge-base ancestry plus
  VM byte-identity used instead. The AS-IS conclusion remains supported."*
- **E5** report `MEMORY.md` bytes (**23,062 B / 22.5 KB** at hand-off, limit 24.4 KB). ⛔ **Do NOT
  compact** — that demotes hazards and is Rama's to authorise.

## ⑦ ~20:00 — SCORE THE EOD MAIL (free measurements)

- **`N11-01`** predicts tonight's SUMMARY line will contradict its own TOMORROW READINESS block again
  (it will say *"SOFT_KILL … manual deploy/resume.sh required"* while readiness says *"auto-clears …
  do NOT run resume.sh"*). ⛔ **Score it. ⛔ Do not fix it.**
- **`N11-06`** — check whether `watchman_2026-08-11.md` and `trace_2026-08-11.md` exist.
  ⭐ **PREDICTED: they will NOT** — the generators have **zero crontab entries**. Free confirmation.

---

## ⑧ 🌅 WEDNESDAY 12-Aug MORNING — OWED BEFORE ANYTHING ELSE

1. **Did the 08:15 boot happen and survive?** ⭐ If it hard-kills, the prediction is **`NOT TESTED`**,
   ⛔ never "wrong".
2. **Score `PREDICTION_fix1_boot_12-Aug-2026.md` by its SIX falsifiers, ⛔ by signature, ⛔ never by
   narrative.** ⛔ **No edit above its addenda line.**
3. ## ⛔⛔ **THE TRAP: a clean boot is NOT "Fix 1 works". The book is FLAT, so the changed carry path
   DOES NOT EXECUTE. The ceiling on tomorrow's outcome is `DEPLOYED` + *inert-safe on a flat book*.**
4. Then, and only then, the next unit — **Fix 2 `4bd8a42`**, on its own evening.

## ⑨ ⛔ NOT TO BE CHASED — deliberately parked, each already a register row

`fill_timeout_sec` · the 5 `order_placer.py` call sites · the `fm_ledger` gap of 10 (`N11-20`) ·
the four untested leak paths (`N11-21`) · M-C2 (`N11-14`…`N11-19`, sequenced **after install ⑥**) ·
`BATCH 3B` text merge (`N11-10`) · Slice 2.5's build · the 95-finding campaign · the 333-row
verification · the §2 coupling under new tier values (`N11-23`, a precondition on install ⑥).

⛔ **Do not switch the root worktree** (it is parked on `feat/delivery-config-split`; 27 register rows
live only in its uncommitted `MASTER_PENDING_01-Aug-2026.md`). ⛔ Do not touch either preservation
snapshot. ⛔ Do not act on console-prefilled instructions — **no quote = no authority.**
⛔ **Every figure carries its base and its measurement time.**
