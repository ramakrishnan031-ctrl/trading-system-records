---
name: a1_e1_orphan_fix_design_02jul
description: A-1+E-1 naked-orphan fix — DESIGN+PLAN done (NO code); tag-correlation recovery; full doc in docs/design/
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e62fe89-aead-435f-8580-0a242667edcc
---

INVESTIGATE+DESIGN phase (NO code) of the most critical fix: audit A-1 (HIGH, timeout) + E-1 (MEDIUM, crash) — same root, found independently. Follows [[system_audit_02jul]]. **Full design + plan + test matrix: `docs/design/a1_e1_orphan_fix_design_02jul2026.md`.** Code lands in a SEPARATE pass after review.

**ROOT CAUSE (re-verified vs current source):** an ENTRY that reached the broker but whose local `orders` row never persisted (timeout `order_placer.py:1291-1323`, or crash between `execute()`:1203 and persist ~:1357) gets marked **FAILED + capital released WITHOUT confirming broker absence** (timeout: `order_reconciler._check_unknown_in_flight` :3053-3186 keys on `get_open_orders()`+`broker_order_id` we never have, and misses FILLED orders which are positions not open-orders; crash: `order_monitor._cleanup_orphaned_pending_trades` :336-391 marks FAILED with NO broker check at all) → the order later fills → `_check2_orphan_adoption` :1366 disowns it as **human → NAKED, no SL** until 15:17 EOD sweep. **Root enabler CONFIRMED:** the broker `tag`=`truncate_tag_for_broker(trade_id)` is written but NEVER read — `orders/` has zero `.get("tag")`; `zerodha_adapter` has no `"tag"` string → `get_open_orders()` DROPS the tag.

**KEY FACTS:** tag = `trd_`+first-12-hex (`tag[:16]`) = 48 bits → collision ~1.8e-11/day, negligible but NOT guaranteed → design fails-safe on multi-match. Adapter has get_open_orders/get_order_history(id)/get_positions but NO "all today's orders" and drops tag; positions carry NO tag (Kite) → correlate via ORDERS not positions. Entry+SL+TGT SHARE the tag → filter to the entry leg by side. Paper never times out (A-1 live-only); paper `_paper_fills` is in-memory → paper crash self-corrects (E-1 danger is LIVE).

**DESIGN (tag-correlation recovery):** (1) adapter NEW `get_all_orders()` surfaces the raw kite `tag` (live) + all `_paper_fills` incl. a NEW stored `tag` (paper parity); (2) reconciler `_correlate_entry_by_tag(trade, orders)` = recompute `truncate(trade_id)`, match tag+entry-side → 0=ABSENT/1=MATCH/>1=AMBIGUOUS(fallback symbol+side+qty+time → else CRITICAL manual); (3) ONE `_adopt_or_fail`: ABSENT+reachable→FAILED+release (only capital-release point, now evidence-based) / ABSENT+unreachable→DEFER (never release blind) / MATCH→backfill `orders` row + broker_order_id, OPEN→register-monitor, COMPLETE→place exits via existing guarded protocol (or FLATTEN if HARD_KILL, reuse CHECK9 FACET-2 oversell), REJECTED/CANCELLED→FAILED; (4) BOTH feeds (timeout UNKNOWN_IN_FLIGHT + crash orphaned-PENDING) go through the SAME path — `order_monitor` stops marking FAILED directly. Idempotent via atomic state-guarded transition (mirrors mark_trade_manually_closed). **RAMCOIND L1-L4 / CHECK9 / G5b PRESERVED** (adoption reuses the guarded exit protocol, never places exits directly). **NO schema change** (recompute truncate over the tiny recovery set; backfill broker_order_id).

**PARITY:** same recovery code both modes; live Kite = durable oracle, paper `_paper_fills` = oracle; tests seed `_paper_fills` with a tagged order + recovery-state trade → proves ONE path without a real broker.

**PLAN:** 5 ordered steps (adapter add → reconciler helpers → rewrite `_check_unknown_in_flight` → unify crash feed + stop order_monitor FAILED → wire startup+15min). Off-market deploy+restart (live order path). Rollback=revert. 12-row test matrix (timeout/crash→adopt not FAILED · human still flagged · HARD_KILL flatten · no-dup-adopt · no-release-pre-confirm · partial-fill · poll-fail-defer · collision · paper-parity · RAMCOIND/CHECK9/G5b intact).

**OBJECTIVES (all hold):** never call a system order human · never release before confirmed absence · never leave a filled position unmanaged · never duplicate adoption.

**NEXT:** Rama reviews the design → implementation pass (separate). NO code changed this pass; NO branch created.
