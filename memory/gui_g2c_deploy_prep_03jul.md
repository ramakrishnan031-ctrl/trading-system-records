---
name: gui_g2c_deploy_prep_03jul
description: "G2c VM deploy — STEP 0 gates PASS + merge-gate branch ready (gui-deploy-03jul @ 853cad2); PUSH HELD at the 1.4 STOP pending Rama's ordering call vs the security batch"
metadata: 
  node_type: memory
  type: project
  originSessionId: 157eab85-5916-43a3-9c57-323a11cc5b69
---

Ops Dashboard **G2c IN PROGRESS** (03-Jul-2026, ~04:30 IST). Follows [[gui_g2b3_ui_polish_03jul]] (ACCEPTED; **Q3 LOCKED: reports download stays FALSE**, revisit post-soak). Locked decisions + **F1–F9 future backlog recorded in mempalace** (roadmap only: F1 replay timeline · F2 explain-why chain · F3 snapshot compare · F4 lifecycle periods · F5 download revisit · F6 journal · F7 CSV · F8 trends · F9 unrealized/LTP).

**STEP 0 — live VM measurements (04:14 IST, read-only): BOTH GATES ASSESSED.** G0a **PASS big**: 11Gi total RAM, **11Gi available**, 2 vCPU, **83G root free** (15% used) — the documented 2GB floor was stale; Python 3.12.3. Units: trading-system inactive (pre-08:15, normal), token-watcher active, alert/security-watcher "activating" (periodic-oneshot pattern, documented normal), watchman inactive (BindsTo), cron-watchdog.timer active. fail2ban: 1 jail (sshd), 0 currently banned, 14 total. auditd live: **11 `-w` watches + 3 copy_attempt execve** — matches G0 §6.2 exactly. G0b: listeners = `:22` sshd, `:53` resolved (loopback), **`:111 rpcbind on 0.0.0.0` — FINDING: pre-existing stock portmapper, NOT GUI-related → reported + parked to VM-hardening (with Q2)**; `:5000/:8080` absent because the trader is down (they are in-process daemon threads — G0 fact).

**STEP 1 — merge gate DONE to the 1.4 STOP.** `gui-deploy-03jul` created via **`git rebase --onto origin/main fix-p1-... gui-g2b3-03jul`** (chosen over cherry-pick: one command, preserves the 4-commit chain) — clean, zero conflicts (the GUI chain's SYSTEM_MAP/PATHS context matched 9becf8c since fix-p1 never touched them). **HARD GATE PASS**: `git diff origin/main --name-only` = ops_dashboard/** + docs/gui_project/** + docs/SYSTEM_MAP.md + PATHS.md ONLY (77 files, verbatim in report). **240 tests green** on the rebased branch (+2 overlay tests).

**STOP at 1.4 (mandated: "merge entanglement → STOP"):** pushing GUI to main breaks the VERIFIED security-batch runbook [[offmarket_deploy_runbook_final_03jul]] which assumes main==9becf8c (C-1 `--ff-only` step + the 08:15 boot-gate `HEAD==9becf8c` check — TODAY). **Both orderings proven content-CLEAN via merge-tree sims** (GUI onto post-batch main = CLEAN; C-1 onto main+GUI = CLEAN — no file-region overlap even in SYSTEM_MAP/PATHS). **RECOMMENDATION (a): security batch first** (tonight after 17:05 / weekend, runbook untouched), **GUI push immediately after** (`git merge --no-ff gui-deploy-03jul` onto the new main) — zero runbook impact, zero calendar cost (VM setup same evening; soak starts Mon 06-Jul either way). Option (b) GUI-first works content-wise but requires amending the verified runbook + contaminates today's boot-gate evidence — not recommended.

**Deploy-prep committed (`853cad2`, ops_dashboard/** only — gate re-verified PASS):**
- `deployment/gui-dashboard.service` — User=ubuntu, WorkingDirectory ops_dashboard, ExecStart venv/bin/python -m backend.app, Restart=always/10s, After=network.target, **NO BindsTo/Wants on trading-system** (GUI survives trader restarts; trader-down banner is a feature). Manual install only.
- **`gui_config.local.yaml` overlay** (git-ignored + chmod 600): `load_gui_config` now deep-merges it over the committed base — **closes the gap where post-receive `checkout -f` would clobber VM paths + auth secrets on every future push** (the phase plan had secrets in the tracked file — foreseeable incident, fixed permanently). `auth --setup --config <local>` creates the file if absent.
- `INSTALL.md` = living runbook: venv + I4 pip-show gate, overlay values (VM abs paths, **`session_cookie_secure: true`** — the G2a lock, `reports_download_enabled: false`), Rama-present auth setup (never echo secrets), smoke curl→302, Tailscale install/up/MagicDNS+HTTPS-certs click-path/`serve --bg https / http://127.0.0.1:8500`, unit install, reboot drill (off-market), rollback (disable unit + `tailscale serve reset`).

**Rama-loop queue:** (1) push-ordering decision → then I execute: push, VM venv (2.1), overlay (2.2); (2) 2.3 auth --setup on VM w/ Rama typing password + TOTP QR; (3) 3.1 `tailscale up` browser auth into HIS tailnet; (4) 3.2 admin console: DNS→MagicDNS enable, DNS→HTTPS Certificates→Enable; (5) reboot-drill timing (off-market/weekend); (6) soak S1–S4 ≥3 market days (Mon 06 – Wed 08 Jul) then the evidence table. NOT RUN yet: STEPS 2–5. After soak PASS → G3.0 control-plane investigation.

**G2c-CONTINUE (03-Jul ~09:52 IST): ORDERING (a) LOCKED by Rama** (batch first per its runbook untouched,
then GUI `--no-ff`; pushes outside 15:30–17:05, batch window = after-17:05-Fri/weekend). Part-1 review:
STEPS 0–1 + 1.4 STOP ACCEPTED; overlay Deviation-2 APPROVED PERMANENT; read-only philosophy re-locked (NO
control in G2c). **Enhanced soak S5–S8 added** (S5 freshness 3×/day vs DB · S6 1–2 real trade traces/day ·
S7 capacity accuracy 2×/day · S8 strategy-badge truth daily; PASS bar 3 clean days; verdict must include
"first-place-I-look" assessment; E3 adds access-documentation requirement to INSTALL.md+SYSTEM_MAP).
**Pre-window gates ALL GREEN @09:52:** STEP-0 boot PASS (logged) · origin/main==9becf8c unchanged · E1 1.2
diff gate PASS (4 buckets/76 files, base 9becf8c) · **full ordering-(a) merge-tree sim CLEAN incl. GUI onto
post-batch main** (678c592→f5fd4d9→4817032→gui-deploy-03jul; final tree 9e91258) · deploy_preflight
correctly REFUSES mid-session (gate armed; PC↔VM skew 2s) · batch runbook DB paths fixed @678c592.
**WAITING for window (17:05+ Fri or weekend) → GO sequence:** re-run preflight+diff gate → VM DB backups
(data_store/!) → batch merges+push+STEP5 verify → GUI --no-ff+push → verify ops_dashboard/ landed via hook
→ E2 venv+overlay to the 2.3 Rama-pause. Nothing pushed yet this session.

**12:32 PART-1/2 UPDATE (pre-GO, [[gui_readiness_g3_0_03jul]]):** readiness verdict = **READY +
DISPLAY-ONLY CONFIRMED** (240 fresh; POST=/login+logout only) → bundle decision input for Rama.
P1.4 credentials.xlsx .gitignore = **already in batch (`aa02f9f`)** — no extra branch/commit
exists or is needed. (Tip e7a6a37 superseded below.)

**13:12 PRE-GO PREP UPDATE: GUI tip now `33e9223`** (docs-only on e7a6a37: INSTALL.md 2.3→
**PC-created credential overlay flow §2a/2b** + rotation/lost-phone recovery §3 + security notes;
`ops_dashboard/docs/SOAK_EVIDENCE_TEMPLATE.md` S1–S8 day-tables + locked verdict block; PATHS/
SYSTEM_MAP pointers). **E1 final diff gate tonight = 4 buckets / 79 files**; ordering-(a) chain
**RE-PROVEN CLEAN vs 33e9223**. Tonight's E2 no longer pauses at 2.3 — the overlay (auth-only +
appended production block) is scp'd + chmod 600 + name-only-verified (INSTALL §2b); Rama's live
GUI involvement = one Tailscale login confirm (§5). **Credential creation on PC = Rama-interactive,
runs in HIS terminal (CLI prints the TOTP secret — must never enter chats/transcripts).**

**13:40 CREDENTIALS DONE + ROTATED:** first attempt's TOTP secret was exposed in a chat →
**treated dead, full rotation run** (INSTALL §3 leak-recovery line exercised in anger); new setup
+ login re-verified by Rama. Artifact verification PASSED (names-only): overlay exists at
`ops_dashboard/backend/config/gui_config.local.yaml` (293B, git-ignored .gitignore:9, repo clean,
base unmodified), all 6 auth keys PRESENT. **⚠️ STEP-3 PASTE STILL PENDING: paths/server/
reports_download_enabled NOT yet in the overlay** — Rama pastes the INSTALL §2a production block
before GO (or §2b verify catches it: the name-only grep expects 3+5). Gates/tip UNCHANGED
(33e9223, 4 buckets/79 files) — GO sequence needs no modification.

**ADDENDUM (03-Jul pre-GO, LOCKED — soak refinements, no other changes):**
1. Holding pattern APPROVED (09:50 refusal correct); GO sequence stands verbatim; **Rama pings GO after 17:05**.
2. **SOAK VERDICT FORMAT LOCKED (replaces free-form):** primary question = "Did Rama need Telegram / logs /
   DB queries / Excel to understand something the dashboard could not show?" **IF YES** → per instance record
   (a) exactly what was missing, (b) which screen SHOULD have shown it, (c) proposed enhancement → **append
   to F-backlog in mempalace, F10+ numbering**. **IF NO** → state explicitly: "the dashboard became the
   primary operational interface."
3. **S6 TRADE TRACE = BOTH per day where available:** (a) one successful trade full lifecycle
   (signal→fill→exit) AND (b) one rejected/failed trade (signal→rejection point; verify the failure shows at
   the RIGHT pipeline stage + in the strategy failure strip). No rejected trade that day → **state so
   explicitly, never fabricate**.
