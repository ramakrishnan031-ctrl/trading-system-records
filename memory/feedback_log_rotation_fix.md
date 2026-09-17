---
name: Log rotation fix - no mid-day .log.1/.log.2 files
description: RotatingFileHandler replaced with FileHandler to enforce one log file per day (Foundation Rule 1.7)
type: feedback
originSessionId: b2686c5d-ac77-4544-9f06-8be8428ac9f2
---
RotatingFileHandler with maxBytes creates .log.1, .log.2 backups mid-day when file exceeds size threshold. This violates Foundation Rule 1.7 (resume-safe, one file per day).

**Why:** Log files contain the date in filename (`{stem}_{date_str}.log`). Mid-day rotation creates duplicate files that break resume-safe assumption and complicates log analysis.

**How to apply:** Use plain `logging.FileHandler` instead of `RotatingFileHandler`. Date rotation is implicit via the date-embedded filename; no size-based rotation needed. If log volume becomes extreme, consider daily compression via cron rather than mid-day splits.

Fix applied in commit (2026-04-29): core/logger.py line 280-286.
