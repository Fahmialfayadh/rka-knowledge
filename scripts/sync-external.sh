#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
echo "[*] Syncing external vendor copies..."

for repo in "Modul-ML-RKA:main:https://github.com/kcv-if/Modul-ML-RKA" "Modul-DM-RKA:master:https://github.com/kcv-if/Modul-DM-RKA"; do
  IFS=: read -r name branch url <<< "$repo"
  tmp="/tmp/$name"
  rm -rf "$tmp"
  echo "[*] Cloning $name ($branch) from $url ..."
  git clone --depth 1 --branch "$branch" "$url" "$tmp"
  echo "    commit: $(git -C "$tmp" log --oneline -1)"
  rsync -av --delete --exclude=".git" "$tmp/" "$BASE/external/$name/"
  echo "    -> $BASE/external/$name/ updated"
done

echo "[*] Done. Update external/ATTRIBUTION.md with new hashes:"
git -C /tmp/Modul-ML-RKA log --oneline -1
git -C /tmp/Modul-DM-RKA log --oneline -1
