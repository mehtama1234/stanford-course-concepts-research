#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "concepts": ROOT / "analysis/concepts/concept-atlas.json",
    "themes": ROOT / "analysis/themes/theme-map.json",
    "subthemes": ROOT / "analysis/themes/subtheme-map.json",
    "evidence": ROOT / "analysis/evidence/evidence-ledger.json",
    "primitives": ROOT / "analysis/throughlines/primitives.json",
    "method_families": ROOT / "analysis/throughlines/method-families.json",
}

REQUIRED_CONCEPT_FIELDS = {
    "id",
    "name",
    "plain_language_definition",
    "everyday_problem",
    "first_principles_reason",
    "mathematical_principle",
    "why_it_matters",
    "what_breaks_without_it",
    "related_concepts",
    "course_evidence_ids",
    "naive_problem",
    "failed_simple_approach",
    "mathematical_object",
    "operation",
    "worked_mini_example",
    "lecture_emphasis",
    "common_misunderstanding",
    "cross_course_connections",
    "recognize_in_new_work",
}

JARGON_START = re.compile(
    r"^(optimiz|latent|policy|diffusion|attention|representation|benchmark|causal|gradient|transformer)\b",
    re.I,
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def walk_empty(obj: Any, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if not nonempty(value) and key not in {"timestamp_start", "timestamp_end", "course_coverage"}:
                errors.append(f"empty field: {path}.{key}")
            walk_empty(value, f"{path}.{key}", errors)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            walk_empty(value, f"{path}[{i}]", errors)


def main() -> int:
    errors: list[str] = []
    data = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue
        try:
            data[name] = load(path)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid json {path}: {exc}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    concepts = data["concepts"]
    themes = data["themes"]
    subthemes = data["subthemes"]
    evidence = data["evidence"]
    primitives = data["primitives"]
    method_families = data["method_families"]

    concept_ids = {c["id"] for c in concepts}
    theme_ids = {t["id"] for t in themes}
    subtheme_ids = {s["id"] for s in subthemes}
    evidence_ids = {e["id"] for e in evidence}

    for i, concept in enumerate(concepts):
        missing = REQUIRED_CONCEPT_FIELDS - set(concept)
        if missing:
            errors.append(f"concept {concept.get('id', i)} missing fields: {sorted(missing)}")
        if not concept.get("course_evidence_ids"):
            errors.append(f"concept {concept['id']} has no evidence")
        for ev_id in concept.get("course_evidence_ids", []):
            if ev_id not in evidence_ids:
                errors.append(f"concept {concept['id']} references missing evidence {ev_id}")
        if JARGON_START.search(concept.get("everyday_problem", "")):
            errors.append(f"concept {concept['id']} starts everyday_problem with jargon")
        if len(concept.get("mathematical_principle", "").split()) < 12:
            errors.append(f"concept {concept['id']} has shallow mathematical_principle")
        deep_words = sum(
            len(str(concept.get(field, "")).split())
            for field in [
                "naive_problem",
                "failed_simple_approach",
                "mathematical_object",
                "operation",
                "worked_mini_example",
                "lecture_emphasis",
                "common_misunderstanding",
                "cross_course_connections",
                "recognize_in_new_work",
            ]
        )
        if deep_words < 220:
            errors.append(f"concept {concept['id']} has shallow deep treatment: {deep_words} words")
        if len(concept.get("worked_mini_example", "").split()) < 35:
            errors.append(f"concept {concept['id']} missing worked mini-example depth")

    for theme in themes:
        if not theme.get("subthemes"):
            errors.append(f"theme {theme['id']} has no subthemes")
        for sub_id in theme.get("subthemes", []):
            if sub_id not in subtheme_ids:
                errors.append(f"theme {theme['id']} references missing subtheme {sub_id}")
        for concept_id in theme.get("core_concepts", []):
            if concept_id not in concept_ids:
                errors.append(f"theme {theme['id']} references missing concept {concept_id}")

    for subtheme in subthemes:
        if subtheme.get("parent_theme") not in theme_ids:
            errors.append(f"subtheme {subtheme['id']} has missing parent theme")
        if not subtheme.get("examples_from_courses"):
            errors.append(f"subtheme {subtheme['id']} has no examples")
        for concept_id in subtheme.get("concepts", []):
            if concept_id not in concept_ids:
                errors.append(f"subtheme {subtheme['id']} references missing concept {concept_id}")

    for ev in evidence:
        transcript_path = ROOT / ev["transcript_path"]
        if not transcript_path.exists():
            errors.append(f"evidence {ev['id']} transcript path missing")
        if ev.get("confidence") not in {"strong", "moderate", "weak"}:
            errors.append(f"evidence {ev['id']} has invalid confidence")
        if not ev.get("matched_terms"):
            errors.append(f"evidence {ev['id']} has no matched_terms")
        if "course-level support" in ev.get("paraphrased_claim", ""):
            errors.append(f"evidence {ev['id']} uses generic evidence wording")
        if not ev.get("evidence_basis"):
            errors.append(f"evidence {ev['id']} has no evidence_basis")
        if not ev.get("evidence_scope"):
            errors.append(f"evidence {ev['id']} has no evidence_scope")
        for field in ["lecture_argument", "example_or_analogy", "mathematical_claim", "caveat_or_warning", "why_span_matters"]:
            if len(str(ev.get(field, "")).split()) < 12:
                errors.append(f"evidence {ev['id']} has shallow {field}")
        if ev.get("confidence") == "strong" and ev.get("keyword_hits", 0) < 20:
            errors.append(f"evidence {ev['id']} has unsupported strong confidence")
        for concept_id in ev.get("supports_concepts", []):
            if concept_id not in concept_ids:
                errors.append(f"evidence {ev['id']} references missing concept {concept_id}")
        for sub_id in ev.get("supports_subthemes", []):
            if sub_id not in subtheme_ids:
                errors.append(f"evidence {ev['id']} references missing subtheme {sub_id}")

    for primitive in primitives:
        if not primitive.get("concepts_in_atlas"):
            errors.append(f"primitive {primitive['id']} is unused")

    for family in method_families:
        if not family.get("course_evidence_ids"):
            errors.append(f"method family {family['id']} has no evidence")
        for concept_id in family.get("concepts", []):
            if concept_id not in concept_ids:
                errors.append(f"method family {family['id']} references missing concept {concept_id}")
        for ev_id in family.get("course_evidence_ids", []):
            if ev_id not in evidence_ids:
                errors.append(f"method family {family['id']} references missing evidence {ev_id}")

    for name, obj in data.items():
        walk_empty(obj, name, errors)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"validated {len(concepts)} concepts, {len(themes)} themes, "
        f"{len(subthemes)} subthemes, {len(evidence)} evidence records, "
        f"{len(primitives)} primitives, {len(method_families)} method families"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
