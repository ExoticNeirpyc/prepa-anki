#!/usr/bin/env bash
# Installe tout ce qu'il faut pour les outils. Sans effet si tout est déjà là.
set -e
CACHE="$HOME/.cache/prepa-anki"

if ! command -v pdflatex >/dev/null || ! kpsewhich simplekv.tex >/dev/null 2>&1; then
  echo "Installation de LaTeX (quelques minutes)…"
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
    texlive-latex-base texlive-latex-extra texlive-pictures texlive-science \
    texlive-fonts-recommended texlive-lang-french texlive-luatex texlive-plain-generic \
    poppler-utils ghostscript >/dev/null
fi

if ! python3 -c "import pymupdf, genanki, matplotlib, cv2, zstandard" 2>/dev/null; then
  echo "Installation des bibliothèques Python…"
  pip install --break-system-packages -q pymupdf genanki matplotlib numpy scipy pillow \
    opencv-python-headless zstandard rdkit 2>&1 | grep -v "^WARNING" || true
fi

if [ ! -f "$CACHE/node_modules/mathjax/es5/tex-chtml-full.js" ]; then
  echo "Installation de MathJax…"
  mkdir -p "$CACHE"
  (cd "$CACHE" && npm install --silent --no-save mathjax@3.2.2 >/dev/null)
fi

echo "Outils prêts."
