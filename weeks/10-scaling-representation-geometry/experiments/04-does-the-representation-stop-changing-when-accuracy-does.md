# Experiment 4 — Does the representation stop changing when accuracy does?

**Dataset:** A modest MNIST subset restricted to five classes, with a small MLP classifier whose penultimate features are recorded through training.

**Key concepts:** representation geometry, within-class scatter, class means, classifier alignment, late training dynamics, neural-collapse-style behaviour.

**Expected computational budget:** Light to moderate. One small classifier is trained once while intermediate features are cached.

**Recommended runtime:** **GPU** if available; CPU is workable with the reduced subset.

**Estimated student time:** **20–25 minutes**, including roughly **2–5 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Load a reproducible MNIST subset containing only digits `0`–`4`, using roughly 5000–8000 training examples and 1000–1500 held-out examples. Build a small MLP classifier with one clearly identified PENULTIMATE representation layer of about 16–32 dimensions followed by a final linear classifier. Before training, print the model and the shapes of the penultimate features and logits. Do not add an embedding loss or metric-learning objective.

### Questions

1. Which layer will we treat as the learned representation?
2. What does the final linear layer do with that representation?
3. At initialisation, should examples from one class already form compact groups?

---

## Prompt 2

> Train this model ONCE for about 20–30 epochs with ordinary cross-entropy. At EVERY epoch, record train accuracy, held-out accuracy and loss. Also, without storing every individual activation forever, compute and save these penultimate-feature diagnostics on a fixed held-out subset: average WITHIN-CLASS squared distance to each class mean; average distance BETWEEN class means; average cosine similarity between each class mean direction and its corresponding classifier weight direction. Save model checkpoints or compact feature snapshots at a few epochs such as 0, 1, 3, 5, 10, final. Use one fixed seed.

### Questions

1. Around which epoch does held-out accuracy become nearly saturated?
2. Do the geometric diagnostics stop moving at exactly the same time?
3. Why can cross-entropy continue changing after accuracy changes very little?
4. What does decreasing within-class scatter mean geometrically?

---

## Prompt 3

> Plot the training trajectory using separate compact figures: accuracy versus epoch; within-class scatter and between-class-mean distance versus epoch; and class-mean/classifier-weight cosine alignment versus epoch. Mark the first epoch where held-out accuracy reaches within 1 percentage point of its final value. Report how much each geometry metric changes AFTER that point. Do not claim a theorem from one small experiment.

### Questions

1. Does representation geometry keep organising after the headline accuracy metric is almost finished?
2. Which geometric quantity changes most late in training?
3. Why would a single final accuracy number hide this trajectory?
4. Does late geometric change necessarily imply better generalisation on every possible distribution shift?

---

## Prompt 4

> For the saved feature snapshots at several epochs, project the SAME held-out examples to 2-D using PCA fitted separately to each snapshot and colour by digit class. Beside each plot report within-class scatter and class-mean separation. Then compare the observed trend carefully with the idea of NEURAL COLLAPSE: late in supervised training, same-class features can compress while class means and classifier directions become more organised. Explicitly state which parts our toy experiment measures and which stronger symmetry claims it does NOT establish.

### Questions

1. Do classes become more compact or separated over training?
2. Why is a PCA picture only a partial view of the full feature space?
3. Which observations are consistent with neural-collapse-style organisation?
4. What additional measurements would be needed to make stronger claims about exact neural collapse?

---

## Try it yourself manually

Without asking Gemini to retrain anything, return to the snapshot-visualisation code from Prompt 4 and change only an `epoch_to_inspect` variable to compare at least three saved stages, for example `1`, `5`, and the final epoch.

Before viewing each plot, predict whether the classes will look more compact and whether that prediction matches the full-dimensional metrics.

- Does the PCA picture tell the same story as within-class scatter?
- Can two checkpoints have similar accuracy but visibly different feature geometry?
- Why should representation claims use quantitative diagnostics as well as plots?

---

## Reveal: what was this experiment really about?

Task performance can saturate before learning dynamics stop.

A classifier only needs the correct class logit to be largest. Cross-entropy can continue encouraging wider margins and more organised internal features after accuracy is already close to its final value. That means **representations have a training trajectory of their own**.

Neural collapse is one striking late-training phenomenon in supervised classifiers, but this small experiment is not a proof of its full theoretical geometry. Its role here is to teach a broader habit: if the scientific question is about a representation, measure the representation rather than assuming task accuracy tells the whole story.

Now ask Gemini:

> Using our accuracy curve, within-class scatter, class-mean separation, classifier alignment and saved feature snapshots, explain what continued changing after classification accuracy nearly saturated. Relate the observed trends cautiously to neural-collapse-style organisation and explain why representation geometry requires its own measurements.

### Final discussion questions

1. Why can accuracy remain unchanged while cross-entropy and geometry continue changing?
2. What does within-class compression reveal that accuracy does not?
3. Why should we avoid identifying every late-training geometric trend with neural collapse?
4. How does this experiment reinforce the course-wide idea of measuring the quantity that answers the actual question?
