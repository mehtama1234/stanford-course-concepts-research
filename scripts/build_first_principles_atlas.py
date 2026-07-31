#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "raw-material/youtube/transcript-index.json"
CME295 = "stanford-cme295-transformers-llms-autumn-2025"
CS224R = "stanford-cs224r-deep-rl-spring-2025"
CME296 = "stanford-cme296-diffusion-large-vision-models-spring-2026"

ALLOWED_EVIDENCE_COURSES: dict[str, set[str]] = {
    "tokenization": {CME295, CME296},
    "positional_encoding": {CME295, CME296},
    "pretraining": {CME295, CME296},
    "fine_tuning": {CME295, CS224R},
    "reasoning_traces": {CME295, CS224R},
    "agents_and_tools": {CME295, CS224R},
    "policy": {CS224R},
    "reward": {CS224R, CME295},
    "credit_assignment": {CS224R},
    "policy_gradient": {CS224R},
    "actor_critic": {CS224R},
    "q_learning": {CS224R},
    "offline_rl": {CS224R},
    "model_based_rl": {CS224R},
    "exploration": {CS224R},
    "rl_for_llms": {CS224R, CME295},
    "diffusion": {CME296},
    "score_matching": {CME296},
    "flow_matching": {CME296},
    "guidance": {CME296},
    "latent_space": {CME296},
    "vision_transformers": {CME296, CME295},
}


PRIMITIVES: list[dict[str, Any]] = [
    {
        "id": "compression",
        "name": "Compression",
        "plain_language": "Keep the parts that matter for the next decision and let go of the rest.",
        "why_it_exists": "Inputs, memories, images, and action histories are too large to carry forward unchanged.",
        "shows_up_in": ["tokenization", "embeddings", "latent_space", "state_abstraction", "distillation"],
    },
    {
        "id": "assignment",
        "name": "Assignment",
        "plain_language": "Decide which piece of evidence should be connected to which cause, label, action, or memory.",
        "why_it_exists": "Many causes can produce the same observation, so learning has to sort responsibility.",
        "shows_up_in": ["attention", "credit_assignment", "reward_learning", "score_matching"],
    },
    {
        "id": "credit",
        "name": "Credit",
        "plain_language": "Decide which earlier choice deserves blame or praise for something that happened later.",
        "why_it_exists": "Consequences arrive after chains of actions, not immediately after the action that mattered.",
        "shows_up_in": ["policy_gradient", "q_learning", "actor_critic", "rl_for_llms"],
    },
    {
        "id": "geometry",
        "name": "Geometry",
        "plain_language": "Arrange things so nearby points mean similar things and directions mean useful changes.",
        "why_it_exists": "A machine needs a numerical space where comparison and movement can be computed.",
        "shows_up_in": ["embeddings", "positional_encoding", "latent_space", "flow_matching"],
    },
    {
        "id": "search",
        "name": "Search",
        "plain_language": "Try to move through possible answers, actions, or images toward ones that satisfy a goal.",
        "why_it_exists": "Hard problems rarely reveal the right answer in one step.",
        "shows_up_in": ["chain_of_thought", "agents_and_tools", "exploration", "planning"],
    },
    {
        "id": "uncertainty",
        "name": "Uncertainty",
        "plain_language": "Keep track of many possible futures or explanations instead of pretending there is only one.",
        "why_it_exists": "Observations are incomplete, and the same present can lead to many futures.",
        "shows_up_in": ["diffusion", "model_based_rl", "offline_rl", "evaluation"],
    },
    {
        "id": "feedback",
        "name": "Feedback",
        "plain_language": "Use a signal after an attempt to change what the system does next time.",
        "why_it_exists": "A learner cannot improve unless something tells it how its guesses or actions worked out.",
        "shows_up_in": ["pretraining", "fine_tuning", "reward_modeling", "policy_gradient"],
    },
    {
        "id": "scale",
        "name": "Scale",
        "plain_language": "Ask what changes when data, model size, compute, or test-time work becomes much larger.",
        "why_it_exists": "Some behavior is invisible at small size because the system has too little capacity or practice.",
        "shows_up_in": ["scaling_laws", "emergence", "in_context_learning", "inference_time_compute"],
    },
    {
        "id": "invariance",
        "name": "Invariance",
        "plain_language": "Preserve the meaning while surface details such as position, wording, or style change.",
        "why_it_exists": "The same idea can appear in many forms, and a useful model should not relearn it from scratch every time.",
        "shows_up_in": ["positional_encoding", "data_augmentation", "vision_transformers", "generalization"],
    },
    {
        "id": "composition",
        "name": "Composition",
        "plain_language": "Build complex behavior by connecting reusable smaller operations.",
        "why_it_exists": "Large tasks are too varied to solve as one giant special case.",
        "shows_up_in": ["transformer_block", "agents_and_tools", "hierarchical_rl", "unet_architecture"],
    },
]


CONCEPTS: list[dict[str, Any]] = [
    {
        "id": "tokenization",
        "name": "Tokenization",
        "theme": "representation_workspace",
        "plain_language_definition": "Turning text into reusable pieces a model can count.",
        "everyday_problem": "The problem is that a model cannot read raw text as meaning; it first needs stable pieces that can be given numbers.",
        "first_principles_reason": "Computation needs finite symbols. Human language is open-ended, so the first constraint is to choose a manageable set of chunks that can cover new text.",
        "mathematical_principle": "A tokenizer is a mapping from a string to a sequence of IDs. The important idea is not the IDs themselves; it is that variable language becomes a sequence with a fixed vocabulary.",
        "why_it_matters": "It sets the length of the model's working memory and controls how rare words, code, numbers, and names are broken apart.",
        "what_breaks_without_it": "The model would have no consistent input units, and every later layer would receive a different kind of object each time.",
        "related_concepts": ["embeddings", "positional_encoding", "pretraining"],
        "primitives": ["compression"],
        "keywords": ["token", "tokens", "tokenization", "tokenizer", "vocabulary", "byte pair", "bpe"],
    },
    {
        "id": "embeddings",
        "name": "Embeddings",
        "theme": "representation_workspace",
        "plain_language_definition": "Learned coordinates that let a model compare things by arithmetic.",
        "everyday_problem": "The problem is that IDs like 17 or 9421 do not say what a word, patch, state, or action means.",
        "first_principles_reason": "A learning system needs a space where similar things can be placed near each other and useful directions can be adjusted by training.",
        "mathematical_principle": "An embedding table maps each item to a vector. A vector is just a list of numbers; training moves those numbers so useful relationships become easier to compute.",
        "why_it_matters": "Embeddings turn symbols into a shared workspace for attention, prediction, retrieval, and generation.",
        "what_breaks_without_it": "The model would treat related symbols as unrelated labels and could not smoothly share what it learns.",
        "related_concepts": ["tokenization", "latent_space", "representation_learning"],
        "primitives": ["geometry", "compression"],
        "keywords": ["embedding", "embeddings", "vector", "vectors", "representation", "representations"],
    },
    {
        "id": "positional_encoding",
        "name": "Position And Order",
        "theme": "representation_workspace",
        "plain_language_definition": "A way to tell the model where each piece sits in a sequence or image.",
        "everyday_problem": "The problem is that the same words or image patches mean different things depending on where they appear.",
        "first_principles_reason": "Attention compares items as a set unless order information is added. Order must be represented explicitly if order matters.",
        "mathematical_principle": "Position information is added as numbers that vary by location. The model can then learn patterns such as before, after, nearby, or far away.",
        "why_it_matters": "It lets transformers handle grammar, layout, time, and spatial structure.",
        "what_breaks_without_it": "The model may know which pieces exist but lose the arrangement that makes them meaningful.",
        "related_concepts": ["attention", "transformer_block", "vision_transformers"],
        "primitives": ["geometry", "invariance"],
        "keywords": ["position", "positional", "rope", "relative position", "sequence length"],
    },
    {
        "id": "attention",
        "name": "Attention",
        "theme": "representation_workspace",
        "plain_language_definition": "A learned way for each piece to decide which other pieces matter right now.",
        "everyday_problem": "The problem is that the input is too large to treat every earlier word, patch, or memory as equally important.",
        "first_principles_reason": "Useful context is selective. The system needs a content-based lookup mechanism instead of a fixed rule for what to read.",
        "mathematical_principle": "Each item makes a query, compares it with keys from other items, turns the match scores into weights, and averages values using those weights. The formula softmax(QK^T)V means: score matches, normalize them, then copy a weighted mixture of information.",
        "why_it_matters": "It gives transformers their main communication channel and lets the same model use different context for different tokens.",
        "what_breaks_without_it": "Long-range dependencies become hard, and the model must rely on fixed local patterns or compressed memory.",
        "related_concepts": ["retrieval", "credit_assignment", "transformer_block"],
        "primitives": ["assignment", "compression"],
        "keywords": ["attention", "self-attention", "self attention", "multi-head", "multi head", "attention head"],
    },
    {
        "id": "transformer_block",
        "name": "Transformer Block",
        "theme": "representation_workspace",
        "plain_language_definition": "A repeated update step where tokens read from each other and then rewrite their own state.",
        "everyday_problem": "The problem is that one lookup is not enough; understanding needs many rounds of communication and local computation.",
        "first_principles_reason": "A complex answer is built by repeatedly mixing information and transforming it. Depth lets simple operations compound.",
        "mathematical_principle": "A block usually combines attention, a small per-token network, normalization, and skip connections. The skip connection keeps the old state while adding a learned update, which makes deep stacks trainable.",
        "why_it_matters": "It is the reusable unit behind modern language, vision, and multimodal models.",
        "what_breaks_without_it": "The system loses the scalable recipe for building many layers of context-dependent computation.",
        "related_concepts": ["attention", "normalization", "residual_connections", "vision_transformers"],
        "primitives": ["composition", "feedback"],
        "keywords": ["transformer", "block", "layer norm", "normalization", "residual", "feed forward", "mlp"],
    },
    {
        "id": "pretraining",
        "name": "Pretraining",
        "theme": "learning_from_feedback",
        "plain_language_definition": "Large-scale practice before the model is asked to be useful in a specific way.",
        "everyday_problem": "The problem is that labeled examples are scarce, but raw text, images, actions, and videos are abundant.",
        "first_principles_reason": "A learner can absorb structure by being given a simple prediction game over huge data, even before people specify the final task.",
        "mathematical_principle": "Training reduces a loss, which is a number measuring how surprised or wrong the model was. Lower loss means the model assigns more probability to what actually happened.",
        "why_it_matters": "It creates broad reusable knowledge that later tuning can steer.",
        "what_breaks_without_it": "Every task would need its own large hand-labeled dataset, and models would learn narrow behavior from scratch.",
        "related_concepts": ["fine_tuning", "scaling_laws", "generalization"],
        "primitives": ["feedback", "scale"],
        "keywords": ["pretrain", "pretraining", "next token", "loss", "cross entropy", "language modeling"],
    },
    {
        "id": "fine_tuning",
        "name": "Fine-Tuning And Preference Learning",
        "theme": "learning_from_feedback",
        "plain_language_definition": "Steering a broad model toward behavior people actually want.",
        "everyday_problem": "The problem is that predicting likely text is not the same thing as being helpful, safe, concise, or correct.",
        "first_principles_reason": "Raw imitation learns what appears in data. Usefulness requires extra feedback about which possible responses people prefer.",
        "mathematical_principle": "Tuning changes probabilities: make wanted answers more likely and unwanted answers less likely. Preference learning turns comparisons between answers into a training signal.",
        "why_it_matters": "It is the bridge between a base model and an assistant, tutor, coder, or agent.",
        "what_breaks_without_it": "The model may be fluent but misaligned with the task, the user, or the deployment setting.",
        "related_concepts": ["reward_modeling", "rl_for_llms", "evaluation"],
        "primitives": ["feedback", "assignment"],
        "keywords": ["fine-tuning", "finetuning", "instruction", "preference", "rlhf", "dpo", "alignment"],
    },
    {
        "id": "reasoning_traces",
        "name": "Reasoning Traces",
        "theme": "inference_time_work",
        "plain_language_definition": "Using written intermediate work as temporary memory for hard problems.",
        "everyday_problem": "The problem is that some answers require several dependent steps, and the first likely sentence may skip a necessary intermediate fact.",
        "first_principles_reason": "A system with limited internal working memory can externalize partial results into tokens and condition on them later.",
        "mathematical_principle": "The model samples or scores a longer sequence before the final answer. Extra tokens change the context, so later predictions can depend on earlier intermediate steps.",
        "why_it_matters": "It turns generation into a multi-step computation instead of a single response reflex.",
        "what_breaks_without_it": "Tasks needing arithmetic, planning, proof, or careful decomposition often collapse into plausible but unsupported guesses.",
        "related_concepts": ["inference_time_compute", "rl_for_llms", "agents_and_tools"],
        "primitives": ["search", "composition"],
        "keywords": ["reasoning", "chain of thought", "cot", "scratchpad", "rationale", "reason"],
    },
    {
        "id": "agents_and_tools",
        "name": "Agents, Retrieval, And Tools",
        "theme": "inference_time_work",
        "plain_language_definition": "Putting a model in a loop where it can look things up, call tools, and react to results.",
        "everyday_problem": "The problem is that many tasks need current facts, external actions, or checks the model cannot store in its weights.",
        "first_principles_reason": "A useful system often needs perception, memory, action, and correction, not only prediction.",
        "mathematical_principle": "The loop is state, action, observation, update. At each step the model chooses an action based on the current context, then new evidence changes the next context.",
        "why_it_matters": "It connects language models to search, code execution, databases, browsers, and multi-step workflows.",
        "what_breaks_without_it": "The model is limited to stale internal knowledge and cannot verify or change the outside world.",
        "related_concepts": ["policy", "retrieval", "planning"],
        "primitives": ["search", "composition", "feedback"],
        "keywords": ["agent", "agents", "tool", "tools", "retrieval", "rag", "browser", "function calling"],
    },
    {
        "id": "evaluation",
        "name": "Evaluation",
        "theme": "measurement_limits",
        "plain_language_definition": "A controlled way to ask what a model can and cannot do.",
        "everyday_problem": "The problem is that a model can look impressive on examples while failing in places the test did not cover.",
        "first_principles_reason": "Measurement is sampling. Any score reflects the cases, rules, and incentives used to produce it.",
        "mathematical_principle": "A metric maps many behaviors to one number or table. The lost detail is as important as the reported score.",
        "why_it_matters": "It decides what work is rewarded, what systems ship, and which failures stay hidden.",
        "what_breaks_without_it": "Claims about capability become anecdotes, and progress can be confused with overfitting to a benchmark.",
        "related_concepts": ["generalization", "reward_modeling", "scaling_laws"],
        "primitives": ["uncertainty", "feedback"],
        "keywords": ["evaluation", "benchmark", "metric", "metrics", "eval", "test set", "generalization"],
    },
    {
        "id": "policy",
        "name": "Policy",
        "theme": "action_and_consequence",
        "plain_language_definition": "The rule an agent uses to choose what to do next.",
        "everyday_problem": "The problem is that the output is an action, and that action changes what happens afterward.",
        "first_principles_reason": "In a changing environment, the learner must connect what it can see now to a choice under uncertainty.",
        "mathematical_principle": "A policy is often written as pi(a|s): the chance of taking action a when the system is in situation s.",
        "why_it_matters": "It is the central object being learned in reinforcement learning and agentic LLM systems.",
        "what_breaks_without_it": "There is no explicit way to discuss or improve the system's behavior over time.",
        "related_concepts": ["reward", "policy_gradient", "q_learning"],
        "primitives": ["search", "uncertainty"],
        "keywords": ["policy", "policies", "policy optimization", "action distribution", "trajectory"],
    },
    {
        "id": "reward",
        "name": "Reward",
        "theme": "action_and_consequence",
        "plain_language_definition": "A signal that says which outcomes should become more likely.",
        "everyday_problem": "The problem is that an agent needs to know not just what happened, but whether it was better or worse.",
        "first_principles_reason": "Learning from action needs a direction of improvement. Reward supplies that direction, even when the right action was not labeled in advance.",
        "mathematical_principle": "Return is accumulated reward over time. The key idea is to value actions by their downstream consequences, not only their immediate effect.",
        "why_it_matters": "It turns behavior into something trainable when direct answers are unavailable.",
        "what_breaks_without_it": "The agent can collect experience but has no preference over outcomes.",
        "related_concepts": ["reward_modeling", "credit_assignment", "policy_gradient"],
        "primitives": ["feedback", "credit"],
        "keywords": ["reward", "rewards", "return", "preference", "reward model", "reinforcement"],
    },
    {
        "id": "credit_assignment",
        "name": "Credit Assignment",
        "theme": "action_and_consequence",
        "plain_language_definition": "Figuring out which earlier choices caused a later success or failure.",
        "everyday_problem": "The problem is that the important mistake may happen long before the bad outcome appears.",
        "first_principles_reason": "Time hides causes. A learner needs a way to connect delayed feedback back to the decisions that shaped it.",
        "mathematical_principle": "Discounted return gives later rewards less weight as they are traced backward. The exact formula varies, but the principle is to spread delayed feedback across earlier actions.",
        "why_it_matters": "It makes long-horizon learning possible in games, robotics, dialogue, and reasoning.",
        "what_breaks_without_it": "The system overreacts to the last action or misses the earlier decision that mattered.",
        "related_concepts": ["attention", "q_learning", "actor_critic"],
        "primitives": ["credit", "assignment"],
        "keywords": ["credit assignment", "delayed reward", "discount factor", "discounted return", "temporal credit"],
    },
    {
        "id": "policy_gradient",
        "name": "Policy Gradient",
        "theme": "action_and_consequence",
        "plain_language_definition": "Changing an action rule toward sampled choices that worked better.",
        "everyday_problem": "The problem is that the correct action is not provided; the agent only sees outcomes after trying things.",
        "first_principles_reason": "When choices are sampled, improvement can come from increasing the odds of sampled actions that beat expectations.",
        "mathematical_principle": "The update uses reward-weighted change in log probability. In plain terms: push up the probability of actions that led to better-than-usual results and push down worse ones.",
        "why_it_matters": "It lets agents learn flexible behavior even when actions are continuous or too many to enumerate.",
        "what_breaks_without_it": "Learning is limited to settings where every action value can be directly estimated.",
        "related_concepts": ["policy", "reward", "actor_critic"],
        "primitives": ["feedback", "credit"],
        "keywords": ["policy gradient", "reinforce", "gradient", "log probability", "advantage", "actor"],
    },
    {
        "id": "actor_critic",
        "name": "Actor-Critic",
        "theme": "action_and_consequence",
        "plain_language_definition": "A learner split into a chooser and a judge.",
        "everyday_problem": "The problem is that raw rewards are noisy, so the agent needs a better estimate of whether an action was actually good.",
        "first_principles_reason": "Decision making improves when action choice and outcome evaluation can help each other.",
        "mathematical_principle": "The actor updates the policy; the critic estimates value. The actor asks what to do, and the critic estimates how good the situation or action is.",
        "why_it_matters": "It reduces noise in learning and underlies many practical RL methods.",
        "what_breaks_without_it": "Policy updates can be too unstable or data-hungry for complex environments.",
        "related_concepts": ["policy_gradient", "value_functions", "rl_for_llms"],
        "primitives": ["feedback", "credit"],
        "keywords": ["actor critic", "actor-critic", "critic", "advantage", "value function", "baseline"],
    },
    {
        "id": "q_learning",
        "name": "Q-Learning",
        "theme": "action_and_consequence",
        "plain_language_definition": "Learning a table or function that estimates how good each action is from each situation.",
        "everyday_problem": "The problem is that an agent must choose now while caring about later consequences.",
        "first_principles_reason": "A decision can be valued by immediate payoff plus the value of the future it leads to.",
        "mathematical_principle": "Q(s,a) means the expected future return after taking action a in situation s. The Bellman idea says today's action value equals immediate reward plus the best estimated future value.",
        "why_it_matters": "It is the cleanest route from delayed reward to a practical decision rule.",
        "what_breaks_without_it": "The agent cannot compare actions by their long-term consequences.",
        "related_concepts": ["value_functions", "offline_rl", "credit_assignment"],
        "primitives": ["credit", "search"],
        "keywords": ["q-learning", "q learning", "q-function", "q function", "bellman", "value iteration"],
    },
    {
        "id": "offline_rl",
        "name": "Offline Reinforcement Learning",
        "theme": "action_and_consequence",
        "plain_language_definition": "Learning from logged experience without freely trying new actions during training.",
        "everyday_problem": "The problem is that in medicine, robotics, finance, and deployed systems, unsafe trial and error is not acceptable.",
        "first_principles_reason": "The learner only sees the slice of the world covered by old data, so it must avoid trusting guesses far outside that slice.",
        "mathematical_principle": "The core lever is distribution shift: the learned policy may choose actions unlike the data. Conservative methods penalize or constrain those unsupported choices.",
        "why_it_matters": "It lets RL use large historical datasets where online exploration would be expensive or dangerous.",
        "what_breaks_without_it": "The agent can exploit errors in its own value estimates for actions the dataset barely contains.",
        "related_concepts": ["q_learning", "generalization", "evaluation"],
        "primitives": ["uncertainty", "feedback"],
        "keywords": ["offline rl", "offline reinforcement", "batch rl", "dataset", "out of distribution", "distribution shift"],
    },
    {
        "id": "model_based_rl",
        "name": "Model-Based Reinforcement Learning",
        "theme": "action_and_consequence",
        "plain_language_definition": "Learning or using a simulator of what might happen next.",
        "everyday_problem": "The problem is that real-world trial and error can be slow, costly, or risky.",
        "first_principles_reason": "If the agent can imagine consequences, it can compare possible futures before acting.",
        "mathematical_principle": "A dynamics model estimates next state from current state and action. Planning searches through predicted futures to choose an action.",
        "why_it_matters": "It can make learning more data-efficient and connects RL to control.",
        "what_breaks_without_it": "The agent must learn mainly by direct experience and may waste attempts.",
        "related_concepts": ["planning", "policy", "uncertainty"],
        "primitives": ["search", "uncertainty"],
        "keywords": ["model-based", "model based", "dynamics model", "planning", "transition", "mpc"],
    },
    {
        "id": "exploration",
        "name": "Exploration",
        "theme": "action_and_consequence",
        "plain_language_definition": "Trying actions to learn what would otherwise remain unknown.",
        "everyday_problem": "The problem is that doing the currently best-known thing can prevent the agent from discovering something better.",
        "first_principles_reason": "Information has value. Some actions are useful because they reveal the world, not because they immediately pay off.",
        "mathematical_principle": "Exploration methods add randomness, uncertainty bonuses, or information-seeking objectives so the learner samples more than its current favorite action.",
        "why_it_matters": "It prevents premature habits and makes sparse-reward problems learnable.",
        "what_breaks_without_it": "The system can get stuck repeating a mediocre behavior because it never tests alternatives.",
        "related_concepts": ["policy", "model_based_rl", "generalization"],
        "primitives": ["search", "uncertainty"],
        "keywords": ["exploration", "explore", "epsilon greedy", "intrinsic reward", "curiosity"],
    },
    {
        "id": "rl_for_llms",
        "name": "RL For LLMs",
        "theme": "learning_from_feedback",
        "plain_language_definition": "Using outcome feedback to steer a language model's choices.",
        "everyday_problem": "The problem is that for helpfulness or reasoning, we often know which final answer is better but not the exact next token at every step.",
        "first_principles_reason": "Language generation is a sequence of actions. Feedback on the whole response has to influence many token choices.",
        "mathematical_principle": "The model is treated like a policy over tokens. Rewards or preferences adjust the probability of whole responses and sometimes intermediate reasoning paths.",
        "why_it_matters": "It connects reinforcement learning to instruction following, preference optimization, and reasoning models.",
        "what_breaks_without_it": "A model may imitate text but fail to optimize for useful task outcomes.",
        "related_concepts": ["fine_tuning", "policy", "reasoning_traces"],
        "primitives": ["feedback", "credit", "scale"],
        "keywords": ["rl for llm", "rl for llms", "language model", "reasoning", "rlhf", "grpo", "ppo"],
    },
    {
        "id": "diffusion",
        "name": "Diffusion",
        "theme": "generative_paths",
        "plain_language_definition": "Generating by starting from noise and repeatedly making it more like data.",
        "everyday_problem": "The problem is that realistic images or videos are too complex to create in one jump from a prompt.",
        "first_principles_reason": "A hard generation problem can be broken into many easier cleanup steps.",
        "mathematical_principle": "A forward process adds noise; a learned reverse process removes it. Each step estimates how to move a noisy sample toward the data distribution.",
        "why_it_matters": "It is a major recipe for high-quality image, video, and multimodal generation.",
        "what_breaks_without_it": "Generation must rely on harder one-shot mappings or unstable adversarial training.",
        "related_concepts": ["score_matching", "guidance", "latent_space"],
        "primitives": ["uncertainty", "search"],
        "keywords": ["diffusion", "denoise", "denoising", "noise", "reverse process", "forward process"],
    },
    {
        "id": "score_matching",
        "name": "Score Matching",
        "theme": "generative_paths",
        "plain_language_definition": "Learning which direction points toward more data-like samples.",
        "everyday_problem": "The problem is that the model needs a local compass for improving a noisy sample.",
        "first_principles_reason": "In a complicated space, knowing the direction toward higher probability can be easier than directly describing the whole distribution.",
        "mathematical_principle": "The score is the gradient of log probability. In plain terms, it points toward nearby places the data says are more likely.",
        "why_it_matters": "It gives diffusion models the step-by-step direction used for denoising.",
        "what_breaks_without_it": "The sampler has no learned local direction for turning noise into structure.",
        "related_concepts": ["diffusion", "flow_matching", "guidance"],
        "primitives": ["geometry", "assignment"],
        "keywords": ["score matching", "gradient of log", "log probability", "denoising score", "score model"],
    },
    {
        "id": "flow_matching",
        "name": "Flow Matching",
        "theme": "generative_paths",
        "plain_language_definition": "Learning a smooth path that carries simple samples into data-like samples.",
        "everyday_problem": "The problem is that generation needs a reliable route from an easy starting distribution to a complex target distribution.",
        "first_principles_reason": "Instead of only asking where to denoise next, one can learn a velocity field that moves points along a path.",
        "mathematical_principle": "A vector field assigns a direction and speed to each point. Matching trains that field so its movement transforms simple noise into data.",
        "why_it_matters": "It offers a clean mathematical view of modern generative modeling and connects diffusion to continuous transport.",
        "what_breaks_without_it": "The model loses one of the simplest ways to describe generation as guided motion.",
        "related_concepts": ["diffusion", "score_matching", "latent_space"],
        "primitives": ["geometry", "search"],
        "keywords": ["flow matching", "vector field", "velocity field", "ode", "optimal transport"],
    },
    {
        "id": "guidance",
        "name": "Guidance",
        "theme": "generative_paths",
        "plain_language_definition": "Steering generation toward a prompt, class, reward, or constraint.",
        "everyday_problem": "The problem is that pure generation may create plausible samples that do not match what the user asked for.",
        "first_principles_reason": "Generation needs both freedom and control: enough freedom to make rich outputs, enough constraint to satisfy the condition.",
        "mathematical_principle": "Guidance modifies the update direction during sampling so the path favors samples consistent with the condition.",
        "why_it_matters": "It makes image and video models controllable by text, labels, layouts, or preferences.",
        "what_breaks_without_it": "The model may produce realistic but irrelevant outputs.",
        "related_concepts": ["diffusion", "reward_modeling", "agents_and_tools"],
        "primitives": ["feedback", "search"],
        "keywords": ["guidance", "classifier-free", "classifier free", "conditional generation", "conditioning", "prompt"],
    },
    {
        "id": "latent_space",
        "name": "Latent Space",
        "theme": "generative_paths",
        "plain_language_definition": "A compressed internal space where generation or prediction can happen more cheaply.",
        "everyday_problem": "The problem is that pixels and long sequences are expensive and full of surface detail.",
        "first_principles_reason": "If the model can work in a smaller space that preserves meaning, it can spend computation on structure instead of every raw detail.",
        "mathematical_principle": "An encoder maps data into a smaller vector space, and a decoder maps it back. The useful trick is preserving important variation while discarding nuisance detail.",
        "why_it_matters": "Latent spaces make large vision generation faster and connect images, text, and actions through shared coordinates.",
        "what_breaks_without_it": "Generation and planning may become too expensive at raw resolution.",
        "related_concepts": ["embeddings", "diffusion", "compression"],
        "primitives": ["compression", "geometry"],
        "keywords": ["latent", "latent space", "vae", "autoencoder", "encoder", "decoder"],
    },
    {
        "id": "vision_transformers",
        "name": "Vision Transformers",
        "theme": "representation_workspace",
        "plain_language_definition": "Treating pieces of an image like items that can read from one another.",
        "everyday_problem": "The problem is that an image has many regions, and the important relation may be far apart in the picture.",
        "first_principles_reason": "Images are not just local texture. Shape, object identity, and layout require comparing distant parts.",
        "mathematical_principle": "An image is split into patches, each patch gets a vector, and attention lets patches exchange information.",
        "why_it_matters": "It connects the transformer recipe from language to large vision and multimodal models.",
        "what_breaks_without_it": "The model may depend too heavily on local filters and struggle with global image relationships.",
        "related_concepts": ["attention", "positional_encoding", "latent_space"],
        "primitives": ["composition", "invariance"],
        "keywords": ["vision transformer", "vit", "patch", "patches", "image transformer", "image"],
    },
    {
        "id": "scaling_laws",
        "name": "Scaling Laws",
        "theme": "measurement_limits",
        "plain_language_definition": "Regular patterns in what improves when models, data, and compute grow.",
        "everyday_problem": "The problem is that building large models is expensive, so teams need a way to predict whether more scale is worth it.",
        "first_principles_reason": "Capacity, data, and compute are bottlenecks. When one bottleneck is relaxed, another can become the limiter.",
        "mathematical_principle": "A scaling law fits a curve between resources and loss or capability. The curve is a planning tool, not a law of nature.",
        "why_it_matters": "It guides training budgets and helps explain why some abilities appear only after enough practice and capacity.",
        "what_breaks_without_it": "Scaling decisions become guesswork, and systems may be undertrained or wastefully oversized.",
        "related_concepts": ["pretraining", "emergence", "evaluation"],
        "primitives": ["scale", "feedback"],
        "keywords": ["scaling", "scaling law", "scale", "compute", "parameters", "emergent", "emergence"],
    },
    {
        "id": "generalization",
        "name": "Generalization",
        "theme": "measurement_limits",
        "plain_language_definition": "Doing well on new cases, not only remembered examples.",
        "everyday_problem": "The problem is that a model can learn shortcuts that work in training but fail in the real world.",
        "first_principles_reason": "Past data is only a sample of future situations. Learning must capture stable structure rather than accidental details.",
        "mathematical_principle": "Generalization is the gap between training behavior and behavior on unseen data or environments. Smaller gaps usually mean the learned rule is less tied to accidents of the sample.",
        "why_it_matters": "It is the difference between memorization and useful competence.",
        "what_breaks_without_it": "Benchmarks and demos stop predicting real deployment behavior.",
        "related_concepts": ["evaluation", "offline_rl", "invariance"],
        "primitives": ["invariance", "uncertainty"],
        "keywords": ["generalization", "generalize", "overfit", "overfitting", "train test", "test"],
    },
]


THEMES: list[dict[str, Any]] = [
    {
        "id": "representation_workspace",
        "name": "Representation As A Working Space",
        "big_picture": "Modern models first turn messy inputs into internal coordinates, then do most of their work by moving, comparing, and editing those coordinates.",
        "why_this_theme_matters": "Without this workspace, text, images, states, and actions remain raw surface forms that cannot share computation.",
    },
    {
        "id": "learning_from_feedback",
        "name": "Learning From Feedback",
        "big_picture": "A model improves by turning mistakes, rewards, preferences, or prediction errors into small changes in future behavior.",
        "why_this_theme_matters": "This is the bridge from passive pattern finding to systems that can be steered toward useful outcomes.",
    },
    {
        "id": "action_and_consequence",
        "name": "Action, Time, And Consequence",
        "big_picture": "Reinforcement learning studies what happens when choices change the future evidence the learner will see.",
        "why_this_theme_matters": "It explains why agents, robots, games, and reasoning systems need more than ordinary supervised prediction.",
    },
    {
        "id": "inference_time_work",
        "name": "Thinking As Extra Work At Use Time",
        "big_picture": "Some systems get better by spending more computation after the prompt arrives: writing intermediate steps, searching, calling tools, or revising.",
        "why_this_theme_matters": "It separates stored knowledge from active problem solving.",
    },
    {
        "id": "generative_paths",
        "name": "Generation As Guided Movement",
        "big_picture": "Diffusion, flow, and guidance methods turn generation into a path through possible samples rather than a one-shot guess.",
        "why_this_theme_matters": "It gives a practical way to create complex images and videos while still obeying conditions.",
    },
    {
        "id": "measurement_limits",
        "name": "Measurement, Scale, And Generalization",
        "big_picture": "Scores, scaling curves, and test sets are claims about behavior under chosen conditions, not full descriptions of intelligence.",
        "why_this_theme_matters": "It keeps model development honest about what has actually been demonstrated.",
    },
]


SUBTHEMES: list[dict[str, Any]] = [
    {
        "id": "text_and_patch_interfaces",
        "parent_theme": "representation_workspace",
        "name": "Turning Messy Inputs Into Countable Pieces",
        "concepts": ["tokenization", "vision_transformers"],
        "everyday_problem": "The system needs a first set of pieces before it can compare, remember, or predict anything.",
        "hidden_principle": "Discrete inputs need a stable interface into numerical computation.",
        "mathematical_lever": "Maps from raw objects into IDs or vectors.",
        "why_it_matters": "The first interface controls the burden placed on every later layer.",
    },
    {
        "id": "learned_geometry",
        "parent_theme": "representation_workspace",
        "name": "Making Meaning Into Geometry",
        "concepts": ["embeddings", "latent_space"],
        "everyday_problem": "Related things need to be near enough that arithmetic can share what is learned.",
        "hidden_principle": "Similarity becomes useful only after it is represented as distance or direction.",
        "mathematical_lever": "Vectors, distances, projections, and learned coordinate systems.",
        "why_it_matters": "It lets one model reuse structure across words, images, states, and actions.",
    },
    {
        "id": "selective_context",
        "parent_theme": "representation_workspace",
        "name": "Choosing Which Context Matters",
        "concepts": ["attention", "positional_encoding"],
        "everyday_problem": "The model cannot treat every past detail as equally relevant.",
        "hidden_principle": "Context is useful only when it is selected and weighted.",
        "mathematical_lever": "Similarity scores, normalized weights, and weighted averages.",
        "why_it_matters": "This is the shared mechanism behind long-context language modeling and global image understanding.",
    },
    {
        "id": "stacked_computation",
        "parent_theme": "representation_workspace",
        "name": "Building Depth From Repeated Simple Updates",
        "concepts": ["transformer_block"],
        "everyday_problem": "Hard understanding requires more than one pass over the input.",
        "hidden_principle": "Repeated small transformations can build complex internal state.",
        "mathematical_lever": "Layer composition, residual updates, normalization, and nonlinear maps.",
        "why_it_matters": "It explains why the same block can be scaled into very different modern models.",
    },
    {
        "id": "prediction_as_practice",
        "parent_theme": "learning_from_feedback",
        "name": "Learning Structure By Guessing Missing Pieces",
        "concepts": ["pretraining"],
        "everyday_problem": "There is much more raw data than carefully labeled instruction.",
        "hidden_principle": "A simple prediction game can expose the structure of language, images, and behavior.",
        "mathematical_lever": "Loss functions that measure surprise and gradients that reduce it.",
        "why_it_matters": "It creates the broad base that later systems tune and specialize.",
    },
    {
        "id": "human_feedback",
        "parent_theme": "learning_from_feedback",
        "name": "Turning Preference Into Training Signal",
        "concepts": ["fine_tuning", "reward", "rl_for_llms"],
        "everyday_problem": "People can often say which answer is better even when they cannot write the perfect answer in advance.",
        "hidden_principle": "Comparison can be converted into a direction for changing behavior.",
        "mathematical_lever": "Preference losses, reward models, and policy updates.",
        "why_it_matters": "It explains why useful assistants require more than next-token prediction.",
    },
    {
        "id": "delayed_feedback",
        "parent_theme": "action_and_consequence",
        "name": "Learning When The Result Comes Later",
        "concepts": ["policy", "credit_assignment", "q_learning", "policy_gradient", "actor_critic"],
        "everyday_problem": "The feedback arrives after a chain of choices, so the learner must decide which choice mattered.",
        "hidden_principle": "Cause and reward are separated by time.",
        "mathematical_lever": "Returns, value estimates, advantages, and Bellman-style recursion.",
        "why_it_matters": "It is the core difficulty behind games, robotics, agents, and long reasoning chains.",
    },
    {
        "id": "learning_from_logged_worlds",
        "parent_theme": "action_and_consequence",
        "name": "Learning Safely From Old Experience",
        "concepts": ["offline_rl"],
        "everyday_problem": "The learner may not be allowed to freely experiment in the real world.",
        "hidden_principle": "A dataset only covers part of what could have happened.",
        "mathematical_lever": "Distribution constraints and conservative value estimates.",
        "why_it_matters": "It makes RL relevant when live exploration is risky.",
    },
    {
        "id": "imagined_futures",
        "parent_theme": "action_and_consequence",
        "name": "Using Prediction To Plan Before Acting",
        "concepts": ["model_based_rl", "exploration"],
        "everyday_problem": "Real trial and error is expensive, but imagined trial and error can be cheap.",
        "hidden_principle": "A model of consequences turns acting into searching over possible futures.",
        "mathematical_lever": "Transition models, uncertainty estimates, and planning objectives.",
        "why_it_matters": "It connects reinforcement learning with control and robotics.",
    },
    {
        "id": "scratch_work_and_tools",
        "parent_theme": "inference_time_work",
        "name": "Solving By Writing, Searching, And Acting",
        "concepts": ["reasoning_traces", "agents_and_tools"],
        "everyday_problem": "A hard task may need intermediate notes, outside facts, or tool results.",
        "hidden_principle": "The context can become a temporary workspace that changes as the system works.",
        "mathematical_lever": "Sequential decision loops over generated tokens, actions, and observations.",
        "why_it_matters": "It connects LLM reasoning to agentic systems and RL.",
    },
    {
        "id": "denoising_paths",
        "parent_theme": "generative_paths",
        "name": "Making A Hard Sample By Many Small Corrections",
        "concepts": ["diffusion", "score_matching"],
        "everyday_problem": "A detailed image is too hard to create in one leap.",
        "hidden_principle": "Many small local directions can solve a global generation problem.",
        "mathematical_lever": "Noise schedules, score fields, and reverse sampling.",
        "why_it_matters": "It explains the central mechanism behind diffusion image generation.",
    },
    {
        "id": "continuous_transport",
        "parent_theme": "generative_paths",
        "name": "Moving Samples Along A Learned Route",
        "concepts": ["flow_matching"],
        "everyday_problem": "Generation needs a route from something easy to sample to something realistic.",
        "hidden_principle": "A path through space can be easier to learn than a direct jump.",
        "mathematical_lever": "Vector fields and continuous-time transformations.",
        "why_it_matters": "It reveals the shared geometry behind diffusion and newer flow methods.",
    },
    {
        "id": "controlled_generation",
        "parent_theme": "generative_paths",
        "name": "Balancing Freedom With Instruction",
        "concepts": ["guidance"],
        "everyday_problem": "A model can make something plausible but not the thing requested.",
        "hidden_principle": "Generation must be constrained without freezing all creative variation.",
        "mathematical_lever": "Conditioned scores, guidance weights, and modified sampling directions.",
        "why_it_matters": "It is what makes image and video generation steerable.",
    },
    {
        "id": "scores_are_samples",
        "parent_theme": "measurement_limits",
        "name": "Remembering That Scores Are Partial Views",
        "concepts": ["evaluation", "generalization"],
        "everyday_problem": "A single score can hide what the model cannot do.",
        "hidden_principle": "Every measurement compresses behavior and loses detail.",
        "mathematical_lever": "Metrics, held-out sets, confidence, and failure slicing.",
        "why_it_matters": "It prevents benchmark success from being confused with broad reliability.",
    },
    {
        "id": "what_changes_with_size",
        "parent_theme": "measurement_limits",
        "name": "What Changes When Systems Get Bigger",
        "concepts": ["scaling_laws"],
        "everyday_problem": "Building larger systems is costly, so developers need clues about what scale will buy.",
        "hidden_principle": "Capability depends on bottlenecks among data, compute, architecture, and training objective.",
        "mathematical_lever": "Curves relating resources to loss or observed capability.",
        "why_it_matters": "It turns scale from superstition into a planning question with limits.",
    },
]


METHOD_FAMILIES: list[dict[str, Any]] = [
    {
        "id": "transformer_family",
        "name": "Transformer Family",
        "first_principles_problem": "How can every part of an input read the parts that matter without a hand-written rule for where to look?",
        "core_move": "Use attention as a reusable lookup operation, then stack that operation many times.",
        "mathematical_primitive": ["assignment", "composition", "geometry"],
        "concepts": ["attention", "positional_encoding", "transformer_block", "vision_transformers"],
        "plain_language_family_summary": "This family treats language and images as collections of pieces that repeatedly exchange information.",
        "evidence_concepts": ["attention", "transformer_block", "vision_transformers"],
    },
    {
        "id": "pretrain_then_adapt_family",
        "name": "Pretrain-Then-Adapt Family",
        "first_principles_problem": "How can a system learn broad structure from abundant data and then become useful for narrower human tasks?",
        "core_move": "First learn from a cheap prediction game, then steer the model with examples, preferences, or rewards.",
        "mathematical_primitive": ["feedback", "scale"],
        "concepts": ["pretraining", "fine_tuning", "rl_for_llms", "evaluation"],
        "plain_language_family_summary": "This family separates broad practice from later behavioral shaping.",
        "evidence_concepts": ["pretraining", "fine_tuning", "rl_for_llms"],
    },
    {
        "id": "agentic_llm_family",
        "name": "Agentic LLM And Retrieval Family",
        "first_principles_problem": "How can a model solve tasks that need fresh information, external tools, or multiple attempts?",
        "core_move": "Wrap prediction in a loop of action, observation, and context update.",
        "mathematical_primitive": ["search", "feedback", "composition"],
        "concepts": ["reasoning_traces", "agents_and_tools", "policy", "evaluation"],
        "plain_language_family_summary": "This family turns a language model from a one-shot answerer into a step-by-step worker.",
        "evidence_concepts": ["reasoning_traces", "agents_and_tools"],
    },
    {
        "id": "value_based_rl_family",
        "name": "Value-Based RL Family",
        "first_principles_problem": "How can an agent choose now when the value of the choice depends on what happens later?",
        "core_move": "Estimate the long-term value of actions and choose actions using that estimate.",
        "mathematical_primitive": ["credit", "search"],
        "concepts": ["q_learning", "credit_assignment", "offline_rl"],
        "plain_language_family_summary": "This family makes delayed consequences comparable by assigning numbers to state-action choices.",
        "evidence_concepts": ["q_learning", "credit_assignment"],
    },
    {
        "id": "policy_optimization_family",
        "name": "Policy Optimization Family",
        "first_principles_problem": "How can a learner improve a behavior rule when it only observes sampled attempts?",
        "core_move": "Increase the chance of actions that led to better outcomes and reduce the chance of worse ones.",
        "mathematical_primitive": ["feedback", "credit"],
        "concepts": ["policy", "reward", "policy_gradient", "actor_critic", "rl_for_llms"],
        "plain_language_family_summary": "This family directly changes the chooser rather than only estimating a table of action values.",
        "evidence_concepts": ["policy_gradient", "actor_critic", "rl_for_llms"],
    },
    {
        "id": "safe_or_data_limited_rl_family",
        "name": "Safe Or Data-Limited RL Family",
        "first_principles_problem": "How can an agent learn when new experiments are expensive, unsafe, or unavailable?",
        "core_move": "Use logged data, conservative estimates, or imagined rollouts while accounting for uncertainty.",
        "mathematical_primitive": ["uncertainty", "feedback", "search"],
        "concepts": ["offline_rl", "model_based_rl", "exploration", "evaluation"],
        "plain_language_family_summary": "This family is about learning under limited access to the real world.",
        "evidence_concepts": ["offline_rl", "model_based_rl", "exploration"],
    },
    {
        "id": "denoising_diffusion_family",
        "name": "Denoising Diffusion Family",
        "first_principles_problem": "How can a model create a complex sample without producing every detail correctly in one step?",
        "core_move": "Start with noise and learn many small corrections toward data.",
        "mathematical_primitive": ["uncertainty", "search", "geometry"],
        "concepts": ["diffusion", "score_matching", "guidance", "latent_space"],
        "plain_language_family_summary": "This family makes generation a controlled cleanup process.",
        "evidence_concepts": ["diffusion", "score_matching", "guidance"],
    },
    {
        "id": "flow_and_transport_family",
        "name": "Flow And Transport Family",
        "first_principles_problem": "How can simple samples be moved smoothly into realistic samples?",
        "core_move": "Learn a field of directions and speeds that carries points through a path.",
        "mathematical_primitive": ["geometry", "search"],
        "concepts": ["flow_matching", "score_matching", "diffusion", "latent_space"],
        "plain_language_family_summary": "This family views generation as learned motion through a space of possibilities.",
        "evidence_concepts": ["flow_matching", "score_matching"],
    },
    {
        "id": "measurement_and_scaling_family",
        "name": "Measurement And Scaling Family",
        "first_principles_problem": "How can builders know whether a model is improving and what more resources will buy?",
        "core_move": "Use tests, curves, and failure slices while remembering that every measurement is partial.",
        "mathematical_primitive": ["scale", "uncertainty", "invariance"],
        "concepts": ["evaluation", "scaling_laws", "generalization"],
        "plain_language_family_summary": "This family is about turning claims of progress into inspectable evidence.",
        "evidence_concepts": ["evaluation", "scaling_laws", "generalization"],
    },
]


def load_index() -> list[dict[str, Any]]:
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def parse_vtt_segments(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    segments: list[dict[str, str]] = []
    start = end = None
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if "-->" in line:
            if start and lines:
                segments.append({"start": start, "end": end or start, "text": " ".join(lines)})
            start, end = [part.strip().split(" ")[0] for part in line.split("-->", 1)]
            lines = []
        elif line and line != "WEBVTT" and not line.startswith(("Kind:", "Language:")) and not re.match(r"^[0-9]+$", line):
            line = re.sub(r"<[^>]+>", "", line)
            line = re.sub(r"\s+", " ", line).strip()
            if line:
                lines.append(line)
    if start and lines:
        segments.append({"start": start, "end": end or start, "text": " ".join(lines)})
    return segments


def keyword_hits(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(len(re.findall(r"(?<![a-z0-9-])" + re.escape(k.lower()) + r"(?![a-z0-9-])", lowered)) for k in keywords)


def matched_terms(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    terms = [
        keyword
        for keyword in keywords
        if re.search(r"(?<![a-z0-9-])" + re.escape(keyword.lower()) + r"(?![a-z0-9-])", lowered)
    ]
    return terms[:8]


def best_evidence_for_concept(concept: dict[str, Any], index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = []
    allowed_courses = ALLOWED_EVIDENCE_COURSES.get(concept["id"])
    for row in index:
        if allowed_courses and row["course_slug"] not in allowed_courses:
            continue
        clean_path = ROOT / row["clean_txt"]
        text = clean_path.read_text(encoding="utf-8", errors="ignore") if clean_path.exists() else ""
        hits = keyword_hits(text, concept["keywords"])
        title_bonus = keyword_hits(row["expected_title"], concept["keywords"]) * 12
        course_bonus = 0
        if concept["theme"] == "generative_paths" and "cme296" in row["course_slug"]:
            course_bonus = 5
        if concept["theme"] in {"action_and_consequence", "learning_from_feedback"} and "cs224r" in row["course_slug"]:
            course_bonus = 5
        if concept["theme"] in {"representation_workspace", "inference_time_work"} and "cme295" in row["course_slug"]:
            course_bonus = 5
        score = hits + title_bonus + course_bonus
        if score > 0:
            scored.append((score, hits, row))
    scored.sort(key=lambda item: item[0], reverse=True)

    evidence = []
    used_courses: set[str] = set()
    for score, hits, row in scored:
        if len(evidence) >= 6:
            break
        if row["course_slug"] in used_courses and len(evidence) < 3:
            continue
        vtt_path = ROOT / row["raw_vtt"]
        timestamp_start = timestamp_end = None
        local_terms: list[str] = []
        for seg in parse_vtt_segments(vtt_path):
            if keyword_hits(seg["text"], concept["keywords"]):
                timestamp_start, timestamp_end = seg["start"], seg["end"]
                local_terms = matched_terms(seg["text"], concept["keywords"])
                break
        if not local_terms:
            local_terms = matched_terms(text + " " + row["expected_title"], concept["keywords"])
        evidence.append(
            {
                "course": row["course_slug"],
                "video_title": row["title"],
                "transcript_path": row["clean_txt"],
                "timestamp_start": timestamp_start,
                "timestamp_end": timestamp_end,
                "matched_terms": local_terms,
                "keyword_hits": hits,
                "confidence": "strong" if hits >= 20 else "moderate" if hits >= 5 else "weak",
            }
        )
        used_courses.add(row["course_slug"])
    return evidence


def evidence_note(concept: dict[str, Any], row: dict[str, Any]) -> str:
    terms = ", ".join(row["matched_terms"][:4]) or "title-level course cues"
    location = f"around {row['timestamp_start']}" if row.get("timestamp_start") else "in this lecture"
    return (
        f"{location}, the lecture uses {terms} while covering {concept['name']}. "
        f"This supports the scoped claim that {concept['plain_language_definition'][0].lower()}"
        f"{concept['plain_language_definition'][1:]}"
    )


def build() -> None:
    index = load_index()
    evidence_records: list[dict[str, Any]] = []
    concept_outputs: list[dict[str, Any]] = []
    evidence_by_concept: dict[str, list[str]] = defaultdict(list)

    for concept in CONCEPTS:
        matches = best_evidence_for_concept(concept, index)
        for i, match in enumerate(matches, 1):
            evidence_id = f"ev-{concept['id']}-{i:02d}"
            evidence_records.append(
                {
                    "id": evidence_id,
                    "course": match["course"],
                    "video_title": match["video_title"],
                    "transcript_path": match["transcript_path"],
                    "timestamp_start": match["timestamp_start"],
                    "timestamp_end": match["timestamp_end"],
                    "paraphrased_claim": evidence_note(concept, match),
                    "evidence_basis": "local VTT timestamp cue" if match["timestamp_start"] else "clean transcript keyword cue",
                    "evidence_scope": "supports the listed concept and subtheme; broader first-principles explanation remains synthesis",
                    "matched_terms": match["matched_terms"],
                    "supports_concepts": [concept["id"]],
                    "supports_subthemes": [s["id"] for s in SUBTHEMES if concept["id"] in s["concepts"]],
                    "confidence": match["confidence"],
                    "keyword_hits": match["keyword_hits"],
                }
            )
            evidence_by_concept[concept["id"]].append(evidence_id)

        out = {k: v for k, v in concept.items() if k not in {"keywords", "theme", "primitives"}}
        out["theme_id"] = concept["theme"]
        out["mathematical_primitives"] = concept["primitives"]
        out["course_evidence_ids"] = evidence_by_concept[concept["id"]]
        out["evidence_status"] = "transcript-backed" if evidence_by_concept[concept["id"]] else "needs review"
        concept_outputs.append(out)

    coverage_by_theme: dict[str, Counter[str]] = defaultdict(Counter)
    for concept in CONCEPTS:
        for ev_id in evidence_by_concept[concept["id"]]:
            ev = next(record for record in evidence_records if record["id"] == ev_id)
            coverage_by_theme[concept["theme"]][ev["course"]] += 1

    theme_outputs = []
    for theme in THEMES:
        subthemes = [s["id"] for s in SUBTHEMES if s["parent_theme"] == theme["id"]]
        concepts = [c["id"] for c in CONCEPTS if c["theme"] == theme["id"]]
        theme_outputs.append(
            {
                **theme,
                "subthemes": subthemes,
                "core_concepts": concepts,
                "course_coverage": dict(coverage_by_theme[theme["id"]]),
            }
        )

    subtheme_outputs = []
    for subtheme in SUBTHEMES:
        examples = []
        for concept_id in subtheme["concepts"]:
            for ev_id in evidence_by_concept[concept_id][:2]:
                ev = next(record for record in evidence_records if record["id"] == ev_id)
                examples.append(
                    {
                        "concept": concept_id,
                        "evidence_id": ev_id,
                        "course": ev["course"],
                        "video_title": ev["video_title"],
                        "timestamp_start": ev["timestamp_start"],
                    }
                )
        subtheme_outputs.append(
            {
                **subtheme,
                "examples_from_courses": examples,
                "connected_concepts": sorted(
                    {
                        related
                        for concept in CONCEPTS
                        if concept["id"] in subtheme["concepts"]
                        for related in concept["related_concepts"]
                    }
                ),
            }
        )

    primitives = []
    for primitive in PRIMITIVES:
        primitive = dict(primitive)
        primitive["concepts_in_atlas"] = [c["id"] for c in CONCEPTS if primitive["id"] in c["primitives"]]
        primitives.append(primitive)

    write_json(ROOT / "analysis/concepts/concept-atlas.json", concept_outputs)
    write_json(ROOT / "analysis/themes/theme-map.json", theme_outputs)
    write_json(ROOT / "analysis/themes/subtheme-map.json", subtheme_outputs)
    write_json(ROOT / "analysis/evidence/evidence-ledger.json", evidence_records)
    write_json(ROOT / "analysis/throughlines/primitives.json", primitives)
    write_json(ROOT / "analysis/throughlines/method-families.json", build_method_families(evidence_by_concept))
    write_big_picture(theme_outputs, subtheme_outputs, primitives)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_method_families(evidence_by_concept: dict[str, list[str]]) -> list[dict[str, Any]]:
    outputs = []
    for family in METHOD_FAMILIES:
        evidence_ids = []
        for concept_id in family["evidence_concepts"]:
            evidence_ids.extend(evidence_by_concept.get(concept_id, [])[:2])
        output = dict(family)
        output["course_evidence_ids"] = evidence_ids
        output["evidence_status"] = "transcript-backed method family" if evidence_ids else "needs review"
        outputs.append(output)
    return outputs


def write_big_picture(themes: list[dict[str, Any]], subthemes: list[dict[str, Any]], primitives: list[dict[str, Any]]) -> None:
    lines = [
        "# Big-Picture Map",
        "",
        "This synthesis is built from the Stanford transcript corpus, but it is not a lecture summary. It maps recurring ideas across transformers, reinforcement learning, diffusion, and large vision models.",
        "",
        "## The Few Deep Ideas",
        "",
        "1. Learning systems need a working space. Text, images, actions, and rewards first have to become numbers that preserve useful relationships.",
        "2. Useful behavior comes from feedback. The feedback may be prediction error, a human preference, a reward, or a benchmark score, but the shared pattern is the same: try, compare, update.",
        "3. Time makes learning harder. In reinforcement learning and reasoning, the important cause may happen many steps before the visible result.",
        "4. Generation is movement under constraint. Diffusion and flow models turn sample creation into a path from simple uncertainty toward structured output.",
        "5. Measurement is always partial. A benchmark, loss curve, or reward model compresses behavior into a signal and therefore hides some failures.",
        "",
        "## What Each Course Adds",
        "",
        "- CME295 adds the language-model view: tokens, embeddings, attention, transformer blocks, tuning, reasoning, agents, and evaluation.",
        "- CS224R adds the action-over-time view: policy, reward, delayed feedback, value, exploration, offline learning, planning, robotics, and RL for LLMs.",
        "- CME296 adds the generative-path view: diffusion, score matching, flow matching, guidance, latent spaces, architectures, training, and evaluation for large vision models.",
        "",
        "## Where The Courses Emphasize Different Intuitions",
        "",
        "CME295 often treats intelligence as context-dependent prediction and tool use. CS224R treats intelligence as choosing actions whose consequences unfold over time. CME296 treats generation as controlled motion through a high-dimensional space. These are not separate stories: they reuse the same primitives of representation, feedback, search, uncertainty, and scale.",
        "",
        "## Recurring Mathematical Primitives",
        "",
    ]
    for primitive in primitives:
        lines.append(f"- **{primitive['name']}**: {primitive['plain_language']}")
    lines.extend(["", "## Themes", ""])
    sub_by_theme = defaultdict(list)
    for sub in subthemes:
        sub_by_theme[sub["parent_theme"]].append(sub)
    for theme in themes:
        lines.extend([f"### {theme['name']}", "", theme["big_picture"], "", f"Why it matters: {theme['why_this_theme_matters']}", ""])
        for sub in sub_by_theme[theme["id"]]:
            lines.append(f"- {sub['name']}: {sub['everyday_problem']}")
        lines.append("")
    (ROOT / "analysis/throughlines/big-picture-map.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build()
