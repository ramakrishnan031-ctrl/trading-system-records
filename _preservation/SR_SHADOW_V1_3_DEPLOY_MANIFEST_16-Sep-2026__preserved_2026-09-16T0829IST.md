# S&R SHADOW v1.3 — TESTING-VM DEPLOY MANIFEST (STANDALONE COPY, OUTSIDE GIT)

**Preserved:** 2026-09-16T0829 IST, per the 16-Sep "DEPLOYMENT CARD AMENDMENT 4" §1.
- **Save it with the cards.**
- **Tracked twin:** `D:/Projects/trading-system/docs/SYSTEM_MAP.md`, sections `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` (~01:12, amended ~01:25, ~01:40 and ~02:09) and the 16-Sep amendment entries.
- ⚠️ That twin is tracked but UNCOMMITTED: `git checkout -- .` or `reset --hard` destroys it. This file is the copy that survives.
- ⛔ **If the two ever differ, the later timestamp wins, and the difference is reported.**
- ✅🔝 **THIS VERSION RECORDS THE GATE 1 RESULT: V2RETAIL RAN 16-Sep **08:26 IST** AND **PASSED** (full entry at the end).** ⛔ **A resuming session must NOT re-run it** — it is specified as ONE read-only run and the broker calls (`instruments=1 historical_data=1`) are already spent. Gates 2–9 have NOT run; ⭐ the VM is still UNCHANGED.
- **Supersedes** `…T0735IST.md`, which superseded 0210, 0156, 0145 and 0128. **This version adds AMENDMENT 8**, applied ~07:21–~07:35 IST: (a) every guarded write is now **IDEMPOTENT** — the precondition has THREE outcomes (`ALREADY_DONE` / proceed / `REFUSED_DRIFT`), so a re-run is no longer indistinguishable from drift; (b) **every command is labelled `RUNNABLE — LITERAL COMMAND` or `TEMPLATE — DO NOT RUN`**, and the ones that mattered are now literal — **20 runnable commands, 0 placeholder tokens, all 20 parse under `bash -n`**; (c) 🔴 a recorded **FINDING**: Amendment 8 §2's claim that the whole sequence becomes re-runnable from the top is true at file level but ⛔ **NOT at sequence level — Gate 3 still STOPs on a second pass**; recorded, ⛔ not fixed. The 0210 version added Amendment 7: every boot-path write (Gates 4c–4f, Gate 5, every rollback restore) becomes a guarded write-then-rename with the md5 checked BETWEEN `cat` and `mv`; Gate 3 gains rename preconditions; and the PRE and POST YAML copies are preserved outside git.
- **Companion files in this folder:** `TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml` and `TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml`. Keep them with this manifest; Gate 5 and the rollback read them.
- ⭐ **NEW COMPANION (Amendment 8):** `SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py` — 3,438 bytes, md5 `dc9476f3e43bbe64b161ed151e973a56`. ⚠️ **The approved Gate 1 wrapper was NOT a file anywhere** — it existed only as the fenced listing inside the manifest. 🔬 Extracted ~07:30, verified to reproduce the approved md5 exactly, and it compiles. Gate 1 step 3 now reads it by that literal path.
- ⚠️ **Time-label correction:** the 0128 version's section labels ran AHEAD of the system clock (e.g. "~01:30", "amended ~01:50"). Measured clock readings put the writes at: manifest ~01:12 · Amendment 3 ~01:15 · `tar -t` check ~01:20 · Amendment 4 ~01:25 · Amendment 5 ~01:40. The tracked SYSTEM_MAP copy is corrected, as is this file. The section IDs (`MANIFEST-…`, `RESULT-…-AMENDMENTn-…`) are the stable references.
- **Precedence inside this file,** where the verbatim notes below differ: the manifest's **Gate 4** (ordered copy) and **Gate 7/8 rollback** (block first, then the four files in reverse copy order, ⛔ no deletion of `sr_shadow/`), amended ~01:25, ~01:40 and ~02:09, supersede the ~01:05 ordered note, which in turn supersedes the order in the ~01:00 atomic note. The content of all three agrees; only the ordering was refined.

**Code:** commit `e7bf477` on `feat/sr-shadow-v1.3-15sep` (worktree `D:/Projects/wt-sr-shadow-15sep`, parent `970aabf`). ⛔ Unamended, ⛔ unpushed, ⛔ never `main`.

**Scope:** COMMIT 27 files · VM DEPLOYMENT 17 files · VM-LOCAL CONFIG = the `sr_shadow:` block, copied back as a validated file. TESTING VM `130.210.13.114` (`trading-sbx`) ONLY; ⛔ production untouched.

**Cards this manifest implements:** "S&R SHADOW v1.3 — DEPLOYMENT AND FIRST SESSION" and Amendments 1–7 (all 16-Sep).

---
## 16-Sep-2026 (Wed) ~01:12 IST — `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` — ⭐ THE TRACKED DEPLOY MANIFEST (Amendment 3 §3) · TESTING VM ONLY

**Why here:** the build report is UNTRACKED and the schedule exists only as in-session timers. This file is tracked. ⚠️ It is also uncommitted in the main tree, so it survives `git clean` but ⛔ not `git checkout -- .` or `reset --hard`. A second copy of the essentials is in the memory ledger.

### ⛔ RESUME RULE
- **Nothing runs by itself.** The in-session timers (16-Sep 08:27 · 17:42 · 17-Sep 08:27 · 17:47) die with the Claude session; they are not VM cron and not evidence.
- If the session closes, a **fresh session resumes from this manifest plus the four 16-Sep cards** (deploy card, Amendments 1–3), starting at the first gate below without a recorded result.
- **Authority:** 👤 Rama's 16-Sep ~00:20 answer (all four; order 4 → 1 → 2–3 only if 1 passes), recorded as a delegated answer. ✅ Item 4 is done: `e7bf477`.
- **Result so far:** ✅ **GATE 1 RAN 16-Sep 08:26 IST and PASSED** (entry below). ⛔ Gates 2–9 have NOT run. ⭐ **The VM is still UNCHANGED** — Gate 1 is read-only and wrote nothing on it; `0` bytes of stderr.

### ⛔🔝 THE ONE UNSAFE CELL, AND THE STARTER RULE (applies to deploy AND rollback; added ~01:55 per Amendment 6 §2)

**The cell (Amendment 6 §2, verified row by row ~01:55):** among states made of COMPLETE files, both ordered procedures visit exactly one unsafe configuration, the same cell from either side:

> **NEW `config/expected_managers.yaml` PRESENT + `sr_shadow:` BLOCK ABSENT**

- The deploy enters it at Gate 4f, before Gate 5; the rollback enters it after removing the block, before restoring the registry (R0).
- No ordering removes it: going the other way lands on the unexpected-manager cell (block present + old registry ⇒ `unknown`, `effect_telemetry.py:182`).
- **The card's rule, verbatim:** *"from the moment `expected_managers.yaml` changes until the YAML block matches it, the service must not start."*

**⛔ The operative starter rule is WIDER.** The card's rule covers only complete-file states, and a transfer can leave a PARTIAL file:
- 🔬 PC demo, GNU tar 1.35 (~01:55): an existing `970aabf` `main.py` (208,758 bytes, md5 `85219d22`) was overwritten by `git archive e7bf477 main.py | head -c 150000 | tar -x` (tar rc=2, "Unexpected EOF").
  - It was left as a **147,968-byte file** (md5 `4041aad9`) that still **COMPILES** but has **no `if __name__ == "__main__":`** (`main.py:4319` of the full file).
  - ⇒ The old file does NOT survive an interrupted copy.
  - 💭 Started, it would define its functions and **exit 0 having done nothing**: `Restart=on-failure` ignores exit 0, and the watcher skips a same-day clean exit (📄 memory, 05-Aug) ⇒ a **silent** no-trade day.
- Partial states exist BEFORE the registry changes (Gates 4c–4e) and during every rollback restore. The checksum gate DETECTS them; only a stopped service PROTECTS until they are repaired.

> **OPERATIVE RULE:** from the first write to any boot-path file (`core/config_loader.py`, `signals/signal_processor.py`, `main.py`, `config/expected_managers.yaml`, `config/system_config.yaml`) until every written file verifies at its target md5 AND `load_all` passes on the VM, **the service must not start**. Deploy and rollback alike.

It contains the card's cell as a special case.

**Both wordings stand** (Amendment 7 §2): ONE unsafe COMPLETE-FILE cell, plus TRANSFER-INTEGRITY hazards. The latter are not a second cell, because their content depends on where the interruption fell.
- Since ~02:09 every boot-path file (Gates 4c–4f, Gate 5 and every rollback restore) is written by a **guarded write-then-rename**: bytes go to `<path>.tmp`, the md5 is checked, the mode is copied, then an atomic `mv`.
  - ⇒ A boot-path file is always either fully old or fully verified-new; the transfer-integrity hazard is removed for those files.
- The operative rule is still kept, as defence in depth: a killed transfer can leave `.tmp` residue, the rename instant exists, and an operator may deviate.

### ⛔🔝 COMMAND LABELLING · THE IDEMPOTENT GUARDED WRITE (Amendment 8, applied ~07:29–~07:33 IST 16-Sep)

⚠️ **Time-label correction (same class as the 0128 one, caught the same way):** this pass's first draft labelled its own work `~07:35 / ~07:40 / ~07:45 / ~07:55 / 0800`, **ahead of the system clock.** 🔬 Corrected against artifact mtimes: guard contract demo **07:21** · round-trip rehearsal **07:27** · wrapper extracted **07:30**, preserved **07:31** · manifest amended **07:29–07:33** · standalone copy **07:35**. ⭐ The section IDs are the stable references, ⛔ not the time labels.

**§3 — EVERY command in this manifest now carries one of two labels, and the label is part of the command.**

| Label | Meaning |
|---|---|
| **`RUNNABLE — LITERAL COMMAND`** | literal paths, literal digests, no placeholders. Safe to paste as-is. |
| **`TEMPLATE — DO NOT RUN`** | contains `<...>` or `…`. It explains a SHAPE. ⛔ Pasting it is an incident. |

- 🔬 **Why:** the **02:08 incident** was a command containing `<path>` / `<validated file>`, written to explain a fix and then typed as if runnable. ⭐ **Nothing was written — the shell was still waiting on the unmatched quote.** ⛔ Not a Gate 5 event · ⛔ no VM state change · ⛔ no rollback. 👤 Authorship of the defective command was accepted by the card's author, 16-Sep.
- ⛔ **Mechanical criterion for a RUNNABLE command** (so the label can be checked, not judged): `grep -oE '<[A-Za-z_][A-Za-z0-9_ .-]*>'` over the command must return **NOTHING**, and it must contain no `…`. A genuine shell redirect (`< path`, `> /dev/null`) is not a placeholder and is allowed.

**§2 — every guarded write is now IDEMPOTENT: the precondition has THREE outcomes, not two.**

⛔ **THE TRAP THIS REMOVES.** An inline current-md5 precondition (ChatGPT §6 — adopted, and right) FAILS on a second run: the file is at the TARGET md5, not the EXPECTED-CURRENT one, so the guard prints `REFUSED` and exits 1 — **output identical to genuine drift.** ⇒ An operator re-running a rollback at 08:10 because they are unsure how far it got sees `REFUSED` and ⛔ **cannot tell "already done" from "something is wrong."** ⭐ That is the worst possible moment for an ambiguous error.

**THE CONTRACT — FOUR terminal states. ⭐ The target is NEVER left partial in any of them.**

*(`EXPECTED-CURRENT` and `TARGET` are used instead of old/new because the two directions swap them: deploying, EXPECTED-CURRENT is the `970aabf` md5 and TARGET the `e7bf477` md5; rolling back, they are exchanged.)*

| `md5(P)` on entry | Stream | Prints | rc | Effect on `P` |
|---|---|---|---|---|
| **EXPECTED-CURRENT** | complete | `WROTE <p>` | **0** | replaced, verified at TARGET |
| **EXPECTED-CURRENT** | short / empty | `REFUSED_WRITE <p>` | **1** | ⭐ **untouched, still EXPECTED-CURRENT**; `.tmp` removed |
| **TARGET** | (drained) | `ALREADY_DONE <p>` | **0** | untouched — already correct |
| anything else, **incl. absent** | (drained) | `REFUSED_DRIFT <p> have=… want=…` | **1** | untouched |

- ⭐ `ALREADY_DONE` and `REFUSED_DRIFT` are now **DISTINGUISHABLE**. `REFUSED_WRITE` is Amendment 7's behaviour, deliberately KEPT — a bad stream must still refuse.
- ⭐ Both early-exit paths run `cat > /dev/null` to **DRAIN the inbound stream**, so the local `git show` is not killed by SIGPIPE and the ssh exit status is the guard's own.

**THE SHAPE — `TEMPLATE — DO NOT RUN`** (every literal instance is in Gate 4, Gate 5 and the rollback below):
```
cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < <PATH>; } 2>/dev/null | cut -c1-32); if [ "$cur" = "<TARGET>" ]; then cat > /dev/null; echo "ALREADY_DONE <PATH>"; exit 0; fi; if [ "$cur" != "<EXPECTED-CURRENT>" ]; then cat > /dev/null; echo "REFUSED_DRIFT <PATH> have=${cur:-NONE} want=<EXPECTED-CURRENT>"; exit 1; fi; cat > <PATH>.tmp && [ "$(md5sum < <PATH>.tmp | cut -c1-32)" = "<TARGET>" ] && chmod --reference=<PATH> <PATH>.tmp && mv -- <PATH>.tmp <PATH> && echo "WROTE <PATH>" || { rm -f -- <PATH>.tmp; echo "REFUSED_WRITE <PATH>"; exit 1; }
```

🔬 **DEMONSTRATED ON THE PC (~07:21 IST, this exact shape, ⛔ not a paraphrase)** — fixtures EXPECTED-CURRENT `2534db9f…`, TARGET `bdf16cfe…` (6,715 B); six cases, each rc and each post-state read back:

| Case | Result | rc | Target after |
|---|---|---|---|
| EXPECTED-CURRENT + full stream | `WROTE` | 0 | TARGET, no `.tmp` |
| ⭐ **immediate RE-RUN** *(the Amendment 8 case)* | `ALREADY_DONE` | 0 | TARGET, unchanged |
| drifted target | `REFUSED_DRIFT have=168c5903… want=2534db9f…` | 1 | unchanged |
| EXPECTED-CURRENT + 3,000-of-6,715-byte stream | `REFUSED_WRITE` | 1 | ⭐ **still EXPECTED-CURRENT**, no `.tmp` |
| EXPECTED-CURRENT + empty stream | `REFUSED_WRITE` | 1 | still EXPECTED-CURRENT |
| target **ABSENT** | `REFUSED_DRIFT have=NONE` | 1 | — · ⭐ **0 bytes of stderr** |

- ⭐ The absent-file case is why the precondition read is wrapped `{ md5sum < P; } 2>/dev/null`: the bare form leaked a shell redirect error to stderr. It **reports**, it does not leak, and it is ⛔ never silent.
- ⚠️🔬 ⛔ **MODE PRESERVATION IS *NOT* PROVEN BY THIS DEMO — THAT CHECK WAS VACUOUS.** Windows did not honour `chmod 600` on the fixture (`stat -c %a` read **644 before AND after**) ⇒ `chmod --reference` **could not have been observed failing**. ⭐ The real protection is the **VM-side `stat -c %a` check after every write**, ⛔ not this demo. Limit inherited unchanged from Amendment 7.

**⭐ WHAT THIS BUYS — AND ITS EXACT LIMIT, WHICH IS NOT WHAT THE AMENDMENT CLAIMS.**

- ✅ **At the FILE level the claim holds:** a fresh session resuming from this manifest does **not** need to know which files landed. It re-runs the writes in order; each either proceeds or reports `ALREADY_DONE`, and only real drift stops it.
- 🔴⛔ **At the SEQUENCE level it does NOT hold yet, and GATE 3 IS WHY.** Gate 3's preconditions are *absence* and *pre-state* checks that a partially-completed run has **already falsified**. On a second pass they STOP — ⭐ **the very two-outcome trap Amendment 8 removed from the writes, surviving one gate earlier:**

  | Gate 3 precondition | After a partial first run | Re-entry verdict |
  |---|---|---|
  | `sr_shadow/` and `scripts/sr_shadow_evaluate.py` must NOT exist | 4a/4b landed them | ⛔ STOP |
  | the 4 wiring md5s must equal `970aabf` | any of 4c–4f landed | ⛔ STOP |
  | `config/system_config.yaml` = `351bd82e…` | Gate 5 landed | ⛔ STOP |
  | crontab must not contain `sr_shadow_evaluate` | Gate 6 landed | ⛔ STOP |

- 🏷️ **STATUS — the two claims are labelled separately, ⛔ never merged:** the write-level fix is **BUILT + 🔬 DEMONSTRATED (PC)**; *"the whole transfer sequence is re-runnable from the top"* is **⛔ NOT YET TRUE**.
- ⏸ **OWED — ⛔ NOT DECIDED HERE, and ⛔ NOT FIXED.** Either Gate 3 gets the same three-outcome treatment (pre-state **or** recorded post-state ⇒ proceed; anything else ⇒ STOP), or a resumed run re-enters at the first gate with no recorded result and Gate 3's pre-state checks are scoped to a first entry. ⭐ **Both are changes to the deploy procedure's STOP conditions, which Amendment 8 does not authorise** (*"No rebuild. No redesign."*). Until one is authorised: **a resumed run that trips Gate 3 STOPS and reports.** ⭐ That is the safe direction, and it is already what the gate does — so this limit costs a stall, ⛔ never a bad write.

### GATE 1 — SPOT-CHECK (after the 08:15 token; decisive for everything below)
0. ⭐ **PREREQUISITE — the approved wrapper is NOT a file in the repo; it exists only as the fenced listing below.** It is now ALSO preserved outside git: `D:/Projects/_preservation/SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py` — **3,438 bytes, md5 `dc9476f3e43bbe64b161ed151e973a56`**. 🔬 Extracted from that listing at ~07:30 and verified to reproduce the approved md5 **exactly**, and it compiles (`py_compile` rc 0). ⛔ If the file is missing, re-extract the listing below and ⛔ run nothing until it hashes to `dc9476f3…`.
1. **Script identity on the twin.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum scripts/sr_corp_action_spotcheck.py'
```
   Must print **`d954c1781e55ebf68d44c9c815ef353e`**. Else ⛔ STOP.
2. **Token freshness — metadata only, ⛔ never the content.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && stat -c "%n mtime=%y size=%s" data_store/session/zerodha_token.json'
```
   The mtime date must be **today**. Else ⛔ STOP — a stale token makes the run meaningless.
3. **THE ONE READ-ONLY RUN.** The wrapper goes over ssh stdin; stdout and stderr are captured **separately on the PC**; ⛔ nothing is written on the VM. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && PYTHONIOENCODING=utf-8 /home/ubuntu/systems/venv/bin/python -B - scripts/sr_corp_action_spotcheck.py' < D:/Projects/_preservation/SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py > D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stdout.txt 2> D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stderr.txt
```
   ⛔ **ONCE.** The wrapper hard-codes the card's exact argv (`--symbol V2RETAIL --around 2026-03-25 --window 20`) and wraps the broker methods so the single `instruments()` and single `historical_data()` are **recorded, not repeated**.
4. **Adjudicate from the returned rows** (⛔ never from the script's headline, which has a known false-pass defect, see ~01:05):
   - **PASS** = sessions demonstrably BEFORE and ON/AFTER 2026-03-25, with no ~10:1 discontinuity;
   - **STOP** = a ~90% discontinuity at the ex-date;
   - **INCONCLUSIVE** = anything else, including a clean post-split-only series. ⛔ No row count is a criterion.
5. **Record:** exact command · stdout · stderr · first and last session · counts before and on/after · instrument token · ISIN if present.

<details><summary>Capture wrapper — md5 <code>dc9476f3e43bbe64b161ed151e973a56</code> (approved, Amendment 2 §4)</summary>

*⭐ This fence is a **PYTHON SOURCE LISTING**, ⛔ not a command — the TEMPLATE/RUNNABLE labels do not apply to it. It is the authoritative copy of the wrapper; the preserved `.py` in Gate 1 step 0 was extracted from it and hashes to the same `dc9476f3…`.*

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
- **Rename preconditions** (added ~02:09 per Amendment 7): the guarded writes replace the directory entry, so they would silently break a symlink or hard link, and could change mode or owner.
  - Run: `cd /home/ubuntu/systems/trading-system && stat -c '%n|%F|%a|%U:%G|links=%h' core/config_loader.py signals/signal_processor.py main.py config/expected_managers.yaml config/system_config.yaml`
  - Each must be a **`regular file`**, **`links=1`**, owner **`ubuntu`**; **record each mode**. Any symlink, hard link or other owner ⛔ STOP.
  - **Absence:** none of `core/config_loader.py.tmp`, `signals/signal_processor.py.tmp`, `main.py.tmp`, `config/expected_managers.yaml.tmp`, `config/system_config.yaml.tmp` may exist. If any exists ⛔ STOP.

- ⭐ **ALL GATE 3 CHECKS IN ONE READ-ONLY SWEEP** (added ~07:33, Amendment 8 §3 — previously these were six separate prose checks an operator had to assemble). Nothing below writes. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && echo "== service (must NOT be active/activating) ==" && systemctl is-active trading-system; echo "== md5 (all five must equal 970aabf / 351bd82e) ==" && md5sum main.py signals/signal_processor.py core/config_loader.py config/expected_managers.yaml config/system_config.yaml; echo "== absence (both must say ABSENT) =="; { [ -e sr_shadow ] && echo "sr_shadow PRESENT" || echo "sr_shadow ABSENT"; }; { [ -e scripts/sr_shadow_evaluate.py ] && echo "evaluator PRESENT" || echo "evaluator ABSENT"; }; echo "== rename preconditions (regular file, links=1, owner ubuntu; RECORD each mode) ==" && stat -c "%n|%F|%a|%U:%G|links=%h" core/config_loader.py signals/signal_processor.py main.py config/expected_managers.yaml config/system_config.yaml; echo "== stray .tmp (nothing listed = clean) =="; ls -l core/config_loader.py.tmp signals/signal_processor.py.tmp main.py.tmp config/expected_managers.yaml.tmp config/system_config.yaml.tmp 2>/dev/null; echo "== cron (count MUST be 0) =="; crontab -l 2>/dev/null | grep -c sr_shadow_evaluate'
```
  ⛔ Any single failure above is a **STOP**. ⚠️ The `crontab -l` count is a `grep -c`, so `0` is the pass value and the command exits non-zero on 0 matches — ⭐ read the printed number, ⛔ not the exit status.

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

  **4a and 4b (new, inert files) — tar, unchanged** (Amendment 8 §2 keeps these on tar: a truncated NEW file destroys nothing, nothing imports them before 4e, and the per-group checksum catches it first). ⚠️ They are ⛔ **NOT** idempotent-reporting — a re-run silently re-extracts. That is safe here and ⛔ nowhere else.

  **4a** — the 12 `sr_shadow/` files. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep archive --format=tar e7bf477 sr_shadow/__init__.py sr_shadow/bars.py sr_shadow/calendar.py sr_shadow/decision.py sr_shadow/evaluator.py sr_shadow/params.py sr_shadow/pipeline.py sr_shadow/pricing.py sr_shadow/runner.py sr_shadow/schema.py sr_shadow/store.py sr_shadow/zones.py | ssh -o BatchMode=yes trading-sbx 'tar -x --no-overwrite-dir -C /home/ubuntu/systems/trading-system'
```
  Verify 4a. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum sr_shadow/__init__.py sr_shadow/bars.py sr_shadow/calendar.py sr_shadow/decision.py sr_shadow/evaluator.py sr_shadow/params.py sr_shadow/pipeline.py sr_shadow/pricing.py sr_shadow/runner.py sr_shadow/schema.py sr_shadow/store.py sr_shadow/zones.py'
```

  **4b** — the evaluator. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep archive --format=tar e7bf477 scripts/sr_shadow_evaluate.py | ssh -o BatchMode=yes trading-sbx 'tar -x --no-overwrite-dir -C /home/ubuntu/systems/trading-system'
```
  Verify 4b. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum scripts/sr_shadow_evaluate.py'
```

  **4c–4f (EXISTING boot-path files): one IDEMPOTENT GUARDED WRITE-THEN-RENAME per file** (Amendment 7 §1 shape; the inline precondition and the three outcomes added by Amendment 8 §2, contract above). The old file stays intact until verified new bytes replace it in one `rename(2)`. ⭐ Each prints exactly one of `WROTE` · `ALREADY_DONE` · `REFUSED_DRIFT` · `REFUSED_WRITE`.

  ⛔ **Run them in this order.** `4e` before `4d` is a TypeError at boot; `4f` is always LAST.

  **4c** — `core/config_loader.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:core/config_loader.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < core/config_loader.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "5b27302483de514ec3117442267609f3" ]; then cat > /dev/null; echo "ALREADY_DONE core/config_loader.py"; exit 0; fi; if [ "$cur" != "a034fc0816582717267bcb1ef70ba5f8" ]; then cat > /dev/null; echo "REFUSED_DRIFT core/config_loader.py have=${cur:-NONE} want=a034fc0816582717267bcb1ef70ba5f8"; exit 1; fi; cat > core/config_loader.py.tmp && [ "$(md5sum < core/config_loader.py.tmp | cut -c1-32)" = "5b27302483de514ec3117442267609f3" ] && chmod --reference=core/config_loader.py core/config_loader.py.tmp && mv -- core/config_loader.py.tmp core/config_loader.py && echo "WROTE core/config_loader.py" || { rm -f -- core/config_loader.py.tmp; echo "REFUSED_WRITE core/config_loader.py"; exit 1; }'
```
  **4d** — `signals/signal_processor.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:signals/signal_processor.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < signals/signal_processor.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "d45cc437815dba5eb876602724fbb52f" ]; then cat > /dev/null; echo "ALREADY_DONE signals/signal_processor.py"; exit 0; fi; if [ "$cur" != "da8c6f983e92f8644656dbe0a081e51d" ]; then cat > /dev/null; echo "REFUSED_DRIFT signals/signal_processor.py have=${cur:-NONE} want=da8c6f983e92f8644656dbe0a081e51d"; exit 1; fi; cat > signals/signal_processor.py.tmp && [ "$(md5sum < signals/signal_processor.py.tmp | cut -c1-32)" = "d45cc437815dba5eb876602724fbb52f" ] && chmod --reference=signals/signal_processor.py signals/signal_processor.py.tmp && mv -- signals/signal_processor.py.tmp signals/signal_processor.py && echo "WROTE signals/signal_processor.py" || { rm -f -- signals/signal_processor.py.tmp; echo "REFUSED_WRITE signals/signal_processor.py"; exit 1; }'
```
  **4e** — `main.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:main.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < main.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "5aacc1b8028682405834b7dd6238ab5a" ]; then cat > /dev/null; echo "ALREADY_DONE main.py"; exit 0; fi; if [ "$cur" != "85219d2285a0b07bc363ebd9e31bac6e" ]; then cat > /dev/null; echo "REFUSED_DRIFT main.py have=${cur:-NONE} want=85219d2285a0b07bc363ebd9e31bac6e"; exit 1; fi; cat > main.py.tmp && [ "$(md5sum < main.py.tmp | cut -c1-32)" = "5aacc1b8028682405834b7dd6238ab5a" ] && chmod --reference=main.py main.py.tmp && mv -- main.py.tmp main.py && echo "WROTE main.py" || { rm -f -- main.py.tmp; echo "REFUSED_WRITE main.py"; exit 1; }'
```
  **4f** — `config/expected_managers.yaml`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:config/expected_managers.yaml | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/expected_managers.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "8625c4b724c34a41f09f06297e3cd797" ]; then cat > /dev/null; echo "ALREADY_DONE config/expected_managers.yaml"; exit 0; fi; if [ "$cur" != "1dad38c53d556db8c8652389f2838d5f" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/expected_managers.yaml have=${cur:-NONE} want=1dad38c53d556db8c8652389f2838d5f"; exit 1; fi; cat > config/expected_managers.yaml.tmp && [ "$(md5sum < config/expected_managers.yaml.tmp | cut -c1-32)" = "8625c4b724c34a41f09f06297e3cd797" ] && chmod --reference=config/expected_managers.yaml config/expected_managers.yaml.tmp && mv -- config/expected_managers.yaml.tmp config/expected_managers.yaml && echo "WROTE config/expected_managers.yaml" || { rm -f -- config/expected_managers.yaml.tmp; echo "REFUSED_WRITE config/expected_managers.yaml"; exit 1; }'
```
  - **After each command** — **`RUNNABLE — LITERAL COMMAND`** *(one file shown; the same three checks for each of `core/config_loader.py`, `signals/signal_processor.py`, `main.py`, `config/expected_managers.yaml`)*:
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum main.py && stat -c %a main.py && ls -l main.py.tmp 2>/dev/null; echo TMP_ABSENT_IF_NOTHING_ABOVE'
```
    md5 = the committed md5 in the table below · `stat -c %a` = the mode Gate 3 recorded · the `.tmp` absent. Else ⛔ STOP → rollback.
  - ⛔ **Why the md5 sits BETWEEN `cat` and `mv`:** 🔬 PC demo (~02:05) shows a stream cut short with a clean EOF makes `cat` exit **0**. `cat > tmp && mv tmp path` alone would therefore rename a PARTIAL file into place. Only the checksum can tell a short stream from a complete one.
  - 🔬 **REHEARSED END-TO-END ON THE PC (~07:27, real blobs, real digests, network removed):** a sandbox seeded with the real `970aabf` bytes ran these four commands ⇒ all four `WROTE`, landing on exactly the four `e7bf477` digests in the table below; an immediate re-run ⇒ all four `ALREADY_DONE` rc 0; no stray `.tmp`. ⭐ **NON-VACUOUS** — the same `4e` command REFUSED twice minutes later: a 90,000-byte truncated `main.py` ⇒ `REFUSED_WRITE`, and the wrong blob ⇒ `REFUSED_WRITE`, with `main.py` left at `85219d22…` both times.
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
- **Source files, preserved outside git** (~02:08) so recovery never depends on the session scratchpad:
  - PRE `D:/Projects/_preservation/TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml` (55,554 bytes);
  - POST `D:/Projects/_preservation/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml` (56,846 bytes).
  - Both were scanned: env-var NAMES only, no secret values; one sandbox alert address.
- **Transfer — IDEMPOTENT GUARDED WRITE-THEN-RENAME** (Amendment 7 §1 replaced the original `cat > config/system_config.yaml`, which 🔬 **truncated the only VM copy BEFORE the first byte arrived** — 0 bytes one second in; Amendment 8 §2 made the precondition three-outcome). The drift precondition is inside the command, so a re-run reports `ALREADY_DONE` instead of an ambiguous `REFUSED`. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/system_config.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "4eab1ae5a9716059431b55a210e917c9" ]; then cat > /dev/null; echo "ALREADY_DONE config/system_config.yaml"; exit 0; fi; if [ "$cur" != "351bd82e73bb0301d850341191c7b72b" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/system_config.yaml have=${cur:-NONE} want=351bd82e73bb0301d850341191c7b72b"; exit 1; fi; cat > config/system_config.yaml.tmp && [ "$(md5sum < config/system_config.yaml.tmp | cut -c1-32)" = "4eab1ae5a9716059431b55a210e917c9" ] && chmod --reference=config/system_config.yaml config/system_config.yaml.tmp && mv -- config/system_config.yaml.tmp config/system_config.yaml && echo "WROTE config/system_config.yaml" || { rm -f -- config/system_config.yaml.tmp; echo "REFUSED_WRITE config/system_config.yaml"; exit 1; }' < D:/Projects/_preservation/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml
```
  - Then the md5 at the destination must be `4eab1ae5…`, the mode must equal Gate 3's, and the `.tmp` must be absent.
  - 🔬 PC demo of this exact shape (~02:05): short stream ⇒ REFUSED, target still `351bd82e`, no `.tmp`; empty stream ⇒ REFUSED, intact; full stream ⇒ `4eab1ae5`, no `.tmp`.
  - 🔬 **RE-REHEARSED ~07:27 with the three-outcome guard, against the real preserved YAML:** `351bd82e…` ⇒ `WROTE` ⇒ `4eab1ae5…`; immediate re-run ⇒ `ALREADY_DONE` rc 0; a deliberately drifted target ⇒ `REFUSED_DRIFT config/system_config.yaml have=b9292e45… want=351bd82e…` rc 1, ⭐ proving the branch is reachable and distinct.
  - 📄 `mv` within one directory is `rename(2)`, atomic on one filesystem (POSIX). The PC demo proves the shell logic, ⛔ not the twin's ext4.
  - The config goes from valid-without-block to valid-with-block in one instant, so Gate 5 never adds an invalid-config moment on top of the Gate 4f cell.
  - ⚠️ If the remote shell is KILLED mid-transfer, the `||` cleanup cannot run: check `config/system_config.yaml.tmp` is absent afterwards; if present, remove it by that literal path and record it (no scratch residue on the VM).
- **Validate ON THE VM** with the deployed loader (read-only; `load_all` and its imports write nothing). ⭐ The payload goes over stdin so there is **no nested quoting** to get wrong. **`RUNNABLE — LITERAL COMMAND`**
```
echo 'from pathlib import Path; from core.config_loader import load_all; c = load_all(Path("config")); print("LOAD_ALL OK sr_shadow.enabled=", c.system.sr_shadow.enabled)' | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && /home/ubuntu/systems/venv/bin/python -B -'
```
  It must print `LOAD_ALL OK sr_shadow.enabled= True`. Then print the block back.

### GATE 6 — CRON (hand-added, testing VM only; ⛔ never the canonical crontab or `cron_registry.yaml`)
Exactly these two lines, appended to the user crontab. Record the installed crontab diff (+2 lines only) and the timestamp. ⚠️ The fence below is the **crontab CONTENT** to add by hand, ⛔ not a shell command — the TEMPLATE/RUNNABLE labels do not apply to it. ⛔ **Never** pipe it to `crontab -` blind: that replaces the WHOLE crontab.
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

- **Rollback mechanism** (~02:09, same guarded write-then-rename as Gates 4c–5, ⛔ never `cat >` straight onto a boot-path file; made IDEMPOTENT ~07:33 per Amendment 8 §2). ⭐ **Run these five in the order given.** Each prints one of `WROTE` · `ALREADY_DONE` · `REFUSED_DRIFT` · `REFUSED_WRITE`; ⭐ an operator re-running because they are unsure how far the rollback got now gets `ALREADY_DONE`, ⛔ not an ambiguous `REFUSED`.
  - **Step 2 — remove the block** (copy back the preserved PRE YAML). **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/system_config.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "351bd82e73bb0301d850341191c7b72b" ]; then cat > /dev/null; echo "ALREADY_DONE config/system_config.yaml"; exit 0; fi; if [ "$cur" != "4eab1ae5a9716059431b55a210e917c9" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/system_config.yaml have=${cur:-NONE} want=4eab1ae5a9716059431b55a210e917c9"; exit 1; fi; cat > config/system_config.yaml.tmp && [ "$(md5sum < config/system_config.yaml.tmp | cut -c1-32)" = "351bd82e73bb0301d850341191c7b72b" ] && chmod --reference=config/system_config.yaml config/system_config.yaml.tmp && mv -- config/system_config.yaml.tmp config/system_config.yaml && echo "WROTE config/system_config.yaml" || { rm -f -- config/system_config.yaml.tmp; echo "REFUSED_WRITE config/system_config.yaml"; exit 1; }' < D:/Projects/_preservation/TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml
```
  - **Step 3.1 — `config/expected_managers.yaml`** — the registry goes FIRST so it never expects an unbuilt manager. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:config/expected_managers.yaml | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/expected_managers.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "1dad38c53d556db8c8652389f2838d5f" ]; then cat > /dev/null; echo "ALREADY_DONE config/expected_managers.yaml"; exit 0; fi; if [ "$cur" != "8625c4b724c34a41f09f06297e3cd797" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/expected_managers.yaml have=${cur:-NONE} want=8625c4b724c34a41f09f06297e3cd797"; exit 1; fi; cat > config/expected_managers.yaml.tmp && [ "$(md5sum < config/expected_managers.yaml.tmp | cut -c1-32)" = "1dad38c53d556db8c8652389f2838d5f" ] && chmod --reference=config/expected_managers.yaml config/expected_managers.yaml.tmp && mv -- config/expected_managers.yaml.tmp config/expected_managers.yaml && echo "WROTE config/expected_managers.yaml" || { rm -f -- config/expected_managers.yaml.tmp; echo "REFUSED_WRITE config/expected_managers.yaml"; exit 1; }'
```
  - **Step 3.2 — `main.py`** — before `signal_processor.py`: new `main.py` + old `signal_processor.py` = TypeError. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:main.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < main.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "85219d2285a0b07bc363ebd9e31bac6e" ]; then cat > /dev/null; echo "ALREADY_DONE main.py"; exit 0; fi; if [ "$cur" != "5aacc1b8028682405834b7dd6238ab5a" ]; then cat > /dev/null; echo "REFUSED_DRIFT main.py have=${cur:-NONE} want=5aacc1b8028682405834b7dd6238ab5a"; exit 1; fi; cat > main.py.tmp && [ "$(md5sum < main.py.tmp | cut -c1-32)" = "85219d2285a0b07bc363ebd9e31bac6e" ] && chmod --reference=main.py main.py.tmp && mv -- main.py.tmp main.py && echo "WROTE main.py" || { rm -f -- main.py.tmp; echo "REFUSED_WRITE main.py"; exit 1; }'
```
  - **Step 3.3 — `signals/signal_processor.py`** — safe here because old `main.py:3575` passes all 36 args BY KEYWORD (R2). **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:signals/signal_processor.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < signals/signal_processor.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "da8c6f983e92f8644656dbe0a081e51d" ]; then cat > /dev/null; echo "ALREADY_DONE signals/signal_processor.py"; exit 0; fi; if [ "$cur" != "d45cc437815dba5eb876602724fbb52f" ]; then cat > /dev/null; echo "REFUSED_DRIFT signals/signal_processor.py have=${cur:-NONE} want=d45cc437815dba5eb876602724fbb52f"; exit 1; fi; cat > signals/signal_processor.py.tmp && [ "$(md5sum < signals/signal_processor.py.tmp | cut -c1-32)" = "da8c6f983e92f8644656dbe0a081e51d" ] && chmod --reference=signals/signal_processor.py signals/signal_processor.py.tmp && mv -- signals/signal_processor.py.tmp signals/signal_processor.py && echo "WROTE signals/signal_processor.py" || { rm -f -- signals/signal_processor.py.tmp; echo "REFUSED_WRITE signals/signal_processor.py"; exit 1; }'
```
  - **Step 3.4 — `core/config_loader.py`** — last; the loader accepts the old YAML. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:core/config_loader.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < core/config_loader.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "a034fc0816582717267bcb1ef70ba5f8" ]; then cat > /dev/null; echo "ALREADY_DONE core/config_loader.py"; exit 0; fi; if [ "$cur" != "5b27302483de514ec3117442267609f3" ]; then cat > /dev/null; echo "REFUSED_DRIFT core/config_loader.py have=${cur:-NONE} want=5b27302483de514ec3117442267609f3"; exit 1; fi; cat > core/config_loader.py.tmp && [ "$(md5sum < core/config_loader.py.tmp | cut -c1-32)" = "a034fc0816582717267bcb1ef70ba5f8" ] && chmod --reference=core/config_loader.py core/config_loader.py.tmp && mv -- core/config_loader.py.tmp core/config_loader.py && echo "WROTE core/config_loader.py" || { rm -f -- core/config_loader.py.tmp; echo "REFUSED_WRITE core/config_loader.py"; exit 1; }'
```
  - After each: md5, mode and `.tmp` absence, exactly as in the deploy.
  - 🔬 **REHEARSED ~07:27 on the PC sandbox, full round trip:** after the deploy rehearsal left all five files at `e7bf477`/`4eab1ae5`, these five commands in this order restored **all five to exactly the `970aabf` / `351bd82e…` digests**; an immediate re-run ⇒ `ALREADY_DONE` rc 0; no stray `.tmp`.
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


---

## AMENDMENT 6 — ONE UNSAFE CELL + PARTIAL WRITES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 6" (16-Sep). It corrects its own §3 connective and fallback (both already recorded ~01:40). The VM is still untouched; `e7bf477` is unchanged.

### §2 — the forward walk, verified against the evidence already gathered
| After | State | Verdict | Evidence |
|---|---|---|---|
| 4a+4b `sr_shadow/`, evaluator | old wiring + inert new files | SAFE | nothing at `970aabf` imports them |
| 4c `config_loader.py` | new loader · blockless YAML · old main/sp/registry | SAFE | matrix row 4 (`enabled: False`); loader diff is +75/−0, additive only |
| 4d `signal_processor.py` | old main × new sp | SAFE | the R2 proof: 0 positional, 36 keywords bind by name, `sr_shadow` → `None` |
| 4e `main.py` | new main/sp/loader · old registry · no block | SAFE (= R1) | `enabled: False` ⇒ `build_sr_shadow` not reached ⇒ nothing built or registered ⇒ the old registry expects nothing |
| 4f `expected_managers.yaml` | new all four · no block | ⚠️ **UNSAFE (= R0)** | registry expects `sr_shadow`, nothing builds it |
| Gate 5 block | new all four + block | SAFE if construction succeeds | built, registered, expected; a construction failure = live CRITICAL (Gate 7/8 grep) |

⇒ **Confirmed: one cell, entered from below by the deploy and from above by the rollback:** NEW registry PRESENT + block ABSENT. No ordering removes it (the alternative lands on `unknown`, `effect_telemetry.py:182`).

### ⛔ But that is not the whole starter requirement: partial files
- 🔬 **Demo** (PC, GNU tar 1.35, ~01:50–01:55): an interrupted stream over an existing `970aabf` `main.py` ⇒ tar rc=2 "Unexpected EOF". The file was replaced by a **147,968-byte `main.py` that compiles but has no `__main__` guard**. The old file does not survive.
  - 💭 As a service it would exit 0 having done nothing ⇒ no restart (`Restart=on-failure`), no watcher retry on a same-day clean exit (📄 05-Aug) ⇒ a **silent** no-trade day.
  - ⚠️ The twin's tar version and behaviour are **not measured**; the demo is the PC's GNU tar.
- **Where partial states occur:** Gates 4c–4e happen BEFORE the registry changes, and every rollback restore writes files, so the card's rule ("from the registry change until the block matches") leaves them uncovered.
- **The operative rule, now in the manifest above both ordered procedures:** from the first write to any boot-path file until every written file verifies at its target md5 AND `load_all` passes on the VM, the service must not start. Deploy and rollback alike. The card's cell is a special case of it.
- For the 17:42 deploy this changes nothing in practice: the window is already after 16:00 and after the same-day clean exit, so no starter can fire (re-checked at Gate 2). It matters for a daytime rollback.

### Optional hardening — PROPOSED, ⛔ NOT ADOPTED without a word
For the four boot-path wiring files and the YAML: write each file only after it has **fully arrived and its md5 verifies**. For example: `git show e7bf477:<path> | ssh trading-sbx "<read all stdin in memory, compare md5 to the manifest value, write the target only on a match>"`.
- It removes the network-truncation class entirely, with no scratch file.
- It does not remove a crash during the local disk write (milliseconds).
- It is not required: the stopped service plus the per-group checksum gate already cover the risk.
- **Standalone manifest, current version (~01:57):** `D:/Projects/_preservation/SR_SHADOW_V1_3_DEPLOY_MANIFEST_16-Sep-2026__preserved_2026-09-16T0156IST.md`, 485 lines, md5 `4102d6cf1cbafd786d0ce9c99747b822`. It supersedes 0145 (kept).


---

## AMENDMENT 7 — GUARDED WRITE-THEN-RENAME, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 7" (16-Sep). The VM is still untouched; `e7bf477` is unchanged.

1. **Confirmed: `cat > config/system_config.yaml` destroys the file first.** 🔬 PC demo (~02:05): with a producer sleeping 2 s, the target was **0 bytes one second in**; the shell's `O_TRUNC` fires before any data.
2. **⛔ Refinement: `cat > <path>.tmp && mv <path>.tmp <path>` alone is NOT enough.** 🔬 PC demo (~02:05): a stream cut to 5,000 bytes and ending in a **clean EOF** makes `cat` exit **0**, so the `&& mv` branch runs and a PARTIAL file is renamed into place.
   - `cat` cannot tell a short stream from a complete one. A remote EOF can arrive before a SIGHUP, for example when the client side ends early.
   - ⇒ **The md5 must gate the rename.**
   - The adopted form, per file: `[pre-md5 check &&] cat > P.tmp && [ md5(P.tmp) = expected ] && chmod --reference=P P.tmp && mv -- P.tmp P || { rm -f -- P.tmp; echo REFUSED; exit 1; }`
   - 🔬 Demo of that exact shape: short ⇒ REFUSED, target intact `351bd82e`, no `.tmp` · empty ⇒ REFUSED, intact · full ⇒ `4eab1ae5`, no `.tmp`.
3. **Two side effects of rename, now gated in Gate 3:**
   - `mv` replaces the directory entry, so it would silently turn a symlink or hard link into a regular file, and the new inode takes the `.tmp`'s mode.
   - ⇒ Gate 3 requires `regular file`, `links=1`, owner `ubuntu`, and records the mode; `chmod --reference` preserves it; the post-check compares it.
   - Gate 3 also requires every `<path>.tmp` to be absent beforehand.
4. **Adopted for Gate 4c–4f as well** (the card's "recommended, take it or leave it"): taken in the lighter per-file form, same directory with no staging directory, for the four EXISTING boot-path files only.
   - `sr_shadow/` and the evaluator stay on `git archive | tar -x` with per-group md5: they are new and inert, since nothing imports them until `main.py` lands after their md5 passes.
   - The rollback restores (the PRE YAML, then the four `970aabf` files) use the same guard.
5. **Durability:** the PRE (`351bd82e…`) and POST (`4eab1ae5…`) YAML copies are now preserved outside git in `D:/Projects/_preservation/…T0208IST.yaml`. Neither recovery nor the Gate 5 source depends on the session scratchpad any more.
6. **"No scratch files on the VM":** each `.tmp` is renamed into the deployed file on success and removed by literal path on refusal. A KILLED remote shell cannot run the cleanup, so the post-check requires the `.tmp` absent; residue is removed by literal path and recorded.
7. **§2 confirmations noted:** the cron line first fires on 17-Sep, not today. A V2RETAIL PASS approves beginning Gate 2 only; it is ⛔ not permission to skip Gates 2–8.

---

## AMENDMENT 8 — IDEMPOTENT GUARDED WRITES + TEMPLATE/RUNNABLE LABELLING, VERBATIM

**Card:** "DEPLOYMENT CARD AMENDMENT 8" (16-Sep), handed over **07:15 IST**, ahead of its own 08:14 slot; applied ~07:21–~07:35 IST. ⛔ The VM is still untouched; `e7bf477` is unchanged, unamended and unpushed.

⚠️ **Time-label correction:** this pass's first draft labelled its own work `~07:35 / ~07:40 / ~07:45 / ~07:55 / 0800`, **ahead of the system clock** — the same class of defect as the 0128 version's. 🔬 Corrected against artifact mtimes: contract demo **07:21** · rehearsal **07:27** · wrapper extracted **07:30**, preserved **07:31** · manifest amended **07:29–07:33** · this copy **07:35**.

1. **§1 closed.** Amendment 7's form is the rule: the md5 must sit BETWEEN `cat` and `mv`, because `cat` cannot tell a short stream from a complete one. Both rename side effects (mode from the `.tmp`; a symlink or hard link silently replaced) stay covered by the Gate 3 preconditions.
2. **§2 ADOPTED — the inline current-md5 precondition goes in EVERY guarded write, and it is IDEMPOTENT.**
   - ⛔ **The trap:** with an inline precondition, a write that has ALREADY SUCCEEDED fails its precondition on a second run — the file is at the TARGET md5, not the EXPECTED-CURRENT one ⇒ `REFUSED`, rc 1, **output identical to genuine drift.** An operator re-running a rollback at 08:10 cannot tell *"already done"* from *"something is wrong."*
   - **The fix — three precondition outcomes, four terminal states:** `md5(P)` = EXPECTED-CURRENT ⇒ proceed (`WROTE`, or `REFUSED_WRITE` rc 1 if the stream is short/empty, target untouched) · = TARGET ⇒ `ALREADY_DONE` rc 0 · anything else, including absent ⇒ `REFUSED_DRIFT` rc 1.
   - **Applied to all four boot-path files in BOTH directions** (Gates 4c–4f and the four rollback restores) **and to Gate 5** (POST copy and PRE copy-back).
   - ⛔ `sr_shadow/` and the evaluator stay on tar, as the card directs. ⚠️ Recorded: they are **NOT** idempotent-reporting — a re-run silently re-extracts.
3. **§3 ADOPTED — TEMPLATE versus RUNNABLE.** Every command carries `RUNNABLE — LITERAL COMMAND` or `TEMPLATE — DO NOT RUN`, with a **mechanical** criterion so the label is checkable: `grep -oE '<[A-Za-z_][A-Za-z0-9_ .-]*>'` over a RUNNABLE command returns nothing.
   - ⭐ **The templates that mattered are now literal.** Gate 4 previously gave ONE example and said *"4d, 4e and 4f are identical in shape"* — i.e. the operator had to CONSTRUCT three boot-path commands by hand at 17:45, the exact shape of the 02:08 incident. All four are now literal, as are 4a (12 paths spelled out), 4b, Gate 5, all five rollback restores, Gate 1's three steps and a new one-paste Gate 3 sweep.
   - Two fences are neither: the Gate 1 wrapper (a **Python source listing**) and the Gate 6 block (**crontab content**). Both are marked as such.

### 🔬 Evidence
- ⭐ **No digest was transcribed by hand**: the runnable commands are emitted by a generator from one verified table, and the markdown is assembled from that generator's output.
- **All 21 digests reproduce** from the refs' blobs (`git show <sha>:<path> | md5sum`): the 17 `e7bf477` files, the 4 `970aabf` wiring files, plus both preserved YAMLs. ⚠️ Confirmed `git show` emits **raw blob bytes despite `core.autocrlf=true`**.
- **Guard contract demo (~07:21, six cases)** and a **full round-trip rehearsal (~07:27)** in a PC sandbox seeded with the real `970aabf`/`351bd82e…` bytes: deploy ⇒ all five at the committed `e7bf477`/`4eab1ae5…` digests; re-run ⇒ all `ALREADY_DONE` rc 0; rollback in the mandated order ⇒ all five back to `970aabf`/`351bd82e…`; re-run ⇒ `ALREADY_DONE`. No stray `.tmp` at any point.
- ⭐ **NON-VACUOUS** — the same commands went RED three times: truncated `main.py` ⇒ `REFUSED_WRITE`; wrong blob ⇒ `REFUSED_WRITE` (left at `85219d22…` both times); drifted YAML ⇒ `REFUSED_DRIFT have=b9292e45…`.
- **All 20 RUNNABLE commands parse under `bash -n`** (parse only, nothing executed), and the Gate 3 sweep was run against the sandbox and produced every expected field.
- ⚠️🔬 ⛔ **ONE CHECK WAS VACUOUS AND IS REPORTED AS SUCH: mode preservation.** Windows did not honour `chmod 600` on the fixture (`stat -c %a` read 644 before and after) ⇒ `chmod --reference` could not have been observed failing. ⭐ The protection is the **VM-side `stat -c %a` after every write**. Limit inherited from Amendment 7.

### 🔴 FINDING — §2's larger claim does not hold as written
> §2: *"It makes the whole transfer sequence re-runnable from the top … That is exactly the gap in the resume rule … This closes it."*

- ✅ **True at FILE level** (demonstrated, both directions).
- 🔴 ⛔ **NOT true at SEQUENCE level.** Gate 3's preconditions are *absence* and *pre-state* checks that a partial run has already falsified, so a second pass STOPS at Gate 3 and never reaches the idempotent writes: `sr_shadow/` must not exist (4a/4b landed it) · the 4 wiring md5s must equal `970aabf` (4c–4f landed) · the YAML must be `351bd82e…` (Gate 5 landed) · the crontab must not contain `sr_shadow_evaluate` (Gate 6 landed). ⭐ **It is the same two-outcome trap, surviving one gate earlier.**
- ⏸ **OWED — ⛔ NOT FIXED, deliberately.** Widening Gate 3 changes the deploy procedure's STOP conditions, which Amendment 8 does not authorise (*"No rebuild. No redesign."*). Until a decision: **a resumed run that trips Gate 3 STOPS and reports** — the safe direction, already what the gate does ⇒ the limit costs a **stall**, ⛔ never a bad write.

---

## 16-Sep-2026 (Wed) 08:26 IST — `RESULT-SR-SHADOW-V13-GATE1-V2RETAIL-16SEP2026` — ✅ **GATE 1 PASS** · ADJUDICATED FROM THE ROWS, ⛔ NOT THE HEADLINE · THE VM IS STILL UNCHANGED

**Authority:** 👤 Rama's 16-Sep ~00:20 delegated answer, §6 item 1. **Timing:** the in-session 08:25 timer fired; preconditions 08:25–08:26; the single run at **08:26:08–08:26:10 IST**, after the **08:15:01** token.

### Preconditions — both PASS
| Check | Required | 🔬 Measured | |
|---|---|---|---|
| `md5sum scripts/sr_corp_action_spotcheck.py` | `d954c1781e55ebf68d44c9c815ef353e` | `d954c1781e55ebf68d44c9c815ef353e` | ✅ exact |
| `data_store/session/zerodha_token.json` mtime | today | `2026-09-16 08:15:01.388324184 +0530` (257 B) | ✅ fresh, metadata only |
| wrapper identity (PC side) | `dc9476f3e43bbe64b161ed151e973a56` | same, checked before the run | ✅ |

### The run
- **ONE** read-only run, exactly the manifest's Gate 1 step 3 literal command. ⭐ **rc 0, stdout 2,711 B, stderr 0 B, and nothing was written on the VM.**
- **Broker calls, as counted by the wrapper: `instruments=1 historical_data=1`** — ⭐ recorded, ⛔ not repeated.
- **Evidence preserved outside git:** `D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stdout.txt` and `….stderr.txt` (0 B).
- **Instrument:** token **`3780097`**, exchange_token `14766`, `NSE`/`EQ`, name `V2 RETAIL`, lot 1, tick 0.01. ⚠️ **No ISIN field** — the Zerodha instruments dump does not carry one, so the manifest's *"ISIN if present"* resolves to **absent**, ⛔ not missed.
- **Request:** `from_date 2026-03-05` → `to_date 2026-04-14`, `interval day`. **Rows 25 · first session `2026-03-05` · last `2026-04-13` · duplicates 0.**
- **Counts: 14 sessions BEFORE 2026-03-25 · 11 ON/AFTER.**

### ✅ ADJUDICATION = **PASS**, on three independent grounds
1. **Both sides of the ex-date are present** — 14 before, 11 on/after. ⛔ This is **not** a post-split-only series.
2. **No ~10:1 discontinuity.** Last pre `2026-03-24` close **192.70** → first post `2026-03-25` open **195.00**, close **196.30**: close→close ratio **1.0187**. An UNADJUSTED 10:1 series would read **~0.10** here. 🔬 Across the **whole** 25-session window the extreme overnight close ratios are **max 1.0542 / min 0.9561** — nothing anywhere approaches a split break.
3. ⭐ **An independent arithmetic fingerprint, computed from the rows and owing nothing to the script:** **14/14** pre-ex-date rows have all four prices landing on whole rupees when multiplied by 10, and **14/14** have volume divisible by 10; post-ex-date only **3/11** and **1/11**. ⇒ the pre-history is (original prices ÷ 10) and (original volume × 10) — **the 10:1 split has ALREADY been applied to it.**

### ⛔ The known defect was checked, not assumed away
📄 The script's `VERDICT: ADJUSTED (continuous) — ✅` headline **can be false**: its failure mode is a window of **post-only candles**, where continuity is trivial (SYSTEM_MAP ~01:05). ⚠️ This window returned **exactly 11 post-ex-date rows**, the same count as in that defect note — but it **also** returned **14 pre-ex-date rows**, so the window spans the ex-date and the continuity is real. ⭐ **The headline was not used; grounds 1–3 above stand without it.**

### What this authorises — and what it does not
- ✅ **A PASS authorises BEGINNING Gate 2** (starter inventory, ~17:36, after the 17:35 self-exit).
- ⛔ **It does NOT skip Gates 2–8**, and it is ⛔ **not** authority to copy anything. The VM remains untouched; `e7bf477` remains unpushed.
