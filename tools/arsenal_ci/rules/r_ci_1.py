"""R-CI-1 (taxonomy-driven, lot 1.2).

Doctrinal statement, generalised from the historical standby_force case:
an AUTORISATION entity must NOT *compose* its state from a control belonging
to a guarding layer (securite / override / stabilisation). Such controls may
only be *read* (exposed in attributes), never constitute the authorisation
state. Structurally: no COMPOSES edge may go from an AUTORISATION source to a
guarding-layer target.

The hardcoded target set of lot 1.1 is removed. Classification now comes from
the Registry (taxonomy). Targets unknown to the registry are handled by the
configurable per-rule policy (warning by default; blocking under META-2 via
the dedicated META-2 rule, not here).
"""
from __future__ import annotations

from typing import List

from ..graph.edge import EdgeKind
from ..graph.graph import Graph
from ..registers.classification import Couche, Registre
from ..registers.registry import Registry
from ..report.violation import Violation
from .policy import Policy, Severity

RULE_ID = "R-CI-1"

# Couches whose controls must never compose an authorisation state.
_GUARDING_REGISTRES = frozenset(
    {Registre.SECURITE, Registre.OVERRIDE, Registre.STABILISATION}
)


def check(graph: Graph, registry: Registry, policy: Policy) -> List[Violation]:
    violations: List[Violation] = []
    for edge in graph.edges_of_kind(EdgeKind.COMPOSES):
        # Source must be an authorisation entity for R-CI-1 to apply.
        if registry.couche_of(edge.source) is not Couche.AUTORISATION:
            continue

        target_registre = registry.registre_of(edge.target)

        if target_registre in _GUARDING_REGISTRES:
            violations.append(
                Violation(
                    rule=RULE_ID,
                    message=(
                        f"'{edge.target}' ({target_registre.value}) compose l'etat "
                        f"de l'autorisation '{edge.source}' (interdit : doit etre "
                        f"uniquement observe)."
                    ),
                    source=edge.source,
                    target=edge.target,
                    file=edge.position.file,
                    host_key=edge.position.host_key,
                    severity=Severity.BLOCKING,
                )
            )
        elif target_registre is None and not registry.is_known(edge.target):
            # Target unknown to registry: configurable severity (not META-2).
            sev = policy.unknown_entity_severity
            if sev is not Severity.IGNORE:
                violations.append(
                    Violation(
                        rule=RULE_ID,
                        message=(
                            f"Cible '{edge.target}' composant l'autorisation "
                            f"'{edge.source}' est inconnue du registre."
                        ),
                        source=edge.source,
                        target=edge.target,
                        file=edge.position.file,
                        host_key=edge.position.host_key,
                        severity=sev,
                    )
                )
    return violations
