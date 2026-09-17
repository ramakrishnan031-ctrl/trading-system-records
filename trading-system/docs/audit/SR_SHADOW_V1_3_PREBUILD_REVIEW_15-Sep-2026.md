# S&R SHADOW CONTRACT v1.3 — PRE-BUILD REVIEW (VERIFY → REPORT → STOP)

**Card:** "FOR VS CODE CLAUDE — S&R SHADOW CONTRACT v1.3 — BUILD CARD", 15-Sep-2026 (pasted into this session).

**Contract read in full:** `docs/design/secondary_filteration/sr-gate/AUTHORITATIVE_SR_SHADOW_CONTRACT_v1.2.txt` (909 lines, §0–§12), plus §A1–§A8 of the card.

**Also read:** the design-folder index `00_READ_THIS_FIRST.txt`.

**Why this is a report and not a build:** two standing rules apply.
- The **pre-build review gate** (`docs/PRE_BUILD_REVIEW_GATE.md`, Rama 21-Aug) covers the signal path, schema/DB, config schema, cron and the boot path. This build touches all five.
- The card's own clauses say the same:
  - "If any clause in v1.2 or §A cannot be implemented as written, STOP and report it … do not resolve an ambiguity by choosing";
  - v1.2 §1.3/§1.4: "report that and stop".

**What has not been done:** no code has been written, and nothing has been committed, pushed, copied to a VM or changed.

**Machines:** testing VM read-only (stdout only; no file created). Production not touched.

**Model and method:** the card names Opus 4.6 High; this session ran on **Opus 5**. The session has ultracode enabled, but the card says "no workflow and no autonomous subagents — implement sequentially". The card is the more specific instruction, so everything here was read directly, in one thread.

---

## 0. VERDICT

**PROCEED WITH CORRECTIONS — after the rulings in §6.**

Nothing blocks the build technically. But the contract cannot be implemented *as written* on seven points (§3). Five more architectural choices (§4) are major-impact and are not settled by the contract. By the contract's own rule, each must be ruled, not chosen by the implementer.

---

## 1. §A — THE EIGHT CHANGES

All eight were read against v1.2. **All eight are implementable exactly as written** and will be applied. None conflicts with another §A item or with an unchanged v1.2 clause.

| # | Change | Implementable as written? | Note for the build |
|---|---|---|---|
| A1 | RECENCY evaluated per SOURCE zone; log `recency_source_zone_id` | Yes | "Most recent pivot on that source zone's origin_side within its timeframe" is taken over **all confirmed pivots** of that side and timeframe, not only the zone's own members. Depends on R7 (the weekly pivot date). |
| A2 | P provenance fields; transitional `p_provenance_available` | Yes, **but see §3 S4** | The in-memory M-S1 quote is in scope at the hook for the ten re-anchored strategies. Whether it may be logged is a ruling. |
| A3 | Two-close flip state machine (observation only) | Yes | The counter resets on any non-qualifying close, including a close exactly on the edge. Evaluated on preliminary zones only. |
| A4 | No confirming candle → `CANDLE_UNAVAILABLE` / `DATA_UNAVAILABLE_NO_CONFIRM_CANDLE` | Yes | "Completed" will be decided the way `v3_chain/truncate.py` 55-100 does: `close_ts <= as_of`. |
| A5 | `fill_price` → `resolution_price` | Yes | Grep gate in the test suite: no schema field contains `fill`. |
| A6 | §8.2 uses the confirm window's high/low/close | Yes | Adds `confirm_window_high`, `confirm_window_low`, `confirm_window_range` |
| A7 | STOP_NOT_DEFENDED → invariant `sr_shadow.stop_invariant_violated` | Yes | The mutation fixture must put the far edge **on the 0.10 grid**. With a far edge of 643.07 and no buffer, rounding down gives 643.00, which is still strictly below it, so the invariant would never fire and the test would be vacuous. |
| A8 | ENTRY_ZONE_CHECK before REQUIRED_STRUCTURE_CHECK | Yes | Reorder confirmed safe: the final-zone map is built before §5.3 either way |

---

## 2. THE CONTRACT'S INVESTIGATE-OR-STOP CLAUSES

### 2.1 §1.3 — canonical ATR: **EXISTS. Bindable unchanged.**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| 970aabf = TW = WT (md5 b7aa4658) | `core/candle_math.py` | 83-131 | `atr(candles, period, method=ATR_WILDER)` | `atr_val = sum(real[:period]) / period` … `atr_val = (atr_val * (period - 1) + tr) / period` |
| 970aabf = TW = WT (md5 db2657eb) | `core/daily_stats.py` | 34-73 | `compute_daily_stats` | `prior = [c for c in candles if _candle_date(c) < trading_date]` … `"atr14": atr(prior, atr_period)` |

- It is Wilder, `period + 1` candles are required, and it returns `None` when history is insufficient.
- `compute_daily_stats` takes only candles dated strictly before the decision date, which is exactly §1.3's "ending with the previous completed session".
- `DATA_UNAVAILABLE_ATR` maps to `atr14 is None or <= 0`.

### 2.2 §1.4 — trading calendar: **EXISTS, BUT ONLY FOR THE CURRENT YEAR → STOP ITEM S1**

| Tree | File | Lines | Literal |
|---|---|---|---|
| 970aabf | `core/config_loader.py` | 2449 | `("nse_holidays", f"nse_holidays_{_date.today().year}.yaml", NseHolidaysConfig)` |
| 970aabf | `main.py` | 441 | `def _load_holidays(app_config) -> set:` |
| 970aabf = TW = WT | `core/market_windows.py` | 93-106 | `is_trading_holiday` — weekend or configured holiday, with a special-session override |
| TW (md5 f0194cee) | `config/nse_holidays_2026.yaml` | — | "Source: NSE Circular NSE/CMTR/71775 dated 12-Dec-2025"; 15 entries. **The only holiday file on the VM and in the working tree.** |

The authoritative calendar is `MarketWindows` plus `nse_holidays_<year>.yaml`, and it covers **2026 only**. The consequences are in §3 S1.

### 2.3 §5.8 — existing 5-minute confirmation rule: **SEARCHED; NOT PROVABLY BINDABLE → `ENTRY_EVENT_ONLY`**

The search result is FF-G2/G3/G4 (`docs/audit/ENTRY_EXECUTION_FACT_FINDING_15-Sep-2026.md`), cited, not repeated. What it found:

| Rule | Where | Why it cannot be bound "unchanged" |
|---|---|---|
| PB-01 `gate_confirm` / `gate_pullback` | `screening/hard_gate.py` 369-466; `v3_chain/pb01_entry.py` 144-261 (md5-identical in both trees) | Needs a watchlist `level` and a 30-minute `atr30`. Neither has a defined source for an arbitrary intraday signal, so supplying them would be inventing a binding. It is LONG-only. FF-G2 records determinism limits: `EXPIRED_WINDOW` depends on wall-clock poll time; memoized statics persist across a failed fetch; whether Kite revises a closed bar is NOT ESTABLISHED. So conditions (a) deterministic and (b) reproducible cannot be **proven**. |
| SNR-V2 `retest_confirm.evaluate` | `sr_detector/retest_confirm.py` | A **1-minute** fold, not 5-minute; `wait_for_retest_enabled: false` |

The contract's own step 3 applies: "An inconclusive search, or any condition that cannot be PROVEN, is treated as OTHERWISE". So:
- `confirmation_rule_bound = ENTRY_EVENT_ONLY`;
- `confirmation_function_name = null`;
- `CONFIRMATION_FAILED` is never emitted.

This is the contract's default path, not an implementer's choice. Rama to acknowledge (R3).

---

## 3. CLAUSES THAT CANNOT BE IMPLEMENTED AS WRITTEN (STOP ITEMS)

### S1 — §1.4 session-gap and zero-session weeks over up to 5 years of history

Up to 5 years of daily history reaches back to 2021, but the calendar knows only 2026 (§2.2). For every date before 01-Jan-2026:
- **(i)** "a session the trading calendar says should exist is absent" **cannot be evaluated**, so `DATA_UNAVAILABLE_SESSION_GAP` is undetectable;
- **(ii)** a calendar week with no daily candles **cannot be classified** as a normal zero-session week or a data gap — the exact confusion §1.4 forbids.

v1.2 forbids writing a calendar inside the module and forbids assuming every weekday is a session.

**Options, not chosen:**
- **(a)** Rama supplies authoritative NSE holiday lists for 2021–2025 (from NSE circulars), as `config/nse_holidays_<year>.yaml`.
- **(b)** The gap check runs only inside the calendar's covered range; each row logs `calendar_coverage_start`; weeks before it are not classified.
- **(c)** Another rule.

### S2 — §7.4 / §9 name fields that have no formula anywhere in v1.2

These fields are named but not defined:
- `box_position_pct` · `rr_position_limit` · `position_test_pass`
- `daily_range_rupees` / `_pct` — the range of which day, or an average over which period?
- `stop_distance_band` — in which unit (÷ ATR is implied, not stated)?
- `target_move ÷ daily_range`
- `pivot_age_days` / `pivot_age_weeks` — which member pivot?
- `selection_difference_rupees` · `timeframe_changed_decision_flag`
- `distance_to_nearest_edge_rupees` — nearest edge of which zone?
- `adjacent_slab_buffer` — the lower or the upper neighbour?
- `boundary_within_2pct` — 2 % of what?
- `distance_to_lower_boundary` / `_upper_boundary` — Rs or %?
- the `_flip_transitions` format

The only candidate formulas are in `superseded/` files, which `00_READ_THIS_FIRST.txt` marks "DEAD. Do not build from any of them". Example: `SR_GATE_REFINED_DESIGN_FULL_14-Sep-2026.txt` 27-30 gives "position from the stop-side wall across the box; limit = 1/(1+R:R)", but its box anchors differ between worked examples. The reviews say only "log it" (`RAMA_VALUE_ADDED_REPLY…ROUND3` 732-751).

**Options:** Rama supplies each definition, **or** authorises specific named formulas, **or** removes these fields from v1.3.

### S3 — §5.8 "the signal timestamp" is not defined

Three instants exist (FF-B7). The choice changes which 5-minute candle confirms.

| Candidate | What it is |
|---|---|
| `signals.triggered_at` | Chartink scan minute. Seconds forced to 0, IST attached, not converted. |
| `signals.received_at` | `now_ist()` at webhook receipt |
| The `_process_one` instant | `now_ist()` at the start of processing (970aabf `signal_processor.py` 867-) |

Example: a scan at 10:00:00 received at 10:00:12. With `triggered_at`, the 10:00 candle confirms; it starts **before** the system knew of the signal. With `received_at`, the 10:05 candle confirms.

### S4 — §1.2 "the project's existing reference entry price" names no variable, and A2 has two readings

**Price candidates** (FF-B2):
- **(i)** `entry_price` as passed to `placer.place` and persisted as `trades.entry_target_price`: M-S1 re-anchored for the ten strategies, trigger × (1∓0.001) for the six; before FIX-075, before the tick snap.
- **(ii)** The post-FIX-075 price.
- **(iii)** The tick-snapped submitted price (persisted nowhere; PPV-Q10).

**A2 readings:** at the only feasible hook point, the M-S1 quote value, instant and branch **are in memory** for the ten strategies (970aabf `signal_processor.py` 1085-1106). A2 says "record `p_provenance_available = false` **where the fields do not exist**" and "Do NOT build the persistence".
- Reading **A:** the flag is always `false` in this build, because the fields are not persisted.
- Reading **B:** populate the four `p_` fields from memory where they are in scope. That writes them into the shadow row, which is arguably building the persistence.

### S5 — §0.2 "each signal that already passes existing entry qualification" has three defensible populations

The order of operations at 970aabf `_process_one`:

| Step | Line |
|---|---|
| `screener.screen` | 998 |
| `_derive_prices` | 1028 |
| M-S1 | 1085-1106 |
| `_admit_and_place` → `risk.approve` | 1315 |
| `fm.reserve` | 1328 |
| P1_ACCEPT evidence | 1427 |
| `placer.place` | 1446 |
| existing SNR-V1 `_sr_observe` | 1550 |

Candidate populations:
- **(a)** **Screener-passed (score ≥ 60).** This includes signals later refused for capacity, throttle, daily gate or risk. Entry price is in memory after 1106.
- **(b)** **Dispatched to placement** (the P1_ACCEPT point).
- **(c)** **Placed** — the precedent the existing S&R observer uses.

Each gives a different corpus to compare against the score ≥ 60 control. There are two more dispatch sites with the same structure: 2145-2296 and 2481-2588.

### S6 — §8.8 "TIME_CLOSE at the 15:00 candle close", and two undefined evaluator edges

- **Which bar:** the 1-minute bar starting 14:59, which closes 15:00, or the bar starting 15:00? Are bars starting at or after 15:00 eligible?
- **Late signals:** a confirming candle that closes at or after 15:00 (signals from about 14:55) has no defined outcome.
- **Missing 1-minute bars** inside the window (a feed gap) have no outcome and no sub-reason. A4 covers only the confirming 5-minute candle.

### S7 — the date of a weekly pivot (§2.2 "the pivot candle's date") is not defined for a 1W candle

The candidates are the Monday of the week, its first session date, or its last session date. The choice changes three things:
- §3.2's flip start ("daily candles strictly after the zone's latest member date"): with Monday or the first session, the pivot week's own later daily closes could flip its own zone;
- A1's "most recent pivot";
- `pivot_age_*`.

### (Readings to confirm — not stops, but not literally stated)

- **S8 — §3.5.** Conflict flags are set on *preliminary* zones, but locking happens on *final* zones. Proposed reading: a final zone is a "conflicting zone" if **any** of its source zones is flagged. Conflict detection runs on all preliminary zones before validity, because STRICT/RECENCY validity is a final-zone property.
- **S9 — §7.3.** The history split "≥ 3 years returned" is proposed as `decision_date − first_daily_candle_date >= 3 × 365 days`, calendar days.
- **S10 — "valid history" (§1.1).** Whether Kite's day candles are split/bonus-**adjusted** is **NOT ESTABLISHED**. The one-time check `scripts/sr_corp_action_spotcheck.py` exists, but no recorded result was found. Over 5 years, an unadjusted split creates phantom zones. Kite's per-request cap on `day` history is external and NOT ESTABLISHED; the fetch would be chunked.

---

## 4. ARCHITECTURE AND DEPLOYMENT — MAJOR-IMPACT FACTS THE CONTRACT DOES NOT SETTLE

### B1 — The build base cannot be the working tree

- The testing VM runs **`feat/evidence-contract-10sep @ 970aabf`**. **792 of 792** tracked code and config files in the md5-verified snapshot match that commit's blobs. Only the VM-local `config/system_config.yaml` and `config/cron_registry.yaml` differ.
- The working tree (`feat/delivery-config-split @ 6d24a83`, plus uncommitted edits) differs **in logic** from the VM: position-cap scope (EM report §0.2), `expires_at` (FF-B7), and more. It also expects **schema v46** — `core/state_store.py:102`: `EXPECTED_SCHEMA_VERSION = 46 # ALLOCATION MODEL (08-Aug-2026)` — against the VM's **v45** (970aabf:102).
- Copying any hook file from the working tree to the VM would deploy undeployed logic (D1, no partial deploy).

**Proposed:** a new branch from `970aabf` in a separate git worktree. The working tree stays untouched; nothing is committed (per §E5, the report lists what is staged).

### B2 — Log destination: a DB table collides with the working tree's v46

A shadow table in `trading_system.db` needs `EXPECTED_SCHEMA_VERSION 45 → 46` on the 970aabf lineage. The working tree's v46 is already the allocation model, so the numbers collide when the lineages merge. The working tree's own v46 comment warns that a schema bump trips `_refuse_migration` for every heartbeat-writing cron until the next 08:15 boot (WT `core/state_store.py:102`).

**Alternative:** a dedicated log outside the migration chain — its own SQLite file or JSONL under `data_store/sr_shadow/`. Precedents: `data_store/v3/would_be.jsonl`, `data_store/v3/pb01_would_be.jsonl`, `data_store/evidence/signal_evidence_<ARM>_<date>.jsonl`, `data_store/regime/regime_state.json`.

Either way it is **not** a production-path table (§0.4).

### B3 — The hook touches the signal path and boot path

- **Precedent (SNR-DETECTOR-V1):**
  - a post-place, async, never-raising observer: 970aabf `signal_processor.py` `_sr_observe` 614-658, called at 1550/2296/2588;
  - built in `main.py` 3421-3508 behind `system.sr_detector.enabled`;
  - `SystemConfig` is `extra="forbid"` (970aabf `config_loader.py` 1987-1988), so a new config block needs a schema field.
- **Timing:** the v1.3 work runs 1 daily fetch of up to 5 years plus a later 5-minute fetch. It must run on a background worker, so the signal path pays only an enqueue — no timing change (§0.4).
- **Alternative with zero pipeline edit:** an out-of-process same-day job reading persisted rows. But then only population (c)/(b) signals have a persisted entry price (`trades.entry_target_price`). The screener-passed-but-refused signals of (a) have none.

### B4 — Rate-limit blast radius (non-order)

- All fetches go through `_make_sr_fetch_fn` (970aabf `main.py` 421-438) → `rate_limiter.acquire("historical")` → `config/broker_limits.yaml` 17-19 `historical: burst 2, rate_per_sec 2`.
- **Shared with:**
  - SNR-V1, **enabled on the VM** (`sr_detector.enabled: True`);
  - PB-01 5-minute polling, 09:20–11:00, every 20 s per pending row;
  - the regime engine (60 s);
  - v3_chain.
- **The order path uses no historical bucket** (FF-G3). The shadow's load can delay those shadows, not orders.
- TW-LOG 15-Sep contains 0 historical rate-limit lines.

### B5 — Candle sources and the outcome schedule

| Need | Source today | Note |
|---|---|---|
| 1D, up to 5 years | None stored. Kite `historical_data(interval="day")` via the shared closure. | Weekly candles are built from these daily candles per §1.4 |
| 5-minute confirming candle | **None stored.** Kite `historical_data("5minute")` after the candle closes. | Aggregating 1-minute bars into a 5-minute candle as the *primary* source is not addressed by A4. **Proposed:** use broker 5-minute bars only. |
| 1-minute outcome bars | TW `analytics.db` `candles`: interval_sec 60 only, 2026-06-19 09:15 → 2026-09-15 15:29, 1,305 symbols, written by the `fetch_daily_candles` cron at 15:40. Or Kite `historical_data("minute")`. | Coverage of every shadow symbol not verified |
| Evaluator schedule | Needs bars to 15:00, so an EOD step | VM crontab precedents: `sr_detector_backfill` 15:58 · `fetch_daily_candles` 15:40 · `forward_shadow_record` 18:15. The VM crontab is hand-maintained and **must never receive the canonical crontab** (MEMORY_BOARD). A new line is a cron change; the alternative is an in-process timer. |

### B6 — Calibration exposure

"Implement with these values, expose them": a new `system.sr_shadow` block (config schema), plus a hand edit to the VM's local `system_config.yaml`, which already differs from the repo.

### B7 — Coexistence with the running SNR-DETECTOR-V1

- **V1 is live on the VM:** `timeframes [day, 60minute, 30minute]`, `lookback_days 180`, writes `sr_detector_results`, backfill cron 15:58.
- v1.2 "supersedes" earlier S&R **design files**. It says nothing about the running V1 observer.
- **Proposed:** leave V1 untouched. The v1.3 shadow is a separate module with separate logs, and **shares no code** with `sr_detector/` beyond the pure `Candle` type and the fetch closure. V1's 1H/30m pivots must never enter the v1.3 map (§2.9).

### B8 — Deployment timing

- The VM tree is not a git checkout; it receives **direct file copies** (MEMORY_BOARD: "twin (direct copy)").
- The service is `inactive` (normal 17:35 self-exit). The next start is **08:15 16-Sep** via the token watcher, and any copied file takes effect at that boot.
- A build, full suite and mutation proof will not be complete and reviewed before 08:15 16-Sep. Deploying the first build therefore targets a later boot, unless Rama rules otherwise.

---

## 5. BUILD PLAN ONCE RULED (for orientation; no code exists)

**Package:** `sr_shadow/`, pure, stdlib plus `core.candle_math`:

| Module | Contract section |
|---|---|
| `models` | — |
| `calendar_adapter` | Uses `MarketWindows` only |
| `weekly` | §1.4 |
| `pivots` | §2.1–2.2 |
| `clusters` | §2.3–2.4 |
| `flip` | §3.1–3.3, plus A3 |
| `conflicts` | §3.5 |
| `merge` | §2.5 |
| `touch` | §2.8 |
| `validity` | §2.7, plus A1 |
| `select` | §4 |
| `stop` | §6, §1.5, plus the A7 invariant |
| `decision` | §5 in A8 order, run once per variant |
| `observations` | §7 |
| `confirm` | §5.8, plus A4 |
| `evaluator` | §8, plus A5/A6 |
| `schema` | §9 |
| `runner` | Async worker; never raises into the pipeline |

- **Wiring:** mirrors SNR-V1 — default-off config flag, construction guarded, one enqueue at the ruled hook point.
- **Tests:**
  - all of v1.2 §10 with the A7 replacement, plus every §D addition;
  - no-lookahead, order-independence (shuffled input) and variant-independence property tests.
- **Mutation proof:** a scripted harness applies each §D and §10.16 mutation to a **temporary copy** of the package, runs the suite, and records RED/GREEN per mutation. Every mutation must be RED. The harness never edits the build tree.

---

## 6. RULINGS NEEDED (one reply; then the build proceeds without further review loops)

| # | Question | Options | Recommendation |
|---|---|---|---|
| R1 | S1 calendar before 2026 | (a) Rama supplies NSE holiday lists 2021–2025 · (b) gap check only within calendar coverage, logged · (c) other | (a) if the circulars can be supplied; otherwise (b) |
| R2 | S2 undefined observation fields | supply definitions · authorise named formulas · drop them from v1.3 | Drop what is not defined now and add later with a dated change; they are diagnostics only |
| R3 | §5.8 binding | acknowledge `ENTRY_EVENT_ONLY` (the contract's default for an unprovable rule) | Acknowledge |
| R4 | S3 signal timestamp | `triggered_at` · `received_at` · processing instant | `received_at`: the first instant the system knows the signal, and no confirming candle can start before it |
| R5 | S4 structural entry, and the A2 reading | price (i)/(ii)/(iii) · reading A/B | Price (i) (`trades.entry_target_price` value at dispatch) · reading A (`p_provenance_available = false` on every row this build) |
| R6 | S5 population | (a) screener-passed · (b) dispatched · (c) placed | (a): the comparison is against the score ≥ 60 control, and capacity refusals are not quality decisions |
| R7 | S7 weekly pivot date | Monday · first session · last session | Last session of the week, so no daily close of the pivot week can flip its own zone |
| R8 | S6 evaluator edges | TIME_CLOSE bar; confirm candle ≥ 15:00; missing 1-minute bars | TIME_CLOSE = close of the bar starting 14:59; bars starting ≥ 15:00 not eligible; confirm close ≥ 15:00 → `DATA_UNAVAILABLE_NO_EVAL_WINDOW`; a 1-minute gap → `DATA_UNAVAILABLE_OUTCOME_BARS` (both new sub-reasons need your approval) |
| R9 | S8–S10 readings | confirm or correct | Confirm S8 and S9. S10: run the existing split spot-check on the VM **before** the first shadow row (one read-only broker call; needs your go-ahead). |
| R10 | B2 log destination | DB table (schema v46 collision) · dedicated SQLite/JSONL outside the migration chain | Dedicated `data_store/sr_shadow/` SQLite, no migration |
| R11 | B3/B5 hook and evaluator schedule | in-process async observer + hand-added VM cron for the EOD evaluator · in-process timer · out-of-process job | In-process async observer at the R6 point, plus an EOD evaluator script on a hand-added VM cron line (15:55, before `sr_detector_backfill`) |
| R12 | B1/B7/B8 | build on a new branch from `970aabf` in a separate worktree; SNR-V1 untouched; first VM boot after full review | As stated |

The card's §F sign-off table is blank. This review treats the card pasted into this session as Rama's instruction to proceed to the gate. It does **not** treat §F as signed.

---

## 7. SOURCES READ FOR THIS REVIEW

- **Contract and design folder:** v1.2 (all); `00_READ_THIS_FIRST.txt`; `superseded/SR_SHADOW_CONTRACT_V1_1_FINAL…` and `…V1_14-Sep…` (for field lineage only); `superseded/SR_GATE_REFINED_DESIGN_FULL…` 20-40, 280-300; `superseded/RAMA_SCENARIO_ANALYSIS_REVISED_MODEL…` 75-100; `reviews/RAMA_VALUE_ADDED_REPLY_TO_WEB_CLAUDE_SR_GATE_ROUND3…` 144-152, 404-411, 556-562, 700-751.
- **Code at 970aabf:**
  - `core/candle_math.py`, `core/daily_stats.py`, `core/market_windows.py`, `core/config_loader.py` 1987-1988 and 2449, `core/state_store.py` 102;
  - `main.py` 421-446 and 3421-3508;
  - `signals/signal_processor.py` 614-658, 867-1106, 1277-1550;
  - `sr_detector/detector.py` 1-51, `sr_detector/fetch.py` 1-60, `sr_detector/models.py` 129-150;
  - `config/broker_limits.yaml` 17-19; `core/instrument_cache.py` 66;
  - all 16 strategy YAMLs (`tgt_risk_reward: 1.5`).
- **Testing VM (read-only):** `system_config.yaml` `sr_detector` block; `config/nse_holidays_*`; `analytics.db candles` summary; the crontab lines for candles, shadow and backfill jobs; `system_2026-09-15.log` lines for `sr_detector` and the historical bucket.
- **Reports:** FF B2, B7, G2–G4; PPV Q9/Q10; EM §0.2 — cited, not re-established.
- **Memory:** `pre_build_review_gate_21aug.md`, `snr_detector_v1_27jun.md`, MEMORY_BOARD (twin direct copy; never the canonical crontab).
