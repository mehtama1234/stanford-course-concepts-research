# Stanford AI Concept Lab — verified measured results

Numbers below were computed by programs we actually ran. Cite them verbatim; never invent new ones.
- Group A (transformers/LLM): REAL pretrained GPT-2 (124M). Script: scripts/experiments/stanford_gpt2.py
- Group B (reinforcement learning): a small gridworld + bandit. Script: scripts/experiments/stanford_rl.py
- Group C (diffusion family): a 2D toy (8 Gaussians on a ring; two class-blobs). Script: scripts/experiments/stanford_diffusion.py
- Group D (LLM reasoning/agents): REAL Qwen3-0.6B runs from the reasoning-from-scratch lab (see reasoning notes at the bottom).

=======================================================================
GROUP A — real GPT-2 (124M), scripts/experiments/stanford_gpt2.py
=======================================================================

## attention (concept: attention)
- A 13-token sentence. If attention were a flat average, each token would get 0.077 of the weight and
  the spread (entropy) would be 2.56. Measured: the single most-attended token gets **0.73** of the
  weight; mean attention entropy is **0.84**, far below the flat 2.56.
- Insight: attention concentrates — it picks out a few relevant tokens rather than averaging everything.

## embeddings (concept: embeddings)
- Each of GPT-2's 50,257 tokens is a point in **768-dimensional** space. Cosine similarities between the
  input vectors (higher = closer in meaning): king/queen **0.66**, king/man **0.37**, dog/cat **0.55**,
  king/bicycle **0.22**, Monday/Tuesday **0.89**.
- Insight: related words sit close together, unrelated ones far apart — meaning became geometry, with no
  rule ever written by hand.

## positional_encoding (concept: positional_encoding)
- Same ten words, correct order -> loss **3.98**. The SAME words shuffled -> loss **8.00** (far worse).
- GPT-2's learned position vectors: neighbouring positions have cosine **1.00**, distant positions **0.39**.
- Insight: without a sense of order, language collapses — position carries real meaning.

## tokenization (concept: tokenization)
- Vocabulary: **50,257** pieces. Token counts: "cat" 1, "running" 1, "unbelievable" 1, "tokenization" 2,
  "antidisestablishmentarianism" **5** pieces, split as **ant / idis / establishment / arian / ism**.
- Insight: words are built from reusable sub-word pieces; common words are one piece, rare words are
  assembled from several.

## transformer_block (concept: transformer_block)
- The "logit lens": track where the token the model will finally choose sits in the ranking of all
  **50,257** words, after each of the **12** layers. It climbs from rank **32,406** (buried) after layer 0,
  to rank **2** by layer 6, to rank **1** at layer 12.
- Insight: each block refines the guess; the answer is not computed at once but sharpened layer by layer.

## pretraining (concept: pretraining)
- On a held-out sentence it was never explicitly taught: average surprise (loss) **3.38**, perplexity
  **29.3**; it names the exact next word **30%** of the time (out of 50,257 choices).
- Insight: one simple goal — predict the next piece — trained on oceans of text is enough to learn grammar,
  facts, and style.

## scaling_laws (concept: scaling_laws)
- Same sentence, three real model sizes, perplexity (lower = less surprised): distilgpt2 (82M params)
  **53.4**, gpt2 (124M) **30.2**, gpt2-medium (355M) **27.0**.
- Insight: bigger models are predictably less surprised — capability improves smoothly and forecastably
  with scale.

## generalization (concept: generalization)
- A brand-new but grammatical sentence -> loss **6.24** (comfortable). A string of random tokens ->
  loss **13.71** (lost).
- Insight: the model generalized the RULES of language to sentences it never saw; it did not memorize
  strings — random noise, which has no rules, leaves it lost.

## latent_space (concept: latent_space)
- The word "bank" in two sentences (river bank vs money bank). Centered cosine of its vector: at the
  input layer **0.98** (nearly identical start, same token), after 12 layers of context **0.51**
  (pulled apart).
- Insight: context reshapes a word's vector — the deep representation is contextual, so "bank" splits into
  two different meanings.

## vision_transformers (concept: vision_transformers)
- A 32x32 image is cut into **16** patches; **4** contain the object. Treating patches as tokens and
  running one self-attention pass, an object patch sends **0.46** of its attention to the other object
  patches (blind chance would be **0.25**).
- Insight: an image becomes a sentence of patches, and the same attention mechanism makes like attend to
  like — this is how a vision transformer sees. (This demo uses untrained patch attention to show the
  mechanism; a trained ViT learns far sharper groupings.)

=======================================================================
GROUP B — reinforcement learning, scripts/experiments/stanford_rl.py
(a 6x6 gridworld: -1 per step, +10 at the goal; optimal path = 10 steps)
=======================================================================

## q_learning (concept: q_learning)
- First 10 episodes averaged **56** steps to stumble to the goal; after training the greedy path is
  **10** steps (optimal is **10**).
- Insight: by tracking the value of each move and updating from experience, the agent goes from random
  flailing to the optimal route.

## policy (concept: policy)
- A RANDOM policy averages a return of **-122** (wanders, racks up step penalties). A GOOD policy scores
  **+1** — the highest possible on the 10-step path.
- Insight: the policy — the rule mapping situation to action — is the whole thing being learned; same
  world, the rule is everything.

## policy_gradient (concept: policy_gradient)
- On a 4x4 grid, at the start the four directions are a coin-flip, so the two goal-ward moves together
  hold **0.50** of the probability. After training by trial and error, the probability on the goal-ward
  moves rose to **0.86**, and average return climbed from **-15** to **-8**.
- Insight: policy gradient directly raises the probability of the moves that paid off (and lowers the rest).

## actor_critic (concept: actor_critic)
- Same policy-gradient method, with and without a critic (a running value estimate used as a baseline),
  4x4 grid, median of 7 runs: plain policy gradient reaches goal-ward probability **0.86** and final
  return **-8**; adding a critic reaches goal-ward probability **1.00** and final return **+5** (optimal is 5).
- Insight: the critic subtracts a running estimate of "expected" reward so the learning signal is just the
  surprise — this sharpens it and gets all the way to optimal where plain policy gradient stalled.

## exploration (concept: exploration)
- A 5-arm bandit where arm 4 is best. Over 50 runs, share that end up identifying the best arm: pure
  greedy (never explores) **0%**; explore 10% of the time **100%**.
- Insight: you cannot choose the best option you never tried — a little deliberate exploration is the
  difference between always missing the best arm and always finding it.

## reward (concept: reward)
- On an 8x8 grid, episodes until the greedy path is optimal (median of 9 runs): sparse reward (only +10
  at the goal) **26**; shaped reward (a small crumb for each step that gets warmer) **18**.
- Insight: the reward signal you design is the behavior you get — a well-shaped reward reaches the goal
  faster (and a badly designed one can teach the wrong thing entirely).

## credit_assignment (concept: credit_assignment)
- Episodes until the far-off reward propagates back to the START state (median of 9 runs): one-step credit
  (eligibility traces off) **6**; eligibility traces (spread credit along the whole path) **2**.
- Insight: when a reward comes only at the end, the hard part is deciding which earlier moves deserve the
  credit; traces spread it back along the path so learning reaches the start far sooner.

## model_based_rl (concept: model_based_rl)
- Real environment steps used to solve the maze (median of 5 runs): model-free (learn values purely by
  trial and error) **705**; model-based (learn the map from ~300 steps, then plan in your head with it)
  **300**.
- Insight: learning how the world works and then planning against that internal model is far more
  sample-efficient than blind trial and error.

## offline_rl (concept: offline_rl)
- Trained ONLY on a fixed, biased log (**65 of 144** state-action pairs ever appeared): a naive copy of
  online Q-learning **never reaches the goal** (it trusts optimistic values for actions it never saw),
  while a conservative method that stays within the logged actions finds the **10**-step optimal path.
- Insight: learning from a fixed dataset with no new interaction is haunted by the unseen — you must not
  trust value estimates for actions absent from the data.

=======================================================================
GROUP C — diffusion family, scripts/experiments/stanford_diffusion.py
(target: 8 Gaussians on a ring; "on the target shape" = within a small radius of a mode)
=======================================================================

## diffusion (concept: diffusion)
- Pure noise lands on the target shape **0%** of the time. After learning to reverse a **50**-step
  noising process (predict-the-noise, then denoise), generated samples land on it **97%** of the time.
- Insight: destroy structure with noise step by step, train a network to undo one step, and you can
  generate new data by denoising pure noise back into the shape.

## score_matching (concept: score_matching)
- After learning the "score" (the direction of increasing data density) and following it by a guided
  random walk (Langevin dynamics), samples settle onto the target shape **79%** of the time.
- Insight: instead of the density itself, learn which way is "uphill" toward the data everywhere; then
  walking uphill (with noise) carries random points onto the data.

## flow_matching (concept: flow_matching)
- After learning a velocity field that flows noise straight to data, integrating it in just **10** steps
  lands **84%** on the target; even **4** steps lands **65%**.
- Insight: learn a smooth current from noise to data along straight paths, and generating is just
  following the current — because the paths are straight it needs very few steps.

## guidance (concept: guidance)
- Two overlapping classes (left/right blobs). Asking for the right-hand class: with NO guidance (ignore
  the label) **51%** of samples land on it (a coin flip) at mean distance **2.30** from its center; adding
  the guidance direction (the conditional-minus-unconditional push) sends **100%** to it at mean distance
  **0.73**.
- Insight: steer the sampler toward what you asked for by adding the "toward this class" direction; it
  turns a coin flip into reliably obeying the request. (How hard you push is the guidance strength, a
  fidelity-vs-variety dial.)

=======================================================================
GROUP D — LLM reasoning/agents: REAL Qwen3-0.6B runs (reasoning-from-scratch lab)
Small model on GSM8K grade-school math, graded against gold answers. Cite verbatim.
=======================================================================

## reasoning_traces (concept: reasoning_traces)
- Over 30 real GSM8K problems: answering directly **14/30**; letting the model write a chain of thought
  first **18/30** (rescued 4, broke 0). Average length grew from 226 tokens to 1449; 12/30 thinking traces
  hit the 2048-token limit without settling.
- Insight: writing out intermediate steps ("thinking") reliably helps a small model (14->18) but is not
  magic — it still misses the hardest ones and rambles to the limit.

## evaluation (concept: evaluation)
- The SAME 25 reasoning traces, graded four different ways: exact string match **0/25 (0%)**; "the right
  number appears somewhere" **16/25 (64%)**; "last number in the text" **10/25 (40%)**; "the final boxed
  answer, read carefully" **11/25 (44%)**.
- Insight: one model, four graders, four scores. How you measure the answer is a design decision — a
  lenient grader (64%) is easy to fool; the careful grader (44%) is the trustworthy one.

## fine_tuning (concept: fine_tuning)
- Fine-tuning the small model by imitation (distillation) on a strong teacher's worked solutions, accuracy
  by epoch: **base 10% -> 35% -> peak 65% -> 50%** (slight over-fit). Answer length stayed full
  (~840 tokens at the end) — it never collapsed.
- Insight: fine-tuning on good demonstrations reshapes the model's behavior fast (10% to 65%) and stably —
  this imitation route is why most small reasoning models are trained this way.

## rl_for_llms (concept: rl_for_llms)
- Reinforcement learning (a plain right/wrong reward) on the same model, accuracy at steps 0/500/3000/9000:
  **5% -> 50% -> 15% -> 15%**. Average answer length: **21 -> 236 -> 8 -> 7** tokens.
- Insight: reward first grew real reasoning (5%->50%, 236-token solutions), then got reward-hacked back down
  — the model learned to emit a lone boxed guess that sometimes hits. RL for language models is powerful
  but fragile without safeguards (a KL "leash" keeps solutions from collapsing).

## agents_and_tools (concept: agents_and_tools)
- The small model counts "how many r's in strawberry" as **1** when answering cold (wrong, 21 tokens) but
  **3** when it thinks first (correct, 336 tokens) — it is unreliable at exact operations. Across GSM8K,
  arithmetic slips are a common failure. Giving the model self-checking loops (self-refine improved
  accuracy 42% -> 58% over two revision rounds, fixing 2 and breaking 0) or exact external tools targets
  precisely this weakness.
- Insight: a language model is a fluent guesser, not a calculator — wrapping it in tools and checking loops
  (an "agent") supplies the exact, verifiable steps it cannot reliably do in its head.
