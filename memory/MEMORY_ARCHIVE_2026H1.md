# Memory Archive — 2026 H1 (historical / superseded pointers)

Moved here from `MEMORY.md` on **06-Jul-2026 eve** to keep the active index lean. **No data loss** — every topic-file link is preserved, just relocated. Older pre-compaction index + the full note: [memory_index_archive_pre_compact_03jul](memory_index_archive_pre_compact_03jul.md).

> 🗄️ **25-Jul relocation (C6 build; from active `MEMORY.md`, VERBATIM — NO data loss; topic-file + wiki-links preserved). Superseded by the C6 DONE line, which links the build report:**
- 🔐🔎 **[C6 SCOPED 25-Jul](receiver_auth_c6_scoping_25jul.md)** — 2 routes; auth STATE already shared ⇒ only the CHECK is duplicated. ✅ PB-01 auth SAFE. 🔴 **Monday risk = boot wiring, not auth**: grep boot log for `"PB-01 watchlist: ENABLED"`. [[receiver-auth-c6-scoping-25jul]]

## 18–22-Jul closed items (relocated from the active `MEMORY.md` on the 23-Jul compaction — all DEPLOYED/PROVEN/DONE; NO data loss: each topic-file link + wiki-link is preserved verbatim here; detail in each topic file):
- ⭐🔬🔝 **[PHASE-2 P&L CARRYOVER — PROVEN IN PROD 21-Jul](phase2_carryover_proven_21jul.md)** — the forced 11:57 mid-session restart replayed real same-day state clean (`daily_pnl=-12.57, 3 rows, 0 anomalies`, `_total`=broker.net, **new E4/W10 contract**). Off the unproven list. [[phase2-carryover-proven-21jul]]
- 📊🔧✅ **[DAILY-REPORT CLASSIFICATION FIX — DEPLOYED 18-Jul `b3a960d`](daily_report_classification_fix_18jul.md)** — reporting-layer only. ⚠️ "3,098→0" = MISLABELLED not miscounted. ✅ routine `KILL_AUTO_CLEARED` mis-count **FIXED 21-Jul (C1, `5c70def`)**.
- ✅ **LOCKED-CONTRACT sweep DONE 22-Jul** `locked_contract_staleness_sweep_22jul2026.md` — **7 stale / 2 clusters** (order-placement two-phase: OP-NS4/5/BL19d/LM3; kill-switch adapter: KS5/11/13), all capital-safety path, corrected+pushed. Pattern: locked ⇒ not re-read.

> 🗄️ **24-Jul relocation (§F of the fixation batch; from active `MEMORY.md`, VERBATIM — NO data loss; topic-file + wiki-links preserved). Each is genuinely superseded (by a later entry or by subsequent proven boots):**
- ✅🟢🔝 **[MONDAY 20-Jul — BOOT + POST-SESSION CLEAN](monday_post_session_clean_20jul.md)** — S4 class did NOT recur; liveness probe proven in prod; fwd shadow SOUND (**OOS 3→4**). **Worst intraday −Rs 18.29**; invariant holds **excl. `RESET_PNL`** (the "−17"/"−18.29" gap = gross-vs-net). [[monday-first-real-boot-proven-20jul]]
- ✅💰 **[E4+W10 — the RESET double-subtract · ✅ DEPLOYED 20-Jul `a266432`](e4_w10_done_17jul.md)** — v44, no migration; **impact Rs 1.32, N=0 outcomes** (charges 7.8% of gross). [[e4-w10-outcome-impact-19jul]]

> 🗄️ **24-Jul relocation (2nd pass — memory compaction; from active `MEMORY.md`, VERBATIM — NO data loss; topic-file + wiki-links preserved). Concluded investigations, superseded as 'current':**
- 🕳️✅🔝 **[403 "BLIND SPOT" CLOSED — refusals ALL correct, NO build (23-Jul)](403_blind_spot_investigation_23jul.md)** — every POST already audited in `webhook_audit`; ~46% of hist. 403s were IN-WINDOW **kill-switch** refusals (June debris, none since 1-Jul), NOT "outside window"; 0×401 + 1 Chartink IP ⇒ no noise. [[signal-mortality-census-19jul]]
- 📦📨 **BACKUP+TELEGRAM addendum (22-Jul)** — backup_retention nightly-abort BENIGN: `--max-delete`=abort-cap NOT delete-count, anchors safe, 72G free. Telegram `<TELEGRAM_CHANNEL_ID_REDACTED>`=SOLE channel (no SECONDARY), 16-22 Jun outage FIXED; standing=**no redundancy**. Doc+`51bc96f`.
- 🩹 **ORPHAN §3 (22-Jul `orphan_adoption_22jul2026.md`, pushed)** — Zerodha system-only ⇒ 'untracked'≠human: a lost SYSTEM pos mislabeled 'human/not-managed'. **Census 4d 15-25 Jun, NONE since.** RAMCOIND=oversell; THELEELA RESOLVED→forensics.
- 🔪 **ORPHAN ROOT (`orphan_adoption_forensics_22jul2026.md`, 22-Jul pushed)** — June orphans = debris of `_place_limit_triple_exits` REJECTED after entry -> unprotected -> **HARD_KILL** -> flatten-oversell. 3x 15/16/19-Jun; **0 recur = LATENT**. FIX-181/182 fixed classify, not root.
- 🧵 **ORPHAN THREADS 1+2 CLOSED** `exit_rejection_hard_kill_forensics_22jul2026.md` — T1: 3 variants **actively prevented**; **HARD_KILL D7 SETTLED: halt STAYS, OP-NS5→anomaly-breaker not naked-pos.** Tail: novel reject→kill (LATENT). **T2 (~5× orphans) = UNDETERMINED, predate the DB.**

## Build History (git log is authoritative; these are decision context)
- [Design Spec Authority](project_v2_spec.md) — docs/v2_design_spec.md + docs/locked_decisions.yaml
- [Module builds through main.py lock](project_main_module.md) · [Phases A-E+F.1](project_phase_e_complete.md) · [Audits consolidated](audit_closeout_final.md)
- [FIX-122→155](project_fix154_complete.md) · [FIX-157](fix_157_check9_closed_manual.md) · [FIX-158](fix_158_antigravity_audit.md) · [FIX-159](ct_day5_complete.md) · [FIX-160 AGY cascade](fix_160_agy_cascade.md)
- [Day-6 retests](ct_day6_retests.md) · [FIX-165 deep audit](fix_165_deep_audit.md) · [FIX-166 P1s](fix_166_complete.md) · [35 findings fixed FIX-165→169](weekend_audit_complete.md)
- [Live trading readiness certified 15-Jun](live_trading_readiness.md) — Rs 10k; LFL836; live from Mon 16-Jun

### 17-Jul Operations (relocated from the active index 17-Jul eve — all DEPLOYED/superseded by the
later 17-Jul work: the S4 boot fix + P3-s14 (`deploy-17jul-s4-p3s14`) and the liveness alarm
(`deploy-17jul-liveness`). No data loss — every topic-file link preserved here. Detail in each topic file):
- ✅🚀🔝🏁 **[BATCH-3 DEPLOYED 17-Jul — `2fa08a77`, tag→`65cd7df`; PC==origin==VM. ⭐ THE BATCH-SAFE PILE IS NOW EMPTY](batch3_done_17jul.md)** — X7 exec-log join · X5 instance lock now OS-owned · **X3 DEFERRED**. **⭐ 2 of 3 ticket premises were wrong.** [[batch3-done-17jul]]
- ✅🚀🔝 **[S1+S3+S5 DEPLOYED 17-Jul — tag `deploy-17jul-s1s3s5`](s1s3s5_done_17jul.md)** — S1 `market_day_only` at the cron entry 30/30 · S3 login THROTTLE replaces the lockout · S5 benign functional set settled. **⭐ 3 instruction premises were WRONG** — incl. **the FIX being riskier than the bug**. [[s1s3s5-done-17jul]]
- ✅🚀🔒🔝 **[17-Jul SWEEP + BATCH-2 DEPLOYED — PC==VM==bare==`b2d7b2b`; the token PURGE is DONE](sweep_done_17jul.md)** — **19 files shredded ⇒ 0 live-token hits outside `.env`.** S2/S4/S6/S7 shipped. **⛔ S1/S3/S5 escalated — the obvious fix was WORSE than the bug.** **🔴 RAMA OWES: ROTATE `@Trade_sysbot`.** [[sweep-done-17jul]]
- 🔎✅ **[P3-s14 INVESTIGATED 17-Jul (read-only)](p3s14_investigation_17jul.md)** — **STEER: the dedup claim is SEPARATE, not transactional** ⇒ the fix MUST explicitly release. **⚠️ THE TRAP: releasing alone is NOT enough** — pair it with a retryable 5xx. **✅ 0×500 in 89,794 POSTs.**
> 🗄️ **16-Jul Operations relocated 17-Jul — the 13 topic links live in [archive_index_16jul_operations](archive_index_16jul_operations.md)** (all DEPLOYED/superseded by `b2d7b2b`; every link preserved). **⚠️ the FIRST LIVE HARD_KILL is still M-C8's real test.**

> 🗄️ **V3 SHARED-ENGINE Steps 1-10b — ALL BUILT + DEPLOYED** (11–13-Jul, live under `277d63e`: shadow×2 + PB-01 fail-closed). The step-by-step links live in [archive_index_v3_shared_engine_steps](archive_index_v3_shared_engine_steps.md). ≥5 soak sessions before any enforce.

## Recent Operations — 12-Jul and earlier (completed/superseded; live items remain in MEMORY.md)
> Relocated from active index 08-Jul + 12-Jul (compaction). Full detail in each topic file.

### 16-Jul Operations (relocated from the active index 16-Jul eve; F1 + alert-watcher MERGED into the consolidation, tag `deploy-16jul-alertwatcher-f1`→`1d5337d`. Detail in each topic file and in [archive_index_16jul_operations](archive_index_16jul_operations.md)):
- 🏦🟡🔝 **[16-Jul F1 — populate trades.sector at INSERT + gate-8 observe mode (register blocker B1)](f1_trades_sector_16jul.md)** — root cause: `trades.sector` NULL ⇒ the 40% sector cap never summed the resting book. Populate + observe SHIP TOGETHER, so deploy is behaviour-neutral. **⏰ observe soak ≥1 session → EXPLICIT-approval enforce flip.** [[f1-trades-sector-16jul]]
- 🔧🟡🔝 **[16-Jul ALERT-WATCHER `--loop` FIX — BUILT+TESTED LOCAL, UNPUSHED (deploy OFF-MARKET)](alertwatcher_loop_fix_16jul.md)** — `--once`+`Restart=always` ⇒ **101,570+ respawns**. Unit → the existing `--loop` daemon. ⭐ The monitor could call a respawning service HEALTHY ⇒ a **5th canary path `respawn`**. [[unpushed-pending-deploy-ledger]]
- ⏸️🟢🔝 **[16-Jul MORNING VERIFY + PLANNED-PAUSE SOFT_KILL — system HALTED; deploy verified clean on first live boot](morning_verify_16jul.md)** — 3 trades, book verified FLAT **at the broker**. **KEY: no live halt/flatten API — an active kill at boot HALTS the service (down), NOT running-but-halted.** **DB status LAGS broker truth.** [[deploy-done-16jul]]
- ✅🔀🟢 **[15-Jul COMBINED-DEPLOY — DEPLOYED 16-Jul (VM==bare==`c9fb298`)](deploy_done_16jul.md)** — F0 SMTP restored + Phase-B prune done; the tag is the rollback anchor. The STOP blocker was resolved **test-only** after an approved compat audit.

### 15-Jul Operations (relocated from active index 16-Jul — ALL superseded by the 15-Jul COMBINED DEPLOY, now LIVE `c9fb298`; their ⏰ owed items are done/captured in the register+ledger):
- 🛡️🔧 **[15-Jul MONITORING HARDENING BUILT (branch, UNPUSHED)](monitoring_hardening_15jul.md)** — closes the two silent-failure classes: F1 no-crash-loop + TELEGRAM FALLBACK · F2 EXECUTION vs FUNCTIONAL status · F3 · F4 · a 4-path CANARY.
- 🩺🔴🟢 **[15-Jul WHOLE-SYSTEM HEALTH AUDIT (read-only, 16 subsystems)](system_health_audit_15jul.md)** — **A) TRADING = PASS.** **B) MONITORING TRUTH = FAIL: SMTP EMAIL DEAD** ⇒ 8/8 critical sentinels UNDELIVERED while heartbeats say SUCCESS.
- 🛠️✅ **[15-Jul THREE FIXES BUILT + backup-validated (branch, UNPUSHED)](fixes_15jul.md)** — eod_cleanup FK-safe prune · read-only screened-csv connect · `fm_ledger` `id`→`ledger_id`. **Validated on a live COPY: 108,243 pruned, FK clean, trades untouched.**
- 🔬🧩 **[15-Jul FOLLOW-UP INVESTIGATION BUNDLE (read-only; fixed nothing)](followup_investigation_15jul.md)** — 6 items evidence-anchored. **🔴 eod_cleanup FK ROOT CAUSE found; M-K3 REFUTED.** **🟠 RE-GRADE M-SC2 CLOSED→PARTIAL.**
- 🟢🔬 **[15-Jul SUPERVISED SESSION-1 day reconstruction (read-only)](day_reconstruction_15jul.md)** — **A: SESSION RAN CLEAN, BOOK FLAT, PREDICTION HELD.** VM is PC-independent. **M-S5 tripped the watch but is IN-BASELINE ⇒ recalibrate, not revert.**

### V3 shared-engine BUILD chain (Steps 1-9, 11–12-Jul) — all DEPLOYED `c1ad82e` 12-Jul (shadow×2); live state = deploy ledger + [[v3_shadow_deploy_soak_12jul]]. Per-step detail in topic files:
- 🧭🛠️🧮 **[Step 6b — 03.05 Portfolio Allocator IMPLEMENTED default-OFF](v3_step6b_portfolio_allocator_impl_12jul.md)** — one-seam ADMIT extraction, NEW `allocation/` pkg; OFF byte-identical; tests(25). [[v3_step6_portfolio_allocator_plan_12jul]]
- 🧭🔎💰 **[Step 5 — 03.06 Risk & Sizing VERIFY + inert delivery scaffold](v3_step5_risk_sizing_12jul.md)** — only change = INERT delivery-sizing scaffold (default None→byte-identical); SL-distance seam=`sl_price` param; T5 flags (kill_switch/sector fail-open, ATR→live-SL).
- 🧭✅⚖️ **[Step 4b BINDING PARITY 114,807 rows PARITY_OK](v3_step4b_parity_artifact_12jul.md)** — @50/56/75 UNCHANGED 99.90% · 0 UNEXPLAINED. [[v3_step4b_hardgate_scorer_impl_11jul]] · [[v3_step4_hardgate_scorer_plan_11jul]]
- 🧭🛠️ **V3 Steps 1–3 + Phase-0 — all default-OFF/unwired; the four links live in [archive_index_v3_steps_1_3](archive_index_v3_steps_1_3.md)**: Market Regime (SHADOW, NIFTY 256265) · S&R ADAPT · candle_math ATR/resample · the Phase-0 gap analysis.
- 🧭✅🔒 Steps 7/8/9 (Entry/Trade-Mgmt/Exit) = VERIFY-only, 0 code — see the deploy line + Step-9 capstone in MEMORY.md active. [[v3_step7_entry_engine_12jul]] · [[v3_step8_trade_mgmt_12jul]] · [[v3_step9_exit_engine_12jul]].

### 09–10-Jul cluster (deployed):
- ✅🧭🚀 **[trade_type/intent Option A `8116b74` — PUSHED 10-Jul](trade_type_intent_segregation_investigation_10jul.md)** — declared-intent segregation, 3 positional_* DELIVERY dormant (12 WILL/3 WON'T); MIS-only double-locked. Loads Monday 08:15 (with `c1ad82e`+`61ae9cc`).
- ✅✅ **[Wave-6 + P1-SHADOW v42 runtime verification — BOTH PASSED 10-Jul](wave6_p1_runtime_verification_10jul.md)** — schema42 clean, 0 CapitalDrift; do NOT flip P1 authoritative (1 cycle).
- ✅ **[Risk-config `61ae9cc` — PUSHED 10-Jul, loads Monday](risk_config_tighten_10jul.md)** — min_pass_score 55→60 + max_consecutive_losses 5→4.
- 🎨 GUI **Screens 01–03 deployed 09–10-Jul — the three links live in [archive_index_gui_screens_jul](archive_index_gui_screens_jul.md)**: Control Tower `ab14650` · Mission Control →FROZEN `b7d72c7` · login hero `e0b26b7`. Next GUI = Screen-04 Signals.
- ✅🏁🧮🚀 **Wave-6 capital+flatten cluster — BUILT 09-Jul + DEPLOYED `d6e3302` off-market** (M-O2 · M-C7 · M-C3; M-O1 already-fixed, dropped). 450 pass / 0 false-fire; runtime-verified 10-Jul. Links: [archive_index_wave6_09jul](archive_index_wave6_09jul.md).
- ✅🛡️🟢 **[PUSH-1 runtime VALIDATED = PASS (09-Jul ~10:12 IST, live)](push1_runtime_validation_09jul.md)** — infra C-3/C-4/F-1/E-4 + A-3 first in-window runtime all clean (service active · schema 41 · `/health` daemon-gating · token 0600 · A-3 0-firings).
- ✅🚀 **08-Jul DEPLOYED cluster — all live; the seven topic links live in [archive_index_08jul_deploy_cluster](archive_index_08jul_deploy_cluster.md)**: PUSH-1 PC=VM sync `9bcc1eb` · A-3 entry-kill TOCTOU · infra C-3/C-4/F-1/E-4 · schema fail-fast · GUI login · P1 → SHADOW `f135fee`.
- 🔎 **Fresh post-remediation audit (08-Jul, `005c007`) — regression-clean, 0 new bugs; set the Wave-6 scope (COMPLETE + deployed).** ELEVATED logged: schema silent-downgrade (fixed by fail-fast) + backups-same-disk DR. [[fresh_audit_postremediation_08jul]]
- ✅🏁🚀 **Wave-5 RUNTIME-VALIDATED — FULL PASS (08-Jul, `271d24f`)** — H-7 cap 5×/held 2-2 · FIX-067 fresh-LTP SL confirmed live · terminal-guard silent · 0 halt/naked/oversell/CAPITAL_DRIFT. 🏁 Wave-5 closed+deployed+verified. [[wave5_runtime_validated_08jul]]
- ✅🏁 **Wave-5 (H-7 · FIX-067/M-S1 · terminal-guard+D-1 · M-C1) BUILT 07-Jul + deployed `271d24f` + RUNTIME-VALIDATED 08-Jul** — links in [archive_index_wave5_07jul](archive_index_wave5_07jul.md). All 13 Audit-A HIGHs addressed; H-6 CNC dead-column remains (delivery-gated).
- ✅ [Full-repo audit 04-Jul](full_repo_audit_04jul_pending.md) — 0 CRIT/13 HIGH/47 MED; theme = dead safety nets (Wave-1/2/3/5 fixed H-1..H-13 **except H-6 CNC dead-column, delivery-gated**); A-3 = entry-kill-TOCTOU [[a3_kill_recheck_investigation_08jul]].
- ✅ **Wave-3 dead-safety-net fixes COMPLETE (06-Jul)** — H-12 signed paper positions · H-13 TokenMonitor relatch · H-11 _invalidate_token path · H-8 ShadowTracker strategy col · H-9 candle off-by-one. Links: [archive_index_wave3_06jul](archive_index_wave3_06jul.md).
- ✅🚀 [Wave-3 + config-55 RUNTIME-CONFIRMED → CLOSED (07-Jul 08:15)](wave3_config55_runtime_closure_07jul.md) — v41 scrubbed DB clean, config-55 in effect, kill-switch new-day auto-cleared; last secret artifact shredded (PC=VM `9709a46`)
- ✅ [Mon 06-Jul session validation (read-only)](monday_validation_06jul.md) — clean-base PASS (0 naked/oversell/CHECK9/HARD_KILL); 2 non-blocking notes (G3 CAPITAL_DRIFT ×2 transient · B-1 shadow DEBUG-hidden)
- ✅ [min-score floor 60→55 all strategies LIVE 06-Jul](min_score_floor_55_06jul.md) `8a3e0b7` — single key `scoring_weights.yaml min_pass_score`; supersedes [[min_score_floor_60_26jun]]
- ✅ [S-1B.2 history scrub COMPLETE (06-Jul)](s1b2_history_scrub_06jul.md) — LIVE scrub 95,431 rows→token=0; shred 21 secret DBs; S-1B COMPLETE
- ✅ [S-1A webhook allowlist CLOSED (06-Jul)](s1a_webhook_allowlist_rotation_05jul.md) — Mon 86×200/0×401 from `23.106.53.213`; /32 allowlist+new-token+redact live; TLS deferred
- ✅ [S-1B.1 redact webhook secret (05-Jul `58ff1e7`)](s1b1_webhook_payload_redaction_05jul.md) · 🔎 [S-1 verify+leak](s1_webhook_verification_05jul.md) · 🔍 [Audit-B Ph9+10 NO IOC](audit_phase9_10_ops_security_05jul.md) (O-5 no off-site backup)
- ✅ **Wave 0-2 (05-Jul)** — H-10 place() None-backstop `ee9f993` · Group-A HARD_KILL (P1/H-4/H-5) · Wave 1 emergency-exit chain (H-1/H-2/H-3/M-O1) · Wave 0a watchers HEALTHY. Links: [archive_index_wave0_2_05jul](archive_index_wave0_2_05jul.md).
- ✅ [Wave-4 eod_verify HONEST-FIX (07-Jul `eb75731`)](eod_verify_honest_fix_07jul.md) — real P&L columns + honest PENDING/N/A/VERIFIED/ISSUES; false-VERIFY facade closed; 176 green
- ⤴️SUPERSEDED [Wave-4 P1 INTEGRATION validated — branch `wave4-p1` (07-Jul)](p1_wave4_integration_validated_07jul.md) — replaced by wave4-p1-v2 → [[p1_reintegrated_271d24f_08jul]]; discard (stale base eb75731)
- 🔎 [Wave-4 P1 eod_broker_reconcile INVESTIGATION (06-Jul)](p1_eod_broker_reconcile_wave4_investigation_06jul.md) — SHADOW feeder design=GO-quality; re-integrated 08-Jul → [[p1_reintegrated_271d24f_08jul]]
- 🚀 [G5 GUI redesign DEPLOYED (04-Jul)](gui_g5e_executed_04jul.md) — merge `b4aea6f`, live https://trading-system.tail1cdc6d.ts.net (tailnet-only), rollback→`80be23a`
- ✅ [Telegram token shadow FIXED (03-Jul)](telegram_token_shadow_FIXED_03jul.md) — deleted `telegram.conf` drop-in → `.env` single bot-token source; Mon-open: confirm alert
- 🌐 [E3 Tailscale LIVE + E4 reboot PASS (03-Jul)](gui_g2c_tailscale_live_reboot_03jul.md) — **https://trading-system.tail1cdc6d.ts.net** (tailnet-only); Rama PC/phone login pending
- 📘 [Strategy add/delete/rename guide (03-Jul)](strategy_change_deps_03jul.md) — 3 config files + Chartink sync; de-synced rename fails at RUNTIME
- ✅ [EOD System Manager alerts (03-Jul)](eod_alert_enh_03jul.md) — P&L gross-vs-net OK; email always sent; 15-strategy roster
- ✅ SSH alerts (03-Jul): [full-details](ssh_alert_full_details_03jul.md) (security.yaml sudo_whitelist OVERRIDES code) · [GeoIP](ssh_alert_geoip_03jul.md) · [over-limit per-IP](ssh_session_alert_03jul.md)
- ✅ [GUI readiness + G3.0 facts (03-Jul)](gui_readiness_g3_0_03jul.md) — kill-switch in-memory sole authority; controls = no backend module
- 📐 [T2 repair spec](t2_full_repair_scope_03jul.md) (3 drifts) · ✅ [boot verify 10 PASS](boot_verify_03jul.md) · 📐 [low-sev verdicts](audit_lowsev_verify_03jul.md) (C-3/C-4/F-1/E-4/A-3=FIX)
- 📐 [D-1 close_trade race](d1_close_trade_race_design_03jul.md) atomic-close after soak · 📐 [B-2 unrealized soft-kill](b1_unrealized_mtm_design_03jul.md) W10-bundled
- ✅ [P1 EOD broker-reconcile BUILT (unpushed SHADOW)](p1_eod_broker_reconcile_impl_02jul.md) — v42 pure-add · [design](p1_eod_broker_reconcile_build_design_02jul.md) · [assessment](p1_eod_broker_sync_assessment_02jul.md)
- ✅ [B-1 BUILT SHADOW](b1_daily_loss_unrealized_mtm_impl_02jul.md) — 15s MTM refresh, deployed 03-Jul · [design](b1_daily_loss_unrealized_mtm_design_02jul.md) · 🗺️ [audit remediation](audit_remediation_status_02jul.md)
- ✅ [A-2 BUILT (fd09a38)](a2_timeout_retry_impl_02jul.md) — BrokerTimeoutError→no-retry; deployed · [design](a2_timeout_retry_design_02jul.md)
- ✅ [Post-rotation creds + security (02-Jul 9becf8c)](post_rotation_creds_02jul.md) — 6 rotated · [security audit](ref_security_audit_02jul.md)
- ✅ [A-1/E-1 orphan-fix COMPLETE 9becf8c](a1_e1_orphan_fix_impl_02jul.md) · [design](a1_e1_orphan_fix_design_02jul.md) — live-verified 03-Jul
- 🔒 [C-2 webhook lockdown Ph2](c2_webhook_lockdown_02jul.md) — Ph3(bind/TLS/HMAC)=Rama · 🔒 [C-1 secret remediation](c1_secret_remediation_02jul.md) — history-purge NOT run
- ✅ [P0 emergency-exit tag bug 9ed8bbb](t2_halt_investigation_reconciler_tag_bug_01jul.md) · ✅ [CHECK9 race-aware f6de000](check9_race_aware_fix_01jul.md) · ⚠️ [get_daily_realized=W10→B-2](get_daily_realized_pnl_double_cost_01jul.md)
- 🆕 **Report sheets (01-Jul, live via Phase C)** — Orders · Dashboard · Slippage · Strategies · Config · snapshots · the Ph0 audit. The seven links live in [archive_index_report_sheets_01jul](archive_index_report_sheets_01jul.md).
- ✅ 30-Jun consolidated push a6ed070 — sr_detector_backfill cron + MIS blocklist (dormant) + T2 docs + [exit-alert sign fix](exit_alert_sign_fix_30jun.md)
- [MIS learned blocklist dormant](mis_learned_blocklist_30jun.md) · [sr_detector_backfill cron wired](sr_detector_backfill_cron_wired_30jun.md)
- [Control Tower Phase 1 deployed 29-Jun](control_tower_phase1a_29jun.md) — read-only ops aggregator, 17:05 Mon-Fri
- [Telegram alert direction/EOD split 29-Jun](telegram_alert_enhancements_29jun.md) · [T5 entry_end 15:00](t5_entry_end_investigation_29jun.md) · [T3 scanners not-worth-it](t3_weekly_scanners_investigation_29jun.md)
- [T2 backup retention keep-N](t2_backup_retention_investigation_29jun.md) · [T1 disk metric shutil](t1_disk_metric_investigation_29jun.md) · [T4 timezone tools + deploy_preflight](t4_timezone_investigation_29jun.md)
- [SSH key re-baseline 28-Jun](ssh_key_rebaseline_28jun.md) · [29-Jun schedule](monday_29jun_schedule.md) · [MFE/MAE empty root cause](mfe_mae_excursions_empty_28jun.md)
- [SNR-V2 Phase B](snr_v2_phaseB_27jun.md) · [Phase A](snr_v2_phaseA_27jun.md) · [SNR-V1 detector](snr_detector_v1_27jun.md) — staged, default-off
- [DDPI enabled on LFL836 26-Jun](ddpi_enabled_26jun.md) — headless delivery sells, no TPIN
- **Slice 2.5, June** — Phase-4 trade_type gate · Phase-3 delivery caps + conditional capital · FIX-183 GTT adoption · P2 `gtt_state` v36 · P1 CNC GTT · min_score floor 60 (superseded by 55). Links: [archive_index_slice25_jun](archive_index_slice25_jun.md).
- [RAMCOIND duplicate-SL fix](ramcoind_duplicate_sl_incident_25jun.md) · [BUILD 2 config auditor](build2_config_sanity_auditor_25jun.md) · [BUILD 1 config authority](build1_config_authority_fixes_24jun.md) · [Hygiene pack](hygiene_pack_24jun.md)
- [Slice 2 strategy control](slice2_strategy_control_24jun.md) · [R:R 1.5 all strategies](part_c_rr_standardized_1.5_24jun.md) · [Governor severity fix](governor_severity_briefing_debounce_24jun.md) · [After-check fix](aftercheck_circuit_cap_fix_24jun.md)
- [tgt_retry crash-loop post-mortem](tgt_retry_crashloop_postmortem_24jun.md) · [Cron Officer email-leak fix](cron_officer_email_leak_fix_24jun.md) · [Test sentinel isolation](test_sentinel_isolation_24jun.md)
- **23-Jun items** — EPACK timeout misread · cron HB false-alarms · gemini_log_review windowing · tick-snap fail-safe · cron framework armed · FIX-191 false SOFT_KILL. Links: [archive_index_23jun](archive_index_23jun.md).
- [SATS triage 22-Jun](sats_triage_22jun.md) · [Slice 1 R:R fix v35](slice1_rr_fix_deployed_22jun.md) · [FnO ban endpoint](fno_ban_endpoint_fix_22jun.md) · [Diary #4 tier multiplier](diary_4_tier_multiplier_switch_21jun.md)
- [Preflight system 55 checks](preflight_system_21jun.md) · [Instruments staleness incident](instruments_staleness_incident_21jun.md) · [Cron Officer revision](cron_officer_revision_20jun.md)
- [Slippage Phase 3a overrides v32](slippage_override_hierarchy_phase3a.md) · [Phase 1 raw layer v31](slippage_intelligence_phase1.md) · [Calibration data](slippage_calibration_data_20jun.md) · [Entry-slippage abort sl_fraction](tiered_slippage_abort.md)
- [SOFT_KILL headless auto-clear](softkill_investigation_20jun.md) · [VM security Phases 2+3 copy-gate](vm_security_phase2.md) · [Phase 1 monitor](vm_security_phase1.md) · [Pre-build audit](vm_security_audit_19jun.md)
- [Gemini/AGY auth non-issue](gemini_agy_auth_check.md) · [Cron env-export fix](cron_env_export_fix.md) · [EOD investigation 19-Jun](eod_investigation_19jun.md) · [CONFIG_GUIDE](task_8_config_guide.md)
- [Entry throttle](bug_g_entry_throttle.md) · [TGT retry v30](tgt_retry_mechanism.md) · [Daily-cap race fix](bug_b_daily_cap_race.md) · [live_test_mode superseded](live_test_mode_permanent.md) · [System Manager EOD](task_5_system_manager.md)
- [Reconciler EXITING auto-resolve](followup_reconciler_exiting_gap.md) · [FIX-190 incident resolved](fix_190_incident.md) · [19-Jun EOD verify](pending_eod_cron_verify_19jun.md) · [Sentinel cleanup](may31_sentinel_cleanup_19jun.md) · [FIX-189 dash-cron](fix_189_dash_cron_overnight.md)
- **18-Jun items** — SMTP alert-watcher · EOD 18-Jun cleanup · SYSTEM_MAP created · FIX-186 orphan leak · reconciliation / capital-sizing / cron-monitoring audits. Links: [archive_index_18jun](archive_index_18jun.md).
- **18-Jun headless items** — FIX-187 headless TOTP · Cron Officer · headless autostart audit · FIX-188 · TASK-11 drift interval · TASK-10 telegram switch. Links: [archive_index_18jun_headless](archive_index_18jun_headless.md).
- **FIX-183/184/185 + the Kite IP allowlist dependency** — ⚠️ **MUST update the Kite console on any IP change.** Links: [archive_index_fix185_187_jun](archive_index_fix185_187_jun.md).
- [FIX-182 EOD squareoff](fix_182_complete.md) · [Human order policy](human_order_policy.md) — system never adopts human Kite orders · [Deploy requires restart](deploy_requires_restart.md) — code in git ≠ code running
- [FIX-181](fix_181_complete.md) · [Concentration cap decision](config_change_needed_concentration.md) · [FIX-180](fix_180_complete.md) · [Weekend cron protection](weekend_cron_protection.md) · [Live Day-1 zombie remediation](live_day1_zombie_remediation.md)
- [FIX-162 AGY automation](fix_162_complete.md) · [AGY status](agy_automation_status.md) · [CT159 gold standard + paper authorized](ct_day6_complete.md) · [Paper from 12-Jun](project_paper_trading_authorized.md)

## Crash Tests (Jun-2026, all complete — full detail in `ct_*.md` files)
- **Crash tests — Days 0–5 + the P0 findings** (capital drift · CHECK9 cascade · AGY CT151-153 · OPEN→OPEN). Every day report and finding link lives in [archive_index_crash_tests](archive_index_crash_tests.md).

## Recent Operations relocated from the active index (13–14 Jul, archived 15-Jul — links preserved)
- [PB-01 SHADOW deploy + 2 findings (14-Jul)](pb01_shadow_deploy_14jul.md) — DEPLOYED `277d63e` (Q4+Q5+P11 + PB-01 flip, off-market); FINDING-1 `trades.sector` NULL → 40% sector cap dead → D1 blocked; FINDING-2 112 sim innings. [[pb01-shadow-deploy-14jul]]
- **[PENDING-LIST RECONCILIATION vs HEAD (14-Jul, read-only)](pending_reconciliation_14jul.md)** — pending source-of-truth; CLOSED ~24 / OPEN ~69 / PARTIAL 7. M-S4 PARTIAL (live bug `secondary_screener.py:407`). [[pending-reconciliation-14jul]]
- **[Q8 VM SECURITY — NO BREACH (14-Jul, read-only)](q8_vm_security_forensics_14jul.md)** — creds not exposed; the only foreign IP was a defeated bot. ⛔ never add an 18:00-08:00 SSH lock. [[q8-vm-security-forensics-14jul]]
- [Q5 Wave-7 audit backlog (14-Jul)](q5_wave7_backlog_14jul.md) — branch `q5-audit-backlog-14jul` (31 commits, deployed under 277d63e); 7 cheap report-path fixes + triaged remainder.
- [Q4 capital-safety hardenings (14-Jul)](q4_capital_safety_hardenings_14jul.md) — gate-8 SECTOR_EXPOSURE TOCTOU + kill_switch boot fail-fast + structure_exit∩trailing_sl guard (deployed under 277d63e).
- [Naked trades / order_protocol dead + exit-mgmt backtest (13-Jul, read-only)](naked_trades_order_protocol_dead_13jul.md) — order_protocol DEAD → 100% LIMIT_TRIPLE → no exit engine; best backtest ≈breakeven; exit-mgmt does NOT outrank M-S4.
- [Capital chain binding-constraint (13-Jul, read-only)](capital_chain_binding_constraint_analysis_13jul.md) — 100% concentration-bound (~₹990/pos); system IS margin-aware (leverage bug refuted); LOW tier 0.5 halves size in 78%.
- [M-S4 dead scorer steps 1&3 (13-Jul, read-only)](m_s4_dead_scorer_steps_investigation_13jul.md) — volume_surge(15)+atr_filter(10) always 0.0 (inputs None @secondary_screener.py:395-399); min_pass 60 ≈92% of a ~65 ceiling; fixing shifts scores +15-25 → re-run parity before enforce.

## 16-Jul Operations — relocated from the ACTIVE index on 17-Jul (all DEPLOYED/superseded; every topic link preserved)
> Relocated per the index's durable rule (relocate, never delete) when MEMORY.md approached the read limit.
> All of the below are superseded by the 17-Jul deploys: batch-1 `eb9cffa` → batch-2 `0a9a6a8` → sweep `b2d7b2b`. Detail lives in each topic file.

- ✅🚀 **[16-Jul DEPLOY DONE — alert-watcher `--loop` + F1 observe LIVE; VM==bare==`11abebb`](deploy_alertwatcher_f1_done_16jul.md)** — **respawn loop KILLED (NRestarts 104,567→0).** ⭐ The TAG is the code identity, not the branch SHA. ⏰ 2 soaks owed.
- ✅🏁🚀 **[16-Jul M-C CAPITAL-SAFETY CLUSTER DEPLOYED (M-C4+C5+C6+C8)](deploy_mc_cluster_done_16jul.md)** — **⚠️ M-C8 rewrote the EMERGENCY path and the drill was MOCK-broker only ⇒ THE FIRST LIVE HARD_KILL IS THE REAL TEST.** [[deploy-mc-cluster-done-16jul]]
- 🏁🔬 **[16-Jul M-C cluster consolidation — merge + regression + sandbox drill](mc_cluster_consolidation_16jul.md)** — 4763 pass, zero-new; drill **35/35**. Its first run (25/35) was a **harness** bug, not a code defect. [[mc-cluster-consolidation-16jul]]
- 🏁✅ **[16-Jul M-C5 CAS + M-C6 zero-mult skip + the test_main logger leak](mc5_mc6_testmain_16jul.md)** — M-C6 **inverts a documented FIX-133 decision — ratified**. The test_main leak made any later test asserting on main's logging **silently vacuous**.
- 🧨✅ **[16-Jul M-C8 FIXED — hard_kill's flatten runs on a worker, not the caller's fill thread](mc8_async_hardkill_16jul.md)** — closes the EXITING-blind shutdown race too. **⚠️ 3 deviations awaited ratification.** [[mc8-async-hardkill-16jul]]
- 🧨🔎 **[16-Jul M-C8 investigation (read-only)](mc8_investigation_16jul.md)** — kept for the Q1-Q6 reasoning. Its fire-and-return steer HELD (6/6 prod callers ignore the report); its "all existing tests pass unchanged" claim was DISPROVEN. [[mc8-investigation-16jul]]
- 🔒🛠️ **[16-Jul M-C4 FIXED — kill-switch lock released before the auto-trip publish+send](mc4_killswitch_lock_16jul.md)** — it blocked the last-mile order gate **20.02s** (measured). RED-on-old proven. **env finding: the known-PC-env failure count is TIME-GATED.** [[pc-test-env-hygiene]]
- 🩺🔒 **[16-Jul M-C4/C5/C6/C8 read-only investigation](mc_cluster_investigation_16jul.md)** — kept for the reachability analysis (only M-C4/M-C8 were reachable; M-C5 gated by the reconciler's atomic caller gate, M-C6 by the allocator's `min_weight` clamp). [[mc-cluster-investigation-16jul]]
- 🔀🚀 **[16-Jul alert-watcher + F1 consolidation](consolidation_16jul.md)** — DEPLOYED as `11abebb` (tag `deploy-16jul-alertwatcher-f1`→`1d5337d`); kept for the merge/rollback detail. [[consolidation-16jul]]
- ⭐📋 **[PENDING-WORK census (16-Jul)](pending_register_16jul.md)** — the register `.txt` is Rama's EXTERNAL git-excluded doc, NEVER in the repo. Both blockers CLOSED. **TOP open engineering item = B2/M-S4** — 25/100 of the live selection score is a constant 0.0. [[pending-register-16jul]]
> Also relocated earlier from the same block: **F1** [[f1-trades-sector-16jul]] · **alert-watcher `--loop`** [[alertwatcher-loop-fix-16jul]] · **morning-verify** [[morning-verify-16jul]] · **15-Jul combined deploy** [[deploy-done-16jul]].

### 17-Jul relocation from the active index (all DEPLOYED or superseded; every topic link preserved — the batch-safe pile is now EMPTY, so the classification entry has served its purpose)
- 🔴💰 **[E4 INVESTIGATED (17-Jul) — E4 *IS* W10; fixing either half ALONE is a regression](e4_investigation_17jul.md)** — **⛔ do NOT "just pass the real costs".** WRITER stores NET, READER subtracts costs again ⇒ **costs subtracted TWICE**.
- 🗂️ **[BATCH-2 (17-Jul) — logger token leak FIXED (L11), stale dup deleted, ITEM 2 REFUSED](batch2_done_17jul.md)** — the leak was **undercounted 41%**. **ITEM 2 refused: the audit was WRONG.** [[batch2-done-17jul]]
- ✅🗂️ **[BATCH-1 DEPLOYED (16-Jul)](deploy_batch1_done_16jul.md)** — 15 items live. **🔴 To the LOOP: E4 — the DAILY-LOSS LIMIT is fed GROSS not net** · **P3-s14** (webhook dedup rollback). 🏆 M-SC2 CLOSED runtime-proven. [[deploy-batch1-done-16jul]]
- 🗂️ **[BATCH-SAFE vs LOOP classification (the approved triage rule)](batch_classification_16jul.md)** — **LOOP if it touches capital/kill/order/schema/sizing/regime/any live trading decision; UNSURE → LOOP.** [[batch-classification-16jul]]

## 17-Jul deploys — relocated from MEMORY.md on 18-Jul (superseded by the 18-Jul work; every topic-file link preserved)

- ✅🔒🚀 **[P1 DONE + DEPLOYED 17-Jul — `/health` honours `require_hmac`](p1_health_require_hmac_17jul.md)** — **⭐ INERT until Rama flips `require_hmac` — the flip no longer opens the `/health` `?token=` oracle.** [[p1-health-require-hmac-17jul]]
- 🚨✅🚀 **[LIVENESS ALARM DEPLOYED 17-Jul](liveness_alarm_17jul.md)** — `*/5 9-15 * * 1-5`: unit inactive in **[09:00,16:00)** on a trading day ⇒ ONE CRITICAL. ⚠️ a `systemctl stop` == a death ⇒ park with SOFT_KILL. **⭐ the canary NEVER watched this unit.**
- 🔴🚀🔝 **[S4 HALTED THE SYSTEM AT BOOT — FIXED + DEPLOYED 17-Jul](s4_boot_outage_17jul.md)** — unauth boot self-check got S4's 401 ⇒ `_shutdown_event.set()` ⇒ down 08:16:09 (0 trades). Fix: **a 401 PROVES Flask is listening**. **⚠️ MONDAY 20-Jul 08:15 = FIRST REAL BOOT PROOF — WATCH IT** (+ liveness alarm's first live run). [[s4-boot-outage-17jul]]
- ✅🚀 **[P3-s14 FIXED + DEPLOYED 17-Jul — `a9a686e`](p3s14_done_17jul.md)** — a store failure releases BOTH claims + returns retryable **503**. **⚠️ OPS FINGERPRINT RETIRED: alert on the CRITICAL `signal store FAILED` line, NOT `response_code=500`.**

## 18-Jul DEPLOYED work — relocated from MEMORY.md (superseded as 'current'; all links preserved)

- 🚨✅🚀 **[MISSING/INVALID `direction` ALERTS AT BOOT — DEPLOYED 18-Jul](missing_direction_alert_18jul.md)** — ANY validation failure fires **ONE Telegram+email CRITICAL naming the file**; **the boot STILL fails**. Before this there was NO alert at all.
- 🧭✅🚀 **[STRATEGY-DIRECTION REGISTRY — DEPLOYED 18-Jul](strategy_direction_registry_17jul.md)** — YAML registry + daily officer (16:22 Mon-Fri): auto-detect → PENDING → notify → CONFIRM on first fill → **DIRECTION_CONFLICT**. **`StrategyConfig.direction` stays the ONE source.**
- 📊🚀 **[REGIME PHASE 0 — DEPLOYED 17-Jul](regime_phase0_17jul.md)** — `fetch_daily_candles` extended to ingest 10 indices via the existing `historical_data` path. **DATA ONLY**, no migration. ⇒ **the regime clock runs with NO new code.** [[regime-phase0-17jul]]

## 18-Jul regime investigations — relocated from MEMORY.md (links preserved)

- 📉🔬🔝 **[Q10 REGIME THESIS — NOT DETERMINABLE 18-Jul](regime_thesis_validation_18jul.md)** — **🔴 RAMA: refresh the Kite token** ⇒ backfill blocked, Part B NOT started. **⭐ But the ceiling is the TRADE side — the backfill CANNOT rescue it:** 21/15/11 days per cell. **Beta trap:** a 91%-long book makes "Bull mornings did better" the null. **LARGE effect ≈ 2.2 months.**
- 📊🔎 **[REGIME PHASE 1 SCOPED 18-Jul — 3 PREMISES INVERTED](regime_phase1_investigation_18jul.md)** — the `direction` axis is a **daily EMA50/200 trend, NOT the 09:15–09:59 move**; **🔴 the V3 chain IS wired to it ⇒ ⛔ do NOT flip `regime.enabled` mid-soak.**

## Q10 / regime pointers — relocated 18-Jul (2nd pass); links preserved

- 📉🔬🔝 **[Q10 PART A — MIN-SCORE CONTROL 18-Jul](regime_minscore_control_18jul.md)** — `config_snapshots` authoritative but starts 02-Jul ⇒ **12 of 23 book days UNDETERMINABLE** (not guessed). **⚠️ git dates PROVEN unsafe — the VM leads git.** **A3: NO cell clears n<10 — the NOT-DETERMINABLE verdict HARDENS.** **⭐ FREEZE `min_pass_score` while measuring.**
- 🗄️📊 **18-Jul regime investigations — the two topic links live in [archive_index_regime_18jul](archive_index_regime_18jul.md)**: Phase 1 scoped (3 premises inverted) · Q10 thesis (NOT DETERMINABLE; **🔴 Part B awaits Rama's Kite token**).

## CT-harness pointers — relocated 18-Jul; links preserved

- 🛡️✅🚀📌 **[CT HARNESS SCRATCH-SAFE + GUARD PINNED BY INVARIANT — 18-Jul](ct_harness_safety_18jul.md)** — the harness can no longer open a live DB **writable**. **It HAD fired.** 5 more bypass routes closed, PROVEN TO BITE. **📌 PERMANENT RULE.**

- **17-Jul live state** (relocated from MEMORY.md 18-Jul during compaction) — P1 /health · liveness · S4 · P3-s14 all DEPLOYED, PC==VM==`2b10b5e`. Code ledger empty but for the sign-off-gated E4/W10.

> [ARCHIVE] **25-Jul relocation (3rd pass - read-limit compaction; from active `MEMORY.md`, VERBATIM - NO data loss; topic-file + wiki-links preserved). All three are CLOSED/COMPLETE, with their topic files intact:**
- 🌅✅ **[FRI 24-JUL §A CLEAN · A3 PROVEN · A1-A3 DONE](friday_boot_24jul_resume.md)** — A1: F2 needs NO new state machinery (cheap=trigger existing KillSwitch; `is_active`+config BOTH boot-only). A2/A3 confirmed. **§B 16:05 xlsx VERIFIED + all DEPLOYED `bc75406` 24-Jul.**
- ✅🔑🔝 **[S4 `/health` 401 FAMILY CLOSED — B2′ DEPLOYED 21-Jul `aff5256`](fix_sprint_21jul2026.md)** — `signals.py:28` now 200-or-401 ⇒ **daily false CRITICAL ENDS** (RED-on-old proven). **No 4th instance** (sweep done); `:703` external, **REFUSED (stands)**. [[preflight-401-third-sibling-20jul]]
- 🏁✅⭐🔝 **Q9 COMPLETE 19-Jul — 22/22 WIRED · 16 REACHABLE.** **LESSONS:** CONFIGURED≠COVERED · WIRED≠REACHABLE. [[consecutive-losses-gate-wired-19jul]] [[q9-batch1-daily-loss-wired-18jul]] [[q9-batch2-killswitch-toctou-18jul]] [[q9-batch3-capital-invariant-18jul]] [[q9-batch4-sizing-reachability-18jul]] [[q9-batch5-post-restart-18jul]] [[q9-live-seed-mc1-wired-19jul]] [[q9-money-path-coverage-18jul]]
- (25-Jul 3rd pass, verbatim) wiki-link stubs relocated from the active index:
  - [[ct-harness-safety-18jul]] [[ct-guard-invariant-18jul]] [[missing-direction-alert-18jul]] [[strategy-direction-registry-17jul]] [[regime-phase0-17jul]] [[p1-health-require-hmac-17jul]] [[liveness-alarm-17jul]] [[p3s14-done-17jul]]

- (27-Jul compaction, VERBATIM from the active index — closed/deployed/verified):
  🔁✅🔝 **[RE-ALERT LOOP FIXED 26-Jul `324be50` — dedup now tracks PRESENCE](realert_presence_ledger_26jul.md)** — persistent ⇒ 6h/24h/7d, **never CRITICAL twice**; cleared-and-returned ⇒ **immediate full severity** (it used to be swallowed). ⛔ `security-watcher` RestartSec=60 ⇒ this went LIVE ON PUSH, not Monday. [[realert-presence-ledger-26jul]]
  🔢✅ **[INIT = one row per PROCESS START — any `SUM(...INIT)` DOUBLES on a restart day](capital_readers_fixed_25jul.md)** — 10/30 dates multi-INIT; 21-Jul read 19,716 vs true 9,857.30. ⭐ FIXED 25-Jul `f8a2639`; use `get_day_opening_capital()` (FIRST row). [[capital-readers-fixed-25jul]]
  ✅🔧🔝 **M-O5 DEPLOYED 22-Jul `4585bd2` (tag `deploy-22jul-mo5`)** — `eod_squareoff.fire_now` now resets `_fired_for_date` on `_fire` raise AND partial-fail (Rider 1); stays set on success ⇒ a fire_now failure no longer disables the 15:17 backstop. comm-23 EMPTY both ways; service NOT restarted. ⚠️ **B1: verify RESET_PNL by SUM (retry=2 nonzero rows)**; no prod-verify day ⇒ tests ARE the evidence. [[mo5-deployed-22jul]]
  ✅🔝 **BOOT-PATH PAIR DONE.** **B1 extraction + midnight day-floor DEPLOYED 21-Jul `e21cf9e`** — `compute_live_seed` in `main.py`; boot floor derived ONCE, passed to seed+rehydrate (closes midnight-straddle residue); gate comm-23=0, RED-on-HEAD shown. ⚠️ 08:15 boot verifies EXTRACTION only; straddle is test-covered. **B2′ 401 DONE `aff5256`.** `:703` REFUSED stands. [[preflight-401-third-sibling-20jul]]
  ✅💰 **E4/W10 ✅ VERIFIED IN PROD 21-Jul** (deployed 20-Jul `a266432`) — first `RESET_PNL` **+18.82 = −Σpnl_delta**, NOT 21.04 old (Σcosts 2.22); zeroing −0.000000, A3 GOOD ⇒ reader returns NET in prod. Shape ≠ 20-Jul 18.29/19.61 (diff book). [[e4-w10-deployed-20jul]]


## Relocated from MEMORY.md on 11-Sep-2026 (room for the no-subagents rule; verbatim, not deleted)

> 🔧✅🔝 **SAT TASK 1 DONE · F BUILT · ⛔ BOTH UNPUSHED.** `38de90f` moved the timing contract to `core/mis_squareoff_timing.py`; `22a143f` is F. 🔬 Gates differentially clean (Δ0, then Δ+29). ⛔ `origin/main` is still `effff24`. ⏸ **`F_RECIPIENT_CONFIRMED` still owed from Rama — ⛔ F must not ship without it.**


---

## Relocated from MEMORY.md, 11-Sep-2026 (compaction; superseded, not deleted)

> 🟢🛡️🔝 **STOP A + DIV-2 SHIPPED — tip `18dd6cc`.** ⭐ **PASS_1 15:03 · PASS_2 15:06 · cutoff 15:09.** ⭐ `_verify_cancelled` polls a **5 s budget**; ⭐ `_restore_protection` puts the stop back on **every** failure path, ⭐ idempotency **side-scoped** (`symbol+transaction_type+trigger>0`). 🔬 Gate 10F/6042P, sets identical. ⛔ Payload fix (F4) NOT shipped — ⭐ needs F3 persistence first.

> 🟢🛡️🔝 **STOP A BUILT 03-Sep (`5455ced`) — SCHEDULE + SETTLE + RESTORE.** 🔬 **PASS_1 15:03 · PASS_2 15:06 · cutoff 15:09** (was 15:07/15:10/15:12) ⇒ ⭐ both finish BEFORE Zerodha's earliest action. ⭐ `_verify_cancelled` now polls to a **5 s budget** (was ONE poll at +27-53 ms; terminal at +1.115 s). 🔴 ⭐ **`_restore_protection` puts the stop back on EVERY failure path.** ⛔ Payload fix NOT shipped.

> 🔴⏱️🔝 **MIS IS **ON** FOR FRI 04-Sep — 👤 Rama: *"First neatly close existing issue>Turn on MIS tomorrow"*.** 🔬 3 attempts / 3 `CANCEL_FAILED` / **0 exits** ⇒ ⭐ **scheduling a manual intervention**, ⛔ not accepting a risk. 👤 **Be at the screen 15:07-15:17; flatten by hand.** ⭐ PASS_1 survivable (G5b recovers ~12 s); 🔴 **PASS_2 is fatal.** ⛔ Both advisors said OFF; ⭐ dissent recorded once.

> 💀🔴🔝 **03-Sep INCIDENT — THE SYSTEM HAS NO WORKING FORCED EXIT. 🔬 THE MIS SQUAREOFF CANCELLED ANANTRAJ'S SL+TGT (`success=True`) THEN REFUSED TO EXIT ⇒ NAKED; the emergency fallback (raw MARKET) was REJECTED **8×**; 👤 Rama closed it by hand.** ⛔ Loss ₹2.13 — ⭐ luck, ⛔ not design. 📄 `docs/incident/2026-09-03_naked_position_ANANTRAJ.md` → [[emergency_exit_market_order_is_rejected_03sep]]

> 🏁🖥️🔝 **GUI CAMPAIGN: 🟢 22 of 22 APPROVED · 🟢 **21 table-bearing screens REFITTED** (⭐ S01 has ⛔ no table) · 🟢 **MERGED + PUSHED 02-Sep as `686df1c`, tip `2d08436`**. ⛔ ⛔ NOT "finished": 🔴 ⛔ **NO screen is `VERIFIED LIVE`** -- every approval was a LOCAL render. ⏸ 👤 **RESTART STILL OWED** -- ⛔ and the live GUI is a **MIXED** state, ⛔ NOT an old one → [[gui_after_deploy_is_mixed_not_old_03sep]]

> 🗿🟢🔝 **TREE ADVANCED `39292d3` → `2d08436` (👤 Option-1 line) AND `80091ce` PUSHED** -- T1 alert-truth + T2 broker-error classification. 🔬 PC=VM bare=deployed tree, **0** differing files. ⭐ *zero new failures; the existing 10 unchanged.* ⛔ MIS **NOT** enabled -- ⭐ activation gated on a sandbox drill.

> 🗿🟢🔝 **BOOT PROVEN 03-Sep 08:15 -- `2d08436` STARTED.** 🔬 `STARTUP` **ev 3814** COLD @ 08:15:41.796 > start 08:15:29, `NRestarts=0`; token 08:15:02; checks OK `warnings=[]`. 🔬 Bare main `2d08436` (ref written 02-Sep 23:59:54, ⭐ BEFORE the boot) vs deployed tree = **0** differing tracked files. ⇒ ⭐ TREE-advance precondition met; ✅ **TAKEN 03-Sep** (see the entry above).

> 🟢🚀🔝 **30-Aug 19:5x IST — THE 9 ARE PUSHED. `origin/main` `effff24` → `39292d3`; 🔬 VM bare **and** the DEPLOYED TREE `/home/ubuntu/systems/trading-system` both `39292d3`.** 👤 On Rama's 11:24 PUSH-AUTH. ⛔ **SERVICE NOT STARTED** (enabled/inactive — correct for a Sunday). 🔴 **MON 08:15 IS THE FIRST RUN OF THIS CODE.** ⛔ F2-CORE ⛔ NOT shipped (V-5 exit 1).
> 🗿🟢🔝 **31-Aug — D-2 TAKEN: ROLLBACK TREE `52ccb4f` → `39292d3`** 👤 on Rama's typed line, ⛔ not the suggested one. 🔬 Boot proven: `STARTUP` **ev 3805** COLD/live @ 08:15:17.489 > start 08:15:05, `NRestarts=0`, clean self-exit 17:35:04. 🔴 **ACCEPTED WITH A KNOWN DEFECT:** `daily_trade_review` FAILED ⇒ ⛔ no 31-Aug report (regenerable). ↩️ Revert in one line → `52ccb4f`.

> ✅📧🔝 **EXECUTED 31-Aug — F FIRST-EXECUTED AT 15:07 ON AN UNVERIFIED CHANNEL.** 🔬 `TRANSPORT_RESULT=BOTH_ACCEPTED` twice (08:15:18, 15:05:04); ⛔ `F_RECIPIENT_CONFIRMED` **NEVER PROVEN**. ⛔ Service NOT stopped — no instruction arrived. ⭐ Harm could not occur: **MIS flat, `mis_candidates=0`**. ⛔ The premise *"logs record NO recipient"* was **FALSE** at this SHA — `to=` IS logged.

> ✅⏰🔝 **EXECUTED 31-Aug — ALL 3 LIVE-BEHAVIOUR CHANGES RAN.** 🔬 `12c4ab1` retention 02:10:01 **rc=0, deleted 0**, 12 refusals, cap 25 respected. 🔬 `0823b75` recipient live — `to="pythonsystemalerts@gmail.com"` in-log ×2. ⚠️ `1a1cb25→bee9755`: retirement CLEAN (both flags verified) ⛔ but `daily_trade_review` **FAILED** 16:07 ⇒ ⛔ **no 31-Aug report** — net regression.

> 🗿🔴🔝 **F2-CORE IS BUILT, GATE-CLEAN AND ⛔ HELD UNPUSHED at `587b306`** (`feat/f2-core-30aug`). 👤 **OPTION 2:** criterion 7 unproven for the GLOBAL-STOP channel (a daily-loss breach still closes **both** books) ⇒ ⛔ 6 of 7 ⇒ ⛔ does not ship. ⛔ Never delete/squash it. ⚠️ ⛔ Its gate does NOT survive a SHA change — ⭐ RE-GATE on resume.

> 🔴⏱️🔝 **28-Aug PUSHED `52ccb4f` → `effff24` (MIS auto-square-off @ 15:07/15:10). ✅ SOURCE_PUSHED + VM_CHECKED_OUT · ⛔ RUNTIME_NOT_STARTED.** ⚠️ ~~TREE STAYS `52ccb4f`~~ — **SUPERSEDED 31-Aug: TREE = `39292d3`.** ⭐ Mon 08:15 = boot/config tier ONLY; 🔴 **Mon 15:07 is the FIRST live exit-order execution** — ⭐ arm a 15:05–15:20 watch. 📄 `docs/audit/BUILD_MIS_ORCHESTRATOR_28-Aug-2026.md`

> 📢🔴🔝 **WEEKEND: F SHIPS FIRST, F2-CORE WAITS.** ⭐ F makes Mon 15:07 observable and has a Monday deadline; F2-CORE does not. ⭐ F needs TWO self-tests (08:15 **and** ~15:05) + **`F_RECIPIENT_CONFIRMED`**. ⛔ A partially accepted F is worse than no F. 📄 `docs/audit/F_SPEC_D1b_NOTIFICATION_28-Aug-2026.md`

> ▶️🔝 **[RESUME](UNPUSHED_PENDING_DEPLOY_LEDGER.md).** ✅ **28-Aug 08:15 BOOT PROVEN at `52ccb4f`** (`STARTUP` 3801 @ 08:15:25.978 > start 08:15:13) ⇒ 🟢 **TREE ADVANCED `bc9a9f5` → `52ccb4f`.** ✅ U3a + ✅ **U1 EXECUTED 10:15:13** — ⛔ NOT the T+1 arm. ⏸ U3b + U2 owed. 📄 `docs/audit/FILE20_CORRECTIONS_AND_BOOT_28-Aug-2026.md`

> 🔴🗿🔝 **F2 — DECIDED 27-Aug (FILE 14), ⭐ F2-CORE BUILT 30-Aug (see above, HELD): SPLIT IN TWO.** ⏸ **F2-CORE BUILT 30-Aug, ⛔ HELD (OPTION 2 — see above)**, method **OPTION B** (reimplement vs main): 🔬 **7 collision files** + new `pipeline_policy.py`; ⛔ NO schema v46, ⛔ NO `intraday_max_*` rename, ⛔ `position_sizer.py` UNTOUCHED. ⏸ **F2-SIZING DEFERRED.** ⛔ never touch that working tree.

> 🔴📄🔝 **01-Sep — `daily_trade_review` FAILED TWO CONSECUTIVE DAYS (31-Aug + 01-Sep) ⇒ ⛔ NO REPORT EITHER DAY.** 🔬 `TypeError: unhashable type: 'StyleProxy'`, openpyxl 3.1.5, exactly 2 tracebacks. ⚠️ ⛔ NOT a one-off — a REPEATING loss. ⏸ Untouched. 🔬 `eod_review` also failed 01-Sep (Gemini quota) ⇒ ⛔ that log is a FAILURE NOTICE, ⛔ not evidence.

> 🏁🖥️🔝 **GUI CAMPAIGN: 🟢 **22 of 22 APPROVED, ⛔ 0 QUALIFIED** — 👤 S16 + 👤 S06 + 👤 S07 all closed 02-Sep.** ⛔ ⛔ NOT "finished": ✅ the **global table rule is BUILT** (`63a3946`+`0bbe127`), ⛔ not VERIFIED LIVE · 🔴 ⛔ **NO screen is `VERIFIED LIVE`** — every approval was a LOCAL render · ✅ **the 119 ARE PUSHED** — `origin/main` **`2d08436`** (top entry). 📄 ledger Entries 33-35
