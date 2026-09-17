---
name: min_score_floor_55_06jul
description: "06-Jul: min_pass_score 60→55 (all strategies) — LIVE VM config edit + restart, floor moved to 55. NOW COMMITTED `8a3e0b7` (deploy-safe); push pending (Rama)."
metadata: 
  node_type: memory
  type: project
  originSessionId: eb1e5157-79f2-4b1e-85be-8679efbceb60
---

**06-Jul-2026 ~11:20 IST — score floor LOWERED 60→55 for ALL strategies (LIVE, Rama-requested).** Reason: 0 trades today; **494 of 1,032** signals (48%; 423 at exactly 59) were `REJECTED_SCORE` in the 55–59 band, just under the 60 floor. Supersedes [[min_score_floor_60_26jun]].

## Single authoritative key
`config/scoring_weights.yaml` → `min_pass_score: 60` → **55**. ALL 16 `config/strategies/*.yaml` have `min_score: 0` (the 26-Jun memory's "set to 60" claim is STALE), so per `screening/secondary_screener.py:251-256` `effective_min = strategy.min_score if strategy.min_score>0 else score_result.min_pass_score` → every strategy falls back to the global `min_pass_score`. **One key = all strategies.** No paper/live fork (mode-agnostic), no hardcoded 60 in the screener.

## Done (live, market hours)
1. VM live edit only; backup `/home/ubuntu/scoring_weights.yaml.bak-premin55-1106`; PyYAML-validated (min_pass_score=55); steps/tier thresholds untouched.
2. `sudo systemctl restart trading-system.service` (Rama-approved; 0 open positions; passwordless sudo works). WARM restart, clean: `run_all_startup_checks OK warnings=[]`, waitress `:5000` up @11:20:14, `check_config_hash: scoring_weights.yaml changed`, kill-switch clear, ~12s webhook downtime.
3. VERIFIED live: post-restart **max REJECTED_SCORE = 54** (was 59); **55–59 band rejects = 0**; signals scoring 59 (ABDL/ARTEMISMED/RADICO/LODHA/SBCL…) now `PASSED score=59`. Binding gates now = entry-throttle(20s min-gap)/sizing-concentration/circuit-proximity/**position-cap(max=5)**, NOT score.
4. Downstream (Rama's goal met): trades now flow — **1 OPEN** (PICCADIL positional_sector_rotation, protected: ENTRY COMPLETE + SL OPEN + TGT OPEN) + several FAILED = `entry_cancelled_zero_fill` (limit entries that didn't fill; reservations released cleanly; **no naked positions, no leaks**; no CAPITAL_DRIFT escalation).

## ⚠️ PERSISTENCE — VM edit is LIVE but EPHEMERAL
VM working tree is NOT a git repo (post-receive `checkout -f`), so a deploy overwrites `scoring_weights.yaml` with the committed value. **RESOLVED 06-Jul eve: `config/scoring_weights.yaml`=55 COMMITTED `8a3e0b7`** (isolated config commit) — the deploy now carries 55, no revert. VERIFIED at commit time: VM live=55, git-HEAD `58ff1e7`=60 → the commit closes the gap. **Push still pending (Rama `git push origin main`)** — until pushed, the bare repo is at 60, but the VM live file is already 55 and only a deploy (post-push checkout-f) touches it. **Keep at 55 until Rama says otherwise.** Revert path: restore the `.bak` on the VM (or set 60) + restart.

## Efficacy note
Score was NOT the only blocker — capital/sizing (Rs 10k), entry-throttle, concentration, circuit-proximity, and the 5-position cap still gate. Lowering to 55 removed the SCORE wall; trades depend on limit-entry fills + these caps.
