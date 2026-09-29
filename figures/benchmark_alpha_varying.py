"""
Benchmark 3: layer-varying pre-gate affinity.

The allocation theorem uses effective rates  γ̃_ℓ = ᾱ_ℓ^pre · γ_ℓ · κ.
If ᾱ^pre is the same on every layer it cancels into the shadow price and
the schedule depends on γ_ℓ alone (fifth limitation, Sec. 7). This script
tests the regime where ᾱ^pre varies across layers, which is the only regime
in which the RCF cost and a rate-only cost can disagree.

Circuit (2 qubits, L layers). Layer ℓ:
    1. fixed single-qubit rotations V_ℓ = Ry(φ_ℓ¹) ⊗ Ry(φ_ℓ²)  (algorithm, not scheduled)
    2. idle pointer-basis dephasing for strength τ_idle      (common to all schedules)
    3. U_RA(θ_ℓ) = exp(-iθ_ℓ G/2),  G = XX + YY + ZZ
    4. gate dephasing at rate γ_ℓ for t_ℓ = κ θ_ℓ
Fidelity is ⟨ψ_ideal|ρ|ψ_ideal⟩ against the noiseless circuit with the same
θ schedule (the convention of benchmark_sweep.py).

Schedules compared (all satisfy Σ sin 2θ_ℓ = E_target, θ_ℓ ∈ [0, π/4]):
    uniform   θ_ℓ = ½ arcsin(E/L)
    rate      Theorem 1 with γ̃_ℓ = γ_ℓ κ           (what the paper's benchmarks run)
    rcf       Theorem 1 with γ̃_ℓ = ᾱ_ℓ^pre γ_ℓ κ, where ᾱ_ℓ^pre is the affinity
              entering layer ℓ's gate, profiled once on the noisy trajectory of
              the rate-only schedule ("profile, then schedule"). A self-consistent
              version is ill-posed: the linear program sends all weight to the
              lowest-ᾱ layers, which moves the ᾱ profile, and the iteration
              oscillates instead of converging.
    rcf2      same profiling, with weight W_ℓ = Σ_{i≠j} h_ij |ρ_ij|² of the state
              exposed to the gate dephasing (h = Hamming distance) — the exact
              first-order infidelity weight, ∝ ᾱ² rather than ᾱ
    oracle    direct numerical maximization of the simulated fidelity (SLSQP,
              multi-start); the reference the proxies are measured against

Run from the repository root:
    python3 figures/benchmark_alpha_varying.py            # full run + figure
    python3 figures/benchmark_alpha_varying.py --quick    # small ensemble
"""
import argparse
import os
import sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcb_optimizer import rcb_schedule  # noqa: E402

# ---------- building blocks ----------
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
G_HEIS = np.kron(SX, SX) + np.kron(SY, SY) + np.kron(SZ, SZ)
HAMMING = np.array([[bin(i ^ j).count('1') for j in range(4)]
                    for i in range(4)], dtype=float)
OFFDIAG = ~np.eye(4, dtype=bool)
PSI0 = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)   # |+0⟩, as in Sec. 6.5
E_FLOOR = 1e-6   # keeps γ̃ > 0 (Theorem 1 hypothesis) when a weight vanishes


def U_RA(theta):
    return expm(-1j * theta * G_HEIS / 2.0)


def ry(phi):
    c, s = np.cos(phi / 2), np.sin(phi / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def ry2(phis):
    return np.kron(ry(phis[0]), ry(phis[1]))


def dephase(rho, strength):
    """Per-qubit Z-dephasing: ρ_ij → ρ_ij · exp(-strength · h_ij)."""
    return rho * np.exp(-strength * HAMMING)


def alpha_bar(rho):
    """ᾱ = √(d/(d-1)) ‖offdiag ρ‖_F, computational pointer basis (Eq. 5)."""
    return float(np.sqrt(4 / 3) * np.sqrt(np.sum(np.abs(rho[OFFDIAG]) ** 2)))


def first_order_weight(rho):
    """W = Σ_{i≠j} h_ij |ρ_ij|²: d(1-F)/d(γt) at γt → 0 for near-pure ρ."""
    return float(np.sum(HAMMING * np.abs(rho) ** 2))


def run(thetas, inst, noisy=True):
    """Simulate one schedule. Returns final ρ and per-layer diagnostics."""
    rho = np.outer(PSI0, PSI0.conj())
    a_pre, a_exp, w_exp = [], [], []
    for ell, th in enumerate(thetas):
        V = ry2(inst['phis'][ell])
        rho = V @ rho @ V.conj().T
        if noisy:
            rho = dephase(rho, inst['tau_idle'])
        a_pre.append(alpha_bar(rho))
        U = U_RA(th)
        rho = U @ rho @ U.conj().T
        a_exp.append(alpha_bar(rho))
        w_exp.append(first_order_weight(rho))
        if noisy:
            rho = dephase(rho, inst['gammas'][ell] * inst['kappa'] * th)
    return rho, np.array(a_pre), np.array(a_exp), np.array(w_exp)


def fidelity(thetas, inst):
    rho, *_ = run(thetas, inst, noisy=True)
    rho_id, *_ = run(thetas, inst, noisy=False)
    # ideal state is pure: F = Tr(ρ_ideal ρ)
    return float(np.real(np.trace(rho_id @ rho)))


# ---------- schedules ----------
def sched_uniform(inst, E):
    L = len(inst['gammas'])
    return np.full(L, 0.5 * np.arcsin(E / L))


def sched_rate(inst, E):
    return rcb_schedule(inst['gammas'] * inst['kappa'], E)['thetas']


def sched_weighted(inst, E, which):
    """Theorem-1 schedule with γ̃_ℓ = w_ℓ γ_ℓ κ; w profiled on the noisy
    trajectory of the rate-only schedule."""
    _, a_pre, _, w_exp = run(sched_rate(inst, E), inst)
    w = np.maximum({'rcf': a_pre, 'rcf2': w_exp}[which], E_FLOOR)
    return rcb_schedule(w * inst['gammas'] * inst['kappa'], E)['thetas']


def sched_oracle(inst, E, starts, n_random=4, rng=None):
    L = len(inst['gammas'])
    rng = rng or np.random.default_rng(0)
    cons = {'type': 'eq', 'fun': lambda t: np.sum(np.sin(2 * t)) - E,
            'jac': lambda t: 2 * np.cos(2 * t)}
    bounds = [(0.0, np.pi / 4)] * L
    x0s = list(starts)
    for _ in range(n_random):
        x = rng.dirichlet(np.ones(L)) * E
        x0s.append(0.5 * np.arcsin(np.clip(x, 0, 1)))
    best, bestF = None, -np.inf
    for x0 in x0s:
        r = minimize(lambda t: -fidelity(t, inst), x0, method='SLSQP',
                     bounds=bounds, constraints=[cons],
                     options={'ftol': 1e-12, 'maxiter': 500})
        t = np.clip(r.x, 0, np.pi / 4)
        if abs(np.sum(np.sin(2 * t)) - E) > 1e-6:
            continue
        F = fidelity(t, inst)
        if F > bestF:
            best, bestF = t, F
    return best


def evaluate(inst, E, rng=None):
    th = {'uniform': sched_uniform(inst, E), 'rate': sched_rate(inst, E)}
    th['rcf'] = sched_weighted(inst, E, 'rcf')
    th['rcf2'] = sched_weighted(inst, E, 'rcf2')
    th['oracle'] = sched_oracle(inst, E, [th['uniform'], th['rate'],
                                          th['rcf'], th['rcf2']], rng=rng)
    F = {k: fidelity(v, inst) for k, v in th.items()}
    return th, F


# ---------- scenarios ----------
def scenarios(L=8):
    return {
        'A: decaying coherence (uniform γ=0.15, idle τ=0.15/layer)': dict(
            gammas=np.full(L, 0.15), kappa=1.0, tau_idle=0.15,
            phis=np.zeros((L, 2))),
        'B: interleaved rotations (uniform γ=0.15, no idle)': dict(
            gammas=np.full(L, 0.15), kappa=1.0, tau_idle=0.0,
            phis=np.array([[-1.4, 0.0], [1.4, 1.4]] * (L // 2))),
        'C: heterogeneous γ (paper Sec. 6.5) + idle τ=0.15': dict(
            gammas=np.array([0.02, 0.05, 0.10, 0.20, 0.02, 0.05, 0.10, 0.30]),
            kappa=1.0, tau_idle=0.15, phis=np.zeros((L, 2))),
    }


def random_instance(rng, L=8):
    return dict(gammas=rng.uniform(0.02, 0.30, L), kappa=1.0,
                tau_idle=rng.uniform(0.0, 0.2),
                phis=rng.uniform(-np.pi / 2, np.pi / 2, (L, 2)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--n', type=int, default=300)
    ap.add_argument('--no-fig', action='store_true')
    args = ap.parse_args()
    n = 40 if args.quick else args.n
    rng = np.random.default_rng(20260929)
    np.set_printoptions(precision=3, suppress=True)

    print('=' * 78)
    print('BENCHMARK 3: layer-varying pre-gate affinity, L = 8')
    print('=' * 78)

    # 0. sanity: layer-independent ᾱ reproduces the rate-only schedule
    inst0 = dict(gammas=np.array([0.02, 0.05, 0.10, 0.20, 0.02, 0.05, 0.10, 0.30]),
                 kappa=1.0, tau_idle=0.0, phis=np.zeros((8, 2)))
    base = sched_rate(inst0, 1.0)
    for c in (1.0, 0.9, 0.5, 0.2):
        t = rcb_schedule(c * inst0['gammas'], 1.0)['thetas']
        assert np.allclose(t, base, atol=1e-9), c
    print('\nSanity: common ᾱ ∈ {1, 0.9, 0.5, 0.2} leaves the schedule unchanged ✓')

    # 1. named scenarios
    sc_results = {}
    for name, inst in scenarios().items():
        for E in (1.0, 2.0):
            th, F = evaluate(inst, E, rng)
            _, a_pre, _, _ = run(th['rate'], inst)
            sc_results[(name, E)] = (inst, th, F, a_pre)
            print(f'\n--- {name}, E_target = {E} ---')
            print(f'  ᾱ_pre under rate schedule : {a_pre}')
            for k in ('uniform', 'rate', 'rcf', 'rcf2', 'oracle'):
                print(f'  θ {k:<8}: {th[k]}   F = {F[k]:.5f}')
            print(f'  ΔF(rcf − rate) = {F["rcf"] - F["rate"]:+.5f}   '
                  f'ΔF(rcf2 − rate) = {F["rcf2"] - F["rate"]:+.5f}   '
                  f'ΔF(oracle − rate) = {F["oracle"] - F["rate"]:+.5f}')
            # direction check: does rcf move θ toward low- or high-ᾱ layers?
            d = th['rcf'] - th['rate']
            if np.ptp(a_pre) > 1e-6 and np.linalg.norm(d) > 1e-9:
                r = np.corrcoef(d, a_pre)[0, 1]
                print(f'  corr(θ_rcf − θ_rate, ᾱ_pre) = {r:+.2f}  '
                      f'({"toward LOW-ᾱ layers" if r < 0 else "toward HIGH-ᾱ layers"})')

    # 2. random ensemble
    print(f'\n--- Random ensemble: {n} instances × E ∈ {{0.5, 1, 2}} ---')
    print('    γ_ℓ ~ U[0.02, 0.30], φ_ℓ¹,² ~ U[-π/2, π/2], τ_idle ~ U[0, 0.2]')
    ens = {E: {k: [] for k in ('uniform', 'rate', 'rcf', 'rcf2', 'oracle')}
           for E in (0.5, 1.0, 2.0)}
    for i in range(n):
        inst = random_instance(rng)
        for E in ens:
            _, F = evaluate(inst, E, rng)
            for k in F:
                ens[E][k].append(F[k])
    summary = {}
    for E, d in ens.items():
        d = {k: np.array(v) for k, v in d.items()}
        gap = d['oracle'] - d['rate']
        rows = {}
        for k in ('rcf', 'rcf2'):
            dF = d[k] - d['rate']
            closed = np.sum(dF) / np.sum(gap) if np.sum(gap) > 0 else np.nan
            rows[k] = dict(mean=dF.mean(), sem=dF.std(ddof=1) / np.sqrt(len(dF)),
                           win=np.mean(dF > 1e-7), lose=np.mean(dF < -1e-7),
                           closed=closed, worst=dF.min(), best=dF.max())
        summary[E] = (rows, gap.mean())
        print(f'\n  E_target = {E}:  mean F(oracle) − F(rate) = {gap.mean():+.5f}')
        for k, r in rows.items():
            print(f'    {k:<5} ΔF vs rate: mean {r["mean"]:+.5f} ± {r["sem"]:.5f}  '
                  f'wins {r["win"]:.0%}  losses {r["lose"]:.0%}  '
                  f'range [{r["worst"]:+.4f}, {r["best"]:+.4f}]  '
                  f'oracle gap closed {r["closed"]:.0%}')

    if not args.no_fig:
        make_figure(sc_results, ens)


def make_figure(sc_results, ens):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    names = list(dict.fromkeys(k[0] for k in sc_results))
    fig, axes = plt.subplots(1, len(names) + 1, figsize=(16, 3.8))
    style = {'rate': ('C0', 'o', 'rate-only'), 'rcf': ('C3', 's', 'RCF (ᾱ)'),
             'rcf2': ('C2', '^', 'first-order (W)'), 'oracle': ('k', 'x', 'oracle')}
    for ax, name in zip(axes, names):
        inst, th, F, a_pre = sc_results[(name, 1.0)]
        x = np.arange(1, len(a_pre) + 1)
        for k, (c, m, lab) in style.items():
            ax.plot(x, th[k], marker=m, color=c, lw=1,
                    label=f'{lab}  F={F[k]:.4f}')
        ax2 = ax.twinx()
        ax2.bar(x, a_pre, color='0.85', zorder=0)
        ax2.set_ylim(0, 1.05)
        ax2.set_ylabel(r'$\bar\alpha^{\rm pre}_\ell$ (bars)', color='0.5')
        ax.set_zorder(ax2.get_zorder() + 1)
        ax.patch.set_visible(False)
        ax.set_title(name.split(' (')[0], fontsize=10)
        ax.set_xlabel(r'layer $\ell$')
        ax.set_ylabel(r'$\theta_\ell$')
        ax.legend(fontsize=7, loc='upper left')
    ax = axes[-1]
    Es = list(ens)
    for k, c, lab in (('rcf', 'C3', 'RCF (ᾱ)'), ('rcf2', 'C2', 'first-order (W)'),
                      ('oracle', 'k', 'oracle')):
        m = [np.mean(np.array(ens[E][k]) - np.array(ens[E]['rate'])) for E in Es]
        s = [np.std(np.array(ens[E][k]) - np.array(ens[E]['rate']), ddof=1)
             / np.sqrt(len(ens[E][k])) for E in Es]
        ax.errorbar(Es, m, yerr=s, marker='o', color=c, label=lab, capsize=3)
    ax.axhline(0, color='0.6', lw=0.8)
    ax.set_xlabel(r'$E_{\rm target}$')
    ax.set_ylabel(r'mean $F - F_{\rm rate}$')
    ax.set_title('Random ensemble', fontsize=10)
    ax.legend(fontsize=7)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'fig4_alpha_varying.pdf')
    fig.savefig(out)
    print(f'\nWrote {out}')


if __name__ == '__main__':
    main()
