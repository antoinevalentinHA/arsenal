"""Lot 3.2 — R-CALL-1, controles runtime + meta-test + isolation (frontiere exec).

Statut epistemique : CONTROLES (lecture seule du runtime reel) et GARDES de
gouvernance. Distinct du lot 3.1 (preuve hermetique du mecanisme).

  1. CONTROLE runtime : la topologie d'appel reelle est conforme (les 3 appelants
     contractualises, et eux seuls, invoquent la cible). Un rouge ici = ajout
     d'un appelant non contractualise dans le runtime (regression REELLE).
  2. META-TEST (A2) : la constante `APPELANTS_AUTORISES` == l'allow-list NORMATIVE
     du contrat (bloc sentinelle). Un rouge ici = derive contrat <-> code.
  3. ISOLATION : R-CALL-1 n'est pas greffe dans l'orchestrateur etage-1.
"""
from arsenal_ci.execution import r_call_1
from arsenal_ci.execution.cli_execution import executer
from arsenal_ci.report import orchestrator
from arsenal_ci.report.result import ExitCode
from arsenal_ci.rules.policy import Severity


# --------------------------------------------------------- 1. controle runtime

def test_runtime_topologie_conforme():
    violations = r_call_1.analyser()
    bloquants = [v for v in violations if v.severity is Severity.BLOCKING]
    assert bloquants == [], (
        "Appelant(s) non contractualise(s) detecte(s) dans le runtime : "
        + ", ".join(v.source for v in bloquants)
    )


def test_runtime_pas_de_divergence_inverse():
    warnings = [
        v for v in r_call_1.analyser() if v.severity is Severity.WARNING
    ]
    assert warnings == [], (
        "Appelant(s) contractualise(s) sans site d'appel : "
        + ", ".join(v.source for v in warnings)
    )


def test_cli_runtime_pass():
    assert executer().exit_code() is ExitCode.PASS


# ----------------------------------------------------- 2. meta-test contrat (A2)

def test_allowlist_constante_egale_contrat():
    assert r_call_1.lire_allowlist_contrat() == r_call_1.APPELANTS_AUTORISES


def test_allowlist_contient_les_trois_appelants():
    assert r_call_1.APPELANTS_AUTORISES == frozenset(
        {
            "10_scripts/chauffage/decision_centrale.yaml",
            "11_automations/chauffage/retry_transactionnel/declenchement.yaml",
            "11_automations/chauffage/modification_consigne.yaml",
        }
    )


# --------------------------------------------------------------- 3. isolation

def test_rcall1_hors_orchestrateur_etage1():
    # R-CALL-1 est un analyseur parallele : aucune de ses fonctions ne doit
    # figurer dans orchestrator.RULES (graphe template, etage-1).
    for rule in orchestrator.RULES:
        assert "execution" not in getattr(rule, "__module__", ""), (
            "R-CALL-1 ne doit pas etre greffe dans l'orchestrateur etage-1."
        )
