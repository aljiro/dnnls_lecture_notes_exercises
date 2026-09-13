# Experiment 2 — Can a large model use only the part it needs?

**Dataset:** A synthetic 2-D regression problem with four regions, each governed by a different simple function.

**Key concepts:** conditional computation, mixture of experts, router, gating, sparse activation, total capacity, active compute, expert specialisation.

**Expected computational budget:** Light. One dense MLP and one small mixture-of-experts model are trained once.

**Recommended runtime:** **CPU** is sufficient; GPU is optional.

**Estimated student time:** **20–25 minutes**, with roughly **1–3 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

> Create a reproducible 2-D regression dataset with inputs `(x1,x2)` in `[-1,1]^2`. Divide the plane into four quadrants and use a DIFFERENT simple target rule in each quadrant, for example one mostly linear in `x1`, one mostly linear in `x2`, one using `x1+x2`, and one using `x1-x2`, plus small noise. Split train/test and plot the target over the input plane. Do not train a model yet. Keep the regime boundaries visible.

### Questions

1. Is one global rule sufficient to describe all four regions simply?
2. What information in the input could a routing mechanism use?
3. Why might several specialised functions be useful even though all examples belong to one task?

---

## Prompt 2

> Train a compact DENSE MLP baseline on the regression task. Use enough hidden units to fit the problem reasonably but keep it small. Save the model and report train/test MSE and total parameter count. Plot the predicted surface beside the true surface. Briefly explain that every parameter path in this dense network is potentially active for every example.

### Questions

1. Where does the dense model make its largest errors?
2. How many parameters does it contain?
3. Does every example pass through the same learned computation?

---

## Prompt 3

> Build a toy MIXTURE-OF-EXPERTS model with four small MLP experts and a learned router. The router sees `(x1,x2)`, produces four scores, and during training keeps only the top `k=2` experts per example, renormalising their softmax weights before combining expert outputs. Keep the implementation explicit; do not import a distributed MoE library. Train once. Report train/test MSE, TOTAL parameter count, approximate ACTIVE expert parameters per example, and the fraction of examples routed to each expert. Plot the dominant expert across the input plane.

### Questions

1. Does the router divide the input space in a structured way?
2. Do experts correspond perfectly to the four quadrants, or only approximately?
3. How can the MoE have more total parameters than the dense model without activating all of them for each example?
4. What failure would occur if the router sent nearly everything to one expert?

---

## Prompt 4

> Evaluate the saved MoE without retraining under three routing conditions: (A) its learned router; (B) shuffle the router decisions across test examples while leaving expert networks unchanged; and (C) force every test example to use the same most-common expert. Report test MSE and expert-use frequencies. Also compare the dense baseline and learned-router MoE in one compact table including total parameters and active experts per example.

### Questions

1. Does shuffling routing hurt even though the experts themselves are unchanged?
2. What does forcing one expert reveal about specialisation?
3. Is a router merely a speed optimisation, or can it change which function is applied to an input?
4. Why should MoE comparisons distinguish total capacity from active computation?

---

## Try it yourself manually

Without asking Gemini to rewrite the model, return to the MoE evaluation code and change only the inference value of `top_k`, evaluating the SAME trained model with `top_k = 1`, `2`, and `4`.

Before running, predict the trade-off between test MSE and active computation.

- Does activating every expert always improve accuracy?
- How much active computation is saved by top-1 or top-2 routing?
- Why is “more parameters” not the same thing as “more parameters used for every token/example”?

Do **not** retrain the MoE for this intervention.

---

## Reveal: what was this experiment really about?

A mixture of experts separates **stored capacity** from **computation used on one example**.

The router makes computation conditional: different inputs can activate different subnetworks. That allows a model to contain many specialised parameters while paying for only a subset on each forward pass. But the routing decision itself becomes part of the learning problem. Poor routing, expert collapse or badly balanced use can waste that capacity.

This is an extension of an idea seen throughout the course: a gate or attention mechanism is not just another layer—it changes **which information or computation is allowed to matter for this example**.

Now ask Gemini:

> Using our dense baseline, routing map, active-parameter estimate and shuffled/forced-routing controls, explain sparse conditional computation. Distinguish total model capacity from active compute, and explain why the router must be evaluated as part of the model rather than assumed to work because experts exist.

### Final discussion questions

1. What does the router learn that an ordinary dense layer does not explicitly represent?
2. Why can expert imbalance be a problem?
3. How is top-k expert routing related to earlier attention/gating ideas?
4. In what sense can a model become larger without multiplying per-example compute by the same factor?
