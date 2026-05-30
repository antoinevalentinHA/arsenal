"""Surface CI etage-2 — verdict decision sur la config vivante (plan 2).

Instance CH-1 du verdict etage-2 : applique au RUNTIME les regles de la region
decision, agrege en un report.result.Result, et renvoie un exit code 0/1/2
identique a la CLI etage-1.

  - R-COV-1 (couverture) : runtime decision_centrale.yaml:reason, SANS axiome
    (A=()) depuis CH-2 — couverture purement structurelle ;
  - R-MIRROR-1 (synchronie) : runtime cerveau <-> miroir ;
  - R-CAUSE-1 (non-remontee consequence->cause, CH-3) : aucune raison emise
    n'est une consequence (etat d'autorisation compose) ;
  - R-ISO-1 (iso-comportement, CH-3) : reason et desired_mode partagent le meme
    squelette de decision de tete.

Source unique de localisation cerveau/miroir : r_mirror_1 (CERVEAU_FICHIER,
CERVEAU_CLE, MIROIR_FICHIER, MIROIR_CLE). Aucun chemin runtime n'est code en
dur ici ; la fixture D2 (ancre self-test) n'apparait pas (entree = runtime).

Le gating warn-only -> bloquant (ARSENAL_CI_ENFORCE) est resolu au niveau du
workflow, PAS ici : cette surface renvoie le vrai code de sortie. Une erreur
d'analyse remonte en Result(execution_error) -> exit 2, jamais en violation.
"""
from __future__ import annotations

import argparse
import sys
from typing import List

from ..report import formatters
from ..report.result import ExecutionError, Result, summarise
from ..report.violation import Violation
from ..rules.policy import Severity
from . import r_cause_1, r_cov_1, r_iso_1, r_mirror_1
from .r_mirror_1 import CERVEAU_CLE, CERVEAU_FICHIER

# Ordre deterministe, aligne sur l'orchestrateur etage-1.
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
    """Applique les regles etage-2 au runtime. Peut lever ExecutionError."""
    violations: List[Violation] = list(
        r_cov_1.analyser_fichier(CERVEAU_FICHIER, CERVEAU_CLE, ())
    )
    violations += r_mirror_1.comparer_runtime()
    violations += r_cause_1.analyser_fichier(CERVEAU_FICHIER, CERVEAU_CLE)
    violations += r_iso_1.comparer_runtime()
    return violations


def executer_ch1() -> Result:
    """Verdict etage-2 sur le runtime reel. Frontiere d'erreur d'execution."""
    try:
        violations = _collecter()
    except ExecutionError as exc:
        return Result(execution_error=str(exc))
    except Exception as exc:  # defensif : tout echec inattendu = erreur d'execution
        return Result(execution_error=f"Echec interne du validateur etage-2 : {exc}")
    return agreger(violations)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="arsenal-ci-decision")
    parser.add_argument("--json", dest="json_out", default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    result = executer_ch1()

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