# READ-ONLY on trading-sbx (130.210.13.114). Commands used: date md5sum stat tail head grep wc ls. No writes, no /tmp, no DB, no broker.
cd /home/ubuntu/systems/trading-system || exit 9
echo "## now: $(date '+%Y-%m-%dT%H:%M:%S%z')"
echo "## md5 of the drift path files on the VM"
md5sum scripts/check_cron_drift.py core/logger.py scripts/cron_officer.py alerts/telegram_notifier.py scripts/generate_crontab.py core/cron_registry.py utils/cron_heartbeat.py config/cron_registry.yaml core/account_registry.py core/state_store.py
echo "## cron-drift-check.log: stat, line count"
stat -c '%y %s %n' logs/cron-drift-check.log
wc -l < logs/cron-drift-check.log
echo "## cron-drift-check.log: last 45 lines"
tail -n 45 logs/cron-drift-check.log
echo "## syslog CRON CMD lines for check_cron_drift (all rotated plain syslogs)"
grep -h 'check_cron_drift' /var/log/syslog /var/log/syslog.1 2>&1 | tail -n 6
echo "## app log 16-Sep: stat + last 2 lines (first 300 chars each)"
stat -c '%y %s %n' logs/system_2026-09-16.log
tail -n 2 logs/system_2026-09-16.log | cut -c1-300
echo "## app log 16-Sep: count of lines mentioning check_cron_drift / CRON INTEGRITY"
grep -c 'check_cron_drift' logs/system_2026-09-16.log
grep -c 'CRON INTEGRITY' logs/system_2026-09-16.log
echo "## positive control: same grep -c on a line known to be in that file"
grep -c 'Shutdown complete' logs/system_2026-09-16.log
echo "## app log 15-Sep and 14-Sep: same two counts (other days)"
for d in 2026-09-15 2026-09-14; do printf '%s check_cron_drift=' "$d"; grep -c 'check_cron_drift' logs/system_$d.log 2>&1; printf '%s CRON_INTEGRITY=' "$d"; grep -c 'CRON INTEGRITY' logs/system_$d.log 2>&1; done
echo "## crontab: line count, md5, evaluator lines"
crontab -l | wc -l
crontab -l | md5sum
crontab -l | grep -n 'sr_shadow_evaluate'
echo "## END"
