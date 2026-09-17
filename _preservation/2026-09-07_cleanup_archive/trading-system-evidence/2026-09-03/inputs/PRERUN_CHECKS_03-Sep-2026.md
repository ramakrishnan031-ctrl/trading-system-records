# PRE-RUN CHECKS — 03-Sep-2026 (👤 FILE 118 §2)

⭐ Kept **outside** the three manifest-listed files, as §2.1 requires.
⭐ All values below are 🔬 **verbatim command output**, ⛔ nothing inferred.

## §2.1 — manifest verify (read-only)
```
$ cd D:\Projects\trading-system-evidence\2026-09-03
$ sha256sum -c SHA256SUMS.txt
gui_sweep_snippet.js: OK
INSTRUMENT_VALIDATION_03-Sep-2026.md: OK
RUN_HEADER_03-Sep-2026.md: OK
rc=0
```
⭐ **THREE OK lines** — the §1.4 pass condition. ⛔ No FAILED line.

⭐ Independent recomputation of the edited artifact:
```
$ sha256sum RUN_HEADER_03-Sep-2026.md
91f3924932d4619d9acabab338dfdfd0aa58ba10b19cca4b25b423fdad784551
```
🔬 **MATCHES** 👤 FILE 118 §1.1's independently computed value ⇒ ⭐ the manifest was
regenerated **after** the corrections and is current.

⭐ Re-verified **again** after the `inputs/` writes (below) — ⭐ still 3× OK,
⭐ confirming the freeze held: ⛔ nothing manifest-listed was touched.

## §2.2 — 🔴 COULD NOT BE EXECUTED AS WRITTEN
🔬 **MEASURED: none of the three named `.txt` files exists on this machine.**
Searched `D:\Projects`, `C:\Users\rama\{Downloads,Desktop,Documents,OneDrive}`
by exact name, by `RAMA_*` / `Reply_to_*` / `*SCOPE-FLAG*` / `*PRE-RUN*`, and by
every `*.txt` modified since 01-Sep. ⭐ Only hits belong to a different project
(`mcx_data_storage`).
⇒ ⛔ A copy was impossible. ⭐ **Transcripts** filed instead, each carrying a
provenance header. 📄 `README_PROVENANCE.md`.
⏸ 👤 **OWED:** file the three originals here.

## §2.3 — covering note written, ⚠️ with a gap named
📄 `FILE117_COVERING_NOTE.md`. 🔴 ⛔ **FILE 117 itself is ABSENT and was never read
by me** — the note is sourced only from 👤 FILE 118 §1.2's two quotations.
⭐ Independent corroboration that does **not** depend on FILE 117: 🔬 this
session's own test **G3** measured the short-scope path stopping after S17
(📄 `INSTRUMENT_VALIDATION`, Round 3 §3).

## §2.4 — liveness, immediately before handover (read-only, ⛔ no sudo)
```
measured 2026-09-03 13:50:42 IST
--- gui-dashboard ---
MainPID=1119981
NRestarts=0
ExecMainStartTimestamp=Thu 2026-09-03 13:08:20 IST
ActiveState=active
--- trading-system ---
MainPID=1101999
NRestarts=0
ExecMainStartTimestamp=Thu 2026-09-03 08:15:29 IST
ActiveState=active
```
| gate | required | 🔬 measured | |
|---|---|---|---|
| gui-dashboard MainPID | 1119981 | **1119981** | ✅ |
| gui-dashboard NRestarts · state | 0 · active | **0 · active** | ✅ |
| trading-system MainPID | 1101999 | **1101999** | ✅ |
| trading-system NRestarts · state | 0 · active | **0 · active** | ✅ |

⇒ ⭐ **The STEP B binding holds.** ⭐ PID was confirmed **first**; the snippet is
handed over **second**. ⛔ The engine was not touched.

---

## 🔴 §3.1 (👤 FILE 120) — SECOND, FRESH liveness read
⭐ Required because the 13:50:42 reading, though 👤 ruled **not** back-dated
(FILE 120 §2), ⭐ was **getting older** — ⭐ a full review round elapsed after it.
⚠️ ⭐ The binding is re-established by **re-measuring**, ⛔ never by arguing about a
timestamp. ⛔ The 13:50:42 block above is **kept**, so the gap stays visible.

```
measured 2026-09-03 14:05:37 IST
--- gui-dashboard ---
MainPID=1119981
NRestarts=0
ExecMainStartTimestamp=Thu 2026-09-03 13:08:20 IST
ActiveState=active
--- trading-system ---
MainPID=1101999
NRestarts=0
ExecMainStartTimestamp=Thu 2026-09-03 08:15:29 IST
ActiveState=active
```
| gate | required | 🔬 measured 14:05:37 | |
|---|---|---|---|
| gui-dashboard MainPID | 1119981 | **1119981** | ✅ |
| gui-dashboard start | 03-Sep 13:08:20 | **13:08:20** | ✅ |
| gui-dashboard NRestarts · state | 0 · active | **0 · active** | ✅ |
| trading-system MainPID | 1101999 | **1101999** | ✅ |
| trading-system start | 03-Sep 08:15:29 | **08:15:29** | ✅ |
| trading-system NRestarts · state | 0 · active | **0 · active** | ✅ |

⭐ **Elapsed between the two liveness reads: 13:50:42 → 14:05:37 = 14 m 55 s.**
⭐ Both readings identical in every field ⇒ ⛔ nothing restarted in between.
🔬 Manifest re-verified at the same moment: **3× OK, rc=0** ⇒ ⭐ the freeze held
through all `inputs/` writes; ⛔ nothing manifest-listed was touched.

⏸ ⭐ **If anything intervenes between this read and 👤 Rama's paste, this block is
run again** (👤 FILE 120 §5.3). ⭐ Re-measuring is cheap; ⛔ a broken binding is
unrecoverable.
⭐ The post-run results record must carry **this timestamp beside the run's own
start time, with the interval stated plainly** and ⛔ no invented tolerance
(👤 FILE 120 §3.2).
