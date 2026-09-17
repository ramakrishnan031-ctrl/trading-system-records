---
name: pending_register_16jul
description: THE single source of truth for pending work (16-Jul census) — MASTER_PENDING_REGISTER_FINAL_16-Jul-2026.txt; supersedes the 14-Jul list
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — FRESH MASTER PENDING REGISTER (read-only census).** The register itself,
`MASTER_PENDING_REGISTER_FINAL_16-Jul-2026.txt`, is **Rama's EXTERNAL working file — git-excluded, NOT a
repo artifact** ([[feedback-operator-planning-docs-external]]). I first (mistakenly) committed it to `main`
(`55c1a98`+`e7a6d70`); those UNPUSHED commits were **excised via `git reset --mixed daa36cd`** so the
register never enters pushed history. **The census FINDINGS are preserved HERE** (below) + in Rama's file —
this memory is the durable in-repo-side record. Pick the next item from Rama's register / these findings,
not the old 14-Jul list.

**Supersedes:** the external `MASTER_PENDING_REGISTER_FINAL_14-Jul-2026.txt` (Web-Claude .txt, **NOT in the repo** — I reconciled against the in-repo twin `docs/audit/pending_reconciliation_14jul2026.md`, now banner-marked SUPERSEDED). Every 14-Jul item got an OPEN/CLOSED/PARTIAL/STALE/UNKNOWN verdict + evidence (SHA/file:line/test); all 14-16-Jul new items folded in; two old paper-phase .txt snapshots mined so nothing lost.

**Verified at HEAD (`c9fb298`), not assumed:**
- 🟡 **B1 trades.sector NULL at INSERT** — the 40% sector cap was dead (`sector_exposure = "... AND sector=?"` → 0). **ADDRESSED-PENDING-SOAK by F1 (16-Jul, [[f1-trades-sector-16jul]], UNPUSHED):** populate at insert from `InstrumentCache.sector` + gate-8 `sector_cap_mode` default `observe`. Deploy + the ENFORCE flip are OFF-MARKET, Rama-gated (observe soak ≥1 session first). Still **blocks D1** until enforced+reviewed.
- 🔴 **B2 M-S4 25/100 dead scorer** — `secondary_screener.py:407 "atr":None` (+408 rsi, 410 prev_close) UNCHANGED. PARTIAL (substrate shipped OFF; live bug persists). Needs re-parity+re-soak.
- 🟠 **B3 P1 authoritative flip** — `system_config.yaml:286 authoritative:false` still SHADOW. OPEN, data-gated (=P0-3/DG-3).
- 🟡 **B4 alert-watcher --loop** — branch `alertwatcher-loop-fix-16jul` (4 commits) UNPUSHED, deploys OFF-MARKET tonight (the ONLY genuinely-pending push). [[alertwatcher-loop-fix-16jul]]

**CLOSED since 14-Jul** (the 15-Jul combined deploy `2dc69d5..c9fb298` + F0 + prune): 3 fixes (eod_cleanup FK `3907a5c`, M-SC2b `d3499b9`, fm_ledger `561d281`) · monitoring F1-F4 (`c405c30`/`795a417`/`d960760`/`5311fe6`) + canary `11520b4` + deploy-gate `66cb182` + Interface Change Checklist `32389c0` + autospec/guard `397f3f6`/`1645bd6` · F0 SMTP restored · Phase-B prune 113,377 cleared.

**Top-5 OPEN by leverage/risk:** (1) B1 trades.sector NULL [blocks D1, latent capital-safety]; (2) B2 M-S4 dead scorer [distorts every pick]; (3) B3 P1 authoritative flip [last Audit-B P&L HIGH]; (4) AB-910 Audit-B Phases 9-10 NEVER produced [unaudited ops+security slice]; (5) capital/kill MEDs — **INVESTIGATED 16-Jul [[mc-cluster-investigation-16jul]]: M-C4 (auto-trip lock-through-send, `kill_switch.py:649-663`) + M-C8 (hard_kill 2h retry starves the fill thread, `:550/1204-1290`) are OPEN+REACHABLE → the real fix targets; M-C5 mitigated (atomic caller gate) + M-C6 latent (allocator min_weight 0.5) = not reachable now.** OR backups-all-one-disk DR HIGH.

**DECISIONS with Rama (do NOT decide):** D1 sizing=HOLD (blocked by B1) · D2 direction · D3 min_pass inversion · **D4 = UNKNOWN** (text lives only in the external .txt; not recoverable from repo — Rama confirm).

**4 named gaps (honest closure):** DG-1 S&R BIR W/L count (needs Rama's manual zone-marking) · AB-910 unaudited findings (until Phases 9-10 run) · D4 text · M-SC2 one runtime EOD confirming the CSV has rows. Source audits `full_system_audit_04july2026.md` + `audit_05jul2026.md` PRESERVED (~55 line-level LOWs; not re-enumerated).

**Surprises:** the named .txt register isn't in the repo (external); eod_cleanup FK was BROKEN by the very P10 `2e61fad` that 14-Jul marked CLOSED (a fix that broke another path — now fixed `3907a5c`); two Apr/May paper-phase .txt snapshots held a never-registered v2.1 feature backlog (BSE/multi-account/AngelOne/hot-reload/bot-commands → folded as BK-7).

Read-only census: changed NO code/config/schema/DB/VM. [[unpushed-pending-deploy-ledger]] [[alertwatcher-loop-fix-16jul]] [[morning-verify-16jul]] [[deploy-done-16jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 521 B (budget 300 B). The index now carries a hook and this link.

- ⭐📋 **[PENDING-WORK census (16-Jul)](pending_register_16jul.md)** — the register `.txt` is Rama's EXTERNAL git-excluded doc, NEVER in the repo ([[feedback-operator-planning-docs-external]]). Both blockers CLOSED (B1 F1-deployed · B4 alert-watcher); M-C cluster + batch-1 DEPLOYED; AB-910 PRODUCED; M-SC2 CLOSED runtime-proven. **TOP open engineering item = B2/M-S4** (`secondary_screener.py:407-410` `atr/rsi/prev_close: None` ⇒ 25/100 of the live selection score is a constant 0.0). [[pending-register-16jul]]
