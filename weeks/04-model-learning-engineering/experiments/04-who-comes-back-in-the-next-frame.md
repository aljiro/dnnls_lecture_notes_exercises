# Experiment 4 — Who comes back in the next frame?

**Dataset:** Structured character annotations from a manageable subset of the public StoryReasoning dataset. Each character has a persistent story-local `character_id`, allowing presence to be tracked across consecutive frames without processing image pixels.

**Key concepts:** binary classification, temporal feature, class imbalance, precision, recall, F1, baseline, threshold, story-level split, permutation control, input dependence.

**Expected computational budget:** Light. Initial annotation loading/parsing is the main cost. The resulting table has only four binary input features, and the tiny classifier trains in seconds on CPU.

**Recommended runtime:** **CPU.** A GPU is unnecessary.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a reproducible, memory-conscious subset of the `train` split of `daniel3303/StoryReasoning`, aiming for roughly 150–250 stories or enough to obtain a few thousand character-window rows. Do not process image pixels. Use the StoryReasoning parser utilities if convenient to parse each story's `chain_of_thought` into per-frame character tables. For every consecutive 5-frame window, collect the character IDs that appear at least once in input frames 1–4. For each such character create one dataframe row with `story_id`, `character_id`, four binary features `f1,f2,f3,f4` indicating presence in the input frames, and binary target `f5` indicating presence in frame 5. Keep `character_id` only as metadata, never as a model input. Also count and report: windows with no input characters, target-frame characters that never appeared in inputs 1–4, the fraction of target characters covered by the candidate set, number of stories, windows and character rows. Show a few rows. Cache the dataframe for later prompts. Briefly explain what one row means.

### Questions

1. What does a row such as `1,0,1,0 → 1` mean in plain language?
2. What happens to a character who appears in the inputs but not in frame 5?
3. Why should a character first appearing in frame 5 not secretly become an input candidate?
4. Is a window with no characters an error, or simply a window that contributes no rows to this subtask?
5. Why must `character_id` remain metadata instead of becoming a feature?

---

## Prompt 2

> Reuse the cached character-history dataframe. Group rows by the 16 possible four-bit histories `f1f2f3f4`. For every history report its count and the empirical probability that `f5=1`; ignore or clearly mark histories with very few examples. Plot the target probability for sufficiently common histories. Separately compute `P(f5=1 | f3=1)` versus `P(f5=1 | f3=0)` and the analogous quantities for `f4`, plus simple transition rates for patterns such as `1010` and `0101` if enough examples exist. Do not train a model yet.

### Questions

1. Do all four-bit histories lead to the same next-frame probability?
2. Is presence in frame 4 automatically the strongest single clue?
3. Are alternating histories such as `1010` or `0101` common enough to inspect?
4. What does this tell you about temporal structure before any neural network is introduced?

---

## Prompt 3

> Split the dataframe by `story_id`, not by individual rows, into reproducible training and validation stories. On the validation rows, evaluate three no-training baselines: (A) predict `f5 = f4` (“same as frame 4”); (B) predict present if the character appeared in any of frames 1–4; and (C) predict present if the character appeared in at least two of frames 1–4. Report positive-class prevalence, accuracy, precision, recall and F1 for each baseline. Also report the always-absent baseline. Briefly explain why story-level splitting is safer than randomly splitting overlapping rows/windows from the same story.

### Questions

1. Does the highest-accuracy baseline also have the highest F1?
2. What does the always-absent predictor reveal about class imbalance?
3. Which simple history rule is hardest for a learned classifier to justify beating?
4. Why do we need baselines before calling a learned classifier useful?
5. Why can overlapping windows from the same story make a random row split misleading?

---

## Prompt 4

> Train a tiny PyTorch binary classifier on the four history bits only: `4 inputs → 8 ReLU hidden units → 1 output logit`, using `BCEWithLogitsLoss`. Do not feed `story_id`, `character_id`, names, images or descriptions into the model. Briefly explain the model's inputs, output and main parameters. During one training run save train/validation loss, validation probabilities and several checkpoints. Compare validation accuracy/precision/recall/F1 at threshold `0.5` with the three rule baselines. Then sweep probability thresholds on the validation set and plot precision, recall and F1 versus threshold; identify the threshold giving the highest validation F1 without touching the test split.

### Questions

1. Does the learned classifier beat every trivial baseline?
2. Is threshold `0.5` automatically the best choice for F1?
3. What trade-off do you see between precision and recall as the threshold moves?
4. Why is the model still conceptually simple despite using a hidden layer?
5. What information is deliberately unavailable to this classifier?

---

## Prompt 5

> Reuse the trained classifier; do not retrain. Measure how much it depends on each of the four history positions by independently permuting `f1`, then `f2`, `f3`, and `f4` across the validation rows while leaving the targets unchanged. For each permutation report the change in F1 and the mean absolute change in predicted probability. Also evaluate one control where all four history columns are jointly shuffled across rows. Plot the effects by input position. Keep the interpretation tied to this classifier and dataset.

### Questions

1. Which frame-position feature appears most influential for the learned predictions?
2. Does disturbing frame 3 matter more or less than you expected?
3. What happens when the whole four-bit history is disconnected from its target row?
4. Why does a permutation control provide stronger evidence of input dependence than the training loss alone?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 4 in this experiment**. Find the probability threshold used to turn probabilities into binary predictions and replace the F1-optimal threshold with `0.5` (or vice versa).

Before rerunning, predict which of precision and recall will change most.

- Did accuracy and F1 move in the same direction?
- Which threshold would you choose if missing a returning character were more costly than predicting one too many?
- Why is a classification threshold a decision rule rather than a learned network weight?

---

## Reveal: what was this experiment really about?

The objective was to use a **real StoryReasoning subproblem** while keeping the machinery at the level you already understand.

The images, names and future visual encoders were deliberately left out. Each example was only a four-bit history followed by a binary question: does this same character appear next? That simple formulation exposed several Week-4 engineering issues at once: honest baselines, class imbalance, story-level splitting, threshold choice, and direct tests of whether predictions depend on the intended signal.

The structured annotations also revealed something about the domain itself before more complex architecture is introduced: movie editing can make an earlier frame surprisingly informative about who appears next.

Now ask Gemini:

> We predicted next-frame character presence using only four binary history bits. Discuss with me what the history-frequency table, trivial baselines, learned classifier, threshold sweep and permutation controls each tell us. Distinguish predictive signal from model complexity, and explain why this experiment does not require a visual encoder even though it comes from a visual storytelling dataset. Connect your discussion to our actual results.

### Final discussion questions

1. What did we learn from the annotations before training a network?
2. Why was F1 more informative than accuracy alone for this subtask?
3. What evidence shows whether the MLP actually uses the four-frame history?
4. What new machinery would be required if we wanted to infer character presence directly from raw image pixels rather than supplied annotations?
