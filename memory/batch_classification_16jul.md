---
name: batch-classification-16jul
description: "16/17-Jul-2026 — read-only BATCH-SAFE vs LOOP-REQUIRED classification of every open register item (27 batch-safe, ~70+ loop, 8 ambiguous). A PROPOSAL awaiting Web Claude's approval; nothing executed."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**READ-ONLY classification PROPOSAL — awaiting Web Claude's approval. NOTHING executed, changed or pushed.**
Report `docs/audit/batch_classification_16jul2026.md`. Source = Rama's external register
`MASTER_PENDING_REGISTER_FINAL_16-Jul-2026.txt` (found at `C:\Users\rama\Downloads\` — **read-only; NEVER
copied into the repo**, only item IDs + my classification are in the report — [[feedback-operator-planning-docs-external]])
+ the four LOW groups in `docs/audit/full_system_audit_04july2026.md` (~55 line-level items) + the code at
the DEPLOYED head.

**📌 THE REGISTER IS STALE (written 16-Jul ~12:45, predates today's 2 deploys) — verified at the deployed
head `06a61cb`, not assumed:** **B1** (trades.sector) **CLOSED** (F1 deployed, observe) · **B4**
(alert-watcher `--loop`) **CLOSED** (running) · **S3/Q3 M-C4+M-C5+M-C6+M-C8 CLOSED** (deployed tonight).
**Still OPEN:** **B2** (`secondary_screener.py:407/408/410` still `"atr"/"rsi"/"prev_close": None`) ·
**B3** (`system_config.yaml:292 authoritative: false`). ⇒ **both original blockers are gone; B2/M-S4 is now
the TOP open engineering item** (a quarter of the selection score is a constant 0.0 in live).

**COUNTS: 27 BATCH-SAFE** — A docs 6 · B repo-hygiene 1 · C logging/observability 5 · D test-hygiene 3 ·
E verify-only 6 · F trivial-code 6. **+3 batch-safe by RISK but TOO LARGE ⇒ own run** (AB-910 Audit-B
Ph9/10 · Q9 integration coverage · BK-1 LONG-strategy review, which feeds D2). **~70+ LOOP-REQUIRED.**
**8 AMBIGUOUS, defaulted to LOOP and flagged for Web Claude** (X1 GUI fail-open 2FA / lockout-DoS —
**the most security-severe item on the list**; X2 `eod_verify` wrong columns → fixing makes a dormant P&L
check LIVE; X3 daily_report retirement = a deletion with EOD operational impact; X4 P4-9 deletions need
dead-proof + the `post-receive` dup is on the DEPLOY path; X5 instance_lock SO_REUSEADDR = a startup
singleton guard; X6 cron_heartbeat holiday degrade changes whether jobs RUN on a holiday; X7 exec-log
trade_id is written from the order path; X8 4.9 charts = a feature).

**🔑 THE BOUNDARY THAT DECIDES GROUP E (state it when proposing):** verification-only items are batch-safe
**as verifications** (they change nothing ⇒ cannot be the expensive error), but a verification of a capital
path TEMPTS a mid-batch fix. **Rule: produce a FINDING and STOP; any implied fix EXITS the batch to LOOP.**
If that boundary isn't accepted, all of Group E moves to LOOP.

**PROPOSED SHAPE:** one continuous run per group (lowest-risk first: B+C1 → A → F → D → E) · **one commit per
item** (keeps L1 rollback per-item) · preconditions (VM `ls` before the DEPLOYMENT.md path fix · M-K5 confirm
nothing reads the snapshot password · crash drills on scratch only) · **FULL suite before the batch deploys**
(the scoped-suite trap bit twice today) · attribute anomalies against the TRUE pre-change tree, never
`git stash` ([[verify-check-the-rc-not-the-output]]) · one off-market tagged push at the end · **any item that
turns out to touch a LOOP area EXITS the batch immediately** rather than being finished "since it's nearly done".

See [[pending-register-16jul]] [[deploy-mc-cluster-done-16jul]] [[deploy-alertwatcher-f1-done-16jul]]
</content>
