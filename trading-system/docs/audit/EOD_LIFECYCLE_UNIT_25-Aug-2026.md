# EOD LIFECYCLE UNIT — BUILD RECORD

**25-Aug-2026, IST.** 🏷️ **`BUILT · GATED · ⛔ UNPUSHED · ⛔ UNDEPLOYED`.**
👤 Authorised: *"Proceed with implementation/design validation… No deployment authorization implied."*

📍 **UNIT `02a2a6b828c25660a0d8905d2adc97d37568e434`** on branch
`fix/eod-lifecycle-pipeline-aware-25aug`, base **`195436bb6323c981d68f313ad7c39858cc0a4653`**
(the deployed HEAD, confirmed two ways this session).
📍 **THROWAWAY WORKTREES** under the session scratchpad: `eod-work` (unit) · `eod-base` (base).
⛔ The ROOT worktree was **not** committed, switched or cleaned — it stayed on
`feat/delivery-config-split` with its 71 pre-existing modifications untouched.
📄 **Frozen prediction:** `docs/audit/PREDICTION_eodlifecycle_25-Aug-2026.md`,
md5 **`199ac19a61835cddfa89885b4132a63a`**, **selector = WHOLE FILE, 78 lines**, frozen BEFORE the
build.

⚠️ **M3 — every line number below holds ONLY at the SHA named beside it.**

---

## 1 · THE IDENTITY-RESOLUTION PATH

👤 Rama's correction governs: **identity is normally KNOWABLE**, so the normal path is
**resolution**, not defence.

```
order/position ──> trades.strategy ──> strategy YAML `intent:`   ← PRIMARY
               └─> orders.product (leg='ENTRY') ──> PRODUCT_TO_INTENT  ← SECOND, INDEPENDENT
```

| both known & DISAGREE | **CONFLICT** → requires the service **+ CRITICAL report** |
| strategy known | resolved = strategy intent |
| only product known | resolved = product intent |
| neither | **UNRESOLVED** → requires the service **+ CRITICAL report** |

⇒ ⭐ **The defensive case is a CONFLICT between two sources that BOTH exist** — a NULL check would
pass exactly that straight through.

### 🔴 AND ONE CORRECTION THE BUILD FORCED: identity ≠ protection

🔬 `PRODUCT_TO_INTENT` maps **`NRML` → `DELIVERY`** (`core/constants.py:5-10`). Resolving NRML to the
delivery pipeline and then treating it as *"broker-protected, safe to exit"* would have been **wrong**:
this system **never places NRML** (`product_map` has only `INTRADAY→MIS`, `DELIVERY→CNC`), and
`core/constants.py` deliberately treats NRML as an unrecognised anomaly the emergency sites flatten
LOUDLY — *"never silently spare the unknown."*
⇒ ⭐ **Only `CNC` is treated as broker-protected** (`_BROKER_PROTECTED_PRODUCTS`, `main.py:1158`
@ `02a2a6b`). A delivery-pipeline position on any other product keeps the service up and raises a
CRITICAL saying there is no OCO behind it.

⛔ **No universal square-off literal.** The configured `trading_hours.eod_squareoff_time` is passed in
and used ONLY to label an abnormal intraday survivor in the report — ⛔ never to decide.

---

## 2 · THE CHANGE

**Three files. Nothing else.**

| file | change |
|---|---|
| `core/state_store.py` | **+41** — new `get_active_positions_with_identity()` at `:658` @ `02a2a6b` |
| `main.py` | **+333 / −10** — resolver + one changed expression + report wiring |
| `tests/unit/test_eod_lifecycle_pipeline_aware.py` | **+313**, new |

**The one expression:**

```
195436b  main.py:1109   active = int(store.count_active_positions())
02a2a6b  main.py:1285   rows = store.get_active_positions_with_identity()
                        active, notes = _classify_active_positions(rows, strategy_intent_fn)
```

⭐ New pure helpers @ `02a2a6b`: `_resolve_position_pipeline` `:1118` ·
`_position_requires_service` `:1161` · `_classify_active_positions` `:1179`.
⭐ `main.py:1320` still holds `count_active_positions()` — as the **fallback**, unchanged.

### ⚠️ A HAZARD THE TESTS EXPOSED, AND THE HARDENING IT EARNED

💭 The prediction said a `Mock` store would raise `TypeError` and fall back. 🔬 **It does not:
`MagicMock` ITERATES AS EMPTY**, so the gate read *"flat"* and would have **exited out from under a
live position**. Six existing tests went red and caught it.
⇒ ⭐ Two hardenings, both real safety, ⛔ not test-fitting:
① the pipeline-aware path is entered **only when the PRIMARY identity source is wired** — the gate
never silently runs in a degraded product-only mode; ② the read **must return a concrete
`list`/`tuple`** — *"looks like zero" is the one answer this gate may never accept from a source it
cannot verify.* On any failure it falls back to the product-blind count (which counts MORE ⇒ biases
toward staying up) and logs at **ERROR**.

---

## 3 · TESTS — T-1…T-6, AND THE PRE-FIX PROOF

**26 tests, all passing on the unit.**

| test | asserts |
|---|---|
| **T-1** | delivery-only carry (BALUFORGE 1 @ 610.45 + KAMATHOTEL 2 @ 220.56) ⇒ **EXITS** |
| **T-1b** | *control*: the product-blind count still sees those same 2 — so T-1 cannot pass on an empty fixture |
| **T-2** | MIS survivor (circuit-lock shape) ⇒ **STAYS UP** |
| **T-3** | identity CONFLICT ⇒ **STAYS UP *and* REPORTS**, with both source values in the note |
| **T-3b** | UNRESOLVED ⇒ stays up + reports, distinct from CONFLICT |
| **T-4** | mixed book ⇒ stays up, counts **only** the stuck MIS |
| **T-5 / 5b / 5c** | empty ⇒ exits · before window_end unchanged · **flatten gate still wins** |
| **T-6 / 6b / 6c** | the three other consumers unchanged; new read has exactly ONE call site |
| + | NRML/no-product protection tests · 9-case resolver truth table · the "looks like zero" test |

### 🔬 PRE-FIX PROOF (F-1)

⛔ On `195436b` the test module **cannot even collect** (`AttributeError: module 'main' has no
attribute '_IDENTITY_CONFLICT'`) — the capability does not exist. ⭐ That is a weak per-test signal, so
a **behavioural differential** was run instead: the SAME book, the same inputs, on both trees.

| tree | API | due | active | verdict |
|---|---|---|---|---|
| `195436b` base | product-blind (no `strategy_intent_fn` parameter exists) | `False` | **2** | 🔴 **STAYS UP — the carry holds the service** |
| `02a2a6b` unit | pipeline-aware | `True` | **0** | ✅ **EXITS — the carry is released** |

---

## 4 · T-6 — THE THREE OTHER CONSUMERS, DEMONSTRABLY UNCHANGED

🔬 `count_active_positions()` body — **byte-identical**, both sides:
**len 943 · md5 `87891c9872f6f186c7e6d1a798803efd`**.
🔬 `git diff --name-only 195436b` = **`core/state_store.py`, `main.py`** — that is the complete change
set. ⛔ `capital/risk_engine.py` and `allocation/portfolio_allocator.py` are **not in it**.
🔬 The only diff lines mentioning `count_active_positions` are **comments/docstrings**.
⭐ Pinned as a **property, not a digest**: `test_t6_...` asserts its body contains no
`product`/`strategy`/`join`/`orders`; `test_t6b_...` asserts the other two still use the shared count
and do **not** consume the new read; `test_t6c_...` asserts exactly **one** call site in `main.py`.

🔬 **F-6:** the flatten gate is untouched — `flatten_in_progress_fn()` /
`_ACTIVE_FLATTEN_IN_PROGRESS` still run **before** any position query, and the only diff lines there
are a docstring rewrap and a trailing comma. EXITING-blindness **inherited, not fixed.**

---

## 5 · THE GATE — FULL DIFFERENTIAL

⚠️ 🔴 **THE FIRST GATE RUN WAS DISCARDED AS TORN.** The foreground run hit the 10-min tool ceiling;
its `pytest` child **survived the shell kill** and continued into the work side while a relaunch raced
it on the same paths. Tells: `work.failids` held **1** id while `work.out` held **8** `FAILED` lines,
and the `.out` mtime was **later** than the `.rc`/`.failids` derived from it. ⛔ Partial artefacts
deleted, ⛔ no delta computed from them.
⚠️ **CORRECTION:** I also cited NUL bytes in the `.out` as evidence of interleaving. 🔬 **That was a
misattribution** — the clean run has **439/440 NUL lines** too. pytest's Windows output contains them
normally. ⭐ The mismatch and the mtime inversion are the tells that actually hold.

🔬 **Re-run clean** with a lockfile, a refusal-if-pytest-alive guard, run-scoped paths, and a `sync`
before deriving `.rc`/`.failids`. ⭐ `PYTHON` set explicitly to `/c/python311/python.exe` (3.11.9,
pytest 9.0.3) — ⛔ not a PATH shim. Run from **Git Bash**. Artefacts: `<scratchpad>/gate_run2/`.

**RAW TAILS**

```
BASE 195436b : 7 failed, 5820 passed, 4 skipped, 281 warnings in 1121.52s (0:18:41)
WORK 02a2a6b : 7 failed, 5846 passed, 4 skipped, 281 warnings in  959.90s (0:15:59)
rc (read from FILES, never a pipe) : base 1 · work 1
```

**ID-LEVEL SET COMPARISON**

| | count |
|---|---|
| 🔴 **NEW failures on work** | **0** |
| FIXED | 0 |
| COMMON (pre-existing, identical id sets both sides) | **7** |

The 7 standing items, unchanged by this unit:
`test_closure_source_contract::test_no_module_restates_the_vocabulary_literals` ·
`test_fix181::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active` ·
`test_main::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret` ·
`test_main::TestContinueFromGate::{test_no_placer_releases_reservation_and_updates_status,
test_price_hit_calls_placer_with_correct_prices, test_stats_placed_incremented_on_success}` ·
`test_phase17_batch2::test_fix077_flask_max_content_length`

**DELTA, DECOMPOSED EXACTLY**

```
passed  5820 -> 5846   = +26  ==  the 26 tests collected in the new file  (fully accounted)
failed     7 ->    7   =   0  ==  IDENTICAL id sets
skipped    4 ->    4   =   0
rc         1 ->    1         pre-existing failures, unchanged
```

⇒ ✅ **CLEAN DIFFERENTIAL. The new-failure set is EMPTY.**

---

## 6 · FROZEN PREDICTION, SCORED

| | outcome |
|---|---|
| **F-1** T-1 fails pre-fix | ✅ **held** — proven behaviourally, base stays up / unit exits |
| **F-2** three consumers unchanged | ✅ **held** — md5-identical body, 2 files in the change set |
| **F-3** T-3 asserts stay-up AND report | ✅ **held** |
| **F-4** T-5 no regression | ✅ **held** |
| **F-5** 4 existing test files pass unchanged | ⚠️ **FALSIFIED as predicted-mechanism, then RESTORED.** The predicted `TypeError` fallback never fires — `MagicMock` iterates empty. 6 tests went red. ⭐ **Zero test files were edited**; production was hardened instead. ⛔ Recorded as falsified, not quietly re-passed. |
| **F-6** flatten gate untouched | ✅ **held** |
| **F-7** clean differential | ✅ **held** — 0 new failures |

⭐ **The prediction earned its keep at F-5**: it named in advance the exact temptation (*"if I find
myself EDITING those 4 test files, F-5 is falsified and I must say so"*), and the red tests exposed a
genuine *"looks like zero"* hazard that would otherwise have shipped.

---

## ⛔ 7 · STATE

⛔ **NOT PUSHED · NOT DEPLOYED · NO SERVICE ACTION · NO CRON · NO TUNING.**
🔬 `origin/main` = `195436bb…` unchanged (wire + VM raw ref). Deployed-tree drift **0**.
⛔ No paper drill — paper nets by SYMBOL while live Kite nets per (SYMBOL, PRODUCT), so a paper green
on a product-semantics change is **vacuous**, and this unit is entirely product semantics.
👤 **Deployment needs Rama's separate explicit word.**
