#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle structurel — Registre des chantiers Arsenal.

Invariant vérifié (unique, volontairement étroit) :
    tout lien Markdown relatif du fichier
    `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md`
    doit pointer vers un fichier (ou dossier) existant.

Le registre est un INDEX D'ÉTAT : sa seule promesse vérifiable mécaniquement
est qu'aucune de ses cibles n'est morte. Ce contrôle NE juge PAS le statut
métier (ouvert/clos) — celui-ci relève du document source, qui fait foi.

Portée :
    - liens relatifs uniquement (les ancres `#...` et les commits sont ignorés) ;
    - URLs absolues (http/https) ignorées ;
    - lecture seule, déterministe, sans dépendance hors stdlib.

Sortie :
    - exit 0 : toutes les cibles existent ;
    - exit 1 : au moins une cible manque (rapport ligne par ligne) ;
    - exit 2 : erreur d'exécution (registre introuvable, etc.).
"""

import os
import re
import sys

# Racine du dépôt = deux niveaux au-dessus de scripts/arsenal_contracts/
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRE = os.path.join(
    REPO_ROOT, "00_documentation_arsenal", "audits", "REGISTRE_CHANTIERS.md"
)

# Capture le contenu des parenthèses d'un lien Markdown `](...)`.
LINK_RE = re.compile(r"\]\(([^)]+)\)")


def cibles(md_text):
    """Liste (cible_nettoyée, brut) des liens relatifs à vérifier."""
    out = []
    for brut in LINK_RE.findall(md_text):
        cible = brut.strip()
        # Ignore les ancres pures et les URLs absolues.
        if cible.startswith("#") or cible.startswith("http://") or cible.startswith("https://"):
            continue
        # Retire l'ancre éventuelle (`fichier.md#section`).
        cible = cible.split("#", 1)[0]
        if cible:
            out.append((cible, brut))
    return out


def main():
    if not os.path.isfile(REGISTRE):
        print(f"::error::Registre introuvable : {REGISTRE}", file=sys.stderr)
        return 2

    base = os.path.dirname(REGISTRE)
    with open(REGISTRE, "r", encoding="utf-8") as fh:
        texte = fh.read()

    manquants = []
    total = 0
    for cible, brut in cibles(texte):
        total += 1
        resolu = os.path.normpath(os.path.join(base, cible))
        if not os.path.exists(resolu):
            rel = os.path.relpath(resolu, REPO_ROOT)
            manquants.append((brut, rel))

    if manquants:
        print(f"REGISTRE_CHANTIERS — {len(manquants)}/{total} cible(s) manquante(s) :")
        for brut, rel in manquants:
            print(f"  MANQUANT  {brut}  ->  {rel}")
        print("::error::Le registre des chantiers contient au moins un lien cassé.")
        return 1

    print(f"REGISTRE_CHANTIERS — OK : {total} cible(s), 0 manquante.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
