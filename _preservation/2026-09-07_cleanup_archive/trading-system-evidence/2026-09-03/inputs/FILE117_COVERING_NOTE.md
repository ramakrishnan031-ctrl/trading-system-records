# COVERING NOTE — FILE 117 (ChatGPT), "STOP_AFTER_C2 control-flow finding"

**Written 03-Sep-2026 under 👤 FILE 118 §2.3.**

## 🔴 PROVENANCE LIMIT — read first
⛔ **I have not read FILE 117.** 🔬 The artifact
`Reply_to_Web_Claude_FILE117_Scope_Control_Final_03Sep2026.txt` is **not present
on this machine** (searched; see `README_PROVENANCE.md`).
⇒ ⭐ Everything below is sourced **solely from the two fragments quoted inside
👤 FILE 118 §1.2**. ⛔ This note makes no claim about any part of FILE 117 that
FILE 118 did not quote.

## What FILE 118 quotes the TITLE / PREAMBLE as asserting
> "CRITICAL STOP_AFTER_C2 CONTROL-FLOW FINDING"
> "…the advertised STOP_AFTER_C2=true short run does NOT actually stop the
>  sweep at C2."

## What FILE 118 quotes FILE 117's OWN §1 as ruling
> "…the `break` targets the enclosing ROUTES loop, not the viewport loop… the
>  short-scope mechanism is structurally valid. My earlier concern about an
>  inner-loop break would be incorrect for this exact uploaded file; it does
>  not apply."

## 🔴 THE RULING, AND WHAT IT RESTS ON
⭐ **PRIMARY BASIS — MEASUREMENT, ⛔ not a reading of the source** (👤 FILE 120 §1.2):
🔬 This session settled the control-flow question **empirically, before FILE 117
existed**:
| test | scope flag | 🔬 measured |
|---|---|---|
| **G3** | `STOP_AFTER_C2: true` via the CFG hook | measured S17, then **did NOT measure the following route** |
| **G4** | `false` | **measured** the following route |
📄 `INSTRUMENT_VALIDATION_03-Sep-2026.md`, Round 3 §3.
⇒ ⭐ **The mechanism was SHOWN to stop.** ⭐ That is stronger than any reading of
the source — 👤 mine, 👤 Web Claude's or 👤 ChatGPT's.

⭐ **CONCURRING READINGS, ⛔ neither of them the basis:**
- ⭐ FILE 117's own §1 (as quoted): the `break` targets the ROUTES loop ⇒ valid.
- ⭐ 👤 FILE 118 §1.2: the preamble is stale draft text; §1 onward is operative.

⇒ ⭐ **RULING: NO DEFECT · ⛔ NO SNIPPET MODIFICATION · ⭐ THE SCOPE HOOK IS
CORRECT.**
⚠️ 🔴 ⭐ **The ruling does NOT depend on FILE 117** — ⭐ which is essential, because
⛔ this folder does not contain it.

## Consequence for this round
- ⛔ `gui_sweep_snippet.js` is **not modified**. 🔬 It remains byte-identical at
  `743a7d461f8a171e228fd8d9d2ffce1fe0c59642f8408569ad3ff80fb10bec93`.
- ⭐ Scope is selected through the CFG hook, ⛔ never by editing the file:
  `window.__GUI_SWEEP_CFG = { STOP_AFTER_C2: true };`

## Why this note exists
⭐ 👤 FILE 118 §1.2: *"an evidence folder that contains a headline claiming a
critical instrument defect, filed without annotation, will be read in four days'
time as an unresolved defect. The annotation is the record's defence."*
⚠️ ⭐ **That defence is currently incomplete:** the headline it defends against is
⛔ not in this folder either. ⏸ 👤 File the real FILE 117 next to this note.

## ⛔ WHAT THIS NOTE IS NOT
⛔ **This is not an independent review of FILE 117.** ⭐ I have not read the
document. ⭐ It is an annotation recording (a) what 👤 FILE 118 quotes from it and
(b) the **measurement** that settles the same question without it.
⛔ It must never be cited as a review, an audit, or a reading of FILE 117.

⛔ a stale preamble ≠ a ruling · ⛔ a quotation ≠ the document · ⛔ a concurring
reading ≠ the basis
