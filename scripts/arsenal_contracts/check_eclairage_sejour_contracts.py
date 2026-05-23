#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Éclairage / Séjour
Contrat : CONTRAT_ECLAIRAGE_SEJOUR.md v1.0.0
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

DOMAIN_DIR   = ROOT / "11_automations/eclairage/sejour"
BOOL_FILE    = ROOT / "05_input_booleans/eclairage"        # sous-dossier à scanner
DT_FILE      = ROOT / "07_input_datetimes/eclairage/sejour_deadline.yaml"
N2_FILE      = ROOT / "12_template_sensors/mouvements/capteurs_agreges.yaml"
N1_FILE      = ROOT / "12_template_sensors/mouvements/capteurs_base.yaml"

# ---------------------------------------------------------------------------
# T01 — Présence des entités canoniques (helpers)
# ---------------------------------------------------------------------------

def test_presence_helpers():
    """
    Vérifie que les helpers persistants du domaine sont déclarés
    dans leurs fichiers canoniques (pattern clé de mapping YAML).
    """
    # input_boolean.sejour_auto_light — scan de 05_input_booleans/
    root_bool = ROOT / "05_input_booleans"
    found_bool = False
    for yaml_file in root_bool.rglob("*.yaml"):
        if not yaml_file.is_file():
            continue
        if re.search(r"^\s*sejour_auto_light\s*:", read(yaml_file), re.MULTILINE):
            found_bool = True
            break
    check(found_bool, "T01 — input_boolean.sejour_auto_light absent de 05_input_booleans/")

    # input_number.duree_absence_sejour — scan de 03_input_numbers/
    root_num = ROOT / "03_input_numbers"
    found_num = False
    for yaml_file in root_num.rglob("*.yaml"):
        if not yaml_file.is_file():
            continue
        if re.search(r"^\s*duree_absence_sejour\s*:", read(yaml_file), re.MULTILINE):
            found_num = True
            break
    check(found_num, "T01 — input_number.duree_absence_sejour absent de 03_input_numbers/")

    # input_datetime.sejour_extinction_deadline
    content = read(DT_FILE)
    check(
        bool(re.search(r"^\s*sejour_extinction_deadline\s*:", content, re.MULTILINE)),
        f"T01 — input_datetime.sejour_extinction_deadline absent de {DT_FILE.relative_to(ROOT)}",
    )
    ok("T01 — présence helpers canoniques")


# ---------------------------------------------------------------------------
# T02 — Présence du capteur N2 dans son fichier canonique
# ---------------------------------------------------------------------------

def test_presence_n2():
    """
    Vérifie que binary_sensor.mouvement_sejour (N2) est déclaré
    dans le fichier d'agrégats via unique_id (template sensor).
    """
    content = read(N2_FILE)
    check(
        bool(re.search(r"unique_id\s*:\s*mouvement_sejour\b", content)),
        f"T02 — binary_sensor.mouvement_sejour (N2) absent de {N2_FILE.relative_to(ROOT)}",
    )
    ok("T02 — présence binary_sensor.mouvement_sejour (N2)")


# ---------------------------------------------------------------------------
# T03 — Présence des trois fichiers d'automations du domaine
# ---------------------------------------------------------------------------

def test_presence_automations():
    """
    Vérifie que les trois fichiers d'automations du domaine existent.
    """
    for filename in ("on.yaml", "off.yaml", "ecriture_deadline.yaml"):
        path = DOMAIN_DIR / filename
        check(
            path.is_file(),
            f"T03 — fichier d'automation manquant : {path.relative_to(ROOT)}",
        )
    ok("T03 — présence des fichiers d'automations du domaine")


# ---------------------------------------------------------------------------
# T04 — IDs d'automations canoniques (I3 : séparation allumage / extinction)
# ---------------------------------------------------------------------------

def test_automation_ids():
    """
    Vérifie que chaque fichier d'automation déclare l'ID attendu par le contrat,
    et qu'aucun fichier ne porte deux IDs du domaine (séparation stricte, hors commentaires).

    IDs contractuels :
      on.yaml              → 10070000000014
      ecriture_deadline.yaml → 10070000000031
      off.yaml             → 10070000000015
    """
    expected = {
        "on.yaml":               "10070000000014",
        "ecriture_deadline.yaml": "10070000000031",
        "off.yaml":              "10070000000015",
    }
    all_ids = set(expected.values())

    for filename, expected_id in expected.items():
        path = DOMAIN_DIR / filename
        if not path.is_file():
            continue
        content = read(path)
        cleaned = strip_comments(content)

        check(
            bool(re.search(rf"\b{re.escape(expected_id)}\b", content)),
            f"T04 — ID {expected_id} absent de {filename}",
        )
        for other_id in all_ids - {expected_id}:
            check(
                not bool(re.search(rf"\b{re.escape(other_id)}\b", cleaned)),
                f"T04 — ID {other_id} trouvé (hors commentaires) dans {filename} "
                f"(violation I3 : séparation allumage/extinction)",
            )
    ok("T04 — IDs d'automations et séparation allumage/extinction (I3)")


# ---------------------------------------------------------------------------
# T05 — Absence de N1 dans les automations du domaine
# ---------------------------------------------------------------------------

def test_no_n1_in_domain():
    """
    Vérifie qu'aucune automation du domaine ne référence les capteurs N1 :
      mouvement_sejour_1
      mouvement_sejour_2
    Hors commentaires. Le domaine doit consommer exclusivement le N2 agrégé.
    """
    n1_fragments = ("mouvement_sejour_1", "mouvement_sejour_2")

    for yaml_file in DOMAIN_DIR.glob("*.yaml"):
        if not yaml_file.is_file():
            continue
        for lineno, line in enumerate(read(yaml_file).splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for fragment in n1_fragments:
                if fragment in line:
                    check(
                        False,
                        f"T05 — consommation N1 ({fragment}) dans "
                        f"{yaml_file.name}:{lineno} (violation I3-N2 exclusif)",
                    )
    ok("T05 — absence de N1 dans les automations du domaine")


# ---------------------------------------------------------------------------
# T06 — Exclusivité de l'écriture sur sejour_extinction_deadline (I4)
# ---------------------------------------------------------------------------

def test_deadline_writer_exclusivity():
    """
    Vérifie que seul ecriture_deadline.yaml écrit
    input_datetime.sejour_extinction_deadline dans le domaine.
    Scope : DOMAIN_DIR/*.yaml hors ecriture_deadline.yaml.
    """
    canonical_writer = "ecriture_deadline.yaml"
    pattern = re.compile(
        r"input_datetime\.set_(?:datetime|value).{0,300}sejour_extinction_deadline"
        r"|sejour_extinction_deadline.{0,300}input_datetime\.set_(?:datetime|value)",
        re.DOTALL,
    )
    for yaml_file in DOMAIN_DIR.glob("*.yaml"):
        if not yaml_file.is_file():
            continue
        if yaml_file.name == canonical_writer:
            continue
        cleaned = strip_comments(read(yaml_file))
        check(
            not bool(pattern.search(cleaned)),
            f"T06 — écriture sur sejour_extinction_deadline dans {yaml_file.name} "
            f"(seul ecriture_deadline.yaml est autorisé — I4)",
        )
    ok("T06 — exclusivité de l'écriture sur sejour_extinction_deadline (I4)")


# ---------------------------------------------------------------------------
# T07 — on.yaml n'écrit pas sejour_extinction_deadline (§5 Interdictions)
# ---------------------------------------------------------------------------

def test_on_no_deadline_write():
    """
    Vérifie que on.yaml ne modifie pas input_datetime.sejour_extinction_deadline.
    """
    path = DOMAIN_DIR / "on.yaml"
    cleaned = strip_comments(read(path))
    pattern = re.compile(
        r"input_datetime\.set_(?:datetime|value).{0,300}sejour_extinction_deadline"
        r"|sejour_extinction_deadline.{0,300}input_datetime\.set_(?:datetime|value)",
        re.DOTALL,
    )
    check(
        not bool(pattern.search(cleaned)),
        "T07 — on.yaml modifie sejour_extinction_deadline (interdit §5)",
    )
    ok("T07 — on.yaml n'écrit pas sejour_extinction_deadline (§5)")


# ---------------------------------------------------------------------------
# T08 — ecriture_deadline.yaml ne pilote pas switch.prise_lampe_sejour (§6.1)
# ---------------------------------------------------------------------------

def test_deadline_writer_no_switch_action():
    """
    Vérifie que ecriture_deadline.yaml ne pilote pas switch.prise_lampe_sejour.
    Détection via bloc target: (service + target dans 5 lignes).
    """
    path = DOMAIN_DIR / "ecriture_deadline.yaml"
    if not path.is_file():
        return
    lines = [
        line for line in read(path).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"switch\.turn_(?:on|off)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"prise_lampe_sejour")

    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        check(
                            False,
                            f"T08 — ecriture_deadline.yaml pilote switch.prise_lampe_sejour "
                            f"ligne {k+1} (interdit §6.1)",
                        )
                break
    ok("T08 — ecriture_deadline.yaml ne pilote pas switch.prise_lampe_sejour (§6.1)")


# ---------------------------------------------------------------------------
# T09 — off.yaml n'allume pas switch.prise_lampe_sejour (§6.2 Interdictions)
# ---------------------------------------------------------------------------

def test_off_no_turn_on():
    """
    Vérifie que off.yaml ne contient pas d'action switch.turn_on
    ciblant switch.prise_lampe_sejour.
    """
    path = DOMAIN_DIR / "off.yaml"
    if not path.is_file():
        return
    lines = [
        line for line in read(path).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"switch\.turn_on")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"prise_lampe_sejour")

    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        check(
                            False,
                            f"T09 — off.yaml contient switch.turn_on sur prise_lampe_sejour "
                            f"ligne {k+1} (interdit §6.2)",
                        )
                break
    ok("T09 — off.yaml n'allume pas switch.prise_lampe_sejour (§6.2)")


# ---------------------------------------------------------------------------
# T10 — off.yaml déclenche sur sejour_extinction_deadline (I4 / §6.2)
# ---------------------------------------------------------------------------

def test_off_triggers_on_deadline():
    """
    Vérifie que off.yaml déclare un trigger platform: time
    pointant sur input_datetime.sejour_extinction_deadline.
    """
    path = DOMAIN_DIR / "off.yaml"
    content = read(path)
    check(
        bool(re.search(
            r"at\s*:\s*input_datetime\.sejour_extinction_deadline",
            content,
        )),
        "T10 — trigger `at: input_datetime.sejour_extinction_deadline` absent de off.yaml (I4)",
    )
    ok("T10 — off.yaml déclenche sur sejour_extinction_deadline (I4)")


# ---------------------------------------------------------------------------
# T11 — Absence de `for:` dans ecriture_deadline.yaml (I4)
# ---------------------------------------------------------------------------

def test_no_for_in_deadline_writer():
    """
    Vérifie que ecriture_deadline.yaml n'utilise pas `for:` hors commentaires.
    """
    path = DOMAIN_DIR / "ecriture_deadline.yaml"
    if not path.is_file():
        return
    for lineno, line in enumerate(read(path).splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if re.search(r"^\s+for\s*:", line):
            ERRORS.append(
                f"T11 — `for:` détecté ligne {lineno} dans ecriture_deadline.yaml "
                f"(causalité temporelle non persistée — violation I4)"
            )
    ok("T11 — absence de `for:` dans ecriture_deadline.yaml (I4)")


# ---------------------------------------------------------------------------
# T12 — I1 : switch.prise_lampe_sejour piloté uniquement depuis le domaine
# ---------------------------------------------------------------------------

def test_switch_exclusivity():
    """
    Vérifie que switch.prise_lampe_sejour n'est piloté (écriture réelle
    via target: block) que depuis les automations du domaine sejour.

    Écrivain légitime externe connu :
      - 10_scripts/scenario_extinction_soir.yaml (script transversal)

    Scope : 10_scripts/ et 11_automations/ hors domaine sejour et hors écrivain externe.
    """
    write_service = re.compile(r"switch\.turn_(?:on|off)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"prise_lampe_sejour")

    external_writer = (ROOT / "10_scripts/scenario_extinction_soir.yaml").resolve()

    scan_roots = [ROOT / "10_scripts", ROOT / "11_automations"]
    for scan_root in scan_roots:
        for yaml_file in scan_root.rglob("*.yaml"):
            if not yaml_file.is_file():
                continue
            if yaml_file.resolve() == external_writer:
                continue
            # Exclure le domaine canonique lui-même
            try:
                yaml_file.relative_to(DOMAIN_DIR)
                continue
            except ValueError:
                pass
            lines = [
                line for line in read(yaml_file).splitlines()
                if not line.lstrip().startswith("#")
            ]
            for i, line in enumerate(lines):
                if not write_service.search(line):
                    continue
                for j in range(i + 1, min(i + 3, len(lines))):
                    if target_kw.search(lines[j]):
                        for k in range(j + 1, min(j + 4, len(lines))):
                            if target_entity.search(lines[k]):
                                check(
                                    False,
                                    f"T12 — pilotage de switch.prise_lampe_sejour détecté dans "
                                    f"{yaml_file.relative_to(ROOT)} ligne {k+1} (violation I1)",
                                )
                        break
    ok("T12 — switch.prise_lampe_sejour exclusif au domaine séjour (I1)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_presence_helpers,
    test_presence_n2,
    test_presence_automations,
    test_automation_ids,
    test_no_n1_in_domain,
    test_deadline_writer_exclusivity,
    test_on_no_deadline_write,
    test_deadline_writer_no_switch_action,
    test_off_no_turn_on,
    test_off_triggers_on_deadline,
    test_no_for_in_deadline_writer,
    test_switch_exclusivity,
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Contrat Éclairage / Séjour\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECLAIRAGE_SEJOUR NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECLAIRAGE_SEJOUR CONFORME")
