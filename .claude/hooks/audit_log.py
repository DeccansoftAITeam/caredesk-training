#!/usr/bin/env python3
"""Audit hook: one JSON line per tool call, appended to .agents/audit.jsonl.

Wired as a PostToolUse hook with matcher "*" (all tools, including Read). See docs/audit-log-schema.md.

FAILS OPEN: any internal error is swallowed and the exit code is always 0, so a logging problem can never block
a tool. (Blocking is the job of permission rules and the other hooks. Exit code 2 would block.)

Redaction is by VALUE, not only by key name: a token inside a shell command string is still a token.
"""
import datetime
import json
import os
import re
import sys

REDACTIONS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"), "[SECRET]"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]{12,}"), r"\1[SECRET]"),
    (re.compile(r"(?i)((?:api[_-]?key|secret|token|password|passwd|pwd)\s*[=:]\s*)\S+"), r"\1[SECRET]"),
    (re.compile(r"(?<![\w.])\+?\d[\d\s().\-]{8,}\d(?![\w.])"), "[PHONE]"),  # 10+ digit runs such as +91-90000-00001
]
MAX_CHARS = 500


def redact(value):
    if isinstance(value, str):
        for pattern, replacement in REDACTIONS:
            value = pattern.sub(replacement, value)
        if len(value) > MAX_CHARS:
            value = value[:MAX_CHARS] + f"...[+{len(value) - MAX_CHARS} chars]"
        return value
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def main() -> None:
    data = json.load(sys.stdin)
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "event": data.get("hook_event_name"),
        "session_id": data.get("session_id"),
        "tool": data.get("tool_name"),
        "input": redact(data.get("tool_input")),
        "cwd": data.get("cwd"),
    }
    folder = os.path.join(root, ".agents")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "audit.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


try:
    main()
except BaseException:  # fail open: never let logging block work
    pass
sys.exit(0)
