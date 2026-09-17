---
name: test-sentinel-isolation-24jun
description: "Full pytest suite on the LIVE VM emails test-written CRITICALs; autouse conftest sandbox now redirects any real-data_store sentinel write to tmp (24-Jun, 72cdfd5)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1a15ec3-5140-4531-93b5-a58f94e7260a
---

**Running the full pytest suite on the LIVE VM EMAILS test-written CRITICAL alerts.** The systemd alert-watcher consumes any `critical_alert_*.flag` in the real `data_store` and emails it. The 23-Jun full-suite run (during PART-1/2 validation) leaked **3 real emails**: a gemini "FAILED — no AI EOD review for 2026-06-01" (`tests/unit/test_fix142_final_cleanup.py` exercising the **new** `_emit_review_failure_alert` None-path **unmocked** — my change gave that path a real side-effect) + two preflight Phase-A 2026-06-22 CRITICALs (`test_preflight` → `scripts/preflight/deliver.py:77`). Both write via `alerts.critical.write_critical_sentinel(sentinel_dir=ROOT/data_store)`.

**Fix (PERMANENT, 24-Jun, commit `72cdfd5`):** `tests/conftest.py` autouse fixture `_isolate_real_sentinels` redirects ANY `write_critical_sentinel` whose `sentinel_dir` resolves to `<project>/data_store` (incl. the bare `"data_store"` default) → a per-test tmp sandbox; an explicit tmp dir (a test's own `tmp_path`) passes through unchanged, so sentinel-content tests still work. Patches the source module **and** the module-level importers (`telegram_notifier`/`cron_watchdog`/`cron_officer`; gemini + preflight use function-level imports → caught by the source patch). **Production sentinel/alert path UNCHANGED** — tests-only isolation. Regression test `tests/unit/test_sentinel_isolation.py`; verified **250 sentinel-writer tests pass with ZERO new flags** in the real data_store.

**Why:** test infra must never touch the live alert pipeline. **How to apply:** any new test that triggers `write_critical_sentinel` (directly or via `run_review`/preflight/cron_*) is auto-sandboxed — no per-test work needed; never point a test's `sentinel_dir` at the real `data_store`. The 3 leaked `.delivered` were moved to `/tmp/leaked_test_sentinels_24jun/` (already emailed; were `.delivered` not `.flag`, so they would not re-fire). See [[gemini_log_review_windowing_23jun]] (the failure sentinel), [[live_test_mode_permanent]], [[may31_sentinel_cleanup_19jun]].
