#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-3 (mode STOCK) : invariant de complétude
#   « tout fichier .md sous audits/01_rapports/** et audits/04_chantiers/**
#     est référencé dans audits/index.md ».
#
# Énumération COMPLÈTE (aucun diff) : robuste aux suppressions de
# référence, aux renommages et aux push directs — angles morts du
# mode flux antérieur, désormais remplacé. Tourne sur push ET
# pull_request, sans base ni profondeur de clone particulière.
#
# Réutilise iter_markdown_files de scripts/docs_navigation/audit_doc_links.py
# (importé, NON modifié) et index_haystack de DOC-CI-1 (qui retire les blocs
# de code via strip_fenced_code, pour ne pas compter une référence d'exemple).
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Codes de sortie : 0 conforme, 1 orphelin(s), 2 erreur d'usage/infra.
#
# Usage :
#   python docs_ci_orphan_report.py
#   (hôte : étape push + pull_request de .github/workflows/docs.yml)
# ==========================================================
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Réutilisation sans modifier audit_doc_links.py ni le script DOC-CI-1.
_HERE = os.path.dirname(os.path.abspath(__file__))
_NAV = os.path.normpath(os.path.join(_HERE, "..", "docs_navigation"))
for _p in (_HERE, _NAV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from audit_doc_links import iter_markdown_files       # noqa: E402
from docs_ci_changelog_index import index_haystack    # noqa: E402

DEFAULT_INDEX = "00_documentation_arsenal/audits/index.md"
DEFAULT_ROOTS = (
    "00_documentation_arsenal/audits/01_rapports",
    "00_documentation_arsenal/audits/04_chantiers",
)

# Exceptions STRUCTURELLES uniquement (un index ne se liste pas lui-même ;
# un README de dossier n'est pas un rapport). Pas d'exception de confort.
STRUCTURAL_EXCEPTIONS = {"index.md", "README.md"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-3 (stock) : invariant de complétude de l'index des audits.")
    ap.add_argument("--index", default=DEFAULT_INDEX,
                    help=f"index des audits (défaut: {DEFAULT_INDEX}).")
    ap.add_argument("--root", action="append", dest="roots",
                    help="racine(s) de rapports (défaut: 01_rapports + 04_chantiers).")
    ap.add_argument("--except", action="append", dest="excepts", default=[],
                    help="basename additionnel à excepter (structurel, documenté).")
    args = ap.parse_args(argv)
    roots = args.roots or list(DEFAULT_ROOTS)
    excepted = STRUCTURAL_EXCEPTIONS | set(args.excepts)

    if not os.path.isfile(args.index):
        sys.stderr.write(f"erreur: index introuvable: {args.index}\n")
        return 2

    index_dir = os.path.dirname(os.path.abspath(args.index))
    haystack = index_haystack(args.index)

    analysed = 0
    excepted_n = 0
    orphans: list[str] = []
    for root in roots:
        for path in iter_markdown_files(Path(root)):
            analysed += 1
            rel = path.as_posix()
            if os.path.basename(rel) in excepted:
                excepted_n += 1
                continue
            token = os.path.relpath(os.path.abspath(rel), index_dir).replace("\\", "/")
            if token not in haystack:
                orphans.append(rel)

    referenced = analysed - excepted_n - len(orphans)
    index_rel = os.path.relpath(args.index)

    if orphans:
        for f in sorted(orphans):
            token = os.path.relpath(os.path.abspath(f), index_dir).replace("\\", "/")
            print(f"DOC-CI-3\t{f}\trapport orphelin : non référencé dans {index_rel} "
                  f"(attendu une référence à « {token} »)")
        print("-" * 60)
        print(f"analysés: {analysed} | référencés: {referenced} | "
              f"exceptions: {excepted_n} | orphelins: {len(orphans)}")
        print(f"DOC-CI-3: {len(orphans)}")
        print(f"TOTAL: {len(orphans)}")
        return 1

    print(f"DOC-CI-3 : conforme — {analysed} analysés, {referenced} référencés, "
          f"{excepted_n} exception(s) structurelle(s), 0 orphelin.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
