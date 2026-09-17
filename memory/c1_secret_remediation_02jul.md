---
name: c1_secret_remediation_02jul
description: C-1 CRITICAL remediation — scrub+scanner DONE; secrets ROTATED 02-Jul (history values now DEAD); full inventory done; git-history purge PLANNED (defense-in-depth, awaits go). Only 9f58848 had real .env.example secrets + LFL836 api_key in 3 scripts
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e62fe89-aead-435f-8580-0a242667edcc
---

Remediation of audit finding **C-1** (real live creds committed in `.env.example` + git history). Follows [[system_audit_02jul]]. Rama rotates all creds at the source (kills the exposure); this is the code/git cleanup. NO real credential values were ever printed.

**A + B = DONE + COMMITTED (isolated).** Branch `fix-c1-secret-scrub-02jul` @ `80da5e6` (off main 59f83b5, **UNPUSHED** — Rama pushes off-market). 4 files, +299/−11:
- **A — scrub:** `.env.example` → pure template; every real value (Zerodha api_key/secret/TOTP for LFL836+DR6114, TELEGRAM_BOT_TOKEN, WEBHOOK_SECRET, + channel/personal-chat IDs) replaced with placeholders (FILL_WHEN_READY / FILL_CHANNEL_ID_1 / FILL_CHAT_ID). Real `.env` confirmed NOT tracked.
- **B — scanner:** NEW `deploy/hooks/secret_scan.py` (pure `scan_content(path,text)` + `scan_staged()`; findings never contain the value). Blocks: telegram bot-token shape, credential-named assignment with a real-looking value (>=16 key-charset / 64-hex / base32), a real `.env`, and a non-placeholder credential in `.env.example`. Conservative (credential-NAMED keys or unambiguous shapes only) → no FP on `LOG_LEVEL=INFO` / `os.environ.get(...)`. Wired FIRST in `deploy/hooks/pre-commit` (robust python auto-detect). Installed to `.git/hooks/pre-commit` on the PC. 11 tests `tests/unit/test_secret_scan.py` (fakes built at runtime so the test file has no literal secret). **PROVEN live:** planted fake secret → commit BLOCKED (exit 1, value redacted); clean C-1 commit → PASSED (scanner scanned itself, no self-trigger).

**Docs left UNCOMMITTED** (PATHS.md, docs/SYSTEM_MAP.md — now carry C-1 + prior T2/audit notes; audit doc untracked) for Rama's off-market doc commit, per the established pattern.

**C = git-history purge — INVESTIGATED, NOT executed (awaits Rama: rotation confirmed + plan approved).** Keys DEAD by then → careful cleanup, not a race.

Topology (confirmed 02-Jul):
- origin = `trading-vm:~/trading-system.git` (VM **bare** repo over SSH). **NO GitHub/public remote** → exposure is private (PC local + VM bare + VM working-tree file); rotation is the real fix.
- **CORRECTED by the 02-Jul inventory:** the ONLY commit whose `.env.example` tree has REAL secrets is **`9f58848`** (10 vars: LFL836+DR6114 key/secret/totp, TELEGRAM_BOT_TOKEN, CHANNEL_PRIMARY, PERSONAL_CHAT_ID, WEBHOOK_SECRET). `bcf03b5` (initial) and `ebf59b7` (5-acct schema) were **placeholders** (`your_…_here` / early style) — NOT real. Exposure window = tree of every commit in `9f58848..7bc3367^`; scrub `7bc3367` (part of deployed `9becf8c`) is clean at HEAD (`FILL_WHEN_READY`). VM bare repo has ONLY `main`; PC has main + feature branches (all share the `9f58848` blob).
- `post-receive`: on push to main → `checkout -f main` to `/home/ubuntu/systems/trading-system` + regen/install crontab iff `generate(registry)==deploy/cron canonical`.
- `git-filter-repo` NOT installed on PC or VM → install first.

Safe purge sequence (execute ONLY after go):
0. Pre: rotation done; C-1 scrub (80da5e6) merged to main + deployed (tip `.env.example` = clean placeholders); BACKUP the PC repo + VM bare repo (`cp -r`) + VM working tree.
1. Install `git-filter-repo` (venv `pip install git-filter-repo`, or the single script).
2. On a FRESH mirror clone (filter-repo best practice): `git filter-repo --replace-text expressions.txt`, where `expressions.txt` maps each DEAD secret literal → `***REMOVED***` (Rama supplies the literals at run time; delete the file after). Rewrites `.env.example` blobs across ALL history; **every SHA from `bcf03b5` onward changes**. (Alt: BFG `--replace-text`.)
3. Verify locally: `git log --all -p -- .env.example` shows only `***REMOVED***`; pickaxe `git log --all -S'<literal>'` → 0 commits.
4. Force-push WITHOUT the deploy hook firing unexpectedly: SSH → `mv ~/trading-system.git/hooks/post-receive{,.disabled}` → `git push --force origin main` → on VM manually resync `git --work-tree=/home/ubuntu/systems/trading-system --git-dir=/home/ubuntu/trading-system.git checkout -f main` (content identical → no restart; deploy≠restart) → `mv` the hook back.
5. Verify on the bare repo: `git --git-dir=/home/ubuntu/trading-system.git log --all -S'<literal>'` → none.
6. PC local repo = the rewritten source; any OTHER clone must re-clone (none known besides PC+VM). Delete `expressions.txt`.

**TRADE-OFF to weigh before purging:** a full-history rewrite changes EVERY commit SHA from the initial commit → all SHA refs in memory/SYSTEM_MAP/docs become historical-only (git log shows new SHAs). Given no public exposure + keys will be dead, purge (clean history, SHA churn, re-clones) vs accept (dead secrets in a PRIVATE repo history) are both defensible — **rotation is the actual fix**; the purge is defense-in-depth. Rama's call.

**Why:** C-1 was the audit's sole CRITICAL. A+B remove the live-tree exposure + prevent recurrence (the old `deploy/hooks/pre-commit` had no secret scan). C is staged for a clean, reversible, hook-safe execution once keys are dead.

---

**INVENTORY + CLASSIFICATION COMPLETE (02-Jul ~20:30 IST, read-only).** Full doc: `docs/audit/c1_credential_exposure_inventory_02jul2026.md` (SYSTEM_MAP + PATHS point to it). Post the 02-Jul rotation ([[post_rotation_creds_02jul]]):
- **6 exposed secrets now DEAD** (rotated): API_SECRET+TOTP for LFL836 & DR6114, TELEGRAM_BOT_TOKEN, WEBHOOK_SECRET. History values are useless.
- **2 ACTIVE** (Zerodha keeps the app key, not rotated): `ZERODHA_API_KEY_LFL836` + `_DR6114`. Both **non-authenticating alone** (matching secret rotated + uncommitted). LFL836 api_key is ALSO hardcoded in 3 tracked scripts at **HEAD** (`scripts/fetch_daily_candles.py:30`, `gemini_data_integrity_check.py:45`, `reconstruct_excursions.py:61`) — a separate live-tree exposure to clean (move to `os.environ`).
- **2 IDENTIFIERS** (not secrets): TELEGRAM_CHANNEL_PRIMARY, PERSONAL_CHAT_ID.
- Real `.env` NEVER tracked ✅. **SMTP password value NEVER committed** — only the env-var NAME in docs/config (one placeholder `app_password_here`); value is VM-.env-only.
- Prevention (4c) already LIVE at HEAD: placeholder `.env.example`, gitignored `.env`, secret-scan hook. Residual gaps: scanner doesn't scan `.xlsx`; scripts hardcode the api_key.
- **Net residual risk = LOW–MODERATE** (internal-only remote + rotated secrets + non-authenticating api_keys).

---

**C-1 COMPLETION (02-Jul ~21:00 IST) — committed `aa02f9f` on branch `fix-c1-completion-02jul` (stacked on A-2 `fd09a38`, UNPUSHED).** Held for Rama's off-market push. 150 tests green. Three parts:
1. **Scripts fixed (permanent):** the hardcoded LFL836 api_key removed from `scripts/{fetch_daily_candles.py, gemini_data_integrity_check.py, reconstruct_excursions.py}` → now `os.environ.get("ZERODHA_API_KEY_LFL836")` behind `load_dotenv(ROOT/.env)` (the reconcile_positions.py / auto_refresh_token.py pattern — cron-safe, rotation-surviving; each errors clearly if unset). No hardcoded key anywhere in the tree now; verified env-resolves len16. So a future api_key rotation needs only a `.env` update.
2. **.xlsx scanner gap CLOSED:** `deploy/hooks/secret_scan.py` gains `scan_xlsx` (parses cells via openpyxl, same secret shapes, **FAIL-CLOSED** on unparseable) + `.xlsx` routed as bytes in `scan_staged` (previously null-byte-skipped → `credentials.xlsx` bypassed it). Paired with the `.gitignore` credentials.xlsx entry. 4 new tests (15 total, runtime fakes) + proven live (staged fake .xlsx → BLOCKED, value redacted).
3. **History-purge RUNBOOK written (not executed):** `docs/audit/c1_history_purge_runbook_02jul2026.md` — exact git-filter-repo procedure for the bare-repo deploy model (backup → mirror rewrite of `.env.example`@9f58848 vals + the api_key literal → force-push with post-receive disabled → re-checkout VM worktree → re-clone PC → rebase unpushed branches → verify → rollback; ~15–30min off-market, zero trading impact). LOW urgency; do before any public push, bundle with optional api_key rotation.

**Still OUTSTANDING (Rama's ops call):** optional regenerate the 2 api_keys in Kite console (bundle with purge); execute the purge. Prevention now fully live (placeholder .env.example + gitignored .env + secret-scan hook incl. .xlsx). Related: [[post_rotation_creds_02jul]], [[ref_security_audit_02jul]].
