# MONDAY VERIFICATION — 07-Sep-2026

Factual record of the first CNC trading day since the 04-Sep delivery disable.
All verification read-only against the live VM at deployed SHA `20061b6`.
⛔ No production configuration was changed as part of this record. No push.

---

## 1. The chain, in order, with figures (SEC-5.1)

Every step verified independently; each figure is quoted from a command run this session.

### 1.1 Config revert — 07:41
The VM cron entry (line **149 of 149**) fired `revert_delivery.sh`:
```
=== 2026-09-07T07:41:01+05:30 revert starting ===
  checkout rc=0
RESULT: REVERTED OK -- all 3 assert enabled: true
```
🔬 Took the **normal path** via `refs/heads/main`, not the `.bak` fallback ⇒ no `user.crit` raised.
🔬 Independently confirmed on the live files: all 3 delivery YAMLs `enabled: true` at line 11.
🔬 Crontab still **149 lines**, entry intact ⇒ no push occurred. Deployed bare `refs/heads/main`
= `20061b6`, **0 tracked-file drift**.

### 1.2 Clean boot — 08:15:21
🔬 `systemctl`: active since **08:15:21 IST**, `NRestarts=0` ⇒ cold boot, not a restart.
🔬 `run_all_startup_checks: OK scenario=CRASH warnings=[]`
- `scenario=CRASH` is the **normal cold-boot shape** — identical on 03-Sep and 04-Sep. `WARM` is the
  mid-session-restart shape. It is not a fault.
- ⭐ `warnings=[]` vs 04-Sep 09:31's `warnings=['temp_config_values(3)']` is an **independent second
  confirmation** that the TEMP disable is gone at the config layer, not merely in the YAML text.

🔬 Stale kill switch cleared at 08:15:21.810: *"auto-cleared: prior SOFT_KILL from 2026-09-04
(reason=circuit_breaker_force_close_15:15 by=order_monitor) — new day 2026-09-07 starts clean
(HEADLESS)"*. 🔬 Zero non-kill-switch ERROR/CRITICAL in `logs/system_2026-09-07.log`.

### 1.3 `will_trade_count = 15` — 08:15:35
🔬 All three positional strategies back in `will_trade`; `pb01_breakout_retest` the sole `wont_trade`.
15 = the 12 already-enabled + the 3 restored. Matches the expected value exactly.

### 1.4 Authenticated webhook traffic
🔬 Auth precedes both 403 branches: `_authenticate` → **401 at `webhook_receiver.py:518`**; kill-switch
403 at `:537`; entry-window 403 below it. ⇒ **a 403 is a POST-authentication refusal.**
⭐ This makes the morning's 403s positive evidence: those requests presented a valid token.

### 1.5 403 → 200 window transition — clean
🔬 last 403 `09:59:16` · first 200 `10:00:24` · **zero 403s after 10:00**.
⭐ Corroborates the kill switch being inactive: an active one produces *in-window* 403s, which the
23-Jul investigation records as otherwise inexpressible.

### 1.6 Scanner roster — 11 at 12:30
🔬 Per-scanner `c401 = 0` for **every** scanner ⇒ each authenticated independently.
🔬 Delivery strategies accepting signals: `positional_sector_rotation` **660**,
`positional_momentum_long` **346**, `positional_swing_long` **62**.

### 1.7 Actual CNC orders
🔬 `orders` today by product: **CNC ENTRY COMPLETE 3, CANCELLED 1**; MIS ENTRY 5, SL 4, TGT 4.
⚠️ CNC carries **no SL/TGT order rows by design** — delivery protection is GTT, held separately.

### 1.8 Independently verified GTT protection
🔬 At 13:22:51 the CNC book read: MVGJL **CLOSED (`GTT_EXIT`)**, QUICKHEAL **CLOSED (`GTT_EXIT`)**,
TEXRAIL **OPEN qty 4**, MAFANG/SKIPPER FAILED qty 0.
🔬 `gtt_state` for TEXRAIL: gtt_id `334980620`, `status=ACTIVE`, `needs_review=0`,
`last_verified_at=13:18:42` — a re-verification, not a write-once flag.
⭐ **Two positions exited through `GTT_EXIT` during the session** ⇒ the delivery protection mechanism
is not merely recorded, it **fired and completed**.

---

## 2. THE 10:20 CORRECTION (SEC-5.2)

⛔ **"13 distinct scanners by 10:20" is the wrong checkpoint. 13 is a FULL-DAY figure.**

🔬 Measured on 04-Sep, the prior trading day — **only 9 had posted by 10:20**:

| scanner | first post 04-Sep |
|---|---|
| positional_momentum_long / positional_sector_rotation | 09:18 |
| gap_go_long / vwap_bounce_long | 09:23 |
| first_pullback_long | 09:24 |
| positional_swing_long / open_low_breakout_long | 09:25 |
| vwap_rejection_short | 09:45 |
| open_high_breakdown_short | 09:54 |
| **gap_go_short** | **10:33** |
| **first_pullback_short** | **10:36** |
| **gap_fade_short** | **10:39** |
| **gap_fade_long** | **12:06** |

⇒ The 13th scanner did not arrive until **12:06**. A 10:20 reading of 9–12 is the **normal shape**.
⛔ Read literally, the 10:20 checkpoint would have failed on the last trading day and manufactures a
false alarm on a clean morning. **Take the count at 12:30+; at 10:20 read only the 401.**
Day total 04-Sep = **14** = the 13 + `pb01_breakout_retest` at 17:00.

---

## 3. THE F6 LIMIT (SEC-5.3) — stated in full, not softened

> Today's two protected positions are evidence about **THOSE positions**. They are **NOT** evidence
> that F6 is fixed. F6 remains **unfixed, batch 2, unauthorised.**

⭐ The observed `GTT_EXIT` closures likewise evidence those specific exits — not the F6 predicate.

---

## 4. TOKEN PROOF — exact wording (SEC-5.4)

✅ **"zero 401s across the 11 scanners that posted"** — proven. 🔬 `401 = 0` across **1,762** requests
(FINAL 12:35:37), per-scanner `c401 = 0`.

⛔ **"all 16 alerts proven on the new token"** — **FALSE, and it stays false.**

Unproven at the time of writing:
| alert | status |
|---|---|
| `pb01_breakout_retest` | posts ~17:00; watch armed, result pending |
| `gap_go_short` | had not posted by 12:30 |
| `open_high_breakdown_short` | had not posted by 12:30 |
| `range_breakout_long` / `range_breakout_short` | ⛔ **PERMANENTLY configuration-verified only** — 0 rows in 223,484; cannot be runtime-proven |

⇒ After PB01: **12 proven at runtime, 2 permanently config-only**, plus whichever shorts posted.
⛔ A scanner with no POST is indistinguishable between bad config and no matching signal — absentees
are recorded, not investigated.

---

## 5. TRADE-COUNT RECONCILIATION (SEC-5.5)

⚠️ Two figures were reported that appeared to disagree — **"7 trades today"** and **"6 of 14 created
today"**. The disagreement was a **model error**, not a typo. Two faults:

1. **Two different date columns.** "7" filtered `entry_time`; "14" filtered `created_at` through a
   JOIN. They count different things and were both labelled "trades today".
2. **The corpus is live-moving.** An unstamped count of an intraday table is meaningless.

**One query, one corpus (trades CREATED today), frozen at `13:43:55 IST`:**

| created_today | reached_entry | never_entered | CLOSED | OPEN | FAILED | REJECTED |
|---|---|---|---|---|---|---|
| **20** | **7** | **13** | 6 | 1 | 11 | 2 |

Identities that close it:
- `created_today (20) = reached_entry (7) + never_entered (13)`
- `reached_entry (7) = CLOSED (6) + OPEN (1)`
- `never_entered (13) = FAILED (11) + REJECTED (2)`

⇒ **Reconciled figure: 20 trades created, 7 reached entry, 13 never entered.** The earlier "7" was
correct for *entered*; the earlier "14" was a smaller, earlier snapshot of *created*.

---

## 6. SELF-CORRECTION — `gap_fade_long` (SEC-5.6)

⚠️ I reported `gap_fade_long` as having posted at **10:43** today. **Wrong.** That timestamp came from
a historical row: the query selected the most recent payload **per scanner across all history**, not
today (two rows in the same result read `2:59 pm`, which cannot be an 11:06 snapshot).

🔬 Corrected by measurement: `gap_fade_long`'s **first post today was `09:31:15`** — genuinely well
ahead of 04-Sep's 12:06, so the conclusion survived while the figure did not.

⭐ Recorded because a corrected error that is not written down gets repeated. The generalisable rule:
**an aggregate "most recent per group" is not scoped to today unless the date predicate is inside the
subquery.**

---

## 7. What this record does NOT claim

- ⛔ Not a claim that F6 is fixed (§3).
- ⛔ Not a claim that all 16 alerts are token-proven (§4).
- ⛔ Not an explanation of the 13 never-entered trades — registered for batch 2, deliberately
  uninvestigated (SEC-8 R1).

---

*🔬 All figures measured read-only via `?mode=ro` against `data_store/trading_system.db` and the live
service at deployed SHA `20061b6`, 07-Sep-2026. Line numbers hold at that SHA only (M3). Snapshot
times are stated wherever the underlying table was still moving.*
