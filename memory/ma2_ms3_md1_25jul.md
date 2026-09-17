---
name: ma2-ms3-md1-25jul
description: "25-Jul batch 2: M-A2 is REAL (order path, fires BEFORE placement); was HELD at the F2 import gate, then SHIPPED 25-Jul batch 3 (afefccb) on written authorisation. M-S3 INERT (66ms vs 5000ms over 287,600 samples) — fixed anyway. M-D1: PB-01 is CLEAN (historical delta volume); the live tick→candle path is DORMANT. M-K3: ZERO latent FK violations."
metadata: 
  node_type: memory
  type: project
  originSessionId: 21328cbe-b100-4397-9f09-6c0d94c58b60
  modified: 2026-07-25T14:04:55.254Z
---

**25-Jul batch 2 — PUSHED: M-S3 + E2 + docs. HELD: M-A2, E1.** ✅ **BOTH SHIPPED 25-Jul batch 3 (`afefccb` / `4a0c0b2`, deployed `cb4c256`) on written authorisation — the override covered these two items ONLY; the F2 gate is normal again. Branch `hold-ma2-send-deadline-25jul` deleted (empty diff vs main).** Off-market, book flat, service DOWN, NOT restarted (loads Mon 08:15). Reports `docs/audit/mk3_fk_enforcement_25jul2026.md` + `docs/audit/ma2_ms3_md1_25jul2026.md`.

## ✅ M-A2 — BUILT, TESTED, HELD AT THE F2 GATE, then **SHIPPED** `afefccb` (was branch `9625b7d`, now deleted)
**It is REAL and on the ORDER path** — `signals/signal_processor.py:1130` says so itself: *"Telegram alert: INTRADAY SIGNAL (fires before order placement)"*, on all three entry paths (`:1131` `_process_one` · `:1901` gate-release · `:2196` retest-resume), **with the capital reservation already held** ⇒ a slow endpoint delays every entry and staleness-defeats the FIX-067/M-S1 fresh re-anchor.

**⭐ The "no timeout" premise is HALF WRONG.** `requests.post` already gets `timeout=5.0`. What is **unbounded** is `_SlidingWindowRateLimiter.acquire()` (`while True` + `sleep(0.5)`, no deadline, called once **per attempt**). The bounded-but-long part on the shipped config is **26 s PER CHAT** = 4 attempts × 5 s + 3 backoffs × 2 s (`max_retries:3`, `retry_backoff:2.0`, one enabled channel — SECONDARY is `enabled:false`).

**⚠️ THE CRITICAL EMAIL FALLBACK IS INERT IN PRODUCTION.** `_send_email_fallback` needs `ALERT_EMAIL_USER` / `ALERT_EMAIL_PASSWORD` / `ALERT_EMAIL_TO`; the VM `.env` defines **NONE** of them (it has `ALERT_SMTP_PASSWORD` — that is the *alert_watcher's* variable, a different consumer). It returns at `:681-685` **before any socket op**, so the `smtplib(timeout=15)` ladder never runs. **The alert_watcher sentinel path IS the backup** — do not cite the email fallback as a delivery guarantee.

**FIX (built): one wall-clock deadline per `send()`**, computed once in `_send_to_all_chats` (shared across channels, so 3 channels ≠ 3 deadlines), covering the rate-limit wait + HTTP timeout + every backoff. **TIMEOUT, not async — async would reintroduce the M-O9 publish-then-read race.** Safe because CRITICAL writes its sentinel FIRST (TG5) and ERROR still writes `failed_alerts.log`. 13/13 RED on HEAD; 188/188 blast radius; fake clock injected as the module's `time` NAME (not the real module) so it cannot leak.

**⛔ WHY HELD — F2 gate FAILS:** `reports/daily_report.py → alerts/telegram_notifier.py`; `scripts/forward_shadow_record.py → utils/cron_heartbeat.py → alerts/cron_alerts.py → alerts/telegram_notifier.py`; `forward_shadow_record.py → core/config_loader.py`. Materially harmless (the report sends INFO *after* writing the file; the recorder uses `config_loader` only for `broker_limits`; 30 s > the 26 s ladder so it would not engage — ⚠️ **that 30 s is SUPERSEDED: tightened to 8 s on 25-Jul `488e7e3`, precisely BECAUSE sitting above the 26 s ladder meant it barely bound**) — **but overriding an explicit gate on my own materiality call is what the gate exists to prevent, the weekend before PB-01 goes live.** **Ship = `git cherry-pick 9625b7d`.** ✅ **DONE 25-Jul batch 3 — and holding it rather than self-overriding was confirmed the right call.**

## ✅ M-S3 — INERT, MEASURED. Fixed anyway (`8d753a0`), labelled INERT
**287,600 recorded step latencies** (`screener_results.latencies`, 33,171 rows, 12-Jun→24-Jul): p50 **0.102 ms**, p100 = **66.06 ms** vs a **5,000 ms** timeout (76× margin); **0 rows ≥1,000 ms**; **0 timeout signatures**. The ten step bodies are pure dict/float arithmetic — no I/O, no network, no lock, no DB; `now_ist()` is `datetime.now(tz)`. **The timeout has never fired.**

**But the code defect is worse than filed:** `future.result(timeout=)` abandons the **WAIT, not the WORK** (Python cannot interrupt a running function; `future.cancel()` is a no-op once started). With FIX-100's shared `max_workers=1` pool, **one hung step turns ALL TEN steps into TIMEOUT and poisons every LATER signal forever.** The RED run showed exactly that. Fixed by **rotating** the poisoned pool (`shutdown(wait=False)`, fresh pool; `run_all` snapshots the pool it submitted to; swap + `shutdown()` share one lock).
**⛔ NOT done, recorded:** `future.cancel()` (placebo here) · **deleting the pool entirely** — arguably correct (it cannot protect against pure-CPU steps, and would make `latencies_ms` true step time instead of queue wait) but it removes the TIMEOUT status ⇒ **Rama's design call.**

## 🟢 M-D1 — **PB-01 IS CLEAN**; no code shipped
**⭐ `confirm_volume_mult` reads HISTORICAL-API candles, NOT the tick candle** — `v3_chain/pb01_entry.py:221/245/289` ← `self._fetcher.fetch_interval` ← `sr_detector/fetch.py:126` ← `Candle.from_kite(row)` = `kite.historical_data()` = **TRUE PER-INTERVAL DELTA volume**. Same for S&R (`detector.py:238/243`, `zones.py:107`) and `core/daily_stats.py:66` (`avg_volume_20d`). **Monday's PB-01 expectations do NOT change.**

The tick path is inert **three times over**: (1) `subscribe()` sets `MODE_LTP` (`live_feed.py:182`) ⇒ no `volume_traded` ⇒ `main.py:2543` `int(t.get("volume") or 0)` = **0**; (2) nothing subscribes (below); (3) **measured** — all **275,129** production `analytics.candles` rows carry `fetch_daily_candles`' space-`ts`; rows in `_persist_candle`'s ISO-`T` format: **ZERO**, ever. Stored volume proven **DELTA from the data** (40/40 (symbol,date) groups non-monotonic), not inferred from the field name. Only tick-volume readers: `smart_tgt_manager.py:392` (config `volume_dependent_trails:false` AND the body is an explicit `pass`) and `_persist_candle`. **No reader selects `volume` from the candles table at all.**

## ✅ M-K3 — **ZERO latent FK violations**; nothing enabled
0 violating rows / 14 FK-carrying tables / 92,318 rows; `integrity_check` ok. **Anti-vacuity proven** (planted one on a throwaway copy: 0→1, and `foreign_keys=ON` blocked the same INSERT). **No FK-off connection writes to ANY FK-carrying table** — the 3 DELETE-capable prune jobs (`db_retention`, `eod_cleanup`, `trade_journal`) all go through `StateStore` ⇒ enabling would be a **behavioural no-op**. **⚠️ M-K3's `synchronous=FULL` half does NOT reproduce**: the default is already **2 (FULL)** on VM (py3.12.3/sqlite3.45.1) and PC — inherited from the compile-time default rather than asserted, which is the (much smaller) real point.

## E-items
**E2 `0a54c61` [LATENT]** — `breakeven_manager._get_sl_broker_order_id` selected `broker_order_id`, a column `orders` does not have (the broker id IS the PK `order_id`); `OperationalError` → own `except` → `None` ⇒ the advance could never fire. **Column only** — the status set is untouched because `structure_exit_manager.py:74` derives `_SL_LIVE_EXCLUDE` from this exact call site by reference. Found by the real schema: the query's `'REJECTED'` clause is **dead** (the schema CHECK forbids that status; `order_monitor` maps Kite REJECTED→FAILED).
**E1 — SHIPPED `4a0c0b2`** (was HELD); the defect is in the CALLER `reports/daily_report.py:1511` (`build_taxonomy_map()` with no arg); `strategies/taxonomy.py:23` is correct. That file **is** the F2-gated 16:05 report. Also a **prod no-op**: the cron runs `-m reports.daily_report` with no `--config-dir`.
**E3 `2592d6e`** — SYSTEM_MAP line for maintained-but-never-wired. Measured: **six** commits on `breakeven_manager.py` (created 31-May FIX-132a, then FIX-148/179/181/23-Jun tick-snap/14-Jul M-X2) while `git log -S "BreakevenManager" -- main.py` returns **NOTHING** for the whole history.

[[silent-failure-gaps-25jul]] [[capital-readers-fixed-25jul]] [[unpushed-pending-deploy-ledger]] [[feedback-verify-rc-not-output]]
