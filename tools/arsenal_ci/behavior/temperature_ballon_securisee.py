"""Oracle contractuel — ECS `sensor.ecs_temperature_ballon_securisee`.

Modèle comportemental **indépendant**, dérivé des invariants opposables du contrat
propriétaire ``contrats/ecs/sensor_ecs_temperature_ballon_securisee.md`` :

- **I-SEC-1** : aucune mesure valide antérieure (ni restauration contractualisée)
  ⇒ état inconnu ; aucune sentinelle numérique.
- **I-SEC-2** : aucun fallback numérique artificiel (ni ``float(0)``/``int(0)``,
  ni valeur par défaut fabriquée).
- **I-SEC-3** : toute valeur retenue est explicitement identifiée
  (``provenance == "retenue"``) et n'est jamais présentée comme fraîche.
- **I-SEC-4** : une nouvelle mesure valide restaure immédiatement l'état nominal
  (``provenance == "mesure"``).
- **I-SEC-5** : une température inconnue ne constitue jamais une autorisation
  thermique (sémantique de la donnée — appliquée côté consommateurs).

Ce module n'est PAS une transcription du Jinja : il exprime la **classification
contractuelle** de la donnée à partir d'entrées abstraites (validité et valeur de
la source, état et provenance restaurés) et en dérive l'état + la provenance.

Ce n'est pas une exécution du moteur de templates Home Assistant : la preuve
associée est **contractuelle et structurelle**, pas un rendu Jinja réel.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Any

#: Ensemble fermé et exhaustif des provenances admissibles (aucune autre valeur,
#: chaîne vide ou ``None`` n'est publiable — I-SEC-3).
PROVENANCES = ("mesure", "retenue", "indisponible")

#: Sentinelle d'état « donnée absente ». Le porteur HA reste disponible ; c'est la
#: DONNÉE qui est inconnue (jamais un nombre — I-SEC-1/I-SEC-2).
ETAT_INCONNU = "unknown"

#: Provenances d'un état restauré autorisant sa rétention. Une provenance absente,
#: vide, inconnue ou ``indisponible`` n'est jamais retenable — ce qui rejette
#: structurellement tout ``0.0`` historique (produit sans provenance).
_PROVENANCES_RETENABLES = ("mesure", "retenue")


def est_numerique(valeur: Any) -> bool:
    """Vraie mesure numérique réelle — jamais un booléen, ``None`` ou un sentinel.

    Accepte les entiers/réels et les chaînes convertibles ; rejette
    ``unknown``/``unavailable``/``none``/``""``/``None``/booléens.
    """
    if isinstance(valeur, bool):
        return False
    if isinstance(valeur, Real):
        return True
    if isinstance(valeur, str):
        jeton = valeur.strip().lower()
        if jeton in ("", "unknown", "unavailable", "none"):
            return False
        try:
            float(valeur)
        except (TypeError, ValueError):
            return False
        return True
    return False


@dataclass(frozen=True)
class Resultat:
    """Sortie de l'oracle : état publié + provenance (∈ ``PROVENANCES``)."""

    etat: Any
    provenance: str


def evaluer(
    *,
    source_valide: bool,
    source_valeur: Any = None,
    etat_restaure: Any = None,
    provenance_restauree: Any = None,
) -> Resultat:
    """Classifie la donnée selon le contrat, indépendamment du Jinja runtime.

    Entrées abstraites :
      - ``source_valide`` : la source canonique est-elle actuellement numérique ?
      - ``source_valeur`` : sa valeur si valide ;
      - ``etat_restaure`` : dernier état publié restauré (nombre / ``unknown`` /
        ``unavailable`` / ``None``) ;
      - ``provenance_restauree`` : provenance restaurée (ou ``None`` si le porteur
        historique n'en portait pas).
    """
    # I-SEC-4 / §4.2 : une source valide est publiée telle quelle, provenance nominale.
    if source_valide:
        if not est_numerique(source_valeur):
            raise ValueError("source_valide=True impose une source_valeur numérique")
        return Resultat(etat=float(source_valeur), provenance="mesure")

    # Restauration contractualisée (règle validée du contrat §6) : la valeur
    # restaurée n'est retenue que si elle est numérique ET porte une provenance
    # réellement issue d'une mesure. Tout le reste — provenance absente/invalide,
    # ancien unknown/unavailable, ancien 0.0 sans provenance — est rejeté.
    restauration_contractualisee = (
        est_numerique(etat_restaure)
        and provenance_restauree in _PROVENANCES_RETENABLES
    )

    if restauration_contractualisee:
        # I-SEC-3 / §4.3 : valeur retenue, explicitement distincte d'une mesure fraîche.
        return Resultat(etat=float(etat_restaure), provenance="retenue")

    # I-SEC-1 / §4.1 : rien de contractualisé ⇒ inconnu. I-SEC-2 : aucune fabrication.
    return Resultat(etat=ETAT_INCONNU, provenance="indisponible")
