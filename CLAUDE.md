# Prépa Anki — spé PC

Ce dépôt transforme les cours de prépa d'un élève de **spé PC** en paquets Anki qui **remplacent entièrement le cours**.
Lire cette page en entier avant chaque demande. La partie *Philosophie* prime sur tout le reste.

---

## Philosophie

### Le but
Une fois un chapitre dans Anki, l'élève ne rouvre plus jamais le cours. Tout ce qu'il doit savoir, comprendre, savoir refaire et savoir rédiger passe par les cartes. La mesure du succès : les DS, les colles, les concours.

### Autonomie complète
L'élève donne un cours (et éventuellement un périmètre ou un paquet existant), puis récupère le paquet fini. Il n'intervient pas en cours de route : aucune validation, aucune question, aucune décision à lui laisser. Chaque choix se fait seul, avec jugement.

### Aucune règle, un jugement
Il n'y a pas de format type. Chaque cours est différent, et chaque élément d'un même cours aussi. Pour chaque élément, une seule question :

> **Que veut dire *maîtriser* cet élément, et quelle carte entraîne exactement ça ?**

Maîtriser peut vouloir dire connaître une donnée, énoncer exactement, comprendre un pourquoi, reconnaître quand appliquer, dérouler une démonstration ou une résolution entière, rédiger, lire ou tracer un schéma, éviter un piège… souvent plusieurs à la fois.

La forme de la carte en découle, et peut varier du tout au tout au sein d'un même chapitre : une donnée isolée, ou une longue démonstration en plusieurs étapes dans une seule carte si c'est l'enchaînement qui compte. Ne pas découper par réflexe, ne pas regrouper par facilité.

Chaque cours se pense à neuf. Ne pas reproduire par habitude les choix faits sur un autre chapitre. Ce qui reste constant : cette philosophie, et la connaissance du prof (`profs/`).

### Comprendre avant de produire
Avant la moindre carte, lire tout le cours (ou la partie demandée) en profondeur : sa logique, ce qui est central et ce qui en découle, les liens avec les autres chapitres, ce qui est exigible au programme de PC, ce qui tombe aux concours, les vrais pièges (rapports de jury), ce sur quoi le prof insiste. Les cartes naissent de cette compréhension.

### Fidélité au cours et au prof
Les cartes transmettent le cours **tel que le prof l'enseigne** : ses notations, ses conventions, les noms qu'il donne aux théorèmes et aux lois, sa rédaction, sa façon de dessiner (en chimie : flèches, doublets, charges, intermédiaires, présentation des mécanismes). Dans le doute, faire comme le prof. La forme peut être reformulée ; le fond et la syntaxe du prof sont respectés.

Une erreur, une coquille ou une incohérence dans le cours n'est jamais recopiée : on la corrige, et la carte concernée le dit brièvement (par exemple « le cours écrit … : coquille »), pour que l'élève ne soit pas déstabilisé en DS ou face à son prof. Une ambiguïté se tranche par l'interprétation la plus juste au regard du programme et des concours.

Compléter le cours est permis quand ça sert vraiment (une intuition, un ordre de grandeur, un piège relevé par les jurys), à condition que ce soit juste et identifiable comme un ajout.

### Rigueur
Quand une carte déroule une démonstration ou une résolution, son verso est la **version de référence**, rédigée comme on la veut en DS : hypothèses citées là où elles servent, théorèmes nommés, signes, conventions et unités justes, aucun saut logique, aucun « on voit facilement ». Tout le reste est exact aussi : chaque valeur, chaque formule, chaque visuel.

### Forme
- **Recto-verso uniquement.**
- **Ne pas spoiler.** Le recto ne contient ni ne suggère la réponse, ni par sa formulation, ni par un schéma, ni par un titre. Éviter aussi qu'une carte donne la réponse d'une autre.
- **Le recto** pose une question sans ambiguïté : il dit ce qui est attendu (énoncer, démontrer, justifier, tracer…) et donne juste assez de contexte pour qu'une seule réponse soit possible.
- **Le verso** se lit d'un coup d'œil : la réponse d'abord, puis le reste. **Concision dans la forme, jamais dans la rigueur** : pas de phrases longues et denses. On reformule, on structure, on découpe en étapes courtes, on utilise flèches, couleurs porteuses de sens et visuels.
- Chaque carte se comprend seule, et doit être lisible sur ordinateur comme sur téléphone Android, en mode clair comme en mode sombre.

### Visuels
Beaucoup, dès qu'un visuel transmet mieux qu'un texte, au recto (lire, interpréter, compléter) comme au verso. Deux sources, choisies au cas par cas :
- **créés** avec l'outil le plus adapté, rigoureusement exacts (des courbes calculées, pas dessinées à main levée), et cohérents avec le style du cours ;
- **capturés** dans le cours quand l'original est le meilleur support, puis nettoyés.

### Couverture et charge
L'ensemble des cartes couvre tout le périmètre demandé : rien d'important ne manque. Mais chaque carte coûte du temps de révision toute l'année : pas de carte inutile, pas de doublon.

---

## Déroulement d'une demande

1. **Cadrer.** Respecter exactement le périmètre donné (tout le cours, ou seulement une partie). Si un paquet existant est fourni, la suite le prolonge.
2. **Paquet existant.** Le lire avec `outils/lire_apkg.py`, comprendre ce qui est couvert et comment, puis continuer sans doublon et dans la continuité. Les anciennes cartes ne sont pas modifiées : le nouveau paquet ne contient que la suite.
3. **Connaître le prof.** Lire `profs/<matiere>.md`.
4. **Analyser** le cours en profondeur et écrire `analyse.md` dans le dossier du chapitre : ce qu'il faut maîtriser et comment, le plan des cartes, les visuels prévus (créés ou capturés), les erreurs du cours repérées. Puis enchaîner directement.
5. **Produire** les visuels puis les cartes.
6. **Vérifier.** Générer l'aperçu de toutes les cartes et **regarder chaque image** : rendu des formules, lisibilité des visuels en clair et en sombre, tenue sur téléphone, absence de spoil. Relire la rigueur. Contrôler la couverture du périmètre.
7. **Livrer** le `.apkg` avec un bilan court, pour information : ce qui a été fait, les choix notables, les corrections apportées au cours.
8. **Mettre à jour** `profs/<matiere>.md` avec ce qui a été appris sur le prof, puis commit et push.

---

## Technique

Tout est en français. Les outils sont dans `outils/` ; chacun affiche son aide avec `--help`. **Au début de chaque session, lancer `bash outils/installer.sh`** : il installe LaTeX, les bibliothèques Python et MathJax s'ils manquent (quelques minutes la première fois, rien ensuite).

### Arborescence
```
profs/<matiere>.md                     carnet du prof, enrichi à chaque chapitre
chapitres/<matiere>/<chapitre>/
    cours/        le cours fourni (PDF, images)
    analyse.md    l'analyse du chapitre
    cartes.txt    les cartes
    visuels/      sources des visuels créés (.tex, .py)
    media/        images utilisées par les cartes (générées ou capturées)
    apercu/       aperçus de vérification (non versionné)
sorties/          les .apkg livrés (non versionné)
```
Matières : `maths`, `physique`, `chimie`, ou autre si besoin.

### Format de `cartes.txt`
```
%% paquet: PC::Physique::Nom du chapitre

%% carte: identifiant-unique-et-stable
%% source: Cours p. 3
Recto (HTML)
%% verso
Verso (HTML)
```
- Le contenu est du HTML. Les maths en MathJax : `\( … \)` en ligne, `\[ … \]` centré. `\ce{…}` (mhchem) pour la chimie.
- Images : `<img src="nom.svg">`, le fichier étant dans `media/`.
- L'identifiant d'une carte ne change jamais : reconstruire le paquet met alors à jour les cartes au lieu de les dupliquer, et la progression de l'élève est conservée.
- La ligne `%% source:` est facultative.

Classes CSS disponibles (rien n'oblige à les utiliser, et on peut écrire du style en ligne) :
- `.reponse` : encadré qui met la réponse en évidence ;
- `.etapes` : liste numérotée d'étapes, avec `.pas-a-pas` en plus pour révéler les étapes une à une au clic ;
- `.attention` : piège ou erreur classique ; `.remarque` : complément discret ; `.ajout` : contenu absent du cours ;
- `.c1` à `.c4` : couleurs sémantiques (texte), lisibles en clair et en sombre ;
- `.cote` : deux blocs côte à côte sur ordi, empilés sur téléphone ;
- images : identiques en mode clair et sombre (en sombre, elles sont posées sur un fond blanc) ; `class="inline"` pour une petite image dans le texte.

### Outils
- `outils/scan.py pages` : rend les pages d'un PDF en PNG pour les lire. `outils/scan.py capture` : découpe une zone d'une page en haute définition et nettoie le scan (fond blanc rendu transparent, contraste).
- `outils/tex2svg.py` : compile un visuel LaTeX (TikZ, circuitikz, chemfig, pgfplots…) en SVG. Couleurs `c1`…`c4` prédéfinies. Chemfig est en version 1.66 : les doublets s'écrivent avec `\charge` (`\lewis` n'existe plus).
- `outils/fig.py` : style matplotlib commun et `sauver()` en SVG, à importer dans les scripts de `visuels/`.
- `outils/construire.py` : construit le `.apkg` d'un chapitre (ou de plusieurs) dans `sorties/`.
- `outils/apercu.py` : rend les cartes en images (téléphone et ordi, clair et sombre) dans `apercu/` pour les vérifier.
- `outils/lire_apkg.py` : extrait le contenu d'un paquet Anki existant (cartes, médias, modèles) pour l'analyser.
