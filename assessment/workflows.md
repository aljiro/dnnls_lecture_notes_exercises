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
- **Student fork:** unnecessary.

Example question: *Does v3 actually use temporal order, or can it perform similarly from an unordered set of frame representations?*

---

## Route B — Make an important architectural change

**Typical aim:** replace, remove, extend, or substantially modify part of one supplied architecture version and test the consequences.

### B1 — Local component replacement in Colab — recommended

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
- **Student fork:** unnecessary.

### B2 — Substantial multi-file change — advanced, authorization required

If the intervention genuinely requires coordinated changes across several supplied source files or changes interfaces throughout a supplied version, discuss the implementation approach with the module team **before** using a repository/fork workflow.

The normal solution is to keep the assessment notebook as the experimental record and submit any changed source/configuration files alongside it.

A **public GitHub fork is an advanced option and requires authorization from the module team before it is used for assessed work**. The supplied architecture repository will be public, and forks of a public GitHub repository are also public. Other students may therefore be able to see code placed in the fork during the assessment period.

Do not create a public fork merely because it seems more sophisticated. Use one only where its organisational benefits clearly outweigh the exposure of the assessed implementation and the module team has agreed that it is appropriate.

If an authorized fork is used:

1. keep the change focused on the selected architecture version;
2. keep the experimental question, comparisons, outputs and interpretation in the Colab notebook;
3. record the fork URL in the notebook/submission manifest; and
4. do **not** open a pull request to the supplied architecture repository unless specifically asked to do so.

A commit SHA and pull request are not assessment requirements.

### When is B2 justified?

Consider the advanced workflow only when you find yourself copying large unchanged classes into the notebook, modifying several connected source files, or needing the notebook to reconstruct a miniature copy of the repository. Most Route B projects should remain in B1.

---

## Route C — Build an alternative architecture

**Typical aim:** construct a substantially different solution, such as a Transformer + CLIP system, and compare it fairly with one or more supplied architectures.

### C1 — Self-contained alternative in the notebook — recommended

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

### C2 — Substantial external implementation — advanced, authorization required

If the alternative architecture has multiple modules, custom training code, configurations, or enough source code that the notebook becomes difficult to inspect, discuss the implementation arrangement with the module team first.

Normally, supporting source files can simply be submitted alongside the notebook. A public repository/fork for assessed implementation is an advanced option and requires authorization because other students may be able to view the code.

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

## Choosing where your code should live

| Situation | Recommended implementation |
|---|---|
| No architecture change; analysis only | Import reference + notebook experiment |
| One replaceable module/component | Import reference + changed component in notebook |
| Small alternative model | Reference import + alternative in notebook / `student_model.py` |
| Several coordinated changes to supplied source | Supporting source files submitted with notebook; discuss with module team |
| Public fork/repository for assessed implementation | **Advanced; authorization required** |

A repository or fork does **not** improve the mark by itself. It is only an organisational tool.

## Process evidence and academic integrity

The notebook, full Gemini conversation, selected AI-trail moments, experimental outputs and any submitted implementation files together provide evidence of how the investigation developed. They make it easier to connect a student's reasoning with the code and results they produced.

These artifacts are **process evidence, not a guarantee of authorship**. Students remain responsible for understanding and being able to explain the decisions, implementation and claims in their submission. Where the provenance of work is unclear, the module team may use the submitted process evidence in accordance with normal university academic-integrity procedures.

## What to record in the notebook

Whichever workflow you choose, identify:

- architecture version/folder (`v1`, `v2`, etc.);
- supplied checkpoint/dataset version where relevant;
- whether the intervention is notebook-local or uses supporting source files;
- authorized student repository/fork URL if one is used;
- the specific component/files changed; and
- the reference condition used for comparison.

The notebook remains the main assessment artifact: it should contain the question, reasoning, experiment, evidence and conclusions even when supporting implementation files are used.
