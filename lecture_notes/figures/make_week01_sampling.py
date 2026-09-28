"""Generate Figure 2.2 with synthetic, reproducible binary-class samples.

Install requirements in a virtual environment, then run this file from any directory.
Outputs are saved alongside this script. No external dataset is required.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch
import numpy as np

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)
p = 0.4
repetitions = 10000
blue, gold, ink = "#23486F", "#C18A2B", "#263442"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "text.color": ink, "axes.labelcolor": ink,
                     "xtick.color": ink, "ytick.color": ink,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
fig = plt.figure(figsize=(10.6, 4.8), facecolor="white")
left = fig.add_axes([0.015, 0.16, 0.49, 0.73])
right = fig.add_axes([0.62, 0.23, 0.36, 0.60])
left.set(xlim=(0, 1), ylim=(0, 1))
left.axis("off")
fig.text(0.025, 0.95, "(a) One process, different samples", weight="bold", fontsize=12)
fig.text(0.59, 0.95, "(b) Repeat sampling 10,000 times", weight="bold", fontsize=12)
left.text(0.235, 0.95, "Data-generating process / population", ha="center", fontsize=9)
left.text(0.235, 0.88, "Class A proportion: p = 0.40", ha="center", fontsize=9)
left.add_patch(Ellipse((0.23, 0.46), 0.44, 0.69, facecolor="#F0F4F7", edgecolor="#BDC9D3"))
# The cloud is a schematic of the process, with exactly 40% class A markers.
radius = np.sqrt(rng.uniform(size=150))
angle = rng.uniform(0, 2 * np.pi, 150)
cloud_labels = np.array([True] * 60 + [False] * 90)
rng.shuffle(cloud_labels)
xx = 0.23 + 0.20 * radius * np.cos(angle)
yy = 0.46 + 0.32 * radius * np.sin(angle)
for label, marker, color in [(True, "o", blue), (False, "^", gold)]:
    left.scatter(xx[cloud_labels == label], yy[cloud_labels == label],
                 s=14, marker=marker, color=color, alpha=0.85, linewidths=0)

# Each displayed sample is an independent draw from the same Bernoulli process.
for j, centre in enumerate([0.73, 0.45, 0.17]):
    labels = rng.random(20) < p
    left.annotate("", xy=(0.62, centre), xytext=(0.455, 0.46),
                  arrowprops={"arrowstyle": "->", "color": "#8496A5", "lw": 1.2})
    left.add_patch(FancyBboxPatch((0.635, centre - 0.07), 0.345, 0.155,
                   boxstyle="round,pad=0.01,rounding_size=0.015",
                   facecolor="#FAFBFC", edgecolor="#CBD4DB"))
    left.text(0.805, centre + 0.12,
              f"Sample {j + 1}: {labels.sum()}/20 = {labels.mean():.2f}",
              ha="center", fontsize=9)
    sx = 0.66 + np.tile(np.arange(10), 2) * 0.032
    sy = centre + 0.045 - np.repeat(np.arange(2), 10) * 0.07
    for label, marker, color in [(True, "o", blue), (False, "^", gold)]:
        left.scatter(sx[labels == label], sy[labels == label], s=19,
                     marker=marker, color=color, linewidths=0)
left.scatter([0.08], [-0.03], color=blue, s=22, clip_on=False)
left.text(0.11, -0.03, "Class A", va="center", fontsize=9)
left.scatter([0.30], [-0.03], color=gold, marker="^", s=22, clip_on=False)
left.text(0.33, -0.03, "Other class", va="center", fontsize=9)

# Equal-width bins and equal repetition counts make histogram heights comparable.
bins = np.arange(-0.025, 1.026, 0.05)
for n, color, label in [(20, gold, "Small samples: n = 20"),
                         (500, blue, "Large samples: n = 500")]:
    estimates = rng.binomial(n, p, size=repetitions) / n
    right.hist(estimates, bins=bins, weights=np.full(repetitions, 100 / repetitions),
               color=color, alpha=0.62, edgecolor="white", linewidth=0.5, label=label)
    print(f"n={n}: mean={estimates.mean():.4f}, SD={estimates.std():.4f}; "
          f"theoretical SD={np.sqrt(p * (1-p) / n):.4f}")
right.axvline(p, color=ink, linestyle=(0, (4, 3)), lw=1.4)
right.text(p + 0.018, 77, "Population p = 0.40", fontsize=9, va="top")
right.set(xlim=(0, 0.85), ylim=(0, 84), xlabel="Estimated class A proportion",
          ylabel="Repeated samples (%)")
right.set_xticks(np.arange(0, 0.81, 0.2))
right.spines[["top", "right"]].set_visible(False)
right.spines[["left", "bottom"]].set_color("#B9C4CE")
right.set_axisbelow(True)
right.grid(axis="y", color="#E4E9ED", lw=0.6)
right.legend(loc="upper right", bbox_to_anchor=(1.02, -0.21), frameon=False, fontsize=9)
fig.savefig(OUT / "week01_sampling.pdf", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(OUT / "week01_sampling.png", dpi=200)
plt.close(fig)
