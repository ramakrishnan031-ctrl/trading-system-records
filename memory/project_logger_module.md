---
name: logger module built and locked (L1–L10)
description: core/logger.py + 32 tests green; L1–L10 locked; Windows teardown fix documented
type: project
originSessionId: fed36863-cc65-4721-ae69-4940be7f7ec0
---
core/logger.py is built and green as of 2026-04-15.

**What was built:**
- L1–L10 locked in docs/locked_decisions.yaml under `logger_module:` section
- core/logger.py: _JsonFormatter, _PlainFormatter, _SystemFilter, _TradesFilter, _ReconcilerFilter, get_logger, TradeContext, bind_trade, log_exception, setup_logging
- tests/unit/test_logger.py: 32 tests, all passing

**Key decisions (locked):**
- L1: 4 daily log files — system/trades/reconciler (JSON-lines), debug (plain text)
- L2: get_logger(name) → Logger; bind_trade(log, *, signal_id, trade_id, order_id) → TradeContext
- L3: Routing by filter — reconciler=order_reconciler*/order_monitor*; trades=has signal_id/trade_id/order_id; system=INFO+ catch-all; debug=all DEBUG+. One record can land in multiple files.
- L4: WARNING+ mirrored to stdout always, no config flag
- L5: get_logger returns stdlib logging.Logger, no handlers attached by get_logger
- L6: Fresh files per setup_logging() call, append mode, filenames from today_ist()
- L7: log_exception reads exc.SEVERITY for TradingSystemError; ERROR for all others; always exc_info + exc.context
- L8: setup_logging() creates log dir (mkdir parents=True, exist_ok=True)
- L9: JSON field order: ts, level, logger, msg, signal_id?, trade_id?, order_id?, symbol?, <extra alphabetical>, exc_type?, exc_traceback?
- L10: get_logger caches by name; setup_logging() removes previous handlers before attaching new ones

**Windows-specific fix:**
- _teardown() in tests MUST be called INSIDE the `with TemporaryDirectory` block (after reading lines, before block exits) — Windows cannot delete a temp dir while FileHandlers still hold the files open.

**Why:** Single structured logging facade for all modules. G2a traceability requires every trade-related log line to carry signal_id/trade_id/order_id.

**How to apply:** Every module calls get_logger(__name__). For trade context, wrap with bind_trade(). main.py calls setup_logging() once before anything else logs. Never call setup_logging() in module code.
