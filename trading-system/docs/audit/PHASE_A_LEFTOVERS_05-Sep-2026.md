# PHASE A LEFTOVERS — /controls BRACKET · ROTATION PRE-CHECKS · REPLAY · CRON · DENIAL
## READ-ONLY · 05-Sep-2026 · 5 agents in 3 recorded batches

**Nothing was modified.** No restart, no push, no commit, no config/YAML/scanner edit, no credential
step, no webhook request constructed or sent, no secret printed. `systemctl show` / `crontab -l` /
`date` are query-only.

| # | Item | Verdict |
|---|---|---|
| §3 | `/controls` liveness bracket | **CONFIRMED — BRACKET HELD** (with a recorded correction) |
| §2.1 | Multi-secret support | **CONFIRMED — SINGLE-SECRET** |
| §1.1 | Replay chain | **CONFIRMED — and worse than claimed** |
| §1.3 | Monday 07:41 revert cron | **CONFIRMED — and a push this weekend deletes it** |
| §1.2 | Cheap-denial surface | **PARTIAL — claim's mechanism refuted, a cheaper one found** |

---

# §3 — THE BRACKET IS CLOSED, AND THE RECORDED IDENTIFIERS WERE MIS-ATTRIBUTED

**BRACKET HELD.** The same process instance was continuously alive across the ~15:48 04-Sep render,
so the render **is** attributable.

| BEFORE (04-Sep 15:44:31) | AFTER (05-Sep 21:45:25) | Same? |
|---|---|---|
| MainPID 1119981 | MainPID **1119981** | yes |
| start 03-Sep 13:08:20 | ExecMainStartTimestamp **Thu 2026-09-03 13:08:20 IST** | yes |
| NRestarts (implied 0) | **0** | yes |
| — | ActiveState **active** / SubState **running** | still up |

PID 1119981 still holds the serving socket: `LISTEN 127.0.0.1:8500 users:(("python",pid=1119981,fd=6))`.

## The correction — the BEFORE read was of `gui-dashboard`, not `trading-system`

Running the literal command against `trading-system` returns `MainPID=0`, `ActiveState=inactive` —
which would have produced a **false "BRACKET BROKEN"**. There is no `trading-system` start at
03-Sep 13:08:20 and no PID 1119981 in its journal; its instance at the BEFORE read was **1214531**,
started 04-Sep 13:47:46. `gui-dashboard`'s journal matches the BEFORE read to the second and shows
nothing thereafter.

**Secondary:** the bracket holds on the `trading-system` reading too — instance 1214531 ran
13:47:46 → 17:35:04 on 04-Sep, spanning both 15:44:31 and ~15:48. Only the *recorded identifiers*
were attributed to the wrong unit.

## Two facts that qualify how the render must be read

* 🔴 **The kill switch was already `SOFT_KILL` at 04-Sep 15:15:01** (`reason=circuit_breaker_force_close_15:15`,
  `triggered_by=order_monitor`) — **~33 minutes BEFORE the render.** The `/controls` screen was
  depicting a system already in SOFT_KILL. Any reading of it must say so; it is not a live-trading screen.
* **The GUI code did not change under the running process** — 7 commits landed on `main` after
  03-Sep 13:08:20, **0 touched `ops_dashboard/`**; 0 GUI source files have an mtime after that instant;
  and a per-file `git hash-object` comparison of deployed `ops_dashboard` against the bare repo at
  `20061b6` gives **183 files compared, 0 differing, 0 missing**. The "long-lived Python process may be
  running pre-push modules" hazard does not bite here.

Deployed SHA `20061b6` ("fix(mis): F1b — a restored stop is not protection until the broker says it rests").

> ⚠ **A `systemctl restart gui-dashboard` would void this bracket.** Rotating `WEBHOOK_SECRET` restarts
> **`trading-system`**, a *different* unit, and would **not** disturb PID 1119981 — so the bracket
> survives the rotation.

---

# §2.1 — SINGLE-SECRET. There is no zero-downtime path.

Checked on **both** the deployed receiver and HEAD `6d24a83`:

* `self._secret` holds exactly one `str`.
* Exactly **two** `compare_digest` sites, one per auth branch, each against that single value. No loop,
  no `any()`, no tuple of candidates.
* Exactly **one** env var consulted — `WEBHOOK_SECRET`. No `_OLD` / `_PREV` / `_NEXT` / `_SECONDARY`.
* Exactly **two** routes registered — `GET /health`, `POST /webhook/<scanner_name>`. **No admin, reload
  or rotate route; no SIGHUP handler; no setter.**

⇒ **No two-token overlap is possible.** Rotation has unavoidable downtime and requires a process
restart. This is exactly why it is a weekend job: with the engine down and the market closed, there is
nothing firing to lose.

---

# §1.1 — REPLAY CONFIRMED, AND WORSE THAN CLAIMED

| Link | Measured |
|---|---|
| Re-dating | **208,946 / 208,946** stored payloads carry a time-only stamp (`"H:MM am"`). It is 100% of live traffic, not an edge case |
| 600 s age gate | Measures age from the **re-dated** stamp ⇒ a same-minute replay has age ≈ 0 ⇒ **passes** |
| 300 s dedup | The fingerprint **and** its `fingerprint_date` partner column **both change every day** |
| The proof | **15,747 groups** of identical `(scanner, symbol, HH:MM)` span more than one day, and in **all 15,747** the distinct-fingerprint count exactly equals the distinct-date count — **zero collisions**, so the UNIQUE index is never even reached |
| Third gate | `signal_processor`'s independent 600 s check fails the same way |

⇒ **Both date-bearing protections fail against the same attack, and they fail daily.** One captured POST
is a repeatable injection at that minute, not a one-shot.

**Not overstated:** an accepted replay is not an automatic order. Measured base rate signal → trade is
**856 / 208,946 = 0.41%**, and the remaining gates in the 20-gate chain still apply.

---

# §1.3 — THE MONDAY REVERT EXISTS, IS CORRECT, AND A PUSH DELETES IT

| Item | Measured |
|---|---|
| The entry | **line 149 of 149** of `crontab -l`: `41 7 7 9 * /home/ubuntu/preserved/2026-09-04_cnc_off/revert_delivery.sh` ⇒ **07:41 IST Mon 07-Sep**, one-shot. Cron active; VM TZ `Asia/Kolkata` |
| What it does | Targets **exactly** the 3 DELIVERY YAMLs; `git checkout refs/heads/main -- $F`; asserts `enabled: true` in all three; `.bak` fallback; exit 2/3 raise `logger user.crit` |
| Does `main` carry `true`? | **Yes** (`20061b6`, all three at `:11 enabled: true`) — the primary path succeeds |
| Rehearsed? | **Yes** — 3 test runs logged 04-Sep, including a forced `.bak` trap path |
| Current state | **12 true / 4 false**. False: `pb01_breakout_retest` (fail-closed) + the 3 positional, each carrying the TEMP comment |
| Timing | **07:41 runs ~34 min BEFORE the 08:15 boot** ⇒ takes effect Monday with no further restart (config is load-once) |
| Monday check | `will_trade_count` should read **15** (`wont=1`, only pb01). **12 means the revert FAILED.** Last observed: 12 on 04-Sep 13:47:55; 15 on 27-Aug…02-Sep |
| Survives a RESTART? | **Yes** — the crontab lives in the cron spool, independent of `trading-system.service` |
| Survives a PUSH? | 🔴 **NO. A push DELETES it.** |

## The push interaction — the load-bearing fact for this weekend

The post-receive hook does a **whole-crontab replace** from `deploy/cron/trading-system.cron`. That
canonical file is **148 lines and does not contain the revert entry** (the live crontab has 149).

So a push this weekend would do **both** of these at once:
1. `checkout -f main` — which **performs the revert itself immediately**, since `main` carries
   `enabled: true` ⇒ the 3 delivery strategies come back on **now**, not Monday 07:41.
2. Replace the crontab — **deleting** the Monday revert entry.

⇒ The revert still effectively happens, but **at push time**, which **removes §1.3's accidental
protection early**. Since rotation does **not** require a push (`.env` is untracked), the two actions
are cleanly separable.

---

# §1.2 — PARTIAL: the named mechanism is refuted; a cheaper one exists

## What was refuted

`max_trades_per_day` **does not exist** in this codebase (positive control: 0 enforcement hits for that
name, 30+ for the real one). The live key is **`max_daily_trades: 10`**, and it **is** in the gate chain
— `capital/risk_engine.py:664`, check #5, with **5,146** signals carrying `REJECTED_DAILY_TRADES`.

The 11th signal is **rejected per-signal**; the day is not halted and no kill switch fires. Two further
facts blunt an attacker: only genuinely *filled* states burn the quota (`FAILED`/`REJECTED`/`CANCELLED`
do not), and `entry_burst_max: 3` per 60 s imposes a hard ~200 s floor to place 10 entries.

At the measured conversion rate, consuming the cap costs **~6,145 injected signals in expectation**
(1 executed trade per 614 signals). **Impractical, and the risk should not be inflated.**

The daily loss limit is the weakest path of all: it keys on realized P&L, so an attacker cannot steer it.
(Worth recording separately: the post-close breach **does** cut **both** books —
`config/system_config.yaml:309-313` states the reason verbatim, that one account-wide realized P&L
exists with no per-book attribution — and it market-closes delivery carry too, then soft-kills.)

## 🔴 What was found instead — a one-request denial

**The per-IP limiter counts REQUESTS; the shared 300-slot queue counts SYMBOLS — and a POST's symbol
list is uncapped** (~56,000 symbols fit inside the 1 MB body limit).

⇒ **A single authenticated POST can cross the 240 backpressure threshold and 503 every subsequent
Chartink signal.** No conversion needed, no market view needed, one request.

Positive control: **18 production 503s** already exist from ordinary operation, so the branch is live
and reachable.

⇒ This is the real cheap-denial surface, it is cheaper than the trade cap by four orders of magnitude,
and it was not visible in the 20-gate list because the gates bound *per-signal* behaviour while this
attacks the *queue* the gates feed from.

---

# WHAT THIS CHANGES FOR THE ROTATION DECISION

Stated as findings, not recommendations:

1. **Rotation does not require a push.** `.env` is untracked; a push would separately re-enable the
   delivery book immediately and delete the Monday cron.
2. **Rotation restarts `trading-system`, not `gui-dashboard`** ⇒ the `/controls` bracket, now recorded,
   survives it.
3. `trading-system` is currently **inactive/dead** (clean self-exit 04-Sep 17:35:04) — Saturday,
   correct by design. Per the standing hazard, do not `start`/`restart` it to "prepare"; the kill switch
   reads `SOFT_KILL` from the routine 15:15 circuit-breaker close.
4. **Rotation closes exposure (a), the screenshots. It does not close (b), the transport** — the token
   still travels in cleartext on plain HTTP on every POST, and HMAC is implemented and switched off.
5. **Rotation does not close the replay finding either** — a *new* token, once captured, is replayable
   daily by the same mechanism.
6. **Monday verification is a single number:** `will_trade_count` = **15** means the revert worked;
   **12** means it failed.

**No Phase B has begun. No credential step was executed. Rama authorises both separately.**
