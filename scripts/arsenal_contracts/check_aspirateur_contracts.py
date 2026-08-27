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

Dix contrôles, tous adossés à une clause déjà normée par le contrat :

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
  ASP-CI-8  Réf. tech.  — le référentiel TECHNIQUE (02 §2.1) est confronté à
                          l'audit — option EXACTE du sélecteur (espace finale
                          comprise), index de carte, index natif de segment, nom
                          Roborock —, mis en correspondance COMPLÈTE avec le
                          référentiel métier, et SÉPARÉ de lui mécaniquement :
                          aucune ligne n'est lue par les deux parseurs. `2_17`,
                          `2_18` et le Garage ne peuvent pas être promus
                          (ASP-INV-66/67, QO-1). Garde aussi, SECTION PAR
                          SECTION, les clauses qui rendent l'exception
                          cartographique close : cardinalité seule interdite,
                          table des trois usages autorisés, conditions 3 et 4
                          d'ASP-IMC-1, comparaison littérale, non-exposition des
                          libellés techniques. Une phrase semblable dans un
                          renvoi ou un index ne satisfait aucune garde.
  ASP-CI-9  États canon.— dix états canoniques exactement, sans synonyme ; image
                          TOTALE de la partition 07 §5.0 vers ces codes
                          (`charger_disconnected` → `repos_hors_base`, classe N →
                          `etat_non_qualifie`), lien vers le refus
                          `ETAT_NON_QUALIFIE`, et compteurs des chapitres 08, 11
                          et 12 réalignés (ASP-INV-44/68). Chaque compteur et
                          l'admissibilité de `repos_hors_base` sont ancrés sur
                          LEUR clause exacte — jamais sur une occurrence isolée
                          de « dix » ou « admissible » ailleurs dans le même
                          chapitre. Vérifie en outre que PARTITION_ATTENDUE et
                          IMAGE_ATTENDUE décrivent le même monde, classe par
                          classe : un état déplacé à image inchangée échoue.
  ASP-CI-10 Fenêtres    — deux constantes temporelles et deux seulement, 30 s
                          pour les confirmations (étapes 6, 8, 10) et 60 s pour
                          la seule transition de démarrage, associée sur SA
                          LIGNE de catalogue à `TRANSITION_NON_OBSERVEE` ;
                          aucune durée concurrente sur LES QUATORZE chapitres —
                          l'observation terrain du 08 §3 est exemptée par sa
                          clause littérale, jamais par une allowlist de nombres ;
                          aucun helper temporel, aucun fallback, révision
                          CONJOINTE contrat + checker + runtime
                          (ASP-INV-69, ARB-3).


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
CODE_TRANSITION = "TRANSITION_NON_OBSERVEE"

# Segments observés dans une carte mais SANS rôle métier V1 (contrat 02 §2,
# QO-1). Attestés par l'audit, ils doivent rester hors de la table canonique.
SEGMENTS_NON_COMMANDABLES = {"2_17", "2_18"}
# Carte observée sans aucun segment nommé — jamais commandable (audit §4).
CARTE_SANS_SEGMENT = "Garage"

# Vocabulaire canonique des états (08 §1). Dix codes, aucun synonyme.
ETATS_CANONIQUES = (
    "mission_ouverte", "nettoyage_reel", "pause", "erreur", "retour_base",
    "amarrage", "charge", "repos_hors_base", "indisponibilite",
    "etat_non_qualifie")
# `mission_ouverte` dérive du TÉMOIN DE SESSION, pas de l'état machine : il se
# superpose aux neuf autres et n'a donc aucune image dans la partition.
ETAT_ORTHOGONAL = "mission_ouverte"
# Image attendue partition (07 §5.0) -> code canonique (08 §1).
IMAGE_ATTENDUE = {
    "charger_disconnected": "repos_hors_base", "charging": "charge",
    "cleaning": "nettoyage_reel", "segment_cleaning": "nettoyage_reel",
    "zoned_cleaning": "nettoyage_reel", "paused": "pause",
    "returning_home": "retour_base", "docking": "amarrage",
    "error": "erreur", "device_offline": "indisponibilite",
    "unknown": "indisponibilite", "unavailable": "indisponibilite"}
CODE_CANONIQUE_CLASSE_N = "etat_non_qualifie"
# i-2 — codes canoniques admis pour chaque classe explicite de la partition.
# Lier les deux ancres par la CLASSE, et pas seulement par l'ensemble des états,
# est ce qui rend détectable un DÉPLACEMENT d'état entre classes à image
# inchangée : `charging` passé de R à A garderait l'image `charge`, qui
# n'appartient pas aux codes de la classe A.
CODES_PAR_CLASSE = {
    "R": {"charge", "repos_hors_base"},
    "A": {"nettoyage_reel", "pause", "retour_base", "amarrage"},
    "E": {"erreur", "indisponibilite"}}

# Fenêtres temporelles contractuelles (07 §3.1). Deux valeurs, et deux seulement.
FENETRE_CONFIRMATION_S = 30
FENETRE_TRANSITION_S = 60
ETAPES_CONFIRMATION = ("6", "8", "10")
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
# ASP-CI-8 — référentiel TECHNIQUE (02 §2.1), ancré sur l'audit
# ─────────────────────────────────────────────────────────────
#
# Le domaine porte DEUX référentiels qui ne doivent jamais se confondre :
#
#   - le référentiel MÉTIER (02 §2)    — libellés canoniques Arsenal, ce que le
#                                        système restitue et ce qu'il désigne ;
#   - le référentiel TECHNIQUE (02 §2.1) — valeurs exactes de l'appareil,
#                                        employées UNIQUEMENT pour écrire et
#                                        confirmer le contexte cartographique.
#
# La séparation est MÉCANIQUE, pas typographique : les deux tables ont des
# parseurs distincts, et ce contrôle vérifie explicitement qu'aucune ligne n'est
# capturée par les deux — une table technique que le parseur métier lirait comme
# un référentiel de désignation serait exactement la confusion que 02 §5 proscrit.
#
# ANCRE : l'audit. Une falsification COHÉRENTE du contrat — table métier, table
# technique, périmètres et raccourcis modifiés ensemble — reste détectée, car
# aucune des deux tables ne s'atteste elle-même.

TECH_CARTE = re.compile(
    r'^\| (?:`(\d)`|—) \| `([^`\n]*)` \| (commandable|non commandable) \|$', re.M)
TECH_SEGMENT = re.compile(
    r'^\| `(\d+_\d+)` \| `(\d+)` \| `([^`\n]*)` \| (commandable|non commandable) \|$',
    re.M)


def section_normative(texte: str, debut: str,
                      fin: str = "\n## ") -> str:
    """Bloc NORMATIF borné : de `debut` jusqu'à la borne suivante.

    Les gardes de clause s'appliquent à ce bloc et à lui seul : une phrase
    semblable placée dans un renvoi, un index ou une autre section ne satisfait
    aucune garde. Les blocs clôturés sont déjà neutralisés en amont (R3).
    """
    try:
        return texte.split(debut, 1)[1].split(fin, 1)[0]
    except IndexError:
        return ""


def bloc_technique(t02: str) -> str:
    """Bloc 02 §2.1 seul — jamais le référentiel métier qui le précède."""
    try:
        return t02.split("### 2.1", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return ""


# M-2 — clauses qui rendent l'exception cartographique CLOSE. Chacune est
# localisée dans SA section normative : (bloc, ancre de début, motifs exigés).
CLAUSES_BORNAGE = (
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une confirmation par cardinalité.**", "inclusion nominale"),
     "l'exception admettrait une confirmation par simple décompte des pièces"),
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une autorité métier.**",),
     "le référentiel technique deviendrait une vérité de désignation"),
    ("02 §2.1", "### 2.1", "\n## ",
     ("- **Ni une donnée d'interface.**",),
     "les libellés d'appareil pourraient être exposés à l'opérateur"),
    ("02 §5", "## 5. Règle de restitution", "\n## ",
     ("| Écrire la sélection de carte |",
      "| Confirmer la sélection par relecture |",
      "| Confirmer les pièces exposées de la carte |"),
     "l'exception ne serait plus énumérée, donc plus close"),
    ("02 §5", "## 5. Règle de restitution", "\n## ",
     ("la comparaison est **littérale**", "approchée"),
     "un rapprochement approximatif deviendrait admissible"),
    ("06 §3", "## 3. Conditions de satisfaction", "\n### ",
     ("| 3 |", "comparaison **littérale**"),
     "la relecture du sélecteur ne serait plus littérale"),
    ("06 §3", "## 3. Conditions de satisfaction", "\n### ",
     ("| 4 |", "contiennent l'intégralité", "§2.1"),
     "la condition 4 ne serait plus fondée sur le référentiel technique"),
    ("06 §3.1", "### 3.1", "\n## ",
     ("Comment l'inclusion se constate", "§2.1", "**littérale**"),
     "le mécanisme d'inclusion nominale ne serait plus dit"),
)


def check_bornage_exception(t02: str, t06: str) -> list[str]:
    """M-2 — l'exception cartographique reste close, clause par clause."""
    errs: list[str] = []
    sources = {"02": t02, "06": t06}
    for section, debut, fin, motifs, consequence in CLAUSES_BORNAGE:
        corps = section_normative(sources[section.split()[0]], debut, fin)
        if not corps:
            errs.append(f"ASP-CI-8 : section {section} introuvable — la clause "
                        "de bornage ne peut plus être vérifiée.")
            continue
        for motif in motifs:
            if motif not in corps:
                errs.append(f"ASP-CI-8 : {section} — clause de bornage absente "
                            f"ou affaiblie ({motif!r} introuvable DANS cette "
                            f"section) : {consequence}.")
    return errs


def check_referentiel_technique(t02: str, t06: str, audit: str) -> list[str]:
    errs: list[str] = []
    bloc = bloc_technique(t02)
    if not bloc:
        return ["ASP-CI-8 : référentiel technique introuvable (02 §2.1) — la "
                "sélection et la confirmation de carte n'ont plus de source."]

    cartes = TECH_CARTE.findall(bloc)
    segments = TECH_SEGMENT.findall(bloc)
    if not cartes:
        errs.append("ASP-CI-8 : table technique des cartes introuvable (02 §2.1).")
    if not segments:
        errs.append("ASP-CI-8 : table technique des segments introuvable (02 §2.1).")
    if errs:
        return errs

    # ---- Séparation mécanique des deux référentiels ----------------------
    if SEGMENT_CANON.search(bloc):
        errs.append("ASP-CI-8 : le référentiel technique est capturé par le "
                    "parseur du référentiel MÉTIER — les deux tables se "
                    "confondent, la séparation de 02 §5 n'est plus mécanique.")
    if TECH_SEGMENT.search(t02.split("### 2.1", 1)[0]):
        errs.append("ASP-CI-8 : le référentiel métier contient une ligne au "
                    "format TECHNIQUE — un libellé d'appareil s'est glissé dans "
                    "la vérité de désignation (ASP-INV-66).")

    # ---- Ancre : cartes attestées par l'audit ----------------------------
    cartes_audit = dict(AUDIT_CARTE.findall(audit))
    if not cartes_audit:
        return errs + ["ASP-CI-8 : table des cartes introuvable dans l'audit — "
                       "le référentiel technique ne peut pas être attesté."]

    commandables = set()
    for idx, option, statut in cartes:
        if statut == "non commandable":
            if option != CARTE_SANS_SEGMENT:
                errs.append(f"ASP-CI-8 : carte `{option}` déclarée non "
                            f"commandable — seule `{CARTE_SANS_SEGMENT}` l'est.")
            elif idx:
                errs.append(f"ASP-CI-8 : `{CARTE_SANS_SEGMENT}` porte un index "
                            f"de carte (`{idx}`) — l'audit ne lui en atteste "
                            "aucun, et lui en donner un le rendrait adressable.")
            continue
        if not idx:
            errs.append(f"ASP-CI-8 : carte commandable `{option}` sans index.")
            continue
        commandables.add(idx)
        if idx not in cartes_audit:
            errs.append(f"ASP-CI-8 : carte `{idx}` ABSENTE de l'audit — le "
                        "référentiel technique invente une carte.")
        elif cartes_audit[idx] != option:
            errs.append(f"ASP-CI-8 : carte `{idx}` — option du sélecteur "
                        f"`{option}` alors que l'audit atteste "
                        f"`{cartes_audit[idx]}`. La comparaison est LITTÉRALE : "
                        "une espace finale attestée fait partie de la valeur "
                        "(ASP-INV-67).")
    if commandables != CARTES_COMMANDABLES:
        errs.append("ASP-CI-8 : cartes commandables "
                    f"{sorted(commandables) or 'aucune'} ; attendu "
                    f"{sorted(CARTES_COMMANDABLES)}.")
    if not any(o == CARTE_SANS_SEGMENT and s == "non commandable"
               for _, o, s in cartes):
        errs.append(f"ASP-CI-8 : `{CARTE_SANS_SEGMENT}` n'est pas déclaré non "
                    "commandable — son statut doit rester explicite.")

    # ---- Ancre : segments attestés par l'audit ---------------------------
    atteste = parse_audit_segments(audit)
    if not atteste:
        return errs + ["ASP-CI-8 : table des segments introuvable dans l'audit."]

    vus = set()
    for seg, index_natif, nom, statut in segments:
        vus.add(seg)
        carte, _, suffixe = seg.partition("_")
        if index_natif != suffixe:
            errs.append(f"ASP-CI-8 : segment `{seg}` — index natif "
                        f"`{index_natif}` incohérent avec la paire (`{suffixe}` "
                        "attendu). C'est cet index qui entre dans la charge "
                        "utile : une dérive y nettoie une autre pièce.")
        if seg not in atteste:
            errs.append(f"ASP-CI-8 : segment `{seg}` ABSENT de l'audit — le "
                        "référentiel technique invente un segment.")
            continue
        nom_atteste, carte_attestee = atteste[seg]
        if nom != nom_atteste:
            errs.append(f"ASP-CI-8 : segment `{seg}` — nom Roborock `{nom}` "
                        f"alors que l'audit atteste `{nom_atteste}`.")
        if carte in cartes_audit and \
                cartes_audit[carte].strip() != carte_attestee.strip():
            errs.append(f"ASP-CI-8 : segment `{seg}` — l'audit le rattache à la "
                        f"carte `{carte_attestee}`, incompatible avec l'index "
                        f"de carte `{carte}` (`{cartes_audit[carte].strip()}`).")
        attendu = "non commandable" if seg in SEGMENTS_NON_COMMANDABLES \
            else "commandable"
        if statut != attendu:
            errs.append(f"ASP-CI-8 : segment `{seg}` déclaré `{statut}` — "
                        f"attendu `{attendu}`. Les segments observés hors "
                        "référentiel V1 confirment la carte, ils ne deviennent "
                        "jamais désignables (QO-1).")
    manquants = sorted(set(atteste) - vus)
    if manquants:
        errs.append("ASP-CI-8 : segment(s) attesté(s) par l'audit et absent(s) "
                    f"du référentiel technique : {', '.join(manquants)} — la "
                    "vue de l'appareil doit y être exhaustive, statut compris.")

    # ---- Correspondance complète métier ↔ technique ----------------------
    canon = parse_segments(t02)
    tech_commandables = {s for s, _, _, st in segments if st == "commandable"}
    if tech_commandables != set(canon):
        errs.append("ASP-CI-8 : les deux référentiels divergent — commandables "
                    f"techniques {sorted(tech_commandables)} contre métier "
                    f"{sorted(canon)}.")
    noms_tech = {s: n for s, _, n, _ in segments}
    for seg in sorted(set(canon) & set(noms_tech)):
        libelle, divergent = canon[seg]
        if (divergent or libelle) != noms_tech[seg]:
            errs.append(f"ASP-CI-8 : segment `{seg}` — le référentiel métier "
                        f"annonce le nom Roborock `{divergent or libelle}`, le "
                        f"référentiel technique `{noms_tech[seg]}`.")
    promus = sorted(SEGMENTS_NON_COMMANDABLES & set(canon))
    if promus:
        errs.append(f"ASP-CI-8 : segment(s) non commandable(s) promu(s) au "
                    f"référentiel métier : {', '.join(promus)}.")

    # ---- M-2 : l'exception cartographique reste close --------------------
    errs.extend(check_bornage_exception(t02, t06))
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-9 — modèle canonique d'états (08 §1), total sur la partition
# ─────────────────────────────────────────────────────────────

ETAT_CANON = re.compile(r'^\| \*\*([^*|\n]+)\*\* \| `([a-z_]+)` \|', re.M)
IMAGE_CANON = re.compile(
    r'^> \| \*\*([RAEN])\*\* \| ([^|\n]+) \| `([a-z_]+)` \|', re.M)


def coherence_ancres(partition: dict | None = None,
                     image: dict | None = None,
                     codes_par_classe: dict | None = None) -> list[str]:
    """i-2 — PARTITION_ATTENDUE et IMAGE_ATTENDUE décrivent le MÊME monde.

    Deux ancres de module qui divergeraient laisseraient passer un contrat
    faux : un état ajouté à la partition sans image canonique, ou une image
    portant un état que la partition ne classe pas. La classe N est traitée à
    part — elle n'énumère rien, sa règle est un défaut.
    """
    partition = PARTITION_ATTENDUE if partition is None else partition
    image = IMAGE_ATTENDUE if image is None else image
    codes_par_classe = (CODES_PAR_CLASSE if codes_par_classe is None
                        else codes_par_classe)
    errs: list[str] = []
    explicites = {v for etats in partition.values() for v in etats}
    for etat in sorted(explicites - set(image)):
        errs.append(f"ASP-CI-9 : ancre incohérente — l'état `{etat}` est classé "
                    "par la partition mais n'a AUCUNE image canonique.")
    for etat in sorted(set(image) - explicites):
        errs.append(f"ASP-CI-9 : ancre incohérente — l'état `{etat}` reçoit une "
                    "image canonique mais n'appartient à AUCUNE classe "
                    "explicite de la partition.")
    for cls, etats in sorted(partition.items()):
        admis = codes_par_classe.get(cls, set())
        for etat in sorted(etats):
            code = image.get(etat)
            if code is not None and code not in admis:
                errs.append(f"ASP-CI-9 : ancre incohérente — `{etat}` est en "
                            f"classe {cls} mais porte l'image `{code}`, qui "
                            f"n'appartient pas aux codes de cette classe "
                            f"({sorted(admis)}). Un DÉPLACEMENT d'état à image "
                            "inchangée est ainsi rendu détectable.")
    return errs


def bloc_etats(t08: str) -> str:
    try:
        return t08.split("## 1. États canoniques", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        return ""


# M-1 — chaque compteur est ancré sur SA clause normative, jamais sur une
# recherche globale de « dix » : une occurrence leurre ailleurs dans le même
# chapitre ne doit satisfaire aucune de ces gardes.
COMPTEURS_ANCRES = (
    ("08", "08 §1, phrase d'ouverture",
     re.compile(r'^Le domaine distingue \*\*dix\*\* situations', re.M)),
    ("08", "08, déclaration `ASP-INV-44`",
     re.compile(r'\*\*`ASP-INV-44`\*\* — Ces dix états sont')),
    ("11", "11 §3, point 3",
     re.compile(r'Restituer les états canoniques distinctement\*\* — les '
                r'\*\*dix\*\* du')),
    ("12", "12 §2.3, rôle `‹etat_canonique›`",
     re.compile(r"^\| `‹etat_canonique›` \|[^\n]*parmi les \*\*dix\*\*", re.M)),
)
# Admissibilité de `repos_hors_base` : la clause vit DANS sa ligne de tableau.
LIGNE_REPOS = re.compile(
    r'^\| \*\*[^*|\n]+\*\* \| `repos_hors_base` \|([^\n]*)$', re.M)
MOTIF_ADMISSIBLE = "**repos admissible au lancement**"


def check_etats_canoniques(t08: str, t11: str, t12: str) -> list[str]:
    errs: list[str] = coherence_ancres()
    bloc = bloc_etats(t08)
    if not bloc:
        return errs + ["ASP-CI-9 : modèle d'états canoniques introuvable "
                       "(08 §1)."]

    codes = [c for _, c in ETAT_CANON.findall(bloc)]
    if len(codes) != len(set(codes)):
        doublons = sorted({c for c in codes if codes.count(c) > 1})
        errs.append(f"ASP-CI-9 : code(s) canonique(s) en doublon : "
                    f"{', '.join(doublons)} — aucun synonyme n'est admis.")
    attendus, reels = set(ETATS_CANONIQUES), set(codes)
    for c in sorted(attendus - reels):
        errs.append(f"ASP-CI-9 : état canonique `{c}` ABSENT du chapitre 08 §1.")
    for c in sorted(reels - attendus):
        errs.append(f"ASP-CI-9 : état canonique `{c}` AJOUTÉ — le vocabulaire "
                    f"est clos à {len(ETATS_CANONIQUES)} codes (ASP-INV-44).")
    if errs:
        return errs

    # ---- Image partition -> code canonique -------------------------------
    image: dict[str, str] = {}
    for _, valeurs, code in IMAGE_CANON.findall(bloc):
        for etat in ETAT.findall(valeurs):
            image[etat] = code
    for etat, attendu in sorted(IMAGE_ATTENDUE.items()):
        if etat not in image:
            errs.append(f"ASP-CI-9 : l'état machine `{etat}` n'a AUCUNE image "
                        "canonique — le modèle n'est plus total (ASP-INV-68).")
        elif image[etat] != attendu:
            errs.append(f"ASP-CI-9 : `{etat}` projeté sur `{image[etat]}` ; "
                        f"attendu `{attendu}`.")
    for etat in sorted(set(image) - set(IMAGE_ATTENDUE)):
        errs.append(f"ASP-CI-9 : l'état machine `{etat}` est projeté alors "
                    "qu'il n'appartient pas à la partition attestée.")
    if ETAT_ORTHOGONAL in image.values():
        errs.append(f"ASP-CI-9 : `{ETAT_ORTHOGONAL}` reçoit une image depuis "
                    "l'état machine — il dérive du TÉMOIN DE SESSION et se "
                    "superpose aux autres, il ne les exclut pas (08 §3).")

    # ---- Classe N -> etat_non_qualifie -> refus ETAT_NON_QUALIFIE --------
    ligne_n = [c for cls, _, c in IMAGE_CANON.findall(bloc) if cls == "N"]
    if not ligne_n:
        errs.append("ASP-CI-9 : la classe N n'a aucune image canonique.")
    elif ligne_n[0] != CODE_CANONIQUE_CLASSE_N:
        errs.append(f"ASP-CI-9 : la classe N est projetée sur `{ligne_n[0]}` ; "
                    f"attendu `{CODE_CANONIQUE_CLASSE_N}`.")
    if CODE_ETAT_NON_QUALIFIE not in bloc:
        errs.append(f"ASP-CI-9 : le chapitre 08 §1 ne relie pas "
                    f"`{CODE_CANONIQUE_CLASSE_N}` au refus "
                    f"`{CODE_ETAT_NON_QUALIFIE}` — l'état est nommé sans être "
                    "opposable au lancement.")
    for confusion in ("ROBOT_INDISPONIBLE", "ERREUR_EQUIPEMENT"):
        if confusion not in bloc:
            errs.append(f"ASP-CI-9 : le chapitre 08 §1 ne distingue pas "
                        f"`{CODE_CANONIQUE_CLASSE_N}` de `{confusion}` — la "
                        "confusion produirait un diagnostic faux (ASP-INV-60).")
    # ---- M-1 : admissibilité ancrée sur la LIGNE de `repos_hors_base` ----
    lignes_repos = LIGNE_REPOS.findall(bloc)
    if not lignes_repos:
        errs.append("ASP-CI-9 : ligne canonique de `repos_hors_base` "
                    "introuvable (08 §1).")
    elif not any(MOTIF_ADMISSIBLE in l for l in lignes_repos):
        errs.append("ASP-CI-9 : `repos_hors_base` n'est plus déclaré "
                    f"{MOTIF_ADMISSIBLE} DANS SA LIGNE canonique — la classe R "
                    "perd son image, et le lancement après transport n'est plus "
                    "acquis (ARB-1). Une occurrence d'« admissible » ailleurs "
                    "dans le chapitre ne vaut pas cette clause.")

    # ---- M-1 : compteurs ancrés sur leur clause normative ----------------
    sources = {"08": t08, "11": t11, "12": t12}
    for nom, ou, motif in COMPTEURS_ANCRES:
        if not motif.search(sources[nom]):
            errs.append(f"ASP-CI-9 : compteur d'états FAUX ou absent — {ou} "
                        "n'annonce plus DIX états canoniques. Une autre "
                        "occurrence de « dix » dans le même chapitre ne "
                        "satisfait pas cette garde.")
    for nom, texte in sources.items():
        if "huit états" in texte or "les huit du" in texte:
            errs.append(f"ASP-CI-9 : le chapitre {nom} compte encore HUIT états "
                        "— renvoi non réaligné.")
    return errs


# ─────────────────────────────────────────────────────────────
# ASP-CI-10 — fenêtres temporelles contractuelles (07 §3.1)
# ─────────────────────────────────────────────────────────────

FENETRE = re.compile(
    r'^> \| \*\*([^*|\n]+)\*\* \| \*\*(\d+) s\*\* \| ([^|\n]+) \|', re.M)
# R1 — `[^\S\n]` et non `\s` : une classe d'espaces incluant `\n` ferait
# d'un nombre en fin de ligne suivi d'un `s` en tête de la suivante une fausse
# durée, et lierait deux clauses distinctes.
DUREE = re.compile(r'(\d+)[^\S\n]*(?:s\b|secondes?\b)')
# Les numéros d'étape se lisent DANS une mention « étape(s) … », jamais par
# sous-chaîne : `ASP-INV-38` contient un « 8 » qui n'est pas une étape.
ETAPES_CITEES = re.compile(
    r'étapes?[^\S\n]+(\d+(?:(?:,|[^\S\n]+et)[^\S\n]*\d+)*)')


def etapes_citees(cellule: str) -> set[str]:
    return {n for groupe in ETAPES_CITEES.findall(cellule)
            for n in re.findall(r'\d+', groupe)}


# M-3 — SEULE exemption au balayage des durées : l'observation terrain du
# désalignement du témoin de session (08 §3). Ce n'est PAS une allowlist de
# nombres : c'est la clause elle-même, littérale, qui est retirée du balayage.
# Altérée, elle cesse d'être reconnue et ses durées redeviennent concurrentes ;
# supprimée, son absence est signalée.
CLAUSE_TERRAIN_08 = ("témoin **sous-inclusif** (53 s puis 25 s de déplacement "
                     "à `off`, deux fois)")
FICHIER_TERRAIN_08 = "08_etats_et_observation.md"

# m-1 — l'association 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE est ancrée
# sur la LIGNE du catalogue, pas sur une co-présence de chaînes dans le fichier.
LIGNE_ECHEC = re.compile(r'^\| `([A-Z][A-Z_]{4,})` \|([^\n]*)$', re.M)
NOTE_FENETRE_09 = ("**La fenêtre d'observation de `TRANSITION_NON_OBSERVEE` "
                   "est de 60 s**")


def bloc_fenetres(t07: str) -> str:
    return section_normative(t07, "### 3.1")


def check_fenetres(textes: dict[str, str]) -> list[str]:
    t07 = textes.get("07_moteur_de_mission.md", "")
    t09 = textes.get("09_refus_et_diagnostics.md", "")
    t12 = textes.get("12_identifiants_a_fournir.md", "")
    t13 = textes.get("13_hors_perimetre_arbitrages_et_questions_ouvertes.md", "")
    errs: list[str] = []
    bloc = bloc_fenetres(t07)
    if not bloc:
        return ["ASP-CI-10 : constantes temporelles introuvables (07 §3.1) — "
                "la séquence n'a plus de borne opposable."]

    lignes = FENETRE.findall(bloc)
    valeurs = [int(v) for _, v, _ in lignes]
    if sorted(valeurs) != sorted((FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S)):
        return errs + [f"ASP-CI-10 : fenêtres déclarées {sorted(valeurs)} s ; "
                       f"attendu exactement "
                       f"[{FENETRE_CONFIRMATION_S}, {FENETRE_TRANSITION_S}] s."]

    portees = {int(v): portee for _, v, portee in lignes}
    conf = etapes_citees(portees[FENETRE_CONFIRMATION_S])
    for etape in ETAPES_CONFIRMATION:
        if etape not in conf:
            errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_CONFIRMATION_S} s "
                        f"ne couvre pas l'étape {etape} — une confirmation "
                        "resterait non bornée.")
    trans_cellule = portees[FENETRE_TRANSITION_S]
    if "transition" not in trans_cellule.lower():
        errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_TRANSITION_S} s n'est "
                    "pas affectée à la transition de démarrage.")
    empietement = sorted(etapes_citees(trans_cellule) & set(ETAPES_CONFIRMATION))
    if empietement:
        errs.append(f"ASP-CI-10 : la fenêtre de {FENETRE_TRANSITION_S} s couvre "
                    f"l'étape {', '.join(empietement)} — les deux portées sont "
                    "INVERSÉES ou confondues.")
    if conf & etapes_citees(trans_cellule):
        errs.append("ASP-CI-10 : une même étape relève des deux fenêtres.")

    # ---- Affectation dans la séquence -----------------------------------
    lignes_seq = {e: [l for l in t07.splitlines()
                      if l.startswith(f"| **{e}** |")]
                  for e in ETAPES_CONFIRMATION}
    for etape, trouvees in lignes_seq.items():
        if not trouvees:
            errs.append(f"ASP-CI-10 : l'étape {etape} est ABSENTE de la "
                        "séquence de lancement — une confirmation supprimée "
                        "n'est pas une confirmation bornée.")
        elif not any(f"{FENETRE_CONFIRMATION_S} s" in l for l in trouvees):
            errs.append(f"ASP-CI-10 : l'étape {etape} de la séquence ne "
                        f"porte pas la fenêtre de "
                        f"{FENETRE_CONFIRMATION_S} s.")

    # ---- M-3 : aucune durée concurrente, sur les 14 chapitres ------------
    autorisees = {FENETRE_CONFIRMATION_S, FENETRE_TRANSITION_S}
    terrain = textes.get(FICHIER_TERRAIN_08, "")
    if terrain:
        vues = terrain.count(CLAUSE_TERRAIN_08)
        if vues != 1:
            errs.append(f"ASP-CI-10 : la clause d'observation terrain de "
                        f"{FICHIER_TERRAIN_08} est {'absente' if not vues else 'dupliquée'} "
                        "— l'exemption au balayage des durées n'est plus ancrée "
                        "sur un texte connu, et ses durées ne peuvent plus être "
                        "distinguées d'une durée normative.")
    for nom in sorted(textes):
        corps = textes[nom]
        if nom == FICHIER_TERRAIN_08:
            corps = corps.replace(CLAUSE_TERRAIN_08, "")
        concurrentes = sorted({int(v) for v in DUREE.findall(corps)} - autorisees)
        if concurrentes:
            errs.append(f"ASP-CI-10 : durée(s) concurrente(s) dans {nom} : "
                        f"{concurrentes} s — le domaine n'admet que "
                        f"{sorted(autorisees)} s.")

    # ---- Ni helper temporel, ni fallback, révision conjointe -------------
    minuscule = bloc.lower()
    if "ni helper" not in minuscule:
        errs.append("ASP-CI-10 : 07 §3.1 n'exclut pas explicitement un helper "
                    "temporel — une durée réglable à chaud serait un second "
                    "arbitre de la sûreté.")
    if "aucun fallback" not in minuscule:
        errs.append("ASP-CI-10 : 07 §3.1 n'exclut pas le fallback — une "
                    "échéance atteinte doit refuser ou qualifier un échec.")
    if "Helper temporel" not in t12 or "Aucun" not in t12:
        errs.append("ASP-CI-10 : le chapitre 12 n'acte pas l'absence de helper "
                    "temporel à fournir (ASP-INV-69).")
    try:
        arb3 = t13.split("### `ARB-3`", 1)[1].split("\n### ", 1)[0].lower()
    except IndexError:
        arb3 = ""
    if not arb3:
        errs.append("ASP-CI-10 : arbitrage ARB-3 introuvable (13).")
    elif not all(m in arb3 for m in ("contrat", "checker", "runtime")):
        errs.append("ASP-CI-10 : ARB-3 ne conserve pas la révision CONJOINTE "
                    "contrat + checker + runtime.")
    # ---- m-1 : 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE ---------------
    catalogue = section_normative(t09, "## 3. Catalogue des échecs")
    if not catalogue:
        errs.append("ASP-CI-10 : catalogue des échecs introuvable (09 §3).")
    else:
        fenetre = f"{FENETRE_TRANSITION_S} s"
        lignes = dict(LIGNE_ECHEC.findall(catalogue))
        if CODE_TRANSITION not in lignes:
            errs.append(f"ASP-CI-10 : `{CODE_TRANSITION}` absent du catalogue "
                        "des échecs (09 §3).")
        else:
            ligne = lignes[CODE_TRANSITION]
            if fenetre not in ligne:
                errs.append(f"ASP-CI-10 : la LIGNE de `{CODE_TRANSITION}` ne "
                            f"porte pas la fenêtre de {fenetre} — la seule "
                            "co-présence des deux chaînes dans le chapitre ne "
                            "vaut pas association.")
            if "transition" not in ligne.lower():
                errs.append(f"ASP-CI-10 : la LIGNE de `{CODE_TRANSITION}` ne "
                            "nomme pas la transition de démarrage.")
        egarees = sorted(code for code, ligne in lignes.items()
                         if code != CODE_TRANSITION and fenetre in ligne)
        if egarees:
            errs.append(f"ASP-CI-10 : la fenêtre de {fenetre} est affectée à "
                        f"{', '.join('`' + c + '`' for c in egarees)} — elle ne "
                        f"qualifie QUE `{CODE_TRANSITION}`.")
        if NOTE_FENETRE_09 not in catalogue:
            errs.append(f"ASP-CI-10 : 09 §3 ne relie plus explicitement la "
                        f"fenêtre de {fenetre} à `{CODE_TRANSITION}`.")
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
    # R3 — la neutralisation vaut pour LES DIX contrôles, pas seulement pour
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
        ("ASP-CI-8  référentiel technique",
         check_referentiel_technique(
             textes.get("02_referentiel_cartes_et_pieces.md", ""),
             textes.get("06_integrite_mono_carte.md", ""), audit)),
        ("ASP-CI-9  états canoniques",
         check_etats_canoniques(textes.get("08_etats_et_observation.md", ""),
                                textes.get("11_frontiere_ui.md", ""),
                                textes.get("12_identifiants_a_fournir.md", ""))),
        ("ASP-CI-10 fenêtres temporelles", check_fenetres(textes)),
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
          "(10 contrôles, 0 écart).")
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

    # ---- ASP-CI-8 : référentiel technique --------------------------------
    AUD8 = ("| `0_16` | `Salon` | RDC |\n| `0_18` | `Entrée` | RDC |\n"
            "| `1_16` | `Palier` | Étage |\n"
            "| `2_17` | `Ext` | Annexe |\n| `2_18` | `Chambre1` | Annexe |\n"
            "| **0** | `RDC` | 2 |\n| **1** | `Étage ` | 1 |\n"
            "| **2** | `Annexe` | 3 |\n")

    # Clauses de bornage (M-2), retirables une à une, avec leurre optionnel.
    CL21 = {
        "cardinalite": "> - **Ni une confirmation par cardinalité.** Compter les "
                       "pièces ne confirme rien : inclusion nominale exigée.\n",
        "autorite": "> - **Ni une autorité métier.** La vérité de désignation "
                    "reste le §2.\n",
        "ui": "> - **Ni une donnée d'interface.** L'UI expose les libellés "
              "canoniques Arsenal.\n"}
    CL5 = {
        "usages": "| Écrire la sélection de carte | Option exacte | §2.1 |\n"
                  "| Confirmer la sélection par relecture | Option exacte | §2.1 |\n"
                  "| Confirmer les pièces exposées de la carte | Noms | §2.1 |\n",
        "litterale": "elle est stricte : la comparaison est **littérale**, "
                     "jamais approchée.\n"}
    CL6 = {
        "cond3": "| 3 | La sélection est confirmée par relecture, par "
                 "comparaison **littérale** à cette option | `X` |\n",
        "cond4": "| 4 | Les pièces exposées **contiennent l'intégralité** des "
                 "segments V1 (§2, §2.1) — voir §3.1 | `X` |\n",
        "inclusion": "> **Comment l'inclusion se constate.** Confrontation aux "
                     "noms de §2.1 — comparaison **littérale**.\n"}

    def t02t(opt1="`Étage `", nom="`Salon`", idx="16", statut17="non commandable",
             garage="| — | `Garage` | non commandable |", metier_extra="",
             tech_extra="", metier_roboro="`Salon`", retirer=(), leurre=False):
        metier = ("## 2. Table canonique des segments\n"
                  f"| `0_16` | **Séjour** | {metier_roboro} |\n"
                  "| `0_18` | **Entrée** | — |\n"
                  "| `1_16` | **Palier** | — |\n") + metier_extra
        b21 = "".join(v for k, v in CL21.items() if k not in retirer)
        b5 = "".join(v for k, v in CL5.items() if k not in retirer)
        # Leurre : la clause retirée reparaît dans une SECTION NON NORMATIVE.
        renvois = "## Renvois\n" + ("".join(CL21.get(k, "") + CL5.get(k, "")
                                            for k in retirer) if leurre else "")
        return (metier +
                "### 2.1 Table technique\n"
                "| `0` | `RDC` | commandable |\n"
                f"| `1` | {opt1} | commandable |\n"
                "| `2` | `Annexe` | commandable |\n"
                f"{garage}\n"
                f"| `0_16` | `{idx}` | {nom} | commandable |\n"
                "| `0_18` | `18` | `Entrée` | commandable |\n"
                "| `1_16` | `16` | `Palier` | commandable |\n"
                f"| `2_17` | `17` | `Ext` | {statut17} |\n"
                "| `2_18` | `18` | `Chambre1` | non commandable |\n"
                f"{tech_extra}{b21}"
                "\n## 3. Périmètres\n"
                "\n## 5. Règle de restitution des libellés\n" + b5 +
                "\n" + renvois)

    def t06t(retirer=(), leurre=False):
        c3 = "".join(v for k, v in CL6.items()
                     if k in ("cond3", "cond4") and k not in retirer)
        inc = CL6["inclusion"] if "inclusion" not in retirer else ""
        renvois = "## Renvois\n" + ("".join(CL6.get(k, "") for k in retirer)
                                    if leurre else "")
        return ("## 3. Conditions de satisfaction — dans cet ordre\n" + c3 +
                "\n### 3.1 La condition 4 est une inclusion\n" + inc +
                "\n## 4. Suite\n\n" + renvois)

    c.conforme(check_referentiel_technique(t02t(), t06t(), AUD8), "CI-8 conforme")
    c.viole(check_referentiel_technique(t02t(opt1="`Étage`"), t06t(), AUD8),
            "LITTÉRALE", "CI-8 espace finale supprimée")
    c.viole(check_referentiel_technique(t02t(nom="`Sallon`"), t06t(), AUD8),
            "l'audit atteste", "CI-8 nom Roborock falsifié")
    c.viole(check_referentiel_technique(t02t(idx="17"), t06t(), AUD8),
            "index natif", "CI-8 index natif dérivé")
    c.viole(check_referentiel_technique(t02t(statut17="commandable"), t06t(), AUD8),
            "attendu `non commandable`", "CI-8 promotion de 2_17")
    c.viole(check_referentiel_technique(
        t02t(metier_extra="| `2_17` | **Extérieur** | — |\n"), t06t(), AUD8),
        "promu(s) au référentiel métier", "CI-8 2_17 promu côté métier")
    c.viole(check_referentiel_technique(
        t02t(garage="| `3` | `Garage` | non commandable |"), t06t(), AUD8),
        "porte un index", "CI-8 Garage rendu adressable")
    c.viole(check_referentiel_technique(t02t(garage=""), t06t(), AUD8),
            "non commandable", "CI-8 Garage absent")
    # Falsification COHÉRENTE : les deux tables internes mentent ENSEMBLE.
    c.viole(check_referentiel_technique(
        t02t(nom="`Sallon`", metier_roboro="`Sallon`"), t06t(), AUD8),
        "l'audit atteste", "CI-8 falsification cohérente des deux tables")
    c.viole(check_referentiel_technique(
        t02t(tech_extra="| `0_99` | `99` | `Cuisine` | commandable |\n"),
        t06t(), AUD8),
        "ABSENT de l'audit", "CI-8 segment inventé")
    c.viole(check_referentiel_technique(t02t(), t06t(), ""),
            "introuvable dans l'audit", "CI-8 audit absent")
    c.viole(check_referentiel_technique("## 2. Table\n| `0_16` | **Séjour** |\n",
                                        t06t(), AUD8),
            "introuvable", "CI-8 §2.1 absent")
    # Séparation MÉCANIQUE : une table technique au format métier est refusée.
    c.viole(check_referentiel_technique(
        t02t().replace("| `0_16` | `16` | `Salon` | commandable |",
                       "| `0_16` | **Salon** | `16` |"), t06t(), AUD8),
        "parseur du référentiel MÉTIER", "CI-8 séparation typographique seule")

    # ---- M-2 : bornage de l'exception cartographique, clause par clause ---
    for cle, libelle in (("cardinalite", "confirmation par cardinalité"),
                         ("autorite", "autorité métier"),
                         ("ui", "donnée d'interface"),
                         ("usages", "table des trois usages"),
                         ("litterale", "comparaison littérale (02 §5)")):
        c.viole(check_referentiel_technique(t02t(retirer=(cle,)), t06t(), AUD8),
                "clause de bornage absente", f"M-2 {libelle} supprimée")
        # LEURRE : la clause reparaît dans « ## Renvois » — non normatif.
        c.viole(check_referentiel_technique(
            t02t(retirer=(cle,), leurre=True), t06t(), AUD8),
            "DANS cette section", f"M-2 {libelle} déplacée en renvoi")
    for cle, libelle in (("cond3", "condition 3 littérale"),
                         ("cond4", "condition 4 fondée sur §2.1"),
                         ("inclusion", "mécanisme d'inclusion nominale")):
        c.viole(check_referentiel_technique(t02t(), t06t(retirer=(cle,)), AUD8),
                "clause de bornage absente", f"M-2 {libelle} supprimée")
        c.viole(check_referentiel_technique(
            t02t(), t06t(retirer=(cle,), leurre=True), AUD8),
            "DANS cette section", f"M-2 {libelle} déplacée en renvoi")

    # ---- i-2 : cohérence PARTITION_ATTENDUE ↔ IMAGE_ATTENDUE -------------
    c.conforme(coherence_ancres(), "i-2 ancres cohérentes")
    c.viole(coherence_ancres(
        partition={**PARTITION_ATTENDUE, "R": PARTITION_ATTENDUE["R"] | {"idle"}}),
        "n'a AUCUNE image", "i-2 état ajouté à la partition sans image")
    c.viole(coherence_ancres(image={**IMAGE_ATTENDUE, "idle": "charge"}),
            "AUCUNE classe", "i-2 image sans appartenance à la partition")
    c.viole(coherence_ancres(partition={
        "R": PARTITION_ATTENDUE["R"] - {"charging"},
        "A": PARTITION_ATTENDUE["A"] | {"charging"},
        "E": PARTITION_ATTENDUE["E"]}),
        "DÉPLACEMENT", "i-2 état déplacé entre classes à image inchangée")

    # ---- ASP-CI-9 : dix états canoniques ---------------------------------
    def t08e(codes=None, image=None, extra="", refus="ETAT_NON_QUALIFIE",
             distinctions="ROBOT_INDISPONIBLE / ERREUR_EQUIPEMENT",
             admis="**repos admissible au lancement**", ouverture=True,
             inv44=True, leurre=""):
        codes = codes or list(ETATS_CANONIQUES)
        image = image or dict(IMAGE_ATTENDUE)
        lignes = "".join(
            f"| **{code}** | `{code}` | "
            + (f"sens {admis}" if code == "repos_hors_base" else "sens")
            + " |\n" for code in codes)
        par_code: dict[str, list[str]] = {}
        for etat, code in image.items():
            par_code.setdefault(code, []).append(etat)
        img = "".join(
            f"> | **A** | {' · '.join(f'`{e}`' for e in etats)} | `{code}` |\n"
            for code, etats in par_code.items())
        img += f"> | **N** | toute autre valeur | `{CODE_CANONIQUE_CLASSE_N}` |\n"
        tete = ("Le domaine distingue **dix** situations, qui ne se confondent "
                "jamais :\n" if ouverture else "Le domaine distingue plusieurs "
                "situations :\n")
        decl = ("> **`ASP-INV-44`** — Ces dix états sont **exposés "
                "distinctement**.\n" if inv44 else
                "> **`ASP-INV-44`** — Ces états sont **exposés distinctement**.\n")
        return ("## 1. États canoniques du domaine\n" + tete + lignes + extra
                + img + decl + leurre
                + f"refus {refus} ; ni {distinctions}\n" + "\n## 2. Autorité\n")

    t11e = ("3. **Restituer les états canoniques distinctement** — les **dix** "
            "du chapitre 08.\n")
    t12e = ("| `‹etat_canonique›` | L'état du domaine parmi les **dix** du "
            "chapitre 08 |\n")
    c.conforme(check_etats_canoniques(t08e(), t11e, t12e), "CI-9 conforme")
    c.viole(check_etats_canoniques(
        t08e(codes=[x for x in ETATS_CANONIQUES if x != "repos_hors_base"]),
        t11e, t12e), "ABSENT", "CI-9 état canonique retiré")
    c.viole(check_etats_canoniques(t08e(extra="| **Onzième** | `onzieme` | s |\n"),
                                   t11e, t12e),
            "AJOUTÉ", "CI-9 onzième état")
    c.viole(check_etats_canoniques(
        t08e(extra="| **Repos** | `repos_hors_base` | doublon |\n"), t11e, t12e),
        "doublon", "CI-9 synonyme")
    c.viole(check_etats_canoniques(
        t08e(image={**IMAGE_ATTENDUE, "charger_disconnected": "charge"}),
        t11e, t12e), "attendu `repos_hors_base`", "CI-9 image charger_disconnected")
    c.viole(check_etats_canoniques(
        t08e().replace(f"| **N** | toute autre valeur | `{CODE_CANONIQUE_CLASSE_N}` |",
                       "| **N** | toute autre valeur | `indisponibilite` |"),
        t11e, t12e), "classe N", "CI-9 classe N détournée")
    c.viole(check_etats_canoniques(t08e(refus="néant"), t11e, t12e),
            "ne relie pas", "CI-9 lien refus rompu")
    c.viole(check_etats_canoniques(t08e(distinctions="rien"), t11e, t12e),
            "ne distingue pas", "CI-9 confusion indisponibilité")
    c.viole(check_etats_canoniques("", t11e, t12e),
            "introuvable", "CI-9 chapitre absent")

    # ---- M-1 : compteurs et admissibilité ancrés, LEURRES compris ---------
    LEURRE_DIX = "Par ailleurs, dix segments sont observés, dont un admissible.\n"
    c.viole(check_etats_canoniques(t08e(ouverture=False), t11e, t12e),
            "phrase d'ouverture", "M-1 compteur 08 (ouverture) faux")
    c.viole(check_etats_canoniques(
        t08e(ouverture=False, leurre=LEURRE_DIX), t11e, t12e),
        "phrase d'ouverture", "M-1 compteur 08 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(inv44=False), t11e, t12e),
            "ASP-INV-44", "M-1 compteur 08 (ASP-INV-44) faux")
    c.viole(check_etats_canoniques(
        t08e(inv44=False, leurre=LEURRE_DIX), t11e, t12e),
        "ASP-INV-44", "M-1 ASP-INV-44 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(), "les états, au nombre de dix.\n", t12e),
            "11 §3", "M-1 compteur 11 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(), t11e, "un rôle parmi dix autres |\n"),
            "12 §2.3", "M-1 compteur 12 faux malgré un leurre « dix »")
    c.viole(check_etats_canoniques(t08e(admis="sens ordinaire"), t11e, t12e),
            "DANS SA LIGNE", "M-1 admissibilité perdue")
    c.viole(check_etats_canoniques(
        t08e(admis="sens ordinaire", leurre=LEURRE_DIX), t11e, t12e),
        "DANS SA LIGNE", "M-1 admissibilité perdue malgré un leurre « admissible »")
    c.viole(check_etats_canoniques(t08e(), "les huit du chapitre", t12e),
            "HUIT", "CI-9 renvoi 11 non réaligné")
    c.viole(check_etats_canoniques(t08e(), t11e, "les dix — jadis huit états"),
            "HUIT", "CI-9 renvoi 12 non réaligné")

    # ---- ASP-CI-10 : fenêtres temporelles --------------------------------
    def t07f(conf=30, trans=60, portee_conf="étapes 6, 8 et 10",
             portee_trans="transition de démarrage — étape 13",
             helper="ni helper", fallback="aucun fallback", seq=True):
        etapes = "".join(
            f"| **{e}** | Confirmer, sous **{conf} s** | refus |\n"
            for e in ETAPES_CONFIRMATION) if seq else ""
        return (etapes + "### 3.1 Constantes\n"
                f"> | **Fenêtre de confirmation** | **{conf} s** | {portee_conf} |\n"
                f"> | **Fenêtre de transition** | **{trans} s** | {portee_trans} |\n"
                f"> {helper} ; {fallback}\n\n## 4. Suite\n")

    def t09f(fenetre_sur=CODE_TRANSITION, note=True):
        lignes = {
            "CANAL_INDISPONIBLE": "La demande n'est pas parvenue",
            "COMMANDE_REJETEE": "La commande a été refusée",
            CODE_TRANSITION: "aucune transition de démarrage observée",
            "MISSION_INTERROMPUE": "arrêt avant terme"}
        corps = "".join(
            f"| `{code}` | {texte}"
            + (" dans la fenêtre de **60 s**" if code == fenetre_sur else "")
            + " | — |\n" for code, texte in lignes.items())
        # Les deux chaînes restent présentes AILLEURS dans le chapitre :
        # seule leur ASSOCIATION sur la ligne fait foi (m-1).
        queue = ("> Rappel : la transition de démarrage et la fenêtre de 60 s "
                 "sont traitées au chapitre 07.\n")
        if note:
            queue += f"> {NOTE_FENETRE_09}, et 30 s pour les réglages.\n"
        return "## 3. Catalogue des échecs\n" + corps + queue + "\n## 4. Qualité\n"

    t12f = "| **Helper temporel** | **Aucun.** |"
    t13f = ("### `ARB-3` — fenêtres\nrévision conjointe contrat + checker + "
            "runtime\n### `ARB-4`\n")
    T08F = ("## 3. Témoin\n| Robot roulant | `off` | Le robot se déplace — "
            + CLAUSE_TERRAIN_08 + " |\n")

    def corpus(t07=None, t09=None, t12=t12f, t13=t13f, t08=T08F, **autres):
        base = {"07_moteur_de_mission.md": t07 if t07 is not None else t07f(),
                "09_refus_et_diagnostics.md": t09 if t09 is not None else t09f(),
                "12_identifiants_a_fournir.md": t12,
                "13_hors_perimetre_arbitrages_et_questions_ouvertes.md": t13,
                FICHIER_TERRAIN_08: t08}
        base.update(autres)
        return base

    c.conforme(check_fenetres(corpus()), "CI-10 conforme")
    # Inversion PURE : l'ensemble des valeurs reste {30, 60}, seule
    # l'affectation ment. C'est le contrôle de PORTÉE qui la lève.
    c.viole(check_fenetres(corpus(t07=t07f(conf=60, trans=30))),
            "INVERSÉES ou confondues", "CI-10 inversion 30/60")
    c.viole(check_fenetres(corpus(
        t07=t07f(portee_trans="transition — étapes 8 et 13"))),
        "INVERSÉES ou confondues", "CI-10 portées confondues")
    c.viole(check_fenetres(corpus(t07=t07f(trans=45))),
            "attendu exactement", "CI-10 disparition d'une fenêtre")
    c.viole(check_fenetres(corpus(t07=t07f(helper="réglable par input_number"))),
            "helper", "CI-10 helper temporel réintroduit")
    c.viole(check_fenetres(corpus(t07=t07f(fallback="repli admis"))),
            "fallback", "CI-10 fallback ajouté")
    c.viole(check_fenetres(corpus(t12="aucune ligne")),
            "chapitre 12", "CI-10 helper non acté au 12")
    c.viole(check_fenetres(corpus(
        t13="### `ARB-3` — fenêtres\nrévisable à chaud\n### `ARB-4`\n")),
        "CONJOINTE", "CI-10 révision conjointe perdue")
    c.viole(check_fenetres(corpus(t07=t07f(portee_conf="étapes 6 et 8"))),
            "étape 10", "CI-10 étape de confirmation non bornée")
    c.viole(check_fenetres(corpus(t07=t07f(seq=False))),
            "ABSENTE de la séquence", "CI-10 étape de confirmation supprimée")
    c.viole(check_fenetres(corpus(t07=t07f().replace(
        "| **8** | Confirmer, sous **30 s** | refus |",
        "| **8** | Confirmer | refus |"))),
        "ne porte pas la fenêtre", "CI-10 étape non bornée")
    c.viole(check_fenetres(corpus(t07="")),
            "introuvables", "CI-10 §3.1 absent")

    # ---- m-1 : association 60 s ↔ transition ↔ TRANSITION_NON_OBSERVEE ----
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur="COMMANDE_REJETEE"))),
            "ne porte pas la fenêtre",
            "m-1 fenêtre déplacée sur COMMANDE_REJETEE")
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur="COMMANDE_REJETEE"))),
            "elle ne qualifie QUE", "m-1 fenêtre affectée à un autre code")
    c.viole(check_fenetres(corpus(t09=t09f(note=False))),
            "ne relie plus explicitement", "m-1 note d'association supprimée")
    c.viole(check_fenetres(corpus(t09="## 4. Qualité\n")),
            "catalogue des échecs introuvable", "m-1 catalogue absent")

    # ---- M-3 : balayage des 14 chapitres, exemption bornée ---------------
    for chapitre in ("01_finalite_et_perimetre.md",
                     "02_referentiel_cartes_et_pieces.md",
                     "06_integrite_mono_carte.md",
                     "11_frontiere_ui.md",
                     "12_identifiants_a_fournir.md"):
        c.viole(check_fenetres(corpus(**{chapitre: "temporisation de 90 s.\n"})),
                "durée(s) concurrente(s)", f"M-3 durée concurrente dans {chapitre[:2]}")
    c.viole(check_fenetres(corpus(t08=T08F + "attente de 15 s avant relecture.\n")),
            "durée(s) concurrente(s)", "M-3 durée concurrente dans 08")
    c.viole(check_fenetres(corpus(t12=t12f + "\nrepli à 120 secondes.\n")),
            "durée(s) concurrente(s)", "M-3 durée concurrente dans 12 (en toutes lettres)")
    # La clause terrain 53 s / 25 s n'est PAS une allowlist de nombres :
    # altérée, elle cesse d'être reconnue et ses durées redeviennent visibles.
    c.viole(check_fenetres(corpus(t08=T08F.replace("53 s puis 25 s", "53 s ou 25 s"))),
            "durée(s) concurrente(s)", "M-3 clause terrain altérée")
    c.viole(check_fenetres(corpus(t08=T08F.replace("53 s puis 25 s", "53 s ou 25 s"))),
            "n'est plus ancrée", "M-3 exemption désancrée")
    c.viole(check_fenetres(corpus(t08="## 3. Témoin\naucune observation.\n")),
            "est absente", "M-3 clause terrain supprimée")

    # ---- Franchissement de ligne et de section — aucun motif ne déborde ---
    # LIGNE_REPOS est ancrée par `$` en mode M : le motif placé à la ligne
    # SUIVANTE, ou ailleurs dans le chapitre, ne satisfait pas la garde.
    c.viole(check_etats_canoniques(
        t08e(admis="sens ordinaire", leurre=MOTIF_ADMISSIBLE + "\n"), t11e, t12e),
        "DANS SA LIGNE", "franchissement — admissibilité hors de sa ligne")
    # Le motif du chapitre 12 ne se satisfait pas d'une répartition sur 2 lignes.
    c.viole(check_etats_canoniques(
        t08e(), t11e,
        "| `‹etat_canonique›` | L'état du domaine\nparmi les **dix** du 08 |\n"),
        "12 §2.3", "franchissement — motif 12 réparti sur deux lignes")
    # Une clause du §5 déplacée DANS le §2.1 ne satisfait pas la garde du §5.
    c.viole(check_referentiel_technique(
        t02t(retirer=("litterale",)).replace(
            "\n## 3. Périmètres\n", CL5["litterale"] + "\n## 3. Périmètres\n"),
        t06t(), AUD8),
        "02 §5", "franchissement — clause du §5 déplacée dans le §2.1")
    # Une clause du 06 §3.1 remontée dans le §3 ne satisfait pas la garde du §3.1.
    c.viole(check_referentiel_technique(
        t02t(), t06t(retirer=("inclusion",)).replace(
            "\n### 3.1", CL6["inclusion"] + "\n### 3.1"), AUD8),
        "06 §3.1", "franchissement — clause du §3.1 remontée dans le §3")

    # ---- m-1 : l'association ne franchit pas la ligne --------------------
    c.viole(check_fenetres(corpus(t09=t09f(fenetre_sur=None))),
            "ne porte pas la fenêtre",
            "m-1 fenêtre à la ligne suivante, hors de la ligne de catalogue")

    # ---- M-3 : blocs clôturés neutralisés, et neutralisation non vacuous --
    FENCE = "```yaml\nwait_template: 90 s\n```\n"
    c.conforme(check_fenetres(corpus(
        **{"01_finalite_et_perimetre.md": strip_fences(FENCE)})),
        "M-3 durée dans un bloc clôturé — neutralisée")
    c.viole(check_fenetres(corpus(
        **{"01_finalite_et_perimetre.md": "wait_template: 90 s\n"})),
        "durée(s) concurrente(s)",
        "M-3 même durée HORS bloc — détectée (neutralisation non vacante)")
    # Une durée ajoutée SUR LA LIGNE de la clause terrain reste visible :
    # l'exemption retire la clause exacte, pas la ligne ni son voisinage.
    c.viole(check_fenetres(corpus(
        t08=T08F.replace(CLAUSE_TERRAIN_08, CLAUSE_TERRAIN_08 + ", puis 15 s"))),
        "durée(s) concurrente(s)",
        "M-3 durée ajoutée à côté des observations 53 s / 25 s")

    # R1 — les motifs de durée et d'étape ne franchissent pas la ligne.
    assert not DUREE.search("90\ns"), "DUREE franchit la ligne"
    assert DUREE.findall("90 s") == ["90"], "DUREE ne lit plus une durée"
    assert not ETAPES_CITEES.search("étape\n6"), "ETAPES_CITEES franchit la ligne"
    assert etapes_citees("étapes 6, 8 et 10") == {"6", "8", "10"}
    assert etapes_citees("étape 13 (§4, `ASP-INV-38`)") == {"13"}, \
        "un chiffre hors mention d'étape ne doit pas être lu comme une étape"
    c.conforme([], "R1 motifs bornés à la ligne (5 assertions)")

    # ---- i-2 : retrait d'un état de l'image canonique --------------------
    c.viole(coherence_ancres(
        image={k: v for k, v in IMAGE_ATTENDUE.items() if k != "docking"}),
        "AUCUNE image", "i-2 état retiré de l'image canonique")

    print(f"selftest OK — 10 contrôles, {c.total()} cas "
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
