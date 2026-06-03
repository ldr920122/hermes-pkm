#!/bin/bash
# batch_wiki_to_html.sh — Convert Obsidian wiki/ markdown files to HTML
# Usage: bash batch_wiki_to_html.sh [wiki_dir] [theme]
#
# Default: wiki_dir=VAULT/wiki, theme=article
# Output: 00-{basename}.html in same directory (00- prefix sorts first in Obsidian)
#
# Excludes: index.md, log.md, overview.md, README.md, entities/, sources/, topics/
# Skips: files < 200 bytes, already-up-to-date HTML files

WIKI_DIR="${1:-/Users/wbaoc/Documents/Obsidian/wbaoc-wiki/wiki}"
THEME="${2:-article}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Find md_to_html.py relative to this script, or fall back to skill path
if [ -f "$SCRIPT_DIR/md_to_html.py" ]; then
  SCRIPT="$SCRIPT_DIR/md_to_html.py"
else
  SCRIPT="/Users/wbaoc/.hermes/skills/huashu-md-html/scripts/md_to_html.py"
fi

SUCCESS=0
FAIL=0
SKIP=0

echo "=== Batch Wiki → HTML ==="
echo "Source: $WIKI_DIR"
echo "Theme: $THEME"
echo "Script: $SCRIPT"
echo ""

find "$WIKI_DIR" -name '*.md' -type f \
  ! -name '00-*' \
  ! -name 'index.md' \
  ! -name 'log.md' \
  ! -name 'overview.md' \
  ! -name 'README.md' \
  ! -path '*/entities/*' \
  ! -path '*/sources/*' \
  ! -path '*/topics/*' \
  | sort | while read -r md_file; do

  # Skip small files
  size=$(wc -c < "$md_file" | tr -d ' ')
  if [ "$size" -lt 200 ]; then
    echo "[SKIP] $(basename "$md_file") (${size}B, too small)"
    SKIP=$((SKIP + 1))
    continue
  fi

  dir=$(dirname "$md_file")
  base=$(basename "$md_file" .md)
  html_file="$dir/00-${base}.html"

  # Skip if HTML already newer than md
  if [ -f "$html_file" ]; then
    if [ "$html_file" -nt "$md_file" ]; then
      echo "[SKIP] 00-${base}.html (up to date)"
      SKIP=$((SKIP + 1))
      continue
    fi
  fi

  result=$(python3 "$SCRIPT" "$md_file" --theme "$THEME" -o "$html_file" 2>&1)
  if [ $? -eq 0 ]; then
    echo "[OK]   ${base}.md → 00-${base}.html"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "[FAIL] ${base}.md"
    FAIL=$((FAIL + 1))
  fi
done

echo ""
echo "=== Done ==="
