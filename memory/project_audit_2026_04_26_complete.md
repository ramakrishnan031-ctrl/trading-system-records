---
name: 2026-04-26 full system audit complete (head 3276f9f, pushed to vm)
description: All 25 items disposed: 11 HIGH + 4 MED + 4 LOW shipped over 11 commits; 6 closed no-fix (TST-1, NM-1, NM-2, NM-3, ACC-1, GIT-1); schema v12->v13; 1775 green (1760 unit + 15 integration)
type: project
originSessionId: 10cbe4dd-821c-4e9d-a171-0348c2ce6014
---
**Source:** `docs/web_claude/03_audit_responses/full_system_audit_2026-04-26.md` (full pre-live audit; 0 CRITICAL, 11 HIGH, 6 MED, 8 LOW).

**Head:** `3276f9f` on `main`, pushed to `vm` remote (auto-checkout via post-receive hook). Origin not pushed yet (typical for this repo — vm is the operational target).

**Tests:** 1760 unit + 15 integration = 1775 full-suite collected (`pytest --co -q tests/`). +7 vs 1753 baseline (the +7 came from new tests added during HIGH-bucket fixes; both the MEDIUM commit at f67a0c7 and the LOW commit at 3276f9f are pure refactor/cosmetic with 0 test delta).

**Schema:** bumped v12 -> v13 in commit `1a2bca1` (CFG-7 + NSK-1 dropped 5 dead `session.*` columns).

**Why:** This was a fresh full-system audit by VS Code Claude on top of the 2026-04-25 supplemental audit, performed before paper Week 2. No CRITICAL items found — system was already in good shape post-25-Apr fixes. Audit focus was *namesake config* (P2 violations: YAML keys that exist but never get read) and DRY consolidation.

**How to apply:** When the user references "the 26-Apr audit", "CFG-1..CFG-7", "DUP-1/DUP-2", "LOG-1", "NSK-1", "EXC-1/EXC-2", "DEAD-1/DEAD-2", "REQ-1", "TST-1", "NM-1..NM-4", "CMT-1", "DOC-1", "ACC-1/ACC-2", or "GIT-1" — point at this entry plus the audit doc. **Audit fully closed** as of 2026-04-27.

**Items shipped (10 commits):**
- `5080a59` CFG-2 — delete namesake `polling:` block from system_config.yaml + PollingConfig from loader.
- `c2284ff` CFG-3 — delete namesake `order_fill_timeout` block; canonical is `order_monitor.fill_timeout_sec`.
- `d4f100a` CFG-4 + DEAD-1 + DEAD-2 — `enable_event_driven` flag removed; OrderStateChanged event class deleted; OSM no longer publishes; bus parameter dropped from OSM ctor; 4 OrderStateChanged-publishing tests rewritten as state-transition assertions (closes TST-1).
- `1a2bca1` CFG-7 + NSK-1 — schema v12->v13: dropped `session.kill_state` (CFG-7, dup of `kill_switch_state.state`) plus 4 dead session columns: `yesterday_pnl`, `yesterday_wins`, `yesterday_losses`, `consecutive_losses`.
- `2bdc1d6` EXC-1 + EXC-2 — state_store exceptions and StartupCheckFailed re-parented to `TradingSystemError` per E1-E6 hierarchy.
- `4b0f713` REQ-1 — `requests` pinned in requirements.txt.
- `ec818e6` CFG-1 — MarketWindows now reads entry_start/entry_end/eod_squareoff_time from system_config.yaml; YAML aligned to spec (09:30 / 13:30 / 15:17).
- `a7e97d2` CFG-5 — `MarketWindows.is_entry_allowed_for_strategy(now, strategy)` added; signal_processor enforces per-strategy windows on top of global.
- `9841029` CFG-6 — paper-mode slippage engine wired (P12 paper/live parity gap closed).
- `f67a0c7` 2026-04-27 — DUP-1 + DUP-2 + LOG-1 single MEDIUM bundle.
- `3276f9f` 2026-04-27 — CMT-1 + NM-4 + DOC-1 + ACC-2 single LOW bundle (cosmetic + minor hardening). schema.sql comment renumber gate_state TABLE 16->17; _apply_reserve(rid)->reservation_id for sibling-helper consistency; is_eod_squareoff_due docstring names 15:17 IST + CFG-1; AccountRow.totp_secret_env comment now explicit that v2 uses request_token OAuth (not TOTP).

**Items closed no-fix (6 total):**
- TST-1 (MED) — already closed-by-equiv inside `d4f100a` (DEAD-2 commit re-shaped the relevant tests).
- NM-1 (MED) — false-positive: all 15 strategy YAMLs already use the flat `pullback_wait_*` shape; `StrategyConfig.model_config = ConfigDict(extra="forbid")` already enforces the shape; the audit's "spot-check" claim of inconsistency did not survive verification.
- NM-2 (LOW) — auto-resolved by DEAD-2 (`d4f100a`): OrderStateChanged was deleted, so the OrderStateChanged/OrderStatusChanged naming collision no longer exists.
- NM-3 (LOW) — auto-resolved by DUP-1 (`f67a0c7`): all `_IST` declarations consolidated to `core.time_authority.ist_timezone()`; the `name="IST"`/no-name inconsistency is gone.
- ACC-1 (LOW) — `LFL836.paper_capital=1000000` (₹10L) is the operator's documented Week 2 paper capital per `project_paper_to_live_plan.md`; the audit's reference to ₹50k was based on the stale F.1 baseline (commit 316b335).
- GIT-1 (LOW) — audit was just noting `.gitignore` is already correct.

**DUP-1 file list (13 modules migrated to `core.time_authority.ist_timezone()`):**
alerts/critical.py, capital/kill_switch.py, capital/risk_engine.py, main.py, orders/order_reconciler.py, orders/shadow_tracker.py, orders/smart_tgt_manager.py, reports/daily_review.py, screening/entry_gate.py, scripts/alert_watcher.py, scripts/zerodha_login.py, signals/signal_processor.py, signals/webhook_receiver.py.
Exemptions kept: core/state_store.py (H-17 layering), core/time_authority.py (definer).

**DUP-1 bug found and fixed during landing:** `scripts/zerodha_login.py:72,145` had `datetime.now(_IST)` calls that would have crashed at import after the local `_IST` was deleted. The earlier in-progress diff added the `from core.time_authority import ist_timezone` import but missed the two call sites — corrected to `datetime.now(ist_timezone())` before commit.

**LOW bucket (deferred — bundle into a future cleanup PR):**
CMT-1 (schema.sql comment renumber), NM-2 (auto-resolved by DEAD-2; document only), plus 6 cosmetic items.

**Phase C from 24-Apr audit (still pending):** WAL cron (4.2), 5-min dedup bucket (6.3), smart-target intra-minute (5.3). Gate = paper Week 2 outcome — unchanged.

**Next session:** Paper Week 2 Day 1 began **today, Mon 27-Apr-2026** (Chaos Diet starts). systemd still disabled; PC + ngrok stays the execution path through Week 3. Live D-Day still targeted Mon 11-May-2026.
