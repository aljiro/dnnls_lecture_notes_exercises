# Experiment 5 — Can several samples beat one StoryReasoning prediction?

**Dataset:** StoryReasoning 5-frame windows, represented by a frozen pretrained visual encoder and split by story.

**Key concepts:** conditional VAE, conditional prior, posterior, stochastic residual, KL divergence, best-of-K, diversity, conditioning test, latent-space generation.

**Expected computational budget:** Moderate. Frozen frame embeddings are extracted once; only small GRU/prediction heads are trained.

**Recommended runtime:** **GPU** for frame embedding extraction; the sequence models themselves are small.

**Estimated student time:** **30–35 minutes**, including roughly **3–7 minutes** of loading/embedding/training depending on Colab.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a manageable reproducible StoryReasoning subset and create roughly 1500–2500 consecutive 5-frame windows, split by STORY. Use a frozen ImageNet-pretrained ResNet-18 with its classification head removed to encode each needed frame ONCE into a cached 512-d embedding. Do not fine-tune ResNet. For each window store four context embeddings and the target-frame embedding. L2-normalise the embeddings for the prediction task. Show several windows and report train/validation counts. Briefly explain that we are modelling a distribution in visual representation space, not directly generating pixels.

### Questions

1. Which component is inherited/frozen and which part will we learn?
2. Why is this cheaper than building another image decoder?
3. What information is lost when we evaluate only in an embedding space?
4. Why must the split still be by story?

---

## Prompt 2

> Build a simple deterministic baseline: a small GRU reads the four 512-d context embeddings in order and its final state passes through an MLP that predicts the normalised target embedding. Train once with cosine-distance loss or MSE on normalised embeddings. Save the best validation checkpoint and predictions. Report validation target cosine distance plus retrieval top-1/top-5 when the predicted embedding ranks the true target among 20 candidate target embeddings (true target + 19 distractors from other validation stories, fixed seed). Also evaluate the same model with the four context embeddings replaced by contexts from other windows.

### Questions

1. Does the deterministic predictor beat a shuffled-context control?
2. What does retrieval tell us that raw training loss does not?
3. Does one predicted embedding represent several possible futures or only one point?

---

## Prompt 3

> Reuse the same GRU-style context summary idea but build a CONDITIONAL VAE head. Let the context state `h` parameterise a diagonal Gaussian PRIOR `p(z|h)`. Let a POSTERIOR network see both `h` and the true target embedding and output `q(z|h,target)`. Implement diagonal-Gaussian reparameterisation and `KL(q||p)` explicitly. A decoder/readout receives `h` and sampled `z` and predicts the target embedding. Train once with target-embedding reconstruction loss plus a modest `beta * KL`, using a short KL warm-up. Record reconstruction, KL and validation metrics each epoch; save the best checkpoint. Briefly explain why the posterior is allowed to see the target during training but the prior is what we sample from at test time.

### Questions

1. What information can the posterior use that the prior cannot?
2. Why must the prior learn to approximate useful posterior samples?
3. What would happen if KL pressure were effectively absent?
4. What would KL near zero plus nearly identical samples suggest?

---

## Prompt 4

> Evaluate the saved conditional VAE WITHOUT retraining. For every validation window, decode (A) the conditional prior mean and (B) `K=5` independent samples from the conditional prior. Report: prior-mean target cosine distance, average single-sample distance, best-of-5 distance, sample diversity as average pairwise distance among the five predictions, and top-1/top-5 retrieval using each predicted embedding. For best-of-5 retrieval, count a window successful if ANY of its five samples retrieves the true target at the requested rank. Also show several windows by displaying the four context frames, true target, and for each latent sample the nearest REAL validation frame to that predicted embedding as a visual proxy. State clearly that nearest-frame display is not a pixel decoder.

### Questions

1. Does best-of-5 improve over the prior mean or one sample on your subset?
2. Are the five samples meaningfully different?
3. Can average single-sample quality worsen while best-of-5 improves?
4. Why would that pattern be sensible for a multimodal future?

---

## Prompt 5

> Test whether the stochastic model actually uses its condition. Re-evaluate prior-mean and K=5 sampling after shuffling the four-frame context sequences across validation windows while keeping targets fixed. Compare target distance, retrieval and diversity with the true-context condition. Also compare posterior-sample reconstruction to prior-sample performance on the true contexts. Do not retrain. Summarise in one table.

### Questions

1. Does shuffling context hurt prediction quality?
2. Does sample diversity remain even if conditioning information becomes useless?
3. What does a large gap between posterior-sample and prior-sample performance indicate?
4. Why is diversity alone not proof of useful conditional generation?

---

## Try it yourself manually

Without asking Gemini to retrain anything, return to the **sampling/evaluation cell generated by Prompt 4**. Change `K` from `5` to `1`, `10`, and `20`, keeping the exact same trained model and evaluation windows.

Before running, predict the shape of the best-of-K curve.

- Does best-of-K keep improving indefinitely at the same rate?
- What happens to average single-sample quality as K changes?
- Why must any best-of-K result report K explicitly?
- At what K would the evaluation stop feeling like a realistic use case for this task?

---

## Reveal: what was this experiment really about?

This is a simplified latent-space version of the StoryReasoning system's variational next-frame idea.

The deterministic model maps four context frames to one point. The conditional VAE instead learns a **distribution of residual possibilities**: during training the posterior can use the target, while the KL term teaches the context-conditioned prior to imitate a distribution that can later be sampled without target access.

The key comparison is therefore not only “which one has the smallest average error?” A stochastic model may trade some average single-sample accuracy for diversity, while **best-of-K** reveals whether some samples land near different plausible target modes.

The full StoryReasoning architecture later decodes such latent samples back to pixels. Here we isolate the generative mechanism by working in frozen visual representation space.

Now ask Gemini:

> Using our deterministic baseline, prior mean, posterior/prior gap, shuffled-context control, sample diversity and best-of-K curve, discuss what evidence we have that the conditional VAE learned a useful conditional distribution rather than merely adding random noise. If best-of-K did not beat the deterministic baseline on our subset, explain what that negative result could mean instead of forcing a success story.

### Final discussion questions

1. Why is the posterior allowed privileged target information during training?
2. What prevents that privileged information from becoming useless target leakage at test time?
3. Why are condition shuffling and diversity both necessary diagnostics?
4. In what sense can sampling beat a deterministic ceiling even if the average sample is not better?
