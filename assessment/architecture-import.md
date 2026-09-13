# Using the architecture repository from Google Colab

A Colab notebook can use Python code directly from the separate DNNLS architecture repository. For this assessment, that is normally preferable to copying supplied classes and functions into the notebook.

The architecture repository contains the supplied model versions in separate folders/modules (`v1`, `v2`, and so on). The **repository itself** should be pinned to the assessment release/tag or an exact commit; the chosen version/folder identifies the architecture being investigated inside that release.

For route-specific examples, including when to use a student fork, see [`workflows.md`](workflows.md).

## Recommended pattern: clone a pinned repository release

For a public repository:

```python
ARCHITECTURE_REPO = "https://github.com/OWNER/ARCHITECTURE_REPO.git"
ARCHITECTURE_REF = "<assessment-release-tag-or-commit>"

!git clone --quiet "$ARCHITECTURE_REPO" /content/architecture_src
%cd /content/architecture_src
!git checkout --quiet "$ARCHITECTURE_REF"
!pip install -q -e .
%cd /content
```

If the repository is not packaged with `pyproject.toml` or `setup.py`, it can instead be added to the Python path:

```python
import sys
sys.path.insert(0, "/content/architecture_src")
```

Then import the required version from its module/folder, for example:

```python
from architecture.v1.model import StoryModel
```

The exact package/import names will depend on the final architecture repository structure.

## Pin the repository, then choose the architecture version

The final notebook should record both:

```text
Architecture repository: OWNER/ARCHITECTURE_REPO
Repository tag/commit: assessment-2026
Architecture version: v1
```

Do not rely on a moving `main` branch for the submitted result. A later change to the repository should not alter what the student's notebook means.

Keeping `v1`, `v2`, `v3`, etc. together inside the same pinned repository release also makes it possible to compare versions within one Colab runtime without repeatedly checking out different historical commits.

## Do not copy an entire version just to modify one part

If a student wants to change one component of `v1`, they should normally import the unchanged `v1` implementation and define only the changed component in the notebook.

For example:

```python
from architecture.v1.model import StoryModel
from architecture.v1.temporal import ReferenceTemporalModel

class MyTemporalModel(ReferenceTemporalModel):
    ...

reference = StoryModel(...)
changed = StoryModel(temporal_model=MyTemporalModel(...), ...)
```

This is preferable to copying the encoder, data loader, training loop, decoder, evaluation code and every other unchanged part of `v1` into the notebook.

A useful design principle for the architecture repository is therefore to make major components injectable or replaceable where practical.

> **Import the reference system; expose the student's intervention.**

## When a student fork is appropriate

A student fork is useful when an intervention requires **coordinated changes across several source files**, changes interfaces throughout a supplied version, or becomes too large to represent clearly as a notebook-local component.

In that case the student may:

1. fork the architecture repository;
2. modify the relevant version/folder;
3. commit the final implementation;
4. record the student repository and exact commit SHA; and
5. clone that pinned commit from the assessment notebook for the experiments.

Example:

```python
STUDENT_REPO = "https://github.com/STUDENT/ARCHITECTURE_REPO.git"
STUDENT_COMMIT = "<exact-commit-sha>"

!git clone --quiet "$STUDENT_REPO" /content/student_architecture
%cd /content/student_architecture
!git checkout --quiet "$STUDENT_COMMIT"
!pip install -q -e .
%cd /content
```

A pull request is **optional**. The commit history or Git diff can make substantial changes easier to inspect, but creating a PR is not itself an assessment requirement.

## What stays in the Colab notebook?

Even when implementation code lives in a student fork, the assessment notebook remains the main investigation artifact. It should contain the question, prediction, setup, experimental comparison, controls, results, figures, interpretation, limitations and AI interaction record.

A useful separation is:

```text
supplied architecture repo  -> reference implementation
student fork (if needed)    -> substantial implementation change
assessment Colab            -> experiment, evidence and reasoning
```

For small changes, the middle layer disappears: the changed component can live directly in the notebook.

## Private repositories

Private repositories can also be used, but authentication must be handled carefully. Do **not** place a GitHub personal access token in a submitted notebook, output cell, URL, or Gemini transcript.

For teaching, the simplest arrangement is usually to make the architecture repository readable to students through an authenticated GitHub/Colab workflow and provide a setup cell that does not expose credentials. If authentication becomes cumbersome, distributing a tagged release/package is safer than asking students to paste tokens.

## Checkpoints, datasets and generated artifacts

Imports alone do not guarantee reproducibility. If the architecture depends on supplied checkpoints, dataset versions, cached embeddings, metadata, or other generated artifacts, identify them in the notebook and ensure the marker can access them.

Do not make the final result depend on a temporary file that exists only in one Colab session.

## What to record

Students should record:

- supplied architecture repository;
- supplied repository tag/commit;
- architecture version/folder (`v1`, `v2`, etc.);
- supplied checkpoint identifier where relevant;
- dataset/version;
- whether their intervention is notebook-local or repository-based;
- student repository and exact commit if a fork/repository is used;
- the specific component or files changed.

See [`workflows.md`](workflows.md) for complete examples for Routes A, B, C and D.
