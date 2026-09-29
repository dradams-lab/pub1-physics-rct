# Relational Coherence Budgeting for Tunable Exchange Gates

[![DOI](https://zenodo.org/badge/1234283634.svg)](https://doi.org/10.5281/zenodo.20130304)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Pointer-Basis Affinity, Decoherence, and Exchange-Angle Coherence Cost**

Author: Dr. Joshua Adams ([ORCID 0000-0002-7185-9125](https://orcid.org/0000-0002-7185-9125)), Independent Researcher

---

## Abstract

Decoherence theory already explains why system properties become definite. This paper asks what that explanation is worth to someone who can tune the strength of an entangling gate. The Relational Coherence framework (RCF) restates four standard identities of pointer-basis coherence theory in terms of a normalized Hilbert–Schmidt quantifier ᾱ(S,E) ∈ [0,1], fixed by einselection, and treats the drop ᾱ<sup>pre</sup> − ᾱ<sup>post</sup> across a circuit layer as a cost. None of this changes the predictions of quantum mechanics. Rovelli's relational interpretation serves as the conceptual setting; I do not argue that Bell's theorem singles it out.

For tunable Heisenberg-exchange gates U<sub>RA</sub>(θ) under Markovian dephasing proportional to gate time, with per-layer rates γ̃<sub>ℓ</sub> and a fixed entanglement target Σ<sub>ℓ</sub>|sin 2θ<sub>ℓ</sub>|, I prove that the cost-minimizing schedule is unique: θ<sub>ℓ</sub>\* = ½ arccos[min(1, γ̃<sub>ℓ</sub>/2λ\*)], where the multiplier λ\* is set by the target. Quiet layers receive more entanglement, and any layer with γ̃<sub>ℓ</sub> ≥ 2λ\* receives none.

In eight-layer density-matrix simulations with unit target, the schedule improves final-state fidelity by up to 0.040 over a single full entangler (γ = 0.15) and by 0.025 over equal angles when per-layer noise ranges from 0.02 to 0.30. The per-gate behavior agrees with published continuous-fSim results on Sycamore-class processors. These gains assume the exchange angle can be calibrated directly; where U<sub>RA</sub>(θ) has to be built from fixed native gates, they may shrink or disappear.

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

- **Pub2 — Philosophy**: [Three Paths to One Structure](https://github.com/dradams-lab/pub2-philosophy) — [DOI: 10.5281/zenodo.23048193](https://doi.org/10.5281/zenodo.23048193) (v0.6.3)
- **Pub3 — Bahá'í Studies**: [Mahabbat and the Two Wings](https://github.com/dradams-lab/pub3-bahai-studies) — [DOI: 10.5281/zenodo.23047977](https://doi.org/10.5281/zenodo.23047977) (v0.4.5)
- **Book**: [The Physics of Love](https://github.com/dradams-lab/book-physics-of-love) (in preparation)

---

## Build

This project compiles with `pdflatex`:

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The compiled PDF is attached to each [GitHub release](https://github.com/dradams-lab/pub1-physics-rct/releases). Zenodo archives the source files under the DOI above.

---

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share, adapt, and reuse with attribution.
