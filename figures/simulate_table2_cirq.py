"""Reproduce Table II of Sec. V via Cirq density-matrix simulation.

Mirrors ``simulate_table2_qiskit.py``: independent cross-platform
verification of the Delta F values reported in Table II.

For each noise model, this script builds the explicit Kraus operators,
applies them after the ideal gate via Cirq's ``KrausChannel``, and
computes the average gate fidelity from the Choi matrix using
Cirq's ``kraus_to_choi`` utility plus the Nielsen identity
F_avg = (d F_proc + 1) / (d + 1) with d = 4.

Run:
    python figures/simulate_table2_cirq.py
"""
from __future__ import annotations

import math
import numpy as np
import cirq

# Re-use the gate matrices and Kraus builders from the Qiskit script.
from simulate_table2_qiskit import (
    u_ra_matrix,
    iswap_matrix,
    kraus_depolarizing_2q,
    kraus_dephasing_single,
    kraus_amp_damp_single,
    kron_pair,
    p_eff,
)


def avg_fidelity_cirq(U: np.ndarray, kraus_full: list[np.ndarray]) -> float:
    """F_avg of (noise channel applied to U), benchmarked against ideal U.

    Builds the composite Kraus set {K_alpha @ U} for the noise-after-gate
    channel, converts to a Choi matrix via cirq.kraus_to_choi, and uses
    F_proc = Tr[Choi(U) . Choi(noise.U)] / d^2 then the Nielsen identity.
    """
    d = 4
    composite_kraus = [K @ U for K in kraus_full]
    choi_noisy = cirq.kraus_to_choi(composite_kraus)
    choi_ideal = cirq.kraus_to_choi([U])
    # Normalise: choi here is the unnormalised Jamiolkowski matrix
    # (sum over Kraus operators of vec(K) vec(K)^dag).  F_proc against
    # the ideal unitary is Tr[Choi_ideal^dag . Choi_noisy] / d^2.
    F_proc = float(np.real(np.trace(choi_ideal.conj().T @ choi_noisy))) / (d * d)
    return (d * F_proc + 1) / (d + 1)


def main() -> None:
    alpha_ura = math.pi / 8
    alpha_isw = math.pi / 4
    U_RA = u_ra_matrix(alpha_ura)
    U_iSW = iswap_matrix()

    print("=== Cirq simulator reproduction of Table II ===")
    print(f"{'noise model':<22}" + "".join(f"  p={pb:<6}" for pb in (0.02, 0.05, 0.10)))
    print("-" * 56)
    for name, kraus_fn, kind in [
        ("Depolarizing",    kraus_depolarizing_2q, "global"),
        ("Dephasing",       kraus_dephasing_single, "per-qubit"),
        ("Amplitude damp.", kraus_amp_damp_single, "per-qubit"),
    ]:
        deltas = []
        for pb in (0.02, 0.05, 0.10):
            pe_u = p_eff(alpha_ura, pb)
            pe_i = p_eff(alpha_isw, pb)
            if kind == "global":
                k_u = kraus_fn(pe_u)
                k_i = kraus_fn(pe_i)
            else:
                k_u = kron_pair(kraus_fn(pe_u))
                k_i = kron_pair(kraus_fn(pe_i))
            f_u = avg_fidelity_cirq(U_RA, k_u)
            f_i = avg_fidelity_cirq(U_iSW, k_i)
            deltas.append(f_u - f_i)
        cells = "  ".join(f"{d:+7.4f}" for d in deltas)
        print(f"{name:<22}{cells}")


if __name__ == "__main__":
    main()
