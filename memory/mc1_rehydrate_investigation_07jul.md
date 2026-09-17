---
name: mc1_rehydrate_investigation_07jul
description: "M-C1 BUILT (0fba665, local/unpushed) — live rehydrate seed excludes today's realized PnL (fixes a LIVE warm-restart double-count; PAPER was correct). Premise was inverted; corrected + built. 239 green. Wave-5 COMPLETE."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e0510fa-7d93-46b1-8ca1-a6360d7c108e
---

**M-C1 BUILT 07-Jul (commit `0fba665`, main, UNPUSHED, NOT deployed) — LAST Wave-5 item → Wave-5 COMPLETE (H-7✓ FIX-067✓ terminal-guard+D-1✓ M-C1✓).** First INVESTIGATED → STOP-and-reported because the build instruction's premise was INVERTED ("paper rehydrate diverges → mirror live"); the audit + code say the OPPOSITE: **LIVE double-counts today's realized PnL on a mid-day warm restart; PAPER was already correct.** Web Claude confirmed the corrected direction (fix LIVE) → built exactly that. Source `docs/audit/full_system_audit_04july2026.md:113`.

**BUILT — fix LIVE to mirror paper's correct semantics (paper UNTOUCHED):**
- `capital/fund_manager.py`: new **`today_realized_pnl_carryover(start=None)`** → Σ of today's `RELEASE_USED` `pnl_delta` via a NEW shared helper **`_today_release_used_pnl_rows(start)`** that **rehydrate Phase 2 now ALSO uses** (was an inline query) → the seed subtraction and the Phase-2 re-addition are GUARANTEED the same rows+sign (can't drift). Read-only, callable BEFORE `initialize` (reads only `self._store`).
- `main.py:2007` (LIVE branch only): `_startup_capital = broker_adapter.get_margins().net − fund_manager.today_realized_pnl_carryover()`. Paper seed (`:2005`) + Phase 2 UNCHANGED. FIX-156 paper adapter re-sync (`:2049 if is_paper`) untouched.
- **Identity:** `broker.net − Σ = (base + today_pnl) − today_pnl = base` → the fixed live seed reduces EXACTLY to paper's static PnL-excluded base, any sign/count → `seed + Phase 2 == broker.net` by construction (no double-count, no phantom `−today_pnl` sync drift). Cold boot: Σ=0 → seed=broker.net (unchanged).

**Tests** `tests/unit/test_mc1_live_seed_rehydrate.py` (7, REAL StateStore+FundManager+fm_ledger): T1 core RED (`BASE+2×pnl`)→GREEN (`broker.net`) + T1a loss-day sign + T1b multi-trade + T1c multi-bucket FULL-SNAPSHOT parity to the paper reconstruction (per-bucket attribution intact) · T2 paper untouched (both ways) · T3 cold-boot no-op · T4 sync-drift RED (`−pnl` phantom)→GREEN (zero). **239 green** across capital/rehydrate/sync (`test_fund_manager` incl. the refactored Phase 2) + cold-start + invariant + Wave-1 emergency-exit + Group-A HARD_KILL + H-12; **0 regressions**. SYSTEM_MAP changelog rides the pending doc-sync; PATHS.md unchanged.

**Original investigation detail (root cause, parity proof) preserved below.**

---
**Original STOP-report (investigation):** the instruction framed M-C1 as "paper rehydrate diverges → make paper mirror live." The actual audit + code say the OPPOSITE: LIVE double-counts, PAPER correct. Building "make paper mirror live" would have injected the bug into the correct paper path → STOPPED per the permanent-fix mandate (like FIX-067). Web Claude then confirmed the corrected direction, now built (above).

**Root cause (code-grounded):**
- Seed (`main.py:2004-2008`): paper `_startup_capital = selected_account.paper_capital` (STATIC opening balance, excludes today's PnL); live `_startup_capital = broker_adapter.get_margins().net` (broker net — on a warm restart ALREADY includes today's realized PnL).
- `main.py:2035` → `fund_manager.rehydrate_from_open_trades()` → **Phase 2** (`capital/fund_manager.py:1598-1622`) walks today's `fm_ledger` `RELEASE_USED` rows and does `_bucket_add_avail(bucket, pnl)` + `_total += pnl` — adds today's realized PnL.
- **Paper (correct):** total = paper_capital + today_pnl (added once). `main.py:2045-2055` FIX-156 then re-syncs the paper ADAPTER to `fm.total` — the comment even documents the INTENDED semantics: "static starting capital + replayed PnL."
- **Live (bug):** total = broker.net + today_pnl = (base + today_pnl) + today_pnl = **base + 2×today_pnl** → reservable capital inflated by today_pnl until the next `sync_from_broker` (`fund_manager.py:1247`, sets `_total=broker.net`), which corrects it but records a phantom `−today_pnl` SYNC delta → **spurious drift alert**. Invisible at 08:15 cold boot (0 closed trades → 0 RELEASE_USED rows → Phase 2 no-op).

**Correct fix (the TRUE parity fix — OPPOSITE direction to the instruction):** make LIVE's rehydrate mirror PAPER's correct semantics (static opening base + PnL-once), NOT paper mirror live. Cleanest = seed live from an opening base that EXCLUDES today's realized PnL so Phase 2 re-adds it exactly once — e.g. `_startup_capital = broker.net − Σ(today RELEASE_USED pnl_delta)` (same rows Phase 2 sums), making live symmetric with paper at the source. (Alt: skip Phase 2 PnL carryover on live — but that loses per-bucket PnL attribution; rejected.) This is a LIVE capital-accounting correctness fix touching the live capital seed — NOT a paper change; paper stays untouched.

**Parity proof:** identical position set, one closed trade with realized PnL=+₹1,000, mid-day warm restart. Paper → total = paper_capital + 1,000 (correct). Live → total = (opening + 1,000) + 1,000 = opening + 2,000 (₹1,000 phantom). H-12 (signed paper get_positions) is unrelated to this — it does not feed the capital seed; the instruction conflated M-C1 with the H-12 paper-parity theme.

**Status:** NOTHING edited/built/committed. Wave-5 NOT yet complete (H-7✓ FIX-067✓ terminal-guard+D-1✓ · M-C1 = investigated, awaiting corrected build directive). Do NOT build "paper mirrors live". [[terminal_state_write_guard_design_07jul]] · [[fix067_ms1_investigation_07jul]] · [[full_repo_audit_04jul_pending]] · [[capital_operational_note]]
