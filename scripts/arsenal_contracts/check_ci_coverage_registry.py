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

  2. Fraîcheur des compteurs §3 du registre (COUNT-0 / COUNT-1)
     - la valeur en gras déclarée pour chaque indicateur countable doit égaler
       le comptage réel ; toute dérive est une ERROR ; une ligne d'indicateur
       manquante (structure §3 modifiée) est une ERROR.

  3. Fraîcheur des volumes §2 « Les trois couches » (COUNT-2 / COUNT-3)
     - la colonne « Volume (cf. §3) » de §2 REDIT des compteurs dont §3 est la
       source déclarée. Cette duplication a dérivé en silence (§2 affichait
       291/80/84 contre 293/82/87 réels au 2026-07-15) parce que la garde
       COUNT-0/1 ne couvrait que §3 : « la mesure de couverture ment » dans le
       document même qui mesure la couverture.
     - Les volumes §2 sont donc confrontés au comptage RÉEL (même source de
       vérité que §3, donc §2 ≡ §3 par construction). Ligne §2 absente ou
       volume dérivé => ERROR.

     Périmètre volontairement ANCRÉ sur les 3 lignes de §2, jamais sur tout le
     document : le §8 (journal) est une trace historique DATÉE truffée de
     nombres périmés par nature (« checkers 68→71 », « contrats 267→290 »,
     « workflows 72→75 »). Un scan global les signalerait comme des dérives et
     rendrait le journal inécrivable. Le journal est de l'histoire, pas une
     déclaration d'état.

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


# ---------------------------------------------------------------------------
# Fraîcheur des volumes §2 « Les trois couches »
# ---------------------------------------------------------------------------
# §2 redit des compteurs dont §3 est la source déclarée ("Volume (cf. §3)").
# On BORNE la recherche à la section §2 : le §8 (journal daté) contient des
# nombres historiques qu'il ne faut jamais confronter au réel.
_SECTION_2 = re.compile(r"^##\s*2\.\s.*?(?=^##\s*3\.\s)", re.M | re.S)

# label logique -> (motif sur la ligne §2, libellé d'erreur)
# `.` ne matche pas le saut de ligne (pas de DOTALL) : chaque motif reste
# confiné à SA ligne de tableau, même si un autre libellé suit.
_SECTION2_ROWS = {
    "contrats_md": (
        re.compile(r"^\|\s*\*\*Vérité normative\*\*.*?\|\s*(\d+)\s*`\.md`\s*de contrats", re.M),
        "§2 Vérité normative — contrats .md",
    ),
    "doctrines": (
        re.compile(r"^\|\s*\*\*Vérité normative\*\*.*?·\s*(\d+)\s*doctrines", re.M),
        "§2 Vérité normative — doctrines",
    ),
    "checkers": (
        re.compile(r"^\|\s*\*\*Couverture mécanique\*\*.*?\|\s*(\d+)\s*checkers", re.M),
        "§2 Couverture mécanique — checkers",
    ),
    "workflows_total": (
        re.compile(r"^\|\s*\*\*CI exécutée\*\*.*?\|\s*(\d+)\s*workflows", re.M),
        "§2 CI exécutée — workflows",
    ),
}


def check_section2_volumes(text: str, counts: dict[str, int]) -> list[str]:
    """Confronte les volumes redits en §2 au comptage réel (§2 ≡ §3 ≡ réel)."""
    errors: list[str] = []
    section = _SECTION_2.search(text)
    if not section:
        return [
            "COUNT-2 : section §2 « Les trois couches » introuvable "
            "(structure du registre modifiee ?)."
        ]
    body = section.group(0)
    for key, (pat, label) in _SECTION2_ROWS.items():
        m = pat.search(body)
        if not m:
            errors.append(
                f"COUNT-2 : volume '{label}' introuvable en §2 "
                f"(ligne supprimee ou reformulee ?)."
            )
            continue
        got = int(m.group(1))
        live = counts[key]
        if got != live:
            errors.append(
                f"COUNT-3 : derive '{label}' — §2 declare {got}, reel {live} "
                f"(§3 est la source declaree de cette colonne)."
            )
    return errors


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
    errors += check_section2_volumes(text, counts)
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
        "0 reference morte, compteurs §3 ET volumes §2 a jour."
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

    # 4. volumes §2 « Les trois couches »
    def registry_s2(contrats=10, doctrines=4, checkers=2, workflows=3, journal=""):
        return (
            "## 2. Les trois couches\n\n"
            "| Couche | Définition | Source canonique | Volume (cf. §3) |\n"
            "|---|---|---|---|\n"
            f"| **Vérité normative** | Ce que le système DOIT faire. | `../contrats/` "
            f"| {contrats} `.md` de contrats · {doctrines} doctrines |\n"
            f"| **Couverture mécanique** | Les contrôles. | `../../scripts/` "
            f"| {checkers} checkers |\n"
            f"| **CI exécutée** | Le sous-ensemble exécuté. | `../../.github/workflows/` "
            f"| {workflows} workflows — **ventilation détaillée au §3**, non recopiée ici |\n"
            "\n## 3. Compteurs\n\n" + journal
        )

    # 4a. volumes §2 conformes -> 0 erreur
    assert not check_section2_volumes(registry_s2(), counts), "selftest §2 conforme"

    # 4b. dérive §2 sur chacun des 4 volumes -> COUNT-3 (le bug réel du 2026-07-15)
    for kwargs, label in (
        ({"contrats": 291}, "contrats"),
        ({"doctrines": 99}, "doctrines"),
        ({"checkers": 80}, "checkers"),
        ({"workflows": 84}, "workflows"),
    ):
        errs = check_section2_volumes(registry_s2(**kwargs), counts)
        assert any("COUNT-3" in e for e in errs), f"selftest derive §2 {label}"

    # 4c. ligne §2 absente -> COUNT-2
    broken = registry_s2().replace("| **Couverture mécanique**", "| **Autre chose**")
    errs = check_section2_volumes(broken, counts)
    assert any("COUNT-2" in e for e in errs), "selftest ligne §2 absente"

    # 4d. section §2 absente -> COUNT-2
    errs = check_section2_volumes("## 3. Compteurs\n", counts)
    assert any("COUNT-2" in e for e in errs), "selftest section §2 absente"

    # 4e. ANTI-FAUX-POSITIF : le journal §8 est une trace historique datée,
    #     truffée de nombres périmés. Il ne doit JAMAIS être confronté au réel.
    #
    #     Deux protections indépendantes, testées séparément ci-dessous :
    #       (1) l'ANCRAGE sur les libellés de ligne §2 — protection primaire ;
    #       (2) le BORNAGE à la section §2 — défense en profondeur, seule
    #           protection si le journal REPRODUIT une ligne §2 (cas réel : une
    #           entrée qui documente une refonte du §2 en citant l'ancien
    #           tableau).
    #
    #     NB : un journal de prose ne suffit PAS à tester le bornage (aucune de
    #     ses lignes ne matche les libellés) — un tel test passerait même sans
    #     bornage, et ne prouverait rien.

    # (1) ancrage : de la prose historique truffée de nombres périmés est ignorée.
    journal_prose = (
        "## 8. Journal\n\n"
        "| 2026-07-01 | Compteurs -> 68 checkers - 72 workflows (68 contrats, 1:1). |\n"
        "| 2026-07-01 | contrats 267->290, doctrines 10->12, checkers 68->71, "
        "workflows total 72->75. |\n"
        "| 2026-06-20 | 80 checkers - 84 workflows (photographie perimee). |\n"
    )
    assert not check_section2_volumes(
        registry_s2(journal=journal_prose), counts
    ), "selftest journal §8 en prose ignore (ancrage sur les libelles)"

    # (2) bornage : ce que le bornage protège VRAIMENT.
    #
    #     `re.search` rend la PREMIERE occurrence, et §2 precede §8 : tant que la
    #     ligne §2 existe, elle est trouvee d'abord et un journal sosie est sans
    #     effet — le bornage ne se voit pas. Il devient load-bearing quand la
    #     ligne §2 DISPARAIT (renommee/reformulee) alors qu'un sosie subsiste au
    #     journal : sans bornage, la recherche tombe sur le sosie et lit une
    #     valeur qui n'est plus declaree en §2 -> COUNT-2 manque, la disparition
    #     passe en SILENCE. Avec bornage : COUNT-2.
    #
    #     Le sosie porte ici la valeur REELLE (2 checkers) : sans bornage le
    #     checker rendrait 0 erreur (faux negatif parfait). Ce cas TUE la
    #     mutation `body = text`.
    s2_ligne_disparue = registry_s2().replace(
        "| **Couverture mécanique**", "| **Couverture outillée**"
    )
    sosie_au_journal = (
        "## 8. Journal\n\n"
        "| 2026-06-20 | Refonte du §2 — ancien tableau conserve pour trace : |\n"
        "| **Couverture mécanique** | Les contrôles. | `../../scripts/` | 2 checkers |\n"
    )
    errs = check_section2_volumes(s2_ligne_disparue + sosie_au_journal, counts)
    assert any("COUNT-2" in e for e in errs), (
        "selftest bornage §2 : ligne §2 disparue + sosie au journal doit lever "
        "COUNT-2 (sans bornage, le sosie masque la disparition)"
    )

    # 5. topologie : conforme / orphelin / référence morte
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
