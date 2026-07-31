#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw-material/youtube"
ANALYSIS = ROOT / "analysis"

CONCEPTS: list[dict[str, Any]] = [
    {
        "name": "tokenization",
        "theme": "text-to-model interface",
        "keywords": ["tokenization", "tokenizer", "tokens", "vocabulary", "byte pair", "bpe"],
        "big_picture": "Text must be cut into reusable pieces before a model can count, compare, or predict it.",
        "problem_solved": "Raw text has no fixed numerical shape, so the model needs stable text pieces it can assign numbers to.",
        "domain": "Language models and multimodal models that process text.",
        "why_important": "The first split of text controls sequence length, rare-word behavior, and what the rest of the model can represent efficiently.",
        "first_principles": "Before learning meaning, the model needs a finite set of pieces. Tokenization chooses those pieces.",
    },
    {
        "name": "embeddings",
        "theme": "representation",
        "keywords": ["embedding", "embeddings", "representation", "representations", "vector", "vectors"],
        "big_picture": "A model turns discrete symbols into points in a learned space where useful relationships can be computed.",
        "problem_solved": "Token IDs are arbitrary labels; the model needs numbers whose distances and directions can carry useful structure.",
        "domain": "Language models, vision models, reinforcement learning policies, and diffusion systems.",
        "why_important": "Most later computation works by moving, mixing, and editing vectors.",
        "first_principles": "Give each item a location, then train those locations so useful items end up arranged in useful ways.",
    },
    {
        "name": "attention",
        "theme": "information routing",
        "keywords": ["attention", "self-attention", "query", "queries", "key", "keys", "value", "values"],
        "big_picture": "Attention lets each token decide which other tokens matter for the current prediction.",
        "problem_solved": "A token cannot carry the whole context by itself, so it needs a way to look up relevant information.",
        "domain": "Transformers for language, vision, diffusion models, and agents.",
        "why_important": "Attention is the main routing mechanism that made transformer models broadly useful.",
        "first_principles": "Ask a question, compare it to labels on earlier information, then copy a weighted mix of what matched.",
    },
    {
        "name": "transformer architecture",
        "theme": "model structure",
        "keywords": ["transformer", "transformers", "residual", "layer norm", "feedforward", "feed-forward"],
        "big_picture": "A transformer repeatedly lets tokens read each other and then updates each token's running vector.",
        "problem_solved": "The model needs many rounds of communication and computation without losing earlier information.",
        "domain": "Modern language models, vision transformers, diffusion transformers, and multimodal models.",
        "why_important": "It is the shared backbone behind much of current language and vision-model work.",
        "first_principles": "Keep a running notebook for each token; each layer reads from other notebooks, edits its own, and passes it forward.",
    },
    {
        "name": "pretraining",
        "theme": "learning from raw data",
        "keywords": ["pretraining", "pre-train", "pre train", "next token", "language modeling", "predict the next"],
        "big_picture": "Pretraining teaches a model broad structure by making it predict missing or future data at large scale.",
        "problem_solved": "Hand-labeled examples are too narrow; raw data provides far more practice.",
        "domain": "Language, vision, and multimodal foundation models.",
        "why_important": "It creates the base model that later tuning, reasoning, and tool use build on.",
        "first_principles": "Make a guess, measure the surprise, and adjust the model so similar guesses improve later.",
    },
    {
        "name": "fine-tuning and preference learning",
        "theme": "behavior shaping",
        "keywords": ["fine-tuning", "finetuning", "instruction", "preference", "rlhf", "dpo", "alignment"],
        "big_picture": "A base model is steered toward behavior people want by training on examples, choices, or rewards.",
        "problem_solved": "Predicting likely text is not the same as answering helpfully or following instructions.",
        "domain": "Assistants, reasoning models, safety tuning, and domain adaptation.",
        "why_important": "It turns a raw predictor into a usable system.",
        "first_principles": "Shift probability away from bad continuations and toward responses that match the intended behavior.",
    },
    {
        "name": "chain-of-thought and reasoning",
        "theme": "inference-time work",
        "keywords": ["chain of thought", "reasoning", "step by step", "scratchpad", "deliberation"],
        "big_picture": "A model can spend extra tokens writing intermediate work before committing to an answer.",
        "problem_solved": "Some problems require holding and combining intermediate facts, not just giving the first likely answer.",
        "domain": "Math, coding, planning, tool use, and language-model agents.",
        "why_important": "It connects model quality with how much work the model is allowed to do at inference time.",
        "first_principles": "Use the output stream as scratch paper: write useful partial results, then base the answer on them.",
    },
    {
        "name": "agents, retrieval, and tools",
        "theme": "external action loop",
        "keywords": ["agent", "agents", "rag", "retrieval", "tool", "tools", "function calling", "search"],
        "big_picture": "A model can be placed in a loop where it reads outside information, calls tools, and updates its next step.",
        "problem_solved": "Many tasks require fresh information or actions outside the model's stored weights.",
        "domain": "Assistants, coding agents, research workflows, and enterprise systems.",
        "why_important": "It moves models from answer generators toward task-completing systems.",
        "first_principles": "Choose an action, observe the result, and decide what to do next.",
    },
    {
        "name": "policy",
        "theme": "decision making",
        "keywords": ["policy", "policies", "actor", "action", "actions"],
        "big_picture": "A policy is the rule a system uses to choose what to do next.",
        "problem_solved": "In reinforcement learning, the output is not just a label; it is an action that changes the future.",
        "domain": "Robotics, games, control, language-model agents, and RL for reasoning.",
        "why_important": "Policy learning is the central object of reinforcement learning.",
        "first_principles": "Given what you can see now, choose the next move.",
    },
    {
        "name": "reward",
        "theme": "feedback signal",
        "keywords": ["reward", "rewards", "return", "advantage", "preference", "feedback"],
        "big_picture": "Reward is the feedback that says which outcomes should become more likely.",
        "problem_solved": "The learner needs a signal that connects actions now to better or worse consequences later.",
        "domain": "Reinforcement learning, preference learning, robot learning, and reasoning-model training.",
        "why_important": "Reward defines what the learner is being pushed toward, including possible loopholes.",
        "first_principles": "Mark some outcomes as better, then change future choices so better outcomes happen more often.",
    },
    {
        "name": "policy gradients",
        "theme": "learning to act",
        "keywords": ["policy gradient", "policy gradients", "reinforce", "gradient estimator"],
        "big_picture": "Policy gradients change an action rule by increasing the chance of actions that led to better outcomes.",
        "problem_solved": "When the best action is not known directly, the system must learn from sampled attempts.",
        "domain": "Deep RL, RLHF, robotics, and RL for language-model reasoning.",
        "why_important": "It is a core bridge between trial-and-error feedback and neural-network training.",
        "first_principles": "Try actions, see which attempts worked better, and nudge the action rule toward those attempts.",
    },
    {
        "name": "q-learning",
        "theme": "value learning",
        "keywords": ["q-learning", "q learning", "q function", "q-function", "bellman", "value function"],
        "big_picture": "Q-learning estimates how good each action is from a given situation.",
        "problem_solved": "The system needs to compare possible actions before knowing the final long-term result.",
        "domain": "Reinforcement learning, control, games, and offline RL.",
        "why_important": "It teaches decision-making by learning the value of choices, not only by imitating examples.",
        "first_principles": "Ask, 'If I do this now, how much future reward should I expect?'",
    },
    {
        "name": "offline reinforcement learning",
        "theme": "learning from fixed experience",
        "keywords": ["offline rl", "offline reinforcement", "dataset", "conservative", "distribution shift"],
        "big_picture": "Offline RL tries to learn a good policy from logged experience without new trial-and-error interaction.",
        "problem_solved": "Real-world exploration can be expensive or unsafe, so the learner must use old data carefully.",
        "domain": "Robotics, healthcare, recommendation systems, and logged control data.",
        "why_important": "It addresses the gap between simulated RL and settings where bad exploration has real cost.",
        "first_principles": "Learn from what was already tried, but avoid trusting guesses far outside that experience.",
    },
    {
        "name": "model-based reinforcement learning",
        "theme": "planning with a learned world",
        "keywords": ["model-based", "model based", "dynamics model", "planning", "rollout"],
        "big_picture": "Model-based RL learns or uses a model of what happens next so it can plan before acting.",
        "problem_solved": "Trying every action in the real world can be too slow, expensive, or risky.",
        "domain": "Robotics, control, games, and simulated agents.",
        "why_important": "It trades real-world trial and error for prediction and planning.",
        "first_principles": "Imagine likely futures, compare them, take the first useful action, and update when reality arrives.",
    },
    {
        "name": "diffusion",
        "theme": "generative modeling",
        "keywords": ["diffusion", "denoising", "noising", "reverse process"],
        "big_picture": "Diffusion models learn to turn noise into data by reversing a gradual corruption process.",
        "problem_solved": "Generating complex images directly is hard; removing noise step by step is easier to learn.",
        "domain": "Image generation, video, audio, and multimodal generative models.",
        "why_important": "Diffusion became a dominant method for high-quality generative vision systems.",
        "first_principles": "Start from a messy picture and repeatedly clean it until structure appears.",
    },
    {
        "name": "score matching",
        "theme": "generative modeling",
        "keywords": ["score matching", "score function", "gradient of log", "denoising score"],
        "big_picture": "Score matching learns which direction data becomes more likely.",
        "problem_solved": "A generator needs guidance for how to move noisy samples toward realistic data.",
        "domain": "Diffusion models, energy-based models, and probability modeling.",
        "why_important": "It gives diffusion models their local direction signal for denoising.",
        "first_principles": "At each noisy point, learn the arrow that points back toward more data-like regions.",
    },
    {
        "name": "flow matching",
        "theme": "generative modeling",
        "keywords": ["flow matching", "velocity field", "ode", "transport"],
        "big_picture": "Flow matching learns a smooth path that moves simple noise into data.",
        "problem_solved": "Instead of many discrete denoising steps, learn the motion that carries one distribution into another.",
        "domain": "Generative modeling, diffusion alternatives, and continuous-time models.",
        "why_important": "It provides another first-principles route from noise to samples.",
        "first_principles": "Learn the velocity field that tells each point how to travel from the starting cloud to the data cloud.",
    },
    {
        "name": "guidance",
        "theme": "controllable generation",
        "keywords": ["guidance", "classifier-free", "classifier free", "conditioning", "conditional"],
        "big_picture": "Guidance steers a generator toward a requested condition such as a prompt or class.",
        "problem_solved": "A generator may make plausible samples that do not match what the user asked for.",
        "domain": "Text-to-image generation, controllable diffusion, and multimodal generation.",
        "why_important": "It links user intent to the sample path.",
        "first_principles": "When cleaning noise, bias each step toward features that match the request.",
    },
    {
        "name": "evaluation",
        "theme": "measurement",
        "keywords": ["evaluation", "evaluate", "metric", "metrics", "benchmark", "fid", "human evaluation"],
        "big_picture": "Evaluation asks whether a model improved and what the score actually measures.",
        "problem_solved": "Generated outputs and learned behavior can look good in one way while failing in another.",
        "domain": "Language models, RL systems, diffusion models, and agents.",
        "why_important": "Without clear measurement, progress can be confused with overfitting to the test.",
        "first_principles": "Choose a sample of behavior, measure it, and be explicit about what that measurement can and cannot prove.",
    },
]

THEMES: list[dict[str, Any]] = [
    {
        "name": "representation as the internal workspace",
        "concepts": ["tokenization", "embeddings", "attention", "transformer architecture"],
        "core_problem": "How does messy input become internal information a model can reuse?",
        "plain_language": "The model first makes things countable, then places them on maps, then repeatedly lets each item read and update those maps.",
    },
    {
        "name": "learning from feedback",
        "concepts": ["pretraining", "fine-tuning and preference learning", "reward", "policy gradients"],
        "core_problem": "How does a model change after being wrong, unhelpful, or unrewarded?",
        "plain_language": "Training turns feedback into small changes in what the model is likely to do next time.",
    },
    {
        "name": "choosing actions that change the future",
        "concepts": ["policy", "q-learning", "offline reinforcement learning", "model-based reinforcement learning"],
        "core_problem": "How does a system learn when its choice changes what evidence it will see next?",
        "plain_language": "An RL system must choose, observe the consequence, and improve future choices under uncertainty.",
    },
    {
        "name": "spending more work at inference time",
        "concepts": ["chain-of-thought and reasoning", "agents, retrieval, and tools"],
        "core_problem": "When is one forward answer not enough?",
        "plain_language": "The system can write intermediate steps, call tools, retrieve outside facts, and revise its next move.",
    },
    {
        "name": "turning noise into structured samples",
        "concepts": ["diffusion", "score matching", "flow matching", "guidance"],
        "core_problem": "How can a model generate a complex image or sample from a simple starting point?",
        "plain_language": "Start from simple noise, learn directions or flows that make it more data-like, and steer the path toward the request.",
    },
    {
        "name": "measurement as a claim with limits",
        "concepts": ["evaluation"],
        "core_problem": "What does a score prove, and what does it hide?",
        "plain_language": "A metric is a controlled sample of behavior, not the full truth about a model.",
    },
]


def load_index() -> list[dict[str, Any]]:
    return json.loads((RAW / "transcript-index.json").read_text(encoding="utf-8"))


def load_text(record: dict[str, Any]) -> str:
    path = ROOT / record["clean_txt"]
    return path.read_text(encoding="utf-8", errors="ignore")


def count_keyword_hits(text: str, title: str, keywords: list[str]) -> int:
    haystack = f"{title}\n{text}".lower()
    total = 0
    for keyword in keywords:
        total += len(re.findall(rf"\b{re.escape(keyword.lower())}\b", haystack))
    return total


def build() -> None:
    (ANALYSIS / "concepts").mkdir(parents=True, exist_ok=True)
    (ANALYSIS / "themes").mkdir(parents=True, exist_ok=True)
    (ANALYSIS / "evidence").mkdir(parents=True, exist_ok=True)

    records = load_index()
    texts = {record["id"]: load_text(record) for record in records}

    concept_rows: list[dict[str, Any]] = []
    evidence_rows: list[dict[str, Any]] = []
    for concept in CONCEPTS:
        matches = []
        for record in records:
            hits = count_keyword_hits(texts[record["id"]], record["title"], concept["keywords"])
            if hits:
                matches.append(
                    {
                        "video_id": record["id"],
                        "course_slug": record["course_slug"],
                        "course_index": record["course_index"],
                        "title": record["title"],
                        "url": record["url"],
                        "clean_txt": record["clean_txt"],
                        "keyword_hits": hits,
                    }
                )
        matches.sort(key=lambda row: row["keyword_hits"], reverse=True)
        by_course = Counter(match["course_slug"] for match in matches)
        concept_rows.append(
            {
                **{key: value for key, value in concept.items() if key != "keywords"},
                "keywords": concept["keywords"],
                "evidence_video_count": len(matches),
                "evidence_by_course": dict(sorted(by_course.items())),
                "strongest_evidence": matches[:8],
                "evidence_kind": "keyword/title match over clean transcript; seed extraction, not final interpretation",
            }
        )
        for match in matches:
            evidence_rows.append(
                {
                    "concept": concept["name"],
                    "theme": concept["theme"],
                    "evidence_kind": "transcript_keyword_match",
                    **match,
                }
            )

    theme_rows = []
    by_concept = {row["name"]: row for row in concept_rows}
    for theme in THEMES:
        related = [by_concept[name] for name in theme["concepts"] if name in by_concept]
        video_ids = set()
        course_counts: Counter[str] = Counter()
        for concept in related:
            for match in concept["strongest_evidence"]:
                video_ids.add(match["video_id"])
                course_counts[match["course_slug"]] += 1
        theme_rows.append(
            {
                **theme,
                "evidence_video_count_from_top_matches": len(video_ids),
                "course_presence_from_top_matches": dict(sorted(course_counts.items())),
                "status": "seed theme; requires transcript reading before publication",
            }
        )

    (ANALYSIS / "concepts" / "concept-atlas-seed.json").write_text(
        json.dumps(concept_rows, indent=2) + "\n",
        encoding="utf-8",
    )
    (ANALYSIS / "themes" / "theme-map-seed.json").write_text(
        json.dumps(theme_rows, indent=2) + "\n",
        encoding="utf-8",
    )
    (ANALYSIS / "evidence" / "evidence-ledger-seed.json").write_text(
        json.dumps(evidence_rows, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(records, concept_rows, theme_rows)


def write_markdown(records: list[dict[str, Any]], concepts: list[dict[str, Any]], themes: list[dict[str, Any]]) -> None:
    course_counts = defaultdict(lambda: {"videos": 0, "words": 0})
    for record in records:
        course_counts[record["course_slug"]]["videos"] += 1
        course_counts[record["course_slug"]]["words"] += record["word_count"]

    lines = [
        "# Stanford Course Research Seed",
        "",
        "This is a transcript-backed starting point, not a final synthesis. Evidence links point to clean transcript files and video records.",
        "",
        "## Corpus",
        "",
    ]
    for slug, stats in sorted(course_counts.items()):
        lines.append(f"- `{slug}`: {stats['videos']} videos, {stats['words']:,} clean words")

    lines.extend(["", "## Seed Themes", ""])
    for theme in themes:
        lines.extend(
            [
                f"### {theme['name']}",
                "",
                f"Core problem: {theme['core_problem']}",
                "",
                f"Plain-language frame: {theme['plain_language']}",
                "",
                "Concepts: " + ", ".join(f"`{name}`" for name in theme["concepts"]),
                "",
            ]
        )

    lines.extend(["## Seed Concept Atlas", ""])
    for concept in concepts:
        top = concept["strongest_evidence"][:3]
        lines.extend(
            [
                f"### {concept['name']}",
                "",
                f"Big picture: {concept['big_picture']}",
                "",
                f"Problem solved: {concept['problem_solved']}",
                "",
                f"First principles: {concept['first_principles']}",
                "",
                f"Evidence coverage: {concept['evidence_video_count']} videos; {concept['evidence_by_course']}",
                "",
            ]
        )
        if top:
            lines.append("Strongest seed evidence:")
            for match in top:
                lines.append(
                    f"- `{match['video_id']}` `{match['course_slug']}` lecture {match['course_index']}: {match['title']} ({match['keyword_hits']} hits)"
                )
            lines.append("")

    (ANALYSIS / "research-seed.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
