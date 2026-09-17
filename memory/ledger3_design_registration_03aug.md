---
name: ledger3-design-registration-03aug
description: "Ledger #3's six design decisions are REGISTERED (docs-only, nothing authorised) — including the binding constraint that any future CHECK6 redesign must name #2b and #2c-R."
metadata: 
  node_type: memory
  type: project
  originSessionId: f7ce096e-aab9-422b-87b9-555725c0c72e
  modified: 2026-08-03T04:01:38.379Z
---

**LEDGER #3 DESIGN REGISTERED 03-Aug-2026 — `docs/audit/ledger3_design_registration_03aug2026.md`.
⛔ REGISTRATION ONLY: no code, no design started, nothing authorised. #3 stays fully GATED.**
Written so implementation later starts from the register, not a chat transcript
(`campaign_practices.md` §0 triggers 1 · 3 · 4).

⭐ **PROVENANCE — do not collapse two different things.** These are **red-team DESIGN
acceptances from ChatGPT, which IS its remit** (architecture review). ⛔ **They are NOT §G2
material** — G2 governs *Rama's* decisions (deploy slots, gates, ride-or-hold), which is what
R1–R5 were. Filing these under G2 would wrongly discount sound review; treating R1–R5 as
advisory would wrongly promote advice into authority.

⛔⛔ **THE ONE THAT BINDS FUTURE WORK (R-3): A CHECK6 REDESIGN MUST NAME #2b AND #2c-R.**
CHECK6's 3-cycle FIX-B is the ONLY thing bounding **#2b**'s CNC spare (`6495baa`) and
**#2c-R**'s CO refusal (`42db913`) to ~3 CRITICALs instead of an unbounded stream — and
⭐ **NEITHER ITEM'S CODE MENTIONS CHECK6**; the bound is emergent from cycle ordering
(CHECK6 runs *after* CHECK2), so a CHECK6 author gets **no local signal** that two shipped
items depend on the counter being retuned. ⇒ any redesign must state, **for each by name**,
whether **alert count · escalation behaviour · refusal semantics** change. Recorded at
THREE sites for that reason: the design record §5 · register §B.1 row 3 ·
`reconciler_product_filter_build_02aug2026.md` §R4.

⭐ **ENDPOINT FRAMING:** IA-P5-02's cancel-race and the CHECK6 route are **two INDEPENDENT
paths to ONE endpoint** (the system's own position filed `HUMAN_ORDER`) ⇒ ⛔ **fixing either
alone leaves it reachable by the other**; a design treating them as two bugs is wrong by
construction. ⭐ **DIRECTION TO TEST AT STEP 1, ⛔ NOT a settled mechanism:** separate
*release the reservation* from *disown the position* — today ONE action, and **whether they
are separable here is a measurement nobody has made.**

**SPLIT:** #3a `orders.qty_filled` ships ALONE · #3b the `HUMAN_ORDER` endpoint covers BOTH
paths. ⛔ Don't bundle 3a into 3b (they share a row, not a fix); ⛔ don't split the paths
inside 3b. ⚠️ **the audit's "~2 lines" is an ESTIMATE, not a measurement.** ⭐ Width:
**405 of 805** rows wrongly zeroed (`qty_filled>0` **0/405**, `filled_at` **405/405**); the
other 400 are CANCELLED and correctly zero. **R-4: FIX-FORWARD by default** — backfill only
on evidence those rows are consumed by production logic, and then as a **separate approved
activity** (⛔ a wrong backfill is indistinguishable from correct data afterwards).

**QUEUE ORDER UNCHANGED: #8b Step 2 → #2d → #3** — asked and answered. ⚠️ **Measured while
registering: that order had never been written down ANYWHERE** (repo-wide `*.md`+`*.txt`),
and **`#2d` still has NO register row** (it lives only in practices §G3/`:290-293`,
`PATHS.md:112`, and §R7 of the reconciler record). Stated, not fixed — a row would move 231.

⛔ **mempalace SKIPPED deliberately this batch**, not forgotten: it is [[unpushed-pending-deploy-ledger]]'s
R13 item awaiting Rama's retire-or-maintain ruling, and writing into it would deepen the very
problem R13 registers.

Related: [[feedback-live-vs-latent-findings]] · [[feedback-status-label-rule-27jul]] ·
[[unpushed-pending-deploy-ledger]]
