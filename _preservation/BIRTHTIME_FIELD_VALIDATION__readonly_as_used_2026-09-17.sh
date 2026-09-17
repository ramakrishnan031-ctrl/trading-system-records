# READ-ONLY (17-Sep card "THREE SMALL ITEMS" section 2): does `stat %w` (birth time) work on the logs/ filesystem?
# Controls with KNOWN creation moments. ⛔ The evaluator's log path, script and cron entry are NOT touched.
L=/home/ubuntu/systems/trading-system/logs
export LC_ALL=C
echo "now=$(date '+%F %T %z')"
stat --version | head -n 1
df -T "$L" | tail -n 1
for f in "$L/system_2026-09-17.log" "$L/cron-drift-check.log"; do
  stat -c 'FILE %n | birth(%%w)=%w | ctime(%%z)=%z | mtime(%%y)=%y | size(%%s)=%s' "$f"
done
echo "KNOWN CREATION MOMENT of system_2026-09-17.log = its first event:"
head -n 1 "$L/system_2026-09-17.log" | cut -c1-48
echo "##### END"
