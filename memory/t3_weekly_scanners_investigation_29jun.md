---
name: t3-weekly-scanners-investigation-29jun
description: "T3 Phase-0 investigation (29-Jun, INVESTIGATE-ONLY): the deferred Control Tower advisory category (dead-code/unused/orphan/duplicate/empty/stale). RUTHLESS TRIAGE verdict = NOT worth building. Codebase too clean (2 markers, all 14 NotImplementedError intentional, dupes=5 __init__.py) + too cron-heavy (27 entry points) for these to be reliable+valuable; logs/backups/configs already covered. Recommend SKIP, or at most a tiny forward-looking TODO/FIXME tracker."
metadata: 
  node_type: memory
  type: project
  originSessionId: ce5f39df-1b39-4e66-a909-988eb932224d
---

**T3 Phase-0 INVESTIGATION ONLY (29-Jun) — ruthless triage; NO fix/design/deploy.** Scope = the deferred Control Tower "advisory" category (dead-code / placeholder / unused / orphan / duplicate / empty / stale, advisory-only, NEVER delete). **HEADLINE VERDICT: most of this is NOT worth building** on THIS codebase — too clean for the reliable categories, too cron-heavy for the noisy ones, and the rest overlaps existing monitors.

**1. PER-CATEGORY (reliability / noise / value, measured on this repo):**
- **Placeholder markers (TODO/FIXME/HACK):** detection RELIABLE, but the repo has **1 TODO total** (`broker/slippage_engine.py:74` FIX-109 FNO-proxy note) + **1 XXX that is a FALSE POSITIVE** (`scripts/check_vm_state.py:57` `--symbol=XXX` doc placeholder, not a marker). ⇒ ~1 actionable finding. Cleanest category, but near-zero to surface.
- **NotImplementedError (14):** detection reliable, but **ALL 14 are INTENTIONAL** → 100% false-positive here: the AngelOne **stub adapter** (`broker/angelone_adapter.py`, ~7, "Stub only"), paper-mode **guards** (`zerodha_adapter.py:1531/1541`), **ABC base methods** (`scripts/preflight/base.py:102/105` run()/fix()), + 1 comment (`main.py:1650`). DROP.
- **Duplicate files:** hash detection reliable, but the only collision = **5 identical empty `__init__.py`** package markers (capital/orders/signals/data/reports) → intentional. ~0 value. DROP.
- **Unused / orphan / dormant:** atime unreliable (relatime); "not imported" MISSES **27 cron-invoked entry-point scripts** (of 53 `scripts/*.py`) + ~20 manual/ad-hoc tools (check_vm_state, approve_ssh_keys, t2_cnc_gtt_realtest, sr_detector_backfill, reconcile_*, …). VERY HIGH noise, fragile hand-maintained whitelist. DROP.
- **Dead code (uncalled):** static analysis misses cron entry points, dynamic dispatch, event hooks, the StrategyLoader/adapters. HIGH noise without a big whitelist. DROP.
- **Stale backups:** OWNED by T2 `backup_retention.py` (just built). DROP (overlap).
- **Stale logs:** OWNED by the `log_cleanup` cron (00:00 daily `find logs -name '*.log' -mtime +30 -delete`). DROP (overlap).
- **Abandoned configs:** PC repo has NONE; only 2 VM-only `config/system_config.yaml.bak*` (operator deploy edits, untracked, KB). Trivial — manual cleanup, not a scanner.
- **Empty resources:** empty-table ≠ problem (e.g. `excursion_reconstruction_runs` was legitimately empty pre-15:50). The Control Tower freshness engine already handles operational empties (NA-before-due). HIGH false-positive. DROP.

**2. OVERLAP MAP (everything is already covered or noise):** stale backups → **T2 retention**; stale logs → **log_cleanup cron**; config sanity/abandoned → **Config Auditor** (+ the .bak are operator artifacts); operational empties/freshness/cron-misses → **Control Tower** (freshness + cron adapter); file-integrity/unexpected files → **Security Monitor**; cron health → **Cron Officer / cron-watchdog**. The advisory category adds little not already monitored.

**3. FALSE-POSITIVE INVENTORY (the whitelist any scanner would need):** 27 cron-invoked `.py` (reconstruct_excursions, backup_retention, capture_metrics_baseline, the gemini_*, cron_officer, system_manager, fetch_*, reconcile_*, eod_*, db_retention, disk_monitor, control_tower/runner, …); ~20 manual/recovery/deploy tools (approve_ssh_keys, check_vm_state, copy_gate, security_monitor, alert_watcher, backup_restore_drill, t2_cnc_gtt_realtest, sr_detector_backfill, generate_crontab, …); the AngelOne stub adapter; ABC base classes (preflight/base); 5 package `__init__.py`. ⇒ the "unused/dead" whitelist would be ~50 entries and brittle.

**4. NOISE ESTIMATE:** placeholder ≈ 1–2 (1 real); NotImplementedError = 14 (all false); duplicates = 5 (all false `__init__.py`); unused/orphan ≈ 40+ (nearly all false); dead-code ≈ dozens (mostly false); empty resources ≈ several (false). Only placeholder is low-noise — and it has nothing to find.

**5. OPERATOR VALUE (solo-dev bar):** for a single dev who knows the codebase, ZERO of these surface something Rama would act on today. The 1 real TODO is already tracked (FIX-109). The .bak configs are a 2-file manual `rm`.

**6. SAFETY (design constraint, confirmed): any advisory scanner MUST be READ-ONLY** — a report line only; NEVER delete/modify/quarantine/move. Blast radius then minimal (a report). This is non-negotiable for the later design IF anything is built.

**7. RECOMMENDED MVP = effectively NONE / tiny.** Strong recommendation: **do NOT build the weekly advisory scanner** — the reliable categories (placeholder/dupe) have ~0 findings; the high-value-sounding ones (unused/dead/orphan/empty) are false-positive factories on this cron-heavy repo; logs/backups/config are already owned. If Rama wants ANY artifact, the ONLY defensible one is a **forward-looking placeholder-debt tracker** (TODO/FIXME/HACK only; EXCLUDE XXX + NotImplementedError + return-None/pass/mock; scoped to operational dirs) whose value is purely TREND (alert when new debt crosses a threshold) since today it emits ~1. Everything else DROPPED. Related: [[t2_backup_retention_investigation_29jun]] · [[control_tower_phase1a_29jun]] · [[feedback_foundation_rules]].
