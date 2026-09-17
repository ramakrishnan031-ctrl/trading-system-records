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
