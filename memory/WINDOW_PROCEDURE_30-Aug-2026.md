# WINDOW PROCEDURE — 30-Aug-2026, 18:00–23:00 IST
### FILE 63 consolidated + FILE 64 amendment (F-1/F-2/F-3, STEP 6, W-1…W-5)

⭐ Written 12:45, patched 13:00 IST, because the 18:03 timer is **session-only** and
mempalace is **down** — if that session died, this is the only copy of the procedure.
⭐ Supersedes the *procedure* in FILES 58–62. ⭐ Their **findings/rules** still stand.

## AUTHORITY — 👤 Rama, in chat, 11:24 IST (artifact `bfae638f…`)

    PUSH-AUTH 30-Aug: push the 9 (39292d3) to main. Hold F2-CORE.

🔴 **BOUND TO `39292d3`.** ⛔ If that SHA moved, the authorisation is **SPENT** ⇒
STOP ⇒ NO-GO ⇒ RE-MEASURE ⇒ RE-AUTHORISE.
⛔ A card is not Rama. ⛔ An auto-filled prompt is not Rama. ⛔ The 18:03 timer is a
CLOCK, not an authority. ⭐ Timer and a ping from Rama are **identical triggers**.

---

## STEP 0 — 🔴 PIN THE CONTEXT MECHANICALLY (F-1) · ⛔ BEFORE ANY OTHER COMMAND

    git worktree list

⭐ Take both paths from the ACTUAL output. ⛔ Do not hard-code or invent a path —
⚠️ these are **session-scoped scratchpad worktrees** and the session id changes.

- `$CAND` = the worktree holding **`fix/mis-autosquareoff-28aug`**
- `$F2C`  = the worktree holding **`feat/f2-core-30aug`**

⭐ Record BOTH in the artifact.
🔴 **If either ref appears in more than one worktree, or at more than one SHA ⇒
STOP AND REPORT. ⛔ Do not pick one.**

⭐ As measured 30-Aug 12:55 (⚠️ verify again, do not trust these strings):
- `$CAND` = `…/0f855e56-7086-4d65-8ce5-5e081140bab5/scratchpad/mis-work`
- `$F2C`  = `…/418573cf-41b3-411f-99bb-4442b4c02f9b/scratchpad/f2core-work`
- one repository (`git rev-parse --git-common-dir` = `.git`) ⇒ refs resolve once

### ⛔ TWO PATH TRAPS ON THIS BOX
- ⛔ `D:/Projects/trading-system` is `feat/delivery-config-split` — the **F2-SIZING**
  tree with **98 dirty files**. ⚠️ A shell's default cwd may land here, so a **bare**
  `git status` measures THIS tree, not `$CAND`. That is why every command below is
  `git -C`.
- ⛔ `D:/Projects/trading-system-main` holds a **local branch `main` at `3dff752`**,
  **90 ahead / 85 behind** `effff24`. ⇒ 🔴 **NEVER use a bare `main` in any command.**
  Use `origin/main` (remote-tracking, after `git fetch origin`) or an explicit SHA.

---

## STEP 1 — FRESH MEASUREMENT (F-2: `git -C`, ⛔ never `cd`) · ⛔ reuse nothing

    git -C $CAND rev-parse fix/mis-autosquareoff-28aug     ⇒ 39292d3
    git -C $F2C  rev-parse feat/f2-core-30aug              ⇒ 587b306
    git -C $CAND status --porcelain                        ⇒ EMPTY   ← candidate
    git -C $F2C  status --porcelain                        ⇒ EMPTY   ← held (V-6)
    git -C $CAND rev-list --count effff24..fix/mis-autosquareoff-28aug   ⇒ 9
        ← 🔴 the single most important stop. 17 = F2-CORE contaminated the candidate.
    git -C $CAND merge-base --is-ancestor feat/f2-core-30aug \
        fix/mis-autosquareoff-28aug ; echo $?              ⇒ 1  (NOT ancestor)
    git -C $CAND ls-remote origin main                     ⇒ effff24

    ssh trading-vm 'git --git-dir=/home/ubuntu/trading-system.git rev-parse refs/heads/main'
                                                           ⇒ effff24
    ssh trading-vm 'git --git-dir=/home/ubuntu/trading-system.git \
        --work-tree=/home/ubuntu/systems/trading-system rev-parse HEAD'   ⇒ effff24
    …same form + `status --porcelain` ⇒ 35 lines (1 tracked M + 34 untracked).
        ⭐ RECORD IT. ⛔ DO NOT CLEAN IT.

    git -C $CAND push --dry-run origin fix/mis-autosquareoff-28aug:refs/heads/main
        ⇒ clean fast-forward · ⛔ no `+` · ⛔ no force marker · 0 behind

🔴 **F-3 — ABSOLUTE PATH ONLY.** ⛔ `--git-dir=~/trading-system.git` **FAILS**:
🔬 measured 30-Aug — `fatal: not a git repository: '~/trading-system.git'`.
⭐ Tilde does not expand after `=`. ⭐ Use `/home/ubuntu/trading-system.git`, both places.

⛔ **ANY mismatch ⇒ STOP.** ⭐ Report measured vs expected. ⛔ No "close enough".

## STEP 2 — ONE artifact: every STEP 0/1 measurement raw + `$CAND`/`$F2C` paths +
Rama's verbatim PUSH-AUTH line + the literal VM porcelain. ⭐ Record its own sha256.

## STEP 3 — 🔴 THE PUSH · ⭐ THE ONLY PERMITTED COMMAND

    git -C $CAND push origin fix/mis-autosquareoff-28aug:refs/heads/main

⚠️ ⛔ `HEAD:main`, ⛔ `git push origin main`, ⛔ bare `git push`, ⛔ any wildcard →
each ships **17 commits including un-authorised F2-CORE**.
⛔ No `--force`. ⛔ No `--force-with-lease`. ⛔ No second push. ⛔ No push of
`feat/f2-core-30aug` anywhere. ⭐ Capture complete raw output **including the hook's**.

## STEP 4 — CLASSIFY THE HOOK BRANCH, quoting the string

- INSTALL ⇒ `post-receive: crontab AUTO-INSTALLED from canonical.`
- SKIP    ⇒ `post-receive: WARNING canonical != generate(registry) on the deployed tree — crontab NOT installed.`

⚠️ A successful push and a failed cron install are **two separate outcomes**.
⭐ On SKIP: V-9's expectations **INVERT** (02:10 absent, 16:05 still present) — that is
the consequence to report, ⛔ not a failure to chase. ⛔ No re-push, ⛔ no hand-install,
⛔ no generator on the VM, ⛔ no hook edit.
⚠️ Residual risk behind this branch: VM Python **3.12.3** vs PC **3.11.9** (W-1).

## STEP 5 — VERIFY (all four = `39292d3`)

- **V-1** `git -C $CAND ls-remote origin main`
- **V-2** `ssh trading-vm 'git --git-dir=/home/ubuntu/trading-system.git rev-parse refs/heads/main'`
- **V-3** 🔴 deployed work-tree — **bare/work-tree form ONLY**:
  `ssh trading-vm 'git --git-dir=/home/ubuntu/trading-system.git --work-tree=/home/ubuntu/systems/trading-system rev-parse HEAD'`
  ⛔ **WITHDRAWN:** `cd /home/ubuntu/systems/trading-system && git rev-parse HEAD` —
  🔬 that dir has **no `.git`**; it returns *"not a git repository"* and reads as a
  FAILED DEPLOY. ⚠️ V-3 proves **which commit** the tree matches; it does ⛔ NOT prove
  the tree is clean.
- **V-4** `git -C $CAND rev-parse fix/mis-autosquareoff-28aug`
- **V-5** 🔴 NEGATIVE CHECK — proves F2-CORE did not ride:
  `git -C $CAND fetch origin` then
  `git -C $CAND merge-base --is-ancestor feat/f2-core-30aug origin/main ; echo $?` ⇒ **1**
  · `git -C $CAND rev-parse origin/main` ≠ `587b306`
  · `git -C $CAND rev-list --count effff24..origin/main` ⇒ **9**
- **V-6** `git -C $F2C rev-parse HEAD` = `587b306`, `status --porcelain` EMPTY, unpushed.
  ⛔ No delete, ⛔ no squash, ⛔ no rebase.
- **V-7** rollback TREE stays `52ccb4f` — read to verify, ⛔ write nothing.
- **V-8** ⛔ **DO NOT START THE SERVICE.** Read-only: service **inactive**, 08:15 boot
  mechanism **enabled**. ⛔ `is-enabled` / `list-timers` / `crontab -l` only.
  ⛔ No `start`, ⛔ no `restart`, ⛔ no `sudo`.
- **V-9** 🔴 `crontab -l` for user **ubuntu**, quote each line:
  · `output_retention` 02:10 **PRESENT**, quoted in full, **with `--apply` visible**
  · `daily_report` 16:05 **ABSENT**
  · `daily_trade_review` 16:07 **PRESENT, unchanged**
  ⚠️ **148-LINE TRAP:** +02:10 and −16:05 ⇒ 148 → 148. ⛔ Count proves nothing; ⛔ nor
  the canonical's md5; ⛔ nor the hook's own claim. ⭐ Report **PREDICTION** and
  **PROOF** as two separate lines.
- **V-10** re-report the dirty VM tree — the 34 untracked survive `checkout -f`.
  ⚠️ A green V-3 does ⛔ not retroactively make it clean. Both stand together.
- **V-11** push record — 9 SHAs + subjects; the three live-behaviour items:
  · `0823b75` email recipient → **ALREADY-LIVE** (byte-identical `1cbf91a8…`, no-op)
  · `12c4ab1` retention → **NEWLY-ARMED** (02:10 `--apply`, first run Mon, delete-set **0**)
  · `1a1cb25→dee5fcf→bee9755` daily_report → **NEWLY-RETIRED** (`enabled:false` AND
    `monitored:false` ⇒ no 16:05 run and ⛔ no false CRITICAL)

## STEP 6 — RECORD (⛔ was missing from the first persisted copy)

- ⭐ Append tonight's outcome to the file-based memory: artifact sha256, hook branch,
  V-1…V-11, the 9 SHAs.
- ⭐ `docs/MASTER_REGISTER.md` — commit **LOCALLY**. ⛔ **NEVER push it** — ⚠️ pushing
  moves `origin/main` and **strands the held unit**.
- ⭐ `docs/SYSTEM_MAP.md` · `PATHS.md` corrections ⛔ stay deferred to the next commit
  window; recorded as **owed**.
- 🔴 `UNPUSHED_PENDING_DEPLOY_LEDGER` / `MEMORY_BOARD.md` — held-unit facts readable
  **without** checking out `$F2C`: 7 F2-CORE commits + 1 ledger commit at `587b306`;
  blocked on criterion 7 / D-A; **regression-gate clean** against the 30-Aug baseline
  (`46c38a3e…`) ⛔ — architectural acceptance **INCOMPLETE**; ⛔ gate results do **not**
  survive a SHA change ⇒ ⭐ **re-gate on resume**.
- 🔴 **mempalace — retry once at session end.** ⛔ If still `CONNECTION_CLOSED`, carry
  the outage **and the full owed replication set** to the **top** of the next session.
  ⛔ Never invent a replacement mechanism.

## STEP 7 — short confirmation to Rama, then **STOP**.
⛔ No cleanup. ⛔ No "while I'm here".

---

## STOP CONDITIONS (above the clock)

`rev-parse` ≠ `39292d3` (authorisation spent) · count ≠ 9 (candidate contaminated) ·
`$CAND` dirty · `origin/main` or VM bare ≠ `effff24` before the push · dry-run not a
clean FF · push errors · V-3 ≠ `39292d3` · **V-5 shows F2-CORE is an ancestor of
`origin/main`** ⇒ 🔴 STOP IMMEDIATELY, attempt **no** correction — ⚠️ a corrective push
on a live main is a second incident · either ref resolving in >1 worktree/SHA · any
forbidden edit becomes necessary (`position_sizer.py`, `kill_switch.py`, the EOD module,
`market_windows.py`, `schema.sql`, the hook, the crontab, `cron_registry.yaml`, the Cron
Officer, the config, `output_retention.py`) · 23:00 with no push.

⭐ **NOT stops — report and continue:** the dirty VM tree · the 34 untracked entries ·
the hook SKIP branch · the email delivery evidence gap · any Monday prediction.
⛔ None blocks the push; ⛔ none licenses an edit.

## WORDING RULES W-1…W-5

- **W-1** The generator is **structurally host-independent from the inspected source**;
  ⛔ PC-vs-VM byte equality was **not measured** (3.11.9 vs 3.12.3) and is not claimed.
- **W-2** The **measured first-run delete-set is zero**, with explicit scope and
  containment protections. ⛔ Never *"cannot delete anything"* / *"retention is harmless"*.
- **W-3** The VM deployment tree is **dirty**; ⛔ a green V-3 does not make it clean.
- **W-4** The Wednesday first-deletion prediction covers **only** the five regular
  one-per-trading-day families; `alert_watcher_` is **irregular**. `MAX_DELETE=25` is a
  **cap**, ⛔ not evidence.
- **W-5** Status is **SUCCESS and exit 0 despite 12 intentional REFUSED entries.**
  ⛔ Never *"the job is healthy"*. ⛔ **exit 0 ≠ healthy.**

⛔ **Never write "all checks passed."** ⭐ Write what passed, what was found, and what
was intentionally left untouched.

⛔ push ≠ cron installation ≠ boot ≠ first execution · ⛔ bare ref ≠ deployed tree ·
⛔ deployed SHA ≠ clean tree · ⛔ armed cron ≠ a job that ran · ⛔ retired ≠ un-monitored ·
⛔ monitored ≠ due · ⛔ grouped count ≠ inventory · ⛔ line count ≠ set equality ·
⛔ prediction ≠ proof · ⛔ exit 0 ≠ healthy · ⛔ a card ≠ a measurement · ⛔ a timer ≠ an
authority · ⛔ **a clean tree ≠ the clean tree.**
