---
name: instruments_staleness_incident_21jun
description: "config/instruments.csv stale 7 weeks (03-May→21-Jun) — caught by Pre-flight's first authentic dry-run; root cause FIX-189 + git-tracked-clobber; audit clean"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b70d7c0-75fd-4f0b-9d69-93adc5e82b95
---

**config/instruments.csv was stale 2026-05-03 → 21-Jun-2026 (~7 weeks)** on the VM.
Caught by the **Pre-flight Phase-A `kite_instruments_fresh` check on its first authentic
dry-run** (21-Jun Sunday) — the entire ops chain missed it for 7 weeks. See [[cron_officer_revision_20jun]] / FIX-189.

**Root cause — two layers:**
1. **PRIMARY: FIX-189** (cron's dash couldn't source `.env`) silently killed cron jobs.
   `refresh_instruments` (09:00 Mon-Fri, writes config/instruments.csv via RI13/atomic
   os.replace) hadn't executed since ~03-May. Evidence: `logs/cron-refresh-instruments.log`
   did not exist (no run in the 30-day log-retention window) + heartbeat NEVER. FIX-189
   fixed 19-Jun (mid-day, so that morning's jobs were still broken) → **first post-fix
   Mon-Fri 09:00 run = Monday 22-Jun.**
2. **LATENT (deeper): config/instruments.csv was git-TRACKED.** The deploy hook runs
   `git checkout -f`, which would silently revert any fresh write back to the committed
   03-May version on the next push. (Not clobbering *yet* only because no refresh had run
   to create a diff.)

**Why unnoticed 7 weeks:** check_cron_drift / Cron Officer heartbeats were broken by the
SAME FIX-189 + under revision (20-Jun) → no missed-job alert. Cron Officer revision restored
monitoring going forward.

**Trade audit (Sunday 21-Jun, read-only): ✅ NO impact.** 63 trades / 49 unique symbols
since 03-May — **all equity (lot_size=1, which never changes), none missing from the CSV.**
The 29 FAILED trades are dated 15-18 Jun = the FIX-190/IP-403 incident window (staleness
would manifest as symbol-not-found, of which there were zero). Token-level Kite comparison
deferred to Monday (no Sunday token) but practical risk nil. See [[fix_190_incident]].

**Phantom-job sweep (Step 5):** besides refresh_instruments, `fetch_fno_ban` (08:35) +
`premarket_healthcheck` (08:30, being retired) also show NEVER-heartbeat — all morning jobs
in the FIX-189 mid-day-Friday shadow; first post-fix run Monday. `daily_report` NEVER =
known Bug C (no heartbeat by design). `backup_restore_drill` monthly (next 01-Jul). Logged
as verify-on-next-run tickets, not fixed (scope discipline).

**Permanent fixes applied 21-Jun (commits 2b4d976, c3c1242):**
1. `git rm --cached config/instruments.csv` + `.gitignore` — stops the deploy-clobber.
   (NB: the rm+`checkout -f` DELETED it on the VM; restored from history `3b72253:` →
   now ignored+untracked so deploys leave the VM's daily-refreshed copy alone.)
2. `refresh_instruments.py` post-write assertion (`_check_fresh_write`) → exit non-zero on
   a silent no-write (caught by heartbeat/marker). PRODUCTION change, active Monday.
3. `check_cron_drift` verified live post-FIX-189 (runs, exit 0, scheduled 18:00 Mon-Fri).
4. Pre-flight `kite_instruments_fresh` graded by TRADING-days-behind (PASS td0 / WARN td1
   refresh-pending / CRITICAL td≥2) — no Monday false-CRITICAL; threshold NOT loosened.

**Monday 22-Jun = live proof:** 09:00 refresh writes a fresh instruments.csv (mtime today,
persists across deploys now), `cron-refresh-instruments.log` appears, Cron Officer 09:20
shows refresh_instruments ✅; also confirm fetch_fno_ban runs. Pre-flight Phase A (08:30,
pre-refresh) shows the restored file as td1 → WARN (expected), not CRITICAL.
