#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Éclairage / Jardin
Contrat : CONTRAT_ECLAIRAGE_JARDIN.md — Arsenal v14.x
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

DOMAIN_MATIN = ROOT / "11_automations/eclairage/jardin/matin"
DOMAIN_SOIR  = ROOT / "11_automations/eclairage/jardin/soir"
SCRIPTS_DIR  = ROOT / "10_scripts/eclairage/jardin"

# Fichiers canoniques — helpers
BOOL_MATIN   = ROOT / "05_input_booleans/eclairage"   # sous-dossier à confirmer via pattern
BOOL_SOIR    = ROOT / "05_input_booleans/eclairage"

DT_SOIR_EXT  = ROOT / "07_input_datetimes/eclairage/jardin_soir_extinction_deadline.yaml"
DT_SEJOUR    = ROOT / "07_input_datetimes/eclairage/sejour_inactivite_deadline.yaml"

SENSOR_OFF   = ROOT / "12_template_sensors/eclairage/jardin/soir/off.yaml"

# Écrivains légitimes sur switch.prise_jardin hors scripts canoniques
EXTERNAL_WRITERS = {
    (ROOT / "11_automations/boutons/cuisine.yaml").resolve(),
    (ROOT / "10_scripts/scenario_extinction_soir.yaml").resolve(),
}

# ---------------------------------------------------------------------------
# T01 — Présence des helpers d'autorisation utilisateur
# ---------------------------------------------------------------------------

def test_presence_booleans():
    """
    Vérifie que les deux input_boolean d'autorisation utilisateur
    sont déclarés quelque part dans 05_input_booleans/ (pattern clé mapping).
    Les entity IDs runtime sont :
      input_boolean.auto_lumiere_jardin_matin
      input_boolean.auto_lumiere_jardin_soir
    """
    root_bool = ROOT / "05_input_booleans"
    targets = {
        "auto_lumiere_jardin_matin": False,
        "auto_lumiere_jardin_soir":  False,
    }
    for yaml_file in root_bool.rglob("*.yaml"):
        if not yaml_file.is_file():
            continue
        content = read(yaml_file)
        for key in list(targets):
            if re.search(rf"^\s*{re.escape(key)}\s*:", content, re.MULTILINE):
                targets[key] = True
    for key, found in targets.items():
        check(found, f"T01 — input_boolean.{key} absent de 05_input_booleans/")
    ok("T01 — présence des helpers d'autorisation matin/soir")


# ---------------------------------------------------------------------------
# T02 — Présence des deux deadlines persistantes
# ---------------------------------------------------------------------------

def test_presence_deadlines():
    """
    Vérifie que les deux deadlines d'extinction soir sont déclarées
    dans leurs fichiers canoniques (pattern clé mapping).
    """
    cases = [
        (
            DT_SOIR_EXT,
            r"^\s*jardin_soir_extinction_deadline\s*:",
            "input_datetime.jardin_soir_extinction_deadline",
        ),
        (
            DT_SEJOUR,
            r"^\s*jardin_sejour_inactivite_deadline\s*:",
            "input_datetime.jardin_sejour_inactivite_deadline",
        ),
    ]
    for path, pattern, entity in cases:
        content = read(path)
        check(
            bool(re.search(pattern, content, re.MULTILINE)),
            f"T02 — {entity} absent de {path.relative_to(ROOT)}",
        )
    ok("T02 — présence des deadlines persistantes soir")


# ---------------------------------------------------------------------------
# T03 — Présence du template sensor d'observabilité extinction soir
# ---------------------------------------------------------------------------

def test_presence_sensor_off():
    """
    Vérifie que binary_sensor.lumiere_jardin_soir_extinction_autorisee
    est déclaré dans son fichier canonique (pattern unique_id).
    Ce capteur est la projection d'observabilité des deux deadlines (§3).
    """
    content = read(SENSOR_OFF)
    check(
        bool(re.search(
            r"unique_id\s*:\s*lumiere_jardin_soir_extinction_autorisee\b",
            content,
        )),
        f"T03 — unique_id lumiere_jardin_soir_extinction_autorisee absent de "
        f"{SENSOR_OFF.relative_to(ROOT)}",
    )
    ok("T03 — présence du sensor d'observabilité extinction soir")


# ---------------------------------------------------------------------------
# T04 — Présence des fichiers d'automations du domaine
# ---------------------------------------------------------------------------

def test_presence_automations():
    """
    Vérifie que les fichiers d'automations canoniques du domaine existent.
    """
    expected = [
        DOMAIN_MATIN / "allumage.yaml",
        DOMAIN_SOIR  / "allumage.yaml",
        DOMAIN_SOIR  / "extinction.yaml",
        DOMAIN_SOIR  / "mouvements_sejour.yaml",
    ]
    for path in expected:
        check(
            path.is_file(),
            f"T04 — fichier d'automation manquant : {path.relative_to(ROOT)}",
        )
    ok("T04 — présence des fichiers d'automations du domaine")


# ---------------------------------------------------------------------------
# T05 — Présence des scripts canoniques du domaine
# ---------------------------------------------------------------------------

def test_presence_scripts():
    """
    Vérifie que les trois scripts de pilotage matériel existent.
    """
    for name in ("on.yaml", "off.yaml", "toggle.yaml"):
        path = SCRIPTS_DIR / name
        check(
            path.is_file(),
            f"T05 — script manquant : {path.relative_to(ROOT)}",
        )
    ok("T05 — présence des scripts canoniques jardin")


# ---------------------------------------------------------------------------
# T06 — Les deux deadlines sont lues dans le sensor d'observabilité (§3)
# ---------------------------------------------------------------------------

def test_sensor_reads_both_deadlines():
    """
    Vérifie que le template sensor off.yaml consomme bien
    les deux deadlines (jardin_soir_extinction_deadline ET
    jardin_sejour_inactivite_deadline).
    Le contrat §3 pose que ce capteur reflète l'état des deux deadlines.
    """
    content = read(SENSOR_OFF)
    for entity in (
        "jardin_soir_extinction_deadline",
        "jardin_sejour_inactivite_deadline",
    ):
        check(
            entity in content,
            f"T06 — {entity} absent du sensor off.yaml (projection incomplète §3)",
        )
    ok("T06 — sensor d'observabilité lit les deux deadlines (§3)")


# ---------------------------------------------------------------------------
# T07 — extinction.yaml déclenche sur les deux deadlines (§3 / §5)
# ---------------------------------------------------------------------------

def test_extinction_triggers_on_deadlines():
    """
    Vérifie que l'automation d'extinction soir déclare deux triggers
    platform: time pointant sur les deux deadlines persistantes.
    L'extinction causale repose sur ces deux triggers (§5).
    """
    path = DOMAIN_SOIR / "extinction.yaml"
    content = read(path)
    for entity in (
        "jardin_soir_extinction_deadline",
        "jardin_sejour_inactivite_deadline",
    ):
        check(
            bool(re.search(rf"at\s*:\s*input_datetime\.{re.escape(entity)}", content)),
            f"T07 — trigger `at: input_datetime.{entity}` absent de extinction.yaml",
        )
    ok("T07 — extinction.yaml déclenche sur les deux deadlines (§5)")


# ---------------------------------------------------------------------------
# T08 — mouvements_sejour.yaml écrit jardin_sejour_inactivite_deadline
# ---------------------------------------------------------------------------

def test_sejour_writer():
    """
    Vérifie que mouvements_sejour.yaml est bien l'automation qui écrit
    input_datetime.jardin_sejour_inactivite_deadline (écriture réelle
    via target: block).
    """
    path = DOMAIN_SOIR / "mouvements_sejour.yaml"
    lines = [
        line for line in read(path).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_datetime\.set_(?:datetime|value)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"jardin_sejour_inactivite_deadline")

    found = False
    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        found = True
                break

    check(
        found,
        "T08 — mouvements_sejour.yaml n'écrit pas jardin_sejour_inactivite_deadline",
    )
    ok("T08 — mouvements_sejour.yaml écrit jardin_sejour_inactivite_deadline")


# ---------------------------------------------------------------------------
# T09 — allumage soir écrit jardin_soir_extinction_deadline
# ---------------------------------------------------------------------------

def test_allumage_soir_writes_deadline():
    """
    Vérifie que l'automation d'allumage soir écrit
    input_datetime.jardin_soir_extinction_deadline (écriture réelle).
    """
    path = DOMAIN_SOIR / "allumage.yaml"
    lines = [
        line for line in read(path).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_datetime\.set_(?:datetime|value)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"jardin_soir_extinction_deadline")

    found = False
    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        found = True
                break

    check(
        found,
        "T09 — allumage soir n'écrit pas jardin_soir_extinction_deadline",
    )
    ok("T09 — allumage soir écrit jardin_soir_extinction_deadline")


# ---------------------------------------------------------------------------
# T10 — I1 : switch.prise_jardin piloté uniquement par les scripts canoniques
# ---------------------------------------------------------------------------

def test_switch_exclusivity():
    """
    Vérifie que switch.prise_jardin n'est piloté (écriture réelle via
    target: block) que par les scripts canoniques du domaine.

    Écrivains légitimes connus hors scripts canoniques :
      - 11_automations/boutons/cuisine.yaml  (bouton physique cuisine)
      - 10_scripts/scenario_extinction_soir.yaml  (script transversal)

    Ces deux fichiers sont explicitement exclus du scan.
    """
    write_service = re.compile(r"switch\.turn_(?:on|off)")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"prise_jardin")

    canonical_scripts = {p.resolve() for p in SCRIPTS_DIR.glob("*.yaml")}

    scan_roots = [ROOT / "10_scripts", ROOT / "11_automations"]
    for scan_root in scan_roots:
        for yaml_file in scan_root.rglob("*.yaml"):
            if not yaml_file.is_file():
                continue
            if yaml_file.resolve() in canonical_scripts:
                continue
            if yaml_file.resolve() in EXTERNAL_WRITERS:
                continue
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
                                    f"T10 — pilotage de switch.prise_jardin détecté dans "
                                    f"{yaml_file.relative_to(ROOT)} ligne {k+1} "
                                    f"(violation I1 — hors scripts canoniques)",
                                )
                        break
    ok("T10 — switch.prise_jardin exclusif aux scripts canoniques (I1)")


# ---------------------------------------------------------------------------
# T11 — Le sensor off.yaml n'a aucun rôle causal (§3)
# ---------------------------------------------------------------------------

def test_sensor_off_not_trigger():
    """
    Vérifie que binary_sensor.lumiere_jardin_soir_extinction_autorisee
    n'est pas utilisé comme trigger dans les automations du domaine soir.

    Le contrat §3 pose explicitement que ce capteur est une projection
    d'observabilité sans rôle causal dans la chaîne d'extinction.
    """
    sensor_id = "lumiere_jardin_soir_extinction_autorisee"
    trigger_pattern = re.compile(
        rf"platform\s*:\s*state.{{0,200}}{re.escape(sensor_id)}"
        rf"|entity_id\s*:.*{re.escape(sensor_id)}.{{0,50}}(?:\n.{{0,50}})*to\s*:",
        re.DOTALL,
    )

    for yaml_file in DOMAIN_SOIR.glob("*.yaml"):
        if not yaml_file.is_file():
            continue
        cleaned = strip_comments(read(yaml_file))
        # On cherche le sensor dans un bloc trigger uniquement
        # Pattern : présence du sensor dans une fenêtre trigger: ... platform:
        blocks = re.split(r"^\s*(?:condition|action|choose)\s*:", cleaned, flags=re.MULTILINE)
        trigger_block = blocks[0] if blocks else ""
        if sensor_id in trigger_block:
            check(
                False,
                f"T11 — {sensor_id} utilisé comme trigger dans "
                f"{yaml_file.relative_to(ROOT)} (violation §3 : rôle causal interdit)",
            )
    ok("T11 — sensor d'observabilité sans rôle causal dans les triggers (§3)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_presence_booleans,
    test_presence_deadlines,
    test_presence_sensor_off,
    test_presence_automations,
    test_presence_scripts,
    test_sensor_reads_both_deadlines,
    test_extinction_triggers_on_deadlines,
    test_sejour_writer,
    test_allumage_soir_writes_deadline,
    test_switch_exclusivity,
    test_sensor_off_not_trigger,
]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Contrat Éclairage / Jardin\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECLAIRAGE_JARDIN NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECLAIRAGE_JARDIN CONFORME")
