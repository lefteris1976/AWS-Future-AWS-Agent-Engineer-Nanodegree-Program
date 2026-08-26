"""Offline integrity and secret checks for the public portfolio repository."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "prompt_design.md"
FAQ_PATH = ROOT / "knowledge" / "online_shop_faq.md"
TESTS_PATH = ROOT / "tests" / "harness-tests.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def validate_prompt() -> None:
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    required_terms = (
        "description",
        "stepsToReproduce",
        "environment",
        "create_bug_report",
        "FAQ",
        "prompt injection",
    )
    for term in required_terms:
        require(term.lower() in prompt.lower(), f"prompt design is missing required term: {term}")


def validate_faq() -> None:
    faq = FAQ_PATH.read_text(encoding="utf-8")
    question_count = len(re.findall(r"^\d+\)", faq, flags=re.MULTILINE))
    require(question_count == 32, f"expected 32 FAQ entries, found {question_count}")


def validate_tests() -> None:
    payload = json.loads(TESTS_PATH.read_text(encoding="utf-8"))
    tests = payload.get("tests", [])
    require(len(tests) == 7, f"expected 7 tests, found {len(tests)}")

    ids = [case.get("id") for case in tests]
    require(len(set(ids)) == len(ids), "test IDs must be unique")
    require(all(case.get("prompt") and case.get("expected") for case in tests),
            "every test needs prompt and expected text")

    routes = {case.get("route") for case in tests}
    require(routes == {"bug_report", "platform_question", "other_request"},
            f"unexpected route coverage: {sorted(routes)}")


def scan_public_text() -> None:
    patterns = {
        "AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
        "AWS account ID": re.compile(r"(?<!\d)\d{12}(?!\d)"),
        "AWS ARN": re.compile("arn" + ":aws:", re.IGNORECASE),
        "S3 URI": re.compile("s3" + "://", re.IGNORECASE),
    }
    suffixes = {".md", ".txt", ".json", ".py", ".yml", ".yaml"}

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        content = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            require(not pattern.search(content), f"possible {label} in {path.relative_to(ROOT)}")


def main() -> None:
    validate_prompt()
    validate_faq()
    validate_tests()
    scan_public_text()
    print("PASS: prompt, FAQ, tests, and public-text secret scan")


if __name__ == "__main__":
    main()
