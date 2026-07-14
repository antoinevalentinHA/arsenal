"""Oracle structurel de la politique d'absence COOL (contrat climatisation 15).

Statut épistémique : ANALYSEUR STRUCTUREL BORNÉ. Cet oracle vérifie que la
matière YAML (template sensors, helper, automations) **encode** les invariants
opposables du contrat
`00_documentation_arsenal/contrats/climatisation/15_absence_vacances_veto_cool.md`
— il ne simule PAS le rendu Jinja et n'évalue AUCUN état runtime.

Ce qu'il PROUVE (par présence/absence de références, sur un texte donné) :
  - INV-VETO-2 : le veto composite agrège Vacances comme cause directe (OR) ;
  - INV-VETO-3 : la chaîne d'absence n'a plus de durée figée (8 h) ni de timer ;
  - INV-VETO-4 : le helper de durée ne porte pas de clé `initial:` ;
  - INV-VETO-5 : l'extinction est ancrée sur l'horodatage de début d'absence ;
  - INV-VETO-6 : l'autorisation consomme le composite, sans dupliquer sa formule ;
  - INV-VETO-7 : l'horodatage a un écrivain unique, d'ID attendu ;
  - INV-VETO-9 : C20 ne crée aucune préparation (frontière C21).

Ce qu'il NE fait PAS (frontière assumée, jamais masquée) :
  - il n'émule ni Jinja, ni timers, ni ordonnancement HA ;
  - il ne lit pas le runtime réel dans les tests (fixtures inline pré/post) ;
    le branchement contre le VRAI runtime est ajouté au Lot 3, une fois le
    runtime conforme (sinon l'oracle rougirait légitimement avant implémentation).

Chaque fonction retourne une liste de violations (chaînes). Liste vide = conforme.
"""
from __future__ import annotations

import re
from typing import List, Mapping, Sequence

import yaml

# ------------------------------------------------------------ entités canoniques
COMPOSITE = "clim_veto_absence_vacances"
EXTINCTION = "clim_extinction_absence_prolongee_autorisee"
VACANCES = "vacances_actives"
HELPER_DUREE = "clim_duree_absence_longue"
HORODATAGE = "clim_debut_absence"
HORODATAGE_WRITER_ID = "10030000000122"
TIMER = "absence_longue_clim"


class VetoModelError(RuntimeError):
    """Entrée illisible / hors périmètre modélisé (jamais un « vrai » silencieux)."""


# ------------------------------------------------------------ loader tolérant
class _LoaderTolerant(yaml.SafeLoader):
    """SafeLoader tolérant aux tags HA inconnus (!input, !secret, …)."""


def _ignorer_tag_inconnu(loader, node):  # pragma: no cover - trivial
    return None


_LoaderTolerant.add_constructor(None, _ignorer_tag_inconnu)


def load_docs(text: str):
    """Charge un document YAML (liste d'entités template, ou mapping de helpers)."""
    try:
        return yaml.load(text, Loader=_LoaderTolerant)
    except yaml.YAMLError as exc:  # pragma: no cover - garde-fou
        raise VetoModelError(f"YAML illisible : {exc}") from exc


# --------------------------------------------------------- INV-VETO-6 (autorité)

def check_autorisation_consumes_composite(cool_text: str) -> List[str]:
    """L'autorisation COOL lit le composite et NE duplique PAS sa formule."""
    v: List[str] = []
    if COMPOSITE not in cool_text:
        v.append("INV-VETO-6 : autorisation_clim_cool ne consomme pas "
                 f"binary_sensor.{COMPOSITE}")
    if re.search(rf"\b{EXTINCTION}\b", cool_text):
        v.append("INV-VETO-6 : autorisation_clim_cool référence l'extinction en "
                 "direct (duplication du veto composite)")
    if re.search(rf"\b{VACANCES}\b", cool_text):
        v.append("INV-VETO-6 : autorisation_clim_cool référence vacances_actives "
                 "en direct (duplication du veto composite)")
    return v


# ------------------------------------------------- INV-VETO-2 (composite / OR)

def check_composite_formula(veto_text: str) -> List[str]:
    """Le composite agrège extinction OU vacances (Vacances = cause directe)."""
    v: List[str] = []
    if EXTINCTION not in veto_text:
        v.append(f"INV-VETO-2 : {COMPOSITE} ne référence pas l'absence longue "
                 f"({EXTINCTION})")
    if VACANCES not in veto_text:
        v.append(f"INV-VETO-2 : {COMPOSITE} ne référence pas {VACANCES} "
                 "(cause immédiate manquante)")
    if not re.search(r"\bor\b", veto_text):
        v.append("INV-VETO-2 : composite sans disjonction `or` explicite")
    return v


# --------------------------------------- INV-VETO-3 / 5 (ancrage horodaté)

def check_extinction_horodatage(absence_text: str) -> List[str]:
    """L'extinction est ancrée sur horodatage + durée, sans timer figé."""
    v: List[str] = []
    if HORODATAGE not in absence_text:
        v.append(f"INV-VETO-5 : extinction n'ancre pas sur "
                 f"input_datetime.{HORODATAGE}")
    if HELPER_DUREE not in absence_text:
        v.append(f"INV-VETO-3 : extinction ne lit pas le helper "
                 f"input_number.{HELPER_DUREE}")
    if re.search(rf"timer\.{TIMER}\b", absence_text) or f"timer.{TIMER}" in absence_text:
        v.append(f"INV-VETO-3 : extinction lit encore timer.{TIMER} "
                 "(base non horodatée)")
    return v


# ------------------------------------------------- INV-VETO-4 (helper sans initial)

def check_helper_no_initial(helper_text: str) -> List[str]:
    """Le helper de durée ne porte pas `initial:` (doctrine R01)."""
    docs = load_docs(helper_text)
    if not isinstance(docs, Mapping) or HELPER_DUREE not in docs:
        return [f"INV-VETO-4 : helper {HELPER_DUREE} absent du document"]
    block = docs[HELPER_DUREE] or {}
    if isinstance(block, Mapping) and "initial" in block:
        return [f"INV-VETO-4 : {HELPER_DUREE} porte une clé `initial:` "
                "(interdit — désactive la restauration d'état)"]
    return []


# --------------------------------------------- INV-VETO-3 (pas de 8 h figée)

def check_no_fixed_duration(*texts: str) -> List[str]:
    """Aucune durée d'absence figée (08:00:00) dans la chaîne."""
    for t in texts:
        if re.search(r"\b0?8:00:00\b", t):
            return ["INV-VETO-3 : durée figée `08:00:00` détectée dans la chaîne "
                    "d'absence (la source unique est le helper réglable)"]
    return []


# ------------------------------------------- INV-VETO-7 (écrivain unique horodatage)

def check_horodatage_single_writer(automations: Sequence[Mapping]) -> List[str]:
    """Exactement une automation écrit l'horodatage, d'ID attendu."""
    writers: List[str] = []
    for auto in automations or []:
        if not isinstance(auto, Mapping):
            continue
        dumped = yaml.safe_dump(auto, allow_unicode=True, default_flow_style=False)
        writes_datetime = "input_datetime.set_datetime" in dumped
        targets_horodatage = HORODATAGE in dumped
        if writes_datetime and targets_horodatage:
            writers.append(str(auto.get("id")))
    if not writers:
        return [f"INV-VETO-7 : aucun écrivain de input_datetime.{HORODATAGE}"]
    if len(writers) > 1:
        return [f"INV-VETO-7 : écrivains multiples de l'horodatage : {writers}"]
    if writers[0] != HORODATAGE_WRITER_ID:
        return [f"INV-VETO-7 : écrivain d'ID inattendu {writers[0]!r} "
                f"(attendu {HORODATAGE_WRITER_ID})"]
    return []


# ------------------------------------------------- INV-VETO-9 (frontière C21)

def check_no_preparation(*texts: str) -> List[str]:
    """C20 ne crée aucune préparation (celle-ci relève de C21)."""
    for t in texts:
        if "preparation_cool" in t:
            return ["INV-VETO-9 : entité de préparation détectée — hors périmètre "
                    "C20 (la préparation du retour relève de C21)"]
    return []
