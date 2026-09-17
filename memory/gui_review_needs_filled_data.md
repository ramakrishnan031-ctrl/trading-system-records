---
name: gui_review_needs_filled_data
description: Every GUI screen shown to Rama for visual approval must be FILLED with data (VM snapshot or demo) — never an empty/dashed screen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 31334cdb-96e4-4a09-bdf4-def39d5ad8ab
  modified: 2026-08-30T11:50:52.488Z
---

👤 **RAMA, 30-Aug-2026:** *"Please always show me every screen using vm db's input
data or your own demo data for clean review."*

⭐ **EVERY screen presented for visual approval must be FILLED.** Use the read-only
VM DB snapshot, or ⭐ generate demo data — either is fine, Rama said so explicitly.
⛔ Never present a screen of dashes, zeroes and NOT AVAILABLE and ask him to judge it.

**Why:** an empty screen ⛔ cannot be reviewed. Density, column alignment, text
overflow, chart axes, badge contrast and "does this panel read correctly" are all
invisible until real values are in the cells. 🔬 S11 proved it twice — the real-VM
snapshot was too sparse (202 of 307 rows never filled) and had to be re-rendered on
demo data before the composition could be judged at all.

⚠️ **THIS OVERRIDES A REVIEWER CARD THAT SAYS OTHERWISE.** The Web-Claude S12 ruling
said *"Do NOT build a demo payload simply because the Windows machine cannot provide
Linux/systemd health data."* 👤 Rama's own instruction supersedes it — ⛔ a card is
never Rama (`WC-PATTERN #7`/`#8`, and see [[MEMORY_HAZARDS]]).

**How to apply:**
- 🔬 Some screens are ⛔ NOT DB-fed. S12 System Health reads **live OS state** —
  systemd, `/proc`, uptime, broker token. On Windows a DB pointer fills NOTHING
  there. ⇒ fill those with an **out-of-repo review harness** that patches the
  reader layer in-process, ⛔ never by editing the app.
- ⛔ **THE DEMO ARTEFACT LIVES OUTSIDE THE REPO.** No demo DB, no fake-host module
  and no pointer may be committed. Revert any pointer **byte-identically** and
  prove it (md5 + 0 pointer lines), and 🔬 prove the real DB's mtime is unchanged.
- 🏷️ **LABEL THE APPROVAL:** a screen approved on demo data is 🟢 VISUALLY APPROVED,
  ⛔ **NOT** `VERIFIED LIVE` — see [[feedback_status_label_rule_27jul]]. Say in the
  ledger entry which data it was approved on.
- ⭐ Serve the filled review on a SECOND port and leave the honest one up, so the
  real unavailable-data states stay inspectable side by side.
