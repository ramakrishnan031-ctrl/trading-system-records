# 🚀 DEPLOY — `origin/main` `742d9da` → **`2f67bb849633eb7844dc46570d2b31f8a8604e97`** · 23-Aug-2026 21:44 IST

🏷️ **DEPLOYED. ⛔ NEVER `VERIFIED LIVE`** — the code has not executed; Monday 24-Aug 08:15 is its
first run. Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
**Authorisation:** 👤 Rama, **conversational provenance**, one-time, scope = the three units below.
⛔ It does **not** activate the standing auto-deploy policy (DRAFT / NOT ACTIVE).

**Provenance:** 🔬 measured · 📄 from evidence · 💭 inference · 👤 Rama's.

---

## §1 — 🔴 THE CARD'S ARITHMETIC HID A PARTIAL DEPLOY. CAUGHT BEFORE THE PUSH.

📄 The card listed U-1 + U-2 + U-3 *"stacked as `076fe57` +9"*.
🔬 **8 (batch) + 1 (NI-5) = 9 already** ⇒ **`63e0d3d` was NOT in that stack**, confirmed by
`git merge-base --is-ancestor 63e0d3d 076fe57` → **absent**.
⇒ 🔴 **Pushing `076fe57` would have breached `D1` — NO PARTIAL DEPLOY.**

⭐ U-3 cherry-picked cleanly onto `076fe57` → **`2f67bb84`, 10 commits**. 🔬 Tree delta vs
`076fe57` = **exactly `deploy/systemd/trading-system.service`, 1 line**
(`RestartPreventExitStatus=3 4` → `3 4 5`).

⚠️ ⭐ **And the gate was re-run on the SHA actually pushed, ⛔ not carried forward** — 🔬 three test
files reference `trading-system.service` (`test_liveness_probe`, `test_preflight_engine`,
`test_preflight_groups`). Inspected: they assert the **unit NAME string**, ⛔ not the repo file's
content. ⭐ But *"a non-Python file cannot matter"* was **not assumed**.

---

## §2 — ✅ STEP 3 · FULL DIFFERENTIAL GATE

**Harness:** `PYTHON=/c/python311/python` set (⛔ **not** a PATH shim), Git Bash,
`/c/python311/python -m pytest tests/unit tests/integration -q -p no:randomly`, two detached
worktrees with the gitignored `config/instruments.csv` copied in.

### RAW TAILS

```
BASE  742d9da : 7 failed, 5751 passed, 4 skipped, 281 warnings in 934.86s (0:15:34)
HEAD  076fe57 : 7 failed, 5797 passed, 4 skipped, 281 warnings in 932.31s (0:15:32)
HEAD  2f67bb84: 7 failed, 5797 passed, 4 skipped, 281 warnings in 898.29s (0:14:58)
```

⭐ **THE HARNESS CONTROL FIRED FIRST: base = `7F / 5,751P / 4S`, the recorded baseline reproduced
EXACTLY.** ⇒ the comparison is trustworthy before it is made. 🔬 Base collected **5,762** =
7 + 5,751 + 4.

### ID-LEVEL SET COMPARISON — 🔬 **IDENTICAL**

| pair | identical? |
|---|---|
| base vs `076fe57` | ✅ **YES** |
| base vs `2f67bb84` | ✅ **YES** |
| `076fe57` vs `2f67bb84` | ✅ **YES** |
| **base-green tests that went red** | ✅ **ZERO** |

The standing 7, unchanged on every side:
`test_closure_source_contract::test_no_module_restates_the_vocabulary_literals` ·
`test_fix181::…::test_inflight_orphan_flattened_when_kill_active` ·
`test_main::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret` ·
`test_main::TestContinueFromGate::{test_price_hit_calls_placer_with_correct_prices,
test_no_placer_releases_reservation_and_updates_status, test_stats_placed_incremented_on_success}` ·
`test_phase17_batch2::test_fix077_flask_max_content_length`

### 🔬 DELTA DECOMPOSED EXACTLY — **+46 = 47 added − 1 removed**

| unit | added ids |
|---|---|
| **batch = +22** | `test_ni18_constraint_reports_multiplier` **6** · `test_ni9_delivery_count_caps_required` **4** · `test_ni19_segment_split_is_partial_by_design` **4** · `test_ni17_qty_cap_guards_the_output` **4** · `test_ni11_c2_has_a_delivery_arm` **4** |
| **NI-5 = +24** | `test_ni5_position_sizer_policy_required` **22** · `test_config_auditor` **+3 −1** |

⭐ The batch's +22 matches its recorded decomposition (NI-9 4 · NI-11 4 · NI-17 4 · NI-18 6 ·
NI-19 4) **exactly**.

### ⚠️ THE ONE REMOVED TEST — RUN DOWN, ⛔ NOT GLOSSED

`tests/unit/test_config_auditor.py::TestGroupFStaleDefault::test_diverging_position_cap_default_warns`
disappears on head.

- 🔬 **NI-5's own intentional replacement** — 1 test → 3
  (`test_required_param_is_reported_explicitly_not_skipped`,
  `test_summary_names_only_what_it_actually_compared`,
  `test_unintrospectable_row_is_reported_not_swallowed`).
- 🔬 ⛔ **NOT a merge casualty:** head's `test_config_auditor.py` is **byte-identical to NI-5's own
  version** — the batch never touched that file's tests.
- ⭐ The old name survives **only inside the replacement's docstring**, which states why it cannot
  exist: *"with no default there is nothing to diverge FROM."* 🔬 `def` count for it on head: **0**.

### ⚠️ AND THE SEMANTIC POINT IS NOT SOFTENED

A clean auto-merge is **more** dangerous than a conflict — ⛔ nothing forced a human to look. The
pre-gate reasoning (NI-5's three required params vs NI-17's `max_single_order_qty`, which keeps its
default) was 💭 **inference**. ⭐ **The gate is what settled it, and it did.**

---

## §3 — ✅ STEP 4 · GATE-TIME CHECKS, ALL FRESH (⛔ nothing carried from the 20:2x run)

| # | check | 🔬 result |
|---|---|---|
| **G-1** | `origin/main`, two independent measures | ✅ `742d9da` from `ls-remote` **and** the VM bare ref |
| **G-2** | FF dry-run, explicit 40-char SHA | ✅ `742d9da..2f67bb8` — two-dot, ⛔ no `+` |
| **G-3** | forbidden ancestry | ✅ `65b7196` · `3dff752` · `c39e799` **absent**; **CONTROL `742d9da` PRESENT**; all three units confirmed in the stack |
| **G-4** | **F6 CONTENT** | ⚠️ `cnc_gtt_monitor.py` **does** differ (3+/1−) — 🔬 **AST-IDENTICAL with docstrings stripped** ⇒ a **NI-12 docstring-only** change, **zero F6 substance**. **CONTROL vs `c39e799`: DIFFERS → fires** |
| **G-5** | VM tracked drift | ✅ **0**, deployed HEAD `742d9da` (needs `GIT_DIR`/`GIT_WORK_TREE`; the tree has no `.git`) |
| **G-6** | fresh before-image | ✅ `trading-system` inactive/PID 0 · `alert-watcher` **3938122** · `gui-dashboard` **3674880** · `token-watcher` **2226721** · all `NRestarts=0` · `RestartPreventExitStatus=3 4 5` · crontab md5 `b8276da7…`, 46 jobs |

**Push executed:** `git push origin 2f67bb849633eb7844dc46570d2b31f8a8604e97:refs/heads/main`
⛔ Not `git push origin main` · ⛔ no `--force` · ⛔ no amend.

---

## §4 — ✅ POST-PUSH (file/config level only)

| check | 🔬 result |
|---|---|
| `origin/main` moved, two ways | ✅ `2f67bb84…` from `ls-remote` **and** the VM bare ref |
| deployed HEAD | ✅ `2f67bb84…` |
| VM tracked drift | ✅ **0** |
| PC == VM per changed file | ✅ **27/27 NON-VACUOUS** (every one differed at `742d9da`); blob spot-check MATCH on `position_sizer.py` `f92eace8d6`, `config_auditor.py` `054d58298b`, `trading-system.service` `3d97c92caf` |
| crontab | ✅ md5 **`b8276da7043975cda2d0ce6578960c6a`**, **46** job lines |
| ⭐ four services vs before-image | ✅ **IDENTICAL — the hook restarted nothing.** MainPIDs `0` / `3938122` / `3674880` / `2226721`; **`NRestarts=0` on all four** |
| `RestartPreventExitStatus` | ✅ **`3 4 5` still in force** |

### ⚠️ 8th OCCURRENCE — ⛔ RECORD, NEVER REPAIR

The hook printed **`post-receive: crontab AUTO-INSTALLED from canonical.`** again.
🔬 Content **unchanged**: md5 and 46 job lines identical either side.

### ⭐ THE PREDICTED md5 GAP HELD, EXACTLY

🔬 installed `/etc/systemd/system/trading-system.service` = **`a8ea94ba…`** ·
repo `deploy/systemd/trading-system.service` = **`ab0ee5b0…`** — ⭐ **still different after the
governance commit**, precisely as the ledger predicted (the two 18-Jun comment lines).
⛔ **Do NOT "fix" this by copying.** ⭐ `3 4 5` survives **because deploy cannot touch
`/etc/systemd/system/`** — it is a manual VM state Rama applied this afternoon.

---

## §5 — ⚠️ WHAT MONDAY LOOKS LIKE

⚠️ **24-Aug 08:15 is the first execution, and it now exercises 18 commits in ONE run** — the 8
pushed at 13:22 plus tonight's 10. ⇒ 🔴 **Nothing is separately attributable.** 👤 Chosen knowingly.

⭐ Runbook unchanged (`ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md`):
🔴 a RED `zerodha_morning.ps1` at 15 s is **~50% likely on a HEALTHY config** (30 s watcher poll) ⇒
**wait 30 s and re-run FIRST**; only then `grep "Config load failed" logs/system_<date>.log`
(⛔ not `journalctl` — it carries no INFO). ⛔ **REVERT (RB-3), ⛔ never tune.**
⛔ **And RB-2 or a ledger entry the SAME DAY** — an unreconciled rollback undoes itself at the next
push, because `post-receive` checks out **`main`**, ⛔ not the pushed SHA.

---

## 🏷️ STATUS

🏷️ **DEPLOYED `2f67bb849633eb7844dc46570d2b31f8a8604e97` · ⛔ NOT `VERIFIED LIVE`.**
✅ **Nothing remains unpushed from the three authorised units.**
⛔ `feat/delivery-config-split` stays local (docs branch, ⛔ not for push).
👤 Still open: **D-1b** · **D-3** · F2's build-fresh-vs-recover · 🔴 MIS ×3.5 (HELD) ·
F13 · POST-COMPROMISE DETECTION legs L1–L4 · F14's sweep.
