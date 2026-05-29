"""Lot 2.5 — cli_decision, surface CI etage-2 (region decision).

Deux sections au statut epistemique DISTINCT :

  1. MECANISME (hermetique) : agregation, mapping d'exit code, ecriture JSON.
     Le comportement des regles est deja couvert par 2.3 / 2.4 ; on ne teste ici
     que le CABLAGE. Echec ici => defaut de cli_decision.

  2. SMOKE LIVE (plan 2) : executer_ch1 tourne de bout en bout sur le runtime
     reel et ne renvoie pas d'erreur d'execution. On n'affirme PAS le nombre de
     violations (cela appartient a 2.3 / 2.4 et changerait a CH-2).
     Echec ici => cablage casse OU runtime illisible, a trier comme tel.
"""
import pytest

from arsenal_ci.decision import cli_decision
from arsenal_ci.report.result import ExecutionError, ExitCode
from arsenal_ci.report.violation import Violation
from arsenal_ci.rules.policy import Severity


def _v(rule="R-X", source="s", target="t", sev=Severity.BLOCKING):
    return Violation(
        rule=rule, message="m", source=source, target=target,
        file="f", host_key="h", severity=sev,
    )


# =====================================================================
# 1. MECANISME  (echec ici => defaut de cli_decision)
# =====================================================================

def test_agreger_vide_conforme():
    r = cli_decision.agreger([])
    assert r.execution_error is None
    assert r.exit_code() == ExitCode.PASS
    assert r.summary.blocking == 0


def test_agreger_violation_bloquante_exit_1():
    r = cli_decision.agreger([_v(sev=Severity.BLOCKING)])
    assert r.exit_code() == ExitCode.VIOLATION
    assert r.summary.blocking == 1


def test_agreger_tri_deterministe():
    a = _v(rule="R-B", source="a")
    b = _v(rule="R-A", source="b")
    r = cli_decision.agreger([a, b])
    # Tri (severite, rule, file, source, target) -> R-A avant R-B.
    assert [v.rule for v in r.violations] == ["R-A", "R-B"]


def test_execution_error_exit_2(monkeypatch):
    def boom():
        raise ExecutionError("entree illisible")

    monkeypatch.setattr(cli_decision, "_collecter", boom)
    r = cli_decision.executer_ch1()
    assert r.execution_error is not None
    assert r.exit_code() == ExitCode.EXECUTION_ERROR


def test_main_conforme_ecrit_json(monkeypatch, tmp_path):
    monkeypatch.setattr(cli_decision, "_collecter", lambda: [])
    out = tmp_path / "decision.json"
    code = cli_decision.main(["--json", str(out)])
    assert code == int(ExitCode.PASS)
    assert out.exists()


def test_main_violation_exit_1(monkeypatch):
    monkeypatch.setattr(cli_decision, "_collecter", lambda: [_v()])
    assert cli_decision.main([]) == int(ExitCode.VIOLATION)


# =====================================================================
# 2. SMOKE LIVE (plan 2)
#
# Echec ici => cablage casse OU runtime illisible (a trier), PAS un faux
# verdict. On verifie seulement que l'outil tourne sur le runtime reel.
# =====================================================================

def test_smoke_live_executer_ch1():
    r = cli_decision.executer_ch1()
    assert r.execution_error is None