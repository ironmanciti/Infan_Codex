"""Check added patch lines for credential-like values before apply_patch runs."""

import json
import re
import sys


PATTERNS = (
    ("API key", r"sk-[A-Za-z0-9_-]{20,}"),
    ("GitHub token", r"ghp_[A-Za-z0-9]{30,}"),
    ("private key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("password", r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}['\"]"),
)


def added_lines(patch: str) -> str:
    """Return only added content, excluding patch headers."""
    return "\n".join(
        line[1:]
        for line in patch.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


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
    content = added_lines(patch)
    hits = [label for label, pattern in PATTERNS if re.search(pattern, content)]
    if hits:
        print(f"Patch blocked: possible hardcoded {', '.join(hits)}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
