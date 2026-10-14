"""Lab 1 checker. Run from the repo root: python scripts/check_lab1.py"""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
problems: list[str] = []


def need(cond: bool, msg: str) -> None:
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        problems.append(msg)


settings_path = root / ".claude" / "settings.json"
need(settings_path.exists(), ".claude/settings.json exists")
if settings_path.exists():
    try:
        s = json.loads(settings_path.read_text())
    except json.JSONDecodeError as e:
        s = {}
        need(False, f"settings.json is valid JSON ({e})")
    perms = s.get("permissions", {})
    need(perms.get("defaultMode") == "default", 'permissions.defaultMode is "default" (Manual)')
    deny = " ".join(perms.get("deny", []))
    ask = " ".join(perms.get("ask", []))
    allow = " ".join(perms.get("allow", []))
    for label, text, needle in [
        ("deny reading .env", deny, "Read(./.env)"),
        ("deny reading patient seed data", deny, "seed/patients"),
        ("deny editing migrations", deny, "migrations"),
        ("deny curl", deny, "Bash(curl"),
        ("deny editing workflows", deny, ".github/workflows"),
        ("ask before git push", ask, "git push"),
        ("allow running pytest", allow, "pytest"),
    ]:
        need(needle in text, label)

claude_md = root / "CLAUDE.md"
need(claude_md.exists(), "CLAUDE.md exists")
if claude_md.exists():
    text = claude_md.read_text()
    need(len(text.splitlines()) < 80, "CLAUDE.md is under 80 lines")
    need("@AGENTS.md" in text, "CLAUDE.md imports @AGENTS.md")
    need("@docs/org-rules.md" in text, "CLAUDE.md imports @docs/org-rules.md")

rule = root / ".claude" / "rules" / "python-tests.md"
need(rule.exists(), ".claude/rules/python-tests.md exists")
if rule.exists():
    need(bool(re.search(r"^paths:", rule.read_text(), re.M)), "rule file has `paths:` frontmatter")

print()
print("ALL CHECKS PASSED" if not problems else f"{len(problems)} CHECK(S) FAILED")
sys.exit(1 if problems else 0)
