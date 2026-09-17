---
name: aftercheck-circuit-cap-fix-24jun
description: Slice-1 SL/TGT after-check false-flagged PACEDIGITK (circuit-clamped TGT read as mismatch); made the after-check clamp-aware (excuse only when placed==band ceiling); no schema; SL+TGT, paper+live; 24-Jun
metadata:
  node_type: memory
  type: project
  originSessionId: 70f5d745-f68b-453a-9155-61b7b08308ff
---

**Issue 2 (branch `aftercheck-circuit-cap-fix-24jun`). Permanent root-cause fix; no schema; alert/observability path only — activates next restart.**

**Symptom:** Slice-1's SL/TGT after-check (`order_placer._verify_exits_placed`) flagged PACEDIGITK (Tue 23-Jun) `exits_verified=0`, detail "TGT 216.15 != intended 220.41". It was the **only `exits_verified=0` trade in the whole DB** — i.e. every after-check-era clamp so far false-flagged (1-for-1).

**Mechanism (grounded):** the intended TGT (220.41, fill-recalc) was above PACEDIGITK's upper circuit, so `place_exits` → `clamp_exit_into_band` legitimately CLAMPED the placed TGT down to the band ceiling 216.15 (`limit_triple.exit_price_clamped_to_band`) and placed it there. The after-check read `placed_tgt` (216.15, clamped) from the order row and compared it to `intended_tgt` (220.41, pre-clamp) → "mismatch" → false WARN. Slice-1's `_exit_price_mismatch` was even DESIGNED to catch clamps (its tolerance comment said so) — that's the design that needed to change. (NOT a retry-net issue: `needs_tgt_retry=0`; the TGT WAS placed. Issue 3 = the separate dead-retry-daemon.)

**SL is clampable too:** `clamp_exit_into_band(leg="SL")` can clamp a LONG's SL UP off the lower circuit (a tighter, still-placeable stop, `placeable=True`) — so the SL leg could also false-flag (as CRITICAL). The fix covers SL + TGT symmetrically.

**Fix (no schema — threaded the in-memory clamp result):**
- The clamp's band ceiling was ALREADY in memory: `ExitLegsResult.tgt_price` / `.sl_trigger_price` hold the clamped (placed) price. Added two booleans `sl_clamped` / `tgt_clamped` to `ExitLegsResult` (defaults False), populated in `LimitTripleProtocol.place_exits` from `sl_res.was_clamped` / `tgt_res.was_clamped`. **No DB field, no migration, no DB-copy gate.**
- `_verify_exits_placed` gained `sl_clamp_price` / `tgt_clamp_price` params (= the band ceiling a leg was clamped to, else None). New helper `_explained_by_clamp(placed, clamp_price)` = clamp recorded AND `placed ≈ clamp_price` (same tick tolerance). When a price differs from intended:
  - explained by the band clamp → record a NOTE ("TGT/SL clamped to circuit band X (intended Y)"), `exits_verified=1`, NO alert.
  - NOT explained (placed ≠ band, or no clamp) → real mismatch → `exits_verified=0` + CRITICAL(SL)/WARN(TGT), unchanged.
- **Discriminator is NOT blind suppression:** the band reference is the clamp's computed output (independent of the read-back order row), so a placed price matching NEITHER intended NOR band still flags (test `test_clamp_flag_set_but_placed_not_band_still_flags`). Qty checks unchanged. Parity: shared path, no mode branch → paper + live identical.
- Call sites: both LIMIT_TRIPLE after-checks (`_place_limit_triple_exits` + the TGT-retry path) pass the per-leg clamp ceiling from `legs`; CO path unchanged (CO-TGT is a documented never-clamp exception; CO-SL is broker-managed). **Also fixed a latent bug:** the retry-path call site passed `legs=legs` to `_verify_exits_placed`, which has no `legs` param — a TypeError masked only because that retry path was itself dead until 23-Jun (Issue 3).

**Re-classification (Part 3):** PACEDIGITK-shaped fixture (SL ok, TGT 216.15 clamped, intended 220.41, band 216.15) now flips `0→1` with detail "TGT clamped to circuit band 216.15 (intended 220.41)" and no alert. The historical PACEDIGITK row is left as-is (documents pre-fix behaviour); the live proof is the next clamped trade.

**Forensics:** clamp events are rare — 0/0/1/1/0 over 18–24 Jun (geometric: entry within ~2% of a circuit). PACEDIGITK is the sole after-check-era instance to date.

**Tests:** +8 in `test_slice1_rr_aftercheck.py` (clamp-valid TGT + SL → verified=1/no alert; discriminator placed≠band → still flag; real mismatch w/o clamp → WARN unchanged; missing SL + TGT-clamp → still CRITICAL; PACEDIGITK 0→1; paper/live parity; end-to-end via a circuit-capable adapter proving place_exits clamp → ExitLegsResult flag → after-check OK). 24/24 file green.

Related: [[slice1_rr_fix_deployed_22jun]] · [[tgt_retry_crashloop_postmortem_24jun]] · circuit-band placeability gate (NOCIL, `clamp_exit_into_band`/`ClampResult`)
