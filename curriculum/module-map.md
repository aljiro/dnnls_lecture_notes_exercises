# DNNLS Module Map

This document is the high-level map of the module. It records what each week introduces and the conceptual role that week plays in the larger progression.

## Week 1 — Introduction and fundamentals of machine learning

**Syllabus focus**
- Core machine-learning concepts and terminology
- Sampling and datasets
- Matrix multiplication as transformation
- Early learning algorithms and simple decision rules

**Conceptual role**
Students should begin to see datasets as samples rather than reality itself, and matrix multiplication as a transformation of representations rather than merely arithmetic.

## Week 2 — Building blocks: linear projections

**Syllabus focus**
- Linear regression
- Linear layers
- Loss functions
- Gradients
- Gradient descent

**Conceptual role**
Establish the loss as a specification of what matters and gradient descent as a mechanism for changing a model in response to that specification.

## Week 3 — Building blocks: MLP projections

**Syllabus focus**
- Multilayer perceptrons
- Non-linearities
- Backpropagation

**Conceptual role**
Move from fitting with a linear map to learning intermediate representations that can transform a difficult problem into an easier one.

## Week 4 — Model and learning engineering

**Syllabus focus**
- Training dynamics
- Initialization and normalization
- Regularization
- Optimization techniques
- Generalization and capacity

**Conceptual role**
Separate successful optimization from successful learning. Show that many solutions can fit the training data and that training dynamics influence which solution is found.

## Week 5 — Visual encoders

**Syllabus focus**
- Convolutional neural networks
- Locality
- Weight sharing
- Receptive fields
- Visual representations

**Conceptual role**
Make architectural inductive bias explicit. A CNN succeeds not because it contains more information, but because it assumes particular structure about images.

## Week 6 — Explainable AI

**Syllabus focus**
- Saliency and attribution
- Representation probing
- Explainability methods
- Intervention and causal intuition

**Conceptual role**
Ask what evidence is sufficient to claim that a model represents or uses a feature. Encourage skepticism about visually plausible explanations.

## Week 7 — Building blocks: basic language encoders

**Syllabus focus**
- Text representations
- Recurrent networks
- LSTM
- Transformers
- Self-supervised and contrastive objectives

**Conceptual role**
Explore how structure, order, and memory enter a representation, and how losses can align representations without explicit class labels.

## Week 8 — Autoencoders and generative AI

**Syllabus focus**
- Autoencoders
- Variational autoencoders
- Adversarial generation
- Basic diffusion

**Conceptual role**
Shift from predicting labels to learning distributions and latent spaces. Compare how different objectives shape what is represented.

## Week 9 — Temporal modelling, attention, and integration

**Syllabus focus**
- Temporal information flow
- Recurrent modelling
- Attention
- Cross-attention and multimodal integration

**Conceptual role**
Unify memory and attention as different solutions to the problem of storing, retrieving, and routing information.

## Week 10 — Representation dynamics and modern understanding

**Potential focus**
- Grokking
- Neural collapse
- Superposition
- Sparse feature recovery
- Scaling and measurement

**Conceptual role**
Study structure that emerges after ordinary metrics appear to have saturated, and reveal that model behaviour is often hidden in representation geometry.

## Week 11 — Learning during inference

**Potential focus**
- In-context learning
- Induction-style circuits
- Test-time training and adaptation
- Test-time compute and verification

**Conceptual role**
Challenge the simple distinction between training and inference. The final conceptual destination is that a trained network can implement a learning process inside its forward computation or test-time procedure.

## Design principle

Each week should contain a small number of canonical experiments. Each experiment should begin with a concrete question, produce evidence that challenges or extends the student's current mental model, and connect explicitly to the larger learning thread documented in `learning-thread.md`.
