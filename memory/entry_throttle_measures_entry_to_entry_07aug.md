---
name: entry-throttle-measures-entry-to-entry-07aug
description: "per_symbol_cooldown_sec=300 measures PREVIOUS ENTRY -> NEW ENTRY, never exit->entry — so it is NOT a fallback for gate 1: its residual protection is max(0, 300 - holding_period), which is ZERO on 82.2% of trades. Measured 07-Aug-2026, read-only."
metadata: 
  node_type: memory
  type: project
  originSessionId: f38a8269-a152-4e11-86f5-0a065785e4e0
  modified: 2026-08-07T11:55:26.885Z
---

**MEASURED 07-Aug-2026 evening, READ-ONLY. Report: `docs/audit/rulings_1_2_verification_07aug2026.md`
§8 (an APPEND — it closes that document's own OPEN-1/OPEN-2 and corrects its H1/H7 row 5).**

⛔ **`_per_symbol_last[symbol]` IS WRITTEN AT EXACTLY ONE PLACE IN THE REPOSITORY —
`signals/entry_throttle.py:113`, inside `admit()`, on the admit path only.** *(Width: repo-wide grep
for `entry_throttle|EntryThrottle|per_symbol_cooldown|\.admit\(` over every `*.py`; every other hit
is a constructor argument, a metrics read, or one of the three `admit()` calls.)* **There is no exit
hook, no fill hook, no reconciler touch — the class CANNOT LEARN that a position closed.**
`admit()` fires at **DISPATCH**: all three production `_placer.place(` sites
(`signal_processor.py:1263 · :2028 · :2305`) are each immediately preceded by it
(`:1249 · :2017 · :2296`). There is no fourth.

## 🔑 THE CONSEQUENCE THAT MATTERS — do not reason about this control without it

> **RESIDUAL PROTECTION AGAINST AN IMMEDIATE RE-ENTRY = `max(0, 300 − holding_period)`.
> For any trade held longer than five minutes it is ZERO.**
> **(P)** over 225 closed trades carrying both timestamps: **185 = 82.2 % were held ≥ 300 s**;
> median hold **1,596 s = 5.3×** the cooldown.

⇒ ⛔ **THE 300 s COOLDOWN IS NOT A FALLBACK FOR GATE 1.** If
`risk.one_trade_per_symbol_direction_per_day` is ever flipped to `false`, then on ~82 % of trades an
immediate same-symbol re-entry after a completed exit falls back onto **nothing**: gates 2+3
(`DUPLICATE_SYMBOL`/`CONTRARY_POSITION`) release the instant the trade leaves
`PENDING_FILL/OPEN/PARTIAL` by design, the concurrency caps were freed by the exit, and
`max_daily_trades` has not bound since 10-Jul. See [[rulings-1-2-taken-07aug]].

## SENCO 27-Jul — the arithmetic, operands quoted from `logs/system_2026-07-27.log`

entry dispatch `10:02:12.687` · TGT exit `10:13:31.744` · re-entry dispatch `10:14:12.331`

| interval | seconds | vs 300 s |
|---|---|---|
| **ENTRY→ENTRY — what the throttle actually measured** | **719.644** | **2.399× ⇒ correctly ADMITTED** |
| EXIT→re-entry dispatch | 40.587 | would have blocked |
| EXIT→re-entry fill *(= the record's "80 s", reconciled)* | 79.413 | would have blocked |

⭐ **THE THROTTLE NEVER SAW 80 SECONDS.** "A live 300 s cooldown did not stop an 80-second
re-entry" is **dissolved, not explained** — the two figures describe different intervals and **no
control in this system measures the second.**

## ⛔ THREE ALTERNATIVE EXPLANATIONS ARE REFUTED, NOT MERELY UNSUPPORTED

- **wrong value** — `git show d3fa5b8:config/system_config.yaml` reads `per_symbol_cooldown_sec: 300`;
  `git log -S` across config/class/processor/`main.py`/loader returns **one commit ever** (`c0554c6`,
  19-Jun) ⇒ never edited.
- **not on the path** — the gate fired **7×** that day, twice in its `per_symbol` category.
- 🔴 **state lost to a restart** — the **COMPLETE** `systemd[1]` record for 27-Jul is **THREE LINES**
  (`Started 08:15:30` · `Deactivated successfully 17:35:04` · CPU summary) ⇒ **one continuous
  process** spanning both entries. ⇒ **the throttle did not fail, was not reset, was not
  misconfigured. NOTHING HERE IS BROKEN.**

## ⭐⭐ PROVEN ON PRODUCTION DATA — the reject string prints its own operand

`f"per_symbol {symbol} {elapsed:.0f}s < …"` ⇒ `per_symbol PYRAMID 60s < 300s` @`10:07:14.035` sits
**60.334 s** after `place_start` `10:06:13.701`; `61s` @`10:12:14.835` sits **60.932 s** after
`10:11:13.903`. **And the discriminator is clean because PYRAMID NEVER EXITED — its 10:06 entry was
BROKER-REJECTED** (`MIS orders are currently blocked`) ⇒ an exit-keyed cooldown had no timestamp to
measure from and could not have printed either value.

⚠️ **AND THAT IS A FINDING IN ITSELF, in no document before today: `admit()` records BEFORE `place()`
(the deliberate TOCTOU-free design) ⇒ A BROKER-REJECTED ENTRY STILL CONSUMES THE SYMBOL'S FULL 300 s.**
PYRAMID blocked 3 later signals for a position that never existed. 🏷️ Same family as
[[counts-db-rows-not-broker-06aug]] — it counts its own **dispatch** where a reader assumes an
**entry**. ⛔ Not a defect; the TOCTOU rationale is sound.

⚠️ PYRAMID's two dispatches are **300.202 s** apart — it re-entered **0.202 s after expiry**. With a
~60 s scanner cadence **the cooldown SCHEDULES the re-entry rather than preventing it.** That is what
OPEN-2 turns on.

## OTHER PROPERTIES

- **Direction-BLIND and product-BLIND** — state is `dict[str, float]` keyed on the bare symbol
  (`:58`); `admit(self, symbol)` takes nothing else ⇒ a CNC and a MIS entry on one symbol contend for
  **one** cooldown.
- 📵 **PARITY IS `(I)`, NEVER `(P)` — exercised in LIVE ONLY.** All 24 retained daily logs
  (`2026-07-07`→`2026-08-07`, the full 30-day window) read `mode=live`; **zero paper days.**
  ⛔ "Never in paper" is NOT established — retention bounds the check. ⭐ But the standing
  PAPER-NETS-BY-SYMBOL hazard does **not** reach this control (it reads no broker quantity), so a
  paper drill here would be genuinely informative rather than vacuously green. See
  [[paper-cannot-exercise-class-26jul]].

## 🔴 AND THE FACT THAT REFRAMES THE WHOLE DECISION

**GATE 1 DID NOT EXIST WHEN SENCO RE-ENTERED.** The tree deployed at 10:14 on 27-Jul was `d3fa5b8`
(26-Jul 23:19) and **both halves are absent from it**. `656b62d` **27-Jul 13:54:12** wrote the code
(*"DEFAULT OFF"*); `300a247` **27-Jul 15:24:31** set it `true` (*"TURN ON … (Rama, 27-Jul eve)"*) —
**+3 h 40 min and +5 h 10 min after the re-entry, the same afternoon.**

⇒ **SENCO is the incident that CREATED gate 1, not a trade gate 1 happens to cover.** ⭐ Settles half
of OPEN-7: there was no pre-existing rule for a deploy to lag.

⛔⛔ **THIS IS A MEASUREMENT AND A FRAMING, NOT A RECOMMENDATION. The flip is Rama's, and the
counter-case is untouched:** the SENCO report measured the re-entry population at **n=2 over five
weeks, total stake ≈ ₹5** — *"two anecdotes… a rule justified on one blocked trade is a rule
justified on nothing."* **A control can be the only one of its kind and still not be worth its cost.**
What changed is that the price of removing it is now **known** rather than assumed.

Related: [[rulings-1-2-taken-07aug]] · [[entries-buy-extension-24jul]] ·
[[feedback-absence-needs-wide-check]] · [[unpushed-pending-deploy-ledger]]
