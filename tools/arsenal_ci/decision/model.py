"""Modele decisionnel normalise (etage 2 — region decision).

Objets manipules par le normaliseur de cascade. Structures de donnees PURES :
aucune logique d'atteignabilite, aucune semantique metier, aucune relation de
domination. Une cascade reason/state est representee comme un arbre ordonne de
branches ; l'ordre est porteur de la pathologie et n'est JAMAIS reordonne.

Ce module ne contient ni R-COV-1 ni R-MIRROR-1. Il fournit le modele et sa
signature structurelle canonique (utilisee pour le determinisme et le simple
constat d'egalite cerveau <-> miroir), rien de plus.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Union


# --------------------------------------------------------------------- gardes

class Garde:
    """Base d'une garde canonique. Chaque garde expose une cle() stable."""

    def cle(self) -> str:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass(frozen=True)
class AtomeEtat(Garde):
    """Canonisation de is_state('<entite>', '<valeur>')."""

    entite: str
    valeur: str

    def cle(self) -> str:
        return f"etat({self.entite}={self.valeur})"


@dataclass(frozen=True)
class AtomeVar(Garde):
    """Canonisation d'une comparaison <variable> == '<valeur>'."""

    variable: str
    valeur: str

    def cle(self) -> str:
        return f"var({self.variable}={self.valeur})"


@dataclass(frozen=True)
class Non(Garde):
    """Negation. Conservee explicite : pas de repli 'on' -> 'off' (qui
    supposerait une connaissance de domaine sur la binarite de l'entite)."""

    operande: Garde

    def cle(self) -> str:
        return f"not({self.operande.cle()})"


@dataclass(frozen=True)
class Et(Garde):
    """Conjonction. Operandes canonicalises par tri sur leur cle (commutatif)."""

    operandes: Tuple[Garde, ...]

    def __post_init__(self) -> None:
        ordonnes = tuple(sorted(self.operandes, key=lambda o: o.cle()))
        object.__setattr__(self, "operandes", ordonnes)

    def cle(self) -> str:
        return "and(" + ",".join(o.cle() for o in self.operandes) + ")"


@dataclass(frozen=True)
class Ou(Garde):
    """Disjonction. Operandes canonicalises par tri sur leur cle (commutatif)."""

    operandes: Tuple[Garde, ...]

    def __post_init__(self) -> None:
        ordonnes = tuple(sorted(self.operandes, key=lambda o: o.cle()))
        object.__setattr__(self, "operandes", ordonnes)

    def cle(self) -> str:
        return "or(" + ",".join(o.cle() for o in self.operandes) + ")"


@dataclass(frozen=True)
class Else(Garde):
    """Branche residuelle {% else %} : vraie par defaut, jamais un atome."""

    def cle(self) -> str:
        return "else"


# Sentinelle unique de la branche else.
ELSE = Else()


# --------------------------------------------------------- issues / structure

@dataclass(frozen=True)
class Liaison:
    """Liaison locale {% set <variable> = states('<source>') %}."""

    variable: str
    source_entite: str


@dataclass(frozen=True)
class Emission:
    """Feuille : jeton de raison emis."""

    jeton: str


@dataclass(frozen=True)
class SousCascade:
    """Cascade imbriquee (cas Vacances / Presence du runtime reel)."""

    branches: Tuple["Branche", ...]


Issue = Union[Emission, SousCascade]


@dataclass(frozen=True)
class Branche:
    """Une branche : garde canonique, liaisons locales eventuelles, issue."""

    garde: Garde
    liaisons: Tuple[Liaison, ...]
    issue: Issue


@dataclass(frozen=True)
class Provenance:
    """Tracabilite : fichier source, cle de cascade, empreinte du scalaire brut."""

    fichier: str
    cle: str
    empreinte: str


@dataclass(frozen=True)
class CascadeNormalisee:
    """Cascade de tete : provenance + liste ordonnee de branches."""

    provenance: Provenance
    branches: Tuple[Branche, ...]

    def signature_structurelle(self):
        """Representation canonique deterministe, HORS provenance.

        Deux cascades sont structurellement egales ssi leurs signatures le
        sont. L'ordre des branches est preserve (porteur de la pathologie) ;
        il n'est jamais trie. Ce n'est PAS R-MIRROR-1 : c'est une capacite du
        modele, consommee par les tests de determinisme et le constat
        d'egalite cerveau <-> miroir.
        """
        return tuple(_signature_branche(b) for b in self.branches)


def _signature_branche(b: Branche):
    liaisons = tuple(sorted((l.variable, l.source_entite) for l in b.liaisons))
    if isinstance(b.issue, Emission):
        issue = ("emit", b.issue.jeton)
    else:
        issue = ("sub", tuple(_signature_branche(x) for x in b.issue.branches))
    return (b.garde.cle(), liaisons, issue)