---
name: 403-blind-spot-investigation-23jul
description: "The 403 \"blind spot\" investigated read-only — all refusals correct, POSTs already fully audited, no code change needed; the \"outside entry window\" framing was ~half wrong"
metadata: 
  node_type: memory
  type: project
  originSessionId: 25d81ec5-448b-4c6c-9d11-f6da2e15611a
  modified: 2026-07-23T16:34:35.527Z
---

The register's "one genuine blind spot" (~25,960 refused POSTs / ~338k signals) INVESTIGATED
read-only 23-Jul → `docs/audit/refused_posts_403_investigation_23jul2026.md`.
**Verdict: all refusals CORRECT · no lost-signal bug · no RED case · no code change warranted.**

Two framing corrections (both matter):
1. **NOT "outside entry window" for ~46%.** 12,069 of 25,960 historical 403s were emitted
   IN-WINDOW [10:00,15:00) = **kill-switch refusals** (`webhook_receiver.py:513`), not window
   refusals (`:528`). Correct given state (system was halted), but the *reason* is different.
   Proven 3 ways: **code** (in-window POST passes `:527` ⇒ only `:513` reachable ⇒ the RED case —
   in-window 403 with kill inactive — is *inexpressible*), **block-structure** (contiguous
   kill→resume blocks on 7 dates 15-Jun..1-Jul, zero fine interleaving), **system_events**
   (SHUTDOWN/STARTUP/KILL_AUTO_CLEARED timestamps align to the block edges). Debris of the
   late-June HARD_KILL / circuit-breaker instability. **GONE since 1-Jul** — live delta 17-23 Jul
   has ZERO in-window 403s.
2. **NOT a "blind spot."** Every POST IS audited in `webhook_audit` (ts/ip/scanner/size/code).
   Only the INNER-signal *tally* inside refused POSTs is unparsed (body not read pre-gate), and it
   is **estimable from stored `payload_size_bytes` with no code change**. So §B collapses: the
   count already exists read-only.

A4 settled: **99.99% from one Chartink IP** (23.106.53.213 / Leaseweb); **zero 401s** across 89,794
audited POSTs (401s ARE audited — `_handle_webhook:453` finally covers every `_process_request`
return) ⇒ no background noise, endpoint not probed. 401-vs-403 codes correct (pre- vs post-auth),
NOT a `/health` repeat. `kill_switch_state` is single-row STATE (no history); timeline came from
system_events + the 403 block structure.

**Why:** corrects a Core-Reference assumption and closes the last high-value board item — the
investigate→design→ChatGPT→build loop **stops at investigate; there is nothing to build.**

**How to apply:** don't quote "~338k lost signals" or "blind spot" unqualified — the number is
already in `webhook_audit`; the inner tally is a `payload_size` estimate, period-sensitive
(~6–12 signals/POST). If in-window 403s ever recur (none since 1-Jul), it means the system was
killed intraday — read `system_events`, not the receiver. Peripheral, not-in-scope: `entry_start
10:00` discards ~7,462 open-bell POSTs (feeds the "relax toward 09:20" decision); circuit breaker
tripped SOFT_KILL nearly daily late-June.
[[signal-mortality-census-19jul]] [[persisted-kill-is-halt-21jul]] [[e4-w10-outcome-impact-19jul]]
