"""Courbes calculées du chapitre MF5 (python3 courbes.py depuis n'importe où)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "outils"))
from fig import plt, np, C, sauver  # noqa: E402


def nu(ax):
    """Axes nus : on garde seulement le tracé."""
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def fleche(ax, x0, y0, x1, y1, coul=C["noir"], txt=None, **kw):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=coul, lw=1.6, mutation_scale=14))
    if txt:
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, txt, color=coul, ha="center", **kw)


def cote(ax, x0, x1, y, txt, coul=C["noir"]):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="<|-|>", color=coul, lw=1.2, mutation_scale=11))
    ax.text((x0 + x1) / 2, y + 0.08, txt, color=coul, ha="center", va="bottom")


# 1. Ondes longitudinale et transversale sur une chaîne de points
def types_ondes():
    fig, axs = plt.subplots(2, 1, figsize=(6.2, 3.6))
    xn = np.arange(0, 12.01, 0.4)
    k = 2 * np.pi / 6
    ax = axs[0]
    ax.plot(xn + 0.28 * np.sin(k * xn), 0 * xn, "o", color=C["c1"], ms=5)
    ax.set_title("onde longitudinale (ex. : son dans une tige)", fontsize=12, loc="left")
    fleche(ax, 12.6, 0, 14.0, 0, C["c2"]); ax.text(13.3, 0.25, "propagation", color=C["c2"], ha="center", fontsize=10)
    ax.annotate("", xy=(1.0, -0.42), xytext=(0.2, -0.42), arrowprops=dict(arrowstyle="<|-|>", color=C["c3"], lw=1.4))
    ax.text(0.6, -0.95, "vibration", color=C["c3"], ha="center", fontsize=10)
    ax.set_xlim(-0.5, 14.3); ax.set_ylim(-1.1, 0.7); nu(ax)
    ax = axs[1]
    ax.plot(xn, 0.6 * np.sin(k * xn), "o", color=C["c1"], ms=5)
    ax.set_title("onde transversale (ex. : corde vibrante)", fontsize=12, loc="left")
    fleche(ax, 12.6, 0, 14.0, 0, C["c2"]); ax.text(13.3, 0.25, "propagation", color=C["c2"], ha="center", fontsize=10)
    ax.annotate("", xy=(-0.3, 0.6), xytext=(-0.3, -0.6), arrowprops=dict(arrowstyle="<|-|>", color=C["c3"], lw=1.4))
    ax.text(-0.15, -1.05, "vibration", color=C["c3"], ha="left", fontsize=10)
    ax.set_xlim(-0.5, 14.3); ax.set_ylim(-1.15, 0.9); nu(ax)
    fig.tight_layout()
    sauver(fig, "types-ondes")


# 2. Approximation des milieux continus
def milieux_continus():
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    x = np.linspace(0, 10, 500)
    lam = 5.0
    ax.plot(x, np.cos(2 * np.pi * x / lam), color=C["gris"], lw=1.2, label=r"$u(x,t)$ à $t$ fixé")
    xn = np.arange(0, 10.01, 0.25)
    ax.plot(xn, np.cos(2 * np.pi * xn / lam), "o", color=C["c1"], ms=4, label=r"$u_n(t)$ en $x_n=na$")
    cote(ax, 0, lam, 1.25, r"$\lambda$")
    ax.annotate("", xy=(3.0, -1.32), xytext=(2.75, -1.32), arrowprops=dict(arrowstyle="<|-|>", color=C["c2"], lw=1.1, mutation_scale=8))
    ax.text(2.88, -1.62, r"$a$", color=C["c2"], ha="center")
    ax.set_xlim(-0.2, 10.4); ax.set_ylim(-1.8, 1.8)
    ax.set_xlabel(r"$x$", loc="right"); nu(ax)
    ax.axhline(0, color=C["noir"], lw=0.8)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=10)
    sauver(fig, "milieux-continus")


# 3. Translation d'une impulsion s(x - ct)
def impulsion():
    fig, ax = plt.subplots(figsize=(5.6, 2.4))
    x = np.linspace(0, 10, 600)
    s = lambda X: np.exp(-((X - 2.5) / 0.7) ** 2)
    ax.plot(x, s(x), color=C["c1"]); ax.text(2.5, 1.08, r"à $t$", color=C["c1"], ha="center")
    ax.plot(x, s(x - 4.5), color=C["c2"]); ax.text(7.0, 1.08, r"à $t+\Delta t$", color=C["c2"], ha="center")
    ax.annotate("", xy=(7.0, 0.5), xytext=(2.5, 0.5), arrowprops=dict(arrowstyle="-|>", color=C["noir"], lw=1.2, ls="--"))
    ax.text(4.75, 0.58, r"$\Delta x = c\,\Delta t$", ha="center")
    ax.axhline(0, color=C["noir"], lw=0.8)
    ax.text(10.1, -0.05, r"$x$", va="top")
    ax.set_ylim(-0.15, 1.35); nu(ax)
    sauver(fig, "impulsion")


# 4. Double périodicité de l'OPPH
def opph():
    fig, axs = plt.subplots(2, 1, figsize=(5.0, 4.2))
    u = np.linspace(0, 2.3, 400)
    for ax, var, per, titre in ((axs[0], r"$x$", r"$\lambda$", r"$t$ fixé"), (axs[1], r"$t$", r"$T$", r"$x$ fixé")):
        ax.plot(u, np.cos(2 * np.pi * u - 0.6), color=C["c1"])
        ax.axhline(0, color=C["noir"], lw=0.8)
        a0 = 0.6 / (2 * np.pi)
        cote(ax, a0, a0 + 1, 1.12, per, C["c2"])
        ax.text(2.35, -0.08, var, va="top")
        ax.set_title(titre, fontsize=12)
        ax.text(-0.05, 1.0, r"$\psi$", ha="right")
        ax.set_ylim(-1.2, 1.55); ax.set_xlim(-0.1, 2.5); nu(ax)
        ax.axvline(0, color=C["noir"], lw=0.8, ymax=0.8)
    fig.tight_layout()
    sauver(fig, "opph")


# 5. Instantanés d'une OSH
def osh():
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    x = np.linspace(0, 2, 500)
    for ph, al in ((0, 1), (0.6, 0.75), (1.1, 0.55), (np.pi - 1.1, 0.55), (np.pi - 0.6, 0.75), (np.pi, 1)):
        ax.plot(x, np.cos(ph) * np.sin(2 * np.pi * x), color=C["c1"], lw=1.4, alpha=al)
    ax.axhline(0, color=C["noir"], lw=0.8)
    for xn in (0, 0.5, 1, 1.5, 2):
        ax.plot(xn, 0, "o", color=C["c2"], ms=6, zorder=5)
    for xv in (0.25, 0.75, 1.25, 1.75):
        ax.plot([xv, xv], [-1, 1], color=C["c3"], ls=":", lw=1.2)
    ax.annotate("nœud", xy=(1.0, 0), xytext=(1.0, 1.25), color=C["c2"], ha="center",
                arrowprops=dict(arrowstyle="-|>", color=C["c2"], lw=1))
    ax.text(0.75, 1.08, "ventre", color=C["c3"], ha="center")
    cote(ax, 1.0, 1.5, -1.38, "", C["noir"]); ax.text(1.25, -1.33, r"$\lambda/2$", ha="center", va="bottom")
    cote(ax, 0.25, 0.75, -1.38, "", C["noir"]); ax.text(0.5, -1.33, r"$\lambda/2$", ha="center", va="bottom")
    ax.text(2.06, -0.06, r"$x$", va="top")
    ax.set_ylim(-1.5, 1.45); ax.set_xlim(-0.05, 2.15); nu(ax)
    sauver(fig, "osh")


# 6. Modes propres de la corde fixée aux deux extrémités
def modes():
    fig, axs = plt.subplots(3, 1, figsize=(5.6, 4.6))
    x = np.linspace(0, 1, 400)
    for n, ax in zip((1, 2, 3), axs):
        for ph in np.linspace(0, np.pi, 7):
            ax.plot(x, np.cos(ph) * np.sin(n * np.pi * x), color=C["c1"], lw=1.0, alpha=0.65)
        ax.plot(x, np.sin(n * np.pi * x), color=C["c1"], lw=2)
        for p in range(n + 1):
            ax.plot(p / n, 0, "o", color=C["c2"], ms=6, zorder=5)
        for p in range(n):
            ax.plot((p + 0.5) / n, 0, "s", color=C["c3"], ms=5, zorder=5)
        nom = "fondamental" if n == 1 else f"harmonique {n}"
        ax.text(1.04, 0, f"$n={n}$ ({nom})\n" + (r"$L=\lambda_1/2$" if n == 1 else rf"$L={n}\,\lambda_{n}/2$"), va="center", fontsize=11)
        ax.set_xlim(-0.03, 1.75); ax.set_ylim(-1.15, 1.15); nu(ax)
        ax.plot([0, 0], [-0.6, 0.6], color=C["noir"], lw=3); ax.plot([1, 1], [-0.6, 0.6], color=C["noir"], lw=3)
    axs[2].text(0.0, -1.1, r"$x=0$", ha="center", va="top", fontsize=11)
    axs[2].text(1.0, -1.1, r"$x=L$", ha="center", va="top", fontsize=11)
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], ls="", marker="o", color=C["c2"], label="nœud"),
                        Line2D([], [], ls="", marker="s", color=C["c3"], label="ventre")],
               loc="lower right", ncol=2, fontsize=10)
    fig.tight_layout()
    sauver(fig, "modes")


# 7. Spectre d'une corde pincée en x = d (sans vitesse initiale)
def spectre():
    L, d = 1.0, 0.25
    fig, axs = plt.subplots(2, 1, figsize=(5.0, 4.6))
    ax = axs[0]
    ax.plot([0, d, L], [0, 1, 0], color=C["c1"])
    ax.plot([0, L], [0, 0], color=C["noir"], lw=0.8)
    ax.set_title(r"$y(x,0)=a(x)$", fontsize=12)
    ax.text(d, -0.12, r"$L/4$", ha="center", va="top", fontsize=11); ax.text(L, -0.12, r"$L$", ha="center", va="top", fontsize=11)
    ax.plot([d, d], [0, 1], color=C["gris"], ls=":", lw=1)
    ax.set_ylim(-0.4, 1.2); nu(ax)
    ax = axs[1]
    n = np.arange(1, 13)
    A = np.abs(np.sin(n * np.pi * d / L) / n ** 2)
    A /= A[0]
    ax.vlines(n, 0, A, color=C["c2"], lw=2.5)
    ax.set_xticks(n); ax.set_xticklabels([r"$f_1$"] + [rf"${i}f_1$" if i in (2, 4, 8) else "" for i in n[1:]], fontsize=10)
    ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(["0", "0,5", "1"])
    ax.set_ylabel(r"$|A_n|/|A_1|$", fontsize=11)
    ax.set_title("spectre", fontsize=12)
    ax.set_xlim(0.3, 12.7)
    fig.tight_layout()
    sauver(fig, "spectre")


# 8. Amplitude des ventres de la corde de Melde (modèle sans amortissement)
def resonance():
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    r = np.linspace(0.02, 3.6, 4000)
    A = 1 / np.abs(np.sin(np.pi * r))
    A[A > 12] = np.nan
    ax.plot(r, A, color=C["c1"])
    for n in (1, 2, 3):
        ax.axvline(n, color=C["c2"], ls="--", lw=1)
    ax.axhline(1, color=C["gris"], ls=":", lw=1)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(["0", r"$f_1$", r"$2f_1$", r"$3f_1$"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["0", r"$a$"])
    ax.set_xlabel(r"$f$ du vibreur", loc="right")
    ax.set_ylabel(r"$\dfrac{a}{|\sin kL|}$", rotation=0, labelpad=26)
    ax.set_ylim(0, 12.5); ax.set_xlim(0, 3.65)
    sauver(fig, "resonance")


# 9. Aspects de la corde de Melde (d'après la figure 4 du cours)
def melde(etiquettes, nom):
    fig, axs = plt.subplots(3, 1, figsize=(6.0, 4.4))
    x = np.linspace(0, 1, 400)
    cas = [(2.6, 0.18), (1, 1.0), (2, 1.0)]  # (f/f1, amplitude affichée)
    legendes = ["fréquence quelconque", "1re résonance ($f=f_1$)", "2e résonance ($f=2f_1$)"]
    for i, (ax, (r, amp)) in enumerate(zip(axs, cas)):
        if i == 0:
            env = np.abs(np.sin(np.pi * r * (x - 1)) / np.sin(np.pi * r)) * amp
            forme = np.sin(np.pi * r * (x - 1)) / np.sin(np.pi * r) * amp
        else:
            env = np.abs(np.sin(r * np.pi * x)) * amp * 0.97 + 0.03 * amp * (1 - x)
            forme = (np.sin(r * np.pi * x) * 0.97 + 0.03 * (1 - x)) * amp * (-1 if r == 1 else 1)
        for c in np.linspace(-1, 1, 9):
            ax.plot(x, c * forme, color=C["c1"], lw=0.8, alpha=0.7)
        ax.fill_between(x, -env, env, color=C["c1"], alpha=0.12, lw=0)
        ax.plot([-0.03, -0.03], [-1.1, 1.1], color=C["gris"], lw=5)
        ax.text(-0.09, 0, f"({i + 1})", ha="right", va="center", fontsize=12)
        if etiquettes:
            ax.text(1.04, 0, legendes[i], va="center", fontsize=11)
        ax.set_xlim(-0.2, 1.75 if etiquettes else 1.05); ax.set_ylim(-1.15, 1.15); nu(ax)
    axs[2].text(0, -1.15, r"vibreur ($x=0$)", ha="left", va="top", fontsize=10)
    axs[2].text(1, -1.15, r"poulie ($x=L$)", ha="center", va="top", fontsize=10)
    fig.tight_layout()
    sauver(fig, nom)


types_ondes(); milieux_continus(); impulsion(); opph(); osh(); modes(); spectre(); resonance()
melde(False, "melde-recto"); melde(True, "melde-verso")
