---
name: build2_config_sanity_auditor_25jun
description: "BUILD 2 Config Sanity Auditor — the enforcement capstone of the Config Authority arc; one rule engine, startup BLOCK gate + 09:20 pre-flight report"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2728af1d-58ce-49b8-8d98-20ad52e4e30f
---

**BUILD 2 (Config Sanity Auditor) — staged 25-Jun, branch `build2-config-sanity-auditor-25jun` (commit eb373c4), NOT yet deployed.** The enforcement capstone of the Config Authority work: BUILD 1 cleaned the config, BUILD 2 keeps it clean + surfaces violations. See [[build1_config_authority_fixes_24jun]].

**Architecture:** ONE rule engine `core/config_auditor.py` — `audit()` → `ConfigAuditReport` of per-group `AuditFinding`s (severity PASS/INFO/WARN/BLOCK). TWO callers (single source of truth, no rule lives twice):
- **STARTUP** — `core/config_loader.py` `SystemConfig._cross_field_sanity_checks` now delegates to `audit_system_config` (startup subset groups `ACG`), logs WARNs, and `raise_if_blocked()` fails fast on BLOCK. The BUILD 1 **#10** `force_intraday_only`+`trade_type=DELIVERY` contradiction is **re-homed here** (message still carries "CONTRADICTORY CONFIG" → `pytest.raises(ValidationError, match=...)` contract preserved). Boot-log unchanged.
- **PRE-FLIGHT** — new `scripts/preflight/checks/config_sanity.py`, 7 rows (A–G, group "Config Sanity") in **Phase A 08:30** → consolidated **09:20 email + Telegram**. ONE auditor run memoised on the shared `CheckContext` feeds all 7 rows (first row ~215ms builds it, rest 0ms cache hits).

**Check groups (each PASS/WARN/BLOCK):** A contradictions (BLOCK incl. #10 + A2 domain + A3 strategy-aware "0 would trade" WARN via `strategy_will_trade`) · B single-source regression guards (deleted key reappearing in **raw YAML** — `capital.daily_loss_limit`, `position_sizing.max_position_value_rs`, `risk.live_test_*`, scoring `tier_multipliers`; reads raw because `extra="forbid"` strips them from the model) · C capital-relative sanity (pct ranges + the **ladder `max_concentration_pct < max_position_value_pct`** so the catastrophe backstop stays looser than routine concentration + migrated cumulative-risk-vs-daily-loss) · D active-override listing (T3 visibility, reuses `orders.order_placer.validate_slippage_overrides`) · E launch-phase reminders (`[LAUNCH-PHASE]` tag registry; entry_start 10:00) · F stale-default guard (introspects `PositionSizer.max_position_value_pct`=0.40 / `FundManager.daily_loss_limit_pct`=0.03 ctor defaults vs config) · G cross-field (entry-window/leverage/min-tick + per-strategy-window-in-envelope).

**Validate + alert ONLY** — no trading-behaviour change beyond the pre-existing #10 boot gate. **Parity:** pure, no mode branch → paper+live identical (test-enforced). **No DB schema.** Tests `tests/unit/test_config_auditor.py` (37); full PC unit suite **3770 passed / 0 failed**. Docs: SYSTEM_MAP changelog 25-Jun + PATHS (auditor section) + CONFIG_GUIDE §10b. Surfaces in [[preflight_system_21jun]] Phase A; CONFIG_GUIDE is [[task_8_config_guide]].

**B6 (BUILD 1 live proof, same session):** clean — daily-loss = 3% × ₹10,011.30 opening cap (fm_ledger INIT) = ₹300.34; max-position cap = 40% × cap = ₹4,004.52 (looser than ₹1,001 concentration); #10 dormant; caps_config_drift PASS; 3 deleted keys absent; 0 POSITION_VALUE_CAP rejections; startup CRITICAL was the headless prior-day SOFT_KILL auto-clear (working as designed).

**Sample 09:20 section:** `Config Sanity (7/7 ok)` — A–F ✅, G ⚠️ (entry_end 15:15 within 15min of squareoff 15:17 — the lone, intended, long-standing warn).

**APPROVED 25-Jun** (Rama + ChatGPT review both cleared). Deploy authorized **post-15:30 close** (`git checkout main && git merge --ff-only build2-config-sanity-auditor-25jun && git push origin main`). NB the push only updates the VM working tree (no auto-restart) → the deploy window is wide (15:30 Thu → ~08:00 Fri); **Fri 08:15 restart activates it**; Fri 09:20 email carries the Config Sanity section. Expected: overall READY_WITH_WARNINGS (the 1 G WARN = pre-existing entry_end/squareoff proximity, already in the daily boot log, NOT new/critical). VM verify after deploy: Config Sanity group in Phase A→09:20 email+Telegram, 7 rows A–G, #10 still blocks the bad combo.

**Group D by-symbol pre-flight typo-check = DEFERRED (Rama's call).** Today all slippage overrides are EMPTY (pure global 0.22) so there's nothing to check; by-STRATEGY typos ARE caught in pre-flight, and by-SYMBOL typos are still caught at **main-startup** (`validate_slippage_overrides` runs there with the full instrument set) → **no gap**, just a pre-flight convenience. Wire `known_symbols` into `scripts/preflight/checks/config_sanity.py` `_build_report` ONLY in the session that introduces the first symbol override. See [[slippage_override_hierarchy_phase3a]].

**CONFIG AUTHORITY ARC COMPLETE** once BUILD 2 deploys + Fri proof: Phase-1 audit → Phase-2 audit → framework → Resolution Table (12) → [[build1_config_authority_fixes_24jun]] (B6-proven) → BUILD 2 (enforcement). **Next bucket (Rama's pick):** LONG strategy review (~13% long vs ~58% short), Slippage Phase 2 reports + daily_review.xlsx redesign, Slice 2.5 Delivery, VM Security hardening, deeper strategy/system analysis, Rama's diary points.
