#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPORT = ROOT / "analysis/audits/editorial-quality-report.md"

CONCEPT_FIELDS = [
    "everyday_problem",
    "first_principles_reason",
    "mathematical_principle",
    "why_it_matters",
    "what_breaks_without_it",
    "naive_problem",
    "failed_simple_approach",
    "mathematical_object",
    "operation",
    "worked_mini_example",
    "lecture_emphasis",
    "common_misunderstanding",
    "recognize_in_new_work",
    "cross_course_connections",
]

REQUIRED_CONCEPT_HEADINGS = [
    "What real-world problem is this about?",
    "Why does this problem exist?",
    "What is the mathematical idea underneath?",
    "Why is this concept important?",
    "What breaks without it?",
    "Worked Mini-Example",
    "Common Misunderstanding",
    "How to Recognize This in a New Paper or Model",
    "Transcript Evidence",
]

GENERIC_PHRASES = [
    "this improves performance",
    "this is important because it is useful",
    "as vocabulary to memorize",
    "course-level support",
    "generated_transcript_cue_needs_review",
    "lorem ipsum",
    "todo",
    "placeholder",
]


def words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def main() -> int:
    errors: list[str] = []
    concepts = json.loads((ROOT / "analysis/concepts/concept-atlas.json").read_text(encoding="utf-8"))
    themes = json.loads((ROOT / "analysis/themes/theme-map.json").read_text(encoding="utf-8"))
    subthemes = json.loads((ROOT / "analysis/themes/subtheme-map.json").read_text(encoding="utf-8"))
    primitives = json.loads((ROOT / "analysis/throughlines/primitives.json").read_text(encoding="utf-8"))
    families = json.loads((ROOT / "analysis/throughlines/method-families.json").read_text(encoding="utf-8"))
    evidence = json.loads((ROOT / "analysis/evidence/evidence-ledger.json").read_text(encoding="utf-8"))

    evidence_by_concept = {}
    for record in evidence:
        for concept_id in record.get("supports_concepts", []):
            evidence_by_concept.setdefault(concept_id, []).append(record["id"])

    concept_rows = []
    for concept in concepts:
        concept_text = " ".join(str(concept.get(field, "")) for field in CONCEPT_FIELDS)
        count = words(concept_text)
        evidence_count = len(evidence_by_concept.get(concept["id"], []))
        path = SITE / "concepts" / f"{concept['id']}.html"
        html = path.read_text(encoding="utf-8") if path.exists() else ""
        if count < 450:
            errors.append(f"concept {concept['id']} has low editorial depth: {count} words")
        if evidence_count < 2:
            errors.append(f"concept {concept['id']} has fewer than 2 reviewed evidence records")
        for heading in REQUIRED_CONCEPT_HEADINGS:
            if heading not in html:
                errors.append(f"concept page {concept['id']} missing heading: {heading}")
        if "learning-diagram concept-flow" not in html:
            errors.append(f"concept page {concept['id']} missing learning diagram")
        concept_rows.append((concept["id"], count, evidence_count))

    site_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in SITE.rglob("*.html"))
    lowered = site_text.lower()
    for phrase in GENERIC_PHRASES:
        if phrase in lowered:
            errors.append(f"published site contains generic or forbidden phrase: {phrase}")

    theme_words = [
        words(
            " ".join(
                str(theme.get(field, ""))
                for field in ["cross_course_argument", "mathematical_spine", "where_analogy_breaks", "lecture_evidence_chain"]
            )
        )
        for theme in themes
    ]
    subtheme_words = [
        words(
            " ".join(
                str(subtheme.get(field, ""))
                for field in [
                    "first_principles_walkthrough",
                    "mathematical_object_in_plain_language",
                    "cross_links_and_limits",
                    "lecture_evidence_chain",
                    "recognize_in_new_work",
                ]
            )
        )
        for subtheme in subthemes
    ]
    primitive_words = [
        words(
            " ".join(
                str(primitive.get(field, ""))
                for field in ["everyday_setup", "formal_object", "symbol_explanation", "course_appearances", "misuse_failure"]
            )
        )
        for primitive in primitives
    ]
    family_words = [
        words(
            " ".join(
                str(family.get(field, ""))
                for field in [
                    "family_walkthrough",
                    "representative_methods",
                    "where_analogy_breaks",
                    "lecture_evidence_chain",
                    "paper_family_treatment",
                ]
            )
        )
        for family in families
    ]

    lines = [
        "# Editorial Quality Report",
        "",
        "This audit is a static editorial pass over the generated research artifacts and reader-facing HTML. It is not a substitute for a human visual browser review, but it catches shallow pages, missing teaching sections, generic phrases, and missing reviewed evidence.",
        "",
        "## Summary",
        "",
        f"- Concepts audited: {len(concepts)}",
        f"- Concept teaching words: min {min(row[1] for row in concept_rows)}, max {max(row[1] for row in concept_rows)}",
        f"- Reviewed evidence per concept: min {min(row[2] for row in concept_rows)}, max {max(row[2] for row in concept_rows)}",
        f"- Theme treatment words: min {min(theme_words)}, max {max(theme_words)}",
        f"- Subtheme treatment words: min {min(subtheme_words)}, max {max(subtheme_words)}",
        f"- Primitive treatment words: min {min(primitive_words)}, max {max(primitive_words)}",
        f"- Method-family treatment words: min {min(family_words)}, max {max(family_words)}",
        f"- Errors: {len(errors)}",
        "",
        "## Lowest Concept Depth",
        "",
    ]
    for concept_id, count, evidence_count in sorted(concept_rows, key=lambda row: row[1])[:10]:
        lines.append(f"- {concept_id}: {count} teaching words, {evidence_count} reviewed evidence records")
    lines.extend(["", "## Errors", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- None")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"audited editorial quality for {len(concepts)} concept pages; errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
