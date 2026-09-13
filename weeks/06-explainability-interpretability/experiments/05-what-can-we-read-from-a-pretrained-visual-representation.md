# Experiment 5 — What can we read from a pretrained visual representation?

**Dataset:** A modest StoryReasoning frame subset with per-frame character annotations, encoded by frozen ResNet-18 feature extractors.

**Key concepts:** pretrained encoder, transfer learning, frozen representation, linear probe, annotation-derived target, shuffled-label control, decodability, representation reuse.

**Expected computational budget:** Light to moderate. Frames are loaded once and two frozen encoders are run once; only tiny linear probes are trained afterward.

**Recommended runtime:** **GPU** if available for feature extraction; probe training is CPU-fast.

**Estimated student time:** **25–30 minutes**, including roughly **2–5 minutes** of StoryReasoning loading/feature extraction depending on Colab and network speed.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a reproducible, memory-conscious subset of the public `daniel3303/StoryReasoning` dataset, aiming for roughly 500–800 frames from enough stories to make a story-level split. Use the StoryReasoning parser utilities to obtain the character list for each frame. For every frame create two binary annotation-derived labels: `has_character` = at least one annotated character, and `multiple_characters` = at least two. Split TRAIN/TEST by `story_id`, never by individual frame. Report class prevalence for both labels in each split and choose as `probe_target` whichever label is closer to balanced in the TRAIN split. Cache frame metadata/labels and show a few positive and negative examples. Do not train a visual model.

### Questions

1. Why do we split by story instead of randomly splitting frames?
2. Which target is more balanced in your subset?
3. Are these labels produced by the visual encoder or by StoryReasoning annotations?
4. What would a majority-class baseline achieve?

---

## Prompt 2

> Create TWO ResNet-18 feature extractors with the classification layer removed: (A) torchvision ImageNet-pretrained weights and (B) the same architecture with random weights. Freeze both completely. Apply the correct pretrained image normalisation to the pretrained model and use the same resized frame content for both. Extract and cache one 512-dimensional embedding per frame ONCE. Train the same simple linear/logistic probe on TRAIN embeddings for `probe_target` and evaluate on held-out TEST stories. Report accuracy, balanced accuracy and F1 for: majority baseline, random-encoder probe and pretrained-encoder probe. Also run a shuffled-training-label control for the pretrained embeddings. Do not fine-tune either encoder. Briefly explain what is learned and what is frozen.

### Questions

1. Does the pretrained representation support a better linear probe than random frozen features?
2. Why is the random-weight encoder a useful comparison?
3. What does the shuffled-label result rule out?
4. If the pretrained probe performs well, what exactly has been demonstrated?

---

## Prompt 3

> Reuse the frozen PRETRAINED embeddings and trained probe. For several correctly classified and misclassified TEST frames, show the image, true label, probe probability and the 5 nearest TRAIN frames in cosine distance. Report how often each test frame's nearest neighbour shares its label, and compare that with chance based on train prevalence. Do not retrain or change the embedding.

### Questions

1. Do visually/semantically similar frames tend to lie near one another in the pretrained representation?
2. Are nearest neighbours always matched on the probe label?
3. What kinds of false positives or false negatives do you see?
4. Why is nearest-neighbour inspection evidence about representation geometry but not proof of the mechanism used inside ResNet?

---

## Prompt 4

> Inspect the trained linear probe itself. Rank embedding dimensions by absolute probe weight. On TEST embeddings, zero the top 5% highest-weight dimensions and measure the change in balanced accuracy/F1; compare with zeroing the same number of randomly chosen dimensions over several fixed random draws. Then repeat with the RANDOM-encoder probe using the same procedure. Do not modify either encoder. Briefly state what this ablation tests and what it cannot tell us about individual ResNet neurons before the final pooled embedding.

### Questions

1. Does removing top probe-weight dimensions hurt more than removing random dimensions?
2. Is the information concentrated in a few embedding coordinates or distributed?
3. Are these dimensions “character detectors” in the full network? Why is that claim too strong?
4. What component's behaviour are we directly testing here: the frozen encoder or the linear probe built on top of its representation?

---

## Try it yourself manually

Without asking Gemini to rewrite the feature-extraction code, reuse the **cached pretrained and random embeddings** but switch the probe target to the other annotation label (`has_character` ↔ `multiple_characters`). Retrain only the tiny probes and recompute the same metrics.

Before running, predict which task will be easier.

- Does the same frozen representation support both tasks?
- Does the gap between pretrained and random features change?
- Why is reusing one representation for a new head an example of transfer learning?

Do **not** rerun either ResNet over the images.

---

## Reveal: what was this experiment really about?

This experiment combined **transfer learning** with **probing**.

The pretrained encoder was learned for a different task and dataset, yet its frozen representation can contain information useful for a new StoryReasoning annotation task. A linear probe tests whether that information is **easily decodable** without changing the encoder.

But the wording matters. Strong probe performance does not prove that ImageNet pretraining explicitly created “character neurons,” nor that some future StoryReasoning predictor would actually use the same information. It shows that a simple readout can recover the chosen annotation from the frozen representation.

That distinction—between information being available and a downstream model using it—is exactly why probes need controls and interventions.

Now ask Gemini:

> Using our majority baseline, random-versus-pretrained probe results, shuffled-label control, nearest-neighbour examples and embedding-dimension ablations, discuss what we can safely claim about the frozen visual representation. Distinguish transferability, decodability and causal use, and explain why a good probe is evidence about representation content rather than a complete explanation of the encoder.

### Final discussion questions

1. What does pretraining appear to contribute compared with random features?
2. Why does a linear probe provide a deliberately restricted test of representation content?
3. Which control was most important for preventing an overclaim?
4. How might a later StoryReasoning predictor test whether it actually uses character-related visual information rather than merely having access to it?
