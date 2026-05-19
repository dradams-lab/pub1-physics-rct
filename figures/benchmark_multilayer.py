"""
Benchmark 1: Multi-layer entanglement-distribution task.

A circuit with L two-qubit gate layers, each implementing U_RA(θ_ℓ)
followed by independent per-qubit dephasing at rate γ_ℓ. The target
is a fixed total entangling capability E_target = Σ sin(2θ_ℓ).

Compare three scheduling strategies:
  (a) RCB-optimal schedule (Lagrangian solution)
  (b) Uniform θ across layers (naive distribute)
  (c) Concentrated full entangler (naive concentrate)

For each, simulate the actual 2-qubit density matrix evolution
and report the final scalar affinity ᾱ_final and joint-state fidelity
against the ideal unitary's output.
"""
import sys
sys.path.insert(0, '/tmp/rcb')
from rcb_optimizer import rcb_schedule, naive_full_entangler
import numpy as np

# ---------- Quantum building blocks ----------
I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)

def kron(*args):
    out = args[0]
    for a in args[1:]:
        out = np.kron(out, a)
    return out

# Heisenberg generator G = σx⊗σx + σy⊗σy + σz⊗σz
G_HEIS = kron(SX, SX) + kron(SY, SY) + kron(SZ, SZ)

def U_RA(theta):
    """U_RA(θ) = exp(-iθ G / 2)."""
    # Diagonalize G: eigenvalues +1 (triplet, ×3) and -3 (singlet, ×1).
    # Bell basis ordering: |Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩
    # In computational basis, we can just exp directly via expm.
    from scipy.linalg import expm
    return expm(-1j * theta * G_HEIS / 2.0)

def apply_dephasing(rho, gamma, t, n_qubits=2):
    """
    Apply per-qubit independent Z-dephasing of strength γt to each qubit
    of an n-qubit state ρ.  For per-qubit ρ_ij with bit i≠j of qubit k,
    multiply by exp(-γt). Implemented as off-diagonal damping by Hamming
    distance.
    """
    rho = rho.copy()
    damping = np.exp(-gamma * t)
    dim = 2 ** n_qubits
    for i in range(dim):
        for j in range(dim):
            if i == j: continue
            # Count Hamming distance between i and j
            h = bin(i ^ j).count('1')
            rho[i, j] *= damping ** h
    return rho

def scalar_affinity(rho, pointer_basis=None):
    """
    ᾱ = √(d/(d-1)) · ||off-diag(ρ)||_F  in the computational pointer basis.
    """
    d = rho.shape[0]
    od = rho.copy()
    np.fill_diagonal(od, 0.0)
    frob = np.sqrt(np.sum(np.abs(od) ** 2))
    return float(np.sqrt(d / (d - 1)) * frob)

def fidelity_pure(rho, psi_target):
    """Fidelity ⟨ψ|ρ|ψ⟩ against a pure target."""
    return float(np.real(psi_target.conj() @ rho @ psi_target))

# ---------- Circuit simulator ----------
def simulate_circuit(thetas, gammas, kappa=1.0, rho_init=None,
                    track_alpha=False):
    """
    Apply U_RA(θ_ℓ) followed by dephasing at rate γ_ℓ for duration
    t_ℓ = κ·θ_ℓ, layer by layer.
    """
    if rho_init is None:
        psi0 = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩
        rho = np.outer(psi0, psi0.conj())
    else:
        rho = rho_init.copy()
    alphas = [scalar_affinity(rho)]
    for theta, gamma in zip(thetas, gammas):
        U = U_RA(theta)
        rho = U @ rho @ U.conj().T
        t = kappa * theta
        rho = apply_dephasing(rho, gamma, t, n_qubits=2)
        alphas.append(scalar_affinity(rho))
    return rho, (np.array(alphas) if track_alpha else None)

def simulate_circuit_noiseless(thetas, rho_init=None):
    """Ideal evolution (no dephasing)."""
    if rho_init is None:
        psi0 = np.array([1, 0, 0, 0], dtype=complex)
        rho = np.outer(psi0, psi0.conj())
    else:
        rho = rho_init.copy()
    for theta in thetas:
        U = U_RA(theta)
        rho = U @ rho @ U.conj().T
    return rho

def state_fidelity(rho_noisy, rho_ideal):
    """Uhlmann fidelity F = (Tr√(√ρ σ √ρ))²."""
    from scipy.linalg import sqrtm
    sqrt_r = sqrtm(rho_noisy)
    inner = sqrt_r @ rho_ideal @ sqrt_r
    sqrt_inner = sqrtm(inner)
    return float(np.real(np.trace(sqrt_inner)) ** 2)

# ---------- Benchmark ----------
def run_benchmark(L, E_target, gammas, kappa=1.0,
                  rho_init=None, label="benchmark"):
    """Compare three scheduling strategies on the multi-layer task."""
    # Default initial state: |10⟩ (so we get entangling action from G)
    if rho_init is None:
        # Use |+0⟩ — already has α ≠ 0 in the computational basis,
        # so we can see relational coherence evolve
        psi0 = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)
        rho_init = np.outer(psi0, psi0.conj())

    # Strategy (a): RCB-optimal
    res_opt = rcb_schedule(gammas, E_target)
    thetas_opt = res_opt['thetas']

    # Strategy (b): Uniform θ across layers (target same E_target)
    # Each layer gets θ such that L·sin(2θ) = E_target
    theta_uniform = 0.5 * np.arcsin(min(1.0, E_target / L))
    thetas_uni = np.full(L, theta_uniform)

    # Strategy (c): Concentrated — one full entangler if E_target ≤ 1,
    # otherwise as many as needed
    n_full = int(np.ceil(E_target))
    if n_full <= L:
        # Place full entanglers on quietest n_full-1 layers,
        # remainder on quietest other layer
        order = np.argsort(gammas)
        thetas_conc = np.zeros(L)
        for k in range(min(n_full - 1, L)):
            thetas_conc[order[k]] = np.pi / 4
        rem = max(0.0, E_target - (n_full - 1))
        if rem > 0 and n_full <= L:
            thetas_conc[order[n_full - 1]] = 0.5 * np.arcsin(min(1.0, rem))
    else:
        thetas_conc = np.full(L, np.pi / 4)

    # Simulate each
    rho_ideal = simulate_circuit_noiseless(thetas_opt, rho_init)
    rho_opt, alpha_opt = simulate_circuit(thetas_opt, gammas, kappa,
                                          rho_init, track_alpha=True)
    rho_uni, alpha_uni = simulate_circuit(thetas_uni, gammas, kappa,
                                          rho_init, track_alpha=True)
    rho_conc, alpha_conc = simulate_circuit(thetas_conc, gammas, kappa,
                                            rho_init, track_alpha=True)

    # For fidelity we compare each to its own ideal (since each strategy
    # implements a different target unitary on rho_init)
    rho_ideal_uni = simulate_circuit_noiseless(thetas_uni, rho_init)
    rho_ideal_conc = simulate_circuit_noiseless(thetas_conc, rho_init)

    F_opt = state_fidelity(rho_opt, rho_ideal)
    F_uni = state_fidelity(rho_uni, rho_ideal_uni)
    F_conc = state_fidelity(rho_conc, rho_ideal_conc)

    print(f"\n=== {label} (L={L}, E_target={E_target}) ===")
    print(f"  γ schedule: {np.round(gammas, 3)}")
    print(f"  Strategy        Σ_ℓ γ_ℓ θ_ℓ    F(noisy, ideal)    ᾱ_final")
    print(f"  RCB optimal    {sum(gammas*thetas_opt):>10.5f}      "
          f"{F_opt:>10.5f}    {alpha_opt[-1]:.5f}")
    print(f"  Uniform θ      {sum(gammas*thetas_uni):>10.5f}      "
          f"{F_uni:>10.5f}    {alpha_uni[-1]:.5f}")
    print(f"  Concentrated   {sum(gammas*thetas_conc):>10.5f}      "
          f"{F_conc:>10.5f}    {alpha_conc[-1]:.5f}")

    return {
        'thetas_opt': thetas_opt, 'thetas_uni': thetas_uni, 'thetas_conc': thetas_conc,
        'F_opt': F_opt, 'F_uni': F_uni, 'F_conc': F_conc,
        'alpha_opt': alpha_opt, 'alpha_uni': alpha_uni, 'alpha_conc': alpha_conc,
    }

# ---------- Run benchmark scenarios ----------
print("=" * 70)
print("BENCHMARK: multi-layer entanglement-distribution task")
print("=" * 70)

# Scenario A: Uniform low noise, modest target — should distribute
np.random.seed(42)
gammas_A = np.full(8, 0.05)
run_benchmark(L=8, E_target=1.5, gammas=gammas_A,
              label="Scenario A — uniform γ=0.05, L=8, E_target=1.5")

# Scenario B: Heterogeneous noise — should route to quietest layers
gammas_B = np.array([0.02, 0.05, 0.10, 0.20, 0.02, 0.05, 0.10, 0.30])
run_benchmark(L=8, E_target=1.5, gammas=gammas_B,
              label="Scenario B — heterogeneous γ, L=8, E_target=1.5")

# Scenario C: High noise — should still beat concentrated
gammas_C = np.full(8, 0.15)
run_benchmark(L=8, E_target=1.0, gammas=gammas_C,
              label="Scenario C — uniform γ=0.15 (high), L=8, E_target=1.0")

# Scenario D: Single full entanglement target (E_target=1, large L)
gammas_D = np.full(16, 0.08)
run_benchmark(L=16, E_target=1.0, gammas=gammas_D,
              label="Scenario D — uniform γ=0.08, L=16, E_target=1.0")
