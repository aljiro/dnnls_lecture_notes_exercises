# Experiment 5 — Can more inference-time compute find a better continuation?

**Dataset:** A manageable StoryReasoning retrieval benchmark where each candidate memory item contains a real frame and its description.

**Key concepts:** retrieval, external memory, two-stage search, reranking, test-time compute, verification, candidate budget, parametric versus non-parametric computation.

**Expected computational budget:** Moderate only for one-off frozen embedding extraction. No sequence model is trained.

**Recommended runtime:** **GPU** for CLIP/MiniLM embedding extraction; retrieval itself is light.

**Estimated student time:** **25–30 minutes**, including roughly **3–6 minutes** for loading and frozen embedding extraction depending on Colab.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Load a reproducible manageable subset of the public `daniel3303/StoryReasoning` dataset and form consecutive 5-frame windows, split by STORY. Aim for roughly 1000–2000 usable windows rather than the full dataset. For each validation query, create one FIXED candidate memory of 100 possible fifth-frame items: the true fifth frame plus 99 fifth frames from other validation stories, fixed seed. Each candidate item may contain its real frame AND its own stored description; make clear that this changes the task from generating a new frame to retrieving an existing item from an external memory. Cache frozen CLIP image embeddings for needed frames and frozen MiniLM embeddings for descriptions. Report counts and chance top-1/top-5 rates.

### Questions

1. How is this retrieval problem different from pixel generation?
2. Where do the candidate frames and their descriptions live?
3. What is chance top-1 with 100 candidates?
4. Why must every method use exactly the same candidate sets?

---

## Prompt 2

> Build three TRAINING-FREE retrieval scores using the cached embeddings. TEXT score: represent the four context descriptions by their mean MiniLM embedding and compare it with each candidate's stored description embedding. IMAGE score: for each candidate frame, compute its maximum CLIP image similarity to any of the four context frames. COMBINED score: z-normalise the two score types within each candidate set and average them equally. Rank all 100 candidates by each score and report top-1, top-5 and mean rank. Also include random ranking as a baseline. Do not train projection heads or a sequence model.

### Questions

1. Which signal is stronger on this subset?
2. Do text and image scores make identical errors?
3. Can combining two imperfect signals improve retrieval?
4. Why is this an inference procedure even though frozen neural encoders are involved?

---

## Prompt 3

> Turn the retrieval into a TWO-STAGE inference procedure. Stage 1 uses the TEXT score to retrieve only the top `M=20` candidates from the 100-item memory. Stage 2 spends extra computation only on those candidates and reranks them using the COMBINED text+image score. Report: Stage-1 recall@20 (whether the true item survives), final top-1/top-5, and an approximate count of candidate score evaluations for one-stage versus two-stage retrieval. Compare final accuracy with text-only ranking and full combined ranking over all 100 candidates. Do not retrain anything.

### Questions

1. What is the ceiling on final success if the correct item is removed at Stage 1?
2. Does reranking help once the correct candidate survives?
3. What computation is saved by scoring the expensive second signal on only `M` candidates?
4. Why is retrieval depth a systems trade-off rather than a model parameter?

---

## Prompt 4

> Inspect several success and failure cases from the two-stage system. For each, display the four context frames/descriptions, the true fifth item, the top 5 Stage-1 text candidates and the top 5 reranked candidates. Label failures as at least: `retrieval failure` if the true item was not in Stage-1 top M, or `reranking failure` if it survived but finished outside the final top 5. Then compare our small benchmark conceptually with this REFERENCE RESULT from the full StoryReasoning architecture narrative: a retrieval formulation using frozen CLIP features selected the true next frame from 2,974 candidates about 7% top-1 and 40% top-10. Compute the corresponding chance rates and state why those percentages are meaningful without claiming our simplified method should reproduce them.

### Questions

1. Which stage is responsible for each failure example?
2. Why is 7% top-1 among 2,974 candidates very different from 7% in a 100-way task?
3. What does retrieval gain by returning a real frame rather than decoding pixels?
4. What does retrieval give up compared with generation?

---

## Try it yourself manually

Without asking Gemini to rewrite the system, return to the **two-stage retrieval code generated by Prompt 3 in this experiment** and change only the Stage-1 candidate budget `M`. Try, for example, `5`, `10`, `20`, `50`, and `100`.

Before running, predict the trade-off.

- How does Stage-1 recall change with `M`?
- Does final top-1 improve monotonically?
- How many candidates receive the more expensive second-stage score?
- At what point are you effectively doing full search rather than selective reranking?

Do **not** train or fine-tune any model.

---

## Reveal: what was this experiment really about?

Inference need not be one forward pass. A system can **retrieve candidates, spend additional computation on a subset, verify or rerank them, and only then return an answer**.

Nothing in this experiment learned new weights. What changed with `M` was the amount and allocation of **test-time computation**. A small budget was cheap but could discard the correct item before reranking; a larger budget protected recall but spent more computation. The location of failure also became explicit: retrieval and reranking could fail independently.

This closes the optional week by separating several ways a deployed system can appear to “learn” or improve at inference time:

- in-context learning changes the information inside the forward-pass context;
- external memory changes what can be retrieved without changing model weights;
- test-time adaptation actually updates some parameters/state;
- search and reranking keep the model fixed but allocate more computation before answering.

Now ask Gemini:

> Using our quality-versus-M curve, Stage-1 recall, reranking results, failure examples and the 2,974-candidate reference result, explain test-time computation as a systems design choice. Distinguish retrieval, reranking/verification, in-context learning and test-time parameter adaptation, and identify what changes at inference in each case.

### Final discussion questions

1. Why can more inference-time compute help even when weights are frozen?
2. What determines whether search fails before verification can help?
3. When is retrieval preferable to generating a new output?
4. Looking across the whole module, where can information live: parameters, activations/context, external memory, or an inference-time search process?
