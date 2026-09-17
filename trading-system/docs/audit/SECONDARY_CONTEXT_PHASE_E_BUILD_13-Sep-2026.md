# SECONDARY CONTEXT — PHASE E BUILD REPORT (13-Sep-2026, Sunday)

**Status: BUILT · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED · ⛔ NOT WIRED · ⛔ NOT VERIFIED LIVE.** Local branch only, fixtures only. **Stopped for review.**

⚠️ **ENGINEERING EVIDENCE ONLY. ⛔ It says nothing about profitability.**

**Branch:** `feat/secondary-context-abc-13sep` in `D:/Projects/wt-secctx-13sep`.
**Commits:** `3143e55` (Phase D, accepted) → `cf22f43` (Phase E) → `0f0565b` (review fixes) → **`25807e3`** (tip).

**Sources read, in rank order:** frozen design v2 · ANSWERS_BEFORE_PHASE_D · UNBOUNDED_ROOM_AND_CHECK_4A · FIVE_READINGS_SETTLED (§3 and §4 **retracted**) · RETRACTION_NO_SIXTH_NUMBER · the Phase E card. Scanner text `Chartink_scanners.v2.txt` md5 `8f619972…`.

⚠️ **Provenance:** sources #4 and #5 were **not on disk** at 15:06. I stopped and asked, as the card directs, and read both once Rama saved them (15:09). Nothing was built before they were read.

🔬 `git diff --shortstat 3143e55 25807e3`: **13 files, +2,229 / −49**, all inside `secondary_context/` and `tests/unit/test_secondary_context_*` (0 files outside). Line numbers pinned to `25807e3`.

---

## 0. What the sources settled, applied first

| settled by | what | where |
|---|---|---|
| FIVE_READINGS §1 | the reaction's **own magnitude** is recorded | `episodes.py` — every activation carries `reaction_distance` and `bars_touch_to_confirmation`; ⛔ no minimum |
| FIVE_READINGS §2 | the adapter uses **the scanner's own operator** | side is strict (`Close Greater than`), contact is inclusive (`High Greater than equal to`) — stated as the reason, not a convention |
| FIVE_READINGS §3 (kept by RETRACTION §2) | **Check 3 OPTIONAL**, 1/2/4/5 required | `adapters.py` `_DECLARED_CHECKS` |
| FIVE_READINGS §5 | qualifier stays inert | unchanged; no check reads it |
| FIVE_READINGS §6 | **4a has no reject reason at all** | `outcomes.py:86` `NEVER_REJECTS`; a verdict on 4a is a construction error (`:106`) |
| RETRACTION §1, §5.1 | **no sixth number**, no history rule, no exclusion | `parameters.py` PA-1/PA-2 — five numbers and two rules, nothing about history length |
| RETRACTION §4 | CLEAR_AIR **carries its coverage** | `check_engine.py:228-240` records sessions, first and last |

---

## 1. Structural zones (`zones.py`, 300 lines)

**Candidates** (`level_candidates` `:204`), from completed sessions **strictly before** the decision day (`:183`):
- swing highs and lows (`swing_candidates` `:186`) — an extreme strictly beyond every bar within `span` either side;
- the previous session's high and low;
- the scanner windows **15 · 20 · 252**. A window with fewer sessions is **not built** and is named in `windows_not_buildable` — ⛔ never silently shortened.

**Clustering** (`build_zones` `:237`): single-linkage over sorted candidate prices; a new zone begins where the gap exceeds the band. The band is `band_width_in_daily_ranges × median(high − low)` over the sessions used — the design's "proportional to the stock's own daily range". 🔬 Pinned by `test_five_paise_apart_read_as_one_shelf_and_the_band_is_what_does_it`: ONGC's 233.55 and 233.50 land in one zone at a wide band and in two at a narrow one, so **the band is doing the work**, not the fixture.

**⛔ Both parameters are UNSET** (`ZoneParameters` `:88`): `band_width_in_daily_ranges` is Rama's #2, and `swing_span` is the shape's own definition. Either absent ⇒ `build_zones` returns NotMeasurable (`ZONE_BAND_WIDTH_UNSET` / `SWING_SPAN_UNSET`) and every dependent check is NOT_MEASURABLE. There is no default anywhere.

**MAJOR** (ZN-5): a **daily interaction** plus a **weekly interaction** with the **same** zone, where an interaction is *the bar's range overlapped the zone **and** its close ended outside it* (`_interaction` `:231`) — price reached it **and reacted**.
- ⛔ **The tautology is excluded:** a weekly bar whose high reaches the zone but whose close lands **inside** it is not confirmation. 🔬 `test_a_weekly_extreme_that_does_not_react_is_not_confirmation` builds exactly that weekly bar and asserts `weekly_touch_count == 0`, `WEEKLY ∉ timeframes_confirmed`, `major is False`; its counterpart asserts the confirming case.

**Each zone carries** (`StructuralZone` `:136`): price range, the timeframes that confirmed it, daily and weekly touch counts, first and last interaction, every interaction (with the bar's own high **and** low), and **the coverage it was derived from**. The `ZoneSet` (`:159`) adds sessions used, first/last session, the typical daily range, the absolute band and the unbuildable windows.

**The three labels are kept apart** (`BoundarySource` `boundaries.py:121`, four members): `STRUCTURAL` · `RECENT_OBSTACLE` (today's own high/low — ⛔ never a zone candidate, never structural) · `SCANNER_REFERENCE` · `CIRCUIT`. 🔬 `test_the_obstacle_labels_are_four_and_never_merged` and `test_the_three_labels_stay_apart_and_today_is_never_structural`.

**No lookahead** is enforced, not asserted: every candidate and interaction carries the stamp of the bar it came from, `assert_knowable_by(zone_set, decision_ts)` passes, the audit bites one second early, and a weekly bar reaching into the session is refused.

---

## 2. The five checks (`check_engine.py`, 617 lines)

⭐ **Every check produces a MEASUREMENT always, and a VERDICT only when its parameter is set.**

| # | check | status | measurement | verdict needs | reject |
|---|---|---|---|---|---|
| 1 | setup still valid (`:281`) | **REQUIRED** | live last price vs the reference now, side + signed distance | — (none) | SETUP_REVERTED |
| 2 | early or late (`:313`) | **REQUIRED** | the three Phase D observables kept separate; age recomputed at **this** decision instant; extension in **both** computable units | activation age · extension limit · extension unit | ACTIVATION_TOO_OLD · OVER_EXTENDED |
| 3 | recent candles (`:376`) | ⭐ **OPTIONAL** | yesterday's completed candle · today-so-far as the CurrentDayState type · the last completed minutes; body direction, body/range, close location, wicks, volume expansion | Rama's contradiction rule | PRICE_ACTION_CONTRADICTS_SETUP |
| 4a | classify (`:454`) | **REQUIRED** | what lies ahead, which kind, how far; room state with coverage | ⛔ **never — it renders no verdict at all** | ⛔ none |
| 4b | room (`:484`) | **REQUIRED**, before placement | room from the **final** entry against the **final** stop | required room (+ the obstacle-force question, §6) | INSUFFICIENT_ROOM |
| 5 | execution (`:550`) | **REQUIRED**, last, veto only | spread as a **fraction of mid** and as a percent; crossed-quote fact | max spread fraction | EXECUTION_UNTRADEABLE |

**Check 1** uses the scanner's own strict operator: a price exactly **at** the reference is reverted (`test_a_price_exactly_at_the_reference_is_reverted_too_the_scanners_own_operator`).

**Check 2** records extension absolutely, as % of price and as % of the day's range so far; the **unit choice is config**. ⚠️ ATR is null everywhere in the live system, so choosing `ATR_MULTIPLE` yields NotMeasurable — ⛔ never a substituted unit (`test_an_unbuildable_unit_is_not_measurable_never_substituted`).

**Check 3 optional, in both directions:** with no completed candle at all the check is NotMeasurable and the decision still passes (`test_absence_does_not_block`); with Rama's rule set and contradicting, it rejects (`test_a_contradiction_still_rejects`).

**Check 4a** selects with the existing direction-aware `nearest_opposing_boundary` — for a SHORT the **largest** candidate below (`test_a_short_takes_the_largest_candidate_below_not_min`). The circuit is a **boundary, per book**: CNC/GTT executes to the quoted limit; MIS's ceiling is the limit less the band margin, and **that margin is injected, never defaulted** (🔬 `DEFAULT_CIRCUIT_MARGIN_PCT = 0.02`, `orders/price_math.py:255` @970aabf, used by the MIS limit protocol and the screener, **not** by `cnc_gtt.py`).

**Check 5** compares a fraction against a fraction and records the percent beside it, so the live system's `max_spread_pct: 0.005`-vs-percent bug is not reproduced. A crossed quote is untradeable as a **fact**, with no threshold.

⛔ **No score, no weighting, no total** anywhere: `test_one_primary_reason_and_the_others_contribute_with_no_score`.

---

## 3. The outcome contract (`outcomes.py`, 191 lines)

Three outcomes — `TECHNICAL_PASS` · `TECHNICAL_REJECT` · `DATA_UNAVAILABLE` — or **no verdict at all** while a required parameter is unset.

**Precedence, fail-closed** (`decide` `:136`): a required check that could not be evaluated → **DATA_UNAVAILABLE** → something actually failed → **TECHNICAL_REJECT** → a required verdict needs an unset parameter → **outcome None** → everything required evaluated and passed → **TECHNICAL_PASS**.

**Proof of §3.2 — required-but-unmeasurable is never a rejection.** 🔬 `test_an_unformed_zone_set_is_data_unavailable_never_clear_air` and `test_a_rejection_outranks_a_withheld_verdict_but_never_a_data_failure`: with a genuine Check-1 failure **and** an unmeasurable Check 4a in the same inputs, the outcome is DATA_UNAVAILABLE with `primary_reject_reason is None`. Mutation **E-06** (DATA_UNAVAILABLE → TECHNICAL_REJECT) is RED [10 tests].

**Proof of §3.3 — absence of evidence is never evidence of no obstacle.** An unformed zone set makes Check 4a NotMeasurable; it never becomes CLEAR_AIR, and the measurement has no `room_state` at all. CLEAR_AIR is claimed only when zones exist and none is ahead, and it then carries its coverage. Mutation **E-05** (missing zone set treated as clear air) is RED.

**One primary reason**, the rest contributing, ordered by the design's own check order (mutation **E-20** RED).

---

## 4. Gate and mutation results

### Adversarial review before the gate

A 6-dimension read-only review with per-finding skeptics (**30 agents**, 3.4 M tokens): **11 confirmed, 13 refuted**, consolidating into **7 defects, all closed** in `0f0565b`:

| # | defect | fix |
|---|---|---|
| CE-10 | an unmeasurable circuit boundary was **silently dropped** from the candidate pool, so a missing / not-yet-available / stale / direction-missing limit — or an unset MIS margin — left room measured against a weaker obstacle and could PASS | the circuit outcome is carried on the classification; 4b is NOT_MEASURABLE when the ceiling is unknown ⇒ DATA_UNAVAILABLE. 4a still classifies |
| CE-11 | 4b measured the **final** entry against the **screening-time** adverse set, so a re-anchored entry past a boundary gave a negative ratio and INSUFFICIENT_ROOM against an obstacle already behind the trade | the adverse set is re-selected at the final entry; nothing ahead ⇒ NotMeasurable, never a pass, never a reject |
| CE-12 | the RECENT_OBSTACLE carried **full force** in the only Check-4 rejection, though its force is explicitly unspecified | 4b **withholds** its verdict when the nearest obstacle ahead is the recent one, and records both ratios (see §6) |
| CE-9 | `refuse_lookahead` omitted `recent_minutes` | guarded append; a late minute bar is refused |
| ZN-6 | `ZoneInteraction` recorded one "extreme that reached in" whose else-branch was dead | records the bar's own high **and** low |
| tests | the weekly-tautology test was **vacuous** (`if inside:` never true) and every ZN-5 mutation survived | explicit weekly PeriodBar closing inside the shelf, plus its confirming counterpart |
| tests | `nearest_is_major` unobserved | pinned in both arms — **and the first version was itself vacuous**, see below |

### Mutations

🔬 **105 mutations at `25807e3` → 105 RED · 0 survived.** Control 358 passed before and after; every restore byte-exact; tree clean after every one. (`mut_values_25807e3.json`, `mut_run_25807e3.txt`.)

**The card's §5.2 twelve, all RED** (failing-test counts in brackets):

| §5.2 mutation | id | result |
|---|---|---|
| 4a rejects on any structure ahead | E-01 | RED [10] |
| nearest-boundary selection uses min() for a SHORT | M-H1 | RED [5] |
| circuit boundary applies a band % | E-03 | RED [8] |
| MIS/CNC clamp difference collapsed | E-04 | RED [5] |
| a missing zone set treated as clear air | E-05 | RED [2] |
| a required check's NOT_MEASURABLE becomes TECHNICAL_REJECT | E-06 | RED [10] |
| Check 3 absence blocks the trade | E-07 | RED [1] |
| Check 3 contradiction ignored | E-08 | RED [1] |
| an unset parameter acquires a default | E-09 | RED [3] |
| a verdict rendered with a parameter unset | E-10 | RED [1] |
| today's high/low admitted as a structural level | E-11 | RED [3] |
| weekly confirmation from a mere weekly extreme | E-12 | RED [2] |

Plus 13 more Phase E mutations and 7 that undo the review fixes (E-26…E-32), and **all 74 A–D mutations re-run at this tip** (§5.3) — including the isolation and no-threshold scanners (§5.4): M-I1, M-I2, R-I1, M-T1, R-T1 all RED.

⚠️ **One mutation survived the first run and is worth recording.** **E-31** (delete the `:major` marker from the structural boundary label) survived at `0f0565b`: my new `nearest_is_major` test derived its expectation from the **same** label substring the code parses, so both sides agreed and the test could not fail. That is precisely the vacuity the reviewer had warned about, reproduced by the harness. The test now asserts against each **zone's own** `major`, with a true arm and a false arm (`25807e3`), and E-31 is RED. 🔬 Two harness facts recorded: the mutation harness itself crashed decoding a pytest message as cp1252 and was fixed to read UTF-8 with `errors="replace"`; the tree was restored clean by its `finally` in both runs.

### Full differential gate (§5.1)

Baseline: this branch's current one, `phase_d_3143e55` (measured 14:10–14:26 with its environment record). `gate_run.sh phase_e_25807e3` ran 16:13:48–16:36:07 IST (1,339 s), alone. 🔬 Environment identical to the baseline record: Git Bash 5.2.37 · `/c/python311/python` 3.11.9 · pytest 9.0.3 · cwd and `PYTHONPATH` = the worktree (explicit) · `PYTHON` unset · instruments md5 `a7b07623…` · no `.env` · `FORCE_COLOR` unset · ANSI bytes 0 · porcelain 0/0 · `pytest tests/unit tests/integration -q`.

| | baseline `3143e55` | Phase E `25807e3` |
|---|---|---|
| failed | 7 | **7** |
| passed | 6,505 | **6,576** (+71 = exactly the new tests, 287 → 358) |
| skipped | 5 | 5 |
| collected | — | 6,588 = 7 + 6,576 + 5 |
| failure-set sha16 | `1855d12c70394465` | **`1855d12c70394465`** |
| `comm -13` (new failures) | | **empty** |
| `comm -23` (vanished failures) | | **empty** |

The 7 pre-existing failures are unchanged by hash, and are the same 7 as at `970aabf`.

**Package tests by file at the tip** (358): check_engine 47 · daily_history 44 · episodes 40 · session_pass 31 · current_day_state 28 · boundaries 26 · intraday 24 · calendar_periods 17 · ema 17 · timed 17 · zones 15 · adapters 13 · isolation 9 · ema_bases 8 · references 8 · checks 6 · no_verdicts 5 · no_thresholds 3.

---

## 5. ⭐ Confirmations

🔬 **No clear-air verdict, anywhere.**
- `ROOM_STATE_SETTLED_OUTCOMES == {HISTORY_TOO_SHALLOW: "DATA_UNAVAILABLE"}`; **CLEAR_AIR is not in it**; `ROOM_STATES_AWAITING_RAMA == {CLEAR_AIR}`.
- The static scan is now **narrower, not weaker**: only `outcomes.py` and `check_engine.py` may name a verdict at all; in every other module the ban is absolute (`test_the_context_layer_itself_still_names_no_verdict_at_all`), and **no module** — those two included — may pair CLEAR_AIR with an outcome, a boolean or a verdict name. Proven on 10 planted forms.
- Nothing classifies into `HISTORY_TOO_SHALLOW`: there is no sufficiency rule to classify with, because there is no sufficiency filter (RETRACTION §1.2).

🔬 **No parameter defaults.**
- `OpenParameters()` is all `None` (`test_an_unset_parameter_never_becomes_a_default`), and so is `ZoneParameters()`.
- The threshold scanner covers the new modules and still bites: E-09 (an age default) and E-13 (a band-width default) are RED through it.
- The MIS band margin is injected; unset ⇒ NotMeasurable ⇒ DATA_UNAVAILABLE, never an invented clamp.
- ⛔ There is **no sixth number** and **no history-length parameter** anywhere.

🔬 **No verdict is rendered while a parameter is unset.** With every parameter unset the engine runs end to end, every check measures, `withheld_for` names each missing parameter, and `outcome is None` (`test_with_every_parameter_unset_the_engine_runs_and_renders_no_verdict`). Mutations E-10 (a verdict without its parameter) and E-24 (a withheld verdict passing by omission) are RED.

🔬 **Isolation:** 9 isolation tests pass; the package imports only the standard library and itself; 0 files outside the package name it; M-I1/M-I2/R-I1 RED.

🔬 **No push:** `origin/main` is still `970aabf`; the branch is absent on the remote; no VM command was run.

---

## 6. Readings — ⛔ not settled, listed for review

1. **The force of a RECENT OBSTACLE against room (the biggest one).** Design §8.1 gives today's high/low "a different label with different force"; ANSWERS §4 records that force as still owed; no later source supplies it. Phase E therefore **withholds** 4b's verdict when the nearest obstacle ahead of the final entry is the recent one, and records **both** ratios — against it, and against design §3.4.4's own pool (structural level or circuit limit) — so the ruling can be applied to already-recorded shadow rows. ⚠️ **Giving it full force and giving it none are both answers to the unanswered question**; withholding is the only reading that decides nothing, but it does mean a breakout whose entry sits under today's high produces no room verdict until the rule exists.
2. **Swing span.** A swing needs a span to be a swing. It is not one of the five numbers and not a trading threshold, so it is treated like `EmaSeed` in Phase C: **required, with no default** — absent ⇒ zones unformed.
3. **Zone band basis.** The band is `multiplier × median daily range` over the sessions used. The design says "proportional to the stock's own daily range"; **median** is my choice of that range, recorded on the ZoneSet so it is visible.
4. **Interaction = overlap + close outside.** That is my reading of "price actually reacted there". It is what excludes the weekly tautology; a different reaction definition would change which zones are major.
5. **Check 2 with no current episode** is NotMeasurable (required ⇒ DATA_UNAVAILABLE) rather than a rejection: nothing is late if nothing activated.
6. **Check 3 with no completed candle at all** is NotMeasurable — today-so-far alone is a state, never a candle. Being optional, it does not block.
7. **Check 5's crossed quote** rejects with no threshold; only the spread magnitude needs Rama's number.
8. **Evaluation points.** Only 4b is BEFORE_PLACEMENT (ANSWERS §1). Checks 1, 2, 3, 4a and 5 stay at SCREENING; no source moves them.
9. **4b's stop-distance guard** treats a stop not behind the entry as NotMeasurable, not as a rejection.

---

## 7. Still not run

⛔ **The Monday measurement** (scanner III clear-air frequency) — needs a token, after Batch 1's 08:15/08:20 proof and **only on Rama's go**. RETRACTION §6 removed its first blocker (there is no sufficiency rule to define); **zones now exist, so its second blocker is gone too** — the measurement can use `build_zones` with a band width Rama supplies, and must report coverage per symbol.

⛔ Also still NOT RUN: RAYMOND week · real 5-year fetch payload/latency · last-bar staleness · forming-bar behaviour · Chartink EMA20 equivalence · the VWAP per-symbol systematic.

---

## 8. Memory — three targets

1. `docs/SYSTEM_MAP.md` top banner.
2. `PATHS.md` top banner.
3. `UNPUSHED_PENDING_DEPLOY_LEDGER` top section.

**Stopped for review. ⛔ Nothing wired, nothing pushed, nothing deployed.**
