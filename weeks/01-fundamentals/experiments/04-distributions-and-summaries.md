# Investigation 4 — Can one number tell two digits apart?

**Dataset:** MNIST training set, focusing initially on digits **1** and **8**. Each image is reduced to one simple measurement: its mean pixel intensity (roughly, how much white "ink" is present).

**Expected computational budget:** Very small. Loading MNIST is the main overhead; all measurements and plots should take only seconds.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this investigation.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the investigation. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load or reuse the MNIST training set. Set `digit_a = 1` and `digit_b = 8` near the top of the cell so I can easily change them later. For every image belonging to either class, compute one number: the mean pixel intensity of that image after scaling pixels to the range 0 to 1. Plot overlapping histograms of these image-mean values for the two digits using the same bins. Also show a few example images from each digit near the low, middle and high ends of its image-mean values. Do not build a classifier yet.

### Questions

1. What does one point/value in each histogram represent?
2. Do the two digits tend to occupy exactly the same range of mean intensities?
3. Is one digit generally brighter than the other?
4. Do the two distributions overlap?
5. Looking at the example images, what visual property is this single number capturing? What is it throwing away?

---

## Prompt 2

> Reuse the image-mean values from the previous investigation. For each digit, calculate the mean, median, standard deviation, and the 25th and 75th percentiles. Print them in a small table. Plot the two histograms again and mark the mean and median of each class with vertical lines. Keep the two statistics visually distinguishable.

### Questions

1. Are the mean and median identical for each digit?
2. Which single number seems to describe the centre of each distribution reasonably well?
3. What information about the distribution is missing if you report only its mean?
4. Could two different distributions have the same mean?
5. What do the quartiles tell you that the mean alone does not?

---

## Prompt 3

> Take exactly the same image-mean values, but first ignore the digit labels and plot one histogram for all of them pooled together. Next to it, plot the same values separated into the two digit classes as before. Do not calculate any new feature; the only difference should be whether we use the digit label when looking at the distribution.

### Questions

1. What structure becomes harder to see when the labels are ignored?
2. Did the data values change when we split them by class?
3. What extra question are we answering when we ask "what is the distribution of mean intensity for digit 1?" rather than "what is the distribution of mean intensity?"
4. Why might knowing a class or context change the distribution we expect to see?

---

## Prompt 4

> Use only the image mean as a feature. Create the simplest possible rule for distinguishing digit 1 from digit 8: put a threshold halfway between the two class medians, and predict one class on one side and the other class on the other side. Report the accuracy and a 2x2 confusion matrix. Then show several misclassified images from both classes, including some close to the threshold. Do not train a more sophisticated classifier.

### Questions

1. Can one number classify the two digits better than random guessing?
2. Why does the rule still make mistakes?
3. Where in the histograms should we have expected most mistakes to occur?
4. Are the misclassified images necessarily strange or corrupted?
5. Is the problem the threshold, or is some information about the digit simply absent from this one-dimensional feature?

---

## Prompt 5

> Make a copy of the image-mean values for digit 1. Append ten artificial extreme values equal to 1.0 to that copy, without modifying the real dataset. Compare the mean and median before and after adding these extreme values. Plot the original and modified distributions side by side and mark both summary statistics. Make it very clear that the added values are artificial and are only being used to test the summaries.

### Questions

1. Which changed more: the mean or the median?
2. Why did the two measures react differently?
3. Which statistic better preserved the location of a "typical" original value in this artificial example?
4. Does this mean the median is always better than the mean?
5. What does this experiment suggest about choosing a summary statistic without thinking about the shape of the distribution?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to **INVESTIGATION 1** and change:

```python
 digit_a = 1
 digit_b = 8
```

to another pair, for example `0` and `1`, or `3` and `8`.

Rerun the investigation cells that use these variables.

- Did the amount of overlap increase or decrease?
- Did the simple threshold become more or less accurate?
- Are mean pixel values equally informative for every pair of digits?
- Can you find a pair for which this one-number representation is particularly poor?

---

## Reveal: what was this investigation really about?

The objective was to build intuition for **distributions, summary statistics, class-conditional distributions, and overlap**.

A measurement such as mean pixel intensity does not have one fixed value for a class: it has a distribution. The mean and median are different ways of summarising the centre of that distribution, but neither captures everything. When we looked at the distribution separately for each digit, we were examining a **conditional distribution**: the distribution of a feature given that we know the class.

The overlap between those conditional distributions also showed something important: a feature can contain useful information without being sufficient to determine the answer perfectly.

Now ask Gemini:

> We reduced every MNIST image to one number and compared how that number was distributed for two classes. Discuss with me what this experiment teaches about distributions, means, medians, conditional distributions, and overlapping classes. Connect the explanation directly to our histograms and threshold errors. Then explain why these ideas will matter later when machine-learning models produce features, predictions, or losses. Keep the discussion intuitive rather than introducing formal probability notation unless I ask for it.

### Final discussion questions

1. What is lost when we replace a whole distribution by only its mean?
2. In plain language, what does "the distribution of a feature given the class" mean?
3. Why can two overlapping class distributions still contain useful predictive information?
4. Why might we eventually want a model to use many learned features rather than one hand-chosen measurement such as mean pixel intensity?
