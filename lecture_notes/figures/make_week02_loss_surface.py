"""Figure 3.2: exact MSE contours and full-batch gradient-descent trajectories.

Synthetic observations: 21 equally spaced x values in [-1, 2], y = x + 0.5.
All panels share the dataset, initial parameters, axes, contours and update count.
Run in the local environment documented in README.md; outputs accompany the script.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

OUT = Path(__file__).resolve().parent
INK = "#263442"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
x = np.linspace(-1, 2, 21)
y = x + 0.5
X = np.column_stack([x, np.ones_like(x)])
start = np.array([-1.2, 2.3])
minimum = np.linalg.lstsq(X, y, rcond=None)[0]
updates = 8


def loss(theta):
    return np.mean((X @ theta - y) ** 2)


def gradient(theta):
    return 2 * X.T @ (X @ theta - y) / len(x)


def trajectory(rate):
    points = [start.copy()]
    for _ in range(updates):
        points.append(points[-1] - rate * gradient(points[-1]))
    return np.array(points)


# Validate the analytical gradient and the behaviours stated on the panels.
eps = 1e-6
numerical = np.array([(loss(start + eps * e) - loss(start - eps * e)) / (2 * eps)
                      for e in np.eye(2)])
np.testing.assert_allclose(gradient(start), numerical, rtol=1e-8)
np.testing.assert_allclose(minimum, [1, 0.5], atol=1e-12)
small, sensible, excessive = [trajectory(rate) for rate in (0.04, 0.35, 0.75)]
assert np.all(np.diff([loss(p) for p in sensible]) < 0)
assert loss(sensible[-1]) < loss(small[-1]) < loss(start) < loss(excessive[-1])
assert np.all(np.diff([loss(p) for p in excessive[2:]]) > 0)

coords = np.linspace(-2, 3.1, 350)
W, B = np.meshgrid(coords, coords)
Z = np.mean((W[..., None] * x + B[..., None] - y) ** 2, axis=-1)
levels = [0.03, 0.1, 0.3, 1, 3, 6, 12, 24]
fig, axes = plt.subplots(1, 3, figsize=(10.2, 5.3))
fig.subplots_adjust(left=0.065, right=0.99, bottom=0.30, top=0.78, wspace=0.16)
fig.text(0.065, 0.955, "Same loss surface, different learning rates", fontsize=14, weight="bold")
fig.text(0.065, 0.886,
         r"$\mathcal{L}(w,b)=\frac{1}{n}\sum_i(wx_i+b-y_i)^2$"
         "     |     Same start and 8 updates in every panel", fontsize=11)

for ax, rate, path, color, title, outcome in zip(
    axes, [0.04, 0.35, 0.75], [small, sensible, excessive],
    ["#B77520", "#2B795F", "#B54549"], ["Small", "Sensible", "Excessive"],
    ["Slow progress", "Approaches the minimum", "Overshoots, then diverges"],
):
    ax.contourf(W, B, Z, levels=[0, *levels, 60], cmap="Blues", alpha=0.10)
    contours = ax.contour(W, B, Z, levels=levels, colors="#9EAFC0", linewidths=0.65)
    # Label only the outer contours to keep the trajectory near the minimum legible.
    ax.clabel(contours, levels=[1, 3, 6, 12, 24], fontsize=7, fmt="%g", inline=True)
    ax.plot(path[:, 0], path[:, 1], color=color, lw=1.4, zorder=3)
    for a, b in zip(path[:-1], path[1:]):
        ax.annotate("", xy=b, xytext=a,
                    arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2,
                                "mutation_scale": 9, "shrinkA": 0, "shrinkB": 0}, zorder=4)
    ax.scatter(path[1:, 0], path[1:, 1], color=color, s=10, zorder=5)
    ax.scatter(*minimum, marker="*", s=110, color=INK, edgecolors="white", linewidths=0.5, zorder=6)
    ax.scatter(*start, s=38, facecolors="white", edgecolors=INK, linewidths=1.4, zorder=7)
    ax.scatter(*path[-1], s=40, marker="s", facecolors=color, edgecolors="white", linewidths=0.6, zorder=7)
    ax.set(xlim=(-2, 3.1), ylim=(-2, 3.1), xlabel=r"Slope $w$")
    ax.set_aspect("equal")  # Preserve perpendicularity of gradients and contours visually.
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.tick_params(labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9EAFC0")
    ax.set_title(title + rf": $\eta={rate:g}$", fontsize=12, pad=12, weight="bold")
    ax.text(0.5, -0.26, outcome, transform=ax.transAxes, ha="center", fontsize=10, color=color)
    ax.text(0.5, -0.36, f"MSE: {loss(start):.2f} → {loss(path[-1]):.3f}",
            transform=ax.transAxes, ha="center", fontsize=9)
    print(f"{title}: eta={rate:g}; MSE={loss(start):.6f} -> {loss(path[-1]):.6f}")
axes[0].set_ylabel(r"Intercept $b$")
# At the start, the gradient points opposite to the first descent update.
g = gradient(start)
end = start + 0.8 * g / np.linalg.norm(g)
axes[1].annotate("", xy=end, xytext=start,
                 arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.5}, zorder=8)
axes[1].text(-1.86, 2.88, r"$\nabla\mathcal{L}$: uphill", fontsize=9)
fig.legend(handles=[
    Line2D([], [], marker="o", color="none", markeredgecolor=INK, markerfacecolor="white", label="Common start"),
    Line2D([], [], marker="*", color="none", markerfacecolor=INK, markersize=10, label="Minimum"),
    Line2D([], [], marker="s", color="none", markerfacecolor=INK, label="After 8 updates"),
], loc="lower center", bbox_to_anchor=(0.46, 0.0), ncol=3, frameon=False, fontsize=10)
fig.text(0.99, 0.038, "Contour labels: MSE", ha="right", fontsize=9, color="#596B7C")
fig.savefig(OUT / "week02_loss_surface.pdf", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(OUT / "week02_loss_surface.png", dpi=200)
plt.close(fig)
