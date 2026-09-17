# DEPLOY RECORD — `742d9da` · 23-Aug-2026 13:22 IST

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
👤 **Authorised by Rama, naming the exact refspec.**

🏷️ **STATUS: `DEPLOYED`. ⛔ NEVER `VERIFIED LIVE`** — that requires an actual live session.
**`origin/main`: `4568385` → `742d9dab5234682d40d2c538fce1b777a42b30e1`.**

---

## OPS ② — THREE EVIDENCES, ⛔ NEVER COLLAPSED

| evidence | 🔬 measured | what it proves | ⛔ what it does NOT |
|---|---|---|---|
| **ENFORCEMENT** | `systemctl show` → `RestartPreventExitStatus=3 4 5`; unit line 33 matches; md5 `136a4e88…` → **`a8ea94ba…`**; `.bak-23aug2026` present (1411 B, mtime preserved); `Restart=on-failure` / `RestartUSec=10s` untouched | systemd **is using** the new policy | ⛔ nothing about whether anyone would be told |
| **DETECTION** | one integrity CRITICAL, **13:18:32** — *"Sensitive file changed: unit_trading … sha256 `7ad85a562ae2`→`faa2cac56bc2`"* | the watch **saw** the change | ⛔ nothing about whether the policy loaded |
| **GOVERNANCE** | 🔴 **OWED** — repo `deploy/systemd/trading-system.service:35` still `3 4` | — | — |

⭐ **DETECTION fired exactly ONCE**, which independently confirms the earlier finding that
`check_watched_files` re-baselines on the same pass that alerts. ⛔ **No `--baseline` was
run**, and none was needed.

⚠️ **GOVERNANCE remains open, deliberately.** Reconciling the repo copy is **its own
commit** — adding it here would have changed the refspec Rama named. ⛔ **And note: even
after that one-token edit the repo md5 (`ab0ee5b0…`) will NOT equal installed
(`a8ea94ba…`)** — the two 18-Jun comment lines. ⛔ Nobody should "fix" that by copying the
repo file over the installed one.

## THE GATES — every zero has a firing control

| | result |
|---|---|
| **V-1** | `4568385`, **two independent ways** — `ls-remote` **and** the VM bare ref. ⛔ The cached local ref was not used |
| **V-2** | `4568385..742d9da` — **two dots = fast-forward**, ⛔ no `+`, ⛔ no forced update |
| **V-5** | before-image **13:20:45 IST**, four units, MainPID + NRestarts |
| **V-6** | **ZERO**, ⭐ with controls that fire — see below |
| **V-7** | **0 drifted tracked files**; config md5 `b088bd3f…` identical both sides ⇒ nothing clobbered |

### ⭐ V-6 — THE EVIDENCE THAT CAN NEVER BE RE-TAKEN

**The pre-NI-1 defect NEVER fired in production.**

| | width | result |
|---|---|---|
| DB `signals` | **160,850** rows, **2026-06-12 → 2026-08-21** | `%unhandled%` = **0** · `PLACEMENT_FAILED`+`%unhandled%msg%` = **0** · `%overwrite%LogRecord%` = **0** |
| logs | **22** files, `system_2026-07-23` → `system_2026-08-21` | both signatures = **0** |

**CONTROLS FIRED:** `PLACEMENT_FAILED` = **144** · `rejection_reason LIKE '%_%'` =
**160,292** · `CRITICAL` present in **22/22** log files.
⚠️ The column is **`rejection_reason`**, ⛔ not `reason`.
🔴 **The obvious search — `sl_direction_warning` — would have returned ZERO BY
CONSTRUCTION** (pre-NI-1 that call *raised* instead of logging). ⭐ **From this deploy
onward the artifact flips form permanently**; a future search must use the warning string,
⛔ not this one.

## POST-PUSH — file/config level only

- `origin/main` = `742d9da`, **two ways** (ls-remote + VM bare ref) ✅
- hook output: *"Deploying main…"* / *"Already on 'main'"* / *"crontab AUTO-INSTALLED from
  canonical."* / *"Deployment complete."*
- deployed-tree drift vs `742d9da` = **0 files** (corrected recipe, `update-index --refresh`) ✅
- ⭐ **THE HOOK RESTARTED NOTHING** — all four PIDs **identical** to V-5
  (`alert-watcher 3938122` · `gui-dashboard 3674880` · `token-watcher 2226721`),
  `NRestarts=0` throughout, `trading-system` still `inactive/dead`. ⭐ Scoreable **only**
  because V-5 was captured first.
- ✅ **`RestartPreventExitStatus=3 4 5` STILL IN FORCE after the deploy** — confirming
  again that deploy does not touch `/etc/systemd/system/`.
- **P-6 per-file** VM == `742d9da` for `position_sizer.py`, `config_loader.py`,
  `system_config.yaml`, `main.py` — ⭐ and **NON-VACUOUS**: each differed from `4568385`
  before, so the check could have failed.

### ⚠️ THE SEVENTH OCCURRENCE — ⛔ RECORDED, ⛔ NOT REPAIRED

The hook printed **"crontab AUTO-INSTALLED from canonical"** while the canonical diff
`4568385..742d9da` is **ZERO lines**. Content is correct: live md5
**`b8276da7043975cda2d0ce6578960c6a`** == canonical, **46** job lines both sides.
⭐ The hook installs whenever regen matches canonical; it does not compare against the
*live* crontab. Cosmetic and idempotent. ⛔ **Do not "fix" it.**

## ⛔ NOT DONE, DELIBERATELY

⛔ Service not started · ⛔ no `--resume` · ⛔ no SOFT_KILL clearing · ⛔ no runtime
verification · ⛔ NI-5 `a4a5cef` not pushed · ⛔ the register not pushed.

## 🔴 NOW OWED

1. **GOVERNANCE** — the unit-file repo commit, on its own.
2. **NI-5 `a4a5cef`** — the third unit, now **1 commit** ahead, sitting directly on the
   deployed SHA.
3. 🔴 **F2's line numbers are now DEAD.** `F2_SEGMENT_CAPITAL_INVENTORY_22-Aug-2026.md`
   measured at `4568385`; F1 + NI-1/NI-2/NI-4 touched `position_sizer.py`,
   `config_loader.py`, `config_auditor.py`, `system_config.yaml`.
   ⛔ **RE-ANCHOR at `742d9da` before using a single line reference (M3).**

## ⚠️ MONDAY 24-AUG — FIRST EXECUTION

⭐ The boot is **ATTENDED** — Rama SCPs the token; the service cannot start without it.
🔴 **A RED `zerodha_morning.ps1` is NOT proof of failure** — 15 s wait vs 30 s poll.
**Wait 30 s and re-run first**, then confirm with
`grep -i "Config load failed" ~/systems/trading-system/logs/system_$(date +%F).log | tail -5`.
⚠️ A matching entry confirms a rejection; ⛔ **no matching entry does NOT prove it was the
timing** — investigate the remaining failure.
⛔ **REVERT — ⛔ never tune — if a VALID config is rejected.** Rollback and the mandatory
same-day reconciliation are in `ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md`.
