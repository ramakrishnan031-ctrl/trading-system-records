---
name: startup-scenario-crash-mislabel-06aug
description: "The 06-Aug 08:15 boot labelled itself startup_scenario=CRASH despite Wednesday's clean stop — filed, not chased"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2a4a3971-dd6a-4008-aba8-92b69d464d12
  modified: 2026-08-06T13:10:26.129Z
---

# `startup_scenario=CRASH` ON A BOOT THAT FOLLOWED A **CLEAN** STOP — ⛔ FILED, NOT CHASED

**(P) 06-Aug-2026 `08:15:02.891`** — `main`:
> `startup_scenario=CRASH: same day, no SHUTDOWN event found`

⛔ **But 05-Aug's stop was clean and verified** — `systemctl stop` issued 22:46:3x, `_shutdown()`
reached, census written `22:46:36.511`, 55 lines, `mismatches=0`
*(`docs/audit/STOP_PROCEDURE_05-Aug-2026.md` §(i))*.

## THE LIKELY MECHANISM — ⚠️ **INFERRED, NOT MEASURED**
The lookup appears to be **same-day** scoped (*"same day, no SHUTDOWN event found"*). A **prior-day**
shutdown therefore does not satisfy it, and every ordinary overnight boot would label itself `CRASH`.
⭐ **If that is right it is LABELLING, not behaviour** — and it would mean the label has been wrong
on most boots, not just this one. ⛔ **Neither half is established. Do not repeat as fact.**

## WHY IT IS WORTH KEEPING RATHER THAN DISCARDING
⭐⭐ **A boot that mislabels itself as a crash is a claim that OVERSTATES what happened — and this
campaign's dominant defect family is exactly that.** A `CRASH` scenario may also select different
recovery behaviour at boot; ⛔ **whether it does is UNVERIFIED and is the first thing to check** if
this is ever picked up.

## ⛔ DO NOT CHASE ON A CLOCKED EVENING
Filed 06-Aug during a live evening with an F6 phantom open. **It changed nothing that night and it
gates nothing.** ⭐ Pick it up only in a quiet off-market window.

Related: [[counts-db-rows-not-broker-06aug]] · [[feedback-status-label-rule-27jul]].
