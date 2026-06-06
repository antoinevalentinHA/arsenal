#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-1 : tout changelog AJOUTÉ doit être référencé
#   dans changelog/index.md.
#
# Contrôle de FLUX, pas de STOCK : seuls les fichiers AJOUTÉS dans le
# diff (git diff --diff-filter=A BASE..HEAD) sous changelog/changelogs/**
# sont vérifiés. L'historique gelé n'est JAMAIS contrôlé (on ne lit ni
# ne réécrit les fichiers gelés ; on vérifie uniquement l'index NON gelé).
#
# Réutilise strip_fenced_code de scripts/docs_navigation/audit_doc_links.py
# (importé, NON modifié) afin qu'une référence d'exemple placée dans un
# bloc de code de l'index ne soit pas comptée comme un vrai référencement.
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.
#
# Usage :
#   python docs_ci_changelog_index.py --base <ref_base> [--head <ref>]
#   (hôte : étape pull_request de .github/workflows/docs.yml)
# ==========================================================
from __future__ import annotations

import argparse
import os
import subprocess
import sys

# --- Réutilisation de strip_fenced_code SANS modifier audit_doc_links.py ----
_HERE = os.path.dirname(os.path.abspath(__file__))
_NAV = os.path.normpath(os.path.join(_HERE, "..", "docs_navigation"))
if _NAV not in sys.path:
    sys.path.insert(0, _NAV)
try:
    from audit_doc_links import strip_fenced_code  # type: ignore
except Exception:  # repli minimal et identique si l'import échoue
    def strip_fenced_code(lines):
        out, in_fence = [], False
        for idx, line in enumerate(lines, start=1):
            if line.strip().startswith("```"):
                out.append((idx, line, True))
                in_fence = not in_fence
                continue
            out.append((idx, line, in_fence))
        return out

DEFAULT_INDEX = "00_documentation_arsenal/changelog/index.md"
DEFAULT_ROOT = "00_documentation_arsenal/changelog/changelogs"


def added_changelog_files(base: str, head: str, root: str) -> list[str]:
    """Fichiers .md AJOUTÉS sous `root` entre base et head (lecture seule)."""
    cmd = ["git", "diff", "--name-only", "--diff-filter=A", base, head, "--", root]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write("erreur: git diff a échoué: " + res.stderr.strip() + "\n")
        raise RuntimeError("git diff failed")
    return [ln.strip() for ln in res.stdout.splitlines()
            if ln.strip().lower().endswith(".md")]


def index_haystack(index_path: str) -> str:
    """Contenu de l'index, blocs de code retirés (références réelles seulement)."""
    with open(index_path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return "\n".join(line for _, line, in_fence in strip_fenced_code(lines)
                     if not in_fence)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-1 : référencement obligatoire des nouveaux changelogs.")
    ap.add_argument("--base", default=os.environ.get("DOC_CI_BASE"),
                    help="ref/SHA de base du diff (base de la pull request).")
    ap.add_argument("--head", default="HEAD", help="ref/SHA de tête (défaut: HEAD).")
    ap.add_argument("--index", default=DEFAULT_INDEX,
                    help=f"index canonique (défaut: {DEFAULT_INDEX}).")
    ap.add_argument("--changelog-root", default=DEFAULT_ROOT,
                    help=f"racine des changelogs (défaut: {DEFAULT_ROOT}).")
    args = ap.parse_args(argv)

    # Hors contexte de diff (ex. push sans base fournie) : non applicable,
    # on ne bloque pas (fail-open volontaire, le contrôle est PR-centré).
    if not args.base:
        print("DOC-CI-1 : aucune base de diff (--base/DOC_CI_BASE) — "
              "contrôle non applicable hors pull_request.")
        return 0

    if not os.path.isfile(args.index):
        sys.stderr.write(f"erreur: index introuvable: {args.index}\n")
        return 2

    try:
        adds = added_changelog_files(args.base, args.head, args.changelog_root)
    except RuntimeError:
        return 2

    if not adds:
        print("DOC-CI-1 : aucun changelog ajouté dans le diff — conforme.")
        return 0

    index_dir = os.path.dirname(os.path.abspath(args.index))
    haystack = index_haystack(args.index)

    violations: list[tuple[str, str]] = []
    for f in adds:
        # Jeton attendu = chemin du fichier relatif au dossier de l'index,
        # soit la forme de lien inline ARB-3 « changelogs/<v>/<fichier>.md ».
        token = os.path.relpath(os.path.abspath(f), index_dir).replace("\\", "/")
        if token not in haystack:
            violations.append((f, token))

    if violations:
        index_rel = os.path.relpath(args.index)
        for f, token in sorted(violations):
            print(f"DOC-CI-1\t{f}\tnon référencé dans {index_rel} "
                  f"(attendu une référence à « {token} »)")
        print("-" * 60)
        print(f"DOC-CI-1: {len(violations)}")
        print(f"TOTAL: {len(violations)}")
        return 1

    print(f"DOC-CI-1 : {len(adds)} changelog(s) ajouté(s), tous référencés — conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
