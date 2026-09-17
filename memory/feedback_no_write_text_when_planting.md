---
name: feedback-no-write-text-when-planting
description: "On Windows, Path.write_text rewrites EVERY newline to CRLF — never use it to plant/restore a source file, or the md5 restore-check fails and the diff becomes whole-file; use read_bytes/write_bytes or the Edit tool."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8999ae0b-3d00-4770-8853-d467ee57f31a
  modified: 2026-07-26T14:50:18.109Z
---

⚠️⚠️ **THE GENERAL RULE, PROMOTED 26-Jul TO THE STANDING RULES
(`docs/foundation_engineering_rules.md` §5.1 "Verification Discipline"):**

> ⛔ **A CLEAN `git diff` IS NOT PROOF THAT NOTHING CHANGED.** Git normalises line endings on
> the way in, so a whole-file newline rewrite is **invisible** to it. **Verify a restore by
> `md5` AND byte count** — those are the only two checks that see it.

⭐ **This project infers "unchanged" from a clean diff constantly. That inference is unsound.**
Say which check you actually ran: "`git diff` is clean" and "md5 matches" are different claims
with different strengths — never report the weaker one as the stronger.
✅ Applied the same evening: the 26-Jul register refresh was **appended**, then proven
append-only by md5 of the original 75,697-byte region + an exact byte delta.

⛔⛔ **AND THE SECOND WAY A RESTORE DESTROYS WORK — HIT 26-Jul, CAUGHT BY THE MD5:**

> **`git checkout -- <file>` IS NOT A PLANT-RESTORE WHEN THE FILE HAS UNCOMMITTED WORK.**
> It restores to **HEAD**, so it silently discards the *whole* uncommitted change, not
> just the plant.

Planted a one-line defect into `broker/zerodha_adapter.py` to prove a behavioural RED, then
ran `git checkout --` to undo the plant. The file's ~5 KB of **uncommitted §B implementation
went with it**: md5 `721B7E74…` / **104,751 B** against a pre-plant `124ED3FA…` / **109,738 B**.
⭐ **The md5+bytes check is the only reason this was noticed at all** — the tests would have
gone green again (they test the old behaviour), and `git diff` looked like a clean revert.

**How to apply:**
- **COMMIT the work FIRST, then plant, then `git checkout --`** — that makes HEAD the thing
  you actually want back. This is the safe order and it is cheap.
- Or **un-plant with the reverse targeted Edit** (never a whole-file restore).
- ⭐ **Always capture md5 + byte count BEFORE the plant and compare AFTER**, and treat a
  SHORTER file as work destroyed, not as a stale hash. Recovery here was only possible
  because the implementation was still in context.

**⛔ NEVER use `Path.write_text()` (or plain `open(..., "w")`) to plant a defect into — or restore
— a source file on this PC. It translates every `\n` to `\r\n`.**

**Why:** this repo proves guards non-vacuous by **PLANTING** a defect, running the suite, then
restoring and checking the file is **md5-identical**. That workflow depends on the restore being
byte-exact. On 26-Jul-2026 I planted into `orders/closure_classifier.py` with a one-off script
using `p.write_text(s2, encoding="utf-8")`. Python text mode uses `newline=None` ⇒ universal-newline
translation ⇒ **all 162 lines became CRLF**. After restoring the exact original text the md5 was
`3879c6f2…` against a pre-plant `0087a05b…` — a mismatch that had nothing to do with the plant.

⭐ **The failure mode is worse than the inconvenience:** the md5 check is the evidence that the
plant left no residue. A restore that fails that check for an unrelated reason either (a) gets
waved through as "just line endings", which is exactly how a real residue would also be waved
through, or (b) burns the time I spent chasing it. And `git diff --stat` **hid it** — git
normalises via `core.autocrlf`, so the diff still read a clean `22 insertions(+), 5 deletions(-)`
while the working file was 100% CRLF. Only the md5 and a byte count exposed it.

**How to apply:**
1. Plant and restore with the **Edit tool**, or with **`read_bytes()` / `write_bytes()`** — bytes
   mode does no newline translation.
2. If a restore's md5 does not match, **check line endings before assuming the plant is still in**:
   `python -c "d=open(F,'rb').read(); print('CRLF:',d.count(b'\r\n'),'LF:',d.count(b'\n'))"`.
3. Repair with `d.replace(b'\r\n', b'\n')` + `write_bytes` — then re-check the md5, which should
   return to the pre-plant value exactly (it did: `0087a05b…`).
4. ⭐ **Audit every changed file for CRLF before committing**, not just the one you planted into.

Related: [[feedback-verify-rc-not-output]] (a green check is evidence only if it could have been
red — an md5 check you explain away is no longer a check) · [[check1-deferral-bound-26jul]]
