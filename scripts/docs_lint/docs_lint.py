#!/usr/bin/env python3
# ==========================================================
# Arsenal — Lint documentaire (lecture seule)
#   R-DOC-FNAME-1 : aucun composant de chemin ne contient d'espace
#   R-DOC-H1-1    : tout .md ouvre sur un H1 ATX exploitable (1re ligne)
#
# Lecture seule : ce script n'écrit, ne crée et ne supprime aucun fichier.
# Code de sortie : 0 = conforme, 1 = violation(s), 2 = erreur d'usage.
#
# Usage :
#   python docs_lint.py [PERIMETRE ...]            # défaut : 00_documentation_arsenal
#   python docs_lint.py --json
#   python docs_lint.py --exceptions chemin.txt
#
# Exceptions (sidecar, optionnel) — une entrée par ligne, '#' = commentaire :
#   REGLE:glob_relatif_au_perimetre
#   ex.  R-DOC-H1-1:contrats/**/registres_*.md
#        R-DOC-FNAME-1:**/fichier avec espace.md
# ==========================================================
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
import unicodedata

DEFAULT_PERIMETER = "00_documentation_arsenal"

# Frontière de doctrine (NON un contournement de confort) : le sous-arbre
# changelog/changelogs/** est un record historique versionné, déclaré
# intouchable par audits/01_rapports/documentation/audit_structure_documentaire.md
# (« ni réécriture de fond, ni renommage »). Il est donc HORS PÉRIMÈTRE des
# invariants, et exclu par construction. --include-frozen lève l'exclusion
# (usage audit uniquement).
FROZEN_PREFIXES = ("changelog/changelogs/",)

# Caractères de décoration ignorés lors de l'extraction du texte d'un titre.
DECORATION = set("=-_*~# \t")

ATX_H1 = re.compile(r"^#(?!#)\s*(.*)$")  # '# ...' mais pas '## ...'


def has_extractable_text(title_body: str) -> bool:
    """Vrai si, après retrait de la décoration et des symboles/emoji,
    il reste au moins un caractère alphanumérique (lettre ou chiffre)."""
    for ch in title_body:
        if ch in DECORATION:
            continue
        cat = unicodedata.category(ch)  # 'L*' lettres, 'N*' chiffres
        if cat[0] in ("L", "N"):
            return True
    return False


def load_exceptions(path: str | None) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not path:
        return out
    if not os.path.isfile(path):
        sys.stderr.write(f"avertissement: fichier d'exceptions introuvable: {path}\n")
        return out
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                sys.stderr.write(f"avertissement: exception ignorée (format REGLE:glob): {line}\n")
                continue
            rule, glob = line.split(":", 1)
            out.setdefault(rule.strip(), []).append(glob.strip())
    return out


def is_excepted(rule: str, rel: str, exceptions: dict[str, list[str]]) -> bool:
    for glob in exceptions.get(rule, ()):
        if fnmatch.fnmatch(rel, glob):
            return True
    return False


def iter_files(roots: list[str]):
    """Itère (chemin_absolu, racine) pour tout fichier sous chaque racine,
    en ignorant .git. Les racines inexistantes sont signalées."""
    for root in roots:
        if not os.path.exists(root):
            sys.stderr.write(f"avertissement: périmètre inexistant: {root}\n")
            continue
        if os.path.isfile(root):
            yield os.path.abspath(root), os.path.dirname(os.path.abspath(root)) or "."
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d != ".git"]
            for name in filenames:
                yield os.path.join(dirpath, name), root


def first_line(path: str) -> str | None:
    """Première ligne du fichier, BOM retiré. None si illisible."""
    try:
        with open(path, "r", encoding="utf-8", errors="strict") as fh:
            line = fh.readline()
    except (UnicodeDecodeError, OSError):
        return None
    return line.lstrip("\ufeff").rstrip("\n").rstrip("\r")


def lint(roots: list[str], exceptions: dict[str, list[str]], include_frozen: bool = False):
    violations: list[dict] = []
    excluded_frozen = 0

    def rel_to(path: str, root: str) -> str:
        base = root if os.path.isdir(root) else os.path.dirname(root) or "."
        return os.path.relpath(path, base)

    for abspath, root in iter_files(roots):
        rel = rel_to(abspath, root)
        rel_posix = rel.replace("\\", "/")

        # Frontière de doctrine : sous-arbre historique gelé, hors invariants.
        if not include_frozen and any(rel_posix.startswith(p) for p in FROZEN_PREFIXES):
            if abspath.lower().endswith(".md"):
                excluded_frozen += 1
            continue

        # R-DOC-FNAME-1 — espace dans un composant de chemin
        offenders = [seg for seg in rel_posix.split("/") if " " in seg or "\t" in seg]
        if offenders and not is_excepted("R-DOC-FNAME-1", rel, exceptions):
            violations.append({
                "rule": "R-DOC-FNAME-1",
                "path": rel,
                "detail": f"composant avec espace: {offenders[0]!r}",
            })

        # R-DOC-H1-1 — première ligne = H1 ATX exploitable (.md uniquement)
        if abspath.lower().endswith(".md") and not is_excepted("R-DOC-H1-1", rel, exceptions):
            line = first_line(abspath)
            if line is None:
                violations.append({"rule": "R-DOC-H1-1", "path": rel,
                                   "detail": "fichier illisible en UTF-8"})
            else:
                m = ATX_H1.match(line)
                if not m:
                    violations.append({"rule": "R-DOC-H1-1", "path": rel,
                                       "detail": f"1re ligne non-H1: {line[:60]!r}"})
                elif not has_extractable_text(m.group(1)):
                    violations.append({"rule": "R-DOC-H1-1", "path": rel,
                                       "detail": f"H1 sans texte exploitable: {line[:60]!r}"})

    return violations, excluded_frozen


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Lint documentaire Arsenal (lecture seule).")
    ap.add_argument("perimeter", nargs="*", default=[DEFAULT_PERIMETER],
                    help=f"racines à analyser (défaut: {DEFAULT_PERIMETER})")
    ap.add_argument("--exceptions", help="sidecar d'exceptions explicites (REGLE:glob)")
    ap.add_argument("--include-frozen", action="store_true",
                    help="lève l'exclusion du record historique gelé (audit uniquement)")
    ap.add_argument("--json", action="store_true", help="sortie JSON machine")
    args = ap.parse_args(argv)

    roots = args.perimeter or [DEFAULT_PERIMETER]
    exceptions = load_exceptions(args.exceptions)
    violations, excluded_frozen = lint(roots, exceptions, include_frozen=args.include_frozen)

    by_rule: dict[str, int] = {}
    for v in violations:
        by_rule[v["rule"]] = by_rule.get(v["rule"], 0) + 1

    if args.json:
        json.dump({"violations": violations, "summary": by_rule,
                   "total": len(violations), "excluded_frozen": excluded_frozen},
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        if excluded_frozen:
            print(f"(exclus — record historique gelé, hors invariants: {excluded_frozen})")
        if not violations:
            print(f"OK — aucun écart. Périmètre: {', '.join(roots)}")
        else:
            for v in sorted(violations, key=lambda x: (x["rule"], x["path"])):
                print(f"{v['rule']}\t{v['path']}\t{v['detail']}")
            print("-" * 60)
            for rule in sorted(by_rule):
                print(f"{rule}: {by_rule[rule]}")
            print(f"TOTAL: {len(violations)}")

    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
