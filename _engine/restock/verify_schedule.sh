#!/bin/zsh
# Verifies both LaunchAgents can actually read their scripts. Run after granting
# Full Disk Access to /bin/zsh. Both jobs live under ~/Documents, which macOS TCC
# blocks for launchd-spawned processes until that grant exists.
UID_=$(id -u)
for job in com.brooks.velantra-restock com.brooks.margin-nightly; do
  err=""
  case $job in
    com.brooks.velantra-restock) err="/Users/brooksorradre2/Documents/marketing brain/_engine/restock/logs/launchd.err.log";;
    com.brooks.margin-nightly)   err="/Users/brooksorradre2/Documents/marketing brain/_engine/finance/logs/launchd.err.log";;
  esac
  : > "$err"
  launchctl kickstart -p gui/$UID_/$job >/dev/null 2>&1
done
sleep 45
ok=1
for pair in \
  "com.brooks.velantra-restock:/Users/brooksorradre2/Documents/marketing brain/_engine/restock/logs/launchd.err.log" \
  "com.brooks.margin-nightly:/Users/brooksorradre2/Documents/marketing brain/_engine/finance/logs/launchd.err.log"; do
  job="${pair%%:*}"; err="${pair#*:}"
  if grep -q "can't open input file" "$err" 2>/dev/null; then
    echo "FAIL  $job — still blocked by Full Disk Access"; ok=0
  else
    echo "OK    $job — launchd can read and run it"
  fi
done
[[ $ok == 1 ]] && echo "\nBoth schedulers are live." || echo "\nAdd /bin/zsh under System Settings > Privacy & Security > Full Disk Access, then re-run this."
