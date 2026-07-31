# Stanford Course Research Seed

This is a transcript-backed starting point, not a final synthesis. Evidence links point to clean transcript files and video records.

## Corpus

- `stanford-cme295-transformers-llms-autumn-2025`: 9 videos, 120,759 clean words
- `stanford-cme296-diffusion-large-vision-models-spring-2026`: 8 videos, 103,018 clean words
- `stanford-cs224r-deep-rl-spring-2025`: 19 videos, 187,514 clean words

## Seed Themes

### representation as the internal workspace

Core problem: How does messy input become internal information a model can reuse?

Plain-language frame: The model first makes things countable, then places them on maps, then repeatedly lets each item read and update those maps.

Concepts: `tokenization`, `embeddings`, `attention`, `transformer architecture`

### learning from feedback

Core problem: How does a model change after being wrong, unhelpful, or unrewarded?

Plain-language frame: Training turns feedback into small changes in what the model is likely to do next time.

Concepts: `pretraining`, `fine-tuning and preference learning`, `reward`, `policy gradients`

### choosing actions that change the future

Core problem: How does a system learn when its choice changes what evidence it will see next?

Plain-language frame: An RL system must choose, observe the consequence, and improve future choices under uncertainty.

Concepts: `policy`, `q-learning`, `offline reinforcement learning`, `model-based reinforcement learning`

### spending more work at inference time

Core problem: When is one forward answer not enough?

Plain-language frame: The system can write intermediate steps, call tools, retrieve outside facts, and revise its next move.

Concepts: `chain-of-thought and reasoning`, `agents, retrieval, and tools`

### turning noise into structured samples

Core problem: How can a model generate a complex image or sample from a simple starting point?

Plain-language frame: Start from simple noise, learn directions or flows that make it more data-like, and steer the path toward the request.

Concepts: `diffusion`, `score matching`, `flow matching`, `guidance`

### measurement as a claim with limits

Core problem: What does a score prove, and what does it hide?

Plain-language frame: A metric is a controlled sample of behavior, not the full truth about a model.

Concepts: `evaluation`

## Seed Concept Atlas

### tokenization

Big picture: Text must be cut into reusable pieces before a model can count, compare, or predict it.

Problem solved: Raw text has no fixed numerical shape, so the model needs stable text pieces it can assign numbers to.

First principles: Before learning meaning, the model needs a finite set of pieces. Tokenization chooses those pieces.

Evidence coverage: 22 videos; {'stanford-cme295-transformers-llms-autumn-2025': 9, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 5, 'stanford-cs224r-deep-rl-spring-2025': 8}

Strongest seed evidence:
- `Ub3GoFaUcds` `stanford-cme295-transformers-llms-autumn-2025` lecture 1: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 1 - Transformer (67 hits)
- `yT84Y5zCnaA` `stanford-cme295-transformers-llms-autumn-2025` lecture 2: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks (63 hits)
- `Q5baLehv5So` `stanford-cme295-transformers-llms-autumn-2025` lecture 3: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 3 - Tranformers & Large Language Models (55 hits)

### embeddings

Big picture: A model turns discrete symbols into points in a learned space where useful relationships can be computed.

Problem solved: Token IDs are arbitrary labels; the model needs numbers whose distances and directions can carry useful structure.

First principles: Give each item a location, then train those locations so useful items end up arranged in useful ways.

Evidence coverage: 29 videos; {'stanford-cme295-transformers-llms-autumn-2025': 9, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 8, 'stanford-cs224r-deep-rl-spring-2025': 12}

Strongest seed evidence:
- `agN3AlfGFrk` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 3: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 3 - Flow matching (125 hits)
- `HpFdSlMeXzQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 5: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 5 - Architectures (117 hits)
- `yT84Y5zCnaA` `stanford-cme295-transformers-llms-autumn-2025` lecture 2: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks (113 hits)

### attention

Big picture: Attention lets each token decide which other tokens matter for the current prediction.

Problem solved: A token cannot carry the whole context by itself, so it needs a way to look up relevant information.

First principles: Ask a question, compare it to labels on earlier information, then copy a weighted mix of what matched.

Evidence coverage: 35 videos; {'stanford-cme295-transformers-llms-autumn-2025': 9, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 7, 'stanford-cs224r-deep-rl-spring-2025': 19}

Strongest seed evidence:
- `yT84Y5zCnaA` `stanford-cme295-transformers-llms-autumn-2025` lecture 2: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks (163 hits)
- `Ub3GoFaUcds` `stanford-cme295-transformers-llms-autumn-2025` lecture 1: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 1 - Transformer (136 hits)
- `Q5baLehv5So` `stanford-cme295-transformers-llms-autumn-2025` lecture 3: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 3 - Tranformers & Large Language Models (109 hits)

### transformer architecture

Big picture: A transformer repeatedly lets tokens read each other and then updates each token's running vector.

Problem solved: The model needs many rounds of communication and computation without losing earlier information.

First principles: Keep a running notebook for each token; each layer reads from other notebooks, edits its own, and passes it forward.

Evidence coverage: 22 videos; {'stanford-cme295-transformers-llms-autumn-2025': 9, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 6, 'stanford-cs224r-deep-rl-spring-2025': 7}

Strongest seed evidence:
- `Q86qzJ1K1Ss` `stanford-cme295-transformers-llms-autumn-2025` lecture 9: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 9 - Recap & Current Trends (46 hits)
- `yT84Y5zCnaA` `stanford-cme295-transformers-llms-autumn-2025` lecture 2: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 2 - Transformer-Based Models & Tricks (43 hits)
- `HpFdSlMeXzQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 5: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 5 - Architectures (39 hits)

### pretraining

Big picture: Pretraining teaches a model broad structure by making it predict missing or future data at large scale.

Problem solved: Hand-labeled examples are too narrow; raw data provides far more practice.

First principles: Make a guess, measure the surprise, and adjust the model so similar guesses improve later.

Evidence coverage: 21 videos; {'stanford-cme295-transformers-llms-autumn-2025': 8, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 4, 'stanford-cs224r-deep-rl-spring-2025': 9}

Strongest seed evidence:
- `Q5baLehv5So` `stanford-cme295-transformers-llms-autumn-2025` lecture 3: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 3 - Tranformers & Large Language Models (25 hits)
- `VlA_jt_3Qc4` `stanford-cme295-transformers-llms-autumn-2025` lecture 4: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 4 - LLM Training (22 hits)
- `Q86qzJ1K1Ss` `stanford-cme295-transformers-llms-autumn-2025` lecture 9: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 9 - Recap & Current Trends (18 hits)

### fine-tuning and preference learning

Big picture: A base model is steered toward behavior people want by training on examples, choices, or rewards.

Problem solved: Predicting likely text is not the same as answering helpfully or following instructions.

First principles: Shift probability away from bad continuations and toward responses that match the intended behavior.

Evidence coverage: 22 videos; {'stanford-cme295-transformers-llms-autumn-2025': 8, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 4, 'stanford-cs224r-deep-rl-spring-2025': 10}

Strongest seed evidence:
- `XKLGuwvSKvI` `stanford-cs224r-deep-rl-spring-2025` lecture 9: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 9: RL for LLMs (102 hits)
- `PmW_TMQ3l0I` `stanford-cme295-transformers-llms-autumn-2025` lecture 5: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 5 - LLM tuning (73 hits)
- `O2VpNnwB4lM` `stanford-cs224r-deep-rl-spring-2025` lecture 10: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 10: RL for LLM Reasoning (16 hits)

### chain-of-thought and reasoning

Big picture: A model can spend extra tokens writing intermediate work before committing to an answer.

Problem solved: Some problems require holding and combining intermediate facts, not just giving the first likely answer.

First principles: Use the output stream as scratch paper: write useful partial results, then base the answer on them.

Evidence coverage: 24 videos; {'stanford-cme295-transformers-llms-autumn-2025': 7, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 7, 'stanford-cs224r-deep-rl-spring-2025': 10}

Strongest seed evidence:
- `k5Fh-UgTuCo` `stanford-cme295-transformers-llms-autumn-2025` lecture 6: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 6 - LLM Reasoning (103 hits)
- `O2VpNnwB4lM` `stanford-cs224r-deep-rl-spring-2025` lecture 10: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 10: RL for LLM Reasoning (24 hits)
- `h-7S6HNq0Vg` `stanford-cme295-transformers-llms-autumn-2025` lecture 7: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 7 - Agentic LLMs (22 hits)

### agents, retrieval, and tools

Big picture: A model can be placed in a loop where it reads outside information, calls tools, and updates its next step.

Problem solved: Many tasks require fresh information or actions outside the model's stored weights.

First principles: Choose an action, observe the result, and decide what to do next.

Evidence coverage: 28 videos; {'stanford-cme295-transformers-llms-autumn-2025': 7, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 4, 'stanford-cs224r-deep-rl-spring-2025': 17}

Strongest seed evidence:
- `h-7S6HNq0Vg` `stanford-cme295-transformers-llms-autumn-2025` lecture 7: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 7 - Agentic LLMs (143 hits)
- `8fNP4N46RRo` `stanford-cme295-transformers-llms-autumn-2025` lecture 8: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 8 - LLM Evaluation (98 hits)
- `Q86qzJ1K1Ss` `stanford-cme295-transformers-llms-autumn-2025` lecture 9: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 9 - Recap & Current Trends (23 hits)

### policy

Big picture: A policy is the rule a system uses to choose what to do next.

Problem solved: In reinforcement learning, the output is not just a label; it is an action that changes the future.

First principles: Given what you can see now, choose the next move.

Evidence coverage: 27 videos; {'stanford-cme295-transformers-llms-autumn-2025': 6, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 2, 'stanford-cs224r-deep-rl-spring-2025': 19}

Strongest seed evidence:
- `-7kv6jf0isQ` `stanford-cs224r-deep-rl-spring-2025` lecture 6: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 6: Q-Learning (280 hits)
- `cRGKc-nAWho` `stanford-cs224r-deep-rl-spring-2025` lecture 5: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 5: Off-Policy Actor Critic (272 hits)
- `iKWYLSVAtfM` `stanford-cs224r-deep-rl-spring-2025` lecture 15: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 15: Hierarchical RL and IL (250 hits)

### reward

Big picture: Reward is the feedback that says which outcomes should become more likely.

Problem solved: The learner needs a signal that connects actions now to better or worse consequences later.

First principles: Mark some outcomes as better, then change future choices so better outcomes happen more often.

Evidence coverage: 30 videos; {'stanford-cme295-transformers-llms-autumn-2025': 7, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 4, 'stanford-cs224r-deep-rl-spring-2025': 19}

Strongest seed evidence:
- `PmW_TMQ3l0I` `stanford-cme295-transformers-llms-autumn-2025` lecture 5: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 5 - LLM tuning (173 hits)
- `XKLGuwvSKvI` `stanford-cs224r-deep-rl-spring-2025` lecture 9: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 9: RL for LLMs (139 hits)
- `oejFZShW9hU` `stanford-cs224r-deep-rl-spring-2025` lecture 4: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 4: Actor-Critic Methods (132 hits)

### policy gradients

Big picture: Policy gradients change an action rule by increasing the chance of actions that led to better outcomes.

Problem solved: When the best action is not known directly, the system must learn from sampled attempts.

First principles: Try actions, see which attempts worked better, and nudge the action rule toward those attempts.

Evidence coverage: 12 videos; {'stanford-cme295-transformers-llms-autumn-2025': 1, 'stanford-cs224r-deep-rl-spring-2025': 11}

Strongest seed evidence:
- `KCAOXd4IO9o` `stanford-cs224r-deep-rl-spring-2025` lecture 3: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 3: Policy Gradients (12 hits)
- `oejFZShW9hU` `stanford-cs224r-deep-rl-spring-2025` lecture 4: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 4: Actor-Critic Methods (10 hits)
- `cRGKc-nAWho` `stanford-cs224r-deep-rl-spring-2025` lecture 5: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 5: Off-Policy Actor Critic (5 hits)

### q-learning

Big picture: Q-learning estimates how good each action is from a given situation.

Problem solved: The system needs to compare possible actions before knowing the final long-term result.

First principles: Ask, 'If I do this now, how much future reward should I expect?'

Evidence coverage: 18 videos; {'stanford-cme295-transformers-llms-autumn-2025': 4, 'stanford-cs224r-deep-rl-spring-2025': 14}

Strongest seed evidence:
- `-7kv6jf0isQ` `stanford-cs224r-deep-rl-spring-2025` lecture 6: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 6: Q-Learning (79 hits)
- `07MQNMcxhZU` `stanford-cs224r-deep-rl-spring-2025` lecture 19: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Tutorial Session: Review of Q-Learning (78 hits)
- `lRDaXnPIzks` `stanford-cs224r-deep-rl-spring-2025` lecture 7: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 7: Offline RL (66 hits)

### offline reinforcement learning

Big picture: Offline RL tries to learn a good policy from logged experience without new trial-and-error interaction.

Problem solved: Real-world exploration can be expensive or unsafe, so the learner must use old data carefully.

First principles: Learn from what was already tried, but avoid trusting guesses far outside that experience.

Evidence coverage: 12 videos; {'stanford-cme295-transformers-llms-autumn-2025': 1, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 1, 'stanford-cs224r-deep-rl-spring-2025': 10}

Strongest seed evidence:
- `lRDaXnPIzks` `stanford-cs224r-deep-rl-spring-2025` lecture 7: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 7: Offline RL (26 hits)
- `PDIxDhA9Z6Y` `stanford-cs224r-deep-rl-spring-2025` lecture 8: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 8: Reward Learning (19 hits)
- `wSiyEpvoGkA` `stanford-cs224r-deep-rl-spring-2025` lecture 13: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 13: Meta RL (17 hits)

### model-based reinforcement learning

Big picture: Model-based RL learns or uses a model of what happens next so it can plan before acting.

Problem solved: Trying every action in the real world can be too slow, expensive, or risky.

First principles: Imagine likely futures, compare them, take the first useful action, and update when reality arrives.

Evidence coverage: 15 videos; {'stanford-cme295-transformers-llms-autumn-2025': 2, 'stanford-cs224r-deep-rl-spring-2025': 13}

Strongest seed evidence:
- `PvqyGnOirgA` `stanford-cs224r-deep-rl-spring-2025` lecture 11: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 11: Model-Based RL (56 hits)
- `O2VpNnwB4lM` `stanford-cs224r-deep-rl-spring-2025` lecture 10: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 10: RL for LLM Reasoning (25 hits)
- `qNdsI_4AQJw` `stanford-cs224r-deep-rl-spring-2025` lecture 12: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 12: Multi-Task RL (18 hits)

### diffusion

Big picture: Diffusion models learn to turn noise into data by reversing a gradual corruption process.

Problem solved: Generating complex images directly is hard; removing noise step by step is easier to learn.

First principles: Start from a messy picture and repeatedly clean it until structure appears.

Evidence coverage: 16 videos; {'stanford-cme295-transformers-llms-autumn-2025': 1, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 8, 'stanford-cs224r-deep-rl-spring-2025': 7}

Strongest seed evidence:
- `_WaR2fjZpEQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 2: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching (36 hits)
- `oyLUvz9nR6E` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 8: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 8 - Trending Topics (34 hits)
- `Q86qzJ1K1Ss` `stanford-cme295-transformers-llms-autumn-2025` lecture 9: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 9 - Recap & Current Trends (28 hits)

### score matching

Big picture: Score matching learns which direction data becomes more likely.

Problem solved: A generator needs guidance for how to move noisy samples toward realistic data.

First principles: At each noisy point, learn the arrow that points back toward more data-like regions.

Evidence coverage: 7 videos; {'stanford-cme296-diffusion-large-vision-models-spring-2026': 4, 'stanford-cs224r-deep-rl-spring-2025': 3}

Strongest seed evidence:
- `_WaR2fjZpEQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 2: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching (24 hits)
- `agN3AlfGFrk` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 3: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 3 - Flow matching (8 hits)
- `KCAOXd4IO9o` `stanford-cs224r-deep-rl-spring-2025` lecture 3: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 3: Policy Gradients (5 hits)

### flow matching

Big picture: Flow matching learns a smooth path that moves simple noise into data.

Problem solved: Instead of many discrete denoising steps, learn the motion that carries one distribution into another.

First principles: Learn the velocity field that tells each point how to travel from the starting cloud to the data cloud.

Evidence coverage: 9 videos; {'stanford-cme296-diffusion-large-vision-models-spring-2026': 8, 'stanford-cs224r-deep-rl-spring-2025': 1}

Strongest seed evidence:
- `agN3AlfGFrk` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 3: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 3 - Flow matching (54 hits)
- `_WaR2fjZpEQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 2: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching (19 hits)
- `IvXTl3yj-4Y` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 6: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 6 - Model Training (10 hits)

### guidance

Big picture: Guidance steers a generator toward a requested condition such as a prompt or class.

Problem solved: A generator may make plausible samples that do not match what the user asked for.

First principles: When cleaning noise, bias each step toward features that match the request.

Evidence coverage: 16 videos; {'stanford-cme295-transformers-llms-autumn-2025': 3, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 6, 'stanford-cs224r-deep-rl-spring-2025': 7}

Strongest seed evidence:
- `agN3AlfGFrk` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 3: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 3 - Flow matching (47 hits)
- `WUUq6TVAu8U` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 4: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 4 - Latent Space & Guidance (10 hits)
- `_WaR2fjZpEQ` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 2: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 2 - Score matching (7 hits)

### evaluation

Big picture: Evaluation asks whether a model improved and what the score actually measures.

Problem solved: Generated outputs and learned behavior can look good in one way while failing in another.

First principles: Choose a sample of behavior, measure it, and be explicit about what that measurement can and cannot prove.

Evidence coverage: 29 videos; {'stanford-cme295-transformers-llms-autumn-2025': 9, 'stanford-cme296-diffusion-large-vision-models-spring-2026': 7, 'stanford-cs224r-deep-rl-spring-2025': 13}

Strongest seed evidence:
- `8fNP4N46RRo` `stanford-cme295-transformers-llms-autumn-2025` lecture 8: Stanford CME295 Transformers & LLMs | Autumn 2025 | Lecture 8 - LLM Evaluation (92 hits)
- `iNaRBp4T57Q` `stanford-cme296-diffusion-large-vision-models-spring-2026` lecture 7: Stanford CME296 Diffusion & Large Vision Models | Spring 2026 | Lecture 7 - Evaluation (75 hits)
- `FacJ_1tTSx4` `stanford-cs224r-deep-rl-spring-2025` lecture 18: Stanford CS224R Deep Reinforcement Learning | Spring 2025 | Lecture 18: Frontiers (22 hits)
