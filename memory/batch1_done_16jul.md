---
name: batch1-done-16jul
description: "16/17-Jul-2026 BATCH-1 — 15 batch-safe items committed (UNPUSHED), 1 escalated to LOOP, 6 deferred with reasons. M-SC2 runtime-CLOSED; a capital finding on CHECK1/RMS costs=0.0."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**BATCH-1 COMPLETE — 15 commits on `main` off base `362e166`, UNPUSHED, awaiting Rama's off-market deploy go.**
One commit per item; a test wherever it was a behaviour change. No schema change. **No trading-path change.**
Report `docs/audit/batch1_done_16jul2026.md`.

**🔝 THE TWO RESULTS THAT MATTER:**
1. **M-SC2 is CLOSED — RUNTIME-PROVEN** (the register's "only outstanding proof"): screened CSVs are
   **1 data row / 40 B on 13-14-15-Jul (pre-fix) → 25 rows / 2,033 B on 16-Jul**, the first EOD after
   M-SC2b `d3499b9` deployed. **One of the four named gaps in the register's HONEST CLOSURE is now shut.**
2. **🔴 CAPITAL FINDING (E4, P3-s13) — finding only, fix = LOOP:** `order_reconciler.py:1109` passes
   `costs=0.0` into `release_used`, where `pnl = gross_pnl - costs` ⇒ **`pnl` is GROSS**;
   `projected_after = avail + margin + pnl` ⇒ **available capital credited with GROSS**; and
   `pnl_delta = pnl` feeds **the daily-loss limit** (per [[capital-operational-note]]). So on EVERY
   CHECK1/RMS/manual close the daily-loss limit's input is **gross, not net — understating the loss by the
   costs**. The register says "by-design"; that is the claim the mechanism must justify. **It matters: the
   book is gross ≈ −0.007R vs net −0.100R — costs ARE the loss, so a control fed gross is fed the wrong
   number.**

**COMMITTED (15):** `681688e` deleted a **1.44MB base64-XLSX with real trade data** committed past the
`*.xlsx` ignore (+ closed the encoded-form gap) · `7b492fb` stopped printing **8 chars of the live access
token** to the cron log (swept: only site) · `67850b8` **DEPLOYMENT.md pointed at a directory that does not
exist** (`/home/ubuntu/trading-system/.env`; the near-miss `trading-system.git` IS real — verified every line
on the VM first) · `63517f2` SYSTEM_MAP HOW-TO-READ + index (**NOT the split** — every report/memory points
into it by section) · `55a9c59` PATHS honest header · `bc5a2a9` **the missing README** (585 files, live since
11-May, `ls README*` empty) + `ops/__init__.py` · `7afbd25` `sqlite3` imported in one function, caught in
another ⇒ **NameError from inside the handler** (AST-proven; masked by INSERT OR IGNORE) · `5193b48`
candle trade-date naive `now()` → `today_ist()` · `803ec0d` **entry_start_time documented NOT "fixed"** (see
below) · `dbeba4a` **M-K5** redact populated secrets before `config_snapshots` (**byte-identical on the real
config ⇒ provably a live no-op**) · `2d56666` **GUI logged Rama out every restart** (secret_key configured
NOWHERE — persisted 0600, fail-safe) · `71c75bc` **two win rates on one report** (61W/91L/**1 breakeven** ⇒
headline 39.87 vs per-strategy 40.13; headline now calls the one definition) · `2bb9194` **daily_trade_review
had no non-trading-day guard** (`market_day_only` is **metadata — nothing enforces it**; skip still heartbeats
SKIPPED) · `6d38d22` **a test vacuous on Windows** that also **created the register's NR-4 stray D:\ folders**
every run · `ffdeffe` **an unreadable cron registry silently downgraded a critical FAILED alert** to ERROR
(losing the email fallback) → tri-state.

**⚠️ ESCALATED TO LOOP (1) — the guardrail fired:** **P3-s14** webhook insert-fail. Classified log-only;
opening it changed what it IS — `_process_signal` has **no generic handler around the INSERT**, so the "300s
dark window" is that the **dedup claim is never rolled back** ⇒ retries DUPLICATE-bounced. The real fix is
that rollback = **control flow on the signal entry path (whether a signal enters at all)**. Not finished.

**DEFERRED with reasons (6):** A5 Word docs (**gitignored binaries — Rama content-authoring**) · A6 BK-4
(**underspecified — the only trace is a one-line table row; executing = inventing scope**) · pytest skew
(**a decision**: root `>=9.0.3` vs GUI `==8.3.4`; bumping unverified risks the safety net) · C4 F2 tail (~20
jobs, each a per-job criterion decision, several reading capital state) · C5 B-1 metrics (**design task**) ·
**D2 CT drills — PRECONDITION IMPOSSIBLE: `tests/crash_test/ct_utils.py:63` hardcodes
`DB_PATH = data_store/trading_system.db` (a REAL db, opened WRITABLE, module constant not injectable)** ⇒
"scratch only, never live" cannot be honoured without a harness change.

**OTHER E FINDINGS:** E2 auto-clear benign (KILL_AUTO_CLEARED daily 08:15, clean cadence) · E6 EOD delivery
healthy (cron_officer/system_manager SUCCESS, 0 pending sentinels, no degraded marker — inbox is Rama's) ·
**E5 BK-8: the core IS clean** (no hardcoded config defaults in capital/orders/signals/screening/core ⇒ the
pydantic loader really is the single source, previously UNVERIFIED); residual = 5 scripts defaulting
`TRADING_MODE` to `"live"` · E3 charges-vs-contract-note **blocked on Rama** (the note lives outside the repo).

**🔑 F5 IS THE ONE TO REMEMBER:** strategy `entry_start_time: "09:25"` vs global `entry_start: "10:00"` looks
like drift; the global genuinely binds. But the global is `[LAUNCH-PHASE]` ("Relax toward 09:20 as the account
scales") ⇒ **rewriting the 16 strategies to 10:00 would silently hold them out of 09:20-10:00 the day that
floor is relaxed — a behaviour change disguised as cleanup.** Documented, not "fixed".

**⏰ Deploy:** off-market on Rama's go; **re-derive the SHA at run time** ([[deploy-mc-cluster-done-16jul]]).
Rollback: per-item revert (L1) or reset to `362e166` (L2); all schema-free. **Production-visible changes:** GUI
stops logging you out; the daily review skips non-trading days; headline win% 39.87→40.13 while a breakeven is
in the window; a critical FAILED alert escalates when the registry is unreadable; no token in the cron log.

See [[batch-classification-16jul]] [[pending-register-16jul]] [[verify-check-the-rc-not-the-output]]
</content>
