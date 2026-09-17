---
name: fix_190_incident
description: "FIX-190 — 19-Jun 10:00 live incident: TGT-above-circuit → emergency-exit + HARD_KILL flatten-all → THELEELA oversold short + orphan SL/TGT; service DOWN until P1 fixes"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

**INCIDENT FIX-190 (19-Jun-2026 ~10:00 IST, LIVE).** First real trading after the IP allowlist was fixed. A Chartink spike fired 5 entries in ~5s; THELEELA's exit hit the upper-circuit band and a single recoverable TGT rejection cascaded into a full HARD_KILL that flattened every open position and left orphan exit orders. Rama manually cancelled 4 orders + bought back 1 THELEELA to cover a naked short. **Net loss ₹2.87 (contained only because Rama was watching).** Service is **DOWN (HARD_KILL)** — DO NOT RESUME until P1 fixes are verified.

**Root-cause chain (evidence-backed, with code locations):**
1. **No circuit-band guard on TGT (P1).** `order_protocol_limit.place_deferred_exits` places SL then TGT; THELEELA TGT (≈target% above 484.60 entry) exceeded upper circuit 503.35 → Zerodha rejected. No clamp/skip. (`orders/order_protocol_limit.py:288-310`)
2. **TGT-only failure mislabeled as "position unprotected" → HARD_KILL (P0).** The protocol even logs `sl_still_standing` (SL DID succeed, order PENDING) but still raises; `order_placer._handle_*` except block treats ANY exit exception as POSITION_UNPROTECTED → `_emergency_market_exit` + `_fire_hard_kill_for_unprotected_position`. A recoverable TGT reject (with SL resting) nukes the whole book. (`orders/order_placer.py:2144-2179`, `:2889`)
3. **Double-sell / oversell (P0).** `_emergency_market_exit` (10:00:31.959 SELL 1) doesn't check broker qty, doesn't cancel the resting SL, and doesn't synchronously mark the trade EXITING; so HARD_KILL `_exit_all_trades_indestructible` first pass (10:00:37.073 SELL 1) still saw THELEELA OPEN and sold AGAIN → **net SHORT −1**. FIX-180's "check broker position before re-firing" is only in the RETRY loop, NOT the first pass. (`orders/order_placer.py:2919`, `capital/kill_switch.py:854-906`)
4. **Orphan SL/TGT after flatten (P1).** HARD_KILL flatten + emergency exit place direct market orders that bypass `_cancel_oco_siblings` (only runs in normal `_handle_exit_fill`, `order_placer.py:1968`). HARD_KILL market-closed AEROENTER (had SL@129.50+TGT OPEN) but never cancelled them → orphans (each a naked-short time-bomb if it fires). (`capital/kill_switch.py:854-906` lacks a pre-flatten cancel of the trade's resting exits)
5. **Duplicate SL (P2).** Two SL placers race: order_placer LIMIT_TRIPLE SL (#1, PENDING) + reconciler **G5b CRASH_RECOVERY_SL** (#2, 10:00:32.626) which thought THELEELA had "no active SL". No coordination. (`orders/order_reconciler.py` G5b)
6. **RCF mislabeled RMS/MANUAL_CLOSE (P2).** Entry filled at broker but local fill lagged (PENDING_FILL) → HARD_KILL FIX-181 broker-sweep flattened it as "orphan broker position", then the lagging local fill placed orphan exits, then CHECK1 saw broker-flat/local-open → external-close label. (`capital/kill_switch.py:913+`)
7. **No entry throttle / no test-mode (P2/P3).** 5 entries in ~5s, cap raced to 6 active (NIACL rejected at "6 active" vs `max_open_positions:5`). No inter-entry delay, no live_test_mode/ramp exist (grep-confirmed).
8. **In-session capital-drift noise (P3).** G3 drift expected=10016.60 actual=9512.88 Δ503.72 fired at 10:00:32 — CORRECT math (deployed capital) but EXPECTED during trading; ₹50 tolerance far too tight; non-escalating but noisy. Related to [[capital_operational_note]] / FIX-189 P1-B (off-hours variant already fixed).

**Worst-case (impact):** with N open positions a single circuit-reject HARD_KILLs all N, leaves up to 2N orphan exit orders (each can oversell to a naked short when it later triggers), and double-sells whichever triggered the cascade. Bounded per-day by broker MIS RMS square-off ~15:20, but unmonitored it could have stacked several naked shorts. [[deploy_requires_restart]] / [[human_order_policy]] context.

**Stage-4 fixes IMPLEMENTED + committed + pushed (19-Jun):**
- **C** (51f5e94): TGT-only failure returns partial (SL-protected) → no emergency-exit/HARD_KILL. `order_protocol_limit.place_exits` + `order_placer._persist_sl_only_protected`. THE cascade stopper.
- **D** (b4cd434): `price_math.clamp_to_circuit_band` applied in `place_exits` → SL/TGT clamped inside circuit band (prevents the trigger).
- **A** (b49764f): `broker/position_helpers.determine_close_direction` — reverse-aware flatten (skip if flat, BUY to cover short, mark EXITING) in kill_switch first pass + `_emergency_market_exit`. Stops the oversell.
- **E** (b49764f): `_cancel_trade_resting_exits` before any flatten → no orphan SL/TGT.
- **F** (dfa36c4): G5b skips recovery-SL when a non-terminal SL order already exists → no duplicate SL.
- **H** (76df472): `live_test_mode` (RiskConfig; YAML ON) → in LIVE mode caps max_open=1, max_daily=3. Gates burst/overshoot for re-enable.
- **I** (870bbc9): `capital_drift_tolerance_pct=0.10` → in-session drift tolerance = max(Rs, expected*10%) (silences normal deployed-capital drift). + hardened the new flatten helpers (fixed 12 test_fix087_* regressions: broker_net_qty/_cancel_trade_resting_exits never crash the indestructible loop).

All unit-tested; full VM suite was 3167 passed / 12 failed→since fixed.

- **G** (575a1dc): entry throttle — `SignalProcessorConfig` min_gap_between_entries_sec=20 + entry_burst_max=3/60s; `signal_processor._throttle_admit()` (thread-safe, before placement, releases reservation on reject). Prevents the 5-in-5s burst.
- **Replay test** (3af8310): `tests/integration/test_fix190_incident_replay.py` — replays THELEELA: Bug D clamps TGT into band, Bug C partial (no cascade) if still rejected, Bug A never sells a flat/short position again. 3 green.

**Bug B — DONE (3b2fcc0): observability metrics added** on top of already-correct counting. signal_processor now tracks in-memory `signals_processed / entries_placed / entries_throttled / entries_rejected` (thread-safe `_bump_metric`/`get_runtime_metrics`), merged into `/metrics` via a `metrics_provider` wired from main.py. `entries_throttled` especially was invisible from DB (throttle drops never become trades). The underlying COUNTING was already correct: `count_trades_today` excludes FAILED/CANCELLED (FIX-181 → rejects don't consume the daily budget, the "undershoot" non-issue) and the concurrent position cap is the **FIX-185 authoritative reservation cap** (`open_count + count_live_reservations`, +1 candidate, max with active_count; rejects > max_open). The "8 yesterday" was the 18-Jun restart burst FIX-185 already closed; the "6 today" was transient PENDING_FILL counting (NIACL was correctly rejected at 6). Remaining B value = pure observability metrics (signals received/placed/throttled) — a nice-to-have, NOT a safety gap. **Decision: B is effectively done via FIX-181+FIX-185; metrics deferred as cosmetic.**

**RESUMED LIVE 19-Jun ~13:24 IST** (Rama's call: stay live, tiny ₹10k). Sequence: backed up DB → flipped the 2 stuck EXITING trades (AEROENTER, THELEELA) → OPEN so the reconciler's CHECK1 would finalize them (see [[followup_reconciler_exiting_gap]]) → bumped `live_test_max_entries_per_day` 3→6 (now PERMANENT — NO revert; later set max_open 1→4 too, see [[live_test_mode_permanent]]) → `resume.sh --force` cleared HARD_KILL→INACTIVE → started. **Verified clean:** /health healthy, 0 open positions, AEROENTER+THELEELA+RCF all CLOSED_MANUAL, all orphan SL/TGT CANCELLED, NO capital-drift since restart (capital released), `LIVE_TEST_MODE ACTIVE max_open=1 max_daily=6`, count_trades_today=3 (→3 fresh PM attempts), B /metrics counters live (0/0/0/0). Note: Telegram banned in IN till 22-Jun so no confirmation alert delivered — confirmed in-conversation. Commit a64bde9 (config bump).

**Paper mode: SKIPPED per Rama** — strategy is to stay LIVE with tiny ₹10k capital (only live exposure catches real bugs). Re-enable = LIVE mode with `live_test_mode=true` (max 1 position, 3 trades/day). **Service stays DOWN until Rama's explicit go-ahead.** Rama confirmed flat in Kite. All 9 bugs addressed (C/D/A/E/F done; H/I done; G done; B already-correct); replay green; full VM regression run.
