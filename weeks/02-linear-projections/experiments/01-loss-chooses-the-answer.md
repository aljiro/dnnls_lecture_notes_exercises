# Experiment 1 — What answer does a loss function prefer?

**Dataset:** A tiny synthetic set of scalar target values, followed by a small subset of MNIST images. No model training is required.

**Key concepts:** prediction error, loss function, mean squared error (MSE), mean absolute error (MAE/L1), mean, median, outliers, constant prediction, pixel-wise loss.

**Expected computational budget:** Very light. All prompts should run in seconds after MNIST is available.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create the target values `[1, 2, 2, 3, 3, 3, 4, 4, 20]`. Imagine we are forced to predict the same single number for every target. Test constant predictions from 0 to 20 in small steps. For every possible prediction, calculate both mean squared error (MSE) and mean absolute error (MAE). Plot the two loss curves separately, mark the prediction that minimizes each one, and print those minimizing predictions together with the mean and median of the targets. Also add an interactive slider labelled `constant prediction` from 0 to 20. When I move it, update a marker on both loss curves and display the MSE and MAE for the selected prediction, while keeping the optimal points visible. Briefly explain what a constant predictor is and how each loss is calculated, but do not yet explain why the minima occur where they do.

### Questions

1. Do MSE and MAE prefer the same constant prediction?
2. Which minimum is closer to the mean?
3. Which minimum is closer to the median?
4. What is unusual about the value `20` compared with the other targets?
5. As you move the slider away from each optimum, do the two losses react in the same way?
6. Does the choice of loss appear to affect what counts as the "best" answer?

---

## Prompt 2

> Reuse the same experiment, but replace the final target value `20` by each of these values in turn: `5`, `10`, `20`, `50`, and `100`. For each version, find the constant prediction that minimizes MSE and the one that minimizes MAE. Plot the two optimal predictions as the extreme value increases. Also plot the mean and median of each target set. Keep the calculation explicit rather than using an optimizer.

### Questions

1. Which preferred prediction moves most as the extreme value grows?
2. Which summary statistic follows the MSE optimum?
3. Which summary statistic follows the MAE optimum?
4. What does this suggest about the sensitivity of mean and median to extreme values?

---

## Prompt 3

Before running this prompt, predict what would happen if there were two extreme values instead of one.

Then copy:

> Starting again from `[1, 2, 2, 3, 3, 3, 4, 4, 20]`, create three variants: the original data, a version with one additional value `20`, and a version with five additional values `20`. For each version, plot the target values on a number line and report the mean, median, MSE-optimal constant prediction, and MAE-optimal constant prediction. Briefly explain why adding more extreme observations eventually changes even a robust summary such as the median.

### Questions

1. Did the median remain fixed forever?
2. What matters besides how extreme an observation is?
3. Is "the median ignores outliers" an accurate statement, or an oversimplification?
4. Why should we care about the whole distribution rather than only one summary number?

---

## Prompt 4

> Load or reuse MNIST. Take at most 1000 training images of digit 8 and scale pixels to 0–1. Suppose we are forced to predict the same image for every one of these targets. Construct two constant images: the pixel-wise mean image and the pixel-wise median image. Show both images beside several real 8s. Then calculate the average MSE and average L1 error of each constant image against all selected targets. Briefly explain what "pixel-wise mean" and "pixel-wise median" mean here and why one scalar experiment can be applied independently at every pixel.

### Questions

1. Which constant image has lower MSE?
2. Which constant image has lower L1 error?
3. Do either of the constant images look exactly like a real handwritten 8?
4. How can an image be optimal for a loss while still looking artificial or blurry?
5. What does this suggest about interpreting a low loss value by itself?

---

## Prompt 5

> Repeat only the constant-image comparison from the previous prompt for a mixed set containing equal numbers of digits 1 and 8. Show the pixel-wise mean and median images and report their MSE and L1 errors. Do not train a model. Briefly compare these mixed-class constant images with the digit-8-only versions.

### Questions

1. What happened visually when two different kinds of targets were pooled together?
2. Can one constant image represent both classes faithfully?
3. Why might averaging or taking a median across several plausible targets produce something that resembles none of them exactly?
4. What question should we ask before deciding that a loss is an appropriate objective for a prediction problem?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 2 in this experiment**. Add an even more extreme value, such as `500`, to the list of tested extremes and rerun the cell.

Before running it, predict which curve will move more.

- Did the MSE-optimal prediction behave as you expected?
- Did the MAE-optimal prediction move at all?
- Change the original target values slightly. Can you make the median move without making any value more extreme?

---

## Reveal: what was this experiment really about?

The objective was to discover that a **loss function specifies what kind of error matters**, and therefore helps determine what answer a model prefers.

For a constant prediction, squared error is minimized by the **mean**, while absolute error is minimized by the **median**. For images with independent pixel losses, the same idea applies pixel by pixel. This is why an apparently reasonable numerical objective can reward a prediction that does not look like any individual target.

Now ask Gemini:

> We have just seen MSE prefer a mean and MAE/L1 prefer a median, first for numbers and then pixel by pixel for images. Discuss with me why a loss function is not merely a score we observe after training but part of the specification of what the learner is being asked to do. Connect the explanation directly to our outlier and MNIST results. Then give one example where MSE would be a sensible choice and one where L1 might be more sensible.

### Final discussion questions

1. In what sense does a loss function define what "good" means?
2. Why can two sensible losses prefer different predictions for the same data?
3. Why might a numerically optimal image still be visually unsatisfying?
4. What information about a prediction problem should influence our choice of loss?
