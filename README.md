![Module banner](lecture_notes/images/DNNLS_Logo.png)

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
- `lecture_notes/` — the LaTeX lecture notes.
  - `main.tex` — master document that assembles the full set of notes.
  - `preamble.tex` — shared packages, notation, and document-wide configuration.
  - `chapters/weekXX.tex` — one independent source file per teaching week/chapter.
- `weeks/` — exercise design, prompt sequences, code, and supporting material, created as each week is developed.
- `templates/` — common structures for lecture chapters and experiments.
- `shared/` — reusable code, figures, datasets, and utilities when needed.
- `references.bib` — shared bibliography for the lecture notes and supporting material.

## Building the lecture notes

Compile from inside `lecture_notes/` so the relative paths to chapters, figures, and the bibliography remain simple:

```bash
cd lecture_notes
latexmk -pdf main.tex
```

The notes use `biblatex` with the `biber` backend. A standard `latexmk` installation should run the required bibliography pass automatically.

Each weekly file is brought into `main.tex` with `\input{chapters/weekXX}`. Weekly development should normally edit the relevant chapter file rather than the master document.

## Development workflow

The stable course structure lives on `main`. Substantial weekly development should normally happen on a dedicated branch and be reviewed before merging. Lecture notes and exercises for the same week should be developed together so that experiments can create the need for theory, and later lecture material can formalise what students observed.
