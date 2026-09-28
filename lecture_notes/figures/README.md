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
