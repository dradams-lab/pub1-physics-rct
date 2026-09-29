# Figures and reproducibility

Scripts that generate the figures and table values referenced in the paper.

## Setup

```bash
python3 -m venv figures/.venv
figures/.venv/bin/pip install numpy matplotlib qiskit qiskit-aer cirq-core
```

The plain figure scripts (`generate_fig1.py`, `generate_fig2.py`) depend only on
`numpy` and `matplotlib`. The Qiskit / Cirq simulators
(`simulate_table2_qiskit.py`, `simulate_table2_cirq.py`) additionally require
`qiskit`, `qiskit-aer`, and `cirq-core`.

## Reproducing the paper artifacts

| Script | Produces | Referenced as |
|---|---|---|
| `generate_fig1.py` | `fig1_affinity_decay.pdf` (and `.png`) | Fig. 1, §III |
| `generate_fig2.py` | `alpha-dynamics.pdf` | Fig. 2, §V |
| `generate_tables.py` | stdout: closed-form Tables I and II | §V |
| `simulate_table2_qiskit.py` | stdout: Table II via Qiskit-Aer density-matrix simulation | §V |
| `simulate_table2_cirq.py` | stdout: Table II via Cirq density-matrix simulation | §V |
| `benchmark_alpha_varying.py` | stdout + `fig4_alpha_varying.pdf`: RCF (ᾱ-weighted) vs rate-only schedules when ᾱ<sup>pre</sup> varies across layers (not yet referenced in the text) | §VII, fifth limitation |

Run each from the repository root:

```bash
figures/.venv/bin/python figures/generate_fig1.py
figures/.venv/bin/python figures/generate_fig2.py
figures/.venv/bin/python figures/generate_tables.py
figures/.venv/bin/python figures/simulate_table2_qiskit.py
figures/.venv/bin/python figures/simulate_table2_cirq.py
figures/.venv/bin/python figures/benchmark_alpha_varying.py   # ~8 min; --quick for ~1 min
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

- **Tables I and II**: all three scripts produce identical Δ F values to
  numerical precision. `generate_tables.py` uses closed-form analytical
  formulas; `simulate_table2_qiskit.py` builds explicit Kraus operators and
  uses Qiskit-Aer's `average_gate_fidelity` against the Choi-Jamiolkowski
  representation; `simulate_table2_cirq.py` does the same via Cirq's
  `kraus_to_choi`. The dephasing channel uses the paper's convention of
  per-qubit off-diagonal damping `1 − γ` (equivalent to a Pauli-Z channel
  with flip probability `p_Z = γ/2`); the amplitude-damping channel uses
  the standard Kraus operators independently per qubit.

- **Layer-varying ᾱ benchmark** (`benchmark_alpha_varying.py`, needs `scipy`):
  tests the one regime where the RCF cost `γ̃_ℓ = ᾱ_ℓ^pre γ_ℓ κ` and a
  rate-only cost give different schedules. ᾱ^pre is profiled once on the
  rate-only schedule's noisy trajectory; a self-consistent fixed point
  oscillates (the linear program is bang-bang) and is not used. The
  `oracle` column is SLSQP maximization of the simulated fidelity under
  the same `Σ sin 2θ = E_target` constraint, multi-start, fixed seed.
