#!/usr/bin/env bash
set -euo pipefail
lab_repository="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$lab_repository"
for lab_command in bash python3 ls mkdir touch cp mv rm rmdir cat head tail grep wc find; do
    command -v "$lab_command" >/dev/null || { printf 'Missing: %s\n' "$lab_command" >&2; exit 1; }
done
bash -n terminal-lab-1/start.sh
python3 -B - <<'PY'
import ast
import importlib.util
from pathlib import Path
import tempfile

kit = Path('terminal-lab-1').resolve()
for name in ('setup.py', 'check.py'):
    ast.parse((kit / name).read_text(), filename=name)
spec = importlib.util.spec_from_file_location('lab_setup', kit / 'setup.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='terminal-lab-preflight-') as folder:
    root = Path(folder) / 'attempt'
    module.create('PREFLIGHT', root)
    assert (root / 'identity.txt').is_file()
    assert (root / 'rescue/system.log').is_file()
    assert len(list((root / 'practice/wildcards').rglob('*.txt'))) == 4
print('Bash tools, Python files, and Lab 1 data generator: ready.')
PY
printf '\nLab 1 is ready. In this repository folder, run:\n\n  bash terminal-lab-1/start.sh\n\nUse your instructor-assigned lab ID, then follow the printed cd command.\n'
