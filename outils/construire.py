#!/usr/bin/env python3
"""Construit un paquet Anki (.apkg) à partir d'un ou plusieurs chapitres.

Exemples :
  python3 outils/construire.py chapitres/physique/induction
  python3 outils/construire.py chapitres/physique/induction -o sorties/induction.apkg
  python3 outils/construire.py            (tous les chapitres, dans un seul paquet)

Les identifiants de cartes servent à fabriquer des GUID stables : réimporter un paquet
reconstruit met à jour les cartes existantes sans toucher à la progression.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import (CHAMPS, CSS, MODELE_ID, MODELE_NOM, MODELE_RECTO, MODELE_VERSO, SORTIES,
                    chapitres_depuis, lire_chapitre, medias_cites, quitter, renommer_medias,
                    verifier)


def id_paquet(nom):
    return int(hashlib.sha1(nom.encode()).hexdigest()[:12], 16)


def modele():
    return genanki.Model(
        MODELE_ID, MODELE_NOM,
        fields=[{"name": c} for c in CHAMPS],
        templates=[{"name": "Recto-verso", "qfmt": MODELE_RECTO, "afmt": MODELE_VERSO}],
        css=CSS, sort_field_index=3,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("chapitres", nargs="*", help="dossiers de chapitres (défaut : tous)")
    p.add_argument("-o", "--sortie", help="fichier .apkg (défaut : sorties/<nom>.apkg)")
    a = p.parse_args()

    dossiers = chapitres_depuis(a.chapitres)
    if not dossiers:
        quitter("Aucun chapitre trouvé.")
    m = modele()
    paquets, medias, total, bloquant = {}, [], 0, False
    for d in dossiers:
        try:
            chap = lire_chapitre(d)
        except ValueError as e:
            quitter(f"Erreur : {e}")
        erreurs, avert = verifier(chap)
        for x in avert:
            print(f"  attention [{chap.cle}] {x}")
        for x in erreurs:
            print(f"  ERREUR    [{chap.cle}] {x}")
        bloquant |= bool(erreurs)
        paquet = paquets.setdefault(chap.paquet, genanki.Deck(id_paquet(chap.paquet), chap.paquet))
        pre = chap.prefixe_media
        for c in chap.cartes:
            tags = [re.sub(r"\s+", "_", t) for t in chap.cle.split("/")]
            paquet.add_note(genanki.Note(
                model=m,
                fields=[renommer_medias(c.recto, pre), renommer_medias(c.verso, pre), c.source, c.id],
                guid=genanki.guid_for("prepa-pc", chap.cle, c.id),
                tags=tags,
            ))
            for s in medias_cites(c.recto + c.verso):
                src = chap.dossier / "media" / Path(s).name
                cible = SORTIES / ".medias" / (pre + Path(s).name)
                if src.exists() and str(cible) not in medias:
                    cible.parent.mkdir(parents=True, exist_ok=True)
                    cible.write_bytes(src.read_bytes())
                    medias.append(str(cible))
        total += len(chap.cartes)
    if bloquant:
        quitter("Paquet non construit : corriger les erreurs ci-dessus.")

    if a.sortie:
        sortie = Path(a.sortie)
    else:
        nom = dossiers[0].resolve().name if len(dossiers) == 1 else "prepa-pc"
        sortie = SORTIES / f"{nom}.apkg"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(paquets.values()), media_files=medias).write_to_file(str(sortie))
    print(f"{total} cartes, {len(medias)} médias → {sortie}")


if __name__ == "__main__":
    main()
