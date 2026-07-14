"""Lot 5.2 — Gate LIVE : l'oracle de politique d'absence COOL sur le VRAI runtime.

Distinct du Lot 5.1 (fixtures inline). Ici l'oracle lit les VRAIS fichiers
runtime livrés au Lot 3 et prouve qu'ils encodent les invariants du contrat 15
(INV-VETO-2/3/4/5/6/7/9). Ce gate ne peut être vert qu'une fois le runtime
conforme — c'est pourquoi il n'a été branché qu'au Lot 3 (et non au Lot 2).

Frontière assumée : structure, pas rendu Jinja. Le comportement runtime complet
(échéance, réconciliation boot, changement de durée) est validé en terrain (Lot 5).
"""
from pathlib import Path

import yaml

from arsenal_ci.behavior.cool_veto_gate import (
    _LoaderTolerant,
    check_autorisation_consumes_composite,
    check_composite_formula,
    check_extinction_horodatage,
    check_helper_no_initial,
    check_horodatage_single_writer,
    check_no_fixed_duration,
    check_no_preparation,
)

_ROOT = Path(__file__).resolve().parents[3]

COOL = _ROOT / "12_template_sensors" / "climatisation" / "autorisation" / "cool.yaml"
VETO = _ROOT / "12_template_sensors" / "climatisation" / "blocages" / "veto_absence_vacances.yaml"
ABSENCE = _ROOT / "12_template_sensors" / "climatisation" / "blocages" / "absence_longue.yaml"
HELPER = _ROOT / "03_input_numbers" / "climatisation" / "absence" / "duree.yaml"
AUTOS_DIR = _ROOT / "11_automations" / "climatisation"


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _load_climatisation_automations():
    autos = []
    for path in sorted(AUTOS_DIR.rglob("*.yaml")):
        docs = yaml.load(path.read_text(encoding="utf-8"), Loader=_LoaderTolerant)
        if isinstance(docs, list):
            autos.extend(d for d in docs if isinstance(d, dict) and "id" in d)
    return autos


# ---------------------------------------------------------- gate live (0 violation)

def test_runtime_autorisation_consumes_composite():
    assert check_autorisation_consumes_composite(_text(COOL)) == []


def test_runtime_composite_formula():
    assert check_composite_formula(_text(VETO)) == []


def test_runtime_extinction_horodatage():
    assert check_extinction_horodatage(_text(ABSENCE)) == []


def test_runtime_helper_no_initial():
    assert check_helper_no_initial(_text(HELPER)) == []


def test_runtime_no_fixed_duration():
    assert check_no_fixed_duration(_text(ABSENCE), _text(VETO), _text(COOL)) == []


def test_runtime_horodatage_single_writer():
    assert check_horodatage_single_writer(_load_climatisation_automations()) == []


def test_runtime_no_preparation_in_c20_scope():
    # C20 ne crée aucune préparation (frontière C21).
    assert check_no_preparation(_text(COOL), _text(VETO), _text(ABSENCE)) == []
