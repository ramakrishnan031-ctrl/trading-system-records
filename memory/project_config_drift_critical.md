---
name: Config parameter drift - CRITICAL architectural issue
description: Hardcoded defaults bypass config values; must build ConfigValidator post-paper
type: project
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
**CRITICAL FINDING (2026-04-28): Config parameter drift across codebase**

Examples discovered during paper testing:
1. `signal_expiry_sec`: config=600, code default=60 (signals expired prematurely)
2. `entry_end_time`: changed in YAML but some paths had hardcoded windows
3. `daily_loss_limit` vs `daily_loss_limit_pct` confusion (two config fields, only one used)
4. `_INVARIANT_TOLERANCE`: hardcoded 0.01 in fund_manager.py, not configurable
5. `in_flight_release_fn`: defaulted to None instead of mandatory injection

**ROOT CAUSE:** No single source of truth enforcement. Modules accept config but fall back to hardcoded defaults when params missing or not passed.

**POST-PAPER PRIORITY: ConfigValidator (v2.1)**

Implementation approach:
1. Pydantic schema for system_config.yaml - typed, validated at load
2. Mandatory config injection via `__init__` - no optional defaults allowed
3. Startup assertion: compare loaded config vs actually-used values
4. "vlookup" audit: one config change must propagate everywhere
5. Fail startup if ANY module uses hardcoded fallback instead of injected config

**Why:** Paper testing surfaced 5 bugs where config values weren't reaching modules. Each required code change + restart. In live trading, this would cause unexpected behavior that's hard to diagnose.

**How to apply:** 
- Week 2 paper: document all drift cases found
- Post-paper v2.1: implement ConfigValidator
- Enforcement: CI check that no module has default values for config params
