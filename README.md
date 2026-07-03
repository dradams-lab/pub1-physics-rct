# Relational Coherence Budgeting for Tunable Exchange Gates

[![DOI](https://zenodo.org/badge/1234283634.svg)](https://doi.org/10.5281/zenodo.20130304)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Pointer-Basis Affinity, Decoherence, and Exchange-Angle Coherence Cost**

Author: Dr. Joshua Adams ([ORCID 0000-0002-7185-9125](https://orcid.org/0000-0002-7185-9125)), Independent Researcher

---

## Abstract

Bell's theorem and its loophole-free experimental verification rule out local non-contextual hidden-variable completions of quantum mechanics. A natural response, on which this work builds, is the relational reading of Rovelli, on which quantum properties are not assigned to systems in isolation but are encoded in their interaction histories. This paper packages one technically explicit aspect of that reading into the **Relational Coherence framework** (RCF), centred on the **Affinity Operator** α(S,E) — the off-diagonal part of the reduced state ρ_S in the einselected pointer basis — whose normalized Frobenius norm ᾱ(S,E) ∈ [0,1] is the Hilbert–Schmidt coherence quantifier of ρ_S in that basis.

The framework collects four standard identities in the language of ᾱ:

1. **Property indefiniteness** — ᾱ > 0 precludes a pointer-basis-diagonal ρ_S
2. **Relational determination** — ᾱ decays exponentially under Markovian dephasing in the pointer basis
3. **Coherence–affinity correspondence** — ᾱ ranges continuously over [0,1], with extrema at full pointer-basis decoherence and at the equal-weight pointer-basis pure superposition
4. **Coherence redistribution** — under closed unitary S–E evolution, local pointer-basis coherence is redistributed into S–E correlations rather than destroyed

Building on existing parametric-gate work, this paper examines the **tunable isotropic-exchange gate** U_RA(θ) = exp[−iθ(σ_x⊗σ_x + σ_y⊗σ_y + σ_z⊗σ_z)/2], a two-qubit unitary on the Heisenberg-exchange diagonal of the Weyl chamber of SU(4)/[SU(2)⊗SU(2)] with exchange angle θ ∈ [0, π/2]. The gate is the standard isotropic-exchange family; within the RCF diagnostic we refer to its use as the relational-affinity parameterization rather than as a new gate primitive. On platforms where Heisenberg-exchange pulse duration scales linearly with θ, U_RA(π/8) accumulates half the coherence-limited error of a full θ = π/4 entangler.

Numerical simulations in Qiskit and Cirq under gate-time-proportional depolarizing, dephasing, and amplitude-damping noise yield a per-gate fidelity advantage of ΔF ∈ [+0.038, +0.039] at p_base = 0.10 over CNOT, iSWAP, and CZ, consistent with the experimental continuous-fSim advantage reported by Foxen et al. on Sycamore. The advantage is contingent on direct exchange calibration; on platforms where U_RA(θ) must be decomposed into fixed native primitives, the advantage may shrink or vanish.

---

## Citation

```bibtex
@article{Adams2026RCF,
  author  = {Adams, Joshua},
  title   = {Relational Coherence Budgeting for Tunable Exchange Gates:
             Pointer-Basis Affinity, Decoherence, and Exchange-Angle
             Coherence Cost},
  year    = {2026},
  doi     = {10.5281/zenodo.20130304},
  note    = {Zenodo preprint. Concept DOI (evergreen).}
}
```

---

## Companion publications

- **Pub2 — Philosophy**: [Three Paths to One Structure](https://github.com/adams-research/pub2-philosophy) — [DOI: 10.5281/zenodo.20130289](https://doi.org/10.5281/zenodo.20130289)
- **Pub3 — Bahá'í Studies**: [Mahabbat and the Affinity Tensor](https://github.com/adams-research/pub3-bahai-studies) (forthcoming Zenodo DOI)
- **Book**: [The Physics of Love](https://github.com/adams-research/book-physics-of-love) (in preparation)

---

## Build

This project compiles with `pdflatex`:

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The PDF is also attached to each [GitHub release](https://github.com/adams-research/pub1-physics-rct/releases) and archived on Zenodo via the DOI above.

---

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share, adapt, and reuse with attribution.
