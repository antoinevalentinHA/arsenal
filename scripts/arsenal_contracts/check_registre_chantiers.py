#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle structurel — Registre des chantiers Arsenal.

Invariants vérifiés (deux, volontairement étroits) :

    REG-1  Tout lien Markdown relatif du fichier
           `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md`
           pointe vers un fichier (ou dossier) existant.

    REG-2  Aucune ligne d'un tableau à colonne `ID` ne porte un identifiant
           **non attribué** : ni placeholder (`Cxx`, `Cnn`, `à attribuer`,
           `TBD`, `??`), ni cellule vide.

Le registre est un INDEX D'ÉTAT : ses deux promesses vérifiables mécaniquement
sont qu'aucune de ses cibles n'est morte (REG-1) et que chaque ligne est
**citable** (REG-2). Un chantier sans identifiant ne peut être ni cité, ni
ordonné, ni suivi ; le placeholder est une dette qui survit à la PR qui
l'introduit. Ces contrôles NE jugent PAS le statut métier (ouvert/clos) —
celui-ci relève du document source, qui fait foi.

REG-2 ne prescrit **aucune forme** d'identifiant : il n'exige pas `C<n>` et
n'attribue aucun numéro. La règle d'attribution (« prochain numéro
disponible ») reste humaine et hors CI ; le checker refuse seulement l'absence
d'attribution. Les tableaux dont la première colonne n'est pas `ID` (p. ex.
`Sujet`) sont hors périmètre de REG-2.

Portée :
    - REG-1 : liens relatifs uniquement (les ancres `#...` et les URLs
      absolues http/https sont ignorées) ;
    - REG-2 : première cellule des lignes de tableau, sous un en-tête dont la
      première colonne est exactement `ID` ; en-têtes et séparateurs exclus ;
    - lecture seule, déterministe, sans dépendance hors stdlib.

Sortie :
    - exit 0 : les deux invariants tiennent ;
    - exit 1 : au moins une violation (rapport ligne par ligne) ;
    - exit 2 : erreur d'exécution (registre introuvable) ou régression du
      checker lui-même (`--selftest`).

Usage :
  python scripts/arsenal_contracts/check_registre_chantiers.py
  python scripts/arsenal_contracts/check_registre_chantiers.py --selftest
"""

import argparse
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

# Ligne de séparation d'un tableau Markdown : `|---|:--:|...`
SEPARATEUR_RE = re.compile(r"^\|[\s:\-|]+\|$")

# Marqueurs d'identifiant non attribué. Volontairement énumérés : on refuse ce
# qui est reconnaissable comme un placeholder, on n'impose pas un format d'ID.
PLACEHOLDER_RE = re.compile(
    r"""(?ix)
      \battribuer\b          # « à attribuer », « Cxx à attribuer », « à faire attribuer »
    | \bà\s+définir\b
    | \bTBD\b
    | \bTODO\b
    | \bC[xn]{2,}\b          # Cxx, CXX, Cnn, CNN
    | \?\?                   # C??, ??
    """
)

# Décorations Markdown à retirer avant jugement d'une cellule.
DECOR_RE = re.compile(r"[*_`~]")


def cibles(md_text):
    """REG-1 — liste (cible_nettoyée, brut) des liens relatifs à vérifier."""
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


def _premiere_cellule(ligne):
    """Contenu brut de la 1re cellule d'une ligne de tableau, ou None."""
    ligne = ligne.strip()
    if not ligne.startswith("|"):
        return None
    return ligne[1:].split("|", 1)[0].strip() if "|" in ligne[1:] else None


def identifiants_non_attribues(md_text):
    """
    REG-2 — cœur de validation, pur (texte -> liste d'écarts).

    Renvoie une liste de (numéro_de_ligne, cellule_ID, motif) pour chaque ligne
    de tableau à colonne `ID` dont l'identifiant n'est pas attribué.
    """
    ecarts = []
    dans_table_id = False

    for num, ligne in enumerate(md_text.splitlines(), start=1):
        cellule = _premiere_cellule(ligne)

        if cellule is None:
            # Hors tableau : toute ligne non-`|` referme la table courante.
            dans_table_id = False
            continue

        if SEPARATEUR_RE.match(ligne.strip()):
            continue  # séparateur d'en-tête : ne juge rien, ne referme rien

        nu = DECOR_RE.sub("", cellule).strip()

        # En-tête : arme (ou désarme) le périmètre selon la 1re colonne.
        if nu.casefold() == "id":
            dans_table_id = True
            continue
        if not dans_table_id:
            continue

        if not nu:
            ecarts.append((num, cellule, "cellule ID vide"))
        elif PLACEHOLDER_RE.search(nu):
            ecarts.append((num, cellule, "identifiant non attribué (placeholder)"))

    return ecarts


# ---------------------------------------------------------------------------
# Auto-test du juge (on ne juge pas avec un juge défectueux). En mémoire.
# ---------------------------------------------------------------------------
def _selftest():
    failures = []

    def expect(cond, label):
        if not cond:
            failures.append(label)

    entete = "| ID | Chantier |\n|----|----------|\n"

    # Le défaut historique : ECS-DESINF-VAC / NOTIF-REDACTION sans numéro.
    ko = entete + "| **ECS-DESINF-VAC** *(Cxx à attribuer)* | Désinfection |\n"
    expect(len(identifiants_non_attribues(ko)) == 1, "REG-2 : placeholder non détecté")
    expect(identifiants_non_attribues(ko)[0][0] == 3, "REG-2 : mauvais numéro de ligne")

    # Un identifiant réel passe — quelle que soit sa forme.
    for bon in ("**C46**", "**C47**", "C3", "**D-C18-CD**", "**D-PRES**"):
        ok = entete + f"| {bon} | Objet |\n"
        expect(identifiants_non_attribues(ok) == [], f"REG-2 : faux positif sur {bon}")

    # Chaque marqueur de placeholder est bien refusé.
    for mauvais in ("*(Cxx à attribuer)*", "**Cnn**", "TBD", "à définir", "C??", "**CXX**"):
        ko2 = entete + f"| {mauvais} | Objet |\n"
        expect(len(identifiants_non_attribues(ko2)) == 1, f"REG-2 : {mauvais} accepté")

    # Cellule ID vide.
    expect(len(identifiants_non_attribues(entete + "|  | Objet |\n")) == 1,
           "REG-2 : cellule vide acceptée")

    # Hors périmètre : tableau sans colonne ID, en-tête, séparateur.
    autre = "| Sujet | Clôturé le |\n|-------|-----------|\n| Code à attribuer | 2026-01-01 |\n"
    expect(identifiants_non_attribues(autre) == [], "REG-2 : tableau sans colonne ID jugé")

    # Le périmètre se referme hors du tableau : la prose n'est pas jugée.
    prose = entete + "| **C46** | Objet |\n\nCode `Cxx` à attribuer par le propriétaire.\n"
    expect(identifiants_non_attribues(prose) == [], "REG-2 : prose hors tableau jugée")

    # Une seconde table sans colonne ID désarme bien la première.
    enchaine = entete + "| **C46** | Objet |\n\n" + autre
    expect(identifiants_non_attribues(enchaine) == [], "REG-2 : périmètre non désarmé")

    # REG-1 reste intact : ancres et URLs absolues ignorées.
    liens = "[a](fichier.md#x) [b](#ancre) [c](https://example.org/z)"
    expect([c for c, _ in cibles(liens)] == ["fichier.md"], "REG-1 : filtrage des liens")

    if failures:
        print("SELFTEST KO :")
        for f in failures:
            print(f"  - {f}")
        return 2
    print("SELFTEST OK — REG-1 et REG-2 exercés.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Contrôle du registre des chantiers.")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if args.selftest:
        return _selftest()

    if not os.path.isfile(REGISTRE):
        print(f"::error::Registre introuvable : {REGISTRE}", file=sys.stderr)
        return 2

    base = os.path.dirname(REGISTRE)
    with open(REGISTRE, "r", encoding="utf-8") as fh:
        texte = fh.read()

    echec = False

    # --- REG-1 : aucune cible morte -----------------------------------------
    manquants = []
    total = 0
    for cible, brut in cibles(texte):
        total += 1
        resolu = os.path.normpath(os.path.join(base, cible))
        if not os.path.exists(resolu):
            rel = os.path.relpath(resolu, REPO_ROOT)
            manquants.append((brut, rel))

    if manquants:
        echec = True
        print(f"REG-1 — {len(manquants)}/{total} cible(s) manquante(s) :")
        for brut, rel in manquants:
            print(f"  MANQUANT  {brut}  ->  {rel}")
        print("::error::REG-1 — le registre des chantiers contient au moins un lien cassé.")
    else:
        print(f"REG-1 — OK : {total} cible(s), 0 manquante.")

    # --- REG-2 : aucun identifiant non attribué ------------------------------
    ecarts = identifiants_non_attribues(texte)
    if ecarts:
        echec = True
        print(f"REG-2 — {len(ecarts)} identifiant(s) non attribué(s) :")
        for num, cellule, motif in ecarts:
            print(f"  L{num}  {cellule!r}  ->  {motif}")
        print(
            "::error::REG-2 — le registre porte un identifiant non attribué. "
            "Règle : prochain numéro disponible (max des codes existants + 1, "
            "sans recyclage de trou)."
        )
    else:
        print("REG-2 — OK : tout identifiant de la colonne ID est attribué.")

    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
