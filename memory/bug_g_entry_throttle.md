---
name: bug_g_entry_throttle
description: "Bug G entry throttle FULLY integrated — EntryThrottle class (global min-gap/burst + per-symbol cooldown), per-reason /metrics"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

**Bug G entry throttle — full integration (19-Jun-2026, commit c0554c6).** The global throttle was already wired into the signal_processor hot path in FIX-190 (575a1dc, both `place()` chokepoints); this completes it with a clean class + per-symbol cooldown + per-reason metrics.

- **`signals/entry_throttle.py` → `EntryThrottle`** (thread-safe). Single method **`admit(symbol)`** does an **ATOMIC check-AND-record** under one lock — deliberately NOT a split check()/record() (that has a TOCTOU window where a burst of concurrent workers all pass check() before any records — the exact race that let entries pile up). 3 gates, evaluated **global-first**: `min_gap` → `burst` → `per_symbol`. Each gate counts its rejections.
- **Three gates** (config under `signal_processor:` in system_config.yaml): global `min_gap_between_entries_sec: 20`, `entry_burst_window_sec: 60` / `entry_burst_max: 3` (≤3 placed entries per 60s), and **`per_symbol_cooldown_sec: 300`** (NEW — no re-entry of the SAME symbol within 5 min; stops rapid same-symbol churn: enter X 10:00 → exit 10:02 → re-fire 10:03 → blocked).
- **Single chokepoint:** signal_processor calls `self._entry_throttle.admit(symbol)` right before BOTH `self._placer.place(...)` sites (`_process_one` + `continue_from_gate`). On not-allowed → release the reservation + `_bump_metric("entries_throttled")` + raise `_PipelineReject("ENTRY_THROTTLED")` → signal status `REJECTED_ENTRY_THROTTLED`. **DROP on throttle (no queuing)** — signals are time-sensitive.
- **/metrics per-reason breakdown** (via `get_runtime_metrics` merging `EntryThrottle.metrics()`): `entries_throttled_min_gap` / `entries_throttled_burst` / `entries_throttled_per_symbol` / `entries_admitted`, alongside the aggregate `entries_throttled`.

13 unit tests (`tests/unit/test_entry_throttle.py`): each gate, burst reset, per-symbol same/diff/expire, global precedence, disabled, per-reason metrics, **thread-safety (50 concurrent admits → exactly burst_max pass)**, and the **19-Jun 5-in-5s burst replay → only 1 admitted** (min_gap dominates a tight burst). Old inline-`_throttle_admit` tests removed (superseded). Activates next restart. Parity: pure in-memory rate logic, identical paper/live. Related: [[fix_190_incident]], [[live_test_mode_permanent]].
