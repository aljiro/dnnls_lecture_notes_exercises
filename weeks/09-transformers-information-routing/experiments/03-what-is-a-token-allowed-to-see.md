# Experiment 3 — What is a token allowed to see?

**Dataset:** A tiny synthetic token corpus with repeated local and long-range patterns.

**Key concepts:** causal mask, bidirectional context, next-token prediction, masked-token prediction, self-supervision, encoder-style versus decoder-style information access.

**Expected computational budget:** Light. Two tiny Transformer models are trained once on the same compact corpus.

**Recommended runtime:** **CPU or GPU.**

**Estimated student time:** **20–25 minutes**, including roughly **1–3 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create a reproducible synthetic token corpus from a small vocabulary, with sequences about 12 tokens long. Include patterns where future tokens would make an earlier prediction trivially easy, plus patterns where both left and right context help identify a missing middle token. Show several sequences. Then display a standard causal attention mask for one sequence length as a labelled matrix and explain which token positions each row is allowed to attend to. Do not train a model yet.

### Questions

1. Why would unrestricted access to future tokens be invalid for next-token prediction?
2. Which cells of the causal mask are blocked?
3. Why might right-side context be useful for reconstructing a missing middle token?

---

## Prompt 2

> Build a tiny decoder-style Transformer for NEXT-TOKEN prediction using token embeddings, learned positional embeddings, one small Transformer block and vocabulary logits. Apply the causal mask so position `t` cannot see tokens after `t`. Train once on the synthetic corpus and save the model. Report validation cross-entropy/perplexity. For one validation sequence, show the top predicted next tokens at several positions and display one attention-weight matrix if practical.

### Questions

1. What information is available when predicting the token after position `t`?
2. Why is a causal mask part of the learning problem rather than just a plotting choice?
3. What would a suspiciously excellent result suggest if the mask were accidentally removed?

---

## Prompt 3

> Build a second tiny encoder-style Transformer for MASKED-TOKEN prediction on the same corpus. Randomly replace about 15% of eligible tokens with a `<mask>` token and predict only the original masked tokens. Do NOT use a causal mask: allow bidirectional attention over the visible sequence. Train once and save the model. Report masked-token validation accuracy and show several masked examples with top predictions. Keep model size comparable to the next-token model.

### Questions

1. What is the target in masked-token training?
2. Why can this model use tokens on both sides of the mask?
3. Is masked-token accuracy directly comparable with next-token perplexity?
4. How can labels be created from the data itself in both objectives?

---

## Prompt 4

> Take one validation sequence and compare what information reaches a chosen position under: (A) the causal next-token mask and (B) unrestricted bidirectional attention. Print the allowed-position pattern and, for the saved models, the attention weights into that position if available. Then make a compact table comparing next-token prediction and masked-token prediction by target, visible context and typical model role. Do not retrain.

### Questions

1. Which objective permits a token representation to incorporate future context?
2. Which objective matches autoregressive generation at test time?
3. Why can the same Transformer-style block support different learning problems simply by changing objective and information access?

---

## Try it yourself manually

Without asking Gemini to rewrite the model, return to the **causal-mask construction/evaluation code from Prompt 2**. Manually allow one illegal future position through the mask for a controlled evaluation example, without retraining.

Before running, predict whether the chosen next-token probability can improve.

- Does seeing one future token change the prediction?
- Why would this constitute information leakage for autoregressive evaluation?
- Why must an apparently strong metric always be interpreted together with what information the model was allowed to see?

---

## Reveal: what was this experiment really about?

Transformer blocks do not define one single learning problem. **The objective and the attention mask define what information may participate in each prediction.**

Causal next-token prediction prevents each position from reading the future, matching autoregressive generation. Masked-token prediction deliberately hides selected tokens while allowing surrounding context to reconstruct them. Both are self-supervised because the training targets are created from the observed sequence itself rather than supplied as external class labels.

The mask is therefore part of the model's information structure, not merely an implementation detail.

Now ask Gemini:

> Using our causal-mask matrix, next-token results, masked-token results and controlled mask leak, explain how attention masks and self-supervised objectives determine what a Transformer can use. Contrast decoder-style causal prediction with encoder-style masked prediction without claiming that one is universally better.

### Final discussion questions

1. Why can future-token access invalidate autoregressive evaluation?
2. What makes next-token and masked-token training self-supervised?
3. Why can the same attention mechanism serve encoder-style and decoder-style models?
4. How does this connect to the broader question, “what information is available to the model?”
