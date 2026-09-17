# `SYSTEM_MAP` CORRECTED · 🔴 WHAT MEMORY IS NOT LOADING, NAMED · `WC-PATTERN #10` INSTANCE 3

**23-Aug-2026, ~19:30 IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **ONE AUTHORISED DOC FIX + MEASUREMENT.** ⛔ No code · ⛔ no VM change · ⛔ no push ·
⛔ no F13 leg built · ⛔ memory NOT restructured.

**Provenance:** 🔬 measured · 📄 from evidence · 💭 inference · 👤 Rama's.

---

## §1 — ✅ `SYSTEM_MAP` CORRECTED — ⚠️ AND THE PREMISE FOR *"ITS OWN COMMIT"* DID NOT HOLD

👤 **AUTHORISED:** correct the *"pins the Control Tower security panel to `warn` FOREVER"* claim,
as its own commit.

### 🔬 MEASURED FIRST — THE CLAIM IS **UNCOMMITTED WORKING-TREE CONTENT**, ⛔ NOT COMMITTED

| where | occurrences of the FOREVER claim |
|---|---|
| `HEAD:docs/SYSTEM_MAP.md` | 🔬 **0** |
| `origin/main:docs/SYSTEM_MAP.md` | 🔬 **0** |
| working tree | 🔬 **1** |

🔬 `docs/SYSTEM_MAP.md` carries **150 uncommitted insertions in 2 hunks** (`@@ -47,0 +48,70 @@` and
`@@ -49,0 +120,80 @@`); the target line **53** sits **inside hunk 1's added range (48–117)**.

⇒ ⭐ **The stale claim was never published — it is one line of a 150-line block still in flight.**
⇒ ⛔ **"Its own commit" would fragment that block**, leaving 1 line committed and 149 not, out of
order. ⭐ **Corrected in place instead**, inside the block it belongs to. 👤 Flagged rather than
forced — ⭐ the authorisation was sound, its premise simply was not.

### ✅ THE CORRECTION, AND THE CONTROL THAT IT CHANGED NOTHING ELSE

**Replaced** *(one exact-string substitution, `assert count == 1`)*:
> *"NI-14: its standing INFO `rootspike` finding pins the Control Tower security panel to `warn`
> FOREVER (`aggregator.py:80` treats any finding, INFO included, as warn)."*

**With the measured behaviour** — 39.8% clean passes · the sole-contributor reading · the real
defect (severity-blindness at `aggregator.py:88-89`) · ⚠️ and the corrected line number
(`:80` → `:88-89`, 🔬 measured) · citing
`docs/audit/F13_OPENED_AND_D1_SEPARATION_23-Aug-2026.md`.

| control | before | after |
|---|---|---|
| FOREVER claim present | 1 | 🔬 **0** |
| correction present | 0 | 🔬 **1** |
| `git diff --stat` | 150 insertions | 🔬 **150 insertions** |
| hunk count | 2 | 🔬 **2** |

⇒ ⭐ **The diff shape is unchanged** ⇒ 🔬 no committed content touched, no new hunk created, ⛔ no
doc sweep. ⭐ Exactly one line replaced.

⚠️ **Found en route:** 🔬 the cron adapter repeats the **identical** severity-blind expression at
`aggregator.py:137-138`. ⇒ ⭐ **D-1b is not security-specific — it is a shared shape across
adapters.** ⛔ Recorded, ⛔ not chased, ⛔ not fixed.

---

## §2 — 🔬 M-1: **WHICH CONTENT DOES NOT LOAD** — NAMED, ⛔ NOT COUNTED

### The limit is on **characters**, and the model is corroborated by this session's own render

🔬 `MEMORY.md` = **25,841 chars / 27,758 bytes / 130 lines.** The harness reported
*"25.3KB (limit: 24.4KB)"* — 🔬 **25.3 KiB matches the CHARACTER count at session start
(≈25,673 chars), ⛔ not the byte count (27,581).** ⇒ limit = `24.4 × 1024` = **24,985 chars**.

⭐ **CONTROL:** the last line this session actually received was **L121** (`PAPER CANNOT EXERCISE
IT — named class`), which starts at char **24,614** — 🔬 **the last line that fits entirely below
24,985.** ⇒ the character-limit model **predicts the observed cut exactly.**

### 🔴 THE UN-LOADED REGION, BY CONTENT

**The cut falls inside L122. Everything from there to EOF — 856 chars, 9 lines — did not load:**

| line | content that DID NOT LOAD |
|---|---|
| **L122** *(cut mid-line)* | 🧪 *"A FIXTURE ASSERTING WHAT ITS OWN DATA CANNOT SUPPORT MAKES A WRONG READER LOOK RIGHT"* |
| **L123** | 💾⛔ *"**NEVER `Path.write_text` to plant/restore a source file** — rewrites EVERY newline to CRLF. ⚠️ `git diff` HIDES it; only md5 + a byte count expose it."* |
| **L125** | 🔴 **`## The CAREFUL-LOOP queue (capital/signal path — ⛔ never sweep these)`** |
| **L126** | 🔴 ⛔ *"The queue lives on the BOARD. **The RULE stays here: anything touching capital, kill, order, schema, sizing or a live trading decision goes through the careful loop — design → review → implement. Unsure ⇒ LOOP.**"* |
| **L128** | 🔴 **`## RAMA-ACTIONS owed`** |
| **L129** | 🔴 ⏰ *"The LIST lives on the BOARD. **Only the DEADLINE one stays here: COMMIT NSE's `nse_holidays_2027.yaml` BEFORE 31-Dec-2026 — the first 08:15 boot of 2027 does NOT start. ⛔ NEVER invent the dates.**"* |

### ⇒ 🔴 THE IRONY IS EXACT, AND IT IS THE FINDING

> 🔴 **The file's own placement discipline pushed the *lists* out to the BOARD and deliberately
> kept the two *RULES* in HOT — each marked "stays here". The truncation then dropped precisely
> those two kept rules and preserved the pointers.**

⇒ 🔴 **What does not load is (i) the governing rule for every capital / kill / order / schema /
sizing change, and (ii) the only hard calendar deadline in all of memory.** ⛔ Not filler.
⚠️ Plus a silent-corruption DO-NOT (`write_text` → CRLF, **invisible to `git diff`**) — ⭐ itself an
"a control that reports healthy and does not do its job" item.

⭐ **Mitigation that is real, stated fairly:** both bodies **do** live on `MEMORY_BOARD.md`, and
the 2027-holiday item **also emails from 15-Dec** (`cbcad2c`). ⚠️ But the BOARD is read *"before
any batch"*, ⛔ not auto-loaded ⇒ **a session that does not open the BOARD gets neither.**

### ⚠️ AND MY OWN CONTRIBUTION, MEASURED

🔬 Tonight's three HOT edits were all to **one** line (L78), net **+168 chars / +177 bytes**.
⇒ overflow **688 chars at session start → 856 chars now.** ⛔ **I made it measurably worse**, by
roughly one additional line pushed past the cut, while recording findings about controls that
silently fail.

---

## §3 — 🔬 M-2: **SINCE WHEN** — TODAY, AND THE PREVIOUS SESSION WAS CLEAN

| probe | result |
|---|---|
| transcripts searched | 🔬 **96 sessions, 2026-07-25 → 2026-08-23** (full retained window) |
| files containing *"Only part of it was loaded"* | 🔬 **1** — `22979f96…`, **this session** |
| ⭐ is the probe non-vacuous? | ✅ **yes** — it matches a warning I demonstrably received; the string is proven to fire |
| the immediately previous session (`1378a38c`, **23-Aug 16:12** — the NI-batch session) | 🔬 **clean** |
| sessions/day in the run-up | 🔬 18-Aug 2 · 19-Aug 2 · 20-Aug 3 · 21-Aug 1 · 22-Aug 2 · 23-Aug 3 |

⇒ 🔬 **The truncation began TODAY, in this session. It has never fired before in 30 days of
retained transcripts.**
⇒ 💭 **The crossing happened in the window between the 16:12 session's memory writes and this
session's start** — i.e. the NI-batch memory pass pushed it over.
⭐ **Consistent with the BOARD's own note:** at the **10-Aug close** the file was `~21 KB` and the
line explicitly records *"(24.4 KB read limit: still loads.)"*.

⚠️ **What this does NOT license:** ⛔ *"sessions have been running on partial memory for weeks"* is
**refuted** for the retained window. ⛔ And it therefore ⛔ **cannot** explain the 15-day
`65b7196` gap or the 18-day sudo inference — 💭 those predate the crossing. ⭐ The mechanism is
real and newly live; ⛔ it has no established victims yet.

🔬 **Growth curve, from the surviving snapshots:** 19-Jul **22,657** → 19-Jul(later) **23,717** →
20-Jul **22,774** → 24-Jul **20,073** → 25-Jul post-split **16,992** → *(10-Aug ≈21 KB, per the
BOARD)* → **23-Aug 25,725 → 25,841.** ⇒ ⭐ **+8,800 chars in the 29 days since the last split.**

---

## §4 — 👤 M-3: OPTIONS AND COSTS — ⛔ NONE CHOSEN

**Recovery needed: 856 chars** (and headroom on top, or it re-crosses within days at the measured
growth rate).

| | option | 🔬 measured cost |
|---|---|---|
| **(a)** | **Relocate to topic files** — the NI-8 approach | 🔴 **Nearly exhausted.** The BOARD records that at the 10-Aug pass only **2 of 70** entries were relocatable under the file's own rule; **the other 68 are all hazard / DO-NOT / invariant / rule.** ⇒ hitting the number means **DEMOTING HAZARDS** — 👤 his call, unchanged |
| **(b)** | **Split `MEMORY.md` again** | ⚠️ Only `MEMORY.md` auto-loads ⇒ a split **moves content out of auto-load** — the same outcome as truncation. ⭐ Its one virtue: **deliberate and known**, ⛔ not silent |
| **(c)** | **Reorder so the cut lands on the least load-bearing lines** | ⭐ **Cheapest real mitigation, ~0 cost, demotes nothing.** ⛔ It does not stop the silent cut — it only chooses what falls off. ⚠️ Today it would move the careful-loop rule and the 2027 deadline **above** the line |
| **(d)** | **Trim within existing lines** | 🔬 **31 lines exceed 300 chars, totalling 11,244 chars.** Recovering 856 = **≈28 chars off each (~7%)**. ⭐ Demotes nothing, deletes no entry — ⚠️ costs prose density on the longest hazards |
| — | ⛔ **raise the cap** | ⛔ Ruled out by the card. ⛔ Not costed |

💭 **(c) + (d) together** would clear the overflow with **zero demotion**; (a) and (b) are the ones
that trade content. ⛔ **Not chosen. ⛔ Memory not restructured.** 👤 To be decided with M-1's list
in front of him.

⚠️ **And one property worth naming:** 🔴 **the file cannot warn about its own truncation from
inside itself** — any warning line placed in the un-loaded region is, by definition, not read.
⭐ The harness banner is the only signal, ⛔ and it appears once, at session start.

---

## §5 — `WC-PATTERN #10` · **INSTANCE 3** — AN INVENTORY READ AS A MECHANISM

📄 **The claim:** *"any finding from any of eleven checks pins the status; raising 400 removes one
contributor and leaves ten."*
🔬 **The measurement:** the Control Tower reads **one file**; live `last_run.json` shows
`findings_count: 1`, `persistent: ["rootspike:…"]` ⇒ **rootspike is the sole contributor**, and
**39.8% of today's passes were clean.**

⭐ **HOW it went wrong is the recordable part:** the mechanism was inferred from an **inventory
count** — my own 65-day tally of eleven alert *types* — instead of from **the state the mechanism
actually writes.** ⇒ ⭐ **A true datum, a wrong reading, and the reading carried as the mechanism**
— 🔴 the exact `WC-PATTERN #10` shape, filed as **instance 3** alongside *"`N9-10` is recorded
against `65b7196`"* and *"the register describes a system that does not exist."*

### ⭐ THE DURABLE RULE

> ⛔ **AN INVENTORY OF OUTPUTS IS NOT A MODEL OF THE MECHANISM.** To claim how something behaves,
> read **the state it writes**, ⛔ never the log of what it has emitted.

⚠️ ⭐ **And the trend is the encouraging half, so record it too:** instance 1 (05-Aug sudo) stood
**18 days**; instance 3 was caught **inside the hour**, by one `cat` of a live state file.
⇒ ⭐ **The countermeasure that worked was not vigilance — it was reading production state before
repeating a claim.** ⛔ Three instances in three cards means the reflex is not yet automatic.

---

## 🏷️ STATUS

🏷️ **ONE DOC LINE CORRECTED (uncommitted block, in place) · MEASURED · ⛔ NOTHING ELSE FIXED ·
⛔ NOT PUSHED · ⛔ NO VM CHANGE · ⛔ MEMORY NOT RESTRUCTURED.**
🔬 `origin/main` = `742d9da`. 👤 **Open: D-3 · D-4 · D-1b · M-3's choice · F13 legs L1–L4.**
