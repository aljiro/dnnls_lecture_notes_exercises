# Python figures

Figure 2.2 is generated from a synthetic two-class process with class A probability
0.40. The seed is fixed; no external dataset is downloaded. The population cloud
is schematic, the three small samples are independent draws, and each histogram
uses 10,000 independent binomial samples. Both histograms use the same bin edges
and show the percentage of repeated samples in each bin.

From the repository root, install dependencies in a local environment and run:

```bash
python3 -m venv /tmp/dnnls-figure22-env
/tmp/dnnls-figure22-env/bin/pip install -r lecture_notes/figures/requirements.txt
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week01_sampling.py
```

This writes `week01_sampling.pdf` (vector artwork included by LaTeX) and
`week01_sampling.png` (preview) alongside the script. The requirements also
include PyMuPDF for inspecting the compiled lecture PDF.

Build the notes using the repository README's `latexmk` instructions. This figure
was checked with Python 3.13, Tectonic 0.15.0 and Biber 2.17, installed locally.
Tectonic's external bibliography runner does not accept `../references.bib`;
when using Tectonic, build a temporary copy of `lecture_notes/`, copy
`references.bib` into that copy, and change only the temporary preamble's
bibliography path to `references.bib`. Put the local Biber executable on `PATH`.
The repository's LaTeX sources retain the normal relative bibliography path.

## Figure 3.1: linear model and residuals

```bash
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week02_line_residuals.py
```

This writes `week02_line_residuals.pdf` and `week02_line_residuals.png`.
The synthetic observations and deliberately unfitted line are fixed. Four arrows
run from predictions to targets, with two positive and two negative residuals.
The slope triangle has a unit horizontal run. The two small panels change only
one parameter at a time and share the same axis limits and original line.

## Figure 3.2: loss surface and learning rates

```bash
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week02_loss_surface.py
```

This writes `week02_loss_surface.pdf` and `week02_loss_surface.png`. The data
contain 21 evenly spaced inputs in [-1, 2] with targets `y = x + 0.5`.
All three panels use the exact mean squared error, the same initial parameters
(-1.2, 2.3), eight full-batch gradient-descent updates, and equal axis scales.
Learning rates 0.04, 0.35 and 0.75 produce slow progress, convergence and
increasing oscillation respectively. The script checks the analytical gradient
against finite differences and verifies the stated loss behaviour. Contour
values and trajectories are calculated from the data rather than drawn by hand.

## Figure 2.4: supervised-learning skeleton

```bash
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week01_supervised_skeleton.py
```

This writes `week01_supervised_skeleton.pdf` (vector artwork) and a PNG preview.
The training panel routes inputs to the model and targets directly to the loss;
a parameter-update loop returns to the model. The inference panel keeps learned
parameters fixed. Dashed evaluation arrows compare held-out predictions and
targets without feeding back into the parameter-update loop.

## Figure 3.3: mini-batch gradient noise

```bash
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week02_gradient_noise.py
```

This writes `week02_gradient_noise.pdf` and a PNG preview. A fixed seed generates
400 noisy linear-regression examples. The left panel samples 600 gradient
estimates for each of B=1, 16 and 128 at one fixed parameter vector, using uniform
sampling with replacement. The right panel computes 100 updates with learning
rate 0.06 from the same start for full-batch, B=16 and B=1 training. This compares
update counts, not equal computation. All contours use the same dataset's MSE.
Checks cover the estimates' mean and variance ordering, decreasing full-batch
loss, and improvement of each trajectory over its initial loss.

## Chapter 4: from linear rules to neural networks

```bash
/tmp/dnnls-figure22-env/bin/python lecture_notes/figures/make_week03_figures.py
```

The single script generates vector PDFs and PNG previews for all four figures:

- **4.1** `week03_linear_separability`: fixed synthetic separable clusters and
  exact XOR corners. Candidate boundary accuracies are checked under either
  class orientation; axes have equal scale so the weight-vector normal is exact.
- **4.2** `week03_activations`: analytical step, sigmoid, tanh and ReLU curves
  and ordinary derivatives. Open markers distinguish undefined derivatives at
  zero; no arbitrary derivative convention is depicted as the mathematical value.
- **4.3** `week03_hidden_geometry`: 160 noisy two-moons examples, data seed 7,
  initialisation seed 42. A 2→8→2→1 tanh MLP trains for 1,200 full-batch Adam
  updates (learning rate 0.01, betas 0.9/0.999, epsilon 1e-8) with squared-error
  targets -1/+1. Both hidden layers use tanh; the output is linear. The final
  two-unit hidden activations are plotted without further projection or jitter.
  All manually calculated parameter gradients are checked against finite
  differences before training. The plotted network classifies all these training
  examples correctly; the illustrative affine least-squares baseline gets 87.5%.
  This is a representation demonstration, not a held-out performance claim.
- **4.4** `week03_computational_graph`: the chapter's exact scalar ReLU network,
  including all four parameters, input and target, with forward/backward arrows.

No image-generation service or new dependencies are needed. Re-running the
script regenerates all four figures and repeats the mathematical checks.
