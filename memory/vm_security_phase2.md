---
name: vm_security_phase2
description: VM Security Manager Phases 2+3 (copy protection + EOD integration) — DONE 20-Jun (b58dfca→a24ae24); DETECTION-ONLY live on VM (auditd rules + checks; test bypass→email verified); System Manager 9th check + Cron Officer watcher supervision + 1-email-per-CRITICAL fix; blocking wrappers staged (install script to enable hard-block)
metadata: 
  node_type: memory
  type: project
  originSessionId: e7a6af13-236a-41d8-aca5-213b591647fd
---

**VM SECURITY MANAGER PHASE 2 — COPY PROTECTION (VM→PC). BUILT + pushed 20-Jun-2026, commit
b58dfca.** Code is in git + on the VM working tree; the OS-level ENFORCEMENT is **NOT yet
activated** (see "Activation" below). Builds on [[vm_security_phase1]]; alert-first, never breaks
SSH/git. Origin spec = Rama's Phase 2 order.

## What it does (priority model)
`scripts/copy_gate.py` = the policy brain. `check_copy_allowed()` in STRICT priority:
1. **TIME-LOCK 18:00–08:00 IST — ABSOLUTE** (overrides everything, incl. the OFF switch AND a live
   token). Top-priority rule per Rama.
2. master switch OFF (`copy_protection.enabled=false`) → copies unrestricted (disabling is what alerts).
3. session cap (`max_sessions_for_copy`, default 2) → over limit blocks.
4. a valid **15-min token** must exist → else block.
Token store `data_store/security/copy_token.json` (atomic); audit log
`data_store/security/copy_audit.log` (JSON-lines: COPY_TOKEN_ISSUED/REVOKED, COPY_ALLOWED,
COPY_DENIED_*). Both gitignored (data_store/). Config = **`copy_protection:` block in the standalone
`config/security.yaml`** (NOT system_config.yaml — that loader is extra=forbid).

## Components
- `scripts/request_copy.py` — `request-copy <reason>` mints a 15-min token (audited + Telegram INFO);
  `--status`, `--revoke`. Refuses during time-lock / over session-cap (WARNING alert).
- `deploy/security/bin/copy-guard` — wrapper symlinked as `/usr/local/bin/{scp,sftp,rsync}`. Runs
  `copy_gate.py --enforce` then `exec`s the REAL `/usr/bin/<tool>` on allow. **FAIL-SAFE: blocks if
  the gate can't be consulted.** Hard-blocks **VM-INITIATED** copies only.
- `deploy/security/bin/request-copy` — `/usr/local/bin/request-copy` launcher.
- `scripts/security_monitor.py` — gained **checks 8 & 9** (now 9 total): (8) `copy_protection` ON→OFF
  transition → CRITICAL (who=SSH peers/when); (9) auditd `copy_attempt` bypass → CRITICAL (an
  outbound scp/sftp/rsync run with no token). Conservative: skips inbound `scp -t` sinks so PC→VM
  pushes (docx sync) don't false-fire. Reads auditd via `sudo -n ausearch -k copy_attempt`
  (ausearch is on the sudo whitelist → no self-alert). Both checks degrade to no-op if auditd/ss
  absent. The live security-watcher (60s) already runs these harmlessly post-push (no rules loaded yet).
- `deploy/security/trading-security.rules` — added auditd execve rules (`-S execve -F exe=/usr/bin/{scp,
  sftp,rsync} -k copy_attempt`).
- `deploy/security/install_copy_protection.sh` — **idempotent installer** (`--uninstall` reverses).

## KEY LIMITATION (told Rama)
Hard-block only covers **VM-INITIATED** copies (VM is the scp client; the wrapper sits in PATH). A
**PC-INITIATED pull** (PC is the client, the VM's sshd serves it via the real binary / sftp-server,
never the wrapper) **cannot be hard-blocked** from the VM without risky `ForceCommand`/sftp-subsystem
changes on the LIVE trading VM → those are **detect+alert only**. Also modern scp uses the sftp
subsystem (not `scp -f`), which the execve rule may not catch → reliable pull-detection needs the
deferred `Subsystem sftp internal-sftp -l INFO` logging (Phase 3 / Rama's call).

## Activation state — HARD-BLOCK ACTIVE (20-Jun 14:00)
**Detection-only first** (auditd `copy_attempt` rules + checks 8/9 live; raw outbound scp/sftp/rsync →
CRITICAL), **then HARD-BLOCK activated** at Rama's go-ahead (Sat 14:00, markets closed, service down).
`bash deploy/security/install_copy_protection.sh` symlinked `/usr/local/bin/{scp,sftp,rsync}` →
`copy-guard` + `/usr/local/bin/request-copy`. `/usr/local/bin` precedes `/usr/bin` in PATH so a
VM-initiated copy hits the gate. **Verified live:** no-token `scp` → DENIED exit 1 (real scp never
ran); `request-copy '<reason>'` → 15-min token → `scp` exit 0 (real binary reached); **git push + ssh
confirmed UNAFFECTED** (this commit deployed fine; ssh used throughout). Pre-checks: no cron / hook /
systemd uses scp/rsync/sftp. Fail-safe = block-on-error. **Workflow: `request-copy '<reason>'` before
any VM→PC copy.** **Rollback: `bash deploy/security/install_copy_protection.sh --uninstall`** (removes
symlinks; real `/usr/bin` binaries untouched; auditd rules stay).

(Hard-block install was the `install_copy_protection.sh` step above — now DONE; the script's
`--uninstall` is the rollback.)

## Copy approval is TELEGRAM-INDEPENDENT (verified 20-Jun, commit cd85994)
**Copying works with Telegram banned (IN, until 23-Jun) — confirmed live.** The token is a LOCAL file
(`data_store/security/copy_token.json`) written + audited to `copy_audit.log` BEFORE `send_alert`; the
gate decision is purely local (time-lock/switch/session/token); `send_alert` is best-effort (try/except,
never blocks the token). So `request-copy` + the wrapper need ZERO Telegram. Proven: `request-copy` →
token granted + `scp` succeeded with Telegram down. **Email fallback added:** `copy_gate.send_alert`
INFO "token issued" / WARNING denials were Telegram-only → now write a sentinel (→ alert-watcher email)
for ANY tier when Telegram didn't deliver (via `result.sentinel_path`/`success`), `context.severity`
keeping the subject correctly labelled; NO email when Telegram is up; CRITICAL still one email. Security
CRITICALs (bypass / protection-disabled, via `security_monitor._send`) already emailed. So the full copy
audit trail reaches **email** while Telegram is down. The durable audit is always `copy_audit.log`
(local) + the daily System Manager EOD report regardless.

## Live findings on the aarch64 VM (commit 7129b38)
The VM is **aarch64** (not x86_64); the auditd `-F arch=b64` rule still works (b64 = native 64-bit →
captures scp execve, confirmed). Two parser bugs found + fixed during activation: (1) real
`ausearch -i` prints a **2-digit year** (`audit(06/20/26 …)`) — parser now accepts 2-/4-digit; (2)
`ausearch` **blocks reading stdin** when it inherits a pipe/tty (hung over ssh) — `ausearch_copy_attempts`
now passes `stdin=DEVNULL` and queries with the locale-proof `-ts recent` (a computed MM/DD/YYYY can be
rejected on 2-digit builds → silent no-op). Lesson: **always run `sudo ausearch … </dev/null`** when
testing over ssh.

## Detection-only ACTIVATED + test bypass seen (20-Jun)
Loaded the auditd `copy_attempt` rules on the VM (NO wrappers — Rama chose detection-only; verified
`/usr/local/bin/{scp,sftp,rsync}` absent, `which scp`=/usr/bin/scp, 3 rules loaded). Fired ONE
controlled test bypass (`scp … CLAUDE_TEST_BYPASS_IGNORE@198.51.100.7`): the watcher raised a real
**CRITICAL "COPY BYPASS DETECTED" → email `.delivered`** (confirmed). In detection-only every
VM-initiated outbound copy alerts; `request-copy` suppresses it (token-window correlation).

## Phase 3 DONE (20-Jun, commits 202b98f + bb351e0 + a24ae24)
**(A) Double-email fix** — security CRITICALs now email EXACTLY ONCE: `security_monitor._send` +
`copy_gate.send_alert` write their own sentinel ONLY when `TelegramNotifier.send()` didn't (checked via
`result.sentinel_path`); preserves email when Telegram is OFF/disabled (the sole channel till 22-Jun;
Telegram banned). **(B) System Manager 9th check** `security_check` (18:45): copy-audit summary +
**bypass/disable = VIOLATION** (escalates the EOD report to CRITICAL→email + exit 3, but **NEVER trips
the trading SOFT_KILL** — security ≠ trading halt) + health (auditd rules loaded / `enabled` / log
writable / watcher alive via `security_state.json` freshness). `security_monitor` persists fresh
bypass/switch findings to `copy_audit.log` = the single EOD source. **(C) Cron Officer** `--eod-summary`
supervises the security-watcher heartbeat (state-file freshness; escalates to CRITICAL if stale/down).
Verified live (9th check: 3 rules / enabled / watcher alive; cron line renders).

## Tests / status
All security unit tests green: `test_copy_gate.py`, extended `test_security_monitor.py`,
`test_system_manager_security.py`, `test_cron_officer_security.py`. (Pre-existing
`test_system_manager.py::test_report_integrity_*` fails on any day ≠ 2026-06-19 — date-hardcoded, NOT a
regression; confirmed via stash.) Related: [[vm_security_phase1]], [[vm_security_audit_19jun]],
[[task_5_system_manager]], [[task_3_cron_officer]].
