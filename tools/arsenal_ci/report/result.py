"""Orchestrator result primitives.

Three planes are kept strictly separate:
  - execution error : the validator could not analyse (exit 2)
  - doctrinal violation : analysed code breaks doctrine (exit 1)
  - analysis warning : non-blocking observation (exit 0, or 1 under --strict)

An execution error is NOT a violation: it short-circuits before any verdict.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Optional

from ..rules.policy import Severity
from .violation import Violation


class ExitCode(IntEnum):
    PASS = 0
    VIOLATION = 1
    EXECUTION_ERROR = 2


class ExecutionError(Exception):
    """The validator could not perform its analysis (registry/IO/parse)."""


@dataclass(frozen=True)
class Summary:
    blocking: int = 0
    error: int = 0
    warning: int = 0

    @property
    def has_blocking_or_error(self) -> bool:
        return self.blocking > 0 or self.error > 0

    @property
    def has_warning(self) -> bool:
        return self.warning > 0


@dataclass(frozen=True)
class Result:
    """Terminal outcome of an analysis run."""

    violations: List[Violation] = field(default_factory=list)
    execution_error: Optional[str] = None
    summary: Summary = field(default_factory=Summary)

    @property
    def status(self) -> str:
        if self.execution_error is not None:
            return "error"
        return "fail" if self.summary.has_blocking_or_error else "pass"

    def exit_code(self, strict: bool = False) -> ExitCode:
        if self.execution_error is not None:
            return ExitCode.EXECUTION_ERROR
        if self.summary.has_blocking_or_error:
            return ExitCode.VIOLATION
        if strict and self.summary.has_warning:
            return ExitCode.VIOLATION
        return ExitCode.PASS


def summarise(violations: List[Violation]) -> Summary:
    b = sum(1 for v in violations if v.severity is Severity.BLOCKING)
    e = sum(1 for v in violations if v.severity is Severity.ERROR)
    w = sum(1 for v in violations if v.severity is Severity.WARNING)
    return Summary(blocking=b, error=e, warning=w)
