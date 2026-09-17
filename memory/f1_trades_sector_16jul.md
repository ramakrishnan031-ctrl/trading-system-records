---
name: f1_trades_sector_16jul
description: "F1 — populate trades.sector at insert + gate-8 sector_cap_mode observe/enforce; BUILT+TESTED, UNPUSHED (deploy + enforce-flip off-market, Rama-gated)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — F1 (register blocker B1 / Finding-1): populate `trades.sector` at INSERT + gate-8
OBSERVE mode. BUILT + TESTED LOCAL, UNPUSHED.** Branch `f1-trades-sector-observe-16jul` (2 commits:
feat `2e35521` + docs `2e01a8e`), off `main`@`3b9041a`. Deploy + the enforce-flip are OFF-MARKET,
Rama-gated (Phase-3 runbook).

**Root cause:** `trades.sector` NULL on every row → `sector_exposure(sector)` (`... AND sector=?`) summed
0 for the resting book → the 40% sector concentration cap (gate-8 SECTOR_EXPOSURE) never summed open
positions. The insert path was ALREADY wired (`order_manager.create_trade` accepts+writes `sector`);
`order_placer.py:895` hardcoded `sector=None`.

**Fix (populate + observe SHIP TOGETHER — never populate while the cap enforces unreviewed):**
- **Populate at insert:** `order_placer._resolve_trade_sector(symbol)` resolves via the SAME source
  gate-8 uses — **`InstrumentCache.sector(symbol)`** (`instruments.csv` ← NSE index-member CSVs;
  `"UNKNOWN"` on miss/blank/no-cache; never raises). FROZEN on the row (create_trade writes-once;
  **nothing UPDATEs trades.sector** — verified). `"UNKNOWN"` = distinct bucket, never NULL. One-shot
  data-quality WARNING (Telegram notifier, else log) when the UNKNOWN fraction of inserts >
  `risk.sector_unknown_alert_pct` (default 0.20), min-sample 10. Parity: mode-agnostic.
- **Gate-8 observe mode:** new `risk.sector_cap_mode: observe|enforce` (**default observe**). observe =
  LOG `sector_cap_would_reject … verdict=WOULD_REJECT` (symbol/sector/current%/projected%/threshold) +
  CONTINUE; enforce = reject as designed. **Default observe ⇒ deploy is behaviour-neutral** (sector
  fills; cap only logs). Wired `main.py:2188` (RiskEngine) + `main.py:2345` (OrderPlacer DQ threshold).

**Canonical-source finding (Phase-1):** live source = `instrument_cache.sector` (`main.py:2199`). TWO
NON-LIVE discrepancies RECORDED (not fixed): `risk_engine.py:123` alt-factory uses non-existent
`instrument_cache.sector_for` (→UNKNOWN; unused builder, main.py constructs directly); `signal_processor
._sector_for` looks for non-existent `sector_for`/`get_sector` → always UNKNOWN (dead, sets the signal's
sector, not the trade).

**Tests:** 226 unit (`test_risk_engine` observe/enforce + multi-position sum · `test_order_placer_sector`
NEW resolver+DQ · `test_gate8_sector_toctou` · `test_config_loader` defaults) + 4 integration
(`test_hardening_scenarios`, flipped to enforce test-locally). `test_main` ZERO-new (4 failures
pre-existing PC-env, identical on base via `git stash`). No schema change. 4 modules compile.

**⏰ PHASE-3 (Rama, OFF-MARKET):** (1) push + deploy (behaviour-neutral) → (2) OBSERVE SOAK ≥1 session,
collect WOULD_REJECT logs + confirm UNKNOWN proportion sane (no DQ-alert storm) → (3) **ENFORCE FLIP only
after Rama reviews the soak + EXPLICITLY approves** (`sector_cap_mode: observe→enforce`, activates the
live cap; never on simulation alone). Rollback = set back to observe (instant de-fang) / revert.

**Relation to D1:** clears D1's DATA prerequisite (trades.sector populated). **D1 (raise
`max_concentration_pct`) stays HOLD** — separate Rama decision, NOT part of this fix.

**Follow-up (16-Jul, folded into the branch — now 5 commits):** **BUG A** `2404799` — `risk_engine.py:123`
`sector_for` was a **class-DOCSTRING `Usage::` example** (NOT an executable factory — earlier
mischaracterization corrected; never ran, never a runtime risk); fixed docstring → `.sector` + a
doc-lint test. **BUG B** (`signal_processor._sector_for` always UNKNOWN) **DEFERRED with evidence** —
its `V3Signal.sector` + `ScoredCandidate.sector` fields are **set-but-never-read** (repo-wide `.sector`
grep = zero reads; `portfolio_allocator.py:173` says the sector cap is gate-8's job; `forward_shadow`
takes sector from `sector_map` not `_sector_for` and is records-only) → **no runtime dependency,
STOP-gate NOT triggered.** **Q6** repo-wide `sector_for(`/`get_sector(` sweep **CLEAN** — only BUG A
(fixed) + BUG B; no other stale resolver. Canonical resolver everywhere = `InstrumentCache.sector`.

Report `docs/audit/f1_trades_sector_16jul2026.md`. Register blocker B1 → addressed-pending-soak.
[[pending-register-16jul]] [[unpushed-pending-deploy-ledger]] [[capital-operational-note]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1319 B (budget 450 B). The index now carries a hook and this link.

- 🏦🟡🔝 **[16-Jul F1 — populate trades.sector at INSERT + gate-8 observe mode (register blocker B1)](f1_trades_sector_16jul.md)** — BUILT+TESTED LOCAL, UNPUSHED; branch `f1-trades-sector-observe-16jul` (feat `2e35521` + docs `2e01a8e`). Root cause: `trades.sector` NULL → `sector_exposure` summed 0 → the 40% sector cap never summed the resting book. Fix (populate + observe SHIP TOGETHER): `order_placer._resolve_trade_sector` resolves at insert from **`InstrumentCache.sector`** (same source as gate-8; UNKNOWN-bucketed, frozen, DQ-alert) + gate-8 **`risk.sector_cap_mode` default `observe`** (LOG WOULD_REJECT, don't reject → deploy behaviour-neutral). Tests **226 unit + 4 integration**; test_main ZERO-new (4 pre-existing PC-env). No schema change. **⏰ Phase-3 OFF-MARKET (Rama): deploy → observe soak ≥1 session → EXPLICIT-approval enforce flip** (activates the live cap). **D1 stays HOLD** (clears its data prereq only). **Follow-up: BUG A (`risk_engine.py:123` `sector_for`) = a class-DOCSTRING example (never executable), fixed→`.sector`; BUG B (`signal_processor._sector_for`) DEFERRED-inert (its signal-sector fields set-but-never-read); Q6 stale-resolver sweep CLEAN. Branch now 5 commits.** [[f1-trades-sector-16jul]] [[pending-register-16jul]] [[unpushed-pending-deploy-ledger]]
