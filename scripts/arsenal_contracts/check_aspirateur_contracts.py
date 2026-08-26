#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : domaine Aspirateur.

Contrat (source normative) : 00_documentation_arsenal/contrats/aspirateur/
Audit factuel du domaine    : 00_documentation_arsenal/audits/01_rapports/
                              aspirateur/audit_faisabilite_roborock_q7_max.md

PÉRIMÈTRE — ce que ce checker vérifie, et ce qu'il ne vérifie pas.

Le domaine Aspirateur est **antérieur au runtime** : il n'existe ni helper, ni
script, ni automation, ni dashboard à confronter. Les obligations de conduite du
contrat (écrivain unique, forme enveloppée de la charge utile, interdiction
d'écrire le mode de nettoyage, séquence de lancement) ne sont donc **pas**
vérifiables aujourd'hui : elles le deviendront avec le premier lot runtime, et
ce checker ne prétend pas les couvrir.

Ce qui EST vérifiable maintenant est l'**intégrité du système normatif
lui-même** : un contrat dont le référentiel, le catalogue de refus ou la
partition d'états se troue cesse d'être opposable, et le trou est silencieux.

TROIS ANCRES INDÉPENDANTES DU CONTRAT. Un contrôle qui ne lit que le contrat ne
prouve que sa cohérence interne : falsifier la table ET ses consommateurs le
laisse passer. Trois ancres extérieures ferment cette porte :

  1. l'AUDIT du domaine        — segments, noms, cartes, entités et primitives ;
  2. les CONSTANTES de module  — partition d'états et énumérations natives,
                                 figées ici et non relues du contrat ;
  3. l'arbre LOVELACE réel     — surface de commande.

Sept contrôles, tous adossés à une clause déjà normée par le contrat :

  ASP-CI-1  Invariants  — `ASP-INV-n` numérotés 1..N sans trou ni doublon,
                          format de déclaration uniforme ; `ASP-IMC-1` défini
                          une fois et une seule.
  ASP-CI-2  Référentiel — chaque couple (segment, nom Roborock) de la table
                          canonique est ATTESTÉ PAR L'AUDIT, index de carte
                          compris ; les segments observés non commandables
                          restent hors table ; le Garage n'est pas promu ; les
                          périmètres et raccourcis restent mono-carte et dans
                          la table (ASP-INV-6/28/55, ASP-IMC-1).
  ASP-CI-3  Codes       — tout code cité figure au catalogue ; tout motif de
                          REFUS y figurant est produit par au moins une clause
                          RÉELLE — catalogues, index, sections de renvois et
                          blocs de code exclus des zones productrices
                          (ASP-INV-50/52).
  ASP-CI-4  États       — la classification est FIGÉE ICI : un état déplacé,
                          ajouté ou retiré échoue, et le lien classe N → refus
                          par défaut → `ETAT_NON_QUALIFIE` est vérifié
                          explicitement (ASP-INV-60).
  ASP-CI-5  Profils     — cinq profils exactement, `gentle` exclu, valeurs
                          natives bornées aux énumérations attestées
                          (ASP-INV-10/11).
  ASP-CI-6  Identifiants— tout jeton `<domaine>.<objet>` d'un domaine Home
                          Assistant doit être EXACTEMENT attesté par l'audit —
                          comparaison par jeton entier, un préfixe tronqué ne
                          passe pas — ou reconnu comme primitive de service
                          documentée ; les domaines de helpers Arsenal sont
                          interdits en bloc (ASP-INV-58).
  ASP-CI-7  Lovelace    — ni entité native d'ACTION du robot, ni NOM DE SERVICE
                          STATIQUE `vacuum.*` / `roborock.*` sous les clés
                          `service:` / `action:` / `perform_action:`, quel que
                          soit le mode de ciblage — `entity_id`, `device_id`,
                          `area_id`, `label_id` (ASP-INV-31, chapitre 11).

Les blocs de code clôturés sont neutralisés avant TOUS les contrôles, et aussi
sur l'audit : un exemple documentaire n'est normatif nulle part, et un faux
tableau placé dans un bloc n'atteste rien.

CE QU'ASP-CI-7 NE PEUT PAS GARANTIR — dit ici plutôt que passé sous silence.
Ces trois angles morts sont réels ; aucun n'est neutralisé par une exemption,
et aucun n'est réductible par une analyse statique du seul dépôt :

  1. **Un appel générique ciblé par `device_id`.** `select.select_option` visant
     un `device_id` peut basculer la carte active sans nommer le robot. Rattacher
     un `device_id` — un UUID opaque — à un appareil exige le registre de
     périphériques, qui ne vit pas dans le dépôt. Interdire globalement
     `select.select_option` serait faux : le motif a des emplois légitimes dans
     d'autres domaines.
  2. **Un nom de service entièrement construit par template.** Sans littéral
     analysable, il n'y a rien à confronter.
  3. **Un second aspirateur relevant d'une autre autorité.** La portée de
     `vacuum.*` est aujourd'hui GLOBALE sur les arbres Lovelace. C'est accepté
     parce qu'Arsenal ne possède qu'un seul aspirateur : la portée coïncide donc
     en pratique avec l'autorité du domaine. **Elle devra être réexaminée avant
     l'ajout d'un second équipement relevant d'une autre autorité**, faute de
     quoi ce checker refuserait une commande qu'il n'a pas à gouverner.

ASP-CI-7 est donc une garde d'anti-régression **sur les commandes statiquement
nommées** : elle balaie une surface réelle, n'y trouve aujourd'hui aucune
violation, et se déclenche sur toute entité d'action ou tout nom de service
littéral. Elle ne prétend pas détecter « toute commande brute ».

Lecture seule : n'écrit, ne crée, ne supprime aucun fichier.
Codes de sortie : 0 conforme, 1 violation(s), 2 erreur d'usage/infra.

Usage :
  python check_aspirateur_contracts.py
  python check_aspirateur_contracts.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN = ROOT / "00_documentation_arsenal" / "contrats" / "aspirateur"
AUDIT = (ROOT / "00_documentation_arsenal" / "audits" / "01_rapports" /
         "aspirateur" / "audit_faisabilite_roborock_q7_max.md")
LOVELACE_DIRS = ("18_lovelace", "19_button_card_templates")
FICHIER_CATALOGUE = "09_refus_et_diagnostics.md"
FICHIER_INDEX = "README.md"

# ── Ancre 2 : constantes de module, jamais relues du contrat ────────────────

# Énumérations natives attestées par l'audit §3.1. Ne pas élargir sans preuve.
FAN_SPEEDS_AUTORISEES = {"quiet", "balanced", "turbo", "max"}
WATER_LEVELS_ATTESTES = {"off", "low", "medium", "high", "custom_water_flow"}
FAN_SPEED_EXCLUE = "gentle"

# Classification contractuelle ATTENDUE des états (contrat 07 §5.0). Figée ici :
# c'est ce qui rend un DÉPLACEMENT d'état entre classes détectable, là où une
# simple vérification de disjonction le laisserait passer. `returning_home` et
# `docking` relèvent du mouvement — fait établi par le contrat alarme
# (ALM-ROBO-1) : côté entité `vacuum`, tous deux sont mappés sur `returning`.
PARTITION_ATTENDUE = {
    "R": frozenset({"charger_disconnected", "charging"}),
    "A": frozenset({"cleaning", "segment_cleaning", "zoned_cleaning",
                    "paused", "returning_home", "docking"}),
    "E": frozenset({"error", "device_offline", "unknown", "unavailable"}),
}
CLASSE_NON_QUALIFIEE = "N"
CODE_ETAT_NON_QUALIFIE = "ETAT_NON_QUALIFIE"

# Segments observés dans une carte mais SANS rôle métier V1 (contrat 02 §2,
# QO-1). Attestés par l'audit, ils doivent rester hors de la table canonique.
SEGMENTS_NON_COMMANDABLES = {"2_17", "2_18"}
# Cartes portant un référentiel commandable. Le Garage n'y figure pas et ne
# doit pas y être promu (contrat 01 §5, ASP-INV-2).
CARTES_COMMANDABLES = {"0", "1", "2"}
CARTE_NON_PROMUE = "Garage"

# ── Ciblage LEXICAL des identifiants du domaine (I1) ───────────────────────
# La protection ne repose sur AUCUNE liste de domaines Home Assistant : une
# telle liste se prétendrait exhaustive et laisserait passer `plant.aspirateur_x`
# ou `sun.aspirateur_x` le jour où le domaine manque. Un jeton est examiné dès
# qu'il désigne LEXICALEMENT ce domaine — objet mentionnant l'aspirateur ou le
# robot — ou qu'il relève des deux domaines propres à l'appareil.
MARQUEURS_DOMAINE = ("roborock", "aspirateur")
ROBOT_DOMAINS = frozenset({"vacuum", "roborock"})
# Domaines de helpers/objets Arsenal. Cette liste n'influe QUE sur le libellé du
# diagnostic : un domaine absent d'ici reste refusé par la règle d'attestation.
# La détection ne dépend donc d'aucune énumération.
ARSENAL_HELPER_DOMAINS = frozenset({
    "automation", "counter", "group", "input_boolean", "input_button",
    "input_datetime", "input_number", "input_select", "input_text", "scene",
    "schedule", "script", "timer", "todo",
})
# Primitives de SERVICE documentées. Ce ne sont pas des `entity_id` : elles
# restent néanmoins soumises à l'attestation par l'audit.
SERVICE_PRIMITIVES = frozenset({
    "vacuum.send_command", "vacuum.start", "vacuum.pause", "vacuum.stop",
    "vacuum.return_to_base", "vacuum.set_fan_speed", "vacuum.clean_area",
    "vacuum.locate", "vacuum.clean_spot", "select.select_option",
})
# Domaines dont un appel de service commanderait le robot en contournant
# l'écrivain unique (ASP-CI-7).
SERVICE_DOMAINS_INTERDITS = ("vacuum", "roborock")
# Domaines d'entités natives capables d'ACTION sur le robot.
ACTION_DOMAINS = ("vacuum", "select", "button")


# ─────────────────────────────────────────────────────────────
# Neutralisation des blocs de code clôturés
# ─────────────────────────────────────────────────────────────

def strip_fences(texte: str) -> str:
    """Neutralise les blocs de code clôturés, lignes de clôture comprises.

    Reproduit strictement la sémantique de `strip_fenced_code`
    (scripts/docs_navigation/audit_doc_links.py), déjà employée par DOC-CI-1 et
    DOC-CI-2 pour ce motif exact : une ligne dont le contenu strippé commence
    par ``` bascule l'état et est elle-même marquée « dans la clôture ».
    Reproduite plutôt qu'importée : un checker de contrat ne dépend d'aucun
    autre outil du dépôt. Le nombre de lignes est conservé.
    """
    sortie: list[str] = []
    dans_cloture = False
    for ligne in texte.splitlines():
        if ligne.strip().startswith("```"):
            sortie.append("")
            dans_cloture = not dans_cloture
            continue
        sortie.append("" if dans_cloture else ligne)
    return "\n".join(sortie)


def sans_clotures(textes: dict[str, str]) -> dict[str, str]:
    return {nom: strip_fences(txt) for nom, txt in textes.items()}


# ─────────────────────────────────────────────────────────────
# ASP-CI-1 — intégrité des invariants
# ─────────────────────────────────────────────────────────────

DECL_INV = re.compile(r'^> \*\*`ASP-INV-(\d+)`', re.M)
DECL_INV_LAXE = re.compile(r'^> \*\*(?:Invariant\s+)?`?ASP-INV-(\d+)`?', re.M)
DECL_IMC = re.compile(r'^> ### `ASP-IMC-1`', re.M)


def check_invariants(textes: dict[str, str]) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    stricts: list[int] = []
    laxes: list[int] = []
    for _, txt in sorted(textes.items()):
        stricts += [int(m.group(1)) for m in DECL_INV.finditer(txt)]
        laxes += [int(m.group(1)) for m in DECL_INV_LAXE.finditer(txt)]
    if not stricts:
        errs.append("ASP-CI-1 : aucun invariant `ASP-INV-n` déclaré dans le domaine.")
        return errs
    divergents = sorted(set(laxes) - set(stricts))
    if divergents:
        errs.append(
            "ASP-CI-1 : format de déclaration non uniforme pour "
            f"ASP-INV-{', '.join(str(n) for n in divergents)} — attendu "
            "`> **`ASP-INV-n`**`.")
    doublons = sorted({n for n in stricts if stricts.count(n) > 1})
    if doublons:
        errs.append("ASP-CI-1 : invariant(s) déclaré(s) plusieurs fois : "
                    + ", ".join(f"ASP-INV-{n}" for n in doublons) + ".")
    trous = [n for n in range(1, max(stricts) + 1) if n not in set(stricts)]
    if trous:
        errs.append("ASP-CI-1 : numérotation trouée — manque "
                    + ", ".join(f"ASP-INV-{n}" for n in trous) + ".")
    imc = sum(len(DECL_IMC.findall(t)) for t in textes.values())
    if imc != 1:
        errs.append(f"ASP-CI-1 : `ASP-IMC-1` doit être défini exactement une fois "
                    f"(trouvé {imc}).")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-2 — référentiel, ancré sur l'audit
# ─────────────────────────────────────────────────────────────

SEGMENT_CANON = re.compile(
    r'^\| `(\d+_\d+)` \| \*\*([^*\n]+)\*\*'
    r'(?:[^\S\n]*\|[^\S\n]*(?:`([^`\n]*)`|([^|`\n]*?))[^\S\n]*\|)?',
    re.M)
PERIMETRE = re.compile(
    r'^\| \*\*([^*|\n]+)\*\* \| `(\d)` \| ([^|\n]+) \|$', re.M)
SEGMENT_REF = re.compile(r'`(\d+_\d+)`')
# Table §5.1 de l'audit : | `0_16` | `Salon` | RDC |
AUDIT_SEGMENT = re.compile(
    r'^\| `(\d+_\d+)` \| `([^`\n]+)` \| ([^|\n]+?)[^\S\n]*\|', re.M)
# Table §4 de l'audit : | **0** | `RDC` | 4 |
AUDIT_CARTE = re.compile(r'^\| \*\*(\d)\*\* \| `([^`\n]+)`', re.M)


def parse_segments(t02: str) -> dict[str, tuple[str, str]]:
    """Renvoie {segment: (libellé canonique Arsenal, nom Roborock si divergent)}."""
    out: dict[str, tuple[str, str]] = {}
    for seg, libelle, roboro_bt, roboro_nu in SEGMENT_CANON.findall(t02):
        divergent = (roboro_bt or roboro_nu or "").strip().strip("`").strip()
        if divergent in {"—", "-", ""}:
            divergent = ""
        out[seg] = (libelle.strip(), divergent)
    return out


def parse_audit_segments(audit: str) -> dict[str, tuple[str, str]]:
    """Renvoie {segment: (nom Roborock, nom de carte)} depuis l'audit §5.1."""
    return {seg: (nom.strip(), carte.strip())
            for seg, nom, carte in AUDIT_SEGMENT.findall(audit)}


def check_referentiel(t02: str, t10: str, audit: str) -> list[str]:
    errs: list[str] = []
    canon = parse_segments(t02)
    if not canon:
        errs.append("ASP-CI-2 : table canonique des segments introuvable "
                    "(02 §2) — le référentiel du domaine est vide.")
        return errs

    # ---- Ancre 1 : attestation par l'audit --------------------------------
    atteste = parse_audit_segments(audit)
    cartes_audit = dict(AUDIT_CARTE.findall(audit))
    if not atteste:
        errs.append("ASP-CI-2 : table des segments introuvable dans l'audit du "
                    "domaine — le référentiel ne peut pas être attesté.")
    else:
        for seg in sorted(canon):
            libelle, divergent = canon[seg]
            attendu = divergent or libelle
            if seg not in atteste:
                errs.append(f"ASP-CI-2 : segment `{seg}` de la table canonique "
                            "ABSENT de l'audit du domaine — un segment non relevé "
                            "ne peut pas être commandable.")
                continue
            nom_audit, carte_audit = atteste[seg]
            if attendu != nom_audit:
                errs.append(f"ASP-CI-2 : segment `{seg}` — le contrat attend le "
                            f"nom Roborock « {attendu} », l'audit atteste "
                            f"« {nom_audit} ». Incohérence du contrat.")
            index = seg.split("_", 1)[0]
            if index not in CARTES_COMMANDABLES:
                errs.append(f"ASP-CI-2 : segment `{seg}` — index de carte "
                            f"`{index}` hors des cartes commandables "
                            f"{sorted(CARTES_COMMANDABLES)}.")
            elif index in cartes_audit and carte_audit not in cartes_audit[index]:
                errs.append(f"ASP-CI-2 : segment `{seg}` — l'index `{index}` "
                            f"désigne « {cartes_audit[index].strip()} » dans "
                            f"l'audit, mais le segment y appartient à "
                            f"« {carte_audit} ».")
            if carte_audit == CARTE_NON_PROMUE:
                errs.append(f"ASP-CI-2 : segment `{seg}` appartient au "
                            f"{CARTE_NON_PROMUE}, que le contrat ne promeut pas "
                            "(ASP-INV-2).")
        # Segments observés mais non commandables : attestés, et hors table.
        for seg in sorted(SEGMENTS_NON_COMMANDABLES):
            if seg not in atteste:
                errs.append(f"ASP-CI-2 : segment observé `{seg}` absent de "
                            "l'audit — la liste des non-commandables ne "
                            "correspond plus au relevé.")
            if seg in canon:
                errs.append(f"ASP-CI-2 : segment `{seg}` est observé mais NON "
                            "COMMANDABLE : il ne doit pas figurer à la table "
                            "canonique (QO-1).")

    # ---- Cohérence interne : périmètres et raccourcis ---------------------
    sources = (("02 §3 (périmètres prédéfinis)", t02), ("10 §3 (raccourcis)", t10))
    vus: set[str] = set()
    for label, txt in sources:
        lignes = PERIMETRE.findall(txt)
        if not lignes:
            errs.append(f"ASP-CI-2 : aucun périmètre lisible dans {label}.")
            continue
        for nom, carte, composition in lignes:
            segs = SEGMENT_REF.findall(composition)
            nom = nom.strip()
            if not segs:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) ne "
                            "désigne aucun segment.")
                continue
            vus.update(segs)
            inconnus = [s for s in segs if s not in canon]
            if inconnus:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) désigne "
                            f"un segment hors référentiel : {', '.join(inconnus)}.")
            cartes = {s.split("_", 1)[0] for s in segs}
            if len(cartes) > 1:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) agrège "
                            f"plusieurs cartes ({', '.join(sorted(cartes))}) — "
                            "violation de ASP-IMC-1.")
            elif cartes and carte not in cartes:
                errs.append(f"ASP-CI-2 : périmètre « {nom} » ({label}) déclare la "
                            f"carte `{carte}` mais désigne des segments de la "
                            f"carte `{cartes.pop()}`.")
    orphelins = sorted(set(canon) - vus)
    if orphelins:
        errs.append("ASP-CI-2 : segment(s) du référentiel jamais employés par un "
                    f"périmètre : {', '.join(orphelins)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-3 — clôture du catalogue des codes
# ─────────────────────────────────────────────────────────────

CODE_LIGNE = re.compile(r'^\| `([A-Z][A-Z_]{4,})`', re.M)
CODE_CITE = re.compile(r'`([A-Z][A-Z_]{4,})`')
LIGNE_CATALOGUE = re.compile(r'^\| `[A-Z][A-Z_]{4,}`.*$', re.M)
SECTION_RENVOIS = re.compile(r'^#{2,3} Renvois\s*$.*?(?=^#{1,3} |\Z)', re.M | re.S)


def split_catalogue(t09: str) -> tuple[set[str], set[str]]:
    try:
        apres = t09.split("## 2. Catalogue des refus", 1)[1]
        sec2, reste = apres.split("## 3. Catalogue des échecs", 1)
    except (IndexError, ValueError):
        return set(), set()
    sec3 = reste.split("\n## ", 1)[0]
    return set(CODE_LIGNE.findall(sec2)), set(CODE_LIGNE.findall(sec3))


def zone_productrice(nom: str, txt: str) -> str:
    """Texte où une citation vaut PRODUCTION d'un refus.

    Sont exclus : le catalogue lui-même (un motif ne se justifie pas seul), les
    sections de renvois (un pointeur n'est pas une règle) et l'index du domaine
    (il oriente, il ne norme pas). Les blocs de code sont déjà neutralisés en
    amont.
    """
    if nom == FICHIER_INDEX:
        return ""
    txt = SECTION_RENVOIS.sub("", txt)
    if nom == FICHIER_CATALOGUE:
        txt = LIGNE_CATALOGUE.sub("", txt)
    return txt


def check_codes(textes: dict[str, str]) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    refus, echecs = split_catalogue(textes.get(FICHIER_CATALOGUE, ""))
    if not refus or not echecs:
        errs.append("ASP-CI-3 : catalogue des refus ou des échecs illisible "
                    "(09 §2 / §3).")
        return errs
    connus = refus | echecs
    cites: set[str] = set()
    produits: set[str] = set()
    for nom, txt in textes.items():
        cites |= set(CODE_CITE.findall(txt))
        produits |= set(CODE_CITE.findall(zone_productrice(nom, txt)))
    orphelins = sorted(cites - connus)
    if orphelins:
        errs.append("ASP-CI-3 : code(s) cité(s) hors catalogue — un motif "
                    f"inexistant rend le refus inapplicable : {', '.join(orphelins)}.")
    # Règle bornée aux REFUS. Un refus est produit par une clause : s'il n'est
    # cité par aucune zone productrice, aucune règle ne le déclenche et il est
    # mort. Un ÉCHEC décrit une issue constatée après émission et se suffit de
    # sa définition — l'exiger ailleurs forcerait une redite sans valeur.
    morts = sorted(refus - produits)
    if morts:
        errs.append("ASP-CI-3 : motif(s) de refus au catalogue mais qu'aucune "
                    "clause ne produit — un renvoi, un index ou le catalogue "
                    f"lui-même ne comptent pas : {', '.join(morts)}.")
    chevauche = sorted(refus & echecs)
    if chevauche:
        errs.append("ASP-CI-3 : code(s) déclarés à la fois comme refus et comme "
                    f"échec : {', '.join(chevauche)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-4 — partition des états, ancrée sur les constantes
# ─────────────────────────────────────────────────────────────

# R1 — `[^|\n]` et non `[^|]` : une classe négative sans `\n` franchirait la
# ligne et laisserait une table malformée capturer de la prose ultérieure.
CLASSE = re.compile(
    r'^\| \*\*([RAEN]) — [^|\n]*\|([^|\n]*)\|([^|\n]*)\|', re.M)
ENUM_08 = re.compile(r'énumération \*\*non exhaustive\*\* : (.+?)…')
ETAT = re.compile(r'`([a-z][a-z_]+)`')


def bloc_partition(t07: str) -> str:
    try:
        return t07.split("### 5.0", 1)[1].split("### 5.1", 1)[0]
    except IndexError:
        return ""


def parse_partition(t07: str) -> dict[str, tuple[set[str], str]]:
    """Renvoie {classe: (états énumérés, cellule d'effet)}."""
    bloc = bloc_partition(t07)
    return {cls: (set(ETAT.findall(valeurs)), effet)
            for cls, valeurs, effet in CLASSE.findall(bloc)}


def check_partition(t07: str, t08: str) -> list[str]:
    errs: list[str] = []
    part = parse_partition(t07)
    attendues = set(PARTITION_ATTENDUE) | {CLASSE_NON_QUALIFIEE}
    if set(part) != attendues:
        errs.append("ASP-CI-4 : partition des états incomplète (07 §5.0) — "
                    f"classes trouvées : {sorted(part) or 'aucune'} ; "
                    f"attendu {sorted(attendues)}.")
        return errs

    # ---- Ancre 2 : classification figée dans ce module --------------------
    for cls, attendu in PARTITION_ATTENDUE.items():
        reel = part[cls][0]
        manquants = sorted(attendu - reel)
        surnumeraires = sorted(reel - attendu)
        if manquants:
            errs.append(f"ASP-CI-4 : classe {cls} — état(s) attendu(s) mais "
                        f"absent(s) : {', '.join(manquants)}.")
        if surnumeraires:
            deplaces = {v: c for c, a in PARTITION_ATTENDUE.items()
                        for v in surnumeraires if v in a and c != cls}
            for v in surnumeraires:
                if v in deplaces:
                    errs.append(f"ASP-CI-4 : état `{v}` DÉPLACÉ — attendu en "
                                f"classe {deplaces[v]}, trouvé en classe {cls}. "
                                "La classification attestée n'est pas "
                                "renégociable par édition du contrat.")
                else:
                    errs.append(f"ASP-CI-4 : classe {cls} — état `{v}` ajouté, "
                                "hors classification attestée.")
    # La classe N n'énumère rien : « toute autre valeur » n'est pas énumérable.
    if part[CLASSE_NON_QUALIFIEE][0]:
        errs.append("ASP-CI-4 : la classe N ne doit énumérer aucune valeur — "
                    "elle absorbe par définition tout ce qui n'est pas nommé.")

    # ---- Lien classe N → refus par défaut → ETAT_NON_QUALIFIE -------------
    effet_n = part[CLASSE_NON_QUALIFIEE][1]
    if CODE_ETAT_NON_QUALIFIE not in effet_n:
        errs.append(f"ASP-CI-4 : la classe N ne produit pas "
                    f"`{CODE_ETAT_NON_QUALIFIE}` — sans ce lien, un état inconnu "
                    "n'a plus de motif de refus nommé.")
    bloc = bloc_partition(t07)
    regle_defaut = [m for m in DECL_INV.finditer(bloc)]
    if not regle_defaut:
        errs.append("ASP-CI-4 : aucune règle de refus par défaut déclarée en "
                    "07 §5.0 — la classe N n'est pas opposable.")
    elif CODE_ETAT_NON_QUALIFIE not in bloc.split(regle_defaut[0].group(0), 1)[1]:
        errs.append(f"ASP-CI-4 : la règle de refus par défaut de 07 §5.0 ne nomme "
                    f"pas `{CODE_ETAT_NON_QUALIFIE}`.")

    # ---- Couverture des états cités ailleurs dans le domaine --------------
    tous = {v for cls in PARTITION_ATTENDUE for v in part[cls][0]}
    m = ENUM_08.search(t08)
    if not m:
        errs.append("ASP-CI-4 : énumération des états introuvable en 08 §2.")
        return errs
    non_classes = sorted(set(ETAT.findall(m.group(1))) - tous)
    if non_classes:
        errs.append("ASP-CI-4 : état(s) cité(s) par le domaine mais non classés "
                    f"par la partition : {', '.join(non_classes)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-5 — table des profils
# ─────────────────────────────────────────────────────────────

PROFIL = re.compile(
    r'^\| \*\*([^*|\n]+)\*\* \| `([a-z_]+)` \| `([a-z_]+)` \|', re.M)


def parse_profils(t03: str) -> list[tuple[str, str, str]]:
    try:
        bloc = t03.split("## 1. Table canonique", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return []
    return PROFIL.findall(bloc)


def check_profils(t03: str) -> list[str]:
    errs: list[str] = []
    profils = parse_profils(t03)
    if len(profils) != 5:
        errs.append(f"ASP-CI-5 : la table des profils doit en compter 5 "
                    f"(trouvé {len(profils)}).")
    if not profils:
        return errs
    noms = [p[0].strip() for p in profils]
    if len(set(noms)) != len(noms):
        errs.append("ASP-CI-5 : deux profils portent le même libellé.")
    for nom, fan, eau in profils:
        nom = nom.strip()
        if fan == FAN_SPEED_EXCLUE:
            errs.append(f"ASP-CI-5 : profil « {nom} » emploie `{FAN_SPEED_EXCLUE}`, "
                        "explicitement exclu par ASP-INV-11.")
        elif fan not in FAN_SPEEDS_AUTORISEES:
            errs.append(f"ASP-CI-5 : profil « {nom} » — aspiration `{fan}` hors "
                        f"énumération attestée {sorted(FAN_SPEEDS_AUTORISEES)}.")
        if eau not in WATER_LEVELS_ATTESTES:
            errs.append(f"ASP-CI-5 : profil « {nom} » — intensité d'eau `{eau}` "
                        f"hors énumération attestée {sorted(WATER_LEVELS_ATTESTES)}.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-6 — identifiants, attestation par jeton exact
# ─────────────────────────────────────────────────────────────

JETON = re.compile(r'\b([a-z][a-z0-9_]*)\.([a-z0-9_]+)\b')


def tous_les_jetons(texte: str) -> set[str]:
    """Tous les jetons `<domaine>.<objet>` du texte, sans filtrage."""
    return {f"{d}.{o}" for d, o in JETON.findall(texte)}


def concerne_le_domaine(jeton: str) -> bool:
    """Le jeton désigne-t-il ce domaine ?

    Deux voies, aucune ne reposant sur une liste de domaines Home Assistant :
    l'objet mentionne l'aspirateur ou le robot, ou le domaine est l'un des deux
    propres à l'appareil (`vacuum.`, `roborock.`). C'est ce qui écarte un nom de
    fichier (`07_moteur_de_mission.md`) ou un littéral (`image.png`) sans avoir à
    énumérer quoi que ce soit.
    """
    domaine, objet = jeton.split(".", 1)
    return domaine in ROBOT_DOMAINS or any(m in objet for m in MARQUEURS_DOMAINE)


def jetons_du_domaine(texte: str) -> set[str]:
    return {j for j in tous_les_jetons(texte) if concerne_le_domaine(j)}


def check_identifiants(textes: dict[str, str], audit: str) -> list[str]:
    """Attend des textes DÉJÀ débarrassés de leurs blocs de code."""
    errs: list[str] = []
    if not audit:
        errs.append("ASP-CI-6 : audit factuel du domaine introuvable — aucun "
                    "identifiant ne peut être attesté.")
        return errs
    # L'attestation se fait contre TOUS les jetons de l'audit : la comparaison
    # est une appartenance exacte, jamais une sous-chaîne.
    attestes = tous_les_jetons(audit)
    cites: set[str] = set()
    for txt in textes.values():
        cites |= jetons_du_domaine(txt)
    for jeton in sorted(cites):
        # Comparaison par JETON ENTIER : un préfixe tronqué d'une entité réelle
        # ne passe pas, là où une recherche par sous-chaîne l'aurait laissé filer.
        if jeton in attestes:
            continue
        domaine = jeton.split(".", 1)[0]
        if domaine in ARSENAL_HELPER_DOMAINS:
            errs.append(f"ASP-CI-6 : `{jeton}` — un contrat antérieur au runtime "
                        "ne nomme aucun objet Arsenal ; ASP-INV-58 interdit d'en "
                        "proposer la valeur.")
        elif jeton in SERVICE_PRIMITIVES:
            errs.append(f"ASP-CI-6 : `{jeton}` est une primitive de service "
                        "documentée, mais elle n'est pas attestée par l'audit du "
                        "domaine.")
        else:
            errs.append(f"ASP-CI-6 : `{jeton}` n'est ni attesté par l'audit du "
                        "domaine, ni une primitive de service documentée.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-7 — aucune commande brute en Lovelace
# ─────────────────────────────────────────────────────────────

ROBOROCK_ACTION = re.compile(
    r'\b(?:' + "|".join(ACTION_DOMAINS) + r')\.[a-z0-9_]*roborock[a-z0-9_]*')
# Nom de service STATIQUE sous une clé Lovelace. La cible (`entity_id`,
# `device_id`, `area_id`, `label_id`) n'est pas regardée : c'est le SERVICE qui
# est interdit, pas la façon de le viser. Limites assumées et documentées en
# tête de module : un appel générique ciblé par `device_id`, un nom de service
# templatisé, et la portée globale de `vacuum.*` face à un futur second
# aspirateur.
APPEL_SERVICE = re.compile(
    r'^[^\S\n]*(?:-[^\S\n]*)?(?:service|action|perform_action)[^\S\n]*:[^\S\n]*["\']?'
    r'((?:' + "|".join(SERVICE_DOMAINS_INTERDITS) + r')\.[a-z0-9_]+)',
    re.M)


def check_lovelace(fichiers: dict[str, str]) -> list[str]:
    errs: list[str] = []
    for chemin, contenu in sorted(fichiers.items()):
        # Une mention en commentaire n'est pas un appel : on retire les lignes
        # dont le premier caractère non blanc est un dièse.
        utile = "\n".join(l for l in contenu.splitlines()
                          if not l.lstrip().startswith("#"))
        for trouve in sorted(set(ROBOROCK_ACTION.findall(utile))):
            errs.append(f"ASP-CI-7 : entité native d'action `{trouve}` exposée "
                        f"dans {chemin} — ASP-INV-31 impose le passage par "
                        "l'écrivain unique du domaine.")
        for service in sorted(set(APPEL_SERVICE.findall(utile))):
            errs.append(f"ASP-CI-7 : nom de service `{service}` sous une clé "
                        f"d'action dans {chemin} — une commande statiquement "
                        "nommée contourne l'écrivain unique, quel que soit le "
                        "mode de ciblage (ASP-INV-31).")
    return errs


# ─────────────────────────────────────────────────────────────
# Exécution réelle
# ─────────────────────────────────────────────────────────────

def load_domain() -> dict[str, str]:
    if not DOMAIN.is_dir():
        return {}
    return {p.name: p.read_text(encoding="utf-8", errors="ignore")
            for p in sorted(DOMAIN.glob("*.md"))}


def load_lovelace() -> dict[str, str]:
    out: dict[str, str] = {}
    for d in LOVELACE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.yaml")):
            if p.is_file():
                out[p.relative_to(ROOT).as_posix()] = p.read_text(
                    encoding="utf-8", errors="ignore")
    return out


def run() -> int:
    bruts = load_domain()
    if not bruts:
        sys.stderr.write(f"erreur : domaine introuvable : {DOMAIN}\n")
        return 2
    # Blocs de code neutralisés : un exemple documentaire n'est pas une
    # déclaration normative (ASP-CI-1, ASP-CI-3, ASP-CI-6).
    # R3 — la neutralisation vaut pour LES SEPT contrôles, pas seulement pour
    # ASP-CI-1/3/6 : un exemple documentaire n'est normatif nulle part. L'audit
    # est neutralisé pour la même raison — un faux tableau de segments placé dans
    # un bloc n'y attesterait rien.
    textes = sans_clotures(bruts)
    brut_audit = AUDIT.read_text(encoding="utf-8", errors="ignore") if AUDIT.is_file() else ""
    audit = strip_fences(brut_audit)
    lovelace = load_lovelace()

    controles = (
        ("ASP-CI-1  invariants", check_invariants(textes)),
        ("ASP-CI-2  référentiel des segments",
         check_referentiel(textes.get("02_referentiel_cartes_et_pieces.md", ""),
                           textes.get("10_raccourcis.md", ""), audit)),
        ("ASP-CI-3  catalogue des codes", check_codes(textes)),
        ("ASP-CI-4  partition des états",
         check_partition(textes.get("07_moteur_de_mission.md", ""),
                         textes.get("08_etats_et_observation.md", ""))),
        ("ASP-CI-5  table des profils",
         check_profils(textes.get("03_profils_metier.md", ""))),
        ("ASP-CI-6  identifiants", check_identifiants(textes, audit)),
        ("ASP-CI-7  Lovelace", check_lovelace(lovelace)),
    )

    erreurs: list[str] = []
    for label, errs in controles:
        print(f"  {'✗' if errs else '✔'} {label}")
        erreurs.extend(errs)

    attestes_audit = tous_les_jetons(audit)
    print(f"\n  périmètre : {len(textes)} fichiers de contrat · "
          f"{len(lovelace)} fichiers Lovelace balayés · "
          f"{len(attestes_audit)} identifiants attestés par l'audit")
    if erreurs:
        print("\nAspirateur — écarts contractuels détectés :")
        for e in erreurs:
            print(f"- {e}")
        return 1
    print("\nOK - domaine Aspirateur : intégrité normative vérifiée "
          "(7 contrôles, 0 écart).")
    return 0


# ─────────────────────────────────────────────────────────────
# Selftest — le juge se vérifie avant de juger
# ─────────────────────────────────────────────────────────────

class Compteur:
    """Décompte DÉRIVÉ des cas joués : aucun total n'est écrit à la main."""

    def __init__(self) -> None:
        self.conformes = 0
        self.violations = 0

    def conforme(self, errs: list[str], libelle: str) -> None:
        assert not errs, f"{libelle} : attendu conforme, obtenu {errs}"
        self.conformes += 1

    def viole(self, errs: list[str], motif: str, libelle: str) -> None:
        assert any(motif in e for e in errs), \
            f"{libelle} : attendu « {motif} », obtenu {errs}"
        self.violations += 1

    def total(self) -> int:
        return self.conformes + self.violations


def selftest() -> None:
    c = Compteur()

    # ---- strip_fences (F6) : un bloc clôturé ne déclare rien --------------
    fixture_bloc = (
        "> **`ASP-INV-1`** — vrai\n> ### `ASP-IMC-1` — vrai\n"
        "```yaml\n> **`ASP-INV-99`** — faux invariant\n"
        "`REFUS_FICTIF`\nscript.faux_identifiant\n```\n")
    neutralise = {"a.md": strip_fences(fixture_bloc)}
    c.conforme(check_invariants(neutralise), "F6/CI-1 bloc clôturé")
    cat_bloc = {
        FICHIER_CATALOGUE: ("## 2. Catalogue des refus\n| `REFUS_UN` | m |\n"
                            "## 3. Catalogue des échecs\n| `ECHEC_UN` | m |\n\n## 4. s\n"),
        "07.md": strip_fences("`REFUS_UN`\n```\n`REFUS_FICTIF`\n```\n")}
    c.conforme(check_codes(cat_bloc), "F6/CI-3 bloc clôturé")
    c.conforme(check_identifiants(
        {"a.md": strip_fences("```\nscript.faux_identifiant\n```\n")},
        "vacuum.roborock_q7_max"), "F6/CI-6 bloc clôturé")

    # ---- ASP-CI-1 --------------------------------------------------------
    bon = {"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-2`** — y\n",
           "b.md": "> **`ASP-INV-3`** — z\n> ### `ASP-IMC-1` — t\n"}
    c.conforme(check_invariants(bon), "CI-1 conforme")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-3`** — z\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "trouée", "CI-1 trou")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n> **`ASP-INV-1`** — y\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "plusieurs fois", "CI-1 doublon")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n"
                                      "> **Invariant `ASP-INV-2`** — y\n"
                                      "> ### `ASP-IMC-1` — t\n"}),
            "non uniforme", "CI-1 format")
    c.viole(check_invariants({"a.md": "> **`ASP-INV-1`** — x\n"}),
            "ASP-IMC-1", "CI-1 IMC absent")

    # ---- ASP-CI-2 : ancre audit (F1) -------------------------------------
    AUD = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
           "| `1_16` | `Palier` | Étage |\n"
           "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
           "| **0** | `RDC` | 2 |\n| **1** | `Étage ` | 1 |\n")

    def t02(seg="0_16", nom="Séjour", roboro="`Salon`", comp="`0_16` · `0_18`",
            carte="0", extra=""):
        return (f"| `{seg}` | **{nom}** | {roboro} |\n"
                "| `0_18` | **Entrée** | — |\n"
                "| `1_16` | **Palier** |\n" + extra +
                f"| **RDC complet** | `{carte}` | {comp} |\n")
    t10_ok = "| **Étage** | `1` | `1_16` |\n"
    c.conforme(check_referentiel(t02(), t10_ok, AUD), "CI-2 conforme")
    # Falsification COHÉRENTE de toute la chaîne : table + périmètre + raccourci.
    c.viole(check_referentiel(t02(seg="0_77", comp="`0_77` · `0_18`"),
                              t10_ok, AUD),
            "ABSENT de l'audit", "F1/CI-2 falsification cohérente")
    c.viole(check_referentiel(t02(nom="Salon Bis", roboro="—"), t10_ok, AUD),
            "l'audit atteste", "F1/CI-2 nom falsifié")
    c.viole(check_referentiel(t02(extra="| `2_17` | **Extérieur** |\n",
                                  comp="`0_16` · `0_18` · `2_17`"), t10_ok, AUD),
            "NON COMMANDABLE", "F1/CI-2 segment observé promu")
    c.viole(check_referentiel(t02(), t10_ok, ""),
            "ne peut pas être attesté", "F1/CI-2 audit absent")
    c.viole(check_referentiel(t02(comp="`0_16` · `0_99`"), t10_ok, AUD),
            "hors référentiel", "CI-2 segment inconnu")
    c.viole(check_referentiel(t02(comp="`0_16` · `1_16`"),
                              "| **X** | `0` | `0_18` |\n", AUD),
            "plusieurs cartes", "CI-2 multi-carte")
    c.viole(check_referentiel(t02(carte="1"), t10_ok, AUD),
            "déclare la carte", "CI-2 carte incohérente")
    c.viole(check_referentiel(t02(), "| **X** | `0` | `0_18` |\n", AUD),
            "jamais employés", "CI-2 segment orphelin")

    # ---- ASP-CI-3 --------------------------------------------------------
    def cat(extra_refus="", cite="", renvoi=""):
        t09 = ("## 2. Catalogue des refus\n| `REFUS_UN` | motif |\n"
               f"{extra_refus}"
               "## 3. Catalogue des échecs\n| `ECHEC_UN` | motif |\n\n## 4. suite\n")
        return {FICHIER_CATALOGUE: t09,
                "07.md": "`REFUS_UN`" + cite + renvoi}
    c.conforme(check_codes(cat()), "CI-3 conforme")
    c.viole(check_codes(cat(cite=" et `REFUS_FANTOME`")),
            "hors catalogue", "CI-3 code orphelin")
    c.viole(check_codes(cat(extra_refus="| `REFUS_MORT` | motif |\n")),
            "qu'aucune clause ne produit", "CI-3 refus mort")
    # F8 : un refus cité UNIQUEMENT dans une section « Renvois » est mort.
    c.viole(check_codes(cat(extra_refus="| `REFUS_RENVOI` | motif |\n",
                            renvoi="\n\n## Renvois\n\n- voir `REFUS_RENVOI`\n")),
            "qu'aucune clause ne produit", "F8/CI-3 refus vivant par renvoi seul")
    # F9 : un code de cinq caractères est traité comme les autres.
    c.viole(check_codes(cat(extra_refus="| `ABCDE` | motif |\n")),
            "ABCDE", "F9/CI-3 code de cinq caractères")
    c.conforme(check_codes({FICHIER_CATALOGUE: ("## 2. Catalogue des refus\n"
                                                "| `ABCDE` | motif |\n"
                                                "## 3. Catalogue des échecs\n"
                                                "| `ECHEC_UN` | m |\n\n## 4. s\n"),
                            "07.md": "`ABCDE`"}),
               "F9/CI-3 code de cinq caractères produit")

    # ---- ASP-CI-4 : classification figée (F2) et lien N (F13) -------------
    def part(r="`charger_disconnected` · `charging`",
             a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · "
               "`returning_home` · `docking`",
             e="`error` · `device_offline` · `unknown` · `unavailable`",
             n_effet="**Refus** `ETAT_NON_QUALIFIE`",
             regle="> **`ASP-INV-60`** — refus par défaut `ETAT_NON_QUALIFIE`.\n"):
        return ("### 5.0 titre\n"
                f"| **R — Repos** | {r} | **Admissible** |\n"
                f"| **A — Activité** | {a} | `MISSION_DEJA_OUVERTE` |\n"
                f"| **E — Erreur** | {e} | Refus |\n"
                f"| **N — Non qualifiée** | toute autre valeur | {n_effet} |\n"
                + regle + "### 5.1 suite\n")
    t08 = ("énumération **non exhaustive** : `charger_disconnected`, `charging`, "
           "`cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, "
           "`returning_home`, `docking`, `error`, `device_offline`…\n")
    c.conforme(check_partition(part(), t08), "CI-4 conforme")
    # F2 : le déplacement A -> R, la régression exacte que le checker vise.
    c.viole(check_partition(part(
        r="`charger_disconnected` · `charging` · `returning_home`",
        a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · `docking`"),
        t08), "DÉPLACÉ", "F2/CI-4 returning_home A -> R")
    c.viole(check_partition(part(
        a="`cleaning` · `segment_cleaning` · `zoned_cleaning` · `paused` · "
          "`returning_home`"), t08),
        "absent", "F2/CI-4 docking retiré")
    c.viole(check_partition(part(r="`charger_disconnected` · `charging` · `idle`"), t08),
            "hors classification attestée", "F2/CI-4 état ajouté")
    # F13 : le lien classe N -> ETAT_NON_QUALIFIE, code conservé ailleurs.
    c.viole(check_partition(part(n_effet="**Refus**"), t08),
            "ne produit pas", "F13/CI-4 lien N rompu")
    c.viole(check_partition(part(regle="> **`ASP-INV-60`** — refus par défaut.\n"),
                            t08),
            "ne nomme pas", "F13/CI-4 règle par défaut muette")
    c.viole(check_partition(part(regle=""), t08),
            "aucune règle de refus par défaut", "F13/CI-4 règle absente")
    # R1 : ligne N tronquée à deux colonnes, suivie d'une prose SANS barre qui
    # mentionne le code. Un motif franchissant la ligne capturerait cette prose
    # comme cellule d'effet et conclurait à tort que le lien tient.
    c.viole(check_partition(
        "### 5.0 titre\n"
        "| **R — Repos** | `charger_disconnected` · `charging` | ok |\n"
        "| **A — Activité** | `cleaning` · `segment_cleaning` · `zoned_cleaning` · "
        "`paused` · `returning_home` · `docking` | ok |\n"
        "| **E — Erreur** | `error` · `device_offline` · `unknown` · `unavailable` | ok |\n"
        "| **N — Non qualifiée** | toute autre valeur |\n"
        "prose libre sans barre mentionnant ETAT_NON_QUALIFIE\n"
        "> **`ASP-INV-60`** — refus par défaut `ETAT_NON_QUALIFIE`.\n"
        "### 5.1 suite\n", t08),
        "incomplète", "R1/CI-4 ligne N tronquée + prose ultérieure")
    c.viole(check_partition("pas de section 5.0", t08),
            "incomplète", "CI-4 partition absente")

    # ---- ASP-CI-5 --------------------------------------------------------
    lignes = [("Normale", "balanced", "off"), ("Turbo", "turbo", "off"),
              ("Max", "max", "off"), ("Moyenne", "quiet", "medium"),
              ("Intensive", "quiet", "high")]

    def t03(rows):
        corps = "".join(f"| **{n}** | `{f}` | `{e}` |\n" for n, f, e in rows)
        return "## 1. Table canonique\n" + corps + "\n## 2. suite\n"
    c.conforme(check_profils(t03(lignes)), "CI-5 conforme")
    c.viole(check_profils(t03(lignes[:4])), "compter 5", "CI-5 cardinalité")
    c.viole(check_profils(t03(lignes[:4] + [("Douce", "gentle", "off")])),
            "gentle", "CI-5 gentle réintroduit")
    c.viole(check_profils(t03(lignes[:4] + [("Bizarre", "ultra", "off")])),
            "hors énumération", "CI-5 valeur inventée")

    # ---- R3 : blocs clôturés sur ASP-CI-2, ASP-CI-4 et ASP-CI-5 ----------
    # Un exemple en bloc clôturé ne modifie ni le référentiel, ni une classe
    # d'état, ni la table des profils. La prose normative hors bloc, elle, reste
    # contrôlée — c'est ce que prouve le second cas de chaque paire.
    AUD_R3 = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
              "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
              "| **0** | `RDC` | 2 |\n")
    t02_r3 = ("| `0_16` | **Séjour** | `Salon` |\n| `0_18` | **Entrée** | — |\n"
              "```markdown\n| `9_99` | **Pièce fictive** | — |\n```\n"
              "| **RDC complet** | `0` | `0_16` · `0_18` |\n")
    t10_r3 = "| **Séjour seul** | `0` | `0_16` |\n"
    c.conforme(check_referentiel(strip_fences(t02_r3), t10_r3, AUD_R3),
               "R3/CI-2 faux segment en bloc clôturé")
    hors_bloc = t02_r3.replace("```markdown\n", "").replace("\n```\n", "\n")
    c.viole(check_referentiel(strip_fences(hors_bloc), t10_r3, AUD_R3),
            "ABSENT de l'audit", "R3/CI-2 le même segment hors bloc reste contrôlé")

    t07_r3 = part().replace("### 5.1 suite\n",
                            "```\n| **R — Repos** | `idle` | ok |\n```\n### 5.1 suite\n")
    c.conforme(check_partition(strip_fences(t07_r3), t08),
               "R3/CI-4 fausse classe en bloc clôturé")

    t03_r3 = ("## 1. Table canonique\n"
              + "".join(f"| **{n}** | `{f}` | `{e}` |\n" for n, f, e in lignes)
              + "```\n| **Faux profil** | `gentle` | `off` |\n```\n\n## 2. suite\n")
    c.conforme(check_profils(strip_fences(t03_r3)), "R3/CI-5 faux profil en bloc clôturé")
    c.viole(check_profils(strip_fences(t03_r3.replace("```\n", ""))),
            "gentle", "R3/CI-5 le même profil hors bloc reste contrôlé")

    # ---- ASP-CI-6 : jeton exact (F7, F12) --------------------------------
    # CONTRE-EXEMPLES DÉLIBÉRÉS, confinés au selftest. `script.aspirateur_lancer`,
    # `switch.aspirateur_relance` et `sensor.roborock_q7_max_eta` n'existent pas
    # et ne doivent jamais être créés : ils prouvent que le contrôle les REFUSE.
    audit_fixture = ("`vacuum.roborock_q7_max`, `sensor.roborock_q7_max_etat`, "
                     "`vacuum.send_command`")
    c.conforme(check_identifiants(
        {"a.md": "on cite `vacuum.roborock_q7_max` et `vacuum.send_command`"},
        audit_fixture), "CI-6 conforme")
    c.conforme(check_identifiants(
        {"a.md": "voir `07_moteur_de_mission.md` et le rôle `‹moteur_de_mission›`"},
        audit_fixture), "CI-6 nom de fichier et rôle abstrait")
    c.viole(check_identifiants({"a.md": "script.aspirateur_lancer"}, audit_fixture),
            "ASP-INV-58", "CI-6 helper Arsenal")
    # F7 : un domaine jusque-là absent de la liste.
    c.viole(check_identifiants({"a.md": "switch.aspirateur_relance"}, audit_fixture),
            "ni attesté", "F7/CI-6 domaine absent (switch)")
    c.viole(check_identifiants({"a.md": "input_button.aspirateur_relance"},
                               audit_fixture),
            "ASP-INV-58", "F7/CI-6 domaine absent (input_button)")
    # I1 : domaines volontairement absents de toute liste — la détection est
    # LEXICALE, elle ne dépend d'aucune énumération de domaines Home Assistant.
    for ident in ("plant.aspirateur_x", "sun.aspirateur_x", "lawn_mower.aspirateur_x",
                  "un_domaine_inexistant.aspirateur_x", "sensor.roborock_q7_max_inexistant"):
        c.viole(check_identifiants({"a.md": ident}, audit_fixture),
                "ni attesté", f"I1/CI-6 ciblage lexical — {ident}")
    # …et les emplois légitimes passent, y compris les primitives de service.
    c.conforme(check_identifiants(
        {"a.md": "`vacuum.start`, `vacuum.send_command`, `select.select_option`, "
                 "`sensor.roborock_q7_max_etat`, `image.png`, `un.texte`"},
        audit_fixture + " `select.select_option` `vacuum.start`"),
        "I1/CI-6 primitives, entité attestée, littéraux hors domaine")
    # F12 : préfixe tronqué d'une entité réelle.
    c.viole(check_identifiants({"a.md": "`sensor.roborock_q7_max_eta`"},
                               audit_fixture),
            "ni attesté", "F12/CI-6 identifiant tronqué")
    c.viole(check_identifiants({"a.md": "x"}, ""),
            "introuvable", "CI-6 audit absent")

    # ---- ASP-CI-7 : entités et services (F3) -----------------------------
    c.conforme(check_lovelace({"18_lovelace/x.yaml":
                               "entity: sensor.roborock_q7_max_batterie\n"
                               "entity: binary_sensor.roborock_q7_max_en_charge\n"
                               "entity: image.roborock_q7_max_rdc\n"}),
               "CI-7 lecture seule préservée")
    c.conforme(check_lovelace({"18_lovelace/x.yaml":
                               "# on ne doit pas appeler service: vacuum.start ici\n"}),
               "CI-7 mention en commentaire")
    c.viole(check_lovelace({"18_lovelace/x.yaml": "entity: vacuum.roborock_q7_max"}),
            "ASP-INV-31", "CI-7 entité d'action")
    c.viole(check_lovelace({"19_button_card_templates/y.yaml":
                            "entity: select.roborock_q7_max_carte_selectionnee"}),
            "ASP-CI-7", "CI-7 sélecteur brut")
    # F3 : cinq services bruts, ciblés sans aucun `entity_id` contenant roborock.
    for cible, service, libelle in (
        ("device_id: abc", "vacuum.send_command", "send_command par device_id"),
        ("area_id: rdc", "roborock.set_vacuum_zoned_cleaning", "service roborock.*"),
        ("label_id: sol", "vacuum.set_fan_speed", "set_fan_speed par label_id"),
        ("device_id: abc", "vacuum.start", "start par device_id"),
        ("area_id: etage", "vacuum.return_to_base", "return_to_base par area_id"),
    ):
        c.viole(check_lovelace({"18_lovelace/d.yaml":
                                "tap_action:\n  action: call-service\n"
                                f"  service: {service}\n  target: {{{cible}}}\n"
                                "  data: {command: app_segment_clean, "
                                "params: [{segments: [21], repeat: 2}]}\n"}),
                "nom de service", f"F3/CI-7 {libelle}")
    c.viole(check_lovelace({"18_lovelace/e.yaml":
                            "  perform_action: vacuum.stop\n  target: {device_id: z}\n"}),
            "nom de service", "F3/CI-7 perform_action")

    print(f"selftest OK — 7 contrôles, {c.total()} cas "
          f"({c.conformes} conformes, {c.violations} violations).")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Vérification contractuelle du domaine Aspirateur.")
    ap.add_argument("--selftest", action="store_true",
                    help="exécute les cas de test internes puis sort.")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    return run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
