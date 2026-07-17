"""Oracle contractuel — ECS `sensor.ecs_consigne_chaudiere_securisee`.

Modèle comportemental **indépendant**, dérivé des invariants du contrat
``contrats/ecs/sensor_ecs_consigne_chaudiere_securisee.md`` :

- **I-SEC-CONS-1** : aucune valeur source valide antérieure (ni restauration
  contractualisée) ⇒ état inconnu ; aucune sentinelle numérique.
- **I-SEC-CONS-2** : aucun fallback numérique fabriqué.
- **I-SEC-CONS-3** : toute valeur retenue est explicitement identifiée
  (``provenance == "retenue"``) ; hold-last-valid sans attribut interdit.
- **I-SEC-CONS-4** : une nouvelle valeur source valide restaure ``provenance ==
  "source"``.
- **I-SEC-CONS-5** : une consigne ``indisponible`` n'est jamais convertie en valeur
  numérique exploitable (sémantique de la donnée — appliquée côté consommateurs).

Vocabulaire de provenance propre au **setpoint** : ``source`` (et non ``mesure``,
qui vaudrait pour une température mesurée). Ce module n'est PAS une transcription
du Jinja : il exprime la classification contractuelle à partir d'entrées
abstraites. Ce n'est pas une exécution du moteur de templates Home Assistant : la
preuve associée est **contractuelle et structurelle**, pas un rendu Jinja réel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from arsenal_ci.behavior.temperature_ballon_securisee import est_numerique

#: Ensemble fermé et exhaustif des provenances admissibles (jamais ``mesure``,
#: chaîne vide, ``None`` ou quatrième valeur — I-SEC-CONS-3).
PROVENANCES = ("source", "retenue", "indisponible")

#: Sentinelle d'état « donnée absente » (jamais un nombre — I-SEC-CONS-1/2).
ETAT_INCONNU = "unknown"

#: Provenances restaurées autorisant la rétention d'un état numérique. Une
#: provenance absente/vide/invalide/``mesure`` (mauvais vocabulaire) n'est jamais
#: retenable ⇒ rejette structurellement tout état historique sans provenance.
_PROVENANCES_RETENABLES = ("source", "retenue")


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
    """Classifie la donnée selon le contrat, indépendamment du Jinja runtime."""
    # I-SEC-CONS-4 / §4.2 : source valide -> valeur source, provenance nominale.
    if source_valide:
        if not est_numerique(source_valeur):
            raise ValueError("source_valide=True impose une source_valeur numérique")
        return Resultat(etat=float(source_valeur), provenance="source")

    # Restauration contractualisée (§6) : numérique ET provenance ∈ {source, retenue}.
    # Toute ancienne valeur numérique sans provenance (ou provenance invalide, ou
    # 'mesure' — vocabulaire du capteur température) est rejetée.
    restauration_contractualisee = (
        est_numerique(etat_restaure)
        and provenance_restauree in _PROVENANCES_RETENABLES
    )

    if restauration_contractualisee:
        # I-SEC-CONS-3 / §4.3 : valeur retenue, explicitement identifiée.
        return Resultat(etat=float(etat_restaure), provenance="retenue")

    # I-SEC-CONS-1 / §4.1 : rien de contractualisé -> inconnu. I-SEC-CONS-2 : pas de fabrication.
    return Resultat(etat=ETAT_INCONNU, provenance="indisponible")
