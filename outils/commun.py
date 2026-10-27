"""Éléments partagés : lecture de cartes.txt, modèle de note Anki, style des cartes."""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CHAPITRES = RACINE / "chapitres"
SORTIES = RACINE / "sorties"
CACHE = Path.home() / ".cache" / "prepa-anki"
MATHJAX = CACHE / "node_modules" / "mathjax" / "es5" / "tex-chtml-full.js"

# Identifiant fixe du modèle de note : ne jamais le changer, sinon Anki crée un nouveau modèle.
MODELE_ID = 1761234567001
MODELE_NOM = "Prépa PC"
CHAMPS = ["Recto", "Verso", "Source", "ID"]


@dataclass
class Carte:
    id: str
    recto: str
    verso: str
    source: str = ""
    ligne: int = 0


@dataclass
class Chapitre:
    dossier: Path
    paquet: str = ""
    cartes: list = field(default_factory=list)

    @property
    def cle(self):
        """Chemin relatif matière/chapitre, utilisé pour les GUID et les noms de médias."""
        try:
            return self.dossier.resolve().relative_to(CHAPITRES.resolve()).as_posix()
        except ValueError:
            return self.dossier.resolve().name

    @property
    def prefixe_media(self):
        return re.sub(r"[^A-Za-z0-9-]+", "_", self.cle) + "__"


def lire_chapitre(dossier):
    """Lit dossier/cartes.txt. Lève ValueError avec un message précis si le format est faux."""
    dossier = Path(dossier)
    fichier = dossier / "cartes.txt"
    if not fichier.exists():
        raise ValueError(f"{fichier} introuvable")
    chap = Chapitre(dossier=dossier)
    carte, partie, tampon = None, None, []

    for n, ligne in enumerate(fichier.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^%%\s*(\w+)\s*(?::\s*(.*))?$", ligne)
        if not m:
            if carte is None:
                if ligne.strip():
                    raise ValueError(f"{fichier}:{n}: texte en dehors d'une carte")
                continue
            tampon.append(ligne)
            continue
        cle, valeur = m.group(1).lower(), (m.group(2) or "").strip()
        if cle == "paquet":
            chap.paquet = valeur
        elif cle == "carte":
            if partie == "recto":
                raise ValueError(f"{fichier}:{n}: la carte « {carte.id} » n'a pas de « %% verso »")
            if carte is not None:
                carte.verso = "\n".join(tampon).strip()
                chap.cartes.append(carte)
            if not valeur:
                raise ValueError(f"{fichier}:{n}: identifiant de carte manquant")
            carte, partie, tampon = Carte(id=valeur, recto="", verso="", ligne=n), "recto", []
        elif cle == "source":
            if carte is None:
                raise ValueError(f"{fichier}:{n}: « %% source » hors d'une carte")
            carte.source = valeur
        elif cle == "verso":
            if carte is None or partie != "recto":
                raise ValueError(f"{fichier}:{n}: « %% verso » inattendu")
            carte.recto = "\n".join(tampon).strip()
            partie, tampon = "verso", []
        else:
            raise ValueError(f"{fichier}:{n}: directive inconnue « %% {cle} »")
    if partie == "recto":
        raise ValueError(f"{fichier}: la carte « {carte.id} » n'a pas de « %% verso »")
    if carte is not None:
        carte.verso = "\n".join(tampon).strip()
        chap.cartes.append(carte)
    if not chap.paquet:
        raise ValueError(f"{fichier}: ligne « %% paquet: … » manquante")
    return chap


RE_SRC = re.compile(r"""(<img\b[^>]*?\bsrc\s*=\s*)(["'])(.*?)\2""", re.I)


def medias_cites(html):
    return [s for _, _, s in RE_SRC.findall(html) if not re.match(r"^(https?:|data:)", s)]


def renommer_medias(html, prefixe):
    def f(m):
        src = m.group(3)
        if re.match(r"^(https?:|data:)", src):
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}{prefixe}{Path(src).name}{m.group(2)}"
    return RE_SRC.sub(f, html)


def verifier(chap):
    """Renvoie (erreurs, avertissements) pour un chapitre."""
    erreurs, avert = [], []
    vus = set()
    for c in chap.cartes:
        ou = f"carte « {c.id} » (ligne {c.ligne})"
        if c.id in vus:
            erreurs.append(f"{ou} : identifiant en double")
        vus.add(c.id)
        if not c.recto:
            erreurs.append(f"{ou} : recto vide")
        if not c.verso:
            erreurs.append(f"{ou} : verso vide")
        for cote, html in (("recto", c.recto), ("verso", c.verso)):
            for o, f in (("\\(", "\\)"), ("\\[", "\\]")):
                if html.count(o) != html.count(f):
                    erreurs.append(f"{ou}, {cote} : délimiteurs {o} {f} déséquilibrés")
            if html.count("{") != html.count("}"):
                avert.append(f"{ou}, {cote} : accolades déséquilibrées")
            if re.search(r"(?<!\\)\$", html):
                avert.append(f"{ou}, {cote} : « $ » trouvé, Anki attend \\( \\) ou \\[ \\]")
            for src in medias_cites(html):
                if not (chap.dossier / "media" / Path(src).name).exists():
                    erreurs.append(f"{ou}, {cote} : média introuvable media/{Path(src).name}")
    cites = {Path(s).name for c in chap.cartes for s in medias_cites(c.recto + c.verso)}
    dossier_media = chap.dossier / "media"
    if dossier_media.exists():
        for f in sorted(dossier_media.iterdir()):
            if f.is_file() and f.name not in cites:
                avert.append(f"media/{f.name} n'est utilisé par aucune carte")
    return erreurs, avert


def chapitres_depuis(args):
    """Liste de dossiers de chapitres à partir des arguments (vide = tous)."""
    if args:
        return [Path(a) for a in args]
    return sorted(p.parent for p in CHAPITRES.glob("*/*/cartes.txt"))


def quitter(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- style des cartes

CSS = r"""
.card {
  --texte: #1d1d1f; --fond: #ffffff; --doux: #6e6e73; --ligne: #d2d2d7;
  --accent: #1f5fbf; --fond-reponse: #eef4fc;
  --c1: #1f5fbf; --c2: #c0392b; --c3: #1e8449; --c4: #7d3c98;
  --fond-attention: #fdf0ee; --bord-attention: #c0392b;
  --fond-remarque: #f5f5f7; --bord-ajout: #7d3c98;
  font-family: "Charter", "Bitstream Charter", "Georgia", "Cambria", serif;
  font-size: 19px; line-height: 1.5; color: var(--texte); background: var(--fond);
  text-align: left; margin: 0; padding: 18px 16px 28px;
}
.card.nightMode, .nightMode .card, .card.night_mode, .night_mode .card {
  --texte: #e8e8ed; --fond: #1c1c1e; --doux: #98989d; --ligne: #3a3a3c;
  --accent: #6ea8ff; --fond-reponse: #1d2a3d;
  --c1: #6ea8ff; --c2: #ff7b6b; --c3: #5fd38d; --c4: #c89cf0;
  --fond-attention: #3a2220; --bord-attention: #ff7b6b;
  --fond-remarque: #2c2c2e; --bord-ajout: #c89cf0;
}
.contenu { max-width: 760px; margin: 0 auto; }
.recto { font-size: 1.05em; }
hr#answer { border: none; border-top: 1px solid var(--ligne); margin: 18px 0; }
p { margin: 0.5em 0; }
b, strong { font-weight: 650; }
ul, ol { padding-left: 1.4em; margin: 0.5em 0; }
li { margin: 0.25em 0; }
h3, h4 { margin: 0.8em 0 0.3em; font-size: 1em; color: var(--accent); }
table { border-collapse: collapse; margin: 0.6em 0; }
td, th { border: 1px solid var(--ligne); padding: 4px 8px; }
th { background: var(--fond-remarque); }

.reponse { background: var(--fond-reponse); border-left: 4px solid var(--accent);
  padding: 8px 12px; border-radius: 4px; margin: 0.4em 0 0.8em; }
.etapes { counter-reset: etape; list-style: none; padding-left: 0; }
.etapes > li { counter-increment: etape; position: relative; padding-left: 2em; margin: 0.55em 0; }
.etapes > li::before { content: counter(etape); position: absolute; left: 0; top: 0.1em;
  width: 1.45em; height: 1.45em; border-radius: 50%; background: var(--accent); color: var(--fond);
  font: 600 0.78em/1.45em system-ui, sans-serif; text-align: center; }
.attention, .remarque, .ajout { padding: 6px 12px; border-radius: 4px; margin: 0.7em 0; font-size: 0.93em; }
.attention { background: var(--fond-attention); border-left: 4px solid var(--bord-attention); }
.attention::before { content: "⚠ "; color: var(--bord-attention); }
.remarque { background: var(--fond-remarque); color: var(--doux); }
.ajout { border-left: 4px solid var(--bord-ajout); background: var(--fond-remarque); }
.ajout::before { content: "Hors cours · "; color: var(--bord-ajout); font: 600 0.8em system-ui, sans-serif; }
.c1 { color: var(--c1); } .c2 { color: var(--c2); } .c3 { color: var(--c3); } .c4 { color: var(--c4); }
.cote { display: flex; gap: 16px; flex-wrap: wrap; align-items: flex-start; }
.cote > * { flex: 1 1 280px; min-width: 0; }
.source { margin-top: 22px; font: 0.72em system-ui, sans-serif; color: var(--doux); text-align: right; }

img { max-width: 100%; height: auto; display: block; margin: 0.6em auto; }
img.inline { display: inline; margin: 0; vertical-align: middle; }
/* Visuels identiques dans les deux modes : en sombre, ils gardent leur fond blanc. */
.nightMode img:not(.inline), .night_mode img:not(.inline) { background: #ffffff; padding: 8px; border-radius: 6px; box-sizing: border-box; }

mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; }

.pas-a-pas.actif > li.cache { display: none; }
.boutons-etapes { margin: 10px 0; display: flex; gap: 8px; }
.boutons-etapes button { font: 600 0.8em system-ui, sans-serif; padding: 7px 14px; border-radius: 6px;
  border: 1px solid var(--accent); background: transparent; color: var(--accent); cursor: pointer; }
.boutons-etapes button.plein { background: var(--accent); color: var(--fond); }
"""

JS_ETAPES = r"""
<script>
(function () {
  document.querySelectorAll('.verso .pas-a-pas').forEach(function (liste) {
    if (liste.dataset.pret) return;
    liste.dataset.pret = '1';
    var etapes = Array.prototype.slice.call(liste.children);
    if (etapes.length < 2) return;
    liste.classList.add('actif');
    var vues = 0;
    var boite = document.createElement('div');
    boite.className = 'boutons-etapes';
    var suivant = document.createElement('button');
    suivant.className = 'plein';
    var tout = document.createElement('button');
    tout.textContent = 'Tout afficher';
    boite.appendChild(suivant); boite.appendChild(tout);
    liste.parentNode.insertBefore(boite, liste.nextSibling);
    function maj() {
      etapes.forEach(function (e, i) { e.classList.toggle('cache', i >= vues); });
      suivant.textContent = 'Étape suivante (' + vues + '/' + etapes.length + ')';
      if (vues >= etapes.length) boite.style.display = 'none';
    }
    suivant.onclick = function (ev) { ev.stopPropagation(); vues++; maj(); };
    tout.onclick = function (ev) { ev.stopPropagation(); vues = etapes.length; maj(); };
    maj();
  });
})();
</script>
"""

MODELE_RECTO = '<div class="contenu"><div class="recto">{{Recto}}</div></div>'
MODELE_VERSO = (
    '<div class="contenu"><div class="recto">{{Recto}}</div>\n'
    '<hr id="answer">\n'
    '<div class="verso">{{Verso}}</div>\n'
    '{{#Source}}<div class="source">{{Source}}</div>{{/Source}}</div>\n'
    + JS_ETAPES
)
