---
name: book-not-long-only-eod-reverse-aware
description: "The book runs intraday SHORT strategies (NOT long-only), so a net-short broker position is EXPECTED, not an oversell. EOD squareoff is reverse-aware (BUYs to cover a short). Distinguish open-short vs oversell via broker buy_qty/sell_qty."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 73061e50-ca6a-4e2e-95e9-91b381c0e60d
  modified: 2026-07-24T07:11:18.040Z
---

**The book is NOT long-only.** Intraday SHORT strategies trade live: `first_pullback_short`,
`gap_go_short`, `gap_fade_short`, `vwap_rejection_short`. A **net-short broker position (qty < 0) is
EXPECTED**, not an anomaly and not necessarily an oversell. Instruction files sometimes assert
"long-only" — that premise is WRONG; verify against the source, which wins.

**Distinguish an open short from an OVERSELL by the broker's `buy_qty`/`sell_qty`** (`kite.positions().net`):
- open short = `buy_qty 0, sell_qty 1` (one sell, never covered) → net −1, correct/expected.
- oversell   = `buy_qty N, sell_qty N+1` (sold more than bought). The 19-Jun THELEELA oversell was
  BUY 1 → SELL 1 (emergency) → SELL 1 (HARD_KILL) → −1. [[orphan-adoption-forensics-22jul]]

**EOD squareoff is reverse-aware — it BUYs to cover a short, cannot take −1 → −2**
(`orders/eod_squareoff.py::_exit_open_positions`): `exit_side = "SELL" if direction == "LONG" else "BUY"`
(:1155); qty from broker truth `abs(int(p.qty))` (:1071); the E.5 broker filter keeps only
broker-nonzero symbols (:1090); the FIX-182 residual sweep derives side from the qty SIGN
(`_place_marketable_limit_exit:1509`). This is a DIFFERENT mechanism from the FIX-190
`determine_close_direction` sign-based helper (`broker/position_helpers.py`) used by the
HARD_KILL/emergency-exit paths — but both cover a short. `exit_protocol=LIMIT_THEN_MARKET`
(`system_config.yaml:239`): aggressive LIMIT, then MARKET after 120 s grace.

**Proven 24-Jul (SPANDANA):** broker `net −1, buy_qty 0, sell_qty 1, avg 269.90` = a normal open
`first_pullback_short` (entry SELL COMPLETE; SL BUY @273.60 TRIGGER PENDING + TGT BUY @263.50 OPEN, both
resting). NOT an oversell, NO defect — closes via TGT/SL, else EOD BUY-to-cover, else Zerodha MIS
auto-square ~15:20. See `docs/audit/spandana_net_short_24jul2026.md`.
