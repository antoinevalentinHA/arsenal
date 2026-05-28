"""Host-key -> EdgeKind typing.

This is the doctrinal core of R-CI-1. Typing is *structural*: it depends
ONLY on the HA key under which a reference appears, never on what the
reference is or what the Jinja expression computes.

  state / value_template / state_template  -> COMPOSES
  everything else (attributes, availability,
  icon, name, picture, ...)                -> READS

A reference appearing in `state:` constitutes the entity's state.
The same reference in `attributes:` is merely observed.
"""
from __future__ import annotations

from ..graph.edge import EdgeKind

# Keys whose content *constitutes* the entity state.
_COMPOSING_KEYS = frozenset(
    {
        "state",
        "value_template",
        "state_template",
    }
)


def kind_for_host_key(host_key: str) -> EdgeKind:
    """Return the EdgeKind for a reference found under `host_key`.

    The host_key is the *top-level* HA template key (already normalised by
    the loader, e.g. nested attribute names collapse to 'attributes').
    """
    if host_key in _COMPOSING_KEYS:
        return EdgeKind.COMPOSES
    return EdgeKind.READS
