#!/usr/bin/env python3
"""
Arsenal — Anti-dérive du registre de couverture CI

Contrat (source normative) :
  00_documentation_arsenal/audits/REGISTRE_COUVERTURE_VERIFICATION.md
Cadrage : 00_documentation_arsenal/audits/04_chantiers/transverses/
          c14_lot1d_antiderive_registre_couverture_ci.md

But (C14 Lot 1D) : empêcher le registre de couverture CI de redevenir un
document déclaratif périmé. Le registre a déjà dérivé (compteurs faux,
affirmation obsolète sur l'absence de checker transversal d'IDs).

Ce que le checker CONTRÔLE :

  1. Intégrité référentielle (calculée en direct, indépendamment du registre)
     - INTEG-1 : tout scripts/arsenal_contracts/check_*.py est référencé par
                 au moins un workflow .github/workflows/*.yml (aucun checker
                 orphelin), sauf helper explicitement classé (CHECKER_HELPERS).
     - INTEG-2 : tout chemin scripts/.../*.py référencé par un workflow existe
                 réellement (aucune référence morte).

  2. Fraîcheur des compteurs §3 du registre (COUNT-*)
     - la valeur en gras déclarée pour chaque indicateur countable doit égaler
       le comptage réel ; toute dérive est une ERROR ; une ligne d'indicateur
       manquante (structure §3 modifiée) est une ERROR.

Ce que le checker N'IMPOSE PAS (pas de faux postulat) :
  - ni « 1 workflow = 1 checker » ;
  - ni « tout workflow appelle un script Python » (docs.yml appelle docs_lint/,
    doctrine.yml est inline, arsenal-ci-chauffage.yml appelle tools/arsenal_ci) ;
  - ni « tout script est appelé par un workflow » si c'est un helper classé.

Ce que le checker NE garantit PAS : qualité métier des checkers, exhaustivité
des normes Markdown, validité Home Assistant, runtime.

Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python scripts/arsenal_contracts/check_ci_coverage_registry.py
  python scripts/arsenal_contracts/check_ci_coverage_registry.py --selftest
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AC_DIR = ROOT / "scripts" / "arsenal_contracts"
WF_DIR = ROOT / ".github" / "workflows"
DOCTRINES_DIR = ROOT / "00_documentation_arsenal" / "architecture" / "03_doctrines"
CONTRATS_DIR = ROOT / "00_documentation_arsenal" / "contrats"
REGISTRE = ROOT / "00_documentation_arsenal" / "audits" / "REGISTRE_COUVERTURE_VERIFICATION.md"

# Helpers explicitement classés « non appelés en CI » (pas des checkers orphelins).
# Aucun aujourd'hui sous arsenal_contracts/ ; docs_lint_fix.py vit sous docs_lint/.
CHECKER_HELPERS: set[str] = set()

_SCRIPT_REF = re.compile(r"scripts/(?:arsenal_contracts|docs_lint)/[A-Za-z0-9_./-]+\.py")


# ---------------------------------------------------------------------------
# Comptages canoniques (source = système de fichiers réel)
# ---------------------------------------------------------------------------
def canonical_counts(root: Path) -> dict[str, int]:
    ac = root / "scripts" / "arsenal_contracts"
    wf = root / ".github" / "workflows"
    doctrines = root / "00_documentation_arsenal" / "architecture" / "03_doctrines"
    contrats = root / "00_documentation_arsenal" / "contrats"
    return {
        "contrats_md": sum(1 for _ in contrats.rglob("*.md")),
        # Doctrines = fichiers .md HORS README (le README du dossier n'est pas une doctrine).
        "doctrines": sum(1 for p in doctrines.glob("*.md") if p.name != "README.md"),
        "checkers": sum(1 for _ in ac.glob("check_*.py")),
        "workflows_total": sum(1 for _ in wf.glob("*.yml")),
        "contracts_prefix": sum(1 for _ in wf.glob("contracts_*.yml")),
    }


# ---------------------------------------------------------------------------
# Intégrité référentielle checkers <-> workflows
# ---------------------------------------------------------------------------
def check_topology(ac_dir: Path, wf_dir: Path, helpers: set[str], root: Path) -> list[str]:
    errors: list[str] = []
    checkers = sorted(p.name for p in ac_dir.glob("check_*.py"))
    workflows = sorted(wf_dir.glob("*.yml"))
    wf_texts = {wf.name: wf.read_text(encoding="utf-8", errors="ignore") for wf in workflows}

    # INTEG-1 : aucun checker orphelin.
    for checker in checkers:
        if checker in helpers:
            continue
        if not any(checker in txt for txt in wf_texts.values()):
            errors.append(
                f"INTEG-1 : checker orphelin — {checker} n'est reference par aucun workflow "
                f"(ajouter son workflow, ou le classer dans CHECKER_HELPERS)."
            )

    # INTEG-2 : aucune reference de script morte dans un workflow (résolue depuis `root`).
    for name, txt in wf_texts.items():
        for ref in sorted(set(_SCRIPT_REF.findall(txt))):
            if not (root / ref).is_file():
                errors.append(
                    f"INTEG-2 : reference morte — {name} reference {ref} qui n'existe pas."
                )
    return errors


# ---------------------------------------------------------------------------
# Fraîcheur des compteurs §3 du registre
# ---------------------------------------------------------------------------
# label logique -> motif de ligne §3 (la valeur en gras **N** est extraite)
_COUNTER_ROWS = {
    "contrats_md": re.compile(r"^\|\s*Contrats\s*`\.md`.*?\*\*(\d+)\*\*", re.M),
    "doctrines": re.compile(r"^\|\s*Doctrines transversales.*?\*\*(\d+)\*\*", re.M),
    "checkers": re.compile(r"^\|\s*Checkers\s*\|\s*\*\*(\d+)\*\*", re.M),
    "workflows_total": re.compile(r"^\|\s*Workflows\s*\(total\).*?\*\*(\d+)\*\*", re.M),
    "contracts_prefix": re.compile(r"^\|\s*Workflows\s*`contracts_\*`.*?\*\*(\d+)\*\*", re.M),
}
_LABELS = {
    "contrats_md": "Contrats .md",
    "doctrines": "Doctrines transversales",
    "checkers": "Checkers",
    "workflows_total": "Workflows (total)",
    "contracts_prefix": "Workflows contracts_*",
}


def parse_registry_counters(text: str) -> dict[str, int | None]:
    out: dict[str, int | None] = {}
    for key, pat in _COUNTER_ROWS.items():
        m = pat.search(text)
        out[key] = int(m.group(1)) if m else None
    return out


def check_counters(text: str, counts: dict[str, int]) -> list[str]:
    errors: list[str] = []
    declared = parse_registry_counters(text)
    for key, live in counts.items():
        label = _LABELS[key]
        got = declared.get(key)
        if got is None:
            errors.append(
                f"COUNT-0 : ligne compteur '{label}' introuvable dans §3 du registre "
                f"(structure modifiee ?)."
            )
        elif got != live:
            errors.append(
                f"COUNT-1 : derive '{label}' — registre declare {got}, reel {live}."
            )
    return errors


# ---------------------------------------------------------------------------
# Point d'entrée réel
# ---------------------------------------------------------------------------
def main() -> None:
    errors: list[str] = []
    if not REGISTRE.is_file():
        print(f"ERROR : registre introuvable — {REGISTRE}")
        sys.exit(1)

    counts = canonical_counts(ROOT)
    text = REGISTRE.read_text(encoding="utf-8", errors="ignore")
    errors += check_counters(text, counts)
    errors += check_topology(AC_DIR, WF_DIR, CHECKER_HELPERS, ROOT)

    if errors:
        print("Registre de couverture CI — ecarts detectes :")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print(
        "OK - registre de couverture CI coherent : "
        f"{counts['checkers']} checkers, {counts['workflows_total']} workflows "
        f"({counts['contracts_prefix']} contracts_*), 0 checker orphelin, "
        "0 reference morte, compteurs §3 a jour."
    )


# ---------------------------------------------------------------------------
# Auto-test du juge (on ne juge pas avec un juge défectueux)
# ---------------------------------------------------------------------------
def selftest() -> None:
    import tempfile

    counts = {"checkers": 2, "workflows_total": 3, "contracts_prefix": 2,
              "contrats_md": 10, "doctrines": 4}

    def registry(checkers=2, workflows=3, contracts=2, contrats=10, doctrines=4):
        return (
            "## 3. Compteurs\n\n"
            f"| Contrats `.md` (récursif) | **{contrats}** | cmd |\n"
            f"| Doctrines transversales | **{doctrines}** | cmd |\n"
            f"| Checkers | **{checkers}** | cmd |\n"
            f"| Workflows (total) | **{workflows}** | cmd |\n"
            f"| Workflows `contracts_*` (préfixe) | **{contracts}** | cmd |\n"
        )

    # 1. compteurs conformes -> 0 erreur
    assert not check_counters(registry(), counts), "selftest compteurs conformes"

    # 2. dérive de compteur -> erreur COUNT-1
    errs = check_counters(registry(checkers=99), counts)
    assert any("COUNT-1" in e for e in errs), "selftest derive compteur"

    # 3. ligne compteur manquante -> erreur COUNT-0
    broken = registry().replace("| Checkers | **2** | cmd |\n", "")
    errs = check_counters(broken, counts)
    assert any("COUNT-0" in e for e in errs), "selftest ligne manquante"

    # 4. topologie : conforme / orphelin / référence morte
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ac = base / "scripts" / "arsenal_contracts"
        wf = base / ".github" / "workflows"
        ac.mkdir(parents=True)
        wf.mkdir(parents=True)
        (ac / "check_a.py").write_text("x\n")
        (ac / "check_b.py").write_text("x\n")
        (wf / "contracts_a.yml").write_text(
            "run: python scripts/arsenal_contracts/check_a.py\n"
        )
        (wf / "contracts_b.yml").write_text(
            "run: python scripts/arsenal_contracts/check_b.py\n"
        )
        assert not check_topology(ac, wf, set(), base), "selftest topologie conforme"

        # orphelin : check_c non référencé
        (ac / "check_c.py").write_text("x\n")
        errs = check_topology(ac, wf, set(), base)
        assert any("INTEG-1" in e for e in errs), "selftest orphelin"
        # helper classé -> plus d'erreur
        assert not check_topology(ac, wf, {"check_c.py"}, base), "selftest helper classe"

        # référence morte
        (ac / "check_c.py").unlink()
        (wf / "contracts_dead.yml").write_text(
            "run: python scripts/arsenal_contracts/check_absent.py\n"
        )
        errs = check_topology(ac, wf, set(), base)
        assert any("INTEG-2" in e for e in errs), "selftest reference morte"

    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
