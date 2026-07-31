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

- Turning Messy Inputs Into Countable Pieces: The system needs a first set of pieces before it can compare, remember, or predict anything.
- Making Meaning Into Geometry: Related things need to be near enough that arithmetic can share what is learned.
- Choosing Which Context Matters: The model cannot treat every past detail as equally relevant.
- Building Depth From Repeated Simple Updates: Hard understanding requires more than one pass over the input.

### Learning From Feedback

A model improves by turning mistakes, rewards, preferences, or prediction errors into small changes in future behavior.

Why it matters: This is the bridge from passive pattern finding to systems that can be steered toward useful outcomes.

- Learning Structure By Guessing Missing Pieces: There is much more raw data than carefully labeled instruction.
- Turning Preference Into Training Signal: People can often say which answer is better even when they cannot write the perfect answer in advance.

### Action, Time, And Consequence

Reinforcement learning studies what happens when choices change the future evidence the learner will see.

Why it matters: It explains why agents, robots, games, and reasoning systems need more than ordinary supervised prediction.

- Learning When The Result Comes Later: The feedback arrives after a chain of choices, so the learner must decide which choice mattered.
- Learning Safely From Old Experience: The learner may not be allowed to freely experiment in the real world.
- Using Prediction To Plan Before Acting: Real trial and error is expensive, but imagined trial and error can be cheap.

### Thinking As Extra Work At Use Time

Some systems get better by spending more computation after the prompt arrives: writing intermediate steps, searching, calling tools, or revising.

Why it matters: It separates stored knowledge from active problem solving.

- Solving By Writing, Searching, And Acting: A hard task may need intermediate notes, outside facts, or tool results.

### Generation As Guided Movement

Diffusion, flow, and guidance methods turn generation into a path through possible samples rather than a one-shot guess.

Why it matters: It gives a practical way to create complex images and videos while still obeying conditions.

- Making A Hard Sample By Many Small Corrections: A detailed image is too hard to create in one leap.
- Moving Samples Along A Learned Route: Generation needs a route from something easy to sample to something realistic.
- Balancing Freedom With Instruction: A model can make something plausible but not the thing requested.

### Measurement, Scale, And Generalization

Scores, scaling curves, and test sets are claims about behavior under chosen conditions, not full descriptions of intelligence.

Why it matters: It keeps model development honest about what has actually been demonstrated.

- Remembering That Scores Are Partial Views: A single score can hide what the model cannot do.
- What Changes When Systems Get Bigger: Building larger systems is costly, so developers need clues about what scale will buy.
