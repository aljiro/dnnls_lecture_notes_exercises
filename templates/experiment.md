# Experiment template

> This is an instructor/design document. It should not be shown to students unchanged.

## Working title

A short internal name for the experiment.

## Opening question

The concrete question the student encounters first.

It should be observable and specific. Avoid naming the hidden learning objective directly.

## Phenomenon

What surprising, revealing, or counter-intuitive behaviour is the experiment designed to expose?

## Hidden learning objectives

What deeper ideas should the student eventually infer or articulate?

- 
- 
- 

## Prior mental model

What is the student likely to believe before the experiment?

## Intended conceptual turn

What observation should make the prior mental model incomplete or untenable?

## Main experiment

Describe the smallest experiment that can produce the phenomenon convincingly.

### Computational budget

Prefer one purposeful training run when training is expensive.

### Instrumentation contract

Before running, specify everything that must be recorded for later analysis. Examples:

- training and validation loss by step/epoch
- overall and class-wise metrics
- predictions on a fixed probe set
- confusion matrices
- selected checkpoints
- hidden activations/representations for a fixed probe set
- gradient norms
- parameter/update norms
- activation means/variances
- attention maps or attribution values where relevant
- random seed and hyperparameters

The goal is for subsequent prompts to inspect, plot, compare, and reason from saved evidence rather than repeatedly retrain the model.

## Student prompt sequence

The final student-facing prompts belong in `sequence.md` for the experiment. Design the sequence here first.

### Prompt 1 — Prediction / framing

What should the student predict before seeing the result?

### Prompt 2 — Build or run

What experiment should the agent help them construct and execute? Explicitly request the instrumentation needed later.

### Prompt 3 — First observation

What is the simplest plot or measurement that reveals the initial pattern?

### Prompt 4 — Complication

What additional evidence makes the first explanation insufficient?

### Prompt 5 — Representation / mechanism

What internal measurement helps explain why the behaviour occurs?

### Prompt 6 — Conceptual synthesis

Ask the student to explain the phenomenon in their own words before naming the formal concept where possible.

### Prompt 7 — Transfer

Change one important condition and ask the student to predict the outcome using the new mental model. Run a new experiment only if genuinely necessary.

## Expected observations

Record what a successful run should approximately show. Avoid depending on exact numerical values unless necessary.

## Failure modes

List ways the phenomenon may fail to appear and how to repair the experiment without changing its conceptual purpose.

## Lecture connection

### Knowledge needed before the experiment

What theory or notation must already be available?

### Theory motivated by the experiment

What should be taught after the student has encountered the phenomenon?

## Instructor notes

What must an instructor understand that should remain hidden from the initial student prompt?

## Reuse / dependencies

What saved artefacts, code, datasets, or concepts from earlier experiments can this exercise reuse?
