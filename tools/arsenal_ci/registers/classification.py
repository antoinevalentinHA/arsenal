"""Classification primitives.

Three CLOSED taxonomies live in code (doctrinal, not business data):
  - Registre : the functional register an entity belongs to.
  - Couche   : the architectural layer of the entity.
  - Statut   : the lifecycle status of the entity.

registre and couche are DISTINCT taxonomies, validated separately. The
historical bug came from conflating section / registre / couche; this
module makes the three explicit and independent.

Adding a value to any taxonomy requires modifying the enum here ->
doctrinal review -> explicit PR. The YAML may only *choose* among them.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


from enum import Enum


class Registre(str, Enum):
    """Closed taxonomy of functional registers."""

    SECURITE = "securite"
    STABILISATION = "stabilisation"
    OVERRIDE = "override"
    AUTORISATION = "autorisation"
    PERCEPTION = "perception"
    DIAGNOSTIC = "diagnostic"
    APPLICATION = "application"
    EXTERNE = "externe"


class Couche(str, Enum):
    """Closed taxonomy of architectural layers.

    Distinct from Registre even where names overlap: an entity's register
    (functional grouping) and its layer (architectural role) are separate
    doctrinal facts and are validated independently.
    """

    SECURITE = "securite"
    STABILISATION = "stabilisation"
    OVERRIDE = "override"
    AUTORISATION = "autorisation"
    PERCEPTION = "perception"
    DIAGNOSTIC = "diagnostic"
    APPLICATION = "application"
    CALIBRATION = "calibration"
    EXTERNE = "externe"
    DECISION = "decision"
    NA = "n/a"


class Statut(str, Enum):
    """Closed taxonomy of lifecycle statuses. Always explicit (no default)."""

    ACTIF = "actif"
    DEPRECIE = "deprecie"
    EXPERIMENTAL = "experimental"
    EXTERNE = "externe"


# Sections that group by register (top-level key must equal entry.registre).
# 'deprecie' is special: it groups by STATUT, not by register.
SECTION_DEPRECIE = "deprecie"

# Special sections (not entity-bearing registers).
CALIBRATION_KEY = "calibration"
PARAMETRES_KEY = "parametres"
COUVERTURE_KEY = "couverture"

# Documentary metadata keys, ignored as classification but not as entities.
METADATA_KEYS = frozenset(
    {"version", "date", "perimetre_statut", "meta2_mode"}
)


@dataclass(frozen=True)
class EntityClass:
    """Rich classification of a single entity, read from a full entry."""

    entity_id: str
    registre: Registre
    couche: Couche
    statut: Statut
    niveau: Optional[str] = None
    calibration: bool = False
    contrat: Optional[str] = None
    note: Optional[str] = None

    @property
    def is_external(self) -> bool:
        return self.registre is Registre.EXTERNE or self.couche is Couche.EXTERNE

    @property
    def is_deprecie(self) -> bool:
        return self.statut is Statut.DEPRECIE


@dataclass(frozen=True)
class RegistryMeta:
    """Registry-level metadata.

    exclus_invariants_registre: from `parametres`; when True the parametres
        entries are excluded from registry invariants.
    couverture: declarative completeness/tracking metadata, kept here to allow
        later coherence checks against the real register (not a layer).
    """

    exclus_invariants_registre: bool
    couverture: tuple = ()
