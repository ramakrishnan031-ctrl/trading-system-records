---
name: config_edit_without_restart_is_a_split_state_04sep
description: "Config is load-once, so an edited config file with no restart fires on the NEXT boot - which may be the wrong day; plus the 04-Sep temporary CNC disable and its Monday 07-Sep revert"
metadata: 
  node_type: memory
  type: project
  originSessionId: 161ed55b-a158-4c12-a83a-53edac5888db
  modified: 2026-09-04T04:29:18.211Z
---

🔴 **A CONFIG EDIT WITHOUT A RESTART IS A SPLIT STATE, ⭐ AND A SPLIT STATE FIRES
ON THE *NEXT* BOOT -- ⛔ WHICH MAY BE THE WRONG DAY.**

🔬 `core/config_loader.py:38` -- *"Does not support hot reload -- load-once at
startup (Phase 0b)"* (⭐ same for `config_validator.py:41`, `logger.py:36`).
⇒ ⭐ Editing a YAML changes **nothing** in the running engine. ⛔ **Either restart
in the same act, or revert. ⛔ Never leave it.**

⭐ **Why "leave it" is the worst option, ⛔ not the neutral one.** 🔬 04-Sep: the
3 DELIVERY strategies were set `enabled: false` and the restart was momentarily
unavailable. ⇒ ⭐ In that window the file said delivery OFF while the process
still had it ON:
  · ⭐ **Today** -- a CNC entry could still fire ⇒ ⭐ the problem the edit existed
    to remove was ⛔ **not removed**.
  · 🔴 ⭐ **Monday** -- the 07-Sep boot would read the edited file ⇒ ⭐ delivery
    turns off on the one day it is wanted ON.
⇒ ⭐ **It flips the outcome on BOTH days.**

⚠️ 🔬 **VS Code / this session has ⛔ NO sudo on the VM** -- `systemctl restart`
is 👤 Rama's own act. ⭐ Plan for it; ⛔ do not discover it mid-change.

## 🔬 The 04-Sep instance (Rama-authorised, TEMPORARY)

👤 **Rama, verbatim:** *"If good to turn-off CNC>Clears the problem >Do it"* ·
*"Simple objective: Do anything to avoid problems, not to hold or increase the
problem"* ⇒ ⭐ **standing principle: when a choice is close, prefer the option
that CLOSES an open risk over the one that preserves today's opportunity.**

🔬 **Book state at the change (⭐ measured before touching anything, ⭐ per the
rule that turning CNC off ⛔ does NOT clear existing CNC):** 0 OPEN/PARTIAL,
0 trades that day, all 42 GTTs terminal (37 CLEANED / 4 TRIGGERED / 1 EXPIRED),
`fm_ledger` SYNC 09:15:00 `broker sync: 10470.10 -> 10470.10` ⇒ ⭐ zero drift
⇒ ⭐ **held = 0** ⇒ ⛔ nothing carrying.

⭐ Change: `positional_momentum_long`, `positional_sector_rotation`,
`positional_swing_long` → `enabled: false`, line 11 of each, ⭐ marked
`# TEMP 04-Sep-2026 ONLY -- Friday carry guard (Rama auth). REVERT MON 07-Sep.`
🔬 Diff-bounded to exactly 3 files / 3 lines. ⭐ Backups at
`/home/ubuntu/preserved/2026-09-04_cnc_off/*.yaml.bak`.

🔬 **Restart 09:31:38** (👤 Rama ran it), PID 1190450, `NRestarts=0`, new
`boot_id=1cafb667d30e`. ⭐ In-process proof: `strategy_control.summary`
`will_trade_count=12` (⭐ all 12 INTRADAY) with all 3 positional strategies
`WON'T TRADE — switch disabled`.

⚠️ 🔬 **`cnc_orders_possible` stayed `true`.** ⭐ It reflects the MASTER flags
(`delivery_enabled` / `force_intraday_only` / `trade_type`), ⛔ **not** strategy
enablement. ⇒ ⭐ The CNC *lock* is still open; ⭐ what closed is that no strategy
can emit a DELIVERY intent. ⭐ **One layer, ⛔ not two.**

## 🔴 THE REVERT IS OWED -- MON 07-Sep, PRE-BOOT

⭐ A session alarm ⛔ cannot survive three days, so the durable carrier is a
**VM cron**: `41 7 7 9 *` →
`/home/ubuntu/preserved/2026-09-04_cnc_off/revert_delivery.sh`, ⭐ which restores
the 3 YAMLs from `refs/heads/main` (⭐ **not** the `.bak`, so it lands on whatever
is committed by then) and writes a pass/fail verdict to `revert.log`.

🔬 **Tested end-to-end, ⛔ not merely written:** ⭐ the real script drove the tree
diff to **0**, then the disable was re-applied and confirmed back to exactly
**3**. ⭐ cron daemon `active`, `git` at `/usr/bin/git` (⭐ on cron's minimal PATH).

🔴 ⚠️ ⭐ **If the revert slips, the symptom is *"no delivery entries"* -- ⛔ NOT an
error.** ⭐ Same silent shape as the kill-switch check. ⇒ ⭐ **VERIFY it Monday
after the 08:15 boot: `will_trade_count` must read 15, ⛔ not 12.**

⭐ See also [[delivery_carry_blocks_shutdown_05aug]] ·
[[stale_local_main_is_a_push_trap_02sep]]

## 🔴 v1 OF THE REVERT COULD PASS WHILE RESTORING THE WRONG THING

⚠️ ⭐ v1 restored from `refs/heads/main` and judged itself by **"tree diff == 0"**.
⇒ ⭐ That proves the MECHANISM, ⛔ **not the INTENDED CONFIGURATION**: ⭐ if anything
commits `enabled: false` to main before Monday, ⭐ the revert restores the
**disable**, ⭐ drives the diff to 0, ⭐ and **logs a pass** -- ⛔ a silent no-op
reporting success on the morning it matters.

⭐ **v2 (04-Sep):** ⭐ the verdict is now the assertion
`^enabled:[[:space:]]*true[[:space:]]*(#.*)?$` **in all three files**, ⛔ never the
diff. ⭐ On failure ⇒ ⭐ fall back to the preserved `.bak`, ⭐ `logger -p user.crit`,
⭐ **exit 2**. ⭐ Total failure ⇒ exit 3.

🔬 **BOTH paths tested end to end, ⛔ not asserted:**
  · ⭐ **Trap path** (checkout stripped, so it "restores" the disable): ⭐ all 3
    ASSERT FAIL logged → ⭐ `.bak` fallback → ⭐ files read `enabled: true` →
    ⭐ **exit 2**. 🔴 ⭐ **v1 would have exited 0 here.**
  · ⭐ **Normal path:** ⭐ `checkout rc=0` → ⭐ *"REVERTED OK -- all 3 assert
    enabled: true"* → ⭐ **exit 0**.
  · ⭐ Final state restored: ⭐ 3 files disabled, ⭐ tree diff exactly 3.

## ✅ MID-SESSION RESTART IS SAFE FOR THE DAILY COUNTERS -- MEASURED 04-Sep

⭐ 📄 Standing open question (⭐ previously flagged as a sandbox experiment): ⭐ does a
mid-session restart re-arm the day's risk limits? ⇒ 🔬 **NO. Answered for free**, ⭐ by
two restarts (09:31, 13:47) taken **after** four trades.

  · ⭐ **Trade cap: DB-DERIVED, ⛔ not an in-memory counter.** 🔬 `risk_engine.py:306`
    `daily_count = self._store.count_trades_today(today)` (⭐ likewise
    `count_settled_trades_today`, `count_daily_delivery_trades`).
    ⇒ ⭐ **A restart CANNOT re-arm it.** 🔬 Read 4 of 10 after both restarts.
  · ⭐ **Realised P&L** comes from the `trades` table ⇒ ⭐ restart-immune. 🔬 net +Rs 10.87.
  · ⭐ **Capital re-INITs per boot** (⭐ a new `fm_` session_id each time) ⭐ but
    re-initialises **from the broker balance**, ⭐ and with a flat book nothing is
    held. 🔬 `G3 MARGIN_RECON: held=0.00 broker_used=0.00 residual=0.00` ⇒ ⭐ **zero
    drift**, ⛔ no CRITICAL.
  · ⭐ 🔬 The boot logs `startup_scenario=WARM: SHUTDOWN event found` ⇒ ⭐ the system
    classifies a mid-session restart as **WARM**, ⛔ not a new day.
  · ⏸ ⛔ NOT observable: ⭐ per-strategy re-entry gating -- ⭐ no entry fired after 13:47.

⚠️ 🔬 **Two restart cycles occurred, ⛔ not one:** ⭐ SHUTDOWN 13:46:10 → start 13:46:11,
⭐ then SHUTDOWN 13:47:46 → start 13:47:47 ⇒ ⭐ **4 `fm_ledger` session_ids for 3
intended boots.** ⭐ The live process is the 13:47:46 one (PID 1214531).
⭐ 📄 `NRestarts=0` remains correct -- ⭐ systemd counts **automatic** restarts only, so
⛔ it is NOT a witness to manual ones. ⭐ Count boots by `fm_ledger` INIT rows or
STARTUP events instead.

⚠️ ⭐ 📄 Do ⛔ NOT compare the `fm_ledger` INIT balance to realised P&L across a day
(🔬 10470.10 → 10459.23 vs net +10.87). ⭐ That is the operand-mismatch trap that
produced 4 false CRITICALs on 20-Aug. ⭐ **The comparator is G3's `residual`.**

## 🔬 THE FOURTH BOOT, ATTRIBUTED -- `systemctl restart` TAKES ~90 s AND LOOKS HUNG

⭐ 🔬 `/var/log/auth.log` (⭐ readable **without** sudo) gives three `ubuntu` sudo
`systemctl restart trading-system` invocations on 04-Sep:
  · ⭐ **09:31:34** (⛔ no TTY) -- the delivery-off restart
  · ⭐ **13:44:37** (⛔ no TTY) → ⭐ Stopping 13:46:06 → **Started 13:46:10**
  · ⭐ **13:46:12** (⭐ `TTY=pts/0`, interactive) → ⭐ Stopping 13:47:42 → **Started 13:47:46**
⭐ 🔬 Journal shows ⛔ no `Scheduled restart`, ⛔ no `Main process exited`, ⛔ no failure
result ⇒ ⭐ **clean external stops only** -- ⛔ neither automatic nor a crash.

🔴 ⭐ **THE OPERATIONAL FACT:** ⭐ the first command took **93 s** from invocation to the
service being back up (⭐ 13:44:37 → 13:46:10), ⭐ because shutdown is graceful.
⇒ ⭐ **That looks exactly like a hang**, ⭐ so the second invocation landed at 13:46:12 --
🔬 **two seconds AFTER the first had already completed.**
⇒ ⭐ **Expect a ~90 s wait and do NOT re-issue.** ⭐ Re-issuing costs a second full
stop/start of a live trading process. ⭐ Watch `ExecMainStartTimestamp` change, ⛔ not
the prompt returning.

⭐ 📄 To attribute any restart: ⭐ `auth.log` for the sudo COMMAND + TTY, ⭐ and the unit
journal for `Scheduled restart` / failure lines. ⛔ Never `NRestarts`.

## 🔴 THE NIGHTLY ENGINE STOP IS **AUTOMATIC** -- ⛔ NOT A HUMAN ACT

🔬 Measured 04-Sep. ⭐ Ten consecutive trading days of `SHUTDOWN` events, **all at
17:35:04** (⭐ one at :05): ⭐ 08-21 · 08-24 · 08-25 · 08-26 · 08-27 · 08-28 · 08-31 ·
09-01 · 09-02 · 09-03. ⭐ Weekends absent (⭐ system down by design).
⇒ ⛔ A human does not hit 17:35:04 ten times running.
🔬 Mechanism: ⭐ the unit is `Type=simple`, `Restart=on-failure`, with ⛔ **no
`RuntimeMaxSec`, ⛔ no `ExecStop`, ⛔ no systemd timer, ⛔ no cron entry** that stops it.
⇒ ⭐ **It is a scheduled self-exit INSIDE the application.**
⇒ ⭐ `Restart=on-failure` means a clean `exit(0)` is ⛔ NOT restarted ⇒ ⭐ the engine
stays down until the 08:15 token watcher starts it.

🔴 ⭐ **BUT THE RECORD WAS NOT SIMPLY WRONG -- reconcile it, ⛔ do not just delete it.**
⭐ 📄 The documented hazard is *"a CARRIED DELIVERY POSITION ⇒ no shutdown ⇒ no boot ⇒
next day takes no entries."* ⇒ ⭐ The stop is **automatic but CONDITIONAL**.
⇒ ⭐ So the real obligation was ⛔ never *"manually stop the engine"* -- ⭐ it is
**"ensure nothing is carried that would block the automatic stop."**
⇒ ⭐ That is why disabling delivery on 04-Sep was the correct response to the real
concern, ⭐ even while the concern was being **described** wrongly.

⚠️ ⭐ **The harm of the false version:** ⭐ it invites a human to run a manual stop ON TOP
of an automatic one, ⭐ or to believe a day was lost to something that was never his
to do. ⇒ ⭐ **A false obligation is ⛔ not harmless overhead** -- ⭐ it manufactures
anxiety and invites unnecessary intervention on a live system.

## ✅ GUI DEPLOYED-PATH QUESTION -- ANSWERED 04-Sep 15:44-15:50

⭐ **Record wording (⭐ use verbatim, ⛔ never broaden):**
> ⭐ *Deployed-path verified by direct render of /controls under PID 1119981; the
> route's backend modules were absent at 39292d3. Height sweep not measured;
> Tier-1/2/3 not measured.*

🔬 **The bracket held:** ⭐ BEFORE 15:44:31 and AFTER 15:50:48 both read
`MainPID=1119981`, `ExecMainStartTimestamp=Thu 2026-09-03 13:08:20`, `NRestarts=0`,
⭐ with the `:8500` socket bound to the same pid both times. ⇒ ⭐ the render is
attributable. ⚠️ ⭐ `Restart=always` means systemd would have silently replaced it
under a NEW pid if it had fallen over mid-click -- ⭐ **that is the case the bracket
exists to catch.**
🔬 Supporting: ⭐ `services/controls.py` + `readers/control_client.py` mtime
**02-Sep 23:39:55**, ⭐ process start **03-Sep 13:08:20** ⇒ ⭐ files precede process by
13.5 h; ⭐ neither existed at `39292d3`.

⭐ 👤 Rama's report: ⭐ the page drew fully -- ⭐ 14 panels, strategy list, control
history, readiness check.
⭐ ⚠️ **The red `CONTROL PLANE UNAVAILABLE — no control token configured` is ⛔ NOT a
failure of this test** -- ⭐ it is `controls.py` **executing correctly** and reporting
honestly that it cannot reach the plane. ⭐ 📄 A page rendered from the old tree could
⛔ not emit that banner: ⭐ the code did not exist. ⭐ Same for `Alerts: UNKNOWN` and the
3 `NOT READY` rows. ⏸ ⭐ The missing control token is a **config item**, ⛔ not a defect.
⏸ ⭐ Still open: ⭐ the 7 remaining `gui09` screens · ⭐ the Tier-2/Tier-3 sweep.
⭐ **Closing the deployment question does ⛔ NOT close the campaign.**

🔬 ⭐ `gui-dashboard` has **NO shutdown schedule**: ⭐ `Type=simple`, `Restart=always`,
⛔ no `RuntimeMaxSec`/`ExecStop`, ⛔ no timer, ⛔ no cron. ⭐ Up continuously since
03-Sep 13:08:20 -- ⭐ through the 03-Sep 17:35 engine self-exit and the 04-Sep 08:15
boot. ⇒ ⭐ **It does ⛔ NOT follow the engine lifecycle**; ⭐ GUI work has no daily
deadline.

## 🔬 THE 15:15 SOFT_KILL IS SCHEDULED -- ⭐ AND IT CLEARS MONDAY

🔬 04-Sep 15:15:01.852 `SOFT_KILL reason=circuit_breaker_force_close_15:15
by=order_monitor`; ⭐ the telegram title says **"SOFT KILL — scheduled"**; ⭐ 0 positions
open ⇒ ⭐ it closed nothing, ⭐ 📄 exactly as documented. ⭐ Fired **after** both passes,
⛔ so it had no bearing on the `NOT EXERCISED` verdict. ⭐ `eod_squareoff` 15:17:03
logged *"Kill switch already active (SOFT_KILL); skipping soft_kill"* -- ⭐ expected.

⚠️ ⭐ **The weekend question, checked because it has a SILENT failure mode:** ⭐ a
Friday kill must clear at a MONDAY boot -- ⭐ a 3-day gap, ⛔ not 1.
🔬 `kill_switch.clear_stale_state` compares **date ORDERING, ⛔ not day arithmetic**:
    triggered_date = self._triggered_at.date()
    if triggered_date >= today: return False
⇒ ⭐ 04-Sep < 07-Sep ⇒ ⭐ **it clears.** ⭐ 📄 Docstring: *"Auto-clear ANY kill switch
triggered on a PREVIOUS calendar day... EVERY prior-day kill is cleared regardless
of type"* (⭐ 👤 Rama's 2026-06-20 headless guarantee). ⭐ Observed working 04-Sep
08:15:28 (`KILL_AUTO_CLEARED` ev 3816). ⇒ ⛔ **No weekend-boundary bug.**
