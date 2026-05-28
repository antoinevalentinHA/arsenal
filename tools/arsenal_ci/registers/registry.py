"""Immutable classification registry.

Symmetric to Graph: built once, frozen, read-only. Rules query doctrinal
questions only; they never see the YAML nor the internal structure.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from .classification import EntityClass, Layer, RegistryMeta


class Registry:
    def __init__(self, entries: Tuple[EntityClass, ...], meta: RegistryMeta) -> None:
        self._by_id: Dict[str, EntityClass] = {e.entity_id: e for e in entries}
        self._meta = meta
        # by_layer index
        by_layer: Dict[Layer, list] = {layer: [] for layer in Layer}
        for e in entries:
            by_layer[e.layer].append(e.entity_id)
        self._by_layer: Dict[Layer, Tuple[str, ...]] = {
            k: tuple(v) for k, v in by_layer.items()
        }

    # ---- doctrinal query surface (read-only) -------------------------------

    def is_known(self, entity_id: str) -> bool:
        return entity_id in self._by_id

    def layer_of(self, entity_id: str) -> Optional[Layer]:
        """None == not classified (distinct from explicitly EXTERNE)."""
        cls = self._by_id.get(entity_id)
        return cls.layer if cls else None

    def is_external(self, entity_id: str) -> bool:
        cls = self._by_id.get(entity_id)
        return bool(cls and cls.is_external)

    def is_calibration(self, entity_id: str) -> bool:
        cls = self._by_id.get(entity_id)
        return bool(cls and cls.calibration)

    def in_layer(self, entity_id: str, layer: Layer) -> bool:
        return self.layer_of(entity_id) is layer

    def entities_in(self, layer: Layer) -> Tuple[str, ...]:
        return self._by_layer.get(layer, ())

    @property
    def meta(self) -> RegistryMeta:
        return self._meta

    def __len__(self) -> int:
        return len(self._by_id)
