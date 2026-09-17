---
name: c5-c5b-risk-pct-card03-09aug
description: "MEASURED — C5/C5b fire in the UNPUSHED tree only; the deployed auditor returns C_ok. Retiring risk_per_trade_pct DELETES C5's real finding. The 4.2% line's x2 has no author. DECISION_CARD_03 awaits Rama."
metadata: 
  node_type: memory
  type: project
  originSessionId: d9595f8a-8cb4-47fd-9b87-a97e7c891339
  modified: 2026-08-09T05:26:09.271Z
---

**09-Aug-2026 (Sun). `DECISION_CARD_03.txt` written to `Downloads/`. ⛔ NOTHING CHANGED — key, value, auditor, thresholds and both alarms untouched.**

## 🔴 THE PREMISE I WAS GIVEN DID NOT SURVIVE MEASUREMENT

⛔ **"C5b FIRES EVERY MORNING" IS FALSE TODAY — and so is any claim that C5 does.** Both are properties of the **UNPUSHED** tree.

**(P) MEASURED, not read** — the real `_group_c_capital_relative` extracted from BOTH trees and run against BOTH configs (stdlib-only module ⇒ no `.env`, no DB; script in scratchpad):

| | auditor | config | result |
|---|---|---|---|
| **A — the VM today** | `origin/main` (`645728d`) | `origin/main` | ⭐ **`[PASS] C_ok` — SILENT. No C5. No C5b arm exists at all.** |
| **B — after the split deploys** | worktree | worktree | 🔴 **`[WARN] C5` (6.0% vs 4.2%) + `[WARN] C5b` (3.6% vs 1.8%)** |

⭐ **The green could have gone red — B did, on the same harness.** ⛔ Deployed C5 cannot fire arithmetically either: `0.01 × 5 = 5%` vs `0.03 × 2 = 6%`. The **normalisation**, not the slot bump, is what makes C5 fire.
⚠️ The build record said *"it will WARN every morning at boot"* (future, correct); **register rows N9-01/N9-02 compressed it to present tense.** ✅ **DONE 09-Aug (LATER), Rama explicitly authorised it: both rows CORRECTED in place (tense + severity, wrong text QUOTED not deleted) and `N9-12` opened for the drift itself — N 244 → 245.** ⇒ [[feedback-tense-drift-09aug]] · [[extracted-validator-technique-09aug]].

## 🔑 THE QUESTION WAS RE-POSED — `DECISION_CARD_04` SUPERSEDES 03

📜 **Rama, 09-Aug (via ChatGPT's reframe, which he accepted):** *"The next decision is NOT 'should we delete `risk_per_trade_pct`?' It is **'WHAT THRESHOLD SHOULD C5 REPRESENT?'**"*
⭐⭐ **AND THE SUBSTANCE UNDER IT IS THE REAL ITEM: `6 × ₹87.50 = ₹525` against a `3% × 70% × ₹10,000 = ₹210` daily stop ⇒ ~2.5×, and the stop is REALISED-loss based so near-simultaneous stop-outs outrun it.** ⛔ **No config change removes that — only fewer slots, a smaller slice, tighter stops, or a deliberate acceptance.** ⛔ **Card 03's A/B/C/D is WITHDRAWN — asking the housekeeping question and the substantive one together is what made it unanswerable.** ⛔ **NO THRESHOLD PROPOSED BY US: a number we pick has the same defect as 4.2 %.** 🗓️ **Timing: before the SIZING REBUILD deploys (no date, frozen) — ⛔ NOT a Monday item.**
**(P) Card 04's arithmetic re-run:** 6/5/4/3/2 slots = `₹525 / ₹437.50 / ₹350 / ₹262.50 / ₹175` ⇒ ⛔ **a slot cut alone does NOT fix it — 3 slots is still ₹262.50, it only crosses under ₹210 at 2.** Slice would need `₹5,833 → ₹2,333` (−60 %); the daily stop would need `3 % → 7.5 %` of the intraday pot.

## 🔑 WHERE THE 4.2% CAME FROM — THERE IS NO AUTHOR

`threshold = daily_loss_limit_pct × intraday_bucket × 2`. **The ×2 entered at `f1dc556` (02-Jun-2026, FIX-147, "pre-live safety batch", Co-Authored-By Claude Sonnet 4.6)**, carried into BUILD 2 `eb373c4` verbatim. Its own comment explains the *comparison* and **never the doubling**.
⛔ **Search width: every file under `docs/` for `2x daily` · `2× daily` · `twice the daily` · `2x the daily` · `factor of 2` · `dll * 2` ⇒ ZERO hits.** ⇒ **4.2% is not a designed ceiling; it is twice a real limit, doubled freehand.** ⭐ That changes what C5 *means* — it is not "a designed ceiling was crossed".

## ⭐ THE ANSWER THE RULING TURNS ON — RETIREMENT **DELETES** C5

- **C5b** — LHS is `delivery_risk_per_trade_pct` ⇒ retirement removes it, and **nothing of value is lost: 0.6% real vs 1.8%, it is FALSE.** ✅ Closed cleanly.
- 🔴 **C5** — LHS is `risk_per_trade_pct`, but the finding is **NOT**: `₹5,833 × 1.5% × 6 = ₹525 = 5.25%` comes from **allocation × stop × slots**, none of which is the key. ⛔ **Retire and the only check that noticed disappears with it.**
- ⭐ **Narrower than it sounds:** the *runtime* daily stop is untouched (`fund_manager.py:1358`). What is lost is the **config-time advance warning**, not the stop.
- ⛔ **Search width for "only check": `core/ capital/ risk/` for `cumulative` · `aggregate.*risk` · `total open risk` ⇒ only C5/C5b** (plus an unrelated fill-qty comment and the per-strategy realised-P&L governor).

## ⚠️ RETIREMENT IS NOT A ONE-LINE DELETE — IT FAILS THE BOOT TWICE

- `PositionSizingConfig` is `extra="forbid"` **and** `risk_per_trade_pct: float` is **REQUIRED with no default** ⇒ **YAML line alone ⇒ ValidationError; model field alone ⇒ ValidationError.** ⛔ Both sides must land together (`D1` — NO PARTIAL DEPLOY).
- The delivery twin is **fail-closed in TWO places** once delivery is active: `config_loader._validate_delivery_policy_complete` and `pipeline_policy` `req(...)`.
- **Size:** ~10 working files (2 comment-only) + **51 test files** + 27 docs mention it.

## ✅ RECONCILIATION CHECKED, ⛔ NOT TWO ERRORS OFFSETTING
`5.25%` and `0.60%` **independently recomputed** from `bucket × leverage ÷ max_daily_trades`: intraday `₹7,000×5÷6 = ₹5,833.33`, worst intraday stop **1.5%** (max of 15 strategy YAMLs, range 0.8–1.5) ⇒ `₹87.50 × 6 = ₹525`. Delivery `₹3,000×1÷6 = ₹500`, stop **2.0%** (all 3 positional YAMLs) ⇒ `₹10 × 6 = ₹60`. ⛔ **`5.25% ≠ 6.0%` — the stale formula does NOT produce the same figure**, it produces the same *conclusion*. Both exceed 4.2%. ⭐ `₹525` is a proper UPPER bound (assumes 6 HIGH-tier full-allocation fills all stopping out).

## 📣 SURFACING & PARITY — MEASURED, ⛔ NOT ASSUMED
- Native severity is **`WARN`, ⛔ NOT `CRITICAL`**: pre-flight group C is `Criticality.WARN`; Control Tower `CONFIG_MAP` maps `WARN → HIGH`. ⚠️ The thread card's *"known-false CRITICAL"* overstates it.
- **PAPER EXERCISES IT IDENTICALLY.** `_cross_field_sanity_checks` is a `@model_validator(mode="after")` on `SystemConfig` ⇒ runs on **every** config load; mode is a `--mode paper|live` CLI flag, **ONE `system_config.yaml`**, and group C reads only `position_sizing`/`risk`/`capital` — none mode-dependent. ⭐ A rare non-member of [[paper-cannot-exercise-class-26jul]].

## THE CARD
Four options (retire · fix the checks · **both** · nothing) + a timing question. ⭐ **Option "both" was ADDED** — the three I was handed excluded the only one that closes all three register rows, and presenting "this closes it" when it does not is the very defect the card indicts. Rollback stated per `G11` two-claim rule: **② is EMPTY here** — no money, no order, no broker effect; the only effect is a warning line and a printed number ceasing.

See also [[two-pipeline-split-08aug]] · [[reversibility-two-claims-08aug]] · [[feedback-verify-the-finding-premise]] · [[feedback-absence-needs-wide-check]] · [[tautological-check-class-05aug]]
