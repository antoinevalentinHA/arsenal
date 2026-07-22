#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : initialisation des paramètres VMC (VINIT)

Contrat (source normative) :
  00_documentation_arsenal/audits/04_chantiers/vmc/
    arbitrage_propriete_parametres_vmc.md   (invariant de propriété)
  00_documentation_arsenal/audits/04_chantiers/vmc/
    realisation_l70_parametres_vmc.md       (réalisation L7.0)

Objet contrôlé :
  11_automations/vmc/initialisation_parametres.yaml  (id 10190000000006)

MOTIVATION
  Les helpers de paramètres VMC n'ont pas de clé `initial:`. Leur sortie de
  l'état sans valeur est assurée par une automatisation, et non par un repli
  numérique — repli que la passe 5 de C35 interdit explicitement.

  Le risque n'est donc pas l'absence d'initialisation : c'est l'initialisation
  DE TROP. Réinitialiser un helper parce qu'il a été momentanément
  `unavailable` écraserait un réglage utilisateur sans que rien ne le signale.

  Ce checker VÉRIFIE LE COMPORTEMENT RÉEL du prédicat écrit dans le YAML : il
  extrait le gabarit Jinja du fichier et l'évalue contre cinq scénarios. Il ne
  reproduit AUCUNE logique — une copie du prédicat dans le test le rendrait
  aveugle à toute dérive du fichier contrôlé.

Règles :
  VINIT-000  Fichier, automatisation ou étape `a_initialiser` introuvable, ou
             gabarit non évaluable (ERROR).
  VINIT-001  Comportement du prédicat d'initialisation. Sémantique retenue,
             sans ambiguïté :
               A. `unavailable`                       -> JAMAIS d'écriture
               B. `unknown` persistant, entité par ailleurs disponible
                                                      -> INITIALISATION, cas
                  normal d'un helper nouvellement déclaré sans état à
                  restaurer, après la persistance exigée par le déclencheur et
                  l'attente bornée (VINIT-002). L'exclure empêcherait tout
                  amorçage
               C. état numérique, y compris différent de l'amorce
                                                      -> CONSERVATION ABSOLUE
               D. épisode `unavailable` puis restauration numérique
                                                      -> AUCUNE réinitialisation
               E. état disponible non numérique quelconque
                                                      -> initialisation
             (ERROR par scénario en échec)
  VINIT-002  Attente bornée présente et effectivement bornée : `wait_template`
             avec `timeout` ET `continue_on_timeout: true`, et `for:` sur le
             déclencheur d'état — sans quoi une indisponibilité passagère
             déclencherait une réinitialisation (ERROR).
  VINIT-003  Aucun repli numérique silencieux : le prédicat ne doit comparer
             qu'à `none`, jamais à une valeur de repli chiffrée (ERROR).
  VINIT-004  Écriture conditionnée : la séquence contient la garde
             `a_initialiser | count > 0` (ERROR).
  VINIT-005  Table d'amorce complète et cohérente avec les helpers déclarés
             dans 03_input_numbers/vmc/ (ERROR).

Logique Arsenal habituelle : ERROR => exit 1 ; régression du checker lui-même
(`--selftest`) => exit 2.

Usage :
  python scripts/arsenal_contracts/check_vmc_initialisation_contracts.py
  python scripts/arsenal_contracts/check_vmc_initialisation_contracts.py --selftest
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import yaml
from jinja2 import Environment

ROOT = Path(__file__).resolve().parents[2]
AUTOMATION = ROOT / "11_automations" / "vmc" / "initialisation_parametres.yaml"
HELPERS = [
    ROOT / "03_input_numbers" / "vmc" / "seuils" / "humidite_par_piece.yaml",
    ROOT / "03_input_numbers" / "vmc" / "bornes_frontiere.yaml",
]

ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def ok(message: str) -> None:
    print(f"  ✔ {message}")


# ---------------------------------------------------------------------------
# Extraction — aucune logique n'est reproduite ici
# ---------------------------------------------------------------------------

def charger_automation(path: Path) -> dict:
    blocs = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(blocs, list) or not blocs:
        raise ValueError("automatisation absente ou mal formée")
    return blocs[0]


def etapes(auto: dict) -> list:
    return auto.get("action") or auto.get("actions") or []


def gabarit_predicat(auto: dict) -> str:
    """Gabarit Jinja de `a_initialiser`, lu dans le fichier contrôlé."""
    for etape in etapes(auto):
        if isinstance(etape, dict) and "variables" in etape:
            v = etape["variables"]
            if isinstance(v, dict) and "a_initialiser" in v:
                return v["a_initialiser"]
    raise ValueError("étape `variables: a_initialiser` introuvable")


def gabarit_attente(auto: dict) -> dict:
    for etape in etapes(auto):
        if isinstance(etape, dict) and "wait_template" in etape:
            return etape
    raise ValueError("étape `wait_template` introuvable")


def evaluer(gabarit: str, etats: dict, amorces: list) -> list:
    """Rend le gabarit réel avec un `states()` simulé et renvoie la liste."""
    env = Environment()
    rendu = env.from_string(gabarit).render(
        amorces=amorces,
        states=lambda e: etats.get(e, "unknown"),
    )
    valeur = ast.literal_eval(rendu.strip())
    return [a["entite"] for a in valeur]


# ---------------------------------------------------------------------------
# VINIT-001 — les cinq scénarios
# ---------------------------------------------------------------------------

def test_scenarios(auto: dict) -> None:
    amorces = auto["variables"]["amorces"]
    gabarit = gabarit_predicat(auto)
    cible = amorces[0]["entite"]
    autres = {a["entite"]: "70.0" for a in amorces[1:]}

    def selectionne(etat: str) -> bool:
        etats = dict(autres)
        etats[cible] = etat
        return cible in evaluer(gabarit, etats, amorces)

    scenarios = [
        ("A. `unavailable` -> JAMAIS d'écriture",
         "unavailable", False),
        ("B. `unknown` persistant, entité disponible -> INITIALISATION",
         "unknown", True),
        ("C. numérique égal à l'amorce -> conservation",
         "74.0", False),
        ("C bis. numérique DIFFÉRENT de l'amorce -> conservation",
         "68.0", False),
        ("C ter. numérique hors plage d'amorce -> conservation",
         "90.0", False),
        ("E. disponible, chaîne vide -> initialisation",
         "", True),
        ("E bis. disponible, état non numérique quelconque -> initialisation",
         "indisponible_capteur", True),
    ]

    for libelle, etat, attendu in scenarios:
        try:
            obtenu = selectionne(etat)
        except Exception as exc:                      # noqa: BLE001
            fail(f"VINIT-000 — gabarit non évaluable ({libelle}) : {exc}")
            return
        if obtenu != attendu:
            fail(
                f"VINIT-001 — scénario « {libelle} » : état {etat!r} => "
                f"{'initialisé' if obtenu else 'non initialisé'}, "
                f"attendu {'initialisé' if attendu else 'non initialisé'}"
            )
        else:
            ok(f"VINIT-001 — {libelle}")

    # ----- D. Épisode d'indisponibilité, joué comme une séquence -----------
    # Le predicat est sans mémoire : la démonstration porte donc sur les deux
    # instants de l'épisode, pendant et après. Si l'un des deux retenait le
    # helper, une valeur utilisateur serait écrasée après une simple panne.
    sequence = [("avant l'épisode, valeur utilisateur", "68.0", False),
                ("pendant l'épisode", "unavailable", False),
                ("après restauration numérique", "68.0", False)]
    echec = False
    for instant, etat, attendu in sequence:
        if selectionne(etat) != attendu:
            fail(
                f"VINIT-001 — scénario D, {instant} : état {etat!r} retenu "
                "pour initialisation ; une indisponibilité passagère "
                "écraserait la valeur utilisateur"
            )
            echec = True
    if not echec:
        ok("VINIT-001 — D. épisode `unavailable` puis restauration numérique "
           "-> aucune réinitialisation, aux trois instants")

    # ----- Contrôle croisé -------------------------------------------------
    etats = dict(autres)
    etats[cible] = "unknown"
    retenus = evaluer(gabarit, etats, amorces)
    if set(retenus) != {cible}:
        fail(
            "VINIT-001 — un helper déjà numérique a été retenu pour "
            f"initialisation : {sorted(set(retenus) - {cible})}"
        )
    else:
        ok("VINIT-001 — seul le helper sans valeur est retenu, jamais les "
           "neuf autres, déjà numériques")

    # ----- Amorçabilité : sans `unknown`, aucun helper neuf ne démarrerait --
    tous_neufs = {a["entite"]: "unknown" for a in amorces}
    retenus = evaluer(gabarit, tous_neufs, amorces)
    if len(retenus) != len(amorces):
        fail(
            "VINIT-001 — un déploiement neuf, où tous les helpers valent "
            f"`unknown`, n'amorcerait que {len(retenus)}/{len(amorces)} "
            "helpers : les autres resteraient définitivement sans valeur"
        )
    else:
        ok(f"VINIT-001 — déploiement neuf : les {len(amorces)} helpers "
           "`unknown` sont tous amorçables")


# ---------------------------------------------------------------------------
# VINIT-002 — attente bornée
# ---------------------------------------------------------------------------

def test_attente_bornee(auto: dict) -> None:
    try:
        attente = gabarit_attente(auto)
    except ValueError as exc:
        fail(f"VINIT-002 — {exc}")
        return

    if "timeout" not in attente:
        fail("VINIT-002 — `wait_template` sans `timeout` : attente non bornée")
    elif attente.get("continue_on_timeout") is not True:
        fail(
            "VINIT-002 — `continue_on_timeout` doit valoir true : sinon "
            "l'expiration de l'attente annule l'initialisation en silence"
        )
    else:
        ok(f"VINIT-002 — attente bornée à {attente['timeout']}, non bloquante")

    declencheurs = auto.get("trigger") or auto.get("triggers") or []
    etat = [t for t in declencheurs if t.get("platform") == "state"
            or t.get("trigger") == "state"]
    if not etat:
        fail("VINIT-002 — aucun déclencheur d'état")
        return
    sans_for = [t for t in etat if not t.get("for")]
    if sans_for:
        fail(
            "VINIT-002 — déclencheur d'état sans `for:` : une indisponibilité "
            "passagère provoquerait une réinitialisation"
        )
    else:
        ok(f"VINIT-002 — persistance exigée avant déclenchement "
           f"({etat[0]['for']})")


# ---------------------------------------------------------------------------
# VINIT-003 / VINIT-004
# ---------------------------------------------------------------------------

def test_aucun_repli(auto: dict) -> None:
    gabarit = gabarit_predicat(auto)
    compact = gabarit.replace(" ", "")
    if "float(none)" not in compact:
        fail(
            "VINIT-003 — le prédicat doit convertir avec `float(none)` : "
            "toute autre valeur de repli masquerait l'absence de valeur"
        )
        return
    for repli in ("float(0", "float(1", "float(2", "float(3", "float(4",
                  "float(5", "float(6", "float(7", "float(8", "float(9"):
        if repli in compact:
            fail(f"VINIT-003 — repli numérique silencieux détecté : `{repli}…`")
            return
    ok("VINIT-003 — aucun repli numérique silencieux")


def test_garde_ecriture(auto: dict) -> None:
    for etape in etapes(auto):
        if isinstance(etape, dict) and "condition" in etape:
            gabarit = str(etape.get("value_template", ""))
            if "a_initialiser" in gabarit and "count" in gabarit:
                ok("VINIT-004 — écriture conditionnée à un besoin réel")
                return
    fail("VINIT-004 — garde `a_initialiser | count > 0` absente")


# ---------------------------------------------------------------------------
# VINIT-005 — table d'amorce complète
# ---------------------------------------------------------------------------

def test_table_amorce(auto: dict) -> None:
    declares: set[str] = set()
    for path in HELPERS:
        if not path.is_file():
            fail(f"VINIT-005 — fichier de helpers introuvable : {path}")
            return
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        declares |= {f"input_number.{k}" for k in data}

    amorces = {a["entite"] for a in auto["variables"]["amorces"]}
    manquants = declares - amorces
    inconnus = amorces - declares

    if manquants:
        fail(
            "VINIT-005 — helper déclaré sans valeur d'amorce, il resterait "
            f"sans valeur : {sorted(manquants)}"
        )
    if inconnus:
        fail(
            "VINIT-005 — amorce visant un helper non déclaré : "
            f"{sorted(inconnus)}"
        )
    if not manquants and not inconnus:
        ok(f"VINIT-005 — {len(amorces)} helpers déclarés, tous amorçables")

    declencheurs = auto.get("trigger") or auto.get("triggers") or []
    surveilles: set[str] = set()
    for t in declencheurs:
        e = t.get("entity_id")
        if isinstance(e, str):
            surveilles.add(e)
        elif isinstance(e, list):
            surveilles |= set(e)
    if surveilles != declares:
        fail(
            "VINIT-005 — déclencheur d'état et helpers déclarés divergent : "
            f"{sorted(declares ^ surveilles)}"
        )
    else:
        ok("VINIT-005 — tous les helpers déclarés sont surveillés")


# ---------------------------------------------------------------------------
# Auto-test — le checker doit détecter un prédicat fautif
# ---------------------------------------------------------------------------

MUTANTS = [
    # Réinitialise sur `unavailable` : écraserait un réglage utilisateur
    # après une simple indisponibilité.
    ("{% set ns = namespace(liste=[]) %}"
     "{% for a in amorces %}{% set etat = states(a.entite) %}"
     "{% if etat | float(none) is none %}"
     "{% set ns.liste = ns.liste + [a] %}{% endif %}{% endfor %}"
     "{{ ns.liste }}",
     "unavailable", False),
    # Repli numérique : ne détecte plus l'absence de valeur.
    ("{% set ns = namespace(liste=[]) %}"
     "{% for a in amorces %}{% set etat = states(a.entite) %}"
     "{% if etat != 'unavailable' and etat | float(0) == 0 %}"
     "{% set ns.liste = ns.liste + [a] %}{% endif %}{% endfor %}"
     "{{ ns.liste }}",
     "unknown", True),
]


def selftest() -> int:
    amorces = [{"entite": "input_number.t1", "valeur": 74},
               {"entite": "input_number.t2", "valeur": 50}]
    regressions = []

    # Le mutant 1 doit initialiser sur `unavailable` — c'est le défaut qu'il
    # injecte. Si l'évaluateur ne le voit pas, il est aveugle.
    retenus = evaluer(MUTANTS[0][0], {"input_number.t1": "unavailable",
                                      "input_number.t2": "50.0"}, amorces)
    if "input_number.t1" not in retenus:
        regressions.append(
            "auto-test : le mutant réinitialisant sur `unavailable` n'est "
            "pas détecté par l'évaluateur"
        )

    # Le mutant 2 doit retenir un helper valant 0 — repli silencieux.
    retenus = evaluer(MUTANTS[1][0], {"input_number.t1": "0",
                                      "input_number.t2": "50.0"}, amorces)
    if "input_number.t1" not in retenus:
        regressions.append(
            "auto-test : le mutant à repli numérique n'est pas détecté"
        )

    # Le prédicat réel, lui, ne doit retenir NI l'un NI l'autre.
    reel = gabarit_predicat(charger_automation(AUTOMATION))
    retenus = evaluer(reel, {"input_number.t1": "unavailable",
                             "input_number.t2": "0"}, amorces)
    if retenus:
        regressions.append(
            f"auto-test : le prédicat réel retient à tort {retenus}"
        )

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

    print("Arsenal — Validation contractuelle : initialisation des "
          "paramètres VMC")
    print("")

    if not AUTOMATION.is_file():
        print(f"\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        print(f"- VINIT-000 — automatisation introuvable : {AUTOMATION}")
        return 1

    try:
        auto = charger_automation(AUTOMATION)
    except Exception as exc:                          # noqa: BLE001
        print(f"\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        print(f"- VINIT-000 — automatisation illisible : {exc}")
        return 1

    for test in (test_scenarios, test_attente_bornee, test_aucun_repli,
                 test_garde_ecriture, test_table_amorce):
        try:
            test(auto)
        except Exception as exc:                      # noqa: BLE001
            fail(f"VINIT-000 — {test.__name__} : {exc}")

    if ERRORS:
        print("\n❌ CONTRAT VMC_INITIALISATION NON CONFORME\n")
        for e in ERRORS:
            print(f"- {e}")
        return 1

    print("\n✅ CONTRAT VMC_INITIALISATION CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
