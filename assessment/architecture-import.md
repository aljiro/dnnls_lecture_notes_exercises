# Using architecture versions from another repository in Google Colab

Yes. A Colab notebook can use Python code directly from a different Git repository. For this assessment, that is usually preferable to copying the important classes and functions into the notebook because it keeps the supplied architecture identifiable and makes comparisons between versions reproducible.

## Recommended pattern: clone a pinned version

For a public repository:

```python
!git clone --quiet https://github.com/OWNER/ARCHITECTURE_REPO.git
%cd ARCHITECTURE_REPO
!git checkout --quiet TAG_OR_COMMIT
```

Then either import from the cloned repository if it is already a Python package:

```python
import sys
sys.path.insert(0, "/content/ARCHITECTURE_REPO")

from package_name.models import ModelName
```

or, if the repository contains `pyproject.toml` or `setup.py`, install it into the Colab environment:

```python
!pip install -q -e /content/ARCHITECTURE_REPO
```

The editable install (`-e`) is useful during an investigation because students can modify a local source file and then reload/restart as appropriate without making a second copy of the architecture.

## Pin the version

The final notebook should record an exact **tag or commit SHA**. Avoid relying on the current `main` branch because `main` can change between the student's investigation and marking.

A robust setup looks like:

```python
ARCHITECTURE_REPO = "https://github.com/OWNER/ARCHITECTURE_REPO.git"
ARCHITECTURE_REF = "<tag-or-commit-sha>"

!git clone --quiet "$ARCHITECTURE_REPO" architecture_src
%cd /content/architecture_src
!git checkout --quiet "$ARCHITECTURE_REF"
!pip install -q -e .
%cd /content
```

Students should report the same `ARCHITECTURE_REF` in the **Reference system** section of the assessment notebook.

## Multiple supplied architecture versions

There are two sensible ways to distribute low-to-high-complexity versions.

### Option 1 — tags or commits in one repository

Use tags such as `v1-baseline`, `v2-cnn`, `v3-sequence`, etc. Students check out the version they want to investigate. This is the cleanest option when the versions form a genuine evolution of the same codebase.

### Option 2 — separate modules/configurations in one repository

Expose versions through stable imports or configurations, for example:

```python
from story_reasoning.versions import BaselineModel, CNNModel, SequenceModel
```

or:

```python
model = build_model(version="v3")
```

This is convenient when students need to compare two versions in the same runtime.

## Private repositories

Private repositories can also be used, but authentication must be handled carefully. Do **not** place a GitHub personal access token in a submitted notebook, output cell, URL, or transcript.

For teaching, the simplest arrangement is usually to make the architecture repository readable to students through an authenticated GitHub/Colab workflow and provide a setup cell that does not expose credentials. If authentication becomes cumbersome, distributing a tagged release/package or including the architecture in the course repository is safer than asking students to paste tokens.

## When should students copy code instead?

Copy only the part that is **the student's own changed component**, or when an external repository is not reliably available in the marking environment.

For example, if a student replaces the supplied recurrent decoder with a transformer decoder, it is reasonable for the new decoder to live in the assessment notebook or in a submitted `.py` file. It is usually *not* useful to duplicate the unchanged dataset loader, encoder, training utilities, and reference model around it.

A good principle is:

> **Import the reference system; expose the student's intervention.**

This makes the notebook shorter, reduces accidental divergence from the supplied model, and makes the assessed change easier to inspect.

## Imports are not enough for reproducibility

If the architecture also depends on external checkpoints, datasets, generated embeddings, or metadata, record their version/path and ensure markers can access them. Do not make the final result depend on a temporary local file that exists only in the student's Colab runtime.

## Suggested assessment convention

Students should record:

- architecture repository;
- exact tag/commit;
- architecture/version name;
- any supplied checkpoint identifier;
- dataset/version;
- their own changed files or modules.

This allows the architecture repository to remain the canonical source while the assessment submission contains only the evidence and the student's intervention.
