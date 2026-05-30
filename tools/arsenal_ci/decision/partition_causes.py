"""Partition cause / consequence — premisse doctrinale de R-CAUSE-1.

Doctrine (libelle INV-D1/D3) : une raison emise par la cascade de decision doit
toujours nommer une CAUSE (condition declenchante amont), jamais une CONSEQUENCE
(etat d'autorisation compose, derive de la decision elle-meme). Surfacer une
consequence a la place de sa cause est la pathologie D1/D2 — la "causalite
menteuse" — dont D2 est le specimen canonique.

Conformement au pattern d'axiomes.py, l'ensemble des jetons de consequence est
RE-DECLARE ici (jamais lu du runtime), avec sa provenance documentee. Source de
verite doctrinale : contrat chauffage/30_decision_centrale.md, section 4
"Hierarchie officielle des causes" + table des raisons : le Niveau 1 est une
categorie reservee et `chauffage_non_autorise` n'est plus emise depuis CH-2 —
elle nomme le compose d'autorisation (binary_sensor.chauffage_autorise_systeme),
donc une consequence, pas une cause declenchante.

La partition est volontairement minimale : seuls les jetons reellement
caracterises comme consequences y figurent. En ajouter de speculatifs serait
inventer de la doctrine. Toute extension future doit pointer une cause
documentee dans le contrat 30 et nommer un etat compose/derive, non une
condition declenchante.
"""
from __future__ import annotations

from typing import FrozenSet

# Jetons interdits comme raison : noms d'un etat d'autorisation compose
# (consequence de la decision), non d'une condition declenchante.
# Provenance : contrat chauffage/30_decision_centrale.md sec. 4 + table des
# raisons (categorie reservee Niveau 1, non emise depuis CH-2).
CONSEQUENCES: FrozenSet[str] = frozenset(
    {
        "chauffage_non_autorise",
    }
)
