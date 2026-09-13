# Experiment 5 — Does the metric agree with what you see?

**Dataset:** A manageable StoryReasoning subset with four context frames and a fifth target frame, evaluated using simple image candidates and a frozen CLIP image encoder.

**Key concepts:** metric validity, floors, pixel L1, semantic similarity, centred embeddings, Fréchet distance, sharpness, objective mismatch, loss as specification.

**Expected computational budget:** Moderate. No prediction model is trained; frozen CLIP embeddings are extracted once and reused.

**Recommended runtime:** **GPU** for CLIP embedding extraction.

**Estimated student time:** **30–35 minutes**, including roughly **3–7 minutes** for loading and one-off embedding extraction depending on Colab.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Load a reproducible, memory-conscious StoryReasoning subset and create about 250–400 consecutive five-frame windows, split or sampled by STORY. Resize only as needed for display/CLIP but keep original pixels for pixel metrics. For every window define these candidates for target frame 5: (A) COPY-LAST = context frame 4; (B) CONTEXT-MEAN = pixelwise mean of the four context frames; and (C) one GLOBAL-MEDIAN image computed from a separate pool of context/training frames, reused for every target. Also create a DIAGNOSTIC-ONLY blurred version of the TRUE target with a visible Gaussian blur; label it clearly as an oracle diagnostic, not a predictor. Display matched grids for several windows. Do not train a model.

### Questions

1. Which candidates look like real frames?
2. Which candidates preserve the target's exact pixels most closely?
3. Why is the blurred target useful for testing metrics even though it is not a valid prediction method?
4. Why must the global median be computed without peeking at each target?

---

## Prompt 2

> Compute mean PIXEL L1 from every candidate to its target. Then load a standard frozen CLIP image encoder, encode every unique candidate/target image ONCE and cache the embeddings. Compute target-aligned CLIP cosine similarity after centring embeddings by the mean TARGET embedding and L2-normalising. Report mean pixel L1 and mean centred CLIP similarity for each candidate. Also report how often COPY-LAST is ranked better than GLOBAL-MEDIAN by each metric. Do not fine-tune CLIP.

### Questions

1. Does pixel L1 prefer the median/average candidate more often than your visual judgement does?
2. Does CLIP similarity distinguish a real but different story frame from the global blob more strongly?
3. What information is each metric sensitive to?
4. Why does using CLIP as a metric not make it an infallible human-perception score?

---

## Prompt 3

> Add two complementary SET/IMAGE diagnostics without retraining anything. First compute a CLIP-feature Fréchet distance between the SET of each candidate type and the SET of targets, using the cached CLIP embeddings, covariance regularisation if needed, and a numerically stable matrix square root. Explain that this measures distribution-level realism and NOT which candidate belongs to which target. Second compute image sharpness as variance of the Laplacian and report each candidate's mean sharpness divided by target sharpness. Summarise pixel L1, centred CLIP similarity, CLIP Fréchet and sharpness ratio in one table. Include the true target row as a sanity check where appropriate.

### Questions

1. Can a candidate set have good Fréchet distance while individual candidates are paired with the wrong targets?
2. Which metric notices blur most directly?
3. Which metric measures semantic alignment to a particular target?
4. Why should no single column be called “image quality” without qualification?

---

## Prompt 4

> Inspect several windows where PIXEL L1 and centred CLIP similarity disagree most strongly about COPY-LAST versus GLOBAL-MEDIAN. Show the context frames, target and both candidates with their scores. Then analyse this recorded full-system StoryReasoning result from the architecture narrative: before adding a semantic image loss, the scaled model's target CLIP similarity was about `0.056`; after adding a differentiable centred-CLIP cosine term through a FROZEN CLIP encoder, it reached about `0.17` within two epochs while pixel L1 was essentially unchanged. Do NOT train the full architecture. Explain what this result supports and what it does not prove.

### Questions

1. When the two metrics disagree, which candidate usually looks more like a plausible frame?
2. What did the semantic loss change according to the recorded result?
3. Why is unchanged pixel L1 compatible with a large improvement in semantic similarity?
4. Does a better CLIP score prove that every visual property improved?

---

## Try it yourself manually

Without asking Gemini to rewrite the analysis, return to the DIAGNOSTIC blurred-target code from Prompt 1 and change only the Gaussian blur strength, trying several values such as sigma `1`, `3`, `6`, and `10`. Recompute the existing metrics; do not re-encode unchanged candidates.

Before each run, predict which metrics will react most strongly.

- How quickly does sharpness fall?
- Does pixel L1 change monotonically with blur?
- How tolerant is CLIP similarity to losing fine detail?
- What does this tell you about the aspects of image quality each metric ignores?

---

## Reveal: what was this experiment really about?

A metric is part of the scientific claim, not just a reporting convenience.

If two outputs are visibly and semantically different but a metric ranks them in the opposite order to the property we care about, then optimising that metric can drive the model toward the wrong behaviour. Pixel L1 is useful when exact aligned pixels matter; it is a poor measure of plausibility after a camera cut. CLIP similarity captures more semantic structure, Fréchet compares sets rather than aligned pairs, and Laplacian variance says something narrow about sharpness.

The course began with **loss as specification**. It ends at the same idea at system scale: before turning an evaluation signal into a training objective, test whether it distinguishes the floors and failures you already understand.

Now ask Gemini:

> Using our StoryReasoning candidate grids, pixel L1, centred CLIP similarity, CLIP Fréchet, sharpness ratios, disagreement examples and the recorded before/after semantic-loss result, explain how to validate an evaluation metric before optimising it. Distinguish per-example alignment, distribution realism and sharpness, and connect the conclusion back to loss as specification.

### Final discussion questions

1. Why can a real related frame be a worse pixel-L1 prediction than a blob?
2. What does CLIP similarity measure that pixel L1 largely misses here?
3. Why are Fréchet distance and target-aligned similarity answering different questions?
4. If this were your assessment system, what evidence would you require before adding a new loss term?
