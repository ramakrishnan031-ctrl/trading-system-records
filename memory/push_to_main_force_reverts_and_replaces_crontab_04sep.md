---
name: push_to_main_force_reverts_and_replaces_crontab_04sep
description: The VM post-receive hook auto-deploys on every push to main - it runs checkout -f (discarding working-tree config edits) and replaces the ENTIRE crontab from canonical; both fired on 04-Sep and silently undid a live config change and a scheduled job
metadata: 
  node_type: memory
  type: project
  originSessionId: 161ed55b-a158-4c12-a83a-53edac5888db
  modified: 2026-09-04T05:34:05.569Z
---

🔴 **A PUSH TO `main` IS ⛔ NOT A READ-ONLY ACT ON THIS MACHINE.** ⭐ It **deploys**,
⭐ it **force-reverts the working tree**, ⭐ and it **replaces the entire crontab**.

## 🔬 The mechanism (`~/trading-system.git/hooks/post-receive`)

    git --work-tree=$TARGET --git-dir=$GIT_DIR checkout -f "$BRANCH"
    ...
    crontab deploy/cron/trading-system.cron   # "AUTO-INSTALLED from canonical"

⭐ **`checkout -f`** ⇒ ⛔ **every** working-tree modification is discarded, ⭐ silently.
⭐ **`crontab <file>`** ⇒ ⭐ the crontab is **REPLACED**, ⛔ not merged ⇒ ⭐ any job not
in `deploy/cron/trading-system.cron` is **gone**.

⚠️ ⭐ 📄 The hook's own header records that it **lied about itself** for a period
(*"NOT the currently-installed hook"* was FALSE) -- ⭐ so ⛔ do not trust a hook's
comments; ⭐ read the armed file.

## 🔬 It fired on 04-Sep-2026 and undid two live things

⭐ Pushing F1b (`18dd6cc` → `20061b6`) immediately:
  · ⭐ reverted the 3 TEMP-disabled delivery YAMLs back to **`enabled: true`**
    ⇒ ⭐ 👤 Rama's Friday carry decision, ⛔ silently undone in the file;
  · ⭐ **deleted the Monday revert cron** (🔬 `crontab -l | grep -c` → **0**).

⭐ Both were caught in the same turn and restored. 🔴 ⭐ **Why it did not become an
incident:** ⭐ the hook does ⛔ **not** restart the service ⇒ 🔬 the running process
(PID 1190450, 09:31:38) was untouched ⇒ ⭐ delivery stayed off **in-process**
(`will_trade_count: 12`) ⇒ ⛔ no CNC entry was ever possible. ⚠️ ⭐ The exposure was
*"if a restart had happened in that window"*, ⛔ not live.

## 🔴 STANDING RULE — the post-push checklist

⭐ After **ANY** push to main, re-verify all three:
  ⭐ **(i)** the 3 delivery YAMLs (or whatever working-tree config is meant to hold)
  ⭐ **(ii)** `crontab -l` -- ⭐ every non-canonical job
  ⭐ **(iii)** the RUNNING process's `will_trade_count` ⇒ ⭐ 📄 file ≠ process
⇒ ⭐ 📄 Pairs with [[config_edit_without_restart_is_a_split_state_04sep]]: ⭐ a push
  creates the split state in the **opposite** direction -- ⭐ file reverted,
  ⭐ process still carrying the edit.

⭐ **Complementarity (⭐ why Monday is still covered):** ⭐ the only thing that wipes
the revert cron is a **push**, ⭐ and that same push runs `checkout -f main`, ⭐ which
itself restores `enabled: true`. ⇒ ⭐ push ⇒ config fixed (⭐ cron unnecessary) ·
⭐ no push ⇒ cron intact (⭐ and it fires). ⚠️ ⭐ Narrow real gap: ⭐ someone re-applies
the disable after a push ⭐ and forgets the cron. ⇒ ⭐ **the checklist closes it.**

## ⛔ Carriers that do NOT work here

🔬 `at` is ⛔ **not installed** (`atd` inactive) · 🔬 `loginctl show-user ubuntu
Linger=no` ⇒ ⭐ a **systemd USER timer will not run while logged out**, ⭐ and
`enable-linger` needs root. ⇒ ⭐ **cron is the only durable carrier available**
without sudo -- ⭐ and it is the one the hook replaces. ⭐ Plan around that.

⏸ ⭐ **OWED:** ⭐ record this in `PATHS.md` beside the branch and PYTHONPATH notes.
⚠️ ⭐ Deliberately **deferred** on 04-Sep: ⭐ committing that note requires a push,
⭐ and a push would re-fire the very hazard while 👤 Rama's TEMP disable is standing.
⇒ ⭐ **Do it after Monday's revert**, ⛔ not before.

⭐ See also [[stale_local_main_is_a_push_trap_02sep]] ·
[[a_count_without_its_environment_is_not_a_baseline]]
