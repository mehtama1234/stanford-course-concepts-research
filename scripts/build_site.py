#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def load_json(path: str) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return value.strip("-")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def page(title: str, body: str, active: str = "", depth: int = 0) -> str:
    prefix = "../" * depth
    nav = [
        ("index.html", "Overview", "overview"),
        ("concepts.html", "Concepts", "concepts"),
        ("themes.html", "Themes", "themes"),
        ("families.html", "Method Families", "families"),
        ("primitives.html", "Primitives", "primitives"),
        ("evidence.html", "Evidence", "evidence"),
    ]
    nav_html = "\n".join(
        f'<a class="{"active" if key == active else ""}" href="{prefix}{href}">{label}</a>' for href, label, key in nav
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Stanford AI Concept Lab</title>
  <link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{prefix}index.html">Stanford AI Concept Lab</a>
    <nav>{nav_html}</nav>
  </header>
  <main>{body}</main>
</body>
</html>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def evidence_lookup(evidence: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {record["id"]: record for record in evidence}


def concept_card(concept: dict[str, Any], evidence_by_id: dict[str, dict[str, Any]]) -> str:
    ev_items = []
    for ev_id in concept["course_evidence_ids"][:3]:
        ev = evidence_by_id[ev_id]
        when = f' <span class="time">{esc(ev["timestamp_start"])}</span>' if ev.get("timestamp_start") else ""
        ev_items.append(
            f'<li><a href="evidence.html#{esc(ev_id)}">{esc(ev_id)}</a>{when}: {esc(ev["video_title"])}</li>'
        )
    return f"""
<article class="concept-card" id="{esc(concept['id'])}">
  <div class="eyebrow">{esc(concept['theme_id']).replace('_', ' ')}</div>
  <h3><a href="concepts/{esc(concept['id'])}.html">{esc(concept['name'])}</a></h3>
  <p class="definition">{esc(concept['plain_language_definition'])}</p>
  <dl>
    <dt>Everyday Problem</dt><dd>{esc(concept['everyday_problem'])}</dd>
    <dt>First-Principles Reason</dt><dd>{esc(concept['first_principles_reason'])}</dd>
    <dt>Math Underneath</dt><dd>{esc(concept['mathematical_principle'])}</dd>
  </dl>
  <ul class="evidence-list">{''.join(ev_items)}</ul>
</article>
"""


def build_index(concepts: list[dict[str, Any]], themes: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> None:
    total_evidence = len(evidence)
    body = f"""
<section class="hero">
  <div>
    <p class="eyebrow">Transcript-backed first-principles research</p>
    <h1>Understand transformers, reinforcement learning, diffusion, and large vision models from the same small set of ideas.</h1>
    <p class="lead">This lab turns 36 Stanford course transcripts into a connected concept atlas. It starts with ordinary problems, then introduces the math only when the idea needs it.</p>
  </div>
  <aside class="stats">
    <strong>{len(concepts)}</strong><span>concepts</span>
    <strong>{len(themes)}</strong><span>themes</span>
    <strong>{total_evidence}</strong><span>evidence records</span>
  </aside>
</section>
<section>
  <h2>The Big Throughline</h2>
  <p>Modern AI systems repeatedly solve the same deeper problems: compress what matters, decide which information deserves attention, assign credit across time, move through possible outputs, learn from feedback, and measure behavior without confusing the score for the whole truth.</p>
</section>
<section>
  <h2>Course Contributions</h2>
  <div class="three">
    <article><h3>CME295</h3><p>Language models, tokens, attention, training, tuning, reasoning, agents, and evaluation.</p></article>
    <article><h3>CS224R</h3><p>Action, reward, delayed feedback, policy learning, exploration, offline RL, planning, robotics, and RL for LLMs.</p></article>
    <article><h3>CME296</h3><p>Diffusion, score matching, flow matching, guidance, latent spaces, large vision architectures, training, and evaluation.</p></article>
  </div>
</section>
<section>
  <h2>Start With The Concepts</h2>
  <div class="grid">{''.join(concept_card(c, evidence_lookup(evidence)) for c in concepts[:6])}</div>
  <p><a class="button" href="concepts.html">Open the full concept atlas</a></p>
</section>
"""
    write(SITE / "index.html", page("Overview", body, "overview"))


def build_concepts(concepts: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> None:
    ev_by_id = evidence_lookup(evidence)
    concept_ids = {concept["id"] for concept in concepts}
    body = f"""
<section class="page-head">
  <h1>Concept Atlas</h1>
  <p>Each concept starts from the real-world problem, then explains the deeper constraint, the mathematical lever, why it matters, what breaks without it, and where the transcript evidence comes from.</p>
</section>
<section class="grid">{''.join(concept_card(c, ev_by_id) for c in concepts)}</section>
"""
    write(SITE / "concepts.html", page("Concepts", body, "concepts"))

    for concept in concepts:
        evidence_rows = [ev_by_id[ev_id] for ev_id in concept["course_evidence_ids"]]
        related = " ".join(
            f'<a class="chip" href="{esc(r)}.html">{esc(r).replace("_", " ")}</a>'
            if r in concept_ids
            else f'<span class="chip muted-chip">{esc(r).replace("_", " ")}</span>'
            for r in concept["related_concepts"]
        )
        ev_html = "\n".join(evidence_row(ev, "../") for ev in evidence_rows)
        body = f"""
<section class="page-head">
  <p class="eyebrow">{esc(concept['theme_id']).replace('_', ' ')}</p>
  <h1>{esc(concept['name'])}</h1>
  <p>{esc(concept['plain_language_definition'])}</p>
</section>
<section class="treatment">
  <h2>What real-world problem is this about?</h2>
  <p>{esc(concept['everyday_problem'])}</p>
  <h2>Why does this problem exist?</h2>
  <p>{esc(concept['first_principles_reason'])}</p>
  <h2>What is the mathematical idea underneath?</h2>
  <p>{esc(concept['mathematical_principle'])}</p>
  <h2>Why is this concept important?</h2>
  <p>{esc(concept['why_it_matters'])}</p>
  <h2>What breaks without it?</h2>
  <p>{esc(concept['what_breaks_without_it'])}</p>
  <h2>Naive Starting Point</h2>
  <p>{esc(concept['naive_problem'])}</p>
  <h2>Why the Simple Approach Fails</h2>
  <p>{esc(concept['failed_simple_approach'])}</p>
  <h2>The Mathematical Object</h2>
  <p>{esc(concept['mathematical_object'])}</p>
  <h2>The Operation</h2>
  <p>{esc(concept['operation'])}</p>
  <h2>Worked Mini-Example</h2>
  <p>{esc(concept['worked_mini_example'])}</p>
  <h2>What the Lectures Emphasize</h2>
  <p>{esc(concept['lecture_emphasis'])}</p>
  <h2>Common Misunderstanding</h2>
  <p>{esc(concept['common_misunderstanding'])}</p>
  <h2>How to Recognize This in a New Paper or Model</h2>
  <p>{esc(concept['recognize_in_new_work'])}</p>
  <h2>Connected Concepts</h2>
  <p>{esc(concept['cross_course_connections'])}</p>
  <p class="chips">{related}</p>
</section>
<section>
  <h2>Transcript Evidence</h2>
  <div class="evidence-stack">{ev_html}</div>
</section>
"""
        write(SITE / "concepts" / f"{concept['id']}.html", page(concept["name"], body, "concepts", depth=1))


def evidence_row(ev: dict[str, Any], link_prefix: str = "") -> str:
    timestamp = ev.get("timestamp_start") or "timestamp unavailable"
    terms = ", ".join(ev.get("matched_terms", []))
    evidence_id = esc(ev["id"])
    return f"""
<article class="evidence" id="{evidence_id}">
  <h3><a href="{link_prefix}evidence.html#{evidence_id}">{evidence_id}</a></h3>
  <p><strong>{esc(ev['video_title'])}</strong></p>
  <p class="meta">{esc(ev['course'])} · {esc(timestamp)} · {esc(ev['confidence'])}</p>
  <p>{esc(ev['paraphrased_claim'])}</p>
  <dl>
    <dt>Lecture Argument</dt><dd>{esc(ev.get('lecture_argument', ''))}</dd>
    <dt>Example Or Analogy</dt><dd>{esc(ev.get('example_or_analogy', ''))}</dd>
    <dt>Mathematical Claim</dt><dd>{esc(ev.get('mathematical_claim', ''))}</dd>
    <dt>Caveat Or Warning</dt><dd>{esc(ev.get('caveat_or_warning', ''))}</dd>
    <dt>Why This Span Matters</dt><dd>{esc(ev.get('why_span_matters', ''))}</dd>
  </dl>
  <p class="meta">Matched terms: {esc(terms)} · Basis: {esc(ev['evidence_basis'])}</p>
  <p><code>{esc(ev['transcript_path'])}</code></p>
</article>
"""


def build_themes(themes: list[dict[str, Any]], subthemes: list[dict[str, Any]], concepts: list[dict[str, Any]]) -> None:
    concept_by_id = {c["id"]: c for c in concepts}
    subs_by_theme: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for subtheme in subthemes:
        subs_by_theme[subtheme["parent_theme"]].append(subtheme)
    sections = []
    for theme in themes:
        sub_html = []
        for sub in subs_by_theme[theme["id"]]:
            concept_links = " ".join(
                f'<a class="chip" href="concepts/{esc(cid)}.html">{esc(concept_by_id[cid]["name"])}</a>'
                for cid in sub["concepts"]
            )
            sub_html.append(
                f"""
<article class="wide-card" id="{esc(sub['id'])}">
  <h3>{esc(sub['name'])}</h3>
  <p>{esc(sub['everyday_problem'])}</p>
  <dl>
    <dt>Hidden Principle</dt><dd>{esc(sub['hidden_principle'])}</dd>
    <dt>Mathematical Lever</dt><dd>{esc(sub['mathematical_lever'])}</dd>
    <dt>Why It Matters</dt><dd>{esc(sub['why_it_matters'])}</dd>
  </dl>
  <p class="chips">{concept_links}</p>
</article>
"""
            )
        sections.append(
            f"""
<section class="theme" id="{esc(theme['id'])}">
  <h2>{esc(theme['name'])}</h2>
  <p>{esc(theme['big_picture'])}</p>
  <p><strong>Why it matters:</strong> {esc(theme['why_this_theme_matters'])}</p>
  <div class="stack">{''.join(sub_html)}</div>
</section>
"""
        )
    body = '<section class="page-head"><h1>Themes And Subthemes</h1><p>The themes group concepts by the deeper problem they solve, not by lecture order.</p></section>' + "\n".join(sections)
    write(SITE / "themes.html", page("Themes", body, "themes"))


def build_families(families: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> None:
    ev_by_id = evidence_lookup(evidence)
    cards = []
    for family in families:
        ev_links = " ".join(f'<a class="chip" href="evidence.html#{esc(ev_id)}">{esc(ev_id)}</a>' for ev_id in family["course_evidence_ids"][:6])
        cards.append(
            f"""
<article class="wide-card" id="{esc(family['id'])}">
  <h2>{esc(family['name'])}</h2>
  <dl>
    <dt>First-Principles Problem</dt><dd>{esc(family['first_principles_problem'])}</dd>
    <dt>Core Move</dt><dd>{esc(family['core_move'])}</dd>
    <dt>Plain-Language Family Summary</dt><dd>{esc(family['plain_language_family_summary'])}</dd>
  </dl>
  <p class="chips">{ev_links}</p>
</article>
"""
        )
    body = '<section class="page-head"><h1>Method Families</h1><p>These are paper and method families framed by the problem they solve, not by name-dropping.</p></section>' + "".join(cards)
    write(SITE / "families.html", page("Method Families", body, "families"))


def build_primitives(primitives: list[dict[str, Any]]) -> None:
    cards = []
    for primitive in primitives:
        concepts = ", ".join(c.replace("_", " ") for c in primitive["concepts_in_atlas"])
        cards.append(
            f"""
<article class="wide-card" id="{esc(primitive['id'])}">
  <h2>{esc(primitive['name'])}</h2>
  <p>{esc(primitive['plain_language'])}</p>
  <p><strong>Why it exists:</strong> {esc(primitive['why_it_exists'])}</p>
  <p class="meta">Concepts: {esc(concepts)}</p>
</article>
"""
        )
    body = '<section class="page-head"><h1>Mathematical Primitives</h1><p>The same small patterns recur across transformers, RL, diffusion, and vision.</p></section>' + "".join(cards)
    write(SITE / "primitives.html", page("Primitives", body, "primitives"))


def build_evidence(evidence: list[dict[str, Any]]) -> None:
    body = '<section class="page-head"><h1>Evidence Ledger</h1><p>Transcript evidence is kept separate from synthesis. Notes are paraphrased and scoped.</p></section><section class="evidence-stack">' + "".join(evidence_row(ev) for ev in evidence) + "</section>"
    write(SITE / "evidence.html", page("Evidence", body, "evidence"))


def build_assets() -> None:
    css = """
:root {
  --bg: #f7f7f4;
  --ink: #1f2328;
  --muted: #5c6470;
  --line: #d9d7cf;
  --accent: #0f766e;
  --accent-dark: #115e59;
  --panel: #ffffff;
  --soft: #eef5f3;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--ink); line-height: 1.55; }
a { color: var(--accent-dark); }
.topbar { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 14px 28px; border-bottom: 1px solid var(--line); background: rgba(247,247,244,.94); backdrop-filter: blur(10px); }
.brand { font-weight: 800; text-decoration: none; color: var(--ink); }
nav { display: flex; flex-wrap: wrap; gap: 8px; }
nav a { padding: 7px 9px; text-decoration: none; border-radius: 6px; color: var(--muted); font-size: 14px; }
nav a.active, nav a:hover { background: var(--soft); color: var(--accent-dark); }
main { max-width: 1180px; margin: 0 auto; padding: 28px; }
.hero { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 36px; align-items: end; min-height: 420px; padding: 60px 0 48px; border-bottom: 1px solid var(--line); }
h1 { font-size: clamp(36px, 7vw, 76px); line-height: .96; letter-spacing: 0; margin: 0 0 20px; }
h2 { font-size: 28px; margin: 34px 0 12px; }
h3 { font-size: 20px; margin: 0 0 10px; }
.lead { font-size: 20px; max-width: 780px; color: var(--muted); }
.eyebrow, .meta { color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: 0; }
.stats { display: grid; grid-template-columns: 1fr; gap: 2px; border-left: 4px solid var(--accent); padding-left: 18px; }
.stats strong { font-size: 44px; line-height: 1; }
.stats span { color: var(--muted); margin-bottom: 14px; }
.three, .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
article, .concept-card, .wide-card, .evidence { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }
.concept-card h3 a { text-decoration: none; color: var(--ink); }
.definition { font-weight: 700; }
dl { display: grid; gap: 8px; margin: 14px 0; }
dt { font-weight: 800; }
dd { margin: 0; color: var(--muted); }
.stack, .evidence-stack { display: grid; gap: 14px; }
.wide-card { margin: 14px 0; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip, .button { display: inline-flex; align-items: center; min-height: 32px; padding: 6px 10px; border-radius: 6px; background: var(--soft); color: var(--accent-dark); text-decoration: none; font-size: 14px; }
.button { background: var(--accent); color: white; }
.evidence-list { padding-left: 18px; color: var(--muted); }
.time { color: var(--accent-dark); font-weight: 700; }
code { white-space: normal; overflow-wrap: anywhere; color: #374151; }
.page-head { max-width: 820px; padding: 26px 0 18px; }
.page-head h1 { font-size: clamp(34px, 5vw, 58px); }
.treatment { max-width: 860px; }
@media (max-width: 820px) {
  .topbar { align-items: flex-start; flex-direction: column; padding: 12px 18px; }
  main { padding: 18px; }
  .hero, .three, .grid { grid-template-columns: 1fr; }
  .hero { min-height: 0; padding-top: 32px; }
}
"""
    write(SITE / "assets/styles.css", css)


def main() -> None:
    concepts = load_json("analysis/concepts/concept-atlas.json")
    themes = load_json("analysis/themes/theme-map.json")
    subthemes = load_json("analysis/themes/subtheme-map.json")
    evidence = load_json("analysis/evidence/evidence-ledger.json")
    primitives = load_json("analysis/throughlines/primitives.json")
    families = load_json("analysis/throughlines/method-families.json")
    build_assets()
    build_index(concepts, themes, evidence)
    build_concepts(concepts, evidence)
    build_themes(themes, subthemes, concepts)
    build_families(families, evidence)
    build_primitives(primitives)
    build_evidence(evidence)


if __name__ == "__main__":
    main()
