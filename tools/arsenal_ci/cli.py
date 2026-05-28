"""CLI entrypoint for the Arsenal Chauffage CI validator.

Usage:
    python -m arsenal_ci.cli --registry REG.yaml --config FILE.yaml [FILE...]
                             [--json OUT.json] [--strict]

Exit codes:
    0  pass        (no blocking/error; warnings allowed unless --strict)
    1  violation   (at least one blocking/error; or warning under --strict)
    2  exec error  (validator could not analyse: registry/IO/parse)

Loading happens inside the execution-error boundary: a failure to load the
registry or a config file is an execution error (exit 2), never a violation.
"""
from __future__ import annotations

import argparse
import sys
from typing import List

from .parsing.builder import GraphBuilder
from .registers.loader import RegistryError, RegistryLoader
from .report import formatters, orchestrator
from .report.result import ExecutionError, Result
from .rules.policy import CHAUFFAGE_POLICY


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise ExecutionError(f"Lecture impossible '{path}' : {exc}") from exc


def _build_result(registry_path: str, config_paths: List[str]) -> Result:
    # Execution-error boundary: any load/parse failure -> Result(error).
    try:
        registry = RegistryLoader().load_from_yaml(_read(registry_path))
        builder = GraphBuilder()
        # lot 1.3: single config file supported per the template: debt;
        # multi-file aggregation is a known later lot, but we accept a list.
        if not config_paths:
            raise ExecutionError("Aucun fichier de configuration fourni.")
        raw = _read(config_paths[0])
        graph = builder.build_from_yaml(raw, file=config_paths[0])
    except (RegistryError, ExecutionError) as exc:
        return Result(execution_error=str(exc))
    except Exception as exc:  # defensive
        return Result(execution_error=f"Echec de chargement : {exc}")

    return orchestrator.run(graph, registry, CHAUFFAGE_POLICY)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="arsenal-ci-chauffage")
    parser.add_argument("--registry", required=True)
    parser.add_argument("--config", required=True, nargs="+")
    parser.add_argument("--json", dest="json_out", default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    result = _build_result(args.registry, args.config)

    # Human format always to stdout.
    print(formatters.format_human(result, strict=args.strict))

    # JSON to file only.
    if args.json_out is not None:
        try:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                fh.write(formatters.format_json(result, strict=args.strict))
        except OSError as exc:
            print(f"\n[avertissement] Ecriture JSON impossible : {exc}", file=sys.stderr)

    return int(result.exit_code(strict=args.strict))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
