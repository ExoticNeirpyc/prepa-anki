"""Style matplotlib commun aux visuels, et enregistrement en SVG.

Dans un script chapitres/…/visuels/nom.py :

    import sys; sys.path.insert(0, "outils")      # ou chemin absolu
    from fig import plt, np, C, sauver, virgules
    fig, ax = plt.subplots()
    ...
    sauver(fig, "nom")        # → chapitres/…/media/nom.svg

C1…C4 (dans C) sont les mêmes couleurs que les classes .c1…c4 des cartes.
Les figures sont transparentes : en mode sombre, Anki les inverse (noir ↔ blanc).
"""

import inspect
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as ticker  # noqa: E402
import numpy as np  # noqa: E402

C = {"c1": "#1F5FBF", "c2": "#C0392B", "c3": "#1E8449", "c4": "#7D3C98", "noir": "#1D1D1F", "gris": "#8E8E93"}

plt.rcParams.update({
    "figure.figsize": (5.2, 3.4),
    "figure.dpi": 100,
    "savefig.transparent": True,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "svg.fonttype": "path",
    "font.family": "serif",
    "font.serif": ["cmr10", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": True,
    "font.size": 13,
    "axes.labelsize": 14,
    "axes.titlesize": 14,
    "legend.fontsize": 12,
    "legend.frameon": False,
    "axes.edgecolor": C["noir"],
    "axes.labelcolor": C["noir"],
    "text.color": C["noir"],
    "xtick.color": C["noir"],
    "ytick.color": C["noir"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.0,
    "lines.linewidth": 2.0,
    "axes.prop_cycle": matplotlib.cycler(color=[C["c1"], C["c2"], C["c3"], C["c4"]]),
    "grid.color": "#C7C7CC",
    "grid.linewidth": 0.6,
})


def virgules(ax, x=True, y=True):
    """Séparateur décimal français (virgule) sur les graduations."""
    fmt = ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))
    if x:
        ax.xaxis.set_major_formatter(fmt)
    if y:
        ax.yaxis.set_major_formatter(fmt)


def axes_fleches(ax):
    """Axes en flèches passant par l'origine, à la manière d'un tracé de cours."""
    for cote in ("left", "bottom"):
        ax.spines[cote].set_position("zero")
    ax.plot(1, 0, ">", transform=ax.get_yaxis_transform(), clip_on=False, color=C["noir"], ms=6)
    ax.plot(0, 1, "^", transform=ax.get_xaxis_transform(), clip_on=False, color=C["noir"], ms=6)


def sauver(fig, nom, dossier=None):
    """Enregistre la figure en SVG dans le dossier media/ du chapitre du script appelant."""
    if dossier is None:
        appelant = Path(inspect.stack()[1].filename).resolve()
        base = appelant.parent.parent if appelant.parent.name == "visuels" else appelant.parent
        dossier = base / "media"
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / f"{nom}.svg"
    fig.savefig(chemin, format="svg")
    plt.close(fig)
    print(f"→ {chemin}")
    return chemin
