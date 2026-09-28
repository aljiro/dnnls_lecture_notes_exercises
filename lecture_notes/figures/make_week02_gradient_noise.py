"""Figure 3.3: sampled gradients and noisy optimisation on one regression dataset.

Run with the local environment in README.md. Sampling is uniform with replacement;
all random seeds are fixed. The right panel compares updates, not equal compute.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
INK, BLUE, GREEN, GOLD = "#263442", "#23486F", "#2B795F", "#B77520"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
rng = np.random.default_rng(2026)
x = np.linspace(-1, 2, 400)
X = np.column_stack([x, np.ones_like(x)])
y = x + 0.5 + rng.normal(0, 0.9, len(x))
minimum = np.linalg.lstsq(X, y, rcond=None)[0]
reference = minimum + [-0.4, 0.4]
start = np.array([-1.0, 2.2])
rate, updates, repeats = 0.06, 100, 600


def loss(theta):
    return np.mean((X @ theta - y) ** 2)


def individual_gradients(theta):
    return 2 * (X @ theta - y)[:, None] * X


def trajectory(batch_size, seed):
    sampler = np.random.default_rng(seed)
    path = [start.copy()]
    for _ in range(updates):
        if batch_size == len(x):
            gradient = individual_gradients(path[-1]).mean(axis=0)
        else:
            ids = sampler.integers(len(x), size=batch_size)
            gradient = 2 * X[ids].T @ (X[ids] @ path[-1] - y[ids]) / batch_size
        path.append(path[-1] - rate * gradient)
    return np.array(path)


grads = individual_gradients(reference)
full_gradient = grads.mean(axis=0)
clouds = {}
for batch in [1, 16, 128]:
    sampler = np.random.default_rng(1000 + batch)
    clouds[batch] = grads[sampler.integers(len(x), size=(repeats, batch))].mean(axis=1)
    # A repeated batch mean has covariance Cov(g_i)/B for replacement sampling.
    standard_error = grads.std(axis=0) / np.sqrt(batch * repeats)
    assert np.all(np.abs(clouds[batch].mean(axis=0) - full_gradient) < 5 * standard_error)
    print(f'B={batch}: gradient spread (RMS distance from full gradient) = '
          f'{np.sqrt(np.mean(np.sum((clouds[batch] - full_gradient)**2, axis=1))):.4f}')
assert np.trace(np.cov(clouds[1].T)) > np.trace(np.cov(clouds[16].T)) > np.trace(np.cov(clouds[128].T))
paths = {batch: trajectory(batch, 3000 + batch) for batch in [400, 16, 1]}
for batch, path in paths.items():
    assert np.isfinite(path).all()
    assert loss(path[-1]) < loss(path[0])
    print(f'B={batch}: MSE {loss(path[0]):.4f} -> {loss(path[-1]):.4f}')
assert np.all(np.diff([loss(p) for p in paths[400]]) <= 1e-12)

fig, (left, right) = plt.subplots(1, 2, figsize=(10.1, 5.8))
fig.subplots_adjust(left=0.08, right=0.975, top=0.79, bottom=0.29, wspace=0.32)
fig.text(0.08, 0.955, "Batch size changes the noise in an update", fontsize=14, weight="bold")
left.set_title("(a) Gradient estimates at one fixed model", fontsize=11, weight="bold", pad=14)
right.set_title("(b) Training with the same learning rate", fontsize=11, weight="bold", pad=14)
for batch, color, marker, alpha in [(1, GOLD, "o", 0.28), (16, GREEN, "^", 0.5), (128, BLUE, "o", 0.65)]:
    points = clouds[batch]
    left.scatter(points[:, 0], points[:, 1], s=11, color=color, marker=marker,
                 alpha=alpha, linewidths=0, label=f"B = {batch}")
left.scatter(*full_gradient, marker="*", s=150, color=INK, edgecolors="white",
             linewidths=0.7, zorder=6, label="Full-data gradient")
left.axhline(0, color="#CAD3DB", lw=0.6, zorder=0)
left.axvline(0, color="#CAD3DB", lw=0.6, zorder=0)
left.set(xlabel=r"Gradient component $\partial\mathcal{L}/\partial w$",
         ylabel=r"Gradient component $\partial\mathcal{L}/\partial b$")
left.legend(loc="upper left", fontsize=9, frameon=True, framealpha=0.95,
            edgecolor="none", markerscale=0.9)

# Exact MSE contours of the same finite dataset.
combined = np.concatenate(list(paths.values()))
wlim = (combined[:, 0].min() - 0.18, combined[:, 0].max() + 0.22)
blim = (combined[:, 1].min() - 0.20, combined[:, 1].max() + 0.20)
W, B = np.meshgrid(np.linspace(*wlim, 220), np.linspace(*blim, 220))
Z = np.mean((W[..., None] * x + B[..., None] - y) ** 2, axis=-1)
right.contour(W, B, Z, levels=loss(minimum) + np.array([0.02, 0.08, 0.2, 0.5, 1, 2, 4]),
              colors="#BAC7D2", linewidths=0.7)
# Plot the noisiest path first so it does not obscure the smooth path.
for batch, color, label in [(1, GOLD, "Single-example SGD: B = 1"),
                            (16, GREEN, "Mini-batch: B = 16"),
                            (400, BLUE, "Full batch: B = 400")]:
    path = paths[batch]
    right.plot(path[:, 0], path[:, 1], color=color, lw=1.4, label=label, alpha=0.9)
    right.scatter(*path[-1], color=color, marker="s", s=22, edgecolors="white", linewidths=0.4, zorder=6)
right.scatter(*start, s=45, facecolors="white", edgecolors=INK, zorder=7)
right.annotate("Common start", xy=start, xytext=(start[0] + 0.35, start[1] + 0.32),
               fontsize=9, va="center", arrowprops={"arrowstyle": "-", "color": INK})
right.scatter(*minimum, marker="*", s=110, color=INK, edgecolors="white", linewidths=0.6, zorder=7)
right.set(xlim=wlim, ylim=blim, xlabel=r"Slope $w$", ylabel=r"Intercept $b$")
right.legend(loc="lower left", bbox_to_anchor=(-0.03, -0.40), fontsize=9, frameon=False)
for ax in [left, right]:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#AEBCC8")
    ax.tick_params(labelsize=9)
left.text(0, -0.29, "600 draws per batch size; uniform sampling\nwith replacement from the same 400 examples.",
          transform=left.transAxes, fontsize=9, linespacing=1.6)
fig.text(0.08, 0.025, r"Right: 100 updates each, $\eta=0.06$; work per update differs."
         "   ★ = minimum; ■ = final iterate.", fontsize=9)
fig.savefig(OUT / "week02_gradient_noise.pdf", metadata={"CreationDate": None, "ModDate": None})
fig.savefig(OUT / "week02_gradient_noise.png", dpi=200)
plt.close(fig)
