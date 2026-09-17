# FILE 20 — THE TEN CORRECTIONS APPLIED · AND THE 28-Aug-2026 08:15 BOOT PROOF

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ VACUOUS / NOT EXERCISED.

**Verdict, in one line:** ✅ **BOOT PROVEN at `52ccb4f`** (L-1 satisfied) ·
✅ **UNIT 3a EXECUTED** · ✅ **UNIT 1 EXECUTED at 10:15:13** — ⚠️ but ⛔ **NOT the T+1 arm**,
and ⛔ **not load-bearing** in the one GTT exit that followed (§1-B-iv).

> 🔴 **SUPERSEDED WITHIN THE DAY, AND THE SUPERSEDED TEXT IS RETAINED, ⛔ NOT DELETED.**
> At **08:40** this record read *"🔴 **UNIT 1 NOT EXECUTED — no CNC position existed** ⇒
> deployment proven, execution ⛔ NOT proven."* ⭐ **That was TRUE when written** — 0 positions,
> 0 holdings, 0 ACTIVE GTTs. It stopped being true at **10:05:49**, when the first CNC
> entry of the day filled. ⭐ The three-way answer is a **statement about a moment**, ⛔ never
> a permanent property, and this is the clearest possible demonstration of why.

---

## §0 — MEASUREMENT BASIS

🔬 Every VM figure below was read **read-only** over `ssh trading-vm` between
**08:26 and 08:40 IST on 28-Aug-2026**. ⛔ Nothing was written to the VM. ⛔ The
service was not restarted, stopped or touched. ⛔ No config, code or DB row changed.

⭐ **PC side, stated in full so nothing is implied to be read-only that is not:**
the serial test gate (§1-D) **executed tests** in an existing worktree at `52ccb4f`
and ⛔ edited no source; the two memory guards (§2 C-10) were **re-run**; and three
files were **written** — this record, `MEMORY.md`'s hot header, and the standing
ledger. 🔬 **ROOT is untouched at `feat/delivery-config-split @ 6d24a83`**, and this
record is the only new path in the repo.

⚠️ **FILE 20 was issued 27-Aug 19:25 for "tomorrow 08:15". That is THIS morning.**
The boot had already happened (08:15:13) when work began at 08:26 ⇒ §1-A is a
**post-hoc measurement of a boot that was not observed live**. ⛔ It is not a
pre-boot control. The L-1 test does not require one — it compares two independently
recorded timestamps — but the distinction is recorded rather than glossed.

---

## §1 — THE BOOT · FILE 20 §2 ORDER A–H, ⛔ NOT REORDERED

### A · BOOT — ✅ **PROVEN**

| fact | command | result |
|---|---|---|
| `origin/main` / bare `HEAD` | `git --git-dir=/home/ubuntu/trading-system.git rev-parse HEAD` | `52ccb4f4f0c303ff47037ca492d5eec7536b01b8` |
| same, 2nd way | `cat /home/ubuntu/trading-system.git/refs/heads/main` | `52ccb4f4…` — **agrees** |
| tracked drift | `update-index --refresh` + `diff-index --name-only HEAD --` | **0 files** |
| deploy instant | `reflog show HEAD --date=iso` | `52ccb4f … 2026-08-27 19:03:14 +0530: push` **and** `: checkout` — **both halves** |
| service | `systemctl show` | `ActiveState=active` · `SubState=running` · `Result=success` · `ExecMainStatus=0` · **`NRestarts=0`** |
| **`ExecMainStartTimestamp`** | `systemctl show` | **`Fri 2026-08-28 08:15:13 IST`** · `ExecMainPID=574218` |
| the start itself | `logs/token_watcher.log` | `[2026-08-28 08:15:13 IST] Fresh token detected (daily start, in service window). Starting trading-system.service.` |

🔬 **Exactly ONE start event exists for the whole day** — `journalctl -u
trading-system.service --since "2026-08-28 00:00"` contains a single matching line,
`Aug 28 08:15:13 … Started trading-system.service`, and ⛔ **no** `Stopped`,
`Failed` or `Deactivated`. ⇒ `NRestarts=0` is corroborated by the journal, ⛔ not
taken from `systemctl` alone. 🔬 `data_store/session/zerodha_token.json` mtime
**`Aug 28 08:15`** — the token refresh that gated the start.

⭐ **The drift check is not vacuous** — the same command against a different
tree-ish prints: `git diff-index --name-only bc9a9f5 --` lists the six files that
differ (`config/system_config.yaml`, `core/config_loader.py`,
`orders/cnc_gtt_monitor.py`, and the three test files). ⇒ an empty result against
`HEAD` is a **measurement**, ⛔ not a silent no-op.

#### ⭐ L-1 — the only definition of "proven to boot"

```
sqlite3 -readonly data_store/trading_system.db \
  "SELECT * FROM system_events WHERE event_type='STARTUP' AND date(timestamp)=date('now','localtime');"
→ 3801|2026-08-28T08:15:25.978225+05:30|STARTUP|COLD|{"mode": "live", "version": "2.0.0"}
```

🔬 **`08:15:25.978225` > `ExecMainStartTimestamp 08:15:13`** ⇒ the row belongs to
**THIS** boot attempt. 🔬 It is the **only** `STARTUP` row today, so ⛔ no earlier
same-day row can be mistaken for it. ✅ **L-1 SATISFIED.**

⭐ **The three-boot chain is now unbroken, each link measured the same way:**

| tree | boot | `ExecMainStartTimestamp` | `STARTUP` row | verdict |
|---|---|---|---|---|
| `75e637c` | 26-Aug | 08:15:18 | `3794` @ 08:15:29.559643 | ✅ proven |
| `bc9a9f5` | 27-Aug | 08:15:15 | `3797` @ 08:15:27.356543 | ✅ proven |
| **`52ccb4f`** | **28-Aug** | **08:15:13** | **`3801` @ 08:15:25.978225** | ✅ **proven** |

#### Startup scenario actually selected · recovery errors

🔬 `STARTUP` row column 4 = **`COLD`** — the authoritative value, ⛔ not inferred
from a log string.
🔬 **`ERROR` lines today: 0.** 🔬 **`CRITICAL` lines today: 1**, and it is the known
designed pair:

```
08:15:14.287 CRITICAL kill_switch  KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL reason=circuit_breaker_force_close_15:15 …
08:15:14.290 (system_events)       KILL_AUTO_CLEARED  prior SOFT_KILL from 2026-08-27 … new day 2026-08-28 starts clean (HEADLESS)
```

⭐ Resolved **3 ms** later by design. 🔬 **`WARNING` lines: exactly 2** — the
auto-clear above and `CONFIG_UNACCESSED` (§1-C). 🔬 `journalctl -u
trading-system.service` for `08:15:00–08:16:30` contains nothing beyond these.
✅ **No unexpected recovery errors.**

---

### B · UNIT 1 (F6-leg, `b5d6c8b`) — ✅ **EXECUTED at 10:15:13** (was 🔴 NOT EXECUTED at 08:40)

#### B-i · The running service DOES import the shipped line — ✅ **PROVEN**

| step | measurement |
|---|---|
| the line is deployed | `orders/cnc_gtt_monitor.py:482` = `held[sym] = held.get(sym, 0) + max(0, int(qty))` |
| the deployed bytes ARE the shipped bytes | `md5sum` = **`094b2884e9b8393e40d002d3f0d0018b`** == `git cat-file blob 52ccb4f:orders/cnc_gtt_monitor.py \| md5sum` — **identical** |
| written at the deploy instant | `mtime 2026-08-27 19:03:14.978543948 +0530` = the reflog checkout second |
| ⛔ not mutated afterwards | `find . -name '*.py' -newermt '2026-08-27 19:03:15'` → **empty** |
| ⭐ **and the RUNNING process compiled it** | `orders/__pycache__/cnc_gtt_monitor.cpython-312.pyc` mtime **`2026-08-28 08:15:14.099`** — inside this boot, ~1 s after `ExecMainStartTimestamp` |
| the process is the deployed tree | `/proc/574218/cwd → /home/ubuntu/systems/trading-system` · cmdline `…/venv/bin/python …/main.py --mode live` |

⭐ The `.pyc` timestamp is the strong link: CPython recompiles **only** when the
source is newer than the cached bytecode, so a `.pyc` stamped *during this boot*
proves the shipped source — ⛔ not a stale cache — is what the live process holds.

#### B-ii · 🔴 A CORRECTION TO FILE 20's OWN PREMISE — the gate is NOT "a GTT state to reconcile"

⚠️ FILE 20 §2 states the changed line *"only runs when the CNC monitor has a GTT
state to reconcile."* 🔬 **Measured at `52ccb4f`, that is not the condition.**

```
reconcile()  orders/cnc_gtt_monitor.py:108
  :122   gathered = self._gather()                      ← UNCONDITIONAL, and FIRST
  :128   rows = self._store.get_active_gtt_states()     ← the GTT rows come AFTER
```

⇒ `_gather()` runs on **every** reconcile pass whether or not a GTT row exists.
The gate on the **changed line** (`:482`) is narrower and different:

> **the changed line executes iff `get_positions()` returns ≥ 1 entry whose
> `product.upper() == "CNC"` and whose `symbol` is truthy.**

⭐ Holdings do **not** reach it — they are summed one loop earlier at `:459`, by a
**different, unchanged** line (`+ int(qty)`). ⛔ A carried holding alone would not
have executed the fix either. ⚠️ 🔬 M3: these line numbers hold **only** at `52ccb4f`.

#### B-iii · The three-way answer — 🔴 **NOT EXECUTED**

🔬 The adapter **is** instrumented. ⚠️ This narrows an older note: *"`get_gtts` has 0
call sites logged"* is still true **for `get_gtts`**, but `get_positions` and
`get_holdings` log `call_start` / `call_end` with a `result_summary`:

```
08:15:23.353 get_holdings  call_start
08:15:23.368 get_holdings  call_end   result_summary:"0 holdings"
08:15:23.368 get_positions call_start
08:15:23.409 get_positions call_end   result_summary:"0 positions"
```

⭐ That `get_holdings` → `get_positions` pair is `_gather()`'s own order
(`gtts → holdings → positions`, `:438-440`).

🔬 **Bounded window — `08:15:14.211` (first log line) → `08:43:05.681`, re-measured
at 08:43:14: every `get_positions` call, `114 of 114`, returned `"0 positions"`.**
(An earlier tally at 08:31 read `58 of 58`; the ratio is unchanged, the denominator
grows with the 15 s poll — ⭐ the figure is only meaningful with its window.)
🔬 **The single `get_holdings` call returned `"0 holdings"`.**
🔬 `cnc_gtt.hydrated count=0` @ 08:15:23.083 · `SELECT status,COUNT(*) FROM gtt_state`
→ `CLEANED 26 · EXPIRED 1 · TRIGGERED 4` ⇒ **ACTIVE = 0**.

⇒ `positions` was **empty**, so `for p in positions:` never entered its body.

> 🔴 **VERDICT AS AT 08:40: NOT EXECUTED — no CNC position and no active GTT
> state existed.** ⇒ ✅ DEPLOYMENT PROVEN · ⛔ EXECUTION NOT PROVEN.
> ⚠️ **RETAINED VERBATIM. SUPERSEDED AT 10:15:13 — see B-iv.**

⭐ This is the non-vacuity discipline applied to a **code change** rather than a log
absence: a clean boot is **silent** about a line whose qualifying condition never arose.

---

#### B-iv · ✅ **THE CONDITION AROSE. THE LINE EXECUTED.**

🔴 **The qualifying condition appeared at 10:05:49**, when the day's first CNC entry
filled. 🔬 **Three CNC entries opened**, and `max_open_delivery_positions: 3`
(`config/system_config.yaml:230`, **ENFORCED**) then closed the book:

| symbol | qty | entry | `margin_reserved` | GTT | entry time |
|---|---|---|---|---|---|
| OAL | 1 | ₹432.75 | ₹432.7328 | `333734599` | 10:05:49 |
| TEJASNET | 1 | ₹568.65 | ₹568.6604 | `333736980` | 10:11:58 |
| RAMRAT | 1 | ₹592.95 | ₹592.9617 | `333737122` | 10:12:22 |

##### ⭐ `_gather()` RUNS ON A ~15-MINUTE CADENCE — and its log signature is `get_holdings`

🔬 Every `_gather()` today, identified by its `get_holdings call_end` marker:

```
08:15:23.368 · 09:15:02.911 · 09:29:54.277 · 09:45:00.144 · 10:00:05.421 · 10:15:13.098 · 10:30:21.758
```

⭐ **This is why a mid-morning check could have got the wrong answer.** The entries
filled at **10:05:49**; the preceding `_gather()` was **10:00:05**, five minutes
*before* them. ⚠️ A reader sampling at 10:06 would have seen `get_positions -> "1
positions"` and concluded the line had run. ⛔ **It had not.** The `get_positions`
calls every 15 s belong to **other components**; only the `get_holdings`-marked ones
are `_gather`.

##### 🔬 THE EXECUTION, WITH ITS OBSERVED INPUT AND RESULT

| | measurement |
|---|---|
| the `_gather()` | **`10:15:13.098`** (`get_holdings` → `"0 holdings"`) |
| its `get_positions` | **`10:15:13.115`** → **`"3 positions"`** |
| **input to the changed line** | 3 same-day CNC positions, each **`qty = +1`**; holdings **0** |
| **result** | `held = {OAL: 1, TEJASNET: 1, RAMRAT: 1}` — `max(0, +1) = 1`, the **BUY** arm |
| corroboration the pass consumed it | all three `gtt_state` rows carry `updated_at = 10:15:13.115 / .119 / .121` ⇒ `_handle_row` ran with that `held_qty` |
| the door | `held == 0` was **False** for all three — ⭐ **correct**: these are live entries, ⛔ not exits. No row took `_finalize_gtt_exit`; the GTTs stayed `ACTIVE`. |

> ✅ **THREE-WAY ANSWER: EXECUTED — with the observed input and result above.**
> ⛔ **AND STILL NOT THE T+1 ARM.** A same-day BUY takes `max(0, +1)`. The T+1 arm
> needs holdings 0 **and** a position of **−1**.

##### 🔴 B-v · A GTT EXIT FOLLOWED — AND THE FIX WAS ⛔ **NOT LOAD-BEARING** IN IT

🔬 **TEJASNET exited at `10:30:21.803`** — `exit_reason = GTT_EXIT`, exit price
**₹558.00** (the SL leg; trigger was 557.29), `net_pnl` **−₹12.11**, GTT `333736980`
→ **`CLEANED`** at `10:30:21.804`. ⭐ The `_gather()` at **`10:30:21.758`** is **45 ms
earlier** ⇒ that reconcile pass is the one that finalised it, through **exactly the
`held == 0` door UNIT 1 repaired**.

⚠️ **It is tempting to record this as the fix working in production. That would be
wrong, and the measurement says so:**

```
10:30:06.488  get_positions -> 2 positions      ← TEJASNET ALREADY GONE
10:30:21.620  get_positions -> 2 positions
10:30:21.776  get_positions -> 2 positions      ← the call INSIDE the 10:30:21.758 _gather
```

⇒ At `_gather` time **TEJASNET was not in `positions` at all**, so the changed line
**never ran for that symbol**; `held_qty.get("TEJASNET", 0)` returned **0** because the
key was absent. ⛔ The old `abs(int(qty))` would have produced the **identical** result.

##### 🔬 B-vi · A **SECOND** GTT EXIT, SAME RESULT — ⛔ STILL NOT LOAD-BEARING

🔬 **OAL exited `GTT_EXIT` at `12:01:21.404`** — the TARGET leg, exit ₹445.55, `net_pnl` **+₹11.68**, GTT `333734599` → `CLEANED` at `.405`. ⭐ The `_gather()` at **`12:01:21.366`** is **38 ms earlier** ⇒ that pass finalised it, through the same `held == 0` door.

⚠️ **And again the fix decided nothing.** 🔬 The position-count transitions today:

```
10:05:52  -> 1 positions   (OAL enters)
10:12:11  -> 2 positions   (TEJASNET)
10:12:26  -> 3 positions   (RAMRAT)
10:26:34  -> 2 positions   <- TEJASNET nets to 0 ... finalised 10:30:21  (3m 47s later)
11:50:59  -> 1 positions   <- OAL nets to 0 ...... finalised 12:01:21  (10m 22s later)
```

> 🔴 **IN BOTH EXITS THE SYMBOL HAD LEFT `positions` MINUTES BEFORE THE DECIDING `_gather` RAN**, so
> `held.get(sym, 0)` returned 0 from a **MISSING KEY**. ⛔ `abs(int(qty))` would have given the identical
> answer both times.

⭐⭐ **AND THIS UPGRADES THE ARGUMENT FROM TWO ANECDOTES TO A MECHANISM.** A same-day round trip nets to
**0 the instant the sale fills**, and the adapter's `!= 0` filter drops it immediately — while the CNC
reconcile runs on a **~15-minute cadence**. ⇒ by the time `_gather` looks, the symbol is essentially
**always** already gone. 🔬 Measured gaps today: **3m 47s** and **10m 22s**.

⇒ 🔴 **`max(0, int(qty))` can only ever matter on T+1**, where the sale leaves a net **−1** with no
offsetting same-day buy. 🏷️ The T+1 arm remains **NOT EXERCISED**.

##### ⭐⭐ AND THE STRUCTURAL REASON — which strengthens the commit's own claim

🔬 **`broker/zerodha_adapter.py:1239`** (live branch; the paper branch matches at
`:1208`):

```python
for row in net
if int(row.get("quantity", 0)) != 0
```

⇒ **The adapter drops every zero-quantity net position.** A same-day CNC round trip
(buy 1 + sell 1) nets to **0** and is therefore **filtered out before `_gather` ever
sees it**.

> ⭐ **⇒ THE SAME-DAY ROUND TRIP CAN NEVER EXERCISE THIS FIX — not today, not ever.**
> ⭐ On **T+1** there is no same-day buy to net against, so the sale leaves a net
> position of **−1**, which **passes** the `!= 0` filter, reaches the loop, and is
> exactly where `abs(−1) = 1` shuts the door and `max(0, −1) = 0` opens it.
> 🔬 This upgrades the commit message's *"only T+1 matters"* from an **assertion**
> to a **structural consequence of the adapter's filter**.

---

### C · UNIT 3a (`52ccb4f`) — ✅ **EXECUTED**

🔬 `08:15:14.272 "Config loaded from config (8 files)"` · 🔬 `grep -c "Config load failed"` → **0**.

#### Why the successful load IS execution proof — a deductive chain, ⛔ not an assumption

| link | measurement |
|---|---|
| 1 | `CapitalConfig` declares **`leverage_safety: LeverageSafetyConfig`** at `core/config_loader.py:316` — **no default**, and the model is `extra="forbid"` |
| 2 | ⇒ if the block were **absent**, load raises; if **misspelled**, `extra="forbid"` raises |
| 3 | ⇒ constructing it **necessarily ran** `LeverageSafetyConfig._finite` and `_validate_bounds` |
| 4 | `LeverageMapConfig._finite` and `_delivery_is_pinned` are `field_validator`s ⇒ they run on **every** construction |
| 5 | `CapitalConfig._validate_leverage_within_safety` is a `model_validator(mode="after")` ⇒ runs on **every** construction |
| 6 | the load **succeeded** ⇒ all of 3–5 ran **and passed** |
| 7 | red-capable: a violation raises → `main.py:2197 _log.critical("Config load failed: …")` → `sys.exit(5)` (`main.py:1895/1898`) |

🔬 **Deployed `core/config_loader.py` md5 `35f640832758c1004ee5b2d50d8cbe65`** ==
its `52ccb4f` blob. 🔬 **Deployed `config/system_config.yaml` md5
`86b27c4f1ecbcc51fb7805548960c62d`** == its blob. 🔬 `config_loader`'s `.pyc`
recompiled **`2026-08-28 08:15:13.716`** — inside this boot.

#### The confirmations FILE 20 §2-C asked for

| asked | 🔬 measured |
|---|---|
| config loads | ✅ `"Config loaded from config (8 files)"` @ 08:15:14.272; `Config load failed` = **0** |
| all four intents present | ✅ `INTRADAY · COVER_ORDER · DELIVERY · BRACKET_ORDER` are required fields; load succeeded |
| finite | ✅ `_validate_finite_leverage` ran on all four (link 4) |
| bounded | ✅ `_validate_leverage_within_safety` ran, bounds `[1.0, 10.0]` (link 5) |
| **`DELIVERY == 1.0`** | ✅ `_delivery_is_pinned` ran; deployed yaml reads `DELIVERY: 1.0` |
| `leverage_safety` block validated | ✅ `min_allowed 1.0 · max_allowed 10.0`; self-validating (link 3) |
| **values unchanged `5.0 / 6.0 / 1.0 / 5.0`** | ✅ read from the deployed yaml, md5-pinned to the blob |

#### ⭐ An independent corroboration nobody designed

🔬 `CONFIG_UNACCESSED`: **388** keys on 26-Aug · **388** on 27-Aug · **390** today.
**Δ = +2**, and the only config change between the 27-Aug boot and today's is the
two-key `leverage_safety` block. 💭 **INFERENCE, labelled:** the log line truncates
its list at 10 keys (*"… and 380 more"*), so the two keys were ⛔ **not** confirmed
**by name**; the count delta is corroboration, ⛔ not the proof. The proof is the
deductive chain above. 📄 Today's `CONFIG_DIFF` system event independently records
`changed_files: ["system_config.yaml"]`.

#### ⚠️ The limit of this claim

⭐ **EXECUTED ≠ EXERCISED.** The validators ran on **conforming** production values,
so every `raise` arm was **NOT TAKEN**. 🏷️ The guard has **not** been exercised
against a violating value in production, and today gives no evidence that it would
reject one. That evidence is the unit suite's, ⛔ not production's.

---

### D · C-4's CLEAN SERIAL BASELINE AT `52ccb4f`

✅ **RUN AND CLEAN.** 🔬 **`10 failed · 5,896 passed · 4 skipped`** in `907.77 s`,
**serial**, at `52ccb4f`, `08:30:59 → 08:46:12 IST`. Failure set == the standing
recorded ten, **name for name**; the +48 new cases decompose exactly. ⭐ Full
command, conditions, ID list and arithmetic — and what it does **not** settle — are
in **§2 C-4**.

---

### E · P-1 · COLD/CRASH — **RECORDED ONLY, ⛔ NOT FIXED**

🔬 **Today is the third consecutive instance of the same pair:**

```
08:15:14.293  startup_scenario=COLD: new day (prev=2026-08-27, today=2026-08-28)
08:15:14.293  Startup scenario: COLD (cold start)
08:15:14.309  startup_scenario=CRASH: same day, no SHUTDOWN event found
08:15:22.376  run_all_startup_checks: OK scenario=CRASH warnings=[]
```

🔬 **Blast radius re-measured, and it is again zero:**

| falsifier that could have fired | result |
|---|---|
| `grep -c "Startup scenario: CRASH"` | **0** |
| `SELECT COUNT(*) … event_type='CRASH_DETECTED' AND date=today` | **0** |
| the `STARTUP` row's own scenario column | **`COLD`** |

⛔ No scenario logic was read, traced or changed today. ⭐ Wording held per C-6.

---

### F · `get_holdings` AT BOOT · `carry` AT 09:15

🔬 **`get_holdings` at boot = `"0 holdings"`** — and it is a **measurement**, not an
absence: the call is bracketed by `call_start` / `call_end`, so a call that never
happened would look different from one that returned zero.

✅ **`carry` at 09:15 — MEASURED, AND IT IS ZERO.**

```
2026-08-28T09:15:00.052  fund_manager.sync_from_broker
    broker_cash=10476.6  carry=0.0  old_total=10476.6  new_total=10476.6
```

⭐ Expectation met ⇒ ⛔ **no finding.** 🏷️ And note what this does **not** say: a zero
carry is the *absence* of a carried book, ⛔ not evidence about how a carried book
would behave. The revert trigger's `carry > 0` remains **0 of 9,289**.

#### 🔴 THE DELIVERY-BOOK CEILING, COMPUTED — because three slots opened

⚠️ The standing hazard says an overnight delivery book above **≈76.9 %** of its own
positional bucket **hard-kills the next 08:15 boot at any capital level**, and its
slot ladder says *"the third delivery slot is the one that kills the boot."*
🔴 **Three slots opened today**, so the hazard was run rather than recalled —
`D` = Σ `margin_reserved` of OPEN delivery trades:

```
D  = 432.7328 + 568.6604 + 592.9617 = 1,594.3549      C₀ = 10,476.60
C₁ ≈ C₀ − D = 8,882.25
boot survives iff  D ≤ 0.30 × C₁ + 1  =  2,665.68
                   1,594.35  ≤  2,665.68        ✅  headroom ₹1,071.33
ratio D / (0.30 × C₀) = 50.7 %   vs the 76.9 % ceiling   ✅
```

⚠️ **AND WHY IT CLEARED IS INCIDENTAL, ⛔ NOT DESIGNED.** The ladder's kill case
assumes each slot at the `0.10 × total` concentration cap ≈ **₹1,047.66**. These are
**1-share buys**, so the **share price** was binding, not the cap, and each slot came
in at ₹433–593. ⭐ **At a higher share count the same three slots would have breached
it.** 🏷️ RECORDED, ⛔ not fixed.

✅ **The exposure is bounded, ⛔ not merely small:** `max_open_delivery_positions: 3`
is **ENFORCED**, so no fourth slot can open, and `margin_reserved` is fixed at entry
⇒ **D can only fall.** 🔬 It did: TEJASNET's 10:30 exit took `D` to **₹1,025.69**.

---

### G · THE ROLLBACK TREE — ✅ **ADVANCED `bc9a9f5` → `52ccb4f`**

⭐ **Only after A proved it, and A did.**

| field | value |
|---|---|
| **reason** | `52ccb4f` is now **the last SHA proven to boot** — the tree's only advancement trigger |
| **evidence** | `STARTUP` row **`3801`** @ **`2026-08-28T08:15:25.978225+05:30`**, AFTER `ExecMainStartTimestamp` **`Fri 2026-08-28 08:15:13 IST`** (L-1) |
| **timestamp of the advance** | **28-Aug-2026 ~08:40 IST** |
| **the OTHER clock, ⛔ not collapsed into this one** | **RB-2 PARENT** = current `origin/main`, re-derived by `git ls-remote` **at incident time** — ⛔ **never** pasted from here |

🔴 **A FINDING THIS ADVANCE EXPOSED, ⛔ not fixed:** the VM's own copy of
`docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md` (49,703 B, mtime **26-Aug
19:28**) still carries **`75e637c`** as the RB-3 `checkout -f` target. ⚠️ It is now
**two proven boots stale** (`bc9a9f5`, then `52ccb4f`). ⭐ That is the file an
operator reads *at an ssh prompt during an incident*. ⛔ **Correcting it is a VM
write and was NOT performed** — 👤 Rama's call.

---

### H · RULE C-1 · THE 15:00 NOTICE

⚠️ **At 08:40 there was no CNC position and no active GTT** ⇒ nothing to notify, and
⛔ nothing was manufactured to look like a notice. **RETAINED; SUPERSEDED at 10:05:49.**

✅ **THE NOTICE WAS DELIVERED IN THE CHAT REPLY, ⛔ not only inside a file** — twice,
because the facts moved:

| # | time | content |
|---|---|---|
| 1 | **~10:10** | `DEADLINE 15:00 IST — DECISION: HOLD/CLOSE OAL · COST ≈ ₹0.30–0.45 · YOUR CALL` |
| 2 | **~10:20** | `DEADLINE 15:00 IST — DECISION: HOLD/CLOSE OAL + TEJASNET + RAMRAT · COST ≈ ₹1.35 total · YOUR CALL` — ⭐ explicitly marked as **superseding** #1 |

⭐ **Both were sent ~4h 40m before the deadline** — ⚠️ the corrective for FILE 19's
record **A**, where a 12:15 notice reached 👤 Rama at 18:20, after its deadline.
⭐ Costs computed from `config/broker_costs.yaml`, ⛔ not from recalled brokerage rates.
🏷️ **THE DECISION ITSELF IS 👤 RAMA'S AND WAS ⛔ NOT MADE, ⛔ NOT PRE-EMPTED, ⛔ NOT
INFERRED** — the analysis was supplied, the call was not.

---

## §2 — THE TEN CORRECTIONS, APPLIED

### C-1 · THE PREDICTION SCORE — ⭐ RESOLVED, ⛔ not left as two options

📄 The frozen wording, verbatim from `FILE16_UNIT3_SCOPE_FROZEN_27-Aug-2026.md:160-162`:

> *"the test suite will require edits in **at least 8 files** (§4.2's six + §4.3's
> two). ⭐ If it turns out to be fewer, my measurement was wrong; if far more, the
> unit may not fit the evening beside UNIT 1."*

⭐ **SCORE, as one verdict:**

> **PREDICTION SATISFIED (lower bound) · PRACTICAL ESTIMATE SUBSTANTIALLY
> UNDERSTATED (8 → 14 files, ~26 sites) · DECISION CLAUSE FIRED CORRECTLY AND
> TRIGGERED THE SPLIT.**

⛔ It is **not** recorded as a miss. ⛔ The estimate is **not** recorded as accurate.
⚠️ FILE 19 §4's *"Predicted ≥8; actual 14 — a 75% overrun"* stands as the score of the
**estimate**, and ⛔ must never be read as the prediction failing: *"at least 8"* is a
lower bound and **14 satisfies it**. ⭐ The clause did its job — it is the reason
UNIT 3 split instead of overrunning the evening.

### C-2 · THE PUSH-GATE WORDING

⛔ *"All six conditions hold"* is **withdrawn**. ⭐ The record reads:

> **"All push-gate conditions applicable to the shipped scope were satisfied."**

🏷️ **UNIT 3a SHIPPED · UNIT 3b DEFERRED / OWED · UNIT 2 UNTOUCHED.**
⚠️ A future reader must not read *"all six"* as U3-c / U3-e having shipped. They did not.

### C-3 · THE 18-CASE MATRIX — 🔴 **"18/18" CANNOT BE WRITTEN**

📄 **The matrix, at its source** — `FILE16_UNIT3_SCOPE_FROZEN_27-Aug-2026.md:185`:

> *"**18-test matrix** (4 valid · 12 fail-closed · 1 parity · 1 neutrality) — ⭐ each
> must be able to go **RED** if its protection is removed. ⛔ One broad green test is
> not acceptable."*

⭐ It is defined **by category**, ⛔ not as 18 numbered rows — so any *"case N"*
citation must be checked against the file, ⛔ never against the number in a test name.

🔴 **AND THE TEST FILE ITSELF SAYS TWO OF THE MATRIX'S PROTECTIONS ARE ABSENT** —
`tests/unit/test_unit3a_leverage_validation.py:33-43`, verbatim:

> *"Two protections from the original 18-case matrix are NOT in this unit and are
> NOT asserted … case 15 — unknown intent must fail rather than silently resolve to
> 1.0 (`position_sizer.py` `.get(intent, 1.0)`) … case 16 — FundManager's hardcoded
> `leverage_map is None` default (`fund_manager.py`) must not be able to activate."*

⇒ ⭐ **The matrix was scoped for the WHOLE of UNIT 3** (U3-c…U3-g). **UNIT 3a shipped
U3-d + U3-f only**; the two matrix protections belonging to **U3-c and U3-e went to
UNIT 3b**.

> 🔴 **RECORDED VERDICT:** `MATRIX = 18 slots (4 valid · 12 fail-closed · 1 parity ·
> 1 neutrality)` · `SHIPPED FILE = 18 test functions` · **`COVERAGE ≠ 18/18` — two
> matrix protections are explicitly NOT asserted.**
> ⛔ **The two 18s are a coincidence of arithmetic, ⛔ not evidence of coverage.**
> ⇒ Per FILE 20 C-3 this is a **MISSING ACCEPTANCE-EVIDENCE item**, and **U3a's
> record is NOT complete** on this point until UNIT 3b lands.

⭐ **What IS traceable — four different quantities, ⛔ never merged:**

| quantity | value | how measured |
|---|---|---|
| matrix slots (design) | **18** | `FILE16:185`, quoted above |
| test **functions** in the file | **18** | `grep "^def test_"` |
| collected **cases** (parametrised) | **40** | this morning's serial gate, per-file result line — 🔬 `26 + 14` dots across the wrapped progress block (⚠️ the second line is a **continuation**; reading only the first would have given a wrong `26`) |
| matrix protections **asserted** | **16 of 18** | the file's own docstring names the 2 that are not |

📄 **Section map** — `tests/unit/test_unit3a_leverage_validation.py`:
`# ══ VALID (matrix 1–4) ══` :74 · `# ── the executable neutrality oracle (matrix
2–4, 18) ──` :89 · `# ══ FAIL-CLOSED — leverage_map (matrix 5–14) ══` :135 ·
`# ══ FAIL-CLOSED — leverage_safety self-validation ══` :197 ·
`# ══ MUTATION DOCUMENTATION (B-3) ══` :247.

**Test IDs (18):** `test_01_the_shipped_config_loads` ·
`test_02_absolute_ceiling_is_an_internal_constant` ·
`test_03_neutrality_oracle_reproduces_real_production_margins` (12 params) ·
`test_04_cover_and_bracket_orders_still_resolve` ·
`test_05_each_missing_intent_is_rejected` (4 params) ·
`test_09_intraday_dropped_decimal_low_is_rejected` ·
`test_10_delivery_is_pinned_to_exactly_one` · `test_11_zero_is_rejected` ·
`test_12_negative_is_rejected` · `test_13_above_the_ceiling_is_rejected` ·
`test_13b_bracket_and_delivery_are_now_covered_too` ·
`test_14_non_finite_is_rejected_explicitly` (3 params) ·
`test_14b_nan_would_have_survived_a_bounds_only_check` ·
`test_15_governance_block_validates_itself` (7 params) ·
`test_16_absolute_ceiling_cannot_be_raised_from_yaml` ·
`test_17_a_deliberate_governance_widening_is_permitted_without_code` ·
`test_18_parity_one_validator_serves_both_modes` ·
`test_mutation_map_documents_what_must_break_this_file`.

⚠️ **Test numbering diverges from matrix numbering above 14** — `test_15…test_18`
are the `leverage_safety` / parity tests and are ⛔ **not** matrix cases 15–18.
⚠️ Numbers 06, 07, 08 are absent from the test names; ⛔ not investigated.

**B-3 mutations and their RED results** — 📄 recorded in the file at :249-258 and in
FILE 19 §4:

| mutation | 🔬 red result |
|---|---|
| delete `_delivery_is_pinned` | `test_10` RED — **1** failure |
| delete `_validate_finite_leverage` | `test_14` (3 params) RED — **4** failures |
| delete `_validate_leverage_within_safety` | `test_09/11/12/13/13b` RED — **5** failures |
| delete `LeverageSafetyConfig` bounds | `test_15` + `test_16` RED — **2** failures |
| change any shipped leverage value | `test_01` + `test_03` (12 params) RED |
| **all four restored** | ✅ **40 pass** |

⚠️ The `40` is the **UNIT 3a-related pass count from FILE 19's mutation table**; ⛔ it
is not the same quantity as the 18 slots or the 18 functions. See C-5.

### C-4 · THE CONCURRENCY ARTEFACT

⭐ **The strongest honest statement, and the one that stands:**

> *"The differential produced zero new failures after two anomalous BASE-only
> failures were isolated and shown to pass independently. ⚠️ Neither set was
> measured under isolated conditions."*

🏷️ **CONDITIONALLY CLEAN** — ⛔ **not clean.**

⚠️ **The symmetry never existed.** BASE and WORK both ran concurrently, **and WORK was
restarted mid-way** ⇒ the two runs were ⛔ not under comparable conditions.
⇒ WORK's 10 could contain artefacts of its own, **and** WORK could equally have
**missed** a failure that only appears under load. ⛔ Neither direction is excluded
by what was measured.

🔴 **THE CONSEQUENCE, which is why this mattered this morning:** the BASE failure set
at `bc9a9f5` is **the reference for every future differential**. A contaminated
reference silently mis-scores every gate built on it.

#### 🔬 THE CLEAN SERIAL BASELINE AT `52ccb4f` — RE-ESTABLISHED

| field | value |
|---|---|
| command | `python -m pytest tests/unit tests/integration` — ⭐ the frozen gate form, ⛔ **not** `run_tests.py` (which `load_dotenv()`s the real `.env`) |
| concurrency | **SERIAL** — no `-n`, and 🔬 no `addopts`/xdist config exists (no `pytest.ini`, `tox.ini`, `setup.cfg`, `pyproject.toml`, root `conftest.py`) |
| shell | **Git Bash**, per the standing environment rule |
| interpreter | `C:\python311\python.exe` 3.11.9 — ⛔ **not** the `python3` WindowsApps stub |
| worktree | `…/2f2481fb…/scratchpad/f6-work` @ **`52ccb4f`**, `git status --short` **clean** |
| the seeded artefact | `config/instruments.csv` present (75,749 B) — ⚠️ gitignored; absent ⇒ **26 phantom failures** |
| window | **28-Aug-2026 08:30:59 → 08:46:12 IST**, `907.77 s` |
| **RESULT** | 🔬 **`10 failed · 5,896 passed · 4 skipped · 281 warnings`**, raw `PYTEST_RC=1` |

🔴 **THE `rc=1` IS THE STANDING PRE-EXISTING SET, ⛔ NOT A REGRESSION — and it is
compared as a SET, ⛔ not by eye.** All ten IDs match the recorded ten
(`UNPUSHED_PENDING_DEPLOY_LEDGER.md:1556`) **name for name**:

`test_closure_source_contract::test_no_module_restates_the_vocabulary_literals` ·
`test_fix181::TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_active` ·
`test_main::TestBl15WebhookSecretRequired::test_paper_mode_does_not_require_webhook_secret` ·
`test_main::TestContinueFromGate::test_price_hit_calls_placer_with_correct_prices` ·
`test_main::TestContinueFromGate::test_no_placer_releases_reservation_and_updates_status` ·
`test_main::TestContinueFromGate::test_stats_placed_incremented_on_success` ·
`test_phase17_batch2::test_fix077_flask_max_content_length` ·
`test_t4_deploy_preflight::test_ist_now_emits_valid_ist` ·
`test_t4_deploy_preflight::test_check_tz_fails_on_broken_utc_form` ·
`test_t4_deploy_preflight::test_check_tz_passes_on_agreement`

⇒ **7 standing pre-existing + 3 `test_t4_deploy_preflight`**, the latter being the
🏷️ **known environment artefact**: a worktree with no `venv/` makes
`scripts/ist_now.sh pick_python()` fall through to the WindowsApps `python3` stub.
⛔ Not chased — it is documented and reproducible, and 👤 the standing baseline for a
venv-less worktree is precisely these ten.

#### ⭐ AND THE ARITHMETIC CLOSES EXACTLY — the part that makes this a baseline rather than a number

| step | 🔬 measured |
|---|---|
| the last **clean, set-compared** reference | `75e637c` closure gate, 25-Aug: **`7F / 5,851P / 4S`** |
| `75e637c` → `bc9a9f5` | 🔬 **docs-only** — `git diff --name-only` = 4 markdown files, `git diff --stat -- tests/` = **empty** ⇒ the test population is **unchanged** |
| `bc9a9f5` → `52ccb4f` | 🔬 **+48 collected cases** — `test_f6_leg_held_qty_predicate.py` **8** + `test_unit3a_leverage_validation.py` **40** |
| today, serial, at `52ccb4f` | **`10F / 5,896P / 4S`** |
| **Δ passed** | `5,896 − 5,851` = **+45** |
| **Δ failed** | `10 − 7` = **+3** — and they are exactly the 3 `test_t4_deploy_preflight` env cases |
| **closure** | **`+45 + 3 = +48`** ⇒ ⭐ **every one of the 48 new cases is accounted for, and ⛔ nothing that passed before now fails** |

✅ ⇒ **A CLEAN SERIAL BASELINE AT `52ccb4f` NOW EXISTS: `10F / 5,896P / 4S`, failure
set == the standing recorded ten.** ⭐ This is the reference the next differential
must be measured against — ⛔ **not** the concurrent `bc9a9f5` set, whose two
anomalous BASE-only failures made it conditional.

⚠️ **What this does ⛔ NOT settle.** ⭐ It re-establishes the **`52ccb4f`** reference
under serial conditions. It does **not** retroactively clean the `bc9a9f5` BASE run,
and it does **not** prove WORK's original 10 were artefact-free — that run is gone.
🏷️ Last night's differential therefore stays **CONDITIONALLY CLEAN**; ⭐ what changes
is that **every future** differential now has an uncontaminated comparand.
🔬 **Independent corroboration of C-5:** the 48 was re-derived here from a fresh run
(`8 + 40`), ⛔ not carried over from last night's arithmetic.

⭐ **FUTURE RULE, now standing:** BASE and WORK full gates run **SERIALLY** unless the
harness is demonstrated resource-isolated. ⚠️ If parallel is ever used, identify the
shared resources **FIRST**: **DB · filesystem · ports · temp dirs · env vars ·
fixtures · external services · caches.**

### C-5 · THREE QUANTITIES, ⛔ NEVER MERGED

| quantity | value |
|---|---|
| **TEST COUNT DELTA** | **48** = 8 (UNIT 1) + 40 (UNIT 3a) |
| **EFFECTIVE FAILURE SET** | **10** |
| **NEW FAILURE SET** | **EMPTY** |

⚠️ **Reclassifying a failure changes the failure SET; it ⛔ never changes the test COUNT.**

🔬 **ALL THREE RE-DERIVED FROM THIS MORNING'S SERIAL RUN, ⛔ not carried over:**

| quantity | 🔬 today's independent measurement |
|---|---|
| UNIT 1's **8** | `test_f6_leg_held_qty_predicate.py ........` — **8 dots, 8 passes** |
| UNIT 3a's **40** | `test_unit3a_leverage_validation.py` — **26 + 14** across the wrapped block |
| the **48** | `8 + 40`, and it closes against the pass/fail deltas (C-4's table) |
| the **10** | the failure set, ID-matched to the recorded ten |
| the **EMPTY** new-failure set | ⛔ zero tests that passed at the reference now fail |

### C-6 · COLD/CRASH — CONDITIONAL WORDING

⭐ The wording that stands:

> *"The observed startup sequence makes the COLD arm appear unreachable under the
> tested production startup path."*

⛔ **NOT** *"COLD is unreachable in production."*
🏷️ The corollary — **crash-recovery as the normal morning path** — remains
💭 **INFERENCE**. ⛔ Neither is upgraded until the branching is traced. ⛔ Nothing was
traced or changed today; §1-E records a third instance and its zero blast radius.

### C-7 · GTT_EXIT WORDING — HOLDS

> *"System records show all CNC positions exited via `GTT_EXIT`."*

⛔ Never upgraded to broker confirmation. 🏷️ **Broker audit data was NOT independently
checked** — that remains true today.

### C-8 · T+1 AND CARRY — 🏷️ **EXPLICITLY NOT EXERCISED**

🔬 Reinforced by this morning: **0 holdings · 0 positions · 0 ACTIVE GTTs** ⇒ there
was nothing for the T+1 arm to run against.

⛔ **And the two claims stay apart:** *"the fix restores reachability of an existing
working path"* is ⛔ **NOT** *"a production-proven T+1 path."* ⭐ Today's §1-B result is
the sharpest form of that distinction yet recorded: the line was **deployed, loaded,
and still did not run.**

### C-9 · U3's TWO EVIDENCE CLASSES — ⛔ NEVER MERGED

**CLASS 1 — 🏷️ HISTORICAL CORROBORATION.** The 722-row persisted population:
**MIS 503 rows @ implied leverage exactly 5.0** · **CNC 84 rows @ exactly 1.0**,
`min == max`; **135 NULL-product rows EXCLUDED**. ⛔ A query over unchanged rows is
**not** a post-fix proof.

**CLASS 2 — ⭐ THE EXECUTABLE ORACLE (the post-fix proof).** The suite calls the
**real `required_margin()`** with the **real config-loaded map** and requires equality
with the independently persisted margin.

- **test ID:** `test_03_neutrality_oracle_reproduces_real_production_margins`
- **file:** `tests/unit/test_unit3a_leverage_validation.py:112-127`
- **commit SHA:** `52ccb4f4f0c303ff47037ca492d5eec7536b01b8`
- **the loaded map:** `INTRADAY 5.0 · COVER_ORDER 6.0 · DELIVERY 1.0 · BRACKET_ORDER 5.0`,
  obtained via `load_all(Path("config")).system.capital.leverage_map` — ⭐ the real
  loader, ⛔ not a literal
- **the equality rule:** `required_margin(qty, price, intent, lev_map) ==
  pytest.approx(expected, rel=0, abs=1e-6)`
- **provenance:** 📄 *"Real production triples (qty, entry_target_price,
  margin_reserved) taken from the live DB on 27-Aug-2026"* — non-circular: none of the
  three columns is derived from the others, and `margin_reserved` was written
  independently at reserve time.
- ⛔ **No broker or account identifiers are recorded — only the three numeric columns.**

| # | intent | qty | entry_target_price | expected = `margin_reserved` | calculated |
|---|---|---|---|---|---|
| 1 | INTRADAY | 2 | 220.6791 | 88.27164 | ✅ equal |
| 2 | INTRADAY | 1 | 634.31505 | 126.86301 | ✅ equal |
| 3 | INTRADAY | 1 | 417.582 | 83.5164 | ✅ equal |
| 4 | INTRADAY | 2 | 245.00476 | 98.001904 | ✅ equal |
| 5 | INTRADAY | 1 | 348.9486 | 69.78972 | ✅ equal |
| 6 | INTRADAY | 2 | 216.70308 | 86.681232 | ✅ equal |
| 7 | DELIVERY | 1 | 415.3676 | 415.3676 | ✅ equal |
| 8 | DELIVERY | 1 | 550.397 | 550.397 | ✅ equal |
| 9 | DELIVERY | 1 | 314.1704 | 314.1704 | ✅ equal |
| 10 | DELIVERY | 2 | 227.57394 | 455.14788 | ✅ equal |
| 11 | DELIVERY | 4 | 127.67414 | 510.69656 | ✅ equal |
| 12 | DELIVERY | 1 | 573.0516 | 573.0516 | ✅ equal |

⭐ Rows 7–12 are the DELIVERY arm at exactly 1×: `expected == qty × price`.
⭐ Rows 1–6 are the MIS arm at exactly 5×: `expected == qty × price / 5`.

### C-10 · "BOTH GUARDS CLEAN" — MADE TRACEABLE

⚠️ **First, an honesty note on identification.** The phrase *"both guards clean"* does
**not** appear in `FILE19_BUILD_27-Aug-2026.md`; it came from review prose. 🔬 The only
place in the standing record that names **exactly two** guards and requires **both** to
be clean is `MEMORY.md`'s SIZE GUARD block. 💭 That identification is **INFERENCE**; the
guards are named and re-run below so the claim is checkable either way.

| | guard | command | 🔬 result |
|---|---|---|---|
| **GUARD 1** | `MEMORY.md` size ceiling | `wc -c MEMORY.md` → **9,557 B** (limit **< 24,000**) | ✅ **PASS** |
| **GUARD 2** | `MEMORY*.md` line-length | `LC_ALL=C awk 'length>(index($0,"🔝")?450:300){print FILENAME" "FNR": "length}' MEMORY*.md` → **no output** | ✅ **PASS** |

- **SHA:** `52ccb4f4f0c303ff47037ca492d5eec7536b01b8` (the final commit)
- **timestamp of this run:** **28-Aug-2026 ~08:33 IST**
- ⛔ A summary phrase remains **not** evidence of which guards ran after the final commit.

#### ⭐ PRESERVED, because it explains an otherwise inexplicable failure

- 🔬 **ROOT untouched:** `feat/delivery-config-split @ 6d24a83` — re-confirmed this
  morning; all UNIT 1 / UNIT 3a work lived in **isolated worktrees off `bc9a9f5`**.
- 🔬 **The gitignored `config/instruments.csv` was seeded into both worktrees** —
  present at 75,749 B in `f6-work` today. ⚠️ **Without it a *byte-identical* checkout
  produces 26 phantom failures.** ⭐ That is why an apparently identical environment can
  produce artificial failures, and why C-4's baseline had to name it.

#### ⭐ UNIT 2's wording, exact

> **"Proof did not complete; removal was therefore prohibited."**

⛔ **NOT** *"ran out of time."* ⭐ A **design decision**: `order_protocol` alone has
**100** production references and is also a live `trades` column; the bounded 7-step
no-live-reader proof did not complete, and removing a key on partial evidence is
forbidden.

---

## §3 — STILL NOT PROVEN AFTER THIS MORNING

⭐ Kept explicit, ⛔ not allowed to collapse into *"verified"*:

| item | 🏷️ label |
|---|---|
| **F6 live T+1** | 🏷️ **NOT EXERCISED** — ⭐ and now with a *structural* reason: the adapter's `!= 0` filter (`zerodha_adapter.py:1239`) means ⛔ only a T+1 sale can ever reach the repaired line (§1-B-v) |
| **UNIT 1's changed line executing at all** | ✅ **EXECUTED 10:15:13** — ⛔ superseded from NOT EXECUTED (§1-B-iv) |
| **UNIT 1's fix being LOAD-BEARING in production** | 🔴 **NOT DEMONSTRATED** — the one GTT exit today was decided by an *absent* key, ⛔ not by `max(0,…)` (§1-B-v) |
| the genuine CNC carry EOD branch | 🏷️ NOT EXERCISED |
| **CHECK 2b** | 🏷️ NOT COMPUTABLE without a carry |
| OWED-2 · CHECK 1 · CHECK 2a | 🏷️ OWED |
| the four-reading series · the three-cause discriminator | 🏷️ OWED |
| G3's settled-CNC `used` | 🏷️ OWED |
| cause ④ | 💭 INFERENCE |
| the revert trigger's `carry > 0` | 🔬 still **0 of 9,289** |
| broker confirmation of the GTT_EXITs | 🏷️ NOT CHECKED — system records only |
| **UNIT 3b** (U3-c + U3-e) | ⏸ DEFERRED / OWED — 14 files, ~26 sites |
| **UNIT 2** (F11) | ⏸ UNTOUCHED — proof did not complete |
| `COVER_ORDER` / `BRACKET_ORDER` | 🏷️ NOT EXERCISED — validated, never applied |
| the 135 NULL-product rows | 🔬 excluded from every per-intent figure |
| **P-1** COLD/CRASH | 🏷️ RECORDED, ⛔ not investigated |
| the 18-matrix's cases 15 & 16 | 🔴 **NOT ASSERTED** (C-3) |
| **UNIT 3a's guard against a violating value** | 🏷️ EXECUTED but **NOT EXERCISED** (§1-C) |
| **the 09:15 `carry`** | ✅ **MEASURED = `0.0`** — ⚠️ a zero carry is an absence, ⛔ not evidence about a carried book |
| the delivery-book ceiling at a realistic share count | 🔴 **UNTESTED** — today cleared at 50.7% only because 1-share buys made price, ⛔ not the cap, binding (§1-F) |
| tonight's **17:35 EOD with a real CNC carry** | ⏳ **PENDING 👤 RAMA'S 15:00 HOLD/CLOSE CALL** — the branch is traced but 🏷️ **NEVER EXERCISED** |
| C-4's serial baseline | ✅ **DONE** — `10F / 5,896P / 4S` at `52ccb4f`, serial, set-matched |
| the VM's RB-3 target | 🔴 **STALE at `75e637c`** — two proven boots behind (§1-G) |

---

⛔ push ≠ boot · ⛔ **boot ≠ the changed line executed** · ⛔ deployed ≠ executed ·
⛔ **loaded ≠ executed** · ⛔ **executed ≠ exercised** · ⛔ exists ≠ correct ·
⛔ green ≠ red-capable · ⛔ 3 flat EODs ≠ 1 discriminating · ⛔ intraday GTT exit ≠ T+1 ·
⛔ historical query ≠ post-fix execution · ⛔ system record ≠ broker confirmation ·
⭐ **absence of the qualifying condition is never evidence about that condition's behaviour.**

## END OF FILE 20 RECORD
