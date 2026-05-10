"""Generate Figure 1: single-qubit affinity decay under Markovian dephasing.

Reproduces Fig. 1 of the RCT paper (sections/03-rct.tex).

System: one qubit, prepared in |+> = (|0> + |1>) / sqrt(2), the
equal-weight superposition for d = 2, with alpha-bar(0) = 1
(Proposition III(ii)).

Dynamics: pure dephasing at rate gamma, jump operators
L_0 = sqrt(gamma) |0><0|, L_1 = sqrt(gamma) |1><1|.  By Proposition II
the single off-diagonal magnitude obeys |rho_01(t)| = |rho_01(0)| e^{-gamma t},
so alpha-bar(t) = e^{-gamma t} exactly under the Markovian approximation.

Output: figures/fig1_affinity_decay.pdf  (and .png companion)
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def lindblad_step(rho: np.ndarray, gamma: float, dt: float) -> np.ndarray:
    """Forward Euler step on the dephasing dissipator (no H_S contribution).

    For pure-dephasing pointer-basis L_k = sqrt(gamma)|k><k|, the magnitude
    of any off-diagonal matrix element decays as d|rho_01|/dt = -gamma|rho_01|.
    """
    drho = np.zeros_like(rho)
    drho[0, 1] = -gamma * rho[0, 1]
    drho[1, 0] = -gamma * rho[1, 0]
    return rho + dt * drho


def main() -> None:
    gamma = 0.10
    t_max = 30.0

    # Continuous analytic curve.
    t_curve = np.linspace(0, t_max, 601)
    alpha_analytic = np.exp(-gamma * t_curve)

    # Discrete simulation samples (forward-Euler integration).
    n_samples = 13
    t_samples = np.linspace(0, t_max, n_samples)
    psi0 = np.array([1.0, 1.0]) / np.sqrt(2.0)
    rho = np.outer(psi0, psi0.conj()).astype(complex)
    alpha_sim = np.empty(n_samples)
    alpha_sim[0] = 2 * abs(rho[0, 1])
    dt = 0.01
    t = 0.0
    for k in range(1, n_samples):
        while t < t_samples[k] - 1e-12:
            step = min(dt, t_samples[k] - t)
            rho = lindblad_step(rho, gamma, step)
            t += step
        alpha_sim[k] = 2 * abs(rho[0, 1])  # for d=2: alpha-bar = 2|rho_01|

    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    ax.plot(t_curve, alpha_analytic, color="black", linewidth=2.0,
            label=r"$\bar\alpha(t) = e^{-\gamma t}$  (analytic)")
    ax.plot(t_samples, alpha_sim, "o", markersize=6, markerfacecolor="white",
            markeredgecolor="tab:red", markeredgewidth=1.4,
            label=r"density-matrix simulation")
    ax.axhline(0.0, color="gray", linewidth=0.6, linestyle=":")

    ax.set_xlabel(r"time  $t$  (in units of $1/\gamma$,  with $\gamma = 0.10$)")
    ax.set_ylabel(r"scalar affinity  $\bar\alpha(t)$")
    ax.set_xlim(0, t_max)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(
        r"Single-qubit affinity decay: $|+\rangle$ under Markovian dephasing",
        fontsize=10,
    )
    fig.tight_layout()

    out_dir = Path(__file__).parent
    pdf_path = out_dir / "fig1_affinity_decay.pdf"
    png_path = out_dir / "fig1_affinity_decay.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=200)
    max_err = np.max(np.abs(alpha_sim - np.exp(-gamma * t_samples)))
    print(f"wrote {pdf_path}  (sim vs analytic max error = {max_err:.4e})")


if __name__ == "__main__":
    main()
