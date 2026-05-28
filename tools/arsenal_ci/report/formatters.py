"""Formatters: human (stdout) and JSON (file)."""
from __future__ import annotations

import json
from typing import List

from ..rules.policy import Severity
from .result import Result
from .violation import Violation

_SEV_LABEL = {
    Severity.BLOCKING: "BLOQUANT",
    Severity.ERROR: "ERREUR",
    Severity.WARNING: "WARNING",
}
_SEV_ORDER = [Severity.BLOCKING, Severity.ERROR, Severity.WARNING]


def format_human(result: Result, strict: bool = False) -> str:
    lines: List[str] = []

    if result.execution_error is not None:
        lines.append("ERREUR D'EXECUTION DU VALIDATEUR")
        lines.append(f"  {result.execution_error}")
        lines.append("")
        lines.append("Aucun verdict doctrinal : l'analyse n'a pas abouti.")
        return "\n".join(lines)

    verdict = "ECHEC" if result.status == "fail" else "CONFORME"
    lines.append(f"Validateur CI Arsenal — Chauffage : {verdict}")
    lines.append("")

    if not result.violations:
        lines.append("Aucune violation.")
    else:
        for sev in _SEV_ORDER:
            group = [v for v in result.violations if v.severity is sev]
            if not group:
                continue
            lines.append(f"[{_SEV_LABEL[sev]}] ({len(group)})")
            for v in group:
                loc = v.file + (f" :: {v.host_key}" if v.host_key else "")
                tgt = f" -> {v.target}" if v.target else ""
                lines.append(f"  {v.rule}  {v.source}{tgt}")
                lines.append(f"      {v.message}")
                lines.append(f"      ({loc})")
            lines.append("")

    s = result.summary
    lines.append(
        f"Resume : {s.blocking} bloquant(s), {s.error} erreur(s), "
        f"{s.warning} warning(s)."
    )
    if strict and s.warning and not s.has_blocking_or_error:
        lines.append("Mode --strict : les warnings provoquent un echec.")
    return "\n".join(lines)


def format_json(result: Result, strict: bool = False) -> str:
    payload = {
        "status": result.status,
        "exit_code": int(result.exit_code(strict=strict)),
        "execution_error": result.execution_error,
        "summary": {
            "blocking": result.summary.blocking,
            "error": result.summary.error,
            "warning": result.summary.warning,
        },
        "violations": [_violation_dict(v) for v in result.violations],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _violation_dict(v: Violation) -> dict:
    return {
        "rule": v.rule,
        "severity": v.severity.value,
        "source": v.source,
        "target": v.target,
        "file": v.file,
        "host_key": v.host_key,
        "message": v.message,
    }
