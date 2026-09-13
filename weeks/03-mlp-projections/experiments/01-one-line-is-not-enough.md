# Experiment 1 — What can two hidden neurons do that one line cannot?

**Dataset:** A tiny synthetic XOR-style binary classification dataset formed by four small 2D clusters near the corners of a square.

**Key concepts:** binary classification, linear decision boundary, XOR, neuron, hidden layer, step activation, multilayer perceptron, intermediate representation, linear separability.

**Expected computational budget:** Negligible. No expensive training is required; all plots and calculations should run in seconds.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create a tiny 2D binary-classification dataset with four compact clusters centred approximately at `(0,0)`, `(0,1)`, `(1,0)`, and `(1,1)`. Give the diagonal corners `(0,0)` and `(1,1)` one class and the other two corners the other class, with a little random jitter and a fixed seed. Plot the points with equal axis scales. Do not build a classifier yet. Briefly explain the class pattern geometrically without naming the famous logical problem it resembles.

### Questions

1. Can you sketch one straight line that puts both classes on opposite sides?
2. If you move or rotate that line, which corner tends to become wrong?
3. Does the difficulty seem to come from noisy data or from the arrangement of the classes?
4. What kind of decision boundary might be needed instead of one straight line?

---

## Prompt 2

> Search over many possible straight decision boundaries by varying their angle and offset. For each boundary, choose the better assignment of the two sides to the two classes and measure classification accuracy on the dataset. Show the best straight boundary you found, report its accuracy, and also plot a small heatmap or contour of accuracy over the searched boundary parameters. Do not train a neural network and do not introduce a nonlinear classifier yet. Briefly explain what score the linear classifier computes and how that score creates one straight decision boundary.

### Questions

1. Did the search find a perfect straight-line classifier?
2. Is failure due to choosing a poor line, or does it persist after searching many lines?
3. What does this tell you about the expressive limit of this model class?
4. Why is "try harder to optimise" not necessarily a solution when the representation itself is insufficient?

---

## Prompt 3

> Keep the same data. Construct explicitly, without training, a tiny network with two hidden threshold/step neurons and one output threshold neuron that solves the four-corner pattern. Use simple weights and biases that are easy to inspect. Plot the two hidden neurons' straight decision boundaries on the original input space and report the network's final classification accuracy. After creating it, briefly explain the architecture: what goes into each hidden neuron, what each hidden neuron outputs, and how the output neuron combines those two hidden values. Do not hide the neuron calculations behind a high-level model class.

### Questions

1. Does each hidden neuron still make only a straight cut in the original space?
2. How can combining two simple cuts produce a decision rule that one cut cannot?
3. Which examples activate each hidden neuron?
4. Where has the extra representational power come from: more data, a different optimiser, or a different computation?

---

## Prompt 4

> For every example, record the pair of outputs from the two hidden neurons in the network from the previous prompt. Plot the original dataset on the left and the resulting 2D hidden representation on the right, using the same class colours. On the hidden-representation plot, draw the output neuron's decision boundary. Print the hidden coordinates for the four ideal corner patterns `(0,0)`, `(0,1)`, `(1,0)`, and `(1,1)`. Briefly explain what has changed and what has not changed between the two plots.

### Questions

1. Are the examples themselves different, or only their representation?
2. Was the class pattern linearly separable in the original coordinates?
3. Is it linearly separable in the hidden coordinates?
4. What job is the hidden layer performing before the output neuron makes its final decision?
5. How does this connect to Week 1's idea that a useful transformation can make a problem easier to separate?

---

## Prompt 5

> Return to the same explicitly constructed network, but replace the two hidden step activations with identity functions so that the hidden neurons output only their weighted sums. Keep the same layer structure and recompute the final outputs. Then show algebraically or numerically that the two linear layers can be collapsed into one equivalent linear transformation before the final threshold. Plot the resulting decision boundary and report the accuracy. Keep the explanation short and concrete.

### Questions

1. Did keeping two layers automatically preserve the successful behaviour?
2. What disappeared when the hidden nonlinearities were removed?
3. Why can two consecutive linear transformations be represented by one linear transformation?
4. Is depth by itself sufficient to create a nonlinear decision boundary?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 3 in this experiment**. Find one hidden neuron's bias and change it slightly.

Before rerunning, predict which region of the input space its boundary will move toward.

- Which corner patterns changed hidden activation first?
- Did the final classification immediately fail, or was there some tolerance?
- Restore the bias and then change one weight instead. How is changing a weight geometrically different from changing a bias?

---

## Reveal: what was this experiment really about?

The objective was to discover why **nonlinear hidden layers increase what a network can represent**.

A single linear classifier can only divide the input plane with one straight boundary. The four-corner pattern cannot be separated that way. Two hidden neurons can each make a simple linear cut, and nonlinear activations turn those cuts into new features. In that hidden representation, the output can solve a problem that was not linearly separable before.

This is the first architecture in the exercises, but deliberately only the smallest useful one:

`input → hidden layer → output`

Now ask Gemini:

> We have just solved a four-corner classification problem by transforming it through two hidden neurons. Discuss with me why the hidden layer changed the representational problem rather than merely adding more arithmetic. Connect the explanation directly to the original and hidden-space plots, and explain why removing the nonlinear activation collapses stacked linear layers back into a single linear transformation. Then tell me why this small network qualifies as a multilayer perceptron.

### Final discussion questions

1. What limitation did the single linear classifier have?
2. What did the hidden representation make easier?
3. Why was nonlinearity essential?
4. In what sense is an MLP learning or constructing a new coordinate system for a problem?
