#!/usr/bin/env bash
SP="/c/Users/rama/AppData/Local/Temp/claude/D--Projects-trading-system/3bdb2912-ae06-4bd6-bc2f-4df54526afca/scratchpad"
PY="/c/python311/python.exe"
export PATH="$SP/shim:$PATH"
# Wait for the n907 run to finish so no two pytest runs overlap (instance-lock).
while [ ! -f "$SP/gate-n907.rc" ]; do sleep 20; done
sleep 5
NAME="gate-tiers"; WT="$SP/$NAME"
echo "############ $NAME START $(date '+%Y-%m-%d %H:%M:%S %Z') ############"
cd "$WT" || exit 9
echo "HEAD:      $(git rev-parse HEAD)"
echo "launcher:  $(uname -s) / bash=$(command -v bash) / python3=$(command -v python3)"
echo "python:    $($PY -V 2>&1)"
echo "pytest:    $($PY -m pytest --version 2>&1)"
FP_BEFORE=$(git diff HEAD | md5sum | cut -d' ' -f1)
echo "tree_fingerprint_before: $FP_BEFORE"
T0=$(date +%s)
$PY -m pytest tests/unit tests/integration -q > "$SP/${NAME}.out" 2>&1
RC=$?
T1=$(date +%s)
echo "RAW_PYTEST_RC=$RC"
echo "elapsed_sec=$((T1-T0))"
FP_AFTER=$(git diff HEAD | md5sum | cut -d' ' -f1)
echo "tree_fingerprint_after:  $FP_AFTER"
if [ "$FP_BEFORE" = "$FP_AFTER" ]; then echo "tree_fingerprint: IDENTICAL"; else echo "tree_fingerprint: ***MOVED***"; fi
echo "--- tail ---"; tail -6 "$SP/${NAME}.out"
grep -E '^FAILED ' "$SP/${NAME}.out" | sed 's/^FAILED //' | sed 's/ - .*//' | sort > "$SP/${NAME}.failids"
grep -E '^FAILED ' "$SP/${NAME}.out" | sort > "$SP/${NAME}.failmsgs"
echo "failed_ids_count=$(wc -l < "$SP/${NAME}.failids")"
echo "$RC" > "$SP/${NAME}.rc"
echo "############ $NAME END $(date '+%H:%M:%S') rc=$RC ############"
