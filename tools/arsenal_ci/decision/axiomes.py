"""Axiomes — premisses externes explicites pour R-COV-1 (region decision).

Un axiome est une contrainte booleenne DECLAREE, supposee vraie, exprimee dans
le meme modele de garde que les cascades (cf. model.py). Conformement a
l'invariant verrouille, les axiomes ne sont ni dans la table d'alias, ni dans la
fixture, ni dans le normaliseur : ce sont des premisses externes, RE-DECLAREES
ici (jamais lues depuis le runtime), avec leur provenance documentee.

L'implication `premisse => conclusion` s'ecrit, par equivalence d'operateur
(de Morgan), comme une clause `Ou(Non(premisse), conclusion)` : equivalence
syntaxique, aucune connaissance metier injectee par la mecanique. Le CONTENU de
l'axiome (ce qui domine quoi) est la seule verite de domaine — explicite,
isolee, auditable.
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import AtomeEtat, Garde, Non, Ou


@dataclass(frozen=True)
class Axiome:
    """Contrainte booleenne declaree, supposee vraie, avec sa provenance."""

    identifiant: str
    formule: Garde
    provenance: str


# Axiome D2 : blocage_aeration='on'  =>  autorise_systeme!='on'.
# Cette implication etait la composition de autorise_systeme AVANT CH-2.
# Depuis CH-2 (Option A, autorise constant 'on'), elle n'est PLUS vraie du
# runtime : elle ne subsiste que comme PREMISSE de la fixture gelee
# d2_reason_pre_correction.yaml (controle positif test_lot_2_3). RE-DECLARE
# ici, non lu depuis le runtime.
_BLOCAGE = AtomeEtat("input_boolean.chauffage_blocage_aeration", "on")
_AUTORISE = AtomeEtat("binary_sensor.chauffage_autorise_systeme", "on")

AX_D2 = Axiome(
    identifiant="AX-D2-BLOCAGE-AUTORISE",
    formule=Ou((Non(_BLOCAGE), Non(_AUTORISE))),
    provenance="prémisse de la fixture gelée d2_reason_pre_correction.yaml (ex-composition de autorise_systeme, antérieure à CH-2)",
)

# Jeu d'axiomes de l'instance D2 du moteur general.
AXIOMES_D2 = (AX_D2,)