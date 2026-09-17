---
name: q9-money-path-coverage-18jul
description: "18-Jul Q9 READ-ONLY — money-path/safety-layer coverage map. 6 WIRED / 8 UNIT-ONLY / 0 untested. The DAILY LOSS LIMIT is the most expensive gap: both halves unit-only, never driven in integration, and the two tests that look like coverage accept ANY of 9 rejection reasons."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**🗺️💰 Q9 — MONEY-PATH + SAFETY-LAYER WIRED-IN COVERAGE MAP. Done 18-Jul-2026 (READ-ONLY).**
Report `docs/audit/q9_money_path_coverage_map_18jul2026.md`. Docs-only. **Nothing built, no flag flipped,
no CTs run.**

**⭐ STEER: 6 WIRED · 8 UNIT-ONLY · 0 wholly untested. The single most expensive silent failure is the
DAILY LOSS LIMIT** — *both* halves UNIT-ONLY (pre-trade RE7 `risk_engine.py:25` + post-close
`fund_manager.py:1280`), **no integration test has EVER driven a realized loss past the threshold**, and it
is also the one layer whose **input contract is known-wrong today** (E4/W10: `pnl_delta`=gross not net,
UNPUSHED) ⇒ simultaneously the least-proven AND most-suspect layer, and the thing that stops the account
bleeding on a bad day.

**🔴 THE NEAR-VACUOUS ASSERTION (a finding in itself).** `test_risk_rejection_max_open_positions` exists in
BOTH integration files (`test_end_to_end_smoke.py:265`, `test_full_signal_flow.py:376`) and each asserts the
signal reached **ANY ONE OF NINE** statuses (incl. `REJECTED_DAILY_LOSS`). ⇒ it proves *"the risk engine
rejected for some reason"*, **not which gate** — if the intended gate silently broke and another fired, the
test still passes. Compounding: `test_full_signal_flow.py:9`'s docstring still advertises *"Sad path 1:
Signal rejected by risk (daily_loss_limit reached)"* but the implemented test is the max-open-positions one
⇒ **the suite DOCUMENTS a daily-loss scenario it does not run.**

**WIRED (6):** kill-switch @ webhook (`smoke:357`) · hard-kill flatten chain (`test_hard_kill_flatten_chain.py:114`
— ⚠️ **mock broker only; the first LIVE hard-kill is still M-C8's real test**) · emergency-exit chain
(`:136`) · **sector gate-8 ENFORCE** (`test_hardening_scenarios.py:111`, fixture forces
`_sector_cap_mode="enforce"` at `:120` — a good pattern to copy) · capital reserve→commit→release lifecycle
(`smoke:694/:746`, long+short EF-3) · capital release on broker rejection (`flow:441`).
**UNIT-ONLY (8):** daily-loss pre-trade · daily-loss post-close · **kill-switch last-mile re-check**
(`order_placer.py:1003` OP-LM1 / `:1274` A-3; only `test_a3_entry_kill_recheck.py`) · `max_position_value` ·
tier multiplier · FIX-133 min-lot floor · M-C6 zero-multiplier SKIP · consecutive-losses gate.

**✅ Q4 GOOD NEWS — money writes are well-encapsulated (the feared class is largely absent):**
`INSERT INTO fm_ledger` = **ONE** production site (`fund_manager.py:2365`); `trades.gross_pnl/charges/net_pnl`
= **ONE** writer (`core/state_store.py:2268`); `kill_switch.py:1254` writes `status` only, no money column.
**⇒ residual risk is the CONTRACT, not scattered writers** — one wrong value into that single writer
propagates everywhere and the suite won't notice (exactly how E4/W10 and X7 hid). **A schema/column test
cannot catch it; only an end-to-end value assertion can.**

**⭐ Q5 REFINEMENT TO THE FIXTURE-BLINDNESS LESSON: "CONFIGURED ≠ COVERED".** Unlike the webhook
`secret_token=None` case, the integration fixtures DO enable the layers (`daily_loss_limit_pct=0.02`
`conftest.py:235` / `0.05` `:257`, `max_open_positions=2` `:253`, `max_consecutive_losses=4` `:256`) — but
the daily-loss limit is **set and never reached**, so its rejecting branch never executes.

**Q6 — E4/W10 interaction:** branch `e4-w10-pnl-contract`@`ad34ee4` makes `pnl_delta` **NET**; covered by
`tests/unit/test_e4_w10_pnl_contract.py` (598 lines) **unit-only, no integration**. **Any Q9 daily-loss
assertion must be written against the NET contract** — assert the RELATIONSHIP ("fires once cumulative net
loss ≤ −pct × total") not a literal figure, so it is correct under both contracts and becomes a
merge-readiness check for E4/W10. ⚠️ Related distortion: **RMS closes pass `costs=0.0`** ⇒ some closes stay
gross even after E4/W10 — assert separately, don't assume.

**📋 Q7 PRIORITISED PLAN (recommend only, ordered by cost-of-silent-failure):**
1. **Daily loss limit fires through the wired path, both halves** — drive real closes past the limit; assert
   **`REJECTED_DAILY_LOSS` specifically**, and that it does NOT fire just below. Cost of failure = unbounded
   daily loss. (M, ~80 lines, reuses `wired_system`.)
2. **Tighten the two 9-way assertions** to the specific gate (S; rides with #1; also stops #1 passing for the
   wrong reason).
3. **Kill-switch last-mile re-check, wired** (TOCTOU: an entry placed AFTER a kill). (M)
4. **Sizing floors/caps wired** — min-lot · M-C6 zero-multiplier SKIP · `max_position_value` (M, one module).
5. **Post-restart capital restoration** (L).
**Honestly LOW-VALUE, do NOT build:** more unit tests for already-unit-covered layers · a sector-enforce
test (**already wired**) · raw-SQL column-name assertions (single writer each; wouldn't have caught E4/W10).

**§0 (ChatGPT CT-invariant rec) — SATISFIED, no change needed:** discovery is `CT_DIR.glob("*.py")`
(`test_ct_guard_invariant.py:69-70`) — a glob, not a manual list. **PROVEN:** a brand-new module with an
unguarded live write made invariants A+B fail **with ZERO allow-list edits** (2 failed/3 passed); removing it
restored green. Fails closed; allow-list = 3 inherent entries. [[ct-guard-invariant-18jul]]

Related: [[ct-guard-invariant-18jul]] · [[ct-harness-safety-18jul]] · [[e4-w10-done-17jul]] ·
[[dual-daily-loss-mechanism]] · [[capital-operational-note]] · [[feedback-verify-rc-not-output]].
