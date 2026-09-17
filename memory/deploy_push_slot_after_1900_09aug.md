---
name: deploy-push-slot-after-1900-09aug
description: "18:15 is the push FLOOR, not a clear window — the EOD cron chain runs to 18:50, forward_shadow_record starts AT 18:15, and a push before 18:45 makes the EOD report the first run of new code."
metadata: 
  node_type: memory
  type: project
  originSessionId: 47b06b64-d65c-4b31-9c0d-e9517c6a78bf
  modified: 2026-08-09T14:13:13.949Z
---

# ⏰ 18:15 IS A FLOOR, ⛔ NOT A QUIET WINDOW — THE EOD CRON CHAIN RUNS TO 18:50

**(P) Measured 09-Aug-2026 from `deploy/cron/trading-system.cron`** — the GENERATED crontab, which the registry's own header declares authoritative over its `schedule:` documentation fields. ⚠️ **Width: this is the PC's generated copy; the LIVE VM crontab is md5-baselined at each push and is known to hold FEWER jobs (the 4 claude heartbeats were removed ~02:12), ⛔ never more.**

| time (Mon-Fri) | job |
|---|---|
| 17:00 | `gemini_data_integrity_check.py` |
| 17:05 | `ops/control_tower/runner.py` — ⭐ last of the afternoon chain |
| 18:00 | `check_cron_drift.py` |
| **18:15** | 🔴 **`forward_shadow_record.py`** — starts the exact minute the push window opens |
| **18:45** | **`system_manager.py`** — the EOD report |
| 18:50 | `cron_officer.py --eod-summary` |

## 🔴 WHY IT MATTERS — TWO SEPARATE COSTS, BOTH AT THE FLOOR ITSELF
1. **18:15 writes the un-regenerable artifact.** `forward_shadow_record.py`'s output **cannot be regenerated** and ⛔ must never be hand-produced — a gap is a loss, a manufactured day is a CORRUPTION. A `checkout -f` landing mid-run swaps its source underneath it. ⭐ **This is ALREADY push gate ② ("forward-shadow banked") — the fact is not new; its ABSENCE from the deploy-sequence document was.** ✅ The crontab writes `data_store/cron_marks/forward_shadow_record.done` carrying `rc` + an ISO timestamp ⇒ **a checkable precondition, ⛔ not a judgement call.**
2. **A push before 18:45 makes the EOD report the first run of the new code** — at night, unwatched. ⭐ **Precedent, deliberate:** ledger Gate 10 was HELD so the 18:45 `system_manager_eod` banked on OLD code as a baseline (28-Jul precedent) rather than becoming the first run of a changed `eod_squareoff.py`.

⇒ 🔑 **THE GENUINELY CLEAR SLOT IS AFTER ~19:00**, which is where every actual push has landed anyway: **03-Aug 23:04 · 06-Aug 20:32 · 07-Aug 18:2x** *(the 07-Aug one sat between forward-shadow and the EOD report)*.

⛔ **THE 18:15 FLOOR ITSELF IS UNCHANGED AND WAS NOT TOUCHED** — it is frozen in `GO_NOGO_f6_deploy.md` and runbook §0.2 step 5, and `D3` states it as a rule. ⭐ **This narrows the window from below; it does not move the gate.**

## ⚠️⚠️ THE CHECK IS NOT UNIFORM — ⛔ DO NOT LOOK FOR A MARKER THAT DOES NOT EXIST
**(P) only 21 of 45 cron lines write a `data_store/cron_marks/*.done` marker.** ✅ `forward_shadow_record` **does** *(and `control_tower`, `fetch_daily_candles`, `sr_detector_backfill`, `reconstruct_excursions`, `strategy_registry_officer`, `capture_metrics` …)*. 🔴 **`system_manager` (18:45) and `cron_officer` (18:50) DO NOT — nor does `check_cron_drift` (18:00).** ⇒ **their completion is provable ONLY by log mtime** (`logs/system-manager.log`, `logs/cron-officer.log`, dated TODAY at/after their times). ⛔ **A check written as *"confirm all four markers"* would be UNRUNNABLE and would get waved through at 19:00** — the `V5` tautological-check shape, arriving as a missing file rather than a passing assertion.

## ✅ HARDENED 09-Aug — IT IS NOW `GO_NOGO_f6_deploy.md` **LINE 10**, ⛔ NOT A NOTE
⭐ **A checklist line fails loudly; a paragraph does not** — and this is read at 19:00 with a push waiting. **Both conditions required, both observable; ⛔ "it is past 19:00" is explicitly NOT the test — the clock is a PROXY, and a late job makes it lie in the PERMISSIVE direction.**
🔒 **THE FREEZE WAS RECONCILED, ⛔ NOT IGNORED.** Line 9's cell declares the gate FROZEN — *"never patch inside the window"*. **(a)** This was added **OUTSIDE** the window *(Sunday eve / Monday daytime, before the stop, before the snapshot, before any line is run)*; the prohibition is against patching **ON THE NIGHT**. **(b)** ⭐⭐ **STRICTLY ADDITIVE AND FAIL-CLOSED: lines 1-9 BYTE-IDENTICAL — (P) verified by `git diff`, exactly ONE old line changed and it was the HEADER's line-count — and line 10 can only ever produce a `NO-GO`.** ⛔ It cannot authorise, loosen, or supply a value validated by its own author — **that same-actor shape is what froze line 9, and a check that only fails closed is not what the freeze exists to prevent.** **(c)** ⚠️ **The alternative was worse and decided it:** page-only would have been **overridden by the page's own new hierarchy statement** *(`GO_NOGO` outranks the page)* ⇒ ALL-GO at 18:20. ⭐ **The header count NINE → TEN was mandatory, by the header's own rule** *(“a stale ‘eight’ would silently authorise skipping it”)*; the original NINE sentence is **kept verbatim** beside it (`G4`). ⛔ **If Rama judges it a breach the remedy is his and cheap — strike line 10; the page's after-19:00 rule then carries it.**

See also [[branch-inventory-deploy-sequence-09aug]] · [[f6-deploy-authorised-08aug]] · [[feedback-absence-needs-wide-check]]
