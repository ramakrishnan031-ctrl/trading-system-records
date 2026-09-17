---
name: Capital invariant drift bug FIXED (commit_to_used excess clipping)
description: max(0,excess) in commit_to_used caused positive drift when fill>reserve price; fixed by allowing negative excess; tolerance 100→1.0
type: project
originSessionId: 18b624c2-2e63-49a9-afbb-03408edc89cc
---
## Bug FIXED 2026-05-06 (commit 1f77f3d)

**Symptom (06-May):** HARD_KILL at 09:34:55, delta=Rs 156.29 after 13 fills. Same pattern 05-May (no trading entire day).

**Root cause:** `commit_to_used` used `max(0.0, res.margin - actual_margin)` for excess. When fill price > reserved price (common in paper LTP fills), the negative excess was clipped to 0, but `used` got the full actual_margin. Net: `used` grew without `available` shrinking → invariant sum drifted positive.

**Fix applied:**
1. Removed `max(0.0, ...)` — excess can now be negative (deficit deducted from available)
2. Changed `if excess > 0` to `if excess != 0.0` in `_apply_commit`
3. Tolerance reduced from 100.0 back to 1.0

**UNIFIED fix:** affects both paper and live modes — fill price can differ from limit price in either mode.

**Tests added:** 2 new tests (76 total in test_fund_manager.py): single higher-fill test + 15-fill drift accumulation test.
