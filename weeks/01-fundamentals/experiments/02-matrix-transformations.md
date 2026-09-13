# Investigation 2 — What does a matrix do to a world?

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the investigation. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create a small asymmetric 2D shape from points — for example a simple arrow — so that rotations and reflections are easy to recognise. Plot it on axes with equal scale. Store the points in a matrix with one point per row. Then multiply every point by the matrix [[2, 0], [0, 1]] and plot the original and transformed shapes side by side. Print the coordinates of the first five points before and after the multiplication. Do not explain the matrix yet; let me inspect what happened first.

### Questions

1. What changed about the shape?
2. What stayed unchanged?
3. Looking at the matrix, which numbers seem responsible for the change?
4. Is it useful to think of the multiplication as producing new coordinates rather than as a collection of arithmetic operations?

---

## Prompt 2

> Reuse the same points. Apply four different 2x2 matrices, one at a time: a vertical stretch, a horizontal shear, a reflection across one axis, and a rotation by 45 degrees. Plot the original shape and all four transformed versions. Print each matrix above its plot. Keep the code explicit so I can change the matrix entries myself later.

### Questions

1. Which transformation was easiest to predict by looking at its matrix?
2. Which was hardest?
3. Does every matrix preserve lengths and angles?
4. What seems to be common to all these transformations despite their different visual effects?

---

## Prompt 3

Before running this prompt, predict whether doing transformation A and then transformation B will always give the same result as doing B and then A.

Then copy:

> Choose two clearly visible transformations from the previous investigation, such as a horizontal stretch and a shear. Apply A then B to the arrow, and separately apply B then A. Plot the two final shapes side by side. Also calculate the single matrix that represents each two-step transformation and print both resulting matrices.

### Questions

1. Were the two final shapes the same?
2. Were the two combined matrices the same?
3. What does this suggest about the order of transformations?
4. If a neural network applies several linear layers one after another with no non-linearity between them, what question does this experiment make you want to ask?

---

## Prompt 4

> Reuse the same arrow. Apply the matrix [[1, 0], [0, 0]]. Plot the result. Then try to recover the original points from the transformed points using only the transformed coordinates and that matrix. Explain in a few lines whether exact recovery is possible and show a visual comparison if useful.

### Questions

1. What happened to the two-dimensional shape?
2. Which information disappeared?
3. Why can we not simply reverse this transformation?
4. Can matrix multiplication therefore both transform information and destroy information?

---

## Prompt 5

> Create two small clouds of 2D points belonging to two classes that overlap when viewed in the original coordinates. Find or construct one simple 2x2 linear transformation that makes the separation between the two classes visually clearer, without training a classifier. Plot the clouds before and after the transformation and show the matrix you used.

### Questions

1. Did the labels change?
2. Did the points themselves change relative to the coordinate system?
3. Why can the same underlying examples look easier to separate after a transformation?
4. What might this have to do with the word "representation" in machine learning?

---

## Reveal: what was this investigation really about?

The objective was to build an intuition for **matrix multiplication as a transformation of representations**.

A matrix can stretch, rotate, reflect, shear, combine coordinates, project information away, and change which structure is easy to see. In neural networks, matrices are not merely pieces of arithmetic: they repeatedly construct new representations of the same underlying example.

Now ask Gemini:

> We have treated matrix multiplication as transforming a small geometric world. Discuss with me how this intuition carries over to a neural-network linear layer. In particular, explain what the rows/columns of a weight matrix are doing to an input representation, what information a projection can lose, and why several linear transformations in sequence raise an important question about the need for nonlinearities. Base the discussion on the plots we generated rather than starting from formal definitions.

### Final discussion questions

1. Why might a useful learned representation make a later prediction problem simpler?
2. What is the difference between changing the representation and changing the underlying example?
3. Why should we care whether a transformation is reversible?
