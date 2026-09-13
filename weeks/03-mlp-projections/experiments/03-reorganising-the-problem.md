# Experiment 3 — Can a hidden layer reorganise a difficult problem?

**Dataset:** A small synthetic two-moons binary-classification dataset generated directly in the notebook.

**Key concepts:** MLP, hidden layer, hidden representation, ReLU, logit, decision boundary, width, training trajectory, linear separability, representation learning.

**Expected computational budget:** Light. The network is tiny and should train in seconds on CPU.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Generate a small noisy two-moons binary-classification dataset with a fixed seed and plot it with equal axis scales. Also search for a good straight decision boundary using the same kind of angle/offset search as in Experiment 1 and report the best linear accuracy you find. Do not train a neural network yet. Briefly explain why a single straight boundary is a restricted model for this geometry.

### Questions

1. Can one line follow the curved class structure perfectly?
2. Is the best straight boundary still useful despite being imperfect?
3. Where are most of its mistakes located?
4. What would a useful representation have to change about this geometry?

---

## Prompt 2

> Train a very small PyTorch MLP on this dataset with architecture `2 inputs → 2 hidden units → 1 output logit`. Put `activation = torch.relu` on a clearly visible line and use it between the two linear layers. Use `BCEWithLogitsLoss` only as the supplied training loss for this experiment; briefly state that the final scalar is a logit but do not turn this into a lesson on classification losses. Use a simple optimizer and fixed seed. Train long enough to fit the small dataset reliably, but keep it fast. During this one run, save model states and the 2D hidden activations at several useful checkpoints such as before training, early, middle, and final. Plot the final decision boundary and loss curve. Briefly explain the input, hidden and output shapes of the network.

### Questions

1. Did the nonlinear network improve on the straight-line baseline?
2. Is the final decision boundary one straight line in the original input space?
3. What does each example become after the hidden layer?
4. Why did we deliberately choose exactly two hidden units for this experiment?
5. What information did we save now so later prompts do not need to retrain the network?

---

## Prompt 3

> Reuse the saved checkpoints from the previous prompt; do not retrain. For each saved checkpoint, plot the original input points beside their 2D hidden activations, using the same class colours. In hidden space, also draw the output layer's straight decision boundary at that checkpoint. If it is straightforward, add a small play/slider control that lets me move through the already-saved checkpoints; the control must not retrain the model. Briefly describe only what visibly changes in the representation over training.

### Questions

1. How are the two classes arranged in hidden space before training?
2. What changes as training progresses?
3. Does the output layer still make a linear decision in hidden space?
4. How can a linear output solve a nonlinear-looking problem in the original space?
5. Is the network learning only a final classifier, or also a transformation of the data?

---

## Prompt 4

> Train a second network from the same initial seed and with the same `2 → 2 → 1` layer sizes, but replace the hidden ReLU with the identity function so there is no nonlinearity between the two linear layers. Use the same training settings and compare final accuracy, original-space decision boundary, and hidden representation with the ReLU network. Also calculate the single equivalent weight matrix/vector and bias obtained by composing the two trained linear layers of the identity network, and verify numerically that it gives the same logits. Briefly explain the equivalence.

### Questions

1. Did adding a second linear layer without a nonlinearity solve the curved problem?
2. Can the two identity-separated linear layers be collapsed into one linear map?
3. How does the hidden representation differ from the ReLU network's representation?
4. What exactly is the nonlinearity buying us?

---

## Prompt 5

> Return to the trained ReLU network. Without retraining, create two ablations: in one, force hidden unit 1 to zero for every example before the output layer; in the other, force hidden unit 2 to zero. For each ablation, report accuracy and plot the resulting decision boundary next to the intact network. Also show the hidden-space points with the removed coordinate collapsed to zero. Briefly explain what was changed and what was left untouched.

### Questions

1. Did removing either hidden unit change the predictions?
2. Did both hidden units contribute in exactly the same way?
3. What does the ablation tell you that final accuracy alone did not?
4. Why is it useful to think of hidden units as parts of a learned representation rather than as isolated mini-classifiers?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 2 in this experiment**. Change:

```python
activation = torch.relu
```

to:

```python
activation = torch.tanh
```

Rerun that training cell and then rerun the hidden-representation visualisation generated by Prompt 3.

Before rerunning, predict whether the hidden geometry will look exactly the same, somewhat different, or fail completely.

- Did the network still learn the task?
- How did the hidden representation change?
- Does a different successful representation imply that there is only one correct internal geometry?

---

## Reveal: what was this experiment really about?

The objective was to see an MLP as a **learned transformation of a problem**, not merely as a more complicated formula for the final prediction.

The output layer remained linear in its own input: the hidden representation. The nonlinear hidden layer learned coordinates in which the classes became easier to separate. Removing the nonlinearity collapsed the stacked layers back to a linear model, while removing hidden units showed that the learned representation itself mattered to the final behaviour.

Now ask Gemini:

> We watched a two-unit hidden representation change during training. Discuss with me how the MLP reorganised the two-moons problem so that a linear output layer could classify it. Compare the ReLU network, the identity network, and the hidden-unit ablations. Then explain depth, width and hidden representation using this exact tiny network rather than giving generic definitions.

### Final discussion questions

1. Where in this network is the nonlinear decision boundary really being created?
2. What is the relationship between the hidden representation and the output decision boundary?
3. Why can two networks solve the same task with different hidden geometries?
4. What do depth and width mean in the specific `2 → 2 → 1` network you trained?
