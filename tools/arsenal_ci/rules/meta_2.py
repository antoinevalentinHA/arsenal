"""META-2 (perimetre_statut: complet).

Doctrinal discipline: every decisional entity entering the graph must be
classified before being accepted. An entity *declared* in the graph (a node
= a governed Arsenal entity) that is absent from the registry is a BLOCKING
violation when META-2 is active.

Scope choice (lot 1.2): META-2 applies to graph NODES (entities Arsenal
declares and governs), not to every external target referenced. Targets are
handled by the configurable unknown-entity policy of individual rules.
"""
from __future__ import annotations

from typing import List

from ..graph.graph import Graph
from ..registers.registry import Registry
from ..report.violation import Violation
from .policy import Policy, Severity

RULE_ID = "META-2"


def check(graph: Graph, registry: Registry, policy: Policy) -> List[Violation]:
    if not policy.meta2_active:
        return []
    violations: List[Violation] = []
    for node in graph.nodes:
        if not registry.is_known(node.entity_id):
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"Entite '{node.entity_id}' presente dans le graphe "
                        f"mais absente du registre (perimetre incomplet)."
                    ),
                    source=node.entity_id,
                    target="",
                    file=node.source_file,
                    host_key="",
                    severity=Severity.BLOCKING,
                )
            )
    return violations
