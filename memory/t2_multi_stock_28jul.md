---
name: t2-multi-stock-28jul
description: "T2 went from 1 position to 3-5 stocks (Rama, 28-Jul). NOTHING BLOCKED, no code change needed. T2 isolation VERIFIED FROM SOURCE. Voids are PER-POSITION so N stocks nearly eliminate void risk — but RAMA'S MINUTES become the binding constraint instead. YESBANK+NHPC must be dropped: 10% circuit band vs a +/-10% GTT."
metadata: 
  node_type: memory
  type: project
  originSessionId: 58e849b5-81c5-4b96-89bc-182326b7fbbc
  modified: 2026-07-28T17:52:31.030Z
---

# T2 MULTI-STOCK — the facts that decide the arm

**Full report: `docs/audit/t2_multi_stock_blockers_28jul2026.md` (`2825cef`).**
**Command card: `Downloads/WED_29-JUL_T2_ARM_COMMANDS.txt`.**

## ✅ RAMA'S FINAL DECISIONS (28-Jul 23:40) — settled, not options
**5 stocks × 3 shares, arm 11:31: IOB · TRIDENT · SOUTHBANK · MSUMI · SJVN.**
⛔ YESBANK + NHPC excluded (10% circuit band). ⛔ Band, qty and basket are CLOSED.
If the automated buy fails he buys manually and the test continues — **the objective is
the CNC lifecycle, not the entry.**

## 🔴🔇 THE OPERATIONAL TRAP FOUND 28-Jul NIGHT — **THE SCRIPT PRINTS ALMOST NOTHING**
**VERIFIED from source + by running it:** `t2_cnc_gtt_realtest.py` calls `get_logger()`
but **never `setup_logging()`**, and `core/logger.py:270` states *"Handlers are NOT
attached here; call setup_logging() at startup first."*
⇒ **Every `log.info` AND `log.critical` in the run goes NOWHERE — not to stdout, not to
`logs/system_<date>.log`.** A real run prints **ONE line** (`=== T2 real-API proof: X x3
… ===`) and exits.
⛔ **SO: the GTT_ID is NEVER shown, and a failed-square `log.critical` would be SILENT.**
⭐ **The exit code is the only signal** (0 = armed+verified · 1 = held but unverified).
⇒ **Take GTT_IDs from Kite → Orders → GTT** — which is also the broker-side proof the
runbook demands ("placing is not existing"). ⚠️ NOT a blocker: §3's by-hand Kite check was
always the authority. ⛔ **But do not promise anyone they will see "ARMED" on screen.**

## 🐚 SHELL TRAP — **GIT BASH, NOT POWERSHELL** (MEASURED twice, 28-Jul)
**PowerShell silently STRIPS the inner quotes** of an `ssh host "... \"...\" ..."`
command; the remote bash then dies on unbalanced quotes or python gets a mangled string.
✅ The `ssh host '…; echo EXIT=$?'` form (outer SINGLE quotes, **no** inner quotes) works
in BOTH. ⇒ any operator command with nested quotes must be labelled **Git Bash only**.

## ✅ VERIFIED BY RUNNING IT, 28-Jul night (nothing placed)
- `--symbol X --qty 3` flows end-to-end: a `--dry-run` wrote `gtt_state` **qty=3**,
  status CANCELLED after cleanup, in its **own** `data_store/t2_proof_<ts>/` with its
  **own** `analytics.db` ⇒ **the isolation guard works.**
- Step-zero hash on the VM copy = `0a3c505c…` ✅ · schema **45** ✅ · all 5 preconditions
  and the GTT lister run clean in Git Bash.
- ⚠️ My dry-runs left 3 throwaway dirs `data_store/t2_proof_20260728_2315*` — **harmless
  and deliberately NOT deleted** (freeze). 10-Jul ones have sat there since.

## Thursday close = 5 runs, `--symbol X --qty 3 --close-overnight <GTT_ID>`
Each needs **symbol AND its own GTT_ID** — ~15 min total, fits 09:15–11:00. Card §G.

## ✅ NOTHING BLOCKED — and both "capital" instructions need NO change
- ⭐ **T2 IS ISOLATED, VERIFIED FROM SOURCE** (`scripts/t2_cnc_gtt_realtest.py`): own
  throwaway DB in its **own subdir** (`_throwaway_store_path`), guarded by
  `_assert_isolated()` which **SystemExits** on a live path — the subdir matters because
  `StateStore` ATTACHes an `analytics.db` *beside* the main DB. ⭐⭐ **NO `FundManager`
  import, no bucket read, no `fm_ledger` write anywhere in the file**; orders go straight
  to `adapter.place_order()`. ⇒ **the 70/30 split is IRRELEVANT to the arm.**
  ⚠️ The **broker ACCOUNT is shared** — that is the one thing not isolated (cash only).
- ✅ **70/30 is ALREADY the deployed config** — `system_config.yaml:136-137`
  (`intraday_bucket_pct: 0.70` / `positional_bucket_pct: 0.30`). Nothing to change.
- ✅ **THERE IS NO RUPEE CAPITAL VALUE IN CONFIG** — every capital key is a *percentage*;
  the amount seeds from **`broker.net`** at the 08:15 INIT (`fund_manager.py:433`, and
  `:1726`/`:1810` state seed == broker.net by construction). ⇒ **"₹10,000" is a BALANCE,
  not a setting.** ⛔ Do not "set" capital anywhere.
- ✅ **`--qty` already exists** ⇒ ">3 shares" needs no modification. **Run it N times:**
  each run mints a **fresh timestamped throwaway DB**, so ⛔ **run 2 cannot overwrite run
  1's evidence.** The step-zero hash is unaffected — running a file does not change it.

## ⭐⭐ THE CONSTRAINT SWAPPED — this is the decision
**Voids are PER-POSITION** (each run = own DB, own GTT, own broker position), and the
question ("does an overnight CNC sell need TPIN?") is answered by **any one survivor**.
⇒ the metric is **P(ALL void)**, not P(≥1 voids):

| arm | N=3 | N=5 |
|---|---|---|
| 13:00 | 0.004% | ~0% |
| 10:30 | 0.12% | 0.001% |

⇒ **VOID RISK STOPS MATTERING; arming at 10:30 becomes nearly free.**
🔴 **BUT N positions = N by-hand §3 checks ⇒ RAMA-MINUTES bind instead:**
**N=1 ~24 min · N=3 ~32 min · N=5 ~40 min** against a 30-min 10:30–11:00 window
⇒ **N=5 DOES NOT FIT IT.** ⛔ Estimates decomposed from the runbook's own ~30-min P6
budget for N=1 — **not measurements, and deliberately not shaved to fit a schedule.**

## 🔴 DROP YESBANK AND NHPC — 10% CIRCUIT BAND vs a ±10% GTT
MEASURED live via `kite.quote()`: **YESBANK** ltp 22.81, circuit **20.53–25.09**;
**NHPC** 78.28, circuit **70.46–86.10** — a 10% band, so **both GTT legs land AT/OUTSIDE
the circuit.** ⭐ **This is exactly the "GTT REJECTED at placement" case runbook §8 names
as unreadable from source — the CIRCUIT LIMIT is readable and answers it.**
The other five (IOB · TRIDENT · SOUTHBANK · MSUMI · SJVN) are **20% band, legs inside.**
⇒ proposed basket **IOB · TRIDENT · SOUTHBANK · MSUMI · SJVN @ qty 4 = ₹859.68**,
worst case ~₹86. Keeps 4 of his 5 preferred.
⚠️ **Circuit LEVELS reset daily off the previous close; the 10%-vs-20% BAND WIDTH is the
scrip property that matters.**

## ⚠️ THE ~2.8% VOID FIGURE DOES NOT APPLY TO THIS BASKET
⛔ **All seven candidates have ZERO candles in `analytics.db`.** Re-derived for the same
PRICE BAND instead (read-only): **under ₹150 → 3.53% @13:00 · 10.59% @10:30**, on
**85 symbol-days / 53 symbols — THIN** (one more void moves it 1.2pp), and on a
*different population* (momentum breakout candidates). ✅ The all-symbol @13:00 figure
(2.36%) and the under-₹150 @11:30 figure (9.41%) corroborate the inherited 2.8%/9.0%.
⛔ **SUB-₹50 IS UNDERIVABLE — our whole dataset holds ONE symbol under ₹50, while five of
seven candidates are.** Do not quote a sub-₹50 number.

## Other verified facts
- ✅ **All seven in `config/instruments.csv`**, tokens match the broker exactly.
  ⚠️ **"South Indian Bank" = `SOUTHBANK`** — `SOUTHINDBANK` does not exist.
- ✅ **None on the F&O ban list** (`fno_ban` table).
- ⛔ **ASM/GSM is NOT exposed by the Kite API** — visible only on the scrip's Kite page.
  **The one item only Rama can close.** A T2T/100%-margin scrip changes the test's meaning.
- ✅ **C6 margin: NOT material.** ₹860 CNC ⇒ ~₹602 off a ~₹6,900 intraday bucket whose
  **peak use today was ₹664 (9.6%)**. The binding constraints are `max_open_positions: 5`
  and the concentration cap, never cash.
- ✅ Thursday = N closes, ~10–15 min for N=5 — fits 09:15–11:00 easily (§7 sets no clock).
- ⚠️ **Per-scrip DP charge (~₹15–16) on each SELL ⇒ N=5 ≈ ₹75–80, not ₹15.**
- ⚠️ Runbook §2 prints ONE `GTT_ID` blank; N runs need **N symbol+id PAIRS**.
- ⚠️ Cosmetic only: the throwaway DB's seeded rows hardcode `symbol='IDEA'` and
  `qty_planned=1`; the store assertion checks gtt_id/status/qty, **not symbol** ⇒ a
  YESBANK run writes an "IDEA" parent row. Harmless, but confusing to a later reader.

[[slice25-execution-plan-27jul]] [[feedback-verify-the-finding-premise]] [[feedback-no-fixed-test-baseline]]
