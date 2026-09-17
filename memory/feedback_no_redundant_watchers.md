---
name: feedback-no-redundant-watchers
description: Never spawn an until-loop/sleep watcher to wait for background work the harness already tracks — it re-invokes on completion. And kill any watcher the moment its result lands.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 288ac9c2-1f83-4084-a791-6a6c0cccdba8
  modified: 2026-07-26T06:10:22.379Z
---

**Do not spawn a second process to wait for work that already reports its own completion.
And when a result lands, stop whatever was waiting for it — do not leave it to expire.**

**Why (26-Jul-2026, Rama's correction):** during the alert-stream/kill-severity batch I started the
full-suite BASE and MERGE runs with `run_in_background: true` — which re-invokes me when the command
exits — and then *also* launched `until grep -qE "passed|failed" …; do sleep 20; done` watchers for
the same two events. Both were pure waste:

- The MERGE gate's own notification arrived at **10:45:02**. Its watcher's output file was last
  touched **10:35:58** and was **0 bytes** — it never reported anything, and was still sleeping when
  the real notification fired.
- I never stopped it. Rama had to point it out. By the time I checked, `TaskStop` returned
  *"No task found"* — so I could not even confirm how it ended, only that nothing was running.

⭐ **The tool guidance already said this:** *"Do NOT schedule a short-interval wakeup to poll for
background work you started — when harness-tracked work finishes, you are re-invoked
automatically."* I read a 14-minute test run as "too long to just wait for" and polled anyway. The
run's length is irrelevant — the notification is not tied to duration.

**How to apply:**
1. Started it with `run_in_background`? ⇒ **it notifies. Do not watch it.** Just do other
   non-conflicting work, or end the turn.
2. Poll only for state the harness genuinely cannot see (a broker/CI/remote job someone else runs) —
   and then size the interval to how fast that state actually changes, not to impatience.
3. If a watcher does exist, **kill it the moment its result lands** — in the same turn that reports
   the result, not later.
4. ⚠️ Before saying "nothing is running", **verify**: `TaskStop`, plus a native process check
   (git-bash `ps` does not see Windows processes — use `Get-Process python`).
5. Cheap interim reads (`tail` the output file) are fine and are *not* watchers — they cost one call
   and terminate.

Sibling: [[no-push-wakeups]] — an armed wakeup dies silently with the session. Same family: **do not
build a second mechanism to observe something that already reports itself.**
