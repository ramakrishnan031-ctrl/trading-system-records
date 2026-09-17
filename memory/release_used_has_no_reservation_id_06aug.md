---
name: release-used-has-no-reservation-id-06aug
description: "RELEASE_USED carries reservation_id on 0 of 220 rows -- a reservation-keyed release query is a structurally guaranteed zero, and it arms a spurious kill before Phase E"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1be512bf-9d53-473e-960c-c17572bc2911
  modified: 2026-08-06T06:52:51.887Z
---

⛔ **THE KEYS ARE PERFECTLY DISJOINT.** Measured 06-Aug across the whole `fm_ledger`:

| entry_type | rows | with `reservation_id` | with `trade_id` |
|---|---|---|---|
| `RESERVE` | 1422 | **1422** | 0 |
| `RELEASE` | 1189 | **1189** | 0 |
| **`RELEASE_USED`** | **220** | **0** | 61 |

⇒ 🔴 **A `WHERE reservation_id=…` query for a release returns a STRUCTURALLY GUARANTEED ZERO** — and `RELEASE_USED` is what a **clean delivery exit** writes. ⛔ **An operator reads that empty result as "capital never released."**

⚠️⚠️ **THE MORNING CARD'S OWN RULE IS BACKWARDS HERE.** *"Key the capital query on `reservation_id`, NOT `trade_id`"* holds for `RESERVE`/`RELEASE` and is **exactly inverted for `RELEASE_USED`** (`reservation_id` always absent, `trade_id` sometimes present). ⭐ **It did not merely fail to catch a blind query — it instructed one.**
✅ **What to use instead:** the ledger's **running balance** (`balance_before`/`balance_after`), which uses **no key at all** and reconciles to the paisa. Or match by **ts + bucket + amount**.

🔴🔴 **HARD ORDERING CONSTRAINT — `reservation_id` MUST land on `RELEASE_USED` BEFORE Phase E.**
**(P)** a fully-released reservation reports its **entire** margin still held (`689.41341`). **(S)** `_check7` publishes `source_module="fund_manager_self_check"` (`order_reconciler.py:3782`), which **IS** in `_ESCALATING_SOURCES` (`drift_handler.py:66-70`) ⇒ **DH1 does NOT bar it** ⇒ single-sample SOFT/HARD escalation. ⇒ **Phase E's orphan detection queries closed reservations ⇒ shipping it first arms a spurious kill on every closed delivery reservation.** Recorded in `docs/04_db_schema_reference.md` (there is **no Phase E work item** to attach it to).

⛔ **AR9 DOES NOT COVER THIS.** AR9's subject is **G3** (`source_module="order_reconciler"`, which DH1 **bars**). **Two checks · one file · one alarm name · two safety postures.** ⚠️ `drift_handler.py:17` still says the escalating set has **one** member; the frozenset four lines below has **three** — **the prose says barred, the code says escalates.**

⚠️ **The BL-3 test is VACUOUS:** `tests/unit/test_state_store.py:1944` inserts a `RELEASE_USED` row **carrying** a `reservation_id` — a shape production has never produced — and asserts the sum is 0. Fix the fixture **first**, re-run on OLD code; it must go RED. Also [[f6-delivery-exit-abs-defect-06aug]].
