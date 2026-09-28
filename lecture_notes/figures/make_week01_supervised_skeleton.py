"""Draw Figure 2.4 as a vector diagram using Matplotlib.

Run in the local environment described in README.md. No data or model is needed.
PDF and PNG outputs are written alongside this script.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as MplPath

OUT = Path(__file__).resolve().parent
BLUE, GREEN, GOLD, INK = "#23486F", "#2B795F", "#A87520", "#263442"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "text.color": INK, "pdf.fonttype": 42, "ps.fonttype": 42})
fig, ax = plt.subplots(figsize=(10.8, 7.1))
fig.subplots_adjust(left=0.015, right=0.985, bottom=0.02, top=0.98)
ax.set(xlim=(0, 10.8), ylim=(0, 7.7))
ax.axis("off")


def panel(y, h, color, fill):
    ax.add_patch(FancyBboxPatch((0.08, y), 10.64, h,
                 boxstyle="round,pad=0.015,rounding_size=0.15",
                 facecolor=fill, edgecolor=color, linewidth=0.8, alpha=0.85))


def box(x, y, title, detail, color=BLUE, width=2.05, height=0.95):
    ax.add_patch(FancyBboxPatch((x, y), width, height,
                 boxstyle="round,pad=0.015,rounding_size=0.09",
                 facecolor="white", edgecolor=color, linewidth=1.4, zorder=3))
    ax.text(x + width / 2, y + height * 0.67, title,
            ha="center", va="center", fontsize=12, weight="bold", color=color)
    ax.text(x + width / 2, y + height * 0.28, detail,
            ha="center", va="center", fontsize=12)


def arrow(points, color=BLUE, dashed=False):
    path = MplPath(points, [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1))
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=14,
                 color=color, linewidth=1.6, linestyle="--" if dashed else "-", zorder=2))


panel(3.62, 3.99, BLUE, "#F3F7FB")
ax.text(0.32, 7.23, "TRAINING", color=BLUE, weight="bold", fontsize=14)
ax.text(3.0, 7.23, "Use examples to change the model's parameters", fontsize=12)
xs = [0.35, 3.0, 5.65, 8.30]
y = 5.55
box(xs[0], y, "Training dataset", r"$(x_i, y_i)$")
box(xs[1], y, "Model", r"$f_\theta$")
box(xs[2], y, "Prediction", r"$\hat{y}_i=f_\theta(x_i)$")
box(xs[3], y, "Training loss", r"$\ell(\hat{y}_i,y_i)$")
for left, right in zip(xs[:-1], xs[1:]):
    arrow([(left + 2.08, y + 0.475), (right - 0.04, y + 0.475)])
ax.text(2.69, 6.23, r"$x_i$", ha="center", color=BLUE)
# Targets bypass the model and enter the loss directly.
arrow([(1.375, 6.52), (1.375, 6.88), (9.325, 6.88), (9.325, 6.52)])
ax.text(5.3, 6.94, r"Targets $y_i$", ha="center", fontsize=11,
        bbox={"facecolor": "#F3F7FB", "edgecolor": "none", "pad": 1})
box(8.3, 3.99, "Parameter update", r"Change $\theta$", color=GOLD)
arrow([(9.325, 5.52), (9.325, 4.97)], GOLD)
ax.text(9.08, 5.23, "Combine errors", ha="right", va="center", fontsize=11, color=GOLD)
arrow([(8.26, 4.465), (4.025, 4.465), (4.025, 5.52)], GOLD)
ax.text(5.87, 4.62, r"Updated parameters $\theta$", ha="center", fontsize=11, color=GOLD)
ax.text(0.35, 3.90, "Repeat: predict → measure error → update", fontsize=11, color=BLUE)

panel(0.13, 3.17, GREEN, "#F1F7F4")
ax.text(0.32, 2.94, "INFERENCE", color=GREEN, weight="bold", fontsize=14)
ax.text(3.0, 2.94, "Apply the learned rule; keep parameters fixed", fontsize=12)
y = 1.08
box(xs[0], y, "New input", r"$x$", color=GREEN)
box(xs[1], y, "Trained model", r"$f_{\theta^*}$", color=GREEN)
box(xs[2], y, "Prediction", r"$\hat{y}=f_{\theta^*}(x)$", color=GREEN)
for left, right in zip(xs[:2], xs[1:3]):
    arrow([(left + 2.08, y + 0.475), (right - 0.04, y + 0.475)], GREEN)
box(xs[3], y, "Evaluation", r"Metric on $(\hat{y},y)$", color=INK)
arrow([(7.73, y + 0.475), (8.26, y + 0.475)], INK, dashed=True)
ax.text(9.325, 2.53, r"Held-out targets $y$", ha="center", fontsize=11)
arrow([(9.325, 2.32), (9.325, 2.07)], INK, dashed=True)
ax.text(0.35, 0.55, "For evaluation, use held-out inputs and compare with their targets.", fontsize=11)
ax.text(0.35, 0.28, "Evaluation measures performance; it does not update the model.", fontsize=11, color=GREEN)

fig.savefig(OUT / "week01_supervised_skeleton.pdf", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(OUT / "week01_supervised_skeleton.png", dpi=200)
plt.close(fig)
