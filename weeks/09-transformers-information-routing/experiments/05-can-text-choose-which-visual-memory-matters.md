# Experiment 5 — Can text choose which visual memory matters?

**Dataset:** Consecutive 5-frame StoryReasoning windows with frozen visual and text embeddings, split by story.

**Key concepts:** cross-attention, multimodal fusion, content-dependent query, visual memory, retrieval prediction, shuffled-condition control, attention as routing.

**Expected computational budget:** Moderate. Reuse cached frozen embeddings; only small attention/projection heads are trained.

**Recommended runtime:** **GPU** is useful but not essential once embeddings are cached.

**Estimated student time:** **30–35 minutes**, including roughly **2–5 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Reuse the cached StoryReasoning frame and description embeddings from Experiment 4. Form consecutive 5-frame windows inside each story: frames/descriptions 1–4 are context and frame 5 is the target. Keep the same story-level split and use a manageable number of windows. For every window store four frozen ResNet frame embeddings, four frozen MiniLM description embeddings and the target-frame embedding. Build fixed retrieval candidate sets containing the true target plus 31 target frames from other validation stories. Report train/validation window counts and show several windows.

### Questions

1. Which representations are inherited rather than learned in this experiment?
2. Why is the target a visual embedding rather than pixels?
3. What makes this a sequence/context problem rather than ordinary paired image-text retrieval?

---

## Prompt 2

> Build a simple MULTIMODAL BASELINE with no attention. Mean-pool the four visual embeddings, mean-pool the four description embeddings, project both to a common small dimension, concatenate them, and use an MLP to predict the normalised target-frame embedding. Train once with cosine-distance loss or MSE on normalised embeddings. Save the best checkpoint and evaluate top-1/top-5/mean-rank retrieval on the fixed candidate sets. Also evaluate after shuffling the four-description context across validation windows while keeping the visual context and targets fixed.

### Questions

1. Does the baseline depend on text according to the shuffled-text control?
2. What information is discarded by mean pooling the four frames?
3. Can the baseline choose different visual positions for different text contexts?

---

## Prompt 3

> Build a second model where TEXT controls VISUAL routing. Create one content-dependent query from the four frozen description embeddings using a small learned projection of their mean or a compact GRU summary inherited from Week 7. Project the four frame embeddings into visual KEYS and VALUES. Apply one small single-query multi-head CROSS-ATTENTION layer so the text-derived query attends over the four visual memories. Combine the attended visual vector with the text query through a small prediction head to predict the target-frame embedding. Train once with the same retrieval-oriented target loss and save the best checkpoint. Briefly identify exactly where queries, keys and values come from.

### Questions

1. What can the cross-attention model do that mean pooling cannot?
2. Why is this cross-attention rather than self-attention?
3. Does the model still inherit most of its visual/language representation from frozen encoders?
4. Why is the text query content-dependent?

---

## Prompt 4

> Evaluate the saved cross-attention model on the SAME fixed candidate sets as the baseline. Report top-1/top-5/mean rank for: (A) normal context, (B) shuffled description context, and (C) descriptions replaced by zero vectors while visual frames stay unchanged. Compare with the mean-pooling baseline. For several validation examples, print the four cross-attention weights over frame positions beside short description snippets and indicate which input frame is visually closest to the true target. Do not retrain. State explicitly that attention weights are not automatically faithful explanations.

### Questions

1. Does cross-attention beat the pooled baseline on this subset?
2. How much does breaking or removing text hurt?
3. Do the largest attention weights always correspond to the visually closest input frame?
4. Why is a change under shuffled text stronger evidence of multimodal dependence than an interesting-looking attention map?

---

## Prompt 5

> Test whether routing varies with the content of the query. Select several validation windows and keep their four visual memories FIXED. For each, run the cross-attention model first with the correct four descriptions and then with descriptions borrowed from two other validation windows. Record the four attention weights, predicted target embedding and retrieval rank each time. Summarise how much attention distributions and predictions change. Do not retrain.

### Questions

1. Can the same visual memory produce different routing under different text queries?
2. If the attention weights change but retrieval does not, what might that mean?
3. If retrieval changes strongly under unrelated descriptions, what does that show about cross-modal dependence?
4. Why should we distinguish “routing changed” from “routing was useful”?

---

## Try it yourself manually

Without asking Gemini to rewrite the model, return to the **evaluation code generated by Prompt 4 in this experiment** and add a variable such as:

```python
text_position_to_blank = 0
```

Zero just ONE of the four description embeddings before forming the text query. Repeat manually for positions `0`, `1`, `2`, and `3`, without retraining.

Before each run, predict which position will matter most.

- Does blanking one description change the attention distribution?
- Is the last description always the most important?
- Does retrieval degrade for the same positions that most change attention?
- What does disagreement between those two effects tell you about interpreting attention weights?

---

## Reveal: what was this experiment really about?

This is the first experiment in the curriculum where the two modalities do more than merely coexist in a shared representation. **Text actively controls which visual information is routed forward.**

The four frame embeddings act as a visual memory. A query derived from the descriptions is compared with visual keys, producing weights over the four visual values. Because the query depends on the current text, the same set of visual memories can be combined differently for different linguistic contexts.

The shuffled-text and blanking controls matter because an attention map by itself does not prove that the routed information affects the prediction. Behavioural intervention is stronger evidence than visual inspection alone.

This is intentionally not the full StoryReasoning architecture. The encoders are inherited and frozen, and the only major new mechanism is multimodal information routing.

Now ask Gemini:

> Using our pooled baseline, cross-attention retrieval results, shuffled/zero-text controls, query-swap test and single-position blanking interventions, explain what evidence supports the claim that text is routing visual information. Distinguish multimodal alignment from multimodal fusion, and distinguish attention weights from causal evidence about what the prediction uses.

### Final discussion questions

1. What did cross-attention add beyond the aligned/frozen representations from Experiment 4?
2. Why is a content-dependent query central to information routing?
3. Which result best demonstrates that the visual prediction depends on text?
4. How does this mechanism address the fixed-summary bottleneck encountered with recurrent sequence models in Week 7?
