# FIX ITEM 1 — MIS/GTT CONFIG INDEPENDENCE + KILL THE SILENT FALLBACK

**Build report.** 22-Aug-2026 (Saturday), IST.
**Card:** VS CODE CLAUDE BUILD CARD, FIX ITEM 1, issued 05:00 IST.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `BUILT · GATED · ⛔ UNPUSHED · ⛔ UNDEPLOYED · ⛔ NOT VERIFIED LIVE`.**
⛔ **PUSHED: NO.** Deploy needs Rama's separate quoted word.

---

## §D — EVIDENCE LINE (opened with, as the gate requires)

| item | measured value |
|---|---|
| **Deployed SHA** | `45683859a0a05f466189ac5bc98f9a9f089f98d3` — **measured at gate time** by `git ls-remote origin refs/heads/main`, ⛔ not read from a card |
| **Branch CONTENT verification** | the unit is built on a **fresh throwaway worktree created from `4568385` itself**, so content parity with the deployed base is by construction, ⛔ not by name. ⚠️ The root worktree's branch `feat/delivery-config-split` — whose NAME matches this work — is the **WRONG** tree: it carries the deferred segment-capital design (`capital/pipeline_policy.py`, `delivery_risk_per_trade_pct: 0.02`, a trim ceiling) that Ruling 4 **defers**. It was ⛔ not used and ⛔ not touched. |
| **Build worktree** | `scratchpad/item1-work`, branch `fix/delivery-config-independence-22aug`, 1 commit ahead of `4568385`, 0 behind |
| **Gate base worktree** | `scratchpad/item1-base`, detached at `4568385` |
| **Dirty / untracked** | work tree **clean** after the commit; root worktree **untouched** (still `feat/delivery-config-split` `6d24a83`, `MASTER_PENDING_01-Aug-2026.md` still uncommitted and intact) |
| **Exact unit changed** | 5 production files + 6 test files + 1 new test file. `orders/order_reconciler.py`, `capital/fund_manager.py`, `capital/kill_switch.py`, `orders/order_placer.py`, `signals/signal_processor.py` and **all** strategy YAMLs verified **UNCHANGED** by `git diff --quiet` |

---

## §1 — RE-CONFIRM AT THE DEPLOYED SHA (measured, not recalled)

All four facts **still hold** at `4568385`. Nothing changed since the earlier passes.

| # | fact | measurement at `4568385` |
|---|---|---|
| 1 | delivery has **NO key at all** for concentration, sector_exposure, daily_loss | `grep -n` over `config/system_config.yaml`: `max_concentration_pct` `:167`, `max_sector_exposure_pct` `:225`, `daily_loss_limit_pct` `:227` — **no `delivery_` twin for any of the three**. The only `delivery_` keys present are the two sizing ones plus the two COUNT caps (`max_open_delivery_positions` `:205`, `max_daily_delivery_trades` `:206`) |
| 2 | delivery's `risk_per_trade` and `max_position_value` keys **EXIST and are NULL** | `config/system_config.yaml:190-191` → `delivery_risk_per_trade_pct: null`, `delivery_max_position_value_pct: null` |
| 3 | `position_sizer.py:300-309` — the silent fallback | verbatim at `4568385`: `eff_risk_pct = self._delivery_risk_per_trade_pct if (bucket == "positional" and self._delivery_risk_per_trade_pct is not None) else self._risk_per_trade_pct`, and the identical shape for `eff_max_position_value_pct` at `:305-309` |
| 4 | `config_loader.py:323-324` — `Optional[float] = None`, validated only when set | verbatim: `delivery_risk_per_trade_pct: Optional[float] = None` / `delivery_max_position_value_pct: Optional[float] = None`, and the validator at `:326-331` reads `if v is not None and not (0 < v <= 1)` — i.e. **`None` passes validation untouched** |

**Also re-measured, because the build depends on it:** `force_intraday_only: false`, `trade_type: BOTH`, `delivery_enabled: true`. The delivery path is fully unlocked — which is what makes the fallback live rather than theoretical.

---

## §2 — KEYS: EACH CREATED / POPULATED, WITH ITS VALUE AND TODAY'S EFFECTIVE EQUIVALENT

Read back through `load_all(Path("config"))` on the built tree — measured, not transcribed:

| key | action | value written | today's EFFECTIVE (inherited) value | source of that value |
|---|---|---|---|---|
| `position_sizing.delivery_risk_per_trade_pct` | **POPULATED** (was `null`) | `0.01` | `0.01` | `position_sizing.risk_per_trade_pct` |
| `position_sizing.delivery_max_concentration_pct` | **CREATED** | `0.10` | `0.10` | `position_sizing.max_concentration_pct` |
| `position_sizing.delivery_max_position_value_pct` | **POPULATED** (was `null`) | `0.40` | `0.40` | `position_sizing.max_position_value_pct` |
| `risk.delivery_max_sector_exposure_pct` | **CREATED** | `0.40` | `0.40` | `risk.max_sector_exposure_pct` |
| `risk.delivery_daily_loss_limit_pct` | **CREATED** | `0.03` | `0.03` | `risk.daily_loss_limit_pct` |

Every delivery value equals the number delivery was already inheriting ⇒ **B-3 behaviour-neutrality by construction**, and asserted as a property (twin == global) rather than as five magic constants, so a future config edit that breaks the equality fails the test rather than passing silently.

**Scope limit, stated rather than glossed:** `risk.delivery_daily_loss_limit_pct` scopes the **PRE-TRADE gate only** (`risk_engine` check 7). The post-close portfolio circuit breaker at `capital/fund_manager.py:1347` stays **GLOBAL** — there is one account-wide realized P&L and no per-book attribution to split it with. `CONSECUTIVE_LOSSES` likewise stays deliberately shared (it already was). Recorded in `RE18` and in the config comment so this is never over-read as "daily loss is now fully book-independent".

---

## §3 — FALLBACK: FILE:LINE OF THE CHANGE, AND THE REJECTION PATH

### The fallback, removed

⚠️ **All line numbers below are measured at `d00e574` and hold only there** (`M3`).

| file:line | what changed |
|---|---|
| `capital/position_sizer.py:356-366` | the `delivery_X if (… is not None) else global_X` conditional is **gone**. Replaced by a hard `if bucket == "positional": … else: …` split. The positional arm calls `_require_delivery()`, which has **no `else` returning a global value**. |
| `capital/position_sizer.py:198-225` | new `_require_delivery(value, key)` — logs CRITICAL `position_sizer.delivery_limit_missing` with `key=position_sizing.<key>` and raises `ValueError` naming the key. |
| `capital/position_sizer.py:481` | `qty_by_concentration` now uses `eff_conc_pct` (the delivery key on a delivery entry), not the global. |
| `capital/position_sizer.py:660, 674` | the CRITICAL log field and the rejection reason now report the **enforced** `eff_max_position_value_pct` — see the trap note below. |
| `capital/risk_engine.py:321-328` | per-book limits resolved **once** in `_approve` (RE11/RE16 discipline), raising rather than inheriting. |
| `capital/risk_engine.py:216-236` | new `_require_delivery()` — CRITICAL `risk_engine.delivery_limit_missing key=risk.<key>` + `ValueError`. |
| `capital/risk_engine.py:662` (DAILY_LOSS), `:707, 721, 730` (SECTOR_EXPOSURE) | both gates read `eff_*`, not `self._*`. |
| `capital/risk_engine.py:474-481` | `_run_checks` takes the two effective limits as **keyword-only REQUIRED** params — deliberately not defaulted to the globals, because a default there would quietly reinstate the inheritance. |
| `capital/risk_engine.py:41-50` | new locked decision **RE18**, recording the per-book rule and its scope limit. |
| `core/config_loader.py:318-350` | the three sizing keys become `Optional[float]` with **no default** (⇒ required) and the validator **rejects `None`**. |
| `core/config_loader.py:567-579` + `:618-630` | same for the two `risk` keys. |
| `main.py:2518-2523` and `:2579-2583` | wires all five from config. |

⭐ **The new raises honour the frozen effect-telemetry contract rather than breaking it.** A2.1 states *"a raise is not a verdict and is deliberately not counted"*: `_require_delivery` raises from inside `_calculate` / `_approve`, so `calculate()` / `approve()` never reach `self._fx_verdict.inc()`. No counter is corrupted by the new rejection path.

### The rejection path, MEASURED end-to-end (not asserted)

`load_all` → `ConfigSchemaError` → `main._config_error_detail` → `_log.critical("Config load failed: …")` → **`return 5`**. The actual rendered boot lines:

```
[missing key]
Config load failed: Schema validation failed for system_config.yaml
  | position_sizing.delivery_risk_per_trade_pct: Field required

[null key]
Config load failed: Schema validation failed for system_config.yaml
  | position_sizing.delivery_max_concentration_pct: Value error, delivery sizing pct
    must be set explicitly to a number in (0, 1]; it does NOT fall back to the global
    (intraday) value

[null key, risk section]
Config load failed: Schema validation failed for system_config.yaml
  | risk.delivery_daily_loss_limit_pct: Value error, delivery gate pct must be set
    explicitly to a number in (0, 1]; it does NOT fall back to the global (intraday) value
```

File named, key named, reason named, non-zero exit. ⛔ Not a warning.
⭐ **No new logging code was added for this** — the boot path already had `_config_error_detail` (built 25-Jul for exactly this problem). The build reuses it rather than adding a second mechanism.

---

## §4 — THE ONE TENSION: `delivery_max_position_value_pct` · ⛔ REPORTED, NOT CHOSEN

**⛔ I have not chosen. This is Rama's call.** What follows is the measurement and the blast radius of each option.

### First, a correction to the premise, because it changes the margin (not the conclusion)

The card states the cap is unreachable because *"concentration caps notional at 10%, tier multipliers top out at 1.0"*. The **conclusion is right**; the **reason is incomplete**:

- `position_sizing.max_multiplier` is **2.0**, not 1.0 — `effective_mult = tier_mult × perf_weight` (`position_sizer.py:527`), so the multiplier is only capped at 1.0 because **`perf_weights` is never wired into `SignalProcessor`**: `main.py`'s single `SignalProcessor(` call at `:3141` passes none, so `self._perf_weights` is empty and `.get(name, 1.0)` always returns **1.0**. `dynamic_by_winrate: true` is read only for a log line (`main.py:2532`) and the dashboard — it gates nothing. (Already on the record at `tests/integration/test_q9_sizing_floors_caps_wired.py:66`.)
- ⇒ **today** max delivery notional = `0.10 × TOTAL` (concentration) vs a cap of `0.40 × TOTAL` — a **4× margin**.
- ⇒ **if the PerformanceAllocator is ever wired**, it becomes `0.10 × 2.0 = 0.20 × TOTAL` — still below 0.40, so the conclusion survives, with a **2× margin**.
- ⇒ it would bind only if `delivery_max_concentration_pct × max_effective_multiplier > delivery_max_position_value_pct`.

**So the honest statement is not "unreachable" but "unreachable while concentration × the effective multiplier stays below it" — a condition, not a property.** That matters for option (c).

### The three ways out

| | option | blast radius |
|---|---|---|
| **(a)** | **populate it anyway** — inert, recorded as such | ⭐ **Zero behavioural blast radius**: measured unreachable today (4× margin) and after an allocator wiring (2× margin). Costs one config line. Keeps the no-fallback rule with **no exception clause**. Keeps the backstop that exists to catch a bug in the constraints that make it unreachable. ⚠️ Cost: one more key an operator must maintain, and a value that has never fired and may never fire — an inert control can rot unnoticed. **This is what the build currently ships**, because B-4 admits no absent key and shipping something was required to gate the unit; ⛔ it is trivially reversible on Rama's word. |
| **(b)** | **scope the no-fallback rule to keys that actually govern behaviour** | 🔴 **Largest blast radius, and it is conceptual, not mechanical.** It re-introduces a *category* of key that may be absent — and "governs behaviour" is a judgement that must be re-made every time a key is added, by whoever adds it. Today's defect is exactly a key that was believed not to govern behaviour and did. ⚠️ It also needs a written, enforced definition of the exempt class, or it degrades into "whatever the last author thought". |
| **(c)** | **remove the unreachable control entirely** — ⛔ separate work, ⛔ not this build | 🔴 **Removes the only check that would catch a bug in concentration/risk/tier sizing.** `position_sizer.py:619-624`'s own stated purpose is *"Catches: Bugs in earlier constraints"* — it is unreachable **by design**, and the config auditor's C2 actively enforces that it stay looser than concentration. Removing it converts a silent-but-armed backstop into no backstop. It would also have to be removed for **both** books (the global cap is unreachable for the same reason), which is a much wider change than item 1. |

⭐ **The card's reading is (a).** I did not test the two premises of that reading blindly: (a)'s "harmless" is confirmed by measurement above, with the margin restated correctly. ⛔ **No option is chosen here.**

---

## §5 — THE OPERATIONAL RISK RAMA MUST BE TOLD ABOUT

🔴 **B-4 CHANGES THE BOOT PATH. After this ships, a config mistake STOPS THE SYSTEM instead of silently degrading it.**

- **Monday's 08:15 boot is UNATTENDED.** A rejected config = no boot, no entries, **a lost trading day** — the same cost as the 10-Aug HARD_KILL day.
- Worse, the failure is quiet in the way that matters: `token_watcher.sh` sees the unit as not-running and *would* start it, but `_main_locked` returns 5 before anything trades; the only artifact is one CRITICAL line in the boot log.
- ⭐ **That is the intended behaviour and it is safer than the alternative** — the alternative is what we have today, where a missing delivery limit silently sizes the delivery book on the intraday risk budget with real money.
- 🔴 **The rejection path is therefore tested hard enough that a VALID config cannot trip it** — see T-5 below: the shipped config, key-reordered, exponent-form, integer-valued, and yaml-round-tripped-and-sorted variants **all load**, and the control proves that check could have gone red.
- 🔮 **Named as a falsifier in the frozen prediction (P-7), with a REVERT TRIGGER stated in advance: if a VALID config is ever rejected, the unit is REVERTED — ⛔ not tuned, ⛔ not loosened, ⛔ not exception-scoped.**

---

## §6 — TESTS

New file: `tests/unit/test_delivery_config_independence.py` (49 tests). Modified: 6 existing test files.

| id | what it asserts | result |
|---|---|---|
| **T-1** | **BEHAVIOUR-NEUTRAL.** Anchors: the three recorded CNC risk legs. Property: **every** leg of a positional entry equals a closed-form recomputation using the GLOBAL percentages — literally what the pre-change code did. Plus config-level: every shipped delivery value == its global twin. | **PASS** |
| **T-2** | **INDEPENDENCE, both directions**, on the sizer AND on the gate. Includes a non-vacuity check that the delivery keys actually bind, so the independence assertions cannot pass by the keys being ignored. | **PASS** |
| **T-3** | **Missing delivery key → startup REJECTS**, key named in the line the boot actually logs (asserted through `main._config_error_detail`, ⛔ not through the exception repr). Plus: it does **not** fall back — a load that returns an `AppConfig` is an explicit failure. | **PASS** (5 keys) |
| **T-4** | **NULL delivery key → same.** | **PASS** (5 keys) |
| **T-5** | **A VALID config boots cleanly** — the §5 falsifier, made thorough: shipped config + 4 valid variants, **plus a control** proving the check can go red. | **PASS** |
| **T-6** | **Intraday sizing unchanged** — 9 (tier × price) combinations, identical whether delivery keys are absent, equal, or wildly different; and the intraday legs still equal the closed-form global computation. | **PASS** |
| **T-7** | **Drift comparator unaffected** — containment check that CHECK 1/CHECK 2 read no sizing/risk percentage (10 forbidden names), and the two comparands are still the recorded algebra. | **PASS** |

### T-1's before/after quantities

| trade | risk_rs / sl_distance | qty_by_risk BEFORE | qty_by_risk AFTER |
|---|---|---|---|
| CLSEL | 105.87 / 5.78 | **18** | **18** |
| MANINDS | 105.87 / 14.46 | **7** | **7** |
| KRONOX | 105.87 / 4.11 | **25** | **25** |

⚠️ **Stated rather than papered over:** the entry/SL prices of those three trades are **not on this PC** — the local `data_store/trading_system.db` holds **0 trades** and the VM was not touched (Saturday, service down, no owed VM op). So the anchors pin the **risk leg**, which is the leg the card's arithmetic names; every **other** leg is pinned by the closed-form property assertion instead. That is a narrower anchor than "the whole trade reproduces", and it is labelled as such.

---

## §7 — THE FALSE COMMENT

**B-5 asked for `config_loader.py:323-324`. There were THREE copies of the same false claim, and all three are gone.**

| file (at `4568385`) | the false text |
|---|---|
| `core/config_loader.py:318-322` | *"INERT: delivery is double-locked OFF + force_intraday_only coerces every strategy to INTRADAY → the positional bucket **is never taken live** → **these are never read**"* |
| `capital/position_sizer.py:143-146` and `:296-299` | *"a positional (delivery) bucket, **which never occurs live** while force_intraday_only coerces every entry to INTRADAY"* |
| `config/system_config.yaml:185-189` | *"the positional (delivery) bucket **is never sized live**"* |

**Every clause was false**: `force_intraday_only: false`, `delivery_enabled: true`, `trade_type: BOTH`, and delivery has traded.

Replaced with text that states the contract and records what was wrong. **Pinned by test** (`test_b5_no_surviving_claim_that_delivery_is_never_live`) across 4 files — and the check is **non-vacuous**: run against the base tree it produces **7 hits**; against the unit, **0**.

---

## §8 — NEW ISSUES FOUND EN ROUTE

⛔ None of these is fixed in this commit — one fix per commit, and §9 forbids bundling. Each is reported with its evidence so it can be scheduled as its own unit.

### 🔴 NI-1 — `PositionSizer`'s SL-direction WARNING **raises `KeyError` instead of warning**. PRE-EXISTING at `4568385`.

`capital/position_sizer.py:278` and `:284` (base line numbers) call `self._warn(msg, {... "msg": ...})`, and `_warn` does `self._log.warning(msg, extra=extra)`. `"msg"` is a **reserved `LogRecord` attribute**, so `logging.Logger.makeRecord` raises `KeyError: "Attempt to overwrite 'msg' in LogRecord"`.

**Proven by experiment at the base SHA, ⛔ not by reading:** a `BUY` with `sl_price > entry_price` on the `4568385` tree raises `KeyError` out of `calculate()`.

🏷️ **LATENT, ⛔ not LIVE** — it needs an inverted SL, which no recorded trade has. ⇒ documented and continued, per the LIVE-vs-LATENT rule. **Consequence if reached:** the sizing call raises instead of returning a `SizingResult`, so the signal is lost **and the warning that would have explained why is never written** — a guard that destroys its own diagnostic.

⭐ **Swept as a CLASS, not as an instance:** an AST sweep of every `.py` in the tree for any dict literal carrying one of the **23** reserved `LogRecord` attribute names into a logging-ish call returns **exactly these 2 sites** and nothing else. (A first, narrower sweep — `extra=` keyword only — returned **0**, and would have been a false all-clear: these two pass the dict **positionally** to `_warn`.)

**Fix is one word** at each site (`"msg"` → e.g. `"detail"`). My own new CRITICAL in `_require_delivery` was written with `"msg"` first, hit exactly this `KeyError` in test, and now carries an inline `⛔` note so it cannot come back.

### 🟠 NI-2 — the config auditor's **C2 ladder check omits the multiplier**, so it can pass a config where the "backstop" binds routinely.

`core/config_auditor.py:414` warns only when `max_position_value_pct <= max_concentration_pct`. The real ceiling on notional is `max_concentration_pct × max_effective_multiplier`. With the PerformanceAllocator wired (`max_multiplier: 2.0`), `conc = 0.25 / posv = 0.40` passes C2 while `0.25 × 2.0 = 0.50 > 0.40` ⇒ the catastrophic-loss backstop would fire on **routine** sizing — the exact thing C2 exists to prevent. Harmless today only because the allocator is unwired. **And there is now a delivery pair too, which C2 does not check at all.**

### 🟡 NI-3 — the delivery COUNT caps still carry a misleading "inert" conditional.

`config/system_config.yaml:214-215` and `capital/risk_engine.py:534, 620` say *"inert while force_intraday_only=true"*. `force_intraday_only` is **false**. The sentence is a true conditional with a false antecedent, so it is misleading rather than false — but it is the same reading hazard B-5 exists to remove, on the two delivery keys this build did **not** touch.

### 🟡 NI-4 — `max_open_delivery_positions: int = 3` / `max_daily_delivery_trades: int = 5` carry **silent schema defaults**.

`core/config_loader.py:536-537`. These are delivery-scoped risk limits with a default, i.e. the same class B-4 removes for the other five: delete the keys from the YAML and the system boots on a hardcoded 3/5 rather than refusing. Out of this card's key list, so ⛔ untouched — but they are the remaining members of the class.

### 🟡 NI-5 — `PositionSizer.__init__` defaults every GLOBAL limit too.

`capital/position_sizer.py:128-139` — `risk_per_trade_pct: float = 0.01`, `max_concentration_pct: float = 0.10`, `max_position_value_pct: float = 0.40`. Unreachable in production (one construction site, from validated config) but it is a silent default on the money path. ⚠️ `RiskEngine`'s docstring already forbids exactly this for itself: *"RiskEngine takes NO defaults — all caps are required, so a component built without config fails fast rather than running loose."* The two classes disagree.

### ⚪ NI-6 — the daily config snapshot hash will change on the first post-deploy day.

`core/config_snapshotter.py` hashes the config JSON. Five new keys ⇒ a new `config_hash`. **That is the correct record of a real config change, ⛔ not drift** — flagged so nobody reads it as an anomaly.

### ⚪ NI-7 — a stale filename, recorded rather than silently renamed.

`tests/unit/test_position_sizer_delivery_scaffold.py` no longer tests a scaffold — its assertions are inverted to the new contract. Kept under the original name so the history of a reversed contract stays traceable; renaming mid-gate would have added a delete+add to the diff.

---

## §8b — GATE

### Environment (the launcher is part of the gate)

| | |
|---|---|
| launcher | **Git Bash** `/usr/bin/bash` — ⛔ never PowerShell (that manufactures 20 phantom failures) |
| `python` | `C:\python311\python.exe` — **Python 3.11.9** |
| `python3` | the session **shim** (a copy of `python.exe` named `python3.exe`, first on `PATH`) — ⛔ NOT the WindowsApps stub |
| pytest | **9.0.3** |
| `config/instruments.csv` | planted into BOTH trees with `cp -p`, md5 `a7b07623909e051cb624ad157cee1671` identical on root + base + unit — ⛔ never `write_text` |
| `venv/` | ⚠️ **the repo's `venv/` on this PC is an EMPTY directory.** Junctions were created and then removed as useless. `pick_python()` therefore falls through to bare `python`, which **here resolves to the real `C:\python311\python.exe`, not the Store stub** — so the 3 `t4_deploy_preflight` phantoms that the venv-hazard note describes do not arise. **Identical on both sides**, and recorded because it is a deviation from the written recipe. |
| ordering | **strictly sequential, never concurrent** — `test_instance_lock` holds a machine-global lock, so two overlapping suites would manufacture failures |
| clock/calendar | both runs on the **same Saturday**, 33 minutes apart, both inside 08:00–16:00 IST ⇒ the time-gated and calendar-gated tests behave identically on both sides |

⚠️ **DISCLOSED, ⛔ not hidden: the FIRST base run was ABORTED at ~31% and re-run from scratch.** Its `PATH` export used a `C:/...` form, and a drive-letter colon splits a colon-separated `PATH` — so `python3` still resolved to the WindowsApps stub. The run was killed, its two orphaned processes reaped (`pytest` PID 32348, a `recover.py` child PID 8640), its artefacts deleted, the launcher fixed to the POSIX `/c/...` form, and **the whole gate restarted**. Same discipline as the 17-Aug 37→7 re-run. ⛔ No partial result from that run is used anywhere.

### Raw pytest tails, BOTH sides

**BASE — `item1-base`, HEAD `45683859a0a05f466189ac5bc98f9a9f089f98d3`, `DIRTY=0`, 10:43:43 → 10:58:44:**

```
FAILED tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
FAILED tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
FAILED tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
FAILED tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
FAILED tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
FAILED tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
FAILED tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
7 failed, 5665 passed, 4 skipped, 281 warnings in 896.31s (0:14:56)
```

`RAW_PYTEST_RC=1` — read from pytest itself via **file redirection**, ⛔ never `| tail; echo $?` (which captures `tail`'s code and has produced a false `RC=0` once already).

**UNIT — `item1-work`, HEAD `d00e574323a0b19cf0f98c3fca65031925d027cc`, `DIRTY=0`, 10:59:48 → 11:16:00:**

```
FAILED tests/unit/test_closure_source_contract.py::test_no_module_restates_the_vocabulary_literals
FAILED tests/unit/test_fix181.py::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active
FAILED tests/unit/test_main.py::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret
FAILED tests/unit/test_main.py::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices
FAILED tests/unit/test_main.py::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status
FAILED tests/unit/test_main.py::TestContinueFromGate::test_stats_placed_incremented_on_success
FAILED tests/unit/test_phase17_batch2.py::test_fix077_flask_max_content_length
7 failed, 5715 passed, 4 skipped, 281 warnings in 966.96s (0:16:06)
```

`RAW_PYTEST_RC=1`. 🏷️ Per `N12-16` `<RULE · BINDING>`: **a non-zero rc alone does NOT fail the gate; an UNATTRIBUTED failure does.** Every failure here is attributed below.

### ID-level two-way differential — ⛔ ID-LEVEL ONLY, per `N20-19`

```
comm -13  (NEW on UNIT)          -> EMPTY   (0)
comm -23  (DISAPPEARED from BASE)-> EMPTY   (0)
comm -12  (COMMON)               -> 7
```

⛔ **No `failmsgs` artefact was produced at all.** `N20-19` records that a "messages identical" claim on `pytest -q` output is **vacuous** — the short-summary lines carry no ` - <reason>` suffix, so a message file is byte-for-byte the id file plus the `FAILED ` prefix. Nothing here can later be mistaken for message-level evidence.

### The 7 are attributed, ⛔ not labelled

They are the campaign's enumerated standing set — `test_closure_source_contract` ×1, `test_fix181` ×1, `test_main` ×4, `test_phase17_batch2` ×1 — identical on both sides. ⭐ **And the harness is proven sound before the comparison is trusted:** this base run reproduces the ledger's own 20-Aug gate of **`4568385`** to the number — recorded there as `rc 1 · 7F / 5,665P / 4S`, measured here as `rc 1 · 7F / 5,665P / 4S`. A base that did not reproduce the recorded baseline would be a broken harness, not a finding.

### The passed-count delta is accounted for by arithmetic, ⛔ not waved through

`5,715 − 5,665 = +50`, and:

| source | collected |
|---|---|
| new `tests/unit/test_delivery_config_independence.py` | **+49** |
| `test_position_sizer_delivery_scaffold.py` 4 → 5 | **+1** |
| | **= +50** ✓ |

⇒ **no test silently disappeared** and none was silently added.

---

## §8c — FROZEN PREDICTION, SCORED

`docs/audit/PREDICTION_item1_22-Aug-2026.md` · **7,775 B** · md5 **`c5a6005bc9194411835795163ec82284`** — re-hashed after the build and **byte-identical to the pre-build hash**, so it is a prediction and not a retrofit.

| | | |
|---|---|---|
| **P-1** | behaviour neutrality | ✅ **CONFIRMED** — anchors 18 / 7 / 25 reproduce; every leg equals the closed-form pre-change arithmetic |
| **P-2** | intraday untouched | ✅ **CONFIRMED** — 9 tier×price combinations identical; no `delivery_*` symbol on an intraday-reachable path |
| **P-3** | the fallback is gone | ✅ **CONFIRMED** — grep finds no surviving `… is not None else global` shape; missing and null both reject, naming the key, at exit 5 |
| **P-4** | independence both ways | ✅ **CONFIRMED**, with its named exclusion (fund_manager's post-close circuit breaker stays global) stated in advance and still true |
| **P-5** | stale comment gone | ✅ **CONFIRMED** — 7 hits at base, 0 at unit |
| **P-6** | the `:596/:609` trap fires on this build | ✅ **CONFIRMED and CLOSED** — it did separate the moment the delivery key was populated, and both sites now report the enforced value |
| **P-7** | a valid config never trips the rejection | ✅ **CONFIRMED for every variant tested** (shipped + 4 valid variants + control). ⚠️ **Its real window is a future 08:15 boot, which has not arrived** — so the LIVE half is `NOT TESTED`, ⛔ never a pass. The REVERT TRIGGER stands. |
| **P-8** | gate set-equality | ✅ **CONFIRMED** on the ID-level halves (0 NEW / 0 disappeared). ⛔ **The clause "and identical failure MESSAGES" is WITHDRAWN AS VACUOUS per `N20-19`** — it was in the frozen text and is scored honestly rather than quietly dropped. |

---

## §9 — LIMITS OBSERVED

⛔ No deploy · ⛔ no push · ⛔ no basis change (`total_capital = snap.total` untouched; Ruling 4's Basis A stands) · ⛔ no value change (behaviour-neutral only) · ⛔ no guard touched · ⛔ no strategy YAML touched (0 files) · ⛔ no funnel work · ⛔ no GUI · ⛔ no bundling with fix-list items 2–7 · ⛔ `DUPLICATE_SYMBOL` / `CONTRARY_POSITION` / `PENDING_FILL` / `portfolio_lock` / `RESERVE·COMMIT·RELEASE` / `margin_per_share` / `qty_by_capital` / the 70/30 split / `qty_by_risk`'s structure — all untouched, verified by diff.

⚠️ **The paper hazard, said in advance as the card requires:** paper nets by **SYMBOL**; live Kite nets per **(SYMBOL, PRODUCT)**. A paper drill of a delivery product-semantics change is vacuously green. ⛔ **No paper result is offered as evidence here, and none was run.**
