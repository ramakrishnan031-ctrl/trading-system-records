---
name: h5-killswitch-sweep-product-fixed-05jul
description: "Wave 2 H-5 FIXED — HARD_KILL broker-position sweep now product-aware (CNC→DELIVERY intent, not hardcoded INTRADAY that opened a naked MIS short). Group-A closes after e2e validation."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 2, H-5 — FIXED (commit `57dfbe2`, main, UNPUSHED).**

Root cause: the HARD_KILL broker-position sweep (`KillSwitch._exit_all_trades_indestructible`, the
FIX-181 LAYER A orphan sweep) hardcoded `intent="INTRADAY"` when flattening an orphan broker position.
Kite nets positions PER PRODUCT, so an orphan CNC position swept with an MIS exit does NOT offset it →
the CNC position stays AND a fresh naked MIS short is created. The first pass is product-aware (Bug C:
`_PRODUCT_TO_INTENT.get(product)`); the sweep reintroduced the hardcode.

Fix (mirror the first pass): read `product` from the Position payload (`getattr(pos,"product","")`,
present in both modes) → map via `core.constants.PRODUCT_TO_INTENT` (MIS→INTRADAY, CNC→DELIVERY,
NRML→DELIVERY, CO→COVER_ORDER) → pass that intent to place_order AND carry it in the failed_trades
entry (so the H-4 retry re-fires under the correct product). Absent product → INTRADAY. No refactor.

Parity: single shared sweep → one fix both modes (product mapping reads the payload, mode-agnostic);
no paper duplicate. H-12 is the qty-sign/DIRECTION axis (separate) — the sweep's direction still
derives from signed pqty (pre-existing), not touched here.

⚠️ Delivery-gate interaction (REPORTED, NOT fixed — H-6 territory): post-fix a CNC orphan is swept as
intent=DELIVERY, so the adapter's SLICE2.5-P1 lock (zerodha_adapter.py:535 — refuse CNC while
delivery_enabled=false) REFUSES the CNC exit while delivery is off. The sweep SURFACES it (CRITICAL
"SWEEP exit failed" → failed_trades → H-4 retry → `_alert_exit_failed` escalation), NOT swallowed; the
FIRST pass already behaves identically. So H-5 changes the failure mode from a SILENT naked MIS short
to a SURFACED+escalated refused CNC exit (strictly better); the un-flattened CNC while delivery-off is
a delivery-lifecycle issue for H-6.

Test: `tests/unit/test_h5_killswitch_sweep_product.py` (4) — drives the REAL sweep (no local trades →
first pass no-op → sweep runs) + a recording adapter returning one orphan position + recording the
intent (does NOT enforce the delivery gate — validates the intent CHOSEN per product). CNC→DELIVERY +
NRML→DELIVERY RED against the hardcode → GREEN; MIS→INTRADAY + absent→INTRADAY pass. kill_switch 56 pass.

**Group-A HARD_KILL: 977✓ H-4✓ H-5✓ — closes ONLY once the Group-A end-to-end VALIDATION passes (next).**
H-10 = Group B (after Group-A validation). H-12 (paper qty-sign) still blocks a paper drill of the
HARD_KILL direction (Wave 3). Deploy caveat: live post-receive = checkout only, no restart; inactive → next start.

Related: [[h4_killswitch_retry_rederive_fixed_05jul]] · [[p1_killswitch_dead_column_fixed_05jul]] · [[slice25_p1_cnc_gtt_25jun]] · [[full_repo_audit_04jul_pending]]
