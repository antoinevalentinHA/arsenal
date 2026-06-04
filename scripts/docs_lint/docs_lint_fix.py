#!/usr/bin/env python3
# ==========================================================
# Arsenal — Applieur de conformité documentaire (idempotent)
#
# Corrige R-DOC-H1-1 (1re ligne = H1 ATX exploitable) sur le périmètre,
# en EXCLUANT par construction le sous-arbre historique gelé
# `changelog/changelogs/**` (doctrine : record versionné, ni réécriture
# ni renommage — cf. audits/.../audit_structure_documentaire.md).
#
# Dry-run par DÉFAUT (aucune écriture). --apply pour écrire.
# Idempotent : re-passer l'applieur sur un corpus déjà conforme ne change rien.
#
# Transformations déterministes (uniquement si la 1re ligne viole l'invariant) :
#   [banner]   cartouche '# ===' / contenu / '# ==='  -> 1 H1 (contenu joint ' · ')
#   [ascii]    cartouche '===' / titre / '==='         -> '# <titre>' + reste
#   [relocate] <!-- ... --> ou > ... en tête, H1 présent dessous -> tête déplacée sous le H1
#   [promote]  ## / ### ... en 1re ligne                -> # ...
#   [blanks]   lignes vides en tête                     -> retirées
#   [prose]    prose nue en tête (titre évident)        -> préfixée '# '
#
# NE TRAITE PAS (à arbitrer / titre à inventer) : voir --list-held.
# ==========================================================
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import sys
import unicodedata

DEFAULT_PERIMETER = "00_documentation_arsenal"
FROZEN_GLOBS = ("changelog/changelogs/**",)  # doctrine : intouchable
DECO = set("=-_*~# \t")

# --- Overrides nommés (décisions explicites, hors heuristique) ----------------
# B — snippets sans titre : titre minimal préfixé en tête.
NAMED_TITLES = {
    "architecture/00_structure_includes/logbook.md": "# Include — logbook.yaml",
    "architecture/00_structure_includes/logger.md": "# Include — logger.yaml",
    "architecture/00_structure_includes/recorder.md": "# Include — recorder.yaml",
    "architecture/00_structure_includes/utility_meter.md": "# Include — utility_meter.yaml",
}
# C — fichier vide : stub titré explicite (ne pas supprimer).
STUBS = {
    "contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md": (
        "# Capteurs observabilité pure\n\n"
        "> Statut : fichier vide détecté lors du lint documentaire.\n"
        "> Contenu à compléter ou suppression à arbitrer dans un chantier dédié.\n"
    ),
}

H1 = re.compile(r"^#(?!#)\s*(.*)$")
HN = re.compile(r"^(#{2,6})\s+(.*)$")
COMMENT = re.compile(r"^<!--.*-->\s*$")
QUOTE = re.compile(r"^>\s+\S")


def deco_only(s: str) -> bool:
    return s.strip() != "" and all(c in DECO for c in s)


def has_text(s: str) -> bool:
    return any(unicodedata.category(c)[0] in ("L", "N") for c in s if c not in DECO)


def usable_h1(line: str) -> bool:
    m = H1.match(line.lstrip("\ufeff"))
    return bool(m) and has_text(m.group(1))


def rel_under(path: str, root: str) -> str:
    return os.path.relpath(path, root).replace("\\", "/")


def is_frozen(rel: str) -> bool:
    return any(fnmatch.fnmatch(rel, g) for g in FROZEN_GLOBS)


def load_exceptions(path: str | None) -> set[str]:
    out: set[str] = set()
    if path and os.path.isfile(path):
        for raw in open(path, encoding="utf-8"):
            line = raw.strip()
            if line and not line.startswith("#") and ":" in line:
                rule, glob = line.split(":", 1)
                if rule.strip() == "R-DOC-H1-1":
                    out.add(glob.strip())
    return out


def join_title(pieces: list[str]) -> str:
    parts = [p.strip() for p in pieces if p.strip()]
    return "# " + " · ".join(parts)


def transform(lines: list[str]):
    """Renvoie (nouvelles_lignes, label) ou (None, raison_held)."""
    if not lines:
        return None, "fichier vide"
    work = list(lines)
    work[0] = work[0].lstrip("\ufeff")  # BOM
    label_bits = []

    # [blanks] retire les lignes vides de tête
    n0 = len(work)
    while work and work[0].strip() == "":
        work.pop(0)
    if len(work) != n0:
        label_bits.append("blanks")
    if not work:
        return None, "fichier sans contenu après blancs"

    first = work[0]

    # déjà conforme après strip des blancs
    if usable_h1(first) and not label_bits:
        return None, "déjà conforme"
    if usable_h1(first) and label_bits:
        return work, "+".join(label_bits)

    # [banner] cartouche '# ===' ... '# ==='
    mb = H1.match(first)
    if mb and deco_only(mb.group(1)):
        close = None
        for i in range(1, min(len(work), 9)):
            mm = H1.match(work[i])
            if mm and deco_only(mm.group(1)):
                close = i
                break
        if close is not None:
            content = []
            for i in range(1, close):
                mm = H1.match(work[i])
                if mm and has_text(mm.group(1)):
                    content.append(mm.group(1))
            if content:
                new = [join_title(content)] + work[close + 1:]
                return new, "+".join(label_bits + ["banner"])
        return None, "cartouche '# ===' non résolu"

    # [ascii] cartouche '===' (sans #) ... '==='
    if deco_only(first) and not first.lstrip().startswith("#"):
        close = None
        for i in range(1, min(len(work), 9)):
            if deco_only(work[i]) and not work[i].lstrip().startswith("#"):
                close = i
                break
        if close is not None:
            content = [work[i].strip() for i in range(1, close) if work[i].strip()]
            content = [c for c in content if has_text(c)]
            if content:
                head = "# " + content[0]
                rest = content[1:]
                new = [head] + rest + work[close + 1:]
                return new, "+".join(label_bits + ["ascii"])
        return None, "cartouche '===' non résolu"

    # [relocate] commentaire HTML ou blockquote en tête + H1 immédiat dessous
    if COMMENT.match(first) or QUOTE.match(first):
        lead = first
        rest = work[1:]
        while rest and rest[0].strip() == "":  # blancs entre tête et H1
            rest.pop(0)
        if rest and usable_h1(rest[0]):
            new = [rest[0], "", lead] + rest[1:]  # H1 en tête, puis tête relocalisée
            return new, "+".join(label_bits + ["relocate"])
        return None, "tête à relocaliser sans H1 immédiat"

    # [promote] ## / ### ... -> #
    mh = HN.match(first)
    if mh and has_text(mh.group(2)):
        new = ["# " + mh.group(2)] + work[1:]
        return new, "+".join(label_bits + ["promote"])

    # [prose] titre nu (pas de token markdown, court, sans ponctuation finale de phrase)
    if (not first.startswith(("#", ">", "-", "*", "`", "|", "<"))
            and has_text(first) and len(first) <= 80
            and not first.rstrip().endswith((".", ":", "!", "?"))):
        new = ["# " + first.strip()] + work[1:]
        return new, "+".join(label_bits + ["prose"])

    return None, f"non déterministe: {first[:50]!r}"


def main(argv):
    ap = argparse.ArgumentParser(description="Applieur conformité documentaire (idempotent, dry-run par défaut).")
    ap.add_argument("perimeter", nargs="?", default=DEFAULT_PERIMETER)
    ap.add_argument("--apply", action="store_true", help="écrit réellement (sinon dry-run)")
    ap.add_argument("--exceptions", help="sidecar REGLE:glob")
    ap.add_argument("--list-held", action="store_true", help="liste les cas non traités (à arbitrer)")
    args = ap.parse_args(argv)

    root = args.perimeter
    exc = load_exceptions(args.exceptions)
    fixed, held, skipped_frozen = [], [], 0

    for dp, dns, fs in os.walk(root):
        dns[:] = [d for d in dns if d != ".git"]
        for f in fs:
            if not f.endswith(".md"):
                continue
            abspath = os.path.join(dp, f)
            rel = rel_under(abspath, root)
            try:
                raw = open(abspath, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                held.append((rel, "illisible UTF-8"))
                continue
            lines = raw.split("\n")
            if usable_h1(lines[0].lstrip("\ufeff") if lines else ""):
                continue  # conforme
            if is_frozen(rel):
                skipped_frozen += 1
                continue
            if any(fnmatch.fnmatch(rel, g) for g in exc):
                continue

            # Overrides nommés (décisions explicites) — prioritaires.
            if rel in STUBS:
                new, label = STUBS[rel].rstrip("\n").split("\n"), "stub"
            elif rel in NAMED_TITLES:
                body = lines
                while body and body[0].strip() == "":
                    body.pop(0)
                new, label = [NAMED_TITLES[rel], ""] + body, "title-inject"
            else:
                new, label = transform(lines)

            if new is None:
                held.append((rel, label))
                continue
            fixed.append((rel, label))
            if args.apply:
                with open(abspath, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(new))

    mode = "APPLIQUÉ" if args.apply else "DRY-RUN (aucune écriture)"
    print(f"[{mode}] périmètre={root}  gelé-ignoré={skipped_frozen}")
    by = {}
    for _, lab in fixed:
        by[lab] = by.get(lab, 0) + 1
    print(f"Corrigés: {len(fixed)}  |  Tenus (à arbitrer): {len(held)}")
    for lab in sorted(by):
        print(f"   {lab}: {by[lab]}")
    if args.list_held and held:
        print("\n-- TENUS (non déterministes / titre à inventer) --")
        for rel, why in sorted(held):
            print(f"   {rel}  ::  {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
