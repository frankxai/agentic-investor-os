#!/usr/bin/env python3
"""Validate public-safe canon cards. Stdlib only."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED = ("id", "type", "domain", "license", "public_ok", "hitl_status")
MAX_QUOTE_WORDS = 90


def fail(msg: str) -> int:
    print(f"canon validation failed: {msg}", file=sys.stderr)
    return 1


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated YAML frontmatter")
    raw = parts[1]
    data: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, buf
        if current is None:
            return
        data[current] = " ".join(x.strip() for x in buf if x.strip())
        current = None
        buf = []

    for line in raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            flush()
            current = m.group(1)
            rest = m.group(2).strip().strip('"')
            if rest in {">-", "|", ">"}:
                buf = []
            else:
                buf = [rest]
        elif current is not None:
            buf.append(line)
    flush()
    return data


def quote_words(value: str) -> int:
    cleaned = re.sub(r"^['\"]|['\"]$", "", value).strip()
    if not cleaned:
        return 0
    return len(cleaned.split())


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    knowledge = root / "knowledge"
    if not (knowledge / "CANON_CONTRACT.md").is_file():
        return fail("missing knowledge/CANON_CONTRACT.md")
    if not (knowledge / "RIGHTS.jsonl").is_file():
        return fail("missing knowledge/RIGHTS.jsonl")

    rights_ids: set[str] = set()
    for i, line in enumerate((knowledge / "RIGHTS.jsonl").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            return fail(f"RIGHTS.jsonl line {i}: {exc}")
        if "id" not in row or "license" not in row:
            return fail(f"RIGHTS.jsonl line {i} missing id or license")
        if row["license"] == "private-cold" and row.get("public_ok") is not False:
            return fail(f"{row['id']} private-cold must set public_ok false")
        rights_ids.add(row["id"])

    cards = sorted((knowledge / "cards").glob("*.md"))
    if len(cards) < 3:
        return fail("need at least 3 cards")

    seen: set[str] = set()
    for path in cards:
        text = path.read_text(encoding="utf-8")
        try:
            meta = parse_frontmatter(text)
        except ValueError as exc:
            return fail(f"{path.name}: {exc}")
        for key in REQUIRED:
            if key not in meta or meta[key] == "":
                return fail(f"{path.name} missing {key}")
        if meta["id"] in seen:
            return fail(f"duplicate id {meta['id']}")
        seen.add(meta["id"])
        if meta["hitl_status"] not in {"pending_human_review", "accepted", "rejected"}:
            return fail(f"{path.name} bad hitl_status")
        words = quote_words(meta.get("quote", ""))
        if words > MAX_QUOTE_WORDS:
            return fail(f"{path.name} quote has {words} words (max {MAX_QUOTE_WORDS})")
        if "C:\\Users\\" in text or re.search(r"/Users/[A-Za-z0-9._-]+/", text):
            return fail(f"{path.name} contains a machine path")

    print(f"canon validation passed: {len(cards)} cards, {len(rights_ids)} rights rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
