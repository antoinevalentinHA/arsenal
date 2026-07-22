#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Aération — Recommandation
Contrat (source normative) : 00_documentation_arsenal/contrats/aeration_recommandation.md
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
# Dossiers et fichiers canoniques
# ──────────────────────────────────────────────────────────────

DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_AUTOMATIONS      = ROOT / "11_automations"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_LOVELACE         = ROOT / "18_lovelace"

DIR_AERATION_SENSORS = DIR_TEMPLATE_SENSORS / "aeration" / "conseillee"

FILE_RDC    = DIR_AERATION_SENSORS / "rdc.yaml"
FILE_ETAGE  = DIR_AERATION_SENSORS / "etage.yaml"
FILE_GLOBAL = DIR_AERATION_SENSORS / "global.yaml"

# Consommateurs légitimes de aeration_preferable_etage (lecture passive)
LEGITIMATE_CONSUMERS = {
    DIR_TEMPLATE_SENSORS / "climatisation" / "autorisation" / "cool.yaml",
    DIR_TEMPLATE_SENSORS / "climatisation" / "autorisation" / "dry.yaml",
    DIR_TEMPLATE_SENSORS / "climatisation" / "blocages" / "blocage_aeration_etage_reel.yaml",
    # C35 L7.1 — `vmc/intention.yaml` SORT de cette liste : sa cause est
    # desormais derivee de l'attribut autoritatif `composition` de la
    # decision (§11.2), et il ne lit plus le verdict d'aeration.
    DIR_TEMPLATE_SENSORS / "vmc" / "delta_humidite_absolue_favorable.yaml",
    # C35 L7.1 — le verrou d'aeration a QUITTE l'agregation
    # `vmc/haute_vitesse_requise.yaml`, qui sort donc de cette liste, et vit
    # desormais dans les deux besoins locaux ci-dessous.
    #
    # ⚠️ ENTREES TEMPORAIRES — RETRAIT PREVU EN C35 L7.2.
    # Elles couvrent l'ECART CONTRACTUEL n° 1 du chantier, que le §4.3 de
    # `contrats/vmc.md` proscrit deja : le verdict d'aeration ne doit pas
    # conditionner la voie humidite. Leur retrait, avec celui du verrou dans
    # les deux fichiers, est la PREUVE du lot L7.2 et sert le critere de
    # cloture 8 de C35.
    DIR_TEMPLATE_SENSORS / "vmc" / "besoins" / "humidite_sdb_parents.yaml",
    DIR_TEMPLATE_SENSORS / "vmc" / "besoins" / "humidite_sdb_enfants.yaml",
    FILE_GLOBAL,
}


# ──────────────────────────────────────────────────────────────
# Détection
# ──────────────────────────────────────────────────────────────

def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf'unique_id\s*:\s*{re.escape(entity_id)}\b')
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_binary_sensors_declared() -> None:
    """T01 — Les trois binary_sensor de recommandation déclarés dans 12_template_sensors/aeration/"""
    for entity_id, filepath in [
        ("aeration_preferable_rdc",   FILE_RDC),
        ("aeration_preferable_etage", FILE_ETAGE),
    ]:
        if not filepath.is_file():
            error(f"T01: {filepath.relative_to(ROOT)} introuvable")
        elif not re.search(
            rf'unique_id\s*:\s*{re.escape(entity_id)}\b', read(filepath)
        ):
            error(f"T01: unique_id '{entity_id}' absent de {filepath.relative_to(ROOT)}")
    ok("T01 — binary_sensor aeration_preferable_rdc et etage déclarés")


def test_global_sensor_declared() -> None:
    """T02 — binary_sensor.aeration_conseillee déclaré dans global.yaml"""
    if not FILE_GLOBAL.is_file():
        error(f"T02: {FILE_GLOBAL.relative_to(ROOT)} introuvable")
    else:
        content = read(FILE_GLOBAL)
        if not re.search(r'unique_id\s*:\s*aeration_conseillee_global\b', content):
            error("T02: unique_id 'aeration_conseillee_global' absent de global.yaml")
    ok("T02 — binary_sensor.aeration_conseillee déclaré")


def test_global_aggregates_rdc_and_etage() -> None:
    """
    T03 — binary_sensor.aeration_conseillee agrège rdc ET etage sans recalcul métier.
    Contrat §DÉCISIONS PORTÉES : agrège RDC + étage, ne refait aucun calcul métier.
    Scope : 12_template_sensors/aeration/conseillee/global.yaml
    """
    if not FILE_GLOBAL.is_file():
        error("T03: global.yaml introuvable")
        return
    content = read(FILE_GLOBAL)
    for ref in ["aeration_preferable_rdc", "aeration_preferable_etage"]:
        if not re.search(re.escape(ref), content):
            error(f"T03: global.yaml ne consomme pas binary_sensor.{ref}")
    ok("T03 — global agrège rdc et etage")


def test_global_exposes_decision_globale() -> None:
    """
    T04 — binary_sensor.aeration_conseillee expose l'attribut decision_globale.
    Contrat §DÉCISIONS PORTÉES : expose decision_globale.
    Scope : global.yaml
    """
    if not FILE_GLOBAL.is_file():
        error("T04: global.yaml introuvable")
        return
    if not re.search(r'decision_globale', read(FILE_GLOBAL)):
        error("T04: global.yaml n'expose pas l'attribut decision_globale")
    ok("T04 — global expose decision_globale")


def test_local_sensors_expose_decision_attribute() -> None:
    """
    T05 — Les capteurs locaux rdc et etage exposent l'attribut decision.
    Contrat §DÉCISIONS PORTÉES : chaque capteur local porte une décision textuelle.
    Scope : rdc.yaml et etage.yaml
    """
    for p in [FILE_RDC, FILE_ETAGE]:
        if not p.is_file():
            continue
        content = read(p)
        if not re.search(r'\bdecision\b\s*:', content):
            error(
                f"T05: {p.relative_to(ROOT)} n'expose pas l'attribut 'decision' "
                f"— décision textuelle obligatoire"
            )
    ok("T05 — capteurs locaux exposent l'attribut decision")


def test_co2_priority_in_local_sensors() -> None:
    """
    T06 — Les capteurs locaux (rdc, etage) intègrent la priorité CO₂.
    Contrat §Priorité CO₂ : critère prioritaire absolu.
    Scope : rdc.yaml et etage.yaml
    """
    for p in [FILE_RDC, FILE_ETAGE]:
        if not p.is_file():
            continue
        content = read(p)
        if not re.search(r'co2|CO2|co_2', content, re.IGNORECASE):
            error(
                f"T06: {p.relative_to(ROOT)} n'intègre pas le critère CO₂ "
                f"— priorité sanitaire obligatoire"
            )
    ok("T06 — capteurs locaux intègrent la priorité CO₂")


def test_no_automation_in_aeration_domain() -> None:
    """
    T07 — Aucune automation ne porte de logique décisionnelle aération.
    Contrat §SÉPARATION DES RESPONSABILITÉS : Automatisations = Aucune.
    Scope : 11_automations/ entier.
    Vérifie qu'aucune automation n'écrit sur les binary_sensor ou ne déclenche
    une action sur transition d'état des capteurs aeration_preferable.
    """
    TRANSITION_TRIGGER = re.compile(
        r'entity_id\s*:.*aeration_preferable'
        r'|aeration_preferable.*\bto\s*:\s*["\']?(on|off)',
        re.IGNORECASE | re.MULTILINE
    )
    for p in yaml_files(DIR_AUTOMATIONS):
        content = read(p)
        if TRANSITION_TRIGGER.search(content):
            error(
                f"T07: automation déclenchée sur transition aeration_preferable "
                f"— logique sur transition interdite par contrat §INVARIANTS : "
                f"{p.relative_to(ROOT)}"
            )
    ok("T07 — aucune automation sur transition aeration_preferable")


def test_no_notification_on_aeration() -> None:
    """
    T08 — Aucune notification n'est émise en lien avec la recommandation d'aération.
    Contrat §INVARIANTS : toute notification interdite — persistante ou mobile.
    Scope : 11_automations/ et 10_scripts/ entiers.
    Détecte la coprésence d'un service de notification ET d'une référence aeration_preferable
    dans le même fichier.
    """
    NOTIF_SERVICE = re.compile(
        r'\b(?:notify\.|persistent_notification\.create|notify\.mobile)',
        re.IGNORECASE
    )
    AERATION_REF = re.compile(r'aeration_(?:preferable|conseillee)', re.IGNORECASE)

    for folder in [DIR_AUTOMATIONS, DIR_SCRIPTS]:
        for p in yaml_files(folder):
            content = read(p)
            if AERATION_REF.search(content) and NOTIF_SERVICE.search(content):
                error(
                    f"T08: notification détectée dans un fichier référençant "
                    f"aeration_preferable/conseillee : {p.relative_to(ROOT)} "
                    f"— interdit par contrat §INVARIANTS"
                )
    ok("T08 — aucune notification liée à la recommandation d'aération")


def test_no_thermal_action_from_aeration() -> None:
    """
    T09 — Les capteurs aeration_preferable ne déclenchent aucune action thermique.
    Contrat §INVARIANTS : une recommandation ne déclenche jamais d'action thermique.
    Scope : 11_automations/ et 10_scripts/ entiers.
    Interdit : service climate.*, switch.* chauffage, ou script chauffage
    dans un fichier déclenchant sur aeration_preferable.
    """
    THERMAL_SERVICES = re.compile(
        r'\b(?:climate\.set_temperature|climate\.set_hvac_mode'
        r'|climate\.turn_on|climate\.turn_off)\b',
        re.IGNORECASE
    )
    AERATION_TRIGGER = re.compile(
        r'entity_id\s*:.*aeration_(?:preferable|conseillee)',
        re.IGNORECASE
    )
    for folder in [DIR_AUTOMATIONS, DIR_SCRIPTS]:
        for p in yaml_files(folder):
            content = read(p)
            if AERATION_TRIGGER.search(content) and THERMAL_SERVICES.search(content):
                error(
                    f"T09: action thermique dans un fichier déclenché sur "
                    f"aeration_preferable/conseillee : {p.relative_to(ROOT)}"
                )
    ok("T09 — aucune action thermique déclenchée par la recommandation")


def test_etage_consumed_only_by_legitimate_consumers() -> None:
    """
    T10 — binary_sensor.aeration_preferable_etage n'est consommé que par
    les domaines autorisés par le contrat §NATURE ARCHITECTURALE.
    Consommateurs légitimes : climatisation blocage gardé, vmc, global.
    Scope : 12_template_sensors/ entier, exclusion des consommateurs légitimes.
    """
    ETAGE_REF = re.compile(r'aeration_preferable_etage', re.IGNORECASE)

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        if p.resolve() in {c.resolve() for c in LEGITIMATE_CONSUMERS}:
            continue
        # Exclure aussi le fichier etage.yaml lui-même
        if p.resolve() == FILE_ETAGE.resolve():
            continue
        content = read(p)
        if ETAGE_REF.search(content):
            error(
                f"T10: binary_sensor.aeration_preferable_etage consommé hors "
                f"domaines autorisés : {p.relative_to(ROOT)}"
            )
    ok("T10 — aeration_preferable_etage consommé uniquement par les domaines autorisés")


def test_dashboard_declared() -> None:
    """T11 — Dashboard aération déclaré dans 18_lovelace/dashboards/"""
    p = DIR_LOVELACE / "dashboards" / "aeration" / "principal.yaml"
    if not p.is_file():
        error(f"T11: {p.relative_to(ROOT)} introuvable — dashboard aération manquant")
    ok("T11 — dashboard aération déclaré")


def test_dashboard_no_logic() -> None:
    """
    T12 — Le dashboard aération ne contient pas de logique métier.
    Contrat §UI : les cartes ne modifient aucun état.
    Scope : 18_lovelace/dashboards/aeration/principal.yaml
    Interdit : service calls dans le dashboard.
    """
    p = DIR_LOVELACE / "dashboards" / "aeration" / "principal.yaml"
    if not p.is_file():
        error("T12: aeration.yaml introuvable")
        return
    content = read(p)
    WRITE_SERVICES = re.compile(
        r'\b(?:input_boolean\.turn_|input_number\.set_|switch\.turn_'
        r'|climate\.|light\.turn_)',
        re.IGNORECASE
    )
    if WRITE_SERVICES.search(content):
        error(
            "T12: service d'écriture détecté dans le dashboard aération "
            "— logique métier interdite dans l'UI"
        )
    ok("T12 — dashboard aération sans logique métier")


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_binary_sensors_declared,
    test_global_sensor_declared,
    test_global_aggregates_rdc_and_etage,
    test_global_exposes_decision_globale,
    test_local_sensors_expose_decision_attribute,
    test_co2_priority_in_local_sensors,
    test_no_automation_in_aeration_domain,
    test_no_notification_on_aeration,
    test_no_thermal_action_from_aeration,
    test_etage_consumed_only_by_legitimate_consumers,
    test_dashboard_declared,
    test_dashboard_no_logic,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Aération — Recommandation\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT AERATION_RECOMMANDATION NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT AERATION_RECOMMANDATION CONFORME")