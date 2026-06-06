#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-5 (mode STOCK) : R-DOC-NAME-1
#   « Les seules pages d'index/atterrissage admises sont README.md
#     (atterrissage) et index.md (ToC). Tout fichier .md dont le basename
#     matche _index.md$ (p. ex. 00_index.md, NN_<famille>_index.md) est
#     interdit. »
#
# Objet : empêcher le retour des conventions de nommage minoritaires
# supprimées par GOV-1 (00_index.md, *_index.md). Contrôle de NOM
# uniquement — le rôle sémantique README vs index relève d'ARB-1 et
# n'est PAS vérifié ici (hors de portée d'une CI fiable).
#
# Énumération COMPLÈTE (aucun diff) : robuste aux push directs comme aux
# pull_request, sans base ni profondeur de clone particulière.
#
# Réutilise iter_markdown_files de scripts/docs_navigation/audit_doc_links.py
# (importé, NON modifié). Zone gelée (records de changelog) exclue, par
# cohérence avec DOC-CI-2/3 : les records sont intouchables.
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Aucun auto-fix. Aucune exception.
# Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.
#
# Usage :
#   python docs_ci_naming.py
#   (hôte : étape push + pull_request de .github/workflows/docs.yml)
# ==========================================================
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# Réutilisation sans modifier audit_doc_links.py.
_HERE = os.path.dirname(os.path.abspath(__file__))
_NAV = os.path.normpath(os.path.join(_HERE, "..", "docs_navigation"))
for _p in (_HERE, _NAV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from audit_doc_links import iter_markdown_files  # noqa: E402

DEFAULT_ROOT = "00_documentation_arsenal"
FROZEN_MARKER = "changelog/changelogs/"

# R-DOC-NAME-1 : nom d'index minoritaire (couvre 00_index.md et *_index.md).
# Ne matche NI index.md NI README.md (pas de « _ » précédant « index »).
MINORITY_INDEX = re.compile(r"_index\.md$")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-5 (stock) : R-DOC-NAME-1, interdit les noms "
                    "d'index minoritaires (00_index.md, *_index.md).")
    ap.add_argument("--root", default=DEFAULT_ROOT,
                    help=f"racine du périmètre (défaut: {DEFAULT_ROOT}).")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        sys.stderr.write(f"erreur: racine introuvable: {args.root}\n")
        return 2

    analysed = 0
    frozen = 0
    violations: list[str] = []
    for path in iter_markdown_files(Path(args.root)):
        rel = path.as_posix()
        if FROZEN_MARKER in rel:
            frozen += 1
            continue
        analysed += 1
        if MINORITY_INDEX.search(os.path.basename(rel)):
            violations.append(rel)

    if violations:
        for f in sorted(violations):
            print(f"DOC-CI-5\t{f}\tnom d'index minoritaire interdit "
                  f"(R-DOC-NAME-1) : renommer en README.md (atterrissage) "
                  f"ou index.md (ToC)")
        print("-" * 60)
        print(f"analysés: {analysed} | gel exclu: {frozen} | "
              f"violations: {len(violations)}")
        print(f"DOC-CI-5: {len(violations)}")
        print(f"TOTAL: {len(violations)}")
        return 1

    print(f"DOC-CI-5 : conforme — {analysed} fichiers analysés "
          f"({frozen} gelé(s) exclu(s)), 0 nom d'index minoritaire.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
