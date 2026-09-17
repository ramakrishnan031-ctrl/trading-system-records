# NI-14 · NI-15 · NI-16 — MEASURED, ⛔ NOT FIXED · 23-Aug-2026

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`). Base **`742d9da`**.
🏷️ **MEASUREMENT ONLY. ⛔ No threshold invented · ⛔ no directory added to the watch list ·
⛔ `max_multiplier` untouched.** Each ends with the decision it makes answerable.

---

# NI-14 · THE ROOT-PROBE THRESHOLD

**The setting:** `config/security.yaml:22` `root_probe_spike_threshold: 400`, mirrored at
`scripts/security_monitor.py:113` with the comment *"per hour (constant noise; alert only
on anomaly)"*. It fires when `scan["root_probes"] > threshold`
(`check_root_probe_spike`, `:695-700`); a probe is a line matching
`_ROOT_PROBE_RE = re.compile(r"authenticating user root")` (`:88`).

## 🔬 IS THERE A DOCUMENTED DERIVATION? **NO.**

`git log -S'root_probe_spike_threshold'` returns exactly one commit — **`a701b0d`**
*"VM Security Manager Phase 1 — monitoring + alerts (build)"*. Its message names the
check (*"root-probe spike"*) and gives **no derivation for 400**. ⭐ The inline comment
is a **rationale**, ⛔ not a measurement.

## 🔬 THE MEASUREMENT — 184 hours of production `auth.log`

Read-only, from `/var/log/auth.log` + `auth.log.1` (16-Aug → 23-Aug), **60,009 probes**
bucketed per hour:

| | probes/hour |
|---|---|
| min | **7** |
| **median** | **331** |
| p90 | **406** |
| p99 | **459** |
| max | **512** |
| **hours exceeding 400** | 🔴 **23 of 184 = 12.5%** |

## 🔴 WHAT THIS SETTLES — AND ONE CORRECTION TO NI-14's OWN SHORTHAND

- **400 sits at roughly the p88 of ordinary background noise.** The comment *"alert only
  on anomaly"* is **false as measured**: it alerts on the top ~12% of an ordinary
  distribution, ⭐ about **three times a day**, on internet scanning that key-only auth
  already blocks.
- ⚠️ **CORRECTION:** NI-14 has been carried as *"a threshold that always fires"*.
  🔬 **It does not always fire — it fires on 12.5% of hours.** The defect is real but the
  shorthand overstates it: it is a threshold set **inside** the noise band, ⛔ not one
  pinned below it.
- ⭐ **The earlier correction stands:** a WARNING→MEDIUM finding is still visible in
  counts, `open_severities`, `health.score_and_band` and the push path. ⛔ It is the
  STATUS signal that lost discrimination, ⛔ not the pipeline.

## 👤 THE DECISION — ⛔ NOT TAKEN

Three options, each now costed against the distribution above:

| option | consequence at the measured numbers |
|---|---|
| **raise the threshold** | to clear observed noise entirely it must exceed **512**; ~**600** gives ~17% headroom over max. ⚠️ Anything ≤ 512 still fires on a quiet week |
| **have status ignore INFO-only findings** | leaves 400 firing but stops it flattening the status signal. ⛔ Does not reduce the noise itself |
| **exclude known-noisy keys from `clean`** | narrowest change; the probe finding stops contributing to `clean` while remaining visible |

⛔ I have not chosen. ⛔ No number invented.

---

# NI-15 · THE WATCHER CONTRACT — 🔴 ADDING THE DIRECTORY WOULD BE FALSE PROTECTION

**Measured by executing the real functions** (`sha256_file`, `check_watched_files`,
`_default_watched_files`) against a temporary `unit.service.d/` tree:

| question the card asked | 🔬 measured answer |
|---|---|
| hashes CONTENTS or metadata? | **CONTENTS** — sha256 of the file's bytes |
| does it accept a DIRECTORY? | 🔴 **NO.** `sha256_file(<dir>)` returns **`None`**, and `check_watched_files` does `if cur is None: continue` ⇒ **silently skipped** |
| does it recurse into `*.d/*.conf`? | 🔴 **NO.** The list is explicit regular-file paths; no directory appears in `_default_watched_files()` |
| MODIFY fires? | ✅ **YES** — `Sensitive file changed: <label>` |
| **ADD a new drop-in fires?** | 🔴 **NO — SILENT.** *This is the case that matters most* |
| REMOVE fires? | 🔴 **NO — SILENT** |

## ⇒ THE CARD'S CONCERN IS CONFIRMED BY MEASUREMENT

⛔ **Putting `/etc/systemd/system/trading-system.service.d/` in the watch list would add a
row that can never fire.** It would read as coverage and provide none — **worse than the
admitted gap**, exactly as the card predicted. ⭐ Any real fix must add *enumeration* of
the directory's contents, ⛔ not a path.

## 🔴 A SECOND FINDING THE CARD DID NOT ASK FOR — **DELETION IS INVISIBLE**

`if cur is None: continue` treats *absent* and *unreadable* identically to *skip*. ⇒ 🔴
**deleting a watched file raises NO alert.** That applies to every CRITICAL row in
`_default_watched_files()` — `/etc/sudoers`, `/etc/ssh/sshd_config`,
`/home/ubuntu/.ssh/authorized_keys`, `.env`, and both unit files.
⭐ An integrity monitor that cannot see a file removed is a materially larger gap than one
that cannot see a directory grow. ⛔ Recorded, ⛔ not fixed — it is a severity/behaviour
change and belongs to the same decision.

---

# NI-16 · ⛔ CANNOT BE BUILT — **BLOCKED ON F2**, ⛔ not "open"

🔬 Re-verified at `742d9da` (the deployed SHA) today:

| fact | measured |
|---|---|
| the FIX-133 expression `max(1, min(tiered_qty, raw_qty * 2))` | **PRESENT** (1 occurrence) |
| the clamp `min(1.0, …)` | **ABSENT** (0) |
| `capital/pipeline_policy.py` | **ABSENT** (not in the tree) |
| `allocation_divisor` | **0 hits** repo-wide |
| `max_multiplier` | **2.0, untouched** |

**Why it cannot be built, stated precisely rather than vaguely:**

1. Deployed does not merely *lack* the clamp — it **carries the exact FIX-133 expression
   that `65b7196` DELETED as forbidden**. It is the presence of a thing a later LOCKED
   decision removed, ⛔ not an absent protection.
2. `min(1.0, …)` clamps a multiplier **to ONE ALLOCATION**.
3. 🔴 **Deployed COMPUTES NO ALLOCATION.** The machinery that would produce one
   (`pipeline_policy.py`, `allocation_divisor`, `base_allocation`) exists **only** in the
   undeployed `65b7196`.

⇒ 🔴 **PORTING THE CLAMP WOULD NOT IMPLEMENT NI-16.** Dropped onto deployed it would
clamp `tier × perf_weight` to 1.0 against a rung that is **10% of TOTAL CAPITAL** — a
different rule wearing the locked policy's words.

🏷️ **STATUS: `BLOCKED ON F2`.** It is F2's dependency, ⛔ not a bug fix, and it will still
be open at the end of this batch. ⭐ **NI-18 has removed its worst side-effect** — the
`constraint` field no longer names a rung the quantity exceeds, so whoever debugs the
allocator when NI-16 does land will not be misled by the audit column.
