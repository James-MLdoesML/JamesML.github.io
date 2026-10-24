#!/usr/bin/env python3
"""Reproduce the primer's phase-transition and step-size diagrams.

Run: python generate_phase_diagrams.py --output-dir figures
Use --quick for a lower-resolution smoke test. See README for assumptions.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from learning_dynamics import sweep, gamma_star

BLUE, ORANGE, GREEN, GREY = "#2977cc", "#ed9d00", "#18a880", "#d7d9dc"


def positive_learned_branch(gammas, N=3):
    """Larger positive root, including the saddle-node; NaN past its end."""
    gs = np.asarray(gammas)
    star = gamma_star(N)
    lo = np.full(gs.shape, ((N-2)/(2*N-2))**(1/N))
    hi = np.ones(gs.shape)
    for _ in range(70):
        mid = (lo+hi)/2
        # h decreases on the upper branch.
        above = mid**(N-2)*(1-mid**N) > 2*gs
        lo = np.where(above, mid, lo)
        hi = np.where(above, hi, mid)
    return np.where(gs <= star, ((lo+hi)/2)**N, np.nan)


def transition_figure(output_dir, quick=False):
    gammas = np.linspace(0, 0.8, 41 if quick else 81)
    steps = 12000 if quick else 40000
    two = sweep(gammas, N=2, init=0.1, steps=steps)
    three = sweep(gammas, N=3, init=1.0, steps=steps)
    cold = sweep(gammas, N=3, init=0.3, steps=steps)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True, layout="constrained")
    ax = axes[0]
    ax.plot(gammas, np.maximum(1-2*gammas, 0), "k--", label="Predicted optimum")
    ax.plot(gammas, two["final_output"], ".", color=BLUE, ms=4, label="Gradient descent, s₀ = 0.1")
    ax.axvline(0.5, color="0.5", ls=":", lw=1)
    ax.set_title("B2 · Two weights: continuous transition")
    ax.set_ylabel("Final output p")
    ax = axes[1]
    dense = np.linspace(0, gamma_star(3), 500)
    ax.plot(dense, positive_learned_branch(dense), "k--", label="Predicted learned branch")
    ax.plot(gammas, three["final_output"], ".", color=BLUE, ms=4, label="Start s₀ = 1")
    ax.plot(gammas, cold["final_output"], ".", color=ORANGE, ms=4, label="Start s₀ = 0.3")
    ax.axvline(gamma_star(3), color="0.5", ls=":", lw=1, label=r"$\gamma^* \approx 0.2362$")
    ax.set_title("D2 · Three weights: discontinuous transition")
    for ax in axes:
        ax.set(xlabel=r"Weight decay $\gamma$", xlim=(0, 0.8), ylim=(-0.03, 1.05))
        ax.grid(alpha=0.18)
        ax.legend(fontsize=8, loc="upper right")
    fig.suptitle("How weight decay changes the learned output", fontsize=15)
    fig.supxlabel(f"Independent full-batch runs · η = 0.01 · {steps:,} updates per point", fontsize=9)
    for ext in ("png", "svg"):
        fig.savefig(output_dir/f"phase-transitions.{ext}", dpi=180)
    plt.close(fig)
    np.savez_compressed(output_dir/"phase-transitions-data.npz", gamma=gammas,
                        N2=two["final_output"], N3_high=three["final_output"],
                        N3_cold=cold["final_output"])
    return dict(transition_steps=steps, transition_points=len(gammas))


def stability_figure(output_dir, quick=False):
    """Actual 2-D simultaneous GD, NOT artificially constrained to a=b."""
    # A spacing of 0.01 is enough to show the phase regions clearly.
    gammas = np.linspace(0, 0.8, 41 if quick else 81)
    etas = np.linspace(0.02, 1.6, 81 if quick else 181)
    G, E = np.meshgrid(gammas, etas)
    a, b = np.full(G.shape, 0.1), np.full(G.shape, 0.11)
    alive = np.ones(G.shape, bool)
    steps = 3000 if quick else 12000
    tail = 300
    amin, amax = np.full(G.shape, np.inf), np.full(G.shape, -np.inf)
    bmin, bmax = amin.copy(), amax.copy()
    with np.errstate(over="ignore", invalid="ignore"):
        for k in range(steps):
            residual = a*b-1
            an = a-E*(residual*b+2*G*a)
            bn = b-E*(residual*a+2*G*b)
            alive &= np.isfinite(an) & np.isfinite(bn) & (np.maximum(abs(an), abs(bn)) <= 1e6)
            a, b = np.where(alive, an, 0), np.where(alive, bn, 0)
            if k >= steps-tail:
                amin, amax = np.minimum(amin, a), np.maximum(amax, a)
                bmin, bmax = np.minimum(bmin, b), np.maximum(bmax, b)
    residual = a*b-1
    grad = np.hypot(residual*b+2*G*a, residual*a+2*G*b)
    settled = alive & (np.maximum(amax-amin, bmax-bmin) < 1e-5) & (grad < 1e-5)
    # 0 learned; 1 bounded/unsettled; 2 collapsed; 3 diverged.
    labels = np.ones(G.shape, dtype=np.uint8)
    labels[settled & (a*b > 1e-4)] = 0
    labels[settled & (np.hypot(a, b) < 1e-4)] = 2
    labels[~alive] = 3
    fig, ax = plt.subplots(figsize=(10, 6.7), layout="constrained")
    ax.pcolormesh(gammas, etas, labels, cmap=ListedColormap([BLUE, ORANGE, GREEN, GREY]),
                  vmin=-0.5, vmax=3.5, shading="nearest", rasterized=True)
    x1 = np.linspace(0, 0.5, 600, endpoint=False)
    sharpness1 = np.maximum(2-4*x1, 4*x1)
    ax.plot(x1, 2/sharpness1, "k--", lw=1.6)
    x2 = np.linspace(0.5, 0.8, 300)
    ax.plot(x2, 2/(2*x2+1), "k--", lw=1.6, label=r"Local stability guide: $\eta=2/\lambda_{\max}$")
    ax.axvline(0.5, color="k", ls=":", lw=1.4, label=r"Output threshold: $\gamma=1/2$")
    ax.set(xlabel=r"Weight decay $\gamma$", ylabel=r"Step size $\eta$",
           xlim=(0, 0.8), ylim=(0, 1.6), title=r"Learning $y=x$ with $f(x)=abx$: full-batch gradient descent")
    handles = [Patch(color=c, label=l) for c,l in zip(
        [BLUE, ORANGE, GREEN, GREY],
        ["Learned stationary state", "Bounded, not settled within budget", "Collapsed to zero", "Diverged (numerical cutoff)"])]
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles+lines, loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncols=2, fontsize=9, frameon=False)
    fig.suptitle("Colours: simulation · dashed curve: local stability prediction", fontsize=11)
    fig.supxlabel(f"Initial weights (0.10, 0.11) · {steps:,} updates · orange can include long transients", fontsize=9)
    for ext in ("png", "svg"):
        fig.savefig(output_dir/f"step-size-phase-diagram-finite-budget.{ext}", dpi=180)
    plt.close(fig)

    # Main illustration: draw the analytic stability regions directly.
    # Keep the finite-budget classification above unchanged as a diagnostic.
    # In particular, slow critical relaxation is NOT an extra asymptotic phase.
    fig, ax = plt.subplots(figsize=(10, 6.7), layout="constrained")
    ax.set_facecolor(GREY)
    x_left = np.linspace(0, 0.25, 501)
    x_middle = np.linspace(0.25, 0.5, 501)
    x_right = np.linspace(0.5, 0.8, 601)
    boundary_left = 2/(2-4*x_left)
    boundary_middle = 2/(4*x_middle)
    boundary_right = 2/(2*x_right+1)
    ax.fill_between(x_left, 0, boundary_left, color=BLUE, linewidth=0)
    ax.fill_between(x_middle, 0, boundary_middle, color=BLUE, linewidth=0)
    ax.fill_between(x_left, boundary_left, 2.1, color=ORANGE, linewidth=0)
    ax.fill_between(x_right, 0, boundary_right, color=GREEN, linewidth=0)
    for x, boundary in ((x_left, boundary_left), (x_middle, boundary_middle)):
        ax.plot(x, boundary, "k--", lw=1.6)
    ax.plot(x_right, boundary_right, "k--", lw=1.6,
            label=r"Stability boundary: $\eta=2/\lambda_{\max}$")
    ax.axvline(0.5, color="k", ls=":", lw=1.4,
               label=r"Output threshold: $\gamma=1/2$")
    ax.set(xlabel=r"Weight decay $\gamma$", ylabel=r"Step size $\eta$",
           xlim=(0, 0.8), ylim=(0, 1.6),
           title=r"Learning $y=x$ with $f(x)=abx$: full-batch gradient descent")
    handles = [Patch(color=c, label=l) for c,l in zip(
        [BLUE, ORANGE, GREEN, GREY],
        ["Stable learned solutions", "Oscillations observed", "Stable zero solution", "Divergence observed"])]
    lines, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles+lines, loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncols=2, fontsize=9, frameon=False)
    fig.supxlabel(r"For $\eta>0$ · slow convergence at $\gamma=1/2$ is part of the zero-output phase", fontsize=9)
    for ext in ("png", "svg"):
        fig.savefig(output_dir/f"step-size-phase-diagram.{ext}", dpi=180)
    plt.close(fig)
    np.savez_compressed(output_dir/"step-size-phase-diagram-data.npz",
                        gamma=gammas, eta=etas, classification=labels, a=a, b=b)
    return dict(stability_steps=steps, stability_shape=list(G.shape), initial_weights=[0.1, 0.11],
                stability_display="Analytic stable-region boundaries; numerical oscillation/divergence observations",
                raw_classification_plot="step-size-phase-diagram-finite-budget.png",
                terminal_window=tail, gradient_tolerance=1e-5, weight_range_tolerance=1e-5,
                divergence_cutoff=1e6, classification_counts=np.bincount(labels.ravel(), minlength=4).tolist())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("figures"))
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    metadata = transition_figure(args.output_dir, args.quick)
    metadata.update(stability_figure(args.output_dir, args.quick))
    metadata.update(numpy=np.__version__, matplotlib=matplotlib.__version__, quick=args.quick,
                    transition_eta=0.01, transition_gamma_range=[0.0, 0.8],
                    transition_initialisations={"N2": 0.1, "N3_high": 1.0, "N3_cold": 0.3},
                    stability_gamma_range=[0.0, 0.8], stability_eta_range=[0.02, 1.6],
                    learned_output_cutoff=1e-4, collapse_weight_norm_cutoff=1e-4)
    (args.output_dir/"run-settings.json").write_text(json.dumps(metadata, indent=2)+"\n")
    print(f"Saved figures, simulation arrays and run settings to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
