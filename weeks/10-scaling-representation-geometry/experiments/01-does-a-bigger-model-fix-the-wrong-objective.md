# Experiment 1 — Does a bigger model fix the wrong objective?

**Dataset:** A controlled synthetic conditional-regression problem with two valid futures for the same input, plus recorded scaling results from the StoryReasoning architecture.

**Key concepts:** scaling, model capacity, data quantity, optimisation, objective mismatch, data-limited versus capacity-limited behaviour.

**Expected computational budget:** Light. Several tiny MLPs are trained on synthetic data.

**Recommended runtime:** **CPU** is sufficient; GPU is optional.

**Estimated student time:** **20–25 minutes**, with roughly **1–3 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Create a reproducible synthetic regression dataset with scalar `x` in `[-1,1]` where each input has two equally likely valid target branches, for example `y = +(1 + 0.5*x) + noise` or `y = -(1 + 0.5*x) + noise`. Make a SMALL training set and a much larger held-out test set. Plot the data and report the conditional mean of the two branches. Do not train a model yet. Briefly remind me why one deterministic MSE prediction is being asked to summarise two possible futures.

### Questions

1. Is there one unique correct `y` for a fixed `x`?
2. Where does the conditional mean lie relative to the two branches?
3. What kind of failure would you expect if a model optimised MSE perfectly?

---

## Prompt 2

> Train two deterministic MLP regressors on exactly the same SMALL training set using MSE: a SMALL model such as two hidden layers of width 16, and a LARGE model such as width 256. Keep optimiser, epochs and random seed comparable. Save both models and plot their prediction curves over the test data. Report train MSE, test MSE, parameter count and the fraction of test predictions that fall in the low-density gap between the two target branches.

### Questions

1. Does the larger model fit the training set better?
2. Does increased capacity move predictions onto the two valid branches?
3. Is a lower training loss enough to say that the underlying prediction problem has been solved?
4. Which limitation here is about capacity, and which is about the objective?

---

## Prompt 3

> Keep the LARGE architecture fixed, generate a training set about 8–10 times larger from the SAME two-branch process, and train one fresh large model with the same MSE objective. Compare the three models in one table: parameter count, training examples, train/test MSE and gap fraction. Do not change the target distribution or loss.

### Questions

1. Does more data improve held-out MSE?
2. Does more data remove the between-modes prediction behaviour?
3. Can a model be both well-optimised and well-generalised while still predicting an undesirable statistical summary?
4. Why should “scale did not help” always specify what was scaled and what metric was measured?

---

## Prompt 4

> Use these recorded StoryReasoning results from the same 5,254 test windows. Make a compact table and bar plot of the REFERENCE versus SCALED system: text retrieval top-10 `41.5% -> 51.6%`; text cross-entropy `2.65 -> 2.40` (lower is better); character F1 `0.44 -> 0.46`; autoencoder reconstruction L1 `0.042 -> 0.036` (lower is better); image prior-mean L1 `0.131 -> 0.132`; image best-of-5 L1 `0.123 -> 0.124`. Compute absolute changes and mark whether each moved in the favourable direction. Do not invent significance tests. Then relate the pattern to the synthetic scaling experiment without claiming the two tasks are identical.

### Questions

1. Which parts of the StoryReasoning system clearly benefited from the scaling changes?
2. Which image-prediction metrics stayed effectively unchanged or worsened slightly?
3. Why is “the larger system is better” too coarse a conclusion?
4. What evidence is consistent with image prediction being limited by the objective rather than capacity alone?

---

## Try it yourself manually

Without asking Gemini to rewrite the experiment, return to the LARGE-model training cell from Prompt 2 and change only the hidden width from about `256` to something much larger such as `512` or `768`. Retrain only that one synthetic model.

Before running, predict both its training loss and its gap fraction.

- Does extra width improve fit?
- Does it move predictions toward actual modes?
- At what point does adding capacity stop addressing the real failure you care about?

---

## Reveal: what was this experiment really about?

Scaling is not one knob, and improvement is not one number.

More parameters can reduce approximation or optimisation limits. More data can improve generalisation. Better pretrained components can improve the representations entering a system. But none of these automatically changes **what the loss rewards**.

In the synthetic task, a larger deterministic MSE model can estimate the conditional mean more accurately—and therefore become a better optimiser of an undesirable point prediction. The updated StoryReasoning results show the same diagnostic principle at system scale: several heads improve when data and representations improve, while the next-frame image objective barely moves.

Now ask Gemini:

> Using our small/large/data-scaled synthetic models and the recorded StoryReasoning scaling table, explain the difference between capacity limitation, data limitation and objective limitation. Be careful to describe evidence rather than claiming that unchanged metrics prove a single cause.

### Final discussion questions

1. Why can scaling improve one head of a multi-task system but not another?
2. What would count as evidence that a model is capacity-limited?
3. What would count as evidence that an objective is rewarding the wrong behaviour?
4. Why should scaling studies report several metrics rather than only training loss?
