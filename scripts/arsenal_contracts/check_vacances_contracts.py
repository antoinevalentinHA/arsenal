#!/usr/bin/env python3

# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
# Domaine : Vacances
# Vérification des invariants structurels
# ==========================================================

from pathlib import Path
import sys


ROOT = Path(".")
ERRORS = []


REQUIRED_ENTITIES = [
    "input_datetime.debut_vacances",
    "input_datetime.fin_vacances",
    "input_boolean.mode_vacances_auto",
    "input_boolean.vacances_demande_manuel",
    "input_boolean.vacances_fenetre_active",
    "binary_sensor.vacances_planifiees_actives",
    "binary_sensor.vacances_demandees",
    "binary_sensor.vacances_actives",
    "sensor.vacances_raison",
    "binary_sensor.parametres_invalides_vacances",
]

REQUIRED_RAISON_STATES = [
    "aucune_demande",
    "presence_indisponible",
    "visite_indisponible",
    "presence_famille",
    "visite_en_cours",
    "vacances_actives",
]

REQUIRED_INVALID_PARAMS_ATTRIBUTES = [
    "debut_indisponible",
    "fin_indisponible",
    "fenetre_inversee",
]

FORBIDDEN_TEMPLATE_TIME_TERMS = [
    "now()",
    "today_at",
]

VACANCES_TEMPLATE_PATHS = [
    Path("12_template_sensors/vacances"),
    Path("12_template_sensors/system/integrite_reglages/vacances.yaml"),
]


def fail(message: str):
    ERRORS.append(message)


def yaml_files():
    for path in ROOT.rglob("*.yaml"):
        if path.is_file():
            yield path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def is_in_vacances_template_scope(path: Path) -> bool:
    return any(
        path == scope or scope in path.parents
        for scope in VACANCES_TEMPLATE_PATHS
    )


# ==========================================================
# TEST 1 — Entités canoniques présentes
# ==========================================================

all_yaml = "\n".join(read(path) for path in yaml_files())

for entity in REQUIRED_ENTITIES:
    if entity not in all_yaml:
        fail(f"Entité canonique Vacances introuvable : {entity}")

print("✔ Entités canoniques Vacances présentes")


# ==========================================================
# TEST 2 — Pas de calcul temporel direct dans les templates
# ==========================================================

for path in yaml_files():
    if not is_in_vacances_template_scope(path):
        continue

    content = read(path)

    for term in FORBIDDEN_TEMPLATE_TIME_TERMS:
        if term in content:
            fail(
                "Calcul temporel direct interdit dans un template Vacances : "
                f"{path} -> '{term}'"
            )

print("✔ Aucun calcul temporel direct interdit dans les templates Vacances")


# ==========================================================
# TEST 3 — vacances_demandees indépendante de mode_maison
# ==========================================================

definition_found = False

for path in yaml_files():

    path_str = str(path)

    if not path_str.startswith("12_template_sensors/"):
        continue

    content = read(path)

    if "binary_sensor.vacances_demandees" not in content:
        continue

    definition_found = True

    if "input_select.mode_maison" in content:
        fail(
            "vacances_demandees dépend de mode_maison : "
            f"{path}"
        )

if not definition_found:
    fail(
        "Définition de binary_sensor.vacances_demandees introuvable"
    )

print("✔ Demande Vacances indépendante de mode_maison")


# ==========================================================
# TEST 4 — Écriture contrôlée de vacances_fenetre_active
# ==========================================================

for path in yaml_files():
    content = read(path)

    if "input_boolean.vacances_fenetre_active" not in content:
        continue

    writes_window = (
        "input_boolean.turn_on" in content
        or "input_boolean.turn_off" in content
        or "service: input_boolean.turn_on" in content
        or "service: input_boolean.turn_off" in content
    )

    if not writes_window:
        continue

    if "Orchestrateur fenêtre planifiée" not in content:
        fail(
            "Écriture de vacances_fenetre_active hors orchestrateur : "
            f"{path}"
        )

print("✔ Écriture de vacances_fenetre_active contrôlée")


# ==========================================================
# TEST 5 — sensor.vacances_raison couvre les états contractuels
# ==========================================================

for state in REQUIRED_RAISON_STATES:
    if state not in all_yaml:
        fail(f"État vacances_raison manquant : {state}")

print("✔ États vacances_raison présents")


# ==========================================================
# TEST 6 — parametres_invalides_vacances complet
# ==========================================================

for attr in REQUIRED_INVALID_PARAMS_ATTRIBUTES:
    if attr not in all_yaml:
        fail(f"Attribut parametres_invalides_vacances manquant : {attr}")

print("✔ Attributs parametres_invalides_vacances présents")


# ==========================================================
# TEST 7 — Agrégat global des paramètres invalides
# ==========================================================

if "binary_sensor.parametres_invalides_vacances" not in all_yaml:
    fail(
        "binary_sensor.parametres_invalides_vacances absent "
        "de l'agrégat ou des templates"
    )

print("✔ Paramètres invalides Vacances référencés")


# ==========================================================
# RÉSULTAT
# ==========================================================

if ERRORS:
    print("\n❌ CONTRAT VACANCES NON CONFORME\n")

    for error in ERRORS:
        print(f"- {error}")

    sys.exit(1)

print("\n✅ CONTRAT VACANCES CONFORME")