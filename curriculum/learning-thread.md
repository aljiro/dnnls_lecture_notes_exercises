# DNNLS Learning Thread

This document records the deeper conceptual progression that runs underneath the weekly syllabus.

The purpose is to keep the module from becoming a collection of disconnected techniques. Each lecture and experiment should advance one or more links in this chain.

## Core progression

Examples
→ Sampling
→ Linear transformations
→ Loss as specification
→ Optimisation
→ Representation
→ Generalisation
→ Inductive bias
→ Information and explanation
→ Memory
→ Information routing
→ Representation geometry
→ Learning during inference

## Interpretation

### Examples → Sampling
A dataset is a finite observation of a larger process. Students should learn to reason about uncertainty, representativeness, and what can or cannot be inferred from a sample.

### Sampling → Linear transformations
Data become useful to a learner through representations. Matrix multiplication should be understood geometrically as transforming, projecting, stretching, combining, or discarding information.

### Linear transformations → Loss as specification
A model does not know what the teacher intends. The loss function defines what differences matter and therefore what kind of solution is rewarded.

### Loss as specification → Optimisation
Gradient-based learning is the mechanism by which the model reacts to the signal encoded by the loss. Gradients are local messages about how parameters should change.

### Optimisation → Representation
With depth and non-linearity, learning becomes more than fitting an output rule. Intermediate layers can reorganise the problem into representations where useful distinctions become easier to express.

### Representation → Generalisation
A network can fit examples without learning the intended structure. Generalisation requires asking what regularities the representation captures beyond the observed data.

### Generalisation → Inductive bias
Architecture, optimization, data augmentation, and regularization constrain which solutions are easy to discover. These biases are part of the learner, not incidental engineering details.

### Inductive bias → Information and explanation
Once a model has learned a representation, we need evidence about what information it contains and what information the prediction actually uses. Explanation methods should therefore be tested, not merely visualized.

### Information and explanation → Memory
Sequential problems require representations that preserve, update, or retrieve information over time. Memory becomes an explicit computational problem.

### Memory → Information routing
Attention and related mechanisms allow different information to become relevant for different queries. Computation becomes conditional rather than uniformly applied.

### Information routing → Representation geometry
Modern neural networks often encode concepts in distributed directions, subspaces, superpositions, and evolving geometries rather than in isolated neurons. Accuracy alone can hide this structure.

### Representation geometry → Learning during inference
The final conceptual step is to question the boundary between learning and inference. A trained model can implement adaptation, retrieval, optimization-like computation, or memory updates during the forward/test-time process itself.

## Design test for new material

Before adding an experiment or lecture topic, ask:

1. What concrete phenomenon will the student observe?
2. Which link in the learning thread does it strengthen?
3. What misconception or incomplete mental model does it challenge?
4. Does the student need to run an experiment, or could the same insight be learned more directly?
5. If the experiment is computationally expensive, what should be recorded so later prompts can reuse the same run?
6. What idea should the student be able to transfer to a new setting afterwards?

A technically interesting demonstration is not automatically a useful DNNLS exercise. It should earn its place by advancing the learning thread.
