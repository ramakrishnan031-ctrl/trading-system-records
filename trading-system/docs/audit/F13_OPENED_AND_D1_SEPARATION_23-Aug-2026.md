# RULINGS RECORDED · THE SELF-SILENCING CHAIN · D-1 SEPARATED · **F13 OPENED**

**23-Aug-2026, ~19:00 IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **RECORD ONLY.** ⛔ No code · ⛔ no VM change · ⛔ no privilege change · ⛔ no push ·
⛔ nothing fixed.
📄 Upstream: `MONITOR_DETECTION_GAP_23-Aug-2026.md` · `SUDO_AND_SUDOERS_WATCH_23-Aug-2026.md`.

**Provenance:** 🔬 measured · 📄 from evidence · 💭 inference · 👤 Rama's.

---

## §1 — 🔴 THE SELF-SILENCING CHAIN — **ONE ROW**, ⛔ NOT FOUR

📄 The clause promoted from the end of a list, where it was buried:

> 🔴 **Whoever reads `.env` obtains both the brokerage credentials AND the means to silence
> the alerting that would report the read.**

🔬 `.env` holds `TELEGRAM_BOT_TOKEN` + 3 chat/channel ids **and** `ALERT_SMTP_PASSWORD` — 🔬 and
`alerts/` delivers CRITICALs by exactly those two channels (Telegram + the CRITICAL email
sentinel consumed by `alert-watcher.service`). ⇒ ⭐ **not two findings — one self-silencing path.**

### 🔬 THE CHAIN, AS ONE ROW

| step | 🔬 what the monitor sees |
|---|---|
| **1 · enumerate** — `sudo -n -l`, learn you hold `(ALL) NOPASSWD: ALL` | 🔴 **NOTHING** — `sudo -l` writes no `COMMAND=` line to `auth.log` ⇒ invisible **by construction** |
| **2 · read** — `sudo cat …/.env` | 🔴 **NOTHING** — `/usr/bin/cat` is whitelisted. ⭐ Proven by the **same-pass control**: 15:01:03 `sudo cat auth.log` silent, 15:01:05 `sudo /usr/bin/true` **alerted** |
| **3 · hold the accounts** | 5 × `ZERODHA_API_KEY` + `API_SECRET` + 🔴 **`TOTP` (the 2FA seeds)** + `ZERODHA_PASSWORD`/`USER_ID` ⇒ **five live brokerage logins, unattended, 2FA defeated** |
| **4 · hold the signal path** | `WEBHOOK_SECRET` ⇒ the ability to **inject signals** |
| **5 · hold the alarm** | 🔴 `TELEGRAM_BOT_TOKEN` + `ALERT_SMTP_PASSWORD` ⇒ **the tokens that would have raised it** |

⇒ ⭐ **The read that starts the chain raises nothing, and the last step takes the alarm.**
⛔ **No leg fixed. ⛔ The whitelist was not touched.** ⭐ It belongs to **F13** (§3).

---

## §2 — ⭐ D-1: 👤 **KEEP 400. FIX THE INTERPRETATION.** — RECORDED AS **TWO ITEMS**

👤 **RULING RECORDED: keep `root_probe_spike_threshold: 400`. ⛔ Do not raise it. Fix the
interpretation.** ⛔ `root_probe_spike_threshold` untouched · ⛔ `aggregator.py` untouched.

### 🔴 ONE PREMISE IN THE CARD DOES NOT SURVIVE MEASUREMENT — ⭐ AND THE RULING IS STILL RIGHT

📄 The card reasoned: *"raising 400 to 600 would not unpin the status — it would only remove one
of eleven contributors; the status would stay pinned by the other ten."*

🔬 **Measured — that is not the mechanism.** The Control Tower's security adapter reads **one
file**, `data_store/security/last_run.json`, and nothing else. The live file, **18:59:15 today**:

```json
{ "checks_run": 10, "clean": false, "findings_count": 1,
  "max_severity": "INFO", "persistent": ["rootspike:2026082318"], … }
```

⇒ 🔴 **The root-probe finding is currently the SOLE contributor — `findings_count: 1`.** The
eleven alert *types* in the 65-day inventory are what the **monitor** has ever raised; they are
⛔ **not** eleven simultaneous pins on the status field.

🔬 **And it is not pinned "forever" either.** Findings-per-pass across **1,135 passes today**:

| findings in the pass | passes | share |
|---|---|---|
| **0** → `clean: true` → **`ok`** | **452** | **39.8%** |
| 1 | 661 | 58.2% |
| 2 / 3 / 4 | 8 / 12 / 2 | 1.9% |

⇒ ⚠️ **`docs/SYSTEM_MAP.md:53` says the standing INFO `rootspike` finding *"pins the Control
Tower security panel to `warn` FOREVER"*. 🔬 OVERSTATED — the panel reads `ok` on ~40% of passes
today.** It **oscillates** with the rolling-hour probe count. ⛔ Flagged, ⛔ not edited — that is a
tracked file and outside this card's scope. 👤 It needs a one-line correction.

### ⭐ THE RULING IS CORRECT ANYWAY, AND FOR A **BETTER** REASON THAN THE CARD GAVE

🔬 The actual interpretation defect, `ops/control_tower/aggregator.py:88-89`:

```python
status = ("critical" if any(f.severity == "CRITICAL" for f in findings)
          else "warn" if findings else "ok")
```

🔬 `SECURITY_MAP = {"CRITICAL": "CRITICAL", "WARNING": "MEDIUM", "INFO": "INFO"}`
(`severity.py:21`). ⇒ the live pass carries `max_severity: "INFO"` → maps to `INFO` → not
CRITICAL → **`status = "warn"`.**

⇒ 🔴 **AN `INFO`-ONLY CONDITION RENDERS THE SECURITY PANEL `warn`. The status line branches on
*whether findings exist*, ⛔ never on how severe they are.**
⇒ ⭐ **AND THIS IS WHY RAISING THE THRESHOLD WOULD BE THE WRONG FIX — ⛔ not because it would fail
to unpin the status (🔬 it largely would), ⭐ but because it would make a real defect LESS
VISIBLE while leaving it in place.** ⚠️ The next INFO-only source to appear would re-pin the
panel and nobody would know why. 👤 **Rama's ruling is well-founded; the arithmetic under it
needed replacing, ⛔ not the conclusion.**

### ⇒ 🔬 TWO ITEMS, ⛔ NOT ONE — **COMPLETELY SEPARABLE**

| # | item | status |
|---|---|---|
| **D-1a** | `root_probe_spike_threshold: 400` | 👤 **RULED: KEEP.** ⭐ It is a live early-warning signal — 🔬 it fired at **401 vs 400** at **15:18:11 today**, while the measurement was being written. ⛔ Closed |
| **D-1b** | the aggregator's **status logic** — distinguish INFO / WARNING / CRITICAL instead of branching on non-emptiness | 🏷️ **OPEN.** ⛔ Not authorised tonight. ⭐ Independent of any threshold |

---

## §3 — 🔴 **F13 · POST-COMPROMISE DETECTION** — OPENED

👤 **RULING RECORDED: D-2 = DESIGN/FIX REQUIRED · ⛔ NO LIVE CHANGE AUTHORISED.**
⛔ (d) rejected · ⛔ no cosmetic directory addition · ⛔ no privilege change · ⛔ no whitelist
edit · ⛔ **no `NOPASSWD` decision inferred from a monitor finding.**

⚠️ **Why it gets a name now, and the argument is this project's own history:** 🔬 `65b7196` was a
finished 30-file build **nobody opened for fifteen days**, and **F12 exists because that happened
three times.** ⇒ ⭐ **an unnamed workstream is how this project loses finished work.**

> ⚠️ **NUMBERING CAVEAT, ⛔ recorded rather than silently renumbered:** `F13` is free in the
> **campaign** F-series (F1 · F2 · F6 · F11 · F12), but it collides with the **closed 14-Jun-2026
> audit's** own finding index (`FIX-166 | F13`, `docs/audit/system_audit_14jun2026.md:41`). ⭐ Two
> namespaces, one string. 👤 The card named it F13 and I have not overridden that — ⛔ but the row
> must always be written **`F13 · POST-COMPROMISE DETECTION`**, never bare `F13`.

### THE LEGS, EACH WITH ITS RULED STATUS

| leg | subject | 👤 status |
|---|---|---|
| **L1** | **`:732-734` ordering** — `hashes[path] = cur` runs before the `None` skip | ✅ 👤 **APPROVED as the first engineering fix** — ⚠️ within a **DEDICATED monitor change**, ⛔ not opportunistically |
| **L2** | **root-side helper** for `/etc/sudoers` + `/etc/sudoers.d` | ⛔ **NOT AUTHORISED** — a privilege-boundary redesign |
| **L3** | **`sudo_whitelist_prefixes`** | ⛔ **NOT AUTHORISED** — must become **path-sensitive** |
| **L4** | **`NOPASSWD: ALL`** | 👤 **A SEPARATE HOST-PRIVILEGE DECISION** — ⛔ not part of NI-15 |

#### L1 — the invariant, stated so the fix cannot be written wrong

> ⭐ **A `None` observation must NEVER overwrite a valid baseline.** Retain the previous hash and
> record an explicit `unreadable / missing` state.
> ⚠️ **And the trap that follows from it:** a later `HASH_B` must ⛔ **not** be treated as a first
> observation because the file vanished once. ⭐ `HASH_A → gone → HASH_B` is a **change**, and it
> must alert as one.

🔬 Closes delete-and-replace for **all eight** watched paths. ⛔ Does **nothing** for sudoers —
that is L2.

#### L2 — what a design must contain before any code

⭐ The measurement proves the **NEED for a design**, ⛔ not the design. Required: threat model ·
exact interface · least-privilege **path contract** · failure behaviour · installation ownership ·
independent tests · ⭐ **and proof the helper cannot itself become an escalation path.**
⚠️ 🔬 Note the standing constraint it must live with: **deploy does not install unit files** —
anything the helper needs under `/etc/` is a **manual VM act, forever.**

#### L3 — why "cat is bad" is the wrong shape

🔬 The whitelist exists because `/usr/bin/cat`, `/usr/bin/grep`, `/usr/bin/ss`, `/usr/bin/ps` are
**the watcher's OWN helpers** (`security.yaml` says so, verified 19-Jun). ⇒ ⛔ **editing it blindly
turns a control into noise** — 🔬 the check already fires **96** times a window; a naive widening
would bury the real event. ⭐ It must key on **(binary, target path)**, ⛔ not binary alone.

#### L4 — the separate decision

🔬 `(ALL) NOPASSWD: ALL` is a **cloud-init default from 03-May-2026**, ⛔ not a decision anyone
made. ⚠️ Revoking it would break **every operator sudo path**, including this campaign's own
read-only measurements. ⭐ It is the only lever that moves this from **detection** back to
**prevention** — 👤 and it is a change to **the box**, ⛔ not to code.

### 🏷️ NI-15 CLOSES

🏷️ **NI-15 = `BLOCKED → F13-L1 / F13-L2`.** ⛔ Not `open`. ⛔ Not `fixed`. ⭐ Its measurement is
complete and is what opened F13.

---

## §4 — 🔬 STATE

🔬 `origin/main` = **`742d9da`**, by `ls-remote`. ⛔ Three units held local: `fix/ni-batch-23aug`
`b397806` (8) · `a4a5cef` NI-5 (1) · `63e0d3d` governance (1).
⭐ NI totals unchanged: **COMPLETED 7 · COMMITTED ONLY 7 · DEPLOYED 0 · BLOCKED 3.**
👤 **Still unanswered: D-3** (`tier_multipliers` — split or keep; one dict serves both books)
and **D-4** (push scope).
⭐ Stacking stands: **batch first**, NI-5 refits and **re-gates** after — ⛔ its current gate dies
the moment the batch lands.
⛔ F2 gated on 👤 build-fresh-vs-recover and 🔴 the MIS ×3.5 ruling (HELD). ⛔ NI-16 **BLOCKED ON
F2**, ⛔ not open.

⚠️ **Found en route, ⛔ not fixed:** `MEMORY.md` is **27.8 KB against a 24.4 KB read limit** — the
truncation warning fires at session start, so part of HOT does not load. The HOT line carrying
this thread's DO-NOT is at **444 / 450 bytes** ⇒ ⛔ **no room remains to elevate the §1 chain into
HOT.** It is recorded in the ledger and on the BOARD instead. 👤 Rama's call.
