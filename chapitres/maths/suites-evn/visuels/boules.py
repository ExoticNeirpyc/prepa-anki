import sys; sys.path.insert(0, "../../../../outils")
from fig import plt, np, C, sauver, virgules, axes_fleches

# Boules unités fermées de R² pour N1, N2, N∞
fig, ax = plt.subplots(figsize=(4.2, 4.2))
t = np.linspace(0, 2*np.pi, 400)
ax.fill([1, 0, -1, 0], [0, 1, 0, -1], color=C["c1"], alpha=0.10)
ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=C["c1"], label=r"$N_1$")
ax.plot(np.cos(t), np.sin(t), color=C["c3"], label=r"$N_2$")
ax.plot([1, -1, -1, 1, 1], [1, 1, -1, -1, 1], color=C["c2"], label=r"$N_\infty$")
axes_fleches(ax)
ax.set_xlim(-1.35, 1.45); ax.set_ylim(-1.35, 1.45); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for (x, y, lab) in [(1.08, -0.13, r"$1$"), (-1.12, -0.13, r"$-1$"), (0.07, 1.07, r"$1$"), (0.07, -1.17, r"$-1$")]:
    ax.text(x, y, lab, fontsize=12)
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.08), ncol=3, handlelength=1.2, columnspacing=0.8)
sauver(fig, "boules-unite")

# Partie bornée : contenue dans une boule pour chaque norme
fig, ax = plt.subplots(figsize=(3.8, 3.8))
th = np.linspace(0, 2*np.pi, 300)
r = 0.42 + 0.08*np.sin(3*th) + 0.05*np.cos(5*th)
ax.fill(r*np.cos(th)+0.05, r*np.sin(th), color=C["gris"], alpha=0.6)
ax.text(0.05, 0, r"$A$", ha="center", va="center", fontsize=15)
M = 0.62
ax.plot([M, -M, -M, M, M], [M, M, -M, -M, M], color=C["c2"], label=r"$\mathcal{B}_f^{(N_\infty)}(0,M)$")
R = M*np.sqrt(2)
ax.plot(R*np.cos(t), R*np.sin(t), color=C["c3"], label=r"$\mathcal{B}_f^{(N_2)}(0,\sqrt{2}M)$")
D = 2*M
ax.plot([D, 0, -D, 0, D], [0, D, 0, -D, 0], color=C["c1"], label=r"$\mathcal{B}_f^{(N_1)}(0,2M)$")
ax.set_aspect("equal"); ax.axis("off")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=1, fontsize=11)
sauver(fig, "partie-bornee")
