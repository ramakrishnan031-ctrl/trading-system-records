---
name: strategy-direction-investigation-17jul
description: "Strategy-direction classification investigated (READ-ONLY) — direction ALREADY structured (StrategyConfig.direction, not name-derived); outcome derives from it; declared==actual perfect ⇒ NO conflict, stop-condition NOT triggered. Q6 build shape recorded. Report 082f610 UNPUSHED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
---

# Strategy-direction classification — INVESTIGATED 17-Jul (READ-ONLY, feeds regime Phase 1)

Report `docs/audit/strategy_direction_investigation_17jul2026.md`, commit **`082f610` UNPUSHED**
(docs-only). Feeds the regime-ranking build (needs each strategy's LONG/SHORT). Folds in the
ChatGPT addendum (outcome-based classify · source priority signal>order>trade · persist ONE field ·
auto-detect+notify like the cron registry · DIRECTION_CONFLICT · robust to renames).

## ⭐ HEADLINE (and the addendum STOP-CONDITION was NOT triggered)
- **Q1: a strategy→direction mapping ALREADY EXISTS and is STRUCTURED** — `StrategyConfig.direction`
  (`strategies/schema.py:58`), required + enum-validated to LONG|SHORT (`:24`,`:143`). **NOT
  name-derived.** All 16 YAMLs declare it.
- **Q2: the outcome is DERIVED from that config field, not independent.** The Chartink webhook carries
  **NO side**; the `signals` table has **NO side column**. `signal_processor.py:778/:812-813` reads
  `strategy_obj.direction` and computes `side = BUY if LONG else SELL` ⇒ flows to
  `orders.transaction_type` + `trades.direction` (`order_placer.py:918/:953`). So priority-1 "signal
  side" is not a stored field (= config direction at processing); priority-2/3 derive from it.
- **⭐ EMPIRICAL: declared == actual PERFECTLY** for all 11 traded strategies; **no strategy has both
  directions** (`HAVING COUNT(DISTINCT direction)>1` = 0 rows). ⇒ **ONE authoritative source, no
  conflict ⇒ STOP-CONDITION NOT triggered; proceed to Q6.**
- **⚠️ THE NUANCE for ChatGPT:** because the outcome is *computed from* the declaration, an
  outcome-based classifier **reproduces `StrategyConfig.direction` and cannot itself catch a config
  mislabel** (it propagates + "agrees"). True independence exists ONLY for **`ORPHAN_ADOPTION`**
  (broker position, no local trade; `order_reconciler.py:21`) — which is exactly where
  DIRECTION_CONFLICT earns its keep.

## Q3 registration · Q4 pattern-to-mirror · Q5 fragility
- **Q3:** a strategy = config files discovered at boot (`loader.py:61` globs `config/strategies/*.yaml`
  + S10 cross-validates `scan_webhook_map.yaml`, `:84-143`). A NEW strategy appears via (a) a new YAML,
  (b) a webhook with a new `scanner_name`. Auto-detect must watch BOTH (loaded YAMLs ∪ distinct
  `signals.scanner`/`strategy`).
- **Q4 (mirror this):** `cron_officer.py` `_auto_discover` (`:536-558`) flags crontab jobs "not in the
  registry"; `_roster_integrity` (`:593`,`:609-612`) surfaces `unregistered` at WARN → Telegram+EOD
  email. Pattern: enumerate ACTUAL → diff vs REGISTRY → flag NEW → notify; never mutate the registry
  silently at runtime.
- **Q5 name fragility is NARROW (display only):** `ops_dashboard/backend/services/strategy_tower.py:32-38`
  `_family_of` strips `_long`/`_short` for a UI grouping key (not a direction classifier);
  `strategies.html:332`. The **trading path never parses the name.** (Do NOT conflate
  `config_loader.py:1086 regime_pref_direction` = a BULL/SIDEWAYS/BEAR→multiplier map, unrelated.)

## Q6 build shape (RECOMMENDATION — not built)
Persist **ONE** `strategy_direction` registry (DB table or file mirroring `cron_registry.yaml`);
classify from the realized side (priority signal@processing→order→trade, *structurally never the
name*); **auto-detect** new strategies (loaded YAMLs ∪ new `scanner_name`) and **persist+notify**
(Telegram+email, mirror cron officer); route the regime module / ranking / allocator
(`long_short_skew_max`) / analytics / reports ALL to it and **RETIRE** the `_family_of` name-parse;
no-outcome-yet → classify at first signal (seed PENDING→L/S) or UNKNOWN-until-trade (Rama/ChatGPT
choice); **DIRECTION_CONFLICT** on an opposite side (never overwrite → flag → investigate); robust to
renames (key on stable strategy identity, not display name). Build seq: Web Claude → ChatGPT →
implement (new table = schema add → test-on-backup + Rama-pause).

Limits: 11/16 strategies have trades (outcome-verified); 5 are declared-only. One snapshot, no forward.

Related: [[regime-phase0-17jul]] · [[bk1-long-short-scanner-17jul]] · [[feedback-verify-the-finding-premise]]
