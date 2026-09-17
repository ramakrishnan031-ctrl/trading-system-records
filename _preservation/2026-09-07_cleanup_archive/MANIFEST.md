# Fresh-start cleanup archive — 07-Sep-2026

Created before the SEC-H cleanup. Everything here is insurance; nothing here is live.

## 1. Git bundles — 136 unpushed commits

Bundled with `git bundle create <out> <branch> --not --remotes`, i.e. exactly the commits
**not reachable from any remote ref**. Every bundle was verified with `git bundle verify`
and its head SHA compared against the worktree head before any removal.

| bundle | branch | head | unpushed commits | bytes | verify | head match |
|---|---|---|---|---|---|---|
| `bundles/main.bundle` | `main` | `3dff752` | **90** | 2,677,025 | pass | OK |
| `bundles/tiers.bundle` | `feat/tier-multipliers-61-62` | `7d1fd4e` | **44** | 1,025,826 | pass | OK |
| `bundles/controlplane.bundle` | `feat/control-plane-g3` | `5cdd7e9` | **1** | 32,917 | pass | OK |
| `bundles/n907.bundle` | `fix/n907-extract-18aug` | `d896968` | **1** | 5,625 | pass | OK |

`90 + 44 + 1 + 1 = 136`.

### ⚠️ Correction to the instruction's premise — measured, and it matters

The SEC-H brief states *"unpushed means unrecoverable"*. **That is not true for these five, and the
measurement is simple:** each worktree's `.git` is a **file pointer**, e.g.
`gitdir: D:/Projects/trading-system/.git/worktrees/trading-system-main` — the object store and the
**branch refs are shared with the parent repo**. Removing a worktree removes a *checkout*, not
history.

🔬 Verified after removal — every ref still resolves:
`feat/control-plane-g3 5cdd7e9` · `main 3dff752` · `fix/n907-extract-18aug d896968` ·
`feat/tier-multipliers-61-62 7d1fd4e` · `fix/f1b-restore-verify-04sep 20061b6`

⇒ The genuine one-way door is deleting the **refs** (or the parent repo), not these directories.
The bundles are kept anyway: they cost 3.7 MB and survive a later ref deletion.

🔬 All five worktrees were **clean (0 dirty entries)** before removal — bundles capture commits,
never working-tree changes, so this was checked rather than assumed.

## 2. `trading-system-evidence/` — PRESERVED, NOT DELETED

⛔ **The instruction lists this directory in scope for removal. I did not delete it.**

🔬 It is **not a git repository** — no bundle is possible and nothing in it is recoverable once
gone. It holds **21 files** across `2026-08-31/` and `2026-09-03/`, including:

- `2026-08-31/system_2026-08-31.log` and `window_15-00_to_15-25.log` — captured log windows
- `2026-09-03/inputs/` — four **transcripts** (FILE-116 / FILE-118 / FILE-120 / FILE117) plus
  `README_PROVENANCE.md` and `PRERUN_CHECKS_03-Sep-2026.md`
- `SHA256SUMS.txt` (both dates) and `RECORD.sha256` — **integrity manifests, i.e. an evidence chain**
- `INSTRUMENT_VALIDATION_03-Sep-2026.md`, `MONDAY_RECORD_31-Aug-2026.md`, `FUNNEL_REPORT_*`

**2026-09-03 is the ANANTRAJ naked-position incident date.** Transcripts and hash manifests cannot be
regenerated, and the captured logs will rotate off the VM (~7 trading days).

⇒ A full **copy** is here (`trading-system-evidence/`, 21/21 files). The original is left in place.
👤 **Rama's ruling required** before it is removed — this is exactly the "archive before delete"
case the guard rail exists for.

## 3. Not touched (H.5)

`D:/Projects/trading-system` (active workspace) · the deployed production repo · the sandbox repo ·
`tests/fixtures/broker_corpus/` + README · `docs/audit/MONDAY_VERIFICATION_07-Sep-2026.md`.

## 4. Side effect worth recording

Removing `trading-system-main` also **retires a standing hazard**: that directory held local `main`
at `3dff752`, **90 ahead / 94 behind** `origin/main`, where a plain `git push origin main` would have
pushed it *over* the deployed SHA. That trap no longer has a working tree to fire from — though the
`main` ref still exists in the shared repo, so the discipline (explicit refspec) still applies.

## 5. State after cleanup (H.6)

`git worktree list` = **1** entry (`D:/Projects/trading-system`, `6d24a83`); stale scratchpad
worktree records pruned (was 9). Three active machine roles remain: **PC · production trading VM ·
sandbox VM.**
