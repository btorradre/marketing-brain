#!/bin/bash
# Poll all jobs and download completed ones; loops until all done or max iterations.
cd "/Users/brooksorradre2/Documents/marketing brain/brands/motilli/landing-pages/assets/new-gen"

MAX_ITER=60
for iter in $(seq 1 $MAX_ITER); do
  pending=0
  for jf in jobs/*.json; do
    [ ! -s "$jf" ] && continue
    name=$(basename "$jf" .json)
    # Skip the throwaway test job
    [ "$name" = "0288cac2-test" ] && continue
    [ -f "${name}.png" ] && continue
    id=$(jq -r '.[0]' "$jf" 2>/dev/null)
    [ -z "$id" ] || [ "$id" = "null" ] && continue

    out=$(higgsfield generate get "$id" --json 2>/dev/null)
    status=$(echo "$out" | jq -r '.status' 2>/dev/null)

    if [ "$status" = "completed" ]; then
      url=$(echo "$out" | jq -r '.result_url' 2>/dev/null)
      if [ -n "$url" ] && [ "$url" != "null" ] && [ "$url" != "" ]; then
        curl -sL -o "${name}.png" "$url"
        sz=$(stat -f%z "${name}.png" 2>/dev/null)
        echo "[iter $iter] DOWNLOADED: ${name}.png ($sz bytes)"
      else
        echo "[iter $iter] NO URL for $name"
        pending=$((pending+1))
      fi
    elif [ "$status" = "failed" ] || [ "$status" = "error" ]; then
      echo "[iter $iter] FAILED: $name ($id)"
    else
      pending=$((pending+1))
    fi
  done
  echo "[iter $iter] pending=$pending"
  [ $pending -eq 0 ] && break
  sleep 15
done

echo "==== FINAL ===="
ls -la *.png 2>/dev/null | wc -l
