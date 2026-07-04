#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Référentiel BSSID Maison
Contrat (source normative) : 00_documentation_arsenal/contrats/bssid.md
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

DIR_INPUT_TEXTS      = ROOT / "04_input_texts"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_BSSID_AUTO       = ROOT / "11_automations" / "system"

# Fichiers canoniques
FILE_BSSID_MAISON    = DIR_INPUT_TEXTS / "system" / "bssid.yaml"
FILE_NOUVEAU_BSSID   = DIR_TEMPLATE_SENSORS / "system" / "bssid" / "nouveau.yaml"
FILE_WIFI_PRESENCE   = DIR_TEMPLATE_SENSORS / "presence" / "securite" / "wifi.yaml"
FILE_BSSID_WIFI_AUTO = DIR_BSSID_AUTO / "bssid_wifi.yaml"
FILE_BSSID_ALERTE    = DIR_BSSID_AUTO / "bssid_alerte.yaml"


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

def test_input_text_bssid_maison_declared() -> None:
    """T01 — input_text.bssid_maison déclaré dans 04_input_texts/system/"""
    folder = DIR_INPUT_TEXTS / "system"
    if not is_declared_as_mapping_key("bssid_maison", folder):
        error(f"T01: input_text.bssid_maison introuvable dans {folder.relative_to(ROOT)}/")
    ok("T01 — input_text.bssid_maison")


def test_binary_sensor_nouveau_bssid_declared() -> None:
    """T02 — binary_sensor.wifi_nouveau_bssid déclaré dans 12_template_sensors/system/bssid/"""
    folder = DIR_TEMPLATE_SENSORS / "system" / "bssid"
    if not is_declared_as_unique_id("wifi_nouveau_bssid", folder):
        error(
            f"T02: binary_sensor.wifi_nouveau_bssid introuvable dans "
            f"{folder.relative_to(ROOT)}/"
        )
    ok("T02 — binary_sensor.wifi_nouveau_bssid")


def test_binary_sensor_presence_wifi_declared() -> None:
    """T03 — binary_sensor.presence_wifi_maison déclaré dans 12_template_sensors/presence/securite/"""
    folder = DIR_TEMPLATE_SENSORS / "presence" / "securite"
    if not is_declared_as_unique_id("presence_wifi_maison", folder):
        error(
            f"T03: binary_sensor.presence_wifi_maison introuvable dans "
            f"{folder.relative_to(ROOT)}/"
        )
    ok("T03 — binary_sensor.presence_wifi_maison")


def test_automation_apprentissage_declared() -> None:
    """T04 — automation d'apprentissage BSSID présente dans 11_automations/system/"""
    if not FILE_BSSID_WIFI_AUTO.is_file():
        error("T04: bssid_wifi.yaml introuvable dans 11_automations/system/")
    ok("T04 — automation apprentissage bssid_wifi.yaml")


def test_automation_alerte_declared() -> None:
    """T05 — automation d'alerte BSSID présente dans 11_automations/system/"""
    if not FILE_BSSID_ALERTE.is_file():
        error("T05: bssid_alerte.yaml introuvable dans 11_automations/system/")
    ok("T05 — automation alerte bssid_alerte.yaml")


def test_nouveau_bssid_consumes_bssid_maison() -> None:
    """
    T06 — binary_sensor.wifi_nouveau_bssid lit input_text.bssid_maison.
    Contrat §11 : seul point d'accès décisionnel au référentiel.
    Scope : 12_template_sensors/system/bssid/nouveau.yaml
    """
    if not FILE_NOUVEAU_BSSID.is_file():
        error("T06: nouveau.yaml introuvable")
        return
    content = read(FILE_NOUVEAU_BSSID)
    if not re.search(r'input_text\.bssid_maison', content):
        error("T06: binary_sensor.wifi_nouveau_bssid ne lit pas input_text.bssid_maison")
    ok("T06 — wifi_nouveau_bssid consomme bssid_maison")


def test_nouveau_bssid_enforces_source_person_coupling() -> None:
    """
    T07 — binary_sensor.wifi_nouveau_bssid applique le couplage source ↔ personne (§7).
    Vérifie la présence des deux sources canoniques ET de leurs personnes couplées.
    Scope : 12_template_sensors/system/bssid/nouveau.yaml
    """
    if not FILE_NOUVEAU_BSSID.is_file():
        error("T07: nouveau.yaml introuvable")
        return
    content = read(FILE_NOUVEAU_BSSID)

    REQUIRED = [
        (r'telephone_antoine_bssid_dynamic', "source antoine"),
        (r'telephone_constance_bssid_dynamic', "source constance"),
        (r'person\.valentin', "person.valentin"),
        (r'person\.constance', "person.constance"),
        (r'Maison securite', "zone Maison securite"),
    ]
    for pattern, label in REQUIRED:
        if not re.search(pattern, content):
            error(
                f"T07: binary_sensor.wifi_nouveau_bssid ne référence pas {label} "
                f"— couplage source ↔ personne incomplet"
            )
    ok("T07 — wifi_nouveau_bssid applique le couplage source ↔ personne")


def test_nouveau_bssid_normalisation() -> None:
    """
    T08 — binary_sensor.wifi_nouveau_bssid applique la normalisation canonique (§6).
    Vérifie la présence des transformations lower, replace(':', ''), replace('-', '').
    Scope : 12_template_sensors/system/bssid/nouveau.yaml
    """
    if not FILE_NOUVEAU_BSSID.is_file():
        error("T08: nouveau.yaml introuvable")
        return
    content = read(FILE_NOUVEAU_BSSID)

    for transform, label in [
        (r'\|\s*lower', "| lower"),
        (r"replace\(['\"]:['\"]", "replace(':','')"),
        (r"replace\(['\"][-]['\"]", "replace('-','')"),
    ]:
        if not re.search(transform, content):
            error(
                f"T08: normalisation '{label}' absente dans wifi_nouveau_bssid "
                f"— contrat §6 non respecté"
            )
    ok("T08 — wifi_nouveau_bssid applique la normalisation canonique")


def test_presence_wifi_reads_bssid_maison_only() -> None:
    """
    T09 — binary_sensor.presence_wifi_maison lit input_text.bssid_maison
    comme source unique du référentiel (§11).
    Scope : 12_template_sensors/presence/securite/wifi.yaml
    """
    if not FILE_WIFI_PRESENCE.is_file():
        error("T09: wifi.yaml introuvable dans 12_template_sensors/presence/securite/")
        return
    content = read(FILE_WIFI_PRESENCE)
    if not re.search(r'input_text\.bssid_maison', content):
        error(
            "T09: binary_sensor.presence_wifi_maison ne lit pas input_text.bssid_maison "
            "— source unique du référentiel non respectée"
        )
    ok("T09 — presence_wifi_maison consomme bssid_maison")


def test_apprentissage_triggered_by_nouveau_bssid() -> None:
    """
    T10 — L'automation d'apprentissage se déclenche sur binary_sensor.wifi_nouveau_bssid.
    Contrat §17.3 : déclenchement sur signal métier.
    Scope : 11_automations/system/bssid_wifi.yaml
    """
    if not FILE_BSSID_WIFI_AUTO.is_file():
        error("T10: bssid_wifi.yaml introuvable")
        return
    content = read(FILE_BSSID_WIFI_AUTO)
    if not re.search(r'wifi_nouveau_bssid', content):
        error(
            "T10: automation apprentissage ne se déclenche pas sur "
            "binary_sensor.wifi_nouveau_bssid"
        )
    ok("T10 — automation apprentissage déclenchée sur wifi_nouveau_bssid")


def test_apprentissage_writes_bssid_maison() -> None:
    """
    T11 — L'automation d'apprentissage écrit sur input_text.bssid_maison.
    Scope : 11_automations/system/bssid_wifi.yaml
    Distingue lecture passive et écriture réelle.
    """
    if not FILE_BSSID_WIFI_AUTO.is_file():
        error("T11: bssid_wifi.yaml introuvable")
        return
    content = read(FILE_BSSID_WIFI_AUTO)
    WRITE_PATTERN = re.compile(
        r'input_text\.set_value[\s\S]{0,300}bssid_maison',
        re.MULTILINE
    )
    if not WRITE_PATTERN.search(content):
        error(
            "T11: automation apprentissage ne contient pas d'écriture "
            "input_text.set_value sur bssid_maison"
        )
    ok("T11 — automation apprentissage écrit sur bssid_maison")


def test_apprentissage_enforces_source_person_coupling() -> None:
    """
    T12 — L'automation d'apprentissage applique le couplage source ↔ personne (§7, §8.6).
    Vérifie que les deux personnes couplées sont référencées dans la garde.
    Scope : 11_automations/system/bssid_wifi.yaml
    """
    if not FILE_BSSID_WIFI_AUTO.is_file():
        error("T12: bssid_wifi.yaml introuvable")
        return
    content = read(FILE_BSSID_WIFI_AUTO)
    for pattern, label in [
        (r'person\.valentin', "person.valentin"),
        (r'person\.constance', "person.constance"),
        (r'Maison securite', "zone Maison securite"),
    ]:
        if not re.search(pattern, content):
            error(
                f"T12: automation apprentissage ne référence pas {label} "
                f"— garde source ↔ personne incomplète"
            )
    ok("T12 — automation apprentissage applique le couplage source ↔ personne")


def test_apprentissage_consumes_candidats_par_source() -> None:
    """
    T13 — L'automation d'apprentissage consomme les attributs candidats par source
    (candidats_antoine, candidats_constance) — pas la fusion globale (§7.4, §16).
    Scope : 11_automations/system/bssid_wifi.yaml
    """
    if not FILE_BSSID_WIFI_AUTO.is_file():
        error("T13: bssid_wifi.yaml introuvable")
        return
    content = read(FILE_BSSID_WIFI_AUTO)
    for attr, label in [
        (r'candidats_antoine', "attribut candidats_antoine"),
        (r'candidats_constance', "attribut candidats_constance"),
    ]:
        if not re.search(attr, content):
            error(
                f"T13: automation apprentissage ne consomme pas {label} "
                f"— étanchéité inter-sources non garantie"
            )
    ok("T13 — automation apprentissage consomme les candidats par source")


def test_bssid_maison_written_only_by_authorized() -> None:
    """
    T14 — input_text.bssid_maison n'est écrit que par l'automation d'apprentissage.
    Scope : 11_automations/ entier, exclusion de bssid_wifi.yaml.
    Scope : 10_scripts/ entier.
    """
    WRITE_PATTERN = re.compile(
        r'input_text\.set_value[\s\S]{0,300}bssid_maison',
        re.MULTILINE
    )

    # Scan automations hors bssid_wifi.yaml
    for p in yaml_files(DIR_AUTOMATIONS):
        if p.resolve() == FILE_BSSID_WIFI_AUTO.resolve():
            continue
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T14: écriture sur input_text.bssid_maison hors automation "
                f"d'apprentissage : {p.relative_to(ROOT)}"
            )

    # Scan scripts
    for p in yaml_files(DIR_SCRIPTS):
        content = read(p)
        if WRITE_PATTERN.search(content):
            error(
                f"T14: écriture sur input_text.bssid_maison depuis un script "
                f"interdit : {p.relative_to(ROOT)}"
            )

    ok("T14 — bssid_maison écrit uniquement par l'automation d'apprentissage")


def test_alerte_triggered_on_bssid_maison() -> None:
    """
    T15 — L'automation d'alerte se déclenche sur input_text.bssid_maison (§9.1).
    Scope : 11_automations/system/bssid_alerte.yaml
    """
    if not FILE_BSSID_ALERTE.is_file():
        error("T15: bssid_alerte.yaml introuvable")
        return
    content = read(FILE_BSSID_ALERTE)
    if not re.search(r'input_text\.bssid_maison', content):
        error(
            "T15: automation alerte ne se déclenche pas sur input_text.bssid_maison"
        )
    ok("T15 — automation alerte déclenchée sur bssid_maison")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_input_text_bssid_maison_declared,
    test_binary_sensor_nouveau_bssid_declared,
    test_binary_sensor_presence_wifi_declared,
    test_automation_apprentissage_declared,
    test_automation_alerte_declared,
    test_nouveau_bssid_consumes_bssid_maison,
    test_nouveau_bssid_enforces_source_person_coupling,
    test_nouveau_bssid_normalisation,
    test_presence_wifi_reads_bssid_maison_only,
    test_apprentissage_triggered_by_nouveau_bssid,
    test_apprentissage_writes_bssid_maison,
    test_apprentissage_enforces_source_person_coupling,
    test_apprentissage_consumes_candidats_par_source,
    test_bssid_maison_written_only_by_authorized,
    test_alerte_triggered_on_bssid_maison,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Référentiel BSSID Maison\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BSSID NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BSSID CONFORME")