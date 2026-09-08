#!/usr/bin/env bash
set -euo pipefail
for lab_command in python3 pwd ls mkdir touch cp mv rm rmdir cat head tail grep wc find; do
  if ! command -v "$lab_command" >/dev/null; then
    printf 'Missing command: %s. Ask your instructor to check the environment.\n' "$lab_command" >&2
    exit 1
  fi
done
lab_kit_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python3 "$lab_kit_dir/setup.py"
