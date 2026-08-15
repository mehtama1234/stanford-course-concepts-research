#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "analysis/deep-rl/lecture-guide.json"
APPROACHES = ROOT / "analysis/deep-rl/lecture-approaches.json"
TRANSCRIPT_INDEX = ROOT / "raw-material/youtube/transcript-index.json"
SITE_PAGE = ROOT / "site/deep-rl.html"
COURSE = "stanford-cs224r-deep-rl-spring-2025"

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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def words(value: str) -> int:
    return len(value.split())


def main() -> int:
    errors: list[str] = []
    if not GUIDE.exists():
        errors.append(f"missing guide: {GUIDE.relative_to(ROOT)}")
    if not APPROACHES.exists():
        errors.append(f"missing approaches: {APPROACHES.relative_to(ROOT)}")
    if not TRANSCRIPT_INDEX.exists():
        errors.append(f"missing transcript index: {TRANSCRIPT_INDEX.relative_to(ROOT)}")
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
        errors.append("lecture guide must be a list")
        guide = []
    if not isinstance(approaches, list):
        errors.append("lecture approaches must be a list")
        approaches = []

    available = {
        int(record["course_index"])
        for record in transcript_index
        if record.get("course_slug") == COURSE and record.get("transcript_status") == "available"
    }
    expected = set(range(1, 20))
    if available != expected:
        errors.append(f"expected transcript index to contain lectures/tutorials 1-19, got {sorted(available)}")

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
            errors.append(f"unexpected lecture number: {lecture['number']}")
        lecture_approaches = approaches_by_number.get(lecture["number"], [])
        if not lecture_approaches:
            errors.append(f"lecture {lecture['number']} has no approaches")
        for approach in lecture_approaches:
            for field in ["name", "problem", "how_it_works", "why_it_matters", "failure_mode"]:
                if not approach.get(field):
                    errors.append(f"lecture {lecture['number']} approach missing {field}")
            if words(approach.get("how_it_works", "")) < 12:
                errors.append(f"lecture {lecture['number']} approach {approach.get('name')} has thin how_it_works")
            if words(approach.get("how_it_works", "")) < 30:
                errors.append(f"lecture {lecture['number']} approach {approach.get('name')} needs a more detailed mechanism")
        if words(lecture["core_problem"]) < 18:
            errors.append(f"lecture {lecture['number']} core_problem is too thin")
        if words(lecture["topic_explanation"]) < 80:
            errors.append(f"lecture {lecture['number']} topic_explanation is too thin")
        if words(lecture["topic_explanation"]) < 140:
            errors.append(f"lecture {lecture['number']} topic_explanation needs first-principles depth")
        if words(lecture["detail_explanation"]) < 70:
            errors.append(f"lecture {lecture['number']} detail_explanation is too thin")
        if words(lecture["detail_explanation"]) < 140:
            errors.append(f"lecture {lecture['number']} detail_explanation needs mechanism depth")
        if len(lecture["core_ideas"]) < 4:
            errors.append(f"lecture {lecture['number']} needs at least 4 core ideas")
        for idea in lecture["core_ideas"]:
            if words(idea) < 10:
                errors.append(f"lecture {lecture['number']} has thin core idea")
        if len(lecture["discussion_flow"]) < 6:
            errors.append(f"lecture {lecture['number']} needs at least 6 ordered discussion_flow items")
        if len(lecture["examples"]) < 2:
            errors.append(f"lecture {lecture['number']} needs at least 2 concrete examples")
        if len(lecture["math_algorithm"]) < 4:
            errors.append(f"lecture {lecture['number']} needs at least 4 math_algorithm items")
        if words(" ".join(lecture["math_algorithm"])) < 120:
            errors.append(f"lecture {lecture['number']} math_algorithm needs more concrete equations or algorithm moves")
        if words(lecture["plain_checkpoint"]) < 15:
            errors.append(f"lecture {lecture['number']} plain_checkpoint is too thin")
        total_words = (
            words(lecture["core_problem"])
            + words(lecture["topic_explanation"])
            + words(lecture["detail_explanation"])
            + words(lecture["plain_checkpoint"])
        )
        total_words += sum(words(item) for item in lecture["discussion_flow"])
        total_words += sum(words(item) for item in lecture["core_ideas"])
        total_words += sum(words(item) for item in lecture["examples"])
        total_words += sum(words(item) for item in lecture["math_algorithm"])
        if total_words < 250:
            errors.append(f"lecture {lecture['number']} guide is too shallow: {total_words} words")
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
        for phrase in [
            "the lecture ",
            "the instructor ",
            "what the lecture covers",
            "how the lecture develops",
            "the topic explains",
            "the topic discusses",
            "the topic stresses",
        ]:
            if phrase in joined:
                errors.append(f"lecture {lecture['number']} contains lecture-report wording: {phrase}")

    if seen != expected:
        errors.append(f"guide must contain exactly lectures/tutorials 1-19, got {sorted(seen)}")

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
        blocked_visible_phrases = [
            "What The Lecture Covers",
            "How The Lecture Develops",
            "The topic explains",
            "The topic discusses",
            "The topic stresses",
            "The lecture explains",
            "The lecture's",
            "The lecture ",
            "the lecture ",
            "The lecture&#x27;s",
            "This lecture explains",
            "The instructor explains",
            "This page reads",
            "lecture by lecture",
            "lecture-summary filler",
            "order of topics",
        ]
        for phrase in blocked_visible_phrases:
            if phrase in html:
                errors.append(f"site page still contains lecture-report wording: {phrase}")
    else:
        errors.append("site/deep-rl.html missing; run scripts/build_site.py")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated Deep RL lecture guide: 19 transcript-backed lecture entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
