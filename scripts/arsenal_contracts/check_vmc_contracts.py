#!/usr/bin/env python3

# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
# Domaine : VMC
# Vérification des invariants structurels
# ==========================================================

from pathlib import Path
import sys


ERRORS = []


# ==========================================================
# CONFIGURATION
# ==========================================================

ROOT = Path(".")


# ==========================================================
# HELPERS
# ==========================================================

def fail(message: str):
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ==========================================================
# TEST 1 — Capteur décisionnel unique
# ==========================================================

matches = []

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    content = read(path)

    if "binary_sensor.vmc_haute_vitesse_requise" in content:
        matches.append(path)

if not matches:
    fail(
        "Capteur décisionnel VMC introuvable : "
        "binary_sensor.vmc_haute_vitesse_requise"
    )

print("✔ Capteur décisionnel présent")


# ==========================================================
# TEST 2 — Scripts VMC sans logique métier
# ==========================================================

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    path_str = str(path).lower()

    if "vmc" not in path_str:
        continue

    if "script" not in path_str:
        continue

    content = read(path)

    forbidden_terms = [
        "humidity",
        "humidite",
        "co2",
        "aeration_preferable",
        "vmc_seuil",
    ]

    for term in forbidden_terms:
        if term in content:
            fail(
                f"Logique métier interdite dans script VMC : "
                f"{path} -> '{term}'"
            )

print("✔ Scripts VMC sans logique métier")


# ==========================================================
# TEST 3 — Automatisation VMC avec mode
# ==========================================================

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    path_str = str(path).lower()

    if "vmc" not in path_str:
        continue

    if "automation" not in path_str:
        continue

    content = read(path)

    if "- id:" in content and "mode:" not in content:
        fail(
            f"Automatisation VMC sans mode : {path}"
        )

print("✔ Automatisations VMC avec mode")


# ==========================================================
# RESULTAT
# ==========================================================

if ERRORS:

    print("\n❌ CONTRAT VMC NON CONFORME\n")

    for error in ERRORS:
        print(f"- {error}")

    sys.exit(1)

print("\n✅ CONTRAT VMC CONFORME")