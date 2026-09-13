# DNNLS Module Map

This document is the detailed teaching map for the module. It is deliberately more detailed than a public-facing syllabus: each week should be usable as a specification/prompt for writing the lecture notes, while preserving the deeper conceptual progression in `learning-thread.md`.

The module should not read as a catalogue of architectures. The recurring questions are:

- What is the learning problem?
- What information is available to the model?
- What computation does the architecture make easy or difficult?
- What objective tells the model what matters?
- How does optimisation turn that objective into behaviour?
- What representation has been learned, and does it generalise?
- What evidence supports our interpretation of the model?
- When there are several plausible outputs, should the model predict one answer, a distribution, or retrieve an existing example?

The StoryReasoning architecture-evolution case study can be used selectively across the module as a running source of concrete examples. It should support the concepts rather than determine the order of the lectures.

---

## Week 1 — What is machine learning? Problems, data, and learning from examples

### Central question
What does it mean for a machine to learn from data, and what kinds of problems can we ask it to solve?

### Lecture-note scope

#### 1. A short intellectual history
Give a compact history connecting statistics, machine learning, neuroscience and modern deep learning. The purpose is not a chronology of famous names, but to show the different traditions that contributed ideas:

- statistical estimation and fitting models to observations;
- pattern recognition and early machine learning;
- biological inspiration: neurons, distributed computation and learning from examples;
- symbolic AI versus learned representations;
- perceptrons and early neural networks;
- the return of neural networks through backpropagation, larger datasets and compute;
- the modern shift from hand-designed features to learned representations and foundation models.

Distinguish biological inspiration from biological realism. Modern neural networks borrow a few broad ideas from neuroscience but are engineering and mathematical systems in their own right.

#### 2. What a machine-learning task is
Introduce the idea that a dataset is a finite sample from a larger process. Define examples, features/inputs, targets/labels where relevant, and the distinction between the data we observe and the process we hope to generalise to.

Introduce the major problem types:

- **classification** — choose among discrete categories;
- **regression** — predict continuous values;
- **density estimation / generative modelling** — model how data are distributed and generate plausible samples;
- **structured prediction** — outputs with internal structure, such as sequences, segmentations or bounding boxes;
- **ranking and retrieval** — identify which candidate is most relevant or similar.

Use modern examples to make clear that the same basic problem types appear in many forms: image classification, semantic segmentation, object detection, sentiment classification, speech recognition, translation, text completion, image generation, next-frame prediction, recommendation and retrieval.

#### 3. Learning paradigms
Introduce, at a conceptual level:

- supervised learning;
- unsupervised learning;
- self-supervised learning;
- semi-supervised learning;
- reinforcement learning only briefly, as a different feedback structure rather than a focus of the module.

Emphasise that modern systems often combine paradigms: for example, a representation can be learned self-supervised and later adapted to a supervised task.

#### 4. The supervised-learning problem formally
Introduce the basic formal ingredients that will be reused throughout the module:

- dataset \(D = \{(x_i, y_i)\}\);
- a parameterised model \(f_\theta(x)\);
- predictions \(\hat y\);
- a loss function measuring what kinds of errors matter;
- training as the process of changing \(\theta\) to reduce an objective;
- evaluation on data that were not used to fit the parameters.

Do not yet develop gradient descent mathematically; Week 2 does that. The purpose here is to give students the complete skeleton of a learning system.

#### 5. Baselines and the meaning of performance
Introduce the habit of asking, "better than what?" A metric is only meaningful next to a sensible comparison: chance, a constant predictor, a simple heuristic or another trivial baseline. This becomes a recurring engineering principle later in the module.

### Key concepts
Examples, sampling, population/process, features, labels, model, parameters, prediction, target, loss, training, inference, classification, regression, density estimation, structured prediction, retrieval, supervised learning, unsupervised learning, self-supervised learning, generalisation, baseline.

### Conceptual role
Students should leave Week 1 seeing machine learning as **learning a rule from a finite sample under an explicitly chosen objective**, not as a collection of algorithms. This establishes the first two links of the learning thread: examples → sampling → model/loss.

### Architecture-evolution connection
The StoryReasoning task is a useful example of why task definition matters: "predict the next frame" can mean pixel prediction, latent prediction, retrieval, or prediction of a distribution over plausible futures. Those choices create different learning problems even when the raw data are identical.

---

## Week 2 — Regression, losses, gradients, and stochastic optimisation

### Central question
How can a model turn inputs into numerical predictions, measure its mistakes, and change itself to improve?

### Lecture-note scope

#### 1. Linear regression as the first complete learning system
Start with scalar regression and move to multiple inputs. Introduce:

- a linear model as weighted combination plus bias;
- matrix multiplication as the compact form of many weighted combinations;
- the geometry of a linear map: projection, rotation, scaling and mixing of coordinates;
- predictions, targets and residuals;
- mean-squared error and, where useful, mean-absolute error as different specifications of error.

Keep matrix multiplication tied to transformations and representations rather than treating it as purely symbolic manipulation.

#### 2. Loss as specification
Make explicit that the model does not know the teacher's intention; it only receives the objective. Different losses reward different behaviours. Use simple examples where MSE and MAE prefer different solutions and introduce the distinction between the training objective and the evaluation metric.

#### 3. Gradients
Develop the intuition of a derivative as local sensitivity and a gradient as a collection of local sensitivities. Show how changing a parameter slightly changes the prediction and therefore the loss.

The mathematical level should be enough for students to understand the update rule and later backpropagation, without turning the lecture into a calculus course.

#### 4. Gradient descent
Introduce:

- learning rate;
- iterative parameter updates;
- loss surfaces at a conceptual level;
- why very small or very large learning rates cause problems;
- convergence as a trajectory rather than a single algebraic solution.

#### 5. Stochastic gradient descent and mini-batches
Move from full-batch gradient descent to stochastic and mini-batch optimisation:

- why computing the exact full-data gradient is expensive;
- batches and epochs;
- stochasticity as both approximation and useful noise;
- the difference between batch size, number of updates and number of epochs;
- shuffling and sampling training examples.

Introduce the practical training loop: sample batch → forward pass → compute loss → compute gradients → update parameters → repeat.

### Key concepts
Linear regression, linear layer, weights, bias, matrix multiplication, residual, objective, MSE, MAE/L1, derivative, gradient, learning rate, gradient descent, SGD, mini-batch, batch size, epoch, training loop.

### Conceptual role
This week makes **loss as specification → optimisation** concrete. Students should be able to explain not only what a linear model computes but how a loss becomes a parameter update.

### Architecture-evolution connection
The architecture study provides a later example of an important Week-2 lesson: pixel L1 is not a neutral choice. On a multimodal next-frame task it rewards an average/median-looking output. The failure is therefore partly in the objective, not merely in the optimiser or architecture.

---

## Week 3 — From perceptrons to MLPs: non-linearity, decision boundaries, and backpropagation intuition

### Central question
What can a neural network represent that a single linear transformation cannot?

### Lecture-note scope

#### 1. The perceptron / artificial neuron
Build directly from Week 2. Present a neuron as a linear projection followed by a non-linear activation. Explain why stacking purely linear layers still produces only a linear transformation.

Introduce common activations with emphasis on intuition:

- step/sign historically;
- sigmoid and tanh;
- ReLU as the main geometric example;
- optionally GELU as a modern smooth activation without dwelling on its formula.

#### 2. Classification and decision boundaries
Introduce binary classification geometrically. A linear classifier creates a hyperplane/decision boundary. Show why some datasets cannot be separated by one linear boundary.

Use 2D examples to connect model behaviour to geometry rather than only equations.

#### 3. Multilayer perceptrons
Introduce:

- input, hidden and output layers;
- depth and width;
- hidden activations as learned intermediate representations;
- how ReLU networks partition input space into regions with different linear behaviour;
- how additional layers can progressively reshape a problem until it becomes linearly separable at the output.

The key mental model is that hidden layers **transform the representation of the problem**.

#### 4. Forward pass and backward pass
Define the forward pass as computation of activations and the loss. Introduce the backward pass as propagating information about sensitivities from the loss back through the computation.

Use a small computational graph to motivate the chain rule and explain why intermediate activations are needed for gradient computation. Leave the fuller implementation and engineering discussion for Week 4.

#### 5. Backpropagation intuition
Explain backpropagation as efficient reuse of local derivatives through a composed function, not as a mysterious neural-network-specific algorithm. Students should understand why every differentiable component participates in one larger computational graph.

### Key concepts
Perceptron, neuron, activation, non-linearity, sigmoid, tanh, ReLU, MLP, depth, width, hidden layer, representation, classification, logit, decision boundary, forward pass, backward pass, computational graph, chain rule, backpropagation.

### Conceptual role
This week establishes **optimisation → representation**. A neural network is no longer only fitting an output rule; it is learning transformations that reorganise the input space.

### Architecture-evolution connection
The narrow 16-dimensional ReLU bottleneck in the original StoryReasoning model later gives a concrete example of representation failure: many latent units died and the representation became almost constant. That case can be foreshadowed here and diagnosed properly in Week 4.

---

## Week 4 — Model and learning engineering: classification, backpropagation, optimisation, and generalisation

### Central question
Why can a mathematically valid neural network still train badly, generalise badly, or optimise the wrong behaviour?

### Lecture-note scope

#### 1. Backpropagation in a complete network
Return to the Week-3 computational graph and now follow gradients through several layers. Explain parameter gradients, activation gradients and how automatic differentiation implements the same chain-rule logic.

Keep the mathematics transparent but not excessively symbolic: students should be able to trace where gradients come from and understand common failure modes.

#### 2. Neural networks for classification
Develop binary and multi-class classification:

- logits;
- one-output binary classifier with sigmoid + binary cross-entropy;
- two-class / multi-class classifier with softmax + cross-entropy;
- why sigmoid and softmax are not interchangeable probability interpretations;
- numerical convention: modern libraries often combine logits and the loss for stability.

Introduce common loss functions and match them to task/output structure rather than presenting them as a memorisation table.

#### 3. Training dynamics
Discuss the shape of optimisation in realistic neural networks:

- plateaus, saddle regions and local minima;
- noisy gradients;
- vanishing and exploding gradients;
- dead ReLUs;
- sensitivity to learning rate and initialisation;
- why "the loss went down" does not by itself prove that the intended behaviour was learned.

Avoid over-emphasising local minima as the dominant practical problem; use them as one part of a broader training-dynamics story.

#### 4. Optimisers and schedules
Introduce SGD with momentum and Adam/AdamW conceptually, then learning-rate schedules such as step/cosine/OneCycle at a high level. Explain weight decay. Introduce curriculum learning as changing the distribution or difficulty of training examples over time.

The goal is to understand what these mechanisms change about the optimisation trajectory, not to memorise APIs.

#### 5. Initialisation and normalisation
Introduce why scale matters through depth. Cover sensible initialisation (e.g. Xavier/Kaiming conceptually) and the purposes of BatchNorm, LayerNorm and GroupNorm. Connect normalization to stable optimisation and to the geometry/statistics of representations.

#### 6. Underfitting, overfitting and generalisation
Develop:

- model capacity;
- underfitting versus overfitting;
- training, validation and test sets;
- why hyperparameter choices use validation data, not test data;
- data leakage;
- early stopping;
- regularisation: weight decay, dropout, data augmentation and capacity control;
- double descent as an important modern complication to the simple bias-variance cartoon.

Treat calibration as distinct from accuracy: a classifier can be correct often but poorly calibrated in its confidence.

#### 7. Diagnostics and experimental discipline
Add an explicit engineering section, informed by the module's architecture-evolution work:

- always compare losses/metrics against simple floors or baselines;
- inspect train and validation trends, not only the last batch;
- check whether predictions vary with the input;
- use shuffled-condition or permutation controls when claiming that a model uses a signal;
- compare against trivial heuristics;
- perform ablations when several components are present;
- select checkpoints using the metric that actually represents the desired behaviour;
- distinguish optimisation failure, representation collapse, overfitting and objective mismatch.

Introduce multi-task learning at a conceptual level: when several losses act through one shared representation, the gradients can compete and one task can dominate.

### Key concepts
Logits, sigmoid, softmax, binary cross-entropy, cross-entropy, backpropagation, automatic differentiation, initialisation, vanishing/exploding gradients, dead ReLU, SGD with momentum, Adam/AdamW, weight decay, schedule, curriculum, BatchNorm, LayerNorm, GroupNorm, capacity, overfitting, underfitting, train/validation/test split, calibration, regularisation, dropout, early stopping, double descent, baseline, ablation, representation collapse, multi-task competition.

### Conceptual role
This week establishes **representation → generalisation** and makes experimental discipline part of the subject rather than an afterthought.

### Architecture-evolution connection
This is the main home for the StoryReasoning diagnostic lessons: the identical content/context output, the constant latent, dead ReLUs, misleading last-batch logging, latent collapse, heads competing through a shared vector, drift in pretrained components, early overfitting, and the need for floors, retrieval metrics, shuffled-condition tests and reconstruction monitors.

---

## Week 5 — Convolutional networks and architectural inductive bias for vision

### Central question
How can architecture encode assumptions about the structure of images so that learning becomes easier and more data-efficient?

### Lecture-note scope

#### 1. Feature extraction versus prediction head
Introduce the useful conceptual split between a **feature extractor / encoder** and a **task-specific head**. Explain that the same visual representation can feed a classifier, detector, segmentation head, retrieval system or decoder.

This is a good point to revisit transfer learning and pretrained feature extractors at a basic practical level.

#### 2. Why fully connected networks are a poor default for images
Use image dimensionality and spatial structure to motivate convolution. Develop the architectural biases:

- local receptive fields;
- weight sharing;
- translation equivariance/robustness;
- fewer parameters;
- hierarchical/compositional features.

Clarify **equivariance** versus **invariance** with concrete transformations.

#### 3. Convolutional layers
Cover:

- filters/kernels;
- channels and feature maps;
- stride;
- padding;
- receptive field growth;
- downsampling;
- parameter count and output-size calculations.

Relate these operations to learned feature detection rather than treating convolution as only an image-processing formula.

#### 4. Pooling, dropout and spatial compression
Discuss max/average pooling, strided convolution and the trade-off between spatial precision and abstraction. Revisit dropout as regularisation rather than a uniquely convolutional component.

#### 5. CNN architectures and architectural evolution
Use a small number of canonical networks to show ideas rather than memorise historical blueprints:

- LeNet as an early pattern;
- AlexNet as the deep-learning/ImageNet turning point;
- VGG as repeated small convolutions and depth;
- ResNet and skip/residual connections as a solution to training deeper networks.

Explain skip connections conceptually as creating easier information and gradient paths. Optionally mention that many modern architectures combine convolutional and attention-based ideas.

#### 6. Encoders, decoders and autoencoders as visual components
Introduce a convolutional encoder/decoder pair lightly here because it becomes central in Week 8. Explain reconstruction as a way to learn a compact latent representation and the importance of the bottleneck.

### Key concepts
Feature extractor, encoder, head, convolution, kernel/filter, channel, feature map, locality, receptive field, weight sharing, translation equivariance, invariance, stride, padding, pooling, dropout, hierarchical features, residual/skip connection, pretrained encoder, transfer learning, latent representation.

### Conceptual role
This week establishes **generalisation → inductive bias**. Architecture is presented as a set of assumptions about the structure of the problem, not as decoration around an optimiser.

### Architecture-evolution connection
The visual autoencoder in the StoryReasoning model is a direct example of separating representation learning from sequence prediction: pretraining the convolutional autoencoder makes the later predictor input-specific, while a randomly initialised image encoder had failed to learn a useful representation. The reconstruction monitor later shows why pretrained components can drift during joint training.

---

## Week 6 — Explainability, interpretability, and evidence about what a model uses

### Central question
What does it mean to explain a neural-network prediction, and what evidence is strong enough to claim that a model represents or uses a feature?

### Lecture-note scope

#### 1. Vocabulary and scope
Organise methods along several axes:

- **global** versus **local** explanations;
- **model-agnostic** versus **model-specific**;
- **post-hoc** versus **inherently interpretable**;
- explanation of a prediction versus explanation of a representation or mechanism.

Make clear that interpretability has several goals: debugging, trust, scientific understanding, compliance, discovering spurious correlations, and identifying failure modes.

#### 2. Families of explanation methods
Introduce the major mechanisms students will later explore in the lab:

- **gradients / saliency** — use model derivatives;
- **feature permutation / perturbation** — change inputs and observe output changes;
- **model approximation** — fit a simpler local surrogate;
- **feature attribution** — assign contribution scores;
- **counterfactuals** — ask what minimal change would alter the prediction.

#### 3. Core methods
Explain the intuition, assumptions and limitations of:

- Integrated Gradients (IG);
- Expected Gradients (EG);
- LIME;
- SHAP / Shapley-value intuition.

Avoid presenting attractive heatmaps as automatically faithful explanations. Distinguish correlation, sensitivity and causal dependence.

#### 4. Probing and intervention
Add representation-level methods that connect naturally to the rest of the module:

- linear probes / classifiers on hidden representations;
- ablation and activation intervention;
- permutation controls;
- testing whether information is merely decodable versus actually used by the prediction.

This is a natural point to warn that **attention weights are not automatically explanations**.

#### 5. Intrinsic interpretability and sparse representations
Give a brief tour of interpretable-by-design models and sparse feature representations. Introduce sparse autoencoders as one modern attempt to decompose distributed representations into more interpretable features, without yet going deeply into superposition; Week 10 revisits the representation-geometry motivation.

#### 6. Transfer learning bridge
Use a short section on transfer learning to connect Week 5's pretrained feature extractors to the question of what features are reusable across tasks. This should be a bridge, not a second full transfer-learning lecture.

### Key concepts
Explainability, interpretability, global/local, model-agnostic/model-specific, post-hoc/intrinsic, saliency, gradient attribution, perturbation, permutation importance, surrogate model, Integrated Gradients, Expected Gradients, LIME, SHAP, counterfactual, probe, ablation, intervention, faithfulness, sparse autoencoder, transfer learning.

### Conceptual role
This week establishes **inductive bias → information and explanation**. Students should become sceptical of explanations that look plausible but are not tested against controls.

### Architecture-evolution connection
The architecture study contains several naturally interpretable quantities—attention weights, gates, retrieval ranks, latent similarities and per-slot character predictions—but also demonstrates why inspectability is not the same as faithfulness. For example, attention learned a positional prior before it learned per-window selection.

---

## Week 7 — Language representations, sequence models, and autoregressive prediction

### Central question
How can a neural network represent ordered symbolic data and use information from earlier positions to predict what comes next?

### Lecture-note scope

#### 1. Turning language into numbers
Introduce:

- tokens and tokenisation;
- word-level versus subword tokenisation;
- one-hot representations as a baseline;
- learned embeddings;
- geometric intuition for embedding spaces and similarity;
- positional/order information as something that must be represented explicitly in many architectures.

#### 2. Recurrent neural networks
Introduce RNNs as repeated application of the same transition over a sequence. Cover hidden state as memory, parameter sharing through time, and backpropagation through time conceptually.

Explain the difficulty of long-range dependencies through vanishing/exploding gradients.

#### 3. LSTM and GRU
Motivate gating as controlled information retention, update and forgetting. Explain LSTM and GRU conceptually; students do not need to memorise every gate equation, but should understand what the gates accomplish.

#### 4. Sequence-to-sequence and conditional generation
Introduce encoder/decoder thinking, teacher forcing, start/end tokens and autoregressive factorisation:

\[
p(x_1, \ldots, x_T) = \prod_t p(x_t \mid x_{<t}).
\]

Explain greedy decoding versus sampling at a basic level. Introduce exposure to previous tokens as both a strength and a source of train/test mismatch.

#### 5. Condition ignoring and information bottlenecks
Use conditional generation to show that a decoder can learn to ignore a conditioning vector if previous tokens already predict the next token well. Introduce word/token dropout as one way of forcing greater use of the condition.

#### 6. Attention as the bridge to transformers
Finish by motivating attention: rather than compressing an entire sequence into one recurrent state, allow a query to retrieve different information from different positions. Give the basic query/key/value idea and defer the full transformer mechanics to Week 9.

#### 7. First transformer view
Show the high-level transformer block and explain why it parallelises sequence processing better than recurrence. Keep this introductory: Week 9 will unpack self-attention, multi-head attention, positional encodings and cross-attention in detail.

### Key concepts
Token, tokenisation, subword, embedding, semantic similarity, sequence, hidden state, RNN, LSTM, GRU, backpropagation through time, sequence-to-sequence, teacher forcing, autoregressive model, language model, greedy decoding, sampling, condition ignoring, attention, query/key/value, transformer.

### Conceptual role
This week establishes **information and explanation → memory**. Sequential modelling is framed as the problem of preserving and using information over time.

### Architecture-evolution connection
The StoryReasoning system contains a useful progression from a tiny frozen LSTM text autoencoder, to MiniLM sentence embeddings, to a conditional LSTM decoder, and finally to a decoder with richer memory/cross-attention. Its shuffled-condition test also provides a clean example of how to verify that a conditional language model is actually using its condition.

---

## Week 8 — Generative modelling: autoencoders, VAEs, GANs, diffusion, and conditioning

### Central question
How do we move from predicting one label or one point estimate to modelling a distribution of plausible data?

### Lecture-note scope

#### 1. Deterministic autoencoders
Develop the encoder → latent → decoder pattern introduced in Week 5. Explain reconstruction losses, bottlenecks, latent representations and the tension between compression and reconstruction fidelity.

Use this to distinguish **representation learning** from **generation**: a standard autoencoder can reconstruct data without defining a useful generative distribution.

#### 2. Variational autoencoders
Introduce:

- a distribution over latent variables rather than a single code;
- prior and approximate posterior;
- mean and variance parameters;
- reparameterisation trick;
- reconstruction term + KL divergence;
- sampling at inference time;
- the trade-off between reconstruction and regularising the latent distribution.

The mathematical treatment should be enough to understand the training objective and why sampling becomes meaningful.

#### 3. Multimodality: why averaging produces blur
Explicitly teach the distinction between point prediction and distributional prediction. If several different outputs are plausible, MSE tends toward a mean and L1 toward a median. A sampled generative model can instead represent multiple possible futures.

This is a central conceptual bridge from earlier regression losses to modern generative AI.

#### 4. GANs
Give a high-level but technically honest account of generator/discriminator training, adversarial objectives, realistic samples, mode collapse and instability. The goal is comparison of generative principles, not implementation detail.

#### 5. Diffusion models
Introduce the basic idea:

- gradually add noise;
- train a model to reverse/denoise the process;
- iterative sampling from noise toward data;
- conditioning as information that steers denoising.

Keep the probability derivation light unless needed elsewhere in the module.

#### 6. Conditioning and multimodal generation
Explain conditional generation by labels, text embeddings or other modalities. Introduce classifier-free guidance only briefly if useful as an example of strengthening conditioning.

#### 7. CLIP and aligned representation spaces
Introduce CLIP as a contrastive image-text representation model. Explain at a high level how paired image/text data and a contrastive objective align two modalities into a shared space. Connect this to conditioning, retrieval and evaluation.

#### 8. Sampling and evaluation
Contrast average metrics with sample-based evaluation. Introduce ideas such as best-of-K, diversity versus fidelity, and retrieval of nearest examples in an embedding space. Emphasise that a generative metric should match what "good" generation means for the task.

### Key concepts
Autoencoder, encoder, decoder, bottleneck, latent space, reconstruction loss, VAE, prior, posterior, KL divergence, reparameterisation trick, sample, multimodal target, GAN, generator, discriminator, mode collapse, diffusion, denoising, conditioning, guidance, CLIP, contrastive alignment, best-of-K, diversity.

### Conceptual role
This week shifts the student from **predicting one answer** to **learning distributions and latent spaces**.

### Architecture-evolution connection
This is the main home for the architecture study's deepest generative lesson: a deterministic L1 predictor produces a smooth/median image because the next frame is genuinely multimodal. The later conditional-VAE residual latent, where multiple prior samples can beat the deterministic ceiling, is a direct demonstration of why sampling can be the correct quantity to predict.

---

## Week 9 — Transformers in depth: self-attention, cross-attention, self-supervision, and multimodal information routing

### Central question
How do transformer architectures decide which information should interact, and how are useful representations learned without explicit labels?

### Lecture-note scope

#### 1. Attention revisited
Start from Week 7's query/key/value intuition and derive scaled dot-product attention. Explain:

- queries, keys and values;
- similarity scores;
- softmax weighting;
- weighted combinations;
- masking;
- why the query determines what information is relevant.

Contrast a fixed learned query with a content-dependent query. A fixed query can learn a positional prior; a content-dependent query can select different information for different examples.

#### 2. Self-attention
Explain self-attention as each token querying the sequence. Show how it enables direct long-range interactions and compare its information path with recurrence.

#### 3. Multi-head attention
Introduce multiple heads as multiple learned projection spaces / interaction patterns. Avoid claiming that each head always has a simple semantic interpretation.

#### 4. Position
Explain why attention alone is permutation-invariant over token order and therefore needs positional information. Introduce learned positional embeddings and sinusoidal/relative position ideas at a conceptual level.

#### 5. The transformer block
Cover the recurring architecture:

- attention;
- residual connections;
- normalization;
- feed-forward/MLP sublayer;
- stacking blocks.

Relate residual streams to the Week-5/4 discussion of skip connections and optimisation.

#### 6. Encoder-only, decoder-only and encoder-decoder transformers
Use BERT-style, GPT-style and sequence-to-sequence patterns to distinguish:

- bidirectional representation learning;
- causal autoregressive generation;
- cross-attention from a decoder to another encoded sequence.

#### 7. Self-supervised objectives
Explain how large datasets can provide their own training signal:

- next-token prediction;
- masked-token prediction;
- denoising/reconstruction objectives;
- contrastive objectives such as InfoNCE.

Connect self-supervision to pretrained representations and transfer learning.

#### 8. Cross-attention and multimodal integration
Develop cross-attention as information routing between modalities or memories: text attending to image features, generated tokens attending to an encoder, or a sequence model attending to entity/region tokens.

Discuss early fusion by concatenation versus attention-based fusion at a conceptual level.

#### 9. Retrieval and memory
Introduce retrieval as an alternative/complement to generation: a representation can be used to select the nearest relevant item. This provides a bridge to Week 11's external-memory and in-context systems.

### Key concepts
Attention, query, key, value, scaled dot-product attention, masking, self-attention, multi-head attention, positional encoding, residual stream, transformer encoder, transformer decoder, causal masking, cross-attention, self-supervision, masked modelling, next-token prediction, contrastive learning, InfoNCE, multimodal fusion, retrieval.

### Conceptual role
This week establishes **memory → information routing**. Computation becomes conditional: different tokens, modalities or memory elements can matter for different queries.

### Architecture-evolution connection
The architecture case study provides concrete contrasts among fixed learned attention, content-dependent attention, latent-similarity attention, attention over character/entity tokens, and text cross-attention over input descriptions. It also shows why attention can learn an easy positional prior before learning the desired per-example pattern.

---

## Week 10 — Scaling, conditional computation, and representation geometry

### Central question
What changes when neural networks become large, heavily pretrained systems, and how can useful structure be hidden inside representations even when ordinary task metrics look saturated?

### Lecture-note scope

This week deliberately carries material that would overload Week 9. It should connect modern architecture design with the geometry and dynamics of learned representations.

#### 1. Scaling as an engineering and scientific idea
Introduce the interaction among model size, data size and compute. Discuss scaling laws conceptually: performance often follows predictable trends over ranges of scale, but the relevant resource is not simply "more parameters".

Discuss compute/data trade-offs, training efficiency and why pretraining followed by adaptation is now a dominant pattern.

#### 2. Conditional computation and mixture of experts
Introduce mixture-of-experts (MoE) models as sparse conditional computation:

- router/gating network;
- only a subset of experts active for a token;
- capacity versus compute;
- routing/load-balancing challenges;
- relation to the broader idea that different inputs can activate different computation paths.

Connect gating to simpler learned gates and mixture-of-inputs mechanisms seen earlier in the module.

#### 3. Pretrained and frozen components
Explain why frozen pretrained encoders/target networks can stabilise learning in small-data settings. Introduce the idea behind target networks / momentum encoders at a conceptual level: prevent both sides of a representation objective from drifting together into a trivial solution.

#### 4. Representation collapse and anisotropy
Develop two modern representation-learning phenomena:

- **collapse** — many inputs map to nearly the same representation;
- **anisotropy / common mean direction** — embeddings share a large common component, so raw cosine similarity can become misleading.

Show why centring, normalisation and retrieval-based diagnostics can reveal structure hidden by a raw similarity score.

#### 5. Neural collapse
Introduce neural collapse as a late-training geometric organisation observed in supervised classifiers: within-class features compress and class means/weights adopt highly symmetric structure. Keep the emphasis on what this teaches us about representation geometry rather than on proofs.

#### 6. Superposition and distributed features
Introduce the idea that networks can represent more features than there are easily interpretable coordinates by using distributed directions/subspaces. This motivates why "one neuron = one concept" is often a poor assumption.

#### 7. Sparse feature recovery / sparse autoencoders
Return to sparse autoencoders from Week 6, now with the representation-geometry motivation. Explain the goal of recovering a more interpretable sparse feature basis from a dense/superposed representation, and the limitations of interpreting recovered features.

#### 8. Grokking and delayed generalisation
Introduce grokking as an example where training accuracy saturates long before the internal representation and generalisation behaviour settle. Use it to reinforce the need to examine learning dynamics beyond a single headline metric.

#### 9. Measurement of representations
Bring together tools students have already seen:

- similarity and centred similarity;
- nearest-neighbour retrieval;
- linear probes;
- activation statistics;
- pairwise distances/cosines;
- ablations and interventions.

The purpose is to show that accuracy/loss alone can hide important representational changes.

### Key concepts
Scaling, compute, data/model trade-off, pretraining, conditional computation, mixture of experts, router, gating, target network, momentum encoder, representation collapse, anisotropy, centring, neural collapse, superposition, sparse feature, sparse autoencoder, grokking, representation geometry, retrieval metric.

### Conceptual role
This week establishes **information routing → representation geometry**. It asks what large networks learn internally and how architecture/scale can change the organisation of computation.

### Architecture-evolution connection
The StoryReasoning work supplies unusually concrete examples for this week: raw embedding cosines hiding a shared mean component, a trainable encoder collapsing toward the mean under a similarity loss, a frozen target encoder preventing that collapse, different heads competing through a shared representation, and gates/mixtures providing conditional computation on a small scale.

---

## Week 11 — Learning during inference: in-context learning, retrieval, adaptation, and test-time computation

### Central question
Where is the boundary between training and inference if a trained model can retrieve, adapt, reason over context, or optimise its behaviour at test time?

### Lecture-note scope

#### 1. Training-time learning versus inference-time adaptation
Start with the conventional picture: parameters are updated during training and frozen during inference. Then introduce systems that blur this boundary through context, memory, retrieval or test-time optimisation.

#### 2. In-context learning
Explain in-context learning as changing behaviour from examples/instructions in the prompt without updating the model's parameters. Distinguish:

- parameter learning;
- temporary information in the context window;
- external retrieval/memory;
- actual weight updates.

Discuss demonstrations, task specification through context and the limits of calling all prompt-conditioned behaviour "learning".

#### 3. Induction-style mechanisms and circuits
Give an accessible account of induction-style behaviour: attention can detect repeated patterns and continue them by copying/retrieving information from earlier context. Use this as a concrete mechanistic hypothesis for some forms of in-context learning, without claiming it explains all such behaviour.

#### 4. Retrieval-augmented models and external memory
Introduce retrieval-augmented generation (RAG) as a system-level architecture:

- encode/query;
- retrieve relevant external items;
- condition generation on retrieved information;
- separate stored knowledge from parametric knowledge;
- retrieval quality as an independent source of failure.

Connect to Week 9 retrieval and Week 10 representation geometry.

#### 5. Test-time training and adaptation
Introduce methods that update some parameters or state at inference time using the test input or an unsupervised objective. Contrast this with in-context learning, where weights remain unchanged.

Examples can include test-time normalization/adaptation, self-supervised adaptation and small learned adapters where appropriate.

#### 6. Test-time compute, search and verification
Explain that inference can itself be an iterative computational process:

- generating multiple candidate solutions;
- reranking or verification;
- self-consistency / sample-and-select patterns;
- search over possible outputs;
- allocating more computation to harder examples.

Connect this to Week 8's best-of-K generative evaluation and to the broader idea that one forward sample is not always the whole model/system.

#### 7. Final synthesis: what has been learned where?
Close the module by revisiting the full learning thread:

- data provide examples;
- the loss specifies what differences matter;
- optimisation changes parameters;
- architecture imposes inductive bias;
- hidden layers build representations;
- memory and attention route information;
- pretraining/scale shape representation geometry;
- inference-time context, retrieval and computation can produce further adaptation without conventional full-model retraining.

Students should be able to look at a modern system and ask where its knowledge, adaptation and computation actually live.

### Key concepts
Inference, in-context learning, context window, demonstrations, induction, circuit, retrieval-augmented generation, external memory, parametric knowledge, non-parametric memory, test-time training, adaptation, test-time compute, sampling, reranking, verification, search, self-consistency.

### Conceptual role
This week completes **representation geometry → learning during inference** and provides the final synthesis of the module.

### Architecture-evolution connection
The StoryReasoning work can provide two useful bridges: retrieval as an alternative output when direct generation is ill-posed, and the broader lesson that a system can combine frozen pretrained components, learned routing, external candidates and sampling rather than relying on one monolithic network to produce one deterministic answer.

---

## Cross-week architecture-evolution thread

The StoryReasoning architecture evolution contains many concepts that should appear in the module, but they are best distributed according to when students have the prerequisites:

| Architecture-evolution lesson | Best teaching home |
|---|---|
| Task formulation, prediction vs retrieval, trivial baselines | Week 1 |
| L1/MSE as specification; batches and SGD | Week 2 |
| ReLU bottlenecks, learned intermediate representations | Week 3 |
| Dying ReLU, normalization, representation collapse, multi-task competition, checkpoint selection, floors/ablations/shuffled controls | Week 4 |
| CNN encoder/decoder, autoencoder pretraining, transfer/frozen encoders, residual connections | Week 5 |
| Attention/gates as inspectable but not automatically faithful explanations; probes/interventions | Week 6 |
| GRU/LSTM, teacher forcing, conditional decoding, word dropout, condition ignoring | Week 7 |
| Autoencoders, VAE prior/posterior, KL, multimodal targets, sampling vs averaging, best-of-K, CLIP conditioning | Week 8 |
| Self-attention, cross-attention, content-dependent queries, entity tokens, early fusion, contrastive objectives, retrieval | Week 9 |
| Scaling, MoE/gating, anisotropy, centred similarity, collapse, frozen target encoders, superposition/sparse features | Week 10 |
| Retrieval/external memory, sample-and-select, adaptation and inference-time computation | Week 11 |

This distribution lets the same architecture case study recur at increasing levels of sophistication without requiring students to understand the full system early in the module.

---

## Lecture-note writing principles

The lecture notes generated from this map should follow these principles:

1. **Begin with a concrete problem or question.** Introduce machinery because it solves a limitation students can already see.
2. **Build from previous weeks.** Reuse the same notation and mental models where possible; for example, a convolutional layer and an attention projection are still learned transformations.
3. **Separate computation, objective and optimisation.** Students should be able to say what a model computes, what the loss rewards, and how parameters are updated.
4. **Use geometry and small examples before abstraction.** Decision boundaries, embedding directions, receptive fields and attention weights should be made visual/concrete before scaling up.
5. **Teach baselines and controls alongside models.** A result without a floor, heuristic baseline, ablation or control often cannot support the intended conclusion.
6. **Distinguish representation from use.** Information can be present in a hidden state without being causally used by the final prediction.
7. **Distinguish point prediction from distributional prediction.** When several outputs are plausible, averaging may be a property of the loss rather than evidence that the model has failed to learn anything.
8. **Use canonical architectures to teach ideas, not names.** AlexNet, ResNet, LSTM, transformers, VAEs and diffusion models should each earn their place by introducing a transferable concept.
9. **Keep implementation detail subordinate to transferable ideas.** APIs and exact hyperparameters belong mainly in labs unless they reveal a conceptual point.
10. **End each week by reconnecting to the learning thread.** The student should know what changed in their mental model and what question the next week will answer.

## Design principle for exercises and lecture integration

Each week should contain a small number of canonical experiments. Each experiment should begin with a concrete question, produce evidence that challenges or extends the student's current mental model, and connect explicitly to the larger learning thread documented in `learning-thread.md`.

The lecture should establish the concepts and the experiment should make the student observe a phenomenon that would be difficult to internalise from exposition alone. Expensive experiments should record reusable outputs so later investigations can analyse them without retraining unless a new run is genuinely required.
