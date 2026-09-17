# PREDICTION — REGISTRY SEED/STATE SPLIT (unit `5094a32`)

**Written:** 2026-08-14, frozen at **19:33 IST**, ⛔ **BEFORE the push.**
**Unit:** `5094a3288054b239c8821be72f09357f938d6ba5` — the **sole deployable target**.
`b27cf6a` is its **parent**, ⛔ **not a second target**.
**Deploys onto:** `origin/main` = `1c8c710bf4df60fcca8b09375d6cd723590d3820`, resolved by
measurement at gate time, **two ways** (`git ls-remote refs/heads/main` + bare-repo
`git --git-dir=/home/ubuntu/trading-system.git rev-parse refs/heads/main`), both identical.
**Scoring window:** Monday **17-Aug-2026**, and specifically **16:22 IST**.

---

## §E — VOCABULARY DECLARED AVAILABLE UP FRONT

`NOT TESTED` and `CANNOT DETERMINE` are **available verdicts** for every line below and
carry **no penalty**. A line that cannot be decided by the evidence is to be written
`CANNOT DETERMINE`, ⛔ never softened into a pass, ⛔ never argued into one later.

Status labels are the campaign's: `BUILT` · `DEPLOYED` · `VERIFIED LIVE` · `PENDING` ·
`DEFERRED`. ⛔ The word "fixed" is not used.

## §F — THE CEILING, STATED IN ADVANCE

**Tonight reaches `DEPLOYED`. ⛔ NOTHING MORE.**

The ladder, and ⛔ never report a lower rung as a higher one:

| Rung | Claim | Reachable tonight? |
|---|---|---|
| ① | the file is on disk on the VM | ✅ **YES** — by md5, at D2 |
| ② | the **running process** loaded it | ⛔ **NO** — see §B; verdict tonight = `CANNOT DETERMINE` |
| ③ | the new behaviour is **correct** | ⛔ **NO** — needs Monday 16:22 |

⛔ `VERIFIED LIVE` requires the **Monday 16:22 officer run**. ⛔ It is not to be
manufactured by running the officer by hand tonight or over the weekend.

---

## §A — THE ACCEPTANCE CRITERION

🔑 **The criterion is ⛔ NOT "does the tracked yaml still diverge from HEAD".**

It is: **after the next officer run, does the git-TRACKED file stay UNCHANGED while the
runtime state goes somewhere else?**

Both halves are required. A run that leaves the tracked file alone *by not running at all*
satisfies the first half and fails the unit.

**The mechanism, measured ⛔ not recalled** (`git diff 1c8c710 5094a32`):

- `core/strategy_direction.py` splits one path into two —
  `DEFAULT_SEED_PATH = "config/strategy_direction_registry.yaml"` (git-tracked, **read-only
  in production**) and `DEFAULT_STATE_PATH = "data_store/strategy_direction_registry.yaml"`
  (**gitignored**, the only thing production writes).
- `load_registry(path, seed_path=...)` reads **STATE first**; the SEED is a **fallback only
  while no state file exists** — the first run after a deploy. ⛔ Never an override.
- `save_registry` writes **STATE only**, and `mkdir -p`s its parent.
- `main()` computes `registry_path = _ROOT/"data_store"/...` and `seed_path = config_dir/...`.

**Today's 16:22 run was the PRE-FIX CONTROL and is measured:**
tracked yaml **5,745 B → 3,734 B (−2,011 B)**, mtime `2026-08-14 16:22:01.809525263 +0530`,
md5 `95933445979bbccb1e8292f3e4cc0074`, `cron_heartbeat` id 4724 `SUCCESS 0.2938s`.
The deployed-tree drift it produced is exactly what `system_manager` reported at 18:45 as its
**1 violation**: `config/strategy_direction_registry.yaml | 29 insertions(+), 54 deletions(-)`.

⭐ **What the −2,011 B actually is, measured:** the officer's `yaml.safe_dump` **cannot
preserve comments**, so each run **strips the 24-line documentation header off a git-tracked
config file**. The remainder is `PENDING → CONFIRMED` advances and quote normalisation
(`"2026-07-17"` → `'2026-07-17'`). Row count is **unchanged at 16 both sides** — ⛔ the officer
is not pruning strategies, it is rewriting the file.

⇒ 🔑 **Tonight's push cannot test this, and Monday's 08:15 boot cannot either.** The officer
is a **cron job at 16:22 Mon–Fri** (crontab line 124), ⛔ not part of `trading-system.service`.
**The post-fix window is Monday 17-Aug 16:22.**

## §B — THE PRESENCE SIGNATURE

📌 **The F7 lesson applies: F1–F6 were all ABSENCE-signatures and a discriminator had to be
bolted on 29 seconds before the push. ⛔ That is not repeated here.**

**The signature is a PRESENCE one, and it is named in advance:**

> **`data_store/strategy_direction_registry.yaml` EXISTS on the VM.**

**Proven discriminating — the currently deployed build cannot produce it:**
- at `1c8c710`, `save_registry`'s default is `DEFAULT_REGISTRY_PATH =
  "config/strategy_direction_registry.yaml"` and `main()` computes
  `registry_path = config_dir / "strategy_direction_registry.yaml"`;
- the old officer's **only two** `data_store` references are `_DEFAULT_DB` (`trading_system.db`)
  and a `sentinel_dir` — ⛔ neither writes a registry;
- crontab line 124 passes **no `--registry`** override, so the default governs in both builds.

**Pre-signature control, taken at 19:29:46 IST tonight, ⛔ before the push:** the path is
**ABSENT**. ⇒ ⭐ the reading is genuine, ⛔ not stale, and the signature **could go red**.

### 🔑 AND THE HONEST VERDICT FOR TONIGHT — `CANNOT DETERMINE`

The signature is well-defined, discriminating and falsifiable — **and it is ⛔ NOT OBSERVABLE
IN TONIGHT'S WINDOW**, because only an officer run can produce it and the next one is
Monday 16:22.

⇒ **Rung ② (the running process loaded the new code) is recorded tonight as
`CANNOT DETERMINE`.** ⛔ No substitute signature is bolted on. ⛔ `grep` on a source file
is rung ①, not rung ②, and is ⛔ not to be reported as evidence of loading.

## §C — EXPECTED STATE, WITH BYTE COUNTS

Derived from tonight's measured state. **Seed blob at `5094a32`: 5,745 B, md5
`f87787ff53aae551fb7136e2b73df196`, 16 strategy rows — byte-identical to the seed at
`1c8c710` ⇒ ⛔ this unit does not touch the seed file.**

| When | `config/…registry.yaml` (TRACKED) | `data_store/…registry.yaml` (STATE) |
|---|---|---|
| now, pre-push (19:29 IST) | **3,734 B**, md5 `95933445…` | **ABSENT** |
| **tonight, right after the push** | **5,745 B**, md5 `f87787ff53aae551fb7136e2b73df196` — the hook's `checkout -f` resets it to seed | **ABSENT** (unchanged) |
| **Mon 08:15 boot** | **5,745 B**, unchanged | **ABSENT** — ⛔ the boot does not run the officer |
| **Mon 16:22, after the officer** | 🔑 **5,745 B, STILL md5 `f87787ff…` — UNCHANGED. This is the whole claim.** | 🔑 **CREATED, ≈3,734 B** |

**On the ≈ in 3,734 B — the uncertainty is named, ⛔ not hidden.** Monday's officer reads the
seed (all **16 rows PENDING**) and advances to CONFIRMED on filled trades, exactly as today's
run did. Today's output was **13 CONFIRMED / 3 PENDING**; the three still PENDING are
**`pb01_breakout_retest`, `range_breakout_long`, `range_breakout_short`**. If any of the three
takes a filled trade on Monday, the state file differs slightly from 3,734 B and md5
`95933445…`. ⇒ ⛔ **The exact byte count is NOT the falsifier. The falsifiers are §D.**

**Predicted 18:45 `system_manager` on Monday:** the deployed-tree violation for this file
**disappears** ⇒ **0 violations from this cause**. ⛔ This does not predict `0v` overall —
any other file may drift independently, and that would be a different finding.

## §D — FALSIFIERS

⛔ **Without these it is not a prediction.** Any ONE firing means the unit did not do what it
claims. Score each independently; ⛔ do not let a pass on one excuse a fail on another.

| # | Falsifier — the unit is WRONG if… | Measured by |
|---|---|---|
| **F1** | after Monday 16:22, `config/strategy_direction_registry.yaml` md5 ≠ `f87787ff53aae551fb7136e2b73df196` | `md5sum` on the VM |
| **F2** | after Monday 16:22, `data_store/strategy_direction_registry.yaml` is still **ABSENT** | `stat` on the VM |
| **F3** | the 16:22 officer run **did not happen or failed** — then F1/F2 are `NOT TESTED`, ⛔ **never a pass** | `cron_marks/strategy_registry_officer.done` + `cron_heartbeat` |
| **F4** | Monday's 18:45 `system_manager` **still** names `config/strategy_direction_registry.yaml` in its deployed-tree violation | `logs/system-manager.log` |
| **F5** | the state file is created but the officer **re-announces strategies as NEW** (a Telegram/email burst naming already-registered strategies) ⇒ the seed fallback did not work and provenance was lost | alert stream + `first_seen` dates in the state file |
| **F6** | any consumer breaks because it read the new default path and got `{}` | boot/EOD logs Monday |
| **F7** | tonight: after the push, the deployed tree differs from HEAD in **any file other than** `config/strategy_direction_registry.yaml` | `git --git-dir=… diff --stat HEAD` |

**F6's risk was measured tonight and is CLOSED in advance, ⛔ not assumed:**
`git grep` over the tracked tree at `5094a32` finds **exactly one production caller** of
`load_registry`/`save_registry` — `scripts/strategy_registry_officer.py`, which passes
`seed_path`. The other matches are `core/effect_telemetry.py`'s **private** `_load_registry`
over `config/expected_managers.yaml`, an unrelated registry. ⇒ F6 is expected **not** to fire;
it stays listed because a prediction that only lists what it expects is not a falsifier set.

**Gitignore, verified ⛔ not assumed:** `git check-ignore -v` →
`.gitignore:17:data_store/` matches `data_store/strategy_direction_registry.yaml` ⇒ the deploy
hook's `checkout -f` will leave state alone. **This is the design's load-bearing assumption.**

⚠️ **Recorded from the code's own comment, ⛔ not re-derived:** untracking the seed instead was
**measured to DELETE the live file on the first deploy** (`checkout -f` removes a path tracked
at the old HEAD). That is why the seed stays tracked. ⛔ Do not "simplify" this later.

## §G — WHAT TONIGHT DOES *NOT* CLAIM

- ⛔ Not `VERIFIED LIVE`. ⛔ Not "the daily CRITICAL is gone" — that is scored Monday 18:45.
- ⛔ Not that the 16:22 run will be silent; a first-run-after-deploy may legitimately notify.
- ⛔ The registry yaml being dirty on the VM **right now** is **expected**, ⛔ not a finding,
  ⛔ not a blocker — it is the pre-fix control this prediction is scored against.

<!-- FROZEN-BOUNDARY — everything ABOVE this line is FROZEN. ⛔ No edit above it, especially if a call turns out wrong. Addenda go BELOW, appended only, each with its own timestamp. -->

## ADDENDA (append-only, below the boundary)

### ADDENDUM 1 — 2026-08-14, push executed 19:33:14 IST

**Pushed:** `git push origin 5094a3288054b239c8821be72f09357f938d6ba5:refs/heads/main`
→ `1c8c710..5094a32 -> main`, rc=0, fast-forward (⛔ no `+`, ⛔ no `!`, ⛔ no `--force`).
Deployed `HEAD` = `5094a32…`. Authorisation: Rama, quoted — *"push it."*

**§C's row for "tonight, right after the push" was stated BEFORE the push and is CONFIRMED:**
`config/strategy_direction_registry.yaml` = **5,745 B**, md5
**`f87787ff53aae551fb7136e2b73df196`**, mtime `2026-08-14 19:33:14.977098358 +0530` ⇒ the hook's
`checkout -f` reset it to seed exactly as predicted. **P7's first half confirmed a 2nd time.**

**D2 — PC == VM by md5 on all six files, ⛔ never by `ahead 0`. All six DIFFERED pre-push ⇒
the check could have gone red:**
`PATHS.md` `26c696e4…`→**`9fdf2acd…`** · `core/strategy_direction.py` `1d50da65…`→**`4e258727…`** ·
`docs/SYSTEM_MAP.md` `812f4b97…`→**`8647ee34…`** · `docs/audit/registry_seed_state_split_10aug2026.md`
**ABSENT**→**`fd03b52f…`** · `scripts/strategy_registry_officer.py` `daf022a3…`→**`8e41617a…`** ·
`tests/unit/test_registry_seed_state_split.py` **ABSENT**→**`b364c298…`**.

**F7 — did NOT fire:** deployed tree vs HEAD = **ZERO differing tracked files**.
**STATE file `data_store/strategy_direction_registry.yaml`: still ABSENT**, correct — the next
officer run is Mon 16:22. ⇒ **Rung ② remains `CANNOT DETERMINE`, exactly as §B stated in advance.**

⚠️ **P8 / `N13-11` HOLDS A THIRD TIME:** the hook printed *"post-receive: crontab AUTO-INSTALLED
from canonical."* and the crontab **did not move** — md5 `b8276da7043975cda2d0ce6578960c6a` and
**46** job lines, IDENTICAL before and after. ⛔ The message states the install RAN, ⛔ not that
content changed. ⭐ Measure the crontab; ⛔ never read the hook's message as a diff.

✅ **⛔ Service NOT started** (`inactive`/`dead`, `NRestarts=0`, `InactiveEnterTimestamp` still
`Fri 2026-08-14 17:35:05 IST`). ✅ **Kill state UNTOUCHED** (`SOFT_KILL` /
`circuit_breaker_force_close_15:15` / `2026-08-14T15:15:00.527210+05:30`). ⛔ `resume.sh` not run.

🏷️ **STATUS = `DEPLOYED`. ⛔ NOT `VERIFIED LIVE`.** Scoring is Monday 17-Aug 16:22, per §A/§D.

### ADDENDUM 2 — 2026-08-17, SCORED AT THE 16:22 WINDOW (probe run 16:22:32 IST)

🏷️ **STATUS ADVANCES `DEPLOYED` → `VERIFIED LIVE`.** ⭐ A production artifact was
observed: the officer's own 16:22 run, its `cron_heartbeat` row, and the state file
it created. ⛔ The officer was **NOT** run by hand at any point.

**Each falsifier scored SEPARATELY. ⛔ No pass on one was allowed to excuse another.**

| # | Falsifier | Verdict | Evidence |
|---|---|---|---|
| **F3** | officer did not run / failed | ✅ **DID NOT FIRE** | mark `0 2026-08-17T16:22:01+05:30` (rc **0**), mtime `16:22:01.894`; `cron_heartbeat` **id 4846**, `2026-08-17T16:22:01.802342`, **SUCCESS 0.29728 s** — a NEW row, id > 4724 |
| **F1** | tracked yaml md5 ≠ `f87787ff…` | ✅ **DID NOT FIRE** | md5 **`f87787ff53aae551fb7136e2b73df196`**, **5,745 B**, mtime **still `2026-08-14 19:33:14.977098358`** — ⭐ the officer ran and did **not touch the file**, which is the whole claim |
| **F2** | state file still ABSENT | ✅ **DID NOT FIRE** | `data_store/strategy_direction_registry.yaml` **CREATED**, **3,734 B**, mtime `2026-08-17 16:22:01.794991551`, md5 `95933445979bbccb1e8292f3e4cc0074` |
| **F4** | 18:45 `system_manager` still names the yaml | ⏳ **PENDING — window not reached** | scored at 16:22; the 18:45 job has not run. ⛔ Deliberately NOT scored as a pass |
| **F5** | strategies re-announced as NEW | ✅ **DID NOT FIRE** | **all 16 rows `first_seen: '2026-07-17'`** — provenance CARRIED, ⛔ not reset to today; alert-burst grep count **0** |
| **F6** | a consumer got `{}` | ✅ **DID NOT FIRE** | grep count **0** in today's system log |
| **F7** | deployed tree differs in any other file | ✅ **DID NOT FIRE** | `GIT_INDEX_FILE` probe (§0's verified method), `read-tree` rc=0, **differing_count = 0**; bare index UNTOUCHED `322e1e8bad39b7b641868aa994c27f99`; deployed HEAD `6fa8a1c…` |

🔑 **F3 WAS SCORED FIRST, ON PURPOSE.** Had the officer not run, F1/F2 would have been
`NOT TESTED` — ⛔ never a pass. It ran, so F1 and F2 are genuine measurements.

⭐ **THE PRESENCE SIGNATURE §B NAMED IN ADVANCE IS SATISFIED:**
`data_store/strategy_direction_registry.yaml` **EXISTS**. §B proved the pre-fix build
could not produce that path, and §0's 09:28 + this morning's 10:45 controls both read
**ABSENT** ⇒ ⭐ **the check could have gone red, and the reading is genuine.**

📏 **§C's PREDICTED TABLE, ROW BY ROW — BOTH HALVES CONFIRMED:**
tracked **5,745 B / `f87787ff…` UNCHANGED** ✅ · state **CREATED at 3,734 B** ✅.
⭐ **The "≈" in §C resolved to EXACT:** the state file is **byte-for-byte the pre-fix
control** (3,734 B, md5 `95933445…`) and the split is **13 CONFIRMED / 3 PENDING**,
precisely as §C predicted. ⇒ none of `pb01_breakout_retest`, `range_breakout_long`,
`range_breakout_short` took a filled trade today — the named uncertainty did not
materialise. ⛔ The byte count was never the falsifier; this is corroboration, not the
test.

⚠️ **ONE PROBE LINE IS UNRELIABLE AND IS FLAGGED RATHER THAN QUOTED:** the row-count
`grep -cE '^[a-z_0-9]+:'` returned **1**, which is a bad pattern, ⛔ not a finding of
1 row. The reliable count is the status split (**13 + 3 = 16 rows**), which matches
the seed's 16 and the pre-fix control's *"row count unchanged at 16 both sides."*

✅ **Service healthy throughout:** `active`, MainPID **3851262** — the same PID as the
08:15 boot, so ⛔ nothing restarted around the window.

⛔ **WHAT THIS ADDENDUM STILL DOES NOT CLAIM.** F4 is unscored until 18:45. The daily
CRITICAL being *gone* is F4's question, ⛔ not this one. ⛔ No claim is made about any
file other than the two named.

### ADDENDUM 3 — 2026-08-17, F4 SCORED AT THE 18:45 WINDOW (read 18:46:16–18:47:19 IST)

**VERDICT: F4 DID NOT FIRE.** The daily false CRITICAL this unit existed to remove is
measurably gone.

**PROBE METHOD, VERIFIED BOTH WAYS BEFORE IT WAS TRUSTED.** `system_manager_eod` writes
no `cron_heartbeat` marker (crontab `45 18 * * 1-5`, appending to
`logs/system-manager.log`), so log mtime is the only evidence that it ran. The falsifier
was therefore stated in both directions *before* the window: mtime must advance from the
Aug-14 baseline, and only then does the content decide. mtime unchanged would have been
`NOT TESTED`, never a pass. The job was NOT run by hand; its scheduled execution is the
evidence.

| | value |
|---|---|
| baseline, measured 18:22 and again 18:35 | `2026-08-14 18:45:07.626977748`, size 178,577 B |
| after the window | **`2026-08-17 18:45:07.721408500`, size 183,200 B** (+4,623 B) |
| stability | two reads 46 s apart (18:46:33, 18:47:19) — size and mtime **identical** ⇒ write complete, not mid-file |

⇒ **mtime ADVANCED. The 18:45 job RAN.** `NOT TESTED` is excluded by measurement.

**VIOLATION COUNT: 0. WHAT IT NAMES: NOTHING.** Verbatim from the block:

```
🌳 DEPLOYED TREE vs HEAD
✅ deployed tree == HEAD (6fa8a1c) — no tracked drift, no untracked .py

SUMMARY: 0 violation(s), 6 warning(s)
```

**SEARCH WIDTH STATED BESIDE THE ZERO.** `config/strategy_direction_registry.yaml` does
not appear anywhere in the run. A case-insensitive grep over the ENTIRE 4,623-byte
appended block on four terms (`strategy_direction_registry|registry|drift|violation`)
returned exactly three hits, none of which is the yaml: `⚠️ Capital drift events: 4`
(capital drift, a different subsystem), the `deployed tree == HEAD` line above, and the
SUMMARY line. `strategy_direction_registry` occurs **zero** times. The absence was
checked wide enough to have found the thing.

**THE SIX WARNINGS, NAMED — a 0-violation run is not a silent run.** (1) `watchman.md
MISSING` (2) `flow_trace.md MISSING` — both are the known zero-crontab-entry finding,
every day loses that record; (3) `Kill switch: SOFT_KILL
(circuit_breaker_force_close_15:15)` — the routine 15:15; (4) `Capital drift events: 4`
— matches the four G3 ERRORs in the service log exactly, classified, NOT explained;
(5) `Strategy vwap_bounce_long: win_rate 33% over 21 — review`; (6) `P&L today ₹16.83 /
prev ₹3.95 — >2x deviation`, arithmetic on very small numbers. None is F4.

**CORROBORATION, NOT THE TEST.** The block independently reproduces figures measured
from other sources: `Trades: 6` and `reconstruct_excursions examined=6 written=6` and
six rows in `trades`; `Signals recv: today 5962` and `forward_shadow_record wrote=5962`;
`Service starts today: 1; crashes detected: 0` and systemd `NRestarts=0`; `gross ₹21.38
| charges ₹4.55 | net ₹16.83`. Day capital base stated by the report itself: ₹10,593 via
`fm_ledger`.

🔴 **NEW FINDING SURFACED BY THIS RUN — RECORDED, NOT FIXED.** The same block reports
`✅ Manual/external closes: 0` and `✅ Orphan detections: 0` on a day when
`cnc_gtt_monitor` logged TWO `orphan_active_gtt_flat` events with detail *"GTT active
but holding flat (external close)"* (15:20:44.353 SHANTIGOLD, 15:20:45.078 RATNAVEER),
and its own ORDER QUALITY section prints both as `GTT_EXIT`. ⇒ The empty
`closure_source` on the delivery rows propagates into the operator's EOD report as a
FALSE ZERO on two counters whose whole purpose is to surface exactly this event. This is
a measured downstream consequence of the delivery-path parity gap, ⛔ not a new
hypothesis. It is unrelated to F4 and does not affect this score.

⛔ **WHAT THIS ADDENDUM DOES NOT CLAIM.** F4 not firing tonight is one window on one
trading day; it is not a claim that the drift can never recur. No claim is made about
any file other than the registry yaml. The 6 warnings are named, not adjudicated. The
capital-drift decomposition remains classified, ⛔ not explained.

### ADDENDUM 4 — 2026-08-17, THE CONTROLLED BEFORE/AFTER, AND RAMA'S RULING

**RAMA'S RULING, QUOTED:** *"F4 DID NOT FIRE ⇒ all seven falsifiers scored ⇒ install ③
is fully VERIFIED LIVE, and the daily false CRITICAL this unit existed to remove is
measurably gone — 1 violation on 14-Aug, 0 tonight."*

**THE COMPARAND WAS VERIFIED FROM THE LOG, ⛔ NOT ACCEPTED ON ASSERTION** — and it is
stronger than a count. The violation on the two runs before the install was **the same
file with a byte-identical diffstat**, which makes this a controlled before/after rather
than a change in a number:

| run | HEAD | DEPLOYED TREE vs HEAD | SUMMARY |
|---|---|---|---|
| 13-Aug (Thu) | `2bfe9e2` | ❌ DIFFERS in 1 file — `config/strategy_direction_registry.yaml \| 83 ++++---` (29 ins, 54 del) | `1 violation(s), 8 warning(s)` |
| **14-Aug (Fri)** | `1c8c710` | ❌ DIFFERS in 1 file — `config/strategy_direction_registry.yaml \| 83 ++++---` (**29 ins, 54 del — identical**) | `1 violation(s), 7 warning(s)` |
| **17-Aug (Mon)** | **`6fa8a1c`** | ✅ **deployed tree == HEAD — no tracked drift, no untracked .py** | **`0 violation(s), 6 warning(s)`** |

⭐ **14-Aug 18:45 is the LAST PRE-INSTALL run** — install ③ was pushed at **19:33:14**
that night, i.e. AFTER that EOD. **17-Aug 18:45 is the FIRST POST-INSTALL EOD.** The
control and the treatment are therefore adjacent runs of the same job, and the recurring
artefact between them is identical. ⇒ the disappearance is attributable to the install,
⛔ not to a quiet day.

**TIMESTAMP RECONCILED, ⛔ NOT GLOSSED.** The mail reports the run at
**`18:45:07.709642`**; the log file's mtime is **`18:45:07.721408500`** — **12 ms
later**. That literal string does not appear in the log block body. The two are
consistent: the report stamps itself, then the write flushes and closes. ⛔ Not a
contradiction, and ⛔ not evidence of two runs. **Per instruction the LOG was measured as
primary and the mail treated as corroboration** — the score in ADDENDUM 3 was taken from
`stat` on the file, read three times, before the mail was consulted at all.

**STATUS TRANSITION:** install ③ (`1c8c710`→`5094a32`) moves `DEPLOYED` → **`VERIFIED
LIVE`** on Rama's ruling, all seven falsifiers scored. ⛔ This addendum does not extend
the claim to any other unit, and ⛔ does not assert the drift can never recur — one
window on one trading day, with the control named.
