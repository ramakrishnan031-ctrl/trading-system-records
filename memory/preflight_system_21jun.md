---
name: preflight_system_21jun
description: "Pre-flight check orchestrator (scripts/preflight) — 3-phase daily readiness, 55 checks, ALERT-ONLY; ACTIVATED 21-Jun for Monday 22-Jun live proof"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b70d7c0-75fd-4f0b-9d69-93adc5e82b95
---

**Pre-flight check orchestrator** (`scripts/preflight/`) — daily pre-market readiness,
designed + built + ACTIVATED 21-Jun-2026 (Sunday). Monday 22-Jun = first live proof.

**3 phases (cron Mon-Fri):** A 08:30 infra (app DOWN) · B 09:14 engine readiness (app UP)
· C 09:15→09:20 signal-warmup watch (`--watch-sec 285`). **55 checks / 10 groups**: VM,
services, DB, broker (adapter-only; paper→SKIP), config, state, security, recovery,
engine, signals. **ALERT-ONLY** (exit 0 always; Rama is the gate, never auto-blocks).
**Auto-fix only on a DB/OS SAFE whitelist** (in-memory app state = alert-only, a separate
process can't reset it).

**Locked design (forks 21-Jun):** F1 infra-in-A / engine-in-B-C; F2 in-memory=alert-only,
DB/OS=auto-fix; F3 premarket_healthcheck SUBSUMED by Phase A (5 checks ported + parity-
tested; script kept w/ deprecation header, **delete after Mon+Tue proof**).

**Key files:** base.py (Check contract) · orchestrator.py (`--phase A/B/C --dry-run
--as-of-date --watch-sec`) · sentinel.py (`data_store/preflight/today.json`) · autofix.py
(whitelist, idempotent, timeout, JSONL audit) · report.py (HTML/Telegram/plaintext, reuses
Cron Officer cosmetics) · deliver.py (email on CRITICAL/phase-C + Telegram outside ban) ·
startup_hook.py (on-demand A/B if a 06:00-09:20 restart missed the cron) · checks/*.py.
Engine readiness attested via the app's `:8080/health` + `/metrics` + DB (no in-memory
introspection). ~150 tests.

**Integration:** Cron Officer morning briefing embeds a pre-flight banner (reads the
sentinel; NOT_RUN/stale → briefing CRITICAL). See [[cron_officer_revision_20jun]].

**Schema v33** (`EXPECTED_SCHEMA_VERSION=33`): 3 NEW append-only tables (preflight_runs /
preflight_check_results / preflight_autofix_log), pure additions (no MIGRATION_TABLES).
**DB-copy tested on the real 64MB live DB**: 32→33 idempotent, data preserved, integrity ok.
Live DB migrates at the **Monday restart** (armed by the v33 push).

**ACTIVATED (commits 165c845 schema, d1355e8 cron+hook):** crontab reinstalled
(`crontab -l | diff`=0, 3 preflight lines live, 13 markers, premarket gone). NB authentic
Phase-A dry-run signed off 21-Jun; instruments-staleness incident caught by it
([[instruments_staleness_incident_21jun]]).

**STILL PENDING:** Monday 22-Jun live proof (08:30 A email/marker, 09:14 B, 09:15-20 C,
09:20 Cron Officer banner, live DB→v33 on restart); then full SYSTEM_MAP/PATHS + this
entry → LIVE PROVEN; Wed delete premarket_healthcheck.py. CONFIG_GUIDE_Rama.docx pre-flight
section (manual SCP) after live proof.
