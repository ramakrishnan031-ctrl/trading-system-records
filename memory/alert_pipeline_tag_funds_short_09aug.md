---
name: alert-pipeline-tag-funds-short-09aug
description: "BUILT 09-Aug (uncommitted) — funds-short Telegram alert + [MODE][PIPELINE] header, answering Rama's two alert questions. Includes the measured ordering facts and a deployed alert that has never fired."
metadata: 
  node_type: memory
  type: project
  originSessionId: d9595f8a-8cb4-47fd-9b87-a97e7c891339
  modified: 2026-08-09T05:58:39.684Z
---

# 📣 RAMA'S TWO ALERT QUESTIONS — `<BUILT 09-Aug · UNCOMMITTED · NOT PUSHED · NOT DEPLOYED>`

📜 **Rama, 09-Aug:** ① *"funds not sufficient … can I get a Telegram alert — funds unavailable, scrip name, qty, intended entry / SL / TGT?"* ② *"Separate identifiable Telegram alerts for MIS and GTT?"*

## 🔬 THE MEASUREMENTS THAT DECIDED THE DESIGN — ⛔ traced, not inferred from names

| question | answer | evidence |
|---|---|---|
| Does a funds shortfall alert today? | 🔴 **NO — Telegram-silent** | the `_PipelineReject` handler logs **INFO**, sets `REJECTED_RESERVE_FAILED`, bumps a counter; **`EXPIRED` is the ONLY reject code that notifies** |
| 🔑 **Does `qty` exist at rejection?** | ✅ **YES — the whole question, and it lands well** | sizing is **step 5**; `reserve()` is **step 7** and takes **`sizing.qty` as an ARGUMENT** ⇒ qty · entry · SL all resolved |
| Is TGT resolved? | ⚠️ **NOT COMPUTED — but DERIVABLE** | `_derive_target(entry, sl, strategy)` runs AFTER the reserve, and is a **pure function of three values already in hand** (no broker, no quote) |
| Does a pipeline marker exist? | ⭐ **YES — in exactly ONE alert** | the loss governor's `f"[{mode}][{pipeline.upper()}] …"`. ⛔ **NOT rebuilt** — its shape is the precedent everything else now follows |

⛔ **`_bucket_for_intent`'s own intent sets are imported for the tag** — a second local copy is how the label and the bucket the money left silently diverge.

## 🔴 TWO THINGS THE MEASUREMENT FOUND THAT NOBODY ASKED ABOUT
1. **A DEPLOYED ALERT THAT HAS NEVER BEEN DELIVERED:** `self._notifier.send_warning(...)` (the EXPIRED alert) — **`send_warning` is defined NOWHERE** *(width: repo-wide `def send_warning` ⇒ **0**; call sites ⇒ **1**)*, in **BOTH** trees; the `AttributeError` dies in a bare `except Exception: pass`. ⚠️ Its 60 s limiter has therefore never limited, **and it stamps the timestamp BEFORE the send** ⇒ a fix alone still eats the first alert. ⛔ **REPORTED, NOT FIXED** (register `N9-14`) — making a never-fired alert start firing is an unrequested behaviour change on the live signal path.
2. **The new-signal alert titled EVERY signal *"🟢 INTRADAY SIGNAL"*, delivery included** — with the books independent that is a **WRONG** label, ⛔ not a missing one. ✅ Fixed here.

## WHAT WAS BUILT
- **`ReservationResult.failure_code`** *(default `""` ⇒ every existing caller unchanged)*: `INSUFFICIENT_CAPITAL` | `INVALID_INPUT`. ⭐ **`reserve()` returned `success=False` for two different reasons with only PROSE to tell them apart** — the alert had to branch, and "never classify by free text" had no structured status to classify by. **This is that status.**
- **`_emit_funds_short_alert`** — same `notifier.send(...)`, ⛔ no parallel path. Reports TGT as **"not derived"** rather than inventing one.
- **`_pipeline_for_intent` / `_alert_prefix`** ⇒ `[MODE][INTRADAY|DELIVERY]`. ⚠️ **An unknown intent emits NO tag: a wrong pipeline on a capital alert is worse than a missing one.**
- **Rate limit: ONE PER SYMBOL PER DAY**, keyed on the **ISO date** ⇒ resets on the DATE CHANGE, ⛔ needs no boot and no cleaner, and a prior day can never suppress today. ⭐ Chosen over a digest because the information is actionable **while the market is open**.
- **15 tests** (`tests/unit/test_funds_short_alert.py`), all green. ⭐ Includes an explicit anti-vacuity test: same shortfall wording with **no** `failure_code` ⇒ **no alert**.

## 🔴 I SHIPPED A REGRESSION AND THE GATE CAUGHT IT — ⛔ recorded, not smoothed over

**Gate run 1: 18 failed** = the baseline 9 **+ 9 MINE** (`test_alert_direction_eod_29jun` ×2, `test_signal_alert_capital_vocabulary` ×7). **CAUSE:** I made `_emit_signal_alert` call `self._alert_prefix(...)`, an INSTANCE method. Those tests call the formatter on a **three-attribute stub** on purpose, so the call raised **inside the helper's own `except Exception`** ⇒ ⛔ **the alert vanished SILENTLY** — the *same shape* as the `send_warning` defect found the same hour. ⭐⭐ **AND MY OWN 14 TESTS WERE BLIND TO IT** — they always used a real processor. **The OLD tests caught it.** 📌 **That is the argument against editing a red test to match new code before understanding what it protected: the red was right and my green was the narrow one.** ✅ **FIXED PROPERLY, ⛔ not by touching those tests:** `_alert_prefix` is now a `@staticmethod(mode, intent)` and both helpers are called CLASS-QUALIFIED, so the formatter has no dependency on the live instance. **+1 regression guard pinning exactly that** (emit on a bare stub).

✅ **GATE run 2 — `pytest tests/unit tests/integration` from Git Bash (⛔ never `run_tests.py`, ⛔ never PowerShell's `bash`): `PYTEST_RC=1` · 9 failed · 5,681 passed · 4 skipped · 892 s.** ⭐ **SET-COMPARED, ⛔ not counted: `comm` EMPTY BOTH WAYS against the branch's recorded 9.** ⭐ **And the passed arithmetic closes exactly: 5,666 (branch baseline) + 15 new = 5,681.** 🕛 Started ~11:50 IST, ended ~12:05 — ⛔ no midnight crossing.

## ✅ PARITY — MEASURED
**Paper reaches the funds path.** `FundManager` is mode-blind; `main.py` states *"paper mode: `get_margins()` returns static `paper_capital` — follows the identical code path (paper/live parity)"*; mode is a `--mode paper|live` flag. ⭐ **A rare NON-member of [[paper-cannot-exercise-class-26jul]]** — tests run both. ⚠️ Whether it *fires* in paper depends on the configured paper capital.

## ⚠️ OPEN / OWED
- ⛔ **UNCOMMITTED, and deliberately: the worktree sits on `feat/delivery-config-split`, which carries the FROZEN sizing build and schema v46.** A commit there joins the set GO/NO-GO line 9c must prove non-ancestor. ⭐ **Gate lines are ref-based, so uncommitted PC work cannot affect Monday** — but the branch for this work is **Rama's call.**
- **Q2 is PARTIAL by measurement: ~80 `notifier.send(` sites exist in the runtime path.** Tagged here: the signal alert + the new funds alert (+ the loss governor already). ⛔ **A blanket sweep is NOT done — many alerts have no pipeline at all and forcing a tag would fabricate one.** 🔴 **Rama to scope the remainder.**

See also [[feedback-never-classify-by-free-text]] · [[daily-resets-clock-bound-06aug]] · [[two-pipeline-split-08aug]]
