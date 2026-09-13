# Experiment 2 — Why did the hidden layer go silent?

**Dataset:** A small synthetic two-class 2D dataset generated directly in the notebook. The task is intentionally easy enough that a healthy tiny MLP should learn it reliably.

**Key concepts:** training dynamics, ReLU, dead activation, gradient flow, initialisation, hidden representation, activation spread, gradient norm, optimisation failure, representation failure.

**Expected computational budget:** Very light. Several tiny MLPs are trained for a small number of epochs on CPU.

**Recommended runtime:** **CPU.** A GPU is unnecessary.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Generate a reproducible 2D binary-classification dataset with two moderately nonlinear but easily separable class regions. Split it into training and validation sets. Build a tiny PyTorch classifier with architecture `2 inputs → 8 hidden ReLU units → 1 output logit` and `BCEWithLogitsLoss`. Use a normal sensible initialization and a simple optimizer. Train for enough epochs to solve the task comfortably. During this one run, record at every epoch: train loss, validation loss, train accuracy, validation accuracy, the fraction of hidden activations equal to zero, the standard deviation of hidden activations, and the gradient norm of the first layer. Save several checkpoints. Plot the final decision boundary and the recorded curves. Briefly explain the model's input, hidden and output shapes and why the output is called a logit.

### Questions

1. Does the healthy network learn the task?
2. Does a ReLU outputting zero sometimes mean something is wrong?
3. What happens to hidden-activation spread during successful training?
4. Do gradients reach the first layer throughout training?
5. Why did we record these measurements during the training run rather than planning to retrain later?

---

## Prompt 2

> Train a second network with exactly the same architecture, data, optimizer and seed structure, but deliberately initialize the first-layer bias to a large negative value such as `-5.0` while keeping the rest of the setup unchanged. Record the same measurements as before. Plot healthy and altered runs side by side: losses, accuracies, fraction of zero hidden activations, hidden activation spread, and first-layer gradient norm. Also show both final decision boundaries. Do not repair the altered network yet. Briefly describe only what differs in the initialization.

### Questions

1. Did the altered network's training loop still execute normally?
2. What happened to its hidden activations?
3. What happened to the first-layer gradient norm?
4. Can the output layer still change even when the hidden layer carries little useful variation?
5. Is “the code ran without errors” evidence that useful learning occurred?

---

## Prompt 3

> Reuse the saved checkpoints from both runs; do not retrain. At four checkpoints from early to late training, plot the 8 hidden-unit activation distributions for the healthy and altered networks. Also report, for each checkpoint, how many hidden units are active for at least 5% of the training examples. Then pass a grid of input points through each saved network and report the standard deviation of the output logits across the grid. Keep the interpretation descriptive for now.

### Questions

1. Does the altered network produce a varied hidden representation?
2. How does output-logit spread compare between the two networks?
3. Can a network have many parameters while effectively behaving like a much simpler predictor?
4. Which measurement gives stronger evidence of a representation problem: final loss alone or the activation diagnostics?

---

## Prompt 4

> Starting again from the same initial random weights, compare three first-layer bias choices: the healthy default, `-1.0`, and `-5.0`. Train each once with otherwise identical settings and record the same diagnostics. Put `first_layer_bias` on a clearly visible line in the training function. Plot final validation accuracy, fraction of dead hidden units, hidden activation spread, and first-layer gradient norm against the three bias choices. Briefly explain how the ReLU derivative connects a negative pre-activation to the gradient reaching an earlier parameter.

### Questions

1. Does the failure appear suddenly or gradually as the bias becomes more negative?
2. What is the relationship between inactive ReLUs and first-layer gradients?
3. Why is this more than simply “the optimizer chose a bad direction”?
4. Which Week 3 backpropagation observation has now become a training pathology?

---

## Prompt 5

> Take the deliberately failed `-5.0` setup and make only one repair: restore a sensible first-layer initialization/bias while leaving the optimizer, learning rate, dataset, architecture and training duration unchanged. Train once and compare the repaired run with the failed run using the saved diagnostics. Do not add extra layers, change optimizer, or tune several hyperparameters at once. Briefly explain why changing one factor at a time makes the diagnosis stronger.

### Questions

1. Did useful hidden variation return?
2. Did gradients return to the first layer?
3. Did validation performance recover without changing the optimizer?
4. What evidence now supports initialization/activation failure over a generic claim that “training was difficult”? 

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 4 in this experiment**. Change the intermediate bias value from `-1.0` to a value of your choice between the healthy setting and `-5.0`.

Before running, predict whether most ReLUs will remain active, become partly inactive, or become almost completely silent.

- Was your prediction correct?
- How closely did activation spread track validation accuracy?
- Did the gradient norm collapse before, after, or at roughly the same time as the activations?

---

## Reveal: what was this experiment really about?

The objective was to distinguish a **training/representation failure** from a merely high loss.

A mathematically valid network can become effectively useless if its hidden representation collapses. With ReLU, sufficiently negative pre-activations produce zeros, and their local derivative blocks gradient flow to earlier parameters. The optimizer can keep running while much of the model has stopped receiving a useful learning signal.

The important engineering habit is therefore to inspect what happens *inside* training: activations, gradients, prediction spread and trajectories, not only the final loss.

Now ask Gemini:

> We trained the same tiny classifier under healthy and deliberately bad first-layer initialization. Discuss with me how the activation, gradient and prediction-spread evidence lets us diagnose the failed network. Distinguish “the optimizer is running”, “parameters are changing”, “gradients reach an early layer”, and “the hidden representation carries useful variation”. Connect the explanation directly to our saved curves rather than giving a generic account of dead ReLUs.

### Final discussion questions

1. Why can a valid forward pass coexist with failed learning?
2. What makes a dead-ReLU problem a representation and gradient-flow problem rather than just a poor final score?
3. Which diagnostic would you look at first if a deeper network suddenly produced nearly constant predictions?
4. Why is changing one suspected cause at a time more informative than trying several fixes simultaneously?
