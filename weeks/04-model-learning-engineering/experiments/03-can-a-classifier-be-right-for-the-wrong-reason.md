# Experiment 3 — Can a classifier be right for the wrong reason?

**Dataset:** A small binary MNIST task using two digits. During training only, a tiny corner patch is deliberately correlated with the label so the network has access to an easy shortcut as well as the real digit shape.

**Key concepts:** training/validation split, shortcut feature, generalisation, distribution shift, ablation, permutation control, confidence, overfitting, leakage-like behaviour.

**Expected computational budget:** Light. A small MLP is trained once on a modest MNIST subset; later prompts reuse its saved predictions and checkpoints.

**Recommended runtime:** **CPU.** GPU is optional but unnecessary for the intended dataset size.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load MNIST and keep only two reasonably distinguishable digits, for example `3` and `8`, using a modest reproducible subset. Split examples into training and validation sets before making any modifications. For training images only, add a very small bright `3 x 3` corner patch to about 95% of examples of one class and leave the other class unpatched. Keep the validation images completely clean. Show a grid containing clean and patched examples from both classes, but do not train a model yet. Put `shortcut_probability = 0.95` near the top of the cell. Briefly explain exactly what statistical relationship the patch introduces without naming the hidden lesson of the experiment.

### Questions

1. Is the corner patch part of the handwritten digit itself?
2. How predictive of the class is the patch in the training set?
3. Does the clean validation set preserve that relationship?
4. Which cue seems easier for a learner to exploit: the whole digit shape or one fixed bright patch?

---

## Prompt 2

> Train a small PyTorch MLP on the flattened patched training images with architecture `784 → 32 ReLU → 1 logit` and `BCEWithLogitsLoss`. Evaluate after every epoch on both the patched training set and the clean validation set. During this one run, save epoch checkpoints, losses, accuracies, prediction probabilities, and the hidden activations needed for later analysis. Train long enough to see the trend but keep it fast. Plot train and validation loss/accuracy and show several validation mistakes with predicted probabilities. Briefly explain the classifier's input/output shapes and how the logit becomes a class probability for inspection.

### Questions

1. Does training accuracy become high?
2. Does validation accuracy improve equally strongly?
3. Is a low training loss enough to conclude that the classifier learned the digit distinction we intended?
4. Why is validation behaviour evidence about something different from optimization on the training set?

---

## Prompt 3

> Reuse the trained model and saved data; do not retrain. Evaluate the same final model on four versions of the validation images: (A) original clean images, (B) add the training-associated patch to the class that had it during training, (C) add that same patch to every validation image regardless of class, and (D) reverse the patch association so the other class receives it. Report accuracy, confusion matrix, mean predicted probability by true class, and how many individual predictions change relative to the clean images. Keep every digit's pixels unchanged except for the patch manipulation.

### Questions

1. Do predictions change when only the corner patch changes?
2. What happens when the patch association is reversed?
3. Does the classifier behave as if the patch contains class information even on otherwise identical digits?
4. What does this intervention tell us that train/validation accuracy alone did not?

---

## Prompt 4

> Reuse the final model. For each clean validation image, create an ablated copy where the `3 x 3` corner region used for the shortcut is forced to zero; also create a control copy where an equally sized unrelated corner region is forced to zero. Compare the probability changes caused by the shortcut-region ablation and the control ablation. Plot the distributions of absolute probability change and show a few images with the largest changes. Do not retrain.

### Questions

1. Does removing the shortcut region affect predictions more than removing an unrelated region?
2. Why is this an ablation rather than another training experiment?
3. Can a model genuinely use an input signal that we consider undesirable?
4. How does this differ from Week 2's case where shuffled inputs contained no useful signal at all?

---

## Prompt 5

> Reuse the saved epoch checkpoints from Prompt 2. For each checkpoint, evaluate clean validation accuracy and also evaluate accuracy after reversing the shortcut patch association. Plot both against epoch together with training accuracy. Identify the checkpoint with the best clean validation accuracy and compare it with the final checkpoint. Do not retrain or use the test set. Briefly explain why checkpoint choice should be based on evidence aligned with the behaviour we want.

### Questions

1. Does the final epoch automatically give the best clean validation performance?
2. At what point does training accuracy stop telling us much about clean generalisation?
3. Why would selecting a checkpoint using training loss favour the wrong behaviour here?
4. Why should the test set remain untouched while we make this choice?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 1 in this experiment**. Change:

```python
shortcut_probability = 0.95
```

to a weaker value such as `0.60` or `0.70`, then rerun the experiment's training and diagnostic cells.

Before rerunning, predict whether the network will rely on the patch more, less, or equally strongly.

- Does clean validation accuracy change?
- Does reversing the patch association still have a large effect?
- Can you find a regime where the shortcut is useful but no longer dominates?

---

## Reveal: what was this experiment really about?

The objective was to experience a **generalisation failure caused by a shortcut feature**.

The classifier was not necessarily failing to optimize. In fact, high training accuracy was evidence that optimization succeeded on the data it was given. The problem was that the training distribution contained an easy correlation that did not represent the behaviour we wanted to generalise.

Ablating, adding, or reversing the patch let us test the model's dependence on that signal directly. This is why validation data, distribution-aware controls and checkpoint selection matter: fitting the training set and learning the intended rule are not the same achievement.

Now ask Gemini:

> We trained a digit classifier with an artificial shortcut and then changed only that shortcut at evaluation time. Discuss with me how the training curves, clean validation results, reversed-patch control, ablation results and checkpoint comparison distinguish successful optimization from successful generalisation. Explain why the network's use of the patch is real learning even though it is not the rule we wanted.

### Final discussion questions

1. Why can excellent training performance coexist with poor generalisation?
2. What made the shortcut attractive to the network?
3. What is the difference between a signal being predictive and a signal being desirable?
4. Which diagnostic provided the strongest evidence that the classifier depended on the patch?
