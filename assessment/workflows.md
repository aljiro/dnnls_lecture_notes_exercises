# Example assessment workflows

This document shows practical ways to organise the implementation for each assessment route. The examples are **patterns**, not required architectures. Use the lightest workflow that keeps the reference system identifiable and makes your own contribution easy to inspect.

The supplied architecture repository contains several versions in separate folders. The repository itself should be pinned to the assessment release/tag or an exact commit. The architecture folder you choose, for example `v1/`, identifies the reference model inside that release.

The central principle is:

> **Import the reference system; expose your intervention; keep the experiment in the notebook.**

Do not copy an entire supplied architecture into the assessment notebook simply because you want to change one part of it.

## Common setup

A typical Colab setup is:

```python
ARCHITECTURE_REPO = "https://github.com/OWNER/ARCHITECTURE_REPO.git"
ARCHITECTURE_REF = "<assessment-release-tag-or-commit>"

!git clone --quiet "$ARCHITECTURE_REPO" /content/architecture_src
%cd /content/architecture_src
!git checkout --quiet "$ARCHITECTURE_REF"
!pip install -q -e .
%cd /content
```

Record both the repository reference and the architecture version/folder used, for example:

```text
Repository release: assessment-2026
Architecture: v1
```

The exact import names will depend on the architecture repository.

---

## Route A — Investigate the existing architecture

**Typical aim:** understand a behaviour, representation, failure mode, component, or performance difference without substantially rewriting the supplied architecture.

### Recommended workflow

Use the supplied repository **read-only**. Import the chosen architecture version directly, run the reference system, and place the experimental probes, ablations, interventions, plots, and measurements in the Colab notebook.

For example:

```python
from architecture.v1.model import StoryModel

model = StoryModel(...)
```

Then investigate it in the notebook:

```python
# Example: inspect or intervene on an internal representation
features = model.encoder(images)
# analysis / probe / perturbation / comparison follows
```

### What belongs where?

- **Architecture repository:** unchanged reference architecture.
- **Notebook:** hypothesis, experimental controls, probes, ablations, measurements, figures and interpretation.
- **Student fork:** normally unnecessary.

### Example investigation

Question: *Does v3 actually use temporal order, or can it perform similarly from an unordered set of frame representations?*

A useful notebook could compare the reference input with a shuffled-order control while leaving weights, data, evaluation and all other settings unchanged.

---

## Route B — Make an important architectural change

**Typical aim:** replace, remove, extend, or substantially modify part of one supplied architecture version and test the consequences.

There are two appropriate implementation modes.

### B1 — Local component replacement in Colab

Use this when your change is concentrated in one component or can be cleanly expressed as a subclass, wrapper, replacement module, configuration, or small amount of new code.

Import the unchanged parts of the reference architecture:

```python
from architecture.v1.model import StoryModel
from architecture.v1.temporal import ReferenceTemporalModel
```

Define only the changed component:

```python
class MyTemporalModel(ReferenceTemporalModel):
    def __init__(self, ...):
        super().__init__(...)
        # changed implementation

    def forward(self, x):
        # changed behaviour
        ...
```

Then construct the changed system using the supplied implementation wherever possible:

```python
reference = StoryModel(...)
changed = StoryModel(temporal_model=MyTemporalModel(...), ...)
```

If the supplied API permits component injection, use it. If not, a small wrapper or clearly documented replacement is preferable to copying the whole architecture.

**What belongs where?**

- **Architecture repository:** unchanged reference code.
- **Notebook:** the student's replacement component and the experiment comparing it with the reference.
- **Student fork:** unnecessary unless the change spreads across the codebase.

### B2 — Repository modification / fork

Use this when the proposed intervention requires coordinated changes across several supplied source files, changes interfaces used throughout the architecture, or is no longer readable as a small notebook-local replacement.

Workflow:

1. Fork the architecture repository.
2. Make the architectural changes in the fork.
3. Commit the final implementation.
4. Record the student repository and exact commit SHA in the assessment notebook.
5. Clone/check out that commit from Colab and run the experiments there.

For example:

```python
STUDENT_REPO = "https://github.com/STUDENT/ARCHITECTURE_REPO.git"
STUDENT_COMMIT = "<exact-commit-sha>"

!git clone --quiet "$STUDENT_REPO" /content/student_architecture
%cd /content/student_architecture
!git checkout --quiet "$STUDENT_COMMIT"
!pip install -q -e .
%cd /content
```

The **Git diff is useful supporting evidence** because it makes the implementation change inspectable. A pull request is optional; it is not required merely to obtain a diff or complete Route B.

The experiment, results, comparison and interpretation still belong in the assessment notebook.

### When to move from B1 to B2

Use the fork workflow when you find yourself copying large unchanged classes into the notebook, modifying several connected source files, or needing the notebook to reconstruct a miniature copy of the repository. Do not use a fork merely because Git feels more sophisticated.

---

## Route C — Build an alternative architecture

**Typical aim:** construct a substantially different solution, such as a Transformer + CLIP system, and compare it fairly with one or more supplied architectures.

Two patterns are appropriate.

### C1 — Self-contained alternative in the notebook

If the alternative can remain compact and readable, import the reference model from the architecture repository and define the new model in the notebook or in a small generated module.

For example:

```python
from architecture.v4.model import StoryModel as ReferenceModel

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

The notebook then imports it and contains the training/evaluation comparison.

### C2 — Student repository for a substantial alternative

If the alternative architecture has multiple modules, custom training code, configurations, or enough source code that the notebook becomes difficult to inspect, place it in a student fork/repository and pin the exact commit used for the results.

The notebook should still make the comparison legible: reference model, alternative model, common dataset/split, controlled training/evaluation choices, results and interpretation.

### Important comparison rule

Do not treat “higher score” as the whole investigation. Make clear what differs besides architecture: pretrained representations, parameter count, training compute, data, augmentation, objective, or external knowledge may all explain a gain.

A good Route C submission therefore distinguishes:

```text
reference implementation  -> imported from pinned supplied repo
alternative implementation -> notebook or pinned student repo
experiment/evidence         -> assessment notebook
```

---

## Route D — Ask a scientific question

**Typical aim:** use a trained architecture as an experimental object to test a claim about what it represents, uses, learns, remembers, or generalises.

### Recommended workflow

In most cases, **do not modify the architecture repository at all**. Import a pinned supplied architecture and add the scientific instrumentation in the notebook.

For example, for the question *“Does the model learn the concept of a place?”*, you might:

1. select a trained architecture and checkpoint;
2. define what evidence would count as place information;
3. extract an appropriate internal representation;
4. run a probe, controlled retrieval analysis, clustering comparison, or intervention;
5. include a control that distinguishes “information can be decoded” from “the model uses this information”; and
6. interpret the result cautiously.

Illustratively:

```python
from architecture.v5.model import StoryModel

model = StoryModel(...)
model.load_state_dict(...)

representations = extract_representations(model, loader)
# probe / intervention / shuffled-label control / comparison
```

### What belongs where?

- **Architecture repository:** unchanged model implementation.
- **Notebook:** operational definition of the scientific claim, probe/intervention, controls, results and interpretation.
- **Student fork:** normally unnecessary; use one only if the scientific experiment genuinely requires changing model internals rather than observing/intervening through a small wrapper or hook.

A strong Route D investigation distinguishes claims such as:

- *place information is decodable from the representation*;
- *the representation clusters by place*;
- *the model's prediction changes when place information is intervened on*;
- *the model causally relies on place information*.

These are not equivalent claims and require different evidence.

---

## Choosing between notebook code and a fork

Use this rule of thumb:

| Situation | Recommended implementation |
|---|---|
| No architecture change; analysis only | Import reference + notebook experiment |
| One replaceable module/component | Import reference + define changed component in notebook |
| Small alternative model | Reference import + alternative in notebook / `student_model.py` |
| Several coordinated changes to supplied source | Student fork + pinned commit |
| Large alternative architecture/codebase | Student repository/fork + pinned commit |

A fork does **not** improve the mark by itself. It is simply a practical way of keeping a substantial implementation organised and inspectable.

## What to record in the notebook

Whichever workflow you choose, the final notebook should identify:

- supplied architecture repository;
- supplied repository tag/commit;
- architecture version/folder used (`v1`, `v2`, etc.);
- supplied checkpoint/dataset version where relevant;
- whether the intervention is notebook-local or in a student repository;
- student repository + exact commit if used;
- the specific component/files changed;
- the reference condition used for comparison.

The notebook remains the main assessment artifact: it should contain the question, reasoning, experiment, evidence and conclusions even when the implementation itself lives in a repository.
