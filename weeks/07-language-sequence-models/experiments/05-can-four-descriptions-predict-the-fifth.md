# Experiment 5 — Can four descriptions predict the fifth?

**Dataset:** Consecutive per-frame descriptions from StoryReasoning, represented by frozen MiniLM sentence embeddings.

**Key concepts:** frozen text encoder, sentence embedding, sequence model, GRU, hidden-state summary, next-step prediction, retrieval, baselines, shuffled-context control, order sensitivity.

**Expected computational budget:** Light to moderate. Description embeddings are computed once and one small GRU is trained once.

**Recommended runtime:** **GPU** if available for MiniLM embedding extraction; GRU training itself is small.

**Estimated student time:** **30–35 minutes**, including roughly **3–6 minutes** for embedding extraction/training depending on Colab.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Reuse the cached StoryReasoning per-frame descriptions and story metadata from Experiment 3. If necessary, load only the same modest subset rather than the full dataset. Form consecutive 5-description windows inside each story: descriptions 1–4 are the context and description 5 is the target. Split windows by STORY. Load a frozen `sentence-transformers/all-MiniLM-L6-v2` encoder and encode every unique description ONCE into a cached sentence embedding. Report the number of train/validation windows and embedding dimension. Show several 5-description windows. Do not train MiniLM.

### Questions

1. What has MiniLM contributed before the GRU learns anything?
2. Why are the sentence embeddings frozen?
3. What information is lost when an entire description becomes one vector?
4. Why must windows from one story remain in only one split?

---

## Prompt 2

> Before building a recurrent model, create two simple baselines for predicting the target description embedding: (A) copy the embedding of context description 4 and (B) use the mean embedding of context descriptions 1–4. Evaluate both by retrieval. For each validation window, create a fixed candidate set containing the true target plus 19 target descriptions from other validation stories. Rank candidates by cosine similarity to the predicted embedding and report top-1, top-5 and mean rank for both baselines. Cache the candidate sets so later models use exactly the same retrieval problem.

### Questions

1. Which baseline is stronger?
2. What does copy-last assume about the sequence?
3. What information does the mean baseline discard?
4. Why is retrieval more interpretable here than asking whether one predicted embedding has a small numerical error?

---

## Prompt 3

> Build a small GRU sequence predictor. Input the four frozen MiniLM embeddings in order, use the FINAL GRU hidden state as a summary, and project it to the MiniLM embedding dimension. Train ONCE on training windows to maximise cosine similarity to the true fifth-description embedding (or equivalently minimise `1 - cosine_similarity`). Record train/validation loss, save the best validation checkpoint, and cache the predicted validation embeddings. Evaluate the saved model on the SAME fixed retrieval candidate sets from Prompt 2. Report top-1, top-5 and mean rank beside copy-last and mean baselines. Briefly explain the GRU input, recurrent state and prediction.

### Questions

1. Does the GRU beat either simple baseline?
2. What does the final hidden state have to represent?
3. If the GRU improves retrieval, does that prove it uses all four context descriptions?
4. Why do we still need behavioural controls?

---

## Prompt 4

> Test what the saved GRU actually uses WITHOUT retraining. Evaluate retrieval under four conditions: (1) normal ordered context; (2) reverse the order of the same four descriptions; (3) randomly permute the four descriptions within each window using a fixed seed; and (4) replace the entire four-description context with a context from another validation window while keeping the original target/candidate set. Report top-1/top-5 and mean rank for each. Also report the average cosine change in the GRU prediction relative to the normal condition.

### Questions

1. What happens when content comes from the wrong story window?
2. How much does changing order hurt compared with replacing the content entirely?
3. If order permutation barely hurts but shuffled context does, what has the model learned to depend on?
4. What would strong order sensitivity tell you about the recurrent state?

---

## Prompt 5

> Reuse the normal validation predictions. Display several successful and failed retrieval examples: the four input descriptions, the true fifth description, the GRU's top 5 retrieved candidates, and the copy-last top 5 candidates. Choose examples where the GRU clearly helps and examples where it fails. Do not retrain. End by printing the four input-to-hidden sequence steps for one example only as tensor norms or compact summaries, not the full vectors.

### Questions

1. What kinds of continuity make the next description easy?
2. When the GRU fails, are its retrieved descriptions still stylistically or semantically plausible?
3. Does compressing all four descriptions into one final state appear sufficient for every example?
4. What information might be difficult to preserve in one fixed-size summary as sequences become longer?

---

## Try it yourself manually

Without asking Gemini to rewrite the model, return to the **evaluation code from Prompt 4** and add a variable such as:

```python
position_to_blank = 0
```

Replace just that one context-description embedding with a zero vector and evaluate retrieval. Repeat manually for positions `0`, `1`, `2`, and `3`, one at a time.

Before each run, predict which position will matter most.

- Is the last description always the most influential?
- Does the model use several positions or rely heavily on one?
- How does this intervention complement the order-shuffling test?

Do **not** retrain the GRU.

---

## Reveal: what was this experiment really about?

This is the first StoryReasoning model that explicitly **combines information across a sequence**.

MiniLM turns each individual description into a fixed vector. The GRU then updates a hidden state four times and uses the final state to predict a representation of what description should come next. Retrieval lets us ask whether that predicted representation points toward the actual continuation better than simple copy-last or averaging rules.

But a GRU final state is also a bottleneck: all useful information from four positions must be compressed into one vector. The order/content controls tell us whether the model actually uses the sequence, and the position ablations reveal which parts of the context matter.

That limitation motivates a later question: instead of forcing all earlier information into one summary, could a prediction retrieve different earlier elements when they become relevant? That is where attention will enter later.

Now ask Gemini:

> Using our copy-last/mean baselines, GRU retrieval scores, shuffled-context test, order perturbations and position ablations, discuss what evidence shows that the model uses sequential context. Distinguish using the content of a window from using its order, and explain why one final recurrent state becomes an information bottleneck.

### Final discussion questions

1. What did the GRU add beyond frozen sentence embeddings?
2. Which control best demonstrates dependence on the four-description context?
3. Is order sensitivity guaranteed merely because the architecture is recurrent?
4. Why might attention become attractive when the context becomes longer or when different predictions need different parts of the history?
