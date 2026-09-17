---
name: artifact-baseline-reconciliation-19jul
description: "19-Jul READ-ONLY: reconciled the live-DB fingerprint that moved between batches (6df0c09a@11:14 → a7a1de53@18:00) — BENIGN: the sole writer is gemini_weekly_patterns (cron 0 18 * * 0, monitored:true) writing ONE cron_heartbeat row; table diff vs the 11:12 census snapshot = only cron_heartbeat +5, every sensitive table (signals 32928/trades 361/orders 610/fm_ledger 2160/kill_switch_state 1) identical; no token; service down; JSONL still 7,827@16-Jul. STANDING RULE: within-batch identity (before==after) ≠ cross-batch identity; the live DB advances on monitored-cron heartbeats + the Sunday vacuum even while DOWN. Named the 'attribution gloss' class; sweep queued for after Monday."
metadata:
  node_type: memory
  type: project
  originSessionId: 35afb62d-26b3-4c8b-a62f-fa6b431ad21b
  modified: 2026-07-20T14:23:55.397Z
---

**ARTIFACT BASELINE RECONCILIATION (19-Jul-2026, READ-ONLY, docs-only).** Report
`docs/audit/artifact_baseline_reconciliation_19jul2026.md`. Prompted by: the live-DB fingerprint moved
`6df0c09a…`(11:14) → `a7a1de53…`(18:00) between batches while a batch reported "all three byte-identical"
(a within-batch check that didn't catch the cross-batch move).

## ⭐ VERDICT: BENIGN — one weekly Gemini heartbeat row
- **Writer = `gemini_weekly_patterns`** (`config/cron_registry.yaml:672-686`, **`cron_expression: 0 18 * * 0`
  = 18:00 every Sunday**, `monitored:true`, `market_day_only:false`) → `cron_heartbeat` **id 2421 SUCCESS @
  18:00:17.330**; live DB mtime `18:00:17.332` matches to the ms.
- **Table diff live vs the preserved census snapshot** (`/home/ubuntu/preserved/signal_census_19jul2026/trading_system_snapshot_20260719.db`, taken 11:12, `mode=ro`): **ONLY `cron_heartbeat` moved (2398→2403, +5)**; every other table identical. The +5 = ids 2417-2421 (4× `eod_cleanup` SKIPPED 11:13-11:14 = the prior throttle `--db copy` disclosure + 1× gemini @18:00). In the 16:05→20:30 window: **+1 row.**
- **NOT moved (all identical to snapshot):** `signals`=32,928 · `trades`=361 · `orders`=610 · `fm_ledger`=2,160 · `kill_switch_state`=1. **No schema change. No `zerodha_token.json`** in `data_store/session/` (only `gui_secret_key`). Service `inactive`. Nothing in the not-benign set moved ⇒ no STOP.
- **JSONL unchanged:** 7,827 lines, mtime 16-Jul 18:15:21, `f7c964fd…` — no contamination.
- **cp before==after** proved my probe wrote nothing; PC stubs (`data\…db` `e3b0c442` 0B · `data_store\…db` `aff1642c` 884KB) are NOT the baseline — earlier batches fingerprinted the VM path correctly.

## ⭐ CLEAN BASELINE — the Monday reference (VM `trading-system:/home/ubuntu/systems/trading-system/`)
- `data_store/trading_system.db` = **`a7a1de53a0e398a0…`** · 89,968,640 · mtime 2026-07-19 18:00:17.
- `data_store/v3/forward_shadow_fs-v1.jsonl` = **`f7c964fd…`** · 4,526,565 · **7,827 lines** · 16-Jul 18:15:21.
- `data_store/analytics.db` = **`bb229f44…`** · 24,133,632 · 02:30:04 (Sun `db_retention --vacuum`).

## ⭐⭐ STANDING RULE (B2) — WITHIN-BATCH IDENTITY ≠ CROSS-BATCH IDENTITY
"byte-identical before→after" proves only that **THIS batch** did not write. It does **not** prove the artifact
is unchanged since the last **recorded** baseline. **Both checks are needed; a moved cross-batch baseline must
be FLAGGED + reconciled (writer identified, benignity verified), never silently adopted.** Correct phrasing:
"unchanged *by this session*; the standing baseline advanced X→Y via <writer>, benign."

## ⭐ THE LIVE DB IS EXPECTED TO KEEP CHANGING WHILE DOWN (B3)
Two mechanisms: (1) **`monitored:true` crons write a `cron_heartbeat` row on completion** even on non-trading
days (seen today: backup_retention 02:00 · monitoring_canary 08:20 · cron_officer_briefing 09:20 ·
gemini_weekly_patterns 18:00-Sun); (2) **the Sunday `db_retention --vacuum` (02:30) rewrites the file** (sha256
changes, row counts don't → why analytics.db mtime is 02:30). ⇒ a changed hash is **benign iff explained by (1)
or (2) AND no sensitive table moved.** **📌 Monday:** by afternoon the live DB differs completely (it trades) —
the post-session check must be **logical/row-level** (did signals/trades/orders grow as expected; JSONL +1 OOS
day with real `sim_R`), **NOT hash-equality** against this Sunday baseline.

## ⭐ THE "ATTRIBUTION GLOSS" CLASS (§C) — sweep QUEUED for after Monday, NOT run
A summary/decision file states an inference its cited source **never made**, and cites that source as authority.
Instance: `06_performance_allocator.md` asserted "masked by the concentration cap … Q9 batch-4 applies here" but
batch-4 reasoned the **opposite, correctly**. **Dangerous HERE because** the decision files/briefs are designed
to be read **instead of** the audits ⇒ a summary-time gloss becomes the operative record and the correct
original is never re-read. **The tell:** a summary *sharper/more actionable* than its cited section — verify
against the section, not the summary. Sweep queued: decision files/briefs for inferences an audit didn't make.

## Queue after Monday + Monday reminders
⚠️ **20-Jul: `check_scanner:703` CLOSED — REFUSED WITH EVIDENCE**; real sibling = `scripts/preflight/checks/signals.py:28`. [[preflight-401-third-sibling-20jul]]
Boot-path pair (careful loop): live-seed extraction from `main()` + `check_scanner:703` · live-path quote
observability · 403 signal-count · deferred `event_type`/`Rejected (Sizing/Capital)`/`build_taxonomy_map()` ·
wave-7 · Rs 0.29 SL · **MEMORY.md compaction (snapshot taken 20:13:38)** · **NEW: the attribution-gloss sweep.**
⚠️ MONDAY 20-Jul: 08:15 TOTP · 08:15-09:00 boot · **pre-10:00 403s NORMAL** · 10:00 entries · 15:15 cutoff ·
15:17 squareoff · 15:50 eod_cleanup (0 rows) · 16:22 registry · **18:15 fwd shadow OOS day 4 — real `sim_R`, not nulls.**

Related: [[masking-premise-sweep-19jul]] [[candle-retention-perfallocator-feasibility-19jul]] [[throttle-selection-record-correction-19jul]] [[signal-mortality-census-19jul]] [[monday-preboot-readiness-19jul]] [[feedback-verify-rc-not-output]] [[migration-on-open-rule-14jul]]
