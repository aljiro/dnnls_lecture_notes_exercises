# Experiment 3 — How much KL is enough?

**Dataset:** The same MNIST subset and VAE architecture from Experiment 2.

**Key concepts:** beta-VAE, KL weight, posterior collapse, prior mismatch, reconstruction–regularisation trade-off, diversity.

**Expected computational budget:** Light to moderate. Train three small VAE variants once each on the cached MNIST subset.

**Recommended runtime:** **GPU** if available.

**Estimated student time:** **20–25 minutes**, including roughly **3–6 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Reuse the cached MNIST data and VAE architecture from Experiment 2. Train three fresh models with identical seeds/capacity but different KL weights `beta = 0.0, 0.1, 1.0`, for the same small number of epochs. Record train/test reconstruction term, KL term, and total loss each epoch. Save the best state for each beta. Do not change anything else.

### Questions

1. Which beta gives the best reconstruction?
2. Which beta produces the largest KL?
3. What does `beta = 0` allow the posterior to do?
4. Is lower reconstruction error automatically evidence of a better generative model?

---

## Prompt 2

> For each saved beta model, draw 64 prior samples from `N(0,I)` and show matched sample grids. Also report: average pairwise pixel distance between generated samples as a simple diversity measure, nearest-training-image L1 distance as a crude fidelity measure, and the average posterior `mu` norm / latent standard deviation on held-out data. Do not retrain.

### Questions

1. Which model gives the sharpest or most recognisable samples?
2. Which gives the most diversity?
3. Does beta=0 reconstruct well but sample poorly from the prior?
4. What would very low sample diversity suggest?

---

## Prompt 3

> Compare posterior-sample reconstruction with prior sampling for the three models. For 100 held-out digits, encode each image and decode one posterior sample; also decode one independent prior sample. Report reconstruction error for posterior samples, KL, and a compact summary of prior-sample fidelity/diversity. Highlight any model where KL is near zero or where posterior and prior behave very differently. Briefly explain posterior collapse and prior/posterior mismatch without assuming either happened.

### Questions

1. When is the posterior carrying information about the target that the prior does not have?
2. What would KL near zero together with nearly identical samples indicate?
3. Why must reconstruction and sampling both be inspected?

---

## Try it yourself manually

Without asking Gemini to redesign the experiment, return to the training cell from Prompt 1 and change the middle setting from `beta = 0.1` to an intermediate value of your choice, such as `0.3` or `0.5`. Train only that one additional model and add it to the existing comparison.

Before running, predict whether reconstruction, KL and prior-sample quality will move monotonically between the neighbouring settings.

- Did the intermediate beta produce a simple compromise?
- Which metric would you use to choose beta if your goal were reconstruction?
- Which metric would you use if your goal were useful sampling?

---

## Reveal: what was this experiment really about?

The KL coefficient is not cosmetic. It controls a tension between **encoding the particular training target** and **keeping the posterior compatible with the prior used at generation time**.

Too little pressure can leave a gap between posterior codes and prior samples. Too much pressure can make the latent ignore the input. The useful regime is therefore an empirical trade-off, not “more KL is always better.”

Now ask Gemini:

> Using our beta sweep, discuss the evidence for reconstruction–regularisation trade-offs, prior/posterior mismatch and possible collapse. Explain why a VAE should be judged using both posterior/reconstruction behaviour and samples from the actual test-time prior.

### Final discussion questions

1. What failure does too little KL permit?
2. What failure does too much KL permit?
3. Why is the test-time prior central to evaluating a VAE?
4. How would this trade-off matter in a conditional model where the future itself is uncertain?
