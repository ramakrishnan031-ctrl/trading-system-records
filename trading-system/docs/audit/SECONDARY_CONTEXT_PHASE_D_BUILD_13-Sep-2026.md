# SECONDARY CONTEXT — PHASE D BUILD REPORT (13-Sep-2026, Sunday)

**Status: BUILT · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED · ⛔ NOT WIRED · ⛔ NOT VERIFIED LIVE.** Local branch only. Code and unit tests only, all on fixtures. **Stopped for review.**

⚠️ **ENGINEERING EVIDENCE ONLY. ⛔ It proves nothing about profitability.**

**Branch:** `feat/secondary-context-abc-13sep` in worktree `D:/Projects/wt-secctx-13sep`.
**Commits:** `932b1ed` (A+B+C, accepted) → **`3143e55`** (Phase D).

**Sources read, in rank order:**
1. `SECONDARY_FILTER_FROZEN_DESIGN_v2_12-Sep-2026.txt`
2. `ANSWERS_BEFORE_PHASE_D_13-Sep-2026.txt`
3. `UNBOUNDED_ROOM_AND_CHECK_4A_13-Sep-2026.txt`
4. `FOR_VSCODE_CLAUDE_13-Sep-2026_PHASE_D.txt`

Scanner clause text is `Chartink_scanners.v2.txt`, md5 `8f619972219adfac4eff2010a0b84f55`, byte-identical to the `D:/system_files` copy.

⚠️ **Provenance note:** sources 2 and 3 were **not on disk** when the instruction arrived (13:39). I searched for them, asked, and read them once Rama saved them (13:40:57 / 13:41:02). Nothing was built before they were read.

Line numbers are pinned to **`3143e55`**. Every figure below comes from a command run in this session. Labels: 🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE.

---

## 1. What was built, file by file, with unit-test results

🔬 `git diff --shortstat 932b1ed 3143e55`: **13 files, +1,889 / −27**. All changes are inside `secondary_context/` and `tests/unit/test_secondary_context_*`.

### New modules

**`references.py`** (146 lines): the REFERENCE a setup names.
- **Fixed levels** (`resolve_fixed_reference`, `:100`) come from completed sessions **strictly before** the session (`:117`): previous high, low or close, and the prior-N-session high.
- **Unbuildable N-session reference:** returns NotMeasurable `PRIOR_SESSIONS_REFERENCE_NOT_BUILDABLE` (`:122`), ⛔ never a shortened window.
- **IV/V window:** "Daily Max(15, …)" without "1 day ago" includes the session itself and never resolves.
- **Moving lines** (`moving_reference_at`, `:137`) read only `MinuteState.vwap` or `.ema20`.

**`adapters.py`** (237 lines): the six fields plus `required_checks` as data.
- `SetupAdapter` (`:116`) enforces consistency: breakout ⇔ fixed reference ⇔ breakout activation rule; pullback ⇔ moving reference ⇔ pullback rule.
- `ScannerBinding` (`:154`) carries numeral, scanner, product and input status.
- `ADAPTER_BINDINGS` (`:185`) holds the 16 bindings.
- `binding_for` (`:235`) raises KeyError for an unknown scanner; there is no default.

**`episodes.py`** (430 lines): the one common lifecycle.
- `EpisodeTracker` (`:219`) with its per-bar steps: `observe` `:265`, `_read` `:305`, `_step_breakout` `:320`, `_step_pullback` `:330`.
- `snapshot` (`:363`).
- `run_session` (`:419`) consumes the **existing** `SessionPass` in its single loop (`:426`).
- Three observable types: `ActivationObservable` `:160`, `FreshnessObservable` `:169`, `ExtensionObservable` `:178`.

### Changed modules

**`checks.py`**: **Check 4 is split** into `STRUCTURE_AT_SCREENING` (4a) and `ROOM_BEFORE_PLACEMENT` (4b, `:58`).
- Each check now has an `evaluation_point` (`EvaluationPoint` `:48`); 4b is `BEFORE_PLACEMENT` (`:71`).
- ⛔ No reject-reason names are encoded (Phase E; see §7).

**`session_pass.py`**: `VwapValue` (`:79`) carries `completed_minutes` and `cumulative_volume` (`:249`).
- `SessionPass.as_of` (`:179`) and `.session_open_at` (`:183`) are exposed read-only.
- The pre-volume NotMeasurable now states the minutes folded.

**`boundaries.py`**: `RoomState` (`:91`) vocabulary.
- `ROOM_STATE_SETTLED_OUTCOMES` (`:99`) maps **only** HISTORY_TOO_SHALLOW → DATA_UNAVAILABLE.
- `ROOM_STATES_AWAITING_RAMA` = {CLEAR_AIR} (`:104`).

**`__init__.py`**: module map updated; "Wiring: NONE" unchanged.

### Tests at `3143e55`

🔬 `pytest tests/unit/test_secondary_context_*.py` → **287 passed** (was 220; **+67**).

| test file | count | change |
|---|---|---|
| `episodes` | **36** | new |
| `adapters` | **13** | new |
| `references` | **8** | new |
| `no_verdicts` | **4** | new |
| `session_pass` | 31 | +5 VWAP maturity |
| `checks` | 6 | +1, Check 4 split |
| unchanged files | 189 | boundaries 22 · calendar_periods 17 · current_day_state 28 · daily_history 44 · ema 17 · ema_bases 8 · intraday 24 · isolation 9 · no_thresholds 3 · timed 17 |

---

## 2. The sixteen adapters

Columns:
- **Family / Dir / Reference** are pinned row by row against frozen design §2.1 and §2.2 by `TestTheTable::test_sixteen_bindings_match_the_design_row_for_row`.
- **Scanner names** equal `config/chartink_scanners.yaml`, and every direction equals `config/strategies/<name>.yaml` (`test_scanner_names_are_the_repos_own_and_directions_match_strategy_config`).

| # | scanner | product | input | family | dir | reference | qualifier (recorded, ⛔ never evaluated) |
|---|---|---|---|---|---|---|---|
| I | positional_swing_long | DELIVERY | LIVE | BREAKOUT | LONG | previous session HIGH | OPENED_AT_SESSION_LOW · **same adapter object as XV** |
| II | positional_sector_rotation | DELIVERY | LIVE | BREAKOUT | LONG | prior 20-session high | — |
| III | positional_momentum_long | DELIVERY | LIVE | BREAKOUT | LONG | prior 252-session high | — |
| **IV** | range_breakout_short | INTRADAY | ⛔ **NO INPUT — scanner cannot fire** | BREAKOUT | SHORT | 15-session window INCLUDING the session (never resolves) | — |
| **V** | range_breakout_long | INTRADAY | ⛔ **NO INPUT — scanner cannot fire** | BREAKOUT | LONG | 15-session window INCLUDING the session (never resolves) | — |
| VI | gap_fade_short | INTRADAY | LIVE | BREAKOUT | SHORT | previous session CLOSE | GAPPED_AGAINST_SETUP_DIRECTION_THEN_RETURNED_THROUGH_PREVIOUS_CLOSE |
| VII | gap_fade_long | INTRADAY | LIVE | BREAKOUT | LONG | previous session CLOSE | same as VI |
| VIII | gap_go_short | INTRADAY | LIVE | BREAKOUT | SHORT | previous session LOW | GAPPED_IN_SETUP_DIRECTION |
| IX | gap_go_long | INTRADAY | LIVE | BREAKOUT | LONG | previous session HIGH | GAPPED_IN_SETUP_DIRECTION |
| X | vwap_rejection_short | INTRADAY | LIVE | PULLBACK | SHORT | session VWAP | — |
| XI | vwap_bounce_long | INTRADAY | LIVE | PULLBACK | LONG | session VWAP | — |
| XII | first_pullback_short | INTRADAY | LIVE | PULLBACK | SHORT | daily EMA20 (intraday) | — |
| XIII | first_pullback_long | INTRADAY | LIVE | PULLBACK | LONG | daily EMA20 (intraday) | — |
| XIV | open_high_breakdown_short | INTRADAY | LIVE | BREAKOUT | SHORT | previous session LOW | OPENED_AT_SESSION_HIGH |
| XV | open_low_breakout_long | INTRADAY | LIVE | BREAKOUT | LONG | previous session HIGH | OPENED_AT_SESSION_LOW · **same adapter object as I** |
| **XVI** | pb01_breakout_retest | SHADOW_NO_ORDERS | ⛔ **NO INPUT — end-of-day only** | BREAKOUT | LONG | prior 20-session high | — |

**Activation and invalidation follow the family, never the scanner.**
- Breakout: `FIXED_LEVEL_CROSSING_OR_GAP_OPEN`. Pullback: `LINE_CONTACT_THEN_CLOSE_BEYOND`.
- Invalidation for all 16: `COMPLETED_CLOSE_THROUGH_REFERENCE_AT_THAT_BAR`.
- **Required checks:** every adapter declares every check REQUIRED, including 4a and 4b (AD-6; see §7).

⚠️ **THE DEAD-INPUT COUNT IS THREE, NOT FOUR.** The instruction's report item says "the four dead-input ones". Every source names exactly three:
- IV and V (design §2.1, §2.4);
- XVI (design §2.1; ANSWERS §6 "joins IV and V with no input").

No fourth is named anywhere. **The source wins.** 🔬 Pinned: `test_iv_v_and_xvi_exist_and_receive_no_input_and_nothing_else_is_dead`.

**Carried forward, pinned:**
- **I and XV:** one adapter object; 15 distinct adapters in total (`test_i_and_xv_are_one_adapter_on_two_products_and_nothing_else_shares`).
- **VI and VII:** breakout continuations through yesterday's close, not fades (`test_vi_and_vii_are_breakout_continuations_through_yesterdays_close_not_fades`).
- **Dead adapters are refused by the engine** (`NoInputForAdapter`; `test_the_dead_input_adapters_cannot_be_tracked`).

**No per-scanner branch and no scanner condition in Python** (design §1.4, §13.2).
- `test_no_engine_module_replays_a_scanner_or_branches_per_scanner` scans the AST of the three engine modules for:
  - scanner-only literals (1.5, 50000, 100, 5000, 0.005, 1.01, 0.99, 0.02, 50, 200);
  - reads of scanner-only state fields (volume, day open, so-far extremes, views, the EMA base);
  - evaluation of a qualifier;
  - any branch on scanner, numeral, adapter_id, qualifier or product.
- It is proven able to fail on 8 planted forms.

---

## 3. §2's four semantics, each with the test that pins it and the mutation that proves it bites

### 3.1 ⭐⭐ Gap-through activation (EP-4)

**Rule:** if the **first completed minute** OPENS strictly beyond the fixed level in the setup direction, the episode is **GAP_OPEN**. It is activated at that bar's **start** (the session open) and is knowable at its completion. The kind is a field: `GAP_OPEN` vs `CROSSING`.

**Pinning tests** (`TestGapOpenActivation`):
- `test_a_first_minute_opening_beyond_the_level_activated_at_the_open_by_gap`: occurred 09:15, available 09:16.
- `test_gap_open_and_crossing_are_different_kinds_never_flattened`.
- `test_the_short_mirror`.
- `test_a_gap_that_closes_back_through_on_its_first_minute_is_activated_then_invalidated`: both boundaries are kept.
- `test_only_the_first_completed_minute_can_gap_a_later_open_beyond_is_a_crossing`.
- `test_a_first_minute_that_is_not_the_opening_minute_is_recorded_as_such`: `first_bar_at_session_open=False`.

**Mutations, all RED:**
- D-02 gap-open not detected [5 failed]
- D-03 kind flattened [9]
- D-24 GAP_OPEN stamped at bar close [2]

⚠️ **WHERE THE SOURCE CORRECTS THE INSTRUCTION.** The instruction says gap-through is "the NORMAL case" for VI, VII, VIII and IX. The scanner text (📄 `Chartink_scanners.v2.txt`) says otherwise:
- **VI** (SHORT) requires `Daily Open Greater than Bracket(1 day ago Close * Number 1.01)` (`:85`). **VII** (LONG) requires `Daily Open Less than Bracket(1 day ago Close * Number 0.99)` (`:102`).
  - Their gap is **against** the setup direction, and their reference is yesterday's close.
  - So the first minute always opens on the **wrong** side, and activation can **only** be a CROSSING, never GAP_OPEN.
  - Pinned: `test_vi_and_vii_gap_against_their_direction_so_they_can_only_activate_by_crossing`.
- **VIII / IX** gap ≥1% from yesterday's **close** (`:119`, `:136`), but their reference is yesterday's **low / high**.
  - A ≥1% gap is therefore not necessarily beyond the reference, so GAP_OPEN is common but not guaranteed. Both kinds are exercised.
- The generic rule is correct for all four without any per-scanner branch. Nothing is silently discarded: a gap is detected when there is one, and a crossing otherwise.

### 3.2 ⭐ Invalidation against a moving reference, per bar (EP-6)

**Rule:** while active, a completed close strictly THROUGH the reference **as it stood at that bar**. Each reading carries the line value at its own bar.

**Pinning tests** (`TestMovingReferencePerBar`):
- `test_a_rising_line_invalidates_against_its_value_at_that_bar_not_at_activation`: close 100.8 is above the activation line 100 but below the line at that bar, 101, so the episode is **INVALIDATED**.
- `test_a_falling_line_does_not_invalidate_against_its_higher_activation_value`: close 99.5 is below 100 but above the line at that bar, 99, so it stays **ACTIVE**.
- `test_past_bars_are_never_re_judged_against_the_current_line`: closes 100.2 and 100.9 were each beyond their own bar's line but lie below the final line 101.0, and it stays **ACTIVE**.
- `test_current_side_is_against_the_lines_current_value`.
- Integration with the real EMA20 line: `test_the_real_ema20_line_drives_a_pullback_episode`.

**Mutations, all RED:**
- **D-04** activation-time line value [2]
- **D-05** current line value applied to past bars [2]

### 3.3 Touch (HIGH/LOW) vs invalidation (CLOSE) (EP-2, EP-5)

**Rule:** the bar's close gives its **side**; its high/low gives **contact**. A bar that pierces the line and closes back on the setup side is an approach-and-reaction **within one bar**, not an invalidation. Contact is geometric (the range reached the line); ⛔ no touch tolerance is applied, because that is Rama's #1. Signed excursions are recorded for it.

**Pinning tests** (`TestTouchAndInvalidationUseDifferentPartsOfTheBar`):
- `test_a_pierce_that_closes_back_on_the_setup_side_is_approach_and_reaction_not_invalidation`: contact True, adverse excursion −1.0, CONTACT_REACTION on that bar, no invalidation.
- `test_the_short_mirror_uses_the_high`.
- `test_an_active_breakout_survives_a_pierce_that_closes_beyond`.
- `test_no_contact_when_the_range_never_reaches_the_line`.
- `test_a_touch_can_be_answered_on_a_later_bar_and_a_close_through_cancels_it`.
- `test_a_close_exactly_at_the_reference_neither_activates_nor_invalidates`.
- `test_a_new_touch_and_reaction_while_active_is_the_new_activation_the_run_start_is_kept`.

**Mutations, all RED:**
- **D-06** invalidation on high/low [20]
- **D-07** touch on close [11]
- D-12 AT counted as through [3]
- D-13 pullback without a touch [4]
- D-14 a through-close keeps a pending touch [1]
- D-21 re-touch overwrites run start [1]

### 3.4 ⭐ Early-session VWAP is thin — recorded, ⛔ not ruled on (SP-8, EP-10)

**Rule:** `VwapValue.completed_minutes` (zero-volume minutes included) and `.cumulative_volume` ride on every VWAP value. Every episode reading's `reference` **is** that VwapValue. ⛔ No minimum exists.

**Pinning tests:**
- `TestVwapMaturity::test_every_vwap_carries_the_minutes_and_volume_behind_it`: (1,1000) (2,4000) (3,4000) (4,6000).
- `test_a_one_minute_vwap_is_thin_and_visible_but_not_suppressed`.
- `test_before_any_volume_the_not_measurable_states_the_minutes_folded`.
- `TestVwapMaturityOnEpisodes::test_a_first_minute_vwap_touch_is_recorded_with_its_thin_maturity`: activation with maturity (1, 100) is **recorded, not suppressed**.
- `test_a_later_touch_carries_its_own_deeper_maturity`.

**Mutations, all RED:**
- **D-08** maturity dropped [6]
- D-25 zero-volume minutes miscounted [3]

### Also pinned (instruction §1.3–§1.5)

- **Current episode** (design §13.4, `TestCurrentEpisode`):
  - **The re-cross case:** a 09:40 cross, a 09:43 fall back and an 11:00 re-cross give activation = **11:00**, with all three boundaries kept.
  - Read at earlier decisions via `truncate_to`: ACTIVE at 09:41:30, INVALIDATED at 09:50, ACTIVE at 11:01.
  - An old activation still valid.
  - No activation ever.
  - **Mutation D-01 "first crossing today": RED [3].**
- **Three observables, three types** (`TestThreeObservables`):
  - Activation: kind, age 9 min, 3 bars since.
  - Freshness: 3 bars after, 1 contact, closest return −0.4, last contact 09:22.
  - Extension: current 0.9, peak 3.0 at 09:21.
  - Same age with different extension stays different. Distances are absolute prices, signed in the setup direction; ⛔ no unit conversion, because the unit is Rama's.
  - Mutations D-22 (freshness counts the activation bar) and D-23 (extension converted to %): RED.
- **One pass over the minutes** (`TestOnePassOverTheMinutes::test_many_trackers_share_the_single_walk_of_the_bars`): three trackers (IX, XI, XIII) over one pass, **bars iterated once**. Mutation D-19 (a second walk): RED.
- **No lookahead:**
  - `test_every_snapshot_is_knowable_by_its_as_of_and_the_audit_bites`
  - `test_a_snapshot_cannot_be_taken_before_its_inputs_were_knowable` (D-20 RED)
  - `references::test_the_fixed_reference_audit_bites_before_its_last_session_completed`
  - D-15, today's bar in a fixed reference: RED.

---

## 4. The differential gate and the mutation results

### Mutations (instruction §3.2)

Harness `scratchpad/secctx/mut_secctx.py`:
- refuses a dirty tree;
- takes a green control run before **and** after;
- replaces exact bytes at anchors that must each occur exactly once;
- runs only the package tests with `-B`, sequentially;
- restores each file byte-exact (md5) and checks the tree is clean after **every** mutation.

🔬 **74 mutations at `3143e55` → 74 RED · 0 survived.**
- Control: 287 passed before and 287 after.
- Every restore byte-exact; tree clean after every mutation.
- Raw files: `mut_values_3143e55.json`, `mut_run_3143e55.txt`.

**The instruction's ten, all RED:**

| instruction §3.2 | id | failed tests |
|---|---|---|
| episode reverts to "first crossing today" (re-cross case) | D-01 | 3 |
| gap-open activation not detected | D-02 | 5 |
| activation kind flattened to one value | D-03 | 9 |
| moving-reference invalidation uses the activation-time line value | D-04 | 2 |
| moving-reference invalidation uses the CURRENT line value on past bars | D-05 | 2 |
| invalidation uses high/low instead of close | D-06 | 20 |
| touch uses close instead of high/low | D-07 | 11 |
| VWAP maturity dropped | D-08 | 6 |
| an adapter re-implements a scanner condition (volume gate in engine · 1 % gap factor constant) | D-09a · D-09b | 1 · 1 |
| a clear-air verdict is encoded (outcome map · engine flag) | D-10a · D-10b | 2 · 1 |

**Plus 15 more Phase D mutations**, all RED:
- D-11 4b folded into 4a
- D-12 through D-14 (AT rule and pending touch)
- D-15 today's bar in a fixed reference
- D-16 N-session reference silently shortened
- D-17 I/XV split
- D-18 dead adapter tracked
- D-19 second walk
- D-20 snapshot before its inputs
- D-21 run start
- D-22 freshness
- D-23 extension %
- D-24 gap stamp
- D-25 maturity count

**§3.3, the isolation and no-threshold scanners still pass AND still fail when they must.** All 47 A+B+C mutations were re-run **at the Phase D tip**: 47 RED. M-C6 was re-anchored to the new pre-volume line; its mutation is unchanged. This includes:
- M-I1 package imports the decision path [2]
- M-I2 `signal_processor` imports the package [2]
- R-I1 aliased dynamic import [1]
- M-T1 threshold default [1]
- R-T1 threshold as a product [1]

### Full differential gate (§3.1)

The baseline is this branch's current one: `final_932b1ed`, measured 13-Sep 12:32–12:51 with its environment record, on the same tree the Phase D commit sits on.

`gate_run.sh phase_d_3143e55` ran 14:10:41–14:26:38 IST (957 s), alone. 🔬 Environment, identical to the baseline record:
- Git Bash 5.2.37;
- `/c/python311/python` 3.11.9, pytest 9.0.3;
- cwd = the worktree, `PYTHONPATH` = the worktree (explicit), `PYTHON` unset;
- `instruments.csv` md5 `a7b07623…`, no `.env`, `FORCE_COLOR` unset, ANSI bytes 0;
- porcelain 0/0;
- invocation `/c/python311/python -m pytest tests/unit tests/integration -q`.

| | baseline `932b1ed` | Phase D `3143e55` |
|---|---|---|
| failed | 7 | **7** |
| passed | 6,438 | **6,505** (+67 = exactly the new tests) |
| skipped | 5 | 5 |
| collected | — | 6,517 = 7 + 6,505 + 5 |
| failure-set sha16 | `1855d12c70394465` | **`1855d12c70394465`** |
| `comm -13` (new failures) | | **empty** |
| `comm -23` (vanished failures) | | **empty** |

The pre-existing 7 are unchanged by hash; they are the same 7 as at `970aabf`.

---

## 5. ⭐ Confirmation: NO clear-air verdict is encoded anywhere

🔬 **Runtime:** `test_clear_air_is_a_state_with_no_outcome_and_awaits_rama`.
- `RoomState` = STRUCTURE_AHEAD · CLEAR_AIR · HISTORY_TOO_SHALLOW.
- `ROOM_STATE_SETTLED_OUTCOMES == {HISTORY_TOO_SHALLOW: "DATA_UNAVAILABLE"}`. This one is settled by ANSWERS §3(c) and UNBOUNDED §4.
- CLEAR_AIR is **not** in the map. `ROOM_STATES_AWAITING_RAMA == {CLEAR_AIR}`.

🔬 **Static:** `test_the_package_encodes_no_verdict_and_no_clear_air_verdict` walks every module's AST, excluding docstrings.
- No verdict or reject-reason token exists anywhere in the package: TECHNICAL_PASS/REJECT, PASS, REJECT and all eight reason names from the sources (design §3's seven plus UNBOUNDED §3's rename).
- No name couples CLEAR_AIR with PASS, REJECT, ACCEPT, ALLOW, BLOCK, TRADE(ABLE), OK or VETO.
- No assignment, dict, if, return, compare or call pairs CLEAR_AIR with an outcome token or a boolean.
- Proven able to fail on **10 planted forms**. The first run caught a gap: a verdict routed through an intermediate name (`allow = state == 'CLEAR_AIR'`). The scanner was extended and that planted case kept.

🔬 **Mutations D-10a and D-10b: RED.**

⛔ **Nothing CLASSIFIES a case into those states.** No zones exist yet, and "sufficient history" is itself undefined. Phase D gives the vocabulary only. ⛔ No threshold was derived for anything. **Case (b), unbounded room, pass or reject, is RAMA's, awaiting his own words** (UNBOUNDED §1: "Do not implement it as settled. Do not record it as his.").

---

## 6. The Monday measurement — ⛔ **NOT RUN**

Needs a Kite token. After Monday 08:20's Batch 1 proof, and **only if Rama says go**. Verbatim from the instruction §4:

> **4. ⏳ THE MONDAY MEASUREMENT — SCANNER III CLEAR-AIR FREQUENCY**
> - **4.1** TERMINOLOGY: the comparison is against **the highest high within the available completed daily history Zerodha actually returned**, ⛔ never an assumed "five-year high". Record the coverage returned for every symbol. — ⛔ **NOT RUN**
> - **4.2** THREE CATEGORIES, ⛔ NEVER MIXED: A STRUCTURE ABOVE · B CLEAR AIR · C HISTORY INSUFFICIENT. Report A/B as a fraction of sufficient-history signals, C as a fraction of all. Raw counts alongside every percentage. — ⛔ **NOT RUN**
> - **4.3** DISTANCE, NOT A BOOLEAN. For every category-A signal: signal_price · nearest_opposing_level · absolute distance · distance as % of price · available_history_days · which timeframe supplied it. — ⛔ **NOT RUN**
> - **4.4** CLEAR-AIR DEPTH for category B: highest available historical high · signal price · coverage · distance beyond that high. — ⛔ **NOT RUN**
> - **4.5** NO LOOKAHEAD: for a signal at time T, the structural cutoff is the LAST COMPLETED TRADING DAY BEFORE T. ⛔ Not later days · not later weeks · not today's final high · not any subsequent price movement. The existing `assert_knowable_by` machinery should enforce it, not a comment. — ⛔ **NOT RUN**
> - **4.6** ⛔ Do not re-implement scanner III. Use the recorded signals corpus. — ⛔ **NOT RUN**
> - **4.7** ⛔ NO THRESHOLD IS DERIVED FROM ANY OF THIS. — ⛔ **NOT RUN**

⚠️ **Two facts for whoever runs it** (📄/💭, not measured):
- **Category B vs C needs a sufficiency definition that no source gives yet.** 4.2 says "sufficient history evaluated" but names no criterion. It must be stated before the run, not chosen from the results.
- **Levels / zones do not exist in the package yet** (design §3.4.1–§3.4.2, zone width = Rama's #2). Category A as "an opposing zone" therefore cannot be computed as specified today. Only "any higher high in available history" can.

The A+B+C token-dependent list also remains **NOT RUN**: RAYMOND week · real 5-year fetch payload/latency · last-bar staleness · forming-bar behaviour · Chartink EMA20 equivalence · VWAP per-symbol systematic.

---

## 7. Readings made to build Phase D, flagged for review, ⛔ not settled

1. **Pullback "reaction" (EP-5).** ANSWERS §4 lists "what counts as a pullback's reaction" as the design owner's to specify before Phase E. Built as the minimal reading of design §6.6 plus instruction §2.3:
   - a contact sets a pending touch;
   - a completed close through the line cancels it;
   - the first completed close beyond the line while a touch is pending is the activation;
   - a fresh touch plus reaction while active is the new activation, and the run's first is kept.
2. **AT the reference is neither side (EP-3).** Activation needs strictly beyond; invalidation needs strictly through ("closes back *through* it"). Stated because reference prices sit on the tick grid, so equality happens.
3. **Gap-open uses the first completed minute's OPEN** ("the first completed minute opens already beyond it"), including when that minute is not 09:15. `first_bar_at_session_open` records which.
4. **Every check REQUIRED for every adapter (AD-6).** No source names an optional check for any setup, and an unsourced "optional" would open a hidden pass (§7.3, §13.1).
5. **QUALIFIER.** The design lists the field but does not define it. Built as recorded nomination premises that shape how an episode is read (gap direction, opened-at-extreme), never evaluated. Product lives on the binding, not the setup, because I and XV share a setup.
6. **Reject-reason naming conflict for Phase E.** The frozen design §3 names 4a's reason ADVERSE_STRUCTURE_AHEAD; UNBOUNDED §3 renames it SETUP_NOT_STRUCTURALLY_VALID. The source order ranks the design first, while the rename is the design author's own correction. Not encoded in Phase D.
7. **Evaluation points.** Only 4b is placed BEFORE_PLACEMENT, per ANSWERS §1. Checks 1, 2, 3, 4a and 5 stay at SCREENING, where the design's shape places them; no source moves them.

---

## 8. Confirmations

🔬 **Isolation:**
- `test_secondary_context_isolation.py` (9 tests) passes at `3143e55`.
- M-I1, M-I2 and R-I1 are RED at `3143e55`.
- The new modules import only the package and the standard library.

🔬 **No thresholds:**
- `test_secondary_context_no_thresholds.py` passes; M-T1, R-T1 and D-23 are RED.
- None of the five Rama numbers exists, not even as a key.
- Contact is geometric; extension is absolute price; VWAP carries no minimum.

🔬 **No push:** `git ls-remote origin refs/heads/main` = `970aabf`; the branch is absent on the remote. No VM command was run.

🔬 **No scanner, scorer, Block A/B, register or config change:** 0 files outside the package and its tests.

---

## 9. Memory — three targets

1. `docs/SYSTEM_MAP.md` top banner.
2. `PATHS.md` top banner.
3. `UNPUSHED_PENDING_DEPLOY_LEDGER` top section.

**Stopped for review. ⛔ Nothing wired, nothing pushed, nothing deployed.**
