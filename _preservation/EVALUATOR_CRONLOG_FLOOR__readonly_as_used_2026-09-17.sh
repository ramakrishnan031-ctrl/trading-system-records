# READ-ONLY (17-Sep card "ONE THING BEFORE 16:05" section 2): the PRE-RUN state of the evaluator's cron log = E-6's
# population floor. INCAPABLE OF CREATING THE FILE: no redirect, no touch, no tee at any logs/ path -- only
# test -e/-L, stat, md5sum/wc with the path as an ARGUMENT, and a listing of the directory.
# NOT a pre-check of the evaluator: the script, the cron entry and the evaluator are NOT read and NOT invoked.
L=/home/ubuntu/systems/trading-system/logs
export LC_ALL=C
echo "now=$(date '+%F %T %z')"
stat -c 'logs_dir type=%F mode=%a owner=%U' "$L"
probe() {
  f="$1"
  if [ -e "$f" ] || [ -L "$f" ]; then
    echo "PRESENT $f"
    stat -c '  type=%F size=%s mtime=%y inode=%i links=%h' "$f"
    echo "  md5=$(md5sum "$f" | cut -c1-32) lines=$(wc -l "$f" | cut -d' ' -f1)"
  else
    echo "ABSENT  $f"
  fi
}
echo "## CONTROL-PRESENT (must read PRESENT, size 12347, md5 a35fd44b...)"; probe "$L/cron-drift-check.log"
echo "## CONTROL-ABSENT (a name that never existed; must read ABSENT)"; probe "$L/cron-sr-shadow-evaluate.log.CONTROL_NEVER_EXISTED_17SEP"
echo "## TARGET"; probe "$L/cron-sr-shadow-evaluate.log"
echo "## logs/ entry names matching sr.shadow (any variant), with the control pattern cron.drift.check"
printf 'match_sr.shadow=%s match_cron.drift.check=%s\n' "$(ls -1A "$L" | grep -c 'sr.shadow')" "$(ls -1A "$L" | grep -c 'cron.drift.check')"
ls -1A "$L" | grep 'sr.shadow'
echo "##### END"
