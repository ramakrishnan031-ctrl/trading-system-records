---
name: cron-framework-armed-23jun
description: Self-maintaining cron framework ARMED 23-Jun (registry→generate→canonical→post-receive auto-install + watchdog); pre-receive DEFERRED
metadata: 
  node_type: memory
  type: project
  originSessionId: e1a15ec3-5140-4531-93b5-a58f94e7260a
---

Self-maintaining cron framework activated **2026-06-23 (~19:00 IST)**, VM bare HEAD `79c70e8`. `config/cron_registry.yaml` is the SINGLE EXECUTABLE SOURCE OF TRUTH; `scripts/generate_crontab.py` deterministically generates `deploy/cron/trading-system.cron` (ASCII+LF, host-independent — fixed VM-path constants). Modes: `--generate` / `--gate` (PROOF 1: zero drops, only `sentinel_retention` added) / `--selftest` (parse↔compose byte-equal round-trip) / `--bootstrap` / `--check`.

**Equality model:** live `crontab -l` == canonical == `generate(registry)`. Verified **four-way SHA256 `1469f905…b9a23`** (PC committed, PC generated, VM deployed, VM live). **41 command-lines** (was 40 + new `sentinel_retention` 02:05).

**ARMED (Rama ran the sequence, 23-Jun):**
- **post-receive** (`~/trading-system.git/hooks/post-receive`, 1336 B, exec; from `deploy/hooks/post-receive`) — every push to `main` regenerates from the *deployed* registry and auto-installs the crontab IF `generate==canonical`, else WARNs + skips (self-protecting). Replaced the old 329-B checkout-only hook. Proven by empty test push `79c70e8` → zero drift.
- **cron-watchdog** systemd timer (`/etc/systemd/system/cron-watchdog.{service,timer}` from `deploy/systemd/`) — Tier-2 watch-the-watcher, runs `scripts/cron_watchdog.py` via venv python; fires **19:30 IST daily** (`Persistent=true`), asserts `cron_officer_eod` + `check_cron_drift` BOTH heartbeated today (market days); missing → CRITICAL sentinel via the **cron-INDEPENDENT** path (alert-watcher emails). First run **Wed 24-Jun 19:30**.

**DEFERRED by choice — NOT installed (23-Jun):**
- **pre-receive** (`deploy/hooks/pre-receive`) — would hard-reject a push whose committed canonical != `generate(registry)` (+ blast-radius bound; override token `[cron-canonical-override]`). Arm later: install + chmod +x, inject `CRON_GUARD_DRYRUN=1` into the *installed* copy (dry-run logs-only) → clear the line to enforce. Break-glass: `rm ~/trading-system.git/hooks/pre-receive`. **Until armed, post-receive still stops a bad canonical reaching the live crontab — it just won't reject the push.**
- **pre-commit** (`deploy/hooks/pre-commit`) — optional, local clones only; not on the VM.

Pre-arm gates **G1–G4 all passed** (G1 zero-drops, G2 canonical==generate, G3 hooks/watchdog exec+shebangs, G4 canonical ASCII+LF) and re-proven natively on the VM at push/reconcile. **Today's `check_cron_drift` heartbeat is absent** only because today's 18:00 drift-check ran on pre-deploy code that didn't self-heartbeat (`scripts/check_cron_drift.py:197-198` self-heartbeats in the deployed code) — benign, self-corrects at tomorrow's 18:00; **do NOT manually start cron-watchdog today** (would false-CRITICAL). See [[cron_officer_revision_20jun]], [[task_3_cron_officer]], [[deploy_requires_restart]].
