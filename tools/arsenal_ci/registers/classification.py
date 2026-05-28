"""Classification primitives.

The taxonomy is CLOSED and lives in code (doctrinal, not business data).
Adding a layer requires modifying this enum -> doctrinal review -> explicit PR.
The YAML may only *choose* among these layers; it cannot declare new ones.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Layer(str, Enum):
    """The eight sovereign functional layers. CLOSED set."""

    SECURITE = "securite"
    STABILISATION = "stabilisation"
    OVERRIDE = "override"
    AUTORISATION = "autorisation"
    PERCEPTION = "perception"
    DIAGNOSTIC = "diagnostic"
    APPLICATION = "application"
    EXTERNE = "externe"


# 'calibration' is a SPECIAL layer carried as an attribute, not an exclusive
# membership: a calibration entity still belongs to its functional layer.
CALIBRATION_KEY = "calibration"


@dataclass(frozen=True)
class EntityClass:
    """Classification of a single entity.

    layer:        functional layer (mandatory, from the closed taxonomy).
    calibration:  special attribute, orthogonal to layer.
    """

    entity_id: str
    layer: Layer
    calibration: bool = False

    @property
    def is_external(self) -> bool:
        return self.layer is Layer.EXTERNE


@dataclass(frozen=True)
class RegistryMeta:
    """Registry-level metadata, from the `parametres` section.

    exclus_invariants_registre: when True, the `parametres` section's own
        entries are excluded from registry invariants (they are not classable
        entities).
    """

    exclus_invariants_registre: bool
