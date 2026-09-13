# Experiment 4 — Can a decoder ignore its condition?

**Dataset:** A controlled synthetic conditional-generation task where each condition selects one of several token patterns, but teacher-forced previous tokens make most of the sequence easy to predict without consulting the condition.

**Key concepts:** conditional generation, teacher forcing, condition ignoring, shuffled-condition test, token dropout, free-running generation, information bottleneck.

**Expected computational budget:** Light. Two tiny conditional LSTM decoders are trained once for comparison.

**Recommended runtime:** **CPU.**

**Estimated student time:** **20–25 minutes**, with about **1–2 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create a simple conditional sequence dataset with three discrete conditions, for example `A`, `B`, `C`. Each condition should correspond to its own short token chain of about 6–8 tokens. Design the chains so that once the first condition-specific token is known, the remaining next tokens are highly predictable from the previous true token. Show several `(condition, target sequence)` pairs and explain why teacher forcing can reveal the correct chain to the decoder even if it pays little attention to the condition after the first step.

### Questions

1. Which information should the condition provide?
2. During teacher forcing, what extra information does the decoder receive at each step?
3. Why could the previous true token become an easier signal than the condition?

---

## Prompt 2

> Build a small conditional LSTM decoder. Embed the previous token, concatenate a learned embedding of the condition at every time step, and predict the next token. Train one BASELINE model with ordinary teacher forcing and cross-entropy. Save it. Evaluate validation cross-entropy twice: once with the TRUE condition and once after randomly SHUFFLING conditions across examples while leaving target tokens unchanged. Also generate sequences freely from `<bos>` for each condition. Report the true-condition loss, shuffled-condition loss, their difference, and how often free generations match the requested condition.

### Questions

1. How much worse is validation loss when the condition is shuffled?
2. Does a small loss difference imply that the decoder uses the condition strongly?
3. Are free-running generations equally condition-specific as teacher-forced loss might suggest?
4. Why is the shuffled-condition test more informative than only checking ordinary validation loss?

---

## Prompt 3

> Train a SECOND model with the same architecture and data, but during teacher forcing replace the previous ground-truth token with a `<mask>` token at random on about 30% of steps. Keep the condition available. Call this TOKEN-DROPOUT model. Save it. Compare baseline versus token-dropout models on: true-condition cross-entropy, shuffled-condition cross-entropy, condition gap (shuffled minus true), and free-running condition-consistency. Do not tune many hyperparameters.

### Questions

1. Which model shows the larger true-versus-shuffled condition gap?
2. Does token dropout make ordinary teacher-forced loss slightly harder?
3. Does stronger dependence on the condition improve free-running condition consistency?
4. Why can making one input less reliable encourage the model to use another input?

---

## Prompt 4

> For both saved models, pick one validation target and show step-by-step next-token probabilities under three cases: correct condition, wrong condition, and correct condition but with the previous token masked. Display only the top few candidate tokens at each step. Keep both models frozen. Briefly describe when the condition appears to influence the distribution most strongly.

### Questions

1. Under ordinary teacher forcing, at which positions does changing the condition matter most?
2. What changes when the previous token is unavailable?
3. Does the token-dropout model react more strongly to the condition?
4. What evidence would justify saying a conditional decoder really uses its condition?

---

## Try it yourself manually

Without asking Gemini to rewrite the models, return to the **training code for the token-dropout model from Prompt 3** and change only the token-dropout probability, for example from `0.30` to `0.10` and then `0.50`. Retrain only this tiny controlled model for each setting.

Before each run, predict the trade-off.

- Does too little dropout leave the condition easy to ignore?
- Does too much dropout make next-token prediction unnecessarily difficult?
- Which setting gives the clearest condition gap without destroying ordinary performance?

---

## Reveal: what was this experiment really about?

A model can be labelled “conditional” in code while learning to rely mostly on another easier signal.

Teacher forcing supplies the correct previous token during training. If that token already reveals the sequence pattern, a decoder can achieve low cross-entropy while using the explicit condition only weakly. The **shuffled-condition test** asks the direct behavioural question: if we break the condition while leaving everything else intact, does performance change?

Token dropout makes teacher-forced history less reliable, increasing the incentive to use the condition. It is not magic; it changes the information available during training.

Now ask Gemini:

> Using our baseline and token-dropout losses, shuffled-condition gaps, free-running generations and step-by-step probabilities, explain condition ignoring. Distinguish “the condition is connected to the model” from “the model's predictions depend on the condition,” and explain why teacher forcing can hide this failure.

### Final discussion questions

1. Why can low teacher-forced loss coexist with weak conditioning?
2. What does the shuffled-condition gap measure?
3. Why is free-running generation an important second check?
4. How does this controlled failure relate to a real StoryReasoning text decoder conditioned on a story representation?
