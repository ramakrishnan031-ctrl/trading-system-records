# CARRY-DAY CARD — 25-Aug-2026 (Tue) · RESULT

**Session scope:** OBSERVE · MEASURE · RECORD. Nothing built, nothing pushed, nothing tuned.
**Measured:** 25-Aug 08:41 → 08:48 IST, from the VM (`trading-vm`), all reads.
**Provenance:** 🔬 measured · 📄 source-derived · 💭 inference · 👤 Rama.

---

## 🔴 HEADLINE — THE CARD'S §3 AND §4 PREMISES ARE BOTH FALSE

🔬 **Nothing carried overnight.** Both positions the card names as carried were **CLOSED on 24-Aug
via `GTT_EXIT`**, hours before the card was issued.

| symbol | trade_id | entry | exit | exit_reason | net_pnl | product |
|---|---|---|---|---|---|---|
| KAMATHOTEL | `trd_50cf0040…` | 24-Aug 10:05:32 | **24-Aug 11:31:29** @ 228.14 | `GTT_EXIT` | +₹14.00 | CNC |
| BALUFORGE | `trd_00971394…` | 24-Aug 10:03:46 | **24-Aug 12:47:50** @ 628.40 | `GTT_EXIT` | +₹16.35 | CNC |

🔬 `gtt_state`: both rows **`status = CLEANED`** (`gtt_id` 333026682 `updated_at` 11:31:29;
`gtt_id` 333025881 `updated_at` 12:47:50).
🔬 `trades`: **ZERO rows** in `OPEN` / `PARTIAL` / `PENDING_FILL`. Every row is
`CANCELLED` (9) · `CLOSED` (240) · `CLOSED_MANUAL` (52) · `FAILED` (343) · `REJECTED` (80).

⇒ 🔴 **THE CARRY TEST IS STILL NOT EVALUABLE.** ⛔ Not "passed". ⛔ Not "did not fire".

📄 **Where the false premise came from:** `docs/audit/BOOT_PROVEN_24-Aug-2026.md:236-237` records the
24-Aug series **"581 samples by 10:42"** — a *mid-morning snapshot*. At 10:42 both positions were
open, and the doc inferred (`:294-296`) *"The two CNC positions below carry into T+1"*. They did not:
they hit their GTT targets at 11:31 and 12:47. ⚠️ **The card was ISSUED at 13:45 — after both
exits.** The doc labelled the downstream exposure 💭 *inference*; the card promoted the same
claims to 🔬 *measured*.

---

## §1 — DID LAST NIGHT'S MANUAL STOP HAPPEN?

🔬 **NO MANUAL STOP IS EVIDENCED, AND NONE WAS NEEDED.**

- **S-1** `systemctl show trading-system`:
  `InactiveEnterTimestamp=Mon 2026-08-24 17:35:04 IST` · `Result=success` · `NRestarts=0`
  `ExecMainStartTimestamp=Tue 2026-08-25 08:15:19 IST` · `ActiveState=active` `SubState=running`
- 🔬 **The discriminator:** `journalctl -u trading-system.service` over the whole of 24-Aug contains
  **`Deactivated successfully` at 17:35:04 and NO `Stopping trading-system.service…` line.**
  A `systemctl stop` on an *active* unit always emits `Stopping…` first. ⇒ 📄 **this was the EOD
  self-exit (clean exit 0), not an operator stop.** If Rama issued the stop after 17:35:04 it was a
  no-op against an already-inactive unit and would log nothing.
- **S-2** 🔬 `system_events` `SHUTDOWN` **`event_id 3789` @ `2026-08-24T17:35:04.509578+05:30`**.
  Lifetime counts moved **78 STARTUP / 76 SHUTDOWN → 79 / 77** (+1 each), exactly as one clean
  shutdown plus one clean boot predicts.
- **S-3** 🔬 `kill_switch_state`: **`state = INACTIVE`**,
  `triggered_at = 2026-08-25T08:15:20.404871+05:30`,
  `reason = auto_clear_stale: was SOFT_KILL from 2026-08-24 (circuit_breaker_force_close_15:15)`,
  `triggered_by = main.auto_clear_stale`. ⇒ ✅ **the prior-day kill auto-cleared; today starts clean
  and TAKES ENTRIES.**

⭐ **Why no manual stop was required:** the invariant is *a **carried delivery position** blocks
shutdown*. 🔬 The book was **flat** by 15:00 (below). Its precondition was never met, so the service
self-exited normally, `token_watcher` found it inactive at 08:15 and started it. ⛔ **This is NOT a
counter-example to the carry-blocks-shutdown rule** — that rule was simply not engaged.

---

## §2 — THE BOOT GATE: ✅ PROVEN

| check | result |
|---|---|
| **V-5** `ExecMainStartTimestamp` | 🔬 `Tue 2026-08-25 08:15:19 IST` |
| **V-6** `STARTUP` row in `data_store/trading_system.db` | 🔬 **`event_id 3791` @ `2026-08-25T08:15:31.423057+05:30`**, `scenario=COLD`, `details={"mode":"live","version":"2.0.0"}` — **12.4 s AFTER V-5** ✅ |
| **V-2** `origin/main`, two independent measures | 🔬 PC `git ls-remote origin refs/heads/main` = `195436bb6323c981d68f313ad7c39858cc0a4653` · VM raw `cat /home/ubuntu/trading-system.git/refs/heads/main` = **same** |
| **V-3** deployed HEAD | 🔬 `195436bb6323c981d68f313ad7c39858cc0a4653` |
| **V-4** deployed tree drift | 🔬 **0 files** (`diff-index` vs HEAD under a throwaway `GIT_INDEX_FILE` + `update-index --refresh`) |
| `NRestarts` | 🔬 **0** ⇒ single attempt; the *"earlier same-day row from a different attempt"* trap is **not reachable** |
| boot health | 🔬 `grep -c "Config load failed" logs/system_2026-08-25.log` = **0**; only CRITICAL today is the `kill_switch` startup notice that then auto-cleared |

⭐ **`origin/main` is unchanged since 23-Aug 22:58.** Per the card's §0, today's proven boot is a
re-proof of the **same** SHA ⇒ ⛔ **the rollback target does NOT move.** It stays `195436b`. No
action was taken and none is recorded.

---

## 🔴 §3 — THE CARRY TEST

### C-1 / C-2 — the series

🔬 `G3 MARGIN_RECON` is a **DEBUG** line (`orders/order_reconciler.py:3709-3715`). ⚠️ It is **NOT** in
`logs/system_<date>.log` — that file returns **0 hits**. It lives in
**`logs/reconciler_<date>.log`** and `logs/debug_<date>.log`.

🔬 **Today, 08:15:28.725 → 08:47:42.650 — 130 samples, ONE distinct tuple:**

```
G3 MARGIN_RECON: held=0.00 carry=0.00 held_today=0.00 broker_used=0.00 residual=0.00
```

🔬 **`carry = 0.00` on 130 / 130 samples.**

⚠️ ⭐ **Note the zero-variance across the WHOLE row, not just `carry`** — `held`, `held_today`,
`broker_used` and `residual` are all `0.00` too. That is **consistent with a genuinely flat book**
(corroborated independently by the `trades` and `gtt_state` reads above), ⛔ **not** with a
pre-market read that has not yet synced. It is the honest reading, not a convenient one.

### C-3 — `broker_used` for a SETTLED CNC holding

🔴 **STILL UNMEASURED. THE OWED MEASUREMENT STANDS.** 📄 `order_reconciler.py:3704-3708` still reads:
*"broker `used` for a SETTLED CNC holding is unmeasured … Owed: measure a T+1 carry, then decide a
threshold."* ⛔ No T+1 carry has occurred, so nothing can be recorded against it.

### C-4 — `CAPITAL_DRIFT` counts

🔬 **ERROR alerts today: 0. Suppressed / throttled: 0.**
⭐ **Search width, stated beside the zero (memory rule):** the literal is `G3 CAPITAL_DRIFT`
(ERROR, `:3679`) and `G3 CAPITAL_DRIFT skipped` (INFO, `:3735`). The same grep across `logs/` finds
**1,977 hits on 14-Aug**, 723 on 20-Aug, **25 on 21-Aug** — so the pattern demonstrably fires.
**`2026-08-24` and `2026-08-25` appear in NO log file's hit list**, across `system_*`, `debug_*` and
`reconciler_*`. ⇒ 📄 the zero is a real zero, not a wrong grep.
⭐ And the check is **live, not dead**: `MARGIN_RECON` is emitted from inside `_g3_capital_drift`,
130 times today.

### 🔴 THE REVERT TRIGGER

> **NOT FIRED — and NOT EVALUABLE.**

🔬 `residual = 0.00` on every one of today's 130 samples. None of **₹1,051.57 · ₹610.45 · ₹441.12**
appeared. ⛔ **This is not a pass.** ⭐ One flat day is not evidence about the carry case, in either
direction. ⛔ Nothing was tuned; `capital_drift_tolerance` and `capital_drift_tolerance_pct` were not
touched, read-only.

### ⚠️ 🔴 A TRAP IN THE TRIGGER ITSELF — NEW, AND IT MATTERS

🔬 **On 24-Aug two of the three trigger values DID appear as residuals — with `carry = 0.00`:**

| samples | tuple |
|---|---|
| **55** | `held=1051.57 carry=0.00 held_today=1051.57 broker_used=610.45 residual=441.12` |
| **46** | `held=699.56  carry=0.00 held_today=699.56  broker_used=89.18  residual=610.37` |

📄 These are **same-day broker `used` settlement lag** — `held_today` jumps on a fill while the
broker's `utilised.debits` has not caught up. They are ⛔ **NOT** the carry algebra failing.
🔴 **⇒ Anyone matching the revert trigger on the NUMBER ALONE would have fired a false REVERT on
24-Aug.** ⭐ **The trigger is only meaningful with `carry > 0` as an explicit precondition.**
⛔ Recorded, not acted on.

---

## §4 — WHAT THE 15:45 WINDOW DID: ALSO NOT EVALUABLE

🔬 **The book was flat well before 15:45.** Last non-zero sample: **`14:55:00.766`**
(`held=89.11`). By **`15:00:03.216`** `held=0.00`, and it stayed 0.00 for the rest of the day.

| day | MARGIN_RECON samples at/after 15:45 | of those, `held > 0` |
|---|---|---|
| 21-Aug | 437 | **0** |
| **24-Aug** | **436** | **0** |

⭐ **Method cross-check (a green check that could have been red):** the same extraction reproduces
the previously-recorded 21-Aug figure — **437 / 0** — exactly. So the 24-Aug row is measured with a
method proven against the record.

- **W-1** 🔬 `CAPITAL_DRIFT` alerts between 15:45 and the 17:35:04 stop: **0 at ERROR, 0 suppressed.**
- **W-2** n/a — none fired.
- **W-3** 🔬 The window ended at the **17:35:04 self-exit**, not at an operator stop.

⇒ 🔴 **The flat-₹50-band exposure has STILL never met a non-empty book.** 💭 The 24-Aug prediction of
*"repeat CRITICALs plausible this evening"* did not occur **because its precondition
(`held = ₹1,169.45` after 15:45) was false** — ⛔ not because the exposure was disproved.
⛔ `capital_drift_tolerance_pct` untouched.

---

## §5 — THE TWO SMALLER OBSERVATIONS

**N-14 — ⛔ NOT EXERCISED. AGAIN.**
🔬 `data_store/security/last_run.json` @ 08:45:11 (fresh, rewritten ~61 s):
`checks_run 10 · clean **true** · findings_count **0** · max_severity "INFO" · persistent_count 0`.
🔬 24-Aug 17:05 control-tower run (`logs/cron-control-tower.log`, `run_id 77f765c6…`):
`'security': 'ok'` · `findings_total 2` · `CRITICAL 0, HIGH 0, MEDIUM 2, LOW 0` · `overall_status
HEALTHY`. ⭐ Both MEDIUMs come from the `cron: warn` source, ⛔ not from `security`.
⇒ 📄 The discriminating case — **`clean:false` with `max_severity: INFO`** — **did not occur.**
`findings_count = 0` means old and new code both return `ok`. ⛔ **NI-14 remains VACUOUS.**

**N-15 — ✅ STILL HOLDING.**
⚠️ These are **not DB tables** — they are keys in `data_store/security_state.json`
(`scripts/security_monitor.py:767-768`), rewritten ~61 s (mtime 08:46).
🔬 `file_unreadable = {"/etc/sudoers": "unreadable"}` ✅
🔬 `file_hashes`: **7 entries, 0 nulls** ✅ · `/etc/sudoers` absent from `file_hashes` ⇒
⭐ **still skipped, which is F13-L2 and remains unauthorised.** ⛔ Not changed.

---

## §6 — STATE OF THE TREE

- ⛔ **NOT PUSHED.** ⛔ **NOTHING TUNED.** ⛔ No code, no deploy, no service action.
- 🔬 `origin/main` = **`195436bb6323c981d68f313ad7c39858cc0a4653`** — unchanged, both measures.
- 🔬 Deployed tree drift **0**. Every VM call this session was a **read**.
- 🏷️ Rollback target stays **`195436b`** — ⛔ not advanced (same SHA re-proved).

---

## §7 — NEW ISSUES

**NEW-1 · 🔴 The card's §3/§4 premises were already false when the card was issued.**
Both exits (11:31:29, 12:47:50) preceded the 13:45 issue time. 📄 The 24-Aug audit correctly
labelled the downstream claim 💭 *inference*; the card restated it as 🔬 *measured* and built a
revert trigger, an expected-value table and a whole session's scope on it.
⭐ **Countermeasure:** a dated prediction about a position must be **re-measured at use time**, never
carried forward from the snapshot that produced it — the same shape as the standing rule that
`origin/main` is resolved at gate time and never from a SHA written into a card hours earlier.

**NEW-2 · 🔴 The revert trigger is matchable by a non-carry transient (details in §3).**
Residuals of **441.12** (55 samples) and **610.37** (46 samples) occurred on 24-Aug with
`carry = 0.00`. ⭐ The trigger needs `carry > 0` stated as an explicit precondition, or it will fire
falsely on ordinary same-day settlement lag. ⛔ Recorded only.

**NEW-3 · ⚠️ Broker 503 outage, 24-Aug 17:20 (post-session, low impact).**
🔬 4 × `503 Service Unavailable` from Zerodha at **17:20**, all within the same minute.
Raised `get_gtts` → `cnc_gtt_adoption: get_gtts failed`, and `get_positions` →
**1 × `order_reconciler: reconcile_once unhandled error`**.
🔬 Recovered — `MARGIN_RECON` samples continue normally through to 17:35:00. Book was already flat
and the session was over, so no position was exposed. 🔬 **0 occurrences on 25-Aug so far.**
⛔ Recorded, not investigated further (out of scope).

---

## ⭐ WHAT WOULD MAKE THE CARRY TEST EVALUABLE

📄 One precondition, and only one: **a CNC position must still be open at the 17:35 self-exit**, so
that `snapshot.intraday_carry + snapshot.positional_carry` is non-zero at the *next* 08:15 boot.
⭐ The cheapest way to know whether tomorrow is the carry day is a **single read at ~15:30 today**:
any row in `trades` with `status IN ('OPEN','PARTIAL','PENDING_FILL')` whose ENTRY order `product`
is `CNC`. ⛔ Not done — outside this card's scope, and 👤 Rama's call.

⛔ **Note the standing consequence:** if a CNC position *does* stay open tonight, the 24-Aug
carry-blocks-shutdown invariant engages, the service will **not** self-exit, and a **manual stop
becomes necessary** — otherwise there is no 08:15 boot tomorrow and the day takes no entries.
