# Experiment 1 — Can a worse-looking prediction get the better score?

**Dataset:** A modest cached subset of the public StoryReasoning dataset. Each story contains a sequence of movie frames. We will form consecutive 5-frame windows, treat frames 1–4 as context, and frame 5 as the target.

**Key concepts:** baseline, floor, L1/MAE, constant prediction, copy baseline, oracle baseline, metric interpretation, objective mismatch, shot continuation, shot cut.

**Expected computational budget:** Light. The first prompt must access and cache a small StoryReasoning subset; after that, the experiment is only image resizing, comparisons and plotting. No model is trained.

**Recommended runtime:** **CPU.** A GPU is unnecessary.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a manageable reproducible subset of the public `daniel3303/StoryReasoning` dataset, using streaming or another memory-conscious method if helpful. Aim for about 100–150 stories, enough to create several hundred consecutive 5-frame windows without downloading the entire dataset unnecessarily. For every story with at least 5 frames, create sliding windows of four input frames followed by one target frame. Resize only the frames needed here to `60 x 125`, scale pixels to 0–1, and cache the resulting windows so later prompts do not reload or resize them. Show 4 randomly selected windows as rows of five images labelled input 1, input 2, input 3, input 4, target. Do not build a model. Briefly explain what one 5-frame window represents.

### Questions

1. Does the target usually look like a small change from input 4, or do camera viewpoints often change sharply?
2. In the examples shown, is input 4 always the visually closest frame to the target?
3. If several different next shots are plausible, what difficulty might that create for a pixel-by-pixel prediction objective?
4. Why did we cache the resized windows rather than reload the dataset in every investigation?

---

## Prompt 2

> Reuse the cached StoryReasoning windows. Construct three image predictions for every window: (A) one constant pixel-wise median target image computed across the cached target frames, used for every window; (B) copy input frame 4; and (C) an oracle that, after looking at the target, chooses whichever of input frames 1–4 has the lowest pixel L1 distance to it. Set `near_copy_threshold = 0.06` near the top of the cell. Call a window `near-copy` if at least one of the four inputs has L1 distance at or below this threshold, otherwise call it `cut`. Report the mean L1 of all three predictors for all windows, near-copy windows, and cut windows, plus the percentage of windows in each group. Briefly explain why predictor C is an oracle and therefore a ceiling for any rule restricted to copying one input.

### Questions

1. Which simple predictor has the lowest overall L1?
2. Does copy-last behave differently on near-copy windows and cut windows?
3. Can the constant median image outperform a real frame from the same story on cut windows?
4. Why is the oracle useful even though it is not a valid deployable predictor?
5. What would be missing if we reported only one overall L1 number?

---

## Prompt 3

> Reuse the results from Prompt 2. Find several cut windows where the constant median image gets lower L1 than copy-last, and several near-copy windows where copy-last is much better than the median. For each example, display input 4, the constant median prediction, the target, and the two L1 values. Also show the four context frames for at least one example. Do not change the metric or train anything. Briefly describe only what is visibly different between the successful and unsuccessful cases for each baseline.

### Questions

1. Does the lowest-L1 image always look like the most plausible continuation to you?
2. What visual property allows a blurry or generic-looking image to obtain a competitive pixel score?
3. On which kind of window does copying an existing frame make sense?
4. Is poor copy-last performance on a cut evidence that the copied frame itself is a bad image?

---

## Prompt 4

> For every cached window, identify which input position 1–4 is closest to the target in pixel L1. Plot the frequency with which each position wins, once for all windows and once for near-copy windows only. Also report the mean distance from each input position to the target. Keep this as a descriptive analysis; do not fit a predictor to these frequencies.

### Questions

1. Is input 4 always the closest position?
2. Is there evidence that an earlier frame, such as frame 3, can be surprisingly competitive?
3. What does this suggest about assuming that temporal proximity always means visual similarity?
4. If a future model learned only these position frequencies, would it be using the actual content of each story window?

---

## Prompt 5

> Using only the saved measurements from this experiment, create one compact summary figure: the three predictor L1 scores for all / near-copy / cut windows, together with the near-copy proportion. Under the figure, print two or three concrete examples where the ranking by L1 conflicts with an intuitive visual ranking. Do not introduce a neural network. Keep the interpretation descriptive rather than naming the hidden lesson yet.

### Questions

1. Which baseline would look strongest if you saw only the overall score?
2. Which split reveals when copy-last is actually useful?
3. Why should a future learned model always be reported next to these floors?
4. What question should we ask before trusting a loss or metric as evidence that a model learned the behaviour we want?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 2 in this experiment**. Change:

```python
near_copy_threshold = 0.06
```

to a stricter value such as `0.04`, rerun the cell, and then try a looser value such as `0.08`.

Before each rerun, predict what will happen to the percentage of windows called near-copy.

- Do the baseline rankings inside each group remain qualitatively similar?
- Does the main conclusion depend on one exact threshold?
- Which threshold makes the two groups easiest for you to interpret visually?

---

## Reveal: what was this experiment really about?

The objective was to discover **objective and metric mismatch** on a real prediction problem.

Pixel L1 does exactly what it is asked to do: it rewards small average pixel differences. But when the next movie frame is often a different camera shot, there may be many plausible continuations and no single pixel-perfect answer determined by the inputs. In that situation a generic median-looking image can receive a better score than a sharp real frame from the same story.

This is why the StoryReasoning system will always need **floors**, meaningful data splits, and diagnostics that answer more than “did the loss go down?”. The failure here is not yet evidence of a bad optimiser or a bad neural-network architecture. The specification itself may reward the wrong behaviour.

Now ask Gemini:

> We compared a constant median image, copy-last and a best-of-four oracle on StoryReasoning, including separate near-copy and cut windows. Discuss with me what our own numbers show about using pixel L1 as both a training objective and an evaluation metric for next-frame prediction. Distinguish clearly between a weak model, a weak baseline, and a metric that rewards an undesirable answer. Then explain why the near-copy/cut split changes how we interpret the same predictor.

### Final discussion questions

1. Why is “lower loss” not automatically equivalent to “better continuation” here?
2. What does the best-of-four oracle tell us that copy-last alone does not?
3. Why are floors especially important before evaluating a complex model?
4. Which part of this problem seems to require better optimisation, and which part requires us to reconsider what we measure or predict?
