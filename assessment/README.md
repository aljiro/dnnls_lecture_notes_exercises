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

**Typical workflow:** import a pinned supplied architecture version without changing it, and perform probes, ablations, interventions, diagnostics and analysis in the assessment notebook. A student fork is normally unnecessary. See [Route A workflow](workflows.md#route-a--investigate-the-existing-architecture).

### Route B — Make an important architectural change

Replace, remove, or substantially modify one component of the reference system and test the consequences. The important part is not the size of the change, but the quality of the hypothesis, comparison, controls, and interpretation.

**Typical workflow:** if the change is local, import the reference architecture and define only the changed component in the notebook. If the change requires coordinated edits across several source files, use a student fork and pin the exact commit used for the experiments. See [Route B workflows](workflows.md#route-b--make-an-important-architectural-change).

### Route C — Build an alternative architecture

Construct a substantially different solution and compare it fairly with the reference system. A Transformer + CLIP approach is one possible example. A more capable model does not automatically constitute a stronger investigation: the comparison must reveal something useful about the task, representation, optimisation, inductive bias, or architecture.

**Typical workflow:** import the reference model from the supplied repository and implement the alternative either in the notebook/small supporting module or, for a substantial multi-file system, in a pinned student repository. See [Route C workflow](workflows.md#route-c--build-an-alternative-architecture).

### Route D — Ask a scientific question

Use the architecture to investigate a claim about what or how the system learns. Examples include questions such as whether the model learns a concept of place, whether information about characters or locations can be read from an internal representation, whether the model actually uses a variable that appears predictive, or whether an apparent representation survives an intervention.

**Typical workflow:** keep the supplied architecture unchanged and treat it as the object of study. Put probes, controlled interventions, shuffled-label tests, retrieval analyses or other scientific instrumentation in the notebook. A fork is normally unnecessary. See [Route D workflow](workflows.md#route-d--ask-a-scientific-question).

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

## Reproducibility and architecture versions

You may work from any architecture version made available for the module. The supplied versions (`v1`, `v2`, and so on) live as separate folders/modules inside the architecture repository. Record both the architecture version and the exact **repository tag or commit** used. Do not rely on an unpinned moving `main` branch for the final submitted result.

Where the architecture lives in a separate repository, prefer importing or cloning the pinned source rather than copying large pieces of supplied model code into the notebook. See [`architecture-import.md`](architecture-import.md).

A good general rule is:

> **Import the reference system; expose your intervention; keep the experiment in the notebook.**

If you substantially alter the supplied implementation, make the change inspectable. For a local change, a focused replacement component in the notebook is preferable to copying the whole architecture. For coordinated multi-file changes, a student fork/repository with an exact commit is appropriate. A pull request is optional; it is not required for the assessment.

See [`workflows.md`](workflows.md) for examples of choosing between these approaches.

## Using Gemini

Gemini is an expected part of the assessment workflow. You are not being assessed on whether you can write every line of PyTorch from memory, nor on whether your prompts sound sophisticated. You are assessed on whether you retain **intellectual control** of the investigation.

The assessment notebook contains a Gemini instruction context. If it is not active in your Colab session, copy the instructions in [`gemini-instructions.md`](gemini-instructions.md) into Gemini at the beginning of the conversation.

Gemini is instructed to treat each student prompt as one investigation step and provide material for **one notebook cell**: one code cell; short Markdown + one code cell; or Markdown-only when computation is unnecessary.

Every Gemini response is also required to end with a compact **AI TRAIL** containing four categories:

- `[CLARIFICATION]` — an assumption, definition, question, or refinement;
- `[MAIN CHANGE]` — the main implementation, model, data, or experimental-design change;
- `[CRITICAL]` — a risk, uncertainty, alternative explanation, disagreement, or validation check;
- `[INTERPRETATION]` — what the available evidence does or does not currently support.

The trail is an index into the conversation. It is **not** a replacement for the conversation itself.

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

If your implementation lives in a student repository/fork, record the repository URL and exact commit SHA in the notebook and submission manifest. The notebook must remain understandable even when external supporting files are used.

Use [`templates/submission-manifest.md`](templates/submission-manifest.md) as a final check when preparing the submission.

Administrative details such as deadline, submission system, and file-naming rules are provided separately by the module team.
