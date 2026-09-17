# PRE-REGISTERED EXPECTED-DIFF — 17-Sep-2026 BOOT LOG vs THE 16-Sep BASELINE

**Written 2026-09-16 10:07 IST — ⭐ BEFORE the baseline was frozen and BEFORE the first VM write.**
Per **DEPLOYMENT CARD AMENDMENT 12 §1**. Subject: `e7bf477` (S&R SHADOW v1.3) onto the twin `trading-sbx`.

> ⛔🔴🔝 **THE RULE THAT MAKES THIS A TEST RATHER THAN A RATIONALISATION**
> - Anything in tomorrow's diff that is **NOT on this list** is an **ANOMALY TO ADJUDICATE**, ⛔ not a line to explain away.
> - Anything **ON this list that is ABSENT** is **equally a finding** — a predicted startup line that never appeared means **the manager did not come up**.
> - ⛔ **DO NOT AMEND THIS LIST AFTER SEEING TOMORROW'S LOG.** If something legitimate was missed, it is recorded as **a MISS IN THE PREDICTION**, ⛔ never as a late addition.
> - ⭐ An expected list written **while looking at the diff** is not a test. This one was written **~7.5 hours before the deployment window**, from committed code only.

**Provenance:** 🔬 derived from `git diff 970aabf..e7bf477` over the four wiring files + the `e7bf477` `sr_shadow:` config block, and from the twin's **live pre-deploy** `system_config.yaml` (`351bd82e…`). ⛔ No VM contact was made to produce this.

---

## E-1 — NEW AT BOOT (these MUST APPEAR; absence is a finding)

| # | Predicted line | Source | Notes |
|---|---|---|---|
| 1 | `sr_shadow: worker started (contract=v1.3 schema=1 db=<…>/data_store/sr_shadow/sr_shadow.db)` | `sr_shadow/runner.py:151` via `_safe_log`, logger name **`sr_shadow`** | 🔬 `CONTRACT_VERSION="v1.3"`, `SCHEMA_VERSION=1` (`sr_shadow/params.py:21-22`); db filename `sr_shadow.db` (`store.py:30`). ⚠️ The **path prefix** is whatever `build_sr_shadow` resolves — ⛔ do not treat the prefix as predicted. |
| 2 | `sr_shadow: ENABLED and started (mode=LIVE, log-only)` | `main.py` `_log.info`, root logger | 🔬 `mode_label = str(args.mode or "live").upper()` ⇒ **`LIVE`** (the unit runs `--mode live`). |

- ⭐ **ORDER IS PREDICTED TOO:** `sr_shadow.start()` is called **before** the `ENABLED and started` line ⇒ **#1 precedes #2**. A reversed order is an anomaly.

## E-2 — CHANGED (must differ, in exactly this way)

| # | Line | Predicted change |
|---|---|---|
| 3 | `effect_telemetry: composition OK (%d registered, %d expected)` (`core/effect_telemetry.py:190`) | ⭐ **BOTH counts exactly +1** vs the baseline's line. 🔬 `expected_managers.yaml` gains exactly one entry (`sr_shadow`, `state: expected-active`). ⛔ **+1 on `expected` but NOT on `registered` = the manager did not register ⇒ STOP.** |
| 4 | the config-hash line | changes (already named by Gate 7/8). 🔬 The YAML goes `351bd82e…` → `4eab1ae5…`. |

## E-3 — NEW AT EOD SHUTDOWN (17-Sep ~17:35, ⛔ not at boot)

| # | Predicted line | Source |
|---|---|---|
| 5 | `sr_shadow: worker stopped counters={…} history={…}` | `sr_shadow/runner.py:158`, called from `_shutdown` |

## E-4 — MUST REMAIN ABSENT (presence = failure ⇒ STOP → ordered rollback)

| # | Line that must NOT appear | Source |
|---|---|---|
| 6 | `sr_shadow wiring failed (continuing without it): …` | `main.py` — construction failed; in **live** this does ⛔ not stop the boot |
| 7 | `effect_telemetry composition assertion FAILED: …` | `core/effect_telemetry.py:197` — ⛔ **grep for this explicitly**; in live it CRITICALs and continues |
| 8 | `sr_shadow: drain error=…` | `runner.py:166` |
| 9 | `sr_shadow.stop_invariant_violated …` | `runner.py:216` |
| 10 | **any new `CRITICAL`** not present in the baseline | — |

## E-5 — PREDICTED **UNCHANGED** (a change here is an anomaly)

| # | Line | Why it must not change |
|---|---|---|
| 11 | `sr_detector/retest enabled but no market-data kite handle (no token?) — fetches will fail safe (fetch_failed rows)` | ⭐🔬 **The key prediction.** `main.py`'s diff adds `_sr_shadow_on` to the `_md_kite` build condition. On the twin that branch was **ALREADY TRUE**: live config has `sr_detector.enabled: true` (`_v1_on`), `v3_chain_mode: "shadow"` (`_v3_chain_on`), `watchlist.enabled: true` (`_watchlist_on`). ⇒ `_build_market_data_kite` was **already being called**, so this warning's **presence/absence must MATCH the baseline exactly**. |
| 12 | `sr_shadow capture failed for <symbol>: …` (`signal_processor.py`) | runtime-only, on a screener-passed signal ⇒ ⛔ absent at boot |
| 13 | everything produced by `core/config_loader.py` | 🔬 its 75-line diff is **pydantic schema only — 0 logging/print statements added** ⇒ no boot output at all |
| 14 | everything else in the boot log | 🔬 the other wiring diffs add no boot-time output: `signal_processor.py` adds a ctor kwarg + a runtime capture path; `expected_managers.yaml` is data read by the composition check (row 3) |

---

## How Gate 7/8 uses this tomorrow
1. Diff tomorrow's boot log against the **FROZEN** baseline artifacts — ⛔ never against a fresh reconstruction of today.
2. Classify **every** differing line into E-1 / E-2 / E-3 / E-4 / E-5, or **UNPREDICTED**.
3. **UNPREDICTED ⇒ adjudicate as an anomaly.** **E-1 or E-2 absent ⇒ a finding.** **E-4 present ⇒ STOP → ordered rollback.**
4. Record the outcome **including any MISSES in this prediction**, ⛔ without editing this file.
