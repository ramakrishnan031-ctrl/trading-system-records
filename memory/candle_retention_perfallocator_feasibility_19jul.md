---
name: candle-retention-perfallocator-feasibility-19jul
description: "19-Jul READ-ONLY: (A) candle retention SURVIVES — D4's data path is safe (90d prune governs analytics.candles, seed 13-16 Jul expires ~12-15 Oct vs sample matures ~mid-Sep; rolling 90d≈62 trading days > 34 needed); D4 stays POWER-bound not data-bound. (B) PerformanceAllocator is the ONLY one of three COMPUTABLE-NOW labels to HOLD — breakdown persisted (v34, 298/361), and the 'masked by concentration' premise is REFUTED: perf_weight is a post-cap multiplier, changes final qty on 233/298 (78%) over [0.5,2.0]. Live DB hash advances on cron_heartbeat writes even when DOWN."
metadata:
  node_type: memory
  type: project
  originSessionId: 35afb62d-26b3-4c8b-a62f-fa6b431ad21b
  modified: 2026-07-19T14:12:04.191Z
---

**CANDLE RETENTION (D4) + PERFORMANCEALLOCATOR FEASIBILITY (19-Jul-2026, READ-ONLY, docs-only, NO rec).**
Report `docs/audit/candle_retention_and_perfallocator_feasibility_19jul2026.md`. All 3 artifacts byte-identical
before==after my session. Queries via `mode=ro` + throwaway snapshots; system confirmed DOWN.

## ⭐ A — CANDLE RETENTION: **SURVIVES** — D4 is power-bound, NOT data-bound
- **Mechanism:** `scripts/db_retention.py:63-70` prunes `candles` at **90d** (`DELETE FROM candles WHERE date < run_date−90d`, keyed on the v27 stored `date` col). Runs **every calendar day** (`cron_registry.yaml:82-111`, `30 2 * * 1-6` + Sun `--vacuum`, `market_day_only:false`, `enabled:true`, **`monitored:false`**). Genuinely governs `analytics.candles` (relocated v28/O6; `db_connect.py:26-30`) because `StateStore.__init__` ATTACHes analytics on every conn (`state_store.py:247`).
- **Anti-vacuity PASSED:** the Sunday VACUUM completed today (`analytics.db` mtime 02:30 + `db_retention.done` 02:30:05) — and VACUUM only runs if `failures==0` (`:139`), so the candle DELETE executed under the attach. 0 deleted because earliest candle = **2026-06-19** (30d old, not yet ≥90d). OOS days read exactly: 07-13 3,750 · 07-14 23,165 · 07-15 34,298 · 07-16 11,962.
- **Dates:** seed OOS candles expire **~12-15 Oct**; D4 sample matures ~17 trading days (~50 winners, ~mid-Aug) to ~34 (~100 winners, ~mid-Sep) ⇒ **5-9 week margin**. Rolling 90-calendar-day window ≈ **62 trading days > 34** needed; only constraint = run the analysis within ~90d of the earliest trade examined. First-ever candle prune ~18-Sep (earliest 19-Jun +91d).
- **§A4 preservation gap immaterial:** census snapshot = `trading_system.db` only, but nightly `analytics_backup` cron (01:05) backs up `analytics.db` (candles) independently.

## ⭐ B — PERFORMANCEALLOCATOR (#06): the 3rd "COMPUTABLE NOW" label **HELD**; "masked by concentration" is **REFUTED**
- **Feasible (data+power both OK — the ONLY one of three; D3 failed on data, D4 on power):** the sizer's full breakdown is persisted per trade (**v34**, `schema.sql:210-223`: `qty_by_risk/capital/concentration`, `binding_constraint`, `tier_weight_applied`, `perf_weight_applied`). Coverage **298/361** (63 pre-v34/recovered are NULL).
- **⭐ Masking premise WRONG on mechanism AND data.** perf_weight is applied **AFTER** `raw_qty=min(risk,capital,conc)` — a **post-cap multiplier** up to a **`2×raw_qty` ceiling** (`position_sizer.py:446/503/506`). So concentration binding raw_qty (confirmed `binding_constraint='concentration'` on **298/298**, = D1's 100%) does NOT stop perf_weight changing final qty.
- **Reachability (validated — my formula `max(1,min(floor(raw_qty·tier·pw),2·raw_qty))` reproduced `qty_planned` on 298/298, 0 mismatch, ⇒ lot_size=1 equity):** final qty changes on **233/298 (78%)** over the config clamp **[0.5,2.0]**, **151/298 (51%)** over a modest **[0.8,1.25]**. Decorative on only **65** trades — those with **raw_qty=1** (integer floor pins at 1 lot), NOT concentration. `perf_weight_applied=1.0` + `tier_weight_applied=0.5` on all 298 (allocator unwired: `main.py:2335-2339` only logs; `signal_processor.py:893/1827/2142` pass `_perf_weights.get(name,1.0)`, never populated).
- **Shelf life (B4):** conditional on **unlevered** sizing (cap ≈ Rs 9,875 ⇒ raw_qty 1-19, mostly ≤6, 65 pinned at 1). Under 5× MIS leverage raw_qty grows ⇒ binds on **even more**; re-run required. NO leverage design done. Q9 batch-4 "4/15 sizing **guards** bind" does NOT transfer — perf_weight is a multiplier, not one of the guards.
- **Merit still open (Rama's call):** reachability ≠ merit; the win-rate signal it would use has no ranking power (M-S4 ρ+0.003, D3 OOS non-replication). Wire/not-wire gates on D2/D3 + leverage + the latent 2× ceiling `:506`.

## ⭐ STANDING LESSON — the live DB hash advances even when the trading system is DOWN
`gemini_weekly_patterns` (`cron_heartbeat` id=2421, SUCCESS) wrote its heartbeat at **18:00:17** today, moving the live DB `6df0c09a…`(@11:14, the resume baseline) → **`a7a1de53…`**(@18:00). Monitoring/gemini crons write `cron_heartbeat` rows to the LIVE DB off-market ⇒ **"prove untouched" = before==after within your OWN session, NOT equality to a prior-day hash.** (Also seen: `eod_cleanup` correctly SKIPs weekends ids 2417-2420; `backup_retention` FAILING its own safety-abort 18/19-Jul — backups accumulating, not lost — flagged, not acted.)

## Queue after this (unchanged, all AFTER Monday)
Boot-path pair (careful loop): **live-seed extraction from `main()`** [[q9-live-seed-mc1-wired-19jul]] + **`check_scanner:703`** (add `==401` tolerance, do NOT escalate to blocking) [[monday-preboot-readiness-19jul]] · live-path quote observability (no partial-response detection) · 403 signal-count instrumentation (~338k) · deferred `event_type` / `Rejected (Sizing/Capital)` label / `build_taxonomy_map()` · wave-7 backlog · degenerate Rs 0.29 SL distance · **MEMORY.md compaction (SNAPSHOT FIRST).**

## ⚠️ MONDAY 20-Jul (first real boot since S4)
08:15 TOTP refresh · 08:15-09:00 boot (liveness alarm 09:00 if dead) · **pre-10:00 403s are NORMAL** · 10:00 entries open · 15:15 cutoff · 15:17 squareoff · 15:50 eod_cleanup (0 rows) · 16:22 registry officer · **18:15 forward shadow OOS day 4 — CHECK real `sim_R`, not nulls.**

Related: [[forward-shadow-capacity-d4-feasibility-19jul]] [[d3-band-inversion-robustness-19jul]] [[q9-batch4-sizing-reachability-18jul]] [[e4-w10-outcome-impact-19jul]] [[throttle-selection-record-correction-19jul]] [[signal-mortality-census-19jul]] [[capital-vocabulary]] [[db-schema-v28-split]] [[monday-preboot-readiness-19jul]] [[feedback-verify-the-finding-premise]]
