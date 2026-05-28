"""Lot 1.2 test suite — taxonomy branching.

Covers: loader internal validation (blocking), Registry query API, external
handling, META-2 blocking, and the migrated taxonomy-driven R-CI-1 proven
again on the historical double reference fixtures.
"""
import os

import pytest

from arsenal_ci.graph.edge import EdgeKind
from arsenal_ci.parsing.builder import GraphBuilder
from arsenal_ci.registers.classification import Layer
from arsenal_ci.registers.loader import RegistryError, RegistryLoader
from arsenal_ci.rules import meta_2, r_ci_1
from arsenal_ci.rules.policy import CHAUFFAGE_POLICY, Policy, Severity

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")
SRC = "binary_sensor.chauffage_autorisation_etage_1"


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


def _registry():
    return RegistryLoader().load_from_yaml(_load("registres_etage1.yaml"))


# ----------------------------------------------------------- loader validation

def test_loader_meta_parsed():
    reg = _registry()
    assert reg.meta.exclus_invariants_registre is True


def test_loader_missing_parametres_blocks():
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml("override:\n  - input_boolean.x\n")


def test_loader_unknown_layer_blocks():
    raw = "foobar:\n  - sensor.x\nparametres:\n  exclus_invariants_registre: true\n"
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_duplicate_blocks():
    raw = (
        "override:\n  - sensor.x\n"
        "perception:\n  - sensor.x\n"
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_bad_entity_id_blocks():
    raw = "override:\n  - NotAnEntityId\nparametres:\n  exclus_invariants_registre: true\n"
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_calibration_orphan_blocks():
    raw = (
        "perception:\n  - sensor.z\n"
        "calibration:\n  - sensor.orphan\n"
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    with pytest.raises(RegistryError):
        RegistryLoader().load_from_yaml(raw)


def test_loader_calibration_overlay_ok():
    raw = (
        "perception:\n  - sensor.z\n"
        "calibration:\n  - sensor.z\n"
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    reg = RegistryLoader().load_from_yaml(raw)
    assert reg.is_calibration("sensor.z")
    assert reg.layer_of("sensor.z") is Layer.PERCEPTION  # keeps functional layer


# --------------------------------------------------------------- registry API

def test_registry_layer_of():
    reg = _registry()
    assert reg.layer_of("input_boolean.standby_force") is Layer.OVERRIDE
    assert reg.layer_of(SRC) is Layer.AUTORISATION
    assert reg.layer_of("sensor.unknown") is None


def test_registry_external_distinct_from_unknown():
    raw = (
        "externe:\n  - sensor.tier\n"
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    reg = RegistryLoader().load_from_yaml(raw)
    assert reg.is_external("sensor.tier")
    assert reg.layer_of("sensor.tier") is Layer.EXTERNE
    assert not reg.is_external("sensor.unknown")  # unknown != external


# ----------------------------------------------------------------- META-2

def test_meta2_blocks_ungoverned_node():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    empty = RegistryLoader().load_from_yaml(
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    vs = meta_2.check(g, empty, CHAUFFAGE_POLICY)
    assert len(vs) == 1
    assert vs[0].rule == "META-2"
    assert vs[0].severity is Severity.BLOCKING


def test_meta2_silent_when_node_classified():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    assert meta_2.check(g, _registry(), CHAUFFAGE_POLICY) == []


def test_meta2_inactive_policy_no_violation():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    empty = RegistryLoader().load_from_yaml(
        "parametres:\n  exclus_invariants_registre: true\n"
    )
    no_meta2 = Policy(meta2_active=False)
    assert meta_2.check(g, empty, no_meta2) == []


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


def test_rci1_ignores_non_authorisation_source():
    # If standby_force composed a perception entity, R-CI-1 must not fire
    # (R-CI-1 only constrains authorisation sources).
    raw = (
        "template:\n"
        "  - sensor:\n"
        "      - name: 'Perception X'\n"
        "        unique_id: chauffage_perception_etage_1\n"
        "        state: \"{{ is_state('input_boolean.standby_force','on') }}\"\n"
    )
    g = GraphBuilder().build_from_yaml(raw)
    assert r_ci_1.check(g, _registry(), CHAUFFAGE_POLICY) == []
