"""Lot 1.1 test suite.

Levels:
  1. unit: jinja_scanner, edge_typer
  2. unit: graph construction (typed edge set)
  3. cardinal: double reference test — topology AND R-CI-1 stub.
"""
import os

import pytest

from arsenal_ci.graph.edge import EdgeKind
from arsenal_ci.parsing.builder import GraphBuilder
from arsenal_ci.parsing.edge_typer import kind_for_host_key
from arsenal_ci.parsing.jinja_scanner import scan_references
from arsenal_ci.rules import r_ci_1
from arsenal_ci.registers.loader import RegistryLoader
from arsenal_ci.rules.policy import CHAUFFAGE_POLICY

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------- level 1

def test_scanner_extracts_function_refs():
    text = "{{ is_state('input_boolean.standby_force','off') and states('sensor.x') }}"
    refs = scan_references(text)
    assert "input_boolean.standby_force" in refs
    assert "sensor.x" in refs


def test_scanner_extracts_state_attr():
    refs = scan_references("{{ state_attr('climate.salon', 'temperature') }}")
    assert refs == ["climate.salon"]


def test_scanner_extracts_dotted_access():
    refs = scan_references("{{ states.binary_sensor.foo.state }}")
    assert "binary_sensor.foo" in refs


def test_typer_state_is_composes():
    assert kind_for_host_key("state") is EdgeKind.COMPOSES
    assert kind_for_host_key("value_template") is EdgeKind.COMPOSES


def test_typer_attributes_is_reads():
    assert kind_for_host_key("attributes") is EdgeKind.READS
    assert kind_for_host_key("availability") is EdgeKind.READS
    assert kind_for_host_key("icon") is EdgeKind.READS


# ---------------------------------------------------------------- level 2

def test_graph_identity_unique_id():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    ids = {n.entity_id for n in g.nodes}
    assert "binary_sensor.chauffage_autorisation_etage_1" in ids


def test_graph_typed_edges_present():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    src = "binary_sensor.chauffage_autorisation_etage_1"
    # perception composes the state
    assert g.has_edge(src, "sensor.chauffage_perception_etage_1", EdgeKind.COMPOSES)
    # standby only read
    assert g.has_edge(src, "input_boolean.standby_force", EdgeKind.READS)
    assert not g.has_edge(src, "input_boolean.standby_force", EdgeKind.COMPOSES)


# ---------------------------------------------------------------- cardinal

SRC = "binary_sensor.chauffage_autorisation_etage_1"


def test_reference_pre_phase3_topology_has_composes():
    g = GraphBuilder().build_from_yaml(_load("autorisation_pre_phase3.yaml"))
    assert g.has_edge(SRC, "input_boolean.standby_force", EdgeKind.COMPOSES)


def test_reference_pre_phase3_rule_violation():
    g = GraphBuilder().build_from_yaml(_load("autorisation_pre_phase3.yaml"))
    violations = r_ci_1.check(g, _registry(), CHAUFFAGE_POLICY)
    assert len(violations) == 1
    assert violations[0].rule == "R-CI-1"
    assert violations[0].target == "input_boolean.standby_force"


def test_reference_post_phase3_topology_no_composes():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    assert not g.has_edge(SRC, "input_boolean.standby_force", EdgeKind.COMPOSES)
    assert g.has_edge(SRC, "input_boolean.standby_force", EdgeKind.READS)


def test_reference_post_phase3_zero_violations():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    assert r_ci_1.check(g, _registry(), CHAUFFAGE_POLICY) == []


# ---------------------------------------------------------------- immutability

def test_graph_is_immutable():
    g = GraphBuilder().build_from_yaml(_load("autorisation_post_phase3.yaml"))
    with pytest.raises((AttributeError, TypeError)):
        g.edges.append("x")  # tuple -> no append

def _registry():
    return RegistryLoader().load_from_yaml(_load("registres_etage1.yaml"))
