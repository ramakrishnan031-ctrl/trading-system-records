# READ-ONLY pass 2. Enumerate EVERY occurrence of "crontab" (case-insensitive) in each non-doc candidate file,
# so each can be classified by reading (read / write / mention). Positive control: deploy/hooks/post-receive
# MUST show its `crontab deploy/cron/trading-system.cron` write.
T=/home/ubuntu/systems/trading-system
cd "$T" || exit 9
echo "now=$(TZ=Asia/Kolkata date '+%F %T') IST"
for f in deploy/hooks/post-receive scripts/generate_crontab.py core/cron_registry.py scripts/check_cron_drift.py scripts/cron_officer.py alerts/cron_alerts.py scripts/strategy_registry_officer.py scripts/preflight/checks/config_integrity.py scripts/preflight/deliver.py scripts/auto_refresh_token.py scripts/output_retention.py scripts/generate_screened_stocks_csv.py scripts/wal_checkpoint.py scripts/sr_shadow_evaluate.py ops/control_tower/aggregator.py ops_dashboard/backend/readers/host_reader.py ops_dashboard/backend/readers/config_reader.py reports/daily_report.py reports/daily_trade_review.py core/config_loader.py deploy/hooks/pre-commit deploy/hooks/pre-receive; do
  n=$(grep -Ici 'crontab' "$f" 2>/dev/null)
  echo
  echo "##### $f  (lines mentioning crontab: ${n:-0}; subprocess/os.system/Popen lines: $(grep -Ec 'subprocess|os\.system|Popen|check_output' "$f" 2>/dev/null))"
  grep -In -i 'crontab' "$f" 2>/dev/null | cut -c1-200 | head -25
done
echo
echo "##### every subprocess/os.system call in the four cron tools (what binaries do they run?)"
for f in scripts/generate_crontab.py core/cron_registry.py scripts/check_cron_drift.py scripts/cron_officer.py; do
  echo "--- $f"; grep -In -E 'subprocess\.(run|call|check_call|check_output|Popen)|os\.system|os\.popen' "$f" 2>/dev/null | cut -c1-200
done
echo
echo "##### cron_watchdog.py (19:30 timer) + token_watcher.sh: imports / binaries"
grep -In -E '^(import|from) |subprocess|os\.system|crontab|cron_registry' scripts/cron_watchdog.py 2>/dev/null | cut -c1-180
grep -In -E 'crontab|cron_registry|generate_crontab|subprocess|python ' deploy/token_watcher.sh 2>/dev/null | cut -c1-180
echo
echo "##### watcher units: full ExecStart (continuation lines)"
for u in trading-watchman alert-watcher security-watcher gui-dashboard; do echo "--- $u"; systemctl cat "$u" 2>/dev/null | grep -A2 '^ExecStart' | cut -c1-200; done
echo
echo "##### python-crontab library present in either venv?"
ls /home/ubuntu/systems/venv/lib/python*/site-packages/ 2>/dev/null | grep -iE '^(python_crontab|crontab)' || echo "  systems/venv: no python-crontab"
ls "$T"/ops_dashboard/venv/lib/python*/site-packages/ 2>/dev/null | grep -iE '^(python_crontab|crontab)' || echo "  ops_dashboard/venv: no python-crontab"
echo
echo "##### which scripts IMPORT the cron tools (indirect invokers)"
grep -rIln --exclude-dir=venv --exclude-dir=logs --exclude-dir=data_store --exclude-dir=__pycache__ --exclude-dir=tests --exclude-dir=docs -E 'generate_crontab|check_cron_drift|cron_officer|from core\.cron_registry|import cron_registry' --include='*.py' --include='*.sh' . 2>/dev/null | sort
