#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : amorçage des paramètres VMC (VINIT)

Contrat (source normative) :
  00_documentation_arsenal/audits/04_chantiers/vmc/
    arbitrage_propriete_parametres_vmc.md   (invariant de propriété)
  00_documentation_arsenal/audits/04_chantiers/vmc/
    correctif_deploiement_l7_vmc.md         (constat de déploiement)

CE QUE CE CHECKER GARDE, ET POURQUOI IL A CHANGÉ D'OBJET
  Sa version initiale vérifiait le comportement d'une automatisation
  d'initialisation qui écrivait les valeurs d'amorce lorsqu'un helper était
  « disponible et non numérique ».

  **Cette condition ne peut jamais être vraie.** Un `input_number` sans état
  restaurable ne prend pas `unknown` : il prend son `min`. Vérifié sur les 38
  bases du corpus — 73 helpers, 32 065 lignes d'état, AUCUN état non
  numérique — et constaté au déploiement : aucune notification émise, les dix
  helpers chargés à leur minimum.

  Le mécanisme a donc été retiré et remplacé par un **amorçage manuel
  explicite**, sans déclencheur.

  Ce checker garde désormais l'ABSENCE de tout retour en arrière.

Règles :
  VINIT-000  Automatisation d'amorçage introuvable ou illisible (ERROR).
  VINIT-001  L'amorçage n'a AUCUN déclencheur : il ne doit jamais pouvoir
             s'exécuter de lui-même (ERROR).
  VINIT-002  Aucune automatisation VMC ne conditionne une écriture de
             paramètre à `unknown` / `unavailable` sur un `input_number` :
             ce prédicat est structurellement inopérant (ERROR).
  VINIT-003  Aucun repli numérique silencieux dans la table d'amorce (ERROR).
  VINIT-004  Table d'amorce complète : tout helper de paramètre déclaré par
             le domaine y figure, et réciproquement (ERROR).

Logique Arsenal habituelle : ERROR => exit 1 ; régression du checker lui-même
(`--selftest`) => exit 2.

Usage :
  python scripts/arsenal_contracts/check_vmc_initialisation_contracts.py
  python scripts/arsenal_contracts/check_vmc_initialisation_contracts.py --selftest
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
AMORCAGE = ROOT / "11_automations" / "vmc" / "amorcage_parametres.yaml"
AUTOMATIONS_VMC = ROOT / "11_automations" / "vmc"
HELPERS = [
    ROOT / "03_input_numbers" / "vmc" / "seuils" / "humidite_par_piece.yaml",
    ROOT / "03_input_numbers" / "vmc" / "bornes_frontiere.yaml",
]

# Prédicat structurellement inopérant : un `input_number` sans état
# restaurable prend son `min`, jamais `unknown` ni `unavailable`.
PREDICAT_INOPERANT = re.compile(
    r"input_number[^\n]{0,120}(unknown|unavailable)"
    r"|(unknown|unavailable)[^\n]{0,120}input_number"
)

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def ok(message: str) -> None:
    print(f"  ✔ {message}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def charger(path: Path) -> dict:
    blocs = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(blocs, list) or not blocs:
        raise ValueError("automatisation absente ou mal formée")
    return blocs[0]


# ---------------------------------------------------------------------------
# VINIT-001 — aucun déclencheur
# ---------------------------------------------------------------------------

def test_sans_declencheur(auto: dict) -> None:
    declencheurs = auto.get("trigger", auto.get("triggers", None))
    if declencheurs:
        fail(
            "VINIT-001 — l'amorçage porte un déclencheur : il pourrait "
            "s'exécuter de lui-même et écraser un réglage délibéré. Une fois "
            "un helper à son minimum, rien ne distingue « jamais initialisé » "
            "de « réglé au minimum »"
        )
    else:
        ok("VINIT-001 — amorçage sans déclencheur, manuel exclusivement")


# ---------------------------------------------------------------------------
# VINIT-002 — le prédicat inopérant ne doit pas revenir
# ---------------------------------------------------------------------------

def test_predicat_inoperant() -> None:
    coupables = []
    for path in sorted(AUTOMATIONS_VMC.glob("*.yaml")):
        for ligne in read(path).splitlines():
            nu = ligne.strip()
            if nu.startswith("#"):
                continue
            if PREDICAT_INOPERANT.search(nu):
                coupables.append(f"{path.name} → {nu[:90]}")
                break
    if coupables:
        for c in coupables:
            fail(
                "VINIT-002 — une automatisation VMC conditionne un paramètre "
                f"à `unknown`/`unavailable` : {c}. Ce prédicat est "
                "structurellement inopérant — un `input_number` sans état "
                "restaurable prend son `min`"
            )
    else:
        ok("VINIT-002 — aucun prédicat fondé sur `unknown`/`unavailable` "
           "pour un paramètre")


# ---------------------------------------------------------------------------
# VINIT-003 / VINIT-004 — table d'amorce
# ---------------------------------------------------------------------------

def _amorces(auto: dict) -> list:
    return (auto.get("variables") or {}).get("amorces") or []


def test_aucun_repli(auto: dict) -> None:
    brut = read(AMORCAGE)
    for repli in ("float(0", "float(1", "float(2", "float(3", "float(4",
                  "float(5", "float(6", "float(7", "float(8", "float(9",
                  "int(0", "int(1", "int(2", "int(3", "int(4",
                  "int(5", "int(6", "int(7", "int(8", "int(9"):
        if repli in brut.replace(" ", ""):
            fail(f"VINIT-003 — repli numérique silencieux : `{repli}…`")
            return
    ok("VINIT-003 — aucun repli numérique silencieux")


def test_table_complete(auto: dict) -> None:
    declares: set[str] = set()
    for path in HELPERS:
        if not path.is_file():
            fail(f"VINIT-004 — fichier de helpers introuvable : {path}")
            return
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        declares |= {f"input_number.{k}" for k in data}

    amorces = {a["entite"] for a in _amorces(auto)}
    manquants = sorted(declares - amorces)
    inconnus = sorted(amorces - declares)

    if manquants:
        fail(
            "VINIT-004 — helper déclaré sans valeur d'amorce, il resterait à "
            f"son `min` : {manquants}"
        )
    if inconnus:
        fail(f"VINIT-004 — amorce visant un helper non déclaré : {inconnus}")
    if not manquants and not inconnus:
        ok(f"VINIT-004 — {len(amorces)} helpers déclarés, tous amorçables")


# ---------------------------------------------------------------------------
# Auto-test
# ---------------------------------------------------------------------------

def selftest() -> int:
    regressions = []

    mutant_declencheur = {"trigger": [{"platform": "homeassistant",
                                       "event": "start"}]}
    avant = len(ERRORS)
    test_sans_declencheur(mutant_declencheur)
    if len(ERRORS) == avant:
        regressions.append("auto-test : un amorçage déclenché n'est pas détecté")
    del ERRORS[avant:]

    if not PREDICAT_INOPERANT.search(
            "{{ states('input_number.x') in ['unknown','unavailable'] }}"):
        regressions.append(
            "auto-test : le prédicat inopérant n'est pas reconnu")
    if PREDICAT_INOPERANT.search("{{ states('sensor.x') == 'unknown' }}"):
        regressions.append(
            "auto-test : faux positif — un `sensor` n'est pas un paramètre")

    if regressions:
        print("\n❌ RÉGRESSION DU CHECKER VMC_INITIALISATION\n")
        for r in regressions:
            print(f"- {r}")
        return 2
    print("✅ AUTO-TEST VMC_INITIALISATION CONFORME")
    return 0


# ---------------------------------------------------------------------------

def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()

    print("Arsenal — Validation contractuelle : amorçage des paramètres VMC")
    print("")

    if not AMORCAGE.is_file():
        print("\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        print(f"- VINIT-000 — amorçage introuvable : {AMORCAGE}")
        return 1

    try:
        auto = charger(AMORCAGE)
    except Exception as exc:                          # noqa: BLE001
        print("\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        print(f"- VINIT-000 — amorçage illisible : {exc}")
        return 1

    for test in (test_sans_declencheur, test_aucun_repli, test_table_complete):
        try:
            test(auto)
        except Exception as exc:                      # noqa: BLE001
            fail(f"VINIT-000 — {test.__name__} : {exc}")
    try:
        test_predicat_inoperant()
    except Exception as exc:                          # noqa: BLE001
        fail(f"VINIT-000 — test_predicat_inoperant : {exc}")

    if ERRORS:
        print("\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        for e in ERRORS:
            print(f"- {e}")
        return 1

    print("\n✅ CONTRAT VMC_INITIALISATION CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
