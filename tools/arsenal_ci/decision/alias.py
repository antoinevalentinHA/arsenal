"""Table d'alias — vocabulaire canonique d'atomes (etage 2 — region decision).

================================ INVARIANT VERROUILLE ========================
La table d'alias est une couche de normalisation SYNTAXIQUE uniquement.

Elle ne porte :
  - aucune semantique metier ;
  - aucune relation de domination ;
  - aucune implication logique ;
  - aucune connaissance d'atteignabilite ;
  - aucune connaissance du domaine Chauffage.

Elle peut normaliser, canoniser, stabiliser ; elle ne doit jamais deduire,
fusionner, ni interpreter. Deux entites distinctes — p. ex.
'binary_sensor.chauffage_autorise_systeme' et
'input_boolean.chauffage_blocage_aeration' — restent DEUX atomes distincts,
quelle que soit une relation logique existant ailleurs dans le systeme.

Seule operation autorisee : identite de reference. Une entree d'alias n'est
permise que si deux ecritures brutes designent le MEME predicat et ne different
que par la representation (quotage, espaces). Jamais une equivalence de valeur
de verite.

La canonisation des operateurs (not / and / or / in) est une couche DISTINCTE,
portee par le normaliseur, pas par cette table.
=============================================================================
"""
from __future__ import annotations

from typing import Dict


# Alias de representation entre ecritures d'une MEME entite. Vide pour CH-1 :
# les deux cascades ecrivent chaque entite de facon identique. Toute entree
# future doit etre une identite de reference, jamais un rapprochement logique.
ALIAS_ENTITES: Dict[str, str] = {}


def canonicaliser_entite(entite: str) -> str:
    """Identifiant canonique d'une entite.

    Identite par defaut ; applique seulement un alias de representation
    explicitement declare. Aucune validation de domaine : une entite inconnue
    est transportee telle quelle. Le vocabulaire clos (fail-closed) porte sur
    la SYNTAXE — traitee par le normaliseur — pas sur la population d'entites.
    """
    e = entite.strip()
    return ALIAS_ENTITES.get(e, e)


def canonicaliser_litteral(valeur: str) -> str:
    """Canonise un litteral (valeur d'etat, valeur de variable) : strip seul."""
    return valeur.strip()