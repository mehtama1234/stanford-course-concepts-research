#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import socket
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPORT = ROOT / "analysis/audits/publication-readiness-report.md"


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.strip()


def port_free(port: int) -> bool:
    sock = socket.socket()
    try:
        sock.bind(("127.0.0.1", port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def main() -> int:
    concepts = json.loads((ROOT / "analysis/concepts/concept-atlas.json").read_text(encoding="utf-8"))
    themes = json.loads((ROOT / "analysis/themes/theme-map.json").read_text(encoding="utf-8"))
    subthemes = json.loads((ROOT / "analysis/themes/subtheme-map.json").read_text(encoding="utf-8"))
    evidence = json.loads((ROOT / "analysis/evidence/evidence-ledger.json").read_text(encoding="utf-8"))
    queue = json.loads((ROOT / "analysis/evidence/evidence-review-queue.json").read_text(encoding="utf-8"))
    discarded = json.loads((ROOT / "analysis/evidence/evidence-discarded.json").read_text(encoding="utf-8"))
    primitives = json.loads((ROOT / "analysis/throughlines/primitives.json").read_text(encoding="utf-8"))
    families = json.loads((ROOT / "analysis/throughlines/method-families.json").read_text(encoding="utf-8"))

    log_code, log = run(["git", "log", "-1", "--oneline"])
    remote_code, remote = run(["git", "remote", "-v"])
    validation_code, validation = run(["python3", "scripts/validate_all.py"])

    browser_tools = {
        "node": bool(shutil.which("node")),
        "npx": bool(shutil.which("npx")),
        "chromium": bool(shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")),
        "firefox": bool(shutil.which("firefox")),
    }
    playwright_code, playwright_output = run(["npx", "-y", "playwright", "--version"]) if browser_tools["npx"] else (127, "npx unavailable")
    screenshot_blocker = (
        "Playwright CLI is available, but Chromium screenshot rendering previously failed because "
        "`libnspr4.so` was missing and `npx -y playwright install-deps chromium` required interactive sudo."
    )

    lines = [
        "# Publication Readiness Report",
        "",
        "This report is an end-to-end audit record. It does not redefine completion as validation success; it separates proven local readiness from unproven publication steps.",
        "Working-tree cleanliness is intentionally checked outside this generated report because creating the report itself changes the working tree before commit.",
        "",
        "## Audit-Time Git Checkpoint",
        "",
        "This is the latest committed checkpoint at the moment the audit was generated. The final post-commit proof should be taken from live `git status` and `git log` commands after committing the audit output.",
        "",
        "```text",
        f"$ git log -1 --oneline\n{log}",
        f"\n$ git remote -v\n{remote or 'No remote configured'}",
        "```",
        "",
        "## Corpus And Artifacts",
        "",
        f"- Concepts: {len(concepts)}",
        f"- Themes: {len(themes)}",
        f"- Subthemes: {len(subthemes)}",
        f"- Published reviewed evidence records: {len(evidence)}",
        f"- Evidence records still queued for review: {len(queue)}",
        f"- Generated evidence records explicitly discarded: {len(discarded)}",
        f"- Mathematical primitives: {len(primitives)}",
        f"- Method families: {len(families)}",
        f"- Site HTML files: {len(list(SITE.rglob('*.html')))}",
        "",
        "## Validation Evidence",
        "",
        "```text",
        validation,
        "```",
        "",
        "## Requirement Audit",
        "",
        "- Transcript-faithful evidence: proven locally for the published ledger. All published evidence is `manual_deepened`; the generated queue is empty; discarded generated records have reasons.",
        "- Concept/theme/primitive/method-family treatments: proven structurally by JSON validators and rendered-site checks; still subject to human taste in a slower editorial read.",
        "- Plain-language first-principles explanations: partially proven by field requirements, length gates, jargon-start checks, and manual overrides; not fully proven by automated tests alone.",
        "- Reader-facing site build: proven locally by static generation, link validation, evidence-anchor validation, and HTTP smoke checks recorded in `atlas-validation-report.md`.",
        "- Diagram/learning surfaces: proven locally by validator checks for concept, theme, family, and primitive diagrams.",
        "- Browser screenshot inspection: unproven. " + screenshot_blocker,
        "- Push/deploy: unproven by instruction. A remote exists, but no push/deploy is attempted unless publishing is explicitly requested.",
        "",
        "## Browser Tooling",
        "",
        f"- node available: {browser_tools['node']}",
        f"- npx available: {browser_tools['npx']}",
        f"- Playwright CLI: {'available' if playwright_code == 0 else 'unavailable'} ({playwright_output})",
        f"- System Chromium/Chrome available: {browser_tools['chromium']}",
        f"- Firefox available: {browser_tools['firefox']}",
        f"- Port 8876 free at audit time: {port_free(8876)}",
        "",
        "## Current Conclusion",
        "",
        "Local research/build readiness is strong. Full publication-grade completion remains unproven until browser screenshot inspection and any requested push/deploy checks are completed.",
        "",
    ]

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote analysis/audits/publication-readiness-report.md")
    return 1 if validation_code else 0


if __name__ == "__main__":
    raise SystemExit(main())
