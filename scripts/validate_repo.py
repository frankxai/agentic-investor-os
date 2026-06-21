#!/usr/bin/env python3
"""Validate Agentic Investor OS starter repo."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "SKILLS.md",
    "WORKFLOWS.md",
    "LOOPS.md",
    "docs/MODULE_CHARTER.md",
    "docs/SAMPLE_DILIGENCE_MEMO.md",
    "docs/COMMERCIAL_STRATEGY.md",
    "docs/INVESTOR_OS_PLAYBOOK.md",
    "docs/README_QUALITY_NOTES.md",
    "registry/investor-os.json",
    "templates/diligence-memo.md",
    "templates/risk-register.md",
    "templates/portfolio-support-plan.md",
    "templates/diligence-sprint-plan.md",
    "templates/investor-update.md",
    "examples/sample-opportunity-intake.json",
]

FORBIDDEN_PATTERNS = [
    re.compile(r"C:\\Users\\", re.IGNORECASE),
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"\bguaranteed\s+(income|returns|profit|revenue)\b", re.IGNORECASE),
    re.compile(r"\bfinancial\s+advice\b", re.IGNORECASE),
]


def fail(message: str) -> int:
    print(f"validation failed: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} root must be an object")
    return data


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            return fail(f"missing {relative}")

    registry = load_json(root / "registry/investor-os.json")
    for key in ["id", "name", "version", "standard", "agents", "workflows", "loops", "approvalGates"]:
        if key not in registry:
            return fail(f"registry missing {key}")
    if registry["id"] != "investor-os":
        return fail("registry id must be investor-os")
    if len(registry["agents"]) < 7:
        return fail("registry should define at least seven agents")

    for path in root.rglob("*"):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".py", ".yml", ".yaml"}:
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_PATTERNS:
                match = pattern.search(text)
                if match:
                    return fail(f"{path.relative_to(root)} contains blocked phrase or path: {match.group(0)}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    for phrase in ["Agentic Investor OS", "diligence", "risk register", "portfolio support"]:
        if phrase not in readme:
            return fail(f"README missing {phrase}")

    print("Agentic Investor OS validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
