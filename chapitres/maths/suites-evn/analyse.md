# Analyse — Chapitre 6 : Suites dans un EVN (maths, spé PC)

Cours fourni : `cours/C6_Espaces_normes.pdf` (42 pages scannées). Pages 1-9 : poly tapé (énoncés et exercices, pagination 55-63). Pages 11-42 : corrections manuscrites du prof (démonstrations, exercices, compléments : comparaison série-intégrale, exercices supplémentaires, Bolzano-Weierstrass). Page 10 : verso blanc.

## Logique du chapitre
1. **Sous-ensembles d'un EVN** : boules (ouverte, fermée, sphère), parties bornées. En dimension finie, normes équivalentes ⇒ boules emboîtées ⇒ « bornée » ne dépend pas de la norme.
2. **Suites dans un EVN** : suite bornée, convergence (3 formulations équivalentes), indépendance de la limite vis-à-vis de la norme en dimension finie (et contre-exemples en dimension infinie : C¹([0,1]), C([0,1]), ℝ[X]), propriétés (unicité, CV ⇒ bornée, extraites, coordonnées, linéarité, N(uₙ) → N(ℓ), domination, produit par une suite scalaire). Application phare : limite de (I + (a/n)J)ⁿ = rotation d'angle a.
3. **Suites réelles ou complexes** (rappels de sup, mais très utilisés en DS) : définitions en quantificateurs, encadrement, minoration, limite monotone, adjacentes (e irrationnel, moyenne arithmético-géométrique), extraites, récurrentes linéaires d'ordre 2, uₙ₊₁ = f(uₙ), Cesàro (HP) et lemme de l'escalier, équivalents de suites récurrentes (sin, x e⁻ˣ, x + 1/x), suites implicites, comparaison série-intégrale, Bolzano-Weierstrass (HP selon le prof).

Ce qui est central pour les concours : savoir **choisir une norme** commode en dimension finie ; savoir **prouver la non-équivalence** de deux normes avec une suite ; les **méthodes** sur les suites récurrentes et implicites (théorème de la bijection, monotonie par comparaison de fₙ(xₙ₊₁) à fₙ(xₙ), développement asymptotique par réinjection) ; Cesàro/escalier pour obtenir des équivalents (choix de l'exposant α) ; comparaison série-intégrale. Pièges de jury : oublier la continuité de f au point limite, conclure « f(ℓ) = ℓ » sans avoir prouvé la convergence, confondre « croissante majorée par M » et « limite M », oublier qu'une suite monotone peut tendre vers ±∞, écrire « lim uₙ = 1/n ».

## Ce qu'il faut maîtriser, et comment
- **Définitions** (boules, partie bornée, convergence P1-P3, limites en quantificateurs, adjacentes, extraite) : énoncer exactement → cartes courtes.
- **Énoncés-outils** (encadrement, minoration, limite monotone, Cesàro, escalier, récurrentes linéaires d'ordre 2, BW) : énoncer avec hypothèses exactes + piège associé (remarques 4, 5, 6 du cours).
- **Démonstrations du prof** (boules et normes équivalentes, limite indépendante de la norme, uₙ pair/impair, coordonnées, Cesàro, escalier, e irrationnel, BW) : dérouler → une carte par démonstration, verso = version de référence en étapes.
- **Exercices corrigés** : ce sont des méthodes types de DS ; chaque exercice devient une carte « refaire » (parfois deux quand les deux questions mobilisent des savoir-faire distincts : limite puis équivalent).
- **Visuels** : boules unités (lire/tracer), escalier de uₙ₊₁ = f(uₙ), graphe de x e⁻ˣ avec intervalles stables, comparaison série-intégrale, dichotomie de BW, partie bornée.

## Plan des cartes (65)
I. Sous-ensembles : `def-boules`, `boules-unite-r2`, `boules-normes-equiv`, `exo1-homothetie`, `exo1-somme`, `def-bornee`, `bornee-dim-finie`, `exo2-diametre`, `exo3-4-matrices-bornees`.
II. Suites d'un EVN : `suite-bornee`, `contre-ex-c1-bornee`, `def-convergence`, `limite-indep-norme`, `contre-ex-n1-ninf`, `exo6-polynomes`, `unicite-bornee`, `norme-limite`, `domination`, `produit-suite-scalaire`, `extraites-evn`, `pair-impair-demo`, `exo5-divergence`, `coordonnees`, `exemples-matrices`, `rotation-limite`.
III. Suites réelles : `def-limites`, `encadrement`, `minoration`, `limite-monotone`, `monotone-pieges`, `adjacentes`, `exo7-adjacentes`, `exo7-irrationnel`, `exo8-agm`, `exo9-harmonique` (ajout), `extraite-def`, `exo10-trois-extraites`, `rec-lin-complexe`, `rec-lin-reel`, `rec-lin-application` (ajout), `arith-geo`, `methode-recurrente`, `exemple-racine`, `exo11-limite`, `exo11-equivalent`, `exo12-limite`, `exo12-equivalent`, `exo13`, `cesaro-enonce`, `cesaro-demo-0`, `cesaro-demo-suite`, `escalier`, `exo14-limite`, `exo14-da`, `exo15-limite`, `exo15-da`, `exo16-existence`, `exo16-da`, `serie-integrale`, `suppl1-riemann`, `suppl1-integrale`, `suppl2-alpha`, `suppl2-harmonique`, `bw-enonce`, `bw-demo`.

Non repris : l'exercice supplémentaire 3 (barré par le prof, non terminé) ; l'exercice 17 (même méthode que l'exercice 14, sans correction) ; définition 3 et remarque 2 (structure d'espace vectoriel de E^ℕ, sans enjeu).

## Visuels prévus (tous créés, matplotlib)
`boules-unite.svg`, `partie-bornee.svg`, `escalier-racine.svg`, `xexp.svg`, `serie-integrale.svg`, `bw-dichotomie.svg`.

## Erreurs du cours repérées (corrigées dans les cartes, signalées)
- Théorème 7 (cas réel) : « Soit (uₙ) une suite complexe » → suite **réelle**.
- Méthode 72, point 4 : « décroissante sur D » → sur **I**. Théorème 3 : « (reps. » coquille.
- Exemple de limite matricielle (manuscrit) : lim Aₙ écrite avec « e » en bas à droite → **e⁻¹** (car (1 − 1/n)ⁿ → 1/e, comme écrit juste avant).
- Exercice 11 : « on choisit α = 2 » alors que le calcul utilise 1/uₙ² → **α = −2**.
- Exercice 12 : « lim uₙ = 1/n » → **uₙ ~ 1/n**.
- Exercice 15 : erreur de signe : rₙⁿ⁺¹ **− 2rₙ + 1** = 0 (et non + 2rₙ − 1) ; d'où rₙ = (1 **+** rₙⁿ⁺¹)/2 et **rₙ = 1/2 + 1/2ⁿ⁺² + o(1/2ⁿ⁺²)** (le cours trouve « − » : impossible car fₙ(1/2) = −1/2ⁿ < 0 impose rₙ > 1/2 ; vérifié numériquement).
- Exercice supplémentaire 1 : Σₖ₌₀ⁿ 1/(n+k) = (1/n)Σₖ₌₁ⁿ 1/(1+k/n) **+** 1/n (le cours écrit « − 1/n »), sans effet sur l'équivalent.
- Exercice 1 : vrai pour λ ≠ 0 seulement (pour λ = 0, 0·B = {0} ≠ ∅) — le prof le précise en tête de correction.
- Exercice 14 : l'énoncé demande deux termes, le prof en donne trois (on garde les trois).
- Bolzano-Weierstrass noté HP par le prof : la carte garde cette mention.
