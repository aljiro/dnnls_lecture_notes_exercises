# Example assessment workflows

This document shows practical ways to organise the implementation for each assessment route. The examples are **patterns**, not required architectures. Use the lightest workflow that keeps the reference system identifiable and makes your own contribution easy to inspect.

The supplied architectures live in:

`https://github.com/aljiro/dnnls_architecture`

The repository contains several versions in separate folders/modules (`v1`, `v2`, and so on). The assessment notebook will use a fixed course release selected by the module team, so students do **not** need to record Git commit SHAs for the supplied architecture.

The central principle is:

> **Import the reference system; expose your intervention; keep the experiment in the notebook.**

Do not copy an entire supplied architecture into the assessment notebook simply because you want to change one part of it.

## Common setup

The released assessment notebook should already contain the correct repository and course release. Conceptually, the setup is:

```python
ARCHITECTURE_REPO = "https://github.com/aljiro/dnnls_architecture.git"
ARCHITECTURE_RELEASE = "<assessment-release>"  # supplied by the module team

!git clone --quiet "$ARCHITECTURE_REPO" /content/dnnls_architecture
%cd /content/dnnls_architecture
!git checkout --quiet "$ARCHITECTURE_RELEASE"
!pip install -q -e .
%cd /content
```

Students then choose the architecture version/folder used in the investigation, for example `v1`.

---

## Route A — Investigate the existing architecture

**Typical aim:** understand a behaviour, representation, failure mode, component, or performance difference without substantially rewriting the supplied architecture.

### Recommended workflow

Use the supplied repository **read-only**. Import the chosen architecture version directly, run the reference system, and place the experimental probes, ablations, interventions, plots, and measurements in the Colab notebook.

For example:

```python
from v1.model import StoryModel

model = StoryModel(...)
```

Then investigate it in the notebook:

```python
features = model.encoder(images)
# analysis / probe / perturbation / comparison follows
```

**What belongs where?**

- **Architecture repository:** unchanged reference architecture.
- **Notebook:** hypothesis, experimental controls, probes, ablations, measurements, figures and interpretation.
- **Student fork:** normally unnecessary.

Example question: *Does v3 actually use temporal order, or can it perform similarly from an unordered set of frame representations?*

---

## Route B — Make an important architectural change

**Typical aim:** replace, remove, extend, or substantially modify part of one supplied architecture version and test the consequences.

There are two appropriate implementation modes.

### B1 — Local component replacement in Colab

Use this when the change is concentrated in one component or can be cleanly expressed as a subclass, wrapper, replacement module, configuration, or small amount of new code.

Import the unchanged parts of the reference architecture:

```python
from v1.model import StoryModel
from v1.temporal import ReferenceTemporalModel
```

Define only the changed component:

```python
class MyTemporalModel(ReferenceTemporalModel):
    def __init__(self, ...):
        super().__init__(...)
        # changed implementation

    def forward(self, x):
        ...
```

Then compare it with the supplied reference:

```python
reference = StoryModel(...)
changed = StoryModel(temporal_model=MyTemporalModel(...), ...)
```

If the supplied API permits component injection, use it. If not, a small wrapper or clearly documented replacement is preferable to copying the whole architecture.

**What belongs where?**

- **Architecture repository:** unchanged reference code.
- **Notebook:** the student's replacement component and experiment.
- **Student fork:** unnecessary unless the change spreads across the codebase.

### B2 — Repository modification / fork

Use this when the intervention requires coordinated changes across several supplied source files, changes interfaces used throughout the architecture, or is no longer readable as a small notebook-local replacement.

Workflow:

1. Fork `aljiro/dnnls_architecture` on GitHub.
2. Make the architectural changes in the student's fork.
3. Keep the final implementation in that fork.
4. Record the **fork URL** in the assessment notebook.
5. Clone the fork from Colab and run the experiments there.

For example:

```python
STUDENT_REPO = "https://github.com/STUDENT/dnnls_architecture.git"

!git clone --quiet "$STUDENT_REPO" /content/student_architecture
%cd /content/student_architecture
!pip install -q -e .
%cd /content
```

A commit SHA is **not required**. A pull request back to the supplied repository is also optional. If one exists, students may include its URL because the PR diff can make the change easier to inspect.

The experiment, results, comparison and interpretation still belong in the assessment notebook.

### When to move from B1 to B2

Use the fork workflow when you find yourself copying large unchanged classes into the notebook, modifying several connected source files, or needing the notebook to reconstruct a miniature copy of the repository. Do not use a fork merely because Git feels more sophisticated.

---

## Route C — Build an alternative architecture

**Typical aim:** construct a substantially different solution, such as a Transformer + CLIP system, and compare it fairly with one or more supplied architectures.

### C1 — Self-contained alternative in the notebook

If the alternative can remain compact and readable, import the reference model and define the new model in the notebook or in a small generated module.

```python
from v4.model import StoryModel as ReferenceModel

class ClipTransformerModel(nn.Module):
    ...
```

For a larger but still self-contained model, Colab can create a supporting file explicitly:

```python
%%writefile student_model.py

import torch
import torch.nn as nn

class ClipTransformerModel(nn.Module):
    ...
```

### C2 — Student repository for a substantial alternative

If the alternative architecture has multiple modules, custom training code, configurations, or enough source code that the notebook becomes difficult to inspect, place it in a student fork/repository and record the repository URL.

Again, no commit SHA is required. A PR is optional.

The notebook should still make the comparison legible: reference model, alternative model, common dataset/split, controlled training/evaluation choices, results and interpretation.

### Important comparison rule

Do not treat “higher score” as the whole investigation. Make clear what differs besides architecture: pretrained representations, parameter count, training compute, data, augmentation, objective, or external knowledge may all explain a gain.

---

## Route D — Ask a scientific question

**Typical aim:** use a trained architecture as an experimental object to test a claim about what it represents, uses, learns, remembers, or generalises.

### Recommended workflow

In most cases, **do not modify the architecture repository at all**. Import a supplied architecture and add the scientific instrumentation in the notebook.

For the question *“Does the model learn the concept of a place?”*, for example, you might:

1. select a trained architecture and checkpoint;
2. define what evidence would count as place information;
3. extract an appropriate internal representation;
4. run a probe, controlled retrieval analysis, clustering comparison, or intervention;
5. include a control that distinguishes “information can be decoded” from “the model uses this information”; and
6. interpret the result cautiously.

A strong Route D investigation distinguishes claims such as:

- *place information is decodable from the representation*;
- *the representation clusters by place*;
- *the model's prediction changes when place information is intervened on*;
- *the model causally relies on place information*.

These are not equivalent claims and require different evidence.

---

## Choosing between notebook code and a fork

| Situation | Recommended implementation |
|---|---|
| No architecture change; analysis only | Import reference + notebook experiment |
| One replaceable module/component | Import reference + define changed component in notebook |
| Small alternative model | Reference import + alternative in notebook / `student_model.py` |
| Several coordinated changes to supplied source | Student fork + repository URL |
| Large alternative architecture/codebase | Student repository/fork + repository URL |

A fork does **not** improve the mark by itself. It is simply a practical way of keeping a substantial implementation organised and inspectable.

## What to record in the notebook

Whichever workflow you choose, identify:

- architecture version/folder (`v1`, `v2`, etc.);
- supplied checkpoint/dataset version where relevant;
- whether the intervention is notebook-local or in a student repository;
- student repository URL if used;
- optional pull request URL if one exists;
- the specific component/files changed;
- the reference condition used for comparison.

The notebook remains the main assessment artifact: it should contain the question, reasoning, experiment, evidence and conclusions even when the implementation itself lives in a repository.
