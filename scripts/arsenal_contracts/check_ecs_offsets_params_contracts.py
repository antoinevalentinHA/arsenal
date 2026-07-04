#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Auto-ajustement des offsets — paramètres
Contrat (source normative) : 00_documentation_arsenal/contrats/ecs/11_ajustement_des_offsets.md (§6, §7, §10 « Notes de gouvernance »)

Verrouille (ECS-OFF-5) les paramètres contractuels du §10 — dont « toute
modification constitue un changement de contrat » — jusqu'ici déclarés
opposables mais NON testés :
  - correcteur `alpha = 0.25` (§7.1) ;
  - zone morte `deadband_min = -0.3` / `deadband_max = +0.5` (§6.1) ;
  - seuils de bucket `delta_init < 2.5` (tiny) / `< 7.0` (medium) + les
    4 buckets tiny/medium/normal/desinfection (§6.2) ;
  - plage durée `0 < duree < 120` (§5 gate 8 / §10) ;
  - format du résumé figé `date|mode|consigne|t0|boost|valide` — dont
    « toute modification constitue une rupture de contrat » (§3.2, §10) :
    producteur, consommateur (6 segments + mapping d'index) et validation.

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


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


# ---------------------------------------------------------------------------
# Chemins canoniques
# ---------------------------------------------------------------------------

SCRIPT = ROOT / "10_scripts/ecs/auto_correction_offsets.yaml"      # paramètres + consommateur
PRODUCER = ROOT / "11_automations/ecs/log/debut.yaml"             # producteur du résumé
GEL = ROOT / "11_automations/ecs/inertie/gel.yaml"               # validation du champ `valide`


def script_body() -> str:
    return strip_comments(read(SCRIPT))


# ---------------------------------------------------------------------------
# T01 — Correcteur alpha = 0.25 (§7.1)
# ---------------------------------------------------------------------------

def test_alpha():
    """§7.1 / §10 : le gain du correcteur proportionnel est un paramètre
    contractuel. `alpha = 0.25` (≈ 4 cycles pour une erreur constante)."""
    check(
        bool(re.search(r"alpha\s*:\s*0\.25(?!\d)", script_body())),
        "T01 — alpha != 0.25 dans auto_correction_offsets.yaml (§7.1 — changement de contrat)",
    )
    ok("T01 — correcteur alpha = 0.25 (§7.1)")


# ---------------------------------------------------------------------------
# T02 — Zone morte -0.3 / +0.5 (§6.1)
# ---------------------------------------------------------------------------

def test_deadband():
    """§6.1 / §10 : zone morte asymétrique contractuelle. Aucune correction
    si -0.3 <= erreur <= +0.5."""
    body = script_body()
    check(
        bool(re.search(r"deadband_min\s*:\s*-0\.3(?!\d)", body)),
        "T02 — deadband_min != -0.3 (§6.1 — changement de contrat)",
    )
    check(
        bool(re.search(r"deadband_max\s*:\s*0\.5(?!\d)", body)),
        "T02 — deadband_max != +0.5 (§6.1 — changement de contrat)",
    )
    ok("T02 — zone morte deadband [-0.3 ; +0.5] (§6.1)")


# ---------------------------------------------------------------------------
# T03 — Buckets : seuils delta_init 2.5 / 7.0 + 4 buckets (§6.2)
# ---------------------------------------------------------------------------

def test_buckets():
    """§6.2 / §10 : définition des buckets et seuils `delta_init`. Contractuel :
    desinfection (mode), tiny (< 2.5), medium (< 7.0), normal (sinon)."""
    body = script_body()
    check(
        bool(re.search(r"delta_init\s*<\s*2\.5(?!\d)", body)),
        "T03 — seuil bucket tiny (delta_init < 2.5) modifié (§6.2 — changement de contrat)",
    )
    check(
        bool(re.search(r"delta_init\s*<\s*7\.0(?!\d)", body)),
        "T03 — seuil bucket medium (delta_init < 7.0) modifié (§6.2 — changement de contrat)",
    )
    check(
        bool(re.search(r"mode_raw\s*==\s*'desinfection'", body)),
        "T03 — bucket desinfection (mode == desinfection) absent (§6.2)",
    )
    for bucket in ("tiny", "medium", "normal", "desinfection"):
        check(
            f"ecs_off_{bucket}" in body,
            f"T03 — offset de bucket ecs_off_{bucket} absent (§6.2 / §4.1)",
        )
    ok("T03 — buckets et seuils delta_init contractuels (§6.2)")


# ---------------------------------------------------------------------------
# T04 — Plage durée 0 < duree < 120 (§5 gate 8 / §10)
# ---------------------------------------------------------------------------

def test_plage_duree():
    """§10 : plage durée `[0 ; 120[` (gate §5.8). Runtime : `0.0 < duree < 120.0`.
    Un cycle hors plage est rejeté."""
    check(
        bool(re.search(r"0\.0\s*<\s*duree\s*<\s*120\.0(?!\d)", script_body())),
        "T04 — plage durée != (0.0 < duree < 120.0) (§10 — changement de contrat)",
    )
    ok("T04 — plage durée 0 < duree < 120 (§10)")


# ---------------------------------------------------------------------------
# T05 — Format résumé figé : consommateur (6 segments + mapping) (§3.2 / §10)
# ---------------------------------------------------------------------------

def test_resume_format_consommateur():
    """§3.2 / §10 : format `date|mode|consigne|t0|boost|valide`. Le consommateur
    exige 6 segments et lit chaque champ à son index canonique. Toute
    modification du format est une RUPTURE de contrat."""
    body = script_body()
    check(
        bool(re.search(r"parts\s*\|\s*length\s*\)\s*<\s*6\b", body)),
        "T05 — garde « < 6 segments » du résumé absente (§3.2 / §5.3 — rupture de format)",
    )
    mapping = [
        ("mode_raw", 1),
        ("consigne", 2),
        ("t0", 3),
        ("boost_flag", 4),
        ("valide_flag", 5),
    ]
    for var, idx in mapping:
        check(
            bool(re.search(rf"{var}\s*:[^\n]*parts\[{idx}\]", body)),
            f"T05 — mapping d'index rompu : {var} ne lit pas parts[{idx}] "
            f"(format date|mode|consigne|t0|boost|valide — rupture de contrat §10)",
        )
    ok("T05 — résumé consommé au format 6 champs, mapping d'index canonique (§3.2 / §10)")


# ---------------------------------------------------------------------------
# T06 — Format résumé figé : producteur (§3.2 / §10)
# ---------------------------------------------------------------------------

def test_resume_format_producteur():
    """§3.2 / §10 : le producteur du résumé (log/debut.yaml) émet exactement
    `date|mode|consigne|t0|boost|pending` — l'ordre des 6 champs est opposable."""
    body = strip_comments(read(PRODUCER))
    check(
        bool(re.search(
            r"\}\}\|\{\{\s*mode_cycle\s*\}\}\|\{\{\s*consigne\s*\}\}"
            r"\|\{\{\s*t0\s*\}\}\|\{\{\s*boost_flag\s*\}\}\|pending",
            body,
        )),
        "T06 — producteur du résumé ne suit pas date|mode|consigne|t0|boost|pending "
        "(log/debut.yaml — rupture de format §3.2 / §10)",
    )
    ok("T06 — producteur émet date|mode|consigne|t0|boost|pending (§3.2 / §10)")


# ---------------------------------------------------------------------------
# T07 — Champ `valide` : gel pose |oui / |non depuis |pending (§3.3)
# ---------------------------------------------------------------------------

def test_resume_valide_gel():
    """§3.3 : le 6ᵉ champ `valide` passe de `pending` à `oui` / `non` lors du
    gel post-inertie. Verrouille la sémantique du dernier segment du format."""
    body = strip_comments(read(GEL))
    check(
        "'|pending', '|oui'" in body,
        "T07 — gel ne pose pas |oui depuis |pending (§3.3 — sémantique du champ valide)",
    )
    check(
        "'|pending', '|non'" in body,
        "T07 — gel ne pose pas |non depuis |pending (§3.3 — sémantique du champ valide)",
    )
    ok("T07 — champ `valide` posé oui/non depuis pending au gel (§3.3)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_alpha,
    test_deadband,
    test_buckets,
    test_plage_duree,
    test_resume_format_consommateur,
    test_resume_format_producteur,
    test_resume_valide_gel,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Auto-ajustement des offsets (paramètres §10)\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_OFFSETS_PARAMS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_OFFSETS_PARAMS CONFORME")
