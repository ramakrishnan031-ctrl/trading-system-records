# F6 — PIPELINE LIFECYCLE ARCHITECTURE · MEASUREMENT RESULT

**25-Aug-2026, IST.** 🔴 MEASUREMENT ONLY. ⛔ No code · no design · no push · no service action.
**Provenance:** 🔬 measured · 📄 source-derived · 💭 inference · 👤 Rama.

⚠️ **M3 — every line number below holds ONLY at the SHA it was measured at:**
🔬 deployed HEAD **`195436bb6323c981d68f313ad7c39858cc0a4653`**, deployed-tree drift **0 files**
(re-measured this session). ⛔ Do not quote these line cites against any other tree.

⛔ §0 is NOT re-confirmed. `count_active_positions()` is product-blind — taken as closed, and used
below only as a *consequence*, never re-derived.

---

## A · Does `trading-system.service` run BOTH MIS and GTT execution?

🏷️ **PROVEN. ONE PROCESS, BOTH PIPELINES.**

📄 `/etc/systemd/system/trading-system.service`: `Type=simple`, a **single** `ExecStart`
(`venv/bin/python main.py --mode live`), `KillSignal=SIGINT`, `Restart=on-failure`,
`RestartPreventExitStatus=3 4 5`. ⇒ ⛔ There is no second unit and no second process.

🔬 Both pipelines are **threads/components inside that one `main.py`**:

| owner | component | file:line |
|---|---|---|
| **MIS** | `signal_processor.start()` · `entry_gate.start()` · `smart_tgt.start()` · `tgt_retry_manager.start()` | `main.py:3541` · `:3542` · `:3543` · `:3544` |
| **MIS** | `order_monitor.start()` | `main.py:3527` |
| **DELIVERY/GTT** | `CncGttPlacer(...)` + `hydrate_from_store()` | `main.py:2688` · `:2700` |
| **DELIVERY/GTT** | `CncGttMonitor(...)` | `main.py:2770` |
| **SHARED** | `order_reconciler.start()` — hosts the MIS reconcile **and** the delivery GTT cadence | `main.py:3528`, wired `:2797` |
| **SHARED** | `candle_store` · `token_monitor` · webhook thread | `main.py:3489` · `:3531` · `:3567` |
| **SHARED / LIFECYCLE** | `eod-pre-alert` · `market-open-margin-sync` · **`eod-self-exit`** | `main.py:966` · `:1035` · **`:1223`** |

⭐ **Why it matters:** the delivery pipeline has no scheduler of its own. It is a passenger on the
**MIS-era reconciler's poll thread** (`order_reconciler._maybe_run_cnc_monitor`, `:661`). That is the
structural fact everything below follows from.

---

## B · Does GTT require the service to remain alive after MIS has finished?

🏷️ **PROVEN — AND THE ANSWER IS THE OPPOSITE OF THE INTUITION.**

📄 `orders/order_reconciler.py:663-683` — `_maybe_run_cnc_monitor()`:

```
in_hours = bool(self._market_hours_fn())
if not in_hours:
    return                     # ← :674-675
```

🔴 **The 15-minute delivery GTT reconcile does NOT run outside market hours at all.** By ~15:30 the
delivery maintenance loop is *already* idle, by design — hours before the 17:35 lifecycle point.

🔬 What still runs out-of-hours, every cycle: the narrow adoption prepass
`_run_gtt_adoption_prepass()` → `adopt_orphan_gtts()` (`order_reconciler.py:696-699`).
⭐ **Observed live:** the 24-Aug journal shows `cnc_gtt_monitor — cnc_gtt_adoption: get_gtts failed`
at **17:20** — i.e. the prepass demonstrably executes post-session. ⇒ 📄 the in-hours gate applies to
`reconcile()`, ⛔ not to the prepass.

⭐ **Why it matters:** *"what breaks if the process is not there after 15:30"* is **nothing that was
running anyway**. The delivery reconcile had already switched itself off.

---

## C · 🔴 THE LOAD-BEARING ONE — are broker-side GTT/OCO orders sufficient with the service down?

🏷️ **PROVEN BY CONSTRUCTION for the steady state. ⚠️ NOT PROVEN BY OBSERVATION — and structurally
it cannot be, see the gap below.**

📄 `orders/cnc_gtt.py:2-7` states the design intent verbatim:
> *"places ONE broker-side two-leg OCO GTT (Good-Till-Triggered) right after the entry fill, so a
> single persistent trigger protects the position entry→exit **and survives a VM outage**."*

🔬 And the code does what the docstring says — `broker/zerodha_adapter.py:678-687`: both legs are
`exit_side` LIMIT, `product=CNC`, `quantity=qty`, `trigger_values=[sl_trigger, tgt_trigger]`
(ascending — SL below, TGT above); LIVE → `kite.place_gtt`. ⇒ 📄 **the stop and the target rest AT
ZERODHA.** Triggering and order placement are broker-side; ⛔ no client process participates.

🔬 Durability of the local mirror: `gtt_state` is the durable table (both 24-Aug rows survived the
overnight stop and were read back this morning), and `CncGttPlacer.hydrate_from_store()`
(`main.py:2700`) rebuilds the in-memory map at every boot.

### ⚠️ THE PRECISE QUALIFIER: PROTECTION IS BROKER-SIDE; **REPAIR** IS SERVICE-SIDE

📄 `orders/cnc_gtt_monitor.py:470-525` — every degraded state needs the process:

| state | action | file:line | with the service down |
|---|---|---|---|
| GTT triggered, holding still > 0 (partial OCO fill) | `_reprotect` | `:599` | 🔴 **remaining qty is NAKED until repaired** |
| GTT missing, holding intact, in-hours | `_recreate` | `:607` | ⛔ no recreate |
| GTT missing, holding intact, out-of-hours | `_queue_preopen` → drain on first in-hours cycle | `:652` / `:659` | ⛔ not detected |
| `held != row.qty` | `_qty_mismatch` — cancels the wrong-qty GTT, **⛔ NO recreate** | `:636` | 🔴 deliberately unprotected pending operator review |

🔬 `_preopen_queue` is an **in-memory dict** (`cnc_gtt_monitor.py:94`) — ⛔ it does **not** survive the
process. ⭐ But it is re-derived from the durable `gtt_state` by the boot-time reconcile
(`order_reconciler.py:429-431`, which at 08:15 is pre-open ⇒ `in_hours=False`), so ⛔ **nothing is
lost overnight.** ⭐ That is sound: the durable table is the state, the queue is a within-session
artefact.

### ⭐ THE STRUCTURAL FACT THAT MAKES THIS SAFE TODAY

🔬 The service is up **08:15 → 17:35**. Market hours are **09:15 → 15:30**. ⇒ 📄 **the service's
scheduled downtime lies entirely inside market closure**, so a GTT cannot trigger while the service
is scheduled-down. ⭐ The exposure only becomes real in the *unscheduled* case — a mid-day crash, or
a manual stop left standing into the next session — and in that case the OCO still rests at the
broker, so the **position** stays protected and only **repair** is lost.

### ⚠️ THE ONE GENUINE OBSERVATIONAL GAP — named, ⛔ not filled

⛔ **No GTT has ever been observed firing while the service was down**, and it cannot be observed in
normal operation, because the two windows do not overlap. 🔬 Both 24-Aug delivery exits
(`GTT_EXIT` at 11:31:29 and 12:47:50) occurred with the service **UP**.
⭐ **The smallest evidence that would settle it:** read the broker's own `get_gtts()` for a resting
system GTT at a moment the service is not running — e.g. a read-only `kite.get_gtts()` from a
throwaway script while a CNC position is held and the service is stopped. ⛔ Not run: it needs a live
carried position, which does not exist today, and 👤 it is Rama's call.
⚠️ 💭 Zerodha GTT persistence is a **broker property**; ⛔ this repo cannot prove it, and the
docstring asserting it is 📄 a design claim, ⛔ not a measurement.

---

## D · Any T+1 / GTT monitoring that must continue overnight?

🏷️ **PROVEN — NO. NOTHING IN THE SERVICE IS REQUIRED BETWEEN 17:35 AND 08:15.**

🔬 The overnight work is done by **cron — separate processes, wholly unaffected by the service's
state** (`crontab -l`, measured):

`45 15` `reconcile_positions.py` · `50 15` `eod_cleanup.py` · `55 15` `eod_verify.py` ·
`58 15` `eod_broker_reconcile.py` · `0 16` `wal_checkpoint.py` · `5 17` `control_tower/runner.py` ·
`15 18` `forward_shadow_record.py` · `0 18` `check_cron_drift.py` · `45 18` `system_manager.py` ·
`50 18` `cron_officer.py --eod-summary` · `0 1`/`5 1` DB backups · `0 5` token cleanup ·
`15 8` `auto_refresh_token.py`.

⇒ 📄 **Settlement tracking, carry rehydration and the 08:15 reconciliation's inputs are all either
cron-owned or reconstructed at boot from `gtt_state` + the DB.** ⛔ Nothing silently degrades because
the process is absent.
⚠️ ⭐ One standing caveat, already recorded and unchanged: `reconcile_positions` reads `positions()`
only and is blind to delivery T+1 — ⛔ that is a pre-existing item, ⛔ not an F6 finding.

---

## E · Is there ALREADY a pipeline-scoped stop or lifecycle mechanism?

🏷️ **PARTIALLY — AND THE EXISTING PRECEDENT IS EXACTLY THE RIGHT SHAPE.**

**① ENTRY-SCOPED: YES, and it is real.** 🔬 `delivery_enabled` (`config/system_config.yaml:102`,
currently **`true`**) is a master delivery lock: `broker/zerodha_adapter.py:558-565` **blocks CNC
`place_order`** when false.

**② AND IT IS DELIBERATELY SPLIT FROM PROTECTION.** 📄 `zerodha_adapter.py:683-687` and `:765-766`:
> *"GTT ops are NOT gated on `delivery_enabled` — protection MUST survive disablement. With delivery
> off there are no new CNC entries (`place_order` blocks them), so a GTT op only ever touches a
> PRE-EXISTING holding (strand-prevention); the entry lock lives on `place_order`."*

⭐ **This is the single most important finding for F2.** A pipeline-scoped control already exists,
and its design rule is already settled: **scope the ENTRY, never the PROTECTION.**

**③ KILL SWITCH: a carve-out, ⛔ NOT scoping.** 🔬 `capital/kill_switch.py:619-631` — SOFT_KILL never
flattens, and EOD6 does not square off delivery (*"Delivery (CNC) is carried by design (EOD6) — not
squared off"*), pinned by `test_kill_alerts_delivery_carveout.py`. ⛔ But `soft_kill()` / `hard_kill()`
/ `is_active()` take **no pipeline argument**, and `_count_open_positions` (`:404-413`) is
product-blind. ⇒ 📄 the delivery awareness is in the *message and the flatten behaviour*, ⛔ not in
the kill's **scope**.

**④ LIFECYCLE (start/stop): ⛔ NO.** 🔬 The systemd unit is the only granularity. There is no
per-pipeline start, stop, pause or enable at **runtime** — `delivery_enabled` is read from config at
boot.

---

## F · The smallest architecture that would make lifecycle independence real

⛔ Described, ⛔ not designed, ⛔ not sized.

Three things would have to **exist**, and no more. First, the notion of *"an active position"* would
have to carry a **pipeline dimension**, because the single product-blind count is what every
lifecycle decision currently reads. Second, the per-pipeline **halt** would have to be a runtime
control rather than a boot-time config read, following the shape `delivery_enabled` has already
established — an **entry lock that is explicitly not a protection lock**. Third, and the only genuinely
new thing, there would have to be a stated **rule for who owns the process lifecycle**: today an open
position in *either* book keeps the *whole* process alive, and independence requires an explicit
answer to *"whose carry may hold the process open, and what happens to the other pipeline while it
does."* ⛔ Nothing about how to build any of it is proposed here.

---

# 🔴 THE VERDICT

## **(i) ALREADY INDEPENDENT — on the question C actually asks.**

📄 GTT protection is broker-side, rests at Zerodha, and needs nothing from this process overnight
(A–D). ⇒ **The whole-service stop costs GTT nothing it would otherwise have had**, because the
delivery reconcile is already in-hours-only (`order_reconciler.py:674-675`) and the scheduled
downtime lies entirely within market closure.

## ⚠️ 👤 BUT I MUST REPORT A CONTRADICTION RATHER THAN ACT ON ONE — verdict (i) carries a rider the evidence does **not** support.

The card's (i) concludes *"…and F6 is an operational inconvenience, ⛔ not an architecture defect."*
🔴 **That half is refuted.** There IS a real coupling — it simply **runs in the opposite direction
from the one the card hypothesised.**

🔬 **The card looked for:** *MIS's carry forces a whole-service stop, and that stop kills something
GTT needs.* ⛔ **Not found** — and the second clause is false.

🔴 **What is actually there:** `_eod_self_exit_due` (`main.py:1074-1113`) gates the entire process on
`store.count_active_positions()` (`main.py:1109`) — the product-blind count. ⇒ 📄 **a carried
DELIVERY position holds the WHOLE service open past 17:35, MIS machinery included.** That is what
creates the operator's manual-stop obligation, and the consequence chain is already recorded:

▎ carried CNC ⇒ no self-exit ⇒ service still `active` at 08:15 ⇒ `token_watcher` reads
▎ *"running — nothing to do"* ⇒ **NO BOOT** ⇒ the 15:15 `SOFT_KILL` never auto-clears ⇒
▎ 🔴 **the next day takes NO ENTRIES — in BOTH pipelines.**

⇒ 🔴 **The operational coupling is DELIVERY → WHOLE SERVICE → MIS**, ⛔ not MIS → GTT. A delivery
carry can silently disable the *intraday* pipeline the following day. ⭐ **That is an architecture
defect, and it should be recorded as one** — ⛔ it is not merely an operational inconvenience.

⚠️ ⭐ And per 👤 Rama's standing wording rule, the manual stop stays labelled the **LEGACY SAFEGUARD**;
this measurement does ⛔ not convert it into an architecture decision. What it does establish is that
the safeguard is compensating for the **EOD gate's product-blindness**, ⛔ not for any GTT fragility.

---

# ⭐ WHAT F2 MUST TAKE AS GIVEN

1. 🟢 **Delivery protection is NOT F2's problem.** The broker holds the OCO. F2 may assume a carried
   CNC position is protected without the service. ⛔ It may **not** assume *repair* of that protection
   survives a stop — repair is service-side and in-hours-only.
2. 🔴 **F2's "own halt" cannot be a lifecycle halt today.** There is exactly one process, one start,
   one stop and one EOD self-exit gate. A per-pipeline halt must be an **entry lock**, ⛔ not a
   process boundary.
3. ⭐ **The shape is already settled and F2 should copy it, ⛔ not invent one:** `delivery_enabled` +
   the **R2 guard split** (`zerodha_adapter.py:683-687`) — *scope the ENTRY, never the PROTECTION.*
   ⚠️ But note it is **boot-time config**, ⛔ not a runtime control; that difference is F2's to face.
4. ⛔ **F2 must NOT assume the active-position count can distinguish pipelines.** It cannot, and the
   process's own EOD exit depends on it. Any per-pipeline counter F2 introduces is a **new** thing,
   ⛔ not a re-reading of the existing one.
5. 🔴 **Independent capital will still sit on a SHARED process lifecycle** until the EOD gate becomes
   pipeline-aware. ⭐ F2 must state explicitly that it is building logical independence on a shared
   lifecycle, and ⛔ must not claim operational independence it does not have.
6. ⚠️ **The kill switch is a carve-out, ⛔ not a scope.** `soft_kill`/`hard_kill`/`is_active` take no
   pipeline argument. F2's "own halt" has **no existing hook** in the kill switch to extend.

---

## ⛔ STATE OF THE TREE

⛔ **NOTHING BUILT · NOTHING PUSHED · NOTHING TOUCHED.** No code, no design, no config change, no
kill-switch change, no service start/stop/restart. Every VM call was a **read**.
🔬 `origin/main` = `195436bb…`, unchanged. Deployed-tree drift **0**.
⛔ §0 was not re-confirmed. ⛔ No F2 work. ⛔ No NI-16. ⛔ No F13 legs. ⛔ The eight closed decisions
were not reopened.
