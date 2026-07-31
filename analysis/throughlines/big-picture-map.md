# Big-Picture Map

This synthesis is built from the Stanford transcript corpus, but it is not a lecture summary. It maps recurring ideas across transformers, reinforcement learning, diffusion, and large vision models.

## The Few Deep Ideas

1. Learning systems need a working space. Text, images, actions, and rewards first have to become numbers that preserve useful relationships.
2. Useful behavior comes from feedback. The feedback may be prediction error, a human preference, a reward, or a benchmark score, but the shared pattern is the same: try, compare, update.
3. Time makes learning harder. In reinforcement learning and reasoning, the important cause may happen many steps before the visible result.
4. Generation is movement under constraint. Diffusion and flow models turn sample creation into a path from simple uncertainty toward structured output.
5. Measurement is always partial. A benchmark, loss curve, or reward model compresses behavior into a signal and therefore hides some failures.

## What Each Course Adds

- CME295 adds the language-model view: tokens, embeddings, attention, transformer blocks, tuning, reasoning, agents, and evaluation.
- CS224R adds the action-over-time view: policy, reward, delayed feedback, value, exploration, offline learning, planning, robotics, and RL for LLMs.
- CME296 adds the generative-path view: diffusion, score matching, flow matching, guidance, latent spaces, architectures, training, and evaluation for large vision models.

## Where The Courses Emphasize Different Intuitions

CME295 often treats intelligence as context-dependent prediction and tool use. CS224R treats intelligence as choosing actions whose consequences unfold over time. CME296 treats generation as controlled motion through a high-dimensional space. These are not separate stories: they reuse the same primitives of representation, feedback, search, uncertainty, and scale.

## Recurring Mathematical Primitives

- **Compression**: Keep the parts that matter for the next decision and let go of the rest.
- **Assignment**: Decide which piece of evidence should be connected to which cause, label, action, or memory.
- **Credit**: Decide which earlier choice deserves blame or praise for something that happened later.
- **Geometry**: Arrange things so nearby points mean similar things and directions mean useful changes.
- **Search**: Try to move through possible answers, actions, or images toward ones that satisfy a goal.
- **Uncertainty**: Keep track of many possible futures or explanations instead of pretending there is only one.
- **Feedback**: Use a signal after an attempt to change what the system does next time.
- **Scale**: Ask what changes when data, model size, compute, or test-time work becomes much larger.
- **Invariance**: Preserve the meaning while surface details such as position, wording, or style change.
- **Composition**: Build complex behavior by connecting reusable smaller operations.

## Themes

### Representation As A Working Space

Modern models first turn messy inputs into internal coordinates, then do most of their work by moving, comparing, and editing those coordinates.

Why it matters: Without this workspace, text, images, states, and actions remain raw surface forms that cannot share computation.

Cross-course argument: The shared argument is that intelligence first needs a manipulable workspace. CME295 shows this with tokens, positions, attention, and transformer blocks: language becomes pieces that can exchange information. CME296 reuses the same idea for images, where patches and latent coordinates let vision systems compare and edit visual structure. CS224R contributes the agent-state version of the same pressure: actions are only learnable after the world has been represented in a form where consequences can be compared.

Mathematical spine: The mathematical spine is mapping and geometry. Raw objects are mapped into IDs or vectors; vectors can be compared by scores, distances, and directions; layers then update those vectors. The point of the math is not decoration. It gives the learner a place where similarity, order, and context can become operations.

Where the analogy breaks: The analogy breaks if all representations are treated as the same kind of thing. A token embedding, an image latent, and an RL state all compress the world, but they preserve different information and create different blind spots. A representation that helps next-token prediction can still be bad for physical control or visual detail.

Evidence chain: This theme is grounded through tokenization, embeddings, positional encoding, attention, transformer block, vision transformers. Its subthemes are text and patch interfaces, learned geometry, selective context, stacked computation. The supporting evidence spans are distributed across cme295-transformers-llms-autumn-2025, cme296-diffusion-large-vision-models-spring-2026, cs224r-deep-rl-spring-2025; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Turning Messy Inputs Into Countable Pieces: Start with the everyday problem: The system needs a first set of pieces before it can compare, remember, or predict anything. The deeper reason is: Discrete inputs need a stable interface into numerical computation. The subtheme groups tokenization, vision transformers because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Making Meaning Into Geometry: Start with the everyday problem: Related things need to be near enough that arithmetic can share what is learned. The deeper reason is: Similarity becomes useful only after it is represented as distance or direction. The subtheme groups embeddings, latent space because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Choosing Which Context Matters: Start with the everyday problem: The model cannot treat every past detail as equally relevant. The deeper reason is: Context is useful only when it is selected and weighted. The subtheme groups attention, positional encoding because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Building Depth From Repeated Simple Updates: Start with the everyday problem: Hard understanding requires more than one pass over the input. The deeper reason is: Repeated small transformations can build complex internal state. The subtheme groups transformer block because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.

### Learning From Feedback

A model improves by turning mistakes, rewards, preferences, or prediction errors into small changes in future behavior.

Why it matters: This is the bridge from passive pattern finding to systems that can be steered toward useful outcomes.

Cross-course argument: The shared argument is that a model does not become useful just by containing parameters. It needs signals after attempts. CME295 emphasizes broad practice and later steering for language models. CS224R makes feedback explicit as rewards, preferences, and policy changes. CME296 shows a related training story in generative models, where prediction errors over noisy or hidden structure teach the model how to improve samples.

Mathematical spine: The mathematical spine is error turned into update. A loss, reward, or preference comparison is compressed into a number or direction. Gradients or policy updates then change future behavior. The important concept is that feedback must be both informative enough to guide learning and narrow enough to compute.

Where the analogy breaks: Prediction error, human preference, and reward are not interchangeable. Prediction error says what was likely in data; preference says which output a judge liked; reward says what outcome the environment paid for. Confusing those signals is how fluent models become unhelpful or agents learn shortcuts.

Evidence chain: This theme is grounded through pretraining, fine tuning, rl for llms. Its subthemes are prediction as practice, human feedback. The supporting evidence spans are distributed across cme295-transformers-llms-autumn-2025, cme296-diffusion-large-vision-models-spring-2026, cs224r-deep-rl-spring-2025; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Learning Structure By Guessing Missing Pieces: Start with the everyday problem: There is much more raw data than carefully labeled instruction. The deeper reason is: A simple prediction game can expose the structure of language, images, and behavior. The subtheme groups pretraining because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Turning Preference Into Training Signal: Start with the everyday problem: People can often say which answer is better even when they cannot write the perfect answer in advance. The deeper reason is: Comparison can be converted into a direction for changing behavior. The subtheme groups fine tuning, reward, rl for llms because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.

### Action, Time, And Consequence

Reinforcement learning studies what happens when choices change the future evidence the learner will see.

Why it matters: It explains why agents, robots, games, and reasoning systems need more than ordinary supervised prediction.

Cross-course argument: The shared argument is that choosing changes what evidence comes next. CS224R is the center of this theme: policies, rewards, credit assignment, Q-values, model-based planning, and offline data all exist because action unfolds through time. CME295 connects when reasoning systems and tool-using LLMs become sequential decision makers instead of one-shot predictors.

Mathematical spine: The mathematical spine is recursion over time. A present choice is judged by immediate feedback plus expected future feedback. Values, advantages, returns, and transition models are different ways to write down that the consequence of an action can be delayed and indirect.

Where the analogy breaks: Not every sequence is reinforcement learning. A language model generating tokens has a sequence, but RL adds an environment, actions that change future states, and feedback tied to outcomes. The analogy is useful only when the later result can change how earlier choices are evaluated.

Evidence chain: This theme is grounded through policy, reward, credit assignment, policy gradient, actor critic, q learning, offline rl, model based rl, exploration. Its subthemes are delayed feedback, learning from logged worlds, imagined futures. The supporting evidence spans are distributed across cs224r-deep-rl-spring-2025, cme295-transformers-llms-autumn-2025; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Learning When The Result Comes Later: Start with the everyday problem: The feedback arrives after a chain of choices, so the learner must decide which choice mattered. The deeper reason is: Cause and reward are separated by time. The subtheme groups policy, credit assignment, q learning, policy gradient, actor critic because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Learning Safely From Old Experience: Start with the everyday problem: The learner may not be allowed to freely experiment in the real world. The deeper reason is: A dataset only covers part of what could have happened. The subtheme groups offline rl because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Using Prediction To Plan Before Acting: Start with the everyday problem: Real trial and error is expensive, but imagined trial and error can be cheap. The deeper reason is: A model of consequences turns acting into searching over possible futures. The subtheme groups model based rl, exploration because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.

### Thinking As Extra Work At Use Time

Some systems get better by spending more computation after the prompt arrives: writing intermediate steps, searching, calling tools, or revising.

Why it matters: It separates stored knowledge from active problem solving.

Cross-course argument: The shared argument is that some capability comes from work done after the input arrives. CME295 shows this through reasoning traces, retrieval, tools, and agents. CS224R supplies the decision-loop vocabulary: state, action, observation, update. Together they explain why a modern system can be more than a frozen predictor when it is allowed to search, write intermediate state, and check external evidence.

Mathematical spine: The mathematical spine is sequential computation over a changing context. Extra tokens, tool calls, and observations become new state. Each step conditions the next step, so the final answer depends on a path rather than a single forward pass.

Where the analogy breaks: More steps do not guarantee better reasoning. Extra computation can compound an early mistake, retrieve irrelevant evidence, or overfit to a brittle procedure. The useful question is whether each added step creates new reliable information or merely adds more text.

Evidence chain: This theme is grounded through reasoning traces, agents and tools. Its subthemes are scratch work and tools. The supporting evidence spans are distributed across cme295-transformers-llms-autumn-2025, cs224r-deep-rl-spring-2025; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Solving By Writing, Searching, And Acting: Start with the everyday problem: A hard task may need intermediate notes, outside facts, or tool results. The deeper reason is: The context can become a temporary workspace that changes as the system works. The subtheme groups reasoning traces, agents and tools because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.

### Generation As Guided Movement

Diffusion, flow, and guidance methods turn generation into a path through possible samples rather than a one-shot guess.

Why it matters: It gives a practical way to create complex images and videos while still obeying conditions.

Cross-course argument: The shared argument is that generation is easier when treated as guided movement. CME296 is the center: diffusion, score matching, flow matching, guidance, and latent spaces all build a route from uncertainty toward a structured sample. CME295 connects through transformer-based vision and conditioning, where instructions or text change the path through visual possibilities.

Mathematical spine: The mathematical spine is a direction field through a space of possible samples. Noise represents many possible worlds. A score, velocity, or guided update tells the sample which way to move. Repeating small moves makes a hard global generation problem manageable.

Where the analogy breaks: A generative path is not proof of understanding the world that produced the data. Many paths can create plausible samples. Guidance can make outputs obey a prompt while also reducing diversity or pushing the sample into artifacts.

Evidence chain: This theme is grounded through diffusion, score matching, flow matching, guidance, latent space. Its subthemes are denoising paths, continuous transport, controlled generation. The supporting evidence spans are distributed across cme296-diffusion-large-vision-models-spring-2026; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Making A Hard Sample By Many Small Corrections: Start with the everyday problem: A detailed image is too hard to create in one leap. The deeper reason is: Many small local directions can solve a global generation problem. The subtheme groups diffusion, score matching because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Moving Samples Along A Learned Route: Start with the everyday problem: Generation needs a route from something easy to sample to something realistic. The deeper reason is: A path through space can be easier to learn than a direct jump. The subtheme groups flow matching because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- Balancing Freedom With Instruction: Start with the everyday problem: A model can make something plausible but not the thing requested. The deeper reason is: Generation must be constrained without freezing all creative variation. The subtheme groups guidance because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.

### Measurement, Scale, And Generalization

Scores, scaling curves, and test sets are claims about behavior under chosen conditions, not full descriptions of intelligence.

Why it matters: It keeps model development honest about what has actually been demonstrated.

Cross-course argument: The shared argument is that progress claims need disciplined measurement. CME295 raises evaluation and scaling for LLM capability. CS224R shows why offline and sequential settings can fool naive scores. CME296 adds visual-generation evaluation, where realism, alignment, diversity, and artifacts are hard to compress into one number.

Mathematical spine: The mathematical spine is sampling and compression. A metric samples behavior under chosen conditions and compresses it into a score or curve. Scaling laws then fit relationships between resources and measured loss or capability. The hidden issue is what the measurement leaves out.

Where the analogy breaks: A higher score is not always a better system. The score may be narrow, stale, or easy to game. Scaling trends also describe observed ranges; they do not remove the need to inspect failure cases, distribution shifts, and human consequences.

Evidence chain: This theme is grounded through evaluation, scaling laws, generalization. Its subthemes are scores are samples, what changes with size. The supporting evidence spans are distributed across cme295-transformers-llms-autumn-2025, cme296-diffusion-large-vision-models-spring-2026, cs224r-deep-rl-spring-2025; the theme-level prose is synthesis over those anchored concepts, so it should be read as a cross-course argument rather than a single lecture quote.

- Remembering That Scores Are Partial Views: Start with the everyday problem: A single score can hide what the model cannot do. The deeper reason is: Every measurement compresses behavior and loses detail. The subtheme groups evaluation, generalization because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
- What Changes When Systems Get Bigger: Start with the everyday problem: Building larger systems is costly, so developers need clues about what scale will buy. The deeper reason is: Capability depends on bottlenecks among data, compute, architecture, and training objective. The subtheme groups scaling laws because each concept is a concrete answer to that same pressure. A reader should first ask what constraint the system faces, then ask what object the method introduces so the constraint can be handled by computation.
