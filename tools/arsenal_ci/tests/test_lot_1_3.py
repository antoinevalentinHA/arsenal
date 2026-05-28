"""Lot 1.3 test suite — orchestration & reporting."""
import json
import os

from arsenal_ci import cli
from arsenal_ci.parsing.builder import GraphBuilder
from arsenal_ci.registers.loader import RegistryLoader
from arsenal_ci.report import formatters, orchestrator
from arsenal_ci.report.result import ExitCode, Result, Summary, summarise
from arsenal_ci.report.violation import Violation
from arsenal_ci.rules.policy import CHAUFFAGE_POLICY, Policy, Severity

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return fh.read()


def _registry():
    return RegistryLoader().load_from_yaml(_load("registres_etage1.yaml"))


def _graph(name):
    return GraphBuilder().build_from_yaml(_load(name), file=name)


# ------------------------------------------------------------ exit codes

def test_exit_pass_on_conform():
    r = orchestrator.run(_graph("autorisation_post_phase3.yaml"), _registry(), CHAUFFAGE_POLICY)
    assert r.status == "pass"
    assert r.exit_code() is ExitCode.PASS


def test_exit_violation_on_pre_phase3():
    r = orchestrator.run(_graph("autorisation_pre_phase3.yaml"), _registry(), CHAUFFAGE_POLICY)
    assert r.status == "fail"
    assert r.exit_code() is ExitCode.VIOLATION
    assert r.summary.blocking == 1


def test_exit_execution_error_distinct_from_violation():
    r = Result(execution_error="registre corrompu")
    assert r.status == "error"
    assert r.exit_code() is ExitCode.EXECUTION_ERROR
    # execution error short-circuits: no violations considered
    assert r.violations == []


# ------------------------------------------------------ three planes isolation

def test_execution_error_is_not_a_violation():
    # A bad registry must yield exec error (2), never a doctrinal verdict.
    r = cli._build_result(
        os.path.join(FIXTURES, "does_not_exist.yaml"),
        [os.path.join(FIXTURES, "autorisation_pre_phase3.yaml")],
    )
    assert r.status == "error"
    assert r.exit_code() is ExitCode.EXECUTION_ERROR


def test_missing_parametres_registry_is_exec_error():
    bad = os.path.join(FIXTURES, "_bad_registry.yaml")
    with open(bad, "w", encoding="utf-8") as fh:
        fh.write("override:\n  - input_boolean.x\n")  # no parametres -> META-2 block
    try:
        r = cli._build_result(bad, [os.path.join(FIXTURES, "autorisation_pre_phase3.yaml")])
        assert r.status == "error"
        assert r.exit_code() is ExitCode.EXECUTION_ERROR
    finally:
        os.remove(bad)


# ------------------------------------------------------------ strict mode

def test_warning_neutral_by_default():
    v = Violation("X", "m", "s", "t", "f", "k", severity=Severity.WARNING)
    r = Result(violations=[v], summary=summarise([v]))
    assert r.exit_code(strict=False) is ExitCode.PASS
    assert r.exit_code(strict=True) is ExitCode.VIOLATION


def test_strict_does_not_downgrade_blocking():
    v = Violation("X", "m", "s", "t", "f", "k", severity=Severity.BLOCKING)
    r = Result(violations=[v], summary=summarise([v]))
    assert r.exit_code(strict=False) is ExitCode.VIOLATION
    assert r.exit_code(strict=True) is ExitCode.VIOLATION


# ------------------------------------------------------------ ordering

def test_deterministic_ordering_blocking_first():
    g = _graph("autorisation_pre_phase3.yaml")
    # craft a registry where the autorisation also reads an unknown -> warning
    reg = _registry()
    r = orchestrator.run(g, reg, CHAUFFAGE_POLICY)
    # blocking must precede any warning
    sevs = [v.severity for v in r.violations]
    ranks = [0 if s is Severity.BLOCKING else (1 if s is Severity.ERROR else 2) for s in sevs]
    assert ranks == sorted(ranks)


# ------------------------------------------------------------ formatters

def test_human_format_conform():
    r = orchestrator.run(_graph("autorisation_post_phase3.yaml"), _registry(), CHAUFFAGE_POLICY)
    out = formatters.format_human(r)
    assert "CONFORME" in out
    assert "Aucune violation" in out


def test_human_format_execution_error_has_no_verdict():
    r = Result(execution_error="boom")
    out = formatters.format_human(r)
    assert "ERREUR D'EXECUTION" in out
    assert "CONFORME" not in out and "ECHEC" not in out


def test_json_format_structure():
    r = orchestrator.run(_graph("autorisation_pre_phase3.yaml"), _registry(), CHAUFFAGE_POLICY)
    payload = json.loads(formatters.format_json(r))
    assert payload["status"] == "fail"
    assert payload["exit_code"] == 1
    assert payload["execution_error"] is None
    assert payload["summary"]["blocking"] == 1
    assert payload["violations"][0]["rule"] == "R-CI-1"


# ------------------------------------------------------------ CLI end-to-end

def test_cli_returns_exit_codes(tmp_path):
    reg = os.path.join(FIXTURES, "registres_etage1.yaml")
    pre = os.path.join(FIXTURES, "autorisation_pre_phase3.yaml")
    post = os.path.join(FIXTURES, "autorisation_post_phase3.yaml")

    assert cli.main(["--registry", reg, "--config", post]) == 0
    assert cli.main(["--registry", reg, "--config", pre]) == 1
    assert cli.main(["--registry", "/nope.yaml", "--config", pre]) == 2


def test_cli_writes_json_to_file(tmp_path):
    reg = os.path.join(FIXTURES, "registres_etage1.yaml")
    pre = os.path.join(FIXTURES, "autorisation_pre_phase3.yaml")
    out = tmp_path / "report.json"
    code = cli.main(["--registry", reg, "--config", pre, "--json", str(out)])
    assert code == 1
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["exit_code"] == 1
    assert payload["summary"]["blocking"] == 1
