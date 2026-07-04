#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Désinfection au retour de vacances
Contrat (source normative) : 00_documentation_arsenal/contrats/ecs/09_invariants_et_interdictions.md (§2 invariants absolus, §3 interdictions)

Couvre (ECS-DESINF-1) les invariants les plus critiques du sous-système
désinfection-retour, jusqu'ici non instrumentés :
  - légitimité établie EXCLUSIVEMENT par `timer.finished` de
    `timer.vacances_longues_ecs`, JAMAIS par `timer.cancel` (§2) ;
  - écrivain souverain UNIQUE par transition de
    `input_boolean.ecs_desinfection_retour_due` (pose ON / consommation OFF, §2) ;
  - idempotence : au plus une exécution par légitimité (§2) ;
  - état souverain PERSISTANT — aucun `initial` (§2) ;
  - décision NE lit JAMAIS l'attribut `remaining` / `finishes_at` (§3).

Couvre aussi (ECS-DESINF-2) la garde préventive de cardinalité de
`input_select.mode_maison` : le couplage `Vacances → Normal` du consommateur
n'est sûr qu'à 2 modes — toute extension doit trip la CI (T10).

Logique Arsenal habituelle : ERROR => exit 1 ; conforme => exit 0.
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


# ---------------------------------------------------------------------------
# Chemins & entités canoniques
# ---------------------------------------------------------------------------

POSER = ROOT / "11_automations/ecs/desinfection_retour_pose_due.yaml"
CONSUMER = ROOT / "11_automations/ecs/desinfection_retour_vacances.yaml"
SOVEREIGN_FILE = ROOT / "05_input_booleans/ecs/desinfection_retour_due.yaml"
TIMER_FILE = ROOT / "08_timers/ecs/desinfection_vacances.yaml"

SCAN_DIRS = [ROOT / "11_automations", ROOT / "10_scripts"]

SOVEREIGN = "ecs_desinfection_retour_due"          # input_boolean (clé + suffixe)
TIMER_ENTITY = "timer.vacances_longues_ecs"
TIMER_KEY = "vacances_longues_ecs"

# ECS-DESINF-2 — garde de cardinalité du contexte de retour
MODE_MAISON_FILE = ROOT / "06_input_selects/modes/mode_maison.yaml"
MODE_MAISON_MODES = {"Normal", "Vacances"}         # cardinalité verrouillée (2 modes)


def files_calling_service_on_target(service: str, target: str) -> set[Path]:
    """
    Retourne l'ensemble des fichiers YAML (automations + scripts) où une ligne
    invoque `service` (ex. input_boolean.turn_on), avec `target` sur la même
    ligne ou dans les 5 lignes suivantes (bloc target/entity_id). Commentaires
    ignorés — seule la logique effective compte.
    """
    svc = re.compile(re.escape(service))
    tgt = re.compile(re.escape(target))
    hits: set[Path] = set()
    for scan_dir in SCAN_DIRS:
        for path in yaml_files(scan_dir):
            lines = strip_comments(read(path)).splitlines()
            for i, line in enumerate(lines):
                if not svc.search(line):
                    continue
                window = lines[i:i + 6]
                if any(tgt.search(w) for w in window):
                    hits.add(path)
                    break
    return hits


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# T01 — Poser présent et déclenché par timer.finished du timer souverain (§2)
# ---------------------------------------------------------------------------

def test_poser_present_declenche_par_finished():
    """
    §2 : la légitimité est établie EXCLUSIVEMENT par `timer.finished` de
    `timer.vacances_longues_ecs`. L'automation de pose doit exister et se
    déclencher sur cet événement pour ce timer précis.
    """
    check(POSER.is_file(), f"T01 — automation de pose absente ({rel(POSER)})")
    content = strip_comments(read(POSER))
    check(
        "timer.finished" in content,
        "T01 — la pose ne se déclenche pas sur `timer.finished` (§2)",
    )
    check(
        TIMER_ENTITY in content,
        f"T01 — la pose ne cible pas `{TIMER_ENTITY}` (§2)",
    )
    ok("T01 — pose présente, déclenchée par timer.finished du timer souverain (§2)")


# ---------------------------------------------------------------------------
# T02 — Aucune légitimité par timer.cancel (§2)
# ---------------------------------------------------------------------------

def test_aucune_legitimite_par_cancel():
    """
    §2 : la légitimité n'est JAMAIS établie par `timer.cancel` — complétion et
    annulation doivent rester discernables. Aucun écrivain ON de l'état souverain
    ne doit référencer `timer.cancel`.
    """
    on_writers = files_calling_service_on_target("input_boolean.turn_on", SOVEREIGN)
    for path in sorted(on_writers):
        content = strip_comments(read(path))
        check(
            "timer.cancel" not in content,
            f"T02 — un écrivain ON de {SOVEREIGN} référence `timer.cancel` "
            f"({rel(path)}) — légitimité par annulation interdite (§2)",
        )
    ok("T02 — aucune légitimité de désinfection-retour par timer.cancel (§2)")


# ---------------------------------------------------------------------------
# T03 — Écrivain ON unique = la pose (§2 souveraineté)
# ---------------------------------------------------------------------------

def test_ecrivain_on_unique():
    """
    §2 : `input_boolean.ecs_desinfection_retour_due` a un écrivain souverain
    unique par transition. La transition ON (pose) doit avoir pour unique
    auteur l'automation de pose.
    """
    on_writers = files_calling_service_on_target("input_boolean.turn_on", SOVEREIGN)
    check(
        POSER in on_writers,
        f"T03 — la pose n'écrit pas ON {SOVEREIGN} ({rel(POSER)})",
    )
    extra = sorted(rel(p) for p in on_writers if p != POSER)
    check(
        not extra,
        f"T03 — écrivain(s) ON supplémentaire(s) de {SOVEREIGN} : {extra} "
        f"— souveraineté unique violée (§2)",
    )
    ok("T03 — écrivain ON unique de l'état souverain = la pose (§2)")


# ---------------------------------------------------------------------------
# T04 — Écrivain OFF unique = le consommateur (§2 souveraineté)
# ---------------------------------------------------------------------------

def test_ecrivain_off_unique():
    """
    §2 : la transition OFF (réinitialisation à la consommation) doit avoir pour
    unique auteur l'automation consommatrice de la désinfection-retour.
    """
    off_writers = files_calling_service_on_target("input_boolean.turn_off", SOVEREIGN)
    check(
        CONSUMER in off_writers,
        f"T04 — le consommateur n'écrit pas OFF {SOVEREIGN} ({rel(CONSUMER)})",
    )
    extra = sorted(rel(p) for p in off_writers if p != CONSUMER)
    check(
        not extra,
        f"T04 — écrivain(s) OFF supplémentaire(s) de {SOVEREIGN} : {extra} "
        f"— souveraineté unique violée (§2)",
    )
    ok("T04 — écrivain OFF unique de l'état souverain = le consommateur (§2)")


# ---------------------------------------------------------------------------
# T05 — Aucune écriture diffuse (toggle) de l'état souverain (§2)
# ---------------------------------------------------------------------------

def test_aucun_toggle_souverain():
    """
    §2 : l'écriture est unique PAR TRANSITION (ON / OFF explicites). Un
    `input_boolean.toggle` sur l'état souverain rendrait la transition
    indéterminée et briserait la souveraineté.
    """
    togglers = files_calling_service_on_target("input_boolean.toggle", SOVEREIGN)
    check(
        not togglers,
        f"T05 — toggle diffus de {SOVEREIGN} : {sorted(rel(p) for p in togglers)} "
        f"— transition non déterministe interdite (§2)",
    )
    ok("T05 — aucune écriture diffuse (toggle) de l'état souverain (§2)")


# ---------------------------------------------------------------------------
# T06 — Idempotence : le consommateur est gardé par l'état ON et le consomme (§2)
# ---------------------------------------------------------------------------

def test_idempotence_consommation():
    """
    §2 : la désinfection-retour est idempotente — au plus une exécution par
    légitimité établie. Le consommateur doit (a) se conditionner à l'état
    souverain == on, et (b) le remettre à off (consommation) dans son action.
    """
    lines = strip_comments(read(CONSUMER)).splitlines()

    # (a) condition d'état sur le souverain == on : occurrence du souverain
    #     avec un `state: on` dans une fenêtre proche.
    gated = False
    on_re = re.compile(r"state\s*:\s*['\"]?on['\"]?")
    for i, line in enumerate(lines):
        if SOVEREIGN in line and "turn_off" not in line and "turn_on" not in line:
            lo = max(0, i - 4)
            if any(on_re.search(w) for w in lines[lo:i + 5]):
                gated = True
                break
    check(gated, f"T06 — le consommateur n'est pas gardé par {SOVEREIGN} == on (§2)")

    # (b) consommation : écrit OFF le souverain
    off_writers = files_calling_service_on_target("input_boolean.turn_off", SOVEREIGN)
    check(
        CONSUMER in off_writers,
        f"T06 — le consommateur ne consomme pas (OFF) {SOVEREIGN} (§2)",
    )
    ok("T06 — idempotence : consommateur gardé par l'état ON et le consomme (§2)")


# ---------------------------------------------------------------------------
# T07 — État souverain persistant : déclaré sans `initial` (§2)
# ---------------------------------------------------------------------------

def test_souverain_sans_initial():
    """
    §2 : l'état souverain est persistant (pas d'`initial`) ; valeur par défaut
    au tout premier démarrage = off (comportement HA natif d'un input_boolean
    sans initial). La déclaration canonique ne doit porter aucune clé `initial`.
    """
    content = read(SOVEREIGN_FILE)
    check(
        bool(re.search(rf"^\s*{re.escape(SOVEREIGN)}\s*:", content, re.MULTILINE)),
        f"T07 — {SOVEREIGN} non déclaré dans {rel(SOVEREIGN_FILE)}",
    )
    check(
        not re.search(r"^\s*initial\s*:", strip_comments(content), re.MULTILINE),
        f"T07 — clé `initial` interdite sur {SOVEREIGN} "
        f"({rel(SOVEREIGN_FILE)}) — l'état souverain doit rester persistant (§2)",
    )
    ok("T07 — état souverain persistant, sans `initial` (§2)")


# ---------------------------------------------------------------------------
# T08 — La décision ne lit jamais `remaining` / `finishes_at` (§3)
# ---------------------------------------------------------------------------

def test_pas_de_lecture_remaining():
    """
    §3 : il est interdit de fonder la décision de désinfection-retour sur
    l'attribut `remaining` du timer (non fiable à l'état `idle`). Par extension,
    `finishes_at` relève de la même dépendance temporelle fragile. Ni la pose ni
    le consommateur ne doivent lire ces attributs.
    """
    for path in (POSER, CONSUMER):
        content = strip_comments(read(path))
        check(
            "remaining" not in content,
            f"T08 — lecture de `remaining` détectée dans {rel(path)} "
            f"(interdit §3 — non fiable à l'état idle)",
        )
        check(
            "finishes_at" not in content,
            f"T08 — lecture de `finishes_at` détectée dans {rel(path)} "
            f"(dépendance temporelle fragile, §3)",
        )
    ok("T08 — décision sans lecture de `remaining` / `finishes_at` (§3)")


# ---------------------------------------------------------------------------
# T09 — Timer souverain déclaré et référencé (§2 socle de légitimité)
# ---------------------------------------------------------------------------

def test_timer_souverain_declare():
    """
    §2 : la légitimité repose sur `timer.vacances_longues_ecs`. Le timer doit
    être déclaré dans son fichier canonique et référencé par la pose.
    """
    content = read(TIMER_FILE)
    check(
        bool(re.search(rf"^\s*{re.escape(TIMER_KEY)}\s*:", content, re.MULTILINE)),
        f"T09 — timer `{TIMER_KEY}` non déclaré dans {rel(TIMER_FILE)}",
    )
    check(
        TIMER_ENTITY in strip_comments(read(POSER)),
        f"T09 — la pose ne référence pas `{TIMER_ENTITY}`",
    )
    ok("T09 — timer souverain déclaré et référencé par la pose (§2)")


# ---------------------------------------------------------------------------
# T10 — Garde de cardinalité de mode_maison (ECS-DESINF-2)
# ---------------------------------------------------------------------------

def test_mode_maison_cardinalite():
    """
    ECS-DESINF-2 — Robustesse du couplage à `mode_maison`.

    Le consommateur (10250000000021) se déclenche sur la transition
    `Vacances → Normal`. Ce couplage n'est sûr que tant que `mode_maison`
    possède exactement 2 modes {Normal, Vacances} : l'ajout d'un 3ᵉ mode le
    fragilise (un retour de Vacances pourrait aboutir ailleurs que `Normal`,
    et la désinfection-retour ne se déclencherait pas).

    Garde préventive : toute extension de `mode_maison` doit trip la CI et
    forcer une revue explicite du trigger de la désinfection-retour (trigger
    plus robuste, ou mise à jour coordonnée assumée).
    """
    body = strip_comments(read(MODE_MAISON_FILE))
    m = re.search(r"options\s*:\s*(.*)$", body, re.DOTALL)
    options = set(re.findall(r"-\s+([A-Za-z0-9_]+)", m.group(1))) if m else set()
    check(
        options == MODE_MAISON_MODES,
        f"T10 — cardinalité de mode_maison modifiée : {sorted(options)} "
        f"≠ {sorted(MODE_MAISON_MODES)} — revoir le couplage Vacances→Normal "
        f"de la désinfection-retour (ECS-DESINF-2)",
    )
    ok("T10 — cardinalité mode_maison verrouillée {Normal, Vacances} (ECS-DESINF-2)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_poser_present_declenche_par_finished,
    test_aucune_legitimite_par_cancel,
    test_ecrivain_on_unique,
    test_ecrivain_off_unique,
    test_aucun_toggle_souverain,
    test_idempotence_consommation,
    test_souverain_sans_initial,
    test_pas_de_lecture_remaining,
    test_timer_souverain_declare,
    test_mode_maison_cardinalite,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Désinfection au retour de vacances\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_DESINFECTION_RETOUR NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_DESINFECTION_RETOUR CONFORME")
