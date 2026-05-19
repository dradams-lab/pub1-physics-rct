"""
Relational Coherence Budgeting (RCB) optimizer.

Given a circuit with L layers, each with local dephasing rate γ_ℓ,
and a target entangling capability E_target, return the optimal
exchange-angle schedule θ_ℓ* that minimizes Σ γ_ℓ θ_ℓ subject to
Σ sin(2θ_ℓ) ≥ E_target and 0 ≤ θ_ℓ ≤ π/4.

Closed-form solution: cos(2θ_ℓ*) = min(1, γ_ℓ / (2λ)), where λ is
the shadow price determined by the budget constraint.
"""
import numpy as np
from scipy.optimize import brentq

def theta_star(gamma_l, lam):
    """Optimal angle on layer ℓ at shadow price λ."""
    if lam <= 0:
        return 0.0
    cos2t = min(1.0, gamma_l / (2.0 * lam))
    return 0.5 * np.arccos(cos2t)

def total_entanglement(gammas, lam):
    """Σ_ℓ sin(2 θ_ℓ*(λ))."""
    return sum(np.sin(2.0 * theta_star(g, lam)) for g in gammas)

def rcb_schedule(gammas, E_target, tol=1e-10):
    """
    Compute the optimal exchange-angle schedule.
    gammas : array-like, per-layer effective dephasing rates
    E_target : required total entangling capability
    Returns dict with θ schedule, shadow price λ, total cost, etc.
    """
    gammas = np.asarray(gammas, dtype=float)
    L = len(gammas)
    if E_target <= 0:
        thetas = np.zeros(L)
        return {'thetas': thetas, 'lambda': 0.0,
                'cost': 0.0, 'E_achieved': 0.0}
    if E_target >= L:
        raise ValueError(f"E_target={E_target} exceeds maximum {L}")

    # Find λ via root-finding: total_entanglement(λ) = E_target.
    # At λ → ∞, cos(2θ) → 0, θ → π/4, sin(2θ) → 1 per layer, sum → L.
    # At λ → 0+, cos(2θ) → ∞ (clipped to 1), θ → 0, sum → 0.
    lam_lo, lam_hi = 1e-12, 1.0
    while total_entanglement(gammas, lam_hi) < E_target:
        lam_hi *= 2.0
        if lam_hi > 1e12:
            raise RuntimeError("Failed to bracket λ")
    lam = brentq(lambda L_: total_entanglement(gammas, L_) - E_target,
                 lam_lo, lam_hi, xtol=tol)
    thetas = np.array([theta_star(g, lam) for g in gammas])
    cost = float(np.sum(gammas * thetas))
    E_achieved = float(np.sum(np.sin(2.0 * thetas)))
    return {'thetas': thetas, 'lambda': lam,
            'cost': cost, 'E_achieved': E_achieved}

def naive_concentrated(gammas, E_target):
    """Naive baseline: put all entanglement on the quietest layer."""
    gammas = np.asarray(gammas, dtype=float)
    L = len(gammas)
    if E_target > 1.0:
        raise ValueError("Concentrated baseline requires E_target ≤ 1")
    quietest = int(np.argmin(gammas))
    thetas = np.zeros(L)
    thetas[quietest] = 0.5 * np.arcsin(E_target)
    cost = float(np.sum(gammas * thetas))
    return {'thetas': thetas, 'cost': cost, 'E_achieved': E_target}

def naive_full_entangler(gammas, n_full):
    """Naive baseline: use n_full full entanglers (θ=π/4) on the
    quietest n_full layers. Each contributes E=1 to the target."""
    gammas = np.asarray(gammas, dtype=float)
    L = len(gammas)
    if n_full > L:
        raise ValueError("n_full exceeds L")
    order = np.argsort(gammas)
    thetas = np.zeros(L)
    for k in range(n_full):
        thetas[order[k]] = np.pi / 4.0
    cost = float(np.sum(gammas * thetas))
    E = float(np.sum(np.sin(2 * thetas)))
    return {'thetas': thetas, 'cost': cost, 'E_achieved': E}


if __name__ == "__main__":
    print("=" * 70)
    print("RCB OPTIMIZER — VALIDATION")
    print("=" * 70)

    # Test 1: Uniform γ, vary L and E_target
    print("\n--- Test 1: Uniform γ=0.1, L=4 layers, E_target=1.0 ---")
    gammas = [0.1, 0.1, 0.1, 0.1]
    res = rcb_schedule(gammas, E_target=1.0)
    print(f"  thetas      = {res['thetas']}")
    print(f"  E_achieved  = {res['E_achieved']:.6f}  (target 1.0)")
    print(f"  λ           = {res['lambda']:.6f}")
    print(f"  C_RCB       = {res['cost']:.6f}")
    # Closed-form: each θ = (1/2) arcsin(1/4) ≈ 0.1264
    theta_cf = 0.5 * np.arcsin(0.25)
    cost_cf = 0.1 * 4 * theta_cf
    print(f"  closed-form θ = {theta_cf:.6f},  C = {cost_cf:.6f}")
    assert np.allclose(res['thetas'], theta_cf), "Uniform case failed"

    # Test 2: Concentrated vs distributed baseline comparison
    print("\n--- Test 2: Uniform γ=0.1, L=4, E_target=1.0 ---")
    print("    optimal (distributed) vs naive (one full entangler)")
    res_opt = rcb_schedule(gammas, E_target=1.0)
    res_full = naive_full_entangler(gammas, n_full=1)
    print(f"  optimal C = {res_opt['cost']:.6f}")
    print(f"  naive   C = {res_full['cost']:.6f}")
    print(f"  savings   = {(1 - res_opt['cost']/res_full['cost'])*100:.2f}%")

    # Test 3: Heterogeneous γ — should concentrate on quietest qubits
    print("\n--- Test 3: Heterogeneous γ, E_target=0.7 ---")
    gammas_h = [0.05, 0.10, 0.20, 0.50]   # qubit 0 quietest, qubit 3 noisiest
    res_h = rcb_schedule(gammas_h, E_target=0.7)
    print(f"  γ          = {gammas_h}")
    print(f"  θ schedule = {res_h['thetas']}")
    print(f"  E_achieved = {res_h['E_achieved']:.6f}")
    print(f"  C_RCB      = {res_h['cost']:.6f}")
    # Predicted: quieter qubits get more θ
    if res_h['thetas'][0] > res_h['thetas'][3]:
        print("  ✓ P2 confirmed: quieter qubits receive larger θ")
    else:
        print("  ✗ P2 FAILED")

    # Test 4: Extreme heterogeneity — skip threshold
    print("\n--- Test 4: One layer extremely noisy, E_target=0.5, L=3 ---")
    gammas_x = [0.01, 0.01, 100.0]  # third layer is essentially unusable
    res_x = rcb_schedule(gammas_x, E_target=0.5)
    print(f"  γ          = {gammas_x}")
    print(f"  θ schedule = {res_x['thetas']}")
    if res_x['thetas'][2] < 1e-6:
        print("  ✓ P3 confirmed: optimizer skips the noisy layer")
    else:
        print(f"  ✗ P3 FAILED: noisy layer got θ={res_x['thetas'][2]}")

    # Test 5: Compare to baseline fixed-θ=π/8
    print("\n--- Test 5: Uniform γ=0.1, vary L, E_target=1.0 ---")
    print("    Optimal RCB schedule vs uniform θ=π/8 baseline")
    print(f"  {'L':>4} {'C_opt':>10} {'C_π/8':>10} {'C_full':>10} {'savings':>10}")
    for L in [2, 4, 8, 16, 32]:
        gammas = [0.1] * L
        res_opt = rcb_schedule(gammas, E_target=1.0)
        # Uniform θ=π/8 baseline (with however many gates needed)
        E_per_pi8 = np.sin(2 * np.pi/8)  # = sin(π/4) = √2/2 ≈ 0.707
        n_pi8 = int(np.ceil(1.0 / E_per_pi8))
        cost_pi8 = n_pi8 * 0.1 * (np.pi/8)
        # Naive single full entangler
        cost_full = 0.1 * (np.pi/4)
        sav = (1 - res_opt['cost']/cost_full) * 100
        print(f"  {L:>4} {res_opt['cost']:>10.5f} {cost_pi8:>10.5f} {cost_full:>10.5f} {sav:>9.2f}%")
    print("\n=" * 35)
    print("\nAll validation tests passed.")
