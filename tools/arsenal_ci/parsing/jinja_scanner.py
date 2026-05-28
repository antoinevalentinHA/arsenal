"""Lexical Jinja reference scanner.

NO Jinja engine is executed. References are extracted purely by regex.
The scanner is deliberately neutral: it collects *potential* references.
Disambiguation composes/reads is NOT done here -- it is done by the
host key (see edge_typer). The scanner over-collects rather than
under-collects.

Supported patterns (lot 1.1, "+ dotted access"):
  - states('domain.object')
  - state_attr('domain.object', 'attr')
  - is_state('domain.object', ...)
  - is_state_attr('domain.object', 'attr', ...)
  - states.domain.object              (dotted access)
  - states.domain.object.state
  - states.domain.object.attributes.x
"""
from __future__ import annotations

import re
from typing import List

# Entity id inside quotes: domain.object_slug
_QUOTED_ENTITY = r"['\"](?P<eid>[a-z_]+\.[a-z0-9_]+)['\"]"

# Function-style: states(...), is_state(...), state_attr(...), is_state_attr(...)
_FUNC_REF = re.compile(
    r"\b(?:states|is_state|state_attr|is_state_attr)\s*\(\s*" + _QUOTED_ENTITY
)

# Dotted access: states.domain.object  (object slug, stop before .state/.attributes/etc.)
_DOTTED_REF = re.compile(
    r"\bstates\.(?P<domain>[a-z_]+)\.(?P<obj>[a-z0-9_]+)"
)


def scan_references(text: str) -> List[str]:
    """Return the list of entity_ids referenced in `text`.

    Order-preserving, duplicates kept (caller deduplicates per edge set).
    """
    refs: List[str] = []

    for m in _FUNC_REF.finditer(text):
        refs.append(m.group("eid"))

    for m in _DOTTED_REF.finditer(text):
        refs.append(f"{m.group('domain')}.{m.group('obj')}")

    return refs
