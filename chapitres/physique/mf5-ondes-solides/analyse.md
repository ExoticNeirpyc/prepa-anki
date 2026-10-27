# MF5 — Ondes mécaniques unidimensionnelles dans les solides déformables : analyse

Cours scanné, 22 pages : un plan tapé avec les définitions encadrées (p. 1-2), une page de figures (p. 3 ; la p. 4 est un verso vierge), puis le cours manuscrit pris en classe (p. 5-22, numéroté 1 à 18).

## Logique du chapitre
Un seul fil : **une même équation, celle de d'Alembert, gouverne deux systèmes très différents**, et ses solutions dépendent du milieu (illimité ou limité).
- II : la tige solide. Modèle microscopique (chaîne d'atomes reliés par des ressorts) → équation discrète → **approximation des milieux continus** (λ ≫ a, développement de Taylor) → d'Alembert avec \(c = a\sqrt{k/m}\). Le pont micro/macro par le **module d'Young** donne \(E = k/a\) et \(c = \sqrt{E/\rho}\).
- III : la corde vibrante. PFD sur un élément de corde, petits angles → d'Alembert avec \(c = \sqrt{T/\mu}\). Tension fixée par une masse via une poulie.
- IV : les solutions. Propriétés de l'équation (réversible, linéaire), solution générale en OPP, OPPH (double périodicité, relation de dispersion, vecteur d'onde, notation complexe), OSH par séparation des variables (nœuds, ventres, pas de propagation).
- V : applications sur la corde. Modes propres de la corde fixée aux deux bouts (quantification \(f_n = nc/2L\)), solution générale par superposition et conditions initiales, puis corde de Melde en régime forcé et résonances (\(f_{\text{rés}} = f_{\text{propres}}\)).

Programme PC : ondes dans les solides (chaîne d'oscillateurs, approximation des milieux continus, module d'Young), corde vibrante, OPPH, OSH, modes propres, résonances de la corde de Melde. Aux concours : les deux démonstrations de d'Alembert (tige et corde) sont des classiques d'oral ; les modes propres et Melde sont omniprésents ; les jurys relèvent la confusion entre célérité et vitesse de vibration, les hypothèses non citées (petits angles, pesanteur négligée, λ ≫ a), et l'oubli que l'écriture \(F(x)G(t)\) se fait en réels.

## Ce qu'il faut maîtriser, et comment
| Élément | Maîtriser = | Carte |
|---|---|---|
| Onde progressive, transversale, longitudinale | énoncer, classer un exemple | définition ; classement tige / corde avec visuel des deux types |
| Modèle de la chaîne | décrire les hypothèses et les notations | carte « modèle » avec schéma de la chaîne (n−1, n, n+1, \(u_n\)) |
| Équation discrète | **démontrer** (PFD, allongements, signes) | une démonstration complète |
| Milieux continus | énoncer la condition et la correspondance \(u(x_n,t) = u_n(t)\) | carte + courbe (atomes sur une sinusoïde) |
| Passage au continu | **démontrer** (Taylor à l'ordre 2) | une démonstration complète |
| d'Alembert, c | énoncer, analyse dimensionnelle, ODG microscopique | une carte dimension + expression, une carte ODG chiffrée |
| Piège c ≠ vitesse de vibration | ne pas confondre | carte dédiée (tige et corde) |
| Module d'Young | énoncer la loi, ses conditions, l'unité | carte avec schéma de traction |
| Allongement relatif, E = k/a, c = √(E/ρ) | **démontrer** | trois cartes (chacune est une étape exigible) |
| Influence de la raideur / de l'inertie | interpréter c pour les deux systèmes | une carte transversale |
| ODG | E, c dans les solides, c sur une corde | deux cartes ; AN de l'acier ajoutée |
| Corde vibrante | hypothèses ; **démontrer** d'Alembert ; c = √(T/μ) | carte hypothèses, démonstration pas-à-pas avec schéma de l'élément de corde |
| Tension par une masse et une poulie, μ = ρS | justifier, calculer | carte PFD sur la masse ; carte AN (424 m/s) |
| Propriétés de d'Alembert | réversibilité, linéarité, conséquences | une carte |
| Solution générale, sens de propagation | écrire, interpréter, vérifier | trois cartes (forme, interprétation avec visuel, vérification par dérivation) |
| Surface d'onde, onde plane | définir | une carte |
| OPPH | écrire, périodes, relation de dispersion, vecteur d'onde, complexe, limites | cartes séparées, visuel double périodicité |
| OSH | **démontrer** par séparation des variables ; nœuds, ventres, λ/2, pas de \(\vec k\) | démonstration + carte propriétés avec instantanés calculés |
| Quel type de solution chercher | selon le milieu (récapitulatif du prof) | une carte |
| Mode, mode propre, résonance | définir | cartes courtes |
| Modes propres de la corde fixée | **démontrer** ; tracer les modes ; nœuds | démonstration, carte de tracé, AN guitare |
| Solution générale par CI | méthode, \(B_n = 0\) sans vitesse initiale, spectre | carte méthode + carte spectre (ajout : spectre calculé d'une corde pincée) |
| Corde de Melde | **démontrer** \(y(x,t)\) ; condition de résonance ; interpréter l'expérience | démonstration ; carte résonance avec courbe d'amplitude calculée ; carte d'interprétation de l'expérience |

## Visuels
Tous **créés** (les figures de la p. 3 sont des photocopies grisées, peu lisibles, avec une flèche mal étiquetée sur la figure 2) :
- TikZ : chaîne d'atomes (modèle), tronçon de tige (allongement relatif), plans d'atomes et ressorts (E = k/a), essai de traction, élément de corde avec tensions et angle, corde + poulie + masse.
- matplotlib (courbes calculées) : ondes transversale / longitudinale (chaîne de points déplacés), atomes sur une sinusoïde (milieux continus), impulsion à t et t+Δt, OPPH en x et en t, instantanés d'OSH, modes 1-2-3, spectre d'une corde pincée, courbe d'amplitude de Melde, aspects de la corde de Melde (fréquence quelconque, 1re et 2e résonance) inspirés de la figure 4.

## Conventions du prof à respecter
Grandeurs : \(u_n(t)\), \(x_n(t) = x_{n,\text{éq}} + u_n(t)\), \(x_{n,\text{éq}} = na\), \(a = \ell_0\), \(u(x,t)\) pour la tige ; \(y(x,t)\), \(T\), \(\mu\), \(\alpha(x,t)\) pour la corde ; \(\psi(x,t)\) générique ; \(\psi_0\), \(\varphi\), \(F(x)\), \(G(t)\), \(\varphi_F\), \(\varphi_G\) ; \(k_n\) « pulsation spatiale », \(\omega_n\) « pulsation temporelle ». Rédaction : « PFD, syst. {…}, réf. labo galiléen », « DL », « approx. des milieux continus », « on extrapole à toute valeur de x ». Sigles : OPP, OPPH, OSH, ODG, CL, CI. « Fondamental » pour n = 1, « n-ième harmonique ». Formules marquées ♡ (à connaître) : d'Alembert, \(\ell = L(1 + F/ES)\), \(c = \sqrt{T/\mu}\), \(k = \omega/c\), \(f_n = n\,c/2L\).

## Erreurs ou imprécisions du cours (corrigées dans les cartes)
- p. 10 (manuscrit p. 4) : la loi d'Young est d'abord écrite « I = L × (I + F/ES) » : c'est \(\ell = L(1 + F/ES)\), réécrit juste en dessous.
- p. 15 : « \(k_{xc} = +\omega/c\) » : lire \(k_x = +\omega/c\).
- p. 8 : avec \(E_{\text{liaison}} \approx \tfrac12 k a^2 \approx 1\) eV et \(a \approx 10^{-10}\) m, on trouve \(k \approx 30\) N·m⁻¹ ; le cours retient \(k \sim 10\) N·m⁻¹, ce qui reste le bon ordre de grandeur (et donne \(c \sim 3\times10^3\) m·s⁻¹).
- p. 3, figure 2 : la flèche de droite est étiquetée \(\vec E\) ; c'est une force \(\vec F\) (E est le module d'Young). Figure recréée.
- p. 22 : l'amplitude \(a/|\sin kL|\) diverge à la résonance ; le modèle sans amortissement ne le dit pas : en réalité l'amortissement la limite (ajout). De même, \(f_{\text{rés}} = f_{\text{propre}}\) n'est exact qu'à amortissement faible.
- p. 20 : « n ≥ 2 : n-ième harmonique » ; usage courant : le fondamental est aussi l'harmonique de rang 1. Rien de faux, précision ajoutée.

## Plan des cartes (43)
- Définitions (2) : onde progressive ; transversale / longitudinale.
- Tige solide (15) : modèle, équation discrète, milieux continus, passage au continu, d'Alembert et c, piège c ≠ vitesse de vibration, ODG micro de c, loi de Young, allongement relatif, E = k/a, c = √(E/ρ), raideur / inertie, ODG de E, ODG des célérités.
- Corde (4) : hypothèses, démonstration de d'Alembert, tension par masse et poulie, AN acier (424 m/s).
- Solutions de d'Alembert (13) : propriétés, solution générale, interprétation s(x − ct), vérification, surface d'onde / onde plane, OPPH, vecteur d'onde, relation de dispersion, notation complexe, OPPH non physique, OSH (démonstration, propriétés, origine), récapitulatif selon le milieu.
- Applications (9) : mode / mode propre, modes propres (démonstration, tracé), guitare, solution générale par CI, spectre, Melde (démonstration, résonance, expérience).
