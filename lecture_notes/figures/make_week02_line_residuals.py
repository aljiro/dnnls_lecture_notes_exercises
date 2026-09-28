"""Generate Figure 3.1: a linear model, signed residuals and parameter changes.

Run with the local environment described in README.md. All data are synthetic;
the line is deliberately chosen rather than fitted. Outputs accompany this file.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
BLUE, GREEN, GOLD, INK = "#23486F", "#2B795F", "#B77520", "#263442"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
w, b = 0.45, 2.0
x = np.array([0.5, 1.0, 1.5, 2.1, 2.7, 3.1, 3.5, 4.0, 4.5, 4.9])
y = np.array([0.8, 1.45, 1.5, 2.85, 3.75, 4.2, 5.0, 5.55, 6.3, 6.7])
selected = [0, 2, 6, 8]
residuals = y - (w * x + b)
assert (residuals[selected] > 0).sum() == 2
assert (residuals[selected] < 0).sum() == 2

fig = plt.figure(figsize=(9.2, 5.0), facecolor="white")
ax = fig.add_axes([0.08, 0.17, 0.57, 0.69])
fig.text(0.08, 0.94, "Predictions and signed residuals", weight="bold", fontsize=13)
fig.text(0.08, 0.885, r"Chosen model: $\hat{y}=wx+b$, with $w=0.45$, $b=2$", fontsize=11)
xx = np.linspace(0, 5.1, 200)
ax.plot(xx, w * xx + b, color=BLUE, lw=2.2, zorder=2)
ax.scatter(x, y, s=31, color=INK, zorder=4, label=r"Observed target $y_i$")
for i in selected:
    prediction = w * x[i] + b
    positive = residuals[i] > 0
    color = GREEN if positive else GOLD
    ax.scatter([x[i]], [prediction], s=36, facecolors="white", edgecolors=BLUE,
               linewidths=1.3, zorder=5)
    ax.annotate("", xy=(x[i], y[i]), xytext=(x[i], prediction),
                arrowprops={"arrowstyle": "->", "color": color, "lw": 1.8,
                            "shrinkA": 4, "shrinkB": 4}, zorder=3)
    ax.text(x[i] + 0.10, (y[i] + prediction) / 2,
            r"$r_i>0$" if positive else r"$r_i<0$", color=color, fontsize=10,
            va="center")

# The intercept is the prediction at x=0; a unit run makes the rise equal to w.
ax.scatter([0], [b], color=BLUE, s=32, zorder=5)
ax.annotate(r"Intercept $b=2$", xy=(0, b), xytext=(0.2, 3.6),
            color=BLUE, fontsize=10,
            arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.0})
start, end = 2.0, 3.0
base = w * start + b
ax.plot([start, end, end], [base, base, w * end + b], color=BLUE,
        linestyle="--", lw=1.2)
ax.text(2.5, base - 0.18, r"run $=1$", ha="center", va="top", fontsize=10, color=BLUE)
ax.text(3.08, base + w / 2, r"rise $=w$", va="center", fontsize=10, color=BLUE)
ax.set(xlim=(-0.15, 5.25), ylim=(0, 7.4), xlabel=r"Input $x$", ylabel=r"Target / prediction $y$")
ax.set_xticks(np.arange(0, 6))
ax.set_yticks(np.arange(0, 8, 2))
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color("#B9C4CE")
ax.grid(color="#E5E9ED", lw=0.6)
ax.set_axisbelow(True)
ax.scatter([], [], s=36, facecolors="white", edgecolors=BLUE,
           label=r"Prediction $\hat{y}_i$")
ax.legend(loc="upper left", frameon=False, fontsize=10)
fig.text(0.08, 0.035, r"Residual: $r_i=y_i-\hat{y}_i$  (arrow points from prediction to target)", fontsize=10)

# Same axis limits and baseline in both insets isolate each parameter's effect.
for rect, title, new_w, new_b, note in [
    ([0.76, 0.59, 0.22, 0.25], r"Increase $w$; fix $b$", 1.05, b, "Rotate about the intercept"),
    ([0.76, 0.20, 0.22, 0.25], r"Increase $b$; fix $w$", w, 3.4, "Shift upward; same slope"),
]:
    inset = fig.add_axes(rect)
    inset.plot(xx, w * xx + b, color=BLUE, lw=1.6, linestyle="--")
    inset.plot(xx, new_w * xx + new_b, color=GREEN, lw=2)
    inset.scatter([0], [b], color=BLUE, s=18, zorder=3)
    at = 3.5
    inset.annotate("", xy=(at, new_w * at + new_b), xytext=(at, w * at + b),
                   arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.1})
    inset.set(xlim=(-0.15, 5.25), ylim=(0, 7.4))
    inset.set_xticks([0, 5])
    inset.set_yticks([0, 6])
    inset.tick_params(labelsize=9)
    inset.spines[["top", "right"]].set_visible(False)
    inset.spines[["left", "bottom"]].set_color("#B9C4CE")
    inset.set_title(title, fontsize=11, weight="bold", pad=10)
    inset.text(0.5, -0.29, note, transform=inset.transAxes, ha="center", fontsize=9)
fig.text(0.755, 0.04, "Dashed: original   Solid: changed", fontsize=9)
fig.savefig(OUT / "week02_line_residuals.pdf", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(OUT / "week02_line_residuals.png", dpi=200)
plt.close(fig)
print("Highlighted residuals:", residuals[selected])
