#!/usr/bin/env python3
"""Rend les cartes d'un chapitre en images pour les vérifier visuellement.

Pour chaque carte, une image apercu/<id>.png montre la carte retournée (recto + verso)
sur téléphone, en mode clair et en mode sombre côte à côte. --ordi ajoute la vue ordinateur.
Les étapes « pas-à-pas » sont toutes affichées.

    python3 outils/apercu.py chapitres/physique/induction
    python3 outils/apercu.py chapitres/physique/induction --cartes id1 id2 --ordi
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import CSS, MATHJAX, lire_chapitre, quitter  # noqa: E402

CONFIG_MATHJAX = r"""
window.MathJax = {
  tex: { inlineMath: [['\\(', '\\)']], displayMath: [['\\[', '\\]']], processEscapes: false,
         packages: {'[+]': ['mhchem', 'mathtools', 'cancel', 'color', 'boldsymbol']} },
  loader: { load: ['[tex]/mhchem', '[tex]/mathtools', '[tex]/cancel', '[tex]/color', '[tex]/boldsymbol'] },
  startup: { pageReady: () => MathJax.startup.defaultPageReady().then(() => { window.__fini = true; }) }
};
"""


def page_html(carte, sombre, dossier_media):
    classe = "card nightMode night_mode" if sombre else "card"
    source = f'<div class="source">{carte.source}</div>' if carte.source else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<base href="{dossier_media.resolve().as_uri()}/">
<style>{CSS}
html, body {{ margin: 0; background: {'#1c1c1e' if sombre else '#ffffff'}; }}
.pas-a-pas.actif > li.cache {{ display: list-item; }}
</style>
<script>{CONFIG_MATHJAX}</script>
<script src="{MATHJAX.as_uri()}"></script>
</head><body class="{'nightMode night_mode' if sombre else ''}"><div class="{classe}">
<div class="contenu"><div class="recto">{carte.recto}</div><hr id="answer">
<div class="verso">{carte.verso}</div>{source}</div></div></body></html>"""


CAPTURE_JS = r"""
const { chromium } = require('playwright');
const jobs = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
(async () => {
  const navigateur = await chromium.launch();
  const erreurs = [];
  for (const j of jobs) {
    const page = await navigateur.newPage({ viewport: { width: j.largeur, height: 600 },
                                            deviceScaleFactor: j.echelle });
    page.on('console', m => { if (m.type() === 'error') erreurs.push(j.id + ' : ' + m.text()); });
    await page.goto('file://' + j.html);
    try { await page.waitForFunction(() => window.__fini === true, null, { timeout: 20000 }); }
    catch (e) { erreurs.push(j.id + ' : MathJax ne termine pas'); }
    const pb = await page.evaluate(() => {
      const r = [];
      document.querySelectorAll('mjx-merror, mjx-container [data-mjx-error]').forEach(e =>
        r.push('erreur MathJax : ' + (e.getAttribute('data-mjx-error') || e.textContent).slice(0, 120)));
      document.querySelectorAll('img').forEach(i => { if (!i.complete || i.naturalWidth === 0)
        r.push('image non chargée : ' + i.getAttribute('src')); });
      if (document.documentElement.scrollWidth > window.innerWidth + 1)
        r.push('déborde en largeur (' + document.documentElement.scrollWidth + 'px)');
      return r;
    });
    pb.forEach(x => erreurs.push(j.id + ' [' + j.vue + '] ' + x));
    await page.screenshot({ path: j.png, fullPage: true });
    await page.close();
  }
  await navigateur.close();
  console.log(JSON.stringify(erreurs));
})();
"""


def assembler(images, sortie):
    ims = [Image.open(i) for i in images]
    marge = 12
    w = sum(i.width for i in ims) + marge * (len(ims) - 1)
    h = max(i.height for i in ims)
    out = Image.new("RGB", (w, h), (128, 128, 128))
    x = 0
    for i in ims:
        out.paste(i, (x, 0))
        x += i.width + marge
    out.save(sortie, optimize=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("chapitre", type=Path)
    p.add_argument("--cartes", nargs="+", help="seulement ces identifiants")
    p.add_argument("--ordi", action="store_true", help="ajouter la vue ordinateur")
    a = p.parse_args()
    if not MATHJAX.exists():
        quitter("MathJax absent : lancer bash outils/installer.sh")
    try:
        chap = lire_chapitre(a.chapitre)
    except ValueError as e:
        quitter(f"Erreur : {e}")
    cartes = [c for c in chap.cartes if not a.cartes or c.id in a.cartes]
    if not cartes:
        quitter("Aucune carte correspondante.")
    dossier = a.chapitre / "apercu"
    dossier.mkdir(exist_ok=True)
    vues = [("tel-clair", 412, False, 2), ("tel-sombre", 412, True, 2)]
    if a.ordi:
        vues.append(("ordi", 1000, False, 1))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        jobs = []
        for c in cartes:
            for nom, largeur, sombre, echelle in vues:
                html = tmp / f"{c.id}-{nom}.html"
                html.write_text(page_html(c, sombre, a.chapitre / "media"), encoding="utf-8")
                jobs.append({"id": c.id, "vue": nom, "html": str(html), "png": str(tmp / f"{c.id}-{nom}.png"),
                             "largeur": largeur, "echelle": echelle})
        (tmp / "jobs.json").write_text(json.dumps(jobs))
        (tmp / "capture.js").write_text(CAPTURE_JS)
        r = subprocess.run(["node", str(tmp / "capture.js"), str(tmp / "jobs.json")],
                           capture_output=True, text=True)
        if r.returncode != 0:
            quitter(r.stderr[-2000:])
        erreurs = json.loads(r.stdout.strip().splitlines()[-1])
        for c in cartes:
            tel = [tmp / f"{c.id}-{n}.png" for n in ("tel-clair", "tel-sombre")]
            assembler(tel, dossier / f"{c.id}.png")
            if a.ordi:
                shutil.copy(tmp / f"{c.id}-ordi.png", dossier / f"{c.id}-ordi.png")
    for e in erreurs:
        print(f"  PROBLÈME {e}")
    print(f"{len(cartes)} aperçu(s) dans {dossier}/" + ("" if erreurs else " — aucun problème détecté"))


if __name__ == "__main__":
    main()
