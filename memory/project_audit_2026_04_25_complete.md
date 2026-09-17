---
name: 2026-04-25 supplemental audit complete (3 batches, commits 89ed020/95f2f47/53e61e2)
description: 17 items fixed (B.1 C.1 D.1 E.5 E.1 E.2 G.1 G.3 A.1 B.3 G.2 D.3 A.2 A.4 I.3 I.4 I.5); F.1+I.1 closed-as-equiv; 1753 green; pushed to vm; 13 items deferred
type: project
originSessionId: 7ee1cc3d-28fa-4bf8-b5d6-a01c36096d55
---
**Source:** `docs/web_claude/03_audit_responses/deep_system_audit_2026-04-25.md` (supplemental, 35 issues across categories A-I)

**Head:** `53e61e2` on `main`, pushed to both `origin` and `vm` remotes (2026-04-26).

**Tests:** 1753 collected (`pytest --co -q`). +40 vs Phase B baseline 1713.

**Why:** This audit was supplemental on top of the 2026-04-24 audit (Phase A/B already shipped at 9b7bcda/13b3d09). The supplement found 4 new CRITICAL items the prior audit missed; user direction was 3-batch sequential ship before paper Week 2 (28-Apr) without any push between batches.

**How to apply:** When the user references "the 25-Apr supplemental audit", "the 4 critical fixes", "Batch 1/2/3", "the rehydrate fill_map fix", "the hard_kill deadlock", or any of the item labels (B.1, C.1, etc), point at this entry + the audit doc.

**Items shipped per batch:**

- Batch 1 (`89ed020`) — Critical: B.1 OrderPlacer.rehydrate_fill_map for SL/TGT/EOD legs after restart; C.1 hard_kill outside capital lock (deadlock fix); D.1 SmartTgtManager rate_limiter on modify_order; E.5 EOD broker-position filter on every fire (not just recovery). +13 tests.
- Batch 2 (`95f2f47`) — Pre-live: E.1 reject sl_pct<=0 in FIXED_PCT branch; E.2 close_trade gross_pnl 10x sanity bound; G.1 require_hmac=True disables token fallback; G.3 SmtpConfig.password_env + resolved_password(); A.1 closed-as-equivalent (Phase B already shipped waitress; gunicorn is UNIX-only). +15 tests.
- Batch 3 (`53e61e2`) — Week-1 hygiene: B.3 get_open_intraday_positions adds qty_filled>0; G.2 LiveFeedManager logs api_key_set bool not prefix; D.3 get_server_time uses quote bucket not margins; A.2 alert_watcher concurrent.futures.wait with _SMTP_TASK_TIMEOUT_SEC=30; A.4 preflight retry on transient (RequestException + 5xx, not 4xx); I.3 RSI bounds [0,100]; I.4 main.py validates broker=='zerodha' (case-insensitive, exit 9); I.5 DEPLOYMENT.md .env step. F.1 closed-by-equiv (idx_trades_status already exists schema.sql:131). I.1 closed-as-N/A (real NSE security master CSV has no exchange column). +12 tests.

**Deferred (not in this work):**
- Next cycle (medium effort): C.2 OrderPlacer fill_map_lock during broker calls; C.3 LiveFeedManager thread pool for tick callbacks; D.4 webhook per-IP rate limit; F.2 SecondaryScreener batch quote_fn; F.3 pass current_time to step_executor; B.2 ShadowTracker bid/ask=0 fallback; I.2 CandleStore docstring.
- Doc/cosmetic only: H.1 deploy/systemd files (already exist); H.2 mempalace.txt (closed by mempalace.yaml update at 53e61e2); A.3 daily_review --scp-target; A.5 alert_watcher config error path.
- Audit explicitly deferred to v2.1: E.3 strategy-time gating; B.4 CandleStore volume from kite historical.

**Schema:** No bumps. v12 (gate_state from Phase B) remains current.

**Pending non-audit workstreams (unchanged by this audit):**
- Phase C of 2026-04-24 audit still pending: WAL cron (4.2), 5-min dedup bucket (6.3), smart-target intra-minute (5.3). Gate = paper Week 2 outcome.

**Next session:** Paper Week 2 Day 1 (Mon 28-Apr) — Chaos Diet: kill-switch, late token, restart scenarios. systemd still disabled; execution stays on PC+ngrok until Week 3.

**Live D-Day:** Mon 11-May-2026 (₹25k Day-1 capital).
