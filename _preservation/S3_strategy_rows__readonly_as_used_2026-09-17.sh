# READ-ONLY. Piped to the VM via `ssh host 'bash -s' < this file` -- NOTHING is copied to the VM.
# Every sqlite3 call is -readonly AND mode=ro. No redirection to any VM path.
cd /home/ubuntu/systems/trading-system || exit 9
DB="file:data_store/trading_system.db?mode=ro"
Q() { sqlite3 -readonly "$DB" "$1" 2>&1; }
echo "host=$(hostname) now=$(TZ=Asia/Kolkata date '+%F %T') IST"
echo "--- identity of the DB file read (stat only) ---"
stat -c '%n %s bytes mtime %y' data_store/trading_system.db
echo "--- (a) trades per strategy: ALL strategies, all rows (no window, no join) ---"
Q "SELECT strategy||'|'||COUNT(*)||'|P_notnull='||SUM(entry_target_price IS NOT NULL)||'|S_notnull='||SUM(sl_initial IS NOT NULL)||'|first='||MIN(created_at)||'|last='||MAX(created_at) FROM trades GROUP BY strategy ORDER BY COUNT(*) DESC;"
echo "--- (a) total trades, and total in the 16-Sep comparable-row selector (JOIN signals, P and trigger NOT NULL) ---"
Q "SELECT 'trades_total='||COUNT(*) FROM trades;"
Q "SELECT 'joined_comparable='||COUNT(*) FROM trades t JOIN signals s ON s.signal_id=t.signal_id WHERE t.entry_target_price IS NOT NULL AND s.trigger_price IS NOT NULL;"
echo "--- (a) the three unmeasured strategies, with a CONTROL strategy that has rows (gap_go_short) ---"
for st in pb01_breakout_retest range_breakout_long range_breakout_short gap_go_short; do
  echo "  [$st] trades=$(Q "SELECT COUNT(*) FROM trades WHERE strategy='$st';") signals=$(Q "SELECT COUNT(*) FROM signals WHERE strategy='$st';") signals_by_scanner_name=$(Q "SELECT COUNT(*) FROM signals WHERE scanner='$st';") first_signal=$(Q "SELECT COALESCE(MIN(received_at),'-') FROM signals WHERE strategy='$st';") last_signal=$(Q "SELECT COALESCE(MAX(received_at),'-') FROM signals WHERE strategy='$st';")"
done
echo "--- (a) signal status breakdown for the three (why no trade) ---"
Q "SELECT strategy||'|'||status||'|'||COALESCE(rejection_reason,'-')||'|'||COUNT(*) FROM signals WHERE strategy IN ('pb01_breakout_retest','range_breakout_long','range_breakout_short') GROUP BY strategy,status,rejection_reason ORDER BY strategy,COUNT(*) DESC LIMIT 40;"
echo "--- (a) webhook_audit by scanner_name (LIKE), all retained rows, with a CONTROL ---"
Q "SELECT scanner_name||'|rows='||COUNT(*)||'|first='||MIN(ts)||'|last='||MAX(ts)||'|codes='||GROUP_CONCAT(DISTINCT response_code) FROM webhook_audit WHERE scanner_name LIKE '%range_breakout%' OR scanner_name LIKE '%pb01%' OR scanner_name='gap_go_short' GROUP BY scanner_name;"
Q "SELECT 'webhook_audit_span='||MIN(ts)||'..'||MAX(ts)||' rows='||COUNT(*) FROM webhook_audit;"
echo "--- (b) pb01 YAML on this VM ---"
md5sum config/strategies/pb01_breakout_retest.yaml config/strategies/range_breakout_long.yaml config/strategies/range_breakout_short.yaml
grep -nE '^(enabled|intent|v3_playbook):' config/strategies/pb01_breakout_retest.yaml config/strategies/range_breakout_long.yaml config/strategies/range_breakout_short.yaml
echo "--- (b) today's boot strategy_control.summary + pb01 process activity so far (app log, read-only grep) ---"
f=logs/system_$(TZ=Asia/Kolkata date +%F).log
if [ -f "$f" ]; then
  grep -h '"msg":"strategy_control.summary"' "$f" | head -2
  echo "  pb01_watchlist lines today so far: $(grep -c '"logger":"pb01_watchlist"' "$f")"
else
  echo "  $f ABSENT"
fi
prev=logs/system_2026-09-16.log
if [ -f "$prev" ]; then
  echo "  16-Sep: strategy_control.summary lines: $(grep -c '"msg":"strategy_control.summary"' "$prev") · pb01_watchlist lines: $(grep -c '"logger":"pb01_watchlist"' "$prev") · pb01 would-be lines: $(grep -c 'pb01 would-be' "$prev")"
  grep -h '"msg":"strategy_control.summary"' "$prev" | head -1 | cut -c1-900
fi
