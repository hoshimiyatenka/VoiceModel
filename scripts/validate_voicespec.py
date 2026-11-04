#!/usr/bin/env python3
"""Validate a VoiceSpec JSON instance against configs/voicespec/voicespec.schema.json.

Usage:
    python scripts/validate_voicespec.py <file.json> [<file2.json> ...]
    python scripts/validate_voicespec.py configs/voicespec/examples/*.json

Exit code 0 = all valid; 1 = at least one invalid; 2 = usage/IO/schema error.
Requires: jsonschema (see scripts/requirements.txt).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: 缺少 jsonschema，请先执行: python -m pip install -r scripts/requirements.txt", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "configs" / "voicespec" / "voicespec.schema.json"


def load_schema() -> dict:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("用法: python scripts/validate_voicespec.py <file.json> [...]", file=sys.stderr)
        return 2
    try:
        schema = load_schema()
        Draft202012Validator.check_schema(schema)
    except Exception as e:  # noqa: BLE001 - CLI 工具直接报错即可
        print(f"ERROR: schema 无法加载/不合法: {e}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema)
    failed = 0
    for arg in argv[1:]:
        p = Path(arg)
        try:
            with p.open("r", encoding="utf-8") as f:
                instance = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[FAIL] {p}: 读取/解析失败: {e}")
            failed += 1
            continue
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
        if not errors:
            print(f"[ OK ] {p}")
            continue
        failed += 1
        print(f"[FAIL] {p}: {len(errors)} 个错误")
        for e in errors:
            loc = "/".join(str(x) for x in e.absolute_path) or "<root>"
            print(f"       - {loc}: {e.message}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
