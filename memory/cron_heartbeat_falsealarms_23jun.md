---
name: cron-heartbeat-falsealarms-23jun
description: "18:00 drift \"missing heartbeat\" for preflight_phase_a/b/c + daily_report = FALSE ALARM; jobs RAN (markers/output) but don't emit heartbeats (detection gap)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e1a15ec3-5140-4531-93b5-a58f94e7260a
---

**The 18:00 cron-drift "missing heartbeats in last 24h" for `preflight_phase_a` (08:30), `preflight_phase_b` (09:14), `preflight_phase_c` (09:15), `daily_report` (16:05) is a FALSE ALARM — proven read-only 23-Jun.** All four RAN today; they simply don't emit cron heartbeats, so the heartbeat-based drift-check flags them.

Evidence:
- preflight markers `data_store/cron_marks/preflight_phase_{a,b,c}.done` = exit **0** at 08:30:02 / 09:14:02 / 09:19:46; sentinel `data_store/preflight/today.json` shows phase_a/b/c all COMPLETED (status WARN but ran); `preflight.log` shows checks PASS today.
- `daily_report`: `reports/output/daily_report_2026-06-23.xlsx` written 16:05:07 (855 KB); `daily_report.log` "Daily report saved …2026-06-23.xlsx".
- `cron_heartbeat` table: **zero rows ever** for all four → they never heartbeat.

Same shape as the tgt_retry stale alarm — a **detection/calibration gap**, NOT a real morning-job gap. preflight is **marker-detected** (exit_code_file); daily_report has neither marker nor heartbeat. **Follow-up (separate, not this phase):** in `config/cron_registry.yaml`, set these jobs' `detection_method` to marker/none (not heartbeat-expected) — or have them emit heartbeats — so the drift-check stops false-flagging. The NEW Cron Officer framework (armed 23-Jun) detects via markers/`detection_method`; the OLD heartbeat-miss pass is the noisy one. See [[gemini-log-review-windowing-23jun]], [[cron_framework_armed_23jun]].
