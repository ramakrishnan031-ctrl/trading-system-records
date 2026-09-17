---
name: e4-w10-deployed-20jul
description: "E4/W10 DEPLOYED 20-Jul at a266432 — fm_ledger.pnl_delta is NET, the reader stops double-subtracting costs; gate passed with comm merge-only = 0; verification is tomorrow's EOD reset (18.29 shape, not 19.61)."
metadata: 
  node_type: memory
  type: project
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-07-21T17:18:48.209Z
---

**E4/W10 DEPLOYED 20-Jul-2026 22:16 IST — `a266432`, tag `deploy-20jul-e4-w10-pnl-contract`.**
`PC == origin == VM bare`; schema v44, no migration; service left **`inactive`** (restarts itself
after the 08:15 token refresh). Report: `docs/audit/e4_w10_deploy_20jul2026.md`.

**⭐ THE SEQUENCING IS THE REUSABLE IDEA.** C3 — the test whose false premise stopped the first
attempt — was **removed from the migration entirely** by noticing its replacement is
**contract-agnostic**: it pins structural facts true on both sides of the change. So it was written,
plant-verified and pushed **on main at `e8313f0` BEFORE the merge existed**. *When a migration
includes a risky test edit, check whether the replacement is contract-agnostic — if it is, ship it
first and the migration shrinks.* [[mc1-live-seed-rederivation-20jul]]

**Verified able to FAIL, not merely green** (plant-and-restore, `capital/` 0 modified after):
Plant A (helper widened to admit `RESET_PNL`) → only the reset test failed, on its intended assertion,
carryover −18094.54 → 94.54 — **the residue is exactly Σcosts**. Plant B (`_total += daily_pnl` at
`:1736`) → only the observational test failed, `_total` −999,528,765.44 vs 471,234.56.

**THE GATE (same-window double regression, `comm -23` on SETS — no fixed baseline):**
BASE `e8313f0` 33 failed / 5002 collected / **1 xfailed** · MERGE `a266432` 32 / 5022 / **0 xfailed**.
**MERGE-ONLY = 0.** Predicted in advance and confirmed: `xfailed` 1→0, collected **+20**.
BASE-ONLY = 1 (`test_instance_lock` p2) — **investigated, not waved away**: E4/W10's whole `main.py`
diff is two `cost_calculator=` kwargs, and 5 runs on the *same* merged tree gave 1,2,2,2,2 failures ⇒
run-to-run flakiness in a PC-only concurrency test. [[feedback-no-fixed-test-baseline]]

**C1's strict xfail did exactly its job** — it XPASSed on the first merge, was reported as a FAILURE,
stopped that deploy, and forced the flip to be deliberate. **C2 was re-aimed, not merely inverted**: a
bare `reader == truth` would duplicate C1, so it now guards the failure mode E4/W10 *creates* —
`round_trip_costs_or_zero` is **FAIL-OPEN**, so a silent degradation to 0.0 would make `reader == truth`
hold **trivially** with cost accounting dead. It asserts `costs > 0` first.

**✅ VERIFIED IN PROD 21-Jul (~19:30 IST, read-only).** The first `RESET_PNL` written by `a266432`
(ledger_id 9283, 15:17:08) = **+18.82 = −Σpnl_delta** over the day's 5 RELEASE_USED rows (net −18.82),
NOT the old **21.04** = `−(Σpnl−Σcosts)` (Σcosts=2.22). Zeroing invariant `SUM(pnl_delta) all rows =
−0.000000`; `reason='EOD reset: previous pnl=-18.82'` agrees. **Shape 18.82/21.04 ≠ the 20-Jul
illustration 18.29/19.61** — today's book differed (5 closes, not 3; the fix_sprint's midday "≈+12.57"
predated 2 later closes); the STRUCTURE (obs == −Σpnl_delta, off the old shape by exactly Σcosts) is
what's tested and holds exactly. Query date-scoped to 21-Jul ⇒ 20-Jul's old 19.61 row untouched
(caveat respected). Cross-day capital continuity exact: Mon close 9857.31 → Tue open 9857.30 → Tue
close(Sys) 9838.48 = −18.82. ⚠️ SIDE-FLAG (not E4/W10, TRACED 21-Jul → `broker_closing_capital_zero_21jul2026.md`):
`[3_Capital]` REVIEW because **Closing Capital—Broker = ₹0** = `daily_report.py:195` reads the LAST
fm_ledger row's `balance_after`, which is RESET_PNL's hardcoded 0.0. **RECURRING (₹0 on 11/15 July days),
a report mislabel — NOT a capture gap; nothing in any control/gate/sizing consumes it** (thresholds use
opening/INIT). ❌ My earlier "Monday=₹9858.63" was WRONG (Monday cell was ₹0; I'd conflated the broker
account delta). Observability, not integrity; queue with C1/B2′ false-daily class. **+ `gemini_watchman`'s 21-Jul
"Rs 0 / 100% loss" CRITICAL is an INDEPENDENT LLM CONFABULATION** (it tails LOGS, not this field —
`gemini_watchman_alerts_21jul2026.md`): NOT a 5th reader, verdict STANDS; its "6 active vs max 5"
REFUTED (max concurrent open on 21-Jul = **1**, cap=5 never breached). Watchman = observe-only, confabulates
specifics; treat as a prompt-to-check, never fact.

**Rollback:** `git revert -m 1 a266432 && git push origin main` — schema-free, no ledger unwind, minutes.
Backup retained: `data_store/backups/pre_deploy_e4_w10_20260720.db` (`quick_check=ok`).

**Queued from this work:** the **midnight day-floor hazard** (seed `main.py:2257` and rehydrate each
derive their own `now_ist()` floor ⇒ a pair straddling midnight breaks the cancellation; pre-existing,
contract-independent) · **re-label the 3 W10-workaround modules** (`risk_capital.py:38`,
`capacity.py:16`, `daily_trade_review.py:1053`) whose "approved permanent" rationale is now false.
Also recorded: `push --tags` incidentally pushed a stale local tag `phase-a-pre-spine-fix` (harmless).

Related: [[e4-w10-deploy-stopped-20jul]] [[e4-w10-done-17jul]] [[e4-w10-outcome-impact-19jul]]
