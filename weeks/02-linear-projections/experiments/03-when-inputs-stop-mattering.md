# Experiment 3 — What does a model learn when the input tells it nothing?

**Dataset:** A small synthetic regression dataset generated directly in the notebook. One version preserves a real relationship between input and target; another destroys that relationship by shuffling the inputs.

**Key concepts:** signal, noise, informative input, shuffled input, linear model, weight, bias, constant predictor, baseline, input dependence, training loss.

**Expected computational budget:** Negligible. All runs should take only seconds.

**Recommended runtime:** **CPU.** A GPU is unnecessary for this experiment.

> **Copy and paste these queries to Gemini in your Colab and answer the questions.**

Do not read ahead while doing the experiment. Run each prompt, inspect the result, and answer the questions before continuing.

---

## Prompt 1

Copy this into Gemini:

> Create about 100 input values `x` and targets generated approximately from `y = 2x + 5` with moderate random noise. Set a fixed seed. Make a second version of the dataset by randomly shuffling the `x` values while leaving the `y` values in their original order. Plot the original `(x, y)` pairs and shuffled `(x, y)` pairs side by side. Also add an interactive slider labelled `fraction shuffled` from 0% to 100%. Moving the slider should update one scatter plot by progressively breaking that fraction of the input-target pairings using a fixed reproducible permutation; do not regenerate the underlying `x` or `y` values. Do not train anything yet. Briefly explain exactly what information the shuffle destroys and what information remains unchanged.

### Questions

1. Which plot shows an obvious relationship between input and target?
2. Do both versions contain exactly the same individual `x` values?
3. Do both versions contain exactly the same individual `y` values?
4. What changed when only the pairing was shuffled?
5. As you move the slider, does the useful relationship disappear all at once or progressively?
6. Could a learner infer the original relationship from the fully shuffled pairs alone?

---

## Prompt 2

> Train the same linear model `y_hat = w*x + b` on both datasets using the explicit gradient-descent code from the previous experiment. Use MSE and the same starting values and learning rate for both runs. Plot both fitted lines, report the final `w`, `b`, and loss, and also print the mean of `y`. Briefly explain how the same model behaves differently when the input-target relationship is preserved versus destroyed.

### Questions

1. What weight did the model learn on the informative data?
2. What happened to the weight on the shuffled data?
3. What value did the bias approach on the shuffled data?
4. How close is that bias to the mean target value?
5. Has the shuffled-data model still been "trained" even though its input is not useful?

---

## Prompt 3

> For both trained models, evaluate predictions over a dense range of `x` values and report the standard deviation of the predictions. Also compare each model with a baseline that always predicts the mean training target. Plot the three prediction behaviours: informative linear model, shuffled-input linear model, and constant-mean baseline. Briefly explain what prediction spread tells us about how much the output changes when the input changes.

### Questions

1. Which trained model changes its prediction most as `x` changes?
2. Which trained model resembles the constant baseline?
3. Can a low-ish loss alone tell us whether the model is using the input?
4. What extra diagnostic did prediction spread provide?

---

## Prompt 4

> Return to the shuffled-input dataset. Train the same linear model twice: once with both `w` and `b`, and once with the bias forced to zero so the model is only `y_hat = w*x`. Use the same optimization settings. Compare the final losses and fitted lines. Briefly explain what role the bias can play when the input carries little or no useful information.

### Questions

1. Which version gets the lower loss?
2. Why does the bias help so much in the shuffled case?
3. Is the bias merely a small correction here, or is it doing most of the predictive work?
4. What would happen if the target mean were close to zero instead?

---

## Prompt 5

> Starting from the informative dataset, create several partially shuffled versions by randomly breaking the input-target pairing for approximately 0%, 25%, 50%, 75%, and 100% of the examples. Train the same linear model on each version with the same settings. Plot learned `w`, learned `b`, final loss, and prediction spread against shuffle percentage. Keep the procedure simple and reproducible. Briefly explain what trend you see as useful input information is gradually removed.

### Questions

1. What happens to the learned weight as more pairings are destroyed?
2. What happens to the bias?
3. What happens to prediction spread?
4. Does the transition from "using the input" to "mostly predicting a baseline" happen abruptly or gradually?
5. Why is deliberately shuffling inputs a useful diagnostic?

---

## Try it yourself manually

Without asking Gemini to rewrite the code, return to the **code cell generated by Prompt 1 in this experiment** and increase or decrease the amount of noise used when generating `y`.

Then rerun the relevant cells from this experiment.

Before rerunning, predict what will happen to the learned weight and final loss.

- Does adding noise make the input completely useless immediately?
- How does the informative model gradually begin to resemble the baseline?
- Can you find a noise level where the relationship is still visible but much harder to learn?

---

## Reveal: what was this experiment really about?

The objective was to discover that a model can optimize its loss while learning **very little dependence on the input**.

When the input-target relationship was destroyed, the linear model could no longer learn a useful slope. Under MSE, its bias moved toward the mean target and the model became close to a constant predictor. The bias was no longer a small correction: it was effectively the whole model.

This gives us an important diagnostic habit: do not ask only whether a model trained or whether its loss decreased. Ask whether its predictions actually change when the informative input changes.

Now ask Gemini:

> We have just compared a linear model trained on correctly paired data with the same model trained after shuffling the inputs. Discuss with me why the shuffled model can still reduce its loss, why its bias approaches a useful baseline, and why this does not mean it learned the intended relationship. Connect the explanation to the learned weight, bias, prediction spread, and constant-mean baseline. Then discuss why shuffling or replacing an input can be a useful test of whether a larger machine-learning model actually uses that input.

### Final discussion questions

1. What is the difference between fitting the target distribution and using the input-target relationship?
2. Why can a bias term become the dominant part of a model?
3. Why is "the loss went down" insufficient evidence that a model learned what we intended?
4. What simple test could you use later to check whether a model depends on one particular input source?
