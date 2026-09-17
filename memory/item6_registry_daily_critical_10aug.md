---
name: item6-registry-daily-critical-10aug
description: "ITEM 6 investigated 10-Aug — the EOD report's daily CRITICAL is a PERSISTENT uncommitted diff, NOT a daily rewrite; the untrack fix is MEASURED to delete the live registry."
metadata: 
  node_type: memory
  type: project
  originSessionId: a9e5145e-3355-41d5-843b-a151f730acea
  modified: 2026-08-10T13:28:01.951Z
---

**ITEM 6 — `strategy_direction_registry.yaml` makes the EOD report CRITICAL. INVESTIGATED 10-Aug-2026, `<NOT BUILT — STOPPED AT THE MECHANISM CHOICE>`.**

## §3.1 — ZERO CALLERS: CONFIRMED, and the file is a CLOSED LOOP
- `registered_direction` is defined at `core/strategy_direction.py:91` and has **ZERO callers**. **WIDTH: `grep -rn` over the ENTIRE working tree, all file types, no include filter** ⇒ hits are the definition, its two `__pycache__` binaries, and two doc lines.
- ⭐ **The broader question has a sharper answer: the FILE's content is read by exactly ONE consumer — `load_registry()` at `strategy_registry_officer.py:224`, the officer that also WRITES it.** Nothing else reads it.
- ⛔ **`eod_squareoff.py:695` is NOT a counter-example** — it imports `build_direction_map`, which reads `config/strategies/*.yaml`, ⛔ never the registry.

## §3.2 — WHAT MAKES IT CRITICAL: the report's OWN severity rule, TRACED in three links
1. `scripts/system_manager.py:1195` runs `git diff --stat HEAD` on the deployed tree; `:1217-1223` calls `res.violation(...)` on any non-empty diff.
2. `generate_full_report:884` sums violations across ALL checks.
3. `main:1336` — `severity = "CRITICAL" if (violations or reasons) else "INFO"`.
- ⭐ **The report has NO WARNING severity — it is BINARY. Warnings alone still render INFO.** ⇒ one violation from any check turns the whole report CRITICAL.
- ⛔ The check NEVER sets `soft_kill_reason` (`:1134-1137`) — it is loud, it does not halt.

## 🔴 §3.2b — THE RECORDED PREMISE IS PARTLY REFUTED, and it changes the fix
- ⛔ **The file is NOT "REWRITTEN DAILY at 16:22".** **(P) `strategy_registry_officer.py:253-254` — `save_registry` is called ONLY `if changed`.** Once every traded strategy is `CONFIRMED` and health is stable, the officer **stops writing**.
- ⭐ **The real mechanism is a PERSISTENT UNCOMMITTED DIVERGENCE:** HEAD holds the 17-Jul seed (**MEASURED: 16 rows, all `PENDING`** — ⛔ not the recorded 18), the deployed file holds converged runtime state (`CONFIRMED`). The diff persists EVERY day between deploys; a deploy's `checkout -f` resets it to all-PENDING and the officer re-confirms, so it returns.
- ⇒ 🔑 **"Make the report treat a DAILY-REGENERATED file as expected" is built on a premise that does not hold.** The root cause is **runtime STATE stored in a git-TRACKED config file**.

## 🔬 §3.3 — THE DEPLOYMENT CONSEQUENCE IS MEASURED, ⛔ NOT INFERRED
- **EXPERIMENT (throwaway repo in scratchpad, exact hook command `deploy/hooks/post-receive:31` `git --work-tree=… --git-dir=… checkout -f`): the first deploy after `git rm --cached` + `.gitignore` DELETES the live file.** ⛔ Untracked-file protection does NOT apply — at checkout time it is still tracked at the OLD head.
- **Cost of untracking, per `reconcile:120-164`:** `load_registry` → `{}` (fail-safe `:70-71`) ⇒ all 16 re-registered NEW ⇒ **one Telegram+email burst**; **`first_seen` PERMANENTLY reset** (⛔ not recoverable from the DB — a `G11` ② effect `git revert` cannot undo). ✅ `registration_status` and `health` DO self-heal from the DB in the same run (`:148-162`).
- ⭐ **PRECEDENT EXISTS AND NAMES THIS EXACT HOOK — `.gitignore:35-39`, `config/instruments.csv`:** *"must NOT be git-tracked or the deploy hook's `git checkout -f` silently reverts the VM's fresh copy — instruments staleness incident 21-Jun-2026."* Same file class, same hook, already ruled.

## 🔴 THE DECISION OWED — three mechanisms, ⛔ NONE TAKEN
- **(A) UNTRACK** — smallest (one `.gitignore` line + `git rm --cached`), follows the `instruments.csv` precedent; ⛔ costs the `first_seen` provenance for 16 strategies + one alert burst, **irreversibly**.
- **(B) SEED + STATE SPLIT** — `config/…yaml` stays TRACKED as the read-only seed; state moves to `data_store/` (**already gitignored, `.gitignore:17` ⇒ no new ignore line, no new config key**). ✅ **Zero loss, zero alert burst, no manual VM step** (the seed's 16 rows load, confirmations are SILENT per `reconcile:107`). ⛔ Larger: touches `core/strategy_direction.py` + the officer's default path.
- **(C) CLASSIFY IN THE REPORT** — ⛔ leaves the root cause in place, and its premise is refuted by §3.2b.
- 📌 `docs/expected_alarms.md:436` records *"DO NOT SUPPRESS THE CHECK; the CLASSIFICATION is what is missing"* — ⚠️ **that is a PRIOR RECOMMENDATION, ⛔ not a Rama ruling.**

Related: [[feedback-verify-the-finding-premise]] [[reversibility-two-claims-08aug]] [[feedback-absence-needs-wide-check]]
