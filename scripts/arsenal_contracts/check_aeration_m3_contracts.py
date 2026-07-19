#!/usr/bin/env python3
# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
#     Aération — M3 — Analyse DeltaT
#     Contrat (source normative) : 00_documentation_arsenal/contrats/aeration_blocage_chauffage/m3_analyse_delta_t/
# ==========================================================

from pathlib import Path
import re
import sys


ROOT = Path.cwd()
ERRORS: list[str] = []


SCRIPT_FILES = {
    "orchestrateur": "m3_0_analyse_deltat.yaml",
    "prolonger": "m3_1_prolonger_blocage.yaml",
    "maintenir": "m3_2_maintenir_blocage.yaml",
}


DELTAT_SENSORS = [
    "sensor.deltat_entree",
    "sensor.deltat_sejour",
    "sensor.deltat_chambre_enfants",
    "sensor.deltat_chambre_matthieu",
    "sensor.deltat_chambre_parents",
    "sensor.deltat_palier",
]


M3_FALLBACKS = [
    "float(0.4)",
    "float(0.8)",
    "float(1.2)",
    "float(60)",
    "float(120)",
    "float(180)",
]


FORBIDDEN_THERMAL_PATTERNS = [
    "climate.",
    "water_heater.",
    "switch.",
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


def load_scripts() -> dict[str, tuple[Path, str]]:
    loaded = {}

    for key, filename in SCRIPT_FILES.items():
        path = find_file(filename)
        if path is None:
            ERRORS.append(f"script M3 introuvable : {filename}")
            continue
        loaded[key] = (path, read(path))

    return loaded


SCRIPTS = load_scripts()


def test_m3_scripts_present() -> None:
    for key, filename in SCRIPT_FILES.items():
        if key not in SCRIPTS:
            ERRORS.append(f"script M3 manquant : {filename}")

    if not ERRORS:
        print("✔ scripts M3 canoniques présents")


def test_script_keys_declared() -> None:
    expected = {
        "orchestrateur": "aeration_m3_analyse_deltat",
        "prolonger": "aeration_m3_prolonger_blocage",
        "maintenir": "aeration_m3_maintenir_blocage",
    }

    for key, script_id in expected.items():
        if key not in SCRIPTS:
            continue
        path, text = SCRIPTS[key]
        require_regex(
            text,
            rf"^\s*{re.escape(script_id)}\s*:",
            f"{path} : déclaration script",
        )

    print("✔ scripts M3 déclarés sous clé YAML canonique")


def test_orchestrator_deltat_sources() -> None:
    if "orchestrateur" not in SCRIPTS:
        return

    path, text = SCRIPTS["orchestrateur"]

    for sensor in DELTAT_SENSORS:
        require_regex(
            text,
            rf"states\(['\"]{re.escape(sensor)}['\"]\)\s*\|\s*float\(0\)",
            f"{path} : source DeltaT",
        )

    require_contains(text, "] | max", f"{path} : calcul delta_max")
    print("✔ orchestrateur : sources DeltaT et conversion float(0) conformes")


def test_orchestrator_diagnostic_publication() -> None:
    if "orchestrateur" not in SCRIPTS:
        return

    path, text = SCRIPTS["orchestrateur"]

    require_contains(
        text,
        "input_number.delta_t_max_decisionnel_aeration",
        f"{path} : publication diagnostic delta_max",
    )
    require_contains(
        text,
        "input_number.aeration_delta_t_utilise",
        f"{path} : mémoire monotone delta_t_utilise",
    )
    require_regex(
        text,
        r"input_number\.aeration_delta_t_utilise.*?\]\s*\|\s*max",
        f"{path} : mise à jour monotone delta_t_utilise",
    )

    print("✔ orchestrateur : publications diagnostic conformes")


def test_orchestrator_routing() -> None:
    if "orchestrateur" not in SCRIPTS:
        return

    path, text = SCRIPTS["orchestrateur"]

    require_regex(
        text,
        r"prolongation_heures\s*\|\s*float\(0\)\s*>\s*0",
        f"{path} : condition routage prolongation",
    )
    require_contains(
        text,
        "script.aeration_m3_prolonger_blocage",
        f"{path} : appel prolongation",
    )
    require_contains(
        text,
        "script.aeration_m3_maintenir_blocage",
        f"{path} : appel maintien",
    )
    require_contains(text, "delta_max:", f"{path} : transmission delta_max")
    require_contains(text, "prolongation_heures:", f"{path} : transmission prolongation_heures")

    print("✔ orchestrateur : routage prolongation / maintien conforme")


def test_orchestrator_contractual_fallbacks() -> None:
    if "orchestrateur" not in SCRIPTS:
        return

    path, text = SCRIPTS["orchestrateur"]

    for fallback in M3_FALLBACKS:
        require_contains(text, fallback, f"{path} : fallback contractuel")

    print("✔ orchestrateur : fallbacks contractuels présents")


def test_orchestrator_forbidden_actions_absent() -> None:
    if "orchestrateur" not in SCRIPTS:
        return

    path, text = SCRIPTS["orchestrateur"]

    forbid_contains(text, "input_boolean.turn_off", f"{path} : levée blocage interdite")
    forbid_contains(text, "input_boolean.turn_on", f"{path} : écriture booléen métier interdite")
    forbid_contains(text, "aeration_pipeline_arme", f"{path} : modification pipeline interdite")
    forbid_contains(text, "timer.start", f"{path} : pilotage timer interdit dans orchestrateur")
    forbid_contains(text, "timer.cancel", f"{path} : annulation timer interdite dans orchestrateur")

    for pattern in FORBIDDEN_THERMAL_PATTERNS:
        forbid_contains(text, pattern, f"{path} : action thermique interdite")

    print("✔ orchestrateur : interdits structurels respectés")


def test_prolongation_monotone_trace_and_timer() -> None:
    if "prolonger" not in SCRIPTS:
        return

    path, text = SCRIPTS["prolonger"]

    require_contains(text, "input_datetime.chauffage_fin_blocage_aeration", f"{path} : trace deadline")
    require_contains(text, "as_datetime", f"{path} : lecture datetime")
    require_contains(text, "fin_blocage_actuelle_valide", f"{path} : validité deadline actuelle")
    require_regex(
        text,
        r"fin_blocage_actuelle\s*>\s*fin_blocage_proposee",
        f"{path} : conservation échéance la plus lointaine",
    )

    require_contains(text, "timer.aeration_blocage", f"{path} : timer blocage")
    require_contains(text, "remaining", f"{path} : lecture remaining")
    require_contains(text, "blocage_remaining_s", f"{path} : conversion remaining")
    require_contains(text, "blocage_cible_s", f"{path} : durée cible")
    require_contains(text, "blocage_start_s", f"{path} : durée start monotone")
    require_regex(
        text,
        r"blocage_start_s\s*>\s*blocage_remaining_s",
        f"{path} : démarrage seulement si prolongation effective",
    )
    require_contains(text, "timer.start", f"{path} : prolongation timer")
    require_contains(text, "duration:", f"{path} : durée timer")

    print("✔ prolongation : monotonie deadline / remaining conforme")


def test_prolongation_forbidden_actions_absent() -> None:
    if "prolonger" not in SCRIPTS:
        return

    path, text = SCRIPTS["prolonger"]

    forbid_contains(text, "timer.cancel", f"{path} : annulation timer interdite")
    forbid_contains(text, "input_boolean.turn_off", f"{path} : levée blocage interdite")
    forbid_contains(text, "input_boolean.turn_on", f"{path} : écriture booléen métier interdite")
    forbid_contains(text, "aeration_pipeline_arme", f"{path} : modification pipeline interdite")

    for pattern in FORBIDDEN_THERMAL_PATTERNS:
        forbid_contains(text, pattern, f"{path} : action thermique interdite")

    print("✔ prolongation : interdits structurels respectés")


def test_maintien_neutralisation() -> None:
    if "maintenir" not in SCRIPTS:
        return

    path, text = SCRIPTS["maintenir"]

    require_contains(text, "input_datetime.set_datetime", f"{path} : neutralisation datetime")
    require_contains(text, "input_datetime.analyse_deltat_disponible", f"{path} : cible neutralisation")
    require_contains(text, "00:00:00", f"{path} : sentinelle minuit")
    require_contains(text, "now().date().isoformat()", f"{path} : jour courant")

    print("✔ maintien : neutralisation analyse DeltaT conforme")


def test_maintien_forbidden_actions_absent() -> None:
    if "maintenir" not in SCRIPTS:
        return

    path, text = SCRIPTS["maintenir"]

    forbid_contains(text, "timer.start", f"{path} : relance timer interdite")
    forbid_contains(text, "timer.cancel", f"{path} : annulation timer interdite")
    forbid_contains(text, "timer.aeration_blocage", f"{path} : modification timer blocage interdite")
    forbid_contains(text, "chauffage_blocage_aeration", f"{path} : modification blocage interdite")
    forbid_contains(text, "aeration_pipeline_arme", f"{path} : modification pipeline interdite")
    forbid_contains(text, "input_boolean.turn_off", f"{path} : levée blocage interdite")
    forbid_contains(text, "input_boolean.turn_on", f"{path} : écriture booléen métier interdite")

    for pattern in FORBIDDEN_THERMAL_PATTERNS:
        forbid_contains(text, pattern, f"{path} : action thermique interdite")

    print("✔ maintien : interdits structurels respectés")


def test_m3_logbook_absent() -> None:
    for key, (path, text) in SCRIPTS.items():
        forbid_contains(text, "logbook.log", f"{path} : journalisation logbook volontairement absente")
        forbid_contains(text, "logbook", f"{path} : journalisation logbook volontairement absente")

    print("✔ M3 : absence volontaire de logbook respectée")


TESTS = [
    "test_m3_scripts_present",
    "test_script_keys_declared",
    "test_orchestrator_deltat_sources",
    "test_orchestrator_diagnostic_publication",
    "test_orchestrator_routing",
    "test_orchestrator_contractual_fallbacks",
    "test_orchestrator_forbidden_actions_absent",
    "test_prolongation_monotone_trace_and_timer",
    "test_prolongation_forbidden_actions_absent",
    "test_maintien_neutralisation",
    "test_maintien_forbidden_actions_absent",
    "test_m3_logbook_absent",
    "test_test_registry_matches_functions",
]


def test_test_registry_matches_functions() -> None:
    assert_test_registry_matches_functions()
    print("✔ registre TESTS cohérent")


def main() -> None:
    for test_name in TESTS:
        globals()[test_name]()

    if ERRORS:
        print("\n❌ CONTRAT AERATION_M3 NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print("\n✅ CONTRAT AERATION_M3 CONFORME.")


if __name__ == "__main__":
    main()