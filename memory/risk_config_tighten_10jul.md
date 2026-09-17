---
name: risk_config_tighten_10jul
description: "10-Jul risk-config tightening (min_pass_score 55->60, max_consecutive_losses 5->4) — pushed while market open, restart deferred"
metadata: 
  node_type: memory
  type: project
  originSessionId: af4824f1-41e0-4c1f-b881-49265a715b87
---

Rama-directed tightening of two risk parameters, committed `61ae9cc` and pushed
10-Jul ~10:05 IST:
- `config/scoring_weights.yaml` `min_pass_score` 55 → 60
- `config/system_config.yaml` `risk.max_consecutive_losses` 5 → 4

Both are single-source (all 15 strategy YAMLs carry `min_score: 0`, deferring to
the global value; no other hardcoded duplicate). Kept in sync: `capital/risk_engine.py`
docstring example (explicitly commented as "aligned to the live config") and
`docs/CONFIG_GUIDE.md` "Current" callouts (also fixed a pre-existing stale "2
losses" figure in its summary table). 205 targeted tests green (config loader,
risk engine, screener, quality scorer, signal processor).

**Why this matters / context for future-me:** `min_pass_score` was deliberately
*lowered* 60→55 only 4 days earlier (06-Jul, commit `8a3e0b7`) after 60 was
causing an "all-signals-rejected" problem live on the VM. Rama's 10-Jul ask to
raise it back to 60 reverses that — told Rama this at the time; treat it as a
deliberate, informed re-tightening, not something to "fix" by lowering again if
signal flow looks thin. If a signal drought reappears, the fix is investigating
*why* (has whatever caused the 06-Jul rejection wave recurred?), not silently
re-lowering the floor.

Separately, `docs/temp_config_tracker.md` (stale, last touched 03-Jun, pre-live)
had once floated `max_consecutive_losses` prod-target=4 as a paper-testing-era
plan that was apparently never executed (git blame shows the value was 5 from
the initial v2 foundation commit onward, never touched again until this
commit) — coincidental independent corroboration that 4 is a reasonable
value, not a load-bearing citation.

**Deploy state (as of 10-Jul ~10:05 IST):** pushed to origin/bare-repo; VM
working tree confirmed updated (`grep` on the VM shows 60/4). `deploy_preflight.py`
refused the restart — VM reported MARKET OPEN (10:05 IST; NSE closes 15:30 IST
per `system_config.yaml trading_hours.market_close`) and this is a market-gated
action (no mid-session `trading-system.service` restart — could disrupt live
positions/in-flight orders/reconciliation). The running process has been up
since 08:15 IST today (NRestarts=0) and still has the OLD values (55/5) loaded
in memory until restarted. `core/config_auditor.py` only runs at startup +
the scheduled 08:30 preflight — no live intraday process compares disk-vs-loaded
config, so leaving the push in place unrestarted through the rest of today's
session is safe (no false-alert risk).

**Restart is the one owed step** — see [[unpushed_pending_deploy_ledger]] DEPLOY-PENDING.
Either a manual restart after 15:30 IST today, or let tomorrow's automatic 08:15
restart pick it up naturally.
