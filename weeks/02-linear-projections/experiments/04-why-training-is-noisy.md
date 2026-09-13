# Experiment 4 — Why is training allowed to be noisy?

**Dataset:** A synthetic one-dimensional regression dataset with a few hundred noisy examples generated directly in the notebook.

**Key concepts:** full-batch gradient descent, stochastic gradient descent (SGD), mini-batch, batch size, gradient estimate, epoch, update, shuffling, gradient noise, training loop.

**Expected computational budget:** Very light. The model has only two parameters and all runs should complete in seconds.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create 400 regression examples with `x` values between -3 and 3 and noisy targets approximately following `y = 3x + 2`. Use a fixed seed. Start a linear model `y_hat = w*x + b` from deliberately poor parameters. At those same parameters, calculate the exact MSE gradient using all 400 examples. Then calculate gradient estimates from 30 different randomly selected single examples and from 30 different random mini-batches. Set `batch_size = 16` near the top of the cell so I can easily change it later. Plot the resulting gradient vectors in `(dw, db)` space, marking the full-data gradient clearly. Keep the gradient calculation explicit rather than using an optimizer library. Briefly explain what data each of the three kinds of gradient uses.

### Questions

1. Do all single-example gradients point in exactly the same direction?
2. Are the mini-batch gradients more tightly grouped than the single-example gradients?
3. Is the full-data gradient inside or near the cloud of estimates?
4. What seems to happen to the reliability of the gradient estimate when more examples are included?
5. Why might using every example for every update be unnecessary?

---

## Prompt 2

> Reuse the same dataset and initial parameters. Train three copies of the same linear model for 20 epochs using the same learning rate: (A) full-batch gradient descent, (B) stochastic gradient descent with `batch_size = 1`, and (C) mini-batch gradient descent with `batch_size = 16`. Shuffle the training examples at the start of every epoch for B and C. Implement the updates explicitly. Record the full-dataset MSE after every parameter update and also at the end of every epoch. Plot the update-by-update loss curves, the epoch-end loss curves, and each model's path through `(w, b)` parameter space. Briefly explain what an update, a batch, and an epoch mean in this code.

### Questions

1. Which optimisation path is smoothest?
2. Does the full-dataset loss decrease after every SGD update?
3. Can a noisy parameter path still reach a good solution?
4. How many updates happen in one epoch for each batch size?
5. Why is comparing only the number of epochs potentially misleading when batch sizes differ?

---

## Prompt 3

> Repeat the mini-batch training with batch sizes `1`, `4`, `16`, `64`, and the full dataset. Put these batch sizes in one clearly marked list near the top of the cell so I can edit them later. For each batch size, calculate the number of updates per epoch and train for the same 20 epochs from identical starting parameters. Plot only the epoch-end loss curves so the overall trend is easy to compare. Also print a small table containing batch size, updates per epoch, total updates, and final loss. Keep the learning rate fixed for this experiment.

### Questions

1. Which batch sizes produce the noisiest learning?
2. Which batch sizes perform the most parameter updates during the same number of epochs?
3. Does the largest batch automatically reach the best solution fastest?
4. What changes simultaneously when you change batch size while keeping epochs fixed?
5. Why should batch size, number of updates, and number of epochs not be treated as interchangeable quantities?

---

## Prompt 4

Before running this prompt, predict whether shuffling should matter if every training example is still seen once per epoch.

Then copy:

> Sort the training examples by their `x` value. Train two SGD models with `batch_size = 1` from the same starting parameters and learning rate for 10 epochs. For one model, always visit the sorted examples in exactly that order. For the other, shuffle the examples independently at the start of every epoch. Record the parameter path and full-dataset loss after every update. Plot both paths and both loss curves. Briefly explain what is identical between the two runs and what differs.

### Questions

1. Did the two models see exactly the same examples overall?
2. Did they follow the same optimisation path?
3. Why can the order of examples matter when parameters change after every example?
4. What does shuffling protect us from when the dataset itself has an ordering?
5. How does this connect to the example-order effect you saw with the perceptron in Week 1?

---

## Prompt 5

> Using the mini-batch run with `batch_size = 16`, show one complete training iteration in detail for a single batch: the selected examples, predictions, residuals, batch loss, gradients, parameter values before the update, and parameter values after the update. Then show the same quantities for the next batch. Keep the explanation concise and connect each quantity to this loop: sample batch → forward pass → compute loss → compute gradients → update parameters → repeat.

### Questions

1. Which quantities are recomputed for every batch?
2. Which quantities persist from one batch to the next?
3. Why is the gradient different for the second batch even though the model architecture is unchanged?
4. Where exactly does learning occur in this loop?
5. Which part of this loop would become computationally expensive for a very large dataset and model?

---

## Try it yourself manually

Without asking Gemini to modify the code, return to the **code cell generated by Prompt 2 in this experiment**. Find the mini-batch setting `batch_size = 16` and change it first to `4`, then to `64`.

Before each run, predict whether the update-by-update loss will look smoother or noisier and whether there will be more or fewer updates per epoch.

- Were your predictions correct?
- Which change affected smoothness most visibly?
- Did changing batch size change how many examples were seen in one epoch?
- Did it change how many times the parameters were updated?

---

## Reveal: what was this experiment really about?

The objective was to build intuition for **stochastic gradient descent and mini-batch optimisation**.

The full-data gradient uses every training example and is therefore stable but potentially expensive. SGD and mini-batch methods use only part of the data for each update, so their gradients are noisy estimates of the full gradient. That noise makes individual steps less predictable, but many cheaper updates can still produce a useful optimisation trajectory.

An **epoch** counts passes through the dataset; an **update** counts parameter changes. Changing batch size changes how many updates occur in an epoch, so these quantities must be distinguished when comparing training runs.

Now ask Gemini:

> We compared full-batch gradient descent, single-example SGD, and mini-batch training on the same linear regression problem. Discuss with me why the stochastic gradients were noisy but still useful, why shuffling matters, and why batch size changes both gradient noise and the number of updates per epoch. Use the plots from this notebook rather than beginning with textbook definitions. Then connect the experiment to the practical training loop: batch → forward pass → loss → gradients → update.

### Final discussion questions

1. Why might a noisy gradient estimate be preferable to an exact gradient on a very large dataset?
2. What is the difference between seeing more data and performing more parameter updates?
3. Why can training loss wobble without implying that training is broken?
4. Which Week 2 ideas now appear together in one practical training loop?
