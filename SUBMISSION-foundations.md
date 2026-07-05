# Submission: Foundations of Physics (Springer Nature)

The **Foundations of Physics**-formatted version of the manuscript lives on `main` as `main-foundations.tex`, alongside the canonical pre-print `main.tex` (Quantum-journal-oriented) and the `submission-quantum` branch. To compile this version, set Overleaf's "Main document" to `main-foundations.tex` (Menu → Settings → Main document).

- **Journal**: [Foundations of Physics](https://link.springer.com/journal/10701) (Springer Nature)
- **Class**: `sn-jnl.cls` (committed in repo root)
- **Bibliography**: `sn-basic.bst` (numbered style, matching this paper's existing plain `\cite{}` usage — NOT `sn-mathphys.bst`, which is author-year and is what pub2 uses instead)
- **Publishing model**: Hybrid. Subscription route has **no author charges**; open-access route costs an APC of $3,690 USD (£2,490 GBP / €2,890 EUR) — choose subscription to submit at no cost. This choice is made *after* acceptance, not at submission time.
- **No arXiv requirement** — unlike Quantum, Foundations of Physics does not require a pre-existing arXiv deposit to submit.

## Differences from `main` / `submission-quantum`

| Element | `main` (Quantum-journal) | `main-foundations.tex` |
|---|---|---|
| Document class | `quantumarticle` (a4paper, onecolumn, 11pt) | `sn-jnl` (`pdflatex,sn-basic`) |
| Author block syntax | `\author{Dr. Joshua Adams}` + `\affiliation{}` + `\email{}` + `\orcid{}` | Springer's structured `\fnm{Joshua} \sur{Adams}` + `\affil*[1]{\orgname{Independent Researcher}}` |
| Abstract | `\begin{abstract}...\end{abstract}`, ~319 words, 2 display equations, 6 citations | `\abstract{...}` command, new file `sections/00-abstract-foundations.tex`, 247 words, **no equations, no citations** (Foundations of Physics requirement) |
| Keywords | not present | `\keywords{...}` (Springer expects this; 8 keywords added) |
| Bibliography style | `quantum.bst` | `sn-basic.bst` (numbered, matches existing `\cite{}` usage) |
| Appendix | `\appendix` | `\begin{appendices}...\end{appendices}` (sn-jnl's own environment) |
| Section files | `\input` works | `\input` works in our build but Springer **prefers single-file submission** — see "Flatten before submission" below |

## Section files unchanged

The 10 section files (9 body + 1 appendix) in `sections/` are imported via `\input{}` exactly as on `main`. Citations using plain `\cite{}` work because `sn-basic.bst` is a numbered style compatible with that syntax (no `\citep`/`\citet` are used anywhere in pub1's sections, confirmed by grep).

## Flatten before submission

Springer Nature's submission guidelines say not to use `\input{...}` to include other tex files — submit as one .tex document.

For day-to-day editing in Overleaf, keep `\input{}` for sanity. **Before submission**, generate a flattened single-file version using the included `flatten-foundations.sh` script (copied from pub2's setup; verify the section-file list at the top of the script matches pub1's 10 files before running):

```sh
./flatten-foundations.sh
# produces main-foundations-flat.tex with all sections inlined
```

Submit `main-foundations-flat.tex` (renamed to whatever you prefer) along with `references.bib`, `figures/`, `sn-jnl.cls`, and `sn-basic.bst`.

## Springer-specific things to verify before submitting

- [ ] Recompile in Overleaf to verify clean build (sn-jnl can be picky about package conflicts, e.g. `quantikz`/`physics`/`braket` alongside its own math setup) — **NOT YET DONE**; this file was authored in a sandbox without a working LaTeX toolchain (see note below)
- [x] Abstract length: rewritten to 247 words with no equations/citations, meeting the ≤250-word / no-equations / no-citations requirement
- [x] Keyword count: 8 keywords added (Springer prefers 4–8)
- [ ] Section numbering: ensure no double-numbering issues (Springer auto-numbers)
- [ ] Bibliography: verify `sn-basic.bst` formatting is acceptable for all 41 entries (some entry types may need tweaks)
- [ ] Figures: if any figures are added later, place inline and reference with `\ref{fig:...}` (Springer is strict about this)
- [ ] Appendix (`sections/A-rct-proof.tex`) renders correctly inside sn-jnl's `appendices` environment

## Submission checklist

- [ ] Recompile current branch in Overleaf — clean build
- [ ] Run `flatten-foundations.sh` to flatten
- [ ] Generate fresh PDF from flattened source
- [ ] Submit via Springer's [Editorial Manager](https://www.editorialmanager.com/foop/) for *Foundations of Physics*
- [ ] Cover letter mentions the Zenodo pre-print: `https://doi.org/10.5281/zenodo.20130304`
- [ ] Suggest reviewers (Springer's submission system asks for 3–5)
- [ ] Disclose pre-print status: "This manuscript has been deposited as a pre-print at Zenodo (DOI: 10.5281/zenodo.20130304)."
- [ ] Choose subscription (non-OA) publishing route after acceptance to avoid the $3,690 APC

## After submission

If accepted: update on `main` if any substantive edits are required, re-port to this file, tag a new release.

If rejected: review feedback, decide whether to revise on `main` and re-submit elsewhere (e.g., *Physical Review A* or *International Journal of Theoretical Physics*, per `PUBLICATION_STRATEGY.md`'s backup order).

## Toolchain note (as of this file's creation)

This variant's structure was verified by static checks only (balanced braces, all `\input` targets resolve, required packages declared, citation-command style matches `sn-basic`) — it has **not** been compiled. The sandbox used to author it has a broken `texlive-core` conda package (missing `mktexlsr.pl`, breaking `fmtutil`/format-file generation) and `tectonic` crashes on first-run bundle download due to a macOS network-API restriction. A real Overleaf compile is the first item on the checklist above for a reason.
