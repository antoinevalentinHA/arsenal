"""Report primitives."""
from __future__ import annotations

from dataclasses import dataclass

from ..rules.policy import Severity


@dataclass(frozen=True)
class Violation:
    rule: str
    message: str
    source: str
    target: str
    file: str
    host_key: str
    severity: Severity = Severity.BLOCKING
