---
name: holiday-reminder-reaches-rama-26jul
description: "The 2027 holiday-calendar boot-blocker now has a reminder that reaches Rama by email with nobody in the loop — hosted in the always-on security watcher because it is the only process that is alive when the trading service is the thing that died, and the only one that already backs off."
metadata: 
  node_type: memory
  type: project
  modified: 2026-07-26T17:46:36.951Z
  originSessionId: 9fb7b626-50eb-452c-aad2-f3509ed2474e
---

⏰📧 **BUILT + COMMITTED 26-Jul-2026 `cbcad2c` (on `main`, UNPUSHED).**
`check_nse_holiday_calendar` in `scripts/security_monitor.py` → CRITICAL sentinel →
`alert-watcher.service` → email. **From 15-Dec, generalised, self-clearing.**

⭐⭐ **THE RULE THIS EXISTS TO ENFORCE: A REMINDER THAT NEEDS SOMEBODY TO RUN THE TESTS IS NOT A
REMINDER.** The tripwire built on 26-Jul lives in the SUITE and fires from 1-Dec — but only if a
developer happens to be mid-session in December. That is a hope with a date on it. **Both are
kept**; the suite one also catches the case where the alert path itself is broken.

**WHY THE SECURITY WATCHER HOSTS A NON-SECURITY CHECK** — three properties are needed and only
that process has all three:
1. ⭐ **ALWAYS ON, and independent of the thing it warns about.** `security-watcher.service` is
   **`Type=simple` + `Restart=always` + `RestartSec=60`** — ⚠️ **NOT `oneshot`, and the unit file
   says why: systemd REFUSES `Restart=always` with `Type=oneshot`.** (Several existing memory
   notes call it a oneshot; the ~60 s cadence they describe is right, the type is not.) Outside
   cron and outside the trading service. **On 1-Jan the trading service is the thing that is
   dead — a boot-path check cannot warn you the boot died.**
2. **It already backs off.** A missing file is inherently persistent; `_dedup`'s presence ledger
   ([[realert-presence-ledger-26jul]]) reports once at full severity then on a widening ladder.
   Hosting it elsewhere = a SECOND suppression mechanism, and 37 CRITICALs from one stale SSH
   baseline is what that costs.
3. It reaches a human without a developer being present.

📏 **TWO HORIZONS, ONE SHAPE.** NEXT year's file is due `holiday_calendar_lead_days` (16) before
31-Dec ⇒ **15-Dec, in every December** (the suite stays at 1-Dec on purpose: developer first,
then the email). **CURRENT year's file is due unconditionally** — if that is missing the boot is
already dead. Both keys carry the filename ⇒ identity ⇒ safe to downgrade repeats.

⏳✅ **TWO PHASES — because ONE email is thin cover for an outage with a known date (`e6ade32`).**
`_send` writes a sentinel only for CRITICAL, so everything the backoff downgrades is
Telegram-only, and a WARNING Telegram dies silently on a delivery failure ⇒ as first shipped,
missing the 15-Dec message meant the next thing Rama heard was a service that would not start.
⭐ **THE KEY CARRIES A PHASE FROM A CLOSED 3-VALUE SET** (`boot-dead`/`notice`/`final`), so the
escalation is a different KEY ⇒ a different CONDITION ⇒ full severity. **That is the presence
ledger's rule APPLYING, not a way around "never CRITICAL twice"** — "16 days remain" and "3 days
remain" are genuinely different conditions. ⭐⭐ **What BOUNDS it is the set's SIZE, not
etiquette: 3 values ⇒ ≤3 CRITICALs per file per year. A DATE in the key was MEASURED at 17** —
the same plant that proved these tests non-vacuous. A test walks 400 consecutive days, asserts
every phase produced is declared AND every declared phase is reachable, and scans keys for a date.

📊 **MEASURED, not projected — the whole 15→31-Dec stream is SEVEN alerts, TWO CRITICAL:**
`15-Dec 00:00 C notice` · 15-Dec 06:00 · 16-Dec 06:00 · 23-Dec 06:00 ·
**`28-Dec 00:00 C final`** · 28-Dec 06:00 · 29-Dec 06:00.
⇒ **TWO guaranteed emails**, five Telegram repeats. `final_days=3` is config and must stay below
`lead_days`; `final` is tested first, so a misconfiguration costs the early notice and **never
the alert** (pinned). Standing backstop either way: `last_run.json` `clean=false` on every ~60 s
pass ⇒ `aggregator.read_security` raises a finding in **every daily pull report** until the file
lands (pushed once by `select_push`'s new/reopened rule, then silent).

✅ **SILENT TODAY, and that is pinned against the REAL `config/` directory.** `nse_holidays_2026.yaml`
exists and July is not December ⇒ the check returns `[]`, writes no sentinel, changes no finding
count. **The only observable delta anywhere is `last_run.json`'s `checks_run` 9→10 — and nothing
branches on it** (`aggregator.read_security` branches on `timestamp` staleness and `clean` only;
the Control Tower's own `checks_run` is a different number). ⇒ **not a Tuesday variable.**

🧪 **Proven by PLANTING three times, each restored md5-identical (`c9ec81cf…`, 63,525 B):**
unwire it from `run_pass` ⇒ 2 RED, one naming the function · put the date in the dedup key ⇒
**17 CRITICALs, one per day — the exact failure §A3 forbids** · pin it to 2027 ⇒ the
generalisation test RED.

⛔⛔ **THE ACTION IS STILL RAMA'S AND STILL UNCHANGED: commit NSE's PUBLISHED
`config/nse_holidays_2027.yaml`. NEVER invent, infer, extrapolate, or copy the previous year
forward** — a guessed calendar is far worse than a missing one, because the system would trade on
a market holiday and believe it was right. The alert body says so; the system only asks.

✅ **DEPLOY OBLIGATION LARGELY DISCHARGED: `main` was MERGED INTO `hold-check1-w8-26jul`
(`6184e79`), so Monday's push carries it.** ⚠️ **Residual risk: if that push slips indefinitely,
so does this — silently, for five months.** Deadline is **15-Dec-2026**, not Tuesday; recorded on
the Monday card and in [[unpushed-pending-deploy-ledger]] (read before every off-market window).

Related: [[clock-dependency-class-26jul]] · [[realert-presence-ledger-26jul]] ·
[[feedback-no-fixed-test-baseline]] · [[unpushed-pending-deploy-ledger]]
