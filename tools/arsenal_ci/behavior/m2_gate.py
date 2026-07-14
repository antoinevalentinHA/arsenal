"""Oracle borné de la PORTE M2 du pipeline aération (preuve comportementale).

Statut épistémique : PREUVE CIBLÉE DE LA PORTE. Cet oracle lit le VRAI
`11_automations/aeration/blocage_chauffage/pipeline.yaml`, isole la branche
M2 (celle dont la `sequence` appelle `script.aeration_m2_fin_episode`), et
évalue son arbre `conditions` contre un état simulé `{states, trigger_id}`.

Ce qu'il PROUVE :
  - pour un couple (états, trigger) donné, la porte M2 réelle passe ou non ;
  - la branche qui passe est bien celle qui appelle M2.

Ce qu'il NE fait PAS (frontière assumée, jamais masquée) :
  - il ne simule AUCUN effet de M2 (P2 : blocage, timers, confirmee…) ;
  - il n'émule ni Jinja général, ni timers, ni ordonnancement HA.
  Les effets complets et leur ordre restent prouvés par
  `scripts/arsenal_contracts/check_aeration_m2_contracts.py` sur le vrai script.

Vocabulaire de conditions supporté (celui, et seulement celui, de la branche
M2) : `state`, `or`, `and`, et deux formes `template` :
  - `trigger.id == '<id>'`
  - `trigger.id in [ ... ]`
  - `states('input_datetime.aeration_debut') not in [ ... ]`
Toute forme inconnue lève `GateModelError` (jamais un « vrai » silencieux).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Tuple

import yaml

_ROOT = Path(__file__).resolve().parents[3]
PIPELINE_FILE = (
    _ROOT
    / "11_automations"
    / "aeration"
    / "blocage_chauffage"
    / "pipeline.yaml"
)
MASTER_ID = "10010000000023"
M2_SCRIPT_ENTITY = "script.aeration_m2_fin_episode"


class GateModelError(RuntimeError):
    """Structure ou vocabulaire de condition hors du périmètre modélisé."""


# ------------------------------------------------------------ loader tolérant

class _LoaderTolerant(yaml.SafeLoader):
    """SafeLoader tolérant aux tags HA inconnus (!input, !secret, …)."""


def _ignorer_tag_inconnu(loader, node):  # pragma: no cover - trivial
    return None


_LoaderTolerant.add_constructor(None, _ignorer_tag_inconnu)


# ------------------------------------------------------------ localisation M2

def _load_pipeline(path: Path = PIPELINE_FILE):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=_LoaderTolerant)


def _find_master(docs) -> dict:
    for item in docs or []:
        if isinstance(item, dict) and str(item.get("id")) == MASTER_ID:
            return item
    raise GateModelError(f"Automation maître {MASTER_ID} introuvable.")


def _choose_branches(master: dict) -> List[dict]:
    actions = master.get("action") or []
    for step in actions:
        if isinstance(step, dict) and "choose" in step:
            return step["choose"] or []
    raise GateModelError("Bloc `choose` introuvable dans l'action maître.")


def _sequence_calls_m2(branch: dict) -> bool:
    for step in branch.get("sequence") or []:
        if isinstance(step, dict) and (
            step.get("action") == M2_SCRIPT_ENTITY
            or step.get("service") == M2_SCRIPT_ENTITY
        ):
            return True
    return False


def find_m2_branch(path: Path = PIPELINE_FILE) -> dict:
    """Retourne la branche `choose` dont la séquence appelle M2 (ancre robuste)."""
    master = _find_master(_load_pipeline(path))
    m2 = [b for b in _choose_branches(master) if _sequence_calls_m2(b)]
    if len(m2) != 1:
        raise GateModelError(
            f"Attendu exactement 1 branche appelant M2, trouvé {len(m2)}."
        )
    return m2[0]


# ------------------------------------------------------- évaluateur de conditions

_TPL_EQ = re.compile(r"trigger\.id\s*==\s*['\"](?P<id>[^'\"]+)['\"]")
_TPL_IN = re.compile(r"trigger\.id\s+in\s*\[(?P<body>[^\]]*)\]", re.DOTALL)
_TPL_DEBUT = re.compile(
    r"states\(\s*['\"]input_datetime\.aeration_debut['\"]\s*\)\s+not\s+in\s*\[(?P<body>[^\]]*)\]",
    re.DOTALL,
)
_QUOTED = re.compile(r"['\"]([^'\"]+)['\"]")


def _eval_template(tpl: str, states: Mapping[str, str], trigger_id: str) -> bool:
    m = _TPL_EQ.search(tpl)
    if m:
        return trigger_id == m.group("id")

    m = _TPL_IN.search(tpl)
    if m:
        ids = _QUOTED.findall(m.group("body"))
        return trigger_id in ids

    m = _TPL_DEBUT.search(tpl)
    if m:
        forbidden = _QUOTED.findall(m.group("body"))
        return states.get("input_datetime.aeration_debut") not in forbidden

    raise GateModelError(f"Template hors périmètre modélisé : {tpl!r}")


def _eval_condition(cond, states: Mapping[str, str], trigger_id: str) -> bool:
    if not isinstance(cond, dict):
        raise GateModelError(f"Condition non-dict : {cond!r}")

    ctype = cond.get("condition")

    if ctype == "state":
        expected = cond.get("state")
        actual = states.get(cond.get("entity_id"))
        return actual == expected

    if ctype == "or":
        return any(
            _eval_condition(c, states, trigger_id) for c in cond.get("conditions", [])
        )

    if ctype == "and":
        return all(
            _eval_condition(c, states, trigger_id) for c in cond.get("conditions", [])
        )

    if ctype == "template":
        return _eval_template(cond.get("value_template", ""), states, trigger_id)

    raise GateModelError(f"Type de condition hors périmètre : {ctype!r}")


def evaluate_gate(
    states: Mapping[str, str],
    trigger_id: str,
    path: Path = PIPELINE_FILE,
) -> Tuple[bool, bool]:
    """Évalue la porte M2 réelle.

    Retourne (gate_passed, calls_m2) :
      - gate_passed : toutes les conditions de la branche M2 sont vraies ;
      - calls_m2    : la branche évaluée appelle bien script.aeration_m2_fin_episode.
    """
    branch = find_m2_branch(path)
    calls_m2 = _sequence_calls_m2(branch)
    conditions = branch.get("conditions") or []
    gate_passed = all(_eval_condition(c, states, trigger_id) for c in conditions)
    return gate_passed, calls_m2
