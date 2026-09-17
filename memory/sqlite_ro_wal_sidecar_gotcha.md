---
name: sqlite-ro-wal-sidecar-gotcha
description: "Opening a WAL-mode SQLite DB read-only with ?mode=ro (no immutable=1) still creates a -shm/-wal sidecar, leaving artifacts. Use ?mode=ro&immutable=1 or copy-first to read a backup with zero trace."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 73061e50-ca6a-4e2e-95e9-91b381c0e60d
  modified: 2026-07-24T06:31:13.384Z
---

Opening a **WAL-mode** SQLite DB via `sqlite3.connect("file:PATH?mode=ro", uri=True)` — read-only,
but WITHOUT `immutable=1` — **still creates a `-shm` sidecar** (32 KB) and touches `-wal` (0 B) beside
the file, because read-only WAL access needs shared memory. The base `.db` is NOT modified (`-wal` = 0 B,
so no pending pages) — data is intact — but you leave artifacts in the directory.

**Proven 24-Jul:** reading `analytics-2026-07-10..15.db` + `trading_system-2026-07-19.db` backups with
`mode=ro` created **14 sidecar files** in `data_store/backups/`.

**To read a WAL backup with ZERO trace:** `file:PATH?mode=ro&immutable=1` (immutable ⇒ SQLite assumes the
file can't change, skips the -shm), OR copy the file out first and read the copy.

**LIVE DB is unaffected** — the running app already owns `trading_system.db`'s `-wal`/`-shm`; a `mode=ro`
reader there uses the existing shared memory and creates nothing new. The gotcha only bites read-only
opens of otherwise-idle **backup** files.

Compounding: `scripts/backup_retention.py`'s `.db`-suffixed categories don't match `-wal`/`-shm`, so such
sidecars land in `unmatched` (never reaped) and accumulate — see `docs/audit/capital_snapshot_and_backup_retention_24jul2026.md`.
