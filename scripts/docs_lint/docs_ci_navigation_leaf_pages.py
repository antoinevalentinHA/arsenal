#!/usr/bin/env python3
# ==========================================================
# Arsenal — DOC-CI-6 : invariant R-NAV-LEAF-1
#   « Tout lien Markdown réel pointant vers un dossier documentaire
#     doit cibler un dossier doté d'une page d'entrée (README.md ou
#     index.md), sauf exemption explicite. »
#
# Énumération COMPLÈTE (aucun diff) sous 00_documentation_arsenal/ :
# robuste aux push directs, renommages et suppressions. Tourne sur
# push ET pull_request, sans base ni profondeur de clone particulière.
#
# Portée STRICTE — ne traite QUE les liens-dossiers :
#   - liens Markdown inline réels [label](cible) uniquement ;
#   - blocs de code clôturés et spans de code inline (`...`) ignorés ;
#   - liens externes / mailto / ancres pures ignorés ;
#   - cible résolue relativement au fichier source ;
#   - SEULES les cibles qui sont des dossiers EXISTANTS sont retenues.
# Hors portée (autres invariants, volontairement non couverts ici) :
#   - liens-fichiers (cible « ....md ») ;
#   - liens morts (cible inexistante) — relève d'un check « cibles » ;
#   - références en backticks / atteignabilité globale.
#
# Réutilise iter_markdown_files et strip_fenced_code de
# scripts/docs_navigation/audit_doc_links.py (importés, NON modifiés).
#
# Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
# Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.
#
# Usage :
#   python scripts/docs_lint/docs_ci_navigation_leaf_pages.py
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
if _NAV not in sys.path:
    sys.path.insert(0, _NAV)
from audit_doc_links import iter_markdown_files, strip_fenced_code  # noqa: E402

DOC_ROOT_DEFAULT = "00_documentation_arsenal"

# Exemptions DOCUMENTÉES (préfixes de chemin-cible, POSIX, depuis la racine
# du dépôt). Une seule, bornée et justifiée :
#   - 00_documentation_arsenal/changelog/ : zone changelog historique
#     (archive append-only « changelogs/v00..v15 » + « chantiers/ »,
#     routée par changelog/index.md). On n'y ajoute pas de page d'entrée
#     par dossier ; un lien qui y pointe référence de l'historique, pas
#     une porte de navigation à maintenir.
# Toute exemption supplémentaire doit rester bornée et justifiée ici même.
EXEMPT_TARGET_PREFIXES = (
    "00_documentation_arsenal/changelog/",
)

# Lien Markdown inline réel : [label](cible). La cible s'arrête au premier
# blanc (gère « [x](path "title") ») et avant la parenthèse fermante.
INLINE_LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+?)\s*\)")
# Spans de code inline : neutralisés (conservation des offsets) pour ne pas
# confondre une illustration de syntaxe `[..](..)` avec un vrai lien.
INLINE_CODE = re.compile(r"`[^`]*`")

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#")
_ABS_HA = "/homeassistant/00_documentation_arsenal/"
_ABS_DOC = "/00_documentation_arsenal/"


def _blank_inline_code(line: str) -> str:
    return INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)


def _resolve(token: str, source: Path) -> Path:
    """Résout un token de lien en chemin POSIX depuis la racine du dépôt."""
    if token.startswith(_ABS_HA):
        return Path(token.replace("/homeassistant/", "", 1))
    if token.startswith(_ABS_DOC):
        return Path(token.lstrip("/"))
    if token.startswith(DOC_ROOT_DEFAULT + "/"):
        return Path(token)
    return Path(os.path.normpath(source.parent / token))


def _is_exempt(rel_target: str, prefixes: tuple[str, ...]) -> bool:
    return rel_target.startswith(prefixes)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="DOC-CI-6 (R-NAV-LEAF-1) : un lien-dossier doit cibler "
                    "un dossier doté de README.md ou index.md.")
    ap.add_argument("--doc-root", default=DOC_ROOT_DEFAULT,
                    help=f"racine documentaire (défaut: {DOC_ROOT_DEFAULT}).")
    ap.add_argument("--except-prefix", action="append", dest="excepts", default=[],
                    help="préfixe-cible additionnel à exempter (documenté).")
    args = ap.parse_args(argv)

    doc_root = Path(args.doc_root)
    if not doc_root.is_dir():
        sys.stderr.write(f"erreur: racine documentaire introuvable: {doc_root}\n")
        return 2

    prefixes = EXEMPT_TARGET_PREFIXES + tuple(args.excepts)

    controlled = 0
    exempted = 0
    violations: list[tuple[str, int, str]] = []

    for path in iter_markdown_files(doc_root):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            sys.stderr.write(f"erreur: lecture impossible: {path} ({exc})\n")
            return 2

        for line_no, line, in_fence in strip_fenced_code(lines):
            if in_fence:
                continue
            for match in INLINE_LINK.finditer(_blank_inline_code(line)):
                raw = match.group(1).strip()
                if not raw or raw.startswith(EXTERNAL_PREFIXES):
                    continue
                token = raw.split("#", 1)[0].split("?", 1)[0]
                if not token or token.endswith(".md"):
                    # lien-fichier ou ancre pure -> hors portée
                    continue
                target = _resolve(token, path)
                if not target.is_dir():
                    # cible inexistante (lien mort) ou fichier -> hors portée
                    continue

                controlled += 1
                rel_target = target.as_posix()
                has_entry = (target / "README.md").is_file() or \
                            (target / "index.md").is_file()
                if has_entry:
                    continue
                if _is_exempt(rel_target, prefixes):
                    exempted += 1
                    continue
                violations.append((path.as_posix(), line_no, rel_target))

    if violations:
        for src, line_no, rel_target in sorted(violations):
            print(f"DOC-CI-6\t{src}:L{line_no}\t{rel_target}\t"
                  f"dossier sans README.md ni index.md")
        print("-" * 60)
        print(f"liens-dossiers contrôlés: {controlled} | exemptions: {exempted} | "
              f"violations: {len(violations)}")
        print(f"DOC-CI-6: {len(violations)}")
        print(f"TOTAL: {len(violations)}")
        return 1

    print(f"DOC-CI-6 : conforme — {controlled} lien(s)-dossier vérifié(s), "
          f"{exempted} exemption(s), 0 violation.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
