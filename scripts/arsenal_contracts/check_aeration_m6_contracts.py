#!/usr/bin/env python3
# ==========================================================
# 🧠 ARSENAL — VALIDATION CONTRACTUELLE
#     Aération M6 — Réfermeture après réouverture
# ==========================================================

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

DOMAIN = "AERATION_M6"

SCRIPT_PATH = ROOT / "10_scripts" / "aeration" / "m6_refermeture.yaml"

SCRIPT_KEY = "aeration_m6_refermeture"

INPUT_DATETIME_FIN_BLOCAGE = "input_datetime.chauffage_fin_blocage_aeration"
INPUT_DATETIME_ANALYSE_DELTAT = "input_datetime.analyse_deltat_disponible"

TIMER_BLOCAGE = "timer.aeration_blocage"
TIMER_ANALYSE_DELTAT = "timer.aeration_analyse_delta_t"

SUSPENSION_ACTIVE = "input_boolean.aeration_suspension_active"
BLOCAGE_AERATION = "input_boolean.chauffage_blocage_aeration"
PIPELINE_ARME = "input_boolean.aeration_pipeline_arme"

FORBIDDEN_SCRIPT_TARGETS = [
    "script.aeration_m3",
    "script.aeration_m4",
]

ERRORS = []


def read_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def uncommented(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


def fail(message: str) -> None:
    ERRORS.append(message)


def ok(message: str) -> None:
    print(f"✔ {message}")


def require_file(path: Path, label: str) -> str:
    if not path.is_file():
        fail(f"{label} absent : {path}")
        return ""
    ok(f"{label} présent")
    return read_file(path)


def has_mapping_key(text: str, key: str) -> bool:
    return re.search(rf"^\s*{re.escape(key)}\s*:", text, re.MULTILINE) is not None


def has_service_with_target(
    text: str,
    service: str,
    target: str,
    radius: int = 350,
) -> bool:
    service_pattern = re.compile(
        rf"(?:service|action)\s*:\s*{re.escape(service)}\b",
        re.MULTILINE,
    )

    for match in service_pattern.finditer(text):
        window = text[match.start(): match.start() + radius]
        if target in window:
            return True

    return False


def has_any_service_domain(text: str, domains: list[str]) -> bool:
    for domain in domains:
        pattern = re.compile(
            rf"(?:service|action)\s*:\s*{re.escape(domain)}\.",
            re.MULTILINE,
        )
        if pattern.search(text):
            return True
    return False


def test_script_canonique_present():
    require_file(SCRIPT_PATH, "script M6 canonique")


def test_script_declare_sous_cle_canonique():
    text = require_file(SCRIPT_PATH, "script M6 canonique")
    if not text:
        return

    if not has_mapping_key(text, SCRIPT_KEY):
        fail(f"{SCRIPT_PATH} : clé script attendue absente : {SCRIPT_KEY}")

    ok("script M6 déclaré sous clé YAML canonique")


def test_m6_relit_les_echeances_normatives():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    required = [
        INPUT_DATETIME_FIN_BLOCAGE,
        INPUT_DATETIME_ANALYSE_DELTAT,
    ]

    for entity_id in required:
        if entity_id not in text:
            fail(f"{SCRIPT_PATH} : échéance normative non relue : {entity_id}")

    ok("M6 : relecture des échéances normatives présente")


def test_m6_redemarre_les_timers_normatifs():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    required_targets = [
        TIMER_BLOCAGE,
        TIMER_ANALYSE_DELTAT,
    ]

    for timer in required_targets:
        if not has_service_with_target(text, "timer.start", timer, radius=500):
            fail(f"{SCRIPT_PATH} : timer.start attendu absent pour {timer}")

    ok("M6 : redémarrage des timers normatifs présent")


def test_m6_desactive_la_suspension_active():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    if not has_service_with_target(text, "input_boolean.turn_off", SUSPENSION_ACTIVE):
        fail(
            f"{SCRIPT_PATH} : extinction attendue absente pour {SUSPENSION_ACTIVE}"
        )

    ok("M6 : désactivation de la suspension active présente")


def test_m6_ne_modifie_pas_les_echeances_datetime():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    forbidden_targets = [
        INPUT_DATETIME_FIN_BLOCAGE,
        INPUT_DATETIME_ANALYSE_DELTAT,
    ]

    for entity_id in forbidden_targets:
        if has_service_with_target(text, "input_datetime.set_datetime", entity_id):
            fail(f"{SCRIPT_PATH} : modification interdite de {entity_id}")

    ok("M6 : échéances datetime non modifiées")


def test_m6_ne_leve_pas_le_blocage_chauffage():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    if has_service_with_target(text, "input_boolean.turn_off", BLOCAGE_AERATION):
        fail(f"{SCRIPT_PATH} : levée interdite de {BLOCAGE_AERATION}")

    ok("M6 : levée du blocage chauffage absente")


def test_m6_ne_desarme_pas_le_pipeline():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    if has_service_with_target(text, "input_boolean.turn_off", PIPELINE_ARME):
        fail(f"{SCRIPT_PATH} : désarmement interdit de {PIPELINE_ARME}")

    ok("M6 : désarmement du pipeline absent")


def test_m6_n_appelle_pas_m3_ou_m4_directement():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    for target in FORBIDDEN_SCRIPT_TARGETS:
        if target in text:
            fail(f"{SCRIPT_PATH} : appel direct interdit vers {target}")

    ok("M6 : aucun appel direct vers M3/M4")


def test_m6_n_initie_aucune_action_thermique():
    text = uncommented(require_file(SCRIPT_PATH, "script M6 canonique"))
    if not text:
        return

    forbidden_service_domains = [
        "climate",
        "water_heater",
    ]

    if has_any_service_domain(text, forbidden_service_domains):
        fail(f"{SCRIPT_PATH} : action thermique interdite détectée")

    ok("M6 : aucune action thermique directe détectée")


def test_test_registry_matches_functions():
    defined = {
        name
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    }

    listed = set(TESTS)

    missing = listed - defined
    extra = defined - listed

    if missing:
        fail(f"TESTS référence des fonctions absentes : {sorted(missing)}")

    if extra:
        fail(f"fonctions de test non référencées dans TESTS : {sorted(extra)}")

    ok("registre TESTS cohérent")


TESTS = [
    "test_script_canonique_present",
    "test_script_declare_sous_cle_canonique",
    "test_m6_relit_les_echeances_normatives",
    "test_m6_redemarre_les_timers_normatifs",
    "test_m6_desactive_la_suspension_active",
    "test_m6_ne_modifie_pas_les_echeances_datetime",
    "test_m6_ne_leve_pas_le_blocage_chauffage",
    "test_m6_ne_desarme_pas_le_pipeline",
    "test_m6_n_appelle_pas_m3_ou_m4_directement",
    "test_m6_n_initie_aucune_action_thermique",
    "test_test_registry_matches_functions",
]


def main() -> None:
    for test_name in TESTS:
        globals()[test_name]()

    if ERRORS:
        print()
        print(f"❌ CONTRAT {DOMAIN} NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print()
    print(f"✅ CONTRAT {DOMAIN} CONFORME.")


if __name__ == "__main__":
    main()