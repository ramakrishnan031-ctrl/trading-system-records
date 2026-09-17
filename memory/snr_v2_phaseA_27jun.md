---
name: snr-v2-phasea-27jun
description: "SNR-V2 Phase A — WAIT_FOR_RETEST entry side, SYMMETRIC LONG+SHORT (divert long-into-HIGH-resistance / short-into-HIGH-support → 1m retest confirm → MARKET entry w/ structure SL); schema v38; staged, default-off, awaiting nod"
metadata: 
  node_type: memory
  type: project
  originSessionId: efdd36b2-7025-4325-9afb-024470b51473
---

**SNR-V2 Phase A (27-Jun, staged, default-OFF, schema v37→v38 .backup-tested, awaiting Rama nod).**
Branch `snr-v2-phaseA-27jun` stacked on the V1 detector branch `snr-detector-v1-27jun`.
**Now SYMMETRIC LONG+SHORT** (the SHORT mirror was folded into the SAME branch, no schema/flag
change). The ENTRY side of "trade the retest, not the level":
- **LONG**: a LONG entry inside a HIGH **resistance** zone → divert → 1m must breakout ABOVE
  band_high → retest the band → reclaim with a strong UPPER close → MARKET LONG with structure
  SL BELOW band_low; reject on timeout / break-down (close < band_low·(1−max_away%)).
- **SHORT** (mirror): a SHORT entry inside a HIGH **support** zone → divert → 1m must breakdown
  BELOW band_low → retest the band → reject with a strong LOWER close → MARKET SHORT with
  structure SL ABOVE band_high; reject on timeout / reclaim-up (close > band_high·(1+max_away%)).
Either side: dup → drop; nothing is reserved while parked (no capital ever held). NOT Phase B
(the SL-reposition / structure-break exit — parked).

**New modules (all pure/core+stdlib except the seam):**
- `sr_detector/zone_cache.py` ZoneCache — in-memory, RLock, per-symbol resistance[]+support[],
  TTL; `get()` is the SYNCHRONOUS hot-path read (miss/expired → None → fall through to normal place).
- `sr_detector/zone_warmer.py` ZoneWarmer — daemon worker; on a queued symbol fetches day/60m/30m
  (reused OhlcFetcher, paced via rate_limiter "historical") + builds zones + caches; re-warms
  before TTL. Enqueued from `signal_processor._dispatcher_loop._warm_zones` on signal arrival.
- `sr_detector/zone_builder.py` — **DRY extract**: `build_zone_knobs/build_scoring_params/
  build_flag_params` + `scored_zones_from_candles` + `split_zones`; the V1 `detector.analyze()`
  was REFACTORED to use it (one zone-building path; V1 tests green).
- `sr_detector/retest_confirm.py` — PURE state machine `evaluate(band_low, band_high, candles,
  elapsed_sec, params, direction="LONG")`; ONE deterministic FOLD from WAIT_BREAKOUT (idempotent +
  restart-safe), the directional predicates flip on `direction`. LONG: break=close>band_high,
  confirm strong UPPER close, reject on close<band_low·(1−max_away%) [break_down]. SHORT:
  break=close<band_low, confirm strong LOWER close, reject on close>band_high·(1+max_away%)
  [reclaim_up]. Retest touch (range re-enters band) is side-agnostic. The persisted state NAMES are
  shared (WAIT_BREAKOUT = "waiting for the directional break") → NO new states, NO schema/glob change.
  No pattern/indicator names. `_strong_close(c, frac, is_long)` and the RetestParams field
  `confirm_strong_close_frac` (was `reclaim_strong_close_frac`) are direction-neutral.
- `screening/retest_monitor.py` `RetestMonitor` (daemon, restart-safe like EntryGate) + `RetestDiverter`
  (the divert decision + dup-drop) + `ParkedCandidate`. Monitor polls fresh 1m (OhlcFetcher
  lookback=onem_lookback_days=2, cache_ttl=0), runs evaluate **passing `parked.direction`**,
  CONFIRMED→continue_from_retest, REJECT→release. `has_symbol` dedup so a re-signal can't
  double-park (overlap invariant). `maybe_divert`: LONG reads `zs.resistance`, SHORT `zs.support`;
  structure SL = band_low·(1−sl_buffer%) LONG / band_high·(1+sl_buffer%) SHORT; audit row flags
  BUYING_INTO_RESISTANCE (fills resistance cols) / SELLING_INTO_SUPPORT (fills support cols).

**signal_processor changes:** ctor `+zone_warmer, +retest_sl_buffer_pct`; `set_retest_diverter`
(late-bound). **Divert in `_process_one`** AFTER side known, BEFORE sizing/reserve (`:818`) →
holds NO capital; reads ZoneCache synchronously; unknown-side/miss/no-HIGH/flag-off → fall through
(BOTH sides); sets `signals.status=RETEST_WAITING`; writes a `sr_detector_results` audit row
(would_wait=1; proposed_retest_entry=band_high LONG / band_low SHORT). **`continue_from_retest`** =
sibling of continue_from_gate: re-checks KS/market-window/control/governor (NOT the 60s expiry —
park & resume), then derives `side` + `is_long` from `parked.direction`, sizes + reserves (capital
reserved HERE for the first time) + places a **MARKET** entry — structure SL=band_low·(1−sl_buffer%)
LONG / band_high·(1+sl_buffer%) SHORT + R:R-preserving TGT via the direction-aware `_derive_target`.
The bad-structure guard flips by direction (entry must sit on the profitable side of the SL).

**MARKET entry route (STEP 7):** threaded `entry_order_type` (default "LIMIT" → every existing
caller byte-identical) through `order_placer.place → full_entry_engine.execute →
{LimitTriple,CoPlusTgt}Protocol.execute → adapter.place_order`. For MARKET the protocol passes
`price=0` (kite + tick-snap ignore it). **The adapter ALREADY fully supported MARKET** (valid
order_type, paper `_synth_fill` fills MARKET at LTP) → parity is the adapter's existing
paper/live split; SL/TGT legs still flow through the existing LIMIT_TRIPLE deferred-exit path.

**Schema v37→v38:** `retest_state` (TABLE 39, pure addition, FK→signals, restart-safe parking;
DAO insert/update/release/clear_all/get_all mirrors gate_state) + **signals.status CHECK widened
with `OR status GLOB 'RETEST_*'`** (the GATE_* precedent) → `MIGRATION_TABLES[38]=["signals"]`
rebuilds the signals table (FK-safe `_rebuild_table_from_schema`; proven since v25). EOD: `eod.
set_retest_monitor` → Step-0 `clear_all` (in-memory + retest_state) alongside the gate clear.

**Wiring (main.py):** shared `_sr_fetch_fn` built once if V1 or V2 on; ZoneCache+Warmer built
before sp (injected); RetestMonitor+Diverter built after sp (need continue_from_retest);
`set_retest_diverter` + `eod.set_retest_monitor` + rehydrate + start; stop both in `_shutdown`.

**DORMANT by default (both sides):** `sr_detector.wait_for_retest_enabled=false` → nothing
constructed (zone_warmer=None, retest_monitor=None, diverter unset) → the `_process_one` divert +
dispatcher enqueue are no-ops → byte-identical. The new ctor kwargs default safely;
`entry_order_type` defaults LIMIT (MIS unchanged). **55 SR-V2 tests (every LONG branch unchanged +
full SHORT mirror)**; full unit suite green / 0 NEW regressions (31 pre-existing PC-env fails
unchanged). SHORT tests added: retest_confirm SHORT (breakdown / retest / rejection+strong-lower
→ CONFIRMED, weak→no-confirm, timeout→REJECT, reclaim-up→REJECT, margin, idempotent), SHORT divert
(in-support-zone HIGH → divert + audit, out-of-zone/cache-miss/flag-off/MEDIUM/only-resistance/dup
→ normal, unknown-side → normal), SHORT monitor poll (confirm+resume / reclaim-up reject →
RETEST_REJECTED_RECLAIM_UP), SHORT continue (MARKET SELL + SL above zone + structure TGT;
entry-above-SL → RETEST_BAD_STRUCTURE), SHORT MARKET parity (paper SELL synth-fills at LTP ==
live). Migration v37→v38 unchanged (direction was already in retest_state.direction + ParkedCandidate).

**Key design calls:** (1) divert is park-and-resume via the EntryGate precedent so it ESCAPES
the 60s expiry (continue_from_retest skips `:607`); (2) capital reserved ONLY at confirm (parked
= no capital); (3) STM stays bypassed — Phase B's structure-SL will reuse the **BreakevenManager**
`modify_order(SL leg)` pattern, NOT the CO-only STM (see investigation); (4) DRY zone_builder
shared with V1; (5) symbol dedup prevents a 2nd MARKET entry; (6) **SHORT mirror = pure
direction-generalisation, NO LONG-only special cases left behind** — ONE state machine, ONE flag,
ONE set of side-neutral knobs, NO schema change (direction already persisted). The live book is
~58% short, so the SHORT path matters; the existing LIMIT_TRIPLE leg path already places short-side
SL/TGT, so no new leg logic. Config keys renamed side-neutral PRE-MERGE (free, nothing merged):
`near_resistance_buffer_pct`→`near_zone_buffer_pct`, `reclaim_strong_close_frac`→
`confirm_strong_close_frac`. Cache-miss = fall-through (the first signal for a cold symbol places
normally; effectiveness grows with warm/re-signalled symbols). NOT pushed/restarted (Rama owns).
Related: [[snr_detector_v1_27jun]],
[[slice25_p2_gtt_durability_25jun]] (the gate_state restart-safe precedent + FK-safe rebuild),
[[feedback_paper_live_parity]], [[feedback_system_map_first]].
