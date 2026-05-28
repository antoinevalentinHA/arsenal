"""Registry loader (rich, sovereign format).

Transforms the real sovereign registres_entites.yaml into a validated,
frozen Registry. The naive `top-level key == couche` model is GONE.

Model:
  - Documentary metadata keys (version, date, perimetre_statut, meta2_mode)
    are ignored as classification.
  - Special sections: parametres (META-2 flag), couverture (kept in meta),
    calibration (attribute overlay).
  - Entity-bearing sections group by REGISTER (top-level key == entry.registre),
    EXCEPT `deprecie` which groups by STATUT (entry keeps its real registre/
    couche, statut == deprecie).
  - Each entry is a full object: entity_id, registre, couche, niveau, statut,
    contrat, note. The couche is READ, never deduced from the section.

Validation (all blocking; the registry is sovereign):
  - entity_id syntactically valid
  - registre in closed taxonomy
  - couche in closed taxonomy
  - statut in closed taxonomy and ALWAYS explicit (no implicit default)
  - section/field coherence (section==registre, or section==statut for deprecie)
  - contrat present for governed entities (all except externe)
  - no duplicate entity_id
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

import yaml

from .classification import (
    CALIBRATION_KEY,
    COUVERTURE_KEY,
    METADATA_KEYS,
    PARAMETRES_KEY,
    SECTION_DEPRECIE,
    Couche,
    EntityClass,
    Registre,
    RegistryMeta,
    Statut,
)
from .registry import Registry

_ENTITY_ID_RE = re.compile(r"^[a-z_]+\.[a-z0-9_]+$")
_REGISTRE_VALUES = frozenset(r.value for r in Registre)
_COUCHE_VALUES = frozenset(c.value for c in Couche)
_STATUT_VALUES = frozenset(s.value for s in Statut)
# Sections that carry entities (group by register) + the special deprecie.
_ENTITY_SECTIONS = _REGISTRE_VALUES | {SECTION_DEPRECIE}


class RegistryError(Exception):
    """Blocking registry-internal error."""


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
        if PARAMETRES_KEY not in doc:
            raise RegistryError("Section 'parametres' absente (META-2 : requise).")
        params = doc[PARAMETRES_KEY]
        if not isinstance(params, dict):
            raise RegistryError("Section 'parametres' doit etre un mapping.")
        flag = params.get("exclus_invariants_registre")
        if not isinstance(flag, bool):
            raise RegistryError(
                "'exclus_invariants_registre' doit etre un booleen (META-2)."
            )

        couverture = self._extract_couverture(doc)
        return RegistryMeta(
            exclus_invariants_registre=flag,
            couverture=couverture,
        )

    def _extract_couverture(self, doc: Dict[str, Any]) -> Tuple:
        """couverture: declarative tracking metadata, kept for later coherence
        checks against the real register. NOT a layer, NOT entity-bearing."""
        raw = doc.get(COUVERTURE_KEY)
        if raw is None:
            return ()
        # Keep it opaque-but-structured: a tuple of (key, value) if mapping,
        # or a tuple of items if list.
        if isinstance(raw, dict):
            return tuple(sorted(raw.items()))
        if isinstance(raw, list):
            return tuple(raw)
        raise RegistryError("Section 'couverture' doit etre un mapping ou une liste.")

    # ----------------------------------------------------------- calibration

    def _extract_calibration(self, doc: Dict[str, Any]) -> set:
        raw = doc.get(CALIBRATION_KEY, []) or []
        if isinstance(raw, dict):
            # allow {entity_id: ...} mapping form
            return set(raw.keys())
        if isinstance(raw, list):
            out = set()
            for i in raw:
                out.add(self._entity_id_of(i))
            return out
        raise RegistryError("La couche 'calibration' doit etre une liste ou un mapping.")

    # -------------------------------------------------------------- entities

    def _extract_entities(
        self, doc: Dict[str, Any], calibration_set: set
    ) -> List[EntityClass]:
        entries: List[EntityClass] = []
        seen: Dict[str, str] = {}

        for key, value in doc.items():
            if key in METADATA_KEYS:
                continue
            if key in (PARAMETRES_KEY, COUVERTURE_KEY, CALIBRATION_KEY):
                continue
            if key not in _ENTITY_SECTIONS:
                raise RegistryError(
                    f"Section top-level inconnue '{key}' (taxonomie fermee)."
                )
            if value is None:
                continue  # declared empty section: warning-level, non-fatal
            if not isinstance(value, list):
                raise RegistryError(f"La section '{key}' doit etre une liste.")

            for item in value:
                ent = self._build_entity(item, section=key, calibration_set=calibration_set)
                if ent.entity_id in seen:
                    raise RegistryError(
                        f"Classification ambigue : '{ent.entity_id}' present dans "
                        f"'{seen[ent.entity_id]}' et '{key}'."
                    )
                seen[ent.entity_id] = key
                entries.append(ent)

        orphan = calibration_set - set(seen)
        if orphan:
            raise RegistryError(
                f"Entites 'calibration' sans entree fonctionnelle : {sorted(orphan)}."
            )
        return entries

    # ---------------------------------------------------------- entry parsing

    @staticmethod
    def _entity_id_of(item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict) and "entity_id" in item:
            return str(item["entity_id"])
        raise RegistryError(f"Entree d'entite invalide (entity_id absent) : {item!r}")

    def _build_entity(
        self, item: Any, section: str, calibration_set: set
    ) -> EntityClass:
        if not isinstance(item, dict):
            raise RegistryError(
                f"Entree d'entite doit etre un objet complet, recu : {item!r}"
            )

        eid = str(item.get("entity_id", "")).strip()
        if not _ENTITY_ID_RE.match(eid):
            raise RegistryError(f"entity_id invalide ou absent : '{eid}'.")

        # registre
        registre_raw = item.get("registre")
        if registre_raw not in _REGISTRE_VALUES:
            raise RegistryError(
                f"'{eid}' : registre '{registre_raw}' hors taxonomie fermee."
            )
        registre = Registre(registre_raw)

        # couche (READ, never deduced)
        couche_raw = item.get("couche")
        if couche_raw not in _COUCHE_VALUES:
            raise RegistryError(
                f"'{eid}' : couche '{couche_raw}' hors taxonomie fermee."
            )
        couche = Couche(couche_raw)

        # statut (always explicit)
        statut_raw = item.get("statut")
        if statut_raw is None:
            raise RegistryError(f"'{eid}' : 'statut' absent (toujours explicite requis).")
        if statut_raw not in _STATUT_VALUES:
            raise RegistryError(
                f"'{eid}' : statut '{statut_raw}' hors taxonomie fermee."
            )
        statut = Statut(statut_raw)

        # section/field coherence
        self._check_section_coherence(eid, section, registre, statut)

        # contrat: required for governed entities (all except externe)
        contrat = item.get("contrat")
        if registre is not Registre.EXTERNE and not contrat:
            raise RegistryError(
                f"'{eid}' : 'contrat' obligatoire (entite gouvernee, registre={registre.value})."
            )

        return EntityClass(
            entity_id=eid,
            registre=registre,
            couche=couche,
            statut=statut,
            niveau=(str(item["niveau"]) if item.get("niveau") is not None else None),
            calibration=eid in calibration_set,
            contrat=(str(contrat) if contrat else None),
            note=(str(item["note"]) if item.get("note") is not None else None),
        )

    @staticmethod
    def _check_section_coherence(
        eid: str, section: str, registre: Registre, statut: Statut
    ) -> None:
        if section == SECTION_DEPRECIE:
            # deprecie groups by STATUT, not by register.
            if statut is not Statut.DEPRECIE:
                raise RegistryError(
                    f"'{eid}' sous section 'deprecie' mais statut='{statut.value}' "
                    f"(attendu 'deprecie')."
                )
            return
        # all other sections group by register.
        if section != registre.value:
            raise RegistryError(
                f"'{eid}' : incoherence section '{section}' / registre "
                f"'{registre.value}'."
            )
