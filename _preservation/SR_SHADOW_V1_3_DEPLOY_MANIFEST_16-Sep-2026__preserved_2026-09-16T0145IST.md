# S&R SHADOW v1.3 — TESTING-VM DEPLOY MANIFEST (STANDALONE COPY, OUTSIDE GIT)

**Preserved:** 2026-09-16T0145 IST, per the 16-Sep "DEPLOYMENT CARD AMENDMENT 4" §1.
- **Save it with the cards.**
- **Tracked twin:** `D:/Projects/trading-system/docs/SYSTEM_MAP.md`, sections `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` (~01:12, amended ~01:25 and ~01:40) and the 16-Sep amendment entries.
- ⚠️ That twin is tracked but UNCOMMITTED: `git checkout -- .` or `reset --hard` destroys it. This file is the copy that survives.
- ⛔ **If the two ever differ, the later timestamp wins, and the difference is reported.**
- **Supersedes** `SR_SHADOW_V1_3_DEPLOY_MANIFEST_16-Sep-2026__preserved_2026-09-16T0128IST.md`. This version adds the Amendment 4 and 5 entries and the verified rollback states.
- ⚠️ **Time-label correction:** the 0128 version's section labels ran AHEAD of the system clock (e.g. "~01:30", "amended ~01:50"). Measured clock readings put the writes at: manifest ~01:12 · Amendment 3 ~01:15 · `tar -t` check ~01:20 · Amendment 4 ~01:25 · Amendment 5 ~01:40. The tracked SYSTEM_MAP copy is corrected, as is this file. The section IDs (`MANIFEST-…`, `RESULT-…-AMENDMENTn-…`) are the stable references.
- **Precedence inside this file,** where the verbatim notes below differ: the manifest's **Gate 4** (ordered copy) and **Gate 7/8 rollback** (block first, then the four files in reverse copy order, ⛔ no deletion of `sr_shadow/`), amended ~01:25 and ~01:40, supersede the ~01:05 ordered note, which in turn supersedes the order in the ~01:00 atomic note. The content of all three agrees; only the ordering was refined.

**Code:** commit `e7bf477` on `feat/sr-shadow-v1.3-15sep` (worktree `D:/Projects/wt-sr-shadow-15sep`, parent `970aabf`). ⛔ Unamended, ⛔ unpushed, ⛔ never `main`.

**Scope:** COMMIT 27 files · VM DEPLOYMENT 17 files · VM-LOCAL CONFIG = the `sr_shadow:` block, copied back as a validated file. TESTING VM `130.210.13.114` (`trading-sbx`) ONLY; ⛔ production untouched.

**Cards this manifest implements:** "S&R SHADOW v1.3 — DEPLOYMENT AND FIRST SESSION" and Amendments 1–4 (all 16-Sep).

---
## 16-Sep-2026 (Wed) ~01:12 IST — `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` — ⭐ THE TRACKED DEPLOY MANIFEST (Amendment 3 §3) · TESTING VM ONLY

**Why here:** the build report is UNTRACKED and the schedule exists only as in-session timers. This file is tracked. ⚠️ It is also uncommitted in the main tree, so it survives `git clean` but ⛔ not `git checkout -- .` or `reset --hard`. A second copy of the essentials is in the memory ledger.

### ⛔ RESUME RULE
- **Nothing runs by itself.** The in-session timers (16-Sep 08:27 · 17:42 · 17-Sep 08:27 · 17:47) die with the Claude session; they are not VM cron and not evidence.
- If the session closes, a **fresh session resumes from this manifest plus the four 16-Sep cards** (deploy card, Amendments 1–3), starting at the first gate below without a recorded result.
- **Authority:** 👤 Rama's 16-Sep ~00:20 answer (all four; order 4 → 1 → 2–3 only if 1 passes), recorded as a delegated answer. ✅ Item 4 is done: `e7bf477`.
- **Result so far:** no gate has run; ⛔ the VM is untouched.

### GATE 1 — SPOT-CHECK (after the 08:15 token; decisive for everything below)
1. On the twin (`ssh -o BatchMode=yes trading-sbx`, cwd `/home/ubuntu/systems/trading-system`), `md5sum scripts/sr_corp_action_spotcheck.py` must be **`d954c1781e55ebf68d44c9c815ef353e`**. Else ⛔ STOP.
2. Token freshness: `data_store/session/zerodha_token.json` mtime must be today (read the metadata only, ⛔ never the content).
3. Run the wrapper below **once**, over ssh stdin:
   - command: `PYTHONIOENCODING=utf-8 /home/ubuntu/systems/venv/bin/python -B - scripts/sr_corp_action_spotcheck.py`;
   - **stdout and stderr captured separately on the PC**; nothing is written on the VM.
4. **Adjudicate from the returned rows** (⛔ never from the script's headline, which has a known false-pass defect, see ~01:05):
   - **PASS** = sessions demonstrably BEFORE and ON/AFTER 2026-03-25, with no ~10:1 discontinuity;
   - **STOP** = a ~90% discontinuity at the ex-date;
   - **INCONCLUSIVE** = anything else, including a clean post-split-only series. ⛔ No row count is a criterion.
5. **Record:** exact command · stdout · stderr · first and last session · counts before and on/after · instrument token · ISIN if present.

<details><summary>Capture wrapper — md5 <code>dc9476f3e43bbe64b161ed151e973a56</code> (approved, Amendment 2 §4)</summary>

```python
"""Evidence capture around the UNMODIFIED scripts/sr_corp_action_spotcheck.py.

Runs the script's own main() with the card's exact argv. Wraps the two broker
methods on the kite object the script builds, so the one instruments() call and
the one historical_data() call are recorded, not repeated. Writes nothing.
Deployment-card amendment §5 fields: first/last session date, sessions before
and on/after the ex-date, instrument token, and every field of the matching
instrument record.
"""
import importlib.util
import sys
import traceback
from datetime import date, datetime

SCRIPT = sys.argv[1] if len(sys.argv) > 1 else "scripts/sr_corp_action_spotcheck.py"
ARGV = ["--symbol", "V2RETAIL", "--around", "2026-03-25", "--window", "20"]
SYMBOL = "V2RETAIL"
EX_DATE = date(2026, 3, 25)

spec = importlib.util.spec_from_file_location("sr_corp_action_spotcheck", SCRIPT)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

cap = {"instruments_calls": 0, "historical_calls": 0, "matches": None, "hist_kwargs": None, "rows": None}
_orig_build = sc._build_kite


def _build():
    k = _orig_build()
    if k is None:
        return None
    inst, hist = k.instruments, k.historical_data

    def instruments(*a, **kw):
        cap["instruments_calls"] += 1
        rows = inst(*a, **kw)
        cap["matches"] = [dict(r) for r in rows if r.get("tradingsymbol") == SYMBOL]
        return rows

    def historical_data(*a, **kw):
        cap["historical_calls"] += 1
        cap["hist_kwargs"] = {"args": [str(x) for x in a], **{key: str(v) for key, v in kw.items()}}
        rows = hist(*a, **kw)
        cap["rows"] = rows
        return rows

    k.instruments, k.historical_data = instruments, historical_data
    return k


sc._build_kite = _build

print("=== SCRIPT OUTPUT: sr_corp_action_spotcheck.main(%r) ===" % (ARGV,), flush=True)
rc = None
try:
    rc = sc.main(ARGV)
except BaseException:  # the evidence below must print even if the script dies after the call
    print("SCRIPT RAISED:", flush=True)
    traceback.print_exc(file=sys.stdout)
print("=== SCRIPT rc=%r ===" % (rc,), flush=True)

print("=== CAPTURED EVIDENCE ===")
print("broker calls: instruments=%d historical_data=%d" % (cap["instruments_calls"], cap["historical_calls"]))
print("instrument records with tradingsymbol=%s: %s" % (SYMBOL, "NONE CAPTURED" if cap["matches"] is None else len(cap["matches"])))
for m in cap["matches"] or []:
    print("  record:", {key: (str(v) if isinstance(v, (date, datetime)) else v) for key, v in sorted(m.items())})
print("historical_data request:", cap["hist_kwargs"])
rows = cap["rows"]
if rows is None:
    print("rows: NONE CAPTURED")
else:
    def _d(r):
        v = r["date"]
        return v.date() if isinstance(v, datetime) else v
    dates = [_d(r) for r in rows]
    print("rows returned: %d" % len(rows))
    if rows:
        print("first session: %s" % min(dates))
        print("last session : %s" % max(dates))
    print("sessions BEFORE %s: %d" % (EX_DATE, sum(1 for d in dates if d < EX_DATE)))
    print("sessions ON/AFTER %s: %d" % (EX_DATE, sum(1 for d in dates if d >= EX_DATE)))
    print("duplicate dates: %d" % (len(dates) - len(set(dates))))
    print("date        open      high      low       close     volume")
    for r in rows:
        print("%s  %-9s %-9s %-9s %-9s %s" % (_d(r), r.get("open"), r.get("high"), r.get("low"), r.get("close"), r.get("volume")))
print("=== END ===")
```
</details>

### GATE 2 — STARTER INVENTORY (Amendment 3 §2; before ANY transition, deploy or rollback)
Establish **on the twin** and record every mechanism that can start `trading-system.service`. 📄 Memory from 05-Aug (production, ⛔ re-verify here):
- `token-watcher.service` (`deploy/token_watcher.sh`, 30 s poll): starts the service only if the token date is today AND the hour is ≥ 8 and < 16 IST AND the last clean exit was a PRIOR day;
- the unit's `WantedBy=multi-user.target` (a VM reboot starts it);
- `Restart=on-failure` + `RestartPreventExitStatus`, and any drop-in (`trading-system.service.d/`, e.g. `watchman.conf`);
- any timer, any cron line, any healthcheck/watchdog that calls `systemctl start|restart`;
- plus `zerodha_morning.ps1` on the PC (manual).

**Suppression rule** (amended ~01:25 per Amendment 4 §3, the refinement from ChatGPT's review):
1. Identify the exact starter.
2. Determine whether it can fire in the window.
3. **Only if it can:** use the least invasive supported suppression.
4. Record what was suppressed, restore it exactly, and verify the restoration.

⛔ Never blind-mask an infrastructure service.

**Exposure:**
- ⭐ The token-watcher facts (no start at or after 16:00; none after a same-day clean exit) make the **17:42 window safe from it**. Re-check at 17:42.
- ⚠️ **A rollback between 08:15 and 16:00 IS exposed** to the watcher, which is the case the rollback ordering exists for.

### GATE 3 — PRE-COPY (the service must be stopped: after the 17:35 self-exit)
- **Service:** `systemctl is-active trading-system` must not be `active` or `activating`. Record the `ExecStart` `--mode` (📄 expected `live`; ⛔ confirm).
- **md5 at the VM, which must equal `970aabf`:**

  | File | md5 at `970aabf` |
  |---|---|
  | `main.py` | `85219d2285a0b07bc363ebd9e31bac6e` |
  | `signals/signal_processor.py` | `da8c6f983e92f8644656dbe0a081e51d` |
  | `core/config_loader.py` | `a034fc0816582717267bcb1ef70ba5f8` |
  | `config/expected_managers.yaml` | `1dad38c53d556db8c8652389f2838d5f` |

- **Absence:** `sr_shadow/` and `scripts/sr_shadow_evaluate.py` must NOT exist. If either exists ⛔ STOP.
- **YAML:** `config/system_config.yaml` must be `351bd82e73bb0301d850341191c7b72b`. Any mismatch ⛔ STOP.
- **Cron:** the crontab must not already contain `sr_shadow_evaluate`. A duplicate ⛔ STOP.

### GATE 4 — COPY 17 FILES (VM DEPLOYMENT SCOPE 17 · COMMIT SCOPE 27 · ⛔ tests and harness never copied)
- **Source:** the committed bytes of `e7bf477`, ⛔ never the PC working copies (three have CRLF).
- **Transfer — ORDERED, one group at a time** (amended ~01:25 per Amendment 4 §2). The md5 of each group is checked at the destination **before the next group is sent**; the first mismatch ⇒ ⛔ STOP → rollback.

  | Order | Group | Why here |
  |---|---|---|
  | 4a | `sr_shadow` (12 files) | the code must exist before anything references it |
  | 4b | `scripts/sr_shadow_evaluate.py` | not on the boot path |
  | 4c | `core/config_loader.py` | the new loader accepts the old YAML, `enabled: False` |
  | 4d | `signals/signal_processor.py` | its new `sr_shadow=None` kwarg is harmless under the old `main.py` |
  | 4e | `main.py` | ⛔ must follow 4d: `970aabf`'s `SignalProcessor.__init__` has **no `sr_shadow` param and no `**kwargs`**, and the new `main.py` passes `sr_shadow=sr_shadow` unconditionally (`main.py:3640`) ⇒ a TypeError at boot in ANY mode |
  | 4f | `config/expected_managers.yaml` | **LAST**: the registry only ever expects a manager whose code and wiring are already in place |

  Per group: `git -C D:/Projects/wt-sr-shadow-15sep archive --format=tar e7bf477 <group paths> | ssh -o BatchMode=yes trading-sbx 'tar -x --no-overwrite-dir -C /home/ubuntu/systems/trading-system'`, then `md5sum <group paths>` on the VM.
- ⛔ **Never one archive of all 17.** 🔬 `git archive` emits paths SORTED ⇒ `config/expected_managers.yaml` is extracted FIRST and `sr_shadow/` LAST, the exact unsafe order (verified with `tar -t`, ~01:20).
- **Check:** every one of the 17 must equal its committed md5.

| # | Path | Committed md5 (`e7bf477`) | Destination md5 | Result |
|---|---|---|---|---|
| 1 | `config/expected_managers.yaml` | `8625c4b724c34a41f09f06297e3cd797` | ⏸ pending | ⏸ |
| 2 | `core/config_loader.py` | `5b27302483de514ec3117442267609f3` | ⏸ pending | ⏸ |
| 3 | `main.py` | `5aacc1b8028682405834b7dd6238ab5a` | ⏸ pending | ⏸ |
| 4 | `scripts/sr_shadow_evaluate.py` | `edebd2d8251084584cad8eca2ef3002c` | ⏸ pending | ⏸ |
| 5 | `signals/signal_processor.py` | `d45cc437815dba5eb876602724fbb52f` | ⏸ pending | ⏸ |
| 6 | `sr_shadow/__init__.py` | `a8eaba39c80dc9f45fe2fb18ab9d26fb` | ⏸ pending | ⏸ |
| 7 | `sr_shadow/bars.py` | `c28e35c1be186824f5112c982d09ed93` | ⏸ pending | ⏸ |
| 8 | `sr_shadow/calendar.py` | `06fe4b44155b2ef9455abdf152b0a44a` | ⏸ pending | ⏸ |
| 9 | `sr_shadow/decision.py` | `bc5a62dfaf1e0faec8c48d1e24e54b1a` | ⏸ pending | ⏸ |
| 10 | `sr_shadow/evaluator.py` | `b7ad4a264a8158db26add8a6f23c5d16` | ⏸ pending | ⏸ |
| 11 | `sr_shadow/params.py` | `25f6e350257a2e85e13a85a670ab5bdd` | ⏸ pending | ⏸ |
| 12 | `sr_shadow/pipeline.py` | `a2bd0dbb2a7a583e56614b0c4814f2f2` | ⏸ pending | ⏸ |
| 13 | `sr_shadow/pricing.py` | `da30bf651c4e4caa2135a4ac7f92d098` | ⏸ pending | ⏸ |
| 14 | `sr_shadow/runner.py` | `d8216592c3d49b60ca16ae5a72044883` | ⏸ pending | ⏸ |
| 15 | `sr_shadow/schema.py` | `2e5b2a833b09c90d30747a1ed2c6c566` | ⏸ pending | ⏸ |
| 16 | `sr_shadow/store.py` | `90c087593218ca9aee30127cb57f204c` | ⏸ pending | ⏸ |
| 17 | `sr_shadow/zones.py` | `e055bb399ab7901b209155313ec52560` | ⏸ pending | ⏸ |

### GATE 5 — VM-LOCAL `config/system_config.yaml` (⛔ copy-back, never hand-edit)
- **Pre-change md5:** `351bd82e73bb0301d850341191c7b72b` (the 15-Sep fetch; re-checked in Gate 3).
- **Post-change md5:** `4eab1ae5a9716059431b55a210e917c9` = that fetch + the `e7bf477` `sr_shadow:` block.
  - The block is 25 lines, md5 `2ac7322e489fc07e32857c58ab2afa12`, = `git show e7bf477:config/system_config.yaml | sed -n '/^sr_shadow:/,/^regime:/p' | sed '$d'`.
  - Regenerate deterministically if the scratch copy is lost; the result must hash to `4eab1ae5…`.
- **Loader validation, done 🔬 locally** (Python 3.11.9, pydantic 2.13.0, PyYAML 6.0.3):
  - `e7bf477` + block ⇒ VALID `enabled: True`;
  - `e7bf477` without block ⇒ VALID `enabled: False`;
  - `970aabf` + block ⇒ INVALID `extra_forbidden`;
  - `970aabf` without block ⇒ VALID.
- **Transfer:** `ssh trading-sbx 'cat > /home/ubuntu/systems/trading-system/config/system_config.yaml' < <validated file>`. Then md5 at the destination must be `4eab1ae5…`.
- **Validate ON THE VM** with the deployed loader (read-only; `load_all` and its imports write nothing):
  `cd /home/ubuntu/systems/trading-system && /home/ubuntu/systems/venv/bin/python -B -c 'from pathlib import Path; from core.config_loader import load_all; c = load_all(Path("config")); print("LOAD_ALL OK sr_shadow.enabled=", c.system.sr_shadow.enabled)'`
  It must print `LOAD_ALL OK sr_shadow.enabled= True`. Then print the block back.

### GATE 6 — CRON (hand-added, testing VM only; ⛔ never the canonical crontab or `cron_registry.yaml`)
Exactly these two lines, appended to the user crontab. Record the installed crontab diff (+2 lines only) and the timestamp.
```
# sr_shadow_evaluate  [16:05 Mon-Fri]  S&R SHADOW v1.3 EOD evaluator — HAND-ADDED, TESTING VM ONLY
5 16 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/sr_shadow_evaluate.py >> logs/cron-sr-shadow-evaluate.log 2>&1
```

### GATE 7/8 — BOOT (17-Sep 08:15, normal; ⛔ never forced; never restart over a manual stop)
Verify in the boot log:
- `sr_shadow: ENABLED and started (mode=…, log-only)`;
- `effect_telemetry: composition OK`;
- ⛔ **grep explicitly for `composition assertion FAILED` and for any CRITICAL**, since in live a construction failure is a CRITICAL and the service continues;
- `sr_shadow wiring failed` must be absent;
- the config loads; compare against the previous boot's log for anything else changed (a config-hash change is expected).

A failure ⇒ **ORDERED ROLLBACK** (standing note ~01:05, amended ~01:25):
1. Starters first (Gate 2).
2. Remove the block.
3. Restore the 4 wiring files from `970aabf` **in the reverse of the copy order**: `config/expected_managers.yaml` → `main.py` → `signals/signal_processor.py` → `core/config_loader.py`.
   - The registry goes first so it never expects an unbuilt manager.
   - `main.py` goes before `signal_processor.py` because new `main.py` + old `signal_processor.py` = TypeError.
4. Remove the cron line.
5. Run `load_all` under the restored loader.
6. Confirm `expected_managers.yaml` = `1dad38c5…`.
7. A normal boot.

- ⛔ **Do NOT delete `sr_shadow/` or `scripts/sr_shadow_evaluate.py` in a rollback.** The `970aabf` wiring never references them, so they are inert, and deleting is extra work that can fail (Amendment 4 §2).
- The same reverse order applies to a **partial** Gate 4 failure: restore only the wiring files that landed, in that order.
- **Intermediate states verified** (Amendment 5, ~01:40):
  - **R0** (new all four, block removed) is the ONE unavoidable composition-incomplete state; the stopped service covers it.
  - **R1, R3 and R4** are safe.
  - **R2** (old `main.py` + new `signal_processor.py`) is safe **only because** old `main.py:3575` passes all 36 arguments **by keyword** (0 positional; `sr_shadow` is NOT the last parameter).
  - ⛔ **Never restore `signal_processor.py` before `main.py`:** new `main.py` + old `signal_processor.py` ⇒ `TypeError: unexpected keyword argument 'sr_shadow'`.

### GATE 9 — FIRST SESSION (17-Sep, measurement only)
Per the deploy card §4 and Amendment §6: TIME_CLOSE is a diagnostic only; print both P counts (R-C); ⛔ no tuning.


---

## ROLLBACK — THE STANDING NOTES, VERBATIM FROM SYSTEM_MAP

### ⛔🔝 STANDING NOTE — S&R SHADOW ROLLBACK IS ATOMIC (testing VM)

**ROLLBACK = all of the following in ONE stopped-service action, or none. There is no valid partial rollback:**
1. Restore **ALL FOUR** wiring files from `970aabf`: `main.py`, `signals/signal_processor.py`, `core/config_loader.py`, `config/expected_managers.yaml`.
2. In the same action, **REMOVE** the VM-local `sr_shadow:` block from `config/system_config.yaml`. ⛔ It is **not optional**.
3. Remove the hand-added cron line.
4. `sr_shadow/`, `scripts/sr_shadow_evaluate.py` and `data_store/sr_shadow/` may be left in place: nothing imports them once the wiring is reverted.

**Hazards:**
- ⛔ **`sr_shadow.enabled: false` ALONE IS NOT A ROLLBACK.** The registry still says `expected-active`, so `assert_composition` (`main.py:4277` @ `e7bf477`) either RAISES (paper, a failed boot) or sends a CRITICAL and continues (live). A quick disable must take the registry entry out in the same action.
- ⛔ **A LEFTOVER `sr_shadow:` BLOCK UNDER THE `970aabf` LOADER KILLS THE BOOT IN ANY MODE.** 🔬 At `970aabf`, `SystemConfig` has `model_config = ConfigDict(extra="forbid")` (`core/config_loader.py:1988`) and system_config.yaml is checked with `schema_cls.model_validate(data)` (`:2507`). Config load precedes the mode, so this hits live too.
  - The amendment's step 3 ("the block may be left or removed; inert either way") is **WRONG**.
  - 🔬 **Proven locally** on the twin's own `system_config.yaml`, as fetched on 15-Sep (md5 `351bd82e…`):

    | Loader | YAML | Result |
    |---|---|---|
    | `970aabf` | + block | **INVALID `sr_shadow: extra_forbidden`** |
    | `970aabf` | as-is | VALID (control) |
    | `e7bf477` | + block | VALID, `enabled: True` (post-append md5 `4eab1ae5…`) |
    | `e7bf477` | as-is | VALID, `enabled: False` (the gap between steps 5 and 6 is safe) |

- ⚠️ **The same pairing applies going forward:** the four wiring files and the VM-local block are one unit, deployed together in one stopped-service window.


### ⛔🔝 STANDING NOTE — S&R SHADOW ROLLBACK ORDER (supersedes the order in the ~01:00 note; the content is unchanged)

Config validity by loader and block (🔬 proven locally on the twin's own YAML, ~01:00):

| Loader | Block present | Config load |
|---|---|---|
| `970aabf` | yes | ⛔ **INVALID** (`extra_forbidden`), the ONLY invalid cell |
| `970aabf` | no | valid |
| `e7bf477` | yes | valid, `enabled: True` |
| `e7bf477` | no | valid, `enabled: False` |

- **DEPLOY order:** files first, then the block.
- **ROLLBACK order is NOT the mirror image:**
  1. Confirm the service is stopped.
  2. **REMOVE the VM-local `sr_shadow:` block** (state: new loader, no block ⇒ valid).
  3. **Restore all four wiring files from `970aabf`** (state: old loader, no block ⇒ valid).
  4. Remove the hand-added cron line (independent of the other steps).
  5. Validate that the config loads under the restored loader.
  6. Confirm `config/expected_managers.yaml` is back at its `970aabf` md5 `1dad38c5…`.
  7. Only then allow a normal boot.
- ⛔ Restoring the files first passes THROUGH the invalid cell, and is safe only if nothing boots meanwhile.
- ⚠️ **One refinement, recorded and not contested:** every state in this order is **config-valid**, but the states between step 2 and the end of step 3 are **composition-inconsistent**. The registry still lists `sr_shadow` as `expected-active` while nothing constructs it, so a boot there ⇒ paper RAISES / live CRITICAL. The same is true forward, between steps 5 and 6. The **stopped service** stays the guard for that dimension, so both windows must be one uninterrupted stopped-service action.


---

## VM-LOCAL YAML — COPY-BACK RULE, VERBATIM

### STEP 6 — COPY BACK THE VALIDATED FILE; ⛔ NEVER HAND-EDIT ON THE VM
1. The VM's current `config/system_config.yaml` must be md5 **`351bd82e73bb0301d850341191c7b72b`**, the file fetched 15-Sep. ⛔ Any other value ⇒ **STOP**: the VM has drifted and the validated append no longer applies.
2. Copy back the locally built file: that fetch + the `e7bf477` `sr_shadow:` block (25 lines, md5 `2ac7322e…`). It is validated under the `e7bf477` loader (`enabled: True`), md5 **`4eab1ae5a9716059431b55a210e917c9`**.
3. Re-verify **`4eab1ae5…`** at the destination.


---

## KNOWN DEFECT IN THE SPOT-CHECK SCRIPT, VERBATIM

### ⛔🔝 KNOWN DEFECT — `scripts/sr_corp_action_spotcheck.py` CAN PRINT A FALSE PASS
- **What:** `main()` never checks that the returned candles span the ex-date. Any series with ≥ 2 rows and every overnight close ratio within 15% of 1.0 prints **"VERDICT: ADJUSTED (continuous) — historical_data returns split/bonus-adjusted candles. ✅"**. That includes a series that is **entirely after** the event.
- **Script hash:** md5 `d954c1781e55ebf68d44c9c815ef353e`, identical at `970aabf` and `e7bf477`. It ships with SNR-DETECTOR-V1 (`dea336a`) and is on the testing VM.
- **Plausible cause** (💭 inference, not verified): an instrument-token change at an ISIN change, as with V2RETAIL on 25-Mar-2026, can return only post-event bars.
- 🔬 **Reproduction** (PC, 16-Sep ~00:55; FAKE broker, fabricated data):
  - a stub `kiteconnect` module whose `historical_data` returns only weekday sessions **≥ 2026-03-25** at a flat 205.0;
  - `main(["--symbol","V2RETAIL","--around","2026-03-25","--window","20"])` prints `V2RETAIL around 2026-03-25: 11 daily candles` · `largest overnight close ratio = 1.000 at None` · **`VERDICT: ADJUSTED (continuous) … ✅`**, rc 0;
  - the capture wrapper, from the same rows, shows `sessions BEFORE 2026-03-25: 0`.
- **Also known:** it prints neither the first nor last date, nor the per-side counts, so a reader cannot see the gap.
- ⛔ **Do not trust its headline.** Adjudicate from the returned rows.
- **Not fixed; not this deployment's job.**


---

## AMENDMENT 3 NOTES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 3" (16-Sep). Nothing needed from Rama; ⛔ the VM is still untouched.

1. **Why the rollback order stays even with the service stopped.** If something DOES start the service mid-transition, the two intermediate states are not equally bad:
   - composition incomplete ⇒ **live: a CRITICAL and the service stays up** (paper: a failed boot);
   - config invalid ⇒ **a failed boot in ANY mode**, before the mode is read.

   On this live VM, the order turns a guaranteed boot failure into a CRITICAL alert. It costs nothing.
2. **⛔ "Keep the service stopped" is a rule, not an enforceable condition.** A clock-driven starter exists (the token watcher, polling every 30 s from 08:00). Before ANY deploy or rollback transition:
   - establish and record every starter;
   - confirm none can fire in the window;
   - mask or stop any that could, FIRST, and restore it LAST, recording both.

   ⛔ A rollback near 08:15 deals with the starter before touching a single file. Procedure: manifest Gate 2 (~01:12).
3. **The deploy manifest is now in this tracked file** (`MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026`, ~01:12): 17 paths with committed md5, the YAML pre/post md5 and validation, the exact cron line, the starter inventory, the wrapper source and the resume rule. **If the Claude session closes, nothing runs; a fresh session resumes from that manifest plus the cards.**


---

## AMENDMENT 4 NOTES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 4" (16-Sep). ⛔ No docs commit, ⛔ no amend. Nothing needed from Rama beyond receiving the file. The VM is still untouched.

1. **Standalone manifest, outside every git repository** (§1):
   - **`D:/Projects/_preservation/SR_SHADOW_V1_3_DEPLOY_MANIFEST_16-Sep-2026__preserved_2026-09-16T0128IST.md`**, 348 lines, md5 `87fbc44b59d9efb415b5b7879e649a89`.
   - It is assembled from this file's manifest (as amended ~01:25) plus the verbatim rollback, copy-back and defect notes, with a precedence line.
   - 🔬 `_preservation/` is not a git repo. It follows the folder's existing `__preserved_<stamp>` convention; Rama saves it with the cards.
   - 📄 **Correction to the card's table:** the memory ledger is also outside git (`~/.claude/projects/…/memory/`, 🔬 not a repo), so `reset --hard` cannot touch it. It holds only the essentials, though, so the standalone file remains the complete copy.
2. **Ordered copy inside Gate 4** (§2), now in the manifest: `sr_shadow/` → evaluator → `config_loader.py` → `signal_processor.py` → `main.py` → `expected_managers.yaml` LAST, with md5 per group before the next.
   - 🔬 **Two facts behind the order:**
     - `git archive` emits SORTED paths, so the planned single archive would have extracted the registry FIRST;
     - `970aabf`'s `SignalProcessor.__init__` has no `sr_shadow` param and no `**kwargs`, while the new `main.py:3640` passes `sr_shadow=` unconditionally ⇒ new `main.py` before new `signal_processor.py` = a TypeError at boot in ANY mode. The card listed the three wiring files as one step; the order within it matters.
   - **Rollback:** restore the files in the exact reverse order (registry → `main.py` → `signal_processor.py` → `config_loader.py`), after removing the block. ⛔ Never delete `sr_shadow/` or the evaluator.
3. **Starter suppression narrowed** (§3, ChatGPT's refinement): identify → can it fire in the window → only then the least invasive supported suppression → record → restore exactly → verify. ⛔ Never blind-mask infrastructure.
   - The watcher cannot start at or after 16:00, nor after a same-day clean exit ⇒ the 17:42 window is safe from it (re-check at 17:42).
   - ⚠️ A rollback between 08:15 and 16:00 IS exposed.
4. **VM-side `load_all` placement accepted** (§4): after the copy-back, before cron and any boot.


---

## AMENDMENT 5 — ROLLBACK STATES VERIFIED, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 5" (16-Sep). Verification only: no code, no commit, and the VM is still untouched.

**⛔ Correction to my own Amendment 4 reply:** "no intermediate state has a config, composition or TypeError failure" was **wrong about R0**. R0 (all four files new, block removed) is composition-incomplete, as I had stated myself when answering Amendment 3.

### The rollback states, verified (block already removed; restore order registry → `main.py` → `signal_processor.py` → `config_loader.py`)

| # | VM state | Verdict | Evidence (🔬 local, `e7bf477` vs `970aabf`) |
|---|---|---|---|
| R0 | new all four · no block | ⚠️ **UNSAFE, unavoidable**: the registry expects `sr_shadow`, nothing builds it ⇒ live CRITICAL + continue / paper raise | (a) + (b) below |
| R1 | new main/sp/loader · OLD registry · no block | SAFE | `enabled` defaults False ⇒ not built and not registered; the old registry does not list it; config valid (matrix row 4) |
| R2 | OLD main · new sp/loader · old registry | **SAFE, by keyword binding** (§3 below) | old call: 0 positional, 36 keywords, binds by NAME |
| R3 | OLD main/sp · new loader · old registry | SAFE | no caller passes `sr_shadow`; config valid (matrix row 4) |
| R4 | all OLD · no block | SAFE | matrix row 2 |

**(a) With no block, `enabled` defaults to False.**
- `SrShadowConfig.enabled: bool = False` (`core/config_loader.py` @ `e7bf477`, class at :1266).
- 🔬 Runtime proof: matrix row 4 printed `VALID enabled: False` on the twin's own YAML.

**(b) With `enabled` False, the manager is neither constructed nor registered.** 🔬 `git grep` over the `e7bf477` tree, excluding tests:
- The only `_effect_handle("sr_shadow")` is `sr_shadow/runner.py:120`, inside `SrShadowService.__init__`.
- The only `SrShadowService(` is `runner.py:252`, inside `build_sr_shadow`.
- The only `build_sr_shadow(` is `main.py:3529`, inside `if _sr_shadow_on:` (`:3526`), where `_sr_shadow_on = bool(cfg is not None and cfg.enabled)` (`:3489`).
- No `register_constructed("sr_shadow")` exists anywhere; the infra tuple (`main.py:4262–4273`) does not name it.

**Why no order removes R0** (the card's argument, confirmed from code): restoring the registry BEFORE removing the block gives new loader + block + old registry ⇒ `enabled: True` ⇒ built and registered but absent from the registry ⇒ `unknown` in `effect_telemetry.assert_composition` (`core/effect_telemetry.py:182`) ⇒ a composition failure. Every order has exactly one unsafe window; this one lands on the CRITICAL-and-continue path on the live VM, not on a config-load failure. The stopped service covers it.

### §3 — the silent positional-binding hazard, checked
1. **Is `sr_shadow` the LAST parameter? ⛔ NO.** In `e7bf477`, `SignalProcessor.__init__` has 43 params including `self`; `sr_shadow` sits at **index 31 of 42**, inserted after `sr_detector` and before `zone_warmer`. The last is `evidence`. No `*args` and no `**kwargs`.
2. **Does old `main.py` bind by keyword? ✅ YES, completely.** 🔬 An AST pass over every non-test `SignalProcessor(` call:
   - `970aabf` `main.py:3575` (the only site) = **positional 0 · `*` expansions 0 · `**` expansions 0 · 36 keywords · 0 duplicates**.
   - `inspect.Signature.bind` of those 36 keywords against the NEW signature ⇒ **OK**: every keyword binds by name, none unexpected, and `sr_shadow` is not supplied (→ default `None`).
   - (`e7bf477` `main.py:3607`: positional 0, 37 keywords.)
   - Non-vacuity control: the same counter on `SignalProcessor(q, store, bus, *extra, mode=1, **kw)` reports positional 4 · `*` 1 · `**` 1.
- ⇒ **R2 is SAFE.** Keyword binding is position-independent, so the inserted parameter cannot shift any argument. The safety condition is (1) **OR** (2); the card's "if either is not true, R2 is unsafe" was stricter than needed, and (2) holds.
- ⛔ **The card's fallback ("swap `main.py` and `signal_processor.py` — safe in the other direction") would NOT have been safe.** Restoring `signal_processor.py` first creates **new `main.py` + old `signal_processor.py`**. 🔬 Binding `e7bf477` `main.py:3607`'s 37 keywords against the `970aabf` signature ⇒ **`TypeError: got an unexpected keyword argument 'sr_shadow'`**, a boot crash in ANY mode (the Amendment 4 finding). That state is not R3.
- ⇒ The restore order **registry → `main.py` → `signal_processor.py` → `config_loader.py` stays**. ⚠️ If a future edit makes old `main.py` pass anything positionally, re-run this check before any rollback.
- Scripts (scratchpad, session-only): `sp_call_binding_check.py` and `sp_call_binding_check_reversed.py`.

### Copies (§4)
Three copies, three failure modes:
- the preserved file in `_preservation/`, outside git;
- SYSTEM_MAP: discoverable, dies to `reset --hard`;
- the ledger: outside git, essentials only.

No docs commit; `e7bf477` stays unamended.
