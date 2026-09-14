![Module banner](../lecture_notes/images/DNNLS_Logo.png)

# Independent Architecture Investigation — Assessment Brief

## Purpose

The assessment asks you to use the DNNLS architecture as an **experimental system**. Your task is not simply to obtain the highest performance or build the most complicated network. Instead, you should formulate a meaningful question, make a justified prediction, design a controlled investigation, use generative AI critically, collect evidence, and decide what that evidence supports.

The weekly practicals prepare you for this process through small guided investigations. In this assessment, **you decide what question is worth asking**.

A careful investigation of a relatively simple model can receive the same mark as a substantially more complex implementation. **Model complexity is not a marking criterion.**

## Investigation routes

Choose one of the following routes. They are different ways of approaching the same assessment and are marked with the same rubric.

Detailed implementation patterns for all four routes are provided in [`workflows.md`](workflows.md). Use the lightest workflow that keeps the supplied architecture identifiable and makes your own contribution easy to inspect.

### Route A — Investigate the existing architecture

Extend or deepen an investigation based on one of the supplied architecture versions or weekly practicals. Examples include asking where performance comes from, which component matters, what a representation contains, or where a particular failure originates.

**Typical workflow:** import a supplied architecture version without changing it, and perform probes, ablations, interventions, diagnostics and analysis in the assessment notebook. A student fork is normally unnecessary.

### Route B — Make an important architectural change

Replace, remove, or substantially modify one component of the reference system and test the consequences. The important part is not the size of the change, but the quality of the hypothesis, comparison, controls, and interpretation.

**Typical workflow:** if the change is local, import the reference architecture and define only the changed component in the notebook. If the change requires coordinated edits across several source files, discuss the implementation arrangement with the module team. A public student fork/repository is an **advanced option and requires authorization** before it is used for assessed work.

### Route C — Build an alternative architecture

Construct a substantially different solution and compare it fairly with the reference system. A Transformer + CLIP approach is one possible example. A more capable model does not automatically constitute a stronger investigation: the comparison must reveal something useful about the task, representation, optimisation, inductive bias, or architecture.

**Typical workflow:** import the reference model from the supplied repository and implement the alternative either in the notebook or a small supporting module. If the implementation becomes a substantial multi-file system, discuss the arrangement with the module team. A public repository/fork is an advanced, authorization-only option.

### Route D — Ask a scientific question

Use the architecture to investigate a claim about what or how the system learns. Examples include questions such as whether the model learns a concept of place, whether information about characters or locations can be read from an internal representation, whether the model actually uses a variable that appears predictive, or whether an apparent representation survives an intervention.

**Typical workflow:** keep the supplied architecture unchanged and treat it as the object of study. Put probes, controlled interventions, shuffled-label tests, retrieval analyses or other scientific instrumentation in the notebook.

## Main submission

Complete [`assessment_investigation.ipynb`](assessment_investigation.ipynb) in Google Colab. The notebook is the main assessed artifact and replaces a conventional long report.

The notebook is structured around:

1. question;
2. motivation and prediction;
3. reference system;
4. proposed experiment or change;
5. implementation;
6. results;
7. interpretation;
8. limitations and alternative explanations;
9. AI interaction record;
10. what changed my mind?;
11. conclusion.

You may add cells where necessary, but retain these sections and keep the investigation easy to follow.

### Length

Use a maximum of **2,000 words of explanatory prose**. Code, references, the supplied template text, and the full Gemini transcript are excluded. Substantive explanatory prose placed inside tables still counts. The intention is to make figures, tables, code, and experimental evidence do much of the work.

## Architecture repository and reproducibility

The supplied architectures are provided in:

`https://github.com/aljiro/dnnls_architecture`

The repository contains the course versions (`v1`, `v2`, and so on) as separate folders/modules. The assessment notebook will use a **fixed course release** selected by the module team. You do not need to find, copy, or report a Git commit SHA for the supplied architecture.

You should record the architecture version you used (`v1`, `v2`, etc.), plus the checkpoint and dataset version where relevant.

Prefer importing the supplied architecture rather than copying large pieces of reference code into the notebook. See [`architecture-import.md`](architecture-import.md).

A good general rule is:

> **Import the reference system; expose your intervention; keep the experiment in the notebook.**

For a local change, a focused replacement component in the notebook is preferable to copying the whole architecture. If your change requires coordinated edits across several source files, discuss the implementation arrangement with the module team. Supporting source/configuration files can be submitted with the notebook.

A **public GitHub fork/repository for assessed implementation is an advanced option and requires authorization from the module team before use**. Once the supplied architecture repository is public, forks of it are public too, so other students may be able to see code placed there during the assessment period. A pull request is not required.

See [`workflows.md`](workflows.md) for examples for every route.

## Using Gemini

Gemini is an expected part of the assessment workflow. You are not being assessed on whether you can write every line of PyTorch from memory, nor on whether your prompts sound sophisticated. You are assessed on whether you retain **intellectual control** of the investigation.

The assessment notebook contains a Gemini instruction context. If it is not active in your Colab session, copy the instructions in [`gemini-instructions.md`](gemini-instructions.md) into Gemini at the beginning of the conversation.

Gemini is instructed to treat each student prompt as one investigation step and provide material for **one notebook cell**: one code cell; short Markdown + one code cell; or Markdown-only when computation is unnecessary.

Every Gemini response must also begin with exactly **one category label** as the first text in the response:

- `[MAIN]` — implements, changes, runs, or otherwise advances the main investigation;
- `[CLARIFICATION]` — asks for, resolves, or states an assumption or definition needed before proceeding;
- `[CRITICAL]` — challenges a claim, identifies a confound or risk, or proposes a validation check;
- `[INTERPRETATION]` — explains what existing evidence does or does not support.

For example:

> `[MAIN] Implement a basic autoencoder`

The category is chosen according to the **main purpose of that response**. Gemini should use one label only and should not append a separate multi-category trail at the end. These labels provide a lightweight chronological trail through the full conversation.

## AI interaction record — assessed evidence

In Section 9 of the notebook, select **exactly four** moments from your Gemini conversation:

1. a moment that helped frame or refine the investigation;
2. a technical or experimental decision;
3. a moment where a suggestion or interpretation was challenged, rejected, modified, or explicitly verified;
4. a moment concerned with interpreting the evidence.

For each moment, identify where it occurs in the full conversation, state what Gemini contributed, state what **you** decided, and give the evidence or reasoning for that decision.

The quality of the prompt itself is not the point. Strong evidence of AI collaboration might show that Gemini proposed explanation X, you recognised Y as an alternative explanation, and you then designed a test that distinguished between them.

## Full Gemini conversation — required audit trail

You must also submit a **full, chronological copy of every Gemini conversation materially used for the assessment**.

The transcript is supporting evidence and is **not normally read in full during marking**. Markers should normally be able to assess the AI-collaboration criterion from the four selected moments in the notebook. The complete transcript may be consulted for moderation, academic-integrity checks, or where the selected evidence is unclear.

The transcript may be submitted as PDF, HTML, Markdown, or plain text, provided that the order of student and Gemini turns is clear. Do not edit the conversation to improve it after the event. Credentials, API keys, or other secrets may be redacted; mark any such omission explicitly as `[REDACTED CREDENTIAL]`.

If your work spans multiple Gemini chats or restarted conversations, include all conversations that materially influenced the submitted work.

A transcript template is provided in [`templates/gemini-conversation.md`](templates/gemini-conversation.md).

## Process evidence and academic integrity

The notebook, full Gemini conversation, category-labelled responses, selected AI-interaction moments, experimental outputs and any submitted implementation files together provide evidence of how the investigation developed. They make it easier to connect reasoning with code changes and results.

These artifacts are **process evidence rather than a guarantee of authorship**. You remain responsible for understanding and being able to explain the decisions, implementation and claims in your submission. Where the provenance of work is unclear, the module team may use the submitted process evidence in accordance with normal university academic-integrity procedures.

## Evidence before polish

A successful run is not enough. Your investigation should normally include an appropriate baseline, control, ablation, intervention, diagnostic, or comparison that makes the main claim testable.

Examples of useful questions include:

- Does this component improve the intended capability, or only the headline metric?
- Does a representation contain information, and does the model actually use it?
- Does an explanation survive a controlled intervention?
- Is an apparent gain caused by architecture, data, optimisation, compute, or an unfair comparison?
- Does the result hold across seeds, examples, stories, classes, or perturbations where that matters?

Negative or failed results can be strong evidence when they are carefully diagnosed.

## What changed my mind?

You must identify **one claim, expectation, explanation, or Gemini suggestion that you revised because of evidence**.

This does not need to be a dramatic failure. The purpose is to show that the investigation changed your model of the problem rather than merely confirming an answer you already intended to give.

## Marking criteria

All four routes use the same rubric.

| Criterion | Weight | Markers are looking for |
|---|---:|---|
| Question, motivation and connection to module theory | **15%** | A clear, worthwhile question; appropriate theoretical motivation; a meaningful prediction rather than a post-hoc story. |
| Experimental design / architectural reasoning | **20%** | Appropriate comparisons, controls, baselines, interventions or ablations; awareness of confounds; a design capable of answering the stated question. |
| Technical implementation and validity | **20%** | Correct and inspectable implementation; appropriate use of the supplied system; reproducible setup; technically valid measurements and data handling. |
| Results and quality of evidence | **20%** | Relevant, readable evidence; appropriate metrics and diagnostics; enough evidence to support or challenge the central claim rather than a single convenient result. |
| Interpretation, limitations and conclusions | **15%** | Conclusions proportional to the evidence; links back to theory; recognition of uncertainty and alternative explanations; a clear answer to the original question. |
| Critical use of Gemini | **10%** | Purposeful use of AI while retaining ownership of decisions; checking, modifying, rejecting, testing, or qualifying AI suggestions using reasoning and evidence. |

### What does not earn marks by itself

The following are not substitutes for the criteria above:

- using a larger model;
- using a fashionable architecture;
- producing a very long Gemini conversation;
- writing elaborate prompts;
- obtaining a higher headline score without a fair comparison;
- including large amounts of generated code without explaining what matters;
- agreeing with Gemini without testing or evaluating its claims.

## Submission artifacts

Submit:

1. the completed **assessment notebook** (`.ipynb`);
2. the **full Gemini conversation transcript(s)** (`.pdf`, `.html`, `.md`, or `.txt`);
3. any supporting source/configuration files required to reproduce changes that are not contained in the notebook.

If you have been authorized to use a student repository/fork, record its URL in the notebook and submission manifest.

Use [`templates/submission-manifest.md`](templates/submission-manifest.md) as a final check when preparing the submission.

Administrative details such as deadline, submission system, and file-naming rules are provided separately by the module team.
