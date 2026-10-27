import sys; sys.path.insert(0, "../../../../outils")
from fig import plt, np, C, sauver, virgules, axes_fleches


def escalier(ax, f, u0, n, couleur):
    u = u0
    xs, ys = [u], [0]
    for _ in range(n):
        v = f(u)
        xs += [u, v]; ys += [v, v]
        u = v
    ax.plot(xs, ys, color=couleur, lw=1.3)
    ax.plot([u0], [0], "o", color=couleur, ms=5, clip_on=False)


# u_{n+1} = sqrt((1+u_n)/2)
f = lambda x: np.sqrt((1 + x) / 2)
fig, ax = plt.subplots(figsize=(5.0, 3.6))
x = np.linspace(-1, 3.3, 400)
ax.plot(x, f(x), color=C["noir"], label=r"$y=f(x)$")
ax.plot(x, x, color=C["gris"], lw=1.2, ls="--", label=r"$y=x$")
escalier(ax, f, -0.9, 6, C["c1"])
escalier(ax, f, 3.0, 6, C["c2"])
axes_fleches(ax)
ax.set_xlim(-1.05, 3.3); ax.set_ylim(-0.3, 2.0); ax.set_aspect("equal")
ax.set_xticks([1]); ax.set_xticklabels([r"$1$"]); ax.set_yticks([1]); ax.set_yticklabels([r"$1$"])
ax.text(-0.9, -0.22, r"$u_0$", color=C["c1"], ha="center", fontsize=12)
ax.text(3.0, -0.22, r"$u_0$", color=C["c2"], ha="center", fontsize=12)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)

sauver(fig, "escalier-racine")

# f(x) = x e^{-x}
g = lambda x: x * np.exp(-x)
fig, ax = plt.subplots(figsize=(5.2, 3.6))
x = np.linspace(-0.75, 3.6, 400)
ax.plot(x, g(x), color=C["noir"], label=r"$y=x\,\mathrm{e}^{-x}$")
ax.plot(x, x, color=C["gris"], lw=1.2, ls="--", label=r"$y=x$")
escalier(ax, g, 0.85, 8, C["c1"])
escalier(ax, g, 3.0, 8, C["c2"])
# u0 < 0 : la suite décroît
u, xs, ys = -0.25, [-0.25], [0]
for _ in range(3):
    v = g(u); xs += [u, v]; ys += [v, v]; u = v
ax.plot(xs, ys, color=C["c3"], lw=1.3); ax.plot([-0.25], [0], "o", color=C["c3"], ms=5)
ax.plot([1, 1], [0, np.exp(-1)], color=C["gris"], lw=0.8, ls=":")
axes_fleches(ax)
ax.set_xlim(-0.8, 3.6); ax.set_ylim(-0.75, 1.15); ax.set_aspect("equal")
ax.set_xticks([1, 3]); ax.set_yticks([np.exp(-1)]); ax.set_yticklabels([r"$1/\mathrm{e}$"])
ax.legend(loc="upper right")
sauver(fig, "xexp")
