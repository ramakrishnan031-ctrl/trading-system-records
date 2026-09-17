# MONDAY RECORD — 31-Aug-2026

First live trading day of the 9-commit stack (`origin/main` = `39292d3`).
Assembled 18:5x IST. Every figure below is 🔬 MEASURED unless labelled otherwise.

⛔ This record does not say "all checks passed."

---

## 1 · 02:10 — `output_retention`, FIRST REAL RUN (`--apply`)

| item | value |
|---|---|
| mark file | `0 2026-08-31T02:10:01+05:30` — **rc 0** |
| deleted | **0** · freed 0.00 MB · cap 25 respected |
| families | 6, all under KEEP=7 (6·6·6·6·6·3) |
| refusals | **12** — 6 `daily_report_*.xlsx` + 6 loose logs, never deleted |

Predicted delete-set of 0, confirmed against live state.
📌 The refusal list is **12, not the 6** the card described — the other six are
undated append-only logs. Addendum to parked item P-a; not chased.

---

## 2 · 08:15 — BOOT

```
08:15:05.000  token_watcher : "Fresh token detected (daily start, in service window)"
08:15:05      systemd       : Started trading-system.service  (MainPID 814664, NRestarts=0)
08:15:06.056  CRITICAL      : KILL SWITCH ACTIVE AT STARTUP  state=SOFT_KILL
08:15:06.059  ev 3803       : KILL_AUTO_CLEARED — from 2026-08-28T15:15:01,
                              classification="scheduled", cleared_via="clear_stale_state"
08:15:13.892  ev 3804       : CONFIG_DIFF  changed_files=["system_config.yaml"]
08:15:14.638  F ARMED       : "F pre-pass poll started (interval=5s)"
08:15:17.489  ConfigValidator: 0/394 keys accessed, 0 drift
08:15:17.489  ev 3805       : STARTUP  COLD  live  2.0.0
```

**Boot proven**: `STARTUP` ev **3805** @ 08:15:17.489 — later than the service start
(08:15:05) and a **new row** vs 28-Aug's 3801. This boot, not a stale read.

⛔ NOT SMOOTHED: startup initially observed SOFT_KILL, immediately auto-cleared;
service continued and produced ev 3805. Never "startup clean."

**Component identities** (sha256, first 16), recorded **separately** from the
combined SHA `39292d3`:

```
alerts/delivery.py                d586e48fa4ebdf9f
alerts/mis_squareoff_notifier.py  5da5f28d0ca293b7
core/mis_squareoff_timing.py      9b98c43810daea6a
main.py                           7cfaf63190a5b27d
config/system_config.yaml         4ec155ae38fc6430
```

**Config validation — corrected, not as first recorded.** `0 drift` is a
**vacuous zero**: `validate_all()` runs once (`main.py:4122`), guarded, before any
trading key access, so it compares 0 of 394 tracked keys.

```
CONFIG_DIFF       = FIRED (ev 3804)          ← RED-CAPABLE, real evidence
CONFIG_DRIFT      = 0 of 0 accessed          ⇒ NOT EXERCISED
CONFIG_UNACCESSED = 394 of 394               ⇒ coverage warning, not a result
```
The system detects that config **changed**; it does not detect **drift within a
session**. F11-class inert control. Recorded, not fixed.

---

## 3 · THE F GATE — TWO LINES, NEVER ONE

```
TRANSPORT_RESULT      = BOTH_ACCEPTED
                        boot     08:15:18  email ACCEPTED_BY_PROVIDER (3461 ms)
                                           telegram ACCEPTED_BY_PROVIDER (670 ms)
                        pre-pass 15:05:04  email ACCEPTED_BY_PROVIDER (3211 ms)
                                           telegram ACCEPTED_BY_PROVIDER (678 ms)
F_RECIPIENT_CONFIRMED = NOT PROVEN
```

Recipient recorded in the log itself both times —
`email_fallback.sent … to="pythonsystemalerts@gmail.com"` — which contradicts the
card's premise that logs record no recipient. Config and `.env` agree
(`to_addresses`, `ALERT_EMAIL_TO`). **The system is proven to send there.**
**Human receipt was never confirmed to this session.**

The service was **not** stopped at 15:05. No instruction arrived; the stop was
never mine to make. The branch's own rationale — *"unconfirmed, F squares off live
positions silently"* — did not apply, because **MIS was flat**. Recorded as:
*service ran through 15:07 on an unverified alert channel with zero candidates
present.* ⛔ Not recorded as the gate being satisfied.

---

## 4 · 15:05 / 15:07 / 15:10

```
15:05:00.151  PRE_PASS initiated
15:05:03.363  email_fallback.sent → pythonsystemalerts@gmail.com
15:05:04.042  F_NOTIFY  aggregate=BOTH_ACCEPTED  kind=PRE_PASS
              boot_id=770811f93559  correlation_id=180f3136a13842f0

15:07:00.174  MIS_AUTO_SQUAREOFF_SCAN  pass=PASS_1
              mis_candidates=0 · cnc_excluded=1 · co_excluded=0 · unknown_product_excluded=0
15:10:00.207  MIS_AUTO_SQUAREOFF_SCAN  pass=PASS_2   (identical counters)
```

Both passes fired within ~200 ms of schedule. No `DEADLINE_BREACH`.

**THE BOOK WAS FLAT OF MIS ALL AFTERNOON. SAYING SO PLAINLY.**

**PROVEN** — scheduled arm executed twice on time on its first live day;
structured telemetry emitted; **product discrimination genuinely exercised**
(`cnc_excluded=1` — the orchestrator resolved SPLPETRO as CNC and declined to act;
squaring off a delivery position at 15:07 would have been a real defect with a real
cost, and this leg had a way to fail and did not); `unknown_product_excluded=0`
means no HAZ-4 blind rows were **encountered** — ⛔ not that the HAZ-4 branch was
exercised.

**NOT EXERCISED** — candidate-bearing cancel→verify→exit; any broker exit order;
partial fill; PASS-1 failure with remaining quantity; `DEADLINE_BREACH`; every
CRITICAL branch.

Highest stage actually observed: *scheduled arm fired → scan executed → product
discrimination applied → zero candidates → no action taken.* Nothing beyond that.

---

## 5 · 15:20–15:30 — EVIDENCE PRESERVED AND HASHED

```
D:\Projects\trading-system-evidence\2026-08-31\
a31fe6a72d1f92df13370f6d9ac90d74f3ae14d291ce200aabcf54107019db9f  system_2026-08-31.log
546e9d8f36f8a27fbd51fd7cb36520e21b3da026328fefb2e8a756b62de1624d  window_15-00_to_15-25.log
53fea2e7232ba0b80912a2889b948f1c9a8b2fbf0de83dd31f77dfa7d1973f9b  trades_and_gtt_2026-08-31.txt
```

Outside `logs/`, `reports/output/`, the repo and the session scratchpad — survives
retention, a repo operation and this session ending. **Content-verified, not merely
hashed**: PRE_PASS 3 · PASS_1 2 · PASS_2 2 · force_close 1 · SOFT_KILL 1 ·
forensic 1 · delete_gtt 1 · gtt_exit 1, with the decisive lines read back verbatim.

🔴 **Because the 16:07 report does not exist, these preserved artifacts are today's
PRIMARY record, not a backup.** Any regenerated XLSX is a reconstruction to be
verified against them, never the source.

---

## 6 · 16:05 / 16:07

**16:05 — CLEAN.** `daily_report` heartbeats today = **0**; zero ERROR/CRITICAL/
WARNING in 16:04–16:09. Registry verified: `enabled: false` **and**
`monitored: false`. Both flags did their job. **A PASS.**

**16:07 — 🔴 FAILED. NO REPORT EXISTS FOR TODAY.**

```
scheduled=yes · executed=yes · result=FAILED · report produced=NO
cron_heartbeat: daily_trade_review | 16:07:07.629903 | FAILED
reports/output/daily_trade_review_report_2026-08-31.xlsx → does not exist
data_store/cron_marks/daily_trade_review.done → no mark
failure: reports/daily_trade_review.py:2537 render_capital_sheet
         cell.fill = FILL_GREEN if rec[key] > 0 else (…)
         TypeError: unhashable type: 'StyleProxy'   (died at :2830)
critical escalation = YES (see item 7) · data lost = NO (regenerable)
```

⛔ **NOT "one of three ported sheets failed"** — that implies the other two passed.
The job **died at :2830**, so any sheet rendered after `render_capital_sheet` never
ran. **Capital sheet FAILED; the other two ported sheets are UNKNOWN.**
Unexercised ≠ proven. Sheet order not yet established.

Both halves of `1a1cb25 → dee5fcf → bee9755` behaved to spec — retirement clean,
replacement failed — and **the net delivered function is a regression**: the old
report is gone and the new one produced nothing. This is the single-point risk
flagged since FILE 68, realised on day one.

---

## 7 · 18:50 — CRON OFFICER, FIRST VIEW OF `output_retention`

```
TITLE: Cron EOD 2026-08-31          SEVERITY: CRITICAL
SUMMARY   Failed: 1   Missed: 0
FAILED (1)  - 16:07  daily_trade_review — unhashable type: 'StyleProxy'
Added   : output_retention
02:10  output_retention     Completed  0s
16:07  daily_trade_review   Failed     6s
```

`output_retention` **is** visible to the Officer and reported `Completed`, flagged
`Added` on its first appearance. The 09:50 membership check (`in_set=True`) held.

🔴 **CORRECTION TO MY OWN 16:11 PREDICTION.** I said the failure would be
"reported but not escalated," reasoning from `critical_miss = any(j.critical for j
in missed)` plus `daily_trade_review: critical: false`. **The alert is
`SEVERITY: CRITICAL`.** Escalation is broader than the one function I read. I
reasoned from a mechanism to an outcome instead of measuring the outcome.

🔴 **AND MY OWN INSTRUMENT COULD NOT SEE IT.** The health poll counts
`"level":"CRITICAL"` in `logs/system_<date>.log` — the trading app's log. The Cron
Officer is a separate process writing a **sentinel file**. `crit` stayed 4 all
evening while a CRITICAL was being raised. S-5 applied to my own instrumentation:
an entire artifact class outside the search space.

### 18:45 System Manager EOD — independent corroboration

```
P&L: gross ₹5.44 | charges ₹4.96 | net ₹0.48     Trades: 5
Partial fills: 0 · Orphan exit orders: 0 · HARD_KILL: 0
Capital drift events: 1 · SOFT_KILL activations: 1 · Manual/external (CHECK1): 1
Service starts today: 1 · crashes: 0
deployed tree == HEAD (39292d3), no tracked drift
SUMMARY: 0 violation(s), 11 warning(s)
```

📌 **CHECK1 counts one manual close — NIACL.** SPLPETRO closed with **no GTT leg
triggered** (exit 729.70 sits between SL 723.10 and TGT 759.95) yet is labelled
`GTT_EXIT`, so its external close is **invisible to the manual-close counter**.
The misnomer mis-attributes a real external close. Recorded; no historical rows
retrofitted.

📌 Carried for tomorrow, from the system's own words: *"SOFT_KILL … prior-day at
the next open, so the 2026-09-01 08:15 boot auto-clears it (HEADLESS GUARANTEE).
No action needed; ⛔ do NOT run `deploy/resume.sh` for this."*

---

## 8 · WHAT DID **NOT** HAPPEN

- **`F_RECIPIENT_CONFIRMED` — never confirmed to this session.** Two alerts sit in
  the mailbox (08:15:18, 15:05:03), both with the recipient in the log.
- **Candidate-bearing 15:07 behaviour — NOT EXERCISED.** MIS flat all afternoon.
- **F6-EOD's discriminating case — NOT EXERCISED**, owed since 25-Aug. The service
  self-exited cleanly at **17:35:04** (`Result=success`, `ExecMainStatus=0`, WAL
  `checkpointed=323/323`), but the mechanism named its own branch:
  `eod_self_exit: past 17:35 IST and flat (0 active positions)`. **Five flat EODs
  are not one discriminating EOD.**
- **P9 carry trigger — NOT TRIGGERED.** Three independent surfaces agreed: 0 OPEN
  rows, broker-derived `held=0.00 carry=0.00 residual=0.00`, 0 ACTIVE `gtt_state`.
  The **REVERT trigger has still never been evaluable** — `carry > 0` false on
  every sample ever taken. Nothing adjudicated, tuned or widened.
- **The whole P9 cluster stays owed** — U1-T+1, OWED-2, G3-T+1 (since 20-Aug),
  CARRY CHECK 1/2a/2b.
- **The emergency SOFT_KILL branch — NOT EXERCISED.** Both ends of the *scheduled*
  branch were: auto-clear 08:15:06, activation 15:15:01.
- **No report exists for 31-Aug.**
- **`daily_report`'s other two ported sheets — status UNKNOWN.**
- **F1 stays UNTESTED** — a broker *order* rejection is not the *config* rejection
  F1 needs.

---

## OPEN FINDINGS RAISED TODAY (none fixed)

1. 🔴 **Gate reachability.** `SYMBOL_DIRECTION_DAILY_LIMIT` is enabled,
   product-blind and correctly computing. It **fired** for
   `positional_sector_rotation` at 10:11 on KOPRAN LONG (n=1) and **did not fire**
   for `gap_go_long` at 12:33 on the same symbol and direction; the order reached
   the broker. Gate called at `signal_processor:1152/1935/2245`. **Cause NOT
   established.** Not a cleanup leak — the FAILED trade is correctly excluded from
   the count. *Harmless by accident:* had KOPRAN not been MIS-blocked, that order
   would have filled.
2. **v45 attribution columns** `closure_source` / `exit_mechanism` — **empty on the
   observed GTT-exit row**. Whether any writer exists anywhere is unmeasured.
3. **Smart TGT** — `SmartTgtManager` was constructed, ran all day and stopped
   cleanly in the ordered shutdown, against a record of *"trailing stop fired 0
   times in 134 trades."* **Ran ≠ wired**; α/β/γ all still live. Unclassified.
4. **In-flight tracking is in-memory and emits nothing on claim or release.** Its
   failure mode is silence. Cleanup was verified behaviourally on 31-Aug only
   because 21 further KOPRAN signals happened to arrive.
5. **`except Exception: charges = 0.0`** in `order_placer` silently books zero
   charges on a cost-calc failure. **0 occurrences today and Friday — LATENT.**
6. **KOPRAN cross-pipeline pairing** — `positional_momentum_long` (CNC, traded)
   and `gap_go_long` (MIS, rejected), same symbol, same day, two pipelines.
   Evidence for the unmade ruling (2); ⛔ not a finding against the system.
7. **MIS-eligibility is not pre-checkable** from anything the system fetches —
   `instruments.csv` carries no eligibility field. The broker's public sheet is the
   only known source. Design question, nothing built.
8. **Broker rejection class recurs** — 2 observed events across the retained
   5-trading-day window. Historical frequency **not measurable** (`output_retention`
   keeps 7 files per family). Never a rate.

---

## WHAT WORKED, WITH ITS BOUND

- **GTT orphan cleanup, live.** 15:20:36 — forensic-log → `delete_gtt` (mode=LIVE)
  → finalise → `gtt_state` CLEANED. The **same-day-SELL** case that previously
  blocked the `held == 0` door was reached and finalise ran.
  ⛔ Bound: the desired behaviour was exercised and succeeded; the specific causal
  contribution of `b5d6c8b` is **not separately established** by this natural event.
- **Broker-rejection cleanup, four legs, each independently evidenced** — capital
  reservation released (residual 0.00 unchanged across 12:33), signal reached
  `PLACEMENT_FAILED`, in-flight claim released (21 later KOPRAN evaluations), dedup
  did not consume the symbol. The cleanup lives in the shared `except`/`finally`, so
  it **architecturally covers** every rejection class — ⛔ but only the MIS-restriction
  class was **exercised**.
- **Cancel-refused-while-filling**, 10:57 — the system did not force local state to
  CANCELLED on an order that was filling; it deferred to `order_monitor` and the TGT
  resolved COMPLETE. ⛔ Bound: that is the **shared** mechanism inside a normal exit;
  **F's own PASS-1 sequencing remains NOT EXERCISED.**
- **CAPITAL_DRIFT 10:06:17** decomposed exactly — delta 868.84 ≡ margin_residual ≡
  (held_today − broker_used), `realised_pnl=0.00`; and `broker_net + broker_used =
  10466.80` = real capital ⇒ **no missing capital**. Resolved to 0.00 by 10:56.
  Operand mismatch, not a loss. No tuning.

---

## TREE DECISION — 👤 RAMA'S CALL, NOT MADE HERE

Project definition retained: **TREE = the last SHA PROVEN TO BOOT.**
Stated plainly: *proven-to-boot ≠ reverting there restores every subsystem.*

| | `52ccb4f` (current TREE) | `39292d3` (candidate) |
|---|---|---|
| daily report | ✅ **working path** | ⛔ **none** until StyleProxy repaired |
| F orchestrator | ⛔ absent | ✅ present, scheduled arm proven |
| retention | ⛔ absent | ✅ armed, rc=0, delete 0 |
| cron officer | ⛔ absent | ✅ ran, escalated the failure |
| email recipient | ⛔ old address | ✅ live, recorded in log |
| product discrimination | ⛔ unproven | ✅ `cnc_excluded=1` |
| GTT orphan cleanup | ⛔ unproven | ✅ live `delete_gtt` 15:20:36 |
| `daily_report` retirement | n/a | ✅ clean (both flags verified) |

**Each target is now missing something the other has, both measured.**
The asymmetry is **temporary**: the report defect is localized, regenerable and one
bounded repair away; `52ccb4f`'s lack of F is not. **That is weight, not a
recommendation.**

⛔ An open defect is **not** an automatic HOLD — this is a reporting defect, not
trading or state corruption. **Rama decides with it visible, not around it.**

---

## STANDING OBLIGATION

👤 **F6 nightly stop** — already satisfied tonight: the service self-exited at
17:35:04 and is `inactive`. No manual stop was needed or made.
⚠️ **Tuesday's 08:15 boot is a separate observation, not a consequence of tonight's
clean shutdown**, and it depends on the morning token refresh — which **fails
silently, not loudly**. Check the token file first.
