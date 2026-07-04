#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Déshumidificateur — Guard d'exécution
Contrat (source normative) : 00_documentation_arsenal/contrats/deshumidificateur/guard.md
"""
from pathlib import Path
import re
import sys

DOMAIN = "DESHUM GUARD"
ROOT = Path(__file__).resolve().parents[2]
ERRORS = []

GUARD_PATH = ROOT / "10_scripts/deshumidificateur/guard_deshumidificateur.yaml"


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


def contains_mapping_key(entity_id: str) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(entity_id)}\s*:", re.MULTILINE)
    return any(pattern.search(read(path)) for path in yaml_files(ROOT))


def assert_ok(condition: bool, message: str):
    if not condition:
        ERRORS.append(message)


def test_guard_file_present():
    assert_ok(
        GUARD_PATH.is_file(),
        "Script guard absent : 10_scripts/deshumidificateur/guard_deshumidificateur.yaml",
    )
    print("✔ fichier guard present")


def test_guard_script_declared():
    if not GUARD_PATH.is_file():
        print("✔ declaration guard non testee : fichier absent")
        return

    text = read(GUARD_PATH)
    assert_ok(
        re.search(r"^\s*guard_deshumidificateur\s*:", text, re.MULTILINE) is not None,
        "Script guard non declare par cle de mapping guard_deshumidificateur:",
    )

    print("✔ script guard declare")


def test_guard_uses_single_truth_source():
    if not GUARD_PATH.is_file():
        print("✔ source de verite guard non testee : fichier absent")
        return

    text = without_full_line_comments(read(GUARD_PATH))

    assert_ok(
        "binary_sensor.deshumidificateur_actif" in text,
        "Guard : source de verite absente",
    )

    forbidden_sources = [
        "switch.deshumidificateur",
        "switch.prise_deshumidificateur",
        "sensor.prise_deshumidificateur_power",
        "last_run_success",
        "last_changed",
    ]

    for token in forbidden_sources:
        assert_ok(
            token not in text,
            f"Guard : source interdite utilisee hors commentaire : {token}",
        )

    print("✔ guard limite a la source de verite contractuelle")


def test_guard_has_no_material_action_or_retry():
    if not GUARD_PATH.is_file():
        print("✔ passivite guard non testee : fichier absent")
        return

    text = without_full_line_comments(read(GUARD_PATH))

    forbidden_patterns = [
        r"(?:action|service)\s*:\s*switch\.",
        r"(?:action|service)\s*:\s*button\.",
        r"(?:action|service)\s*:\s*script\.set_deshumidificateur_state",
        r"(?:action|service)\s*:\s*script\.turn_on",
        r"(?:action|service)\s*:\s*homeassistant\.turn_on",
        r"(?:action|service)\s*:\s*homeassistant\.turn_off",
    ]

    for pattern in forbidden_patterns:
        assert_ok(
            re.search(pattern, text) is None,
            f"Guard : action ou reemission interdite detectee : {pattern}",
        )

    print("✔ guard sans action materielle ni retry")


def test_guard_writes_only_diagnostic_helpers():
    if not GUARD_PATH.is_file():
        print("✔ ecritures diagnostic guard non testees : fichier absent")
        return

    text = without_full_line_comments(read(GUARD_PATH))

    actions = re.findall(r"(?:action|service)\s*:\s*([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)", text)
    forbidden = [action for action in actions if action != "input_text.set_value"]

    assert_ok(
        not forbidden,
        f"Guard : actions non diagnostiques detectees : {sorted(set(forbidden))}",
    )

    print("✔ guard limite aux ecritures diagnostiques input_text")


def test_guard_diagnostic_helpers_declared():
    helpers = [
        "deshum_guard_last_verdict",
        "deshum_guard_last_expected_state",
        "deshum_guard_last_observed_state",
        "deshum_guard_last_reason",
        "deshum_guard_last_ts",
        "deshum_guard_last_request_source",
        "deshum_guard_last_request_id",
    ]

    for helper in helpers:
        assert_ok(
            contains_mapping_key(helper),
            f"Helper diagnostic guard non declare : input_text.{helper}",
        )

    print("✔ helpers diagnostiques guard declares")


def test_guard_canonical_verdicts_and_reasons_present():
    if not GUARD_PATH.is_file():
        print("✔ verdicts guard non testes : fichier absent")
        return

    text = read(GUARD_PATH)

    required_literals = [
        "confirmed",
        "not_confirmed",
        "command_error",
        "converged_immediate",
        "converged_early",
        "timeout_reached",
        "unavailable_at_open",
        "unavailable_during_wait",
    ]

    for literal in required_literals:
        assert_ok(
            literal in text,
            f"Guard : literal canonique absent : {literal}",
        )

    print("✔ verdicts et raisons canoniques presents")


def test_guard_timeout_is_internal_and_fixed():
    if not GUARD_PATH.is_file():
        print("✔ timeout guard non teste : fichier absent")
        return

    text = without_full_line_comments(read(GUARD_PATH))

    assert_ok(
        re.search(r"timeout_seconds\s*:\s*120\b", text) is not None,
        "Guard : timeout_seconds interne fixe a 120 absent",
    )

    assert_ok(
        "timeout_seconds:" not in text.split("fields:", 1)[1].split("sequence:", 1)[0],
        "Guard : timeout_seconds expose comme champ appelant",
    )

    print("✔ timeout guard interne et souverain")


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
    "test_guard_file_present",
    "test_guard_script_declared",
    "test_guard_uses_single_truth_source",
    "test_guard_has_no_material_action_or_retry",
    "test_guard_writes_only_diagnostic_helpers",
    "test_guard_diagnostic_helpers_declared",
    "test_guard_canonical_verdicts_and_reasons_present",
    "test_guard_timeout_is_internal_and_fixed",
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