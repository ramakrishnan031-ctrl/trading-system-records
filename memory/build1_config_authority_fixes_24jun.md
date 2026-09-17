---
name: build1-config-authority-fixes-24jun
description: "BUILD 1 — resolved 12 audited config conflicts; single daily-loss source (pct), capital-relative position cap, dead-config deletions,"
metadata: 
  node_type: memory
  type: project
  originSessionId: 88855a30-943e-4416-8cc6-b022dd4301df
---

BUILD 1 (Config Authority Fixes), staged on branch `build1-config-authority-fixes-24jun`
(commit c69f1fd), 24-Jun-2026 post-close. Resolves the 12 config conflicts from the
Phase 1+2 audit (all LOCKED by Rama). **Trading-path; no DB schema; parity (shared
paper+live paths).** Activates next restart (08:15).

**#1 SINGLE DAILY-LOSS SOURCE:** deleted absolute `capital.daily_loss_limit` (₹300).
`risk.daily_loss_limit_pct` (3%) is the SOLE authority. FundManager post-close **realized**
breach derives ₹ = `daily_loss_limit_pct × current capital` (`self._total`) — same pct the
pre-trade RiskEngine MTM gate uses (`main.py` feeds it to BOTH). Basis split preserved
(pre=realized+unrealized, post=realized). Scales: ₹10k→₹300, ₹1L→₹3000. See
[[dual_daily_loss_mechanism]].

**#2 CAPITAL-RELATIVE POSITION CAP:** `position_sizing.max_position_value_rs` (₹2500) →
`max_position_value_pct` (0.40). PositionSizer cap = 0.40×capital; keeps REJECT
(POSITION_VALUE_CAP, catastrophic/bug-guard, NOT a clamp). Removes ₹25k scaling cliff;
routine sizing still bound by concentration 10% + risk 1%. ₹10k→₹4000, ₹1L→₹40000.

**#10 STARTUP-BLOCKING GUARD:** `force_intraday_only=true` + `trade_type=DELIVERY` (0
strategies could trade) raises a ValidationError in `SystemConfig._cross_field_sanity_checks`
→ refuses to boot (fail fast).

**#3/#4/#11 DEAD CONFIG DELETED:** `live_test_mode`/`live_test_max_*` (were == base caps
5/10 → main.py swap was a no-op; base caps now sole authority both modes — supersedes
[[live_test_mode_permanent]]); scoring_weights `tier_multipliers` (sizer reads system_config
0.70, never this 0.75); per-strategy `max_risk_pct` (dead in live; replay falls back to 0.01).

**#A.4 STALE DEFAULTS ALIGNED:** FundManager 10000→0.03, PositionSizer 50000→0.40,
RiskEngine docstring 10/20/4/0.05→5/10/5/0.03.

**#12 BOOT INVARIANT:** comment + `assert _startup_reconcile_done` so reconcile_once()
provably precedes signal_processor.start()/webhook (phantom capital corrected before any
trade — proven no-trade-in-window).

**#5/#6/#7/#8 DOC-ONLY** + a PERMANENT-vs-LAUNCH-PHASE tagging convention in
system_config.yaml (entry_start 10:00 = launch-phase; caps/limits now capital-relative =
permanent). Feeds BUILD 2.

**AUDITORS (beyond the 12, forced by the deletions):** `scripts/system_manager.py` EOD +
`scripts/preflight/checks/config_integrity.py` recompute the pct→₹ thresholds from a NEW
`StateStore.get_day_opening_capital()` (fm_ledger INIT row, **OPENING** basis, `accounts.csv`
paper_capital **bootstrap fallback** when no INIT row, no broker call → parity-safe). Preflight
`LiveTestModeCapsCheck` → `CapsConfigDriftCheck` (guards base caps 5/10).

**Tests:** full suite green except 1 PRE-EXISTING time-of-day artifact
(`test_interactive_startup::test_holiday_guard_missing_yaml_proceeds` — main() exits 0 outside
08:00–16:00 IST market window; confirmed failing on clean HEAD too). Added #10 test, repurposed
preflight test, auditor-capital-basis tests. Crash-test isolated scripts (ct_day3_isolated.py
:109/:140 ref `fm._daily_realized_pnl`/`_daily_loss_limit`) left as-is — already pre-broken
(reference a long-removed attr) + not pytest-collected.

**DEPLOY:** committed on branch, NOT yet pushed/merged to live (awaiting Rama's go — it's a
live money-path; auto-activates next restart once deployed). CONFIG_GUIDE.md `.docx` companion
needs a manual re-SCP. **NEXT: BUILD 2 — Config Sanity Auditor** (enforces these rules, blocks
contradictions, lists overrides, flags launch-phase params, covers the Phase-2 never-validated
list; #10 already lives as a startup-blocking check).
