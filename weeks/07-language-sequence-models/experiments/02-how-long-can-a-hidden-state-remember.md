# Experiment 2 — How long can a hidden state remember?

**Dataset:** Synthetic sequences in which the first symbol determines the final binary target while all later symbols are distractors.

**Key concepts:** recurrent neural network, hidden state, memory, parameter sharing through time, vanishing gradients, GRU, gating, sequence length.

**Expected computational budget:** Light. Two tiny recurrent models are trained once on the same synthetic data.

**Recommended runtime:** **CPU** is sufficient; GPU is optional.

**Estimated student time:** **25–30 minutes**, with roughly **1–3 minutes** of training.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Generate a reproducible binary delayed-memory task. Each sequence should contain one informative first token `+1` or `-1`, followed by random distractor tokens, and the label should be whether the FIRST token was `+1`. Use variable training lengths from about 5 to 30 and create held-out evaluation sets at lengths 5, 10, 20, 30, 40, 60 and 80. Show a few sequences and labels. Explain why a model that looks only at the last token should be near chance.

### Questions

1. Where is the only reliable information about the label?
2. What must a sequence model do with that information while distractors arrive?
3. Why does increasing sequence length make the same task harder for some recurrent systems?

---

## Prompt 2

> Build two small PyTorch models with the same hidden size: (A) a one-layer tanh `nn.RNN` and (B) a one-layer `nn.GRU`. Each receives one scalar token at a time and predicts the binary label from the FINAL hidden state. Train both ONCE on exactly the same training batches using BCEWithLogitsLoss and the same optimiser settings, recording train and validation accuracy. Save both models. Briefly explain the input, hidden state and final output, and note that the GRU contains learned gates whereas the vanilla RNN does not.

### Questions

1. Can both models fit short training sequences?
2. Is one model clearly easier to train?
3. What does the final hidden state have to contain for the classifier to succeed?
4. Why is parameter sharing through time useful here?

---

## Prompt 3

> Evaluate the saved RNN and GRU separately at every sequence length from Prompt 1 and plot accuracy against sequence length. On the same graph include a chance line at 50%. Do not retrain at longer lengths. Also report the models' average confidence for correct and incorrect predictions.

### Questions

1. Which model retains useful performance over longer delays?
2. Does accuracy degrade smoothly or suddenly?
3. Is high confidence reliable once the sequence is much longer than those used in training?
4. What does this experiment tell you about calling a hidden state “memory”?

---

## Prompt 4

> For a correctly classified example at several lengths, compute the gradient of the final classification logit with respect to EACH input token. Plot absolute gradient magnitude by sequence position for the RNN and GRU. Use the saved models and no additional training. Also print the gradient magnitude at the first informative token and the last distractor token.

### Questions

1. How much influence from the first token reaches the final output through each model?
2. Does the gradient generally weaken as the path through time becomes longer?
3. Is the gradient plot identical to a direct measure of stored information?
4. How do the GRU's gates relate conceptually to preserving useful state?

---

## Try it yourself manually

Without asking Gemini to rewrite the model, return to the **evaluation code from Prompt 3** and add an even longer sequence length such as `120` or `160`.

Before running, predict the accuracy of both models.

- Does either model retain performance beyond the training-length range?
- Is failure at a new length necessarily evidence that the model never learned the original task?
- Why should claims about “long-term memory” state the range over which they were tested?

---

## Reveal: what was this experiment really about?

A recurrent network repeatedly compresses its past into a hidden state. In principle that state can carry information indefinitely; in practice, learning to preserve information across many repeated transformations is difficult.

Vanilla recurrence can attenuate both state information and gradients over long paths. GRU gates provide learned routes for deciding what to preserve, update and forget, which can make longer dependencies easier to maintain.

The important lesson is not that a GRU has perfect memory. It is that **architecture changes the path through which information and gradients must survive**.

Now ask Gemini:

> Using our accuracy-versus-length curves and input-gradient plots, compare the vanilla RNN and GRU as memory mechanisms. Explain what the experiment supports about gating and long-range dependencies, and distinguish training-range generalisation from the broader claim that a model can remember arbitrarily long sequences.

### Final discussion questions

1. Why can an RNN succeed at short sequences but fail as the delay grows?
2. What problem are gates trying to solve?
3. Why is the final hidden state a bottleneck?
4. What kind of architecture might avoid forcing all earlier information through one long recurrent path?
