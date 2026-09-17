---
name: wave5_runtime_validated_08jul
description: Wave-5 (H-7/FIX-067/terminal-guard+D-1/M-C1) + eod_verify RUNTIME-VALIDATED clean on 08-Jul LIVE session (271d24f) — FULL PASS; Wave-5 fully closed+deployed+verified; TRACK-1 formally cleared
metadata: 
  node_type: memory
  type: project
  originSessionId: a1ce6ed3-8992-41fa-9570-f5c148c8d6b8
---

**Wave-5 RUNTIME validation — FULL PASS (08-Jul-2026, LIVE session, VM=PC=`271d24f`).** Read-only observation in the first-signal window (~10:00–10:16 IST). Completes the runtime half after the earlier boot-gated PASS (schema 41 / trigger present / integrity ok / eod_verify honest N/A / 0 restarts). **Note:** runbook said "paper session" but the service runs `main.py --mode live` and trades are tagged `mode=LIVE` (real broker positions) — validated on LIVE, not paper.

**Checks 1–5 evidence:**
- **C1 (signals + health):** 96 signals received today from the correct Chartink IP `23.106.53.213` (169×200 accepted; all 318×403 strictly PRE-open 09:17–09:59, the known S-1A time-gate, NOT token). 6 PROCESSED / 3 OPEN + 2 CLOSED trades. Every ERROR/CRITICAL/traceback accounted-for benign: 1 startup kill-switch CRITICAL **auto-cleared 5ms later** (new-day), 1 transient GTT `get_gtts` ReadTimeout @09:16 (pre-window, handled, delivery disabled), 4 `slippage_exceeded` OrderRejectedError (FIX-128 guard working; kill-switch correctly does NOT count them toward its connectivity breaker). ZERO IntegrityError / illegal-transition / naked / oversell / CHECK9 / CAPITAL_DRIFT / HARD_KILL / halt.
- **C2 (H-7 cap):** actively fired **5×** (positional_sector_rotation, vwap_bounce_long), each at exactly `2/2`, never exceeded; `reserved=2` in a firing proves atomic in-`portfolio_lock` reservation counting. Live DB ≤1 open/strategy. Not just "trivially holds" — genuinely stressed + held. STRONG PASS. [[h7_strategy_cap_toctou_07jul]]
- **C3 (FIX-067 fresh-LTP SL) — CONFIRMED (not deferred):** unambiguous DB+log cross-check. VAIBHAVGBL log `stale=259.09 live=259.00` → DB `entry_target_price=258.482 = 259.00×0.998` (fresh, not 259.09×0.998=258.57), `sl_initial=253.31236 = fresh-entry×0.98` (2% below the FRESH entry). GEMAROMA `stale=222.15 live=221.31` → entry `221.08869=221.31×0.999`, SL=`fresh-entry×0.988`. SL distance measured from FRESH price, not stale trigger; D1 plumbing (quote_fn→dict[str,Quote]) proven live (real distinct `live=` values, no silent stale-fallback). [[fix067_ms1_investigation_07jul]]
- **C4 (terminal-state guard):** grep for IntegrityError/illegal-transition/`trg_trades_terminal_status_guard`/RAISE(ABORT) = EMPTY. Silence = success; no writer crashed on an abort. [[terminal_state_write_guard_design_07jul]]
- **C5 (M-C1/restart):** `NRestarts=0`, ExecMainStart 08:15:12, no warm restart → M-C1 rehydrate path not exercised (expected); no capital double-jump; 2 closed net −₹11.43 sane. [[mc1_rehydrate_investigation_07jul]]

None of the FAIL indicators fired. **🏁 WAVE-5 FULLY CLOSED + DEPLOYED + RUNTIME-VALIDATED.**

**TRACK-1 clearance (now FORMAL):** P1 SHADOW deploy cleared to sequence (next OFF-market, NOT same-day, per P1 SHADOW plan [[p1_wave4_integration_validated_07jul]]) · low-sev batch C-3/C-4/F-1/E-4/A-3 cleared to build+commit [[build_plans_commitA_B_d1_07jul]] · W10 = Rama's decision · **B-1b still BLOCKED** (MTM heartbeat/observability first) · daily_report retirement needs the reports-dir check · T2/H-6 unchanged. SYSTEM_MAP.md runtime-validation changelog entry PENDING the next off-market doc-sync (market open during validation — no mid-market push). [[wave5_pcvm_sync_deployed_07jul]] · [[full_repo_audit_04jul_pending]]
