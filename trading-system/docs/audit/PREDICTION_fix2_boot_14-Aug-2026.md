# PREDICTION — Fix 2's first live boot, Friday 14-Aug-2026

**FROZEN 2026-08-13T18:55:09 IST, BEFORE the push of `1c8c710`.**
⛔ **Nothing below this line is edited after the push.** Corrections and outcomes go in `ADDENDA`
at the foot of the file, under their own dated heading, and never by altering the frozen text.

---

## 0 · WHAT IS BEING DEPLOYED, AND THE STATE IT IS DEPLOYED INTO

**Target SHA `1c8c710bf4df60fcca8b09375d6cd723590d3820`** — Fix 2, four commits, refitted onto the
measured `origin/main` `2bfe9e2` at ~17:31 IST today. Net diff **6 files, 542 insertions / 7
deletions**, `md5 189de14d93065623b55f66cdbf087e35`, byte-identical to `da49ccd` and to `4bd8a42`
before it. Gate on this exact SHA: raw `rc=1`, 10 F / 5,579 P / 4 S / 5,593 collected.

The three code changes, read from the blob at `1c8c710`, not from a card:

1. **`scripts/preflight/checks/engine.py` — `CapitalDeploymentCheck` gains a predicate.** It
   previously returned `_passed()` on every reachable path below the div-0 guard. It now WARNs when
   `used > opening`. `Criticality.WARN` — it can never escalate a run to CRITICAL.
2. **`scripts/preflight/checks/broker.py` — `KiteFundsAvailableCheck` gains an adequacy floor.**
   The liveness predicate `cash <= EXPECTED_MIN_CASH (0.0)` is unchanged, with its original wording.
   A second predicate `cash < floor` is added, floor = `₹2,000`.
3. **`config/preflight.yaml` — new file**, holding `startup_floors.min_broker_cash_rs: 2000`.

**State it lands in, all broker-measured today:** book **FLAT** (`get_positions` → 0 positions
@ `17:29:49.911`; `get_holdings` → 0 holdings @ `15:18:19`; EOD Pass 2 `broker open symbols=0`).
Cash `margins().net = ₹10,578.60` @ `17:29:49.987`. 6 filled trades, **all MIS, zero CNC** ⇒ **no
carry**. Kill state `SOFT_KILL / circuit_breaker_force_close_15:15`, which the 08:15 boot
auto-clears under the headless guarantee. Service down since `17:35:04` via its own `eod_self_exit`.

**Timing — the windows are NOT 08:15.** Boot 08:15. Preflight **phase A = 08:30** (the funds check).
Preflight **phase B = 09:14** (the deployment check). Market opens 09:15.

## 1 · PRE-INSTALL CONTROL — captured `18:15:45 IST`, expires the moment the push lands

All five read *"before"*. Each flips, or is asserted not to flip, in §2.

| # | Probe | Value BEFORE |
|---|---|---|
| C1 | `ls config/preflight.yaml` | **No such file or directory** |
| C2 | `grep -c min_broker_cash_rs scripts/preflight/checks/broker.py` | **0** |
| C3 | `grep -c "used > opening" scripts/preflight/checks/engine.py` | **0** |
| C4 | `grep -c min_broker_cash_rs logs/preflight.log` | **0** |
| C5 | `EXPECTED_MIN_CASH` at `broker.py:26` | **`0.0`** |

VM md5 of the six files before the push — **all six differ from the PC blobs at `1c8c710`**, so the
post-push identity check can go red:
`config/preflight.yaml` **ABSENT** · `docs/audit/fix2_preflight_capital_checks_10aug2026.md`
**ABSENT** · `broker.py` `223122c1…` · `engine.py` `cfdedae3…` · `test_preflight_broker.py`
`beb33035…` · `test_preflight_engine.py` `1db51c00…`.

## 2 · THE PREDICTIONS

### P1 — the 08:15 boot is UNAFFECTED. Confidence HIGH.
Nothing in the boot chain reads the preflight sentinel; `main.py`'s only touchpoint launches a
missed phase detached and never reads a result.
**The one failure mode I could identify, and it is CLOSED BY MEASUREMENT rather than by the code's
own comment:** Fix 2 adds a new file *into `config/`*, and every AppConfig model is `extra="forbid"`.
Measured on the deployed tree tonight — `_CONFIG_FILES` is an **explicit 8-entry tuple**, there is
**no `glob`/`iterdir`/`listdir`** anywhere in `core/config_loader.py`, and `config/security.yaml`
already sits in `config/` unlisted (0 references). ⇒ a new file in `config/` cannot be picked up.
**FALSIFIER:** the service fails to start, or any Fix-2 file is named in a boot-time error.

### P2 — the presence signature appears at phase A, 08:30. Confidence HIGH.
`min_broker_cash_rs` is emitted as a structured field on **all three** branches of the funds check
(liveness-fail, adequacy-fail, pass), so any live run that reaches `margins()` must emit it.
**FALSIFIER:** `grep -c min_broker_cash_rs logs/preflight.log` still **0** after phase A.
⚠️ **ABSENCE HAS TWO INNOCENT CAUSES AND THEY MUST NOT BE READ AS "NOT DEPLOYED":** `ctx.is_paper`
returns SKIPPED on the first line (not applicable — LIVE), and **`probe is None` returns
`_skipped("no broker session (token missing/invalid)")` BEFORE the `margins()` call**, emitting no
field at all. A failed 08:15 token refresh therefore produces exactly the same absence as a failed
deploy. **Discriminate with C1/C2 on disk, never with the log alone.**

### P3 — `kite_funds_available` PASSES, wording `funds available: ₹X (floor ₹2,000)`. Confidence HIGH.
Tonight's cash `₹10,578.60` is above both `0.0` and `₹2,000`.
⚠️ **THE PREDICTED NUMBER CARRIES AN OPERAND UNCERTAINTY I AM NAMING RATHER THAN HIDING:** the check
reads `margins()["available"]["cash"]` **first**, falling back to `net` only if that is None. My
`₹10,578.60` is the **`net`** field. The logged `cash=` may therefore be a different operand.
**Predicted BRACKET, not a point value: `₹9,500`–`₹11,500`**, absent an external transfer.
**FALSIFIER:** a FAIL on either predicate, or `_warn("margins returned no cash field")`.

### P4 — `capital_deployment` PASSES at phase B 09:14 with `capital_deployed_pct` ≈ `0.0`. Confidence HIGH.
The book is flat and 09:14 precedes the 09:15 open, so no position can exist; `margin_used` sums
`trades.margin_reserved` over `OPEN/PARTIAL/EXITING` ⇒ ≈ 0 ⇒ `used > opening` is FALSE.
**FALSIFIER:** the WARN branch fires (`capital deployed …% of opening CASH — over 100%`), or a
non-zero pct appears.
⚠️ **A THIRD OUTCOME EXISTS AND IS NEITHER:** if the INIT ledger row is missing or non-positive at
09:14 the check WARNs `capital_deployed_pct unavailable: …`. That is a *div-0 guard*, ⛔ not the new
predicate, and must not be scored as P4 failing.

### P5 — a prediction about the EVIDENCE, not the system: the ₹2,000 floor CANNOT be shown to be config-driven from the log. Confidence CERTAIN.
`MIN_BROKER_CASH_RS_DEFAULT = 2000.0` in code is **equal to** the yaml's `min_broker_cash_rs: 2000`.
So `floor ₹2,000` in `logs/preflight.log` is consistent with **both** *"the yaml deployed"* **and**
*"the yaml is absent and the in-code default was used"* — the loader degrades silently by design.
⇒ **The yaml's arrival must be proven by `ls config/preflight.yaml` and its md5, NEVER by the logged
floor.** Anyone who cites the logged `₹2,000` as proof the config shipped has proved nothing.

### P6 — ZERO behavioural change to trading. Confidence HIGH.
Both new predicates are alert-only. `capital_deployment` is `Criticality.WARN`; the funds check is
CRITICAL but `report.py:44-51`'s `is_blocking` only rolls up the *report*, and nothing reads it.
No order, sizing, kill, capital or schema path is touched.
**FALSIFIER:** any change in entries, sizing, kills or capital attributable to these six files.

### P7 — the push resets `config/strategy_direction_registry.yaml`. Confidence HIGH.
`post-receive` runs `checkout -f main`, which resets all tracked files. Tonight's single
`system_manager_eod` violation (*deployed tree differs from HEAD in 1 file*) should therefore be
**absent** at tomorrow's 18:45 run and **re-appear** after the 16:22 officer run. Expected, lossless.
**FALSIFIER:** the drift survives the push, or does not return after 16:22.

### P8 — the crontab is unchanged. Confidence MODERATE.
The hook reinstalls the crontab only if `generate(registry) == canonical` on the deployed tree. The
tree delta is 6 files, none cron-related, so the relationship is whatever it already was.
**Baseline captured pre-push: `md5 b8276da7043975cda2d0ce6578960c6a`, 46 job lines.**
**FALSIFIER:** a different md5 or a different job count after the push.
*Confidence is MODERATE, not HIGH, because I did not evaluate `generate(registry)` against canonical
on the deployed tree — I am predicting invariance from the tree delta alone.*

## 3 · THE CEILING ON TOMORROW'S OUTCOME — stated in advance so it cannot be inflated afterwards

**The best available label tomorrow is `DEPLOYED`, plus *"present and passing on a flat, funded
book"*. ⛔ It CANNOT become `VERIFIED LIVE`, and this is structural, not cautious:**

- The **adequacy floor** only demonstrates its new behaviour when **cash < ₹2,000**. Tomorrow's cash
  is ~₹10,578. **No such morning is scheduled**, and one must never be manufactured.
- The **`capital_deployment` WARN branch** only fires when `used > opening`, which is reachable
  **only via a carry**. The book is flat and no delivery entry is scheduled.

⇒ Tomorrow exercises the **PASS** arm of both new predicates and **neither new failure arm**. A green
morning is evidence the code is present and does not break a healthy boot — ⛔ it is **not** evidence
the floor works. That evidence requires a state that has not occurred since 10-Aug.

## 4 · WHAT MUST NOT BE CONCLUDED

- ⛔ *"The gate passed"* — the mandated wording is *"full clean-worktree regression completed; rc=1;
  all failures independently attributed; no Fix-2-specific failure found."*
- ⛔ *"The ₹2,000 floor is verified"* — see §3. It will not have been exercised.
- ⛔ *"The config file is live because the log says ₹2,000"* — see P5.
- ⛔ *"No signature ⇒ not deployed"* — see P2's two innocent causes.
- ⛔ A PASS on P3/P4 does **not** retire M-C2, F6, Fix 3, or the 76.9 % delivery-book ceiling.

## 5 · SCORING ORDER FOR TOMORROW — nothing before it

1. Did the service boot at 08:15? If not, **every P below is `NOT TESTED`**, not failed.
2. C1–C4 on disk **first** (did the code arrive), then the log (did it run).
3. P2 → P3 at phase A 08:30. P4 at phase B 09:14.
4. Score P5 explicitly as a statement about evidence quality.
5. P7, P8 from the deployed tree and the crontab.
6. Only then the label — and §3 caps it at `DEPLOYED`.

---

## ADDENDA
*(⛔ Nothing above this line is edited. Outcomes and corrections are appended here, dated.)*

---

## ADDENDUM 1 — SCORED, Friday 14-Aug-2026, windows 08:30 / 09:14

**Label reached: `DEPLOYED` + *proven live-loaded*. NOT `VERIFIED LIVE`. This is the ceiling §3
stated in advance, and it was not exceeded.**

Ladder: (1) file on disk — proven (md5, 13-Aug, re-verified today) · (2) the running process loaded
it — proven today · (3) the predicates are CORRECT — **NOT REACHED**, neither failure arm fired.

### Boot
`ExecMainStartTimestamp` **Thu 13-Aug 08:15:16 -> Fri 2026-08-14 08:15:12 IST**, `active`/`running`,
`MainPID 3612311`, `NRestarts=0`. A pre-boot control was taken at `08:10:32` reading `inactive`/
`dead` with the stamp still on *yesterday*, so the post-boot read is a measurement, not an
observation. **`HARD_KILL` today: 0.** Prior-day `SOFT_KILL` **auto-cleared** at `08:15:13.714` ->
`INACTIVE`, `auto_clear_stale`, by `main.auto_clear_stale`.

### Scores

| # | Call | Verdict |
|---|---|---|
| P1 | boot unaffected | **CONFIRMED** |
| P2 | presence signature at phase A | **CONFIRMED** — but its falsifier is **mis-specified**, see below |
| P3 | funds check PASSES, wording | PASS + wording **CONFIRMED**; **BRACKET REFUTED** |
| P4 | `capital_deployment` PASSES ~0.0% | **CONFIRMED** |
| P5 | floor not provable from the log | **CONFIRMED** (statement about evidence) |
| P6 | zero behavioural change | holds so far; **entries NOT YET DETERMINABLE** (`entry_start=10:00`) |
| P7 | registry reset by the push | first half CONFIRMED; **second half NOT YET DETERMINABLE** (16:22) |
| P8 | crontab unchanged | **CONFIRMED** |

**P1.** `"Config loaded from config (8 files)"` — the explicit 8-entry tuple. `config/preflight.yaml`
is a 9th file in `config/` and was **not** picked up, so `extra="forbid"` never engaged. The one
identified boot risk is now closed live as well as pre-push. Zero Fix-2 files named in any error.

**P2 — CONFIRMED, and the falsifier as written FIRED ANYWAY. This is the finding of the morning.**
Phase A ran `08:30:03` (marker `0 2026-08-14T08:30:03+05:30`, rc=0). The signature, `preflight.log`
line 4432:

    kite_funds_available   PASS   38ms  funds available: Rs 5,589 (floor Rs 2,000)

Non-vacuous: the **eleven** prior runs in the same file (lines 3156-4316, 04-Aug to 13-Aug) all read
`funds available: Rs X` with **no `(floor ...)` suffix**. The suffix exists in exactly one run:
today's. **BUT `grep -c min_broker_cash_rs logs/preflight.log` is STILL `0`** — the falsifier's
literal text. Cause: `preflight.log` renders a human tree (`|- name  PASS  Nms  message`) and
**never carries structured field names**; C2 shows `min_broker_cash_rs` appears **6x** in
`broker.py`, it simply does not reach this log. So **the falsifier can fire on a correct deploy, and
did.** Anyone following it literally would have reported *"the running process is NOT the new code"*
about a process that demonstrably is. Same evidence-quality family as P5: a probe aimed at the wrong
artefact.
P2's two innocent causes were both ruled out **in advance**: run header `LIVE/LFL836` (not paper),
and `kite_token_fresh_today  PASS  token minted today (2026-08-14)` (token file mtime
`2026-08-14 08:15:01.694`), so `probe is None` was impossible.

**P3 — PASS and wording CONFIRMED; the BRACKET is REFUTED, and the cause is timing, not mechanism.**
Predicted `Rs 9,500`-`Rs 11,500`; logged **`Rs 5,589`** at 08:30. The operand escape P3 named does
**not** explain it — the boot's adapter log reads `result_summary:"net=5588.6"`, the **same `net`
operand** behind yesterday's `Rs 10,579`. What actually happened, measured from consecutive
`get_margins` calls: `net=5588.6` held from `08:15:26` through **`09:16:10.750`**, then stepped to
`net=10588.6` at **`09:16:25.847`** and held. A single **+Rs 5,000.00** credit at ~09:16, just after
the 09:15 open. Yesterday's close was `Rs 10,578.60`, so today's settled figure is
**`Rs 10,588.60`, i.e. `+Rs 10.00`**.
So the bracket was wrong **in the 08:30 window** and would have been right 46 minutes later. Scored
**REFUTED** on the number as measured; not softened, and not re-labelled by the later value.

**P4 — CONFIRMED.** Phase B ran `09:14:02` (marker `0 2026-08-14T09:14:02+05:30`, rc=0). Line 4489:

    capital_deployment  PASS  1ms  capital deployed 0.0% of opening cash (margin_used Rs 0 / opening cash Rs 5,589; pending Rs 0)

`grep -c "of opening cash"` = **1** across all 4,500 lines, so this is the first-ever occurrence.
Prior runs read `... 0.0% (margin_used Rs 0 / total Rs 10,579; ...)`. The WARN branch did not fire.
And the P4 third outcome did **not** occur — no `capital_deployed_pct unavailable`; a real 0.0% over
a real denominator, so the **new predicate genuinely evaluated** and returned FALSE.

**P5 — CONFIRMED, and honoured in practice.** The log does say `(floor Rs 2,000)`, and that proves
nothing, `MIN_BROKER_CASH_RS_DEFAULT = 2000.0` being equal to the yaml's `2000`. The yaml's arrival
was proven **separately, by `ls` + md5 on the VM**: `-rw-rw-r-- ubuntu ubuntu 2108 Aug 13 18:56`,
`md5 8e841fb949a7a5ca6f047f8c6127927f` = the D2-recorded value. Reported as two separate lines.

**P8 — CONFIRMED.** `crontab -l | md5sum` = `b8276da7043975cda2d0ce6578960c6a`, **identical** to the
pre-push baseline; **46** job lines (of 148 total), identical. Phases **A `30 8 * * 1-5`**,
**B `14 9 * * 1-5`**, **C `15 9 * * 1-5`** all present and `1-5` covers Friday, so an absent
signature could not have been blamed on a missing entry. `N13-11` holds a second time: the hook
again printed *"crontab AUTO-INSTALLED from canonical"* while the **content did not move**.

### A CRITICAL fired, and it is NOT Fix 2 — attributed by width, not by assumption
`09:16:25.848 ERROR order_reconciler` — `G3 CAPITAL_DRIFT: expected=5588.60 actual=10588.60
delta=5000.00 tolerance=558.86 (base=50.00 human_orders=none)`, dispatched as a CRITICAL-severity
telegram at `09:16:26.497`. `drift_handler` logged `"drift event from non-escalating source"`,
`tier=HARD`, so **it alerted and could not escalate**, exactly as recorded for G3.
It is the Rs 5,000 credit above, seen from the reconciler's side: capital was snapshotted at boot
(Rs 5,588.60) and the broker moved under it. **Width measured across every August log:** the class
fired 05-Aug **17x**, 06-Aug **12x**, 07-Aug **6x**, 11-Aug **2x**, 12-Aug **2x**, 14-Aug **1x**;
zero on 03, 04, 10, 13. So **it predates the deploy on five separate days** and `order_reconciler`
is not among Fix 2's six files. Not attributable to Fix 2.
**But the recorded decomposition does NOT apply today.** The standing note says the drift delta
= *deployed capital + unsettled realised P&L*. Today deployed = Rs 0 and trades = 0, so that
decomposition yields Rs 0, not Rs 5,000. **Today's cause is a broker-side credit, a different
mechanism wearing the same alert.** Recorded, not chased.

### A BONUS FINDING: the new predicate is REACHABLE, proven from the historical record
`preflight.log` line 4025, `PRE-FLIGHT — Phase B — 10-Aug-2026`:

    capital_deployment  PASS  1ms  capital deployed 432.3% (margin_used Rs 907 / total Rs 210; pending Rs 0)

That is a **real production state where `used > opening`** (Rs 907 > Rs 210) which the **old code
PASSED silently**. Under Fix 2 that same state WARNs.
This answers *"could this check ever go red?"* with a measured **YES** — the predicate is
non-vacuous. **It does NOT make it `VERIFIED LIVE`:** the code was not deployed on 10-Aug and this
is a retrospective read of a log, not an execution. Rung (3) still requires a live firing.

### ONE LATENT OBSERVATION — documented, not chased, not fixed
Phase B's new operand is the **opening** snapshot: it recorded `opening cash Rs 5,589` at 09:14 while
live cash became `Rs 10,588.60` at 09:16:25 — a Rs 5,000 divergence **within two minutes of the
check**. If margin used ever exceeds the *opening* snapshot while actual cash is higher, the new WARN
can fire on a healthy book. **LATENT** (needs `used > 5,588.60`; today `used = Rs 0`), not LIVE, so
per the live-vs-latent rule: continue, document, do not chase. No code was touched.

### A method error of my own, caught before it was reported as a finding
The re-verification of this file's frozen md5 first came back **mismatched**. The file was not
touched — `mtime 2026-08-13 18:56:12.791`, 10,260 bytes, 154 lines, **0 CR bytes**. My region
selector was wrong: the frozen region is **`head -153`** (through the `## ADDENDA` heading itself),
which reproduces `2a193eb8cb5cfddb8f360752ab6c4f97` exactly. The mirror of the standing rule:
*a green check is evidence only if it could have been red* — and **a RED check is evidence only once
its method is verified.** A mis-specified probe reports a false alarm in whichever direction it
points; today it pointed both ways (here, and at P2's falsifier).

### What today did NOT do
No deploy · no push · no service start/stop/restart · no kill clear · no `resume.sh` · no config
edit · no code · no broker **call** of my own (every cash figure above is read from the system's own
logs) · no second unit · no M-C2 · no filesystem cleanup · nothing removed under `D:\Projects\` ·
no worktree/branch/tag touched (**worktrees 9 · heads 78 · tags 32 — unchanged**) · no failing
state manufactured · nothing edited above the addenda line.

---

## ADDENDUM 2 — P7's SECOND HALF SCORED, 14-Aug-2026 16:25 IST

**P7 ✅ CONFIRMED IN FULL. All eight predictions P1–P8 are now scored, and the
prediction is closed.**

### The measurement, with its control taken FIRST

| when | registry mtime | size | tracked-file drift |
|---|---|---|---|
| 09:18:00 | `2026-08-13 18:56:31.764` (the push) | 5,745 B | **EMPTY** |
| **16:21:56** (pre-officer) | `2026-08-13 18:56:31.764` | 5,745 B | **EMPTY** |
| officer marker | `0 2026-08-14T16:22:01+05:30` (rc=0) | — | — |
| **16:25:13** (post-officer) | **`2026-08-14 16:22:01.809`** | **3,734 B** | **` M config/strategy_direction_registry.yaml`** |

⭐ **The 16:21:56 reading is what makes this evidence rather than observation** —
four minutes before the run the drift was still absent, so the post-run `M` could
only have come from the officer. ⛔ Without it, "drift is present at 16:25" would
have been consistent with drift that had been there all along.

**P7's falsifier was:** *"the drift survives the push, or does not return after
16:22."* ⇒ **Neither occurred.** First half confirmed 13-Aug (the push's
`checkout -f` reset the file to seed); second half confirmed now (it re-diverged
at the officer run). **Expected, lossless, and exactly as predicted.**

### ⭐ A bonus the byte count makes visible
The file went **5,745 → 3,734 bytes, a loss of 2,011 bytes**, while its mtime moved
to the officer's run. That is `N11-03` — *the self-erasing invariant* — witnessed
again with exact figures: `scripts/strategy_registry_officer.py` rewrites the yaml
through a PyYAML round-trip that **strips the 25-line header block**, the only
in-repo statement of the "nothing reads direction from here" rule.
⛔ Recorded, ⛔ not chased, ⛔ nothing fixed.

### FINAL SCORECARD — Fix 2 (`1c8c710`), first live boot

| # | Verdict |
|---|---|
| P1 boot unaffected | ✅ CONFIRMED |
| P2 presence signature at phase A | ✅ CONFIRMED — **falsifier mis-specified and fired on a correct deploy** |
| P3 funds check PASSES + wording | ✅ PASS/wording · ⛔ **BRACKET REFUTED** (₹5,589 vs ₹9,500–11,500; a +₹5,000 credit landed 09:16:25, 46 min after the window) |
| P4 `capital_deployment` ≈0.0% | ✅ CONFIRMED |
| P5 floor unprovable from the log | ✅ CONFIRMED (statement about evidence) |
| P6 zero behavioural change | ✅ CONFIRMED — 1 trade (CAMLINFINE SHORT, TGT_HIT, **+₹2.28**), nothing attributable to the six files |
| P7 registry reset then re-diverge | ✅ **CONFIRMED IN FULL** (this addendum) |
| P8 crontab unchanged | ✅ CONFIRMED |

**LABEL, FINAL: `DEPLOYED` + *proven live-loaded*. ⛔ NOT `VERIFIED LIVE`.**
Ladder rung ③ was never reached — neither new failure arm could fire on a flat,
funded book, exactly as §3 stated in advance. ⛔ The ceiling was not exceeded and
⛔ no failing state was manufactured to reach it.

⏱️ **P7's closure also releases the standing *"no GUI push until P7 closes"* gate.**
⚠️ It does **not** release the other blocker: the GUI branch is **4 behind**
`origin/main` and `git push --dry-run` returns **`! [rejected] … (non-fast-forward)`**
— a rebase onto `1c8c710` producing a NEW SHA, with its own verification run, is
still owed.
