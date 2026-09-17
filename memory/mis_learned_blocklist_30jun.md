---
name: mis_learned_blocklist_30jun
description: "MIS Learned Blocklist BUILT (staged, branch mis-tradability-filter-30jun, NOT pushed) — source-free fix for NO_FILL Mechanism B; daily-list gated out in Step 0"
metadata: 
  node_type: memory
  type: project
  originSessionId: 064a7869-6371-4c00-a7fc-cd5fd33d479a
---

**MIS Learned Blocklist — BUILT 30-Jun, STAGED on branch `mis-tradability-filter-30jun` (from main 7103d74), NOT pushed (Rama owns push).** Source-free fix for NO_FILL **Mechanism B** (broker MIS-block: Zerodha refuses MIS orders on non-MIS-list stocks; `force_intraday_only` can't fall back to CNC → 19 trades/9 symbols wasted, all SHORT+LONG, 0 fills ever).

**Why this shape:** Step 0 (30-Jun) PROVED no clean/stable/authoritative machine-readable MIS source exists — Zerodha has **no API**; the list is **RMS-dynamic intraday**; the documented Google Sheets are fragile + mutually inconsistent (CSV export 400'd). So **NO daily list, NO `mis_tradable` table, NO cron fetch, NO schema change, NO external source.** Instead observe the broker's own 400 and learn.

**Design (root-cause, reuses excluded_symbols/liquidity-check/reject-label patterns):**
- NEW `core/mis_blocklist.py`: `is_mis_block_rejection(exc)` (matches "mis orders are currently blocked" in str(exc)+context) + `MisLearnedBlocklist` (persisted JSON `data_store/mis_blocklist.json`, `{SYMBOL: last_blocked_date}`, thread-safe, atomic write, restart-safe, corrupt→fail-open).
- **RECORD** (always-on, flag-independent — warms the list while dormant): `order_placer._handle_placement_failure` appends ONE guarded `record_block(symbol)` when `is_mis_block_rejection(exc)`; every existing step (mark FAILED + release capital) UNCHANGED.
- **RE-TEST TTL** (self-correcting): a symbol is blocked iff in store AND `(today − last) < ttl_days` (default 5 calendar days). TTL expiry → allowed through to re-test; fresh 400 refreshes the date; a trade self-corrects. Pure-persist would permanently false-drop a re-enabled stock — TTL is the only safe "persist across days".
- **DROP** (flag-gated): `secondary_screener.screen()` step-0 hook (before quote fetch; mirrors REJECTED_CIRCUIT_PROXIMITY) → `REJECTED_NOT_MIS_TRADABLE` (accepted by signals.status GLOB 'REJECTED*' — NO schema change). Applied ONLY when resolved product == MIS (future-proof for CNC; via injected broker-free `resolve_product` closure). LOGS every would-drop (symbol, direction, last_blocked_date, days-since, shadow/active).
- **Flag (`config/system_config.yaml` `mis_filter`, `core/config_loader.py` MisFilterConfig, default_factory):** `enabled: false` (default → DORMANT, byte-identical), `shadow: true` (log-only when enabled), `ttl_days: 5`. Rollout: OFF → enabled+shadow (validate vs real 400s) → shadow:false (active).
- Wired in `main.py`: ONE shared `MisLearnedBlocklist` → OrderPlacer (record) + SecondaryScreener (read).

**Tests:** `tests/unit/test_mis_blocklist.py` (22) — detection, record/persist/reload-restart, TTL expiry+refresh, fail-safe, handler records-on-MIS-only + existing-steps-unchanged + None-safe, screener active-reject (LONG+SHORT)/pass/non-MIS/shadow/**dormancy**. Suite green (config 65, screener, order_placer 123, full-suite-result pending in report). NO schema/table/cron/external-source. Parity: filter logic mode-identical (recording fires only on the live 400; paper never 400s).

Files: NEW `core/mis_blocklist.py`, `tests/unit/test_mis_blocklist.py`; MOD `core/config_loader.py`, `config/system_config.yaml`, `orders/order_placer.py`, `screening/secondary_screener.py`, `main.py`. Branch base from main (no a47efca cron) — different files, clean future merge except a trivial SYSTEM_MAP changelog-header co-edit. Relates to NO_FILL Mechanism B investigation + [[snr_detector_v1_27jun]].
