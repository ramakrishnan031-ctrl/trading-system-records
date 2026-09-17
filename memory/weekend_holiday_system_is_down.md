---
name: weekend_holiday_system_is_down
description: "On weekends and NSE holidays the VM/trading system does not run and sits in SOFT_KILL — an off-market \"engine down\" reading is EXPECTED, not an incident"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 31334cdb-96e4-4a09-bdf4-def39d5ad8ab
  modified: 2026-08-30T11:53:46.671Z
---

👤 **RAMA, 30-Aug-2026 (Sunday):** *"during weekend & holidays VM or trading system
wont runs stays in 'soft kill' mode."*

⭐ **ON A WEEKEND OR AN NSE HOLIDAY THE SYSTEM IS SUPPOSED TO BE DOWN.** The header
reads `PHASE WEEKEND` and `KILL SOFT_KILL`, the engine's `/health` does not answer,
and there is no uptime, no heartbeat and no activity for that date.

⚠️ **SO AN OFF-MARKET OBSERVATION PROVES ALMOST NOTHING.** These readings are the
CORRECT weekend state, ⛔ not evidence of a fault:
- `Trading Engine FAILED` / "health endpoint did not answer"
- `Uptime NOT AVAILABLE`, no `last_heartbeat` anywhere
- `TRADING READINESS: NOT READY`
- every throughput / activity / trend series **empty for that date**

⛔ **NEVER open an incident, roll anything back, or "fix" a screen on the strength of
an off-market reading.** ⭐ First ask: *is it a trading day?* Compare against a
MARKET-HOURS observation, or ⛔ do not compare at all.

⚠️ **DISTINGUISH TWO DIFFERENT EMPTINESSES OFF-MARKET** — they look identical and
⛔ are not the same thing:
- 🔬 **weekend down** — real, correct, and it resolves itself on Monday 08:15.
- 🔬 **a DEV-HOST gap** — e.g. every systemd unit `UNKNOWN` because `systemctl`
  does not exist on the Windows PC. ⛔ That one never resolves, on any day.

⇒ ⭐ **This is exactly why a screen review needs filled data:** on a weekend there is
no live data to judge a screen against, and none arrives until Monday. See
[[gui_review_needs_filled_data]].

⭐ Related: the Monday boot chain is what ends this state — [[boot_chain_token_watcher_05aug]].
