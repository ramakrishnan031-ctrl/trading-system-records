# READ-ONLY pass 3 (17-Sep card "PREDICTION VERIFIED INDEPENDENTLY" section 3): the importer-list members
# that scan2's per-file loop never classified. SAME per-file block as scan2 (flags unchanged), ASCII stdout.
# Positive controls FIRST: the ARMED hook and its repo copy must show the `crontab deploy/cron/...` write.
T=/home/ubuntu/systems/trading-system
cd "$T" || exit 9
echo "now=$(date '+%F %T %z')"
for f in /home/ubuntu/trading-system.git/hooks/post-receive deploy/hooks/post-receive core/state_store.py ops/control_tower/runner.py scripts/cron_report_render.py scripts/monitoring_canary.py scripts/preflight/checks/services.py scripts/system_manager.py strategies/control.py; do
  n=$(grep -Ici 'crontab' "$f" 2>/dev/null)
  echo
  echo "##### $f  (lines mentioning crontab: ${n:-0}; subprocess/os.system/Popen lines: $(grep -Ec 'subprocess|os\.system|Popen|check_output' "$f" 2>/dev/null))"
  echo "md5=$(md5sum < "$f" 2>/dev/null | cut -c1-32) bytes=$(wc -c < "$f" 2>/dev/null)"
  grep -In -i 'crontab' "$f" 2>/dev/null | cut -c1-200 | head -25
done
echo
echo "##### what each of the seven imports from the cron tools (the reason it was on the importer list)"
for f in core/state_store.py ops/control_tower/runner.py scripts/cron_report_render.py scripts/monitoring_canary.py scripts/preflight/checks/services.py scripts/system_manager.py strategies/control.py; do
  echo "--- $f"; grep -In -E 'generate_crontab|check_cron_drift|cron_officer|from core\.cron_registry|import cron_registry' "$f" 2>/dev/null | cut -c1-180
done
echo "##### END"
