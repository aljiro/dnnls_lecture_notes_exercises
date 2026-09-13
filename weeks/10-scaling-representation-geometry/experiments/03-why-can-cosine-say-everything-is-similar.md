# Experiment 3 — Why can cosine say everything is similar?

**Dataset:** Synthetic high-dimensional embeddings with known cluster structure and a controllable shared mean direction.

**Key concepts:** representation geometry, cosine similarity, anisotropy, common direction, centring, collapse, retrieval margin.

**Expected computational budget:** Very light. No neural network training is required.

**Recommended runtime:** **CPU.**

**Estimated student time:** **15–20 minutes**, with effectively no compute wait.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Create a reproducible synthetic embedding dataset in about 32 dimensions with 6 known clusters. Give each cluster a different random unit-vector centre and sample noisy points around it. L2-normalise the embeddings. Plot a 2-D PCA projection, then report mean cosine similarity for SAME-cluster pairs versus DIFFERENT-cluster pairs and nearest-neighbour cluster accuracy. Keep the true cluster labels only for evaluation.

### Questions

1. Do same-cluster pairs have higher cosine similarity?
2. Is the cluster structure visible in PCA and nearest-neighbour retrieval?
3. What geometric information is cosine using after L2 normalisation?

---

## Prompt 2

> Starting from the SAME embeddings, add one large COMMON direction to every vector before normalising again. Use a variable such as `common_strength = 8.0`. Compare the raw cosine distributions before and after adding this shared component. Report same-cluster cosine, different-cluster cosine, their difference as a retrieval margin, and nearest-neighbour cluster accuracy. Plot histograms of same/different pair cosines.

### Questions

1. What happens to the average cosine between unrelated embeddings?
2. Does a high raw cosine now necessarily mean two points belong to the same cluster?
3. Can useful distinctions survive even when most vectors point partly in the same direction?
4. Why is this different from every embedding becoming exactly identical?

---

## Prompt 3

> Centre the anisotropic embeddings by subtracting their dataset mean vector, then L2-normalise them again. Recompute the same/different cosine distributions, retrieval margin and nearest-neighbour accuracy. Show the mean-vector norm before centring and verify that the centred mean is approximately zero. Compare RAW versus CENTRED results in one compact table.

### Questions

1. What common structure does centring remove?
2. Does centring restore separation between same-cluster and different-cluster similarities?
3. Why can centred cosine reveal distinctions hidden by a dominant mean direction?
4. Would centring be guaranteed to improve every representation-learning problem?

---

## Prompt 4

> Create a second failure mode from the original clustered embeddings: progressively shrink each point's cluster-specific component toward zero so that the embeddings genuinely COLLAPSE toward one shared vector. Compare three cases—healthy clusters, anisotropic/common-direction embeddings, and collapsed embeddings—using mean pairwise cosine, average per-dimension standard deviation, retrieval margin and nearest-neighbour cluster accuracy. Do not use only cosine to diagnose collapse.

### Questions

1. Which statistics distinguish anisotropy from genuine collapse?
2. Can anisotropic embeddings still contain useful information?
3. What disappears when the representation truly collapses?
4. Why should a representation diagnostic inspect both similarity and spread/task structure?

---

## Try it yourself manually

Without asking Gemini to rewrite the analysis, return to the code from Prompt 2 and change only `common_strength`, trying values such as `0`, `2`, `8`, and `20`.

Before each run, predict the raw cosine distribution and retrieval margin.

- At what point do unrelated embeddings all begin to look deceptively similar?
- Does nearest-neighbour accuracy fail at the same rate as the raw cosine margin?
- Why is the strength of a common direction a geometric property rather than a new class label?

---

## Reveal: what was this experiment really about?

A representation can be poorly arranged for a particular similarity measure without containing no information.

**Anisotropy** means embeddings occupy some directions much more strongly than others. A large common component can make raw cosine similarity high for almost every pair, compressing the numerical distinction between related and unrelated examples. **Centring** removes one such common direction and can expose the relative geometry underneath.

That is different from **collapse**, where meaningful variation itself disappears. This distinction matters whenever we interpret an embedding loss or similarity score: a bad score can reflect the geometry of the representation, not necessarily the absence of useful information.

Now ask Gemini:

> Using our healthy, anisotropic, centred and collapsed embeddings, explain the difference between a common mean direction and representation collapse. Discuss why raw cosine alone can be misleading and why centring, spread statistics and retrieval behaviour provide complementary evidence.

### Final discussion questions

1. Why can two unrelated vectors have high cosine similarity in an anisotropic space?
2. What does centring change and what does it leave untouched?
3. Why is collapse a stronger failure than anisotropy?
4. How does this connect to using frozen target embeddings or cosine losses in larger systems?
