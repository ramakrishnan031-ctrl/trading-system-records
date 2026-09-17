---
name: c6-auth-collapse-25jul
description: "C6 DONE 25-Jul — the receiver's three-way auth decision collapsed into ONE _authenticate() called by /health and /webhook. Byte-identical; the four divergences preserved (above all the EOD early return). RED-first by planting. Unblocks F2."
metadata: 
  node_type: memory
  type: project
  originSessionId: 94025df9-7b5d-4673-aa44-14ccbe9d87b3
  modified: 2026-07-25T03:29:19.960Z
---

**C6 — receiver auth collapsed to one call site. BUILT + DEPLOYED 25-Jul (off-market, service down, book flat; NO restart — loads Mon 08:15).**

**What it actually was.** Not "introduce shared auth" — the auth STATE was already shared (`_secret`, `_require_hmac`, `_ip_limiter` are instance attributes both routes read). What was duplicated was the CHECK: the same three-way decision (HMAC → require_hmac → token) spelled twice in two idioms. `/webhook` returned early per branch; `/health` accumulated an `ok` boolean and issued one 401. `/health:300-311`'s `elif receiver._require_hmac: ok = False` existed ONLY to reproduce in boolean form what `/webhook:482-489` did with an early return. The two had already been patched separately (G.1 on `/webhook` 2026-04-25; the `/health` parity fix later) — that is the hazard removed.

**The build.** New `WebhookReceiver._authenticate(hmac_payload) -> tuple[bool, str]` (mirrors `_cast_numeric_fields`, the idiom already in the file). `/health` calls `_authenticate(b"")`, `_process_request` calls `_authenticate(raw_body)`. Behaviour byte-identical across all 7 branches on both routes.

**⛔ The four divergences PRESERVED (a naive flattening destroys these):**
1. **HMAC payload is per-route** — `b""` on GET `/health`, `raw_body` on POST `/webhook`; passed as an argument, never assumed. (Consequence documented in situ: a valid `/health` signature is a CONSTANT for a given secret and indefinitely replayable.)
2. **`/health`'s uniform 401 message** — the granular reason is returned by the helper and DELIBERATELY DISCARDED at the `/health` call site. Naming it would tell an anonymous caller on `0.0.0.0:5000` whether `require_hmac` is on.
3. **⭐ The EOD early return is UNTOUCHED** — `/webhook/<eod scanner>` still returns BEFORE the kill-switch and entry-window gates. **That early return is what makes the 17:00 PB-01 capture possible.** Auth still runs before it.
4. **Audit trail** — `/webhook` still writes a `webhook_audit` row on every outcome including 401; `/health` still writes none.

Gate order unchanged on both routes: shutting-down → per-IP limiter → **auth** → unknown-scanner 404 → EOD dispatch → kill → backpressure → entry window.

**⭐ RED-first for a refactor that CANNOT be red on HEAD.** A behaviour-preserving collapse changes no outcome, so the proof is by **planting**: 5 flattenings planted one at a time, each made its guard test RED, source restored md5-identical each time (`8c269f55…`). P1 helper ignores `hmac_payload` · P2 `/health` returns the granular reason · **P3 EOD return moved below the kill gate** · P4 `/health` writes an audit row · P5 auth re-inlined into `/webhook`. **The tests are not vacuous.** Script `scratchpad/red_proof.py`; method recorded because it generalises to any pure refactor.

**Tests** `tests/unit/test_c6_auth_collapse.py` — 21 pass. `TestC6BranchMatrix` (9, both routes × every branch) · `TestC6DivergencesPreserved` (8) · `TestC6Structure` (3: `compare_digest` appears ONLY inside `_authenticate`; both routes call the helper; **no paper/live branch ⇒ parity by construction**).

**⭐ `TestS4SeamUnchangedByP1` still green** — it asserts the unauthenticated `/health` answers exactly `{"error": "authentication required"}` / 401 under BOTH `require_hmac` settings and feeds that real 401 to the real `check_webhook_endpoint`. S4 cost a whole trading day on 17-Jul via exactly this surface. **This refactor did not re-create S4.**

**Unblocks F2** (Rama's Option 2 — an authenticated in-process operator trigger into the existing `KillSwitch`): its auth is now one named function with a stated contract instead of two idioms a new surface would have to choose between. ⛔ The F2 design and the trigger-surface investigation are still NOT started.

⚠️ Unchanged and still true: **the Monday PB-01 risk is boot wiring, not auth** — grep the 08:15 boot log for `"V3 Step 10b PB-01 watchlist: ENABLED"`. See [[receiver-auth-c6-scoping-25jul]].

Report `docs/audit/c6_auth_collapse_25jul2026.md`.
