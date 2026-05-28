"""Graph node primitive."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    """A declared entity in the abstract graph.

    entity_id: canonical identity, e.g. 'binary_sensor.chauffage_autorisation_etage_1'.
    domain:    HA domain, e.g. 'binary_sensor'.
    source_file: file where the entity was declared.
    """

    entity_id: str
    domain: str
    source_file: str
