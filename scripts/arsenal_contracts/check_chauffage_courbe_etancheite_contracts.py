#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Chauffage — Étanchéité de l'observabilité courbe
Contrat : 76_observabilite_auto_ajustement_courbe.md (§9 séparation runtime/diagnostic,
          §10 INV-2 étanchéité)

Rend OPPOSABLE et BLOQUANT l'invariant INV-2 (jusqu'ici seulement porté en warn-only
par le graphe chauffage) : le flux d'observabilité est unidirectionnel
(capture → conservation → dérivation → présentation) et AUCUNE grandeur dérivée
d'observabilité de la courbe NE réentre dans la cascade de décision.

Garde du lot L5 (phase P5, écart É-11), posée AVANT les dérivés L5 :
  - T01 — le chemin décisionnel `auto_ajustement.yaml` ne LIT aucune entité
          d'observabilité courbe (liste fermée L1–L5) ;
  - T02 — confinement : dans la surface logique chauffage (scripts + automations),
          ces entités n'apparaissent QUE dans la couche d'observabilité (allowlist) ;
  - T03 — intégrité de la garde : cibles et liste fermée cohérentes.

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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# Chemins & liste fermée
# ---------------------------------------------------------------------------

DECISION_FILE = ROOT / "11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml"

# Surface logique chauffage (là où vit la décision ; les capteurs template et
# statistics des dossiers 12/13 ne sont pas de la logique décisionnelle).
SCAN_DIRS = [ROOT / "10_scripts/chauffage", ROOT / "11_automations/chauffage"]

# Fichiers de la COUCHE d'observabilité — seuls autorisés à référencer les
# grandeurs d'observabilité courbe dans la surface logique (allowlist).
OBSERVABILITY_FILES = {
    "11_automations/chauffage/courbe_de_chauffe/observabilite_completude_apprentissage.yaml",  # L4
    "11_automations/chauffage/courbe_de_chauffe/observabilite_derivation_courbe.yaml",         # L5
}

# Liste FERMÉE des grandeurs d'observabilité courbe (entités d'état / compteurs).
# NB : les ÉVÉNEMENTS (chauffage_courbe_cycle_evalue / _gel_episode) ne sont pas des
# entités et n'y figurent pas — leur émission par la décision est la capture (L1),
# pas une réentrée de grandeur dérivée.
OBSERVABILITY_ENTITIES = [
    # L4 — complétude & apprentissage (livrés)
    "chauffage_courbe_dernier_cycle",
    "chauffage_courbe_apprentissage_statut",
    "chauffage_courbe_gel_cause",
    "chauffage_courbe_completude",
    "chauffage_courbe_apprenant_num",
    "chauffage_courbe_taux_jours_apprenants",
    # L5 — dérivation diagnostic (planifiés ; la garde est posée d'avance)
    "chauffage_courbe_derive_pente",
    "chauffage_courbe_derive_parallele",
    "chauffage_courbe_reversions",
    "chauffage_courbe_refus_consecutifs",
    "chauffage_courbe_persistance",
    "chauffage_courbe_dernier_sens_pente",
    "chauffage_courbe_dernier_sens_parallele",
]


def entities_referenced(content: str) -> list[str]:
    body = strip_comments(content)
    return [e for e in OBSERVABILITY_ENTITIES if e in body]


# ---------------------------------------------------------------------------
# T01 — Décision étanche : auto_ajustement.yaml ne lit aucune grandeur d'obs. (INV-2)
# ---------------------------------------------------------------------------

def test_decision_etanche():
    """
    §9 / INV-2 : la décision NE consomme aucune grandeur dérivée d'observabilité.
    Le chemin décisionnel de la courbe (`auto_ajustement.yaml`) ne doit référencer
    AUCUNE entité de la liste fermée d'observabilité — sinon une grandeur de
    diagnostic redeviendrait entrée de décision (rupture d'étanchéité).
    """
    check(DECISION_FILE.is_file(), f"T01 — chemin décisionnel absent ({rel(DECISION_FILE)})")
    leaked = entities_referenced(read(DECISION_FILE))
    check(
        not leaked,
        f"T01 — la décision {rel(DECISION_FILE)} lit une grandeur d'observabilité : "
        f"{leaked} — rupture d'étanchéité (76 §9 / INV-2)",
    )
    ok("T01 — décision étanche : aucune grandeur d'observabilité lue (INV-2)")


# ---------------------------------------------------------------------------
# T02 — Confinement : les grandeurs d'obs. ne vivent que dans la couche obs.
# ---------------------------------------------------------------------------

def test_confinement_couche_observabilite():
    """
    §9 / INV-2 : sens unidirectionnel. Dans la surface logique chauffage
    (10_scripts/chauffage + 11_automations/chauffage), toute référence à une
    grandeur d'observabilité courbe ne doit apparaître QUE dans les fichiers de
    la couche d'observabilité (allowlist). Toute autre référence signale qu'un
    fichier de décision/exécution touche une grandeur dérivée.
    """
    for scan_dir in SCAN_DIRS:
        for path in yaml_files(scan_dir):
            if rel(path) in OBSERVABILITY_FILES:
                continue
            leaked = entities_referenced(read(path))
            check(
                not leaked,
                f"T02 — {rel(path)} (hors couche observabilité) référence "
                f"{leaked} — confinement rompu (76 §9 / INV-2)",
            )
    ok("T02 — grandeurs d'observabilité confinées à la couche d'observabilité (INV-2)")


# ---------------------------------------------------------------------------
# T03 — Intégrité de la garde (cibles présentes, allowlist réelle)
# ---------------------------------------------------------------------------

def test_integrite_garde():
    """
    La garde n'a de valeur que si ses cibles existent : le chemin décisionnel et
    les fichiers d'allowlist doivent être présents (sinon la garde passerait à
    vide). Vérifie aussi que la liste fermée est non triviale.
    """
    check(DECISION_FILE.is_file(), f"T03 — cible décision absente ({rel(DECISION_FILE)})")
    for allowed in sorted(OBSERVABILITY_FILES):
        check(
            (ROOT / allowed).is_file(),
            f"T03 — fichier d'allowlist observabilité absent : {allowed} "
            f"(mettre à jour la garde si le fichier a été renommé/déplacé)",
        )
    check(
        len(OBSERVABILITY_ENTITIES) >= 6,
        "T03 — liste fermée d'entités d'observabilité anormalement courte",
    )
    ok("T03 — intégrité de la garde (cibles et allowlist présentes)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_decision_etanche,
    test_confinement_couche_observabilite,
    test_integrite_garde,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Chauffage : étanchéité de l'observabilité courbe (INV-2)\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT CHAUFFAGE_COURBE_ETANCHEITE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CHAUFFAGE_COURBE_ETANCHEITE CONFORME")
