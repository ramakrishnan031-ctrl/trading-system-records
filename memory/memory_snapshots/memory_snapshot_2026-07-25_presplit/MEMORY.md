# Memory Index (ACTIVE)

**Structure:** ACTIVE index; older → **[archive](MEMORY_ARCHIVE_2026H1.md)** (**relocate, never delete**). **⚠️ BYTE BUDGET (20-Jul): ≤300 B/line, ≤450 B for 🔝. A batch adds ONE line *or* edits one; a 2nd clause goes in the topic file.** Check (must print NOTHING): `LC_ALL=C awk 'length>(index($0,"🔝")?450:300){print NR": "length"B"}' MEMORY.md`. Compacted 25-Jul: `docs/audit/memory_compaction_25jul2026.md`.

## Core References
- 🗳️🔝 **[DECISIONS BOARD → `docs/decisions/00_INDEX.md`](decision_packages_19jul.md)** — Rama's **10 open choices**: E4/W10 · D1 · D2 · D3 · D4 · PerfAllocator(#06) · Regime(#07) · Freeze(#08) · Prune(#09) · Throttle(#10). **3 DECIDABLE NOW** (01·08·09, briefs `BRIEF_*`) · 7 gated on 3 roots. [[decision-readiness-triage-19jul]] [[e4-w10-outcome-impact-19jul]]
- 🔐🔎 **[C6 SCOPED 25-Jul](receiver_auth_c6_scoping_25jul.md)** — 2 routes; auth STATE already shared ⇒ only the CHECK is duplicated. ✅ PB-01 auth SAFE. 🔴 **Monday risk = boot wiring, not auth**: grep boot log for `"PB-01 watchlist: ENABLED"`. [[receiver-auth-c6-scoping-25jul]]
- 🗂️✅ **WAVE-7 TRIAGED** (`wave7_nine_investigation_22jul2026.md`): 45→34 closed · **Tier A EMPTY** (M-O5 deployed 22-Jul `4585bd2`) · 4 inert · 6 ordinary · **M-C2/O4/O7 arm IFF delivery; M-O4 inert (system-only)**. Pushed.
- ⏰✅ **[SHUTDOWN = CONFIG 17:35 — DEPLOYED 25-Jul `570b3e8`](service_window_configurable_25jul.md)** — the constant had **TWO roles**; split + locked to one schema bound. ⚠️ the boot guard **cannot read config**; START window now 18:15. [[service-window-configurable-25jul]]
- 🔧✅ **[FIXATION BATCH 24-Jul — DEPLOYED `bc75406`](fixation_batch_24jul_handoff.md)** — M-K2 + §E + F1(CLOSED) + docs SHIPPED; 16:10 verify PASSED; backup clear EXECUTED (76 files/4.73GB). **ONLY §B `capital_snapshot` (boot-gate) remains.** 🆕 daily-report cron = NO heartbeat.
- ⛔🔑🔝 **[PERSISTED KILL = HALT, not "entries-blocked" (21-Jul)](persisted_kill_is_halt_21jul.md)** — SOFT_KILL+restart ⇒ exit 4; in-process form has NO operator trigger. ⚠️ **a HALTED day forfeits `RESET_PNL`** — ⭐ but the routine **15:15 circuit-breaker kill does NOT** (24-Jul: kill 15:15, RESET_PNL 15:19 = −Σpnl_delta, MEASURED) ⇒ don't misread F1's scope. [[persisted-kill-is-halt-21jul]]
- 🌙 **Service self-exits at the CONFIGURED `service_window_end` — 17:35 from Mon 27-Jul (was 16:00)**, when flat ⇒ a night `inactive(dead)`/exit-0 is BY DESIGN, NOT S4 (restarts 08:15). ~09:00 exit + 0 trades + LIVENESS-DOWN = S4. [[service-window-configurable-25jul]]
- 🪝⛔🔝 **[PRE-RECEIVE HOOK — DO NOT ARM AS-IS (20-Jul)](pre_receive_hook_newline_bug_20jul.md)** — guard-2 cron-integrity **false-rejects EVERY push** (trailing-newline bug `deploy/hooks/pre-receive:53-60`) ⇒ arming = deploy lockout; needs 1-line fix + dry-run soak. Guard-1 sound.
- 📉🔬🔝 **RESEARCH (19/20-Jul):** [D3](d3_band_inversion_robustness_19jul.md) UNRESOLVED · [D4](forward_shadow_capacity_d4_feasibility_19jul.md) · [#06](candle_retention_perfallocator_feasibility_19jul.md) ⇒ D1 · [#07](regime_computable_today_20jul.md) · [book=TIME-sel](throttle_selection_record_correction_19jul.md) · [mortality](signal_mortality_census_19jul.md). ⚠️ **NEVER run `forward_shadow_record.py` manually.**
- 🗑️📐 **PRUNE #09 DESIGN (Option B) — written, awaits review** — ⚠️ the naive diff makes the 15:50 job a **permanent no-op** (`EXPIRED`/`DUPLICATE` are NEVER persisted). Keeping rejects = **+9.9 MB/trading day, unbounded**; ×15 via backups. [[prune-09-design-20jul]]
- 🔐 **2FA seed→VM-only RUNBOOK — written, NOT executed, weekend-only (20-Jul)** — seed hash-identical PC+VM. ⚠️ re-enrol is **ONE-WAY** (no rollback). Path A (delete PC copy, no rotation) = zero risk. `docs/decisions/RUNBOOK_2fa_seed_vm_only.md`. [[token-workflow-confirmed-21jun]]
- 🔑🧾 **[ARTIFACT BASELINE — the cross-batch rule (19-Jul)](artifact_baseline_reconciliation_19jul.md)** — **⭐⭐ RULE: within-batch before==after ≠ cross-batch unchanged** (the live DB advances on cron heartbeats even while DOWN) ⇒ **verify ROW-LEVEL, not by hash.**
- 🔒🎯 **[EXITS THREAD CLOSED 24-Jul — reopen ONLY post-M-S4](trailing_stop_never_fired_24jul.md)** — trail UNREACHABLE (423/423 LIMIT_TRIPLE); 8 exit policies MEASURED −0.076..−0.144R, none profitable; lever=TGT; +1.43R uncapturable (whipsaw). [[e4-w10-outcome-impact-19jul]]
- 🎯📉🔝 **[ENTRIES BUY EXTENSION — ⛔ DO NOT loosen the V3 gate/rr_floor (24-Jul)](entries_buy_extension_24jul.md)** — STATISTICAL + GEOMETRIC (RR median 0.33) + ARITHMETIC (38-39% win vs 43.5% breakeven) converge. The gate is the only INDEPENDENT read on entries — tuning it to agree destroys it.
- 📌⛔ **RULE: never `scripts/*.py --db <copy>`** — it writes to the LIVE DB *before* parsing `--db`. There is no safe read-only copy invocation.
- 🗄️✅ **DONE/DEPLOYED → [archive](MEMORY_ARCHIVE_2026H1.md)** (links relocated 25-Jul). ⚠️ RAMA: `cleanup.py --live` REMOVED — return as a `scripts/` tool? 6 destructive CTs UNBLOCKED, NOT RUN.
- ⛔🔍 **security-watcher is NOT broken** — `activating/auto-restart` is the designed `RestartSec=60` heartbeat; nothing reads its `ActiveState`. Do NOT 'fix'. [[ct-guard-invariant-18jul]]
- 🔒🔎 **[AB-910 Ops+Sec audit](ab910_ops_security_audit_16jul.md)** — 5 HIGH, no CRITICAL. OPEN: §2.2 `market_day_only` decorative on 20/25 · §1.2 · §2.1. [[ab910-ops-security-audit-16jul]]
- 🔑⏰ **[A PRIOR-DAY kill auto-clears at the next 08:15 boot](killswitch_autoclear_prior_day.md)** — only SAME-day *emergency* kills need `deploy/resume.sh`; compare `triggered_at` DATE to boot date. The 15:15 circuit-breaker SOFT_KILL persists overnight BY DESIGN.
- 🗄️⚠️ **[MIGRATION-ON-OPEN rule (14-Jul)](migration_on_open_rule_14jul.md)** — schema migrates on DB-OPEN not at boot. **GUARD `ed1c4b9`:** only main.py boot migrates; others refuse + CRITICAL sentinel.
- ✅🔝 **[UNPUSHED / PENDING-DEPLOY LEDGER](UNPUSHED_PENDING_DEPLOY_LEDGER.md) — READ before EVERY off-market window.** ✅ **CODE LEDGER EMPTY** — latest deploy 25-Jul `570b3e8` (service window); PC == origin == VM bare == VM tree.
- 🗂️ **BUCKET BOARD (17-Jul):** decision items → the DECISIONS BOARD above · **D** own-run D2 CT-harness (`ct_utils.py:63` LIVE DB); BK-1 ✅ [[bk1-long-short-scanner-17jul]] · **G** ✅ Mon 20-Jul · F1 enforce (Rama) · HARD_KILL = M-C8 · **H** X8 · W1 · **I** T2 · S&R V1.
- [SATS tooling](sats_tooling.md) — PC-only manual SAST (Bandit+Semgrep); `sats\scripts\scan_*.bat` → `sats\reports\`; git-ignored
- [Token workflow (21-Jun)](token_workflow_confirmed_21jun.md) — AUTOMATIC: 05:00 delete → 08:15 TOTP refresh → token-watcher starts app. `auto_refresh_token` gates whether the system trades at all.
- [VM Architecture LOCKED (161.118.187.249)](project_vm_architecture_locked.md) — ubuntu; shared venv; IST; bare `~/trading-system.git` → post-receive checkout to `/home/ubuntu/systems/trading-system` (tree NOT a git repo). GUI = Waitress `127.0.0.1:8500` behind `tailscaled`.
- [Master project state](project_master_state.md) — LIVE since 11-May-2026 · [PHASE 21 COMPLETE (17-May)](project_phase_21_complete.md) — 92+ fixes; 2112 tests
- [Capital operational note](capital_operational_note.md) — daily loss limit reads `fm_ledger.pnl_delta`, not `trades.net_pnl`; RMS closes pass costs=0.0
- [Order lifecycle note](order_lifecycle_operational_note.md) — pending_rr_cancel failure logs ERROR but doesn't escalate; backstops catch it
- [CO bracket note](co_bracket_operational_note.md) — CO SL is broker-managed; CHECK1 is the only external-close backstop
- 💰 [Dual daily-loss mechanism](dual_daily_loss_mechanism.md) — ⚠️ **ONE limit** `daily_loss_limit_pct=0.03` (≈**Rs296** = 3%×Rs9,875.60), two enforcement points, **NO absolute**. **RULE: read a threshold from code before computing against it.**
- [DB schema v28 analytics split](db_schema_v28_split.md) — TWO DB files (trading_system.db + analytics.db ATTACHed); raw sqlite must use `core.db_connect.connect`. ⚠️ `fm_ledger.date`/`webhook_audit.date` are **VIRTUAL GENERATED** cols; `pragma_table_info` HIDES them — real, do NOT "fix".
- 🗃️ **[ro-open of a WAL backup DB leaves `-shm`/`-wal` artifacts](sqlite_ro_wal_sidecar_gotcha.md)** — `?mode=ro` alone still creates a `-shm`; use `?mode=ro&immutable=1` or copy-first for zero-trace. LIVE DB unaffected (app owns them). Created 14 in backups 24-Jul.

## Hygiene Queue (low priority)
- [PC test-env](pc_test_env_hygiene.md) — pre-existing PC failures (⚠️ **NOT "baseline 14"** — see the regression rule below); `ops_dashboard/tests` need `ops_dashboard/.venv` (357/357); pin tzdata

## Feedback / Rules
- 💱📏🔝 **[CAPITAL VOCABULARY — label which capital every rupee figure means](capital_vocabulary.md)** — ACTUAL **Rs 9,875.60** (70/30 MIS/CNC) · BUYING POWER ×5 MIS/×1 CNC · RISK CAPITAL · POSITION EXPOSURE. **System UNAWARE of leverage (sizes unlevered).**
- 🕛📊🔝 **[A REGRESSION RUN MUST NOT CROSS MIDNIGHT](feedback_regression_must_not_cross_midnight.md)** — `_TODAY` captured at COLLECTION but dated at EXECUTION ⇒ a run after ~23:15 IST corrupts attribution silently. SIBLING: an exact compare on a small delta off a LARGE EPOCH is float64-unsafe.
- 🧪📉🔝 **[NO FIXED-NUMBER TEST BASELINE — a remembered failure COUNT is a property of one env at one moment](feedback_no_fixed_test_baseline.md)** — take a fresh BASE run in the SAME session/window, `comm -23` the SETS (merge-only must be EMPTY). PC `bash` = **WSL stub** ⇒ ~20 tests run-not-skip. Predict before running.
- 🚫🔤🔝 **[NEVER classify/count/filter by FREE TEXT when a structured status exists](feedback_never_classify_by_free_text.md)** — rendering text OK; BRANCHING on it is the defect. Sweep the CLASS, ONE classifier, guard in CODE not comments.
- ⚖️🔎🔝 **[LIVE vs LATENT decides stop-and-report](feedback_live_vs_latent_findings.md)** — judge by REACHABILITY. LIVE ⇒ STOP. LATENT ⇒ CONTINUE + document + pin with a test that fails when it becomes reachable.
- ⚠️🔎🔝 **[An audit finding is a HYPOTHESIS — verify its premise](feedback_verify_the_finding_premise.md)** — 17-Jul 2 of 3 defective; 20-Jul `:703` was carried through many files unverified. **Refusing an item with evidence is valid.**
- ⚠️🔍🔝 **[A green check is evidence ONLY if it could have been red](feedback_verify_rc_not_output.md)** — errored command · stale baseline · vacuous test · a self-referential query. **⭐ Schema-validating the QUERIES does not validate the EXPECTATIONS — ask of every GOOD/BAD: measured, or assumed?** [[verify-check-the-rc-not-the-output]]
- 🔕⏰ **[No self-wakeups for time-gated pushes](feedback_no_push_wakeups.md)** — armed wakeup fails SILENTLY if the session's down (no alert/trace; class of liveness-probe/S4). Instruction-file handoff, not a wakeup. Proven 23-Jul (15:31 push-wakeup didn't fire). [[no-push-wakeups]]
- 🚫📋 **[Operator planning docs are external / git-excluded](feedback_operator_planning_docs_external.md)** — NEVER commit `MASTER_PENDING_REGISTER_*.txt` / `*_DECISION_SHEET_*.txt`. Tracked analysis reports live in `docs/audit/`.
- 🎨 **[GUI redesign review-first workflow](feedback_gui_redesign_workflow.md) — FOLLOW VERBATIM (next: Screen-04 Signals).** PNG+TXT → pixel-study → reuse Screen-02 language → additive read-only backend → pixel-review pre-commit → verify via `serve_verify.py` + headless Edge.
- [Sequential agents ONLY (04-Jul)](feedback_sequential_agents_only.md) — never parallel fan-out; one agent → report → next (API limit burn)
- [Foundation Rules](feedback_foundation_rules.md) — derive don't duplicate; boring code; fail fast/loud; no real alerts on non-trading days
- [READ SYSTEM_MAP.md before any work (NON-NEGOTIABLE)](feedback_system_map_first.md) — + PATHS.md; update after any path/cron/service change
- [Naive IST timestamps in tests](feedback_naive_ist_timestamps.md) — now_ist().replace(tzinfo=None)
- [Memory hygiene](feedback_memory_hygiene.md) — MH1-MH6 + WCH1-WCH5
- [Paper/Live parity PERMANENT RULE](feedback_paper_live_parity.md) — every change checks both modes
- [Reply style (Web Claude only)](feedback_reply_style.md) — short replies; long content to .txt
- [SSH key passwordless](feedback_ssh_automation.md) — trading_vm_secure has no passphrase
- [Use VM terminal for curl](feedback_vm_curl_tests.md) — PowerShell escaping breaks JSON
- [Webhook flow diagnosis](feedback_webhook_flow_diagnosis.md) — check `webhook_audit` (authoritative POST record), NOT signals+journal. Entry window is **[10:00, 15:00)**: 403s BOTH before 10:00 and after 15:00 are the designed gate, not an outage.
- [Transfer VM scripts via base64](feedback_vm_script_transfer_base64.md) — heredoc over ssh halves backslashes; base64 instead
- [in_flight is in-memory only](feedback_in_flight_memory.md) — restart to clear
- [Log rotation](feedback_log_rotation_fix.md) — FileHandler not RotatingFileHandler; **age-based pruning DOES work** (`log_cleanup` cron, `-mtime +30`) [[batch2-done-17jul]]
- [Trade export filters](feedback_trade_export_filters.md) — candles exclude CANCELLED

## Recent Operations (active)
> 🗄️ **ALL ≤17-Jul Operations → [archive](MEMORY_ARCHIVE_2026H1.md)**: 15/16-Jul blocks · Build History · Crash Tests · 13–14 Jul · ≤09-Jul (Wave-6, PUSH-1, Wave-5, full-repo audit) · V3 Steps 1-10b BUILT+DEPLOYED (`277d63e`). FIRST LIVE HARD_KILL still M-C8's test.
- 📉🔀 **[Book is NOT long-only; net-short EXPECTED not oversell](book_not_long_only_eod_reverse_aware.md)** — intraday SHORT strategies live. Short-vs-oversell via broker `buy_qty/sell_qty`. EOD squareoff BUYs to COVER a short (`eod_squareoff.py:1155`); can't go −1→−2.
- ★ Deferred (OPEN): **S&R V1 calibration** (data-gated) [[sr_v1_calibration_deferred_30jun]] · **C-2 webhook Ph3** = Rama [[c2_webhook_lockdown_02jul]]
- ★ Deferred (OPEN): **Slice 2.5 T2** REPAIRED `fix-t2-repair-07jul`@`ef442ab` UNPUSHED [[t2_repair_built_07jul]] [[t2_repair_verify_07jul]] [[t2_full_repair_scope_03jul]] [[delivery_slice25_status_30jun]]

## The CAREFUL-LOOP queue (capital/signal path — never sweep these)
- ✅🔧🔝 **M-O5 DEPLOYED 22-Jul `4585bd2` (tag `deploy-22jul-mo5`)** — `eod_squareoff.fire_now` now resets `_fired_for_date` on `_fire` raise AND partial-fail (Rider 1); stays set on success ⇒ a fire_now failure no longer disables the 15:17 backstop. comm-23 EMPTY both ways; service NOT restarted. ⚠️ **B1: verify RESET_PNL by SUM (retry=2 nonzero rows)**; no prod-verify day ⇒ tests ARE the evidence. [[mo5-deployed-22jul]]
- ✅🔝 **BOOT-PATH PAIR DONE.** **B1 extraction + midnight day-floor DEPLOYED 21-Jul `e21cf9e`** — `compute_live_seed` in `main.py`; boot floor derived ONCE, passed to seed+rehydrate (closes midnight-straddle residue); gate comm-23=0, RED-on-HEAD shown. ⚠️ 08:15 boot verifies EXTRACTION only; straddle is test-covered. **B2′ 401 DONE `aff5256`.** `:703` REFUSED stands. [[preflight-401-third-sibling-20jul]]
- 🆕 **Fallout — RECORDED not fixed (a):** `test_instance_lock`×2 · 3 `event_type` sites · `Rejected (Sizing/Capital)` label · `build_taxonomy_map --config-dir` · wave-7 · W9 webhook-drop · 403-POST count (~338k). [[signal-mortality-census-19jul]] [[q9-batch4-sizing-reachability-18jul]]
- 🆕 **Fallout — RECORDED not fixed (b):** `position_sizer.py:506` 2× ceiling (latent) · **`eod_cleanup` FK crash 15-Jul, no heartbeat (#09)** · Rs 0.29 SL. [[consecutive-losses-gate-wired-19jul]] [[q9-batch5-post-restart-18jul]]
- 🔴 **[S4 BOOT OUTAGE — FIXED+DEPLOYED; 1 follow-up OPEN](s4_boot_outage_17jul.md)** — OPEN: should a non-2xx `_shutdown_event.set()` block the boot, or degrade? (Rama's call).
- 🔎 **P3-s14 loop tail** — same defect shape at `webhook_receiver.py:875` (`fetch_one` inside `except IntegrityError` escapes with both claims held); recorded not widened. [[p3s14-done-17jul]]
- ✅💰 **E4/W10 ✅ VERIFIED IN PROD 21-Jul** (deployed 20-Jul `a266432`) — first `RESET_PNL` **+18.82 = −Σpnl_delta**, NOT 21.04 old (Σcosts 2.22); zeroing −0.000000, A3 GOOD ⇒ reader returns NET in prod. Shape ≠ 20-Jul 18.29/19.61 (diff book). [[e4-w10-deployed-20jul]]
- 🔬❓ **[W10 workarounds still needed? (23-Jul §D)](w10_workaround_still_needed_23jul.md)** — QUESTION not finding; the double-subtract that justified avoiding the reader is now fixed. Reader-by-reader (recon block STILL must avoid it: RESET_PNL). NOT acted. [[e4-w10-done-17jul]]
- **X3-retirement** (`daily_report` + `fetch_daily_candles`) — BLOCKED on W1 + a Candles/Capital keep-or-lose decision. [[batch3-done-17jul]]
- **S5-tail** — per-job functional criteria for the **7 jobs reading reconciliation/CAPITAL state**; 27 are execution-only. Decide each, never bulk. [[s1s3s5-done-17jul]]

## RAMA-ACTIONS owed
- 🔴 **ROTATE the Telegram token** (`@Trade_sysbot`, compromised-at-rest) · 2FA seed VM-only · offsite backup · disable rpcbind · SSH → Tailscale-only (C1 re-baseline first) [[sweep-done-17jul]]
- 🔴 **D1–D4** (⚠️ D1 carries a corrected claim — the Rs990 direction) [[throttle-selection-record-correction-19jul]] · `require_hmac` → **KEEP FALSE**, REFUSED 20-Jul [[require-hmac-keep-false-20jul]] · arm `pre-receive`? → **NOT as-is** [[pre-receive-hook-newline-bug-20jul]]
