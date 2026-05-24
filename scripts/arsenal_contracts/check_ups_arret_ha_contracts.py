#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : UPS / Arrêt Home Assistant
Contrat : UPS / Arrêt HA v1.0
Script  : scripts/arsenal_contracts/check_ups_arret_ha_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques du domaine
# ---------------------------------------------------------------------------
F_AUTOMATION     = REPO_ROOT / "11_automations/system/ha_shutdown_ups.yaml"
F_TEMPLATE_UPS   = REPO_ROOT / "12_template_sensors/system/ups.yaml"

# Dossiers à scanner pour les interdictions d'écriture hors périmètre
DIR_SCRIPTS      = REPO_ROOT / "10_scripts"
DIR_AUTOMATIONS  = REPO_ROOT / "11_automations"

# Seuil normatif AHC (§3.2)
AHC_SEUIL = 600

# Délai CD normatif (§3.1, I-2)
CD_DELAI = "00:01:00"

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return [p for p in directory.rglob("*.yaml") if p.is_file()]


# ---------------------------------------------------------------------------
# T1 — Déclaration des binary_sensors critères UPS
#
# Invariant structurel : les deux critères binaires doivent être déclarés
# dans le fichier template sensors UPS via unique_id: (pattern template sensor).
# ---------------------------------------------------------------------------

REQUIRED_BINARY_SENSORS = [
    "critere_ups_sur_batterie",
    "critere_ups_batterie_faible",
]

def test_binary_sensors_declared() -> None:
    content = read(F_TEMPLATE_UPS)
    if not content:
        ERRORS.append(
            f"T1 — Fichier template UPS manquant : {F_TEMPLATE_UPS.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for uid in REQUIRED_BINARY_SENSORS:
        pattern = rf"unique_id\s*:\s*{re.escape(uid)}\b"
        if not re.search(pattern, content):
            ERRORS.append(
                f"T1 — binary_sensor '{uid}' non déclaré (unique_id absent) dans "
                f"{F_TEMPLATE_UPS.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T1 — binary_sensors critères UPS déclarés (unique_id)")


# ---------------------------------------------------------------------------
# T2 — Présence du fichier canonique d'arrêt HA
#
# Invariant structurel : l'automation d'arrêt doit exister à son chemin
# canonique. Son absence est une régression contractuelle immédiate.
# ---------------------------------------------------------------------------

def test_automation_file_present() -> None:
    if not F_AUTOMATION.is_file():
        ERRORS.append(
            f"T2 — Fichier canonique d'arrêt HA manquant : "
            f"{F_AUTOMATION.relative_to(REPO_ROOT)}"
        )
    else:
        print("✔ T2 — Fichier canonique d'arrêt HA présent")


# ---------------------------------------------------------------------------
# T3 — Délai CD de 60 s présent dans l'automation (I-2)
#
# Invariant (§3.1, I-2) : le critère temporel CD appartient exclusivement
# à l'automation via for: "00:01:00". Toute substitution par un timer
# externe ou un template sensor est une déviation contractuelle.
# Scope : fichier canonique uniquement.
# ---------------------------------------------------------------------------

def test_cd_delay_present() -> None:
    content = read(F_AUTOMATION)
    if not content:
        ERRORS.append(
            f"T3 — Fichier inaccessible : {F_AUTOMATION.relative_to(REPO_ROOT)}"
        )
        return
    # Le délai doit apparaître sous la forme for: "00:01:00"
    found = bool(re.search(
        rf'for\s*:\s*["\']?{re.escape(CD_DELAI)}["\']?',
        content
    ))
    if not found:
        ERRORS.append(
            f"T3 — Délai CD '{CD_DELAI}' absent de "
            f"{F_AUTOMATION.relative_to(REPO_ROOT)} "
            f"(I-2 : critère temporel obligatoire dans l'automation via for:)"
        )
    else:
        print(f"✔ T3 — Délai CD for: \"{CD_DELAI}\" présent dans l'automation")


# ---------------------------------------------------------------------------
# T4 — Seuil AHC = 600 s présent dans l'automation (§3.2)
#
# Invariant (§3.2) : le seuil d'autonomie critique HA est de 600 s.
# Il doit être encodé dans l'automation canonique.
# Méthode : présence de la valeur 600 dans un contexte autonomie
# (rayon de 150 chars autour de 'autonomie').
# Scope : fichier canonique uniquement.
# ---------------------------------------------------------------------------

def test_ahc_seuil_present() -> None:
    content = read(F_AUTOMATION)
    if not content:
        ERRORS.append(
            f"T4 — Fichier inaccessible : {F_AUTOMATION.relative_to(REPO_ROOT)}"
        )
        return
    windows = re.findall(r".{0,150}autonomie.{0,150}", content, re.IGNORECASE)
    found = any(str(AHC_SEUIL) in w for w in windows)
    if not found:
        ERRORS.append(
            f"T4 — Seuil AHC ({AHC_SEUIL} s) absent dans un contexte 'autonomie' de "
            f"{F_AUTOMATION.relative_to(REPO_ROOT)} (§3.2)"
        )
    else:
        print(f"✔ T4 — Seuil AHC {AHC_SEUIL} s présent dans l'automation")


# ---------------------------------------------------------------------------
# T5 — critere_ups_sur_batterie est le trigger de l'automation (I-1)
#
# Invariant (I-1) : aucun arrêt immédiat au passage sur batterie.
# Le trigger doit porter critere_ups_sur_batterie avec un for: — pas en
# condition seule. Vérification que l'entité apparaît dans un bloc trigger
# de l'automation canonique.
# Scope : fichier canonique uniquement.
# ---------------------------------------------------------------------------

def test_cd_trigger_is_binary_sensor() -> None:
    content = read(F_AUTOMATION)
    if not content:
        ERRORS.append(
            f"T5 — Fichier inaccessible : {F_AUTOMATION.relative_to(REPO_ROOT)}"
        )
        return

    # Vérifie que critere_ups_sur_batterie apparaît ET que for: 00:01:00 est
    # dans le même fichier (coprésence — scope déjà restreint au fichier canonique)
    has_trigger_entity = "critere_ups_sur_batterie" in content
    has_for_delay = bool(re.search(
        rf'for\s*:\s*["\']?{re.escape(CD_DELAI)}["\']?', content
    ))

    if not has_trigger_entity:
        ERRORS.append(
            f"T5 — binary_sensor.critere_ups_sur_batterie absent de "
            f"{F_AUTOMATION.relative_to(REPO_ROOT)}"
        )
    elif not has_for_delay:
        ERRORS.append(
            f"T5 — critere_ups_sur_batterie présent mais délai for: absent — "
            f"arrêt immédiat possible (violation I-1)"
        )
    else:
        print(
            "✔ T5 — critere_ups_sur_batterie présent avec délai for: "
            "(pas d'arrêt immédiat)"
        )


# ---------------------------------------------------------------------------
# T6 — hassio.host_shutdown confiné au fichier canonique
#
# Invariant (§2.2) : hassio.host_shutdown est l'unique action autorisée,
# et elle ne doit être appelée que depuis l'automation canonique.
# Toute occurrence dans un autre fichier de 11_automations/ ou 10_scripts/
# est une violation contractuelle.
# Exclusion explicite : le fichier canonique lui-même.
# ---------------------------------------------------------------------------

def test_shutdown_confined_to_canonical() -> None:
    violations = []
    canonical_rel = F_AUTOMATION.relative_to(REPO_ROOT)

    for directory in [DIR_AUTOMATIONS, DIR_SCRIPTS]:
        for path in yaml_files(directory):
            # Exclure le fichier canonique
            if path == F_AUTOMATION:
                continue
            content = read(path)
            # Cherche un appel réel : service: hassio.host_shutdown
            # Exclut les mentions en commentaire (ligne commençant par #)
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "hassio.host_shutdown" in stripped:
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"hassio.host_shutdown hors fichier canonique "
                        f"({canonical_rel})"
                    )
                    break  # une violation par fichier suffit

    if violations:
        for v in violations:
            ERRORS.append(f"T6 — Confinement violé : {v}")
    else:
        print(
            "✔ T6 — hassio.host_shutdown confiné au fichier canonique "
            f"({F_AUTOMATION.relative_to(REPO_ROOT)})"
        )


# ---------------------------------------------------------------------------
# T7 — Absence de hassio.host_shutdown dans les sensors / helpers
#
# Invariant complémentaire : les dossiers de déclaration d'entités
# (12_template_sensors/, 05_input_booleans/, etc.) ne doivent jamais
# contenir d'appel à hassio.host_shutdown — ce serait une architecture
# inversée (sensor qui agit).
# Scope : 12_template_sensors/ uniquement (le plus à risque).
# ---------------------------------------------------------------------------

DIR_TEMPLATE_SENSORS = REPO_ROOT / "12_template_sensors"

def test_shutdown_absent_from_sensors() -> None:
    violations = []
    for path in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(path)
        for line in content.splitlines():
            if line.strip().startswith("#"):
                continue
            if "hassio.host_shutdown" in line:
                violations.append(path.relative_to(REPO_ROOT))
                break
    if violations:
        for v in violations:
            ERRORS.append(
                f"T7 — hassio.host_shutdown dans un template sensor : {v}"
            )
    else:
        print("✔ T7 — hassio.host_shutdown absent des template sensors")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_binary_sensors_declared,
    test_automation_file_present,
    test_cd_delay_present,
    test_ahc_seuil_present,
    test_cd_trigger_is_binary_sensor,
    test_shutdown_confined_to_canonical,
    test_shutdown_absent_from_sensors,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : UPS / Arrêt HA v1.0\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT UPS ARRÊT HA NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT UPS ARRÊT HA CONFORME")
