# Cover letter — Physical Review A

Paste the text below into the APS submission portal's cover-letter field.
Fill in the date. Suggested referees are optional for PRA; add names in
the portal if you want them.

---

Dear Editors,

I submit the manuscript "Relational Coherence Budgeting for Tunable
Exchange Gates: Pointer-Basis Affinity, Decoherence, and Exchange-Angle
Coherence Cost" for consideration as a Regular Article in *Physical Review A*.

The paper asks a practical question: on hardware where the exchange angle
of a two-qubit gate can be calibrated directly, how should entanglement
be distributed across the layers of a circuit when each gate's duration
costs coherence? Its main result is a Coherence-Budget Allocation
Theorem. For the isotropic Heisenberg-exchange family U(θ) under Markovian
dephasing proportional to gate time, with per-layer rates γ̃_ℓ and a fixed
entanglement target Σ_ℓ |sin 2θ_ℓ|, the cost-minimizing schedule is unique
and has closed form, θ*_ℓ = ½ arccos[min(1, γ̃_ℓ / 2λ*)], with λ* set by
the target. The theorem gives three testable predictions: spread
entanglement across layers under uniform noise, route it onto quieter
layers under heterogeneous noise, and skip layers whose rate exceeds
2λ*.

In eight-layer density-matrix simulations with unit target, the schedule
improves final-state fidelity by up to 0.040 over a single full entangler
and by 0.025 over equal angles when per-layer noise ranges from 0.02 to
0.30. The per-gate behavior is consistent with the continuous-fSim results
reported on Sycamore-class processors. The manuscript also states the
limits of the result plainly: the gains assume direct angle calibration
and may shrink or vanish when the gate must be synthesized from fixed
native gates (a break-even analysis is given).

The coherence cost is expressed through a normalized Hilbert–Schmidt
measure of pointer-basis coherence. The paper does not claim new
quantum-mechanical predictions or novelty for the gate family; its
contribution is the allocation result and its derivation as the unique
solution of a convex program. I believe this combination of an analytic
scheduling result with numerical and hardware-motivated checks suits
PRA's quantum-information readership.

A preprint and all simulation and figure-generation code are archived on
Zenodo (concept DOI 10.5281/zenodo.20130304) and at
https://github.com/dradams-lab/pub1-physics-rct. The Zenodo deposit is a
preprint, not a prior publication. The manuscript is not under
consideration elsewhere. Use of AI tools in preparing the work is
disclosed in the Acknowledgments. I have no conflicts of interest to
declare.

Sincerely,

Joshua Adams
Independent Researcher
ORCID 0000-0002-7185-9125
contact@joshuaadams.dev
