#!/usr/bin/env python3
from pathlib import Path
import re
import sys

DOMAIN = "DESHUMIDIFICATEUR METIER"
ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(base: Path):
    if not base.exists():
        return []
    return [p for p in base.rglob("*.yaml") if p.is_file()]


def without_full_line_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def require_file(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        ERRORS.append(f"Fichier manquant : {relative}")
    return path


def contains_unique_id(entity_id: str, scope: Path) -> bool:
    pattern = re.compile(rf"unique_id\s*:\s*{re.escape(entity_id)}\b")
    return any(pattern.search(read(path)) for path in yaml_files(scope))


def contains_mapping_key(entity_id: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(entity_id)}\s*:", re.MULTILINE)
    return any(pattern.search(read(path)) for path in yaml_files(ROOT))


def assert_ok(condition: bool, message: str):
    if not condition:
        ERRORS.append(message)


def test_contract_entities_declared():
    template_scope = ROOT / "12_template_sensors/deshumidificateur"

    expected_template_entities = [
        "deshumidificateur_actif",
        "critere_deshumidification_cave",
        "critere_deshumidification_ha_cave",
        "deshumidificateur_cave_demarrage_recommande",
        "deshumidificateur_conformite_execution",
        "parametres_invalides_deshumidificateur",
    ]

    expected_mapping_entities = [
        "deshumidificateur_delai_min_redemarrage",
        "deshumidificateur_duree_mini_cycle",
        "deshumidificateur_cycle",
        "deshumidificateur_blocage_redemarrage",
    ]

    for entity_id in expected_template_entities:
        assert_ok(
            contains_unique_id(entity_id, template_scope),
            f"Template sensor/binary_sensor non declare par unique_id : {entity_id}",
        )

    for entity_id in expected_mapping_entities:
        assert_ok(
            contains_mapping_key(entity_id),
            f"Helper/timer non declare par cle de mapping : {entity_id}",
        )

    print("✔ entites metier canoniques declarees")


def test_canonical_domain_files_present():
    expected_files = [
        "12_template_sensors/deshumidificateur/etat.yaml",
        "12_template_sensors/deshumidificateur/demarrage_recommande.yaml",
        "12_template_sensors/deshumidificateur/criteres/humidite_relative.yaml",
        "12_template_sensors/deshumidificateur/criteres/humidite_absolue.yaml",
        "11_automations/deshumidificateur/activation.yaml",
        "11_automations/deshumidificateur/blocage_redemarrage.yaml",
        "11_automations/deshumidificateur/fermeture_cycle.yaml",
    ]

    for relative in expected_files:
        require_file(relative)

    print("✔ fichiers canoniques du domaine presents")


def test_recommendation_is_pure_aggregator():
    path = require_file("12_template_sensors/deshumidificateur/demarrage_recommande.yaml")
    if not path.is_file():
        print("✔ recommandation non testee : fichier absent")
        return

    text = without_full_line_comments(read(path))

    required = [
        "binary_sensor.critere_deshumidification_cave",
        "binary_sensor.critere_deshumidification_ha_cave",
    ]

    forbidden = [
        "sensor.humidite_relative_cave",
        "sensor.humidite_absolue_cave",
        "input_number.cave_rh_cible_on",
        "input_number.cave_rh_cible_off",
        "last_changed",
    ]

    for entity_id in required:
        assert_ok(
            entity_id in text,
            f"Recommandation : critere requis absent : {entity_id}",
        )

    for token in forbidden:
        assert_ok(
            token not in text,
            f"Recommandation : recalcul ou historique interdit detecte : {token}",
        )

    print("✔ recommandation metier limitee aux criteres locaux")


def test_no_last_changed_in_temporal_decision_scope():
    scopes = [
        ROOT / "11_automations/deshumidificateur",
        ROOT / "12_template_sensors/deshumidificateur",
        ROOT / "10_scripts/deshumidificateur",
    ]

    for scope in scopes:
        for path in yaml_files(scope):
            text = without_full_line_comments(read(path))
            if "last_changed" in text:
                ERRORS.append(f"Usage interdit de last_changed : {path.relative_to(ROOT)}")

    print("✔ aucune decision temporelle ne repose sur last_changed")


def test_timers_are_explicitly_used_by_discipline():
    automation_scope = ROOT / "11_automations/deshumidificateur"
    content = "\n".join(without_full_line_comments(read(p)) for p in yaml_files(automation_scope))

    required_tokens = [
        "timer.deshumidificateur_cycle",
        "timer.deshumidificateur_blocage_redemarrage",
        "input_number.deshumidificateur_duree_mini_cycle",
        "input_number.deshumidificateur_delai_min_redemarrage",
    ]

    for token in required_tokens:
        assert_ok(
            token in content,
            f"Discipline temporelle : artefact requis non consomme : {token}",
        )

    print("✔ discipline temporelle portee par helpers et timers explicites")


def test_automations_do_not_write_physical_switch_directly():
    scope = ROOT / "11_automations/deshumidificateur"
    writer_pattern = re.compile(
        r"(?:action|service)\s*:\s*switch\.(?:turn_on|turn_off|toggle)"
        r"[\s\S]{0,300}?"
        r"entity_id\s*:\s*switch\.deshumidificateur",
        re.MULTILINE,
    )

    for path in yaml_files(scope):
        text = without_full_line_comments(read(path))
        if writer_pattern.search(text):
            ERRORS.append(
                f"Pilotage materiel direct interdit depuis automation : {path.relative_to(ROOT)}"
            )

    print("✔ automations metier sans pilotage direct du switch physique")


def test_test_registry_matches_functions():
    defined = {
        name for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    }
    registered = set(TESTS)

    missing = registered - defined
    extra = defined - registered - {"test_test_registry_matches_functions"}

    if missing:
        ERRORS.append(f"TESTS reference des fonctions inexistantes : {sorted(missing)}")
    if extra:
        ERRORS.append(f"Fonctions de test non referencees dans TESTS : {sorted(extra)}")

    print("✔ registre TESTS coherent")


TESTS = [
    "test_contract_entities_declared",
    "test_canonical_domain_files_present",
    "test_recommendation_is_pure_aggregator",
    "test_no_last_changed_in_temporal_decision_scope",
    "test_timers_are_explicitly_used_by_discipline",
    "test_automations_do_not_write_physical_switch_directly",
    "test_test_registry_matches_functions",
]


def main():
    for test_name in TESTS:
        globals()[test_name]()

    if ERRORS:
        print(f"\n❌ CONTRAT {DOMAIN} NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print(f"\n✅ CONTRAT {DOMAIN} CONFORME.")


if __name__ == "__main__":
    main()