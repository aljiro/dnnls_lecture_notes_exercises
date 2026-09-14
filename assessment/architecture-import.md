# Using the architecture repository from Google Colab

The supplied DNNLS architectures live in:

`https://github.com/aljiro/dnnls_architecture`

The repository contains the course architecture versions in separate folders/modules (`v1`, `v2`, and so on). For the assessment, students should normally **import the supplied architecture rather than copy it into the notebook**.

For route-specific examples, including when an external implementation is appropriate, see [`workflows.md`](workflows.md).

## Recommended setup

The assessment notebook will use a fixed course release/tag chosen by the module team. Students do not need to find or record a commit SHA.

A typical setup cell is:

```python
ARCHITECTURE_REPO = "https://github.com/aljiro/dnnls_architecture.git"
ARCHITECTURE_RELEASE = "<assessment-release>"  # supplied by the module team

!git clone --quiet "$ARCHITECTURE_REPO" /content/dnnls_architecture
%cd /content/dnnls_architecture
!git checkout --quiet "$ARCHITECTURE_RELEASE"
!pip install -q -e .
%cd /content
```

The released assessment notebook should already contain the correct `ARCHITECTURE_RELEASE`. Students should not need to edit it.

If the repository is not packaged with `pyproject.toml` or `setup.py`, it can instead be added to the Python path:

```python
import sys
sys.path.insert(0, "/content/dnnls_architecture")
```

Students then select the architecture version/folder they are investigating, for example `v1`.

## What students need to record

For the supplied reference system, students only need to identify:

```text
Architecture: v1
Checkpoint: ...       # if relevant
Dataset/version: ...  # if relevant
```

The module team controls the repository release used by the notebook, so there is no need for every student to copy a tag or commit identifier into the report.

## Do not copy an entire version just to modify one part

If a student wants to change one component of `v1`, they should normally import the unchanged `v1` implementation and define only the changed component in the notebook.

For example:

```python
from v1.model import StoryModel
from v1.temporal import ReferenceTemporalModel

class MyTemporalModel(ReferenceTemporalModel):
    ...

reference = StoryModel(...)
changed = StoryModel(temporal_model=MyTemporalModel(...), ...)
```

This is preferable to copying the encoder, data loader, training loop, decoder, evaluation code and every other unchanged part of `v1` into the notebook.

A useful design principle for the architecture repository is therefore to make major components injectable or replaceable where practical.

> **Import the reference system; expose the student's intervention.**

## Substantial changes across several source files

If an intervention requires coordinated changes across several supplied source files, changes interfaces throughout a supplied version, or becomes too large to represent clearly as a notebook-local component, discuss the implementation approach with the module team first.

The normal option is to submit the changed source/configuration files alongside the notebook.

A **public student repository or fork is an advanced option and requires authorization from the module team before it is used for assessed work**. Once `dnnls_architecture` is public, a GitHub fork of it will also be public, so code placed in that fork may be visible to other students during the assessment period.

If an authorized fork is used, the student should:

1. modify only the relevant version/folder;
2. record the fork URL in the assessment notebook;
3. clone the fork from Colab for the experiments; and
4. avoid opening a pull request to the supplied architecture repository unless specifically asked to do so.

For example:

```python
STUDENT_REPO = "https://github.com/STUDENT/dnnls_architecture.git"

!git clone --quiet "$STUDENT_REPO" /content/student_architecture
%cd /content/student_architecture
!pip install -q -e .
%cd /content
```

A commit SHA and pull request are **not required** for the assessment.

## What stays in the Colab notebook?

Even when implementation code lives outside the notebook, the assessment notebook remains the main investigation artifact. It should contain the question, prediction, setup, experimental comparison, controls, results, figures, interpretation, limitations and AI interaction record.

A useful separation is:

```text
supplied architecture repo  -> reference implementation
supporting source/fork      -> substantial implementation change, only if needed
assessment Colab            -> experiment, evidence and reasoning
```

For small changes, the middle layer disappears: the changed component can live directly in the notebook.

## Public repository

The architecture repository is intended to be public for teaching. Public visibility means students can read and fork the repository; it does **not** give them permission to push changes to the original repository.

Because public forks are themselves public, do not use a public fork for assessed implementation unless the module team has authorized that workflow.

## Checkpoints, datasets and generated artifacts

Imports alone do not guarantee reproducibility. If the architecture depends on supplied checkpoints, dataset versions, cached embeddings, metadata, or other generated artifacts, identify them in the notebook and ensure the marker can access them.

Do not make the final result depend on a temporary file that exists only in one Colab session.

## What to record

Students should record:

- architecture version/folder (`v1`, `v2`, etc.);
- supplied checkpoint identifier where relevant;
- dataset/version;
- whether their intervention is notebook-local or uses supporting source files;
- authorized student repository/fork URL if one is used; and
- the specific component or files changed.

See [`workflows.md`](workflows.md) for complete examples for Routes A, B, C and D.
