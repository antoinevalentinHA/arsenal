#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-2 : cohérence des compteurs de contrats/index.md.
#
# Invariant : dans la table « Domaine | Fichiers | … » de
# contrats/index.md, l'entier de la colonne « Fichiers » de chaque
# ligne doit égaler le nombre TOTAL de fichiers .md sous le dossier lié,
# en RÉCURSIF, README/index INCLUS (convention rec_all), zone gelée
# (changelog/changelogs/**) exclue.
#
# Périmètre : contrats/index.md UNIQUEMENT. Seul l'entier de la colonne
# « Fichiers » est lu ; aucune prose (Navigation/Description) n'est analysée.
# Les blocs de code sont neutralisés (strip_fenced_code) pour ne pas
# parser une table d'exemple.
#
# Réutilise iter_markdown_files de scripts/docs_navigation/audit_doc_links.py
# et strip_fenced_code (via le même module), AUCUN n'est modifié.
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Codes de sortie : 0 conforme, 1 écart(s), 2 erreur d'usage/infra.
#
# Usage :
#   python docs_ci_contract_counts.py
#   (hôte : étape push + pull_request de .github/workflows/docs.yml)
# ==========================================================
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_NAV = os.path.normpath(os.path.join(_HERE, "..", "docs_navigation"))
if _NAV not in sys.path:
    sys.path.insert(0, _NAV)
from audit_doc_links import iter_markdown_files, strip_fenced_code  # noqa: E402

DEFAULT_INDEX = "00_documentation_arsenal/contrats/index.md"
FROZEN_MARKER = "changelog/changelogs/"

# Ligne de table : 1re cellule = lien [dossier/](./dossier/) ; 2e cellule = entier.
ROW = re.compile(r"^\|\s*\[\s*([A-Za-z0-9_]+)/\s*\]\([^)]*\)\s*\|\s*(\d+)\s*\|")


def rec_all_count(directory: Path) -> int:
    """Nombre de .md sous `directory` en récursif, README/index inclus,
    zone gelée exclue (convention rec_all)."""
    return sum(
        1 for p in iter_markdown_files(directory)
        if FROZEN_MARKER not in p.as_posix()
    )


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-2 : cohérence des compteurs de contrats/index.md (rec_all).")
    ap.add_argument("--index", default=DEFAULT_INDEX,
                    help=f"index des contrats (défaut: {DEFAULT_INDEX}).")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.index):
        sys.stderr.write(f"erreur: index introuvable: {args.index}\n")
        return 2

    index_dir = os.path.dirname(os.path.abspath(args.index))
    with open(args.index, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    checked = 0
    violations: list[tuple[str, int, int]] = []
    for _, line, in_fence in strip_fenced_code(lines):
        if in_fence:
            continue
        m = ROW.match(line)
        if not m:
            continue
        domain, declared = m.group(1), int(m.group(2))
        checked += 1
        real = rec_all_count(Path(index_dir) / domain)
        if real != declared:
            violations.append((domain, declared, real))

    index_rel = os.path.relpath(args.index)
    if violations:
        for domain, declared, real in sorted(violations):
            print(f"DOC-CI-2\t{index_rel}\t{domain}/ : déclaré={declared} réel={real} "
                  f"(rec_all : .md récursif, README/index inclus, gel exclu)")
        print("-" * 60)
        print(f"lignes contrôlées: {checked} | écarts: {len(violations)}")
        print(f"DOC-CI-2: {len(violations)}")
        print(f"TOTAL: {len(violations)}")
        return 1

    print(f"DOC-CI-2 : conforme — {checked} compteur(s) vérifié(s), 0 écart.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
