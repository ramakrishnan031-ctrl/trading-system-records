# PRE-REGISTERED EXPECTED-DIFF **v2** — 17-Sep-2026 BOOT vs THE 16-Sep BASELINE

**Written 2026-09-16 10:25 IST — ⭐ BEFORE the first VM write.** Supersedes **v1** (`…T1007IST.md`, md5 `b5f7019c30095c1e536578f695a38710`), which is **KEPT**.
Per **AMENDMENT 12 §1** and **AMENDMENT 13 §§1–4**. Subject: `e7bf477` onto the twin `trading-sbx`.

## ⚠️ WHY v2 EXISTS — v1 CARRIED A SINK ERROR THAT WOULD HAVE FAILED A CORRECT DEPLOYMENT

Amendment 13 §1 asked whether a brand-new logger name (`sr_shadow`) can reach the log file. 🔬 **It can — but the real hazard was one layer over:** v1 did not say **WHICH SINK** each predicted line lands in, and **the two sinks have different level cut-offs**.

| 🔬 Measured from `core/logger.py` | |
|---|---|
| handlers attach to the **ROOT** logger (`root.addHandler`), ⛔ not per logger name | `core/logger.py:375,452` |
| `get_logger(name)` = `logging.getLogger(name)`; ⛔ **handlers are NOT attached per name** | `core/logger.py:266-273` |
| **no `Logger.propagate = False` anywhere** in the codebase | grep: 0 hits (all "propagate" hits are prose about *exceptions*) |
| `system_*.log` filter = **`_SystemFilter` → `record.levelno >= INFO`, a pure LEVEL catch-all, ⛔ NO name restriction** | `core/logger.py` `_SystemFilter` |
| ⛔🔴 **stdout handler is `setLevel(WARNING)`** — and the unit sends **stdout+stderr → journal** | `core/logger.py:420`; `trading-system.service` |
| `system_*.log` is **JSON lines**, fields `ts` · `level` · `logger` · `msg` (+extras) | `_JsonFormatter` |

> ⛔🔴🔝 **CONSEQUENCE: EVERY `INFO` LINE IS ABSENT FROM THE JOURNAL.** The journal only ever receives **WARNING and above**. ⭐ **All three of the "must appear" rows are INFO** ⇒ they exist **ONLY** in `logs/system_2026-09-17.log`. ⚠️ **Had Gate 7/8 looked for them in the journal, it would have found them absent and declared "the manager did not come up" — stopping a CORRECT deployment.** That is precisely the failure §1 warned about.

- ⚠️ `_safe_log` **swallows silently** (`except Exception: pass`, `runner.py:218-221`) ⇒ a logging failure inside the worker is ⛔ invisible. The routing above is verified, so this is a residual note, ⛔ not an expected event.

---

## SINK MAP — check each row in the RIGHT file. ⛔ Absence in the wrong sink is NOT a finding.

| Predicted event | level | `logs/system_2026-09-17.log` | journal |
|---|---|---|---|
| E1.1 `sr_shadow: worker started …` | INFO | ✅ **YES** | ⛔ **NO** |
| E1.2 `sr_shadow: ENABLED and started …` | INFO | ✅ **YES** | ⛔ **NO** |
| E2.3 `effect_telemetry: composition OK …` | INFO | ✅ **YES** | ⛔ **NO** |
| E3.5 `sr_shadow: worker stopped …` | INFO | ✅ **YES** | ⛔ **NO** |
| E4.6 `sr_shadow wiring failed …` | ERROR | ✅ YES | ✅ YES |
| E4.7 `composition assertion FAILED …` | **CRITICAL** | ✅ YES | ✅ YES |
| E4.8 `sr_shadow: drain error=…` | ERROR | ✅ YES | ✅ YES |
| E4.9 `sr_shadow.stop_invariant_violated …` | ERROR | ✅ YES | ✅ YES |
| E5.11 `…no market-data kite handle…` | WARNING | ✅ YES | ✅ YES |
| E5.12 `sr_shadow capture failed for …` | ERROR | ✅ YES | ✅ YES |

---

## E-1 — NEW AT BOOT (each MUST appear **exactly once**, in `system_2026-09-17.log`)

| # | `logger` | `level` | `msg` | Source |
|---|---|---|---|---|
| 1 | **`sr_shadow`** | INFO | `sr_shadow: worker started (contract=v1.3 schema=1 db=<resolved>/sr_shadow.db)` | `sr_shadow/runner.py:151` via `_safe_log` |
| 2 | **`main`** | INFO | `sr_shadow: ENABLED and started (mode=LIVE, log-only)` | `main.py` `_log.info`; 🔬 `_log = get_logger("main")` (`main.py:113,2187`) |

- 🔬 `CONTRACT_VERSION="v1.3"`, `SCHEMA_VERSION=1` (`sr_shadow/params.py:21-22`); db filename `sr_shadow.db` (`store.py:30`). ⚠️ **The db PATH PREFIX is runtime-resolved ⇒ normalized, ⛔ not predicted** (see the ruleset).
- 🔬 `mode_label = str(args.mode or "live").upper()` ⇒ **`LIVE`** (unit runs `--mode live`).
- ⭐ **MULTIPLICITY (Amendment 13 §4):** each **exactly 1**. **0 ⇒ a FINDING** (the manager did not come up). **2 ⇒ an ANOMALY** (double construction).
- ⭐ **ORDER:** `start()` is called **before** the `ENABLED and started` line in the same function ⇒ **E1.1 precedes E1.2**. ⛔ This is the ONLY order this list asserts — 🔬 it is proven by the SOURCE. ⛔ **Incidental baseline ordering is NEVER promoted to a contract.**

## E-2 — CHANGED

| # | Event | Predicted change |
|---|---|---|
| 3 | `effect_telemetry: composition OK (%d registered, %d expected)` (`core/effect_telemetry.py:190`, **INFO**) | ⭐ **BOTH counts exactly +1** vs baseline. **Three deltas stay DISTINCT, ⛔ never merged:** (a) **+1/+1 ⇒ PASS**; (b) **+1 expected, +0 registered ⇒ ⛔ STOP** — the manager did **not** register; (c) **any other delta ⇒ ⛔ STOP**. ⛔ **The asymmetric case (b) is NEVER downgraded to a warning.** |
| 4 | the config-hash line | ⛔ **"hash changed" is NOT proof of a correct deployment.** Record **all three**: the **baseline** hash, the **expected** hash, the **observed** hash. 🔬 The YAML goes `351bd82e…` → `4eab1ae5…`. |

## E-3 — NEW AT EOD SHUTDOWN (17-Sep ~17:35) — ⭐ **a SEPARATE observation window from boot**

| # | `logger` | `level` | `msg` |
|---|---|---|---|
| 5 | `sr_shadow` | INFO | `sr_shadow: worker stopped counters={…} history={…}` (`runner.py:158`) |

- ⛔ **The boot window and the EOD window are observed SEPARATELY.** E-3's absence at **boot** is expected and is ⛔ not a finding.

## E-4 — MUST REMAIN ABSENT (presence ⇒ ⛔ STOP → ordered rollback)

| # | Event | level / sink |
|---|---|---|
| 6 | `sr_shadow wiring failed (continuing without it): …` | ERROR · both |
| 7 | `effect_telemetry composition assertion FAILED: …` | **CRITICAL** · both — ⛔ grep explicitly; in live it CRITICALs and **continues** |
| 8 | `sr_shadow: drain error=…` | ERROR · both |
| 9 | `sr_shadow.stop_invariant_violated …` | ERROR · both |
| 10 | **CRITICAL set comparison** | ⭐ Compare the **baseline CRITICAL SET** against the **post-deploy CRITICAL SET**. ⛔ **A CRITICAL already present in the baseline is NOT new** — only set-difference members are findings. |

## E-5 — PREDICTED **UNCHANGED**

| # | Event | Why |
|---|---|---|
| 11 | `sr_detector/retest enabled but no market-data kite handle (no token?) — fetches will fail safe (fetch_failed rows)` (WARNING) | ⭐🔬 **The sharpest prediction.** `main.py` adds `_sr_shadow_on` to the `_md_kite` build condition, so a naive read expects a possible NEW warning. ⛔ **It cannot appear:** the twin's live config already has `sr_detector.enabled: true`, `v3_chain_mode: "shadow"`, `watchlist.enabled: true` ⇒ that branch was **already taken**. ⇒ presence/absence must **match the baseline exactly, in BOTH sinks**. |
| 12 | `sr_shadow capture failed for <symbol>: …` | ⭐ **Row 12 means: NO BOOT-TIME APPEARANCE EXPECTED.** ⛔ It is **not** a claim that it can never occur — a capture failure during the session is a **RUNTIME FINDING**, adjudicated on its own, ⛔ not a boot-diff anomaly. |
| 13 | anything from `core/config_loader.py` | 🔬 its 75-line diff is **pydantic schema only — 0 logging statements** ⇒ no output at all |
| 14 | everything else | 🔬 `signal_processor.py` adds a ctor kwarg + a runtime path; `expected_managers.yaml` is data consumed by row 3 |

---

## How Gate 7/8 uses this
1. **Verify the frozen artifacts first:** baseline (both sinks), **this file**, and the **normalization ruleset** — each at its recorded filename + size + md5. ⛔ Any mismatch ⇒ **STOP**, the test is void.
2. Normalize **only** per the frozen ruleset. ⛔ **Never widen it.**
3. Compare as **normalized semantic events**, ⛔ not raw lines; check each row **in its correct sink**.
4. Classify every difference into E-1…E-5 or **UNPREDICTED**. **UNPREDICTED ⇒ adjudicate** · **E-1/E-2 absent ⇒ a finding** · **E-4 present ⇒ STOP**.
5. ⛔ **THE PREDICTION IS CLOSED FROM THE FIRST VM WRITE.** A legitimate missed event is recorded as a **MISS IN THE PREDICTION**, ⛔ never as a late addition.
