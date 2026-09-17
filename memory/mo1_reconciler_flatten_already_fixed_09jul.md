---
name: mo1_reconciler_flatten_already_fixed_09jul
description: "Wave-6 M-O1 (reconciler flatten NSE:NSE: double-prefix → FIX-181 cap dead) was ALREADY FIXED by 959badf (05-Jul), deployed in HEAD 9815786 — premise stale, NO build needed, NO residual twin"
metadata: 
  node_type: memory
  type: project
  originSessionId: 079a8694-5552-4907-ae65-c573d090d444
---

**Wave-6 M-O1 INVESTIGATION (09-Jul-2026, READ-ONLY) → FINDING: ALREADY FIXED. No build.**
The 09-Jul instruction asked to investigate + design-fix M-O1 (`order_reconciler.py::_flatten_broker_position` double-prefixes the quote key `NSE:NSE:SYM` → `ltp` always None → every reconciler flatten goes out as raw MARKET, FIX-181 marketable-limit cap silently dead). **That premise is STALE** — true only at the 04-Jul audit snapshot; remediated the next day.

**Evidence:**
- **`959badf` (2026-07-05 14:57 IST)** "fix(orders): M-O1 - flatten quote key uses bare symbol (restore FIX-181 marketable-limit cap)" IS the M-O1 fix, and **IS an ancestor of HEAD `9815786`** (i.e. DEPLOYED — same tree validated live on the VM this morning, [[push1_runtime_validation_09jul]]). Diff = the 2-line bare-symbol fix (`_quote_fn([f"NSE:{symbol}"])`→`([symbol])`, `.get(f"NSE:{symbol}")`→`.get(symbol)`) + 94-line regression test.
- Current `order_reconciler.py:1753-1760` uses the correct bare idiom; `NSE:NSE:` survives only in a past-tense explanatory comment (:1750).
- `tests/unit/test_mo1_flatten_quote_key.py` (Wave-1 regression) = **2 passed** today at HEAD (long→SELL / short→BUY marketable LIMIT, not raw MARKET).

**Flatten-path map:** `_check2_inflight_orphan:1701` (ONLY caller; fires when an in-flight orphan coincides with active HARD_KILL — FIX-181 GICRE abandonment-race backstop, tag "KILL") → `_flatten_broker_position` → `raw=self._quote_fn([symbol])`/`raw.get(symbol)` (bare) → if `ltp>0`: `marketable_limit_price(side, ltp, EMERGENCY_EXIT_BUFFER_PCT, DEFAULT_TICK)` LIMIT, else MARKET fallback (by-design, genuine no-quote only) → `_adapter.place_order(symbol=bare, ...)`.

**No residual twin.** The double-prefix was unique because it mixed idioms: `get_quote`/`_quote_fn` is **bare-in/bare-out** (adapter:1544 prepends NSE: at :1574, strips at :1588; paper delegates to injected provider, same contract). Every OTHER `f"NSE:{symbol}"` site (kill_switch.py:895/898, slippage_recorder.py:152, order_placer.py:3928-3958) uses **`get_quote_raw`** which is **prefixed-in/prefixed-out** (adapter:1622, raw kite passthrough) with MATCHED keys on request+lookup → correct usage of a different API, not a twin. Whole-repo grep for bare-contract-with-prefix misuse = only the (now-fixed) reconciler site. The twin 959badf itself flagged was a *dead-column* twin (kill_switch.py:977), a different class.

**Parity:** `_quote_fn=adapter.get_quote` mode-agnostic → one shared method covers paper+live; flatten gets a real LTP in BOTH modes (paper via injected provider). Confirmed intact.

**RECOMMENDATION:** Re-scope Wave-6 — **DROP M-O1 (DONE, deployed, test-green)**. The Wave-6 cluster list in [[fresh_audit_postremediation_08jul]] carried M-O1 forward in error (it was already closed 05-Jul). Remaining Wave-6 candidates (M-O2 CHECK4 partial-close capital/PnL, M-C3/M-C7 capital accounting, M-K1, M-R1-2, M-SC2) are unaffected by this finding and still need their own verification before any build. Did NOT start M-O2 (per instruction). No code touched. [[full_repo_audit_04jul_pending]] [[fresh_audit_postremediation_08jul]]
