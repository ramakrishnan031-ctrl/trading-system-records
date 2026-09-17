---
name: feedback-verify-scheduling-facts-31jul
description: A holiday/trading-day/weekday claim must be checked against the file text or the NSE circular BEFORE it drives scheduling — one was asserted from memory on 31-Jul and nearly moved an irreversible step.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c02564a9-2e09-492b-b830-0b35d1e9e449
  modified: 2026-07-31T17:26:21.875Z
---

⛔⛔ **NEVER ASSERT A CALENDAR FACT FROM RECOLLECTION. QUOTE THE LINE, OR DO NOT
MAKE THE CLAIM.** Any **holiday / trading-day / weekday** claim that affects
SCHEDULING must be verified against the **file text** (`config/nse_holidays_<yr>.yaml`,
resolved at `config_loader.py:2166`; every consumer routes through
`utils/holiday_guard.py`) — and ideally the **NSE circular** — *before* it drives a
decision. ⭐ Best single check: run the system's own
`is_trading_day(date, Path('config'))`, which answers in one line.

**Why:** on **31-Jul-2026 ~22:0x** it was claimed that Mon **3-Aug-2026 was an NSE
holiday** ("Sunday / Independence-Day weekend"), and on that basis the
observe-Mon → flip-Tue sequence was proposed to be re-gated — i.e. **a false fact
was about to move an IRREVERSIBLE step.** It was wrong twice over: 3-Aug-2026 is a
**MONDAY**, and Independence Day is **15-Aug**, a **Saturday**. Rama caught it only
by pulling circular **NSE/CMTR/71775 (12-Dec-2025)** himself. ✅ It never reached an
artifact — the calendar, card and memory index were correct throughout.

⭐⭐ **ROOT CAUSE — A COMMENT IN A DATA FILE WAS READ AS DATA.** The yaml has **no
August entry at all** (`2026-06-26` → `2026-09-14`); its only "Aug" string is the
weekend comment `#   15-Aug-2026 (Sat) Independence Day`. ⛔ **The `holidays:` list is
the data; everything above it is prose.** ⇒ **MISREAD, NOT a data defect** — and the
two have OPPOSITE fixes (a wrong file is a gated boot-path config change; a misread
is nothing to edit), so **naming which one it is comes before proposing any fix.**
The file reconciles to the circular **15/15 + 4/4, EXACT**.

**How to apply:** state the filename and quote the line in the SAME sentence as the
date claim. ⛔ A weekday is a one-line check — there is no version of this that is
cheaper to assume than to verify. ⭐ And when a date claim would move a dated,
irreversible step, the burden goes UP, not down: verify first, propose second.

Related: [[feedback-verify-the-finding-premise]] · [[feedback-absence-needs-wide-check]] ·
[[clock-dependency-class-26jul]] · [[mon-03aug-observation-gate]] ·
[[feedback-status-label-rule-27jul]]
