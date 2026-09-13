# Experiment 4 — How does an error reach an earlier layer?

**Dataset:** No dataset is required. The experiment follows one scalar example through an extremely small two-layer network so every intermediate value can be inspected.

**Key concepts:** forward pass, intermediate activation, loss, computational graph, local derivative, sensitivity, chain rule, backward pass, gradient, backpropagation, autograd.

**Expected computational budget:** Negligible. The network contains only a few scalar values.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Build one scalar example with an input `x`, target `y`, and the tiny network `z1 = w1*x + b1`, `h = ReLU(z1)`, `y_hat = w2*h + b2`, `loss = (y_hat - y)**2`. Choose small simple numeric values so that `z1` is clearly positive and the prediction is not already perfect. Compute everything explicitly with ordinary Python/NumPy scalars, not PyTorch autograd. Print every intermediate value and draw a simple computational graph with the current numbers next to `x → z1 → h → y_hat → loss`, showing where the parameters enter. Briefly explain what the forward pass means in this exact graph.

### Questions

1. Which quantities are parameters and which are intermediate values?
2. Which value is produced by the hidden neuron?
3. Where is the nonlinearity applied?
4. What information does the loss contain about the final prediction?
5. During the forward pass, has any parameter changed yet?

---

## Prompt 2

> Keep exactly the same numbers. Estimate how sensitive the final loss is to each parameter `w1`, `b1`, `w2`, and `b2` using a very small centred finite-difference perturbation. Print the four estimated derivatives and, for one parameter from each layer, also print the losses obtained after the positive and negative perturbations. Do not use autograd or symbolic differentiation. Briefly explain what the sign and magnitude of one estimated derivative mean.

### Questions

1. Can changing an early-layer parameter affect the final loss even though it does not connect directly to the output?
2. Which sequence of intermediate quantities carries that effect forward?
3. What does a positive derivative tell you about a small increase in that parameter?
4. Why is finite-difference estimation useful conceptually but inconvenient for a network with millions of parameters?

---

## Prompt 3

> Now compute the same parameter derivatives by breaking the graph into local derivatives. Explicitly calculate quantities such as `d(loss)/d(y_hat)`, `d(y_hat)/d(h)`, `d(h)/d(z1)`, `d(z1)/d(w1)`, and the analogous terms for the biases and `w2`. Then multiply the appropriate local derivatives along each path to obtain `d(loss)/d(w1)`, `d(loss)/d(b1)`, `d(loss)/d(w2)`, and `d(loss)/d(b2)`. Show the calculations in a small table and compare the results numerically with the finite-difference estimates from the previous prompt. Do not use PyTorch yet.

### Questions

1. Why does the gradient for `w1` contain information from several later computations?
2. What role does the chain rule play?
3. Which local derivatives are reused when calculating gradients for several parameters?
4. Why is working backward through the graph more efficient than perturbing every parameter independently?

---

## Prompt 4

> Recreate exactly the same scalar network and numeric values using PyTorch tensors with `requires_grad=True`. Perform one forward pass and call `.backward()` on the loss. Print PyTorch's gradients beside the manual chain-rule gradients from the previous prompt and report the numerical differences. Briefly explain what autograd stored during the forward computation and what `.backward()` computes. Do not add an optimizer or update the parameters yet.

### Questions

1. Did autograd agree with the manual calculation?
2. Does `.backward()` itself perform gradient descent?
3. Why are intermediate forward values useful during the backward pass?
4. What work is autograd saving us from doing manually?

---

## Prompt 5

> Keep the same network but change only the first-layer bias enough that `z1` becomes clearly negative, so the ReLU output is zero. Repeat the explicit forward pass and PyTorch backward pass. Compare all parameter gradients with the previous positive-`z1` case. Plot or print the two computational paths side by side and highlight where the local derivative becomes zero. Briefly explain the immediate consequence without expanding into a general discussion of training pathologies.

### Questions

1. What happened to `h` when `z1` became negative?
2. What happened to the gradients for `w1` and `b1`?
3. Can the output-layer parameters still receive gradients?
4. Which local derivative blocked information from travelling farther backward?
5. What future training problem does this make you curious about?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 5 in this experiment**. Adjust the first-layer bias manually so that `z1` moves from clearly negative to clearly positive.

Before each rerun, predict whether the first-layer gradients will be zero or non-zero.

- Can you identify the point where the ReLU switches behaviour?
- What happens to the forward activation at the same point?
- Why are the forward and backward behaviours linked?

---

## Reveal: what was this experiment really about?

The objective was to encounter **backpropagation as efficient application of the chain rule through a computational graph**.

The loss depends on early parameters through a chain of intermediate computations. The backward pass starts from the loss sensitivity and combines local derivatives in reverse order. Autograd automates exactly this bookkeeping; it is not a separate learning rule and it does not update parameters by itself.

The final intervention also foreshadowed an important practical fact: if a ReLU is inactive, its local derivative can block gradient flow to earlier parameters. Week 4 will examine the training consequences more fully.

Now ask Gemini:

> We followed one scalar example through a forward pass, estimated parameter sensitivities by perturbation, reconstructed them from local derivatives, and then compared them with PyTorch autograd. Discuss with me why backpropagation is an efficient use of the chain rule rather than a mysterious neural-network-specific learning algorithm. Distinguish clearly between forward pass, backward pass, gradient computation, and parameter update using only this experiment.

### Final discussion questions

1. Why must an early parameter's gradient depend on later computations?
2. What is reused during backpropagation?
3. What is the difference between computing a gradient and using it to update a parameter?
4. Why does a computational-graph view become more valuable as networks get deeper?
