# Figures and reproducibility

Scripts that generate the figures and table values referenced in the paper.
All scripts are self-contained and depend only on `numpy` and `matplotlib`.

## Setup

```bash
python3 -m venv figures/.venv
figures/.venv/bin/pip install numpy matplotlib
```

## Reproducing the paper artifacts

| Script | Produces | Referenced as |
|---|---|---|
| `generate_fig1.py` | `fig1_affinity_decay.pdf` (and `.png`) | Fig. 1, §III |
| `generate_fig2.py` | `alpha-dynamics.pdf` | Fig. 2, §V |
| `generate_tables.py` | stdout: Tables I and II values | §V |

Run each from the repository root:

```bash
figures/.venv/bin/python figures/generate_fig1.py
figures/.venv/bin/python figures/generate_fig2.py
figures/.venv/bin/python figures/generate_tables.py
```

## Notes for reviewers

- **Fig. 1** (single qubit, |+⟩ under Markovian dephasing): the simulation
  uses forward-Euler integration of the Lindblad dissipator at `dt = 0.01`;
  the analytic curve `ᾱ(t) = e^{−γt}` and the simulation samples agree to
  better than `2 × 10⁻⁴` over `t ∈ [0, 30]`.

- **Fig. 2** (two qubits, |++⟩ under independent dephasing): the script
  computes `ρ_S(t)` analytically by element-wise multiplication of the
  initial density matrix by the Hamming-distance decay factor
  `exp(−γ d_H(i,j) t)`, then evaluates `ᾱ(t)` from the Frobenius norm of
  the off-diagonal block. The closed form
  `ᾱ²(t) = (2/3) e^{−2γt} + (1/3) e^{−4γt}`
  is asserted internally (`np.allclose`, atol = 1e-12).

- **Tables**: the analytical formulas in `generate_tables.py` reproduce
  Table I (depolarizing, gate-time-proportional) **exactly**. The
  dephasing and amplitude-damping rows of Table II in the paper come from
  full Qiskit/Cirq simulation; the analytical estimates in this script
  give the same sign and order of magnitude but not the exact values.
  The full simulator notebooks are linked from the Code Availability
  statement in §VII.
