# TRANSCRIPT — FILE 116 (03-Sep-2026, 13:25 IST)

🔴 **PROVENANCE: this is a TRANSCRIPT of the FILE 116 text as received in the
session, ⛔ NOT a copy of `RAMA_03-Sep-2026_FILE-116_SCOPE-FLAG.txt`** — that
file does not exist on this machine (see `README_PROVENANCE.md`). ⛔ Do not cite
this as the original artifact.

---

```
================================================================================
FILE 116 — ⭐ VERY SHORT · 🔴 DO NOT EDIT THE FILE TO SET THE SCOPE
================================================================================
ISSUED            : 03-Sep-2026 (Thu) 13:25 IST
MODEL REQUIRED    : Claude Opus 4.6+ · REASONING: HIGH
STATE             : ✅ ⭐ **STEP B PASSED** — ⭐ PID **1119981**, ⭐ start Thu 03-Sep
                    **13:08:20**, ⭐ NRestarts 0, ⭐ active. ⭐ Engine untouched at
                    1101999 / 08:15:29.

🔬 ⭐ **Hash verified independently:**
`743a7d461f8a171e228fd8d9d2ffce1fe0c59642f8408569ad3ff80fb10bec93` ⭐ — matches.
🔬 ⭐ Route table read directly: ⭐ **21** routes. 🔬 ⭐ `S02_EXPECT = { h: 1212,
ovf: false, sub13: 0 }` ⭐ — correct.

================================================================================
1 — 🔴 THE SCOPE FLAG · ⭐ EDITING LINE 53 WOULD BREAK THE HASH
================================================================================
🔬 ⭐ Line 53 reads ⭐ `const STOP_AFTER_C2 = CFG.STOP_AFTER_C2 ?? false;`
⇒ ⚠️ ⭐ **The default is `false` — ⭐ the FULL ~3-minute sweep.** ⭐ Pasting the file
as-is gives 👤 Rama the long run, ⛔ not the short one both of us recommended.

⚠️ ⭐ And the instruction *"change one line at the top of the file"* has a trap in
it: ⇒ 🔴 ⭐ **editing line 53 changes the file, ⭐ so it no longer matches the
`SHA256SUMS.txt` hash he was just told to verify.** ⭐ The verification and the
edit contradict each other.

 ⇒ ⭐ **Do it through the CFG hook instead — ⭐ the file stays byte-identical:**
   ⭐ **Paste this line FIRST, on its own, then paste the file unchanged:**
   ```
   window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true };
   ```
   🔬 ⭐ `CFG.STOP_AFTER_C2 ?? false` reads it, ⭐ so `true` wins. ⭐ Verified hash
   preserved, ⭐ short scope selected, ⛔ nothing edited.
 ⭐ For the full run: ⭐ paste the file alone, ⛔ no CFG line. ⭐ The default is
   already `false`.

================================================================================
2 — ⭐ TWO RECORD CORRECTIONS BEFORE THE EVIDENCE IS FINALISED
================================================================================
 ⭐ **`RUN_HEADER` §B carries the OLD verdict vocabulary.** ⭐ It still lists
   ⭐ `COMPARABLE / SCROLLBAR-PLAUSIBLE / UNEXPLAINED`. ⚠️ ⭐ The Round-3 instrument
   no longer emits `SCROLLBAR-PLAUSIBLE` — ⭐ it emits **`HEIGHT ONLY`** /
   **`MORE THAN THE HEIGHT MOVED`** with the magnitudes printed. ⇒ ⭐ Update the
   header, ⛔ or the evidence record contradicts the instrument that produced it.
 ⭐ **`RUN_HEADER` §D says Tier 2 covers 22 screens.** 🔬 ⭐ The instrument carries
   **21** routes. ⇒ ⭐ Reconcile it. ⚠️ ⭐ And keep the two facts apart: ⭐ the
   *historical campaign* covered **22 screens** (⭐ S01 has no table); ⭐ *this
   sweep* covers **21 routes**. ⛔ Do not silently merge them.

================================================================================
3 — ⭐ THE RUN
================================================================================
1  sha256sum -c SHA256SUMS.txt        → must read 743a7d46…
2  log in to the dashboard, land on any dashboard page (its OWN origin)
3  DevTools → Console:
      window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true };     ← short scope
      then paste gui_sweep_snippet.js UNCHANGED
4  KEEP THE TAB FOCUSED until it prints END
5  copy the whole output back (also in window.__GUI_SWEEP)

 ⭐ **Expect and do not misread:** ⭐ **S14 overflow PRESENT = PASS.** ⭐ And S02 may
   deviate — ⭐ the run prints Δh beside the scrollbar width and their ratio, ⭐ and
   halts by design rather than guessing.
 ⭐ **If C2 is clean, the record reads exactly:** ⭐ *"Live deployment verification
   completed at C2; S02 and S17 verified; Tier-2/Tier-3 sweep not measured."*
   ⛔ Never *"sweep complete"* · ⛔ never *"22-screen GUI verified"* · ⛔ never
   *"all 21 table screens visually verified."*
 ⭐ Then: ⭐ record → ⭐ report to 👤 Rama → ⭐ **separate** TREE advance
   `39292d3 → 2d08436` → ⭐ STOP.

⭐ **The decisive fact is already on the record and it is worth keeping:**
🔬 ⭐ `controls.py` and `control_client.py` carry mtime **02-Sep 23:39:55**;
🔬 ⭐ the process started **03-Sep 13:08:20** — ⭐ 13 h 28 m later. ⇒ ⭐ By CPython
import semantics this process holds the deployed modules, ⭐ including the two
that did not exist at `39292d3`. ⭐ And the Jinja cache is empty, ⭐ so every render
is a first render off the deployed tree.

⛔ verifying a hash then editing the file ≠ verification · ⛔ a default ≠ the
recommended scope · ⛔ 21 routes ≠ 22 screens · ⛔ a header's vocabulary ≠ the
instrument's.

================================================================================
END OF FILE 116
================================================================================
```

---

## ⚠️ Superseded within FILE 116 itself, by 👤 FILE 118
- ⭐ §3 step 1 *"must read 743a7d46…"* → 👤 **FILE 118 §1.4 corrects the output
  shape:** `sha256sum -c` prints **one `: OK` line per file**; ⭐ three OK lines
  is the pass condition. ⛔ The bare hash string is not what appears.
- ⭐ §3 *"S14 overflow PRESENT = PASS"* → 👤 **FILE 118 §1.3 WITHDRAWS S14 from
  the C0–C2 scope.** ⭐ It is a TIER-1 control of the **full** sweep, ⛔ not a
  criterion of this run, and ⛔ its absence is not a failure.
