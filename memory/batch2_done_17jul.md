---
name: batch2-done-17jul
description: "BATCH-2 (AB-910 batch-safe) DONE + TAGGED, UNPUSHED — token leak fixed (L11), stale post-receive dup deleted, ITEM 2 refused as invalid-premise; 4 new findings incl. a 2nd (revoked) token in the logs and FIX-065's guard never being live."
metadata: 
  node_type: memory
  type: project
  originSessionId: a8c00bd7-f7a4-4643-bf7d-9bab09ae2c49
---

**BATCH-2 built 17-Jul ~01:10–02:00 IST, off-market. Base `57f28a1` → head `0a9a6a8`. Tag
`deploy-17jul-batch2` = rollback point. NOTHING PUSHED — awaiting Rama's off-market go.**
Report: `docs/audit/batch2_done_17jul2026.md`. Regression **4787 pass / 11 known-PC-env fail /
0 attributable**. Schema v44, no migration; no trading path touched; no escalations from the items.

## What shipped
- **ITEM 1 `6f69419` — §1.1 HIGH, the live Telegram token no longer reaches the debug log.**
  Root cause: `setup_logging()` sets root DEBUG for the DEBUG+/all-loggers sink (L3) ⇒ we sink
  urllib3's wire DEBUG; urllib3 logs the request line; **Telegram puts the token in the URL PATH**
  ⇒ structural leak, our code never printed it. Fix = cap third-party HTTP loggers
  (urllib3/requests/httpx/httpcore) at **INFO** in `setup_logging()`, recorded as **L11** +
  `cap_third_party_http_loggers()`. Chose the emitter over the message because **urllib3 leaks the
  same URL from 3 call sites** (request line, redirect, retry). **Rejected the redaction filter:**
  a filter on the debug handler mutates a LogRecord shared with all 4 sinks ⇒ correctness would
  depend on handler order.
- **ITEM 3 `3d03ff0` — §2.4 MED, `deploy/post-receive` DELETED.** md5-proven dead
  (live VM hook `bd950b7…` == `deploy/hooks/post-receive`; the dup was `604d2b3…`). It even lied
  about its own install path (claimed `install_vm_services.sh`, which never mentions it) and
  pointed at `/home/ubuntu/trading-system`, **a directory that does not exist**. Recover if ever
  needed: `git show 57f28a1:deploy/post-receive`. SYSTEM_MAP updated; mempalace entry superseded.

## ⛔ ITEM 2 REFUSED — the audit was wrong, not the system
**§2.3 "log growth unbounded; no retention" is FALSE.** `log_cleanup` (`deploy/cron/trading-system.cron:15-16`)
has existed all along, **is in the live crontab**, ran at `2026-07-17T00:00:02` rc=0, and leaves
**0 `*.log` files older than 30d**. Live since **11-May**, oldest log **15-Jun** ⇒ **~5 weeks were
pruned**. The audit read *"oldest ≈30 days"* as proof of NO retention when it is the exact signature
of a **working** 30-day retention; 1.1 GB is the **steady state** (30d × ~35 MB/day), not growth.
Adding a second prune would duplicate a working mechanism → no code. See [[feedback-verify-rc-not-output]].

## 4 NEW findings (none were on any list)
1. **🔴 §1.1 was UNDERCOUNTED 41%.** Scanning by token **shape** (not by the known `.env` value)
   found **TWO** distinct bot tokens: live `79b64abe7c82` (**984 lines / 10 files**, 03-Jul→16-Jul)
   **+ `a581ca0b6831` (678 lines / 9 files, 15-Jun→02-Jul)** = the old systemd drop-in from
   [[telegram-token-shadow-investigation-03jul]]. **Total 1,662 / 19 files.** Severity UNCHANGED:
   the 2nd token is **401-REVOKED**. Explains the "leak started 03-Jul" illusion — that is just when
   the main process switched from the drop-in to `.env`. **Corollary: rotation is PROVEN clean here.**
2. **🔴 FIX-065's market-hours push guard has NEVER been live** → LOOP. The deleted dup held the
   **only** copy; live VM hook grep=**0**. So *"no push during market hours"* is **manual discipline,
   not enforcement**. Its **12 tests are vacuous** — they assert against a mock bash string they
   define inline, never a real hook, so they pass regardless (+ skipped on Windows).
3. **🟡 The prune can't reach append-only `cron-*.log`** (0 of 31 match `-mtime +30`; mtime always
   fresh). Only 0.1 MB ⇒ no code — **but §1.9's residue can therefore NEVER self-purge.**
4. **🟡 `deploy/hooks/post-receive`'s header contradicts reality** — says "NOT the currently-installed
   hook"; md5 proves it **IS**. Not fixed: editing breaks the byte-identity that proves which hook is real.

## Owed
- **VM purge at deploy: 19 files** (10 live-token + 9 revoked) + `logs/cron-candle-fetch.log`.
  **Deploy before the 08:15 boot** ⇒ today's log never gets the token.
- **🔴 RAMA: ROTATE the live token** (`@Trade_sysbot`, id 8648177777) — **compromised-at-rest**.
- The purge is VM-only: **the PC never had it** (PC `logs/` = 2 test artifacts; token only in `.env`).

Links: [[ab910-ops-security-audit-16jul]] [[unpushed-pending-deploy-ledger]] [[batch1-done-16jul]]
[[feedback-verify-rc-not-output]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 301 B (budget 300 B). The index now carries a hook and this link.

- 🗂️ **[BATCH-2 (17-Jul) — logger token leak FIXED (L11), stale dup deleted, ITEM 2 REFUSED](batch2_done_17jul.md)** — DEPLOYED (above). The leak was **undercounted 41%** (a 2nd token, 401-REVOKED). **ITEM 2 refused: the audit was WRONG — `log_cleanup` exists/works.** [[batch2-done-17jul]]
