---
name: v3_shadow_deploy_soak_12jul
description: V3 Steps 1-9 PUSHED c1ad82e (12-Jul Sun) + scorer & allocator OFF→SHADOW; both shadow soaks start Monday 08:15; SESSION-1 sanity check OWED; ≥5 sessions before any enforce; rollback=flags-off+restart
metadata:
  node_type: memory
  type: project
  originSessionId: e31b6e26-79d0-41d6-b1cc-db98a712e270
---

**V3 SHARED ENGINE Steps 1-9 DEPLOYED + scorer/allocator flipped OFF→SHADOW (12-Jul-2026, Sunday off-market). PUSHED `8116b74..c1ad82e`. Both shadow soaks begin at the MONDAY 13-Jul 08:15 auto-boot.** See the deploy ledger for the authoritative state; this note holds the SOAK PROTOCOL + the owed checks.

**Push:** 2 commits — `536172c` (Steps 1-9 code, ALL default-OFF → byte-identical) + `c1ad82e` (scorer+allocator OFF→SHADOW, config-only). Deploy hook ran (post-receive `checkout -f main` + crontab auto-install). **PC==bare==`c1ad82e`; VM working-tree config VERIFIED: `v3_hardgate_mode: shadow` + `allocator_mode: shadow`, EVERYTHING ELSE OFF** (regime false · sr anchors false · force_intraday_only true · delivery_enabled false · trade_type INTRADAY · enforce_scope v3_only · NO enforce anywhere). V3 files present on VM. **No restart owed** (weekend; Monday 08:15 boot loads `c1ad82e`). VM working tree = `/home/ubuntu/systems/trading-system/`; bare = `~/trading-system.git`; git remote alias `trading-vm`.

**No-live-change (both shadow paths are provably log/observe-only):**
- **Scorer shadow:** `secondary_screener.screen()` calls `_log_v3_shadow_compare` (logs OLD score/tier vs NEW score/tier/gate per signal); the LIVE decision below FOLLOWS OLD, unchanged (`secondary_screener.py:287-296`). Zero order interaction.
- **Allocator shadow:** `_process_one` calls `allocator.observe(copy)` fire-and-forget (guarded, never raises/blocks); the fused FCFS admit still runs + places; the allocator's window worker computes regret + writes `data_store/allocator/regret.jsonl` and calls NEITHER reserve NOR place (Step-6b tests `test_shadow_admits_identically_and_only_observes` + `test_shadow_window_computes_regret_without_reserve_or_place`). Zero added live latency (append is O(1)).

**Soak tooling (so Rama runs nothing) — `scripts/v3_shadow_soak_report.py` (read-only):**
- `--scorer [--since YYYY-MM-DD]` → date-scoped OLD-vs-NEW flip-set over the live `screener_results`, reusing the VALIDATED classifier from `scripts/v3_hardgate_parity_recompute.py` (`analyze`); prints counts + flip-set + UNEXPLAINED + PARITY_OK. Expected post-flip: age-band (FLIP_PASS/TIER_SHIFT) + rounding-boundary (FLIP_FAIL) ONLY, 0 UNEXPLAINED (matches the offline artifact `v3_step4b_parity_artifact_12jul`).
- `--allocator [--since]` → per-session regret summary (windows · crowd_out · starvation · score_weighted_regret) from `regret.jsonl`.
- Opens the main DB read-only (`file:…trading_system.db?mode=ro`); verified runs clean at 0 rows.

**SOAK PROTOCOL (execute over the coming sessions):** MIN 5 trading sessions of BOTH soaks before any enforce discussion. **⏰ SESSION-1 SANITY CHECK (owed after Monday's first live session, report it):** is shadow data flowing? any hot-path exception from shadow code? any latency/throughput change vs a normal session? ANY live-behaviour delta? Then MID-SOAK (~session 3) + FINAL (≥session 5). **STOP CONDITIONS → halt soak, set both flags → off, restart off-market, report AT ONCE:** any scorer flip NOT explained by age-band/rounding-boundary (anything the offline artifact didn't predict) · any hot-path exception from shadow · any measurable latency/throughput degradation · ANY live trading-behaviour difference · anything unexplained (err toward reverting).

**T4 (NIFTY index historical access, regime precondition):** DEFERRED — Sunday has no live broker session (`.env` holds only the static `ZERODHA_API_KEY`; the daily access token is refreshed 08:15 on a trading day, absent Sunday; app down). Token 256265 IS the correct NIFTY 50 instrument_token (config right); only the live-API precondition is unverified → check in a Monday token-fresh window BEFORE ever enabling regime. regime stays OFF.

**Rollback = config-only:** set `v3_hardgate_mode`+`allocator_mode` back to `off` + off-market restart → today's byte-identical behaviour. No code revert. **NOT flipped: regime, sr anchors, delivery, any enforce.** Review-queue flags remain (Step-8 SL-owner, Step-5 kill_switch fail-open, gate-8 TOCTOU, ATR-into-live-SL). NEXT = SESSION-1 sanity check Monday → soak reports → (after ≥5 clean sessions + review) enforce discussion. Follows the shared-engine build [[v3_step6b_portfolio_allocator_impl_12jul]].
