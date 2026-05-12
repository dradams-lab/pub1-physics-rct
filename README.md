# The Relational Coherence Theorem

[![DOI](https://zenodo.org/badge/1234283634.svg)](https://doi.org/10.5281/zenodo.20130304)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Quantum Affinity, Decoherence, and a Coherence-Optimized Two-Qubit Gate**

Author: Dr. Joshua Adams ([ORCID 0000-0002-7185-9125](https://orcid.org/0000-0002-7185-9125)), Independent Researcher

---

## Abstract

Quantum mechanics has lacked an internally consistent ontological framework compatible with Bell's theorem since its formulation. Bell's theorem eliminates local hidden variables, implying that quantum properties are not intrinsic to systems but emerge through relational interaction. This paper formalizes the relational structure through the **Relational Coherence Theorem** (RCT), which introduces the **Affinity Tensor** α(S,E) as a measure of quantum coherence built from the off-diagonal elements of the reduced state ρ_S in the einselected pointer basis, with scalar summary ᾱ(S,E) ∈ [0,1].

The RCT comprises four propositions:

1. **Property indefiniteness** — a nonzero ᾱ precludes any definite pointer-state assignment
2. **Relational determination** — ᾱ decays exponentially under Markovian dephasing
3. **Coherence–affinity correspondence** — ᾱ = 1 at the equal-weight pointer-basis superposition, ᾱ = 0 at full pointer-basis decoherence
4. **Conservation of relational potential** — under closed-system unitary evolution, local coherence is redistributed into S–E correlations rather than destroyed

Motivated by the RCT, this paper introduces the **Relational Affinity Gate** U_RA(θ), a continuously parameterized two-qubit gate on the Heisenberg-exchange diagonal of the Weyl chamber of SU(4)/[SU(2)⊗SU(2)] with exchange angle θ ∈ [0, π/2]. On hardware where Heisenberg-exchange duration scales linearly with θ, U_RA(π/8) outperforms CNOT, iSWAP, and CZ by ΔF ∈ [+0.038, +0.039] at p_base = 0.10 (and [+0.019, +0.020] at p_base = 0.05), consistent across depolarizing, dephasing, and amplitude-damping noise — an operational expression of the RCT conservation law that suggests utility in near-term quantum devices.

Numerical simulations in Qiskit and Cirq compare U_RA(θ) against fixed entangling gates under depolarizing, dephasing, and amplitude-damping noise models.

---

## Citation

```bibtex
@article{Adams2026RCT,
  author  = {Adams, Joshua},
  title   = {The Relational Coherence Theorem: Quantum Affinity,
             Decoherence, and a Coherence-Optimized Two-Qubit Gate},
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
