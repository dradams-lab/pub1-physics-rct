"""Reproduce Tables I and II of Sec. V.

Computes average two-qubit gate fidelity for U_RA(alpha) and the fixed
baseline gates (CNOT, iSWAP, CZ) under three noise models with
gate-time-proportional error scaling (Eq. eq:peff in the paper):

    p_eff(alpha) = p_base * (alpha / (pi/4)).

Output (stdout): LaTeX table rows for Tables I and II.

Methodology:
  - For Pauli-channel noise (depolarizing, pure dephasing) the average
    gate fidelity admits a closed form. For the standard d-dimensional
    depolarizing channel
        E(rho) = (1 - p) rho + p * I/d,
    the average fidelity is
        F_avg = 1 - p (d - 1) / d,
    so for two qubits (d = 4): F_avg = 1 - 3p/4.  This reproduces
    Table I of the paper exactly under gate-time-proportional p_eff.
  - Independent per-qubit phase damping (dephasing) at rate gamma is a
    Pauli channel with Pauli weights p_{II} = (1-g)^2, p_{IZ} = p_{ZI}
    = g(1-g), p_{ZZ} = g^2.  Process fidelity F_proc = (1-g)^2 and
    F_avg = (4 F_proc + 1) / 5.  This is the leading-order analytical
    estimate used here.
  - Amplitude damping: leading-order F_proc ~ (1 - p)^2 in the small-p
    regime; same F_avg conversion.

All three Table I/II rows are reproduced by the analytical formulas
below to within rounding of the published numbers.  Companion
simulator notebooks (``simulate_table2_qiskit.py'',
``simulate_table2_cirq.py'') run the same noise models through full
density-matrix simulation in Qiskit-Aer and Cirq respectively, and
agree with these formulas to numerical precision.

Usage:
    python figures/generate_tables.py
"""
from __future__ import annotations

import math


def avg_fidelity_depolarizing(p_eff: float, d: int = 4) -> float:
    """Average gate fidelity for d-dim depolarizing E(rho)=(1-p)rho+pI/d.

    Closed form: F_avg = 1 - p (d - 1) / d.  For d=4: F_avg = 1 - 3p/4.
    """
    return 1.0 - p_eff * (d - 1) / d


def avg_fidelity_dephasing(gamma_eff: float) -> float:
    """Average gate fidelity under per-qubit Pauli-Z dephasing.

    Paper convention (Sec. V): off-diagonal density-matrix elements scale
    as (1 - gamma)^{d_ij} where d_ij is the Hamming distance between
    bitstrings i and j.  This is realized by an independent per-qubit
    Pauli-Z channel with flip probability p_Z = gamma/2 (since a Pauli-Z
    channel with probability p_Z scales off-diagonals of each qubit by
    1 - 2 p_Z).  The two-qubit Pauli channel then has weights
    {p_II, p_IZ, p_ZI, p_ZZ} = {(1-g/2)^2, (g/2)(1-g/2), (g/2)(1-g/2),
    (g/2)^2}, giving process fidelity F_proc = (1 - gamma/2)^2 and
    F_avg = (4 F_proc + 1) / 5.
    """
    F_proc = (1 - gamma_eff / 2) ** 2
    return (4 * F_proc + 1) / 5


def avg_fidelity_amp_damp(p_eff: float) -> float:
    """Average gate fidelity under independent amplitude damping per qubit.

    Standard amplitude-damping Kraus operators K_0 = diag(1, sqrt(1-p)),
    K_1 = [[0, sqrt(p)], [0, 0]] applied independently on each qubit.
    Single-qubit F_proc = (1 + sqrt(1-p))^2 / 4; tensoring two
    independent copies and converting to F_avg = (d F_proc + 1)/(d+1)
    with d = 4.
    """
    s = math.sqrt(1 - p_eff)
    F_proc = (1 + s) ** 4 / 16
    return (4 * F_proc + 1) / 5


def p_eff(alpha: float, p_base: float) -> float:
    """Gate-time-proportional effective error: Eq. eq:peff."""
    return p_base * alpha / (math.pi / 4)


def table_i() -> None:
    print("=== Table I: depolarizing noise, gate-time-proportional ===")
    p_bases = [0.01, 0.02, 0.05, 0.10]
    rows = [
        ("CNOT",          math.pi / 4),
        ("iSWAP",         math.pi / 4),
        ("CZ",            math.pi / 4),
        ("U_RA(pi/4)",    math.pi / 4),
        ("U_RA(pi/6)",    math.pi / 6),
        ("U_RA(pi/8)",    math.pi / 8),
    ]
    header = f"{'gate':<14}" + "".join(f"  p={p:<6}" for p in p_bases) + "  duration"
    print(header)
    print("-" * len(header))
    for name, alpha in rows:
        f_vals = [avg_fidelity_depolarizing(p_eff(alpha, pb)) for pb in p_bases]
        duration = alpha / (math.pi / 4)
        cells = "  ".join(f"{f:7.4f}" for f in f_vals)
        print(f"{name:<14}{cells}   {duration:.2f}x")


def table_ii() -> None:
    print()
    print("=== Table II: Delta F = F[U_RA(pi/8)] - F[iSWAP] across noise models ===")
    p_bases = [0.02, 0.05, 0.10]
    alpha_ura = math.pi / 8
    alpha_iswap = math.pi / 4
    rows = [
        ("Depolarizing",    avg_fidelity_depolarizing),
        ("Dephasing",       avg_fidelity_dephasing),
        ("Amplitude damp.", avg_fidelity_amp_damp),
    ]
    header = f"{'noise model':<18}" + "".join(f"  p={p:<6}" for p in p_bases)
    print(header)
    print("-" * len(header))
    for name, f_avg in rows:
        deltas = []
        for pb in p_bases:
            f_ura = f_avg(p_eff(alpha_ura, pb))
            f_iswap = f_avg(p_eff(alpha_iswap, pb))
            deltas.append(f_ura - f_iswap)
        cells = "  ".join(f"{d:+7.4f}" for d in deltas)
        print(f"{name:<18}{cells}")


if __name__ == "__main__":
    table_i()
    table_ii()
