#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle structurel — Registre des chantiers Arsenal.

Invariants vérifiés (trois, volontairement étroits) :

    REG-1  Tout lien Markdown relatif du fichier
           `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md`
           pointe vers un fichier (ou dossier) existant.

    REG-2  Aucune ligne d'un tableau à colonne `ID` ne porte un identifiant
           **non attribué** : ni placeholder (`Cxx`, `Cnn`, `à attribuer`,
           `TBD`, `??`), ni cellule vide.

    REG-3  Aucune ligne de la table de la section **① Actifs** n'affiche,
           dans sa colonne `Statut`, une clôture **effective** (« CLOS »,
           « CLÔTURÉ »/« CLOTURÉ » en tête de cellule). Un chantier qui
           s'annonce lui-même clos n'a plus sa place parmi ceux qui attendent
           une action : le § Cycle de vie du registre prescrit sa migration
           vers ⑤ Clos récents, dans le même commit que la clôture (règle de
           gouvernance « co-commit obligatoire »). Une clôture conditionnelle
           ou partielle (« clôture conditionnelle acquise », par exemple)
           n'est **pas** une clôture effective : REG-3 ne cible que l'annonce
           d'une fin de chantier, jamais une réserve en cours.

Le registre est un INDEX D'ÉTAT : ses promesses vérifiables mécaniquement
sont qu'aucune de ses cibles n'est morte (REG-1), que chaque ligne est
**citable** (REG-2), et que la section « chantiers en attente d'une action »
ne contient aucune ligne qui se déclare elle-même terminée (REG-3). Un
chantier sans identifiant ne peut être ni cité, ni ordonné, ni suivi ; le
placeholder est une dette qui survit à la PR qui l'introduit. Ces contrôles
NE jugent PAS le bien-fondé métier d'un statut (est-ce que le chantier EST
réellement terminé) — cela relève du document source, qui fait foi. REG-3
vérifie une règle mécanique de **placement**, pas la justesse de la clôture
elle-même.

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
    - REG-3 : colonne `Statut` des lignes de tableau de la section de 2e
      niveau (`## `) dont le titre contient « ① Actifs » ; section absente ou
      table sans colonne `Statut` : aucun écart signalé (REG-3 ne prescrit pas
      la forme du registre, seulement son contenu quand la forme attendue est
      là) ;
    - lecture seule, déterministe, sans dépendance hors stdlib.

Sortie :
    - exit 0 : les trois invariants tiennent ;
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

# REG-3 — Pipe de séparation de colonne, en respectant l'échappement `\|`
# (une cellule peut légitimement contenir un pipe littéral, ex. un motif
# regex en ligne : `is_state('a\|b')`). Contrairement à `_premiere_cellule`
# (qui ne lit jamais que la 1re cellule), REG-3 doit retrouver une colonne
# nommée à une position arbitraire : il lui faut la ligne entière.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")

# REG-3 — bruit de tête (emoji, ponctuation, espaces) à ignorer avant de
# juger si une cellule Statut *commence* par une annonce de clôture.
LEADING_NOISE_RE = re.compile(r"^[^\wÀ-ÖØ-öø-ÿ]+")

# REG-3 — annonce d'une clôture EFFECTIVE en tête de cellule Statut : le mot
# « clos », ou le participe « clôturé »/« cloturé » (accent aigu final
# obligatoire — ce qui exclut le nom commun « clôture », qui se termine par
# un e nu et n'annonce rien de terminé, ex. « clôture conditionnelle
# acquise »).
STATUT_CLOS_RE = re.compile(r"(?i)^(clos|cl[oô]turé)\b")


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


def _cellules(ligne):
    """
    REG-3 — cellules d'une ligne de tableau, pipes échappés (`\\|`) préservés.

    Contrairement à `_premiere_cellule` (qui ignore tout ce qui suit le 1er
    `|` non échappé), REG-3 doit retrouver une colonne nommée à une position
    arbitraire de la ligne : il lui faut le découpage complet.
    """
    parts = CELL_SPLIT_RE.split(ligne.strip())
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def chantiers_clos_en_actifs(md_text):
    """
    REG-3 — cœur de validation, pur (texte -> liste d'écarts).

    Renvoie une liste de (numéro_de_ligne, id_chantier, statut_brut) pour
    chaque ligne de la table de la section « ① Actifs » dont la colonne
    `Statut` annonce une clôture effective.

    Portée strictement bornée à cette section : un statut de clôture ailleurs
    (② Parqués, ⑤ Clos récents...) n'est pas un écart — c'est sa place
    normale. Absence de section « ① Actifs », ou table sans colonne `Statut`
    dans cette section : aucun écart (REG-3 ne prescrit pas la forme, il
    juge le contenu quand la forme attendue est là — cf. portée du module).
    """
    lignes = md_text.splitlines()

    debut = fin = None
    for i, ligne in enumerate(lignes):
        if debut is None:
            if ligne.startswith("## ") and "① Actifs" in ligne:
                debut = i + 1
        elif ligne.startswith("## "):
            fin = i
            break
    if debut is None:
        return []
    if fin is None:
        fin = len(lignes)

    ecarts = []
    entete = None  # None = hors table ; dict = {nom_colonne_casefold: index}

    for num in range(debut, fin):
        ligne = lignes[num]
        premiere = _premiere_cellule(ligne)

        if premiere is None:
            entete = None  # hors tableau : referme la table courante
            continue

        if SEPARATEUR_RE.match(ligne.strip()):
            continue  # séparateur d'en-tête : ne juge rien, ne referme rien

        colonnes = _cellules(ligne)
        noms = [DECOR_RE.sub("", c).strip().casefold() for c in colonnes]

        if noms and noms[0] == "id":
            entete = {nom: idx for idx, nom in enumerate(noms)}
            continue
        if entete is None or "statut" not in entete:
            continue

        idx_statut = entete["statut"]
        if idx_statut >= len(colonnes):
            continue

        statut_brut = colonnes[idx_statut]
        statut_nu = LEADING_NOISE_RE.sub("", DECOR_RE.sub("", statut_brut))
        if not STATUT_CLOS_RE.match(statut_nu):
            continue

        idx_id = entete.get("id", 0)
        id_brut = DECOR_RE.sub("", colonnes[idx_id]).strip() if idx_id < len(colonnes) else premiere
        ecarts.append((num + 1, id_brut, statut_brut.strip()))

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

    # --- REG-3 -----------------------------------------------------------
    entete_actifs = (
        "| ID | Chantier | Domaine | Prio | Statut | Action attendue | Source |\n"
        "|----|----------|---------|------|--------|------------------|--------|\n"
    )
    registre_type = (
        "## ① Actifs — test\n\n"
        + entete_actifs
        + "| **C1** | Objet 1 | dom | P1 | **Ouvert (2026-01-01)** — en cours. | faire X | src |\n"
        + "| **C2** | Objet 2 | dom | P1 | **CLOS (2026-01-02)** — terrain validé. | — (clos) | src |\n"
        + "| **C3** | Objet 3 | dom | P1 | **CLÔTURÉ** — clôturé pour de bon. | — | src |\n"
        + "| **C4** | Objet 4 | dom | P1 | **CLOTURÉ** — sans circonflexe aussi détecté. | — | src |\n"
        + "| **C5** | Objet 5 | dom | P1 | clôture conditionnelle acquise | réserve | src |\n"
        + "| **C6** | Objet 6 | dom | P1 | ✅ **CLÔTURE CONDITIONNELLE ACQUISE** — réserve E1. | réserve | src |\n"
        "\n"
        "## ② Parqués — test\n\n"
        + entete_actifs
        + "| **C7** | Objet 7 | dom | P2 | **CLOS (2026-01-03)** — hors périmètre REG-3. | — | src |\n"
    )
    ecarts3 = chantiers_clos_en_actifs(registre_type)
    ids_detectes = {id_ for _, id_, _ in ecarts3}
    expect(ids_detectes == {"C2", "C3", "C4"}, f"REG-3 : mauvais ensemble détecté {ids_detectes}")
    expect(len(ecarts3) == 3, "REG-3 : nombre d'écarts inattendu")
    expect("C1" not in ids_detectes, "REG-3 : faux positif sur statut Ouvert")
    expect("C5" not in ids_detectes, "REG-3 : faux positif sur clôture conditionnelle (nom, sans gras)")
    expect("C6" not in ids_detectes, "REG-3 : faux positif sur clôture conditionnelle (gras + emoji)")
    expect("C7" not in ids_detectes, "REG-3 : section ② jugée à tort (hors périmètre)")

    # Une section ① absente, ou sans colonne Statut, ne casse rien et ne juge rien.
    expect(chantiers_clos_en_actifs("# Rien ici\n") == [], "REG-3 : absence de section ① doit être neutre")
    sans_statut = (
        "## ① Actifs — test\n\n"
        "| ID | Chantier |\n|----|----------|\n| **C9** | **CLOS** |\n"
    )
    expect(chantiers_clos_en_actifs(sans_statut) == [], "REG-3 : table sans colonne Statut jugée à tort")

    if failures:
        print("SELFTEST KO :")
        for f in failures:
            print(f"  - {f}")
        return 2
    print("SELFTEST OK — REG-1, REG-2 et REG-3 exercés.")
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

    # --- REG-3 : aucun chantier clos resté en section ① Actifs --------------
    clos_mal_places = chantiers_clos_en_actifs(texte)
    if clos_mal_places:
        echec = True
        print(f"REG-3 — {len(clos_mal_places)} chantier(s) clos resté(s) en section ① Actifs :")
        for num, id_chantier, statut in clos_mal_places:
            apercu = statut if len(statut) <= 80 else statut[:77] + "..."
            print(f"  L{num}  {id_chantier}  ->  {apercu!r}")
        print(
            "::error::REG-3 — un chantier au statut de clôture effective figure "
            "encore en section ① Actifs ; migrer la ligne vers ⑤ Clos récents "
            "dans le même commit (§ Cycle de vie, § Règles de gouvernance)."
        )
    else:
        print("REG-3 — OK : aucun chantier clos resté en section ① Actifs.")

    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
