---
name: t2_halt_investigation_reconciler_tag_bug_01jul
description: "T2 live run DEFERRED 1-Jul — the \"halt\" was actually a stuck naked-position SOFT_KILL whose emergency-flatten is BROKEN (CHECK9 tag>20 bug); T2 not run"
metadata: 
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**01-Jul-2026 ~13:00 IST — T2 live run investigated (STEP A read-only) → GATE = STOP, DEFERRED. No order placed.**
Relates to [[delivery_slice25_status_30jun]] (the T2 tracker).

**The task premise was WRONG, and the investigation surfaced a real safety bug.** The brief said the intraday
system "STOPPED on 3 consecutive losses (a benign protective halt, all flat)". The ACTUAL live state (VM
read-only): `kill_switch_state = SOFT_KILL`, set **11:31:26 by order_reconciler**, reason
`MISSING_EXITS: naked position BANSALWIRE`. Reconciler log tells the story:
- 11:31:26 CHECK9 MISSING_EXITS flagged BANSALWIRE naked (its SL order was gone from broker open orders — SL was mid-trigger).
- 11:31:26 **the reconciler's EMERGENCY MARKET EXIT itself FAILED**: `Zerodha rejected order: Invalid tags: max allowed tag length is 20` → then SOFT_KILL.
- 11:31:28 BANSALWIRE closed on its own via SL_HIT (−8.23) — the "naked" was a transient race that self-resolved.
- Now: system FLAT (0 non-terminal trades), `gtt_state`=0, **SOFT_KILL stuck** (a MISSING_EXITS/emergency kill needs manual `--resume`; not auto-cleared).

**★ REAL SAFETY BUG (P0-grade) → ✅ FIXED (01-Jul, branch `fix-emergency-exit-tag-01jul`, NOT pushed — Rama pushes off-market).**
`orders/order_reconciler.py:2133` the CHECK9 naked-position EMERGENCY MARKET EXIT passed **`tag=trade_id`** (`trd_`+32hex = 36 chars),
un-truncated → exceeds Zerodha's 20-char tag limit → the emergency flatten was REJECTED every time (the naked-position last
line of defense was broken; a genuinely naked position would NOT auto-flatten — only SOFT_KILL + CRITICAL alert). Today it
didn't bite (SL had already filled). **ROOT-CAUSE FIX (not just a point patch):** a defensive truncation GUARD at THE single
order-submission chokepoint — `broker/zerodha_adapter.py::place_order` truncates the tag right before `kite.place_order`
(`if tag: tag = truncate_tag_for_broker(tag)`), so **NO caller can EVER submit an over-length tag** (also covers the
17-18-char `ks_hard_kill_*` sweep tags, near the limit). Plus the call-site fix at `:2133` (`truncate_tag_for_broker(trade_id)`,
mirrors the entry leg `:1680`). Investigation: only `:2133` was a direct un-truncated LONG (>20) call; the 4 `order_placer.py`
`tag=trade_id` sites (2569/2737/3031/3369) are SAFE (truncated downstream by the order protocols). Matching is by order_id
not tag → truncation loses no traceability. Paper never saw this (paper path doesn't submit to Kite — parity confirmed).
**PROOF:** `tests/unit/test_emergency_exit_tag_fix.py` (6 tests) — a Zerodha-mimicking kite (rejects tag>20); FAILS on old
code (36-char tag rejected + un-truncated call site), PASSES on the fix; regression sweep 254 green (adapter/ids/reconciler).

**✅ DEPLOYED MID-SESSION 1-Jul (main `a6ed070→9ed8bbb`, ~13:55 IST) + out-of-order-resume RECOVERY.**
Rama chose deploy-now over off-market. **Mishap:** `deploy/resume.sh` was run BEFORE the fix deployed → it
CLEARED the SOFT_KILL and restarted `trading-system.service` on the OLD (unguarded) code → the system was
briefly RUNNING + TRADING-ENABLED on the un-fixed net (FLAT, so ~nil exposure — the only defect is the
naked-position emergency exit, which needs a naked position to matter). **Recovery (halt→deploy→verify→hold,
executed on Rama's GO#1):** (1) HALT — `systemctl stop token-watcher.service` FIRST (a plain `systemctl stop`
of trading-system alone would be AUTO-RESTARTED by token-watcher: mid-session = in-window + fresh token →
crash-recovery/fresh-token start path within 30s → premature trading), then `systemctl stop trading-system`
(clean exit 0), then **set a DB `SOFT_KILL` via the sanctioned `KillSwitch(store,EventBus,log).soft_kill(...)`
pattern** (mirror of `clear_kill_switch.py`; service stopped → no in-memory overwrite) as belt-and-suspenders
(any accidental start → HALT scenario → exit-4 → token-watcher respects it) + the clean tomorrow-path. (2) PUSH
`git push origin fix-emergency-exit-tag-01jul:main` (ff; post-receive `checkout -f main` + crontab no-op;
bare HEAD 9ed8bbb). (3) STATIC VERIFY (box halted): `zerodha_adapter.py` guard on disk, reconciler `:2133`
truncated, no bare `tag=trade_id`, tree=9ed8bbb, both services inactive, kill=SOFT_KILL, 0 positions, gtt_state=0.
(4) HELD for Rama's GO#2. **GO#2 (trade) = `deploy/resume.sh`** (clears kill + restarts on 9ed8bbb) + start
token-watcher → afternoon trades the FIXED net to ~15:00. **GO#2 (leave) =** keep halted; tomorrow's 08:15
auto-clears (below). LESSON: deploy the fix BEFORE resume.sh, or resume.sh runs the OLD in-memory code
(push swaps files; the RUNNING trader keeps old code until RESTART).

**STEP 4 — the stuck SOFT_KILL:** `kill_switch.clear_stale_state()` (`:199-248`) auto-clears ANY prior-calendar-day kill
regardless of type ("HEADLESS GUARANTEE — EVERY prior-day kill cleared"). Today's kill is dated 1-Jul → **tomorrow's 08:15
boot AUTO-CLEARS it; no manual `--resume` needed.** (Same-day `auto_clear_scheduled_kill` would NOT clear an emergency reason
→ needs `--resume`; so leave it HALTED for the rest of today.) BANSALWIRE is closed/flat → won't re-trigger tomorrow.

**T2 technical read (would the halt/reconciler touch a T2 CNC position?) — mostly clean, but STOP anyway:**
- A1: SOFT_KILL does NOT flatten/cancel (`kill_switch.py:449` "block new entries; allow exits and monitoring"; only HARD_KILL cancels/flattens). The halt itself won't touch the T2 position.
- A2: reconciler runs under SOFT_KILL. T2 CNC (no local trade, no gtt_state) → CHECK1/CHECK9 don't apply (need a local trade); CHECK2 orphan-adoption fires but only FLATTENS on HARD_KILL, not SOFT_KILL (`order_reconciler.py:753-779`) → leaves it (matches the 30-Jun "human order, do NOT flatten" read). So C1 holds under SOFT_KILL too.
- A3: t2 script is PURE DIRECT-API (`scripts/t2_cnc_gtt_realtest.py:60-91`) — builds its own adapter from the token file, never consults is_killed()/risk_engine; bypasses the halt. Guards = `--confirm` + market-hours only.
- A4: 15:15/EOD CNC exemption is architectural (unchanged by the kill).

**GATE VERDICT = STOP / DEFER (did not proceed to dry-run or live).** Not because the halt would touch the T2
position (it technically wouldn't), but because (1) the actual state ≠ described (stuck naked-position SOFT_KILL,
not a consecutive-loss halt), and (2) the investigation exposed a broken emergency-flatten (the tag bug) — running a
real-money CNC test into a system with compromised naked-position protection + a stuck emergency kill is exactly the
"do NOT force it" case. Recommend to Rama: clear the stuck SOFT_KILL (`--resume`), fix the :2133 tag bug, then run T2
on a clean day. ₹15 at risk is trivial; the SYSTEM STATE is the issue. Awaiting Rama's call. NO code changed, NO order placed.
