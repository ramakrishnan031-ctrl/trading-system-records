---
name: fresh_audit_postremediation_08jul
description: "Fresh post-remediation audit (READ-ONLY, HEAD 005c007) — ~18 fixes regression-CLEAN, 4 interaction probes all clean, 0 new bugs; schema-version silent-downgrade ELEVATED (P1/v42 imminent); Wave-6 = flatten+capital-accounting cluster"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e32bad3-6610-4e3c-a772-6502eeb354b4
---

**Fresh post-remediation audit — 08-Jul-2026, READ-ONLY, HEAD `005c007`** (runbook said `0dd2ba0` = nonexistent; `005c007` = post-PUSH-1 HEAD, only a docs-changelog line over `9bcc1eb`, 0 code). Scope gate before Wave-6/7. Fixed NOTHING.

**VERDICT: REGRESSION-CLEAN.** All 4 interaction probes clean; all spot-checked HIGHs still enforced at HEAD; 0 new bugs from the ~18 fixes. One pre-existing latent LOW (schema-version silent-downgrade) ELEVATED because P1/v42 is imminent.

**A. Interaction probes (ALL CLEAN):**
1. Terminal-trigger (`schema.sql:278`) — terminal-LOCK fires only FROM {CLOSED,CLOSED_MANUAL,FAILED,CANCELLED,REJECTED*} & only when NEW≠OLD. EXITING NOT terminal → H-2 EXITING→CLOSED passes; A-3 PENDING→FAILED passes; every fix's edge originates non-terminal → no legal transition blocked.
2. H-7 lock × FIX-067 re-anchor (`signal_processor.py:858-946`) — FIX-067 live-LTP fetch+re-anchor completes BEFORE `portfolio_lock`(:924); H-7 cap+reserve(strategy=) atomic inside(:928-946), count-based/price-orthogonal. No network-in-lock, no double-count.
3. M-C1 seed × capital writes (`main.py:2022-2025`,`fund_manager.py:1664-1711`) — live-only read-only Σ once before initialize(); cancels exactly vs rehydrate Phase-2 (shared `_today_release_used_pnl_rows`); paper FIX-156 disjoint branch.
4. A-3 reject-path (`order_placer.py:1229-1237`) — trade PENDING, no broker order yet, `_handle_placement_failure` releases+FAILED, raised OUTSIDE try (429 handler can't catch-retry); BL-19 → prior 429 attempt already cancelled its legs → no orphan.

**B. New/forward-looking (0 new bugs):**
- **ELEVATED — schema-version silent-downgrade** (`state_store.py:348-376`, was Audit-A LOW). `old_version < EXPECTED` gate SKIPS on a NEWER DB (42<41 false) → `executescript`(:367) stamps version DOWN to 41 → `41==41`(:371) boots clean. Does NOT fail-fast on a newer DB. **Contradicts the P1 memory's "old code refuses a v42 DB"** — a v41 code-revert after P1/v42 SILENTLY downgrades (v42 `eod_broker_reconciliation` stranded; re-deploy re-migrates idempotently, pure-add). ⇒ P1 rollback MUST be `authoritative:false` flag, NOT code-revert. Fix: `old_version > EXPECTED → raise`.
- MINOR: A-3 adds a 2nd last-mile `is_active("entry")` caller → inherits (does not worsen beyond +1 caller) M-C4's lock-hold-through-Telegram exposure; fixing M-C4 benefits OP-LM1+A-3.
- MINOR/forward: terminal-trigger graceful-degrade depends on every `update_trade_status` caller wrapping try/except (the fn itself doesn't swallow the IntegrityError); U1-U9 verified — keep invariant for new callers.

**C. Closed-HIGH spot-checks — ALL enforced at HEAD:** H-1 `order_placer.py:3722` SELECT order_id · H-4 `kill_switch.py:1244` determine_close_direction/retry · H-5 `:1166` _PRODUCT_TO_INTENT sweep · H-7 `signal_processor.py:928` inside-lock · H-8 `shadow_tracker.py:320` trade["strategy"] · H-10 `order_placer.py:1386` result-None guard · H-11 `main.py:127` _TOKEN_PATH · H-12 `zerodha_adapter.py:1084` signed paper qty · H-13 `token_monitor.py:144` re-arm+classify · H-9 `candle_store.py` dead-code removed+off-by-one · D-1 CAS `order_manager.py:618` · terminal-lock `schema.sql:278` · S-1 redaction `webhook_receiver.py:639`. Only open HIGH = **H-6** (CNC GTT exit-day, delivery-gated).

**D. Backlog re-prioritized:** OBSOLETE(fixed Wave-5): M-C1, M-S1. ELEVATED: schema-downgrade(LOW→MED), backups-same-disk(Audit-B HIGH DR), M-C4(via A-3). **Wave-6 = "flatten + capital-accounting integrity" cluster:** M-O1 (reconciler `_flatten_broker_position` NSE:NSE: double-prefix → FIX-181 cap dead → raw MARKET) · M-O2 (CHECK4 partial external close never releases capital/PnL) · M-C3 (per-bucket invariant only global) + M-C7 (release_used recomputes from current leverage_map) · M-K1+M-R1+M-R2 (P&L DATE(updated_at) keying + daily_report holiday guard + CLOSED_MANUAL exclusion) · schema-version fail-fast · M-SC2 (screened CSV wrong DB→empty). + Audit-A systemic rec: schema-backed integration tests for every raw-SQL money path + wired-in assertions.

**E. Gated tracks:** P1 READY for SHADOW (v42, `authoritative:false`, `wave4-p1-v2@3ef7c35`, validated, unmerged; caveats: schema-downgrade=flag-rollback-only + Audit-B cron-StateStore-init auto-migrates v42 before app restart, benign pure-add). Delivery NOT ready (H-6 + M-O6/M-O7 GTT + Slice-2.5 T2 repaired-not-run; delivery_enabled=false). Security: C-2 Ph3 bind/TLS/HMAC (Rama) + webhook MEDs (M-S2 QUEUE_FULL dedup-poison, M-S8 unauth INSERT) + git-history purge (last C-1) + backups-same-disk DR. CO: broker-managed SL/CHECK1 sole backstop; M-O8 open.

**F. Overall:** the ~18 fixes are regression-clean & mutually non-interfering (emergency-exit/HARD_KILL/terminal/capital changes compose correctly). Next fix-work once P1 SHADOW deploys = Wave-6 cluster above. Sources: [[full_repo_audit_04jul_pending]] (Audit-A 13H/47M) · `docs/audit/audit_05jul2026.md` (Audit-B ops) · [[push1_pc_vm_sync_08jul]].
