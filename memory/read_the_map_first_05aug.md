---
name: read-the-map-first-05aug
description: "SYSTEM_MAP.md is step zero of every session, before any measurement — the campaign re-derived facts the system had already written down, twice in four days."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T07:20:31.730Z
---

⛔⛔ **READ `docs/SYSTEM_MAP.md` IN FULL AT THE START OF EVERY SESSION — BEFORE ANY MEASUREMENT.**
Step zero. ⛔ Not *"if it seems relevant"*. Registered as **`campaign_practices.md` §M8**.

**Why:** written as an **ORDER OF OPERATIONS, not a virtue** — *"be more careful"* cannot be checked;
*"did you read the map before your first measurement?"* is answerable yes or no.

**Earned twice in four days, same shape both times — the system had already recorded the answer
while the campaign was deriving it by hand:**
- **04–05-Aug:** `trade_type` was *"the flag nobody listed"*, found by measuring `control.py`'s two
  layers — while **`delivery_lock.status` (`main.py:2838-2846`) published the whole conjunct verbatim
  at every boot.**
- **05-Aug:** two operator-card revisions were spent tuning a `grep` anchor against `journalctl`
  before measuring that the census is `INFO` and stdout is `WARNING`+ ⇒ **never in journald at all.**
  **SYSTEM_MAP had carried that since 25-Jul** — ⭐⭐ **and the SAME entry carried the rule that would
  have prevented both revisions:** *"an operator instruction that says 'grep X' must be VERIFIED
  against a real log before it ships — a check that silently finds nothing is WORSE than no check,
  because 'no output' reads as 'it failed'."* **The map held the fact AND the generalised lesson,
  unread.**

⭐ **THE ASYMMETRY:** reading the record is **cheaper** (one file, once) **and more authoritative**
(written by whoever measured it, at the time, with the incident in view) than re-deriving from
source — **and a re-derivation can be wrong, which then ships as a command.**

⚠️ **BOUNDED — ⛔ this is NOT "trust the map blindly".** [[feedback-verify-the-finding-premise]] and
§M3 still govern, and **map entries go STALE**: the same session found its *Delivery (Slice 2.5)*
section still reading *"DORMANT / never exercised, flags OFF"* **on the day delivery traded** — the
exact hazard debt-ledger #12 names (*a cited document that is WRONG is worse than one that is
absent*). ⇒ **Read first, then verify what you are about to rely on. Reading first changes WHAT you
verify, not WHETHER you verify.**

✅ **CLOSED 05-Aug ~12:4x (`3548cac`) — the map's *Delivery (Slice 2.5)* section and its INDEX line
read *"DORMANT / never exercised"* ON THE DAY DELIVERY TRADED, and are now corrected.**
⭐⭐ **M8 IS PRECISELY WHY IT COULD NOT WAIT: a rule that MANDATES reading a document RAISES THE COST
OF THAT DOCUMENT BEING WRONG.** Before M8 a stale entry was a trap someone *might* walk into; after
M8 it is a trap **every future session walks into first, by rule** ⇒ shipping M8 while leaving it
stale would have armed the exact failure M8 exists to prevent, **with the campaign's own authority
behind it.**
Label = **`<DEPLOYED — ENTRY PATH VERIFIED LIVE 05-Aug; EXIT PATH UNVERIFIED>`** — ⛔ never "live"
(a fill proves the ENTRY path; trigger/T+1/carry are unproven). ⛔ **No position count or rupee value
was copied in from conversation** — still unmeasured by this bridge.
⛔ **Scope, stated so the sweep is falsifiable: CURRENT-STATE claims only** (`:36` + the section).
**~14 further hits in the Changelog and dated banners were LEFT ALONE — they were true when written,
and rewriting dated history destroys the record.**

⚖️ **AND THE TWO STRIKETHROUGH RULES NOW BOTH EXIST — the map edit states which is which, so the next
session does not apply the wrong one:** **§G4 struck-but-legible governs REGISTER-CLASS documents
(nobody EXECUTES them, so history is safe)**; ⛔ **an operator CHECKLIST is revised CLEANLY, because a
struck-out command is a command someone might still run.**

Related: [[feedback-system-map-first]], [[census-not-in-journalctl-05aug]], [[feedback-absence-needs-wide-check]].
