---
name: project-fix133-complete
description: "FIX-133 batch6 complete -- Items 19,21,22,24,28,29,30; replay + dynamic sizing + entry windows + metrics + angelone + multi-account + trade journal"
metadata: 
  node_type: memory
  type: project
  originSessionId: d26ce7c8-a930-497d-bfb6-d94acc035027
---

FIX-133 batch6 landed in commit 38fa4e9, pushed to VM. Schema v19.

**Why:** Operational tooling, strategy refinement, observability, and foundation for multi-broker/multi-account expansion.

**How to apply:** All items are live. Trade journal cron at 16:10 IST Mon-Fri. Strategy entry windows are now production values (TEMP PAPER windows removed).

## Items delivered

| Item | What | Tests |
|------|------|-------|
| 19 | scripts/replay_signals.py — read-only signal replay CSV | 5 |
| 21 | perf_weight 2x cap + PositionSizingConfig dynamic fields | 5 |
| 22 | Per-strategy entry windows (gap_fade 09:15-09:45, gap_go -11:00, positional -14:00, default -15:00) | 5 |
| 24 | /metrics + /metrics/prometheus endpoints on healthcheck :8080 | 4 |
| 28 | broker/angelone_adapter.py stub + BrokerConfig in system_config | 7 |
| 29 | Multi-account warning + accounts_multi_example.csv | 3 |
| 30 | trade_journal table (schema v19) + scripts/trade_journal.py + cron 16:10 | 5 |

## Key changes
- **Schema v19**: +trade_journal table; state_store EXPECTED_SCHEMA_VERSION=19
- **Strategy YAMLs**: all 15 files updated from TEMP PAPER to production entry windows
- **Config**: broker.primary/fallback/fallback_enabled; position_sizing.dynamic_by_winrate/min_multiplier/max_multiplier
- **test_strategies.py** updated: positional entry_end assertion changed from "15:20" to "14:00"

## Test counts
- Baseline: 2367 -> New: 2401 (+34)
- Pre-existing failures: 11 (9 Windows PermissionError + 2 Pydantic deprecation)
- Zero new regressions

## Related memories
- [[project-fix132-complete]] — predecessor batch (Items 8,9,10,11,15)
- [[project_vm_architecture_locked]] — VM deployment target
