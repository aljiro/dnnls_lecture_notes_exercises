# Experiment 4 — Can a machine learn only from its mistakes?

**Dataset:** No external dataset. The experiment creates a tiny synthetic 2D binary-classification dataset of about 20 points directly in the notebook.

**Key concepts:** binary classification, linear classifier, decision boundary, weights and bias, prediction score, mistake-driven learning, perceptron, update size, linear separability, example order.

**Expected computational budget:** Negligible. Training the simple learner and producing the plots should take only seconds.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment and would add complexity without a useful speed benefit.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create a very small 2D binary classification dataset with about 20 points, split into two clearly separable classes. Plot the points. Add an arbitrary straight decision boundary that initially misclassifies several examples. For every point, show whether the current boundary classifies it correctly or incorrectly. Keep the dataset and boundary parameters available for later prompts. Do not train anything yet. After creating it, briefly explain the classifier you chose: what score it computes from the two input coordinates, what the weights and bias do, how that score creates a straight decision boundary, and how the score determines which class is predicted.

### Questions

1. Can a straight line separate the two classes in this dataset?
2. How many points does the initial boundary get wrong?
3. What information would a learner need in order to improve the boundary?
4. Does it need to know the perfect boundary in advance?

---

## Prompt 2

> Starting from the boundary in the previous prompt, implement a simple mistake-driven learning rule. Set `update_size = 1.0` near the top of the cell so I can easily change it later. Visit the training points one at a time. If the current boundary classifies a point correctly, do nothing. If it is wrong, change the weights and bias in the direction that would favour the correct class for that point, scaled by `update_size`. Process the dataset repeatedly until it completes a full pass with no mistakes, or for at most 30 passes. Record the number of mistakes in each pass and save the boundary after every update. Plot the mistakes per pass and show six representative snapshots of the boundary changing from its initial position to its final position. Do not use sklearn's Perceptron class. After implementing the rule, briefly explain one update using one mistaken point: what changes in the weights and bias, and why that change makes the correct class more likely for that point.

### Questions

1. What caused the boundary to move?
2. What happened when the learner encountered a point it already classified correctly?
3. Did the number of mistakes generally decrease?
4. At what point did learning stop?
5. Does this look more like calculating an answer directly, or gradually adapting a rule from experience?

---

## Prompt 3

> Reset the learner to exactly the same initial weights and bias, but shuffle the order of the same training points before each pass. Train it again with the same mistake-driven update rule. Plot the original final boundary and the new final boundary together with the dataset. Print the training accuracy of both solutions.

### Questions

1. Did the two runs necessarily end with exactly the same boundary?
2. Could both boundaries still classify every training point correctly?
3. What does this tell us about whether the data determine a unique solution?
4. Why might the order in which examples are presented matter to an iterative learning algorithm?

---

## Prompt 4

> Make one copy of the dataset and change the label of one carefully chosen point so that the two classes are no longer perfectly separable by a straight line. Reset the learner and run the same mistake-driven algorithm for 50 passes. Plot mistakes per pass and show the final boundary together with the modified dataset. Do not change the learning rule to solve the problem.

### Questions

1. Did the learner ever reach a pass with zero mistakes?
2. Does continued updating necessarily mean the implementation is broken?
3. What assumption about the dataset made the previous experiment easy?
4. What does this tell us about the relationship between a learning algorithm and the kinds of patterns its model can represent?

---

## Prompt 5

> Return to the original separable dataset. For every weight update during learning, calculate and store the prediction score for the point that caused the mistake immediately before and immediately after the update. Plot before-versus-after scores, using the true class to distinguish the points. Also print three concrete examples of an update: the point, its label, the weights before, the weights after, and how its score changed.

### Questions

1. Does an update usually move the mistaken point's score in the intended direction?
2. Does one update guarantee that all other points improve too?
3. How can many small local corrections eventually produce a useful global boundary?
4. What is the learner using as its teaching signal?

---

## Try it yourself manually

Without asking Gemini to modify the code, go back to the **code cell generated by Prompt 2 in this experiment**. Find `update_size = 1.0` and change it to `0.1`.

Rerun that cell.

- Does the learner still reach a separating boundary?
- Does it take more or fewer updates?
- Does the final boundary look exactly the same?
- Now try a larger update size. What changes, and what stays the same?

Do not worry yet about finding a "best" value. The point is to see which parts of the behaviour are controlled by this number.

---

## Reveal: what was this experiment really about?

The objective was to encounter an **early learning algorithm: the perceptron**, and to build intuition for **iterative learning, linear separability, and learning from an error signal**.

The learner never receives the correct line. It receives examples and whether its current decision is wrong, and changes its parameters incrementally. On linearly separable data this simple process can find a separating solution; when the model class cannot represent a perfect solution, the same update rule cannot make that limitation disappear.

Now ask Gemini:

> We have just built a mistake-driven linear learner without naming it until the end. Discuss with me how this perceptron experiment anticipates ideas we will meet later in neural networks. Focus on parameters, predictions, error signals, iterative updates, order of examples, and the difference between a limitation of the learning algorithm and a limitation of the model representation. Do not introduce backpropagation or gradient descent in detail yet; explain only the connection we can already justify from this experiment.

### Final discussion questions

1. In what sense did the machine "learn" rather than simply execute a fixed classification rule?
2. Why was the separability of the data important?
3. If two runs find different perfect boundaries, what might determine which solution is reached?
4. Which parts of this simple loop do you expect to reappear in more complicated neural-network training?
