"""Generate Figure 2: scalar affinity dynamics under independent dephasing.

Reproduces Fig. 2 of the RCT paper (sections/05-simulation.tex).

System: two qubits S, prepared in |++> = (1/2)(|00>+|01>+|10>+|11>),
the equal-weight superposition in the 4-d computational pointer basis,
for which alpha-bar(0) = 1 (Proposition III(ii) of Sec. III).

Dynamics: independent pure dephasing on each qubit at rate gamma.
Under the Lindblad equation with single-qubit jump operators
L_a = sqrt(gamma) * Z_a (a = 1, 2), an off-diagonal element
rho_{ij,kl} between computational basis states |ij> and |kl> decays
at rate gamma * d_H(ij, kl), where d_H is the Hamming distance.

Output: figures/alpha-dynamics.pdf
"""
from __future__ import annotations

import itertools
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def hamming(i: int, j: int, n_qubits: int) -> int:
    """Hamming distance between two computational basis indices."""
    return bin(i ^ j).count("1")


def simulate(gamma: float, t_grid: np.ndarray, n_qubits: int = 2) -> np.ndarray:
    """Return alpha-bar(t) for |+>^n under independent per-qubit dephasing."""
    d = 2**n_qubits
    # |+>^n in the computational basis: every amplitude is 1/sqrt(d).
    psi0 = np.full(d, 1.0 / np.sqrt(d), dtype=complex)
    rho0 = np.outer(psi0, psi0.conj())

    # Hamming-distance matrix for the off-diagonal decay rates.
    H = np.array([[hamming(i, j, n_qubits) for j in range(d)] for i in range(d)])

    alpha_bar = np.empty_like(t_grid, dtype=float)
    for k, t in enumerate(t_grid):
        decay = np.exp(-gamma * H * t)            # diagonal entries get exp(0) = 1
        rho_t = rho0 * decay                       # element-wise: pure dephasing
        # Affinity tensor: zero out diagonal, keep off-diagonal coherences.
        alpha = rho_t - np.diag(np.diag(rho_t))
        frob_sq = np.sum(np.abs(alpha) ** 2).real
        alpha_bar[k] = np.sqrt(d / (d - 1) * frob_sq)
    return alpha_bar


def main() -> None:
    gamma = 0.10
    t_max = 30.0
    t_grid = np.linspace(0.0, t_max, 601)

    alpha = simulate(gamma, t_grid)

    # Closed-form check (two qubits):
    #   alpha_bar^2(t) = (2/3) e^{-2 gamma t} + (1/3) e^{-4 gamma t}
    # from the two off-diagonal classes (Hamming distance 1 and 2).
    closed_form = np.sqrt(
        (2 / 3) * np.exp(-2 * gamma * t_grid) + (1 / 3) * np.exp(-4 * gamma * t_grid)
    )
    assert np.allclose(alpha, closed_form, atol=1e-12), "numerical / analytic mismatch"

    # Single-qubit reference: alpha-bar(t) = e^{-gamma t} (Fig. 1, Sec. III).
    # Plotted to show the slowdown introduced by the heterogeneous Hamming
    # spectrum of off-diagonals in the two-qubit case.
    single_qubit = np.exp(-gamma * t_grid)

    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    ax.plot(t_grid, alpha, color="black", linewidth=2.0,
            label=r"$\bar\alpha(t)$, two qubits ($|{+}{+}\rangle$)")
    ax.plot(t_grid, single_qubit, color="tab:blue", linewidth=1.0, linestyle="--",
            label=r"$e^{-\gamma t}$, one-qubit reference (Fig. 1)")
    ax.axhline(0.0, color="gray", linewidth=0.6, linestyle=":")

    # 1/e marker on the two-qubit curve.
    idx_1e = int(np.argmin(np.abs(alpha - 1.0 / np.e)))
    ax.axhline(1.0 / np.e, color="gray", linewidth=0.4, linestyle=":")
    ax.annotate(rf"$\bar\alpha = 1/e$ at $t\approx{t_grid[idx_1e]:.1f}$",
                xy=(t_grid[idx_1e], 1.0 / np.e),
                xytext=(t_grid[idx_1e] + 1.5, 0.50),
                fontsize=8, color="gray",
                arrowprops=dict(arrowstyle="-", color="gray", linewidth=0.4))

    ax.set_xlabel(r"time  $t$  (in units of $1/\gamma$,  with $\gamma = 0.10$)")
    ax.set_ylabel(r"scalar affinity  $\bar\alpha(t)$")
    ax.set_xlim(0, t_max)
    ax.set_ylim(-0.02, 1.05)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(
        r"Affinity tensor dynamics: independent dephasing of $|{+}{+}\rangle$",
        fontsize=10,
    )
    fig.tight_layout()

    out = Path(__file__).parent / "alpha-dynamics.pdf"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}  (max alpha = {alpha.max():.6f}, min alpha = {alpha.min():.6f})")


if __name__ == "__main__":
    main()
