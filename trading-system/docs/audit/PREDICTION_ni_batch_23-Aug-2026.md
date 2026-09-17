# FROZEN PREDICTION — THE TEN NI ITEMS

**Written 23-Aug-2026 BEFORE any change.** Base **`742d9da`** (deployed), branch
`fix/ni-batch-23aug`. Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
👤 Authorising quote, Rama: *"Now complete pending!!"*

> ⛔ Nothing below may be edited after the batch starts. A wrong prediction is recorded as
> wrong, ⛔ never corrected retroactively.

⚠️ **There is no NI-10.** Ten rows: 9 · 11 · 12 · 13 · 14 · 15 · 16 · 17 · 18 · 19.

---

## P-A · THE SEVEN THAT SHOULD CLOSE

| item | predicted change | 🔴 FALSIFIER |
|---|---|---|
| **NI-13** | docstring text only in `tests/unit/test_position_sizer_delivery_contract.py` | any executable line changes ⇒ STOP |
| **NI-12** | comments only, ≥2 sites (`cnc_gtt_monitor.py:26`, `t2_cnc_gtt_realtest.py:5`). ⭐ I predict the **sweep finds MORE than the two named** — NI-3's card said 3 and found 6 | a sweep that finds exactly 2 means my sweep is too narrow, ⛔ not that only 2 exist |
| **NI-18** | change what `constraint` **reports**, ⛔ never the qty. `breakdown` already carries the rungs | `final_qty` changes for ANY input ⇒ STOP, that is a money-path change |
| **NI-17** | 🔬 measure first whether the cap could **ever** bind at today's config. I predict **it cannot** (`max_single_order_qty=10000` vs rungs in the tens) ⇒ moving it is latent-only | if it CAN bind today, moving it is a live behaviour change ⇒ STOP and put it in §3 |
| **NI-9** | remove the `= 3` / `= 5` defaults in `risk_engine.py:160-161`; 2 test files need the caps passed | a third production file needs editing ⇒ STOP |
| **NI-11** | add a delivery arm to C2 in `config_auditor.py`, mirroring NI-2 | the existing C2 test goes red ⇒ I broke the intraday arm |
| **NI-19** | ⭐ I predict the correct answer is **RECORDED, NO CODE** — creating 5 delivery keys with no consumer is the defect class this campaign keeps finding | if a consumer already exists for any of the five, my premise is wrong |

## P-B · THE THREE THAT NEED SOMETHING FIRST

- **NI-14** — measurement only. I predict the `400` threshold has **no documented
  derivation**. **FALSIFIER:** a comment/commit stating why 400.
- **NI-15** — contract measurement only. I predict `_default_watched_files()` handles
  **regular files only** (`sha256_file` on an explicit path) and would **not** see a NEW
  drop-in. **FALSIFIER:** it recurses or accepts a directory ⇒ adding it is safe and the
  gap is smaller than recorded.
- **NI-16** — ⛔ cannot be built. Will end **BLOCKED ON F2**. **FALSIFIER:** none —
  ⛔ if I find myself editing `max_multiplier` or porting `min(1.0, …)`, I have violated
  the card.

## P-C · PROCESS

- **One commit per item**, named `BUG-NI<n>`, independently reversible.
  **FALSIFIER:** any commit containing two items.
- **No item's diff reaches beyond its own file(s) + its tests.**
  **FALSIFIER:** it does ⇒ STOP that item, report, move on (NI-5's rule).
- **Gate:** full differential, `PYTHON=/c/python311/python` set.
  I predict base = **7F / 5,751P / 4S**, ⛔ not 10F — the `PYTHON` var is the difference.
  **FALSIFIER:** base ≠ 7F ⇒ the harness is wrong, ⛔ not the code.
- **Head:** the same 7 failures, ⛔ zero base-green tests going red.

## P-D · 🔴 A COLLISION I HAVE ALREADY MEASURED, RECORDED BEFORE IT BITES

🔬 NI-5 (`a4a5cef`) touches **`capital/position_sizer.py`** and
**`core/config_auditor.py`**. This batch touches **both** (NI-17/NI-18 → the sizer,
NI-11 → the auditor). Both branches are children of `742d9da`.
⇒ 🔴 **A merge conflict between NI-5 and this batch is CERTAIN, not possible.**
⭐ Predicted resolution: they must be **stacked**, ⛔ not merged in parallel.
👤 Which goes first is Rama's — it belongs in the §3 decision block.

## P-E · WHAT MUST NOT HAPPEN

⛔ No F2 · no allocation model · no cherry-pick from `65b7196` · no schema migration ·
no `max_multiplier` change · no MIS ×3.5 · no strategy YAML · no GUI · no invented NI-14
threshold · no directory added to the watch list before its contract is proven · no
delivery key without a consumer · no `token_watcher.sh` or service-file change ·
no `--baseline` · ⛔ no push without Rama naming the refspec.
