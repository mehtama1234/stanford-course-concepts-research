# Evidence Fidelity Report

This audit separates transcript anchoring from editorially reviewed evidence. A record can have a timestamp and still need manual review if its explanatory payload was generated from local cues rather than hand-selected lecture argument.

## Counts

- Published evidence records: 94
- Published manual deepened records: 94
- Published generated records: 0
- Unpublished generated transcript-cue records in review queue: 0
- Discarded generated transcript-cue records: 37
- Review-queue generated records: 0
- Template-style example records still published: 0
- Published generated records incorrectly marked strong: 0
- Published records missing useful local transcript windows: 0

## Confidence Counts

- moderate: 23
- strong: 60
- weak: 11

## Evidence Basis Counts

- local VTT timestamp cue: 94

## Remaining Review Queue


## Discarded Records

- ev-tokenization-02 (tokenization) — The span uses rare token in a personalization prompt context but does not explain tokenization as the text-to-units interface.
- ev-embeddings-01 (embeddings) — The span mentions representation while discussing an SDE transition, but it does not explain embeddings or learned coordinate tables.
- ev-embeddings-03 (embeddings) — The span mentions a continuous vector task descriptor, which is too general to support the embeddings concept page.
- ev-attention-03 (attention) — The span only name-checks self-attention in a paper comparison and does not explain the attention mechanism.
- ev-attention-06 (attention) — The span uses attention in an everyday strategy-selection sense and is too thin for the transformer attention concept.
- ev-transformer_block-02 (transformer_block) — The span only states that transformers were a landmark paper family and does not explain the block mechanism.
- ev-transformer_block-03 (transformer_block) — The span discusses per-task normalization in RL, which is not enough support for transformer block composition.
- ev-transformer_block-04 (transformer_block) — The record lacks a local VTT window and is based only on clean transcript keyword cues.
- ev-transformer_block-05 (transformer_block) — The matched term is a physical block in a robotics example, not a transformer block.
- ev-evaluation-06 (evaluation) — The span mentions a metric in tuning but does not provide enough detail about evaluation as measurement.
- ev-credit_assignment-02 (credit_assignment) — The span mentions discounted return for multi-task replay buffers but does not explain credit assignment directly.
- ev-credit_assignment-03 (credit_assignment) — The tutorial span mentions discount factor and horizon only as review parameters, with too little conceptual payload.
- ev-credit_assignment-05 (credit_assignment) — The span states gamma equals one in a setting but does not explain credit assignment or delayed consequence.
- ev-credit_assignment-06 (credit_assignment) — The record lacks a local VTT window and is based only on clean transcript keyword cues.
- ev-policy_gradient-04 (policy_gradient) — The span name-checks REINFORCE and vanilla policy gradient while contrasting offline data, but does not explain the estimator.
- ev-policy_gradient-05 (policy_gradient) — The span name-checks PPO, SAC, actor-critic, and value fitting but is too broad to support policy-gradient mechanics.
- ev-actor_critic-06 (actor_critic) — The span says another method learned a value function and Q function, but does not explain actor-critic.
- ev-q_learning-02 (q_learning) — The span is only a tutorial welcome and overview cue, not a substantive Q-learning argument.
- ev-offline_rl-02 (offline_rl) — The span uses dataset as a task descriptor in meta-RL, which is too indirect for offline RL evidence.
- ev-offline_rl-06 (offline_rl) — The span briefly name-checks offline RL as a future topic but does not explain the fixed-dataset problem.
- ev-model_based_rl-04 (model_based_rl) — The span lists model-based RL in a course overview without explaining learned dynamics or planning.
- ev-exploration-06 (exploration) — The span gives a navigation example with a wrong turn but is too fragmentary to support exploration as a concept.
- ev-diffusion-02 (diffusion) — The span is a lecture greeting and title cue, not evidence for the diffusion mechanism.
- ev-score_matching-05 (score_matching) — The span lists diffusion, score matching, and flow matching as topics but does not explain score matching.
- ev-score_matching-06 (score_matching) — The span mentions score matching as one item in a list of paradigms and shared inputs, without a score-field explanation.
- ev-flow_matching-03 (flow_matching) — The span contrasts SDE and ODE but is too local and incomplete to support the flow matching page by itself.
- ev-guidance-03 (guidance) — The span says prompts can be complicated, but does not explain guidance as a sampling or conditioning mechanism.
- ev-guidance-06 (guidance) — The span introduces prompts at a setup level, which is weaker than other published guidance evidence already in the ledger.
- ev-latent_space-02 (latent_space) — The span only points back to the latent space and guidance lecture title, without explaining the latent-space mechanism.
- ev-latent_space-06 (latent_space) — The record lacks a local VTT window and is based only on clean transcript keyword cues.
- ev-vision_transformers-01 (vision_transformers) — The span discusses denoising an image and is not evidence for vision transformer architecture.
- ev-scaling_laws-03 (scaling_laws) — The span mentions learnable parameters locally but does not discuss scale, scaling laws, or resource tradeoffs.
- ev-scaling_laws-04 (scaling_laws) — The span mentions emergence of multimodal LLMs but does not connect emergence to scaling evidence.
- ev-scaling_laws-05 (scaling_laws) — The span mentions policy parameters in an RL algorithm recap, not scaling laws or model-size behavior.
- ev-scaling_laws-06 (scaling_laws) — The span refers to a small-scale exercise but is too incomplete to support scaling-law claims.
- ev-generalization-03 (generalization) — The span fragment mentions test time but does not provide enough context for a generalization argument.
- ev-generalization-05 (generalization) — The span mentions generalization capabilities but is too brief to support the generalization concept page.
