"""Orchestrator.

Runs the rule set against a graph + registry under a policy, aggregates
violations into a deterministically ordered Result. Execution errors are
caught and surfaced as ExecutionError -> they never become violations.

The orchestrator is the authority over what severity *produces* (exit code);
the policy/rules remain the authority over what severity is *attributed*.
"""
from __future__ import annotations

from typing import Callable, List

from ..graph.graph import Graph
from ..registers.registry import Registry
from ..rules import meta_2, r_ci_1
from ..rules.policy import Policy, Severity
from .result import ExecutionError, Result, summarise
from .violation import Violation

# Rule signature: (graph, registry, policy) -> list[Violation]
Rule = Callable[[Graph, Registry, Policy], List[Violation]]

# Registered rule set (order here is irrelevant; output is sorted).
RULES: List[Rule] = [meta_2.check, r_ci_1.check]

# Deterministic severity ordering: blocking first.
_SEVERITY_RANK = {
    Severity.BLOCKING: 0,
    Severity.ERROR: 1,
    Severity.WARNING: 2,
    Severity.IGNORE: 3,
}


def _sort_key(v: Violation):
    return (
        _SEVERITY_RANK.get(v.severity, 99),
        v.rule,
        v.file,
        v.source,
        v.target,
    )


def run(graph: Graph, registry: Registry, policy: Policy) -> Result:
    """Execute all rules and aggregate. Catches execution errors."""
    try:
        collected: List[Violation] = []
        for rule in RULES:
            collected.extend(rule(graph, registry, policy))
    except ExecutionError as exc:
        return Result(execution_error=str(exc))
    except Exception as exc:  # defensive: any unexpected failure is exec error
        return Result(execution_error=f"Echec interne du validateur : {exc}")

    ordered = sorted(collected, key=_sort_key)
    return Result(violations=ordered, summary=summarise(ordered))
