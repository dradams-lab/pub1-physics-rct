#!/usr/bin/env bash
# Flatten main-foundations.tex by inlining \input{sections/*.tex} so the
# result is a single self-contained .tex file suitable for Springer
# Nature submission (which requires single-file submissions).
#
# Usage: ./flatten-foundations.sh
# Output: main-foundations-flat.tex
#
# Prerequisites: just bash + sed (no LaTeX needed for this step).

set -euo pipefail

cd "$(dirname "$0")"

INPUT="main-foundations.tex"
OUTPUT="main-foundations-flat.tex"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: $INPUT not found in $(pwd)"
  exit 1
fi

# Work to a temp file then move into place atomically.
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# Add a header marker
cat > "$TMP" <<'EOF'
% ============================================================
% AUTO-GENERATED SUBMISSION FILE — DO NOT EDIT BY HAND.
%
% Generated from main.tex by make-submission.sh.
% This is the single-file flattened version for journal submission.
% Edit main.tex and the section files in sections/, then re-run
% make-submission.sh to regenerate this file.
% ============================================================

EOF

# Walk through main.tex line by line, inlining \input{sections/X}
# occurrences -- INCLUDING when \input{...} is nested inside another
# command on the same line (e.g. \abstract{\input{sections/00-abstract}}),
# which a whole-line-only match would silently skip, leaving a dangling
# \input in the flattened file that Editorial Manager's compiler cannot
# resolve (it has no sections/ directory -- confirmed by an actual failed
# compile: "File `sections/00-abstract-foundations.tex' not found").
while IFS= read -r line; do
  out_line="$line"
  # Repeatedly substitute each \input{sections/NAME} found anywhere in the
  # line (there may be more than one, though in practice at most one).
  while [[ "$out_line" =~ \\input\{sections/([^}]+)\} ]]; do
    section_name="${BASH_REMATCH[1]}"
    section_path="sections/${section_name}"
    if [[ ! -f "$section_path" && -f "${section_path}.tex" ]]; then
      section_path="${section_path}.tex"
    fi
    if [[ -f "$section_path" ]]; then
      section_content="$(cat "$section_path")"
      # Replace only the first occurrence of this exact \input{...} token.
      match="\\input{sections/${section_name}}"
      prefix="${out_line%%"$match"*}"
      suffix="${out_line#*"$match"}"
      out_line="${prefix}
% ─── Inlined from ${section_path} ───
${section_content}
% ─── End of ${section_path} ───
${suffix}"
    else
      echo "WARNING: section file not found for: $section_name (line: $line)" >&2
      break
    fi
  done
  echo "$out_line" >> "$TMP"
done < "$INPUT"

mv "$TMP" "$OUTPUT"
trap - EXIT

LINES_IN=$(wc -l < "$INPUT" | tr -d ' ')
LINES_OUT=$(wc -l < "$OUTPUT" | tr -d ' ')

echo "Wrote $OUTPUT ($LINES_OUT lines, expanded from $LINES_IN-line $INPUT)."
echo ""
echo "Next steps for submission:"
echo "  1. Compile $OUTPUT in Overleaf or pdflatex to verify clean build"
echo "  2. Submit $OUTPUT (renamed as desired) along with:"
echo "     - references.bib"
echo "     - figures/ directory"
echo "     - sn-jnl.cls"
echo "     - sn-basic.bst"
echo "     - any figures referenced in the body"
