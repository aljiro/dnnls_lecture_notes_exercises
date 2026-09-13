# Investigation 1 — How much can a sample fool you?

**Dataset:** MNIST training set: 60,000 grayscale images of handwritten digits 0–9. The notebook will download it automatically the first time it is needed.

**Expected computational budget:** Very light. Apart from the initial dataset download, each investigation should run in seconds to well under a minute. No model training is involved.

**Recommended runtime:** **CPU.** A GPU is not needed for this investigation and will not provide a meaningful advantage.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the investigation. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load the MNIST training dataset with torchvision. Do not train a model. Randomly select 20 images from the training set and show them in a grid with their digit labels. Also print the number of examples of each digit in this sample. Use a fixed random seed so we can reproduce the result.

### Questions

1. Looking only at these 20 examples, which digits would you think are common in MNIST?
2. Which digits would you think are rare?
3. Are there any digits missing completely?
4. If this were the only data you had seen, what claims about MNIST would you be tempted to make?

---

## Prompt 2

> Using the same MNIST dataset and the same random seed, repeat the sampling experiment for sample sizes 20, 50, 100, 500, 1000 and 5000. Do not show the images this time. For each sample size, calculate the proportion of each digit and plot the ten proportions as lines as sample size increases. Also calculate the true digit proportions in the complete training set and show them as horizontal reference lines.

### Questions

1. Which estimates change the most when the sample is small?
2. At roughly what sample size do the proportions begin to look stable?
3. Does a larger sample guarantee that every estimate is exactly correct?
4. What seems to happen to the size of the sampling error as the sample grows?

---

## Prompt 3

> Keep the sample size fixed at 100. Draw 200 different random samples from MNIST. For each sample, record the proportion of digit 0. Plot a histogram of those 200 estimates and mark the true proportion of digit 0 in the complete training set with a vertical line. Print the mean, minimum and maximum estimated proportion.

### Questions

1. Why do we get 200 different answers even though every sample came from the same dataset?
2. Is the true value usually near the centre of the distribution?
3. How different can a perfectly valid sample of 100 examples look from the full dataset?
4. If two students independently sampled 100 examples, could they reasonably reach different conclusions?

---

## Prompt 4

Before running this prompt, make a prediction: would a sample containing 1000 images always give a more representative estimate than a sample containing 100 images?

Then copy:

> Search among 500 random samples of size 100 and 500 random samples of size 1000. For each sample, measure the total absolute difference between its ten digit proportions and the true MNIST proportions. Find one unusually representative sample of size 100 and one unusually unrepresentative sample of size 1000. Print their class proportions side by side and their total errors.

### Questions

1. Did the larger sample always win?
2. Does this contradict the pattern from Prompt 2?
3. What is the difference between saying "larger samples are usually more representative" and "a larger sample must be more representative"?
4. Why is this distinction important when interpreting one particular dataset or experiment?

---

## Try it yourself manually

Without asking Gemini to write the code, change the sample size in **INVESTIGATION 3** from 100 to 25 and run it again.

- What happened to the histogram?
- Did the range of estimates become wider or narrower?
- Try 500 instead. Does the change go in the direction you expected?

---

## Reveal: what was this investigation really about?

The objective was **sampling and uncertainty**.

A dataset is not reality itself. It is a sample from some process or population, and measurements made on a sample fluctuate. Larger samples usually give more stable estimates, but an individual sample can still be unusually representative or unrepresentative.

Now ask Gemini:

> We have just investigated sampling variability using MNIST. Explain what this teaches us about training sets, validation sets and test sets in machine learning. Do not give me a generic definition first: connect the explanation directly to the results we observed in this notebook. Then discuss with me what could go wrong if I repeatedly use the test set while designing a model.

### Final discussion questions

1. Why should we be cautious about conclusions from a small validation set?
2. Why can two experiments report different results even when neither contains a bug?
3. What does this suggest about reporting only one accuracy number without saying how it was obtained?
