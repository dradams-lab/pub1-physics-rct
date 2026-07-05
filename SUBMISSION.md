# Submission: Quantum journal

This branch contains the **Quantum journal**-formatted version of the manuscript.

- **Journal**: [Quantum](https://quantum-journal.org)
- **Class**: `quantumarticle.cls` (committed in repo root)
- **Bibliography**: `quantum.bst` (committed in repo root)
- **License required by journal**: CC-BY 4.0 (we have it)

## Differences from `main` branch

The canonical pre-print version lives on `main` and uses the standard `revtex4-2` (PRA-style) class. This branch ports the LaTeX to the Quantum journal class:

| Element | `main` | `submission-quantum` |
|---|---|---|
| Document class | `revtex4-2` (`aps,pra,preprint`) | `quantumarticle` |
| Author block syntax | revtex `\author{}` `\email{}` `\affiliation{}` | quantumarticle `\author{}` + `\affiliation{}` + `\email{}` + `\orcid{}` |
| ORCID display | `\orcidlink` macro | built-in `\orcid` command |
| Bibliography style | revtex automatic | `quantum.bst` (Quantum's house style) |
| Section files | `\input` works | `\input` works (Quantum allows it) |

## Key class options used

```latex
\documentclass[a4paper,onecolumn,11pt,unpublished]{quantumarticle}
```

- `unpublished` — keeps Quantum branding off until the paper is accepted. Replace with `accepted=YYYY-MM-DD` after acceptance.
- `onecolumn` — easier reading during submission; switch to `twocolumn` for the final-style preview.

## Submission checklist

- [ ] Recompile in Overleaf to verify clean build
- [x] Check abstract length (Quantum prefers ≤ 350 words) — confirmed 337 words
- [ ] Verify all figures render correctly
- [ ] Check that bibliography compiles with `quantum.bst` (some entries may need format tweaks for the BST)
- [ ] Generate a fresh PDF
- [ ] Submit via Quantum's Scholastica-based system at [quantum-journal.scholasticahq.com](https://quantum-journal.scholasticahq.com/for-authors) (NOT ScholarOne — corrected after verification). Submission requires an arXiv reference (posted to or cross-listed with quant-ph); the paper cannot be submitted to Quantum before its arXiv deposit is live. No submission fee.
- [ ] Cover letter mentions the Zenodo pre-print: `https://doi.org/10.5281/zenodo.20130304`
- [ ] Suggest reviewers (Quantum's submission system asks for 3–5)

## After submission

If accepted: change documentclass option `unpublished` → `accepted=YYYY-MM-DD`. Rebuild PDF. Tag a new release on this branch.

If rejected: review the editorial feedback, update content on `main` if substantive changes are warranted, then re-port to the next target journal in a new branch (e.g., `submission-foundations` for backup).
