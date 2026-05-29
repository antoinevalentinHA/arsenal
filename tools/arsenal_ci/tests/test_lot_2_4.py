"""Lot 2.4 — R-MIRROR-1, synchronie cerveau <-> miroir (region decision).

Deux sections au statut epistemique DISTINCT :

  1. PREUVE DU MECANISME (cas synthetiques, hermetiques, deterministes).
     Echec ici => defaut de R-MIRROR-1.

  2. CONSTAT DE SYNCHRONIE DU DEPOT (runtime vivant, lecture seule).
     Echec ici => depot desynchronise (corriger la config), PAS necessairement
     un defaut du moteur. C'est la suite synthetique verte qui autorise cette
     attribution (notamment le must-pass a forme differente, qui ecarte le faux
     positif).
"""
from pathlib import Path

import pytest

from arsenal_ci.decision.normaliseur import normaliser_texte
from arsenal_ci.decision.r_mirror_1 import (
    RULE_ID,
    comparer,
    comparer_fichiers,
    comparer_runtime,
)
from arsenal_ci.report.result import ExecutionError
from arsenal_ci.rules.policy import Severity


def _yaml_reason(jinja: str) -> str:
    corps = "\n".join("  " + ligne for ligne in jinja.strip("\n").split("\n"))
    return "reason: |\n" + corps + "\n"


def _cascade(jinja: str, fichier: str = "synthetique"):
    return normaliser_texte(_yaml_reason(jinja), "reason", fichier)


# =====================================================================
# 1. PREUVE DU MECANISME  (echec ici => defaut de R-MIRROR-1)
# =====================================================================

def test_must_pass_forme_differente():
    # Memes structure/gardes/emissions/ordre, mais commentaires + espacement
    # differents : la forme doit etre ignoree, le sens compare.
    cerveau = _cascade(
        "{% if is_state('x.a','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n"
        "{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade(
        "{# miroir diagnostic #}\n"
        "{% if is_state('x.a', 'on') %}\n\n  A\n\n"
        "{% elif is_state('x.b', 'on') %}\n  {# note #}\n  B\n"
        "{% else %}\n  C\n{% endif %}"
    )
    assert comparer(cerveau, miroir) == []


def test_garde_differente():
    cerveau = _cascade(
        "{% if is_state('x.a','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade(
        "{% if is_state('x.c','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    violations = comparer(cerveau, miroir)
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.severity is Severity.BLOCKING
    assert "[0]" in v.message
    assert "garde differente" in v.message


def test_ordre_different():
    cerveau = _cascade(
        "{% if is_state('x.a','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade(
        "{% if is_state('x.b','on') %}\nB\n"
        "{% elif is_state('x.a','on') %}\nA\n{% else %}\nC\n{% endif %}"
    )
    violations = comparer(cerveau, miroir)
    assert len(violations) == 2
    assert "[0]" in violations[0].message
    assert "[1]" in violations[1].message


def test_nombre_different():
    cerveau = _cascade(
        "{% if is_state('x.a','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade("{% if is_state('x.a','on') %}\nA\n{% else %}\nC\n{% endif %}")
    violations = comparer(cerveau, miroir)
    assert len(violations) == 1
    assert "nombre de branches" in violations[0].message
    assert "reason=3" in violations[0].message
    assert "state=2" in violations[0].message


def test_issue_differente():
    cerveau = _cascade("{% if is_state('x.a','on') %}\nA\n{% else %}\nC\n{% endif %}")
    miroir = _cascade("{% if is_state('x.a','on') %}\nZ\n{% else %}\nC\n{% endif %}")
    violations = comparer(cerveau, miroir)
    assert len(violations) == 1
    assert "[0]" in violations[0].message
    assert "issue" in violations[0].message


def test_sous_cascade_differente():
    cerveau = _cascade(
        "{% if is_state('x.p','on') %}\n"
        "{% if is_state('x.q','on') %}\nA\n{% else %}\nB\n{% endif %}\n"
        "{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade(
        "{% if is_state('x.p','on') %}\n"
        "{% if is_state('x.r','on') %}\nA\n{% else %}\nB\n{% endif %}\n"
        "{% else %}\nC\n{% endif %}"
    )
    violations = comparer(cerveau, miroir)
    assert len(violations) == 1
    assert "[0]" in violations[0].message
    assert "sous-cascade differente" in violations[0].message


def test_determinisme():
    cerveau = _cascade(
        "{% if is_state('x.a','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    miroir = _cascade(
        "{% if is_state('x.c','on') %}\nA\n"
        "{% elif is_state('x.b','on') %}\nB\n{% else %}\nC\n{% endif %}"
    )
    assert comparer(cerveau, miroir) == comparer(cerveau, miroir)


def test_entree_illisible_execution_error(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("autre: 1\n", encoding="utf-8")
    with pytest.raises(ExecutionError):
        comparer_fichiers(bad, "reason", bad, "state")


# =====================================================================
# 2. CONSTAT DE SYNCHRONIE DU DEPOT  (runtime vivant, lecture seule)
#
# Echec ici => depot desynchronise, corriger la CONFIG (pas le moteur).
# Apres CH-2, ce constat reste vert si la correction est appliquee des deux
# cotes ; il est rouge pendant un etat transitoire desynchronise — c'est sa
# fonction, pas une regression du moteur.
# =====================================================================

def test_constat_synchronie_depot():
    assert comparer_runtime() == []