---
name: part-c-rr-standardized-1.5-24jun
description: Part C — ALL 15 strategy YAMLs set to tgt_risk_reward 1.5 (was gap_fade 1.5 unchanged, gap_go 2.5→1.5, other 11 2.0→1.5); config-only, no schema; Slice-1 mechanism carries it to the broker; takes effect next restart
metadata:
  node_type: memory
  type: project
  originSessionId: 70f5d745-f68b-453a-9155-61b7b08308ff
---

**Part C done 24-Jun (branch `part-c-rr-1.5-all-strategies-24jun`). Rama's standardization — config value change only, NO schema, NO code (the R:R MECHANISM was fixed + proven in Slice 1, 22-Jun).**

**Change:** ALL 15 `config/strategies/*.yaml` now `tgt_risk_reward: 1.5`. Before: `gap_fade_long`/`gap_fade_short` = 1.5 (unchanged), `gap_go_long`/`gap_go_short` = 2.5→1.5, the other 11 = 2.0→1.5. So **13 files changed**, 1 line each (only `tgt_risk_reward`; `tgt_method` stayed `"RISK_REWARD"` in all 15 — the 1.5 only bites because the method is RISK_REWARD). Surgical `sed` on the `2.0`/`2.5` lines; git diff = exactly 13 value lines, nothing else.

**Verification:** `grep` → all 15 read 1.5; `StrategyLoader.load_all_strategies` → 15 load CLEANLY (pydantic validator `tgt_risk_reward > 0` passes), each parsed object `tgt_risk_reward=1.5` + `tgt_method=RISK_REWARD`; 176 real-config-loading unit tests green (no test hardcodes the old per-strategy RR from real config — all `2.0`/`2.5` test refs are self-contained mock fixtures / hardcoded math). No full-suite needed (config-only).

**Wiring to broker (Slice 1, proven Tue 23-Jun — no code change here):** `tgt_risk_reward` is frozen at placement into `trades.tgt_risk_reward_applied` and the fill-time recalc re-reads it → the next trade after restart stores 1.5 and the broker TGT is placed at 1.5×risk. NULL → 2.0 fallback + WARN (won't fire now — all 15 set).

**Activation:** the running app holds the old YAMLs in memory until its restart; takes effect on the **next trading-system restart** (tomorrow's 08:15 token-refresh cycle / morning start). Deployed to the VM working tree now (git push → post-receive checkout).

**To retune any strategy's R:R later:** edit `tgt_risk_reward` in its YAML → commit → push → restart. It now correctly reaches the broker (Slice 1). **Standardized baseline = 1.5 across all strategies.** Docs: `docs/CONFIG_GUIDE.md` Section 11 updated; the `.docx` manual needs a manual re-SCP (gitignored, out-of-band — flagged to Rama).

**Live proof (tomorrow):** every strategy's `tgt_risk_reward_applied` = 1.5 and `tgt_initial` == broker resting TGT (all at 1.5×risk). Especially a `gap_go` trade → TGT now at 1.5 (was 2.5) = the visible proof.

Related: [[slice1_rr_fix_deployed_22jun]] (the mechanism) · NEXT = Slice 2 (strategy control system + status table: 3-layer trade_type/intent/enabled + status table; Phase-1 grounding done).
