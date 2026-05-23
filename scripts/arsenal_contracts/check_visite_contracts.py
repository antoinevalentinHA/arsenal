#!/usr/bin/env python3

# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
# Domaine : Présence / Visite
# Vérification des invariants structurels
# ==========================================================

from pathlib import Path
import sys


ROOT = Path(".")
ERRORS = []


VISITE_WRITER_IDS = {
    "10210000000003",
    "10210000000004",
    "10210000000005",
}

UI_NOTIFICATION_ID = "10210000000006"

STATE_TARGETS = [
    "input_boolean.visite_en_cours",
    "input_boolean.presence_visiteur",
]

ALLOWED_TEMPORAL_FILE = Path("12_template_sensors/presence/visite.yaml")

TEMPORAL_LOGIC_TERMS = [
    "today_at",
    "weekday",
    "timestamp_custom",
    "as_datetime",
]

FORBIDDEN_ENERGY_SERVICES = [
    "switch.turn_on",
    "switch.turn_off",
    "climate.set_temperature",
    "climate.set_hvac_mode",
    "water_heater.set_operation_mode",
    "water_heater.set_temperature",
    "number.set_value",
]


def fail(message: str):
    ERRORS.append(message)


def yaml_files():
    for path in ROOT.rglob("*.yaml"):
        if path.is_file():
            yield path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ==========================================================
# TEST 1 — Entités canoniques présentes
# ==========================================================

all_yaml = "\n".join(read(path) for path in yaml_files())

required_entities = [
    "input_boolean.mode_visiteur",
    "input_boolean.visite_en_cours",
    "input_boolean.presence_visiteur",
    "binary_sensor.creneau_visiteur_actif",
    "input_boolean.systeme_stable",
]

for entity in required_entities:
    if entity not in all_yaml:
        fail(f"Entité canonique Visite introuvable : {entity}")

print("✔ Entités canoniques Visite présentes")


# ==========================================================
# TEST 2 — Écriture contrôlée des états métier
# ==========================================================

for path in yaml_files():
    content = read(path)

    if not any(target in content for target in STATE_TARGETS):
        continue

    writes_state = (
        "input_boolean.turn_on" in content
        or "input_boolean.turn_off" in content
        or "service: input_boolean.turn_on" in content
        or "service: input_boolean.turn_off" in content
    )

    if not writes_state:
        continue

    if not any(writer_id in content for writer_id in VISITE_WRITER_IDS):
        fail(
            "Écriture non autorisée des états métier Visite : "
            f"{path}"
        )

print("✔ Écritures Visite contrôlées")


# ==========================================================
# TEST 3 — Notification persistante réservée
# ==========================================================

for path in yaml_files():
    content = read(path)

    if "visiteur_etat" not in content:
        continue

    if UI_NOTIFICATION_ID not in content:
        fail(
            "Manipulation non autorisée de visiteur_etat : "
            f"{path}"
        )

print("✔ Notification persistante Visite réservée")


# ==========================================================
# TEST 4 — Calcul temporel actif centralisé
# ==========================================================

VISITE_TEMPORAL_ENTITIES = [
    "input_datetime.visiteur_start",
    "input_datetime.visiteur_end",
    "input_select.jour_visiteur",
    "binary_sensor.creneau_visiteur_actif",
]

for path in yaml_files():
    content = read(path)

    if not any(entity in content for entity in VISITE_TEMPORAL_ENTITIES):
        continue

    if not any(term in content for term in TEMPORAL_LOGIC_TERMS):
        continue

    if path != ALLOWED_TEMPORAL_FILE:
        fail(
            "Logique temporelle Visite hors capteur canonique : "
            f"{path}"
        )

print("✔ Calcul temporel actif Visite centralisé")


# ==========================================================
# TEST 5 — Isolation énergétique du domaine Visite
# ==========================================================

for path in yaml_files():
    path_str = str(path).lower()

    if not (
        "presence/visite" in path_str
        or "presence/visiteur" in path_str
    ):
        continue

    content = read(path).lower()

    for service in FORBIDDEN_ENERGY_SERVICES:
        if service in content:
            fail(
                "Pilotage énergétique interdit dans le domaine Visite : "
                f"{path} -> '{service}'"
            )

print("✔ Isolation énergétique Visite respectée")


# ==========================================================
# RÉSULTAT
# ==========================================================

if ERRORS:
    print("\n❌ CONTRAT VISITE NON CONFORME\n")

    for error in ERRORS:
        print(f"- {error}")

    sys.exit(1)

print("\n✅ CONTRAT VISITE CONFORME")