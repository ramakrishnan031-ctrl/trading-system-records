---
name: realert-presence-ledger-26jul
description: "security_monitor's dedup now tracks PRESENCE, not just last-alert — persistent conditions decay 6h/24h/7d and are never CRITICAL twice; a cleared-and-returned condition alerts immediately. Ships live on push, not Monday."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4ce1013a-db92-4899-ac6c-796dd439a76e
  modified: 2026-07-26T16:41:43.977Z
---

**DEPLOYED 26-Jul-2026 `324be50`.** `scripts/security_monitor.py:_dedup` used to store **ONE
float per finding key** (the last alert time). One number cannot say whether a condition *never
went away* or *went away and came back*, so it failed **both ways at once**:

- **"still true"** → a persistent benign condition re-fired at full CRITICAL every 6 h forever.
  One stale SSH baseline = **37 CRITICAL emails / 45% of the whole delivered stream**, 9 days.
- **"true again"** → a condition that **cleared and recurred inside the cooldown was silently
  dropped**. ⚠️ The dangerous half, invisible because the other half was so loud.

**Now:** the ledger holds `{first_seen, last_seen, last_alerted, repeats}`.
- absent > `realert_presence_gap_sec` (300) then back ⇒ **RECURRENCE** → immediate, **full severity**;
- present continuously ⇒ **PERSISTENCE** → interval widens `realert_backoff_multipliers` **[1,4,28]**
  = 6 h → 24 h → 7 d (capped), and **every repeat after the first is downgraded out of CRITICAL**
  and titled `(STILL PRESENT) … [REPEAT #n] UNCHANGED for …`;
- a one-pass flicker is persistence, not recurrence.

⭐ **Why the downgrade is safe (structural, not empirical): every `Finding.key` encodes the
condition's IDENTITY** — `authkeys:unexpected:<fps>`, `file:<label>:<sha12>`,
`copybypass:<event_id>`. **Any change to what is wrong is a different key ⇒ full severity.** A
test source-scans for that and fails if a key loses its identity component.

**Where "still broken" lives now:** `data_store/security/last_run.json` is written from the
**PRE-dedup** findings on **every ~60 s pass** and now **names** the keys (`persistent[]`,
`persistent_count`); `ops/control_tower/aggregator.read_security` raises a finding whenever it
says `clean=false`. ⚠️ The WARNING repeat is a *courtesy* — a WARNING Telegram is dropped
silently on delivery failure. **`last_run.json` is the guaranteed channel.**

⚠️ **PINNED CONSEQUENCE — a monitoring GAP counts as a clear.** If `security-watcher` is down
longer than the gap and the condition is still there on return, it is reported as a RECURRENCE
at full severity (across a blind spot we don't *know* it cleared). Cost: ≤1 extra CRITICAL.

⛔ **`security-watcher` is `Type=simple`+`Restart=always`+`RestartSec=60` (26-Jul: NOT a
`oneshot` as written here and elsewhere — the unit file records that systemd REFUSES
`Restart=always` with `Type=oneshot`; the ~60 s cadence is right, the type was not) ⇒ changes to `security_monitor.py` /
`config/security.yaml` go LIVE within ~60 s of the push, NOT at the Monday 08:15 boot.**
Ladder + gap are **config**, retunable without a deploy (a test proves the yaml reaches the
behaviour). Report: `docs/audit/alert_stream_fixes_26jul2026.md`.
[[rms-manual-close-is-mislabel-26jul]] [[feedback-verify-rc-not-output]]
