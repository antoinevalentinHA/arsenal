#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Déshumidificateur — Socle transactionnel
Contrat (source normative) : 00_documentation_arsenal/contrats/deshumidificateur/deshumidificateur.md
"""
from pathlib import Path
import re
import sys

DOMAIN = "DESHUM TX"
ROOT = Path(__file__).resolve().parents[2]
ERRORS = []

AUTHORIZED_SWITCH_WRITER = Path("10_scripts/deshumidificateur/forcer_etat.yaml")
SYSTEM_TRANSACTION_SCRIPT = Path("10_scripts/system/transactions_bots.yaml")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(base: Path):
    if not base.exists():
        return []
    return [p for p in base.rglob("*.yaml") if p.is_file()]


def all_yaml_files():
    ignored_parts = {
        ".git",
        ".github",
        "documentation_arsenal",
        "00_documentation_arsenal",
    }

    for path in ROOT.rglob("*.yaml"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        yield path


def without_full_line_comments(text: str) -> str:
    return "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().startswith("#")
    )


def contains_mapping_key(entity_id: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(entity_id)}\s*:", re.MULTILINE)
    return any(pattern.search(read(path)) for path in all_yaml_files())


def contains_unique_id(entity_id: str) -> bool:
    pattern = re.compile(rf"unique_id\s*:\s*{re.escape(entity_id)}\b")
    return any(pattern.search(read(path)) for path in all_yaml_files())


def assert_ok(condition: bool, message: str):
    if not condition:
        ERRORS.append(message)


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def has_switch_write(text: str) -> bool:
    pattern = re.compile(
        r"(?:action|service)\s*:\s*switch\.(?:turn_on|turn_off|toggle)"
        r"[\s\S]{0,300}?"
        r"entity_id\s*:\s*switch\.deshumidificateur",
        re.MULTILINE,
    )
    return pattern.search(text) is not None


def test_tx_entities_declared():
    expected_unique_id_entities = [
        "bot_tx_busy_deshumidificateur",
        "bot_tx_cooldown_deshumidificateur",
    ]

    expected_mapping_entities = [
        "bot_tx_failures_deshumidificateur",
        "bot_tx_lock_deshumidificateur",
        "bot_tx_cooldown_deshumidificateur",
    ]

    for entity_id in expected_unique_id_entities:
        assert_ok(
            contains_unique_id(entity_id),
            f"Entite TX template non declaree par unique_id : {entity_id}",
        )

    for entity_id in expected_mapping_entities:
        assert_ok(
            contains_mapping_key(entity_id),
            f"Entite TX helper/timer/counter non declaree par cle : {entity_id}",
        )

    print("✔ artefacts TX declares")


def test_authorized_execution_script_present_and_writes_switch():
    path = ROOT / AUTHORIZED_SWITCH_WRITER

    assert_ok(
        path.is_file(),
        f"Script autorise manquant : {AUTHORIZED_SWITCH_WRITER}",
    )

    if not path.is_file():
        print("✔ script autorise non teste : fichier absent")
        return

    text = without_full_line_comments(read(path))

    assert_ok(
        has_switch_write(text),
        "Script autorise present mais aucune ecriture switch.deshumidificateur detectee",
    )

    assert_ok(
        "script.guard_deshumidificateur" in text,
        "Script autorise : appel guard post-commande absent",
    )

    assert_ok(
        "binary_sensor.deshumidificateur_actif" in text,
        "Script autorise : lecture etat reel absente",
    )

    print("✔ script autorite unique ecrit le switch et appelle le guard")


def test_no_other_physical_switch_writers():
    offenders = []

    for path in all_yaml_files():
        rel = relative(path)

        if rel == AUTHORIZED_SWITCH_WRITER:
            continue

        text = without_full_line_comments(read(path))
        if has_switch_write(text):
            offenders.append(str(rel))

    assert_ok(
        not offenders,
        f"Ecriture non autorisee sur switch.deshumidificateur : {offenders}",
    )

    print("✔ aucun writer materiel hors autorite unique")


def test_system_transaction_layer_is_reference_only_for_switch():
    path = ROOT / SYSTEM_TRANSACTION_SCRIPT

    assert_ok(
        path.is_file(),
        f"Script transactionnel systeme absent : {SYSTEM_TRANSACTION_SCRIPT}",
    )

    if not path.is_file():
        print("✔ couche transactionnelle non testee : fichier absent")
        return

    text = without_full_line_comments(read(path))

    assert_ok(
        "switch.deshumidificateur" in text,
        "Transaction bots : reference switch.deshumidificateur absente",
    )

    assert_ok(
        not has_switch_write(text),
        "Transaction bots : ecriture directe interdite sur switch.deshumidificateur",
    )

    print("✔ couche transactionnelle sans ecriture directe du switch")


def test_domain_automations_do_not_write_switch():
    scope = ROOT / "11_automations/deshumidificateur"

    for path in yaml_files(scope):
        text = without_full_line_comments(read(path))
        if has_switch_write(text):
            ERRORS.append(
                f"Automation domaine ecrit directement le switch : {relative(path)}"
            )

    print("✔ automations domaine sans ecriture switch directe")


def test_guard_does_not_write_switch():
    path = ROOT / "10_scripts/deshumidificateur/guard_deshumidificateur.yaml"

    if not path.is_file():
        ERRORS.append("Guard absent : impossible de verifier la passivite TX")
        print("✔ guard TX non teste : fichier absent")
        return

    text = without_full_line_comments(read(path))

    assert_ok(
        not has_switch_write(text),
        "Guard : ecriture switch interdite detectee",
    )

    assert_ok(
        "switch.deshumidificateur" not in text,
        "Guard : reference active au switch detectee hors commentaire",
    )

    print("✔ guard sans ecriture ni lecture active du switch")


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
    "test_tx_entities_declared",
    "test_authorized_execution_script_present_and_writes_switch",
    "test_no_other_physical_switch_writers",
    "test_system_transaction_layer_is_reference_only_for_switch",
    "test_domain_automations_do_not_write_switch",
    "test_guard_does_not_write_switch",
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