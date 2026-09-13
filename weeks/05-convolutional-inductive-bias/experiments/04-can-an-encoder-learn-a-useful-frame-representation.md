# Experiment 4 — Can an encoder learn a useful representation of a movie frame?

**Dataset:** A manageable subset of StoryReasoning frames, cached at 60x125 and split by story.

**Key concepts:** convolutional encoder, decoder, autoencoder, bottleneck, latent representation, reconstruction, pretraining, representation spread.

**Expected computational budget:** Moderate. Dataset access happens once and one small autoencoder is trained once. All later investigations reuse the saved model and latent vectors.

**Recommended runtime:** **GPU** if available.

**Estimated student time:** **40–50 minutes total**: roughly **30–35 minutes active work** plus **5–12 minutes** of data loading/training depending on Colab and network speed.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a reproducible, manageable subset of the public `daniel3303/StoryReasoning` dataset. Cache roughly 2000–4000 frames at 60x125 RGB, scaled to 0–1, while preserving `story_id` and frame order metadata. Split by STORY, not by individual frame, into training and validation sets so frames from the same story never occur in both. Use a memory-conscious loading method and do not repeatedly download or resize later. Show several frames from each split and report the number of stories and frames. Also compute one constant pixel-wise median training image and its L1 reconstruction error on validation frames.

### Questions

1. Why must the split be by story rather than by frame?
2. What does the constant median image provide before we train anything?
3. Why cache resized frames now?
4. Is reconstructing a frame the same problem as predicting a future frame?

---

## Prompt 2

> Build a modest convolutional autoencoder for the cached 60x125 RGB frames. The ENCODER should use three or four strided `Conv2d` blocks with increasing channels, then flatten/project to a latent vector of about 128 dimensions with LayerNorm. The DECODER may mirror this with a linear projection plus `ConvTranspose2d` blocks and may resize only the final output if needed to return exactly 60x125 with sigmoid output. Keep the architecture simple. Before training, pass one batch through it and print a compact table of tensor shapes after each encoder stage, the latent, and the reconstruction. Also print the parameter count. Briefly explain the encoder input/output, the bottleneck, and why the decoder is needed for this experiment.

### Questions

1. At which stages is spatial resolution reduced?
2. What information must eventually be represented by the latent vector if reconstruction is to work?
3. Why is the latent much smaller than the raw image?
4. Which part of this system do we expect later models to reuse?

---

## Prompt 3

> Train the autoencoder ONCE on the cached training frames using pixel L1 loss. Use a fixed seed, a sensible batch size, Adam/AdamW, and at most about 12 epochs; stop earlier if validation reconstruction clearly stops improving. Record train and validation L1 after every epoch, save the best validation checkpoint, and at every epoch save enough information to plot the trajectory without retraining. After training, restore the best checkpoint. Cache latent vectors for all validation frames together with their story/frame metadata. Also save per-latent-dimension standard deviation and the overall latent spread. Do not run any additional training in later prompts.

### Questions

1. Does validation reconstruction beat the constant median-image floor?
2. Does train loss continue improving after validation loss stops improving?
3. Are most latent dimensions varying across validation images, or are many nearly constant?
4. Why is reconstruction error useful as a diagnostic of the encoder representation?

---

## Prompt 4

> Reuse the best saved autoencoder. Plot the train/validation reconstruction curves and display 8 validation originals beside their reconstructions, including some of the best and worst reconstruction errors. Print the median-image floor next to the model's validation L1. Also show a histogram of per-image reconstruction errors. Do not retrain.

### Questions

1. Which visual details are reconstructed well and which are lost?
2. Does a low average reconstruction error imply that every frame reconstructs equally well?
3. How does the model compare with the constant floor visually as well as numerically?
4. What would it mean if the decoder produced nearly the same image for every input?

---

## Prompt 5

> Choose two clearly different validation frames, encode them to latent vectors `z_a` and `z_b`, and decode 7 evenly spaced linear interpolations between them. Display the decoded sequence from A to B. Under it, show the two endpoint reconstructions and report the latent distance between A and B. Do not train or optimise during interpolation. Keep the interpretation descriptive.

### Questions

1. Do intermediate latent points decode to abrupt jumps or gradual visual changes?
2. Are all intermediate images equally realistic?
3. What does this suggest about treating the latent vector as a representation space rather than only compressed storage?
4. Why should we still be cautious about assuming geometric distance automatically means semantic similarity?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 5 in this experiment**. Before decoding one validation frame, set a chosen fraction of its latent coordinates to zero—for example 10%, then 25%, then 50%—and decode each altered vector.

Before each run, predict how much the reconstruction will change.

- Does damage grow smoothly with the fraction removed?
- Are some visual properties more robust than others?
- Does the experiment suggest that information is distributed across multiple latent dimensions?

Do **not** retrain the autoencoder.

---

## Reveal: what was this experiment really about?

This was the first genuine visual representation-learning component of the StoryReasoning system.

A convolutional encoder exploits local structure and weight sharing to turn a large image into a compact **latent representation**. Reconstruction gives us a concrete test: if the latent does not preserve enough information about the input, the decoder cannot recover the frame. The autoencoder therefore provides both a learned representation and a measurable reconstruction ceiling for later systems that operate through that representation.

The important architectural separation is now visible:

`image -> encoder -> latent representation -> decoder -> reconstructed image`

Later components can reuse the encoder's latent without needing to reason directly over every pixel.

Now ask Gemini:

> Using our validation reconstruction L1, median-image floor, reconstruction examples, latent spread and interpolation, discuss what evidence we have that the convolutional encoder learned an input-dependent visual representation. Distinguish reconstruction quality from semantic usefulness, and explain why this encoder can be pretrained before a later story-prediction system exists.

### Final discussion questions

1. Why is reconstruction a useful pretraining task for an image encoder?
2. What evidence would suggest representation collapse even if the code runs successfully?
3. Why does a good autoencoder not by itself solve next-frame prediction?
4. What new operation can we perform now that images have become vectors?
