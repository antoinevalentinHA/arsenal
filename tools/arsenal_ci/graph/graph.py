"""Immutable abstract graph.

The Graph carries *only* topology: typed nodes and edges. It knows
nothing of the classification (registers) nor of the rules. It is
built in a single pass by GraphBuilder and is read-only thereafter.
"""
from __future__ import annotations

from typing import Iterable, Iterator, Tuple

from .edge import Edge, EdgeKind
from .node import Node


class Graph:
    """Read-only graph. No mutation method is exposed after construction."""

    def __init__(self, nodes: Iterable[Node], edges: Iterable[Edge]) -> None:
        self._nodes: Tuple[Node, ...] = tuple(nodes)
        self._edges: Tuple[Edge, ...] = tuple(edges)

    @property
    def nodes(self) -> Tuple[Node, ...]:
        return self._nodes

    @property
    def edges(self) -> Tuple[Edge, ...]:
        return self._edges

    def edges_of_kind(self, kind: EdgeKind) -> Tuple[Edge, ...]:
        return tuple(e for e in self._edges if e.kind is kind)

    def edges_from(self, source: str) -> Tuple[Edge, ...]:
        return tuple(e for e in self._edges if e.source == source)

    def has_edge(self, source: str, target: str, kind: EdgeKind) -> bool:
        return any(
            e.source == source and e.target == target and e.kind is kind
            for e in self._edges
        )

    def __iter__(self) -> Iterator[Edge]:
        return iter(self._edges)

    def __len__(self) -> int:
        return len(self._edges)
