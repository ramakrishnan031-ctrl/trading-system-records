---
name: feedback_foundation_rules
description: "Rama's design rules — single source of truth (derive don't duplicate), boring code, fail fast, no real alerts on non-trading days"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0084080d-8dce-4adb-88eb-2c4b5a0e4693
---

Rama follows a numbered set of **"Foundation Rules"** and cites them when steering
design. Confirmed ones from the 20-Jun Cron Officer work:

- **Single source of truth / no duplication (Rule 1.4 + 1.9):** when a value can be
  DERIVED from an existing field, derive it — do NOT add a parallel field that must
  be kept in sync. Concrete decision: `category` was DERIVED from the existing
  `cadence` (via `resolve_category`, + optional override) instead of adding a
  `category:` line to all 33 cron jobs. He explicitly rejected the duplicate.
- **"Boring code":** prefer the least-to-maintain, least-likely-to-drift option.
- **Fail Fast (Rule ~3.x):** reject bad input loudly rather than silently degrade —
  e.g. an HTML email sentinel with no `plain_fallback` RAISES in `alert_watcher`.
- **Atomic / no corrupt state (Rule 3.2):** write-to-tmp + fsync + rename (already
  the sentinel + attempts-counter pattern).

**Why:** these are his standing engineering principles; aligning to them avoids
rework (he will push back on duplicated/over-clever code).

**How to apply:** when a spec literally says "add field X to every item," first check
whether X is derivable from existing data; if so, derive-with-override and explain the
deviation. Default to the boring, single-source option.

**Operational corollary:** do NOT send real emails/Telegrams/alerts on a non-trading
day under the LFL836 account when testing — use dry/`--force-dry-run` paths or a test
mailbox (the holiday safeguard is intentional). See [[cron_officer_revision_20jun]],
[[feedback_paper_live_parity]].
