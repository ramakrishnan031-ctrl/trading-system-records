---
name: alert-watcher-log-name-frozen-18aug
description: alert_watcher's date-embedded log name is fixed at process start and --loop outlives it
metadata:
  type: project
---


## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 831 B (budget 300 B). The index now carries a hook and this link.

- 🗓️🕳️ **18-Aug — ⛔ NEVER TRUST *"grep today's `alert_watcher` log"*: THE DATE-EMBEDDED NAME IS FIXED AT PROCESS START AND `--loop` OUTLIVES IT. `<MEASURED · LATENT · ⛔ NOT FIXED>`** (P) the process killed at `09:11:21.238` was still writing to **`logs/alert_watcher_2026-08-01.log`** — 17 days stale, 1,415,501 B; the new PID `3938122` opened `alert_watcher_2026-08-18.log`. Same shape at `alert_watcher_2026-07-28.log`, which stops at `2026-08-01 06:17:50` ⇒ **a property, ⛔ not an incident.** F4's date-embed (`5311fe6`) vs `--loop` (`34c2993`) — **the two fixes defeat each other.** ⛔ Observability plane only ⇒ LATENT, documented and continued. 🔴 **OWED: name the log per-write, or rotate on date change.** 📋 `N18-06`; [[feedback-live-vs-latent-findings]] · [[alertwatcher-loop-fix-16jul]]
