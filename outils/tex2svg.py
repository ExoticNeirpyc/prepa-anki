#!/usr/bin/env python3
"""Compile des visuels LaTeX (TikZ, circuitikz, chemfig, pgfplots…) en SVG.

Un fichier .tex peut contenir un document complet (\\documentclass…) ou seulement le
dessin : il est alors placé dans un document « standalone » avec les paquets usuels
(voir PREAMBULE). Une ligne « % preambule: … » ajoute du préambule au cas par cas.
Un fichier placé à côté de la source peut être inclus avec \\input{nom} (macros communes
à plusieurs visuels d'un même chapitre, par exemple).

Par défaut, chapitres/…/visuels/nom.tex produit chapitres/…/media/nom.svg.

Exemples :
  python3 outils/tex2svg.py chapitres/chimie/x/visuels/mecanisme.tex
  python3 outils/tex2svg.py chapitres/physique/y/visuels/*.tex --echelle 1.6
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PREAMBULE = r"""\documentclass[border=3pt,varwidth=false]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,mathtools,bm}
\providecommand{\vv}[1]{\overrightarrow{#1}}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc,positioning,decorations.pathmorphing,decorations.markings,
  decorations.pathreplacing,patterns,shapes,3d,angles,quotes,intersections,backgrounds,fit}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage[european,straightvoltages]{circuitikz}
\usepackage{chemfig}
\usepackage[version=4]{mhchem}
\usepackage{siunitx}
\sisetup{locale=FR}
\definecolor{c1}{HTML}{1F5FBF}
\definecolor{c2}{HTML}{C0392B}
\definecolor{c3}{HTML}{1E8449}
\definecolor{c4}{HTML}{7D3C98}
% Dessin de molécules en TikZ (formules topologiques) :
%   \coin{A}{B}       liaison en coin plein de A (étroit) vers B (large)
%   \hach{A}{B}       liaison hachurée de A vers B
%   \dbl{A}{B}{90}    trait intérieur d'une double liaison A–B, décalé du côté +90° (ou -90)
\tikzset{every picture/.append style={line cap=round, line join=round, line width=0.75pt}}
\newcommand{\coin}[2]{\fill let \p1=($(#2)-(#1)$), \n1={atan2(\y1,\x1)} in
  (#1) -- ($(#2)+(\n1+90:0.075)$) -- ($(#2)+(\n1-90:0.075)$) -- cycle;}
\newcommand{\hach}[2]{\foreach \t in {0.14,0.28,...,1.0}{\draw[line width=0.55pt] let \p1=($(#2)-(#1)$),
  \n1={atan2(\y1,\x1)} in ($(#1)!\t!(#2)+(\n1+90:0.075*\t)$) -- ($(#1)!\t!(#2)+(\n1-90:0.075*\t)$);}}
\newcommand{\dbl}[3]{\draw ($($(#1)!0.17!(#2)$)!0.11cm!#3:(#2)$) -- ($($(#2)!0.17!(#1)$)!0.11cm!-#3:(#1)$);}
"""


def document(source):
    if r"\documentclass" in source:
        return source
    extra = "\n".join(re.findall(r"^%\s*preambule:\s*(.*)$", source, re.M))
    return PREAMBULE + extra + "\n\\begin{document}\n" + source + "\n\\end{document}\n"


def agrandir(svg, echelle):
    """Dimensions de pdftocairo (en points, sans unité) → pixels, multipliées par l'échelle."""
    def f(m):
        return f'{m.group(1)}="{float(m.group(2)) * echelle * 4 / 3:.2f}px"'
    m = re.search(r"<svg\b[^>]*>", svg)
    tete = re.sub(r'\b(width|height)="([\d.]+)(?:pt)?"', f, m.group(0))
    return svg[:m.start()] + tete + svg[m.end():]


def compiler(tex, sortie, echelle, moteur):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "v.tex").write_text(document(tex.read_text(encoding="utf-8")), encoding="utf-8")
        # Deux passes quand des nœuds sont mémorisés entre dessins (\chemmove, remember picture).
        passes = 2 if re.search(r"chemmove|remember picture", tex.read_text(encoding="utf-8")) else 1
        for _ in range(passes):
            r = subprocess.run([moteur, "-interaction=nonstopmode", "-halt-on-error", "v.tex"],
                               cwd=tmp, capture_output=True, text=True,
                               env={**os.environ, "TEXINPUTS": f"{tex.resolve().parent}:"})
            if r.returncode != 0:
                break
        if r.returncode != 0:
            log = (tmp / "v.log").read_text(errors="replace") if (tmp / "v.log").exists() else r.stdout
            erreurs = [l for l in log.splitlines() if l.startswith("!") or l.startswith("l.")]
            print(f"ÉCHEC {tex} :\n  " + "\n  ".join(erreurs[:12] or log.splitlines()[-15:]),
                  file=sys.stderr)
            return False
        subprocess.run(["pdftocairo", "-svg", "v.pdf", "v.svg"], cwd=tmp, check=True)
        svg = (tmp / "v.svg").read_text()
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(agrandir(svg, echelle))
    print(f"{tex} → {sortie}")
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichiers", nargs="+", type=Path)
    p.add_argument("-o", "--sortie", type=Path, help="fichier .svg (un seul fichier source)")
    p.add_argument("--echelle", type=float, default=1.4,
                   help="facteur d'affichage (défaut 1.4 : texte 10 pt ≈ texte des cartes)")
    p.add_argument("--moteur", default="pdflatex", choices=["pdflatex", "lualatex"])
    a = p.parse_args()
    if a.sortie and len(a.fichiers) > 1:
        p.error("-o n'est possible qu'avec un seul fichier")
    if not shutil.which(a.moteur):
        sys.exit(f"{a.moteur} absent : lancer bash outils/installer.sh")
    ok = True
    for tex in a.fichiers:
        if a.sortie:
            sortie = a.sortie
        elif tex.parent.name == "visuels":
            sortie = tex.parent.parent / "media" / (tex.stem + ".svg")
        else:
            sortie = tex.with_suffix(".svg")
        ok &= compiler(tex, sortie, a.echelle, a.moteur)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
