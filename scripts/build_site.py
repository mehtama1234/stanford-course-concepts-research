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


def topic_copy(value: Any) -> str:
    text = str(value)
    replacements = [
        ("The final lecture steps back from ", "Step back from "),
        ("The final lecture first surveys ", "Survey "),
        ("The lecture starts from ", "Start from "),
        ("The lecture starts with ", "Start with "),
        ("The lecture starts by ", "Start by "),
        ("The lecture begins by ", "Begin by "),
        ("The lecture begins with ", "Begin with "),
        ("The lecture first narrows ", "Narrow "),
        ("The lecture first completes ", "Complete "),
        ("The lecture then shifts to ", "Then move to "),
        ("The lecture then uses ", "Then use "),
        ("The lecture then turns into ", "Then turn this into "),
        ("The lecture turns into ", "Turn this into "),
        ("The lecture studies ", "Study "),
        ("The lecture introduces ", "Introduce "),
        ("The lecture adds ", "Add "),
        ("The lecture focuses on ", "Focus on "),
        ("The lecture moves from ", "Move from "),
        ("The lecture narrows ", "Narrow "),
        ("The lecture finishes ", "Finish "),
        ("The lecture compares ", "Compare "),
        ("The lecture asks ", "Ask "),
        ("The lecture points out ", ""),
        ("This lecture treats ", "Treat "),
        ("This lecture has ", "This topic has "),
        ("This robotics lecture points out ", ""),
        ("The instructor explains ", ""),
        ("The instructor then explains ", "Then "),
        ("The instructor then uses ", "Then use "),
        ("The instructor then develops ", "Then develop "),
        ("The instructor then reframes ", "Then reframe "),
        ("The instructor brings in ", "Then use "),
        ("The instructor emphasizes ", ""),
        ("the instructor explains ", ""),
        ("the instructor then explains ", "then "),
        ("the instructor then uses ", "then use "),
        ("the instructor then develops ", "then develop "),
        ("the instructor then reframes ", "then reframe "),
        ("the instructor brings in ", "then use "),
        ("the instructor emphasizes ", ""),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    direct_rewrites = [
        ("The split between a high-level policy and a low-level policy.", "The useful split is between a high-level policy and a low-level policy."),
        ("the split between a high-level policy and a low-level policy.", "the useful split is between a high-level policy and a low-level policy."),
        ("The lecture's focus on action distributions matters because expert behavior can have branches.", "Action distributions matter because expert behavior can have branches."),
        ("The lecture's methods are different ways to stay close to what the log can justify while still improving beyond plain copying.", "Offline RL methods are different ways to stay close to what the log can justify while still improving beyond plain copying."),
        ("The lecture's RL framing treats each partial solution as a state and each next step as an action.", "The RL framing treats each partial solution as a state and each next step as an action."),
        ("The lecture's planning loop is therefore cautious:", "The planning loop is therefore cautious:"),
        ("The lecture's design questions matter because bad skills or bad switching rules can hide failure.", "Those design choices matter because bad skills or bad switching rules can hide failure."),
        ("The topic's design questions matter because bad skills or bad switching rules can hide failure.", "Those design choices matter because bad skills or bad switching rules can hide failure."),
        ("The topic explains the recursive nature of this estimate.", "The estimate is recursive."),
        ("The topic explains coverage:", "Coverage means:"),
        ("The topic explains why ", "The reason "),
        ("The topic discusses sampling ", "One method is sampling "),
        ("The topic discusses reset policies, backward policies, expert state distributions, and task proposals as ways to make practice continue without human intervention.", "Reset policies, backward policies, expert state distributions, and task proposals are ways to make practice continue without human intervention."),
        ("The topic discusses robustness, adaptation from recent history, and whether explicit terrain maps are needed.", "Robustness, adaptation from recent history, and terrain information decide whether the policy keeps working outside the simulator."),
        ("The topic stresses that ", "The hard part is that "),
        ("The topic also stresses ", ""),
        ("The topic also explains why ", "The reason "),
        ("The guest lecture compares ", "Compare "),
        ("the guest lecture compares ", "compare "),
    ]
    for old, new in direct_rewrites:
        text = text.replace(old, new)
    removable = [
        "The lecture explains ",
        "This lecture explains ",
        "The topic explains ",
        "This topic explains ",
        "The lecture discusses ",
        "This lecture discusses ",
        "The topic discusses ",
        "This topic discusses ",
        "The lecture also explains ",
        "The topic also explains ",
        "The lecture also stresses ",
        "The topic also stresses ",
        "The lecture stresses ",
        "The topic stresses ",
        "The lecture covers ",
        "The topic covers ",
    ]
    for phrase in removable:
        pattern = rf"(^|(?<=[.!?])\s+){re.escape(phrase)}"
        text = re.sub(pattern, lambda match: match.group(1), text)
    text = text.replace("frames the lecture", "frames the method")
    text = text.replace("frame the lecture", "frame the method")
    text = re.sub(
        r"(^|(?<=[.!?])\s+)The [A-Za-z0-9|: &-]+ lecture (opens by|introduces|frames|covers|explains|discusses) ",
        lambda match: match.group(1),
        text,
    )
    for old, new in direct_rewrites:
        text = text.replace(old, new)
    text = re.sub(r"(^|(?<=[.!?])\s+)([a-z])", lambda match: match.group(1) + match.group(2).upper(), text)
    return text


def page(title: str, body: str, active: str = "", depth: int = 0) -> str:
    prefix = "../" * depth
    nav = [
        ("index.html", "Overview", "overview"),
        ("llms.html", "LLMs", "llms"),
        ("deep-rl.html", "Deep RL", "deep_rl"),
        ("diffusion.html", "Diffusion", "diffusion"),
        ("deep-unsupervised.html", "Unsupervised", "deep_unsupervised"),
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
    content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    path.write_text(content, encoding="utf-8")


def evidence_lookup(evidence: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {record["id"]: record for record in evidence}


def flow_diagram(title: str, steps: list[tuple[str, str]], class_name: str = "concept-flow") -> str:
    cards = []
    for label, text in steps:
        cards.append(
            f"""<div class="flow-step">
  <span>{esc(label)}</span>
  <p>{esc(text)}</p>
</div>"""
        )
    return f"""<figure class="learning-diagram {esc(class_name)}">
  <figcaption>{esc(title)}</figcaption>
  <div class="flow-steps">{''.join(cards)}</div>
</figure>"""


def concept_diagram(concept: dict[str, Any]) -> str:
    return flow_diagram(
        "First-Principles Map",
        [
            ("Problem", concept["everyday_problem"]),
            ("Constraint", concept["first_principles_reason"]),
            ("Math Handle", concept["mathematical_object"]),
            ("Failure Mode", concept["what_breaks_without_it"]),
        ],
    )


def theme_diagram(theme: dict[str, Any], subtheme_names: list[str]) -> str:
    return flow_diagram(
        "Cross-Course Map",
        [
            ("CME295", "Language-model machinery: context, prediction, tuning, reasoning, tools, and evaluation."),
            ("CS224R", "Decision machinery: actions, rewards, delayed consequence, policies, planning, and deployment."),
            ("CME296", "Vision-generation machinery: denoising, flow, guidance, latent spaces, training, and visual evaluation."),
            ("Shared Spine", f"{theme['name']} connects through {', '.join(subtheme_names)}."),
        ],
        "theme-flow",
    )


def family_diagram(family: dict[str, Any]) -> str:
    primitives = ", ".join(family["mathematical_primitive"])
    return flow_diagram(
        "Paper-Family Reading Path",
        [
            ("Pressure", family["first_principles_problem"]),
            ("Core Move", family["core_move"]),
            ("Primitive", primitives),
            ("Evidence", family["lecture_evidence_chain"]),
        ],
        "family-flow",
    )


def primitive_diagram(primitive: dict[str, Any]) -> str:
    return flow_diagram(
        "Equation Breakdown",
        [
            ("Why Needed", primitive["why_it_exists"]),
            ("Formal Handle", primitive["formal_object"]),
            ("Relation", primitive["useful_equation"]),
            ("Misuse", primitive["misuse_failure"]),
        ],
        "primitive-flow",
    )


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
{concept_diagram(concept)}
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


DEEP_RL_COURSE = "stanford-cs224r-deep-rl-spring-2025"
DIFFUSION_COURSE = "stanford-cme296-diffusion-large-vision-models-spring-2026"
LLM_COURSE = "stanford-cme295-transformers-llms-autumn-2025"
DEEP_UNSUPERVISED_COURSE = "berkeley-cs294-158-deep-unsupervised-learning-spring-2024"

DEEP_RL_LECTURE_GUIDE: dict[int, dict[str, Any]] = {
    1: {
        "core_problem": "An agent must choose actions before it knows the full result. The lecture sets up that problem: a choice changes the next situation, and the useful score may arrive later.",
        "plain_takeaway": "Deep RL is about learning a rule for acting. The rule is tested by running it, seeing what happens, and changing it so future choices work better.",
        "key_terms": [
            ("agent", "the learner that chooses"),
            ("state", "the situation the learner uses"),
            ("action", "one move the learner can make"),
            ("reward", "the score after a move or after a chain of moves"),
        ],
        "before_next": "Be able to say what the learner sees, what it can do, and what score says the action helped.",
        "concepts": ["policy", "reward", "credit_assignment"],
    },
    2: {
        "core_problem": "Sometimes trial and error is costly. A robot, driver, or assistant may need to start from examples of good behavior instead of learning only by mistakes.",
        "plain_takeaway": "Imitation learning copies actions from examples. The hard part is that small errors can move the learner into situations the examples did not cover.",
        "key_terms": [
            ("demonstration", "an example of what an expert did"),
            ("behavior cloning", "training the learner to copy expert actions"),
            ("distribution shift", "ending up in situations the examples did not show"),
        ],
        "before_next": "Know why copying one step at a time can fail after several steps.",
        "concepts": ["policy", "agents_and_tools", "generalization"],
    },
    3: {
        "core_problem": "The learner has a rule with adjustable numbers, but the score comes after sampled actions. We need a way to push the rule toward actions that led to better scores.",
        "plain_takeaway": "Policy gradient raises the chance of actions that did better than expected and lowers the chance of actions that did worse.",
        "key_terms": [
            ("policy", "the rule that picks action odds"),
            ("gradient", "a direction for changing the rule"),
            ("return", "the total future score from a point"),
        ],
        "before_next": "Understand why the learner must connect a sampled action to the later score before it can update the rule.",
        "concepts": ["policy", "policy_gradient", "credit_assignment"],
    },
    4: {
        "core_problem": "Raw trial scores are noisy. A good action can happen in a bad run, and a bad action can happen in a lucky run.",
        "plain_takeaway": "Actor-critic splits the job. The actor chooses. The critic estimates how good the situation or action is, so updates have a better comparison point.",
        "key_terms": [
            ("actor", "the chooser"),
            ("critic", "the judge that estimates future score"),
            ("baseline", "a normal score used for comparison"),
            ("advantage", "how much better an action was than the comparison point"),
        ],
        "before_next": "Know why a comparison point can make learning less noisy.",
        "concepts": ["policy_gradient", "actor_critic", "credit_assignment"],
    },
    5: {
        "core_problem": "Fresh experience is expensive. The course asks when the learner can reuse old experience instead of throwing it away.",
        "plain_takeaway": "Off-policy actor-critic learns from data made by another rule, but it must correct for the fact that the old rule chose actions with different odds.",
        "key_terms": [
            ("on-policy", "learning from the current rule's own runs"),
            ("off-policy", "learning from runs made by another rule"),
            ("importance weight", "a correction for different action odds"),
        ],
        "before_next": "Be clear about the danger: old data can help, but it can also give a biased picture of what the current rule would do.",
        "concepts": ["policy", "policy_gradient", "actor_critic", "q_learning"],
    },
    6: {
        "core_problem": "Instead of directly learning which action to take, the learner can ask a simpler question: how much future score should I expect if I take this action here?",
        "plain_takeaway": "Q-learning learns action values. After that, choosing can be as simple as picking the action with the highest estimated value.",
        "key_terms": [
            ("Q-value", "estimated future score for one action in one situation"),
            ("Bellman update", "new estimate equals immediate score plus estimated future score"),
            ("bootstrapping", "training an estimate using another estimate"),
        ],
        "before_next": "Understand why using your own estimates as targets can become unstable.",
        "concepts": ["q_learning", "credit_assignment", "exploration", "policy"],
    },
    7: {
        "core_problem": "In some settings the learner cannot try new actions. It only has a fixed log of past experience.",
        "plain_takeaway": "Offline RL must learn from old data without pretending the data covers every action. The central question is what the log actually proves.",
        "key_terms": [
            ("offline data", "stored past experience"),
            ("coverage", "which situations and actions the data actually includes"),
            ("out-of-data action", "an action the learner wants but the log barely supports"),
        ],
        "before_next": "Know why a high estimated value is not trustworthy when the data barely contains that action.",
        "concepts": ["offline_rl", "q_learning", "policy", "actor_critic"],
    },
    8: {
        "core_problem": "The score may not be given by the world. A person may know which behavior is better but not how to write the right reward rule.",
        "plain_takeaway": "Reward learning turns judgments, examples, or preferences into a score that can train the agent.",
        "key_terms": [
            ("reward model", "a learned scorer"),
            ("preference", "a comparison saying which outcome is better"),
            ("mis-specified reward", "a score that rewards the wrong behavior"),
        ],
        "before_next": "Be able to explain why the learned score can be wrong even when the learner optimizes it well.",
        "concepts": ["reward", "offline_rl", "q_learning", "rl_for_llms"],
    },
    9: {
        "core_problem": "Language models already know how to produce text, but we may want to steer answers toward what people prefer.",
        "plain_takeaway": "RL for LLMs uses feedback about answers to change the model's output rule. The action is often the next token or a whole answer.",
        "key_terms": [
            ("language policy", "the model's odds over next words or answers"),
            ("human feedback", "people judging which answer is better"),
            ("alignment", "making useful behavior score higher than unwanted behavior"),
        ],
        "before_next": "Know the difference between predicting text and being trained to produce preferred text.",
        "concepts": ["rl_for_llms", "reward", "fine_tuning", "scaling_laws"],
    },
    10: {
        "core_problem": "For reasoning, the final answer may hide which earlier step helped or hurt. The learner needs feedback across a chain of written steps.",
        "plain_takeaway": "RL for reasoning treats intermediate work as a sequence of choices. The hard part is deciding which step deserves credit for the final answer.",
        "key_terms": [
            ("reasoning trace", "the visible chain of work"),
            ("process feedback", "scoring steps, not only final answers"),
            ("advantage", "how much a choice improved the expected result"),
        ],
        "before_next": "Be able to say why a correct final answer is not enough information to judge every step.",
        "concepts": ["reasoning_traces", "rl_for_llms", "policy_gradient", "actor_critic", "q_learning", "generalization"],
    },
    11: {
        "core_problem": "Real trial and error can be slow or costly. If the learner can predict what will happen, it can plan before acting.",
        "plain_takeaway": "Model-based RL learns or uses a model of consequences, then searches possible actions inside that model.",
        "key_terms": [
            ("world model", "a predictor of next situations"),
            ("planning", "testing possible moves before making one"),
            ("model error", "wrong predictions that lead to bad choices"),
        ],
        "before_next": "Know why planning helps only as much as the prediction model can be trusted.",
        "concepts": ["model_based_rl", "offline_rl", "exploration"],
    },
    12: {
        "core_problem": "A learner may need to handle many tasks, not just one fixed goal.",
        "plain_takeaway": "Multi-task RL tries to share what is common across tasks while still choosing actions for the current task.",
        "key_terms": [
            ("task", "the goal or setting that changes"),
            ("shared policy", "one rule reused across tasks"),
            ("task information", "the clue that tells the learner which goal it is solving now"),
        ],
        "before_next": "Understand why sharing can help when tasks overlap and hurt when the tasks need different behavior.",
        "concepts": ["policy", "model_based_rl", "generalization"],
    },
    13: {
        "core_problem": "A learner may face a new task and need to adapt quickly from little experience.",
        "plain_takeaway": "Meta RL trains the learner so that learning itself becomes faster on new but related tasks.",
        "key_terms": [
            ("meta learning", "learning how to learn faster"),
            ("adaptation", "changing behavior after a small amount of new experience"),
            ("task family", "a set of related problems"),
        ],
        "before_next": "Know the difference between learning one task and learning a way to adapt across tasks.",
        "concepts": ["exploration", "generalization", "transformer_block"],
    },
    14: {
        "core_problem": "The learner cannot know which actions are good if it never tries anything uncertain.",
        "plain_takeaway": "Exploration is the controlled act of trying actions to learn more, even when another action currently looks better.",
        "key_terms": [
            ("exploration", "trying to learn what is unknown"),
            ("exploitation", "using the best-known action"),
            ("uncertainty", "not knowing enough yet to trust an estimate"),
        ],
        "before_next": "Be able to explain why always picking the current best-looking action can trap the learner.",
        "concepts": ["exploration", "q_learning", "model_based_rl"],
    },
    15: {
        "core_problem": "Long tasks are hard if the learner must choose every tiny action from scratch.",
        "plain_takeaway": "Hierarchical RL uses larger actions made from smaller actions. The learner can choose a skill, then let that skill handle details.",
        "key_terms": [
            ("hierarchy", "big choices built from small choices"),
            ("skill", "a reusable action pattern"),
            ("subgoal", "a smaller target inside the larger task"),
        ],
        "before_next": "Know why grouping actions can make long-horizon problems easier, and why bad groups can hide mistakes.",
        "concepts": ["policy", "exploration", "model_based_rl", "attention"],
    },
    16: {
        "core_problem": "Robots act in the physical world, where data is costly and small errors can matter.",
        "plain_takeaway": "RL for robots connects policies to sensors, motors, imitation, simulation, and real deployment.",
        "key_terms": [
            ("embodied agent", "a learner with sensors and physical actions"),
            ("simulation", "a practice world"),
            ("deployment", "running the learned rule in the real world"),
        ],
        "before_next": "Understand why a policy that works in a simulator may fail on real hardware.",
        "concepts": ["agents_and_tools", "evaluation", "policy", "generalization"],
    },
    17: {
        "core_problem": "Robot intelligence needs more than one narrow trained behavior. It needs perception, action, memory, and adaptation to work together.",
        "plain_takeaway": "The lecture points toward systems that combine learned skills and broader models so robots can handle open-ended tasks.",
        "key_terms": [
            ("perception", "turning sensor input into useful state"),
            ("skill reuse", "using an old behavior inside a new task"),
            ("open-ended task", "a task where the exact situation is not fixed in advance"),
        ],
        "before_next": "Know why a robot needs both a way to understand the scene and a way to choose useful actions.",
        "concepts": ["agents_and_tools", "policy", "generalization", "model_based_rl"],
    },
    18: {
        "core_problem": "Frontier systems are judged not only by training scores but by whether they work under new tasks, new users, and real constraints.",
        "plain_takeaway": "The final lecture asks what still blocks reliable agents: measurement, generalization, data, planning, and deployment.",
        "key_terms": [
            ("frontier", "the current edge of what systems can do"),
            ("evaluation", "tests that reveal what works and what fails"),
            ("generalization", "working on cases not seen during training"),
        ],
        "before_next": "Be able to name what evidence would convince you that a learned agent really works outside the training setup.",
        "concepts": ["evaluation", "exploration", "model_based_rl", "generalization"],
    },
    19: {
        "core_problem": "Q-learning has several moving parts, and the tutorial reviews how state value, action value, rewards, and updates fit together.",
        "plain_takeaway": "The review makes the value idea explicit: judge an action by immediate score plus the future score expected after it.",
        "key_terms": [
            ("value function", "estimated future score from a situation"),
            ("action value", "estimated future score after one action"),
            ("discount", "giving later scores less weight than sooner scores"),
        ],
        "before_next": "Be able to write the story of a Q update in words before using the equation.",
        "concepts": ["q_learning", "actor_critic", "model_based_rl", "credit_assignment"],
    },
}


def format_duration(seconds: int | None) -> str:
    if not seconds:
        return "duration unavailable"
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {sec}s"


def lecture_number(record: dict[str, Any]) -> int:
    title = record.get("expected_title", "")
    match = re.search(r"Lecture\s+(\d+)", title)
    if match:
        return int(match.group(1))
    return int(record.get("course_index", 0))


def deep_rl_evidence_by_title(evidence: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_title: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in evidence:
        if ev.get("course") == DEEP_RL_COURSE:
            by_title[ev["video_title"]].append(ev)
    return by_title


def course_evidence_by_title(evidence: list[dict[str, Any]], course_slug: str) -> dict[str, list[dict[str, Any]]]:
    by_title: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in evidence:
        if ev.get("course") == course_slug:
            by_title[ev["video_title"]].append(ev)
    return by_title


def concept_links(concept_ids: list[str], concept_by_id: dict[str, dict[str, Any]]) -> str:
    links = []
    for concept_id in concept_ids:
        concept = concept_by_id.get(concept_id)
        if concept:
            links.append(f'<a class="chip" href="concepts/{esc(concept_id)}.html">{esc(concept["name"])}</a>')
    return " ".join(links)


def deep_rl_big_picture() -> str:
    return """
<section class="wide-card">
  <h2>Big Picture From First Principles</h2>
  <p>Start with one ordinary fact: some problems cannot be solved by labeling one input with one answer. A learner may need to act, wait, see what changed, and then act again. The first action can make the next situation easier or harder. The score may arrive much later. Deep RL is the study of how to improve a learned action rule under those conditions.</p>
  <p>The course keeps rebuilding the same core loop. The learner has a situation, chooses an action, receives new information, and changes its future rule. Every topic in the course exists because one part of that loop is hard.</p>
  <div class="principle-grid">
    <article><h3>Behavior Needs Names</h3><p>Before learning can start, we need names for the learner, the situation, the move, the run through time, the score, and the rule that chooses moves.</p></article>
    <article><h3>Copying Is Not Enough</h3><p>Imitation can start behavior, but copied mistakes move the learner into new situations where the examples may no longer help.</p></article>
    <article><h3>Delayed Scores Need Credit</h3><p>If a reward comes later, the learner must decide which earlier action helped or hurt. Policy gradients, values, advantages, and Q-functions are different tools for this problem.</p></article>
    <article><h3>Old Data Has Limits</h3><p>Offline and off-policy methods reuse past experience, but old data only supports the actions and situations it actually contains.</p></article>
    <article><h3>The Score Can Be Wrong</h3><p>Reward learning and RL for LLMs ask how to train from human judgment, and why a learned score can be gamed if it misses what people meant.</p></article>
    <article><h3>Planning Needs A World Guess</h3><p>Model-based RL learns what happens next so the agent can test actions before taking them. The danger is that a wrong model can make bad actions look good.</p></article>
    <article><h3>Many Tasks Need Reuse</h3><p>Multi-task, goal-conditioned, meta, and hierarchical methods ask how one learner can reuse pieces of behavior across goals, tasks, and long plans.</p></article>
    <article><h3>Real Use Breaks Clean Assumptions</h3><p>Robots, exploration, and deployment remove the clean reset, perfect reward, and narrow test setup. The course ends by asking what evidence would prove the agent really works.</p></article>
  </div>
</section>
<section class="wide-card">
  <h2>How The Ideas Build</h2>
  <ol>
    <li><strong>Lectures 1-2:</strong> define the learning problem and show why expert copying is useful but brittle.</li>
    <li><strong>Lectures 3-6:</strong> build online value and policy learning: policy gradients, actor-critic, off-policy correction, and Q-learning.</li>
    <li><strong>Lectures 7-10:</strong> move to fixed data, learned rewards, and language-model training, where the agent cannot freely explore or the score comes from people.</li>
    <li><strong>Lectures 11-15:</strong> add prediction, reuse, adaptation, exploration, and hierarchy so the agent can plan, solve many tasks, and handle long tasks.</li>
    <li><strong>Lectures 16-18 plus the tutorial:</strong> test the ideas in robotics, frontiers, and a clean Q-learning review where the Bellman idea is visible.</li>
  </ol>
</section>
"""


def deep_rl_lecture_card(
    lecture: dict[str, Any],
    guide: dict[str, Any],
    approaches: list[dict[str, Any]],
    evidence_rows: list[dict[str, Any]],
    concept_by_id: dict[str, dict[str, Any]],
) -> str:
    number = lecture_number(lecture)
    title = lecture.get("expected_title") or lecture.get("title")
    fallback = DEEP_RL_LECTURE_GUIDE.get(number, {})
    guide_concepts = guide.get("concepts", fallback.get("concepts", []))
    examples = guide.get("examples", [])
    math_steps = guide.get("math_algorithm", [])
    core_ideas_html = "".join(f"<li>{esc(topic_copy(item))}</li>" for item in guide.get("core_ideas", []))
    approaches_html = "".join(
        f"""
<article class="approach-card">
  <h4>{esc(approach['name'])}</h4>
  <dl>
    <dt>Problem</dt><dd>{esc(approach['problem'])}</dd>
    <dt>How It Works</dt><dd>{esc(approach['how_it_works'])}</dd>
    <dt>Why It Matters</dt><dd>{esc(approach['why_it_matters'])}</dd>
    <dt>Where It Breaks</dt><dd>{esc(approach['failure_mode'])}</dd>
  </dl>
</article>
"""
        for approach in approaches
    )
    examples_html = "".join(f"<li>{esc(item)}</li>" for item in examples)
    math_html = "".join(f"<li>{esc(item)}</li>" for item in math_steps)
    if evidence_rows:
        evidence_html = "".join(
            f'<li><a href="evidence.html#{esc(ev["id"])}">{esc(ev["id"])}</a> '
            f'<span class="time">{esc(ev.get("timestamp_start") or "time unavailable")}</span>: '
            f'{esc(topic_copy(ev.get("lecture_argument", ev.get("paraphrased_claim", ""))))}</li>'
            for ev in evidence_rows
        )
    else:
        evidence_html = "<li>No reviewed evidence span is attached yet, but the local transcript is available.</li>"
    return f"""
<article class="lecture-card" id="lecture-{number}">
  <div class="lecture-heading">
    <div>
      <p class="eyebrow">Lecture {number}</p>
      <h2>{esc(title)}</h2>
    </div>
    <a class="button" href="{esc(lecture['url'])}">Open video</a>
  </div>
  <p class="meta">{esc(format_duration(lecture.get('duration')))} · {esc(lecture.get('word_count', 'unknown'))} transcript words</p>
  {flow_diagram(
      "Study Path",
      [
          ("Problem", topic_copy(guide["core_problem"])),
          ("Core Idea", "Start with the detailed topic explanation below, then use the examples and algorithm notes."),
          ("Math", "Use the algorithm and equation notes as the minimum technical spine."),
          ("Check", guide["plain_checkpoint"]),
      ],
      "lecture-flow",
  )}
  <section class="lecture-notes">
    <h3>Detailed Topic Explanation</h3>
    <p>{esc(topic_copy(guide.get("topic_explanation", "")))}</p>
    <p>{esc(topic_copy(guide.get("detail_explanation", "")))}</p>
    <h3>Core Ideas</h3>
    <ul>{core_ideas_html}</ul>
    <h3>Approaches Taught</h3>
    <div class="approach-stack">{approaches_html}</div>
    <h3>Examples Used</h3>
    <ul>{examples_html}</ul>
    <h3>Equations And Algorithm Moves</h3>
    <ul>{math_html}</ul>
    <h3>What You Should Be Able To Say</h3>
    <p>{esc(guide["plain_checkpoint"])}</p>
  </section>
  <section class="lecture-links">
    <h3>Linked Concepts</h3>
    <p class="chips">{concept_links(guide_concepts, concept_by_id)}</p>
    <h3>Transcript Evidence</h3>
    <ul class="evidence-list">{evidence_html}</ul>
    <p><code>{esc(lecture["clean_txt"])}</code></p>
  </section>
</article>
"""


def build_deep_rl(
    transcript_index: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    lecture_guides: list[dict[str, Any]] | None = None,
    lecture_approaches: list[dict[str, Any]] | None = None,
) -> None:
    lectures = [
        record
        for record in transcript_index
        if record.get("course_slug") == DEEP_RL_COURSE and record.get("transcript_status") == "available"
    ]
    lectures.sort(key=lambda record: int(record.get("course_index", 0)))
    concept_by_id = {concept["id"]: concept for concept in concepts}
    evidence_by_title = deep_rl_evidence_by_title(evidence)
    guide_by_number = {
        int(guide["number"]): guide
        for guide in (lecture_guides or [])
    } or DEEP_RL_LECTURE_GUIDE
    approaches_by_number = {
        int(record["number"]): record.get("approaches", [])
        for record in (lecture_approaches or [])
    }
    lecture_links = " ".join(
        f'<a class="chip" href="#lecture-{lecture_number(lecture)}">{esc(lecture.get("expected_title", lecture.get("title", "")))}</a>'
        for lecture in lectures
    )
    cards = []
    for lecture in lectures:
        number = lecture_number(lecture)
        guide = guide_by_number.get(number)
        if not guide:
            continue
        cards.append(
            deep_rl_lecture_card(
                lecture,
                guide,
                approaches_by_number.get(number, []),
                evidence_by_title.get(lecture["title"], []),
                concept_by_id,
            )
        )
    body = f"""
<section class="page-head">
  <p class="eyebrow">Stanford CS224R Deep Reinforcement Learning</p>
  <h1>Deep RL Lecture Guide</h1>
  <p>Deep RL studies how a learner improves actions when each move changes what happens next, rewards may arrive late, and the useful training signal has to be extracted from experience.</p>
</section>
<section>
  <h2>Course Spine</h2>
  <p>Deep RL studies a learner that acts, sees what changed, receives a score, and changes its future action rule. The course keeps returning to five hard facts: the score can arrive late, data can be missing, learned scores can be wrong, real trial and error can be costly, and tests can miss behavior that matters.</p>
  <p class="chips">{lecture_links}</p>
</section>
{deep_rl_big_picture()}
<section class="stack">
  {''.join(cards)}
</section>
"""
    write(SITE / "deep-rl.html", page("Deep RL Lecture Guide", body, "deep_rl"))


def diffusion_big_picture() -> str:
    return """
<section class="wide-card">
  <h2>Big Picture From First Principles</h2>
  <p>Start with one ordinary fact: a realistic image is too many choices to make all at once. The model needs a path. Diffusion, score matching, flow matching, latent spaces, guidance, architectures, training, and evaluation are different answers to the same pressure: how do we move from something easy, like random noise, into something structured, like a useful image?</p>
  <p>The course keeps rebuilding one loop. Pick a representation, choose a path through that representation, learn the local direction of improvement, follow that direction to make samples, and then check whether the result is realistic, controlled, diverse, and useful.</p>
  <div class="principle-grid">
    <article><h3>Generation Needs A Path</h3><p>Noise is easy to sample and images are hard to sample. The core problem is learning a reliable route between them.</p></article>
    <article><h3>Small Moves Beat One Leap</h3><p>Diffusion breaks image generation into many cleanup steps, each easier to learn than the full image at once.</p></article>
    <article><h3>Direction Can Replace Probability</h3><p>Score matching learns which way a noisy point should move without writing down the full data probability.</p></article>
    <article><h3>Flow Means Learned Motion</h3><p>Flow matching learns arrows that carry simple samples toward data-like samples.</p></article>
    <article><h3>Compression Saves Work</h3><p>Latent spaces let the model work in a smaller code where important structure remains but raw pixel cost drops.</p></article>
    <article><h3>Guidance Adds Control</h3><p>A generated image must often obey a prompt or condition, so the sampling direction needs a steering signal.</p></article>
    <article><h3>Architecture Carries Information</h3><p>The network must combine local detail, global layout, time, and conditions at every update.</p></article>
    <article><h3>Evaluation Has Many Axes</h3><p>A sample can look good, ignore the prompt, copy data, or fail rare cases, so one score is not enough.</p></article>
  </div>
</section>
<section class="wide-card">
  <h2>How The Ideas Build</h2>
  <ol>
    <li><strong>Lectures 1-3:</strong> build the three main generation views: denoise step by step, follow score directions, and follow a learned flow.</li>
    <li><strong>Lecture 4:</strong> adds practical control and cheaper computation through latent spaces and guidance.</li>
    <li><strong>Lectures 5-6:</strong> turn the ideas into trainable systems: architecture, time inputs, conditioning, losses, schedules, and scale.</li>
    <li><strong>Lecture 7:</strong> asks how to judge outputs when realism, prompt following, safety, diversity, and usefulness disagree.</li>
    <li><strong>Lecture 8:</strong> frames new papers by the bottleneck they attack: speed, video, 3D, control, consistency, or evaluation.</li>
  </ol>
</section>
"""


def diffusion_lecture_card(
    lecture: dict[str, Any],
    guide: dict[str, Any],
    approaches: list[dict[str, Any]],
    evidence_rows: list[dict[str, Any]],
    concept_by_id: dict[str, dict[str, Any]],
) -> str:
    number = lecture_number(lecture)
    title = lecture.get("expected_title") or lecture.get("title")
    guide_concepts = guide.get("concepts", [])
    core_ideas_html = "".join(f"<li>{esc(topic_copy(item))}</li>" for item in guide.get("core_ideas", []))
    approaches_html = "".join(
        f"""
<article class="approach-card">
  <h4>{esc(approach['name'])}</h4>
  <dl>
    <dt>Problem</dt><dd>{esc(approach['problem'])}</dd>
    <dt>How It Works</dt><dd>{esc(approach['how_it_works'])}</dd>
    <dt>Why It Matters</dt><dd>{esc(approach['why_it_matters'])}</dd>
    <dt>Where It Breaks</dt><dd>{esc(approach['failure_mode'])}</dd>
  </dl>
</article>
"""
        for approach in approaches
    )
    examples_html = "".join(f"<li>{esc(item)}</li>" for item in guide.get("examples", []))
    math_html = "".join(f"<li>{esc(item)}</li>" for item in guide.get("math_algorithm", []))
    if evidence_rows:
        evidence_html = "".join(
            f'<li><a href="evidence.html#{esc(ev["id"])}">{esc(ev["id"])}</a> '
            f'<span class="time">{esc(ev.get("timestamp_start") or "time unavailable")}</span>: '
            f'{esc(topic_copy(ev.get("lecture_argument", ev.get("paraphrased_claim", ""))))}</li>'
            for ev in evidence_rows
        )
    else:
        evidence_html = "<li>No reviewed evidence span is attached yet, but the local transcript is available.</li>"
    return f"""
<article class="lecture-card" id="lecture-{number}">
  <div class="lecture-heading">
    <div>
      <p class="eyebrow">Lecture {number}</p>
      <h2>{esc(title)}</h2>
    </div>
    <a class="button" href="{esc(lecture['url'])}">Open video</a>
  </div>
  <p class="meta">{esc(format_duration(lecture.get('duration')))} · {esc(lecture.get('word_count', 'unknown'))} transcript words</p>
  {flow_diagram(
      "Study Path",
      [
          ("Problem", topic_copy(guide["core_problem"])),
          ("Core Idea", "Start with the detailed topic explanation below, then use the approaches and examples."),
          ("Math", "Use the equation and algorithm notes as the minimum technical spine."),
          ("Check", guide["plain_checkpoint"]),
      ],
      "lecture-flow",
  )}
  <section class="lecture-notes">
    <h3>Detailed Topic Explanation</h3>
    <p>{esc(topic_copy(guide.get("topic_explanation", "")))}</p>
    <p>{esc(topic_copy(guide.get("detail_explanation", "")))}</p>
    <h3>Core Ideas</h3>
    <ul>{core_ideas_html}</ul>
    <h3>Approaches Taught</h3>
    <div class="approach-stack">{approaches_html}</div>
    <h3>Examples Used</h3>
    <ul>{examples_html}</ul>
    <h3>Equations And Algorithm Moves</h3>
    <ul>{math_html}</ul>
    <h3>What You Should Be Able To Say</h3>
    <p>{esc(guide["plain_checkpoint"])}</p>
  </section>
  <section class="lecture-links">
    <h3>Linked Concepts</h3>
    <p class="chips">{concept_links(guide_concepts, concept_by_id)}</p>
    <h3>Transcript Evidence</h3>
    <ul class="evidence-list">{evidence_html}</ul>
    <p><code>{esc(lecture["clean_txt"])}</code></p>
  </section>
</article>
"""


def build_diffusion(
    transcript_index: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    lecture_guides: list[dict[str, Any]],
    lecture_approaches: list[dict[str, Any]],
) -> None:
    lectures = [
        record
        for record in transcript_index
        if record.get("course_slug") == DIFFUSION_COURSE and record.get("transcript_status") == "available"
    ]
    lectures.sort(key=lambda record: int(record.get("course_index", 0)))
    concept_by_id = {concept["id"]: concept for concept in concepts}
    evidence_by_title = course_evidence_by_title(evidence, DIFFUSION_COURSE)
    guide_by_number = {int(guide["number"]): guide for guide in lecture_guides}
    approaches_by_number = {
        int(record["number"]): record.get("approaches", [])
        for record in lecture_approaches
    }
    lecture_links = " ".join(
        f'<a class="chip" href="#lecture-{lecture_number(lecture)}">{esc(lecture.get("expected_title", lecture.get("title", "")))}</a>'
        for lecture in lectures
    )
    cards = []
    for lecture in lectures:
        number = lecture_number(lecture)
        guide = guide_by_number.get(number)
        if not guide:
            continue
        cards.append(
            diffusion_lecture_card(
                lecture,
                guide,
                approaches_by_number.get(number, []),
                evidence_by_title.get(lecture["title"], []),
                concept_by_id,
            )
        )
    body = f"""
<section class="page-head">
  <p class="eyebrow">Stanford CME296 Diffusion And Large Vision Models</p>
  <h1>Diffusion Lecture Guide</h1>
  <p>Diffusion and vision generation study how to move from simple noise or compressed codes into structured images, videos, and visual worlds by learning small reliable update directions.</p>
</section>
<section>
  <h2>Course Spine</h2>
  <p>Diffusion and flow models study how to generate structured visual data by moving from something simple to something complex. The course keeps returning to six facts: direct generation is too hard, local directions are learnable, representation changes cost, guidance changes control, architecture changes what information can be used, and evaluation must check several kinds of failure.</p>
  <p class="chips">{lecture_links}</p>
</section>
{diffusion_big_picture()}
<section class="stack">
  {''.join(cards)}
</section>
"""
    write(SITE / "diffusion.html", page("Diffusion Lecture Guide", body, "diffusion"))


def deep_unsupervised_big_picture() -> str:
    return """
<section class="wide-card">
  <h2>Big Picture From First Principles</h2>
  <p>Start with one ordinary fact: most data has no answer key. A pile of images, text, video, molecules, or 3D views does not say what label each example deserves. But the data is not random. It has repeated parts, hidden causes, patterns over time, and rules about what can exist. Deep unsupervised learning asks how a model can use those regularities as its teacher.</p>
  <p>The course keeps rebuilding one problem in different forms: choose what structure to learn, choose how to train from raw examples, choose how to generate or represent new examples, and then check whether the learned structure is useful rather than just memorized.</p>
  <div class="principle-grid">
    <article><h3>Raw Data Still Teaches</h3><p>Labels are missing, but every example contains relations among parts that can become a training signal.</p></article>
    <article><h3>Probability Measures Fit</h3><p>Some methods ask whether the model assigns high probability to real data and low probability elsewhere.</p></article>
    <article><h3>Generation Needs A Route</h3><p>Models make samples by predicting pieces, transforming noise, decoding hidden codes, competing with a judge, or denoising step by step.</p></article>
    <article><h3>Hidden Codes Explain Causes</h3><p>Latent variables compress observations into factors that can help reconstruction, sampling, or downstream tasks.</p></article>
    <article><h3>Good Features Drop Noise</h3><p>Self-supervised learning builds representations that keep stable meaning while ignoring changes that should not matter.</p></article>
    <article><h3>Control Changes The Task</h3><p>Text, class labels, properties, views, or scientific constraints turn random generation into directed generation.</p></article>
    <article><h3>Scale Changes Bottlenecks</h3><p>Large models make simple objectives powerful, but memory, communication, sampling speed, and evaluation become central.</p></article>
    <article><h3>Scores Are Incomplete</h3><p>A model can have good likelihood, sharp samples, useful features, or scientific value; one number rarely captures all of that.</p></article>
  </div>
</section>
<section class="wide-card">
  <h2>How The Ideas Build</h2>
  <ol>
    <li><strong>Lectures 1-3:</strong> set up unlabeled data, then study exact probability through ordered prediction and invertible transformations.</li>
    <li><strong>Lectures 4-6:</strong> move through the main generative families: hidden-code models, adversarial generators, and diffusion models.</li>
    <li><strong>Lectures 7-8:</strong> connect unsupervised objectives to representation learning and large language models.</li>
    <li><strong>Lectures 9-10:</strong> extend the same ideas to video and semi-supervised learning, where time and limited labels add new constraints.</li>
    <li><strong>Lectures 11-13:</strong> apply generative modeling to science, 3D scenes, and multimodal systems where outputs must obey outside structure.</li>
    <li><strong>Lecture 14:</strong> explains the hardware and parallel training moves needed when the models become too large for one machine.</li>
  </ol>
</section>
"""


def build_deep_unsupervised(
    transcript_index: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    lecture_guides: list[dict[str, Any]],
    lecture_approaches: list[dict[str, Any]],
) -> None:
    lectures = [
        record
        for record in transcript_index
        if record.get("course_slug") == DEEP_UNSUPERVISED_COURSE and record.get("transcript_status") == "available"
    ]
    lectures.sort(key=lambda record: int(record.get("course_index", 0)))
    concept_by_id = {concept["id"]: concept for concept in concepts}
    evidence_by_title = course_evidence_by_title(evidence, DEEP_UNSUPERVISED_COURSE)
    guide_by_number = {int(guide["number"]): guide for guide in lecture_guides}
    approaches_by_number = {
        int(record["number"]): record.get("approaches", [])
        for record in lecture_approaches
    }
    lecture_links = " ".join(
        f'<a class="chip" href="#lecture-{lecture_number(lecture)}">{esc(lecture.get("expected_title", lecture.get("title", "")))}</a>'
        for lecture in lectures
    )
    cards = []
    for lecture in lectures:
        number = lecture_number(lecture)
        guide = guide_by_number.get(number)
        if not guide:
            continue
        cards.append(
            diffusion_lecture_card(
                lecture,
                guide,
                approaches_by_number.get(number, []),
                evidence_by_title.get(lecture["title"], []),
                concept_by_id,
            )
        )
    body = f"""
<section class="page-head">
  <p class="eyebrow">UC Berkeley CS294-158 Deep Unsupervised Learning</p>
  <h1>Deep Unsupervised Learning Lecture Guide</h1>
  <p>Deep unsupervised learning studies how raw data can teach a model without ordinary labels by exposing repeated structure, hidden causes, predictable parts, and useful representations.</p>
</section>
<section>
  <h2>Course Spine</h2>
  <p>Deep unsupervised learning studies how a model can learn from raw data when labels are missing, partial, expensive, or not the main point. The course keeps returning to six facts: data has hidden structure, probability can describe that structure, generation needs a route, representations must keep useful factors, control changes what counts as success, and scale creates new engineering limits.</p>
  <p class="chips">{lecture_links}</p>
</section>
{deep_unsupervised_big_picture()}
<section class="stack">
  {''.join(cards)}
</section>
"""
    write(SITE / "deep-unsupervised.html", page("Deep Unsupervised Learning Lecture Guide", body, "deep_unsupervised"))


def llm_big_picture() -> str:
    return """
<section class="wide-card">
  <h2>Big Picture From First Principles</h2>
  <p>Start with one ordinary fact: text is a chain of pieces, and each piece gets its meaning from other pieces around it. Transformers and LLMs are built around that fact. The model turns text into tokens, turns tokens into vectors, lets vectors compare with each other, trains on prediction, then gets tuned and tested for useful behavior.</p>
  <p>The course keeps rebuilding one pipeline: represent the text, mix context with attention, train the model to predict, tune the model toward desired answers, extend it with reasoning or tools, and evaluate whether it actually works.</p>
  <div class="principle-grid">
    <article><h3>Text Needs Pieces</h3><p>Tokenization decides the units the model can see and predict.</p></article>
    <article><h3>Pieces Need Numbers</h3><p>Embeddings turn tokens into vectors that can be compared and changed.</p></article>
    <article><h3>Context Changes Meaning</h3><p>Attention lets each token pull information from other tokens.</p></article>
    <article><h3>Order Must Be Added</h3><p>Position information tells the model where each token sits.</p></article>
    <article><h3>Prediction Teaches Patterns</h3><p>Next-token pretraining teaches grammar, facts, style, and code structure at scale.</p></article>
    <article><h3>Tuning Shapes Behavior</h3><p>Fine-tuning and preference training turn a predictor into a more useful assistant.</p></article>
    <article><h3>Tools Extend The Model</h3><p>Retrieval and tool calls let the system use outside information and actions.</p></article>
    <article><h3>Scores Are Partial</h3><p>Evaluation must check correctness, usefulness, safety, cost, and failure cases.</p></article>
  </div>
</section>
<section class="wide-card">
  <h2>How The Ideas Build</h2>
  <ol>
    <li><strong>Lectures 1-3:</strong> build the transformer and LLM pipeline from tokens, embeddings, attention, order, blocks, and next-token prediction.</li>
    <li><strong>Lectures 4-5:</strong> explain large-scale training and post-training: data, compute, optimization, fine-tuning, and preference tuning.</li>
    <li><strong>Lectures 6-7:</strong> extend the base model into reasoning and agent systems with traces, verifiers, retrieval, and tools.</li>
    <li><strong>Lecture 8:</strong> asks how to measure behavior without confusing benchmark scores for real usefulness.</li>
    <li><strong>Lecture 9:</strong> recaps the full pipeline and shows how to read new trends by finding the bottleneck they change.</li>
  </ol>
</section>
"""


def build_llms(
    transcript_index: list[dict[str, Any]],
    concepts: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    lecture_guides: list[dict[str, Any]],
    lecture_approaches: list[dict[str, Any]],
) -> None:
    lectures = [
        record
        for record in transcript_index
        if record.get("course_slug") == LLM_COURSE and record.get("transcript_status") == "available"
    ]
    lectures.sort(key=lambda record: int(record.get("course_index", 0)))
    concept_by_id = {concept["id"]: concept for concept in concepts}
    evidence_by_title = course_evidence_by_title(evidence, LLM_COURSE)
    guide_by_number = {int(guide["number"]): guide for guide in lecture_guides}
    approaches_by_number = {
        int(record["number"]): record.get("approaches", [])
        for record in lecture_approaches
    }
    lecture_links = " ".join(
        f'<a class="chip" href="#lecture-{lecture_number(lecture)}">{esc(lecture.get("expected_title", lecture.get("title", "")))}</a>'
        for lecture in lectures
    )
    cards = []
    for lecture in lectures:
        number = lecture_number(lecture)
        guide = guide_by_number.get(number)
        if not guide:
            continue
        cards.append(
            diffusion_lecture_card(
                lecture,
                guide,
                approaches_by_number.get(number, []),
                evidence_by_title.get(lecture["title"], []),
                concept_by_id,
            )
        )
    body = f"""
<section class="page-head">
  <p class="eyebrow">Stanford CME295 Transformers And LLMs</p>
  <h1>LLM Lecture Guide</h1>
  <p>Transformers and LLMs study how text becomes tokens and vectors, how attention mixes context, and how prediction, tuning, tools, reasoning, and evaluation shape useful behavior.</p>
</section>
<section>
  <h2>Course Spine</h2>
  <p>Transformers and LLMs study how text becomes vectors, how context is mixed, how prediction becomes pretraining, how tuning changes behavior, and how reasoning, tools, and evaluation turn a raw model into a usable system.</p>
  <p class="chips">{lecture_links}</p>
</section>
{llm_big_picture()}
<section class="stack">
  {''.join(cards)}
</section>
"""
    write(SITE / "llms.html", page("LLM Lecture Guide", body, "llms"))


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
    <dt>Local Transcript Window</dt><dd>{esc(ev.get('local_transcript_window', ''))}</dd>
  </dl>
  <p class="meta">Matched terms: {esc(terms)} · Basis: {esc(ev['evidence_basis'])} · Review: {esc(ev.get('evidence_review_status', 'unknown'))}</p>
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
    <dt>First-Principles Walkthrough</dt><dd>{esc(sub['first_principles_walkthrough'])}</dd>
    <dt>Mathematical Object In Plain Language</dt><dd>{esc(sub['mathematical_object_in_plain_language'])}</dd>
    <dt>Cross-Links And Limits</dt><dd>{esc(sub['cross_links_and_limits'])}</dd>
    <dt>Lecture Evidence Chain</dt><dd>{esc(sub['lecture_evidence_chain'])}</dd>
    <dt>Recognize In New Work</dt><dd>{esc(sub['recognize_in_new_work'])}</dd>
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
  {theme_diagram(theme, [sub['name'] for sub in subs_by_theme[theme['id']]])}
  <dl>
    <dt>Cross-Course Argument</dt><dd>{esc(theme['cross_course_argument'])}</dd>
    <dt>Mathematical Spine</dt><dd>{esc(theme['mathematical_spine'])}</dd>
    <dt>Where The Analogy Breaks</dt><dd>{esc(theme['where_analogy_breaks'])}</dd>
    <dt>Lecture Evidence Chain</dt><dd>{esc(theme['lecture_evidence_chain'])}</dd>
  </dl>
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
  {family_diagram(family)}
  <dl>
    <dt>First-Principles Problem</dt><dd>{esc(family['first_principles_problem'])}</dd>
    <dt>Core Move</dt><dd>{esc(family['core_move'])}</dd>
    <dt>Plain-Language Family Summary</dt><dd>{esc(family['plain_language_family_summary'])}</dd>
    <dt>Family Walkthrough</dt><dd>{esc(family['family_walkthrough'])}</dd>
    <dt>Representative Methods</dt><dd>{esc(family['representative_methods'])}</dd>
    <dt>Where The Analogy Breaks</dt><dd>{esc(family['where_analogy_breaks'])}</dd>
    <dt>Lecture Evidence Chain</dt><dd>{esc(family['lecture_evidence_chain'])}</dd>
    <dt>Paper-Family Treatment</dt><dd>{esc(family['paper_family_treatment'])}</dd>
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
  {primitive_diagram(primitive)}
  <dl>
    <dt>Everyday Setup</dt><dd>{esc(primitive['everyday_setup'])}</dd>
    <dt>Formal Object</dt><dd>{esc(primitive['formal_object'])}</dd>
    <dt>Useful Equation</dt><dd><code>{esc(primitive['useful_equation'])}</code></dd>
    <dt>Symbol Explanation</dt><dd>{esc(primitive['symbol_explanation'])}</dd>
    <dt>Where It Appears</dt><dd>{esc(primitive['course_appearances'])}</dd>
    <dt>Misuse Failure</dt><dd>{esc(primitive['misuse_failure'])}</dd>
  </dl>
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
.hero { display: grid; grid-template-columns: minmax(0, 1fr) 190px; gap: 32px; align-items: center; min-height: 520px; padding: 42px 0 46px; border-bottom: 1px solid var(--line); }
h1 { font-size: clamp(36px, 5.4vw, 62px); line-height: 1.04; letter-spacing: 0; margin: 0 0 20px; }
h2 { font-size: 28px; margin: 34px 0 12px; }
h3 { font-size: 20px; margin: 0 0 10px; }
.lead { font-size: 19px; max-width: 780px; color: var(--muted); }
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
.learning-diagram { margin: 18px 0 30px; padding: 0; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); overflow: hidden; }
.learning-diagram figcaption { padding: 12px 16px; border-bottom: 1px solid var(--line); color: var(--accent-dark); font-weight: 800; }
.flow-steps { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; }
.flow-step { position: relative; min-height: 160px; padding: 16px; border-right: 1px solid var(--line); background: linear-gradient(180deg, #ffffff, #f8fbfa); }
.flow-step:last-child { border-right: 0; }
.flow-step span { display: inline-flex; align-items: center; min-height: 28px; margin-bottom: 10px; padding: 4px 8px; border-radius: 6px; background: var(--soft); color: var(--accent-dark); font-size: 13px; font-weight: 800; }
.flow-step p { margin: 0; color: var(--muted); font-size: 14px; overflow-wrap: anywhere; }
.lecture-card { margin: 16px 0; }
.lecture-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.lecture-heading h2 { margin-top: 0; }
.lecture-grid { display: grid; grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr); gap: 18px; }
.lecture-grid section { min-width: 0; }
.lecture-flow .flow-step { min-height: 138px; }
.approach-stack { display: grid; gap: 12px; }
.approach-card { background: #fbfcfc; }
.approach-card h4 { margin: 0 0 8px; font-size: 18px; }
.principle-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 16px; }
.principle-grid article { padding: 14px; }
.principle-grid h3 { font-size: 17px; }
.principle-grid p { color: var(--muted); margin-bottom: 0; }
@media (max-width: 820px) {
  .topbar { align-items: flex-start; flex-direction: column; padding: 12px 18px; }
  main { padding: 18px; }
  .hero, .three, .grid { grid-template-columns: 1fr; }
  .hero { min-height: 0; padding-top: 32px; }
  h1 { font-size: clamp(34px, 10vw, 44px); }
  .flow-steps { grid-template-columns: 1fr; }
  .flow-step { min-height: 0; border-right: 0; border-bottom: 1px solid var(--line); }
  .flow-step:last-child { border-bottom: 0; }
  .lecture-heading, .lecture-grid { display: grid; grid-template-columns: 1fr; }
  .principle-grid { grid-template-columns: 1fr; }
}
"""
    write(SITE / "assets/styles.css", css)


def main() -> None:
    concepts = load_json("analysis/concepts/concept-atlas.json")
    themes = load_json("analysis/themes/theme-map.json")
    subthemes = load_json("analysis/themes/subtheme-map.json")
    evidence = load_json("analysis/evidence/evidence-ledger.json")
    transcript_index = load_json("raw-material/youtube/transcript-index.json")
    lecture_guides = load_json("analysis/deep-rl/lecture-guide.json")
    lecture_approaches = load_json("analysis/deep-rl/lecture-approaches.json")
    diffusion_guides = load_json("analysis/diffusion/lecture-guide.json")
    diffusion_approaches = load_json("analysis/diffusion/lecture-approaches.json")
    llm_guides = load_json("analysis/llms/lecture-guide.json")
    llm_approaches = load_json("analysis/llms/lecture-approaches.json")
    deep_unsupervised_guides = load_json("analysis/deep-unsupervised/lecture-guide.json")
    deep_unsupervised_approaches = load_json("analysis/deep-unsupervised/lecture-approaches.json")
    primitives = load_json("analysis/throughlines/primitives.json")
    families = load_json("analysis/throughlines/method-families.json")
    build_assets()
    build_index(concepts, themes, evidence)
    build_llms(transcript_index, concepts, evidence, llm_guides, llm_approaches)
    build_deep_rl(transcript_index, concepts, evidence, lecture_guides, lecture_approaches)
    build_diffusion(transcript_index, concepts, evidence, diffusion_guides, diffusion_approaches)
    build_deep_unsupervised(
        transcript_index,
        concepts,
        evidence,
        deep_unsupervised_guides,
        deep_unsupervised_approaches,
    )
    build_concepts(concepts, evidence)
    build_themes(themes, subthemes, concepts)
    build_families(families, evidence)
    build_primitives(primitives)
    build_evidence(evidence)


if __name__ == "__main__":
    main()
