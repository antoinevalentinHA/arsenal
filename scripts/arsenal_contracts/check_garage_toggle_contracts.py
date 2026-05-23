#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : script.garage_toggle
Contrat : CONTRAT_IMPLEMENTATION_GARAGE_TOGGLE.md v1.0.0
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # racine homeassistant/

ERRORS = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if not line.lstrip().startswith("#")
    )


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


# ---------------------------------------------------------------------------
# Chemins canoniques
# ---------------------------------------------------------------------------

SCRIPT_FILE = ROOT / "10_scripts/eclairage/garage/bascule_lumiere.yaml"
BOOL_FILE   = ROOT / "05_input_booleans/eclairage/garage/etat.yaml"

# ---------------------------------------------------------------------------
# T01 — Présence du script canonique
# ---------------------------------------------------------------------------

def test_presence_script():
    """
    Vérifie que le fichier canonique du script existe et déclare
    garage_toggle (pattern clé de mapping YAML).
    """
    check(
        SCRIPT_FILE.is_file(),
        f"T01 — fichier script absent : {SCRIPT_FILE.relative_to(ROOT)}",
    )
    content = read(SCRIPT_FILE)
    check(
        bool(re.search(r"^\s*garage_toggle\s*:", content, re.MULTILINE)),
        "T01 — clé garage_toggle absente de bascule_lumiere.yaml",
    )
    ok("T01 — présence et déclaration de script.garage_toggle")


# ---------------------------------------------------------------------------
# T02 — Présence du helper d'état logique
# ---------------------------------------------------------------------------

def test_presence_boolean():
    """
    Vérifie que input_boolean.garage_light_state est déclaré
    dans son fichier canonique (pattern clé de mapping YAML).
    """
    content = read(BOOL_FILE)
    check(
        bool(re.search(r"^\s*garage_light_state\s*:", content, re.MULTILINE)),
        f"T02 — input_boolean.garage_light_state absent de {BOOL_FILE.relative_to(ROOT)}",
    )
    ok("T02 — présence de input_boolean.garage_light_state")


# ---------------------------------------------------------------------------
# T03 — I1 : button.garage_1 et button.garage_2 uniquement dans le script canonique
# ---------------------------------------------------------------------------

def test_button_exclusivity():
    """
    Vérifie que button.garage_1 et button.garage_2 ne sont appelés
    (hors commentaires) nulle part ailleurs que dans bascule_lumiere.yaml.

    Scope : arborescence entière hors bascule_lumiere.yaml.
    Justification : I1 pose que le script est l'unique point d'exécution physique.
    Tout appel direct à button.garage_X depuis un autre fichier violerait I1.
    """
    for yaml_file in ROOT.rglob("*.yaml"):
        if not yaml_file.is_file():
            continue
        if yaml_file.resolve() == SCRIPT_FILE.resolve():
            continue
        cleaned = strip_comments(read(yaml_file))
        for btn in ("button.garage_1", "button.garage_2"):
            if btn in cleaned:
                check(
                    False,
                    f"T03 — {btn} référencé (hors commentaires) dans "
                    f"{yaml_file.relative_to(ROOT)} (violation I1)",
                )
    ok("T03 — button.garage_1/2 exclusifs au script canonique (I1)")


# ---------------------------------------------------------------------------
# T04 — I3 : les deux actionneurs sont référencés dans le script
# ---------------------------------------------------------------------------

def test_both_buttons_present():
    """
    Vérifie que bascule_lumiere.yaml référence bien button.garage_1
    et button.garage_2 (les deux branches de la table I3 doivent exister).
    """
    content = read(SCRIPT_FILE)
    for btn in ("button.garage_1", "button.garage_2"):
        check(
            btn in content,
            f"T04 — {btn} absent de bascule_lumiere.yaml (table I3 incomplète)",
        )
    ok("T04 — présence des deux actionneurs dans le script (I3)")


# ---------------------------------------------------------------------------
# T05 — I4 : le script écrit input_boolean.garage_light_state
# ---------------------------------------------------------------------------

def test_script_writes_boolean():
    """
    Vérifie que bascule_lumiere.yaml contient une écriture sur
    input_boolean.garage_light_state (coprésence service turn_on/turn_off
    et entité cible dans une fenêtre de 300 chars), hors commentaires.

    Garantit que l'étape 4 (mise à jour état logique) est bien implémentée.
    """
    cleaned = strip_comments(read(SCRIPT_FILE))
    pattern = re.compile(
        r"input_boolean\.turn_(?:on|off).{0,300}garage_light_state"
        r"|garage_light_state.{0,300}input_boolean\.turn_(?:on|off)",
        re.DOTALL,
    )
    check(
        bool(pattern.search(cleaned)),
        "T05 — aucune écriture sur input_boolean.garage_light_state dans bascule_lumiere.yaml (I4 absent)",
    )
    ok("T05 — écriture sur input_boolean.garage_light_state présente (I4)")


# ---------------------------------------------------------------------------
# T06 — I5 : absence de lecture post-action dans le script
# ---------------------------------------------------------------------------

def test_no_post_action_read():
    """
    Vérifie que bascule_lumiere.yaml n'utilise pas last_changed
    ni last_updated (indicateurs de validation post-action interdits par I5).
    Hors commentaires.
    """
    cleaned = strip_comments(read(SCRIPT_FILE))
    for forbidden in ("last_changed", "last_updated"):
        check(
            forbidden not in cleaned,
            f"T06 — '{forbidden}' présent dans bascule_lumiere.yaml (validation post-action — violation I5)",
        )
    ok("T06 — absence de lecture post-action dans le script (I5)")


# ---------------------------------------------------------------------------
# T07 — I6 : mode single déclaré dans le script
# ---------------------------------------------------------------------------

def test_mode_single():
    """
    Vérifie que bascule_lumiere.yaml déclare mode: single,
    condition nécessaire à la garantie d'atomicité logique (I6).
    """
    content = read(SCRIPT_FILE)
    check(
        bool(re.search(r"^\s*mode\s*:\s*single\b", content, re.MULTILINE)),
        "T07 — mode: single absent de bascule_lumiere.yaml (atomicité I6 non garantie)",
    )
    ok("T07 — mode: single déclaré dans le script (I6)")


# ---------------------------------------------------------------------------
# T08 — Absence de retry dans le script (I5)
# ---------------------------------------------------------------------------

def test_no_retry():
    """
    Vérifie que bascule_lumiere.yaml ne contient pas de pattern de retry
    (repeat:, retry:, until:) hors commentaires.
    Ces patterns constitueraient une re-tentative automatique interdite par I5.
    """
    cleaned = strip_comments(read(SCRIPT_FILE))
    for forbidden in (r"^\s*repeat\s*:", r"^\s*retry\s*:", r"^\s*until\s*:"):
        if re.search(forbidden, cleaned, re.MULTILINE):
            check(
                False,
                f"T08 — pattern de retry détecté dans bascule_lumiere.yaml (violation I5)",
            )
    ok("T08 — absence de retry dans le script (I5)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_presence_script,
    test_presence_boolean,
    test_button_exclusivity,
    test_both_buttons_present,
    test_script_writes_boolean,
    test_no_post_action_read,
    test_mode_single,
    test_no_retry,
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Contrat script.garage_toggle\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT GARAGE_TOGGLE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT GARAGE_TOGGLE CONFORME")
