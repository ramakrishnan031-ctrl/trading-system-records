---
name: q9-batch4-sizing-reachability-18jul
description: "18-Jul Q9 batch 4 — sizing floors/caps wired-proven (15-guard ladder, binding order, bite-proven). ⭐ NEW LESSON 'WIRED IS NOT REACHABLE': only 4 of 15 guards can bind in production. ⚠️ PerformanceAllocator is NEVER wired (perf_weight≡1.0 on 298/298) and daily_report reports 3,098 CAPITAL rejections when the true count is 0."
metadata: 
  node_type: memory
  type: project
  originSessionId: 53e59a7c-edb5-400e-9b3e-6d5981ddd5a2
  modified: 2026-07-19T06:30:13.370Z
---

**📏✅ Q9 BATCH 4 — SIZING FLOORS + CAPS ARE WIRED, AND THE REACHABILITY QUESTION IS ANSWERED.
18-Jul-2026.** Report `docs/audit/q9_batch4_sizing_floors_caps_18jul2026.md`.
**TEST-ONLY — zero production files; no runtime behaviour change.**

## ⭐ THE NEW PERMANENT LESSON: **WIRED IS NOT REACHABLE**
Q9's founding lesson was *CONFIGURED IS NOT COVERED*. This batch adds its sibling: a guard can be
correctly implemented, correctly wired, and bite-proven in a fixture — **and still never bind under
production config**, because an earlier guard always clamps first. A green wired test then says
nothing about whether it protects real capital.
**⇒ REACHABILITY is now a permanent field in the Q9 coverage matrix.**

**Of the 15 sizing guards in `capital/position_sizer.py::calculate()`, only 4 can bind:**
**G5 concentration** (298/298) · **G7 >cap rejection** (3,098 signals) · **G9 tier multiplier**
(0.5 on 298/298) · **G10a floor-at-1** (produced the qty on **65/298 = 21.8%** of trades — without it
those would have been BELOW_MIN rejects). **10 unreachable, 1 conditional.**

## ⚠️⚠️ THE FINDING UNDER FIVE OF THOSE VERDICTS — AN ENTIRE SUBSYSTEM IS DECORATIVE
**`PerformanceAllocator` is NEVER instantiated anywhere outside its own docstring, and
`perf_weights` is NEVER passed to `SignalProcessor` (`main.py:2914`).** So
`SignalProcessor._perf_weights == {}` and `signal_processor.py:893` always resolves to the **1.0
default**. Verified 3 ways: static · wiring · **runtime (`perf_weight_applied = 1.0` on 298/298
sized trades)**. ⇒ `dynamic_by_winrate: true`, `min_multiplier: 0.5`, `max_multiplier: 2.0` in
`system_config.yaml` are **read by nothing on the sizing path** (only config_loader defines them, one
main.py line logs them, the ops dashboard displays them).
📌 The M-C6 comment at `position_sizer.py:462` explains G8's unreachability as *"performance_allocator
clamps min_weight=0.5 … effective_mult >= 0.25"* — **conclusion right, premise wrong** (the allocator
does not run at all, so the floor is 0.5). Recorded, NOT changed.

## ⚠️ A CAP THAT *CAN* BE EXCEEDED — latent, and the config already asks for it
`position_sizer.py:506` — `tiered_qty = max(1, min(tiered_qty, raw_qty * 2))`. For any
`effective_mult > 1` the final qty reaches **2× the tightest clamp arm**. Runtime-demonstrated:
`perf_weight=2.0` → **qty=100 vs a concentration arm of 50 = 20% of capital against a 10% cap**;
**G14 (40%) cannot catch it**; and the stored **`binding_constraint` still says `'concentration'`**.
**NOT live today** (perf_weight ≡ 1.0 ⇒ `tiered <= raw` always) — but `max_multiplier: 2.0` is
already in production config, so wiring the allocator would make it live silently. **A test now fails
the moment `PerformanceAllocator(` is constructed or `perf_weights=` is passed.**

## ⚠️ REPORTING DEFECT — the daily report states the OPPOSITE of the truth
`reports/daily_report.py:464` counts `"CAPITAL" in rejection_reason.upper()`. The CONCENTRATION reason
string embeds `capital_qty=` ⇒ **it reports 3,098 "capital" rejections when the true SIZING_CAPITAL
count is 0 — a 100% false positive.** Also `:549` buckets by `rejection_reason` first, and that string
embeds the symbol + arm values ⇒ **246 distinct strings for 3,098 rejections**, so the single largest
sizing constraint is fragmented into 246 low-count lines instead of one. **NOT FIXED (out of a
test-only batch's scope) — careful-loop item.**

## §A3 — the 13-Jul sizing audit RE-VERIFIED (298 trades, 22-Jun→16-Jul; capital Rs 9,875.60)
**Nothing inverted.** 5 VERIFIED, 2 CHANGED (direction held):
concentration binds **298/298** ✅ · `qty_by_risk <= qty_by_concentration` in **0** rows (mean arms
risk 34.4 / capital 130.8 / **conc 3.4**) ✅ · actual risk **median Rs 4.92** vs intended **Rs 98.76**
= **1/20th** ✅ · tier **0.5 on 298/298** ✅ · median position **Rs 442**, max **Rs 999** ✅ ·
exclusion **23.1%** of priced signals (7,604/32,928) ⚠️CHANGED-in-character (see above) ·
LONG:SHORT skew **2,804 vs 294 = 9.54×** (was ~4.5×) ⚠️CHANGED-worse — attributed via the
authoritative `StrategyConfig.direction` registry, **not** inferred from strategy names (the registry
classifies `positional_sector_rotation` as LONG; name-inference had under-counted the skew at 7.34×).

> **⚠️ CORRECTED 19-Jul (census claim 3):** the 9.54× is a **COUNT** ratio = the **10.2× long-volume skew**, NOT differential treatment. By **RATE** the cap hits SHORTs marginally harder — LONG **10.00%** vs SHORT **10.72%**. Threshold (~Rs 990) + share (~23%) VERIFIED. ⚠️ **This sits in D1's evidence package — the corrected direction must travel with it.** C2 qualifier: batch-4 verdicts hold for the *sizer* population (enriched **1.45× >Rs 990**); domain-bounded, not invalidated. [[signal-mortality-census-19jul]]

## THE ALGEBRA (why the risk sizer is dead)
`CONCENTRATION binds ⟺ sl_distance < (risk_pct/conc_pct) × price = 10% of price`. Intraday stops are
1–3% ⇒ always true. `CAPITAL binds ⟺ intraday avail < Rs 197.51 of Rs 6,912.92` (97.1% reserved);
max concurrent margin is 5 × 197.51 = Rs 987.56 ⇒ never close. **G1 masks G3** (G3 needs
sl_distance < Rs 0.0099, G1 rejects below Rs 0.05 first — G3 needs **capital ≥ Rs 50,000** to become
reachable). **G10's floor masks G15**; `lot_size: 1` on all **16** strategies makes **G12 an identity
and G13 unguarded-unreachable**.

## §A4 — RULE F EARNED ITS PLACE AGAIN
**A bare webhook POST does NOT reach sizing** — `REJECTED_STEP_ERROR: price_action` (no market data);
`calculate()` called **0** times. Sizing is reached only with **`sim_kite.set_rich_quote` + patched
`screener._build_market_data`** (test_end_to_end_smoke's pattern) ⇒ 1 call, args
`('RELIANCE','BUY',999.0,991.008,'INTRADAY','HIGH',1) perf_weight=1.0`.
**📌 And the existing "full lifecycle" integration tests invoke the sizer ZERO times —
`test_full_signal_flow._drive_lifecycle` hard-codes `qty=10` and reserves directly.**

## §B — the test file
`tests/integration/test_q9_sizing_floors_caps_wired.py`, **23 tests**, existing `wired_system`
fixture, no parallel harness. Every test proves **WHICH** guard bound via a **strict-unique-minimum**
check (`_assert_bound_by` refuses a tie as non-decisive) — **no multi-way accepts**.
**M-C6 proven end-to-end** through the real `_perf_weights` seam: `REJECTED_SIZING_ZERO_MULTIPLIER`,
**broker calls `[]`** (asserted on `adapter.place_order`'s record), **no trade row**, capital
**byte-identical**, and `raw_qty > 0` as anti-vacuity. **§B3 answered: the min-lot floor CANNOT breach
a cap** — structural, because G7 rejects `raw_qty <= 0` so anything reaching the floor has
`raw_qty >= 1 <=` every arm (proven + swept 3 tiers × 9 prices).

## ⭐ §B6 BITE PROOF — and TWO plants exposed gaps in MY OWN tests
4 value-shaped plants. **Plant A** (conc 10× loose) was caught partly by production's OWN
`POSITION_VALUE_CAP` ⇒ instructive, worthless as evidence (batch 3's lesson, again).
**Plant B is the meaningful one**: dropping the tier multiplier yields qty 50 instead of 35 — a
perfectly **legal** quantity inside every cap ⇒ **production's runtime guard fired 0 times** (measured:
`CapitalInvariantViolation` = 0) **yet the tests failed**. That is the E4/W10 class, in sizing.
**⚠️ Plant B initially UNDER-bit** (every test used HIGH=1.0 so removing the multiplier changed
nothing) and **Plant D was MISSED entirely** (a 2.0 multiplier never reaches a 2× ceiling, so it
cannot detect where the ceiling sits). **Both gaps closed with new tests.** ⇒ *bite-testing is not a
formality; it found real holes twice in one batch.*

## PARITY — structural
`position_sizer.py` has **no** `paper_mode`/`is_paper`/`live_mode` branch and no mode argument; it
reads only the mode-free `FundManager.get_snapshot()`. `signal_processor.py:885` is upstream of the
mode branch (divergence at `zerodha_adapter.py:348`). `TestParity` asserts these so a future
duplicate cannot drift.

## ⭐📌 REGRESSION METHODOLOGY — "the ~30-test flake band" is NOT flake (CAUSE FOUND)
**`config/instruments.csv` (75,749 bytes) is GIT-IGNORED** ⇒ a throwaway `git worktree` lacks it ⇒
`main.py:1949` can't build the InstrumentCache ⇒ preflight fails ⇒ **`main.py:2014`
`assert instrument_cache is not None`** trips ⇒ ~30 boot-path `test_main.py` + preflight/T4 tests
fail **spuriously**. Proven causally: the test **fails in isolation in 0.56s** in the worktree (⇒ not
ordering/contention), passes in the main tree, and **copying that one file in makes it pass**; the
full base re-run went **42F → 15F**.
**⚠️ WHY IT MATTERS: a bare worktree INFLATES the base failure set, and inflation is the MASKING
direction** — a genuine new failure can coincidentally match one of the ~30 spurious base failures
and be waved through as pre-existing. Same trap as [[verify-check-the-rc-not-the-output]]'s stale
baseline, new disguise.
**📌 SHARPENED RULE: prefer `git checkout <base> -- <files>` in the MAIN tree (it preserves
git-ignored runtime data), or seed the worktree with the ignored files before trusting its numbers.
`git stash` stays FORBIDDEN.** And keep base+mine in the SAME TIME WINDOW (batch 3's lesson).

## Regression + deploy (18-Jul ~19:1x–20:0x IST, off-market, system DOWN)
**BASE2 (true, worktree + ignored data) 15F/4941P/7S/1xf = 4964** vs **MINE `f177c60` 12F/4969P/5S/1xf
= 4987**. **`comm -13` EMPTY ⇒ ZERO ATTRIBUTABLE** (empty against the discarded inflated base too).
**Totals reconcile EXACTLY 4964 + 23 = 4987.** `xfailed=1 / XPASS=0` ⇒ batch 3's E4/W10 contract xfail
still genuinely xfailing. Tag **`deploy-18jul-q9-batch4` → `f177c60`**; PC == VM bare == **`7f0bf45`**
(delta tag..HEAD = **markdown only**). Backup `pre_deploy_q9b4_20260718.db` **SOUND** (`quick_check=ok`,
v44, 361 trades, 0 FK). Schema **v44 unchanged, no migration**; integrity ok; 0 FK; **kill-switch
INACTIVE**; services unchanged; **the 23 new tests PASS ON THE VM**.

## Remaining Q9 queue
**#5 post-restart capital restoration** · back-fill the coverage-matrix metadata for the remaining
layers. **Separate/larger:** HARD-kill order cancellation + flatten-worker verification.

Related: [[q9-batch3-capital-invariant-18jul]] · [[q9-batch2-killswitch-toctou-18jul]] ·
[[q9-batch1-daily-loss-wired-18jul]] · [[q9-money-path-coverage-18jul]] ·
[[feedback-verify-the-finding-premise]] · [[capital-operational-note]].
