#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Éclairage / Entrée
Contrat : CONTRAT_ECLAIRAGE_ENTREE.md v1.0.0
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


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


# ---------------------------------------------------------------------------
# T01 — Présence des entités canoniques (helpers)
# ---------------------------------------------------------------------------

def test_presence_helpers():
    """
    Vérifie que les trois helpers persistants du domaine sont déclarés
    dans leurs fichiers canoniques (pattern clé de mapping YAML).
    """
    cases = [
        (
            ROOT / "05_input_booleans/eclairage/entree_auto.yaml",
            r"^\s*entree_auto_light\s*:",
            "input_boolean.entree_auto_light",
        ),
        (
            ROOT / "03_input_numbers/eclairage/duree_absence/entree.yaml",
            r"^\s*duree_absence_entree\s*:",
            "input_number.duree_absence_entree",
        ),
        (
            ROOT / "07_input_datetimes/eclairage/entree_deadline.yaml",
            r"^\s*entree_extinction_deadline\s*:",
            "input_datetime.entree_extinction_deadline",
        ),
    ]
    for path, pattern, entity in cases:
        content = read(path)
        check(
            bool(re.search(pattern, content, re.MULTILINE)),
            f"T01 — {entity} absent de {path.relative_to(ROOT)}",
        )
    ok("T01 — présence helpers canoniques")


# ---------------------------------------------------------------------------
# T02 — Présence du capteur N2 dans son fichier canonique
# ---------------------------------------------------------------------------

def test_presence_n2():
    """
    Vérifie que binary_sensor.mouvement_entree (N2) est déclaré
    dans le fichier d'agrégats via unique_id (template sensor).
    """
    path = ROOT / "12_template_sensors/mouvements/capteurs_agreges.yaml"
    content = read(path)
    check(
        bool(re.search(r"unique_id\s*:\s*mouvement_entree\b", content)),
        f"T02 — binary_sensor.mouvement_entree (N2) absent de {path.relative_to(ROOT)}",
    )
    ok("T02 — présence binary_sensor.mouvement_entree (N2)")


# ---------------------------------------------------------------------------
# T03 — Présence des trois fichiers d'automations du domaine
# ---------------------------------------------------------------------------

def test_presence_automations():
    """
    Vérifie que les trois fichiers d'automations du domaine existent.
    """
    domain_dir = ROOT / "11_automations/eclairage/entree"
    for filename in ("automatique.yaml", "ecriture_deadline.yaml", "extinction.yaml"):
        path = domain_dir / filename
        check(
            path.is_file(),
            f"T03 — fichier d'automation manquant : {path.relative_to(ROOT)}",
        )
    ok("T03 — présence des fichiers d'automations du domaine")


# ---------------------------------------------------------------------------
# T04 — IDs d'automations canoniques (I4 : séparation allumage / extinction)
# ---------------------------------------------------------------------------

def test_automation_ids():
    """
    Vérifie que chaque fichier d'automation déclare l'ID attendu par le contrat,
    et qu'aucun fichier ne porte deux IDs du domaine (séparation stricte).

    IDs contractuels :
      automatique.yaml     → 10070000000026
      ecriture_deadline.yaml → 10070000000032
      extinction.yaml      → 10070000000027
    """
    domain_dir = ROOT / "11_automations/eclairage/entree"
    expected = {
        "automatique.yaml": "10070000000026",
        "ecriture_deadline.yaml": "10070000000032",
        "extinction.yaml": "10070000000027",
    }
    all_ids = set(expected.values())

    for filename, expected_id in expected.items():
        path = domain_dir / filename
        if not path.is_file():
            continue  # déjà couvert par T03
        content = read(path)

        # ID attendu présent (contenu brut — l'ID propre doit y figurer)
        check(
            bool(re.search(rf"\b{re.escape(expected_id)}\b", content)),
            f"T04 — ID {expected_id} absent de {filename}",
        )

        # Aucun autre ID du domaine dans les lignes non-commentaires (séparation I4).
        # Les headers Arsenal mentionnent légitimement les IDs amont/aval en commentaire ;
        # seule une occurrence hors commentaire constitue une violation.
        cleaned = "\n".join(
            line for line in content.splitlines()
            if not line.lstrip().startswith("#")
        )
        for other_id in all_ids - {expected_id}:
            check(
                not bool(re.search(rf"\b{re.escape(other_id)}\b", cleaned)),
                f"T04 — ID {other_id} trouvé (hors commentaires) dans {filename} "
                f"(violation I4 : séparation allumage/extinction)",
            )

    ok("T04 — IDs d'automations et séparation allumage/extinction (I4)")


# ---------------------------------------------------------------------------
# T05 — Consommation N2 exclusive dans les automations du domaine (I3)
# ---------------------------------------------------------------------------

def test_no_n0_n1_in_domain():
    """
    Vérifie qu'aucune automation du domaine ne référence N0 ou N1 :
      N0 : binary_sensor.capteur_mouvements_entree_occupancy
      N1 : binary_sensor.mouvement_entree_1

    Scope : 11_automations/eclairage/entree/ uniquement.
    Les commentaires (#) sont inclus dans le scan volontairement :
    leur présence dans un bloc d'action constituerait une anomalie
    de documentation, mais la violation réelle est la présence
    dans entity_id: ou trigger/condition entity_id:.
    On cible donc les occurrences hors contexte de commentaire.
    """
    domain_dir = ROOT / "11_automations/eclairage/entree"
    forbidden = {
        "N0": "capteur_mouvements_entree_occupancy",
        "N1": "mouvement_entree_1",
    }

    for yaml_file in domain_dir.glob("*.yaml"):
        if not yaml_file.is_file():
            continue
        content = read(yaml_file)
        lines = content.splitlines()
        for lineno, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue  # ligne de commentaire pure — ignorée
            for level, fragment in forbidden.items():
                if fragment in line:
                    check(
                        False,
                        f"T05 — consommation {level} ({fragment}) dans "
                        f"{yaml_file.name}:{lineno} (violation I3)",
                    )

    ok("T05 — absence de N0/N1 dans les automations du domaine (I3)")


# ---------------------------------------------------------------------------
# T06 — Absence d'écriture sur entree_extinction_deadline hors ecriture_deadline.yaml (I5)
# ---------------------------------------------------------------------------

def test_deadline_writer_exclusivity():
    """
    Vérifie que seul ecriture_deadline.yaml écrit input_datetime.entree_extinction_deadline.

    Une écriture est détectée par la coprésence (dans une fenêtre de 300 chars) de :
      - le service input_datetime.set_datetime ou input_datetime.set_value
      - la cible entree_extinction_deadline

    Scope : 11_automations/eclairage/entree/*.yaml, hors ecriture_deadline.yaml.
    """
    domain_dir = ROOT / "11_automations/eclairage/entree"
    canonical_writer = "ecriture_deadline.yaml"

    for yaml_file in domain_dir.glob("*.yaml"):
        if not yaml_file.is_file():
            continue
        if yaml_file.name == canonical_writer:
            continue
        content = read(yaml_file)
        # Fenêtre glissante : service datetime + cible dans 300 chars
        pattern = re.compile(
            r"input_datetime\.set_(?:datetime|value).{0,300}entree_extinction_deadline"
            r"|entree_extinction_deadline.{0,300}input_datetime\.set_(?:datetime|value)",
            re.DOTALL,
        )
        check(
            not bool(pattern.search(content)),
            f"T06 — écriture sur entree_extinction_deadline dans {yaml_file.name} "
            f"(seul ecriture_deadline.yaml est autorisé — I5)",
        )

    ok("T06 — exclusivité de l'écriture sur entree_extinction_deadline (I5)")


# ---------------------------------------------------------------------------
# T07 — automatique.yaml n'écrit pas entree_extinction_deadline (§6 Interdictions)
# ---------------------------------------------------------------------------

def test_automatique_no_deadline_write():
    """
    Vérifie que automatique.yaml ne modifie pas input_datetime.entree_extinction_deadline.
    Complément de T06, scoped explicitement sur l'automation d'allumage.
    """
    path = ROOT / "11_automations/eclairage/entree/automatique.yaml"
    content = read(path)
    pattern = re.compile(
        r"input_datetime\.set_(?:datetime|value).{0,300}entree_extinction_deadline"
        r"|entree_extinction_deadline.{0,300}input_datetime\.set_(?:datetime|value)",
        re.DOTALL,
    )
    check(
        not bool(pattern.search(content)),
        "T07 — automatique.yaml modifie entree_extinction_deadline (interdit §6)",
    )
    ok("T07 — automatique.yaml n'écrit pas entree_extinction_deadline (§6)")


# ---------------------------------------------------------------------------
# T08 — ecriture_deadline.yaml n'allume ni n'éteint switch.lumiere_entree (§7.1 Interdictions)
# ---------------------------------------------------------------------------

def test_deadline_writer_no_switch_action():
    """
    Vérifie que ecriture_deadline.yaml ne pilote pas switch.lumiere_entree.

    Une action de pilotage est détectée par la coprésence (300 chars) de :
      switch.turn_on / switch.turn_off  ET  lumiere_entree
    hors lignes de commentaires.
    """
    path = ROOT / "11_automations/eclairage/entree/ecriture_deadline.yaml"
    if not path.is_file():
        return
    content = read(path)

    # Retirer les lignes de commentaires pour éviter les faux positifs
    cleaned = "\n".join(
        line for line in content.splitlines() if not line.lstrip().startswith("#")
    )

    pattern = re.compile(
        r"switch\.turn_(?:on|off).{0,300}lumiere_entree"
        r"|lumiere_entree.{0,300}switch\.turn_(?:on|off)",
        re.DOTALL,
    )
    check(
        not bool(pattern.search(cleaned)),
        "T08 — ecriture_deadline.yaml pilote switch.lumiere_entree (interdit §7.1)",
    )
    ok("T08 — ecriture_deadline.yaml ne pilote pas switch.lumiere_entree (§7.1)")


# ---------------------------------------------------------------------------
# T09 — extinction.yaml n'allume pas switch.lumiere_entree (§7.2 Interdictions)
# ---------------------------------------------------------------------------

def test_extinction_no_turn_on():
    """
    Vérifie que extinction.yaml ne contient pas d'action switch.turn_on
    ciblant switch.lumiere_entree (seul switch.turn_off est autorisé).
    """
    path = ROOT / "11_automations/eclairage/entree/extinction.yaml"
    if not path.is_file():
        return
    content = read(path)

    cleaned = "\n".join(
        line for line in content.splitlines() if not line.lstrip().startswith("#")
    )

    pattern = re.compile(
        r"switch\.turn_on.{0,300}lumiere_entree"
        r"|lumiere_entree.{0,300}switch\.turn_on",
        re.DOTALL,
    )
    check(
        not bool(pattern.search(cleaned)),
        "T09 — extinction.yaml contient switch.turn_on sur lumiere_entree (interdit §7.2)",
    )
    ok("T09 — extinction.yaml n'allume pas switch.lumiere_entree (§7.2)")


# ---------------------------------------------------------------------------
# T10 — Absence de `for:` comme causalité métier dans ecriture_deadline.yaml (I5 / §7.1)
# ---------------------------------------------------------------------------

def test_no_for_in_deadline_writer():
    """
    Vérifie que ecriture_deadline.yaml n'utilise pas `for:` dans un bloc trigger
    ou condition comme substitut de la deadline persistée.

    La présence de `for:` dans ce fichier est un signal d'alarme contractuel (I5).
    Les commentaires sont exclus.
    """
    path = ROOT / "11_automations/eclairage/entree/ecriture_deadline.yaml"
    if not path.is_file():
        return
    content = read(path)

    for lineno, line in enumerate(content.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if re.search(r"^\s+for\s*:", line):
            ERRORS.append(
                f"T10 — `for:` détecté ligne {lineno} dans ecriture_deadline.yaml "
                f"(causalité temporelle non persistée — violation I5)"
            )

    ok("T10 — absence de `for:` dans ecriture_deadline.yaml (I5)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_presence_helpers,
    test_presence_n2,
    test_presence_automations,
    test_automation_ids,
    test_no_n0_n1_in_domain,
    test_deadline_writer_exclusivity,
    test_automatique_no_deadline_write,
    test_deadline_writer_no_switch_action,
    test_extinction_no_turn_on,
    test_no_for_in_deadline_writer,
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Contrat Éclairage / Entrée\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECLAIRAGE_ENTREE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECLAIRAGE_ENTREE CONFORME")
