"""Reproduce Chapter 4's four figures with NumPy and Matplotlib.

Run in the local environment documented in README.md. No external data is used.
The geometry example trains a 2 -> 8 -> 2 -> 1 tanh MLP for 1,200 Adam updates
on fixed synthetic moons; it plots the actual final two-unit hidden layer.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
import numpy as np

OUT = Path(__file__).resolve().parent
BLUE, GOLD, GREEN, INK = '#23486F', '#B77520', '#2B795F', '#263442'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'text.color': INK, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK,
                     'pdf.fonttype': 42, 'ps.fonttype': 42})


def save(fig, name):
    fig.savefig(OUT / f'{name}.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(OUT / f'{name}.png', dpi=200)
    plt.close(fig)


def style(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('#ADBBC8')
    ax.tick_params(labelsize=9)


def classes(ax, X, y, size=28):
    for label, color, marker in [(0, BLUE, 'o'), (1, GOLD, 's')]:
        points = X[y == label]
        ax.scatter(*points.T, s=size, color=color, marker=marker,
                   edgecolors='white', linewidths=0.35, zorder=5)


def separability():
    rng = np.random.default_rng(11)
    X = np.r_[rng.normal([-.85, -.65], .23, (28, 2)),
              rng.normal([.85, .65], .23, (28, 2))]
    y = np.repeat([0, 1], 28)
    w = np.array([1., .7])
    assert np.all((X @ w > 0) == y)
    xor = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])
    labels = np.array([0, 1, 1, 0])
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.8))
    fig.subplots_adjust(left=.09, right=.97, top=.82, bottom=.25, wspace=.32)
    grid = np.linspace(-1.7, 1.7, 200)
    A, B = np.meshgrid(grid, grid)
    axes[0].contourf(A, B, A + .7 * B, levels=[-5, 0, 5], colors=[BLUE, GOLD], alpha=.06)
    classes(axes[0], X, y)
    axes[0].plot(grid, -grid / .7, color=INK, lw=1.6)
    axes[0].annotate('', xy=.75*w, xytext=(0, 0),
                     arrowprops={'arrowstyle': '-|>', 'lw': 2, 'color': GREEN})
    axes[0].text(.23, -.18, r'Normal $\mathbf{w}$', color=GREEN, fontsize=10)
    axes[0].text(-1.52, 1.39, r'$\mathbf{w}^{\mathsf{T}}\mathbf{x}+b=0$', fontsize=10,
                 bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 2})
    axes[0].set_title('(a) One line separates the classes', fontsize=12, pad=12, weight='bold')
    classes(axes[1], xor, labels, size=110)
    axes[1].axvline(0, color=GREEN, ls='--', lw=1.2)
    axes[1].axhline(0, color='#8A6B9B', ls=':', lw=1.6)
    axes[1].plot(grid, .8-grid, color='#737E86', ls='-.', lw=1.2)
    for k, (normal, bias) in enumerate([(np.array([1, 0]), 0), (np.array([0, 1]), 0), (np.ones(2), -.8)]):
        score = xor @ normal + bias
        correct = max(np.sum((score > 0) == labels), np.sum((score <= 0) == labels))
        assert correct < 4
        print(f'Figure 4.1 candidate {k+1}: best label orientation {correct}/4 correct')
    axes[1].text(.10, 1.40, 'A', color=GREEN, fontsize=10)
    axes[1].text(-1.54, .13, 'B', color='#8A6B9B', fontsize=10)
    axes[1].text(1.29, -.70, 'C', color='#737E86', fontsize=10)
    axes[1].set_title('(b) XOR: opposite corners share a class', fontsize=12, pad=12, weight='bold')
    for ax in axes:
        ax.set(xlim=(-1.7, 1.7), ylim=(-1.7, 1.7), xlabel=r'$x_1$', ylabel=r'$x_2$')
        ax.set_aspect('equal'); ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1]); style(ax)
    fig.legend(handles=[Line2D([], [], ls='', marker='o', color=BLUE, label='Class 0'),
                        Line2D([], [], ls='', marker='s', color=GOLD, label='Class 1')],
               loc='lower left', bbox_to_anchor=(.08, .02), ncol=2, frameon=False, fontsize=10)
    fig.text(.54, .105, 'Best side labels: A 2/4; B 2/4; C 3/4 correct.', fontsize=9)
    fig.text(.54, .057, 'No straight boundary separates all four corners.', fontsize=9)
    save(fig, 'week03_linear_separability')


def activations():
    z = np.linspace(-5, 5, 1001)
    sigmoid = 1 / (1 + np.exp(-z))
    tanh = np.tanh(z)
    fig, axes = plt.subplots(2, 4, figsize=(9.2, 4.8), sharex=True)
    fig.subplots_adjust(left=.07, right=.985, top=.82, bottom=.20, hspace=.37, wspace=.35)
    fig.text(.07, .95, 'Same pre-activation, different response and sensitivity', fontsize=13, weight='bold')
    titles = ['Step', 'Sigmoid', 'tanh', 'ReLU']
    for j, title in enumerate(titles):
        axes[0, j].set_title(title, fontsize=12, weight='bold')
        for ax in axes[:, j]:
            style(ax); ax.set_xlim(-5, 5); ax.axhline(0, color='#CAD3DB', lw=.6)
            ax.axvline(0, color='#CAD3DB', lw=.6); ax.set_xticks([-5, 0, 5])
        axes[1, j].set_xlabel(r'$z$')
    # Step is 0 at z=0 and 1 only for z>0; its ordinary derivative is undefined there.
    axes[0, 0].plot([-5, 0], [0, 0], color=BLUE, lw=2)
    axes[0, 0].plot([0, 5], [1, 1], color=BLUE, lw=2)
    axes[0, 0].scatter([0, 0], [0, 1], s=28, facecolors=[BLUE, 'white'], edgecolors=BLUE, zorder=5)
    axes[1, 0].plot([-5, 5], [0, 0], color=GREEN, lw=1.7, alpha=.7)
    axes[1, 0].scatter([0], [0], facecolors='white', edgecolors=GREEN, s=30, zorder=5)
    axes[0, 0].set_ylim(-.15, 1.2); axes[1, 0].set_ylim(-.15, 1.2)
    for j, values, derivative, threshold in [(1, sigmoid, sigmoid*(1-sigmoid), 3),
                                            (2, tanh, 1-tanh*tanh, 2)]:
        axes[0, j].plot(z, values, color=BLUE, lw=2)
        axes[1, j].plot(z, derivative, color=GREEN, lw=1.7, alpha=.7)
        for ax in axes[:, j]:
            ax.axvspan(-5, -threshold, color=GOLD, alpha=.09)
            ax.axvspan(threshold, 5, color=GOLD, alpha=.09)
        axes[1, j].set_ylim(-.03, .29 if j == 1 else 1.15)
    axes[0, 3].plot(z, np.maximum(z, 0), color=BLUE, lw=2)
    axes[1, 3].plot([-5, 0], [0, 0], color=GREEN, lw=1.7, alpha=.7)
    axes[1, 3].plot([0, 5], [1, 1], color=GREEN, lw=1.7, alpha=.7)
    axes[1, 3].scatter([0, 0], [0, 1], s=28, facecolors='white', edgecolors=GREEN, zorder=5)
    axes[1, 3].set_ylim(-.15, 1.2)
    axes[0, 0].set_ylabel(r'Activation $\phi(z)$')
    axes[1, 0].set_ylabel(r'Sensitivity $\phi\,\prime(z)$')
    fig.text(.07, .08, 'Open circles: excluded / undefined values at the switch or kink.', fontsize=9)
    fig.text(.07, .035, 'Shaded tails: saturation, where sigmoid and tanh have small derivatives.', fontsize=9)
    save(fig, 'week03_activations')


def train_geometry():
    rng = np.random.default_rng(7)
    t = np.linspace(0, np.pi, 80)
    X = np.r_[np.c_[np.cos(t), np.sin(t)], np.c_[1-np.cos(t), .5-np.sin(t)]]
    X += rng.normal(0, .025, X.shape)
    y = np.r_[np.full(80, -1.), np.ones(80)]
    rng = np.random.default_rng(42)
    ps = [rng.normal(0, .7, (2, 8)), np.zeros(8), rng.normal(0, .5, (8, 2)),
          np.zeros(2), rng.normal(0, .7, 2), np.zeros(1)]
    m = [np.zeros_like(p) for p in ps]; q = [np.zeros_like(p) for p in ps]
    for step in range(1, 1201):
        W1, b1, W2, b2, v, c = ps
        A = np.tanh(X@W1+b1); H = np.tanh(A@W2+b2); s = H@v+c
        ds = 2*(s-y)/len(y)
        dz2 = ds[:, None]*v*(1-H**2); dz1 = (dz2@W2.T)*(1-A**2)
        gs = [X.T@dz1, dz1.sum(0), A.T@dz2, dz2.sum(0), H.T@ds, np.array([ds.sum()])]
        if step == 1:
            # Check every manually implemented gradient once against finite differences.
            def objective():
                a = np.tanh(X@ps[0]+ps[1]); h = np.tanh(a@ps[2]+ps[3])
                return np.mean((h@ps[4]+ps[5]-y)**2)
            for p, grad in zip(ps, gs):
                for index in np.ndindex(p.shape):
                    old = p[index]; eps = 1e-6
                    p[index] = old+eps; high = objective()
                    p[index] = old-eps; low = objective(); p[index] = old
                    np.testing.assert_allclose(grad[index], (high-low)/(2*eps), atol=1e-8, rtol=1e-5)
        for j, (p, g) in enumerate(zip(ps, gs)):
            m[j] = .9*m[j]+.1*g; q[j] = .999*q[j]+.001*g*g
            p -= .01*(m[j]/(1-.9**step))/(np.sqrt(q[j]/(1-.999**step))+1e-8)
    W1, b1, W2, b2, v, c = ps
    H = np.tanh(np.tanh(X@W1+b1)@W2+b2)
    accuracy = np.mean((H@v+c > 0) == (y > 0))
    assert accuracy == 1
    print(f'Figure 4.3: 160 paired examples; MLP accuracy {accuracy:.1%}; MSE {np.mean((H@v+c-y)**2):.6f}')
    return X, y, H, v, c


def geometry():
    X, y, H, v, c = train_geometry()
    fig = plt.figure(figsize=(9.2, 4.9))
    left = fig.add_axes([.075, .26, .30, .53])
    right = fig.add_axes([.67, .26, .30, .53])
    middle = fig.add_axes([.40, .28, .21, .46]); middle.axis('off')
    fig.text(.075, .94, 'The examples stay the same; their coordinates change', fontsize=13, weight='bold')
    left.set_title('Input space', fontsize=12, weight='bold', pad=12)
    right.set_title('Final hidden space', fontsize=12, weight='bold', pad=12)
    classes(left, X, (y > 0).astype(int), size=16)
    classes(right, H, (y > 0).astype(int), size=16)
    # A concrete least-squares affine baseline illustrates its remaining mistakes.
    beta = np.linalg.lstsq(np.c_[X, np.ones(len(X))], y, rcond=None)[0]
    xx = np.linspace(-1.15, 2.15, 200)
    left.plot(xx, -(beta[0]*xx+beta[2])/beta[1], color='#7E8E9C', ls='--', lw=1)
    linear_accuracy = np.mean((np.c_[X, np.ones(len(X))]@beta > 0) == (y > 0))
    print(f'Figure 4.3 illustrative affine baseline: {linear_accuracy:.1%} training accuracy')
    left.set(xlim=(-1.15, 2.15), ylim=(-.65, 1.16), xlabel=r'$x_1$', ylabel=r'$x_2$')
    xx = np.linspace(H[:, 0].min()-.12, H[:, 0].max()+.12, 200)
    right.plot(xx, -(v[0]*xx+c[0])/v[1], color=INK, lw=1.5)
    right.set(xlim=(xx.min(), xx.max()), ylim=(H[:, 1].min()-.12, H[:, 1].max()+.12),
              xlabel=r'$h_1$', ylabel='')
    right.text(-.08, 1.01, r'$h_2$', transform=right.transAxes, fontsize=11)
    # Letter tags track exactly the same point IDs, not new or invented points.
    for letter, idx, offset in [('A', 8, (5, 7)), ('B', 58, (5, 7)),
                                ('C', 90, (5, -13)), ('D', 140, (5, -13))]:
        for ax, data in [(left, X), (right, H)]:
            ax.scatter(*data[idx], s=40, facecolors='none', edgecolors=INK, linewidths=.9, zorder=7)
            ax.annotate(letter, xy=data[idx], xytext=offset, textcoords='offset points', fontsize=9,
                        weight='bold', zorder=8, bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': .5})
    middle.add_patch(FancyBboxPatch((.08, .30), .84, .40,
                     boxstyle='round,pad=.015', facecolor='#F3F7FB', edgecolor=BLUE))
    middle.text(.5, .59, 'Nonlinear MLP', ha='center', weight='bold', color=BLUE, fontsize=11)
    middle.text(.5, .46, '2 → 8 → 2 units', ha='center', fontsize=10)
    middle.annotate('', xy=(1., .50), xytext=(.95, .50), arrowprops={'arrowstyle': '->', 'color': BLUE})
    middle.annotate('', xy=(.06, .50), xytext=(0., .50), arrowprops={'arrowstyle': '->', 'color': BLUE})
    middle.text(.5, .14, 'Trained tanh layers', ha='center', fontsize=10)
    middle.text(.5, .03, 'Output remains linear', ha='center', fontsize=10)
    for ax in [left, right]: style(ax)
    fig.text(.075, .14, 'Dashed: one fitted straight separator.', fontsize=9)
    fig.text(.67, .14, r'Output boundary: $\mathbf{v}^{\mathsf{T}}\mathbf{h}+c=0$', fontsize=9)
    fig.text(.075, .06, 'Same 160 examples in both spaces. A–D track individual points; colour and shape identify class.', fontsize=10)
    save(fig, 'week03_hidden_geometry')


def computational_graph():
    fig, ax = plt.subplots(figsize=(9.8, 4.6))
    fig.subplots_adjust(left=.025, right=.975, bottom=.025, top=.975)
    ax.set(xlim=(0, 11), ylim=(0, 5)); ax.axis('off')
    ax.text(.1, 4.75, 'One scalar network, two directions of computation', fontsize=14, weight='bold')
    positions = [1.05, 3.65, 6.25, 8.85]
    titles = ['Weighted sum', 'ReLU', 'Output', 'Squared error']
    equations = [r'$z_1=w_1x+b_1$', r'$h=\max(0,z_1)$', r'$\hat{y}=w_2h+b_2$', r'$\mathcal{L}=(\hat{y}-y)^2$']
    def arrow(a, b, color=BLUE):
        ax.annotate('', xy=b, xytext=a, arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': 1.6})
    for x, title, equation in zip(positions, titles, equations):
        ax.add_patch(FancyBboxPatch((x, 2.3), 1.95, 1.0, boxstyle='round,pad=.02,rounding_size=.08',
                     facecolor='#F3F7FB', edgecolor=BLUE, lw=1.3))
        ax.text(x+.975, 2.99, title, ha='center', fontsize=11, weight='bold', color=BLUE)
        ax.text(x+.975, 2.62, equation, ha='center', fontsize=12)
    ax.text(.30, 2.78, r'$x$', fontsize=15, ha='center'); arrow((.50, 2.8), (1.02, 2.8))
    for a, b, label in zip(positions[:-1], positions[1:], [r'$z_1$', r'$h$', r'$\hat{y}$']):
        arrow((a+1.98, 2.8), (b-.03, 2.8)); ax.text((a+1.95+b)/2, 2.99, label, ha='center', fontsize=11)
    for x, labels in [(positions[0], [r'$w_1$', r'$b_1$']), (positions[2], [r'$w_2$', r'$b_2$'])]:
        for offset, label in zip([.48, 1.47], labels):
            ax.text(x+offset, 3.97, label, fontsize=13, ha='center', color=GOLD)
            arrow((x+offset, 3.83), (x+offset, 3.33), GOLD)
    ax.text(9.825, 3.97, r'Target $y$', fontsize=12, ha='center')
    arrow((9.825, 3.83), (9.825, 3.33), INK)
    arrow((1.05, 1.7), (10.8, 1.7), BLUE)
    ax.text(5.8, 1.84, 'Forward: values', ha='center', color=BLUE, fontsize=12, weight='bold')
    arrow((10.8, .95), (1.05, .95), GREEN)
    ax.text(5.8, 1.10, 'Backward: sensitivities', ha='center', color=GREEN, fontsize=12, weight='bold')
    ax.text(.1, .26, 'Backpropagation computes gradients. A separate optimiser step changes the parameters.', fontsize=11)
    save(fig, 'week03_computational_graph')


if __name__ == '__main__':
    separability()
    activations()
    geometry()
    computational_graph()
