# READ-ONLY crontab-REWRITE invoker scan. Piped via `ssh trading-sbx 'bash -s'`. No writes, no sudo.
# Question (Rama, 17-Sep): what, other than the push hook, can REWRITE the ubuntu crontab
# (a correct reinstall from canonical/cron_registry drops the hand-added evaluator line as a side effect)?
T=/home/ubuntu/systems/trading-system
echo "host=$(hostname) user=$(id -un) now=$(TZ=Asia/Kolkata date '+%F %T') IST"
echo
echo "=== 0. current crontab: size, evaluator entry still present ==="
echo "lines=$(crontab -l | wc -l) md5=$(crontab -l | md5sum | cut -c1-32) evaluator_entry=$(crontab -l | grep -c 'scripts/sr_shadow_evaluate.py')"
echo
echo "=== 1. bare repo hooks (non-sample) ==="
ls -la /home/ubuntu/trading-system.git/hooks/ 2>&1 | grep -v '\.sample$'
echo "--- post-receive, full text ---"
cat /home/ubuntu/trading-system.git/hooks/post-receive 2>&1
echo
echo "=== 2. deployed tree: every file that mentions crontab / python-crontab / cron_registry (code + scripts + deploy; excl venv/logs/data/.git/tests/docs) ==="
grep -rIl --exclude-dir=venv --exclude-dir=.venv --exclude-dir=logs --exclude-dir=data_store --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=tests --exclude-dir=docs -e 'crontab' -e 'CronTab' -e 'cron_registry' "$T" 2>/dev/null | sed "s|$T/||" | sort
echo
echo "=== 3. deployed tree: lines that can WRITE a crontab (crontab <file>|- , crontab -r, CronTab(...).write, subprocess with crontab) ==="
grep -rIn --exclude-dir=venv --exclude-dir=.venv --exclude-dir=logs --exclude-dir=data_store --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=tests --exclude-dir=docs -E 'crontab[[:space:]]+(-u[[:space:]]+[a-z]+[[:space:]]+)?("|\$|/|[a-zA-Z_.]+\.cron|-[[:space:]]*$|-r|<)|crontab"[[:space:]]*,|\["crontab"|'"'"'crontab'"'"'[[:space:]]*,|CronTab\(|\.write\(\)|cron\.write|write_crontab|install_crontab|crontab_install' "$T" 2>/dev/null | sed "s|$T/||" | grep -v 'crontab -l' | cut -c1-220 | head -60
echo
echo "=== 4. system cron + systemd + home + /usr/local/bin: any mention of crontab ==="
for f in /etc/crontab /etc/cron.d/* /etc/cron.hourly/* /etc/cron.daily/* /etc/cron.weekly/* /etc/cron.monthly/*; do [ -f "$f" ] && grep -IHn 'crontab' "$f" 2>/dev/null; done
grep -rIHn 'crontab' /etc/systemd/system /home/ubuntu/.config/systemd /usr/local/bin 2>/dev/null | cut -c1-220 | head -20
find /home/ubuntu -maxdepth 2 -type f \( -name '*.sh' -o -name '*.py' \) -not -path '*/systems/*' 2>/dev/null | while read -r f; do grep -IHn 'crontab' "$f" 2>/dev/null | cut -c1-200; done
echo "(root crontab / /var/spool/cron not readable without sudo -- NOT searched)"
echo
echo "=== 5. timers + running services (names) ==="
systemctl list-timers --all --no-pager 2>/dev/null | head -30
systemctl list-units --type=service --state=running --no-pager --plain 2>/dev/null | awk '{print $1}' | grep -vE '^(UNIT|LOAD|ACTIVE|SUB|$)' | head -60 | tr '\n' ' '; echo
echo
echo "=== 6. ExecStart/ExecStartPre/Post of non-OS units that could run our scripts ==="
for u in $(systemctl list-unit-files --type=service --type=timer --no-pager --plain 2>/dev/null | awk '{print $1}' | grep -E 'trading|token|watch|cron|monitor|alert|gui|dashboard|backup|deploy|officer|preflight'); do echo "--- $u"; systemctl cat "$u" 2>/dev/null | grep -E '^(ExecStart|ExecStartPre|ExecStartPost|ExecStop|OnCalendar|OnBootSec|Unit=)' ; done
echo
echo "=== 7. what the CURRENT crontab runs that might install/reconcile cron (lines mentioning cron/registry/officer/watchdog/install/deploy/crontab) ==="
crontab -l | grep -nE 'cron|registry|officer|watchdog|install|deploy' | grep -v '^[0-9]*:#' | cut -c1-240
echo
echo "=== 8. deployed tree is a git work tree? other hooks there? ==="
ls -la "$T/.git" 2>&1 | head -3; ls "$T/.git/hooks" 2>/dev/null | grep -v '\.sample$'
