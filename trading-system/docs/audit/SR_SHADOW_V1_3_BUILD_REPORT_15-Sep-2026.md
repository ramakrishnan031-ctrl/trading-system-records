# S&R SHADOW v1.3 — BUILD REPORT (LOG-ONLY, GATES NOTHING)

**Cards:**
- "FOR VS CODE CLAUDE — S&R SHADOW CONTRACT v1.3 — BUILD CARD"
- "… CONTRACT ADDENDUM AND BUILD AUTHORISATION"

Both dated 15-Sep-2026 and pasted into this session.

**Contract built:** `docs/design/secondary_filteration/sr-gate/AUTHORITATIVE_SR_SHADOW_CONTRACT_v1.3.txt` = v1.2 + card §A1–§A8 + addendum.

**Pre-build review:** `docs/audit/SR_SHADOW_V1_3_PREBUILD_REVIEW_15-Sep-2026.md`. The rulings R1–R12 there were answered by the addendum.

**Model and method:** the card names Opus 4.6 High; this session ran on **Opus 5**. The session has ultracode on, but the card says "no workflow, no autonomous subagents", so the build was done sequentially in one thread.

**Where it lives:**
- **Code:** a separate worktree, `D:/Projects/wt-sr-shadow-15sep`, on branch `feat/sr-shadow-v1.3-15sep` created from **`970aabf`** (the testing VM's code; R12). The working tree `feat/delivery-config-split` is untouched.
- **Commits and pushes:** none (§E5). The build files are **staged** in that worktree (§11).
- **Testing VM:** nothing copied, no cron line, no broker call. See §10 for what is held and why.
- **Production:** not contacted.

---

## 0. IN ONE PARAGRAPH

The shadow is built and proven locally.
- **Signal path:** every screener-passed signal writes one immutable snapshot to a durable spool before the signal path continues. That is the only work added to the signal path.
- **Worker:** a background worker rebuilds the 1D + 1W structure map from scratch per signal, runs the §5 path once per validity variant (STRICT and RECENCY; no canonical decision), and writes one row to a dedicated SQLite file.
- **Evaluator:** an EOD script fills the §8 counterfactual outcomes from broker 5-minute and 1-minute candles.

**Tests:** 188 new tests, all green. **Mutations:** all 25 required mutations are demonstrated RED against the unmodified-copy baseline (§6). **Regression gate:** no regression against pristine `970aabf` in the same environment (§5).

**Deployment to the testing VM is prepared but held** (§10). It needs Rama's explicit go, because the §F and §6 sign-off columns are blank. It also needs Rama to name the one corporate action for the authorised spot-check (R9/S10).

---

## 1. §A — EVERY CHANGE CONFIRMED APPLIED

| # | Change | Where implemented | Proven by | Mutation RED |
|---|---|---|---|---|
| A1 | RECENCY per SOURCE zone; `recency_source_zone_id` | `sr_shadow/zones.py` `valid_recency`; `pipeline.py` writes `recency_<side>_recency_source_zone_id` | `test_a1_recency_decided_by_the_qualifying_source_of_opposite_origin`, `test_a1_merged_zone_where_no_source_qualifies_is_not_recency_valid` | M19 |
| A2 | P provenance; `p_provenance_available` | `pipeline.py`: `p_provenance_available = False` on every row (addendum §2.1, reading A). No `p_*` fields added. | `test_structural_entry_is_the_snapshot_value_and_p_provenance_is_false_on_every_row`; statistics report `rows_with_trustworthy_p` (0 this build) | — |
| A3 | Two-close flip state machine (observation only) | `zones.py` `resolve_flip(…, closes_required=2)`, fed to `flip_result_2close` only | `test_a3_*` (5 tests) | M20 |
| A4 | No confirming candle → `CANDLE_UNAVAILABLE` / `DATA_UNAVAILABLE_NO_CONFIRM_CANDLE` | `evaluator.py` `select_confirming_candle`, `evaluate_signal` | `test_a4_*` (4 tests) | M21 |
| A5 | `fill_price` → `resolution_price` | `schema.py` (no column contains "fill"); `evaluator.py` | `test_a5_*`, `test_a5_no_field_is_named_fill` | — |
| A6 | §8.2 on the window HIGH/LOW/CLOSE; `confirm_window_*` | `evaluator.py` `counterfactual_entry_invalid`; schema adds the three fields | `test_a6_*` (LONG ×5, SHORT ×4, clean ×1, row-level) | M22 |
| A7 | STOP_NOT_DEFENDED → invariant `sr_shadow.stop_invariant_violated`; row `INVARIANT_VIOLATION`; excluded from statistics | `pricing.py` `stop_invariant_holds`; `decision.py` §5.6; `runner.py` logs ERROR with every input; `params.REJECT_CODES` has no STOP_NOT_DEFENDED | `test_a7_*`, `test_invariant_violation_marks_the_row_and_logs`, `test_stop_not_defended_is_not_a_reject_code` | M23, **M25 (non-vacuity: buffer removed, far edge on the 0.10 grid)** |
| A8 | ENTRY_ZONE_CHECK before REQUIRED_STRUCTURE_CHECK | `decision.py` `decide_variant` (5.3 inside → 5.4 required → 5.5 lock → 5.6 invariant → 5.7 target) | `test_a8_*` (2 tests) | M24 |

---

## 2. ADDENDUM — EVERY RULING CONFIRMED APPLIED

| Ruling | Applied as |
|---|---|
| **§1 session gap** | The check runs only on the calendar's last 15 expected sessions (`bars.check_data_available`). Deeper history is never voided. Logged fields: `history_first_candle_date`, `history_candle_count`, `history_span_days`, `history_weekday_coverage_pct`, `calendar_coverage_start`. The calendar reads **every** `config/nse_holidays_<year>.yaml`, so added years extend coverage without code. |
| **R2** | 11 fields defined as written (§3 below). Every other undefined field is NULL and listed in `contract_formula_undefined_fields` (§7). |
| **R3** | `confirmation_rule_bound = ENTRY_EVENT_ONLY`, `confirmation_function_name = NULL`, and CONFIRMATION_FAILED is never emitted (a test greps every module). The determination is recorded in `params.CONFIRMATION_BINDING_DETERMINATION`. |
| **R4** | `received_at` is read by `signal_id` from `signals` (read-only) and logged as `signal_timestamp_used` plus `signal_timestamp_source = signals.received_at`. |
| **R5 / §2.1** | Captured in `signal_processor._process_one` right after the path's own M-S1 step: the first point where this path's entry price is final, and before sizing and admission. The worker never re-derives it. |
| **R6** | Population = every screener-passed signal. A sizing refusal still captures (test). The EOD evaluator records `admission_status` / `admission_reason` from `signals`; the row is never removed. |
| **R7** | The weekly candle is dated at its last actual session (`bars.build_weekly`). |
| **R8** | TIME_CLOSE = close of the bar beginning 14:59. Bars beginning at or after 15:00 are ineligible. A confirming candle closing at or after 15:00 → `DATA_UNAVAILABLE_NO_EVAL_WINDOW`. A missing bar → `DATA_UNAVAILABLE_OUTCOME_BARS`, and the scan stops there. |
| **R9** | S8: a final zone is conflicting if any source is flagged (`FinalZone.structure_uncertain_flag`). S9: calendar-anniversary split (`bars.years_before`). S10: spot-check **not yet run** (§10). |
| **R10** | `data_store/sr_shadow/sr_shadow.db`: own `meta.schema_version = 1`; a mismatch is refused, never migrated; atomic single-transaction writes; duplicates refused; no trading-DB write or schema change. One dataset, no JSONL. |
| **R11** | Background worker plus an EOD evaluator script; the cron line is prepared, not installed (§10). Bar presence and retention evidence in §10. |
| **R12** | Built from `970aabf` in a separate worktree. SNR-DETECTOR-V1 files are untouched: only the shared `Candle` type and the fetch closure are reused. Testing VM only; no commit or push. |
| **§4.1** durable enqueue | `ShadowStore.spool_insert`: WAL + `synchronous=FULL`, one INSERT before `capture()` returns. A write failure is caught, logged ERROR and counted, and never raised. The evaluator reconciles screener-PASSED against the spool every day and lists missing captures. **Local cost:** spool insert p50 4.04 ms, p99 4.34 ms (🔬 Windows PC, today). The twin's fsync was measured earlier on the BOARD at mean 2.03 ms, p99 2.71 ms (n = 600); that is an earlier measurement, not re-measured for this build. |
| **§4.2** caching | Raw daily candles are cached per `(symbol, as-of date)`, LRU 512. Zone maps, validity and decisions are never cached (a test asserts `build_structure_map` runs per signal). Every fetch goes through the shared `rate_limiter.acquire("historical")` closure. |
| **§4.3** 5-minute source | Broker 5-minute candles only. A test proves 1-minute bars are never aggregated into a confirming candle. |
| **§4.4** A7 fixture | The mutation fixture's far edge is 480.00, on the grid. A companion test shows 480.07 would have made the mutation vacuous. |
| **§4.5** statistics | `evaluator.outcome_statistics`: total rows · rows with trustworthy P · rows with CONTRACT_FORMULA_UNDEFINED fields · INVARIANT_VIOLATION rows (excluded) · per variant: DATA_UNAVAILABLE by sub-reason · COUNTERFACTUAL_ENTRY_INVALID · AMBIGUOUS_SAME_BAR · resolvable · TARGET_HIT / STOP_HIT / TIME_CLOSE · the §8.6 stress statistic · **a per-decision breakdown**, so rejected-variant counterfactuals never mix into SHADOW_TRADE figures. |
| **§4.6** no lookahead | Only daily candles strictly before the decision date are used; the current week never becomes a weekly candle; a confirming candle must be completed; bars start at or after T; P comes from the snapshot. A property test appends future candles and gets an identical row. |
| **§4.7** variants | One immutable structure map, frozen dataclasses, two independent `decide_variant` calls. A test proves they disagree and are never collapsed (M18). |

---

## 3. WHAT WAS BUILT

**New package `sr_shadow/`** (2,697 lines, including the 21-line `__init__.py`):

| Module | Lines | Role |
|---|---|---|
| `params.py` | 207 | FROZEN constants; `Calibration` (from config, recorded per row as `calibration_json`); the §5.8 binding determination |
| `calendar.py` | 130 | Wraps `core.market_windows.MarketWindows` over every `nse_holidays_<year>.yaml`; None where uncovered |
| `bars.py` | 152 | Completed daily, weekly (§1.4 + R7), coverage fields, DATA_UNAVAILABLE checks (addendum §1) |
| `zones.py` | 457 | Pivots §2.1–2.2, clustering §2.3, geometry §2.4, flip §3 + A3, conflicts §3.5, sorted-sweep merge §2.5, touch §2.8, validity §2.7 + A1 |
| `pricing.py` | 131 | §6 stop, §6.5 slabs, §1.5 10-paise-then-tick rounding (Decimal), A7 invariant, adjacent slab |
| `decision.py` | 432 | §5 per variant in A8 order (**no ATR input**); §7 observations; addendum §3 formulas |
| `evaluator.py` | 278 | §8 with A4/A5/A6/R8; §4.5 statistics |
| `schema.py` | 222 | §9 columns (single source of truth); evaluator-owned column list |
| `store.py` | 253 | Dedicated SQLite, spool, rows, evaluation runs |
| `pipeline.py` | 156 | Pure snapshot + candles → one decision row |
| `runner.py` | 258 | `SrShadowService` (capture, worker, retry/backoff, counters), `DailyHistorySource` (chunked 5-year fetch, raw cache), `build_sr_shadow` |

**Wiring** (`git diff 970aabf`, 195 insertions / 1 deletion):

| File | Change |
|---|---|
| `signals/signal_processor.py` | `sr_shadow=None` ctor param; a guarded capture right after M-S1; `_sr_shadow_capture` (never raises) |
| `main.py` | `_sr_shadow_on` joins the shared fetch-closure condition; construction next to SNR-V1 inside try/except; SignalProcessor arg; `_shutdown` stop. ⚠️ **Corrected 16-Sep:** this block does not raise, but it can still fail the boot. The service registers `sr_shadow` in its ctor (`runner.py:120`, after the calendar and store are built). If construction fails, the C2 check (`effect_telemetry.assert_composition`, `main.py:4277`) finds `sr_shadow` missing: in **paper** it raises and fails the boot; in **live** it sends a CRITICAL and continues. SNR-V1 behaves the same way. |
| `core/config_loader.py` | `SrShadowConfig` + `SrShadowSlabConfig` (validators) + `SystemConfig.sr_shadow` |
| `config/system_config.yaml` | `sr_shadow:` block — `enabled: true` plus the CALIBRATION register values |
| `config/expected_managers.yaml` | `sr_shadow` entry, `expected-active` (C2: a new manager ctor needs a registry entry in the same diff) |

**Scripts:**
- `scripts/sr_shadow_evaluate.py` (191 lines): the EOD evaluator. Testable `run()`; trading DB read-only; refuses today before 15:30; idempotent; catches up earlier unevaluated dates, outcomes only, within 7 days; exit 2 when rows are left unevaluated.
- `scripts/sr_shadow_mutation_check.py` (298 lines): the mutation proof.

**Tests** (2,197 lines): `tests/unit/sr_shadow_testkit.py` + 7 `test_sr_shadow_*.py` modules.

**Paper↔live:** identical code. Paper's market-data handle is the read-only kite built by the existing `_build_market_data_kite`; the mode only tags the row.

---

## 4. TEST SUITE (v1.2 §10 as amended, + §D + addendum)

**Environment:** local Python 3.11.9 · `PYTHONPATH=D:/Projects/wt-sr-shadow-15sep` (the inherited PYTHONPATH pointing at the main tree was overridden) · cwd = worktree · `python -B -m pytest -q -p no:cacheprovider tests/unit/test_sr_shadow_*.py`.

**Result:** **188 passed, 0 failed.**

| Module | Tests | Covers |
|---|---|---|
| `test_sr_shadow_zones.py` | 34 | §10.1 zone · §10.2 touch · §10.3 flip · §10.4 merge · A1 · A3 |
| `test_sr_shadow_bars_calendar.py` | 21 | §10.6 weekly · calendar · addendum §1 · R7 · R9/S9 |
| `test_sr_shadow_pricing.py` | 11 | §10.7 (A7-amended) stop · rounding · tick · slabs |
| `test_sr_shadow_decision.py` | 46 | §10.5 entry · §10.8 target · §10.9 paths · §10.13/§10.14 · §3.5 · A7 · A8 · addendum §3 |
| `test_sr_shadow_evaluator.py` | 39 | §10.10 5m · §10.11 prices · §10.12 counterfactual · §10.15 outcome · A4 · A5 · A6 · R8 · §4.5 |
| `test_sr_shadow_pipeline_runner.py` | 31 | row · no-lookahead · order-independence · variants · §9 schema · R10 store · spool · cache · the signal-path seam (R6, §2.1) · `build_sr_shadow` |
| `test_sr_shadow_evaluate_script.py` | 6 | coverage reconciliation · admission metadata · idempotence · fetch failure · catch-up · dry run · read-only trading DB |

---

## 5. REGRESSION GATE (`pytest tests/unit tests/integration`)

**Method:** the identical invocation was run on two trees and the failing-test sets were compared by node id.
- **Baseline:** a pristine detached worktree at `970aabf` (`D:/Projects/wt-base-970aabf-15sep`).
- **Build:** the build worktree.

**Environment (both runs):**
- Local Python 3.11.9 from Git Bash.
- `PYTHONPATH` = that run's own worktree (the inherited main-tree path was overridden).
- cwd = that worktree.
- `config/instruments.csv` present in both.
- Command: `python -m pytest tests/unit tests/integration -q -p no:cacheprovider -rfE`.

| Run | Started (IST, 15-Sep) | Result | Wall |
|---|---|---|---|
| Baseline `970aabf` | 23:18 | **10 failed, 6215 passed, 5 skipped** | 944.84 s |
| Build `feat/sr-shadow-v1.3-15sep` | 23:34 | **10 failed, 6403 passed, 5 skipped** | 1095.69 s |

**Comparison:**
- **New failures in the build: 0.**
- **Baseline failures that disappeared: 0.**
- **Passes:** +188, exactly the 188 new shadow tests. The rest of the suite is unchanged.

**The 10 failures are identical, by node id, in both runs.** They are pre-existing at `970aabf` and independent of this build:
- `test_closure_source_contract::test_no_module_restates_the_vocabulary_literals`
- `test_fix181::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active`
- `test_main::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret`
- `test_main::TestContinueFromGate` ×3: `test_no_placer_releases_reservation_and_updates_status`, `test_price_hit_calls_placer_with_correct_prices`, `test_stats_placed_incremented_on_success`
- `test_phase17_batch2::test_fix077_flask_max_content_length`
- `test_t4_deploy_preflight` ×3: `test_ist_now_emits_valid_ist`, `test_check_tz_fails_on_broken_utc_form`, `test_check_tz_passes_on_agreement`. These are PC shell/timezone environment tests.

**Re-check after the gate:** two YAML **comment** lines were reworded after the gate so that they cite the addendum rather than attribute sign-off to Rama:
- `config/system_config.yaml` line 549;
- `config/expected_managers.yaml` line 126.

Every test file that reads either YAML (23 files) was re-run after the edit: **4 failed, 760 passed**. The 4 failures are the pre-existing `test_main` ones above.

**Could this gate have been RED?** Yes. The wiring touches `main.py`, `signal_processor.py`, `config_loader.py`, the repo YAML (`sr_shadow.enabled: true`) and the C2 registry (`expected-active`). The suite includes the boot, config-loader, registry-composition and signal-processor tests that would fail on a broken ctor, a missing registry entry or an invalid config block.

---

## 6. MUTATION PROOF — every mutation RED

**Harness:** `scripts/sr_shadow_mutation_check.py`.
- Each mutation runs on a **fresh temp copy** of `sr_shadow/` plus the shadow tests; the build tree is never edited.
- The import is proven to resolve to the copy.
- The **unmutated copy is GREEN** first.
- Each anchor must occur exactly once.

**Baseline (unmutated copy):** 188 passed in 3.01s — rc 0.

| ID | Mutation (contract reference) | Verdict | Suite result | Caught by (first tests) |
|---|---|---|---|---|
| M01 | §10.16 mutate the nearest zone | **RED** | 4 failed, 184 passed in 3.08s | `test_a_conflicting_zone_that_is_not_locked_is_logged_and_processing_continues`, `test_l2_l3_are_logged_but_never_selected`, `test_no_noise_threshold_or_stepping_code_in_any_shadow_source` (+1 more) |
| M02 | §10.16 mutate the target wall | **RED** | 3 failed, 185 passed in 3.12s | `test_long_target_must_fit_before_the_resistance_near_edge`, `test_reject_code_is_first_failing_step_and_others_are_diagnostics`, `test_strict_and_recency_codes_are_independent` |
| M03 | §10.16 mutate the stop edge | **RED** | 14 failed, 174 passed in 3.13s | `test_a7_invariant_violation_marks_the_variant_logs_inputs_and_is_not_a_reject`, `test_a_farther_wall_is_never_substituted`, `test_distances_buffers_and_ratios` (+11 more) |
| M04 | §10.16 remove the clear-air reject | **RED** | 4 failed, 184 passed in 3.10s | `test_a8_straddle_with_no_other_zone_on_the_required_side_is_entry_inside_never_absent`, `test_clear_air_and_history_limited_absent_codes`, `test_uncertain_takes_precedence_over_absent_when_both_hold` (+1 more) |
| M05 | §10.16 remove the inside-zone reject | **RED** | 8 failed, 180 passed in 3.10s | `test_a8_straddle_with_both_sides_present_is_entry_inside`, `test_a8_straddle_with_no_other_zone_on_the_required_side_is_entry_inside_never_absent`, `test_a_zone_on_either_side_containing_the_entry_rejects` (+5 more) |
| M06 | §10.16 invert long/short rounding | **RED** | 14 failed, 174 passed in 3.09s | `test_distances_buffers_and_ratios`, `test_l2_l3_are_logged_but_never_selected`, `test_long_base_is_shadow_trade_with_contract_stop_and_target` (+11 more) |
| M07 | §10.16 let 5m alter structure (the 5m close moves the target) | **RED** | 1 failed, 187 passed in 3.06s | `test_evaluator_uses_confirm_entry_while_the_decision_used_structural_entry` |
| M08 | §10.16 make the baseline step to L2 | **RED** | 4 failed, 184 passed in 3.09s | `test_a_conflicting_zone_that_is_not_locked_is_logged_and_processing_continues`, `test_l2_l3_are_logged_but_never_selected`, `test_no_noise_threshold_or_stepping_code_in_any_shadow_source` (+1 more) |
| M09 | §10.16 insert an ATR floor into §5 | **RED** | 1 failed, 187 passed in 3.05s | `test_no_atr_term_in_the_decision_path` |
| M10 | §10.16 apply the buffer % to the entry price instead of the level | **RED** | 12 failed, 176 passed in 3.11s | `test_distances_buffers_and_ratios`, `test_l2_l3_are_logged_but_never_selected`, `test_long_base_is_shadow_trade_with_contract_stop_and_target` (+9 more) |
| M11 | §10.16 count AMBIGUOUS_SAME_BAR in the resolvable denominator | **RED** | 1 failed, 187 passed in 3.06s | `test_statistics_keep_ambiguous_invalid_and_data_unavailable_out_of_the_resolvable_denominator` |
| M12 | §10.16 count COUNTERFACTUAL_ENTRY_INVALID as TARGET_HIT | **RED** | 1 failed, 187 passed in 3.05s | `test_a6_invalid_row_outcome_is_invalid_not_data_unavailable_and_has_no_resolution_price` |
| M13 | §10.16 allow today's candle into the structure map | **RED** | 3 failed, 185 passed in 3.10s | `test_todays_and_future_candles_are_excluded`, `test_no_lookahead_candles_on_or_after_the_decision_date_change_nothing`, `test_todays_candle_cannot_flip_via_the_completed_daily_filter` |
| M14 | §10.16 merge opposite-side overlapping zones | **RED** | 4 failed, 184 passed in 3.09s | `test_flips_resolve_before_merge_and_a_merged_zone_is_never_reflipped`, `test_mixed_origin_merge_is_the_union_with_per_source_provenance`, `test_same_side_overlap_merges_and_exact_edge_equality_joins` (+1 more) |
| M15 | §10.16 count every candle of one visit as a separate touch | **RED** | 1 failed, 187 passed in 3.06s | `test_one_visit_spanning_many_candles_counts_once_two_visits_twice` |
| M16 | §10.16 use pivot_count where touch_count is specified | **RED** | 2 failed, 186 passed in 3.10s | `test_a1_recency_decided_by_the_qualifying_source_of_opposite_origin`, `test_pivot_count_and_touch_count_differ_and_strict_uses_touch_count` |
| M17 | §10.16 re-flip a merged zone | **RED** | 1 failed, 187 passed in 3.06s | `test_flips_resolve_before_merge_and_a_merged_zone_is_never_reflipped` |
| M18 | §10.16 collapse the two variant decisions into one | **RED** | 1 failed, 187 passed in 3.05s | `test_two_variants_are_never_collapsed_and_disagreement_is_ambiguous` |
| M19 | §D evaluate RECENCY against merged members instead of source zones | **RED** | 2 failed, 186 passed in 3.08s | `test_two_variants_are_never_collapsed_and_disagreement_is_ambiguous`, `test_a1_recency_decided_by_the_qualifying_source_of_opposite_origin` |
| M20 | §D reset the two-close counter only on an opposing close | **RED** | 2 failed, 186 passed in 3.11s | `test_a3_close_exactly_on_the_edge_resets_the_counter`, `test_a3_close_then_failing_close_then_close_does_not_flip_counter_reset` |
| M21 | §D substitute the previous candle when the confirming one is missing | **RED** | 1 failed, 187 passed in 3.04s | `test_a4_missing_confirming_candle_never_substitutes_the_previous_one` |
| M22 | §D check §8.2 on the close alone | **RED** | 7 failed, 181 passed in 3.09s | `test_a6_invalid_row_outcome_is_invalid_not_data_unavailable_and_has_no_resolution_price`, `test_a6_long_invalid_cases[100.8-97.9-100.0]`, `test_a6_long_invalid_cases[103.2-97.9-100.0]` (+4 more) |
| M23 | §D restore STOP_NOT_DEFENDED as a reject code | **RED** | 2 failed, 186 passed in 3.05s | `test_a7_invariant_violation_marks_the_variant_logs_inputs_and_is_not_a_reject`, `test_invariant_violation_marks_the_row_and_logs` |
| M24 | §D restore the original §5.3/§5.4 order | **RED** | 1 failed, 187 passed in 3.04s | `test_a8_straddle_with_no_other_zone_on_the_required_side_is_entry_inside_never_absent` |
| M25 | A7 remove the buffer from §6.2 — the invariant must fire | **RED** | 28 failed, 160 passed in 3.15s | `test_a8_straddle_with_both_sides_present_is_entry_inside`, `test_a_conflicting_zone_that_is_not_locked_is_logged_and_processing_continues`, `test_a_farther_wall_is_never_substituted` (+25 more) |

**25 of 25 mutations RED; none vacuous.**

**Run:** 15-Sep, after the regression gate, on the final staged code.
- Command: `PYTHONPATH= PYTHONIOENCODING=utf-8 python -B scripts/sr_shadow_mutation_check.py`, from the build worktree.
- Harness exit code 0.
- Full JSON, with every failing node id per mutation, was saved to the session scratchpad as `sr_shadow_mutation_results_final.txt`.

**Two notes, so that no RED is over-read:**
- **M01 and M08.** A static test, `test_no_noise_threshold_or_stepping_code_in_any_shadow_source`, is among the tests that catch them. Each is also caught by three behavioural tests (`test_the_nearest_zone_by_near_edge_is_locked_never_a_farther_one`, `test_l2_l3_are_logged_but_never_selected`, `test_a_conflicting_zone_that_is_not_locked_is_logged_and_processing_continues`), so neither RED rests on a text search.
- **M25 is the A7 non-vacuity proof.** It removes the buffer from the production `compute_stop`. The base fixture's far edge (480.00 / 520.00) sits on the 0.10 grid (addendum §4.4), so the stop lands exactly on the level and the invariant fires. `test_the_base_fixture_never_violates_the_invariant` goes RED, and every SHADOW_TRADE expectation becomes INVARIANT_VIOLATION (28 tests). Separately, `test_a7_off_grid_far_edge_would_make_the_mutation_vacuous_which_is_why_the_fixture_is_on_grid` shows that an off-grid edge (480.07) would have let this mutation survive.

---

## 7. FIELDS NULL WITH `CONTRACT_FORMULA_UNDEFINED` (addendum §3 — listed, never inferred)

Every row lists them in `contract_formula_undefined_fields`. None was deleted from the schema.

**Always undefined (formula not given in v1.2 or the addendum):**
- `atr14_pct` — "atr14 Rs and %" names no base.
- Per variant (`strict_` and `recency_`), for both `support_` and `resistance_`:
  - `final_zone_width_pct` (the base of the %);
  - `merge_enlarged_flag` (the enlargement test);
  - `zone_width_pct`;
  - `rejection_ratio` (a zone has many member pivots; no zone-level formula).
- Per variant:
  - `stop_candidate_l1_distance_pct`, `stop_candidate_l2_distance_pct`, `stop_candidate_l3_distance_pct`;
  - `stop_distance_pct`;
  - `risk_pct`;
  - `target_distance_pct`.

**Conditionally undefined (listed on the row only when it occurs):**
- `<v>_<side>_flip_result_2close` — a merged zone whose source zones disagree under the two-close variant. v1.2/A3 define the two-close result per preliminary zone only.
- `<v>_adjacent_slab_buffer` — P exactly equidistant from both neighbouring slab boundaries, so "the NEARER neighbouring slab" has no answer.

Defined per the addendum and implemented as written:
- `daily_range_rupees/_pct`, `box_position_pct`, `rr_position_limit`, `position_test_pass`;
- `stop_distance_band`, `target_move_div_daily_range` (logged as §9's `<v>_target_div_daily_range`);
- `pivot_age_days/_weeks`, `distance_to_nearest_edge_rupees`, `selection_difference_rupees`, `timeframe_changed_decision_flag`;
- `distance_to_lower/upper_boundary`, `boundary_within_2pct`, `adjacent_slab_buffer`, `flip_transitions`.

---

## 8. READINGS APPLIED — named, each isolated to one function or constant so it can be ruled

None of these selects structure, moves a stop or target, or changes a canonical decision. Each is a literal reading of text that is silent on the edge case.

| # | Clause | Reading applied | Where |
|---|---|---|---|
| 1 | §2.1 symmetric window | The FIRST `PIVOT_WINDOW` candles, like the last, cannot be confirmed pivots (they lack `PIVOT_WINDOW` candles on one side) | `zones.detect_pivots` |
| 2 | §3.3 "the current incomplete week cannot flip" | Flips use completed DAILY closes after the member date (§3.2 as written), including completed days of the current week. The incomplete WEEKLY candle never exists, so it can never flip anything. | `zones.resolve_flip`, `bars.build_weekly` |
| 3 | §6.5 / addendum §3 slab edges | Bands `[0,100) [100,200) … [800,1100] (1100,∞)`, honouring both "under 100" and "above 1100". Exact-boundary prices are flagged `<v>_slab_boundary_exact_flag`. **Unreachable for today's strategies:** P = tick-valid trigger × (1∓0.001 or 0.002) never lands exactly on 100/200/…/1100. | `pricing.pick_slab` |
| 4 | addendum §3 `stop_distance_band` edges | `[0,0.5) [0.5,0.75) [0.75,1.0) [1.0,1.25) [1.25,1.5] (1.5,∞)`, honouring "<0.5" and ">1.5" | `decision.stop_distance_band` |
| 5 | addendum §1 "the 2026 calendar always covers this window" | When the 15-session window needs a date in a year with no holiday file (early January, if the prior year's file were absent), the check is logged `UNADJUDICABLE_CALENDAR_COVERAGE` and **nothing is voided** — the addendum's own principle. Not reachable while `nse_holidays_2026.yaml` remains. | `calendar.last_expected_sessions`, `bars.check_data_available` |
| 6 | `calendar_coverage_start` | First day of the contiguous run of covered years ending at the decision year | `calendar.coverage_start` |
| 7 | `history_span_days` | Inclusive calendar span from the first to the last completed daily candle; `history_weekday_coverage_pct` over the same span | `bars.history_coverage` |
| 8 | `flip_transitions` on a MERGED zone | The chronological union of its source zones' transitions, in the addendum's `{date, from_side, to_side}` form | `FinalZone.flip_transitions_json` |
| 9 | `selection_difference_rupees` "per side" | Two columns: `<v>_selection_difference_rupees_support` / `_resistance` | `schema.py` |
| 10 | "nearest 1D-/1W-sourced candidate / zone alone" | The preliminary SOURCE zones of the variant's valid candidate final zones on that side, using their own geometry; `timeframe_changed_decision_flag` runs §5.6–§5.7 with only the nearest 1D (resp. 1W) source per side | `decision._nearest_source`, `_single_timeframe_decision` |
| 11 | A1 "log which source zone satisfied it" when two qualify | The first qualifying source in merge order | `zones.valid_recency` |
| 12 | §5.9 "decision_strict == decision_recency" | Compares the decision value (SHADOW_TRADE / REJECTED / …); reject codes stay separate fields (§5.10) | `pipeline.py` |
| 13 | A7 "mark the row INVARIANT_VIOLATION" | A violation in either variant marks the ROW (`invariant_violation_flag`, `shadow_decision`); that variant's decision is INVARIANT_VIOLATION; the path stops (no target) | `decision.py`, `pipeline.py` |
| 14 | §8 which variants are evaluated | Any variant that has a stop and a target, including e.g. TARGET_BEYOND_WALL rejects; variants without them get outcome NULL. Statistics are broken down by decision so the two never mix. | `evaluator.evaluate_signal`, `outcome_statistics` |
| 15 | R8 NO_EVAL_WINDOW vs A4 CANDLE_UNAVAILABLE | When both apply, the outcome sub-reason is NO_EVAL_WINDOW; `confirmation_status` still records the candle's availability | `evaluator.evaluate_signal` |
| 16 | `resolution_timestamp` / `gap_slippage_*` | A hit or AMBIGUOUS is stamped at the resolving bar's start; TIME_CLOSE at 15:00. `gap_slippage` is 0.0 on a non-gap hit and NULL where there is no hit. | `evaluator.resolve_outcome` |
| 17 | `confirmation_status` values | `CANDLE_OBTAINED` \| `CANDLE_UNAVAILABLE`; `confirmation_result` is NULL under ENTRY_EVENT_ONLY | `params.py` |
| 18 | "screener-pass point" | Immediately after M-S1, the first point where this path's entry price is final. A signal diverted by SNR-V2 WAIT_FOR_RETEST (**disabled on the VM**) returns before this point and would show as `missing_capture` in the daily coverage reconciliation, never silently. | `signal_processor._process_one` |
| 19 | Non-market failures | No market-data handle, a missing `received_at`, or a broker fetch error is **never** a DATA_UNAVAILABLE decision: the spool row retries with back-off and ends FAILED (counted) | `runner.process_spool_row` |
| 20 | 5-year daily request | Chunked into ≤1,000-day `day` requests (the broker's per-request span is not stated in code: NOT ESTABLISHED) | `runner.DailyHistorySource` |

**Anything in v1.2 the code could not express:** none outside the fields in §7 and the readings above.

---

## 9. WORKLOAD (addendum §5) — to be measured after the first session

The service keeps these counters, logged at stop:
- `captured`, `capture_duplicates`, `capture_failures`;
- `rows_written`, `attempt_failures`, `spool_failed`, `invariant_violations`;
- `DailyHistorySource.stats`: `cache_hits`, `cache_misses`, `fetch_calls`.

Each evaluator run records `fetch.distinct_symbol_dates` and `fetch.fetch_calls` in `evaluation_runs`.

The historical-bucket wait is not directly logged by the rate limiter; it has to be measured from worker timestamps after the first session. **Not yet measured.**

---

## 10. TESTING-VM DEPLOYMENT — PREPARED, HELD FOR RAMA'S EXPLICIT GO

**Why held:**
- The card's §F and the addendum's §6 sign-off columns are blank.
- Standing rule: a card cannot speak for Rama.
- R12: "a correct build reviewed on 17-Sep beats a rushed one deployed on 16-Sep".

**Before the first shadow row — R9/S10 spot-check (authorised, NOT run):**
- Exactly one read-only call: `scripts/sr_corp_action_spotcheck.py --symbol <SYMBOL> --around <EX-DATE> --window 20` on the VM with a live token (after 08:15).
- **Input needed from Rama:** the symbol and ex-date of a known split or bonus inside the last 5 years. The script's docstring example (IDEA, 2026-01-15) is not a verified corporate action, and choosing one would be inventing evidence.
- If the result shows a discontinuity: STOP and report before any row is treated as evidence.

**Pre-copy check:** on the VM, `md5sum` of the four files to be replaced must equal their `970aabf` content (🔬 computed locally with `git show 970aabf:<file> | md5sum`). Any mismatch means the VM has drifted: STOP.

| File | md5 at `970aabf` |
|---|---|
| `main.py` | `85219d2285a0b07bc363ebd9e31bac6e` |
| `signals/signal_processor.py` | `da8c6f983e92f8644656dbe0a081e51d` |
| `core/config_loader.py` | `a034fc0816582717267bcb1ef70ba5f8` |
| `config/expected_managers.yaml` | `1dad38c53d556db8c8652389f2838d5f` |

Also check that `sr_shadow/` and `scripts/sr_shadow_evaluate.py` do not already exist on the VM, so nothing is overwritten.

**Copy (direct copy, never a push), into `/home/ubuntu/systems/trading-system/`:**
- `sr_shadow/` (12 files) · `scripts/sr_shadow_evaluate.py`
- `main.py` · `signals/signal_processor.py` · `core/config_loader.py` · `config/expected_managers.yaml`

This is the complete change set (D1). Tests and the harness are not needed on the VM.

**VM-local config** (`config/system_config.yaml` is VM-local and differs from the repo): append the identical `sr_shadow:` block (repo lines added after the `sr_detector` block).

**Timing:**
- Copy while the service is stopped (after its 17:35 self-exit); it takes effect at the next 08:15 boot.
- Never restart while a manual stop is standing.
- The first rows appear at the first screener pass. The first evaluator run is that day at 16:05.

**Cron line — hand-added on the VM only, never the canonical crontab, never `cron_registry.yaml`.** The exact line to install:

```
# sr_shadow_evaluate  [16:05 Mon-Fri]  S&R SHADOW v1.3 EOD evaluator — HAND-ADDED, TESTING VM ONLY
5 16 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/sr_shadow_evaluate.py >> logs/cron-sr-shadow-evaluate.log 2>&1
```

**R11 — why 16:05; bar presence and retention (EVIDENCE, read-only today):**
- **1-minute bars exist by 15:40.** On the VM, `fetch_daily_candles` runs at 15:40 and pulls broker 1-minute history. `analytics.db candles` holds 15-Sep bars 09:15–15:29 for 78 symbols, and 09/10/11-Sep likewise through 15:29. So the broker's day of minute bars is complete by 15:40, and a 16:05 run is after it.
- **Proof on the first real run** is intrinsic: any missing bar is reported per row as `DATA_UNAVAILABLE_OUTCOME_BARS`.
- **No retention job can delete the evaluator's inputs or outputs:**
  - the bars are fetched from the broker at run time, not from a local store;
  - `scripts/output_retention.py` scope is closed to `reports/output` and `logs`;
  - `scripts/db_retention.py` targets `trading_system.db` tables;
  - `log_cleanup` deletes `logs/*.log` older than 30 days by mtime; the evaluator's append-mode cron log is touched daily.
  - Nothing targets `data_store/sr_shadow/`.
- **Deadline:** the evaluator must run before **05:00**, when `token_cleanup` deletes the token. 16:05 satisfies this.
- **Concurrency:** the service is still running at 16:05 (self-exit 17:35). The worker and evaluator share `sr_shadow.db` under WAL with a 10 s busy timeout. The evaluator writes only evaluator-owned columns of already-decided rows.

**Rollback:** set `sr_shadow.enabled: false` in the VM-local YAML before a boot (not constructed ⇒ byte-identical pipeline), remove the cron line, and restore the four files from `970aabf`. `data_store/sr_shadow/` can be left in place.

⛔ **Corrected 16-Sep: `enabled: false` ALONE IS NOT A ROLLBACK.** While `config/expected_managers.yaml` still lists `sr_shadow` as `expected-active`, a boot with the flag off fails the composition check in paper mode. The flag and the registry must be reverted **together**; restoring the four files from `970aabf` does that, since it restores the registry. The same applies in the other direction: never deploy the registry entry without the flag and the code.

⛔ **Corrected again 16-Sep ~01:00: the VM-local `sr_shadow:` block must ALSO be REMOVED in the same action.** At `970aabf`, `SystemConfig` is `extra="forbid"` (`core/config_loader.py:1988`, validated at `:2507`). A leftover block fails config load, and so the boot, in **any** mode. 🔬 Proven locally on the twin's own YAML: `970aabf` loader + block ⇒ `INVALID sr_shadow extra_forbidden`; the control without the block is VALID.

**The atomic rollback is therefore:** restore the 4 files + remove the block + remove the cron line, in one stopped-service action. It is recorded as a standing note in `docs/SYSTEM_MAP.md` (16-Sep).

**Blast radius:**
- The signal path gains one guarded durable INSERT (≈ milliseconds).
- Historical fetches share the 2/s bucket with SNR-V1, PB-01, regime and v3_chain. The order path uses none of these.
- No trading-DB write; no score, sizing, admission or order change.

---

## 11. WHAT IS STAGED (worktree `D:/Projects/wt-sr-shadow-15sep`, branch `feat/sr-shadow-v1.3-15sep`, NOT committed)

**Git state:**
- `HEAD` = `970aabf3c78d777d9d34549e021f7c8e756c7bdb`, with no commits on the branch.
- `git status --short` shows every change staged and nothing unstaged.
- The index holds **27 files, +5,578 / −1**: 22 added, 5 modified.

| Status | File | Lines |
|---|---|---|
| M | `config/expected_managers.yaml` | +7 |
| M | `config/system_config.yaml` | +25 |
| M | `core/config_loader.py` | +75 |
| M | `main.py` | +35 / −1 |
| M | `signals/signal_processor.py` | +53 |
| A | `sr_shadow/__init__.py` | +21 |
| A | `sr_shadow/bars.py` | +152 |
| A | `sr_shadow/calendar.py` | +130 |
| A | `sr_shadow/decision.py` | +432 |
| A | `sr_shadow/evaluator.py` | +278 |
| A | `sr_shadow/params.py` | +207 |
| A | `sr_shadow/pipeline.py` | +156 |
| A | `sr_shadow/pricing.py` | +131 |
| A | `sr_shadow/runner.py` | +258 |
| A | `sr_shadow/schema.py` | +222 |
| A | `sr_shadow/store.py` | +253 |
| A | `sr_shadow/zones.py` | +457 |
| A | `scripts/sr_shadow_evaluate.py` | +191 |
| A | `scripts/sr_shadow_mutation_check.py` | +298 |
| A | `tests/unit/sr_shadow_testkit.py` | +127 |
| A | `tests/unit/test_sr_shadow_bars_calendar.py` | +231 |
| A | `tests/unit/test_sr_shadow_decision.py` | +360 |
| A | `tests/unit/test_sr_shadow_evaluate_script.py` | +168 |
| A | `tests/unit/test_sr_shadow_evaluator.py` | +324 |
| A | `tests/unit/test_sr_shadow_pipeline_runner.py` | +495 |
| A | `tests/unit/test_sr_shadow_pricing.py` | +113 |
| A | `tests/unit/test_sr_shadow_zones.py` | +379 |

**Not done:** no commit (§E5), no push, and `origin` was not contacted. A commit needs Rama's authorisation.

**Also changed, outside the worktree (untracked docs in the main tree):**
- `docs/design/secondary_filteration/sr-gate/AUTHORITATIVE_SR_SHADOW_CONTRACT_v1.3.txt` (new);
- `…/sr-gate/superseded/AUTHORITATIVE_SR_SHADOW_CONTRACT_v1.2.txt` (moved, md5 91465dc2…);
- `docs/design/secondary_filteration/00_READ_THIS_FIRST.txt` (the file-1 row and folder map now name v1.3; the "state of play" paragraph is left as Rama wrote it);
- this report.

**Not part of the change:** `config/instruments.csv` (gitignored) was copied into the two worktrees so the gate is runnable. The pristine comparison worktree is `D:/Projects/wt-base-970aabf-15sep` (detached at `970aabf`).
