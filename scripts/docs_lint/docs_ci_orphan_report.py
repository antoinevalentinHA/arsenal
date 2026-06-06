#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-3 : tout rapport AJOUTÉ doit être référencé
#   dans audits/index.md.
#
# Contrôle de FLUX, pas de STOCK (comme DOC-CI-1) : seuls les fichiers
# .md AJOUTÉS dans le diff (git diff --diff-filter=A BASE..HEAD) sous
#   audits/01_rapports/**  et  audits/04_chantiers/**
# sont vérifiés. Choix assumé : l'état actuel comporte des rapports
# orphelins préexistants (hors NAV-1) qu'un gate de stock bloquerait à
# tort ; le flux scelle l'avenir sans correction opportuniste du passé.
#
# Réutilise la machinerie DOC-CI-1 (added_changelog_files / index_haystack),
# qui réutilise elle-même strip_fenced_code de audit_doc_links.py — aucun
# de ces deux modules n'est modifié.
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.
#
# Usage :
#   python docs_ci_orphan_report.py --base <ref_base> [--head <ref>]
#   (hôte : étape pull_request de .github/workflows/docs.yml)
# ==========================================================
from __future__ import annotations

import argparse
import os
import sys

# Réutilisation directe des helpers DOC-CI-1 (même dossier), NON modifiés.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from docs_ci_changelog_index import added_changelog_files, index_haystack  # noqa: E402

DEFAULT_INDEX = "00_documentation_arsenal/audits/index.md"
DEFAULT_ROOTS = (
    "00_documentation_arsenal/audits/01_rapports",
    "00_documentation_arsenal/audits/04_chantiers",
)

# Exceptions structurelles : un index ne se liste pas lui-même ; un README
# de dossier n'est pas un rapport. (Doctrine : exceptions structurelles,
# pas de confort.) Extensible via --except <glob_basename> si documenté.
STRUCTURAL_EXCEPTIONS = {"index.md", "README.md"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-3 : référencement obligatoire des nouveaux rapports.")
    ap.add_argument("--base", default=os.environ.get("DOC_CI_BASE"),
                    help="ref/SHA de base du diff (base de la pull request).")
    ap.add_argument("--head", default="HEAD", help="ref/SHA de tête (défaut: HEAD).")
    ap.add_argument("--index", default=DEFAULT_INDEX,
                    help=f"index des audits (défaut: {DEFAULT_INDEX}).")
    ap.add_argument("--root", action="append", dest="roots",
                    help="racine(s) de rapports (défaut: 01_rapports + 04_chantiers).")
    ap.add_argument("--except", action="append", dest="excepts", default=[],
                    help="basename additionnel à excepter (doctrine documentée).")
    args = ap.parse_args(argv)
    roots = args.roots or list(DEFAULT_ROOTS)
    excepted = STRUCTURAL_EXCEPTIONS | set(args.excepts)

    # Hors contexte de diff (push sans base) : non applicable, fail-open.
    if not args.base:
        print("DOC-CI-3 : aucune base de diff (--base/DOC_CI_BASE) — "
              "contrôle non applicable hors pull_request.")
        return 0

    if not os.path.isfile(args.index):
        sys.stderr.write(f"erreur: index introuvable: {args.index}\n")
        return 2

    # Fichiers .md ajoutés sous chaque racine (réutilise la détection CI-1).
    adds: list[str] = []
    try:
        for root in roots:
            adds.extend(added_changelog_files(args.base, args.head, root))
    except RuntimeError:
        return 2
    adds = sorted(set(adds))

    # Filtre des exceptions structurelles (par basename).
    adds = [f for f in adds if os.path.basename(f) not in excepted]

    if not adds:
        print("DOC-CI-3 : aucun rapport ajouté dans le diff — conforme.")
        return 0

    index_dir = os.path.dirname(os.path.abspath(args.index))
    haystack = index_haystack(args.index)

    violations: list[tuple[str, str]] = []
    for f in adds:
        # Jeton = chemin du rapport relatif au dossier de l'index (audits/),
        # soit la forme de lien utilisée dans audits/index.md.
        token = os.path.relpath(os.path.abspath(f), index_dir).replace("\\", "/")
        if token not in haystack:
            violations.append((f, token))

    if violations:
        index_rel = os.path.relpath(args.index)
        for f, token in sorted(violations):
            print(f"DOC-CI-3\t{f}\trapport orphelin : non référencé dans {index_rel} "
                  f"(attendu une référence à « {token} »)")
        print("-" * 60)
        print(f"DOC-CI-3: {len(violations)}")
        print(f"TOTAL: {len(violations)}")
        return 1

    print(f"DOC-CI-3 : {len(adds)} rapport(s) ajouté(s), tous référencés — conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
