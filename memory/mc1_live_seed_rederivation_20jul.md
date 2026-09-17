---
name: mc1-live-seed-rederivation-20jul
description: "The M-C1 live-seed cancellation survives E4/W10 — STILL SOUND but for a NEW structural reason; the original §A2's \"the reader is not involved\" was literally false, and its test pinned a numerical proxy instead of the property."
metadata: 
  node_type: memory
  type: project
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-07-20T15:55:49.923Z
---

**Re-derived 20-Jul-2026. VERDICT: STILL SOUND, NEW REASON.** Design/analysis only — no test edited,
no merge. Awaiting ChatGPT review before the E4/W10 retry.
Report: `docs/audit/mc1_live_seed_rederivation_20jul2026.md`.

**The mechanism was never in doubt** (`test_the_carryover_equals_exactly_what_phase_2_re_applies`
passes). What was void is the **reason**. Re-deriving it found the original §A2 contained a **false
structural claim that happened not to matter**:

- §A2 said *"the seed and Phase 2 never consult [the reader]"*. **FALSE** —
  `rehydrate_from_open_trades` calls `get_daily_realized_net_pnl` at **`fund_manager.py:1736`**. The
  true, narrower claim: the value is used **only as a log field**, read *after* Phase 2 (`:1703-1711`)
  and *after* the invariant check, feeding neither `_total`, nor a bucket, nor the return dict.
- ⭐ **§A2's test pinned NUMERICAL difference (`reader != carryover`) as a proxy for STRUCTURAL
  non-involvement.** The `Σcosts` gap was a *consequence* of the old contract, never the *reason*.
  **A test that pins a symptom of a property rather than the property fails on changes that don't
  threaten it, and stays silent on changes that do.** [[feedback-verify-rc-not-output]]

**The new reason (structural, and stronger):** (1) both sides draw the same rows/field from the shared
helper `_today_release_used_pnl_rows` (`:1757`) ⇒ `(net−Σ)+Σ = net` for **any** meaning of `pnl_delta`;
(2) ⭐ **the ONLY reader-derived ledger row — `RESET_PNL`, written by `reset_daily_pnl` as
`−reader(today)` (`:1603`/`:1610`) — is EXCLUDED from both sides by the helper's
`entry_type='RELEASE_USED'` filter**, so the reader's value cannot reach the cancellation under any
contract (nobody had stated this); (3) the one reader call on the path is observational.

Reader and carryover are **equal during the session** post-E4/W10 and **differ after the EOD reset**
(the reader has no `entry_type` filter, so it sees `RESET_PNL`). Neither fact touches the cancellation.

**4 falsification conditions stated** (the original had none) — the load-bearing one is #2: *if the
helper's `RELEASE_USED` filter is ever dropped or widened to admit `RESET_PNL`, independence genuinely
breaks.* 5 orderings enumerated incl. restart-after-reset and restart-after-limit-fired.

**⚠️ Separate latent found, NOT an E4/W10 blocker:** the seed (`main.py:2257`) and
`rehydrate_from_open_trades` each derive their **own** day-floor from their own `now_ist()` ⇒ a
seed/rehydrate pair **straddling midnight** breaks the cancellation. Pre-existing and
contract-independent; sibling of [[feedback-regression-must-not-cross-midnight]]. Queued, not fixed.
Fix = compute the floor once, pass to both.

**Retry-scope item:** 3 modules avoid the reader *because of* W10 (`ops_dashboard/.../risk_capital.py:38`,
`services/capacity.py:16`, `reports/daily_trade_review.py:1053`, all "approved permanent"). Post-fix they
**agree** with the new reader rather than conflict — not a defect, but their stated rationale becomes
false and must be re-labelled (attribution-gloss shape).

Related: [[e4-w10-deploy-stopped-20jul]] [[q9-live-seed-mc1-wired-19jul]] [[e4-w10-done-17jul]]
