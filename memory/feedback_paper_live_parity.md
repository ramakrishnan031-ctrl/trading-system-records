---
name: Paper/Live parity enforcement (PERMANENT RULE)
description: MANDATORY - every code change touching paper OR live mode must check counterpart mode; commit message must include parity tag
type: feedback
originSessionId: 20e7cadd-4487-4f2d-87c2-551f76dc9808
---
Paper/Live parity is MANDATORY. Every code change touching paper OR live mode must consider both modes.

**Why:** Foundation Rule "Unified Execution Path" — same OrderManager/RiskEngine code path for both modes. Only the final broker adapter may differ. Violating this creates false-positive paper trials (bugs pass paper but break live, or vice versa). The commit 56e79a9 bug (paper orders stuck at SUBMITTED) was caused by exactly this kind of single-mode thinking.

**How to apply — BEFORE every commit touching paper/live code:**

1. IMMEDIATELY check if the same logic applies to the other mode
2. If YES → apply the fix to BOTH modes in the same commit
3. If NO → document WHY the divergence is architecturally necessary
4. Add a comment in the code explaining the paper/live difference
5. Run tests for BOTH modes
6. Include parity tag in commit message

## Commit message parity tag (REQUIRED)

Append to every commit that touches paper or live code:
- `Paper/Live parity: UNIFIED` — fix applies to both modes identically
- `Paper/Live parity: DIVERGENT-SAFE` — only one mode affected; reason documented
- `Paper/Live parity: NEEDS-SYNC` — counterpart mode needs follow-up work

Examples:
- `fix: order timeout handling (Paper/Live parity: UNIFIED)`
- `feat: paper fill simulation (Paper/Live parity: DIVERGENT-SAFE - live uses real Kite fills)`

## REQUIRED parity (must apply to both)
- Bug fixes in order flow
- State management changes
- Error handling improvements
- Validation logic
- Timeout handling

## ALLOWED divergence (must document why)
- Broker API calls (live uses Kite, paper simulates)
- Fill simulation (paper needs `_synth_fill`, live doesn't)
- Cost calculation (both modes but different data sources)
- `_paper_fills` dict (paper-only; live has real broker state via Kite API)

## Checklist before committing
- [ ] Traced code path in BOTH modes
- [ ] If paper has extra state, verified live doesn't need it
- [ ] If adding to a status set, verified it's correct/no-op in other mode
- [ ] Checked for duplicate event publishing paths
- [ ] Checked `docs/pending_skipped_items.txt` for known gaps
- [ ] Tests pass for both modes
- [ ] Parity tag in commit message

## Known idempotency guards
- Duplicate `OrderFilled`: `_fill_map.pop()` (first-wins) + OSM `InvalidTransitionError`
- Paper `_synth_fill` + `order_monitor` both can fire → OSM transition fails on second → publish skipped
