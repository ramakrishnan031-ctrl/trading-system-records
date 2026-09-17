---
name: strategy-direction-registry-17jul
description: Strategy-direction registry DONE + DEPLOYED 17/18-Jul — YAML registry + daily auto-detect/notify/confirm/DIRECTION_CONFLICT; GUI name-parse retired; consumers routed to canonical StrategyConfig.direction. UNBLOCKS regime Phase 1.
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
---

# Strategy-direction registry — DONE + DEPLOYED (17→18-Jul-2026)

Report `docs/audit/strategy_direction_registry_done_17jul2026.md`. **Tag
`deploy-18jul-strategy-registry` → `c2f82ff`; PC == origin == VM bare == `44fdbcb`.** No schema
migration (YAML registry; v44 unchanged). Backup `pre_deploy_strat_registry_20260718_002539.db`.
**⭐ UNBLOCKS regime Phase 1** — the long-vs-short tilt now has a reliable per-strategy direction.

## The model (built on the investigation [[strategy-direction-investigation-17jul]])
`StrategyConfig.direction` (`strategies/schema.py:58`, enum-validated) is **already** the
authoritative structured source (order side + `trades.direction` derive from it). So this is **NOT**
a reclassifier or a duplicate field — it's a REGISTRY + auto-detect + notify + confirm + conflict,
and it **NEVER overrides** `StrategyConfig.direction`.

**THREE separate concepts (ChatGPT mandate)** in `config/strategy_direction_registry.yaml` (keyed on
`StrategyConfig.name`, the stable machine identity):
- `direction` LONG|SHORT (mirrors the config field) · `registration_status` PENDING|CONFIRMED ·
  `health` OK|DIRECTION_CONFLICT · + first_seen + evidence. Seeded with the 16 current strategies.

## Pieces (2 code commits `26885bb` feature + `c2f82ff` routing)
- `core/strategy_direction.py` — canonical accessor (`build_direction_map`/`canonical_direction`
  reading `StrategyConfig.direction`, never the name) + registry I/O.
- `scripts/strategy_registry_officer.py` — daily **16:22 Mon-Fri** (in cron_registry + crontab).
  Mirrors `cron_officer._auto_discover`(:536)+`_roster_integrity`(:593): enumerate loaded YAMLs ∪
  distinct `signals.scanner`/`strategy`, diff vs registry, register UNSEEN PENDING (direction from
  config) + **notify Telegram+email** (reuses `TelegramNotifier` + critical-sentinel email — no
  parallel notifier); PENDING→CONFIRMED on first filled trade (silent); the daily job OWNS writes;
  no-change run is SILENT. **Zero code for future strategy additions.**

## ⭐ DIRECTION_CONFLICT — premise CORRECTED (FIX-182)
The instruction placed the check on ORPHAN_ADOPTION assuming an adopted orphan is a
strategy-attributed trade. **FALSE:** post-FIX-182 the system does NOT adopt untracked broker
positions — they're human orders (`trade_id=None`, no strategy; `order_reconciler.py:1461`), only a
system-oversell is flattened. **There is no orphan-with-strategy to check.** So the conflict check is
a **daily realized-vs-declared DB scan**: any FILLED `trades.direction` ≠ declared ⇒
health=DIRECTION_CONFLICT, declared value KEPT (never overwritten), notify (on the OK→CONFLICT
transition). Additive, no live trade-path hook; config-path trades can't diverge, so a fire is a
genuine anomaly (dual-direction strategy, config-vs-history, future external import). Mirror of
[[feedback-verify-the-finding-premise]].

## Consumer routing (behaviour-neutral; audit found it SMALL — the live path is already canonical)
- **Allocator** reads `candidate.side` ← `strategy_obj.direction` (`signal_processor.py:812`) — already canonical.
- **Regime module** consumes no strategy direction today. **Reports** intentionally read realized `trades.direction`. **GUI direction value** already from YAML.
- ✅ **RETIRED the ONE name-parse:** GUI `strategy_tower._family_of` (`endswith("_long")/("_short")`) → strips the token matching the structured `basic.direction`. Byte-identical for current naming.
- ✅ **Routed `eod_squareoff`** EOD-summary 🟢/🔴 grouping from a trade-VOTE to a canonical direction map (built by the caller so `_format_summary_body` stays PURE; default None → the vote → byte-identical). It was the one non-name, non-canonical strategy-direction guess.

## Validation
Tests 18 (12 officer/core + 6 routing) + RED-on-old (GUI 3F, eod 3F on base). Regression 44F/4863P
**zero-attributable** (43 known env + 1 calendar: `test_daily_trade_review` weekend-skip on an
UNTOUCHED file — the session crossed into Sat 18-Jul; Friday runs passed it → add to
[[pc-test-env-hygiene]] calendar-gated set). **⭐ Officer validated on REAL VM data
(`main() --dry-run`): new=[] · confirmed=[the exact 11 BK-1-traded strategies] · conflict=[] ·
total=16** — 0 new (no notify storm), 0 conflicts (declared==actual everywhere). First live run Mon
20-Jul 16:22 (weekends skip). **Deploy-reset self-heals** (officer re-derives status/health from DB).

Related: [[strategy-direction-investigation-17jul]] · [[bk1-long-short-scanner-17jul]] · [[regime-phase0-17jul]] · [[feedback-verify-the-finding-premise]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 533 B (budget 300 B). The index now carries a hook and this link.

- 🧭✅🚀 **[STRATEGY-DIRECTION REGISTRY — DEPLOYED 18-Jul](strategy_direction_registry_17jul.md)** — YAML registry + daily officer (16:22 Mon-Fri) mirroring the cron officer: auto-detect → PENDING → notify → CONFIRM on first fill → **DIRECTION_CONFLICT** (declared KEPT). **3 fields; `StrategyConfig.direction` stays the ONE source.** Conflict = a daily realized-vs-declared DB scan (FIX-182 correction). No migration. Tag →`c2f82ff`. PROVEN: 0 new, 11 confirmed, 0 conflicts. [[strategy-direction-registry-17jul]]
