"""Warn when a Python file touched by apply_patch exceeds 500 lines."""

import json
from pathlib import Path
import re
import sys


LINE_LIMIT = 500
FILE_MARKER = re.compile(r"^\*\*\* (?:Add|Update) File: (.+\.py)$", re.MULTILINE)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (ValueError, TypeError):
        return 0
    if event.get("tool_name") != "apply_patch":
        return 0
    patch = event.get("tool_input", {}).get("command", "")
    if not isinstance(patch, str):
        return 0
    root = Path(event.get("cwd") or ".").resolve()
    findings = []
    for name in set(FILE_MARKER.findall(patch)):
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            continue
        try:
            count = len(path.read_text(encoding="utf-8").splitlines())
        except OSError:
            continue
        if count > LINE_LIMIT:
            findings.append(f"{name}: {count} lines")
    if findings:
        print(json.dumps({"systemMessage": "Python file length exceeds 500 lines: " + ", ".join(findings)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
