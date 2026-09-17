---
name: deploy-record-exists-28jul
description: "The VM deploy record EXISTS — ~/trading-system.git/logs/HEAD, 801 entries back to 3-May-2026, push + checkout timestamped. Corrects my own same-day 'no reflog at all'. ✅ The 90-day expiry is CLOSED (gc.reflogExpire=never, 28-Jul ~15:3x) and PROVEN to survive the 18:46 deploy — not owed again."
metadata: 
  node_type: memory
  type: project
  originSessionId: c4bb72b3-0d74-4f27-bc40-b99f67899e79
  modified: 2026-07-28T13:24:37.999Z
---

# 🧾🔑 THE DEPLOY RECORD EXISTS — and I reported the opposite the same day

**`~/trading-system.git/logs/HEAD` on the VM.** 801 entries, unbroken back to
**3-May-2026 15:13 IST**, 125,774 B. It records **BOTH halves of every deploy**,
timestamped to the second:

```
52ead46 HEAD@{2026-07-28 09:15:25 +0530}: checkout: moving from main to main
52ead46 HEAD@{2026-07-28 09:15:25 +0530}: push
```

`push` = receive-pack taking the commit. `checkout` = post-receive's `git checkout -f`
**writing the deployed tree** — that second line *is* the deploy event, not a proxy for it.

▶️ `ssh trading-vm "git -C ~/trading-system.git reflog show HEAD --date=iso | head -20"`

## ⛔ THE ERROR IT CORRECTS (mine, 28-Jul, hours earlier)

I reported *"the bare repo has NO REFLOG AT ALL, no `logs/` dir, NOTHING records deployment."*
**All three clauses false.** The check ran `git reflog show main` — which **is** genuinely empty
(0 lines) because the repo is bare and no *per-ref* log was ever created — saw `core.logAllRefUpdates`
unset, and **generalised from one ref to all refs**. The record is on **HEAD**.

⭐ **MECHANISM, so nobody "fixes" it away:** git **appends to a reflog file that already exists**
regardless of `core.logAllRefUpdates`; that setting only governs whether one is **CREATED**.
`logs/HEAD` was created 3-May by the initial `checkout: moving from master to main` and has
recorded silently ever since. `core.bare=true` confirmed.

## ✅ CLOSED — the 90-day clock was stopped, and the fix is now PROVEN AGAINST A REAL PUSH

⭐⭐ **NOT OWED AGAIN. Confirmed surviving a live deploy on 28-Jul at 18:46:19** (`52ead46..ce08668`):
after that push the reflog showed the NEW pair **and** the prior `52ead46 HEAD@{2026-07-28 09:15:25
+0530}` pair still present ⇒ nothing was pruned. ⭐ **The push also demonstrated the record's actual
value:** it was the only artifact that could show **BOTH** halves — `push` *and*
`checkout: moving from main to main` at the same second — and the `checkout` line is the one that
proves the deployed tree was actually WRITTEN, not merely received. [[feedback-verify-rc-not-output]]

*Historical framing, kept because it explains why the deadline existed:*
`gc.reflogExpire` was **UNSET** ⇒ git's default **90 days**. The 3-May entries were ~86 days old on
28-Jul. **Any `gc --auto` on a push could have pruned them.**

```
ssh trading-vm "git -C ~/trading-system.git config gc.reflogExpire never"
ssh trading-vm "git -C ~/trading-system.git config gc.reflogExpireUnreachable never"
```
⭐ **Do it BEFORE the next push (Thu 30-Jul)** or ~3 months of deployment history is lost to a
default nobody chose. ✅ **DONE 28-Jul ~15:3x — applied BEFORE any push** (both keys read back `never`, 801 entries intact). The Thursday deferral was correct while Tuesday was no-deploy; Rama's 15:45 PC==VM override moved the deadline to tonight. Optional belt-and-braces
afterwards: `core.logAllRefUpdates true` creates the per-ref log going forward.

## Why it matters beyond attribution

- ⭐ **It independently corroborates the T2 finding:** `e6ec75b` shows push+checkout at
  **27-Jul 22:33:58**, 39s after its 22:33:19 commit stamp — a **second, VM-side witness** that
  never entered the PC-side reasoning behind [[handoff-28jul-resume]].
- ⭐ It makes the unbuilt **deployed-tree-vs-HEAD** check cheaper: the *"which known commit"* half
  already exists, so only the comparison remains. That item stays **registered, NOT built**
  (gate: after Tue 4-Aug's flag flip) — `docs/decisions/ACTIONS_not_decisions.md`.

## The lesson, which repeated twice in one session

**An ABSENCE asserted from a check too narrow to see the thing.** The same shape produced the
`.gitignore` error the same day (read line 45, missed `*.py[cod]` on line 46, reported "no bare
`*.pyc` rule"). Both were caught only by **re-deriving from measurement instead of re-reading the
earlier note**. ⇒ When reporting that something does not exist, state *what you looked at*, and
check whether a neighbouring name/ref/line would hold it.

[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]] [[handoff-28jul-resume]]
