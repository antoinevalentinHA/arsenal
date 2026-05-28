"""Registry loader.

Transforms registres_entites.yaml into a validated, frozen Registry.
Internal validation (document coherence) is BLOCKING: a sovereign registry
must never yield a half-working validator. Inter-artifact validation
(graph vs registry, e.g. META-2) belongs to the rules, not here.

Expected YAML shape (per stabilised contract):

    securite:
      - binary_sensor.x
      - sensor.y
    perception:
      - sensor.z
    externe:
      - sensor.tier_cloud
    calibration:                # SPECIAL layer: attribute overlay
      - sensor.z                # marks z as calibration, keeps its layer
    parametres:
      exclus_invariants_registre: true

Entities may appear as bare strings or as mappings carrying flags.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

import yaml

from .classification import (
    CALIBRATION_KEY,
    EntityClass,
    Layer,
    RegistryMeta,
)
from .registry import Registry

_PARAMETRES_KEY = "parametres"
_VALID_LAYER_VALUES = frozenset(layer.value for layer in Layer)
_ENTITY_ID_RE = re.compile(r"^[a-z_]+\.[a-z0-9_]+$")


class RegistryError(Exception):
    """Blocking registry-internal error."""


def _entity_id_from(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict) and "entity_id" in item:
        return str(item["entity_id"])
    raise RegistryError(f"Entree d'entite invalide : {item!r}")


class RegistryLoader:
    def load_from_yaml(self, raw: str) -> Registry:
        doc = yaml.safe_load(raw) or {}
        if not isinstance(doc, dict):
            raise RegistryError("Le registre doit etre un mapping au niveau racine.")

        meta = self._extract_meta(doc)
        calibration_set = self._extract_calibration(doc)
        entries = self._extract_entities(doc, calibration_set)

        return Registry(entries=tuple(entries), meta=meta)

    # ------------------------------------------------------------------ meta

    def _extract_meta(self, doc: Dict[str, Any]) -> RegistryMeta:
        # META-2: parametres section must be present and well-typed (blocking).
        if _PARAMETRES_KEY not in doc:
            raise RegistryError(
                "Section 'parametres' absente (META-2 : requise)."
            )
        params = doc[_PARAMETRES_KEY]
        if not isinstance(params, dict):
            raise RegistryError("Section 'parametres' doit etre un mapping.")
        flag = params.get("exclus_invariants_registre")
        if not isinstance(flag, bool):
            raise RegistryError(
                "'exclus_invariants_registre' doit etre un booleen (META-2)."
            )
        return RegistryMeta(exclus_invariants_registre=flag)

    # ----------------------------------------------------------- calibration

    def _extract_calibration(self, doc: Dict[str, Any]) -> set:
        """calibration is an attribute overlay, not an exclusive layer."""
        raw = doc.get(CALIBRATION_KEY, []) or []
        if not isinstance(raw, list):
            raise RegistryError("La couche 'calibration' doit etre une liste.")
        return {_entity_id_from(i) for i in raw}

    # -------------------------------------------------------------- entities

    def _extract_entities(
        self, doc: Dict[str, Any], calibration_set: set
    ) -> List[EntityClass]:
        entries: List[EntityClass] = []
        seen: Dict[str, str] = {}  # entity_id -> layer (duplicate detection)

        for key, value in doc.items():
            if key in (_PARAMETRES_KEY, CALIBRATION_KEY):
                continue
            if key not in _VALID_LAYER_VALUES:
                raise RegistryError(
                    f"Couche inconnue '{key}' (taxonomie fermee)."
                )
            layer = Layer(key)
            if value is None:
                # declared but empty -> warning-level; we keep it non-fatal.
                continue
            if not isinstance(value, list):
                raise RegistryError(f"La couche '{key}' doit etre une liste.")
            for item in value:
                eid = _entity_id_from(item)
                if not _ENTITY_ID_RE.match(eid):
                    raise RegistryError(f"entity_id invalide : '{eid}'.")
                if eid in seen:
                    raise RegistryError(
                        f"Classification ambigue : '{eid}' present dans "
                        f"'{seen[eid]}' et '{key}'."
                    )
                seen[eid] = key
                entries.append(
                    EntityClass(
                        entity_id=eid,
                        layer=layer,
                        calibration=eid in calibration_set,
                    )
                )

        # calibration entities must exist in a functional layer
        orphan_calib = calibration_set - set(seen)
        if orphan_calib:
            raise RegistryError(
                "Entites 'calibration' sans couche fonctionnelle : "
                f"{sorted(orphan_calib)}."
            )
        return entries
