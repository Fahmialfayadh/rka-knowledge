#!/usr/bin/env bash
set -euo pipefail
# Convert PPT/PPTX/PPSX/DOCX -> PDF (PDF-only policy)
# Usage: ./scripts/convert_ppt_to_pdf.sh [src_dir] [out_base]
# Default src: scan for *.ppt*/*.docx under /home/data/kuliah/rka (excludes venv)
# Output: courses/<slug>/slides/pdf/

SRC_ROOT="/home/data/kuliah/rka"
OUT_BASE="/home/data/kuliah/rka-knowledge"
TMP_DIR="/tmp/rka-pdf-convert-$$"

mkdir -p "$TMP_DIR"

# Mapping: source pattern -> dest slug
declare -A MAP=(
  ["KK/ASSET_MATERI"]="kk"
  ["kka"]="kka"
  ["PAA"]="paa"
  ["probstat"]="probstat"
  ["tegrf"]="tegrf"
  ["ppt_fp_tegraf"]="tegrf"
)

# Collect files (exclude venv, .git, __pycache__, .godot)
echo "[*] Scanning for PPT/DOCX under $SRC_ROOT ..."
find "$SRC_ROOT" -type f \( -iname "*.pptx" -o -iname "*.ppt" -o -iname "*.ppsx" -o -iname "*.docx" \) \
  -not -path "*/.venv/*" \
  -not -path "*/venv-ppt/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.godot/*" \
  -not -path "*/aima-data/*" \
  -print0 | sort -z | while IFS= read -r -d '' f; do
  echo "  - $f"
done

echo ""
echo "[*] Converting with LibreOffice (soffice --headless) ..."

SUCCESS=0
FAIL=0
SKIP=0
declare -A SEEN

find "$SRC_ROOT" -type f \( -iname "*.pptx" -o -iname "*.ppt" -o -iname "*.ppsx" -o -iname "*.docx" \) \
  -not -path "*/.venv/*" \
  -not -path "*/venv-ppt/*" \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/.godot/*" \
  -not -path "*/aima-data/*" \
  -not -path "*/templates/default.pptx" \
  -print0 | sort -z | while IFS= read -r -d '' src; do

  # Skip duplicates & weird double extensions
  base=$(basename "$src")
  # Handle double extension .pptx.pptx, .pptx.pdf
  # Normalize: strip all known extensions sequentially
  norm_base="$base"
  # Remove .pdf suffix if it's .pptx.pdf
  if [[ "$norm_base" == *.pptx.pdf ]]; then
    norm_base="${norm_base%.pdf}"
  fi
  if [[ "$norm_base" == *.pptx.pptx ]]; then
    norm_base="${norm_base%.pptx}"
  fi

  # Determine slug from path
  slug=""
  for key in "${!MAP[@]}"; do
    if [[ "$src" == *"$key"* ]]; then
      slug="${MAP[$key]}"
      # Prefer more specific: kka/asset_ppt still -> kka, ppt_fp_tegraf -> tegrf
      break
    fi
  done
  # Special handling: files directly under tegrf vs ppt_fp_tegraf both -> tegrf
  if [[ -z "$slug" ]]; then
    slug="misc"
  fi

  # Special case: docx PAA -> paa
  if [[ "$src" == *"PAA"* ]]; then slug="paa"; fi
  if [[ "$src" == *"probstat"* ]]; then slug="probstat"; fi
  if [[ "$src" == *"tegrf"* ]] || [[ "$src" == *"ppt_fp_tegraf"* ]]; then slug="tegrf"; fi
  if [[ "$src" == *"KK/"* ]]; then slug="kk"; fi
  if [[ "$src" == *"kka/"* ]]; then slug="kka"; fi

  # Kebab-case output name: lower, spaces->-, dots->-, remove special
  out_name=$(echo "$norm_base" | sed -E 's/\.(pptx|ppt|ppsx|docx)$//I' | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-|-$//g')
  if [[ -z "$out_name" ]]; then out_name="slide"; fi
  out_name="${out_name}.pdf"

  dest_dir="$OUT_BASE/courses/$slug/slides/pdf"
  mkdir -p "$dest_dir"
  dest_path="$dest_dir/$out_name"

  # Deduplicate: if same out_name already produced, append counter
  if [[ -n "${SEEN[$dest_path]:-}" ]]; then
    # Add suffix
    base_noext="${out_name%.pdf}"
    c=2
    while [[ -n "${SEEN[$dest_dir/${base_noext}-${c}.pdf]:-}" ]] || [[ -f "$dest_dir/${base_noext}-${c}.pdf" ]]; do
      c=$((c+1))
    done
    out_name="${base_noext}-${c}.pdf"
    dest_path="$dest_dir/$out_name"
  fi

  # Skip if dest already exists (idempotent)
  if [[ -f "$dest_path" ]]; then
    echo "[SKIP] exists: $dest_path  <- $src"
    SEEN["$dest_path"]=1
    continue
  fi

  echo "[CONVERT] $src -> $dest_path"
  # Clean tmp
  rm -f "$TMP_DIR"/*

  if timeout 90 soffice --headless --convert-to pdf --outdir "$TMP_DIR" "$src" >/dev/null 2>&1; then
    # Find generated pdf in TMP_DIR
    gen_pdf=$(find "$TMP_DIR" -maxdepth 1 -name "*.pdf" | head -1)
    if [[ -n "$gen_pdf" && -f "$gen_pdf" ]]; then
      mv "$gen_pdf" "$dest_path"
      echo "  [OK] $dest_path ($(du -h "$dest_path" | cut -f1))"
      SEEN["$dest_path"]=1
    else
      echo "  [FAIL] no pdf generated for $src"
      FAIL=$((FAIL+1))
    fi
  else
    echo "  [FAIL] soffice error for $src"
    FAIL=$((FAIL+1))
  fi
done

echo ""
echo "[*] Done. Check courses/*/slides/pdf/"
find "$OUT_BASE/courses" -path "*/slides/pdf/*.pdf" -type f -exec ls -lh {} \; 2>/dev/null | awk '{print $9, $5}'
echo ""
echo "[*] Total PDFs:"
find "$OUT_BASE/courses" -path "*/slides/pdf/*.pdf" -type f | wc -l
rm -rf "$TMP_DIR"
