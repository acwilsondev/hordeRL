#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
locale_dir="$repo_root/horderl/resources/locales"

REPO_ROOT="$repo_root" python3 - <<'PY'
import json
import re
import os
from pathlib import Path

repo_root = Path(os.environ["REPO_ROOT"]).resolve()
locale_dir = repo_root / "horderl" / "resources" / "locales"

pattern = re.compile(r"t\(\s*(['\"])(.*?)\1")
keys = set()
for path in (repo_root / "horderl").rglob("*.py"):
    text = path.read_text(encoding="utf-8")
    for match in pattern.finditer(text):
        key = match.group(2).strip()
        if key:
            keys.add(key)

locale_files = sorted(locale_dir.glob("*.json"))
if not locale_files:
    raise SystemExit(f"No locale files found in {locale_dir}")

exit_code = 0
for locale_path in locale_files:
    data = json.loads(locale_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"Locale file {locale_path} must be a JSON object")
    missing = sorted(keys - data.keys())
    if missing:
        exit_code = 1
        print(f"\n{locale_path.name} is missing {len(missing)} keys:")
        for key in missing:
            print(f"  - {key}")

if exit_code == 0:
    print(f"All {len(keys)} keys present in {len(locale_files)} locale file(s).")

raise SystemExit(exit_code)
PY
