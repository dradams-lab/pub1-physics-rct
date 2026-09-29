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
| `figures/` | 4 referenced figures: `fig1_affinity_decay.pdf`, `alpha-dynamics.pdf`, `fig3_rcb_sweep.pdf`, `fig4_alpha_varying.pdf` |
| `COVER-LETTER-pra.md` | Cover letter text to paste into the APS portal |

Upload `main-pra-flat.tex` + `references.bib` + the 4 figures. Regenerate
the flat file first with `bash flatten-pra.sh` (the script is not marked
executable).

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
- **ORCID via the `orcidlink` package.** REVTeX 4.2 has no native
  `\orcid` command (a bare `\orcid{}` = "undefined control sequence"). The
  documented RevTeX mechanism is `\orcidlink{iD}` in the author's name
  argument, provided by `\usepackage{orcidlink}` (loaded after hyperref +
  tikz, both of which it needs). Also enter your ORCID in the submission
  portal's author metadata. **Note:** `orcidlink` must be present in the
  Overleaf/APS TeX tree — it is in TeX Live and on Overleaf, so this is
  fine, but it is one more package the Overleaf compile will confirm.
- **No PACS codes.** APS dropped the PACS requirement years ago.
- **No length limit.** Unlike PRL's 4-page cap, a regular PRA article has
  no strict length limit.

---

## BEFORE you submit — must do

1. **Compile `main-pra-flat.tex` on Overleaf** (Integrations → GitHub →
   pull, then set Settings → Main document → `main-pra-flat.tex`,
   Recompile, and switch back afterwards). As of 2026-09-29 the PRA and
   Quantum builds were clean (0 errors, 0 overfull boxes) at `f092abe`;
   the §3/§4 correction (`cf3b32e`) and the Acknowledgments/AI disclosure
   added after it still need one compile.

2. **Read the Foundations of Physics decision letter** (see note below)
   before uploading.

3. **Confirm the AI-use disclosure** in `sections/08-acknowledgments.tex`
   is accurate as worded. APS expects AI-tool use to be disclosed; it is
   rendered as the Acknowledgments section in all three variants.

4. **Cover letter:** `COVER-LETTER-pra.md`.

Done: abstract is a single paragraph with no display math and no
citations (APS style).

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

pub1 was rejected by *Foundations of Physics*. **The actual decision
letter has not been read** (it went to contact@joshuaadams.dev; the
status portal only showed "rejected"), so the cause is not confirmed.
Three possibilities, none yet ruled out:

1. **Technical / compile failure.** The Foundations manuscript was never
   compiled locally (the sandbox LaTeX toolchain is broken), and the first
   Editorial-Manager attempts *did* throw real compile errors
   (`\orcidlogo` collision, missing `bigfoot`, `\bottomrule` undefined,
   dropped abstract file) that were fixed over two rounds. An uncompiled
   document or an unverified bibliography style is a very plausible source
   of a Technical Check flag. **This must be ruled out for PRA: compile
   `main-pra-flat.tex` on Overleaf before uploading (see above).**
2. **Editorial scope/fit.** A practical gate-scheduling result is not the
   conceptual/ontological work *Foundations of Physics* typically selects
   for; PRA's experimental-physics ethos fits a gate-fidelity result
   better. This is *a* plausible reason but is **not confirmed** and should
   not be treated as the established cause.
3. **Quality / novelty concern.** Also not ruled out.

**Action:** read the decision letter before assuming (2). If it cites a
technical/format problem, the fix is a clean compile, not a new journal;
if it cites scope/fit, PRA is well-justified; if it cites quality/novelty,
revisit the argument (note the §6.6 CNOT-count correction made this
session already strengthens the paper's rigor).

## Math-verification status (this session)

The full mathematics was independently re-verified. One genuine error was
found and fixed: the decomposition break-even analysis (§6.6) assumed
`N_CNOT = 2` (Vatan–Williams' *real*/SO(4) special case, which does not
apply to `U_RA(θ)`); the correct generic count is **3** (Vidal–Dawson
2004), confirmed by Qiskit exact synthesis and a Makhlin-invariant
calculation. The break-even threshold and its conclusion were corrected
accordingly (commit on `main`). All simulation results (Tables I/II,
headline ΔF = +0.040 / +0.025) were reproduced and are correct.
