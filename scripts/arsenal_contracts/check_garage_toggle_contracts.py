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
# T03 — I1 : switch.lumiere_garage uniquement dans le script canonique
# ---------------------------------------------------------------------------

def test_switch_exclusivity():
    """
    Vérifie que switch.lumiere_garage n'est pas piloté (hors commentaires)
    depuis un fichier autre que bascule_lumiere.yaml.

    Runtime : l'actionneur physique est switch.lumiere_garage (module Zigbee).
    Le contrat d'implémentation documentait une architecture button.garage_X
    désormais obsolète.

    Scope : 10_scripts/ et 11_automations/ — les domaines susceptibles
    d'écrire un switch. Lovelace et template sensors sont exclus (lecture seule).

    Écrivains légitimes hors script canonique : aucun identifié dans le runtime.
    """
    # Une écriture réelle sur switch.lumiere_garage requiert :
    #   service: switch.turn_on/off
    #   target:
    #     entity_id: switch.lumiere_garage
    #
    # On détecte le pattern en cherchant `lumiere_garage` uniquement
    # dans les lignes qui suivent un `target:` lui-même consécutif
    # au service — ce qui exclut les lectures passives en condition:
    # (ex. entree/automatique.yaml lit lumiere_garage en condition,
    # puis appelle switch.turn_on sur switch.lumiere_entree plus bas).
    write_service = re.compile(r"switch\.turn_(?:on|off)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"lumiere_garage")

    scan_roots = [ROOT / "10_scripts", ROOT / "11_automations"]
    for scan_root in scan_roots:
        for yaml_file in scan_root.rglob("*.yaml"):
            if not yaml_file.is_file():
                continue
            if yaml_file.resolve() == SCRIPT_FILE.resolve():
                continue
            lines = [
                line for line in read(yaml_file).splitlines()
                if not line.lstrip().startswith("#")
            ]
            for i, line in enumerate(lines):
                if not write_service.search(line):
                    continue
                # Cherche un bloc target: dans les 2 lignes qui suivent
                for j in range(i + 1, min(i + 3, len(lines))):
                    if target_kw.search(lines[j]):
                        # Cherche lumiere_garage dans les 3 lignes du bloc target:
                        for k in range(j + 1, min(j + 4, len(lines))):
                            if target_entity.search(lines[k]):
                                check(
                                    False,
                                    f"T03 — pilotage de switch.lumiere_garage détecté dans "
                                    f"{yaml_file.relative_to(ROOT)} ligne {k+1} (violation I1)",
                                )
                        break
    ok("T03 — switch.lumiere_garage exclusif au script canonique (I1)")


# ---------------------------------------------------------------------------
# T04 — I3 : les deux branches de bascule sont présentes dans le script
# ---------------------------------------------------------------------------

def test_both_branches_present():
    """
    Vérifie que bascule_lumiere.yaml implémente bien les deux branches
    de la table I3 (OFF→ON et ON→OFF) via switch.turn_on et switch.turn_off
    sur switch.lumiere_garage.

    Runtime : actionneur = switch.lumiere_garage (Zigbee).
    """
    content = read(SCRIPT_FILE)
    for service in ("switch.turn_on", "switch.turn_off"):
        check(
            service in content,
            f"T04 — {service} absent de bascule_lumiere.yaml (branche I3 manquante)",
        )
    ok("T04 — présence des deux branches switch dans le script (I3)")


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
    test_switch_exclusivity,
    test_both_branches_present,
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
