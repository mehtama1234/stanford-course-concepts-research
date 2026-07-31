#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "analysis/evidence/evidence-ledger.json"
REVIEW_QUEUE = ROOT / "analysis/evidence/evidence-review-queue.json"
REPORT = ROOT / "analysis/audits/evidence-fidelity-report.md"


def main() -> int:
    records = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    review_queue = json.loads(REVIEW_QUEUE.read_text(encoding="utf-8")) if REVIEW_QUEUE.exists() else []
    status_counts = Counter(record.get("evidence_review_status", "missing") for record in records)
    queue_status_counts = Counter(record.get("evidence_review_status", "missing") for record in review_queue)
    confidence_counts = Counter(record.get("confidence", "missing") for record in records)
    basis_counts = Counter(record.get("evidence_basis", "missing") for record in records)
    generated = [record for record in records if record.get("evidence_review_status") != "manual_deepened"]
    generic = [
        record
        for record in records
        if "Use the lecture context as a concrete case" in record.get("example_or_analogy", "")
    ]
    generated_strong = [record for record in generated if record.get("confidence") == "strong"]
    missing_windows = [record for record in records if len(record.get("local_transcript_window", "").split()) < 8]

    lines = [
        "# Evidence Fidelity Report",
        "",
        "This audit separates transcript anchoring from editorially reviewed evidence. A record can have a timestamp and still need manual review if its explanatory payload was generated from local cues rather than hand-selected lecture argument.",
        "",
        "## Counts",
        "",
        f"- Published evidence records: {len(records)}",
        f"- Published manual deepened records: {status_counts.get('manual_deepened', 0)}",
        f"- Published generated records: {status_counts.get('generated_transcript_cue_needs_review', 0)}",
        f"- Unpublished generated transcript-cue records in review queue: {len(review_queue)}",
        f"- Review-queue generated records: {queue_status_counts.get('generated_transcript_cue_needs_review', 0)}",
        f"- Template-style example records still published: {len(generic)}",
        f"- Published generated records incorrectly marked strong: {len(generated_strong)}",
        f"- Published records missing useful local transcript windows: {len(missing_windows)}",
        "",
        "## Confidence Counts",
        "",
    ]
    for key, value in sorted(confidence_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Evidence Basis Counts", ""])
    for key, value in sorted(basis_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Remaining Review Queue", ""])
    for record in review_queue[:80]:
        concept = ", ".join(record.get("supports_concepts", []))
        lines.append(
            f"- {record['id']} ({concept}) — {record['course']} — {record.get('timestamp_start') or 'timestamp unavailable'} — {record.get('confidence')}"
        )
    if len(review_queue) > 80:
        lines.append(f"- ... {len(review_queue) - 80} more generated records")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"audited {len(records)} published evidence records and {len(review_queue)} queued records; "
        f"{status_counts.get('manual_deepened', 0)} manual, "
        f"{status_counts.get('generated_transcript_cue_needs_review', 0)} published generated-needs-review, "
        f"{len(generated_strong)} generated strong"
    )
    return 1 if generated_strong or missing_windows else 0


if __name__ == "__main__":
    raise SystemExit(main())
