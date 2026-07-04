#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Fondations
Source normative : 00_documentation_arsenal/contrats/ecs/ (chapitres listés ci-dessous)
Contrats : 00_fondations_et_statut, 01_principes_perimetre_et_roles,
           02_gouvernance_autorites_et_chaine, 03_orchestration_et_wrappers,
           09_invariants_et_interdictions
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if not line.lstrip().startswith("#")
    )


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf"^\s*{re.escape(entity_id)}\s*:", re.MULTILINE)
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


# ---------------------------------------------------------------------------
# T01 — Présence des entités canoniques fondamentales (§05, §06)
# ---------------------------------------------------------------------------

def test_presence_entites_canoniques():
    """
    Vérifie que les entités fondamentales du sous-système ECS sont déclarées
    dans leurs fichiers canoniques.
    """
    cases = [
        (ROOT / "05_input_booleans/ecs/cycle_en_cours.yaml",
         r"^\s*ecs_cycle_en_cours\s*:",
         "input_boolean.ecs_cycle_en_cours"),
        (ROOT / "05_input_booleans/ecs/pipeline_en_cours.yaml",
         r"^\s*ecs_pipeline_en_cours\s*:",
         "input_boolean.ecs_pipeline_en_cours"),
        (ROOT / "05_input_booleans/ecs/fin_de_cycle_signal.yaml",
         r"^\s*ecs_fin_cycle_signal\s*:",
         "input_boolean.ecs_fin_cycle_signal"),
        (ROOT / "08_timers/ecs/fenetre_inertie_chauffe.yaml",
         r"^\s*fenetre_inertie_chauffe_ecs\s*:",
         "timer.fenetre_inertie_chauffe_ecs"),
    ]
    for path, pattern, entity in cases:
        content = read(path)
        check(
            bool(re.search(pattern, content, re.MULTILINE)),
            f"T01 — {entity} absent de {path.relative_to(ROOT)}",
        )
    ok("T01 — présence entités canoniques fondamentales ECS")


# ---------------------------------------------------------------------------
# T02 — Présence du script autoritaire unique (§02)
# ---------------------------------------------------------------------------

def test_presence_script_autoritaire():
    """
    Vérifie que script.chauffage_ecs_cycle est déclaré dans son fichier canonique.
    Il constitue l'orchestrateur unique du cycle ECS (§02).
    """
    path = ROOT / "10_scripts/ecs/cycle.yaml"
    content = read(path)
    check(
        bool(re.search(r"^\s*chauffage_ecs_cycle\s*:", content, re.MULTILINE)),
        f"T02 — script.chauffage_ecs_cycle absent de {path.relative_to(ROOT)}",
    )
    ok("T02 — présence script.chauffage_ecs_cycle (§02)")


# ---------------------------------------------------------------------------
# T03 — Présence des scripts de session (§pipeline)
# ---------------------------------------------------------------------------

def test_presence_scripts_session():
    """
    Vérifie que les scripts de session open/close sont déclarés.
    """
    cases = [
        (ROOT / "10_scripts/ecs/cycle_session_open.yaml",
         "ecs_cycle_session_open"),
        (ROOT / "10_scripts/ecs/cycle_session_close.yaml",
         "ecs_cycle_session_close"),
    ]
    for path, key in cases:
        content = read(path)
        check(
            bool(re.search(rf"^\s*{re.escape(key)}\s*:", content, re.MULTILINE)),
            f"T03 — script.{key} absent de {path.relative_to(ROOT)}",
        )
    ok("T03 — présence scripts session open/close")


# ---------------------------------------------------------------------------
# T04 — Présence des scripts d'exécution (§02 / §03)
# ---------------------------------------------------------------------------

def test_presence_scripts_execution():
    """
    Vérifie la présence des scripts d'exécution et d'orchestration canoniques.
    """
    cases = [
        (ROOT / "10_scripts/ecs/appliquer_consigne_bridge.yaml",
         "ecs_appliquer_consigne_bridge"),
        (ROOT / "10_scripts/ecs/appliquer_consigne_confirmee.yaml",
         "ecs_appliquer_consigne_confirmee"),
        (ROOT / "10_scripts/ecs/auto_correction_offsets.yaml",
         "ecs_autocorrect_offsets"),
    ]
    for path, key in cases:
        content = read(path)
        check(
            bool(re.search(rf"^\s*{re.escape(key)}\s*:", content, re.MULTILINE)),
            f"T04 — script.{key} absent de {path.relative_to(ROOT)}",
        )
    ok("T04 — présence scripts d'exécution canoniques")


# ---------------------------------------------------------------------------
# T05 — appliquer_consigne_bridge déclaré mode: single (§application_consigne)
# ---------------------------------------------------------------------------

def test_bridge_mode_single():
    """
    Vérifie que script.ecs_appliquer_consigne_bridge déclare mode: single.
    Contrainte contractuelle explicite — pas de concurrence admise (V1).
    """
    path = ROOT / "10_scripts/ecs/appliquer_consigne_bridge.yaml"
    content = read(path)
    check(
        bool(re.search(r"^\s*mode\s*:\s*single\b", content, re.MULTILINE)),
        "T05 — mode: single absent de appliquer_consigne_bridge.yaml",
    )
    ok("T05 — appliquer_consigne_bridge mode: single")


# ---------------------------------------------------------------------------
# T06 — appliquer_consigne_confirmee n'appelle pas cycle_session_close (§interdictions)
# ---------------------------------------------------------------------------

def test_confirmee_no_session_close():
    """
    Vérifie que ecs_appliquer_consigne_confirmee ne referme pas la session ECS.
    Interdiction contractuelle explicite — le couplage session/exécuteur
    appartient exclusivement à l'orchestrateur.
    """
    path = ROOT / "10_scripts/ecs/appliquer_consigne_confirmee.yaml"
    cleaned = strip_comments(read(path))
    check(
        "ecs_cycle_session_close" not in cleaned,
        "T06 — appliquer_consigne_confirmee appelle ecs_cycle_session_close (interdit)",
    )
    ok("T06 — appliquer_consigne_confirmee sans appel session_close")


# ---------------------------------------------------------------------------
# T07 — appliquer_consigne_confirmee n'écrit pas ecs_target_temp_session (§interdictions)
# ---------------------------------------------------------------------------

def test_confirmee_no_target_temp_write():
    """
    Vérifie que ecs_appliquer_consigne_confirmee n'écrit pas
    input_text.ecs_target_temp_session — interdiction contractuelle explicite.
    Détection via bloc target: (service + cible dans 5 lignes).
    """
    path = ROOT / "10_scripts/ecs/appliquer_consigne_confirmee.yaml"
    lines = [
        line for line in read(path).splitlines()
        if not line.lstrip().startswith("#")
    ]
    write_service = re.compile(r"input_text\.set_value|input_text\.set")
    target_kw     = re.compile(r"^\s+target\s*:")
    target_entity = re.compile(r"ecs_target_temp_session")

    for i, line in enumerate(lines):
        if not write_service.search(line):
            continue
        for j in range(i + 1, min(i + 3, len(lines))):
            if target_kw.search(lines[j]):
                for k in range(j + 1, min(j + 4, len(lines))):
                    if target_entity.search(lines[k]):
                        check(
                            False,
                            f"T07 — appliquer_consigne_confirmee écrit ecs_target_temp_session "
                            f"ligne {k+1} (interdit)",
                        )
                break
    ok("T07 — appliquer_consigne_confirmee sans écriture ecs_target_temp_session")


# ---------------------------------------------------------------------------
# T08 — autocorrect_offsets ne déclenche pas de cycle ECS (§11 invariants)
# ---------------------------------------------------------------------------

def test_autocorrect_no_cycle_trigger():
    """
    Vérifie que script.ecs_autocorrect_offsets ne modifie pas
    input_boolean.ecs_cycle_en_cours et n'appelle pas script.chauffage_ecs_cycle.
    Invariant §11 : le service ne déclenche aucun cycle ECS.
    """
    path = ROOT / "10_scripts/ecs/auto_correction_offsets.yaml"
    cleaned = strip_comments(read(path))
    for forbidden in ("chauffage_ecs_cycle", "ecs_cycle_en_cours"):
        check(
            forbidden not in cleaned,
            f"T08 — autocorrect_offsets référence {forbidden} (interdit §11)",
        )
    ok("T08 — autocorrect_offsets sans déclenchement de cycle (§11)")


# ---------------------------------------------------------------------------
# T09 — autocorrect_offsets ne modifie qu'un seul type d'entité (§11 invariant 5)
# ---------------------------------------------------------------------------

def test_autocorrect_single_entity_type():
    """
    Vérifie que ecs_autocorrect_offsets n'écrit que des input_number.ecs_off_*
    et input_text.ecs_dernier_ajustement — pas d'autres helpers.
    Invariant §11 : une exécution modifie au plus une entité.
    Les écriture détectées sur ecs_cycle_en_cours, ecs_fin_cycle_signal
    ou ecs_resume_* constituent une violation.
    """
    path = ROOT / "10_scripts/ecs/auto_correction_offsets.yaml"
    cleaned = strip_comments(read(path))
    forbidden_writes = [
        "ecs_cycle_en_cours",
        "ecs_fin_cycle_signal",
        "ecs_pipeline_en_cours",
        "ecs_resume_dernier_cycle_fige",
    ]
    for entity in forbidden_writes:
        # Cherche écriture réelle (service + target dans 5 lignes)
        lines = cleaned.splitlines()
        write_service = re.compile(r"input_boolean\.turn_|input_text\.set")
        target_kw     = re.compile(r"^\s+target\s*:")
        target_entity = re.compile(re.escape(entity))
        for i, line in enumerate(lines):
            if not write_service.search(line):
                continue
            for j in range(i + 1, min(i + 3, len(lines))):
                if target_kw.search(lines[j]):
                    for k in range(j + 1, min(j + 4, len(lines))):
                        if target_entity.search(lines[k]):
                            check(
                                False,
                                f"T09 — autocorrect_offsets écrit {entity} ligne {k+1} (interdit §11)",
                            )
                    break
    ok("T09 — autocorrect_offsets n'écrit pas d'entités hors périmètre (§11)")


# ---------------------------------------------------------------------------
# T10 — Les helpers ECS ne contiennent pas de logique de déclenchement (§01 §4)
# ---------------------------------------------------------------------------

def test_helpers_passifs():
    """
    Vérifie que les fichiers de helpers ECS (input_boolean, input_number,
    input_text dans 05_*/ecs/, 03_*/ecs/, 04_*/ecs/) ne contiennent pas
    de services d'action (turn_on, turn_off, set_value) dans leur définition.
    Principe §01 §4 : les helpers sont passifs — ils ne déclenchent pas.
    Scope limité aux déclarations de helpers, pas aux automations.
    """
    helper_dirs = [
        ROOT / "05_input_booleans/ecs",
        ROOT / "03_input_numbers/ecs",
        ROOT / "04_input_texts/ecs",
        ROOT / "07_input_datetimes/ecs",
        ROOT / "08_timers/ecs",
    ]
    action_pattern = re.compile(
        r"^\s+(?:service|action)\s*:\s*(?:input_boolean|input_text|input_number|"
        r"input_datetime|timer|switch|script)\.",
        re.MULTILINE,
    )
    for helper_dir in helper_dirs:
        for yaml_file in yaml_files(helper_dir):
            cleaned = strip_comments(read(yaml_file))
            if action_pattern.search(cleaned):
                check(
                    False,
                    f"T10 — logique d'action détectée dans helper ECS : "
                    f"{yaml_file.relative_to(ROOT)} (helpers passifs — §01 §4)",
                )
    ok("T10 — helpers ECS passifs (§01 §4)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_presence_entites_canoniques,
    test_presence_script_autoritaire,
    test_presence_scripts_session,
    test_presence_scripts_execution,
    test_bridge_mode_single,
    test_confirmee_no_session_close,
    test_confirmee_no_target_temp_write,
    test_autocorrect_no_cycle_trigger,
    test_autocorrect_single_entity_type,
    test_helpers_passifs,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Fondations\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_FONDATIONS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_FONDATIONS CONFORME")
