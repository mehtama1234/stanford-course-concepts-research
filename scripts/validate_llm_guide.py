#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "analysis/llms/lecture-guide.json"
APPROACHES = ROOT / "analysis/llms/lecture-approaches.json"
TRANSCRIPT_INDEX = ROOT / "raw-material/youtube/transcript-index.json"
SITE_PAGE = ROOT / "site/llms.html"
COURSE = "stanford-cme295-transformers-llms-autumn-2025"

REQUIRED_FIELDS = {
    "number",
    "core_problem",
    "topic_explanation",
    "detail_explanation",
    "core_ideas",
    "discussion_flow",
    "examples",
    "math_algorithm",
    "plain_checkpoint",
    "concepts",
}

VAGUE_PHRASES = {
    "deep dive",
    "unlock",
    "game changer",
    "cutting edge",
    "leverage synergies",
    "robust solution",
    "comprehensive overview",
    "various topics",
    "many things",
}

BLOCKED_VISIBLE_PHRASES = [
    "What The Lecture Covers",
    "How The Lecture Develops",
    "The topic explains",
    "The topic discusses",
    "The topic stresses",
    "The lecture explains",
    "The lecture's",
    "The lecture&#x27;s",
    "This lecture explains",
    "The instructor explains",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(value: str) -> int:
    return len(value.split())


def main() -> int:
    errors: list[str] = []
    for path, label in [(GUIDE, "guide"), (APPROACHES, "approaches"), (TRANSCRIPT_INDEX, "transcript index")]:
        if not path.exists():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    try:
        guide = load_json(GUIDE)
        approaches = load_json(APPROACHES)
        transcript_index = load_json(TRANSCRIPT_INDEX)
    except json.JSONDecodeError as exc:
        print(f"invalid json: {exc}", file=sys.stderr)
        return 1

    if not isinstance(guide, list):
        errors.append("LLM lecture guide must be a list")
        guide = []
    if not isinstance(approaches, list):
        errors.append("LLM lecture approaches must be a list")
        approaches = []

    available = {
        int(record["course_index"])
        for record in transcript_index
        if record.get("course_slug") == COURSE and record.get("transcript_status") == "available"
    }
    expected = set(range(1, 10))
    if available != expected:
        errors.append(f"expected transcript index to contain LLM lectures 1-9, got {sorted(available)}")

    seen: set[int] = set()
    approaches_by_number = {int(record.get("number", -1)): record.get("approaches", []) for record in approaches}
    for i, lecture in enumerate(guide):
        missing = REQUIRED_FIELDS - set(lecture)
        number = lecture.get("number", f"index-{i}")
        if missing:
            errors.append(f"lecture {number} missing fields: {sorted(missing)}")
            continue
        if not isinstance(lecture["number"], int):
            errors.append(f"lecture {number} number must be an int")
            continue
        seen.add(lecture["number"])
        if lecture["number"] not in expected:
            errors.append(f"unexpected LLM lecture number: {lecture['number']}")
        lecture_approaches = approaches_by_number.get(lecture["number"], [])
        if not lecture_approaches:
            errors.append(f"lecture {lecture['number']} has no approaches")
        for approach in lecture_approaches:
            for field in ["name", "problem", "how_it_works", "why_it_matters", "failure_mode"]:
                if not approach.get(field):
                    errors.append(f"lecture {lecture['number']} approach missing {field}")
            if words(approach.get("how_it_works", "")) < 12:
                errors.append(f"lecture {lecture['number']} approach {approach.get('name')} has thin how_it_works")
        if words(lecture["core_problem"]) < 16:
            errors.append(f"lecture {lecture['number']} core_problem is too thin")
        if words(lecture["topic_explanation"]) < 75:
            errors.append(f"lecture {lecture['number']} topic_explanation is too thin")
        if words(lecture["detail_explanation"]) < 65:
            errors.append(f"lecture {lecture['number']} detail_explanation is too thin")
        if len(lecture["core_ideas"]) < 4:
            errors.append(f"lecture {lecture['number']} needs at least 4 core ideas")
        if len(lecture["discussion_flow"]) < 6:
            errors.append(f"lecture {lecture['number']} needs at least 6 discussion_flow items")
        if len(lecture["examples"]) < 2:
            errors.append(f"lecture {lecture['number']} needs at least 2 concrete examples")
        if len(lecture["math_algorithm"]) < 4:
            errors.append(f"lecture {lecture['number']} needs at least 4 math_algorithm items")
        if words(lecture["plain_checkpoint"]) < 15:
            errors.append(f"lecture {lecture['number']} plain_checkpoint is too thin")
        joined = " ".join(
            [
                lecture["core_problem"],
                lecture["topic_explanation"],
                lecture["detail_explanation"],
                lecture["plain_checkpoint"],
            ]
            + lecture["core_ideas"]
            + lecture["discussion_flow"]
            + lecture["examples"]
            + lecture["math_algorithm"]
        ).lower()
        for phrase in VAGUE_PHRASES:
            if phrase in joined:
                errors.append(f"lecture {lecture['number']} contains vague phrase: {phrase}")

    if seen != expected:
        errors.append(f"LLM guide must contain exactly lectures 1-9, got {sorted(seen)}")

    if SITE_PAGE.exists():
        html = SITE_PAGE.read_text(encoding="utf-8")
        for number in expected:
            if f'id="lecture-{number}"' not in html:
                errors.append(f"site page missing lecture anchor: lecture-{number}")
        required_sections = [
            "Big Picture From First Principles",
            "How The Ideas Build",
            "Detailed Topic Explanation",
            "Core Ideas",
            "Approaches Taught",
            "Examples Used",
            "Equations And Algorithm Moves",
            "What You Should Be Able To Say",
            "Transcript Evidence",
        ]
        for section in required_sections:
            if section not in html:
                errors.append(f"site page missing section: {section}")
        for phrase in BLOCKED_VISIBLE_PHRASES:
            if phrase in html:
                errors.append(f"site page still contains lecture-report wording: {phrase}")
    else:
        errors.append("site/llms.html missing; run scripts/build_site.py")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated LLM lecture guide: 9 transcript-backed lecture entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
