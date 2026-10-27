import sys; sys.path.insert(0, "../../../../outils")
from fig import plt, np, C, sauver, virgules, axes_fleches
from matplotlib.patches import Rectangle

f = lambda t: 1.6 / t
fig, axs = plt.subplots(1, 2, figsize=(6.6, 3.2))
for k, ax in enumerate(axs):
    t = np.linspace(1.05, 4.6, 300)
    ax.plot(t, f(t), color=C["noir"])
    n = 2.5
    if k == 0:
        ax.add_patch(Rectangle((n - 1, 0), 1, f(n), fc=C["c1"], alpha=0.25, ec=C["c1"], lw=1.4))
        ax.add_patch(Rectangle((n, 0), 1, f(n), fc=C["c2"], alpha=0.15, ec=C["c2"], lw=1.4))
        ax.set_xticks([n - 1, n, n + 1]); ax.set_xticklabels([r"$k-1$", r"$k$", r"$k+1$"])
        ax.set_yticks([f(n)]); ax.set_yticklabels([r"$f(k)$"])
        ax.set_title(r"$\int_k^{k+1}f\ \leq\ f(k)\ \leq\ \int_{k-1}^{k}f$", fontsize=15, pad=12)
    else:
        ax.add_patch(Rectangle((n, 0), 1, f(n), fc=C["c2"], alpha=0.15, ec=C["c2"], lw=1.4))
        ax.add_patch(Rectangle((n, 0), 1, f(n + 1), fc=C["c1"], alpha=0.25, ec=C["c1"], lw=1.4))
        ax.set_xticks([n, n + 1]); ax.set_xticklabels([r"$k$", r"$k+1$"])
        ax.set_yticks([f(n + 1), f(n)]); ax.set_yticklabels([r"$f(k+1)$", r"$f(k)$"])
        ax.set_title(r"$f(k+1)\ \leq\ \int_k^{k+1}f\ \leq\ f(k)$", fontsize=15, pad=12)
    ax.set_xlim(1, 4.7); ax.set_ylim(0, 1.75)
    ax.plot(1, 0, ">", transform=ax.transAxes, clip_on=False, color=C["noir"], ms=6)
    ax.plot(0, 1, "^", transform=ax.transAxes, clip_on=False, color=C["noir"], ms=6)
fig.tight_layout(w_pad=3)
sauver(fig, "serie-integrale")

# Dichotomie de Bolzano-Weierstrass
rng = np.random.default_rng(3)
u = np.clip(0.5 + 0.42 * np.sin(np.arange(1, 41) * 2.17) + 0.04 * rng.standard_normal(40), 0.02, 0.98)
fig, ax = plt.subplots(figsize=(6.2, 2.6))
a, b = 0.0, 1.0
for k in range(4):
    y = -k
    ax.plot([a, b], [y, y], color=C["c1"], lw=3, solid_capstyle="butt")
    ax.plot([a, a], [y - 0.13, y + 0.13], color=C["c1"], lw=1.5)
    ax.plot([b, b], [y - 0.13, y + 0.13], color=C["c1"], lw=1.5)
    ax.text(a - 0.03, y, rf"$a_{k}$", ha="right", va="center", fontsize=12)
    ax.text(b + 0.03, y, rf"$b_{k}$", ha="left", va="center", fontsize=12)
    m = (a + b) / 2
    gauche = np.sum((u >= a) & (u <= m)); droite = np.sum((u >= m) & (u <= b))
    if k < 3:
        ax.plot([m, m], [y - 0.2, y + 0.2], color=C["gris"], lw=1, ls=":")
        a, b = (a, m) if k % 2 == 0 else (m, b)
ax.text(1.32, -1.5, "à chaque étape, on garde\nune moitié contenant\nune infinité de termes",
        ha="left", va="center", fontsize=11, color=C["noir"], family="DejaVu Serif")
ax.set_xlim(-0.15, 2.1); ax.set_ylim(-3.5, 0.5); ax.axis("off")
sauver(fig, "bw-dichotomie")
