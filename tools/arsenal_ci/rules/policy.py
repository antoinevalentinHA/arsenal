"""Severity policy.

Generic engine mechanism, decoupled from domain policy. The engine permits
four levels; the Chauffage domain (with META-2 active) sets its own policy.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    IGNORE = "ignore"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


@dataclass(frozen=True)
class Policy:
    """Domain severity policy.

    meta2_active: when True, an entity referenced by the graph but absent
        from the registry is a BLOCKING violation (perimetre_statut: complet).
    unknown_entity_severity: severity for a graph entity absent from the
        registry when META-2 is NOT active (configurable per rule/domain).
    """

    meta2_active: bool
    unknown_entity_severity: Severity = Severity.WARNING


# Chauffage policy: META-2 active -> unknown == blocking.
CHAUFFAGE_POLICY = Policy(meta2_active=True, unknown_entity_severity=Severity.WARNING)
