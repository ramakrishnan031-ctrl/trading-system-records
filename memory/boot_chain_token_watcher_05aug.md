---
name: boot-chain-token-watcher-05aug
description: "Nothing in cron starts trading-system.service — token-watcher.service polls a token file every 30s; a failed token refresh is SILENT, so \"no order today\" has two indistinguishable causes."
metadata: 
  node_type: memory
  type: project
  originSessionId: ab103fd7-7892-466d-bcca-d63b2be8a964
  modified: 2026-08-05T02:42:09.514Z
---

**MEASURED 05-Aug-2026 07:5x on the VM, read-only. Every flip-day and observation card this campaign wrote says "the 08:15 boot" as though cron starts the service. It does not.**

**The actual chain:**
1. `15 8 * * 1-5` cron runs `scripts/auto_refresh_token.py` → writes
   `data_store/session/zerodha_token.json` with `date` = today.
2. **`token-watcher.service`** → `deploy/token_watcher.sh` (FIX-188), `Restart=always`,
   running continuously since 28-Jul, **polls every 30s** (`SLEEP_SEC=30`).
3. It starts `trading-system.service` only when **all** hold: token file exists AND
   `tok["date"] == today` · `within_service_window()` = hour ≥8 and <16 IST ·
   the previous clean `exit 0` was a **PRIOR day**.

⇒ **Expect `active` at ~08:15:30–08:16, NOT 08:15:00 — it is a 30s poll, not a timer.**

**Why the unit alone never restarts it:** `WantedBy=multi-user.target` (VM-boot only),
`Restart=on-failure` + `RestartPreventExitStatus=3 4`. The 17:35 self-exit is status 0 /
`Result=success` ⇒ systemd will never bring it back on its own.

## ⛔ THE HAZARD — a failed token refresh produces SILENCE, not an error

No token file ⇒ no boot ⇒ no alert, no CRITICAL. The system simply does not trade.
**The token file is a single point of failure with no alarm on it.**

⇒ **"No delivery order appeared today" has TWO causes that look identical:**
 (a) the flip did not work — a gate behind a gate, a real finding;
 (b) the service never started — nothing to do with delivery at all.
⛔ **Check (b) FIRST or (a) gets reported as a major finding when the truth was an
absent token file.** Order: token file → service `active` → boot checks → strategy orders.

⚠️ **`logs/cron-auto-token.log` is NOT the gate.** It is written only on abnormality —
measured 1 line, 323 bytes, mtime **2026-07-28** (the v45 migration), no write in 8 days
while the cron ran every weekday. **Silence there is success**, so an unchanged log is not
proof the token refreshed. The **FILE** is the gate. Same shape as
[[feedback_absence_needs_wide_check]] — a zero that measures the LOGGING POLICY, not the
outcome.

⚠️ That stale line reads `MIGRATION_REFUSED schema v44 -> v45 pending` and looks exactly
like a pending migration contradicting the flip's schema-diff-0. **Check the mtime before
reporting it.** See [[schema_push_overnight_refusal_27jul]].

**Owed (docs-only, deferred to after flip-day evidence): record this chain in
`docs/SYSTEM_MAP.md`, and note the unalarmed single point of failure.**
Same declared-vs-actual class as the config comments and the schema doc.

## 🔴 23-Aug-2026 — ⛔ THE 08:15 BOOT IS **NOT UNATTENDED**. THREE PARTIES SAID IT WAS; NOBODY HAD CHECKED.

🔬 **The morning start is MANUAL and OPERATOR-VERIFIED.** `deploy/zerodha_morning.ps1` — its own header: *"Run once each trading morning from the project root."* Steps: check/refresh the token (**browser TOTP**) → **`scp` it to the VM** → **wait 15 s** → **`ssh trading-vm "systemctl is-active trading-system"`** → report. `token_watcher.sh:14`: *"All start attempts also require a fresh token for today"* ⇒ ⛔ **the service CANNOT start until Rama sends the token.** `docs/first_day_live_runbook.md:31` — *"**08:00** — Run `zerodha_morning.bat` on PC"*. 🔬 **No `schtasks`/`Register-ScheduledTask` registers it anywhere.**

⭐ **HE IS TOLD, ~15 s after sending the token.** On `-ne "active"` the script prints a RED *"ERROR: trading-system service is NOT active on VM."* and **runs `Start-Process ssh trading-vm`** — a VM shell opens by itself. ⇒ ⭐ **the recommended rollback runs from exactly where the failure leaves him.**

⚠️ **STILL AN ARGUMENT FOR OPS ②, just a different one:** the PS1 tests `-ne "active"`, and a crash-looping unit reports `activating`, so it *would* be caught — **but the 15 s sample lands inside a ~11 s restart cycle, so it is a COIN-FLIP.** With `RestartPreventExitStatus=3 4 5` the unit sits in **`failed`** deterministically. ⛔ And nothing else in the day would tell him: `token_watcher` reads `activating` as *"running — nothing to do"* and deletes the alert flags every poll.

⚠️ **The residual exposure is him running the script and WALKING AWAY before step 5 prints.** 📄 `docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md`.
