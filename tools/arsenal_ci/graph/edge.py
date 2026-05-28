"""Graph edge primitives.

An Edge is the atomic doctrinal unit of the validator. Its `kind`
(composes | reads) is the foundation of R-CI-1 and is derived
*exclusively* from the host HA key of the source, never from the
Jinja content itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EdgeKind(str, Enum):
    """Type of a typed edge.

    COMPOSES: the target reference *constitutes* the source entity's state.
              (host key: state / value_template / state_template)
    READS:    the target reference is merely *observed* / exposed and does
              not constitute the state. (host key: attributes / availability /
              icon / name / any cosmetic key)
    """

    COMPOSES = "composes"
    READS = "reads"


@dataclass(frozen=True)
class Position:
    """Positional context of a reference, for reporting."""

    file: str
    host_key: str  # the HA key under which the reference appeared


@dataclass(frozen=True)
class Edge:
    """A typed, immutable edge: (source) --kind--> (target).

    source: entity identity of the declaring entity (slug/unique_id).
    target: referenced entity_id (e.g. 'input_boolean.standby_force').
    kind:   EdgeKind, derived from host_key only.
    """

    source: str
    target: str
    kind: EdgeKind
    position: Position

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return (
            f"Edge({self.source} -{self.kind.value}-> {self.target} "
            f"@ {self.position.host_key})"
        )
