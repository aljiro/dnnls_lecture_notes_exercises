# Experiment 5 — What kind of failure are you looking at?

**Dataset:** No new dataset. This capstone reuses the measurements, checkpoints, controls and plots already produced in Experiments 1–4.

**Key concepts:** diagnosis, objective mismatch, optimisation failure, representation failure, signal-use failure, generalisation failure, baseline, ablation, permutation control, checkpoint selection, evidence.

**Expected computational budget:** Negligible. No new expensive training is required; the experiment analyses saved evidence from the notebook.

**Recommended runtime:** **CPU.** No special hardware is needed.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Review the investigations already present in this Week 4 notebook from Experiments 1–4. Using only measurements and outputs that actually exist in the notebook, create a compact evidence table with one row for each experiment. Include columns for: the main observed symptom; the most relevant baseline/floor; whether predictions changed when the intended input signal changed; any internal activation/gradient evidence; train-versus-validation evidence where available; and one alternative explanation that the data help rule out. Quote concrete values from the notebook when available rather than inventing numbers. Do not assign formal failure-category names yet.

### Questions

1. Which experiments required looking inside the network, and which could be diagnosed from outputs alone?
2. Where did a baseline provide evidence that a model score by itself could not?
3. Which experiment used an intervention on the input signal rather than only observing normal predictions?
4. Why is one symptom rarely enough to determine the cause of a failure?

---

## Prompt 2

> Reuse the saved checkpoint information from the shortcut-learning experiment. Build a small dataframe with one row per saved epoch/checkpoint and the available training loss, training accuracy, clean validation accuracy, and reversed-shortcut validation accuracy. Put `selection_metric = "clean_validation_accuracy"` on a clearly visible line. Select the best checkpoint according to that metric and print its epoch and measurements. Then also report which checkpoint would be selected by lowest training loss and whether it is the same model. Do not retrain anything. Briefly explain what a checkpoint-selection rule is doing.

### Questions

1. Do the two selection rules keep the same checkpoint?
2. Which rule is more aligned with the behaviour we actually want?
3. Why can the lowest training loss choose a model that is less useful at deployment?
4. What information would be leaked if we repeatedly used the final test set for checkpoint selection?

---

## Prompt 3

> Using the evidence table from Prompt 1, create four short anonymous diagnostic case cards, one derived from each of Experiments 1–4. Each card should contain only observed symptoms and diagnostic evidence from our notebook, not the experiment title and not the answer. Shuffle their order. Label them Case A–D. For each case include enough evidence to distinguish among these possibilities without defining them yet: objective/metric problem, optimisation or gradient-flow problem, representation problem, signal-use problem, and generalisation problem. Do not reveal the intended diagnosis.

### Questions

For each Case A–D, write your own diagnosis before continuing.

1. What is the strongest single piece of evidence for your diagnosis?
2. What competing explanation did you consider?
3. What additional measurement would you ask for if the case were still ambiguous?
4. Are any of the cases reasonably described by more than one failure category?

---

## Prompt 4

> Read the diagnoses I wrote directly above in the notebook for Cases A–D. Compare them with the evidence in the original Week 4 investigations. For each case, state which diagnosis is best supported and cite the specific notebook evidence that supports it. If more than one category genuinely applies, say which is primary and which is secondary. Now introduce and distinguish the terms `objective mismatch`, `optimisation failure`, `representation failure`, `signal-use failure`, and `generalisation failure`. Keep the explanation anchored to our four cases rather than giving dictionary definitions.

### Questions

1. Which categories were easiest to confuse?
2. Why can representation failure and optimisation failure occur together?
3. How can a model use a signal successfully and still generalise badly?
4. Why is objective mismatch fundamentally different from simply failing to minimise the objective?

---

## Prompt 5

> Turn the Week 4 evidence into a compact diagnostic workflow for a future neural-network experiment. Start from a symptom such as “the metric is poor” or “the training loss decreased but behaviour looks wrong”, and use questions such as: better than what baseline? does the metric reward the intended behaviour? do predictions vary with the intended input? what happens under permutation/ablation? do activations and gradients carry variation? do training and validation trends diverge? which checkpoint was selected and why? Present the workflow as a small decision tree or flowchart plus a short checklist. Use only concepts encountered in this week's notebook.

### Questions

1. Which diagnostic should usually come before changing the optimizer?
2. At what point would inspecting hidden activations become useful?
3. When is a shuffled/permuted control more informative than another training run?
4. Why should checkpoint choice appear in a diagnostic workflow rather than as an administrative detail?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 2 in this experiment**. Change:

```python
selection_metric = "clean_validation_accuracy"
```

to the training-loss option used in that cell and rerun it.

Before running, predict which checkpoint will be selected and whether its clean validation behaviour will be better or worse.

- Did the selected epoch change?
- What did you gain according to the new criterion?
- What did you lose according to the behaviour we actually care about?
- Restore the validation-based rule when finished.

---

## Reveal: what was this experiment really about?

The objective was to make **diagnosis itself part of neural-network engineering**.

A disappointing score does not uniquely identify a cause. Across this week we saw very different failures: a metric that rewards an undesirable answer, a hidden representation that goes silent, a classifier that exploits a shortcut, and a real temporal classifier whose usefulness can only be judged against baselines and signal-use controls.

The engineering task is therefore not “try a better optimizer” whenever something looks wrong. It is to gather evidence that separates competing explanations and then change the smallest relevant mechanism.

Now ask Gemini:

> Use the diagnostic workflow we just created to discuss how I should approach a future neural-network system that trains but behaves suspiciously. Base the discussion on the actual Week 4 cases: StoryReasoning pixel floors, dead hidden activations, shortcut generalisation, and character-history prediction. Explain why a baseline, a permutation/ablation control, internal-state diagnostics, train/validation curves and checkpoint selection answer different questions rather than being interchangeable tests.

### Final discussion questions

1. What evidence would convince you that an optimizer is genuinely the main problem?
2. What evidence would convince you that the objective is the main problem instead?
3. Why is “predictions depend on the input” necessary but not sufficient evidence of good generalisation?
4. Which Week 4 diagnostic habit do you expect to reuse most often in later architecture experiments?
