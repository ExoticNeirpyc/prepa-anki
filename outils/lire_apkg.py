#!/usr/bin/env python3
"""Extrait le contenu d'un paquet Anki (.apkg ou .colpkg) pour l'analyser.

Produit dans le dossier de sortie :
  cartes.md    toutes les notes : paquet, modèle, tags, champs (HTML brut)
  modeles.md   les modèles de notes : champs, gabarits recto/verso, CSS
  media/       les médias, sous leur vrai nom

Fonctionne avec les exports récents d'Anki (compressés) comme avec les anciens.

    python3 outils/lire_apkg.py paquet.apkg -o /tmp/paquet
"""

import argparse
import json
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path

ZSTD = b"\x28\xb5\x2f\xfd"


def dezstd(data):
    if not data.startswith(ZSTD):
        return data
    import zstandard
    return zstandard.ZstdDecompressor().stream_reader(data).read()


def varint(b, i):
    r = s = 0
    while True:
        x = b[i]
        i += 1
        r |= (x & 0x7F) << s
        s += 7
        if not x & 0x80:
            return r, i


def protobuf(b):
    """Décodage générique : {numéro de champ: [valeurs]} (varint ou bytes)."""
    champs, i = {}, 0
    while i < len(b):
        cle, i = varint(b, i)
        num, typ = cle >> 3, cle & 7
        if typ == 0:
            v, i = varint(b, i)
        elif typ == 2:
            n, i = varint(b, i)
            v, i = b[i:i + n], i + n
        elif typ == 1:
            v, i = b[i:i + 8], i + 8
        elif typ == 5:
            v, i = b[i:i + 4], i + 4
        else:
            raise ValueError("protobuf inattendu")
        champs.setdefault(num, []).append(v)
    return champs


def texte(champs, num):
    v = champs.get(num)
    return v[0].decode("utf-8", "replace") if v else ""


def table_medias(z):
    brut = dezstd(z.read("media"))
    try:
        return {k: v for k, v in json.loads(brut).items()}
    except (ValueError, UnicodeDecodeError):
        entrees = protobuf(brut).get(1, [])
        return {str(i): texte(protobuf(e), 1) for i, e in enumerate(entrees)}


def lire(chemin, sortie):
    z = zipfile.ZipFile(chemin)
    noms = z.namelist()
    base = next((n for n in ("collection.anki21b", "collection.anki21", "collection.anki2") if n in noms), None)
    if base is None:
        sys.exit("Aucune collection dans ce fichier : est-ce bien un paquet Anki ?")
    tmp = Path(tempfile.mkdtemp()) / "col.db"
    tmp.write_bytes(dezstd(z.read(base)))
    db = sqlite3.connect(tmp)
    tables = {r[0] for r in db.execute("select name from sqlite_master where type='table'")}

    modeles, paquets = {}, {}
    if "notetypes" in tables:
        for ntid, nom, config in db.execute("select id, name, config from notetypes"):
            modeles[ntid] = {"nom": nom, "css": texte(protobuf(config), 3), "champs": [], "gabarits": []}
        for ntid, _, nom in db.execute("select ntid, ord, name from fields order by ntid, ord"):
            modeles[ntid]["champs"].append(nom)
        for ntid, _, nom, config in db.execute("select ntid, ord, name, config from templates order by ntid, ord"):
            c = protobuf(config)
            modeles[ntid]["gabarits"].append((nom, texte(c, 1), texte(c, 2)))
        for did, nom in db.execute("select id, name from decks"):
            paquets[did] = nom.replace("\x1f", "::")
    else:
        models, decks = db.execute("select models, decks from col").fetchone()
        for ntid, m in json.loads(models).items():
            modeles[int(ntid)] = {"nom": m["name"], "css": m.get("css", ""),
                                  "champs": [f["name"] for f in m["flds"]],
                                  "gabarits": [(t["name"], t["qfmt"], t["afmt"]) for t in m["tmpls"]]}
        for did, d in json.loads(decks).items():
            paquets[int(did)] = d["name"]

    sortie.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(sortie / "cartes.md", "w", encoding="utf-8") as f:
        notes = db.execute("""select n.id, n.mid, n.tags, n.flds, min(c.did)
                              from notes n left join cards c on c.nid = n.id
                              group by n.id order by min(c.did), n.id""").fetchall()
        for nid, mid, tags, flds, did in notes:
            n += 1
            m = modeles.get(mid, {"nom": "?", "champs": []})
            f.write(f"## Note {n}\n- paquet : {paquets.get(did, '?')}\n- modèle : {m['nom']}\n")
            if tags.strip():
                f.write(f"- tags : {tags.strip()}\n")
            for i, val in enumerate(flds.split("\x1f")):
                nom = m["champs"][i] if i < len(m["champs"]) else f"champ {i + 1}"
                f.write(f"\n### {nom}\n{val}\n")
            f.write("\n---\n\n")
    with open(sortie / "modeles.md", "w", encoding="utf-8") as f:
        for m in modeles.values():
            f.write(f"## {m['nom']}\nChamps : {', '.join(m['champs'])}\n\n")
            for nom, q, a in m["gabarits"]:
                f.write(f"### Gabarit « {nom} »\nRecto :\n```html\n{q}\n```\nVerso :\n```html\n{a}\n```\n\n")
            f.write(f"### CSS\n```css\n{m['css']}\n```\n\n")

    medias = table_medias(z) if "media" in noms else {}
    (sortie / "media").mkdir(exist_ok=True)
    for num, nom in medias.items():
        if num in noms and nom:
            (sortie / "media" / Path(nom).name).write_bytes(dezstd(z.read(num)))
    print(f"{n} notes, {len(modeles)} modèle(s), {len(medias)} média(s) → {sortie}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paquet", type=Path)
    p.add_argument("-o", "--sortie", type=Path, required=True)
    a = p.parse_args()
    lire(a.paquet, a.sortie)


if __name__ == "__main__":
    main()
