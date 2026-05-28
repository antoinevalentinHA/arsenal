"""Immutable classification registry.

Symmetric to Graph: built once, frozen, read-only. Rules query doctrinal
questions only. The new explicit API distinguishes registre / couche /
statut. `layer_of` is kept as a thin deprecated alias of `couche_of` for
R-CI-1 compatibility.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from .classification import (
    Couche,
    EntityClass,
    Registre,
    RegistryMeta,
    Statut,
)


class Registry:
    def __init__(self, entries: Tuple[EntityClass, ...], meta: RegistryMeta) -> None:
        self._by_id: Dict[str, EntityClass] = {e.entity_id: e for e in entries}
        self._meta = meta
        by_couche: Dict[Couche, list] = {c: [] for c in Couche}
        for e in entries:
            by_couche[e.couche].append(e.entity_id)
        self._by_couche: Dict[Couche, Tuple[str, ...]] = {
            k: tuple(v) for k, v in by_couche.items()
        }

    # ---- doctrinal query surface (read-only) -------------------------------

    def is_known(self, entity_id: str) -> bool:
        return entity_id in self._by_id

    def registre_of(self, entity_id: str) -> Optional[Registre]:
        cls = self._by_id.get(entity_id)
        return cls.registre if cls else None

    def couche_of(self, entity_id: str) -> Optional[Couche]:
        """None == not classified (distinct from explicitly EXTERNE)."""
        cls = self._by_id.get(entity_id)
        return cls.couche if cls else None

    def statut_of(self, entity_id: str) -> Optional[Statut]:
        cls = self._by_id.get(entity_id)
        return cls.statut if cls else None

    def niveau_of(self, entity_id: str) -> Optional[str]:
        cls = self._by_id.get(entity_id)
        return cls.niveau if cls else None

    def contrat_of(self, entity_id: str) -> Optional[str]:
        cls = self._by_id.get(entity_id)
        return cls.contrat if cls else None

    def is_external(self, entity_id: str) -> bool:
        cls = self._by_id.get(entity_id)
        return bool(cls and cls.is_external)

    def is_deprecie(self, entity_id: str) -> bool:
        cls = self._by_id.get(entity_id)
        return bool(cls and cls.is_deprecie)

    def is_calibration(self, entity_id: str) -> bool:
        cls = self._by_id.get(entity_id)
        return bool(cls and cls.calibration)

    def in_couche(self, entity_id: str, couche: Couche) -> bool:
        return self.couche_of(entity_id) is couche

    def entities_in(self, couche: Couche) -> Tuple[str, ...]:
        return self._by_couche.get(couche, ())

    # ---- deprecated alias for R-CI-1 ---------------------------------------

    def layer_of(self, entity_id: str) -> Optional[Couche]:
        """Deprecated alias of couche_of (kept for rule compatibility)."""
        return self.couche_of(entity_id)

    @property
    def meta(self) -> RegistryMeta:
        return self._meta

    def __len__(self) -> int:
        return len(self._by_id)
