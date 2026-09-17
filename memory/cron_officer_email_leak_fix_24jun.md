---
name: cron-officer-email-leak-fix-24jun
description: Post-ban CRITICAL Cron Officer briefing emailed a raw-MarkdownV2 blob; fixed via write_sentinel=False + own clean HTML backup; full job list in email; DEPLOYED 24-Jun
metadata: 
  node_type: memory
  type: project
  originSessionId: 0f749f67-83ec-4017-8cb1-3dd7bd23c640
---

**Fixed + DEPLOYED 24-Jun (commit `8a7de23`, branch `cron-officer-email-leak-fix-24jun`, live tree 10:38 IST; alerting-only — no schema, no restart, next 09:20 cron uses it).**

**Symptom:** first post-ban day (Telegram `telegram_ban_until` 2026-06-23 lapsed) the 09:20 morning briefing — CRITICAL via `_compute_severity` — emailed an ugly raw-MarkdownV2 blob (`24\-Jun…+11 more`, no proper subject) IN ADDITION to the correct Telegram message. Masked during the ban (ban branch emailed clean HTML + skipped Telegram); first post-ban day = first leak.

**Root cause:** `cron_officer._send_telegram_md` (post-ban Telegram-only path) → `TelegramNotifier.send(severity=CRITICAL)` → `_handle_critical` UNCONDITIONALLY wrote a bare `write_critical_sentinel` (no subject/html, body = the MarkdownV2 telegram render, tag TG5); `alert_watcher` SMTP'd it. Ban-over IS detected correctly (`ban_active = today <= telegram_ban_until` → False on 24-Jun) — this was NOT a ban-detection bug.

**Fix (Option A, backward-compatible):** `TelegramNotifier.send`/`_handle_critical` gained `write_sentinel: bool = True`. Default keeps the TG5 sentinel→email for EVERY other CRITICAL caller (main, kill_switch, order_reconciler, eod_squareoff, token_monitor, order_placer — all verified unchanged). `False` suppresses BOTH the sentinel and the telegram-failure email fallback. `_send_telegram_md` now passes `write_sentinel=False`; `deliver_report` writes ONE clean HTML email backup for the post-ban CRITICAL case (`email_backup = is_eod or ban or severity=="CRITICAL"`, reusing `render_briefing_html`). **Net (Rama's belt-and-suspenders call):** post-ban CRITICAL = clean Telegram + clean HTML email backup; post-ban INFO/WARN = Telegram only; ban window + EOD unchanged.

**Full job list:** the `+N more` cap lives ONLY in `render_briefing_telegram` (compact/phone) — the HTML + plaintext email renderers never truncated, so routing the email through `render_briefing_html` restores the full ~39-job list automatically (live-data proof: 33/33 completed+pending in the email). Added a "📧 Full list → email" Telegram footer when CRITICAL.

**Why today was CRITICAL (Part 3 — investigated, NOT a fix):** transient FALSE-POSITIVE — recomputed `build_report` is INFO (today's 19 heartbeats all SUCCESS, security-watcher fresh, preflight READY). NOT `daily_report` (PENDING_REDESIGN never escalates), NOT a real persistent miss — most consistent with a sub-second heartbeat-visibility race at the 09:20:00 cron boundary (~14 crons fire near 09:20; the briefing snapshotted state before a sibling heartbeat committed). Self-cleared; not reproducible post-hoc.

**Tests/verification:** +5 (`test_telegram_notifier` write_sentinel-suppress ×2 + signature-lock updated; `test_cron_officer_revision` post-ban clean-HTML / INFO-telegram-only / 39-job no-truncation). Full suite **3720 pass** (1 pre-existing PC-env `test_system_manager` fail, proven pre-existing by stash); VM-venv touched-area **145 pass**; live-data `deliver_report` proof = exactly 1 clean HTML email, subject `[LFL836] …`, no MarkdownV2.

**Follow-ups (separate, NOT done):** (1) debounce the briefing CRITICAL transient race (re-check after a short grace, or stagger the 09:20 briefing after the */5 metrics crons) so Rama stops getting a daily false CRITICAL — now at least it is a CLEAN email. (2) Queued next: `tgt_retry_manager` crash post-mortem, PACEDIGITK after-check circuit-cap false-positive, YAMLs→1.5, Slice 2.

Related: [[test_sentinel_isolation_24jun]] · [[fix_191_false_softkill_23jun]] · [[task_10_telegram_master_switch]] · [[cron_officer_revision_20jun]]
