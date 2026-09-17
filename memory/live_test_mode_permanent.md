---
name: live_test_mode_permanent
description: "PERMANENT live_test_mode caps — RAISED 23-Jun to max_open=5, max_entries_per_day=10, max_consecutive_losses=5 (was 4/6/2); active bug-hunting on live"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

**live_test_mode PERMANENT values (set 19-Jun, commit 6b6979c; caps RAISED 23-Jun on resume, commit 7ff24b2):**
`risk.live_test_mode: true`, `live_test_max_open_positions: 5`, `live_test_max_entries_per_day: 10` in `config/system_config.yaml` (were 4 / 6). When `mode=live`, `main.py` overrides base `risk.max_open_positions` and `max_daily_trades` with these — effective live caps = **5 positions / 10 trades per day**. Also raised (both modes): `max_consecutive_losses` 2→**5**, base `max_daily_trades` 20→**10** (paper parity). Confirmed live in the running process 23-Jun (`FIX-190 LIVE_TEST_MODE ACTIVE: max_open_positions=5, max_daily_trades=10`). Caps raised because [[fix-191-false-softkill-23jun]] resume needed the session to continue past the old 2-loss consecutive cap.

**Why (Rama's strategy):** active bug-hunting on LIVE with controlled exposure. 4 concurrent positions exercises concurrency/race paths (the kind that produced [[fix_190_incident]]); small qty/trade (typically 1-2 shares) on ₹10k naturally caps daily loss; more trades = more bug discovery. **PERMANENT — NOT temporary, no revert.** No auto-disable mechanism exists (it's manual-only by design); stays ON until Rama edits the config.

**Implementation note:** the config is FLAT fields under `risk:` (`live_test_mode` / `live_test_max_open_positions` / `live_test_max_entries_per_day`), NOT a nested `live_test_mode:` block. `RiskConfig` is `extra="forbid"`, so do NOT add `required_clean_days`/`manual_disable_required` — they'd break config loading and map to nothing (there's no auto-disable to configure). The live_test_* fields have no validator constraint. Activates on next service restart (deploy ≠ restart). The System Manager (check 1) reports actual-vs-effective against these caps. Related: [[task_5_system_manager]], [[fix_190_incident]].

**Preflight envelope aligned (24-Jun, commit 9919652):** the `live_test_mode_caps` CRITICAL drift-check (`scripts/preflight/checks/config_integrity.py` → `LIVE_TEST_EXPECTED_MAX_OPEN`/`_MAX_ENTRIES`) was stale at **4/6** → would fire a false CRITICAL "caps drift" at the 08:30 preflight against the live 5/10. Updated the expected envelope to **5/10** to match these deliberate caps (it's the guard's expected value, NOT the live source — the live system reads `risk.*` from system_config.yaml). The check covers open+entries only (not consec_losses). Preflight is **alert-only** (`run_on_demand_if_missed` "never blocks startup"), so it never gated trading — this just silences the daily false CRITICAL. See [[test-sentinel-isolation-24jun]].
