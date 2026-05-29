"""Lot 2.0 — etage 2 scaffold sentinel (decision cascade model region).

This lot carries NO invariant and NO business logic. Its single purpose is
to prove that the etage 2 region ``arsenal_ci.decision`` is collected and
imported by the EXISTING runner (``PYTHONPATH=tools`` + pytest) without
perturbing etage 1.

The cascade normaliser (T1), R-COV-1 (T3) and R-MIRROR-1 (T4) will populate
``arsenal_ci.decision`` later; until then it is an intentionally empty
reserved namespace. No graph model, no registry, no runtime is touched here.
"""
from arsenal_ci import decision


def test_decision_subpackage_importable():
    # The etage 2 model region imports under the existing import mode.
    assert decision is not None


def test_decision_subpackage_is_a_package():
    # Reserved namespace: it is a package (has __path__), not a stray module.
    assert hasattr(decision, "__path__")