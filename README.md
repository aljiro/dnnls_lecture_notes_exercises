# Deep Neural Networks and Learning Systems

This repository contains the lecture notes and narrative exercises for the **Deep Neural Networks and Learning Systems (DNNLS)** module.

The module is organised around two parallel structures:

1. **The syllabus** — the mechanisms, models, and methods introduced week by week.
2. **The learning thread** — the deeper conceptual progression students build through experiments: sampling, projection, optimisation, representation, generalisation, inductive bias, information flow, memory, and learning during inference.

## Exercise philosophy

Exercises are designed as investigations rather than demonstrations. Each begins with a concrete question or surprising phenomenon. Students progress through a sequence of prompts that asks them to predict, run a purposeful experiment, inspect saved evidence, and revise their mental model.

The deeper learning objective is often *not directly named in the opening question*. It should emerge as the explanation the student earns from the experiment.

Whenever training is computationally expensive, the first substantial run should record enough diagnostics for later prompts to analyse the result without repeatedly retraining the model.

## Repository structure

- `curriculum/` — module-level pedagogical design and conceptual progression.
- `weeks/` — lecture notes and experiments for individual weeks.
- `templates/` — common structures for lectures and experiments.
- `shared/` — reusable code, figures, datasets, and utilities when needed.

The stable course structure lives on `main`. Substantial weekly development should normally happen on a dedicated branch and be reviewed before merging.
