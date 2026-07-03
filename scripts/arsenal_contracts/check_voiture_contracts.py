#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Voiture — Audi A3 e-tron
Contrat Arsenal — voiture.md
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ──────────────────────────────────────────────────────────────
# Dossiers canoniques Arsenal
# ──────────────────────────────────────────────────────────────

DIR_INPUT_NUMBERS    = ROOT / "03_input_numbers"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_VOITURE_AUTO     = ROOT / "11_automations" / "voiture"

# Fichiers canoniques
FILE_HELPERS         = DIR_INPUT_NUMBERS / "voiture" / "autonomie.yaml"
FILE_AUTONOMIE_AUTO  = DIR_VOITURE_AUTO / "autonomie.yaml"
FILE_ARCHIVE_AUTO    = DIR_VOITURE_AUTO / "archive.yaml"
FILE_NOTIF_AUTO      = DIR_VOITURE_AUTO / "notification_etat_charge.yaml"


# ──────────────────────────────────────────────────────────────
# Détection de déclaration
# ──────────────────────────────────────────────────────────────

def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(
        rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(
        rf'unique_id\s*:\s*{re.escape(entity_id)}\b'
    )
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_helpers_declared() -> None:
    """T01 — Les trois helpers métier déclarés dans 03_input_numbers/voiture/"""
    folder = DIR_INPUT_NUMBERS / "voiture"
    for entity_id in [
        "autonomie_audi_etron_full",
        "audi_temperature_charge",
        "audi_autonomie_corrigee_temperature",
    ]:
        if not is_declared_as_mapping_key(entity_id, folder):
            error(f"T01: input_number.{entity_id} introuvable dans {folder.relative_to(ROOT)}/")
    ok("T01 — helpers métier pleine charge")


def test_automations_declared() -> None:
    """T02 — Les trois automations canoniques présentes dans 11_automations/voiture/"""
    for filepath, auto_id, label in [
        (FILE_AUTONOMIE_AUTO, "10150000000001", "consolidation pleine charge"),
        (FILE_ARCHIVE_AUTO,   "10150000000004", "archivage mensuel"),
        (FILE_NOTIF_AUTO,     "10150000000005", "notification état charge"),
    ]:
        if not filepath.is_file():
            error(f"T02: {filepath.name} introuvable dans 11_automations/voiture/")
            continue
        if not re.search(re.escape(auto_id), read(filepath)):
            error(f"T02: ID {auto_id} ({label}) absent de {filepath.name}")
    ok("T02 — automations canoniques voiture")


def test_template_sensors_local_declared() -> None:
    """
    T03 — Les capteurs locaux stabilisés déclarés dans 12_template_sensors/voiture/
    Contrat §Couche 1 : seules sources autorisées pour les couches supérieures.
    Les unique_id suivent la convention Audi native (anglais) avec suffixe _local.
    """
    folder = DIR_TEMPLATE_SENSORS / "voiture"
    LOCAL_SENSORS = [
        "audi_a3_sportback_e_tron_primary_engine_percent_local",
        "audi_a3_sportback_e_tron_range_local",
        "audi_a3_sportback_e_tron_charging_state_local",
    ]
    for entity_id in LOCAL_SENSORS:
        if not is_declared_as_unique_id(entity_id, folder):
            error(
                f"T03: sensor unique_id '{entity_id}' introuvable dans "
                f"{folder.relative_to(ROOT)}/ — capteur local stabilisé manquant"
            )
    ok("T03 — capteurs locaux stabilisés déclarés")


def test_consolidation_triggered_by_local_sensor() -> None:
    """
    T04 — L'automation de consolidation se déclenche sur un capteur local stabilisé,
    pas sur un capteur cloud brut.
    Contrat §Couche 3 : déclenchée par variation du % batterie local.
    Scope : 11_automations/voiture/autonomie.yaml
    """
    if not FILE_AUTONOMIE_AUTO.is_file():
        error("T04: autonomie.yaml introuvable")
        return
    content = read(FILE_AUTONOMIE_AUTO)
    # Doit référencer un sensor local (suffixe _local)
    if not re.search(r'sensor\.\w+_local', content):
        error(
            "T04: automation consolidation ne se déclenche pas sur un capteur "
            "local stabilisé — source cloud brute potentielle"
        )
    ok("T04 — consolidation déclenchée sur capteur local")


def test_consolidation_writes_three_helpers_atomically() -> None:
    """
    T05 — L'automation de consolidation écrit les trois helpers dans la même séquence.
    Contrat §Couche 2 : écriture atomique des trois helpers.
    Scope : 11_automations/voiture/autonomie.yaml
    """
    if not FILE_AUTONOMIE_AUTO.is_file():
        error("T05: autonomie.yaml introuvable")
        return
    content = read(FILE_AUTONOMIE_AUTO)
    for entity_id in [
        "autonomie_audi_etron_full",
        "audi_temperature_charge",
        "audi_autonomie_corrigee_temperature",
    ]:
        if not re.search(re.escape(entity_id), content):
            error(
                f"T05: input_number.{entity_id} absent de l'automation de "
                f"consolidation — atomicité des trois helpers non garantie"
            )
    ok("T05 — consolidation écrit les trois helpers")


def test_consolidation_uses_temperature_jardin() -> None:
    """
    T06 — L'automation de consolidation consomme sensor.temperature_jardin
    comme source canonique température (§Couche 3, dépendance contractuelle).
    Scope : 11_automations/voiture/autonomie.yaml
    """
    if not FILE_AUTONOMIE_AUTO.is_file():
        error("T06: autonomie.yaml introuvable")
        return
    content = read(FILE_AUTONOMIE_AUTO)
    if not re.search(r'sensor\.temperature_jardin', content):
        error(
            "T06: automation consolidation ne consomme pas sensor.temperature_jardin "
            "— source température canonique absente"
        )
    ok("T06 — consolidation consomme sensor.temperature_jardin")


def test_consolidation_checks_battery_threshold() -> None:
    """
    T07 — L'automation de consolidation vérifie une condition batterie ≥ 99 %.
    Contrat §Couche 3 : condition batterie ≥ 99 % — implémentée via above: 98.9.
    Scope : 11_automations/voiture/autonomie.yaml
    """
    if not FILE_AUTONOMIE_AUTO.is_file():
        error("T07: autonomie.yaml introuvable")
        return
    content = read(FILE_AUTONOMIE_AUTO)
    if not re.search(r'above\s*:\s*9[89]', content):
        error(
            "T07: seuil pleine charge (above: 98.x ou 99) absent de l'automation "
            "de consolidation — condition pleine charge non vérifiable"
        )
    ok("T07 — consolidation vérifie le seuil batterie ≥ 99 %")


def test_helpers_written_only_by_consolidation() -> None:
    """
    T08 — Les trois helpers métier ne sont écrits que par l'automation de consolidation.
    Contrat §Couche 3 : aucune automation tierce ne peut écrire ces trois helpers.
    Scope : 11_automations/ entier (exclusion autonomie.yaml) + 10_scripts/ entier.
    """
    HELPERS = [
        "autonomie_audi_etron_full",
        "audi_temperature_charge",
        "audi_autonomie_corrigee_temperature",
    ]
    WRITE_PATTERN = re.compile(
        r'input_number\.set_value[\s\S]{0,300}(?:'
        + '|'.join(re.escape(h) for h in HELPERS)
        + ')',
        re.MULTILINE
    )

    for p in yaml_files(DIR_AUTOMATIONS):
        if p.resolve() == FILE_AUTONOMIE_AUTO.resolve():
            continue
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T08: écriture sur helper pleine charge hors automation de "
                f"consolidation : {p.relative_to(ROOT)}"
            )

    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T08: écriture sur helper pleine charge depuis un script "
                f"interdit : {p.relative_to(ROOT)}"
            )

    ok("T08 — helpers pleine charge écrits uniquement par la consolidation")


def test_notification_no_logic() -> None:
    """
    T09 — L'automation de notification état de charge ne contient pas de logique
    décisionnelle (calcul, condition métier complexe, écriture sur helper).
    Contrat §Couche 3 : aucune logique décisionnelle, aucun calcul, aucun historique.
    Scope : 11_automations/voiture/notification_etat_charge.yaml
    """
    if not FILE_NOTIF_AUTO.is_file():
        error("T09: notification_etat_charge.yaml introuvable")
        return
    content = read(FILE_NOTIF_AUTO)

    # Interdit : écriture sur un helper métier
    WRITE_HELPERS = re.compile(
        r'input_number\.set_value[\s\S]{0,200}'
        r'(?:autonomie_audi_etron_full|audi_temperature_charge|audi_autonomie_corrigee)',
        re.MULTILINE
    )
    if WRITE_HELPERS.search(content):
        error(
            "T09: notification_etat_charge.yaml écrit sur un helper métier — "
            "logique décisionnelle interdite dans cette automation"
        )

    # Interdit : calcul thermique
    if re.search(r'temperature_jardin', content):
        error(
            "T09: notification_etat_charge.yaml consomme sensor.temperature_jardin — "
            "calcul interdit dans l'automation de notification"
        )
    ok("T09 — automation notification sans logique décisionnelle")


def test_archive_triggered_monthly() -> None:
    """
    T10 — L'automation d'archivage est déclenchée mensuellement.
    Contrat §Couche 3 : déclenchée mensuellement.
    Scope : 11_automations/voiture/archive.yaml
    """
    if not FILE_ARCHIVE_AUTO.is_file():
        error("T10: archive.yaml introuvable")
        return
    content = read(FILE_ARCHIVE_AUTO)
    MONTHLY = re.compile(
        r'(?:platform\s*:\s*time|trigger.*time|day\s*:\s*1|monthly)',
        re.IGNORECASE
    )
    if not MONTHLY.search(content):
        error(
            "T10: automation archive ne contient pas de déclencheur mensuel "
            "identifiable"
        )
    ok("T10 — automation archive déclenchée mensuellement")


def test_no_cloud_sensor_in_automations() -> None:
    """
    T11 — Aucune automation voiture ne consomme directement un capteur cloud brut.
    Contrat §Architecture : aucune donnée cloud brute dans les automations métier.
    Les capteurs cloud sont identifiés par leur pattern Audi sans suffixe _local.
    Scope : 11_automations/voiture/ uniquement.
    """
    # Capteurs cloud bruts connus (sans _local)
    CLOUD_SENSORS = re.compile(
        r'sensor\.audi_(?!.*_local)'
        r'(?:e_tron_pourcentage_moteur_principal|e_tron_kilometrage'
        r'|e_tron_autonomie|e_tron_etat_de_charge'
        r'|a3_sportback_e_tron_range|a3_sportback_e_tron_charging_state'
        r'|a3_sportback_e_tron_primary_engine_percent)\b'
    )
    for p in yaml_files(DIR_VOITURE_AUTO):
        content = read(p)
        if CLOUD_SENSORS.search(content):
            error(
                f"T11: capteur cloud brut consommé directement dans une automation "
                f"voiture : {p.relative_to(ROOT)}"
            )
    ok("T11 — automations voiture sans capteur cloud brut")


def test_dashboards_declared() -> None:
    """
    T12 — Les trois dashboards normatifs sont présents dans 18_lovelace/dashboards/voiture/.
    Contrat §Couche 5.
    """
    DIR_DASHBOARDS = ROOT / "18_lovelace" / "dashboards" / "voiture"
    for filename in ["audi.yaml", "audi_securite.yaml", "audi_batterie.yaml"]:
        p = DIR_DASHBOARDS / filename
        if not p.is_file():
            error(f"T12: dashboard {filename} introuvable dans {DIR_DASHBOARDS.relative_to(ROOT)}/")
    ok("T12 — dashboards normatifs voiture")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_helpers_declared,
    test_automations_declared,
    test_consolidation_triggered_by_local_sensor,
    test_consolidation_writes_three_helpers_atomically,
    test_consolidation_uses_temperature_jardin,
    test_consolidation_checks_battery_threshold,
    test_helpers_written_only_by_consolidation,
    test_notification_no_logic,
    test_archive_triggered_monthly,
    test_no_cloud_sensor_in_automations,
    test_dashboards_declared,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Voiture — Audi A3 e-tron\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT VOITURE NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT VOITURE CONFORME")