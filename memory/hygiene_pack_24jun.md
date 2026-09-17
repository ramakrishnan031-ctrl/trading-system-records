---
name: hygiene-pack-24jun
description: Hygiene 24-Jun — date-coupled system_manager test FIXED (test bug, not function); tzdata already fine; 9 merged branches pruned; CT114/127/130/132/133/135 PARKED (destructive, sandbox-only). Deployed post-15:30 close.
metadata:
  node_type: memory
  type: project
  originSessionId: 70f5d745-f68b-453a-9155-61b7b08308ff
---

**Hygiene cleanup pass 24-Jun. Assess-first, fix-only-the-real. Branch `hygiene-pack-24jun`. Deployed AFTER the 15:30 IST close (Rama's gate — protect live trades). No restart.**

## 1. Date-coupled test → FIXED (the only real fix)
`tests/unit/test_system_manager.py::test_report_integrity_missing_and_present` passed **only on 19-Jun**. Root cause = a **TEST bug, not a function bug**: the test wrote `logs/system_2026-06-19.log` (so the file's mtime = the run day) but called `report_integrity_check(day="2026-06-19")`. `report_integrity_check` (`scripts/system_manager.py:362`) intentionally warns when a report file's **mtime-day ≠ the checked `day`** (anti-staleness — catches a report that wasn't regenerated today). On 19-Jun mtime==day → ✅; on any other day → "stale" → the `assert "system log" … "✅"` flipped. **Fix:** the test now derives `date.today()` so the file's mtime matches `day`; the function is correct and untouched. This was the lone remaining pytest failure → full suite now green.

## 2. tzdata PC-env failures → ALREADY FINE (no action)
The earlier "test_main 23 / fix129 2 / fix135 6" PC-env failures were resolved by the **22-Jun tzdata install** (an OS-package fix, not code). Re-verified: `test_main` + `test_fix129_ntp_check` + `test_fix135_auto_token` = **122 passed, 0 fail**. Nothing to fix/mask.

## 3. Branch prune → 9 merged branches deleted (local + origin)
All 9 were re-verified merged into main (`git branch --merged main`) and deleted with `git branch -d` (refuses if not merged — safety) + `git push origin --delete`:
`fix-fno-ban-endpoint-22jun`, `aftercheck-circuit-cap-fix-24jun`, `cron-officer-email-leak-fix-24jun`, `governor-severity-and-briefing-debounce-24jun`, `part-c-rr-1.5-all-strategies-24jun`, `preflight-activation`, `slice1-rr-fix-aftercheck-22jun`, `slice2-strategy-control-24jun`, `tgt-retry-postmortem-24jun`. **Kept** `preflight-check-21jun` (UNmerged). Nothing lost — main has every commit; a merged branch is recreatable from its SHA. Result: only `main` + `preflight-check-21jun` remain.

## 4. CT crash-tests CT114/127/130/132/133/135 → PARKED (NOT run)
These are **destructive, operator-run crash-test SCENARIOS** (`tests/crash_test/scenarios/*.yaml` driven by `scenario_runner.py`, `subprocess shell=True` on the real `BASE_DIR`) — **NOT pytest tests, not in the suite, don't gate green**. What each does: CT114 Disk-Full (`fallocate` fills `/` to 2GB free), CT127 Clock-Backward-60s, CT130 Cron-Silent-Failure-Detection, CT132 Delete-Config-Mid-Session (`rm config/strategies/gap_fade_short.yaml`), CT133 Bad-YAML (**`sudo systemctl stop trading-system`** + corrupt a config), CT135 Cleanup-During-Active-Trading; CT132/CT135 need `market_hours: required`. **NOT run** — they would halt the live service / fill the disk / delete configs, and it was live market hours. "UNKNOWN status" = never completed in a prior manual run. **Run ONLY** in a dedicated throwaway sandbox VM, off-market, with operator supervision — never on the live box. Future drill, not a code fix.

**Lesson** (`tasks/lessons.md`): don't date-couple tests — derive/inject the date; a hardcoded "today" passes only on that calendar day. Verify which side (test vs function) is actually wrong before fixing.

Related: [[pc_test_env_hygiene]] (now largely cleared) · [[task_5_system_manager]] (the report_integrity_check function) · [[feedback_naive_ist_timestamps]]
