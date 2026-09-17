---
name: deploy_a2_b1_gui_03jul
description: "03-Jul ~17:25 IST off-market deploy EXECUTED: A-2+B-1(shadow)+GUI live on VM — main 9becf8c→a9d44e0→7b1c92d→2e2b2bb; P1 (schema v42) deliberately NOT pushed; trader inactive → A-2/B-1 activate Mon 06-Jul 08:15; gui-dashboard unit ACTIVE"
metadata: 
  node_type: memory
  type: project
  originSessionId: 05a97712-3f38-461a-8f6d-e1afd35edc10
---

**03-Jul-2026 ~17:17–17:30 IST — tonight-plan EXECUTED (Rama's GO file; all gates GREEN, clean GO).**

**Pushed (origin = trading-vm bare repo; "Deployment complete" ×3, crontab byte-identical `f4242b94…` all three — zero drift):**
1. **Push #1 `a9d44e0`** — `main` ff→ C-1 tip `678c592` (carries **A-2 `fd09a38`** + `aa02f9f` api_key-scrub/.gitignore + audit/design/runbook docs), then **B-1 `f5fd4d9`** `--no-ff`. STEP5 verify on VM: A-2 `except BrokerTimeoutError` ×3 ✓, `daily_loss_include_unrealized: false` ✓, B-1 markers ×4 ✓, schema 41 ✓.
2. **Push #2 `7b1c92d`** — GUI `gui-deploy-03jul`@`33e9223` `--no-ff` (exactly the 79 gated files; ordering (a) honored: batch first, GUI right after).
3. **Push #3 `2e2b2bb`** — docs: SYSTEM_MAP header deploy record + deferred pointers (D-1/B-2/low-sev → [[d1_close_trade_race_design_03jul]] [[b1_unrealized_mtm_design_03jul]] [[audit_lowsev_verify_03jul]]) + PATHS G2a/G2c flipped to DEPLOYED.

**⚠️ P1 `4817032` (EOD broker-reconcile, schema v42) DELIBERATELY EXCLUDED** per Rama's tonight-plan (batch = code-only/no-schema; rollback list = fd09a38·f5fd4d9·GUI only). Verified NOT an ancestor of the C-1 stack. Still unpushed on `fix-p1-eod-broker-reconcile-02jul`; its @15:58 cron NOT installed; the shadow→cutover clock (§5.2/§7, earliest 20-Jul) has NOT started. **Weekend window remains open if Rama wants P1 in** — runbook §2.3 still valid (merge P1 `--no-ff` onto current main; P1-onto-(main+B-1) was proven clean; DB backups already taken).

**Gates (all PASS pre-push):** deploy_preflight PASS (VM market-CLOSED 17:21, skew 3s) · E1 diff gate = 4 buckets/79 files exact · B-1 flag false · schema 41 both branches · both DBs backed up (`data_store/{trading_system,analytics}.db.pre-deploy-2026-07-03`, 256MB+7MB) · trader already inactive (EOD-self-exited).

**Activation:** trader left INACTIVE (not restarted) → **A-2+B-1 go live Mon 06-Jul 08:15 boot**. Monday validation = plan §3 / runbook §4.1 minus P1: A-2 timeout→TIMEOUT-mark+reservation-HELD (rate-limit retry intact), B-1 `_mtm_refresh_success` climbing ~15s + `would_reject_with_unrealized` logs-only + stale→realized-only+WARN, clean boot/prepass/invariant.

**GUI live same night (E2 complete):** overlay was auth-only (STEP-3 paste pending) → I appended the INSTALL §2a production block on the PC **without reading the file** (no secrets in transcript), scp'd, chmod 600, §2b name-only 3+5 PASS. venv built, **I4 PASS (no kiteconnect)**. Manual smoke 302→/login. Unit `gui-dashboard` enabled+ACTIVE, survives pushes (overlay git-ignored, re-verified after push #3), binds **127.0.0.1:8500 ONLY** (ss verified), API-noauth→401. **REMAINING: E3 Tailscale (§5, Rama-interactive: `tailscale up` + MagicDNS/HTTPS-certs + `serve --bg`) → soak S1–S8 from Mon 06-Jul (template `ops_dashboard/docs/SOAK_EVIDENCE_TEMPLATE.md`, locked verdict format) → E4 reboot drill (off-market).** Until Tailscale, GUI reachable only via SSH tunnel to 127.0.0.1:8500.

**Rollback:** revert merge commits → 9becf8c; B-1 one-flag fallback stays false; GUI = `systemctl disable --now gui-dashboard`. DB backups in place (code-only batch — backups precautionary).

**SOAK EXECUTION CONTRACT (03-Jul pre-GO addendum, LOCKED — carry verbatim into the Mon–Wed soak; supersedes any free-form assessment. Also in [[gui_g2c_deploy_prep_03jul]] + committed `ops_dashboard/docs/SOAK_EVIDENCE_TEMPLATE.md`@33e9223):**
1. Holding-pattern approval / "Rama pings GO after 17:05" = now MOOT (GO executed ~17:25, pushes landed). Kept for provenance only.
2. **SOAK VERDICT FORMAT (locked, replaces free-form):** the primary question each day = *"Did Rama need Telegram / logs / DB queries / Excel to understand something the dashboard could not show?"* **IF YES** → per instance record (a) exactly what was missing, (b) which screen SHOULD have shown it, (c) proposed enhancement → append to the **F-backlog, F10+ numbering**. **IF NO** → state explicitly: *"the dashboard became the primary operational interface."*
3. **S6 TRADE TRACE = BOTH per day where available:** (a) one successful trade full lifecycle (signal→fill→exit) AND (b) one rejected/failed trade (signal→rejection point; verify the failure shows at the RIGHT pipeline stage AND in the strategy failure strip). No rejected trade that day → **state so explicitly, never fabricate**.
4. No other changes, no new features — everything else per the persisted G2c GO/soak sequence.
