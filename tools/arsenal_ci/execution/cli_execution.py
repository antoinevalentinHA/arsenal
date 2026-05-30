"""CLI du validateur de frontiere d'execution Chauffage (CH-4 / R-CALL-1).

Troisieme analyseur Arsenal, parallele a l'etage-1 (cli) et a l'etage-2
(decision/cli_decision). Verdict sur le runtime reel.

Usage :
    python -m arsenal_ci.execution.cli_execution [--json OUT] [--strict]

Exit codes (identiques au reste du moteur) :
    0  conforme
    1  violation doctrinale (appelant non autorise)
    2  erreur d'execution (entree illisible / outil casse)

Frontiere d'erreur : une entree illisible remonte en ExecutionError (exit 2),
jamais en violation. R-CALL-1 n'est PAS enregistree dans orchestrator.RULES
(isolation : etage-1 template / etage-2 decision / frontiere d'execution).
"""
from __future__ import annotations

import argparse
import sys
from typing import List

from ..report import formatters
from ..report.result import ExecutionError, Result, summarise
from ..report.violation import Violation
from ..rules.policy import Severity
from . import r_call_1

_SEVERITE_RANG = {
    Severity.BLOCKING: 0,
    Severity.ERROR: 1,
    Severity.WARNING: 2,
    Severity.IGNORE: 3,
}


def _cle_tri(v: Violation):
    return (_SEVERITE_RANG.get(v.severity, 99), v.rule, v.file, v.source, v.target)


def agreger(violations: List[Violation]) -> Result:
    """Agrege une liste de violations en un Result trie deterministe."""
    ordonnees = sorted(violations, key=_cle_tri)
    return Result(violations=ordonnees, summary=summarise(ordonnees))


def _collecter() -> List[Violation]:
    """Applique R-CALL-1 au runtime. Peut lever ExecutionError."""
    return r_call_1.analyser()


def executer() -> Result:
    """Verdict frontiere d'execution sur le runtime reel."""
    try:
        violations = _collecter()
    except ExecutionError as exc:
        return Result(execution_error=str(exc))
    except Exception as exc:  # defensif : tout echec inattendu = erreur d'execution
        return Result(execution_error=f"Echec interne du validateur R-CALL-1 : {exc}")
    return agreger(violations)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="arsenal-ci-execution")
    parser.add_argument("--json", dest="json_out", default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    result = executer()

    print(formatters.format_human(result, strict=args.strict))

    if args.json_out is not None:
        try:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                fh.write(formatters.format_json(result, strict=args.strict))
        except OSError as exc:
            print(f"\n[avertissement] Ecriture JSON impossible : {exc}", file=sys.stderr)

    return int(result.exit_code(strict=args.strict))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
