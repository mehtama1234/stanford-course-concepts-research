#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urldefrag

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def main() -> int:
    errors: list[str] = []
    concepts = json.loads((ROOT / "analysis/concepts/concept-atlas.json").read_text(encoding="utf-8"))
    themes = json.loads((ROOT / "analysis/themes/theme-map.json").read_text(encoding="utf-8"))
    primitives = json.loads((ROOT / "analysis/throughlines/primitives.json").read_text(encoding="utf-8"))
    families = json.loads((ROOT / "analysis/throughlines/method-families.json").read_text(encoding="utf-8"))
    evidence = json.loads((ROOT / "analysis/evidence/evidence-ledger.json").read_text(encoding="utf-8"))
    required = [
        SITE / "index.html",
        SITE / "concepts.html",
        SITE / "themes.html",
        SITE / "families.html",
        SITE / "primitives.html",
        SITE / "evidence.html",
        SITE / "assets/styles.css",
    ]
    required.extend(SITE / "concepts" / f"{concept['id']}.html" for concept in concepts)
    for path in required:
        if not path.exists():
            errors.append(f"missing site file: {path.relative_to(ROOT)}")

    html_files = list(SITE.rglob("*.html"))
    evidence_html = (SITE / "evidence.html").read_text(encoding="utf-8") if (SITE / "evidence.html").exists() else ""
    for ev in evidence:
        if f'id="{ev["id"]}"' not in evidence_html:
            errors.append(f"evidence anchor missing from evidence.html: {ev['id']}")

    for concept in concepts:
        path = SITE / "concepts" / f"{concept['id']}.html"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        if 'class="learning-diagram concept-flow"' not in text:
            errors.append(f"concept page missing concept diagram: {path.relative_to(ROOT)}")
        for label in ["Problem", "Constraint", "Math Handle", "Failure Mode"]:
            if f"<span>{label}</span>" not in text:
                errors.append(f"concept page missing diagram label {label}: {path.relative_to(ROOT)}")

    themes_html = (SITE / "themes.html").read_text(encoding="utf-8") if (SITE / "themes.html").exists() else ""
    if themes_html.count('class="learning-diagram theme-flow"') < len(themes):
        errors.append("themes.html missing theme diagrams")
    families_html = (SITE / "families.html").read_text(encoding="utf-8") if (SITE / "families.html").exists() else ""
    if families_html.count('class="learning-diagram family-flow"') < len(families):
        errors.append("families.html missing family diagrams")
    primitives_html = (SITE / "primitives.html").read_text(encoding="utf-8") if (SITE / "primitives.html").exists() else ""
    if primitives_html.count('class="learning-diagram primitive-flow"') < len(primitives):
        errors.append("primitives.html missing primitive diagrams")

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        if "<main>" not in text or "</main>" not in text:
            errors.append(f"missing main element: {path.relative_to(ROOT)}")
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            href_path, frag = urldefrag(href)
            target = (path.parent / href_path).resolve() if href_path else path.resolve()
            try:
                target.relative_to(SITE.resolve())
            except ValueError:
                errors.append(f"link escapes site: {path.relative_to(ROOT)} -> {href}")
                continue
            if href_path and not target.exists():
                errors.append(f"broken link: {path.relative_to(ROOT)} -> {href}")
            if frag and target.exists() and f'id="{frag}"' not in target.read_text(encoding="utf-8"):
                errors.append(f"missing anchor: {path.relative_to(ROOT)} -> {href}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"validated {len(html_files)} html files and {len(evidence)} evidence anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
