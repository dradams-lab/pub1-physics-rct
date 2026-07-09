# Physical Review A — Submission Checklist

**Manuscript:** *Relational Coherence Budgeting for Tunable Exchange Gates:
Pointer-Basis Affinity, Decoherence, and Exchange-Angle Coherence Cost*
**Author:** Dr. Joshua Adams (Independent Researcher), ORCID 0000-0002-7185-9125
**Target journal:** Physical Review A (APS)

---

## What's in this submission variant

| File | Purpose |
|------|---------|
| `main-pra.tex` | REVTeX 4.2 source (`[aps,pra,preprint]`), inlines `sections/*.tex` |
| `main-pra-flat.tex` | **Auto-generated** single-file version (run `./flatten-pra.sh` to regenerate) — this is what you upload |
| `flatten-pra.sh` | Regenerates `main-pra-flat.tex` from `main-pra.tex` + `sections/` |
| `references.bib` | Bibliography (unchanged from other variants) |
| `figures/` | 3 referenced figures: `alpha-dynamics.pdf`, `fig1_affinity_decay.pdf`, `fig3_rcb_sweep.pdf` |

The prebuilt zip (`pub1-pra-submission.zip`, saved as an artifact) contains
`main-pra-flat.tex` + `references.bib` + the 3 figures.

**Do NOT bundle `revtex4-2.cls` or `apsrev4-2.bst`** — APS and Overleaf
provide REVTeX; including your own copy can conflict with theirs.

---

## Class / format decisions (and why)

- **`preprint` (one-column), not `reprint` (two-column).** APS *prefers*
  the one-column referee format for submission; `reprint` is the
  published-page look. One-column also means the shared section files'
  `\begin{table}`/`\begin{figure}` never overflow a column, so no
  section file needed a PRA-specific edit.
- **`apsrev4-2.bst` (numbered).** Matches the plain `\cite{}` used
  throughout `sections/*.tex` — no `\citep`/`\citet`, so no natbib needed.
- **No `\orcid` macro in the .tex.** REVTeX 4.2 does not define `\orcid`
  (using it = "undefined control sequence"). Enter your ORCID in the
  submission portal's author metadata instead.
- **No PACS codes.** APS dropped the PACS requirement years ago.
- **No length limit.** Unlike PRL's 4-page cap, a regular PRA article has
  no strict length limit.

---

## BEFORE you submit — must do

1. **Compile `main-pra-flat.tex` on Overleaf** (New Project → Upload the
   zip, or paste the flat file + upload figures/bib). The sandbox LaTeX
   toolchain here cannot generate a format file (missing `mktexlsr.pl`),
   so this variant was **NOT compiled locally** — only statically
   verified (brace balance, no dangling `\input`, single `documentclass`,
   no undefined-macro / package-conflict patterns of the kind that broke
   the Foundations variant). A real compile is still required.

2. **Decide on the abstract.** `sections/00-abstract.tex` is
   multi-paragraph, contains 2 displayed equations and a bold inline
   header, and has 6 citations. REVTeX will compile it, but **APS style
   prefers a single-paragraph abstract with no display math and no
   citations.** Options: (a) leave as-is and risk an editorial nudge, or
   (b) produce a single-paragraph, no-display-math version for submission.
   *(Ask the agent to generate option (b) if you want it.)*

## Portal form fields (same content as the Foundations submission)

- **Title:** Relational Coherence Budgeting for Tunable Exchange Gates:
  Pointer-Basis Affinity, Decoherence, and Exchange-Angle Coherence Cost
- **Data availability:** Yes — simulation code at
  `https://github.com/dradams-lab/pub1-physics-rct` and archived at Zenodo,
  concept DOI `10.5281/zenodo.20130304`.
- **Dual publication:** No (the Zenodo deposit is a preprint/archive, not a
  prior publication; the paper was not accepted elsewhere).
- **Author contributions:** J.A. designed the study, developed the
  theoretical framework, performed the simulations, and wrote the
  manuscript.
- **Suggested referees / PACS:** not required.

---

## Note on the previous (Foundations of Physics) rejection

pub1 was desk-rejected by *Foundations of Physics* — most plausibly a
scope/fit issue (a practical gate-scheduling result is not the conceptual/
ontological work that journal selects for), not a quality or novelty
deficit. PRA's experimental-physics ethos is a better fit for a
gate-fidelity result. If the actual decision letter says otherwise (e.g.
a quality/novelty concern), revisit the framing before resubmitting.

## Math-verification status (this session)

The full mathematics was independently re-verified. One genuine error was
found and fixed: the decomposition break-even analysis (§6.6) assumed
`N_CNOT = 2` (Vatan–Williams' *real*/SO(4) special case, which does not
apply to `U_RA(θ)`); the correct generic count is **3** (Vidal–Dawson
2004), confirmed by Qiskit exact synthesis and a Makhlin-invariant
calculation. The break-even threshold and its conclusion were corrected
accordingly (commit on `main`). All simulation results (Tables I/II,
headline ΔF = +0.040 / +0.025) were reproduced and are correct.
