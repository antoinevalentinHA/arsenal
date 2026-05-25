#!/usr/bin/env python3
# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
#     Aération — M4 — Fin blocage horaire
# ==========================================================

from pathlib import Path
import re
import sys


ROOT = Path.cwd()
ERRORS: list[str] = []

SCRIPT_FILENAME = "m4_fin_blocage_horaire.yaml"
SCRIPT_ID = "aeration_m4_fin_blocage_horaire"

FORBIDDEN_THERMAL_PATTERNS = [
    "climate.",
    "water_heater.",
    "switch.",
]

FORBIDDEN_SCRIPT_CALLS = [
    "script.aeration_m1",
    "script.aeration_m2",
    "script.aeration_m3",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_file(filename: str) -> Path | None:
    candidates = [
        path
        for path in ROOT.rglob(filename)
        if path.is_file()
        and ".git" not in path.parts
    ]

    if not candidates:
        return None

    preferred = [
        path
        for path in candidates
        if "10_scripts" in path.parts and "aeration" in path.parts
    ]

    return preferred[0] if preferred else candidates[0]


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        ERRORS.append(f"{label} : contenu attendu absent : {needle}")


def require_regex(text: str, pattern: str, label: str) -> None:
    if not re.search(pattern, text, flags=re.MULTILINE | re.DOTALL):
        ERRORS.append(f"{label} : pattern attendu absent : {pattern}")


def forbid_contains(text: str, needle: str, label: str) -> None:
    if needle in text:
        ERRORS.append(f"{label} : contenu interdit présent : {needle}")


def assert_test_registry_matches_functions() -> None:
    defined = {
        name
        for name, obj in globals().items()
        if callable(obj) and name.startswith("test_")
    }
    registered = set(TESTS)

    missing = registered - defined
    extra = defined - registered

    if missing:
        ERRORS.append(f"TESTS référence des fonctions absentes : {sorted(missing)}")
    if extra:
        ERRORS.append(f"fonctions test_* non référencées dans TESTS : {sorted(extra)}")


SCRIPT_PATH = find_file(SCRIPT_FILENAME)
SCRIPT_TEXT = read(SCRIPT_PATH) if SCRIPT_PATH else ""


def test_m4_script_present() -> None:
    if SCRIPT_PATH is None:
        ERRORS.append(f"script M4 introuvable : {SCRIPT_FILENAME}")
        return

    print("✔ script M4 canonique présent")


def test_m4_script_declared() -> None:
    if SCRIPT_PATH is None:
        return

    require_regex(
        SCRIPT_TEXT,
        rf"^\s*{re.escape(SCRIPT_ID)}\s*:",
        f"{SCRIPT_PATH} : déclaration script",
    )

    print("✔ script M4 déclaré sous clé YAML canonique")


def test_m4_lifts_heating_block() -> None:
    if SCRIPT_PATH is None:
        return

    require_contains(SCRIPT_TEXT, "input_boolean.turn_off", f"{SCRIPT_PATH} : service levée blocage")
    require_contains(
        SCRIPT_TEXT,
        "input_boolean.chauffage_blocage_aeration",
        f"{SCRIPT_PATH} : cible levée blocage",
    )

    print("✔ M4 : levée blocage chauffage présente")


def test_m4_cancels_domain_timers() -> None:
    if SCRIPT_PATH is None:
        return

    require_contains(SCRIPT_TEXT, "timer.cancel", f"{SCRIPT_PATH} : annulation timers")
    require_contains(
        SCRIPT_TEXT,
        "timer.aeration_blocage",
        f"{SCRIPT_PATH} : annulation timer blocage",
    )
    require_contains(
        SCRIPT_TEXT,
        "timer.aeration_analyse_delta_t",
        f"{SCRIPT_PATH} : annulation timer analyse DeltaT",
    )

    print("✔ M4 : annulation explicite des timers présente")


def test_m4_neutralizes_datetime_traces() -> None:
    if SCRIPT_PATH is None:
        return

    require_contains(
        SCRIPT_TEXT,
        "input_datetime.set_datetime",
        f"{SCRIPT_PATH} : service neutralisation datetime",
    )
    require_contains(
        SCRIPT_TEXT,
        "input_datetime.chauffage_fin_blocage_aeration",
        f"{SCRIPT_PATH} : neutralisation fin blocage",
    )
    require_contains(
        SCRIPT_TEXT,
        "input_datetime.analyse_deltat_disponible",
        f"{SCRIPT_PATH} : neutralisation analyse DeltaT",
    )
    require_contains(SCRIPT_TEXT, "00:00:00", f"{SCRIPT_PATH} : sentinelle minuit")
    require_contains(
        SCRIPT_TEXT,
        "now().date().isoformat()",
        f"{SCRIPT_PATH} : date du jour",
    )

    print("✔ M4 : neutralisation des traces datetime conforme")


def test_m4_resets_cycle_artifacts() -> None:
    if SCRIPT_PATH is None:
        return

    require_contains(
        SCRIPT_TEXT,
        "input_number.set_value",
        f"{SCRIPT_PATH} : service neutralisation input_number",
    )
    require_contains(
        SCRIPT_TEXT,
        "input_number.aeration_delta_t_utilise",
        f"{SCRIPT_PATH} : reset DeltaT utilisé",
    )
    require_regex(
        SCRIPT_TEXT,
        r"input_number\.aeration_delta_t_utilise.*?value\s*:\s*0",
        f"{SCRIPT_PATH} : aeration_delta_t_utilise remis à 0",
    )

    print("✔ M4 : neutralisation des artefacts de cycle conforme")


def test_m4_disarms_pipeline_and_suspension() -> None:
    if SCRIPT_PATH is None:
        return

    require_contains(
        SCRIPT_TEXT,
        "input_boolean.aeration_pipeline_arme",
        f"{SCRIPT_PATH} : désarmement pipeline",
    )
    require_contains(
        SCRIPT_TEXT,
        "input_boolean.aeration_suspension_active",
        f"{SCRIPT_PATH} : remise off suspension",
    )

    require_regex(
        SCRIPT_TEXT,
        r"input_boolean\.turn_off.*?input_boolean\.aeration_pipeline_arme",
        f"{SCRIPT_PATH} : pipeline remis off",
    )
    require_regex(
        SCRIPT_TEXT,
        r"input_boolean\.turn_off.*?input_boolean\.aeration_suspension_active",
        f"{SCRIPT_PATH} : suspension remise off",
    )

    print("✔ M4 : désarmement pipeline et suspension conformes")


def test_m4_logbook_absent() -> None:
    if SCRIPT_PATH is None:
        return

    forbid_contains(
        SCRIPT_TEXT,
        "logbook.log",
        f"{SCRIPT_PATH} : logbook volontairement absent",
    )

    print("✔ M4 : absence volontaire de logbook respectée")


def test_m4_forbidden_actions_absent() -> None:
    if SCRIPT_PATH is None:
        return

    forbid_contains(SCRIPT_TEXT, "timer.start", f"{SCRIPT_PATH} : relance timer interdite")

    for call in FORBIDDEN_SCRIPT_CALLS:
        forbid_contains(SCRIPT_TEXT, call, f"{SCRIPT_PATH} : appel script amont interdit")

    for pattern in FORBIDDEN_THERMAL_PATTERNS:
        forbid_contains(SCRIPT_TEXT, pattern, f"{SCRIPT_PATH} : action thermique interdite")

    print("✔ M4 : interdits structurels respectés")


def test_m4_does_not_modify_snapshots() -> None:
    if SCRIPT_PATH is None:
        return

    forbidden_snapshot_patterns = [
        "ref_temp_",
        "t_ref",
        "T_REF",
    ]

    for pattern in forbidden_snapshot_patterns:
        forbid_contains(SCRIPT_TEXT, pattern, f"{SCRIPT_PATH} : modification snapshot T_REF interdite")

    print("✔ M4 : snapshots T_REF non modifiés")


def test_m4_transactional_closure_complete() -> None:
    if SCRIPT_PATH is None:
        return

    required_closure_markers = [
        "input_boolean.chauffage_blocage_aeration",
        "timer.aeration_blocage",
        "timer.aeration_analyse_delta_t",
        "input_datetime.chauffage_fin_blocage_aeration",
        "input_datetime.analyse_deltat_disponible",
        "input_number.aeration_delta_t_utilise",
        "input_boolean.aeration_pipeline_arme",
        "input_boolean.aeration_suspension_active",
    ]

    for marker in required_closure_markers:
        require_contains(SCRIPT_TEXT, marker, f"{SCRIPT_PATH} : clôture transactionnelle")

    print("✔ M4 : clôture transactionnelle complète")


TESTS = [
    "test_m4_script_present",
    "test_m4_script_declared",
    "test_m4_lifts_heating_block",
    "test_m4_cancels_domain_timers",
    "test_m4_neutralizes_datetime_traces",
    "test_m4_resets_cycle_artifacts",
    "test_m4_disarms_pipeline_and_suspension",
    "test_m4_logbook_absent",
    "test_m4_forbidden_actions_absent",
    "test_m4_does_not_modify_snapshots",
    "test_m4_transactional_closure_complete",
    "test_test_registry_matches_functions",
]


def test_test_registry_matches_functions() -> None:
    assert_test_registry_matches_functions()
    print("✔ registre TESTS cohérent")


def main() -> None:
    for test_name in TESTS:
        globals()[test_name]()

    if ERRORS:
        print("\n❌ CONTRAT AERATION_M4 NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print("\n✅ CONTRAT AERATION_M4 CONFORME.")


if __name__ == "__main__":
    main()