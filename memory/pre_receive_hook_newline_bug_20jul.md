---
name: pre-receive-hook-newline-bug-20jul
description: The candidate pre-receive hook would false-reject EVERY push (trailing-newline bug in its $()+printf capture); cron content is actually consistent. DO NOT arm as-is. Market-hours guard (guard-1) is sound.
metadata: 
  node_type: memory
  type: project
  originSessionId: b14d1d0c-0ba5-4905-a624-c9bdc6af7245
  modified: 2026-07-20T08:12:35.873Z
---

**`deploy/hooks/pre-receive`'s cron-integrity guard would FALSELY REJECT EVERY PUSH if armed in enforce mode** — verified read-only 20-Jul against `51e6759` on the VM. Report: `docs/audit/pre_receive_hook_investigation_20jul2026.md`. NOT armed; nothing changed. (Hook is currently disarmed — VM bare has only `pre-receive.sample`.)

**The bug (guard 2, `deploy/hooks/pre-receive:53-60`):** `GEN="$(generate_crontab.py --generate …)"` strips the trailing newline (command substitution always does), then `printf '%s' "$GEN" | diff - deploy/cron/trading-system.cron` compares it against a canonical file that legitimately ends in `\n` → last-line mismatch, every push. **PROOF:** post-receive-style `generate | diff -q - canonical` = MATCH rc=0 (content consistent); pre-receive-style = DIFFERS; `od -c` shows both end `…2>&1\n` byte-identical. So it's the hook's shell plumbing, not real drift. Deterministic reject unless `[cron-canonical-override]` in the HEAD commit msg. **Fix (NOT applied — careful-loop):** `printf '%s\n'` at :60, or pipe the generator directly like `post-receive:34`; then dry-run soak before enforce.

**Two guards in the hook:** guard 1 = **market-hours deploy guard** (`market_hours_guard.sh`, FIX-065) — HARD-rejects 09:15-15:30 IST weekday pushes (bypass `[force-deploy]`), fail-OPEN on absence/bad-clock, does NOT honour dry-run, and **IS tested** → **sound + valuable** (structurally prevents deploy-under-live-session, an S4 class). guard 2 = the broken cron-integrity check above; honours `CRON_GUARD_DRYRUN=1`.

**Untested:** no test exercises the hook's shell comparison path (only `test_fix065` [guard-1 .sh], `test_generate_crontab`, `test_check_cron_drift_content` [Python logic] exist) — matches the record's "untested, defaults to enforce."

**Verdict:** DO NOT arm as-is = immediate total deploy lockout, blocking all 3 approved deploys (E4/W10, prune #09, boot-pair). Break-glass = `rm ~/trading-system.git/hooks/pre-receive` (SSH; available whenever a push is, same channel/key); a rejected push leaves NO state (atomic — post-receive never runs, `mktemp` trapped). What the hook buys: guard-1 = real added protection; guard-2 = marginal (post-receive already refuses to install a drifted crontab `post-receive:34-38` + daily `check_cron_drift` alerts).

**Why:** the record listed "arm pre-receive?" as a ready action; it is not.
**How to apply:** before arming — fix the newline capture, arm `CRON_GUARD_DRYRUN=1` first, confirm zero false-rejects on a real push. Then Rama's sequence call (arm now / after queue clears / dry-run / leave) per report §C. No recommendation made.

Related: [[require-hmac-keep-false-20jul]] [[s4-boot-outage-17jul]] [[sweep-done-17jul]] [[feedback-verify-the-finding-premise]] [[project-vm-architecture-locked]]
