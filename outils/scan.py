#!/usr/bin/env python3
"""Lire un cours scanné et en capturer des morceaux propres.

pages : rend les pages d'un PDF en PNG pour les lire. Avec --grille, superpose une
        grille graduée de 0 à 1 qui permet de repérer précisément une zone à capturer.
    python3 outils/scan.py pages cours.pdf -o /tmp/pages --grille
    python3 outils/scan.py pages cours.pdf -o /tmp/pages --de 3 --a 5 --dpi 150

capture : découpe une zone d'une page (fractions de 0 à 1 de la largeur et de la hauteur,
          depuis le coin haut gauche), en haute définition, puis nettoie le scan :
          fond uniformisé, fond blanc rendu transparent (lisible en mode sombre),
          marges vides retirées.
    python3 outils/scan.py capture cours.pdf --page 4 --zone 0.1 0.35 0.9 0.6 -o media/schema.png
    python3 outils/scan.py capture photo.jpg --zone 0 0 1 1 -o media/tableau.png --rotation -1.5
    Options : --brut (aucun nettoyage), --opaque (garder le fond blanc), --dpi 300.
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf


def rendre_page(chemin, page, dpi):
    """Page (numérotée à partir de 1) en tableau RGB."""
    chemin = Path(chemin)
    if chemin.suffix.lower() == ".pdf":
        doc = pymupdf.open(chemin)
        if not 1 <= page <= doc.page_count:
            sys.exit(f"Page {page} inexistante ({doc.page_count} pages)")
        pix = doc[page - 1].get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB, alpha=False)
        return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).copy()
    return np.array(Image.open(chemin).convert("RGB"))


def grille(img):
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    w, h = im.size
    try:
        police = ImageFont.truetype("DejaVuSans-Bold.ttf", max(12, w // 70))
    except OSError:
        police = ImageFont.load_default()
    for i in range(1, 20):
        f = i / 20
        fort = i % 2 == 0
        coul = (230, 0, 120) if fort else (255, 150, 200)
        d.line([(f * w, 0), (f * w, h)], fill=coul, width=2 if fort else 1)
        d.line([(0, f * h), (w, f * h)], fill=coul, width=2 if fort else 1)
        if fort:
            t = f"{f:.1f}"
            d.text((f * w + 3, 3), t, fill=(230, 0, 120), font=police)
            d.text((3, f * h + 2), t, fill=(230, 0, 120), font=police)
    return np.array(im)


def cmd_pages(a):
    a.sortie.mkdir(parents=True, exist_ok=True)
    chemin = Path(a.fichier)
    n = pymupdf.open(chemin).page_count if chemin.suffix.lower() == ".pdf" else 1
    fin = min(a.a or n, n)
    for p in range(a.de, fin + 1):
        img = rendre_page(chemin, p, a.dpi)
        if a.grille:
            img = grille(img)
        out = a.sortie / f"page-{p:03d}.png"
        Image.fromarray(img).save(out)
        print(out)
    print(f"{fin - a.de + 1} page(s) sur {n}")


def nettoyer(img, opaque):
    """Uniformise le fond d'un scan, puis rend le blanc transparent (« dé-mélange » du blanc)."""
    f = img.astype(np.float32)
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    k = max(15, (min(img.shape[:2]) // 12) | 1)
    fond = cv2.morphologyEx(gris, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    fond = cv2.GaussianBlur(fond, (0, 0), k / 3).astype(np.float32)
    f = np.clip(f / np.maximum(fond[..., None], 1) * 255, 0, 255)
    # Niveaux : le papier légèrement grisé devient blanc pur, l'encre est renforcée.
    haut, bas = 225.0, 30.0
    f = np.clip((f - bas) / (haut - bas) * 255, 0, 255)
    if opaque:
        return Image.fromarray(f.astype(np.uint8), "RGB")
    alpha = (255 - f.min(axis=2)) / 255.0
    with np.errstate(invalid="ignore", divide="ignore"):
        coul = np.where(alpha[..., None] > 0, (f - 255 * (1 - alpha[..., None])) / alpha[..., None], 0)
    rgba = np.dstack([np.clip(coul, 0, 255), alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def rogner(im, marge):
    if im.mode == "RGBA":
        masque = np.array(im)[..., 3] > 20
    else:
        masque = np.array(im.convert("L")) < 235
    ys, xs = np.nonzero(masque)
    if len(xs) == 0:
        return im
    x0, x1 = max(xs.min() - marge, 0), min(xs.max() + marge + 1, im.width)
    y0, y1 = max(ys.min() - marge, 0), min(ys.max() + marge + 1, im.height)
    return im.crop((x0, y0, x1, y1))


def cmd_capture(a):
    img = rendre_page(a.fichier, a.page, a.dpi)
    if a.rotation:
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), a.rotation, 1.0)
        img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255))
    h, w = img.shape[:2]
    x0, y0, x1, y1 = a.zone
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        sys.exit("--zone attend x0 y0 x1 y1 entre 0 et 1, avec x0 < x1 et y0 < y1")
    img = img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    im = Image.fromarray(img) if a.brut else nettoyer(img, a.opaque)
    if not a.brut:
        im = rogner(im, int(a.dpi / 25))
    if a.largeur and im.width > a.largeur:
        im = im.resize((a.largeur, round(im.height * a.largeur / im.width)), Image.LANCZOS)
    a.sortie.parent.mkdir(parents=True, exist_ok=True)
    im.save(a.sortie, optimize=True)
    print(f"→ {a.sortie} ({im.width}×{im.height})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    pp = s.add_parser("pages", help="rendre les pages en PNG")
    pp.add_argument("fichier")
    pp.add_argument("-o", "--sortie", type=Path, required=True, help="dossier de sortie")
    pp.add_argument("--dpi", type=int, default=110)
    pp.add_argument("--de", type=int, default=1, help="première page (défaut 1)")
    pp.add_argument("--a", type=int, help="dernière page (défaut : la dernière)")
    pp.add_argument("--grille", action="store_true", help="superposer une grille de repérage")
    pp.set_defaults(f=cmd_pages)
    pc = s.add_parser("capture", help="capturer une zone nettoyée")
    pc.add_argument("fichier")
    pc.add_argument("--page", type=int, default=1)
    pc.add_argument("--zone", type=float, nargs=4, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    pc.add_argument("-o", "--sortie", type=Path, required=True, help="fichier .png")
    pc.add_argument("--dpi", type=int, default=300)
    pc.add_argument("--rotation", type=float, default=0, help="redresser (degrés, sens trigo)")
    pc.add_argument("--largeur", type=int, default=1400, help="largeur max en pixels (0 = aucune)")
    pc.add_argument("--brut", action="store_true", help="aucun nettoyage")
    pc.add_argument("--opaque", action="store_true", help="nettoyer mais garder le fond blanc")
    pc.set_defaults(f=cmd_capture)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
