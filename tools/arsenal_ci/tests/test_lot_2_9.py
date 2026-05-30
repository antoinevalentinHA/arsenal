"""Lot 2.9 — R-ISO-1, iso-comportement de la decision centrale (region decision).

Libelle doctrinal : INV-30-5. Deux sections au statut epistemique DISTINCT :

  1. PREUVE DU MECANISME (cas synthetiques, hermetiques, deterministes) :
     - iso parfait -> aucune violation ;
     - emissions differentes a squelette egal -> aucune violation (must-pass :
       ecarte le faux positif sur renommage de raison) ;
     - profondeur de sous-cascade differente a tete egale -> aucune violation
       (la presence se decline cote reason, se collapse cote desired_mode) ;
     - garde de tete divergente -> violation localisee ;
     - nombre de branches de tete different -> violation.
     Echec ici => defaut de R-ISO-1.

  2. CONSTAT D'ISO DU DEPOT (runtime vivant, lecture seule) :
     reason <-> desired_mode -> VERT sur le runtime corrige. Echec ici => depot
     desynchronise (corriger la config) OU runtime illisible, a trier comme tel,
     PAS necessairement un defaut du moteur (la suite synthetique verte autorise
     cette attribution).

Aucun runtime touche.
"""
from pathlib import Path

from arsenal_ci.decision.normaliseur import normaliser_texte
from arsenal_ci.decision.r_iso_1 import (
    RULE_ID,
    THERMIQUE_CLE,
    comparer,
    comparer_runtime,
)
from arsenal_ci.rules.policy import Severity


def _yaml(cle: str, jinja: str) -> str:
    corps = "\n".join("  " + ligne for ligne in jinja.strip("\n").split("\n"))
    return f"{cle}: |\n" + corps + "\n"


def _cascade(cle: str, jinja: str):
    return normaliser_texte(_yaml(cle, jinja), cle, "synthetique")


# ------------------------------------------------------ 1. preuve du mecanisme

def test_iso_parfait_aucune_violation():
    j = (
        "{% if is_state('x.a','on') %}\nr1\n"
        "{% elif is_state('x.b','on') %}\nr2\n"
        "{% else %}\nr3\n{% endif %}"
    )
    narration = _cascade("reason", j)
    thermique = _cascade("desired_mode", j)
    assert comparer(narration, thermique) == []


def test_emissions_differentes_squelette_egal_must_pass():
    # Meme squelette de gardes, emissions differentes : renommer une raison ne
    # doit JAMAIS faire rougir R-ISO-1.
    jn = (
        "{% if is_state('x.a','on') %}\nconfort_force\n"
        "{% elif is_state('x.b','on') %}\nbesoin_thermique\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    jt = (
        "{% if is_state('x.a','on') %}\ncomfort\n"
        "{% elif is_state('x.b','on') %}\ncomfort\n"
        "{% else %}\nreduced\n{% endif %}"
    )
    assert comparer(_cascade("reason", jn), _cascade("desired_mode", jt)) == []


def test_profondeur_sous_cascade_differente_must_pass():
    # Tete egale ; cote reason la branche [1] se decline par valeur, cote
    # desired_mode elle se collapse en {{ var }}. Divergence de narration
    # legitime, exclue du squelette -> aucune violation.
    jn = (
        "{% if is_state('x.a','on') %}\nr1\n"
        "{% elif is_state('x.p','on') %}\n"
        "{% set c = states('x.s') %}\n"
        "{% if c == 'comfort' %}\nbesoin_thermique\n"
        "{% elif c == 'neutre' %}\npresence_on\n"
        "{% else %}\nconfort_suffisant\n{% endif %}\n"
        "{% else %}\nabsence\n{% endif %}"
    )
    jt = (
        "{% if is_state('x.a','on') %}\ncomfort\n"
        "{% elif is_state('x.p','on') %}\n"
        "{% set c = states('x.s') %}\n"
        "{% if c in ['comfort','neutre','reduced'] %}\n{{ c }}\n"
        "{% else %}\nneutre\n{% endif %}\n"
        "{% else %}\nreduced\n{% endif %}"
    )
    assert comparer(_cascade("reason", jn), _cascade("desired_mode", jt)) == []


def test_garde_tete_divergente_violation_localisee():
    jn = (
        "{% if is_state('x.a','on') %}\nr1\n"
        "{% elif is_state('x.b','on') %}\nr2\n"
        "{% else %}\nr3\n{% endif %}"
    )
    jt = (
        "{% if is_state('x.a','on') %}\nm1\n"
        "{% elif is_state('x.DIFFERENT','on') %}\nm2\n"
        "{% else %}\nm3\n{% endif %}"
    )
    violations = comparer(_cascade("reason", jn), _cascade("desired_mode", jt))
    assert len(violations) == 1
    v = violations[0]
    assert v.rule == RULE_ID
    assert v.source == "desired_mode[1]"
    assert v.target == "reason[1]"
    assert v.severity is Severity.BLOCKING


def test_nombre_branches_tete_different_violation():
    jn = (
        "{% if is_state('x.a','on') %}\nr1\n"
        "{% elif is_state('x.b','on') %}\nr2\n"
        "{% else %}\nr3\n{% endif %}"
    )
    jt = "{% if is_state('x.a','on') %}\nm1\n{% else %}\nm2\n{% endif %}"
    violations = comparer(_cascade("reason", jn), _cascade("desired_mode", jt))
    assert len(violations) == 1
    assert violations[0].source == THERMIQUE_CLE
    assert "nombre de branches" in violations[0].message


# ----------------------------------------------------- 2. constat live runtime

def test_constat_iso_runtime_vert():
    assert comparer_runtime() == []


def test_determinisme():
    assert comparer_runtime() == comparer_runtime()
