---
name: b1_daily_loss_unrealized_mtm_impl_02jul
description: "B-1 BUILT (02-Jul, f5fd4d9, branch fix-b1-daily-loss-mtm-02jul off main, unpushed) — unrealized MTM wired into daily-loss gate, SHADOW default (zero behaviour change). Deploy-safe"
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Audit B-1 (HIGH) IMPLEMENTED 02-Jul per [[b1_daily_loss_unrealized_mtm_design_02jul]]. Branch **`fix-b1-daily-loss-mtm-02jul` @ `f5fd4d9`** (off `main`/9becf8c, ISOLATED, UNPUSHED). 11 files +513/−15. Design doc `docs/design/b1_daily_loss_unrealized_mtm_design_02jul2026.md` (committed on the c1 branch's docs commit, not on b1).

**What shipped:**
- `orders/order_reconciler._refresh_unrealized_mtm()` in the 15s cycle: batch `get_quote(open symbols)` → `unrealized=(ltp−entry_actual_price)×qty_filled×sign` per OPEN/PARTIAL → `fm.update_unrealized_mtm` → **SET-BASED prune** (`prune_unrealized_mtm(open_ids)` — removal for a close by ANY path, no per-close hook) → `mark_unrealized_mtm_refreshed(available)`. Never raises. `_mtm_refresh_success/failure` counters. Quote outage / no-usable-quote → `available=False`.
- `capital/fund_manager`: `mark_unrealized_mtm_refreshed`, `get_unrealized_mtm_status()→(total,is_fresh)` (fresh = available AND age ≤ `_MTM_STALE_AFTER_SEC`=45s), `prune_unrealized_mtm`. `_unrealized_mtm` stays a SEPARATE advisory dict — never touches reservations/_total/3-balance invariant (test-asserted). Added `import time`.
- `capital/risk_engine` DAILY_LOSS gate: reads `get_unrealized_mtm_status`; enforces realized+unrealized ONLY when `daily_loss_include_unrealized` flag ON **and** fresh; stale/unavailable→realized-only+WARN (`mtm_unavailable`); shadow logs `would_reject_with_unrealized`. Gate stays reject-only (no kill).
- `core/config_loader.RiskConfig.daily_loss_include_unrealized: bool=False` + `system_config.yaml risk.daily_loss_include_unrealized: false` (SHADOW DEFAULT) + `main.py` wiring.

**Parity:** ONE path — `get_quote` returns a real LTP in paper (paper_quote_provider) + live; compute mode-agnostic (test proves identical paper/live).

**Rollout:** SHADOW default = reconciler populates MTM + gate LOGS would_reject but ENFORCES realized-only → **ZERO behaviour change → deploy-safe anytime**. Flip `daily_loss_include_unrealized=true` to enforce (validate shadow logs first). Rollback = flip flag / revert `f5fd4d9`.

**Tests:** 4 fund_manager (freshness/prune/invariant) + 4 risk_engine (shadow/enforce/stale-fallback/realized-regression) + 6 reconciler (`test_b1_reconciler_mtm.py`: populate/set-prune/outage/no-quote/empty/parity) + 3 updated FIX-035 (now flag-on) + 3 mock updates (`get_unrealized_mtm_status` added to _MockFundManager in test_risk_engine/test_signal_processor/test_p0_live_day1). **Full unit suite: 4150 pass / 13 skip / 32 fail = the SAME 32 pre-existing Windows-env failures ([[pc_test_env_hygiene]]); ZERO new.**

**Deploy/branch:** b1 off main, isolated. Overlap with the A-2+C-1 stack (`fix-c1-completion-02jul`@3d34357) = **ONLY `tests/unit/test_signal_processor.py`** (b1 mock ~L233 vs A-2 tests ~L2176 — non-adjacent → clean auto-merge). All deploy-critical SOURCE files disjoint → effectively conflict-free; can push b1 independently OR merge with the stack. **SHADOW-safe so it can deploy before the 03-Jul boot gate.** Sequenced BEFORE P1 per [[audit_remediation_status_02jul]]. NOTE: the SYSTEM_MAP/PATHS b1 pointer (committed on c1 docs commit `3d34357`) still says "DESIGN" — update to IMPLEMENTED when convenient. Related: [[a2_timeout_retry_impl_02jul]], [[c1_secret_remediation_02jul]], [[dual_daily_loss_mechanism]].
