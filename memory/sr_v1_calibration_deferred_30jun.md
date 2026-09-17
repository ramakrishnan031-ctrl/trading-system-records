---
name: sr_v1_calibration_deferred_30jun
description: S&R V1 shadow calibration DEFERRED — data-gated reopen (~50 fills + ~8-10 BIR-filled W/L); validate zone accuracy + BIR thesis before enabling Phase A/B
metadata: 
  node_type: memory
  type: project
  originSessionId: 064a7869-6371-4c00-a7fc-cd5fd33d479a
---

**S&R V1 shadow calibration = DEFERRED — COLLECTING (30-Jun-2026).** One of only TWO open deferred items (the other = [[delivery_slice25_status_30jun]]); everything else is closed/deployed/dormant.

**WHAT:** validate the V1 shadow S&R detector — (i) zone ACCURACY and (ii) the **BIR** ("buying into resistance") PREDICTIVE thesis — before enabling Phase A (WAIT_FOR_RETEST entry) / Phase B (structure exit). A/B are all DORMANT; **V1 shadow is LIVE and auto-collecting** (`sr_detector.enabled=true`, wait_for_retest + structure_exit OFF).

**STATUS:** no manual work until the verdict review. Outcomes are populated nightly by the backfill cron (`sr_detector_backfill` @15:58 Mon-Fri; first auto-run Wed 1-Jul once [[sr_detector_backfill_cron_wired_30jun]] pushes — else stays hand-run).

**REOPEN — DATA-gated, NOT calendar:** when ~**50 FILLED trades overall** AND ~**8–10 BIR-flagged rows that ACTUALLY FILLED** with W/L outcomes exist. First checkpoint ~**mid-July (≈14-Jul)** for zone accuracy; the PASS/RECALIBRATE verdict likely ~**3–4 weeks** (BIR fills accrue slowly — recall 29-Jun: both BIR-flagged rows were NO_FILL, so validated BIR samples come slowly).

**CONTINUATION (when reopened):**
1. Review zone ACCURACY from accumulated detections — watch the **TSFINV-style too-wide-zone** pattern.
2. Review **BIR-FILLED W/L outcomes** → verdict: **PASS or RECALIBRATE**.
3. PASS → proceed to **Phase A enable per `SR_V2_MERGE_VALIDATION_RUNBOOK`** (flag-gated stages). RECALIBRATE → adjust **zone params only** (no redesign).

Relates to [[snr_detector_v1_27jun]], [[snr_v2_phaseA_27jun]], [[snr_v2_phaseB_27jun]], [[sr_detector_backfill_cron_wired_30jun]].
