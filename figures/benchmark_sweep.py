"""
Benchmark 2: Parameter sweep — fidelity vs E_target across γ regimes.

For a fixed L=8 layer circuit, sweep E_target ∈ [0.25, 4.0] and three
γ regimes (uniform-low, uniform-high, heterogeneous). For each
(E_target, regime), compute the noisy-circuit fidelity under three
scheduling strategies and plot the result.
"""
import sys
sys.path.insert(0, '/tmp/rcb')
from rcb_optimizer import rcb_schedule
from benchmark_multilayer import (
    simulate_circuit, simulate_circuit_noiseless, state_fidelity)
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_strategies(gammas, E_target):
    """Return (thetas_opt, thetas_uni, thetas_conc) for the three strategies."""
    L = len(gammas)
    # RCB-optimal
    res = rcb_schedule(gammas, E_target)
    thetas_opt = res['thetas']
    # Uniform θ — each layer gets sin(2θ) = E_target / L (if feasible)
    if E_target / L <= 1.0:
        theta_uniform = 0.5 * np.arcsin(E_target / L)
    else:
        theta_uniform = np.pi / 4
    thetas_uni = np.full(L, theta_uniform)
    # Concentrated — place full entanglers on quietest layers
    n_full = int(np.floor(E_target))
    order = np.argsort(gammas)
    thetas_conc = np.zeros(L)
    for k in range(min(n_full, L)):
        thetas_conc[order[k]] = np.pi / 4
    rem = E_target - n_full
    if rem > 0 and n_full < L:
        thetas_conc[order[n_full]] = 0.5 * np.arcsin(min(1.0, rem))
    return thetas_opt, thetas_uni, thetas_conc

def fidelity_for_strategy(thetas, gammas, rho_init, kappa=1.0):
    rho_ideal = simulate_circuit_noiseless(thetas, rho_init)
    rho_noisy, _ = simulate_circuit(thetas, gammas, kappa, rho_init)
    return state_fidelity(rho_noisy, rho_ideal)

# Initial state: |+0⟩, has α≠0 in computational basis
psi0 = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)
rho_init = np.outer(psi0, psi0.conj())

L = 8
E_grid = np.linspace(0.25, 3.5, 22)

# Three γ regimes
np.random.seed(42)
regimes = {
    'Uniform low (γ=0.05)':   np.full(L, 0.05),
    'Uniform high (γ=0.15)':  np.full(L, 0.15),
    'Heterogeneous (γ ∈ [0.02, 0.30])': np.array([0.02, 0.05, 0.10, 0.20, 0.02, 0.05, 0.10, 0.30]),
}

results = {name: {'opt': [], 'uni': [], 'conc': []} for name in regimes}
costs = {name: {'opt': [], 'uni': [], 'conc': []} for name in regimes}

print("Computing sweep ...")
for name, gammas in regimes.items():
    for E_t in E_grid:
        if E_t >= L:
            for k in ('opt', 'uni', 'conc'):
                results[name][k].append(np.nan)
                costs[name][k].append(np.nan)
            continue
        t_opt, t_uni, t_conc = make_strategies(gammas, E_t)
        results[name]['opt'].append(fidelity_for_strategy(t_opt, gammas, rho_init))
        results[name]['uni'].append(fidelity_for_strategy(t_uni, gammas, rho_init))
        results[name]['conc'].append(fidelity_for_strategy(t_conc, gammas, rho_init))
        costs[name]['opt'].append(float(np.sum(gammas * t_opt)))
        costs[name]['uni'].append(float(np.sum(gammas * t_uni)))
        costs[name]['conc'].append(float(np.sum(gammas * t_conc)))

# Figure: 2 rows × 3 cols. Top: fidelity vs E_target. Bottom: cost vs E_target.
fig, axes = plt.subplots(2, 3, figsize=(12, 6.5), sharex=True)
colors = {'opt': '#1f77b4', 'uni': '#ff7f0e', 'conc': '#2ca02c'}
labels = {'opt': 'RCB-optimal', 'uni': 'Uniform θ', 'conc': 'Concentrated'}
linestyles = {'opt': '-', 'uni': '--', 'conc': ':'}

for col, (name, gammas) in enumerate(regimes.items()):
    # Top: fidelity
    ax = axes[0, col]
    for k in ('opt', 'uni', 'conc'):
        ax.plot(E_grid, results[name][k], color=colors[k], ls=linestyles[k],
                lw=2, label=labels[k])
    ax.set_title(name, fontsize=10)
    ax.grid(True, ls=':', alpha=0.4)
    if col == 0:
        ax.set_ylabel('Final-state fidelity\nF(noisy, ideal)', fontsize=10)
    ax.set_ylim(0.40, 1.02)
    if col == 0:
        ax.legend(loc='lower left', fontsize=8)
    # Bottom: cost
    ax2 = axes[1, col]
    for k in ('opt', 'uni', 'conc'):
        ax2.plot(E_grid, costs[name][k], color=colors[k], ls=linestyles[k], lw=2)
    ax2.grid(True, ls=':', alpha=0.4)
    if col == 0:
        ax2.set_ylabel(r'Coherence cost $\sum_\ell \gamma_\ell \theta_\ell$',
                       fontsize=10)
    ax2.set_xlabel(r'Entanglement target $E_{\rm target}$', fontsize=10)

fig.suptitle(r'RCB allocation vs naive scheduling — $L=8$ layers, '
             r'2-qubit chain, per-qubit dephasing',
             fontsize=12, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.96])
out = '/tmp/rcb/fig3_rcb_sweep.pdf'
plt.savefig(out, dpi=200, bbox_inches='tight')
plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
print(f"Saved {out}")

# Numerical summary table
print("\n" + "=" * 76)
print("Summary at representative E_target values")
print("=" * 76)
for E_t in [0.5, 1.0, 1.5, 2.0]:
    idx = np.argmin(np.abs(E_grid - E_t))
    print(f"\nE_target ≈ {E_grid[idx]:.3f}")
    for name in regimes:
        f_opt = results[name]['opt'][idx]
        f_uni = results[name]['uni'][idx]
        f_conc = results[name]['conc'][idx]
        c_opt = costs[name]['opt'][idx]
        c_uni = costs[name]['uni'][idx]
        c_conc = costs[name]['conc'][idx]
        print(f"  {name:38} "
              f"F_opt={f_opt:.4f}  F_uni={f_uni:.4f}  F_conc={f_conc:.4f}  "
              f"|  ΔF_opt-conc={f_opt-f_conc:+.4f}")
