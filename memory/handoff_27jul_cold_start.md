---
name: handoff-27jul-cold-start
description: "COLD-START HANDOFF for 27-Jul-2026. Six branches all PUSHED to origin (main untouched, nothing deployed). What each carries, its slot, and what is owed tonight."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T13:10:27.247Z
---

# ▶️ READ FIRST ON RESUME — 27-Jul-2026 (Monday)

## ✅ SUPERSEDED 18:1x–19:0x — THE EVENING RAN. Everything below is the 16:0x snapshot.

**Checks 4-7: ALL PASS.** Service ran **08:15:30 → 17:35:04 unbroken, NRestarts=0, exit 0** (that one
fact answers checks 4 AND 7, and covers the whole 16:00–17:35 blind spot better than a point probe
would have). `pb01_capture` heartbeat 17:00:03 **and** 25 rows written — **the first real PB-01
capture ever**. VM `up 23 days` — the power cut never touched it. 111 heartbeats, 0 non-SUCCESS.
13 ERROR/CRITICAL, all classified, none unexplained. ⭐ **The rotated TOTP is now PROVEN against the
live broker** — 4 real orders reached Zerodha. That was an open unknown.

**✅ v45 PUSHED 18:17:37** on Rama's confirm — `d0fd7b8`→`d3fa5b8`, fast-forward, crontab
**byte-identical**, service **not** restarted. ⚠️ **It bought a night of ~25 CRITICAL "Schema
migration refused" emails** (live DB stays v44 until the Tue 08:15:30 boot). Rama ACCEPTED; the
token still refreshes; NOT an incident. [[schema-push-overnight-refusal-27jul]]
📄 **Tuesday's expectations pre-written: `Downloads/TUESDAY_28-JUL_CARD.txt`** — good boot, failed
migration, and the one-command rollback.

---

## The 16:0x snapshot, as written before the power cut

⭐ **EVERYTHING IS ON THE VM. Nothing is lost if the PC never comes back.** All six branches were
pushed ~16:0x. ⛔ **`main` was NOT pushed ⇒ NOTHING WAS DEPLOYED.** Verified after: deployed tree
still `d0fd7b8`, service `active`, `NRestarts=0`, start still Mon 08:15:30.

## THE SIX HEADS (all on origin, none merged to main)

| branch | head | +n | what it is | slot |
|---|---|---|---|---|
| `hold-check1-w8-26jul` | `d3fa5b8` | 24 | **v45 SCHEMA MIGRATION** | ⏳ after Monday is observed clean |
| `fix-tests-27jul` | `1542c6e` | 3 | test-only: instance-lock fix · **outbound-network guard** · **real-`data_store` guard** | Thu 30-Jul eve |
| `fix-boot-27jul` | `14305e1` | 2 | ⚠️ **BOOT PATH ×2**: #16a BLOCK gate · S4 degrade | Thu 30-Jul eve |
| `fix-symdir-27jul` | `300a247` | 7 | ⚠️ **the one-trade rule (ON)** · mis_filter SHADOW · alert audit trail | **Fri 31-Jul eve** |
| `fix-t2-repair-07jul` | `854112b` | 3 | the repaired T2 script | Tue 28-Jul eve (with the band widen) |
| `docs-27jul` | `4e85a9f` | 1 | the day's 5 analysis documents | any time (docs only) |

⛔ **`fix-symdir-27jul` is STACKED on `fix-tests-27jul`** — the network guard must be present whenever
a suite runs, or the gate itself posts to Rama's live channel. **Do not deploy symdir without it.**

## ⏳ OWED TONIGHT

Checks **4** (~17:10 `is-active`) · **5+6** (after 17:00 — heartbeat AND row count; **heartbeat-but-
no-rows is a REAL state**) · **7** (~17:40, the **17:35** self-exit, not 16:00). **Then, only on
Rama's confirmation, push the 24 to `main`.** ⛔ **No service restart.**
📄 **If the PC is down: `Downloads/TONIGHT_IF_PC_IS_DOWN_27-JUL.txt`** has every check as a
copy-paste SSH one-liner, plus the answer to the calendar question below.

## ⭐ IF THE PUSH SLIPS — ANSWERED IN ADVANCE

**Cost = ONE DAY and nothing else.** The check evidence does not expire; "Monday observed clean"
stays true.
⛔ **But do NOT let it land on WEDNESDAY's boot — that is the T2 ARM day.** v45's failure mode is
*the service does not start*, which is the worst thing possible on the morning a real CNC position
is armed. **Slip to Thu 30-Jul eve ⇒ Fri 31-Jul boot takes v45 alone**, and everything downstream
shifts one slot. ⭐ **Nothing in the T2 sequence depends on v45** — the script is standalone, sets its
own `delivery_enabled=True`, and writes to a throwaway DB.

## ✅ NOTHING IS OWED — the last gate landed 16:3x

`1542c6e` (the real-`data_store` guard) gated clean: **10F / 5146P / 4 skipped**, failure set
IDENTICAL to the documented PC-env baseline, **0 `REAL data_store` trips, 0 `BLOCKED outbound`
trips**. Predicted 5146 before the run, observed 5146.

## DECISIONS MADE TODAY

- ✅ **The one-trade rule is ON** — `config/system_config.yaml` → `risk.
  one_trade_per_symbol_direction_per_day: true`. **Earliest LIVE = Mon 3-Aug 08:15.** The CODE default
  stays `False` so an absent key cannot silently enable it.
- ⛔ **MIS→CNC fallback: CLOSED, will not be built.** Architecture settled: INTRADAY=MIS ·
  DELIVERY=CNC/GTT.
- ✅ **#16a → BLOCK · S4 → DEGRADE** [[failfast-vs-degrade-discriminator-27jul]]
- ✅ **T2 band → −10/+10, arm ~13:00**, applied Tue eve with the merge ⚠️ **and the runbook's
  step-zero sha256 MUST be rewritten in the same sitting** or Wednesday's card says STOP.
- ⛔ **2FA seed move deferred to Fri 7/Sat 8-Aug** (not 31-Jul — that made 3-Aug a credential day).
- ⚠️ **Slot SPLIT 27-Jul eve, retracting my own earlier answer:** the rule going ON made it a live
  behavioural change, so Thu-eve would have been a 3-variable boot. Boot-path pair → Fri boot; the
  rule → Mon 3-Aug boot.

## THE DAY'S FINDINGS

[[senco-double-entry-27jul]] · [[test-suite-sends-real-telegram-27jul]] ·
[[test-side-effect-class-27jul]] · [[instance-lock-flake-mechanism-27jul]] ·
[[slice25-execution-plan-27jul]] · [[failfast-vs-degrade-discriminator-27jul]]

⭐ **The one that outranks the rest: after a TGT_HIT the symbol traded HIGHER later the same day in
49 of 50 cases (98.0%, n=50).** That is the strongest evidence yet that **the TARGET is the lever** —
and it corroborates the 24-Jul exits conclusion from a new direction. It is also why the price-based
re-entry rule was the dangerous proposal.
⭐ **And the proportion: first entries are −₹71.91 across 181 trades, win 40.3% vs ~43.5% breakeven.**
A third independent arrival at that number. Everything cleared since 24-Jul is correctness, safety
and observability — **none of it makes the system profitable.**
