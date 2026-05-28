"""Lot 1.2 test suite — rich sovereign-format taxonomy branching.

Covers: rich loader validation (blocking), Registre/Couche/Statut API,
section/field coherence, the deprecie special case, external handling,
META-2, and the taxonomy-driven R-CI-1 on the historical double reference.
"""
import os

import pytest

from arsenal_ci.parsing.builder import GraphBuilder
from arsenal_ci.registers.classification import Couche, Registre, Statut
from arsenal_ci.registers.loader import RegistryError, RegistryLoader
from arsenal_ci.rules import meta_2, r_ci_1
from arsenal_ci.rules.policy import CHAUFFAGE_POLICY, Policy, Severity

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
SRC = "binary_sensor.chauffage_autorisation_etage_1"

_PARAMS = "parametres:\n  exclus_invariants_registre: true\n"


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


def _registry():
    return RegistryLoader().load_from_yaml(_load("registres_etage1.yaml"))


def _entry(eid, registre, couche, statut="actif", contrat="C.md", extra=""):
    return (
        f"  - entity_id: {eid}\n"
        f"    registre: {registre}\n"
        f"    couche: {couche}\n"
        f"    statut: {statut}\n"
        + (f"    contrat: {contrat}\n" if contrat else "")
        + extra
    )


# --------------------------------------------------------- loader validation

def test_loader_meta_parsed():
    reg = _registry()
    assert reg.meta.exclus_invariants_registre is True


def test_loader_couverture_kept_in_meta():
    reg = _registry()
    cov = dict(reg.meta.couverture)
    assert cov.get("registres_couverts") == 8
    assert cov.get("perimetre") == "etage_1"


def test_loader_ignores_documentary_metadata():
    # version/date/perimetre_statut/meta2_mode must not raise "section inconnue".
    reg = _registry()
    assert len(reg) >= 4  # entities loaded despite metadata keys present


def test_loader_missing_parametres_blocks():
    raw = "override:\n" + _entry("input_boolean.x", "override", "override")
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_unknown_section_blocks():
    raw = "foobar:\n" + _entry("sensor.x", "perception", "perception") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_unknown_registre_blocks():
    raw = "perception:\n" + _entry("sensor.x", "nope", "perception") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_unknown_couche_blocks():
    raw = "perception:\n" + _entry("sensor.x", "perception", "nope") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_missing_statut_blocks():
    raw = (
        "perception:\n"
        "  - entity_id: sensor.x\n"
        "    registre: perception\n"
        "    couche: perception\n"
        "    contrat: C.md\n"
    ) + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_unknown_statut_blocks():
    raw = "perception:\n" + _entry("sensor.x", "perception", "perception", statut="zombie") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_section_registre_incoherence_blocks():
    # entry under 'perception' but registre=override -> incoherence
    raw = "perception:\n" + _entry("sensor.x", "override", "override") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_contrat_required_for_governed():
    raw = "perception:\n" + _entry("sensor.x", "perception", "perception", contrat="") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_contrat_optional_for_externe():
    raw = "externe:\n" + _entry("sensor.tier", "externe", "externe", contrat="") + _PARAMS
    reg = RegistryLoader().load_from_yaml(raw)
    assert reg.is_external("sensor.tier")


def test_loader_duplicate_blocks():
    raw = (
        "override:\n" + _entry("sensor.x", "override", "override")
        + "perception:\n" + _entry("sensor.x", "perception", "perception")
        + _PARAMS
    )
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_bad_entity_id_blocks():
    raw = "perception:\n" + _entry("NotAnId", "perception", "perception") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


# ----------------------------------------------------- deprecie special case

def test_deprecie_entity_is_known_and_classified():
    reg = _registry()
    eid = "input_boolean.blocage_geofencing"
    assert reg.is_known(eid)              # META-2 satisfied
    assert reg.is_deprecie(eid)
    assert reg.statut_of(eid) is Statut.DEPRECIE
    assert reg.registre_of(eid) is Registre.SECURITE   # keeps real register
    assert reg.couche_of(eid) is Couche.SECURITE
    assert reg.contrat_of(eid)            # deprecie keeps its contract


def test_deprecie_section_requires_deprecie_statut():
    # an entry under 'deprecie' with statut=actif must be rejected
    raw = "deprecie:\n" + _entry("sensor.x", "perception", "perception", statut="actif") + _PARAMS
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


# --------------------------------------------------------------- registry API

def test_registry_couche_and_registre():
    reg = _registry()
    assert reg.couche_of("input_boolean.standby_force") is Couche.DECISION
    assert reg.registre_of("input_boolean.standby_force") is Registre.OVERRIDE
    assert reg.couche_of(SRC) is Couche.AUTORISATION
    assert reg.couche_of("sensor.unknown") is None


def test_registry_layer_of_alias():
    reg = _registry()
    assert reg.layer_of(SRC) is reg.couche_of(SRC)


def test_registry_external_distinct_from_unknown():
    reg = _registry()
    assert reg.is_external("sensor.meteo_exterieure_cloud")
    assert reg.couche_of("sensor.meteo_exterieure_cloud") is Couche.EXTERNE
    assert not reg.is_external("sensor.unknown")


def test_registry_calibration_overlay_keeps_couche():
    reg = _registry()
    eid = "sensor.chauffage_perception_etage_1"
    assert reg.is_calibration(eid)
    assert reg.couche_of(eid) is Couche.PERCEPTION


# ----------------------------------------------------------------- META-2

def test_meta2_blocks_ungoverned_node():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    empty = RegistryLoader().load_from_yaml(_PARAMS)
    vs = meta_2.check(g, empty, CHAUFFAGE_POLICY)
    assert len(vs) == 1
    assert vs[0].rule == "META-2"
    assert vs[0].severity is Severity.BLOCKING


def test_meta2_silent_when_node_classified():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    assert meta_2.check(g, _registry(), CHAUFFAGE_POLICY) == []


def test_meta2_inactive_policy_no_violation():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    empty = RegistryLoader().load_from_yaml(_PARAMS)
    assert meta_2.check(g, empty, Policy(meta2_active=False)) == []


# ------------------------------------ cardinal: taxonomy-driven R-CI-1

def test_rci1_pre_phase3_violation_via_taxonomy():
    g = GraphBuilder().build_from_yaml(_load("autorisation_pre_phase3.yaml"))
    vs = r_ci_1.check(g, _registry(), CHAUFFAGE_POLICY)
    assert len(vs) == 1
    assert vs[0].rule == "R-CI-1"
    assert vs[0].target == "input_boolean.standby_force"
    assert vs[0].severity is Severity.BLOCKING


def test_rci1_post_phase3_zero_violations_via_taxonomy():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    assert r_ci_1.check(g, _registry(), CHAUFFAGE_POLICY) == []
