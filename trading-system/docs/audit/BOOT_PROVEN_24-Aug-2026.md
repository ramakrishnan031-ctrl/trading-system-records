# BOOT PROVEN — Mon 24-Aug-2026 · THE FIRST EXECUTION OF 20 COMMITS

**Governed by** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`). **Scope executed:** OBSERVE AND RECORD.
⛔ No code · ⛔ no push · ⛔ no deploy · ⛔ no F2 · ⛔ no NI-16 · ⛔ no F13 leg · ⛔ no sweep · ⛔ no memory work.
**Provenance:** 🔬 measured · 📄 source-derived · 💭 inference · 👤 Rama.
**Measured from:** PC `D:\Projects\trading-system` + `ssh trading-vm`, 24-Aug **10:31–10:45 IST**
(PC 10:44:58 +0530 / VM 10:45:01 +0530 — clocks agree to 3 s).

---

# §1 — BOOT: ✅ **PROVEN**

| # | check | 🔬 value |
|---|---|---|
| **V-5** | `systemctl show trading-system -p ExecMainStartTimestamp --value` | **Mon 2026-08-24 08:15:20 IST** |
| **V-6** | `STARTUP` row in `data_store/trading_system.db` → `system_events` | **`event_id 3788` · `2026-08-24T08:15:33.134646+05:30` · `STARTUP` · `COLD` · `{"mode": "live", "version": "2.0.0"}`** |
| ⇒ | row **AFTER** the attempt's start | **08:15:33.13 > 08:15:20** ⇒ ✅ **belongs to THIS attempt** |

**Query used, verbatim:**
```sql
SELECT event_id, timestamp, event_type, scenario, details FROM system_events
WHERE event_type='STARTUP' ORDER BY timestamp DESC LIMIT 5;
-- against file:/home/ubuntu/systems/trading-system/data_store/trading_system.db?mode=ro
```

### ⭐ Why this is not a lucky read

* 🔬 **`NRestarts=0`**, `ActiveState=active` / `SubState=running`, `ExecMainPID=241264`,
  `ExecMainStatus=0`, `Result=success`. ⇒ **there was exactly ONE attempt today**, so M-1's concrete
  Monday — *"an earlier same-day row from a DIFFERENT attempt"* — is **not reachable**: there is no
  other attempt to confuse it with.
* 🔬 **The path trap was checked FIRST, not assumed:** live DB `data_store/trading_system.db` =
  **374,145,024 B**, mtime 10:33. The decoy `data/trading_system.db` = **0 B**, mtime **18-May**.
  No `no such table` error occurred.
* 🔬 **The query is not vacuous:** `system_events` holds **STARTUP 78 · SHUTDOWN 76 ·
  KILL_AUTO_CLEARED 44 · CONFIG_DIFF 29**. The 23-Aug record measured **77 STARTUP / 76 SHUTDOWN**
  ⇒ **exactly +1 STARTUP**, and it is today's. The historical 1-row STARTUP/SHUTDOWN imbalance is
  **unchanged** (78−76 = 2, of which today's not-yet-shut-down boot is one) ⇒ ⛔ no new pairing anomaly.
* 🔬 **The negative control fired nothing:** `grep -c "Config load failed" logs/system_2026-08-24.log`
  = **0**. ⭐ Per the runbook this proves only that THAT signature is absent — but combined with a
  STARTUP row written at `main.py:3832`, ~1,900 lines PAST the `:1916` rejection point, the boot
  demonstrably reached Phase 0h.

### 🔬 The full boot sequence, as recorded

| time (IST) | event |
|---|---|
| 08:15:20 | systemd `ExecMainStartTimestamp` / `InactiveExitTimestamp` / `ActiveEnterTimestamp` |
| 08:15:21.633 | `CRITICAL kill_switch` — *"KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL reason=circuit_breaker_force_close_15:15"* |
| 08:15:21.635 | `KILL_AUTO_CLEARED` (`event_id 3786`) — ⭐ the designed prior-day auto-clear, 2 ms later |
| 08:15:29.534 | `CONFIG_DIFF` (`event_id 3787`) |
| 08:15:30.241 | `fm_ledger` **INIT** — `amount=10563.90`, `reason="initialize with broker_balance=10563.9"` |
| 08:15:33.134 | **`STARTUP` (`event_id 3788`)** ← the gate |

⭐ The 08:15:21 CRITICAL is **Friday's routine 15:15 kill auto-clearing**, ⛔ not a fault — 44
`KILL_AUTO_CLEARED` rows in history. It is the **only** CRITICAL in the whole day's log.

### ⛔ KEEPING THE GATE NARROW — what this does NOT prove

⛔ Not the strategy loop · ⛔ not market data · ⛔ not broker connectivity · ⛔ not the absence of a
later crash-loop · ⛔ **not the correctness of any one of the 20 commits.**
💭 **The SHA↔boot association remains an INFERENCE** (M-1: the STARTUP payload carries no code
identity; `VERSION = "2.0.0"` is hardcoded and byte-identical across days on which `origin/main`
moved). ⭐ What §2 adds is a **FALSIFIER**, ⛔ not a measurement.

---

# §2 — V-2 / V-3 / V-4: ✅ **ALL THREE HELD** (⛔ nothing moved)

**Recorded SHA, VERIFIED — ⛔ NOT re-captured.** Source: `docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md`
header, written **before** the boot: `RECORDED = 195436bb6323c981d68f313ad7c39858cc0a4653`.

| # | check | 🔬 result |
|---|---|---|
| **V-2** | `origin/main` | `195436bb6323c981d68f313ad7c39858cc0a4653` — **measured TWO independent ways**: `git ls-remote origin refs/heads/main` from the PC **and** `cat /home/ubuntu/trading-system.git/refs/heads/main` on the VM. ✅ **== RECORDED** |
| **V-3** | deployed `HEAD` | `195436bb6323c981d68f313ad7c39858cc0a4653` ✅ **== RECORDED** |
| **V-4** | tree drift | **0 files** (`git diff-index --name-only HEAD --` → EMPTY) ✅ |

**V-4 form used — the `GIT_INDEX_FILE=$(mktemp)` shape, ⛔ not the plain `GIT_DIR`/`GIT_WORK_TREE`
one** (the latter writes the bare repo's **shared index**). `update-index --refresh` was run; without
it the recipe reports 1,309 phantoms.

### 🔬 V-4 NON-VACUITY, PROVEN TODAY — ⛔ not carried from 23-Aug

⭐ *A green check is evidence only if it could have been red.* The identical recipe pointed at
**`4568385`** instead of `HEAD` reports **29 paths** (28 `M` + 1 `D`: `capital/position_sizer.py`,
`capital/risk_engine.py`, `config/system_config.yaml`, `core/config_auditor.py`,
`core/config_loader.py`, `core/schema.sql`, `core/state_store.py`, `main.py`,
`scripts/security_monitor.py`, `orders/cnc_gtt_monitor.py`, …, `D tests/unit/test_position_sizer_delivery_scaffold.py`).
⇒ **the mechanism demonstrably reports non-empty ⇒ the 0 against `HEAD` is a real zero.**
⭐ **And it required no write of any kind** — it tests a property of *git*, not of the box, so the
23-Aug standing preference (validate in a disposable structure; ⛔ live VM only for properties *of*
the live VM) is honoured. ⛔ Nothing planted, nothing restored, nothing to disclose.

### ⇒ VERDICT
✅ **The SHA↔boot association is NOT broken.** All three falsifiers were available and none fired.

**Repeated at report time (10:45:01 IST) — identical:** V-2 `195436b…` · V-3 `195436b…` ·
V-4 `0` · start `08:15:20` · `NRestarts 0` · `active/running` · `RestartPreventExitStatus=3 4 5`.

---

# §3 — ROLLBACK TARGET: ⭐ **ADVANCED `4568385` → `195436b`**

🔬 The TREE's clock ticked, exactly as §0.1 of the runbook said it would.

| | before today | 🔬 **now** | goes stale on |
|---|---|---|---|
| **TREE / RB-3 target** | `4568385` (last proven boot Fri 21-Aug 08:15:25) | **`195436bb6323c981d68f313ad7c39858cc0a4653`** | every **PROVEN BOOT** |
| **PARENT** (RB-2 only) | `195436b` | **derive at use time** — ⛔ never pasted | every **PUSH** |

⭐ **Both read `195436b` today, and that is a coincidence of timing, ⛔ not an identity.** Two facts,
two clocks; they must stay measured separately.

🔴 **Consequence, and it is the whole reason this step exists:** before this advance, RB-3 would have
**reverted 20 commits** on the next incident when the correct answer is **ZERO**.

**Runbook updated in the same breath** — `docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md`:
the §1 invariant box, RB-2's tree, RB-3's `checkout -f` target, V-7's comparand and the
phone-readable step 5 now read `195436b`. ⛔ **Every 23-Aug historical measurement in that file was
left byte-intact** — the record of what was true *then* is not rewritten; it is superseded in place,
with a dated advance block at the top.

---

# 🔴 §4 — ATTRIBUTION: ⛔ **A CLEAN BOOT VALIDATES NOTHING INDIVIDUAL**

🔬 `git rev-list --count 4568385..195436b` = **20**. All twenty executed for the first time,
together, at 08:15:20 today.

⛔ **No behaviour today — good or bad — is assigned to** `d00e574` item 1 · `940a572` job 1 ·
NI-1 `4928941` · NI-2 `c146eb7` · NI-3 `5a7dbf6` · NI-4 `6ad328e` · NI-6 `4c495d0` · NI-7 `742d9da` ·
NI-9 `a056768` · NI-9-follow-up `b397806` · NI-11 `b44750c` · NI-12 `c7145c7` · NI-13 `b6e85af` ·
NI-17 `ba5db64` · NI-18 `e39655a` · NI-19 `b23f72d` · NI-5 `076fe57` · the governance/unit commit
`2f67bb8` · NI-14 `b0cfe71` · NI-15 L1 `195436b`.

⭐ **The unit of attribution is THE SET.** 👤 Chosen knowingly.
⚠️ **AND THE INVERSE HOLDS: a clean morning closes no open item.** 🏷️ Ceiling stays **DEPLOYED**.

---

# §5 — THE §6 WATCH ITEMS · 🔬 RECORDED, ⛔ NOTHING FIXED

## 5.1 · F1 / NI-4 fail-closed — ⭐ the config was ACCEPTED; ⛔ the REJECTION arm was not exercised

🔬 All **7** required delivery keys are present in the deployed `config/system_config.yaml`:

| key | value |
|---|---|
| `position_sizing.delivery_risk_per_trade_pct` | `0.01` |
| `position_sizing.delivery_max_concentration_pct` | `0.1` |
| `position_sizing.delivery_max_position_value_pct` | `0.4` |
| `risk.max_open_delivery_positions` | `3` |
| `risk.max_daily_delivery_trades` | `5` |
| `risk.delivery_max_sector_exposure_pct` | `0.4` |
| `risk.delivery_daily_loss_limit_pct` | `0.03` |

🔬 Boot reached Phase 0h · `Config load failed` **0 matches**.
🔴 **BUT BE PRECISE:** this proves the strict schema **ACCEPTED a complete config**. ⛔ It does
**NOT** prove the fail-closed arm *rejects* a missing key in production — for that, a key would have
to be absent. ⭐ That arm is proven **by test**, ⛔ not by today's run.
🏷️ **DEPLOYED · ⛔ NOT VERIFIED LIVE.**

## 5.2 · NI-15 L1 — ✅ **LIVE AND WORKING. 🔬 MEASURED.**

🔬 `data_store/security_state.json` now carries the key NI-15 L1 introduced:

```json
"file_unreadable": { "/etc/sudoers": "unreadable" }
```

🔬 **It is genuinely new code, ⛔ not a pre-existing field:**
`git show 4568385:scripts/security_monitor.py | grep -c file_unreadable` = **0**; at `195436b` = **2**.
🔬 **And the state it replaced is gone:** all **7** paths in `file_hashes` now hold real digests —
⛔ **zero nulls** (`sshd_config`, `sshd_config.d/99-trading-security.conf`, `security-watcher.service`,
`trading-system.service`, `.env`, `accounts.csv`, `system_config.yaml`). That is exactly the
`{k: v for k, v in hashes.items() if v is not None}` line, observed doing its job on live state.
⭐ **The `missing` vs `unreadable` discrimination also worked:** `/etc/sudoers` exists but is
`0440 root:root` and the watcher runs `User=ubuntu` ⇒ correctly classified `unreadable`, ⛔ not `missing`.

✅ **P-4 / P-5 / P-6 of the frozen prediction all hold.**
🔴 **P-6 explicitly: sudoers is STILL unreadable and STILL skipped — L1 made the skip
NON-DESTRUCTIVE, ⛔ it did not close the gap.** That is F13-L2, ⛔ unauthorised.

## 5.3 · NI-14 — 🔴 **NOT EXERCISED TODAY. THE PLANNED OBSERVATION IS VACUOUS UNDER TODAY'S INPUT.**

🔬 The live input right now — `data_store/security/last_run.json`, mtime 10:36:
```json
{"checks_run": 10, "clean": true, "findings_count": 0, "max_severity": "INFO",
 "persistent": [], "persistent_count": 0, "timestamp": "2026-08-24T10:36:19.557417+05:30"}
```
🔴 **`findings_count = 0`.** The old derivation was
`"critical" if any CRITICAL else "warn" if findings else "ok"` ⇒ with **zero** findings, **both the
old and the new code return `ok`.**
⇒ ⛔ **A green security panel at 17:05 today is NOT evidence that NI-14 works.**

⚠️ On 23-Aug the input was `clean:false, findings_count:1, max_severity:"INFO"` — the case that
**would** have discriminated (old `warn` / new `ok`). 💭 That INFO finding has since gone away;
💭 plausibly downstream of the pre-L1 null now cleaned out of `file_hashes` — ⛔ **not measured;
labelled as inference.**
⚠️ **Timing:** the control tower runs at **17:05** (`ops/control_tower/runner`), so NI-14's first
possible exercise today **has not happened yet** as of 10:45.
🔬 Historic `control_tower_status.security_status` already reads `ok` on 17· 20· 21-Aug (zero-finding
days) ⇒ ⭐ **`ok` alone is not the signal; the signal is `ok` on a day carrying ≥1 INFO-only finding.**
🏷️ **DEPLOYED · ⛔ NOT VERIFIED LIVE · ⛔ NOT EXERCISED.**

## 5.4 · NI-17 — 🔬 **CONFIRMED LATENT AT TODAY'S CAPITAL**

🔬 Today's capital, from `fm_ledger` INIT: **₹10,563.90** (`broker_balance=10563.9`, 08:15:30.241).
📄 NI-17's own measurement: `min_tick_size 0.05` caps `qty_by_risk` at `R × risk_pct / 0.05` ≈ **2,117**,
and the 2× ceiling caps the ORDER at **4,235** — both far under `max_single_order_qty = 10,000`; the
output guard first becomes reachable at ≈ **₹25,000** capital (~2.4× today).
⇒ ✅ At ₹10,563.90 **it cannot bind.** 🔬 Today's largest quantity was **3 shares**.
⛔ Not exercised — as designed.

## 5.5 · NI-18 — 🔬 **ITS CHANGED BRANCH WAS NOT REACHED. ⭐ WHICH IS THE PREDICTED RESULT.**

NI-18 fires only `if tiered_qty > raw_qty`. 🔬 On all **5** of today's trades
`tier_weight_applied = 0.5` and `perf_weight_applied = 1.0` ⇒ multiplier **0.5** ⇒
`tiered_qty < raw_qty` ⇒ **the branch is unreachable today.**
🔬 And the observable agrees: `binding_constraint = "concentration"` on all 5 — ⛔ **`MULTIPLIER`
never appeared.**
⇒ ✅ Consistent with the card's claim that NI-18 changes what `constraint` **REPORTS** and ⛔ never
what it **computes**: today it changed **nothing at all**. 🔬 The arithmetic checks out per trade —
e.g. `BALUFORGE min(8, 3, 1) = 1 × 0.5 → 1`; `RBZJEWEL min(89, 251, 7) = 7 × 0.5 = 3.5 → 3`.

⭐ **The same measurement settles NI-16's hazard for today: `perf_weight_applied = 1.0` on 5/5** ⇒ the
*"multiplier applied AFTER the min with nothing re-capping"* defect stayed **LATENT** — every
multiplier today was ≤ 1, so it only ever *reduced*. 🔬 measured.
⛔ NI-16 remains blocked on F2, untouched.

## 5.6 · 🔴 THE CAPITAL-DRIFT COMPARATOR — **CLEAN TODAY, AND THE CARRY CASE IS STILL UNPROVEN**

### 🔬 What ran

`orders/order_reconciler.py` logs `G3 MARGIN_RECON` at **DEBUG** every ~15 s:
`held · carry · held_today · broker_used · residual`. **581 samples** by 10:42.

| 🔬 | value |
|---|---|
| `carry=0.00` | **581 / 581 samples** |
| `held` | `0.00` → `89.33` → … → **`1169.45`** (steady since ~10:12) |
| `residual` now | **−1.07 / −1.82** (converged; `broker_used ≈ 1170.5` vs `held = 1169.45`) |
| **`CAPITAL_DRIFT` at ERROR** | **0** |
| **`CAPITAL_DRIFT (suppressed/throttled)`** | **0** |

### ✅ 🔬 THE ZERO IS REAL — IT CAN GO NON-ZERO

| day | ERROR-level drift alerts | suppressed/throttled | note |
|---|---|---|---|
| 20-Aug (**pre-fix**; `7fc5d5a` landed 19:34 that evening) | **8** | many | old message shape, `actual < expected` |
| 21-Aug (**post-fix**) | **2** | **23** | new shape, bracketed diagnostics |
| **24-Aug (today)** | **0** | **0** | ⇐ |

⇒ ⭐ **the check could have been red, and today it is not.**

### 🔬 THE ALGEBRA, MEASURED — the residual IS the FM-vs-broker gap

Both 21-Aug alerts satisfy the identity **exactly**:
```
10:01:24  expected_net=8991.04  actual_net=10186.39  delta=1195.35
          real_capital=10587.40  held=1596.36  broker_used=401.01  ->  held - used = 1195.35
15:14:45  expected_net=9481.05  actual_net=10475.48  delta= 994.43
          real_capital=10580.32  held=1106.35  broker_used=111.92  ->  held - used =  994.43
```
⇒ 🔬 **`delta == held − broker_used`, 2/2.** Those alerts are the **transient window in which the
FundManager has reserved capital the broker has not yet blocked** — ⭐ the same operand-mismatch
class, a different operand pair.

### ⚠️ TODAY'S SILENCE HAS A THIN MARGIN — ⛔ do not read it as structural

🔬 Peak residual today: **₹935.71** at 10:02:14.523 (`held=996.00 broker_used=60.29`).
🔬 The in-session band at that instant = `max(50, |expected| × 0.10)` with
`expected ≈ 10563.90 − 996.00 − 0 = 9567.90` ⇒ **₹956.79**.
⇒ 💭 **cleared by ≈ ₹21.08 (2.2 %)** — 💭 inferred via the `delta == residual` identity above
(🔬 measured 2/2 on 21-Aug); ✅ **corroborated** by the **0** suppressed/throttled count, which is the
direct measurement that `delta` never crossed tolerance at any of the 581 samples.
⭐ Other transients today: 745.75 · 528.78 · 416.25 · 346.05 · 67.56 · 30.50 · 26.70.

### 🔴 THE CARRY CASE — ⛔ **NOT TESTED TODAY, AND THE CODE ITSELF NAMES WHEN IT WILL BE**

📄 `orders/order_reconciler.py`, CHECK 2, verbatim:
> *"Measured every cycle (forensics) … **No alert of its own yet**, and the reason is a measurement
> gap rather than convenience: broker `used` for a SETTLED CNC holding is unmeasured … so alerting
> here would **fire falsely on the first carry day**. **Owed: measure a T+1 carry, then decide a
> threshold.**"*

🔬 `carry = 0.00` on **581/581** samples, because Friday's book was flat (21-Aug `SHUTDOWN` at
17:35:04 ⇒ nothing carried in).
🔴 **⇒ The card's revert trigger — *"if a carried CNC produces a CHECK 1 residual ≈ that position's
value, the carry algebra is WRONG ⇒ REVERT"* — was NOT evaluable today.** ⛔ Today's clean run is
**not** evidence about the carry case.

🔬 **AND THE FIRST REAL TEST IS DATED.** The two CNC positions below carry into T+1 ⇒
`intraday_carry + positional_carry` becomes non-zero for the first time at the **25-Aug 08:15 boot**.
⚠️ Watch it there. ⛔ Do **NOT** tune the tolerance · ⛔ do not add a carry term · ⛔ do not touch
`_total`, RESERVE, COMMIT or the buckets. 🏷️ Trigger = **REVERT the unit**, 👤 on Rama's word.

### ⚠️ AND A NEW, DATED EXPOSURE TONIGHT — 🔬 the flat-band window has never met `held > 0`

🔬 `_MARGIN_RELIABLE_CLOSE = dt_time(15, 45)` (`orders/order_reconciler.py:118`). After **15:45** the
`capital_drift_tolerance_pct = 0.10` widening **switches off** and the band reverts to the flat
`capital_drift_tolerance = 50.0` — while `held` will still be **₹1,169.45**.

🔬 **This window has never been exercised with a non-empty book since the fix:**

| day | MARGIN_RECON samples at/after 15:45 | of those, `held > 0` |
|---|---|---|
| 21-Aug | **437** | **0** |
| 20-Aug | 0 | 0 |
| 19-Aug | 0 | 0 |

⇒ 💭 from ~15:45 until the service stops, `delta` faces a **₹50** band against `held = ₹1,169.45`.
⭐ The `FIX-189 (P1-B)` guard suppresses this **only** when broker `net` reads **exactly 0.0**; a
non-zero out-of-session net is not covered. ⇒ 💭 **repeat CRITICALs at the 30-min throttle
(`capital_drift_alert_interval_sec = 1800`) are plausible this evening.** ⛔ Recorded, ⛔ not fixed,
⛔ not tuned. ⭐ **Note the interaction: the F6 manual stop below also ends this exposure.**

---

# 🔴 §6 — F6 · **THE MANUAL STOP IS OWED TONIGHT.** 🔬 MEASURED, ⛔ NOT INFERRED

## 🔬 Today traded. 5 entries — and 2 of them are DELIVERY

| entry | symbol | dir | product | strategy | qty | entry px | status | exit | reason | net P&L |
|---|---|---|---|---|---|---|---|---|---|---|
| 10:03:46 | **BALUFORGE** | LONG | **CNC** | positional_swing_long | 1 | 610.45 | 🔴 **OPEN** | — | — | — |
| 10:04:16 | RBZJEWEL | LONG | MIS | vwap_bounce_long | 3 | 146.97 | CLOSED | 10:11:45 | SL_HIT | **−3.34** |
| 10:05:32 | **KAMATHOTEL** | LONG | **CNC** | positional_sector_rotation | 2 | 220.56 | 🔴 **OPEN** | — | — | — |
| 10:06:22 | OPTIEMUS | LONG | MIS | gap_go_long | 1 | 589.40 | OPEN | — | — | — |
| 10:08:24 | GUJTHEM | LONG | MIS | gap_go_long | 1 | 394.35 | CLOSED | 10:09:47 | TGT_HIT | **+6.69** |

🔬 `CNC|OPEN 2 · MIS|CLOSED 2 · MIS|OPEN 1`. Realised today **+₹3.35** (`fm_ledger` `RELEASE_USED`
agrees).
🔬 Corroborated **independently** by two ACTIVE `gtt_state` OCO rows created today —
`333025881 BALUFORGE SELL 1 sl 598.20 tgt 628.80` and `333026682 KAMATHOTEL SELL 2 sl 216.15 tgt 227.18`,
both `last_verified_at 10:30:37`.
⭐ Within the deployed caps (`max_open_delivery_positions 3`, `max_daily_delivery_trades 5`).

## 🔴 THE MECHANISM, READ FROM THE DEPLOYED SOURCE

```python
# core/state_store.py — count_active_positions()
SELECT COUNT(*) AS n FROM trades WHERE status IN ('OPEN', 'PARTIAL', 'PENDING_FILL')
```
🔬 **It is PRODUCT-BLIND** — a CNC row counts exactly like a MIS row. `main.py:1109` feeds it to
`_eod_self_exit_due`.

⇒ 🔴 **THE CHAIN, and every link is measured:**
**2 CNC rows stay `OPEN` past 17:35** (that is what delivery *is*) ⇒ `count_active_positions() ≥ 2`
⇒ `_eod_self_exit_due` is never due ⇒ **NO self-exit** ⇒ the service is still `active` at tomorrow's
08:15 ⇒ `token_watcher.sh:139-141` reads `active`, says *"running — nothing to do"*, and **never calls
`start`** ⇒ **NO BOOT** ⇒ the 15:15 `SOFT_KILL` has nothing to auto-clear
⇒ 🔴 **TUESDAY 25-Aug: NO ENTRIES, presenting as *"no signals today"*.**

## ⇒ 👤 **RAMA MUST RUN, ON THE VM, AFTER 17:35 TODAY:**
```bash
sudo systemctl stop trading-system.service
```
⛔ **I cannot run it** (§8 hard limit: no service start/stop). ⭐ **Reminded — ⛔ NOT done.**
⚠️ **Monday is not Friday: a missed stop costs TUESDAY, a full trading day.**
⛔ Cancelling the GTT does not help. ⛔ A restart is not the safe default.
⚠️ **And tomorrow: read `kill_switch_state.triggered_at` BEFORE any `start`/`restart` — ⛔ never
restart while a manual stop is standing** (`STOP_PROCEDURE_06-Aug §7`).

---

# §7 — NEW ISSUES, EACH SEPARATELY, WITH EVIDENCE

## 🔴 N-1 · **OPS ② LANDED AT 23-Aug 13:18, ⛔ NOT "~19:0x" — AND THE ORDERING INVERTS**

🏷️ `OPENED · record-accuracy · the SUBSTANCE is unaffected.`

🔬 **Three independent measurements agree on 13:18:**

| 🔬 evidence | value |
|---|---|
| unit-file mtime | `/etc/systemd/system/trading-system.service` — **Aug 23 13:18**, md5 `a8ea94babea410135da05ea648dc1f93` |
| `journalctl` | `Aug 23 13:18:23 sudo[177744]: ubuntu : … COMMAND=/usr/bin/systemctl daemon-reload` → `Reloading finished in 268 ms` — ⭐ **the ONLY reload on 23-Aug** |
| the integrity control | CRITICAL sentinel `20260823_131831_2b42fc55` at **13:18:31.438** — *"/etc/systemd/system/trading-system.service content changed (sha256 `7ad85a562ae2`→`faa2cac56bc2`)"* |

⇒ 🔬 **File written, `daemon-reload`, and alert — all inside ~8 seconds at 13:18.** There is no later
reload, so *"landed ~19:0x"* cannot be rescued as *"edited early, took effect later"*.

🔴 **WHY IT IS NOT PEDANTRY:** the record places OPS ② **after** the 13:22 and 21:44 pushes;
🔬 it actually landed **4 minutes BEFORE the first push**. ⇒ **the causal ordering asserted in
`ROLLBACK_AND_ATTENDANCE` §"NOTE ON F2" and in the Monday card is inverted.** 👤 Rama had exit-5
protection in force for **all three** pushes, ⛔ not merely the last.
⭐ It appears in ≥2 places: the Monday card §0, and the runbook's F2 correction table.

✅ **The substance is independently re-measured today and holds:** `RestartPreventExitStatus=3 4 5`,
`Restart=on-failure`, `RestartUSec=10s`, `StartLimitBurst=5`, `StartLimitIntervalUSec=10s`.

🔬 **Applied by editing the MAIN unit file, ⛔ NOT via the prepared drop-in** — `DropInPaths` lists
only `/etc/systemd/system/trading-system.service.d/watchman.conf` (Jun 11); ⛔ there is no
`exit5-no-restart.conf`.
⭐ **That turned out to be the LUCKY choice:** the main unit file **IS** integrity-watched at CRITICAL,
so the change alerted. The record notes the **drop-in directory is NOT watched** ⇒ the prepared
drop-in would have landed **silently**. 🔬 The control fired and delivered. ⛔ Recorded, ⛔ not chased.

## ⚠️ N-2 · **THE THIRD PUSH LANDED 22:58:35, ⛔ NOT "22:2x"**

🔬 From `checkout -f` write times on the deployed tree — each file is rewritten only when its content
changes, which is *why* the three timestamps differ; that difference is the control:

| file | mtime | ⇒ push |
|---|---|---|
| `config/system_config.yaml` (last changed in `742d9da`) | **2026-08-23 13:22:51.994** | `742d9da` ✅ matches "13:22" |
| `main.py` (last changed in `2f67bb8`) | **2026-08-23 21:43:32.174** | `2f67bb8` ✅ ≈ "21:44" |
| `scripts/security_monitor.py` (changed only in `195436b`) | **2026-08-23 22:58:35.338** | 🔴 `195436b` — **"22:2x" is wrong by ~36 min** |

⛔ Low consequence today. ⭐ Logged because it is the same class as N-1, and because that makes
**three timestamp errors in one weekend's record** — all in the direction of a tidier story.

## ⚠️ N-3 · **THE CONFIG CHANGE RAISED NO SENTINEL — ⭐ CHECKED, AND IT IS BY DESIGN**

🔬 `config/system_config.yaml`'s sha256 moved `ec792551482c` (`4568385`) → `2d5c4190b987` (`742d9da`
onward), and `security_state.alerted` carries `file:system_config:2d5c4190b987` — yet **only one**
sentinel exists on 23-Aug. 🔬 Explanation, `config/security.yaml:133`:
`{ path: …/config/system_config.yaml, severity: WARNING, label: system_config }` — ⛔ WARNING, not
CRITICAL ⇒ no sentinel, by design. `unit_trading` is CRITICAL, hence the 13:18 sentinel.
⇒ ✅ **Not a gap. Recorded so the absence is not re-investigated as one.**
⚠️ ⭐ It does, however, compose with the runbook's ADDENDUM §4 finding: a config change on the
deployed path already produces no operator-visible signal from `startup_checks` — and the integrity
watcher's signal for it is sub-CRITICAL too. 🏷️ **F11 shape. ⛔ Not in scope.**

## ⚠️ N-4 · **`MEMORY_BOARD.md`'s TOP LINE IS STALE — `fix/ni-batch-23aug` HAS SHIPPED**

📄 Board line 1: *"`D-4` PUSH SCOPE IS THE HIGHEST-VALUE OPEN ITEM — SEVEN COMMITTED NI FIXES WAIT ON
IT ALONE (`fix/ni-batch-23aug` b397806, 8 commits, gate clean)"*.
🔬 `b397806` is **inside** `4568385..195436b` and is **deployed** ⇒ the item it names is closed.
⛔ **NOT corrected** — §8 forbids memory work today. 🏷️ **Owed at the next authorised memory pass.**

## ✅ N-5 · **NO OTHER NEW FAULT SIGNAL TODAY** — and the check was wide enough to have found one

🔬 **Search width, stated:** whole-day `logs/system_2026-08-24.log` (2.01 MB — **11,389 INFO /
139 WARNING / 6 ERROR / 1 CRITICAL**) + `logs/reconciler_2026-08-24.log` + every
`data_store/critical_alert_*` + `security_state.json` + `system_events`.
🔬 **CRITICAL = 1**, and it is the routine kill-auto-clear at 08:15:21.
🔬 **Pending sentinels (`*.flag`) = 0** — the watcher has delivered everything.
🔬 Today's only delivered sentinel is the routine 09:19:47 daily one
(`critical_alert_20260824_091947_f1cc205c`, 11,179 B), whose size matches the 19/20/21-Aug 09:19
sentinels (11,180 / 11,177 / 11,179 B) ⇒ ⭐ routine.
🔬 `daemon-reload` count today: **0** ⇒ nothing has altered the unit since 23-Aug 13:18.

---

# §8 — WHAT WAS **NOT** DONE (⭐ scope kept)

⛔ No code · ⛔ no push · ⛔ no deploy · ⛔ no commit · ⛔ no F2 re-anchor · ⛔ no NI-16 · ⛔ no F13 leg ·
⛔ no F11/F14 sweep · ⛔ no D-1b / D-3 · ⛔ no morning-timing change · ⛔ no sector work ·
⛔ no memory write · ⛔ no `AUTO-INSTALLED` repair · ⛔ no systemd md5 copy · ⛔ no `--resume` ·
⛔ no service start / stop / restart of anything ·
⛔ **nothing written to the VM — every VM command in this session was a read.**
⚠️ 👤 **EIGHT DECISIONS REMAIN WITH RAMA. ⛔ None is unblocked by a clean boot.**

**Only two files were written — both on the PC, both untracked, neither pushed:**
`docs/audit/BOOT_PROVEN_24-Aug-2026.md` (this file), and the operative-SHA advance in
`docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md` (see §3).
