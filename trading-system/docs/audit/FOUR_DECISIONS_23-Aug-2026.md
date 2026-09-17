# THE FOUR DECISIONS — 23-Aug-2026 (Sunday), IST

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
**Authorising quote — Rama, 23-Aug:** *"act on these 2 files simultaneously, dont skip
anything"*, forwarding ChatGPT's four recommendations.

🏷️ **⛔ NOT PUSHED · ⛔ NOT DEPLOYED · `origin/main` = `45683859a0a05f466189ac5bc98f9a9f089f98d3`**
(measured at 23-Aug by `git ls-remote origin refs/heads/main`, ⛔ not read from a card.)

---

# §1 — THE `65b7196` READ · STAGED · **ANSWERED AT R-1**

> 🔴 **SHARPENED 23-Aug afternoon — THIS IS THE WORDING THAT SURVIVES.**
> ⛔ NOT *"the clamp is missing"* / *"never ported"*, which invites someone to port it.
> ⭐ **The deployed sizer CARRIES THE EXACT FIX-133 EXPRESSION THAT `65b7196` DELETED AS
> FORBIDDEN** — the *presence* of a thing a later LOCKED decision removed, ⛔ not an absent
> protection. 🔴 **AND NI-16 CANNOT BE FIXED BY COPYING `min(1.0, …)` ACROSS:** deployed
> computes **no allocation** — `pipeline_policy.py`, `allocation_divisor` and
> `base_allocation` are **`65b7196`-only** (re-measured; zero hits on `4568385`). ⛔ You
> cannot clamp to a single allocation in a system that does not compute one.
> → full record: `docs/audit/F12_INSTANCE3_AND_GATE_GUARD_23-Aug-2026.md` §1

⭐ **The read stopped at R-1.** `docs/audit/order_sizing_allocation_build_08aug2026.md`
§4.1 answered the question outright, so **R-2 and R-3 were never opened** — the named test
and the allocator implementation were not read. The only further act was a **path
locate** (`git grep -l`, no file bodies) to satisfy the report's *"exact file/function/
test"* requirement, plus R-4's mandatory comparison against deployed.

⛔ No merge, no cherry-pick, no revive, no modify, no delete, no deploy, no checkout of
that branch. The blob was read with `git show 65b7196:<path>`, which is not a checkout.

## ⭐ IT IS NOT EMPTY — THE CLAMP EXISTS

| | |
|---|---|
| **file (implementation)** | `65b7196:capital/position_sizer.py` — carries the clamp expression and the `effective_mult_unclamped` audit field |
| **file (multiplier source)** | `65b7196:capital/performance_allocator.py:36` — `class PerformanceAllocator` |
| **test** | `test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic`, in `65b7196:tests/unit/test_mc6_zero_multiplier_skip.py` |

**Exact behaviour:** `effective_mult = min(1.0, tier × perf_weight)`.

- The clamp is on the **COMBINED** multiplier, ⛔ not on `perf_weight` alone.
- **HIGH tier (1.0)** — no headroom, so `max_multiplier: 2.0` is fully clipped.
  **MEDIUM (0.7)** — a perf weight up to ~1.43 still raises size; beyond that, clipped.
  **LOW (0.5)** — the full `max_multiplier: 2.0` remains usable.
- ⇒ a winning strategy **can** be lifted back up to a full allocation; what it can never
  do is spend **past** one. `min_multiplier: 0.5` applies in full — the **downside is
  not clamped**.
- `effective_mult_unclamped` keeps the raw value auditable.
- FIX-133's `max(1, min(tiered, raw*2))` is **DELETED** in that build.

## Does it enforce the single-allocation ceiling? **YES — and the policy is LOCKED**

> 🟢 **LOCKED 08-Aug-2026, verbatim:** *"Performance and tier may move a trade's
> allocation up or down WITHIN the single-allocation ceiling — ⛔ they may never spend a
> second trade's allocation."*

The record states the reason is structural, not discretionary: `6 × allocation = the
basis, exactly`, so letting one trade exceed one allocation **silently spends a LATER
trade's slot**. It marks the earlier OWED entry **CLOSED**.

## R-4 — is it absent from deployed? **YES, and deployed enforces the OPPOSITE**

Measured at `4568385` (= `origin/main`) and at `742d9da`. `git grep` for
`effective_mult_unclamped`, `clamped_to_one`, `single-allocation`, `single_allocation`
returns **zero hits on both**.

Deployed arithmetic, `capital/position_sizer.py` **@ `4568385`** (M3 — line numbers hold
only at their measured SHA):

| line | expression |
|---|---|
| `:428` | `raw_qty = min(qty_by_risk, qty_by_capital, qty_by_concentration)` |
| `:470` | `effective_mult = tier_mult * max(0.0, perf_weight)` — 🔴 **no upper clamp** |
| `:527` | `tiered_qty = int(math.floor(raw_qty * effective_mult))` |
| `:530` | `tiered_qty = max(1, min(tiered_qty, raw_qty * 2))` — 🔴 an explicit **2×** ceiling |

At **`742d9da`** the same three survive at `:527` / `:584` / `:587`, arithmetic unchanged.

⇒ deployed does not merely *lack* the clamp; the ceiling it does enforce is **twice** the
one the locked policy permits. `:530` **is** FIX-133's expression — the one `65b7196`
deleted as forbidden.

## The `N9-07` lesson applied — does another deployed mechanism enforce it? **NO**

Every candidate swept, each negative for a stated reason:

| candidate | @ `4568385` | why it does not enforce the ceiling |
|---|---|---|
| `POSITION_VALUE_CAP` | `:589`, `max_position_value_pct = 0.40` | **REJECTS** above 40% of *total capital*. 2× the 10% concentration rung = **20% < 40%** ⇒ ⛔ **arithmetically cannot bind.** It is also capital-relative, not allocation-relative |
| `QTY_EXPLOSION_GUARD` | `:389`, `max_single_order_qty = 10000` | an anomaly guard on `qty_by_risk`, evaluated **before** the multiplier |
| RiskEngine count caps | `max_open_positions`, `max_daily_trades`, delivery caps | cap the **NUMBER** of positions, ⛔ never per-trade size |
| FundManager reservation | `:2355` | an **availability** constraint, not a ceiling — and it bites only *after* earlier trades have already overspent |

## 🔴 AND THE DEEPER ANSWER: THERE IS NO ALLOCATION FOR A CEILING TO BE *OF*

| measured @ `4568385` | |
|---|---|
| `capital/position_sizer.py:294` | `avail = snap.intraday_avail if bucket == "intraday" else snap.positional_avail` |
| `capital/position_sizer.py:419` | `qty_by_capital = int(math.floor(avail / margin_per_share))` |
| `capital/fund_manager.py:478` | `self._intraday_avail = broker_balance * self._intraday_pct` |

`avail` is the **whole remaining bucket**, decremented on reserve (`:2355`) — ⛔ not a
per-trade allocation. `max_daily_trades` divides **nothing** on deployed: it appears only
in `risk_engine.py` as a count cap and in `config_loader.py` as schema.

⇒ ⭐ **The correct statement is not "the clamp is missing from a system that otherwise has
allocations."** It is: **the allocation MODEL is not deployed at all**, so the concept the
locked policy governs has no deployed analogue. On deployed the binding per-trade rung is
the **concentration** arm (10% of total capital), and `:530` lets one order spend **twice**
it.

## What is GENUINELY missing

1. **A CLOSED, locked, dated policy (08-Aug-2026) is enforced nowhere on the deployed
   path** — and is not restored by F1 either: `742d9da` (which contains `d00e574`) has
   **zero** hits for the clamp. ⇒ ⛔ **pushing F1 does not bring the locked ceiling with
   it.** ⚠️ This bears directly on §4 and is easy to assume otherwise.
2. **The deployed 2× ceiling contradicts the locked policy in direction, not just
   degree.**

## ⚠️ LATENT, ⛔ NOT LIVE — stated so the finding is not over-read

`PerformanceAllocator` is **never instantiated** on deployed (`docs/SYSTEM_MAP.md:149`
finding (a) @ `4568385`) ⇒ `perf_weight ≡ 1.0`. With `tier_mult ≤ 1.0`, `raw_qty * 2` is
**unreachable today**. This is **NI-16**. ⛔ Nothing here was designed or fixed;
`max_multiplier` stays **2.0** as instructed.

## ⚠️ ONE EN-ROUTE CORRECTION — a memory index line is imprecise

The HOT index line reads *"⛔ THE SIZING DIVISOR IS `max_daily_trades`, ⛔ NEVER
`max_open_positions`"*. Its topic file
(`stated_vs_configured_limits_09aug.md`) is **correct** — it says this of the **frozen
`65b7196` build** (*"intraday trades/day 6 … and it is ALSO the sizing divisor"*). The
index line dropped that qualifier, so as written it reads as a claim about deployed,
where **no sizing divisor exists**. ⭐ The measurement was right; the compression lost
the scope.

---

# §4 — DEPLOY SHAPE · TWO PUSHES · ⛔ **NEITHER AUTHORISED**

## The ruling and its **correct** justification

**Two pushes.** ⭐ Justified by **CONTROLLED LIVE ATTRIBUTION**: if F1 and the seven-commit
NI stack land in the same 08:15 boot, any Monday anomaly has two candidate causes and no
way to separate them. One unit per live session makes the next morning's behaviour
attributable to exactly one change.

⛔ **NOT justified by policy.** *"One unit per evening"* is **not a written rule** —
verified today by `grep -rin` over `docs/` and the root `*.md`: the only hits are
`docs/audit/OPS_FINDINGS_22-Aug-2026_evening.md:528` and **§F.5**, which exist precisely to
record that it is **not** a written rule. It is Rama's operating preference, and it should
be named as his preference, not dressed up as documentation.

## The two units — ancestry MEASURED, not assumed

| | push | SHA | contents | fast-forward? |
|---|---|---|---|---|
| **PUSH 1** | F1 alone | `d00e574` | **1 commit** — *fix(sizing): item 1 — delivery risk config is explicit; the silent fallback is gone* | ✅ `4568385` **is** an ancestor of `d00e574` |
| **PUSH 2** | the NI stack | `742d9da` | **7 commits** — `940a572` job 1 · `4928941` NI-1 · `c146eb7` NI-2 · `5a7dbf6` NI-3 · `6ad328e` NI-4 · `4c495d0` NI-6 · `742d9da` NI-7 | ✅ `d00e574` **is** an ancestor of `742d9da` |

## Gate coverage — ⭐ no extra gate run is needed

Each push is covered by a differential gate whose **base is the then-deployed state**:

| gate | base | head |
|---|---|---|
| `4568385` → `d00e574` | `rc 1 · 7F / 5,665P / 4S` | `rc 1 · 7F / 5,715P / 4S` |
| `d00e574` → `742d9da` | `rc 1 · 7F / 5,715P / 4S` | `rc 1 · 7F / 5,751P / 4S` |

The **7 failures are a pre-existing standing set**, identical on every side —
`test_closure_source_contract` ×1, `test_fix181` ×1, `test_main` ×4,
`test_phase17_batch2` ×1. ⛔ A green gate is **never** deploy authorisation.

## 🔴 THE REAL TIMELINE — ⛔ NOT TWO CONSECUTIVE EVENINGS

*"Observe F1 before push 2"* requires a **TRADING DAY**, not a night.

| step | earliest | note |
|---|---|---|
| OPS ② (§3) | **before** push 1 | the protection must exist when the seven fail-closed keys first become reachable |
| **PUSH 1** — `d00e574` | Sun **23-Aug** evening | the push floor is ~19:00, ⛔ and the clock is not the test |
| F1's first live exposure | Mon **24-Aug** 08:15 boot | ⚠️ an **UNATTENDED** boot |
| F1 observed | Mon **24-Aug**, through ~17:35 | a full session |
| **PUSH 2** — `742d9da` | Mon **24-Aug** evening **at the earliest** | |
| NI stack's first live exposure | Tue **25-Aug** 08:15 boot | |

⇒ ⭐ **minimum span Sunday evening → Tuesday morning: three calendar days, with ONE
intervening trading session.**

**Calendar, measured ⛔ not recalled:** `config/nse_holidays_2026.yaml` lists **15**
holidays and **none in August** — `grep 'date:' … | grep '2026-08'` returns empty. ⚠️ The
file's only August mention (`15-Aug-2026 (Sat) Independence Day`) is a **COMMENT**, not
data, and Saturday anyway. ⇒ Mon 24-Aug and Tue 25-Aug are trading days.

## ⛔ THE CONSTRAINTS THAT STAND

- ⛔ **Neither push happens without Rama's explicit words naming that push.** A forwarded
  recommendation is ⛔ not a GO on a refspec.
- ⛔ **Neither goes into an unattended 08:15 boot on a green gate alone.**
- ⚠️ **Resolve `origin/main` by MEASUREMENT at gate time.** The FF check **is**
  `git push --dry-run origin <sha>:refs/heads/main`. A comparand written hours earlier
  passes and tells you nothing.
- 🔴 **This changes the boot path.** A bad config now STOPS the unattended 08:15 boot.
  ⛔ REVERT if a VALID config is rejected.
- ⚠️ **NI-5 (§2) is in NEITHER push.** It is a **third unit**, on its own branch.
- ⚠️ **F1 does not carry the §1 single-allocation clamp** — see §1's "genuinely missing".

---

# §2 — NI-5 · OPTION (a) · **BUILT AND GATED** · ⛔ NOT PUSHED

🏷️ **`BUILT · GATED · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED`**
**Commit `a4a5cef`** on **`fix/ni5-policy-defaults-23aug`**, base `742d9da`.
12 files, **+328 / −20**. Worktree clean at commit time = exactly what was gated.

**Frozen prediction, written BEFORE the build:**
`docs/audit/PREDICTION_ni5_23-Aug-2026.md` (scored in the same file).

## The preserved patch was RE-VERIFIED, not trusted

`docs/audit/NI5_STOPPED_22-Aug-2026.patch` — **19,032 B**, md5
**`e1bce4ac3583e2ff0f1f8c37c794fc7f`** ✅ matches the card. Against the current tree its
recorded blob index for `position_sizer.py` (`321e1fd`) **equals** `742d9da`'s, and
`git apply --check` passed on all 10 files. ⭐ It was a starting point; the auditor half
below is new work.

## The classification — reason recorded per parameter

| class | parameters | why |
|---|---|---|
| **SAFETY-CRITICAL POLICY** — default REMOVED | `risk_per_trade_pct` · `max_concentration_pct` · `max_position_value_pct` | these three multiply capital into a number of shares; a silent value sizes REAL MONEY on a number nobody chose |
| **LEGITIMATE PROGRAMMING** — default KEPT | `min_qty_threshold` · `tier_multipliers` · `logger` · `instrument_cache` · `lot_skew_rejection_threshold` · `min_tick_size` · `max_single_order_qty` · `broker_adapter` · `enabled` · `flat_value_rs` · `delivery_*` | ⭐ **none of these can ENLARGE a position** — a floor, tick/skew guards, a sanity cap, optional collaborators, a mode switch with its own raise, and item 1's delivery knobs whose `None` is a hard error on use |

⛔ **Deleting every default was NOT the fix.** The kept set is named parameter-by-parameter
in the new test, so removing one later is also a deliberate act.

`max_position_value_pct` moved **above** the defaulted block (a required parameter cannot
follow a defaulted one). Safe: **every** construction site passes by keyword, 0 positional.

## The call-site sweep — run, ⛔ not taken from a list

**21** real `PositionSizer(` sites (`_MockPositionSizer` is a different class, excluded).
**1 production — `main.py:2501`** — already passed all three from `ps_cfg` ⇒ ⛔ **`main.py`
is not touched.** 20 in tests, 0 positional.

## 🔴 THE AUDITOR HALF — proven necessary BEFORE it was written

The ruling rests on §5's claim that finishing NI-5 makes group F vacuous. ⭐ **I measured
that claim in an intermediate state — defaults removed, `config_auditor.py` deliberately
NOT yet fixed — so the check could come back red.** All three arms reproduced:

| arm | measured |
|---|---|
| the row is dropped **silently** | probe: `PositionSizer row emitted? -> False` — no finding of **any** severity |
| the PASS is **vacuous** | `VERDICT: PASS`, `code='F_ok'`, *"component defaults match config intent (position-value cap + daily-loss pct)"* — naming a cap it had **not** checked |
| the existing test **fails** | `test_diverging_position_cap_default_warns` → `assert False`, having **PASSED at base minutes earlier** |

⇒ this is the `V5` tautological-check class, and ⭐ it is worse than a missing check: a
missing check leaves you uncertain, a **tautological one leaves you wrongly certain**.

## What group F does now

Each registry row is classified **compared** / **required** / **unresolved**; the latter
two are reported **explicitly**; the summary names **only what it actually compared**:

```
[PASS] F_PositionSizer_max_position_value_pct_required
       metrics={'component':'PositionSizer','param':'max_position_value_pct','outcome':'required'}
[PASS] F_ok  "component defaults match config intent (FundManager.daily_loss_limit_pct)"
```

⭐ `required` is PASS because a **removed** default is STRONGER than a matching one.
⛔ `unresolved` (a rename or failed import — the guard silently ceasing to exist) is now
**visible** but deliberately **left at PASS**: changing what this audit *alerts* on is a
separate, major-impact decision under the gate and was **not** taken. ⚠️ **Flagged for
Rama:** that branch arguably deserves WARN. It is his call, not mine.

## Tests — and the control that makes them evidence

`test_diverging_position_cap_default_warns` could not survive (with no default there is
nothing to diverge *from*) and is replaced by three that pin the **property**, not a
string: the row is reported not skipped · the summary names only what it compared · an
unintrospectable row is not swallowed. Plus the new
`tests/unit/test_ni5_position_sizer_policy_required.py` (22 tests).

⭐ **CONTROL — all three new auditor tests were run against the UNFIXED auditor and all
three FAILED**, then passed against the fixed one. ⛔ They are not vacuous.

## The tripwire — HELD

Production files in the diff: **exactly `capital/position_sizer.py` +
`core/config_auditor.py`.** The other 10 are tests. That is precisely the *"+2 files
beyond the tripwire"* option (a) authorises.

## The differential gate — SET-compared, ⛔ not count-compared

| | base `742d9da` | head `a4a5cef` |
|---|---|---|
| | **10 failed · 5,748 passed · 4 skipped** (944.89 s) | **10 failed · 5,772 passed · 4 skipped** (976.55 s) |
| collected | 5,762 | 5,786 |

- **failure sets IDENTICAL** — `diff` of the sorted `FAILED` lists is **empty**;
- **+24 passes decomposes exactly**: 22 new NI-5 tests + 2 group-F tests; collection rose
  by the same 24 ⇒ ⛔ nothing unexplained;
- skips unchanged.

## ⚠️ DISCLOSED — the harness does NOT reproduce the recorded baseline

Recorded for `742d9da`: **`7F / 5,751P / 4S`**. Measured today: **`10F / 5,748P / 4S`**.
The gap is **exactly 3**, **environmental**, ⛔ not a defect in `742d9da` and ⛔ not
caused by NI-5. All 7 recorded standing failures are present and unchanged; the extra 3
are all `tests/unit/test_t4_deploy_preflight.py`.

**Cause, measured:** `D:/Projects/trading-system/venv/` is **EMPTY** (no `Scripts/`, no
`bin/`) and no sibling worktree has one ⇒ `scripts/ist_now.sh`'s `pick_python()` falls
past `$REPO_ROOT/venv/…` to `command -v python3`, the **WindowsApps stub**.
**Control, both directions, both trees** (files byte-identical, md5 `1e4eaad9…` /
`4f8e1d4a…`): without `PYTHON` → 3 failed / 6 passed; **with `PYTHON=/c/python311/python`
→ 9 passed**. ⚠️ A PATH shim for `python3` is **not** sufficient — measured.

⇒ with `PYTHON` set the base reads **`7F / 5,751P / 4S`** — the recorded baseline exactly.
🔴 **The PC gate harness needs `PYTHON` set (or a restored `venv/`) or it reads 10F.**

## ⛔ NOT DONE

⛔ Not pushed · ⛔ not deployed · ⛔ not in either §4 push (**a third unit**) ·
⛔ `max_multiplier` untouched at 2.0 · ⛔ the `raw_qty * 2` ceiling untouched ·
⛔ no config change · ⛔ `main.py` untouched.
