---
name: strategy-change-deps-03jul
description: "Operator guide — what's AUTOMATIC vs MANUAL when adding/deleting/renaming a strategy (full dependency map, 03-Jul investigation)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3b1fa8b6-3ab8-4f25-a39a-0a6806490486
---

READ-ONLY investigation (03-Jul-2026, 3 parallel agents + first-hand trace +
empirical boot test). Answers: on strategy ADD/DELETE/RENAME, what applies
automatically vs needs a manual step.

## The dependency chain (two independent namespaces, currently shipped 1:1)
`scanner_name` (Chartink URL path + `scan_webhook_map` KEY) is mechanically
SEPARATE from `strategy_name` (the YAML `name:` field + `scan_webhook_map`
`strategy:` VALUE + the loaded-strategies dict key). All 15 are spelled
identically today, which MASKS that they are two different things.

Runtime flow: Chartink scanner POSTs `/webhook/<scanner_name>` →
`signals/webhook_receiver.py:436` **404 if scanner_name ∉ scan_webhook_map**
(no signals row) → (optional body `scan_name` normalized `lower().replace(" ","_")`
must == scanner_name else **400**, webhook_receiver.py:493) → queued →
`signals/signal_processor.py:676-696`: `scan_webhook_map[scanner].strategy` →
`strategies[strategy_name]` → **`REJECTED_UNKNOWN_STRATEGY`** if either misses
(silent to Chartink; DB status + log only). `trades.strategy` stores the
RESOLVED strategy_name as a snapshot.

## The 3 config files that must stay in sync (the manual surface)
1. `config/strategies/<name>.yaml` — the strategy definition (`name:` field is authoritative, NOT the filename).
2. `config/scan_webhook_map.yaml` — `scanners: <scanner_name>: {strategy: <name>, chartink_url: ...}`. Runtime-critical routing.
3. `config/chartink_scanners.yaml` — flat `scanner_name: url` for the P17 preflight HEAD check (WARNING-only, see below).
Plus the **Chartink side** (external): the scanner itself + its webhook URL `/webhook/<scanner_name>`.

## LOADING is dynamic
`StrategyLoader.load_all_strategies` (strategies/loader.py:57) does
`sorted(strategies_dir.glob("*.yaml"))` — every `config/strategies/*.yaml` is
auto-enumerated at boot, keyed by the YAML `name:` field. Add/remove/rename a
YAML → auto-picked-up on next **trader restart** (loaded ONCE, no hot reload —
[[deploy_requires_restart]]).

## What is startup-BLOCKING vs runtime-only vs warning (empirically verified)
- **BLOCKING** — a malformed/schema-invalid strategy YAML → `ConfigSchemaError`
  (main.py:2330 + startup_checks `check_strategy_configs` → `blocking_failures`).
- **BLOCKING** — a structurally-invalid `scan_webhook_map.yaml` (missing
  `strategy:` key, bad url, extra key, dup scanner key) → pydantic in `load_all()`.
- **NOT blocking / runtime-only** — a `scan_webhook_map` entry pointing to a
  strategy with no YAML (the de-synced-rename / dangling case). **The S10
  cross-check `StrategyLoader._validate_scan_webhook_map` (loader.py:93) is DEAD
  CODE in production** — NO production caller passes `scan_webhook_map_path`
  (main.py:2330, startup_checks:1222, both preflight checks, control_tower all
  omit it; only `tests/unit/test_strategies.py` passes it). Verified empirically
  03-Jul: injected a dangling scanner→nonexistent-strategy into a temp config,
  ran main.py's exact boot sequence → load_all + load_all_strategies BOTH PASSED,
  boot continued. Fails only when a signal for that scanner arrives.
  ⚠️ One 03-Jul agent WRONGLY claimed this is "caught loudly at boot" — it is NOT.
- **WARNING only** — Chartink URL unreachable (`check_scanner_connectivity`,
  startup_checks:1534 → `warnings`, and skipped entirely on COLD start). A stale/
  placeholder `chartink_scanners.yaml` URL never blocks the trader.

## NO hardcoded strategy names in the trading/reporting path
Exhaustive grep: **zero** production `if strategy == "..."` branching (all such
hits are test fixtures). LONG/SHORT comes from the YAML `direction` field;
intraday/positional `bucket` from `intent` (NOT name-prefix matching — the
`"positional"` literals in risk_engine/position_sizer are the intent-derived
bucket). `tier_multipliers` (system_config.yaml:151) are keyed HIGH/MEDIUM/LOW
(score tier), NOT per-strategy. `dynamic_by_winrate` → `capital/performance_allocator.py`
iterates names dynamically. Slippage `by_strategy` override map is **empty `{}`**
today (a rename WITH an override present → config-auditor WARN, not a break).

## Reports / alerts / GUI all enumerate DYNAMICALLY (no fixed list anywhere)
- EOD System Manager (`system_manager.py` `_enabled_strategy_names` globs yaml ∪ traded) — [[eod_alert_enh_03jul]].
- Cron Officer morning STRATEGY STATUS (`strategy_status.py:71` globs yaml) — the authoritative "all configured" alert enumerator.
- daily_trade_review + old daily_report — GROUP BY `trades.strategy` / glob for min-scores.
- GUI dashboard (127.0.0.1:8500 = ops_dashboard, ONE app) strategy_tower: `config_reader.get_strategies` globs yaml FRESH per request, UNION with DB `GROUP BY strategy`; each row flags `configured` + `enabled`.
- `strategy_metrics` table: no seed; written per `SELECT DISTINCT strategy FROM trades` (trailing 30d closed). Configured-but-never-traded → no row (why system_manager unions with the glob).
- Reports/GUI re-derive per run → a yaml add/delete shows there WITHOUT a trader restart (separate cron scripts + separate dashboard process); only the live trading pipeline needs the restart.

## PER-OPERATION GUIDE
### ADD a strategy
- AUTO (next trader restart): strategy loads (glob); appears in every report/alert/dashboard; strategy_metrics row on first closed trade.
- MANUAL: (1) create `config/strategies/<name>.yaml`; (2) add `scan_webhook_map.yaml` scanner entry `strategy: <name>` — **without this the strategy loads but NO signal can ever route to it (silent dormancy)**; (3) add `chartink_scanners.yaml` URL; (4) create the Chartink scanner + point its webhook at `/webhook/<scanner_name>`; (5) restart trader.
- GOTCHA: adding only the YAML (no map entry) = dormant-but-looks-configured (shows in status/dashboard as configured, never trades).

### DELETE a strategy
- AUTO: drops from all config-derived views on restart; trade-derived views/`strategy_metrics` keep historical rows (genuine history, not stale refs).
- MANUAL: (1) remove/disable the `config/strategies/<name>.yaml` (or set `enabled: false`); (2) **remove its `scan_webhook_map.yaml` entry** — if left, an inbound signal for that scanner → `REJECTED_UNKNOWN_STRATEGY` at runtime (not a boot error); (3) remove `chartink_scanners.yaml` entry; (4) disable/delete the Chartink scanner; (5) restart. (`enabled: false` alone keeps it loaded but gated OFF by the strategy-control resolver — cleaner than deleting if temporary.)

### RENAME a strategy (RISKIEST — flag)
Two failure points depending on which identifier drifts:
- Change YAML `name:` but NOT the map's `strategy:` value → boot OK, but signals 200-ACCEPTED then die at `signal_processor.py:691` `REJECTED_UNKNOWN_STRATEGY` (silent to Chartink).
- Change the map KEY (scanner_name) but Chartink still POSTs the old URL → **404** at the webhook edge.
- MANUAL (do ALL together): rename `config/strategies/<name>.yaml` + its `name:` field; update `scan_webhook_map.yaml` (key and/or `strategy:` value as intended); update `chartink_scanners.yaml`; update the Chartink scanner name + webhook URL (+ its `scan_name`/display if the body sends `scan_name`, else 400); update any `by_strategy` slippage override if one existed; restart.
- HISTORY SPLIT: old `trades`/`signals`/`strategy_metrics` rows keep the OLD name; new rows get the NEW name → every trade-derived report/dashboard shows the strategy as TWO entries until history ages out. No migration renames history (and none should — it's a faithful record).
- Renaming ONLY the file (keeping `name:`) changes nothing (loader keys on `name:`).

## Parity
Strategy handling is mode-agnostic — same code/config both paper and live; no
paper/live branch in loader or signal_processor strategy resolution.
`force_intraday_only=true` rewrites every strategy's intent→INTRADAY at load in
BOTH modes ([[project_master_state]]).

## Out-of-scope latent finding (flagged, not fixed)
`scripts/gemini_premarket_brief.py` selects column `sharpe_ratio` but the
`strategy_metrics` schema column is `sharpe` — possible latent name mismatch
(enumeration itself is dynamic/fine). Separate from this investigation.
