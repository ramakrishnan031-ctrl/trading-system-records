---
name: E.1 / H-17 time_authority sweep landed (19-Apr-2026, commit 1a6c49c)
description: Phase E.1 - datetime.now() -> now_ist() in 5 production modules; H-11 folds in as subset; two deliberate exemptions documented inline; 1597->1603 green
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
**Commit:** `1a6c49c` (19-Apr-2026 11:12 IST)
**Subject:** `E.1 / H-17 | time_authority sweep — datetime.now() -> now_ist() in 5 files`

**One-line:** Replaced raw `datetime.now()` calls with `core.time_authority.now_ist()` at 6 call sites across 5 production modules, closing H-17 (H-11 is a strict subset, folded in).

**Sites swept:**
- `orders/shadow_tracker.py:_parse_ts` (2 sites: empty + invalid branches)
- `orders/order_reconciler.py:_now_ist`
- `capital/risk_engine.py:approve` (today = now_ist().date())
- `reports/daily_review.py:_now_ist_date`
- `alerts/critical.py:write_critical_sentinel`

**Deliberate exemptions (inline H-17 SKIP comments added):**
- `core/state_store.py:_now_ist_iso` — state_store sits below time_authority in the layering; importing here would invert dep direction.
- `utils/startup_checks.py:check_config_files` — pre-init config-file gate that runs BEFORE time_authority is constructed; only needs `datetime.now().year` to pick `nse_holidays_<year>.yaml`.

**Test count delta:** 1597 → 1603 (+6)
**New test file:** `tests/unit/test_time_authority_sweep.py` (6 regression guards via `unittest.mock.patch` on the imported `now_ist` binding; risk_engine uses source-text + import-binding guard)
**Phase A gate:** 15/15 green

**Deferred-EF tracker deltas:** none (E.1 is pure audit closure; no EF changes)
**Architectural locks added:** the two SKIP comments codify the layering invariant (state_store & pre-init startup_checks bypass time_authority by design).

**Why:** Close H-17 before capital/order-lifecycle commits (E.2+) so all downstream timestamping flows through time_authority.
**How to apply:** New production code MUST use `core.time_authority.now_ist()`; the only valid exemptions are the two documented above.
