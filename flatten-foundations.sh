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

# Walk through main.tex line by line, inlining \input{sections/X} occurrences.
while IFS= read -r line; do
  # Match \input{sections/something} or \input{sections/something.tex}
  if [[ "$line" =~ ^[[:space:]]*\\input\{sections/([^}]+)\}[[:space:]]*$ ]]; then
    section_name="${BASH_REMATCH[1]}"
    # Try .tex suffix and bare name
    section_path="sections/${section_name}"
    if [[ ! -f "$section_path" && -f "${section_path}.tex" ]]; then
      section_path="${section_path}.tex"
    fi
    if [[ -f "$section_path" ]]; then
      echo "% ─── Inlined from $section_path ───" >> "$TMP"
      cat "$section_path" >> "$TMP"
      echo "" >> "$TMP"
      echo "% ─── End of $section_path ───" >> "$TMP"
      echo "" >> "$TMP"
    else
      echo "WARNING: section file not found for: $line" >&2
      echo "$line" >> "$TMP"
    fi
  else
    echo "$line" >> "$TMP"
  fi
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
echo "     - sn-mathphys.bst"
echo "     - any figures referenced in the body"
