"""YAML loader + graph builder for HA `template:` blocks.

Scope (lot 1.1): handle the `template:` platform with entity-type lists
(binary_sensor, sensor, ...). Each entity's keys are walked; for every
string value, the Jinja scanner extracts references, which are typed by
the host key and emitted as edges.

Entity identity resolution: unique_id -> slugified name (fallback).
The domain is the template entity type key (binary_sensor, sensor, ...).
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

import yaml

from ..graph.edge import Edge, EdgeKind, Position
from ..graph.graph import Graph
from ..graph.node import Node
from .edge_typer import kind_for_host_key
from .jinja_scanner import scan_references

# Template entity types we recognise as node-declaring keys.
_ENTITY_TYPES = frozenset(
    {"binary_sensor", "sensor", "switch", "number", "select", "button", "cover"}
)


def _slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def _resolve_identity(entity: Dict[str, Any], domain: str) -> str:
    """unique_id -> name(slug) fallback. Returns canonical 'domain.slug'."""
    uid = entity.get("unique_id")
    if uid:
        return f"{domain}.{uid}"
    name = entity.get("name")
    if name:
        return f"{domain}.{_slugify(str(name))}"
    return f"{domain}.<anonymous>"


def _normalise_host_key(top_key: str) -> str:
    """Collapse the entity key into a typing-relevant host key.

    Nested attribute keys are collapsed to 'attributes' by the walker,
    so here we mostly pass through; this hook keeps it explicit.
    """
    return top_key


def _walk_entity(
    entity: Dict[str, Any], source: str, file: str
) -> List[Edge]:
    edges: List[Edge] = []
    for top_key, value in entity.items():
        if top_key in ("unique_id", "name"):
            continue
        host_key = _normalise_host_key(top_key)
        # attributes is a dict of sub-keys: all collapse to host_key 'attributes'
        if host_key == "attributes" and isinstance(value, dict):
            kind = kind_for_host_key("attributes")
            for sub_val in value.values():
                _emit(edges, source, str(sub_val), kind, file, "attributes")
            continue
        kind = kind_for_host_key(host_key)
        if isinstance(value, str):
            _emit(edges, source, value, kind, file, host_key)
    return edges


def _emit(
    edges: List[Edge],
    source: str,
    text: str,
    kind: EdgeKind,
    file: str,
    host_key: str,
) -> None:
    pos = Position(file=file, host_key=host_key)
    for target in scan_references(text):
        edges.append(Edge(source=source, target=target, kind=kind, position=pos))


class GraphBuilder:
    """Single-pass builder. Produces an immutable Graph."""

    def build_from_yaml(self, raw: str, file: str = "<memory>") -> Graph:
        doc = yaml.safe_load(raw) or {}
        nodes: List[Node] = []
        edges: List[Edge] = []

        template_blocks = self._extract_template_blocks(doc)
        for block in template_blocks:
            for ent_type, entities in block.items():
                if ent_type not in _ENTITY_TYPES:
                    continue
                if not isinstance(entities, list):
                    continue
                for entity in entities:
                    if not isinstance(entity, dict):
                        continue
                    identity = _resolve_identity(entity, ent_type)
                    nodes.append(
                        Node(entity_id=identity, domain=ent_type, source_file=file)
                    )
                    edges.extend(_walk_entity(entity, identity, file))

        return Graph(nodes=nodes, edges=edges)

    @staticmethod
    def _extract_template_blocks(doc: Any) -> List[Dict[str, Any]]:
        """Return the list of template blocks regardless of top-level shape.

        Accepts:
          template: [ {binary_sensor: [...]}, ... ]
          template: {binary_sensor: [...]}
          {binary_sensor: [...]}   (bare, no template wrapper)
        """
        if isinstance(doc, dict) and "template" in doc:
            tpl = doc["template"]
            if isinstance(tpl, list):
                return [b for b in tpl if isinstance(b, dict)]
            if isinstance(tpl, dict):
                return [tpl]
        if isinstance(doc, dict):
            return [doc]
        return []
