# Submission: International Journal of Theoretical Physics (Springer Nature)

The **IJTP**-formatted version lives on `main` as `main-ijtp.tex`. It is built from
`main-foundations.tex` (same publisher, same template) and keeps every fix from the
Foundations of Physics Editorial Manager compiles. To compile it in Overleaf, set
Menu → Settings → **Main document** to `main-ijtp.tex`, recompile, then switch back.

- **Journal:** [International Journal of Theoretical Physics](https://link.springer.com/journal/10773) (Springer Nature)
- **Why IJTP:** backup #3 in `PUBLICATION_STRATEGY.md` ("broader scope, lower
  competition"); it accepts theoretical work with foundational framing, and its
  hybrid model has a free subscription route, which fits the no-APC rule.
- **Class / bibliography:** `sn-jnl.cls` with `sn-basic.bst` (numbered, matching
  pub1's plain `\cite{}`), exactly as in the Foundations variant.

## Step 0 — before anything else: read the Foundations of Physics decision letter

pub1 was rejected by *Foundations of Physics*, and the decision letter has never been
read (see `SUBMISSION-pra.md`). Log in to Foundations of Physics' Editorial Manager
and read it.

- [ ] **If it cites scope or fit:** IJTP is the right next step; carry on.
- [ ] **If it cites quality or novelty:** address that first, or IJTP will likely say
      the same.
- [ ] **Look for a transfer offer.** Springer rejection letters often offer to move the
      submission to another Springer journal. If IJTP (or *Quantum Studies:
      Mathematics and Foundations*) is offered, accepting the transfer is faster than
      a fresh submission.

## What differs from the Foundations variant

| Element | `main-foundations.tex` | `main-ijtp.tex` |
|---|---|---|
| Template and compile fixes | `sn-jnl`, `bigfoot`, `\botrule` alias, ORCID glyph | identical |
| Abstract | `sections/00-abstract-foundations.tex` (211 words, no equations or citations) | same file |
| Keywords | 8 | same 8 |
| Declarations | none | **added:** Funding, Competing interests, Data and code availability, Author contributions |
| Flatten script | `flatten-foundations.sh` | `flatten-ijtp.sh` → `main-ijtp-flat.tex` |

## Requirements to confirm on IJTP's own page

I could not open Springer's site from the session that built this variant, so these
follow Springer Nature's standard requirements and need a quick check against
IJTP's [submission guidelines](https://link.springer.com/journal/10773/submission-guidelines):

- [ ] Abstract length (Springer's usual limit is 150–250 words; ours is 211)
- [ ] Number of keywords (ours: 8)
- [ ] Required declarations and their headings (Springer asks at minimum for Funding
      and Competing interests)
- [ ] LaTeX: single-file source accepted, and whether `sn-basic` is acceptable
      (Springer re-typesets references in production)
- [ ] Publishing model: confirm the subscription route has no author charge; choose it
      after acceptance
- [ ] Preprint policy (Springer generally permits preprints; disclose the Zenodo DOI)
- [ ] AI policy: Springer requires use of large language models to be documented and
      not listed as an author. pub1's acknowledgments already declare it in detail.

## Before uploading

- [ ] Overleaf: set Main document to `main-ijtp.tex` and recompile — 0 errors
- [ ] Confirm the **Funding** and **Competing interests** statements in `main-ijtp.tex`
      are accurate (written as "no funding" and "no competing interests")
- [ ] Regenerate the upload file after any edit: `bash flatten-ijtp.sh`
- [ ] Upload `main-ijtp-flat.tex`, `references.bib`, the four figure PDFs
      (`alpha-dynamics`, `fig1_affinity_decay`, `fig3_rcb_sweep`, `fig4_alpha_varying`),
      `sn-jnl.cls` and `sn-basic.bst`
- [ ] Suggested reviewers, if the system asks (optional)
- [ ] Cover letter (draft below)

## Cover letter (draft — edit for your voice)

> Dear Editors,
>
> I submit "Relational Coherence Budgeting for Tunable Exchange Gates: Pointer-Basis
> Affinity, Decoherence, and Exchange-Angle Coherence Cost" for consideration as a
> regular article in the *International Journal of Theoretical Physics*.
>
> The paper restates standard results of pointer-basis coherence theory in terms of a
> normalized coherence quantifier and proves a closed-form allocation theorem for
> tunable Heisenberg-exchange gates: under Markovian dephasing and a fixed
> entanglement target, the cost-minimizing schedule of exchange angles is unique.
> Density-matrix simulations show fidelity gains of up to 0.040 over a single full
> entangler. The discussion states the limits of the result, including its dependence
> on direct gate calibration and on how coherence varies between layers.
>
> The manuscript is deposited as a preprint on Zenodo
> (https://doi.org/10.5281/zenodo.20130304), and the simulation code is public. It is
> not under consideration elsewhere. [Optional: mention the earlier *Foundations of
> Physics* submission and what has changed since.] The use of AI assistance is
> declared in the acknowledgments.
>
> Sincerely,
> Joshua Adams

## After submission

- **Accepted:** choose the subscription route (no charge), then tag a release.
- **Rejected:** next free options, in order: *Quantum Studies: Mathematics and
  Foundations* (Springer, same template, so this variant needs only its journal name
  changed), then *Quantum Information Processing* (lead with the scheduling result).

## Build status

Not compiled locally (no TeX on this machine). Static checks on `main-ijtp-flat.tex`
passed: balanced braces and environments, one `\documentclass`, no leftover `\input`,
all 45 citation keys in `references.bib`, all 58 cross-references resolve, all four
figures present. The Overleaf compile is the real test.
